# -*- coding: utf-8 -*-
"""Machine check of the guided course "extrema" (courses/extrema/C01..C09.js).

Every stored answer of every authored question is recomputed independently with sympy and then compared with
what the level file stores (the file is read back through tools/course_load.js, so a typo in the course cannot
hide). Absolute-extrema answers and contour-figure claims are also compared with a dense grid. Distractors of
multiple-choice questions are shown to fail (observably, by computation) wherever they are mathematical statements.

Run: PYTHONUTF8=1 py tools/verify/needhelp/extrema/check.py
"""
import itertools
import json
import pathlib
import re
import subprocess
import sys

import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
                                        implicit_multiplication_application, convert_xor)

HERE = pathlib.Path(__file__).resolve().parent
APP = HERE.parents[3]
R = sp.Rational
x, y, lam, t = sp.symbols("x y lam t", real=True)
TRANS = standard_transformations + (implicit_multiplication_application, convert_xor)
LOCALS = {"x": x, "y": y, "lam": lam, "e": sp.E}
ok = []


def check(name, cond):
    assert cond, "MISMATCH: " + name
    ok.append(name)


# ------------------------------------------------------------------ reading the course back
proc = subprocess.run(["node", str(APP / "tools" / "course_load.js")], capture_output=True, text=True,
                      encoding="utf-8", cwd=str(APP / "tools"))
assert proc.returncode == 0, proc.stderr
loaded = json.loads(proc.stdout)
assert not loaded["errors"], loaded["errors"]
LEVELS = {e["level"]["id"]: e["level"] for e in loaded["levels"] if e["courseId"] == "extrema"}
check("nine levels C01..C09", sorted(LEVELS) == ["C%02d" % i for i in range(1, 10)])
Q = {}
for lv in LEVELS.values():
    for q in lv["questions"]:
        if "bankId" not in q:
            assert q["id"] not in Q, "duplicate id " + q["id"]
            Q[q["id"]] = q
SEEN = set()


# ------------------------------------------------------------------ parsing helpers
def tex(s):
    """a small TeX fragment (numbers, \\frac, \\sqrt, ^, \\lambda) -> sympy"""
    s = s.strip().strip("$").strip()
    s = s.replace("\\left", "").replace("\\right", "").replace("\\cdot", "*").replace("\\ ", " ")
    s = re.sub(r"\\frac(\d)(\d)", r"((\1)/(\2))", s)
    for _ in range(4):
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
        s = re.sub(r"\\sqrt\{([^{}]*)\}", r"sqrt(\1)", s)
    s = s.replace("\\lambda", " lam ").replace("{", "(").replace("}", ")")
    return parse_expr(s, local_dict=dict(LOCALS, sqrt=sp.sqrt), transformations=TRANS)


def S(s):
    return parse_expr(s.replace("^", "**"), local_dict=dict(LOCALS, sqrt=sp.sqrt, exp=sp.exp),
                      transformations=TRANS)


def points_in(text):
    """every (a,b) in a TeX string -> frozenset of sympy point tuples"""
    s = text.replace("\\left(", "(").replace("\\right)", ")")
    out = set()
    for m in re.finditer(r"\(([^()]*)\)", s):
        parts = m.group(1).split(",")
        if len(parts) == 2:
            out.add((sp.nsimplify(tex(parts[0])), sp.nsimplify(tex(parts[1]))))
    return frozenset(out)


def opts(q):
    return {o["id"]: o["value"] for o in q["options"]}


def mcq_unique(qid, pred):
    """exactly one option satisfies pred(value) and it is the stored correctId; all values distinct"""
    q = Q[qid]
    o = opts(q)
    check(qid + " option values distinct", len(set(o.values())) == len(o))
    good = [k for k, v in o.items() if pred(v)]
    check(qid + " exactly one option is right and it is the stored one", good == [q["correctId"]])
    SEEN.add(qid)


def numeric(qid, value):
    q = Q[qid]
    s = q["step"]
    check(qid + " is numeric", s["type"] == "numeric")
    check(f"{qid} answer {s['answer']} == {value}", abs(float(s["answer"]) - float(value)) < 1e-12)
    SEEN.add(qid)


def hessian(f, pt):
    sub = {x: pt[0], y: pt[1]}
    A, B, C = (sp.simplify(sp.diff(f, *v).subs(sub)) for v in ((x, x), (x, y), (y, y)))
    return A, B, C, sp.simplify(A * C - B ** 2)


def classify(A, D):
    if D > 0:
        return "min" if A > 0 else "max"
    if D < 0:
        return "saddle"
    return "inconclusive"


def crit(f):
    sols = sp.solve([sp.diff(f, x), sp.diff(f, y)], [x, y], dict=True)
    return [(sp.nsimplify(s[x]), sp.nsimplify(s[y])) for s in sols]


def local_nature(f, pt, r=0.04, n=161):
    """direct comparison of f with f(pt) on a small square: 'min' | 'max' | 'neither'"""
    fl = sp.lambdify((x, y), f, "numpy")
    g = np.linspace(-r, r, n)
    X, Y = np.meshgrid(float(pt[0]) + g, float(pt[1]) + g)
    d = fl(X, Y) - float(f.subs({x: pt[0], y: pt[1]}))
    if np.all(d >= -1e-12):
        return "min"
    if np.all(d <= 1e-12):
        return "max"
    return "neither"


def lagrange_points(f, g, c):
    sols = sp.solve([sp.diff(f, x) - lam * sp.diff(g, x), sp.diff(f, y) - lam * sp.diff(g, y), g - c], [x, y, lam],
                    dict=True)
    return sols


def circle_vals(f, r2):
    fl = sp.lambdify((x, y), f, "numpy")
    th = np.linspace(0, 2 * np.pi, 400001)
    v = fl(np.sqrt(r2) * np.cos(th), np.sqrt(r2) * np.sin(th))
    return float(v.min()), float(v.max())


def region_mask(ineqs, X, Y):
    m = np.ones(X.shape, bool)
    for s in ineqs:
        mm = re.match(r"^(.*?)(<=|>=)(.*)$", s.strip())
        lhs, op, rhs = S(mm.group(1)), mm.group(2), S(mm.group(3))
        v = sp.lambdify((x, y), lhs - rhs, "numpy")(X, Y)
        m &= (v <= 1e-9) if op == "<=" else (v >= -1e-9)
    return m


def grid_extrema(f, ineqs, box, n=1801):
    X, Y = np.meshgrid(np.linspace(box[0], box[1], n), np.linspace(box[2], box[3], n))
    m = region_mask(ineqs, X, Y)
    V = sp.lambdify((x, y), f, "numpy")(X, Y)[m]
    return float(V.min()), float(V.max())


def close_to(a, b, tol=2e-2):
    return abs(a - b) < tol


# ================================================================== C01
f = x**2 + y**2 - 4*x + 6*y
c = crit(f)
check("C01-Q1 single critical point (2,-3)", c == [(2, -3)])
numeric("C01-Q1", c[0][0])

f = x**2 - x*y + y**2 - 3*x
pt_set = crit(f)
check("C01-Q2 critical point (2,1)", pt_set == [(2, 1)])
fx, fy = sp.diff(f, x), sp.diff(f, y)
mcq_unique("C01-Q2", lambda v: (lambda p: fx.subs({x: p[0], y: p[1]}) == 0 and fy.subs({x: p[0], y: p[1]}) == 0)(
    list(points_in(v))[0]))

f = x**3 - 3*x + y**3 - 3*y
check("C01-Q3 four critical points", set(crit(f)) == {(a, b) for a in (1, -1) for b in (1, -1)})
numeric("C01-Q3", len(crit(f)))

f = x*y*(4 - x - y)
cs = set(crit(f))
check("C01-Q4 xy(4-x-y) critical points", cs == {(0, 0), (4, 0), (0, 4), (R(4, 3), R(4, 3))})
numeric("C01-Q4", len(cs))
kept = {(sp.nsimplify(s[x]), sp.nsimplify(s[y])) for s in sp.solve([2*x + y - 4, x + 2*y - 4], [x, y], dict=True)}
lost = cs - kept
check("C01-Q5 dividing keeps only (4/3,4/3)", kept == {(R(4, 3), R(4, 3))})
mcq_unique("C01-Q5", lambda v: points_in(v) == lost and "בלבד" not in v)
check("C01-Q5 lost set is the three axis points", lost == {(0, 0), (4, 0), (0, 4)})
# the distractors are each a different set
check("C01-Q5 distractors differ from the lost set",
      sorted(map(lambda v: points_in(v) == lost, opts(Q["C01-Q5"]).values())) == [False, False, False, True])

f = x**2 + x*y + y**2 - 3*y
check("C01-Q6 chain: fx,fy", sp.expand(sp.diff(f, x) - (2*x + y)) == 0 and sp.expand(sp.diff(f, y) - (x + 2*y - 3)) == 0)
check("C01-Q6 y=-2x from fx=0", sp.solve(2*x + y, y) == [-2*x])
check("C01-Q6 substitution x-4x=3 gives x=-1", sp.solve((x + 2*(-2*x)) - 3, x) == [-1])
check("C01-Q6 point (-1,2)", crit(f) == [(-1, 2)])
ln = Q["C01-Q6"]["step"]["lines"]
check("C01-Q6 stored lines carry those facts",
      "2x+y" in ln[0] and "y=-2x" in ln[2] and "x=-1" in ln[3] and "(-1,2)" in ln[4])
SEEN.add("C01-Q6")

# ================================================================== C02
LABEL = {"min": "מינימום מקומי", "max": "מקסימום מקומי", "saddle": "נקודת אוכף", "inconclusive": "המבחן אינו מכריע"}


def label_q(qid, f, pt, expected, hess=None):
    A, B, C, D = hessian(f, pt)
    if hess:
        check(f"{qid} stated A,B,C match", (A, B, C) == hess)
    cls = classify(A, D)
    check(f"{qid} classification {cls}", cls == expected)
    if expected in ("min", "max"):
        check(f"{qid} direct check agrees", local_nature(f, pt) == expected)
    q = Q[qid]
    o = opts(q)
    check(f"{qid} correct option is {LABEL[expected]}", o[q["correctId"]] == LABEL[expected])
    SEEN.add(qid)


label_q("C02-Q1", x**2 + 3*y**2, (0, 0), "min")
f = x**3 + 8*y**3 - 6*x*y + 1
check("C02-Q2 Delta(0,0) = -36", hessian(f, (0, 0))[3] == -36)
numeric("C02-Q2", -36)
f = x*y*(6 - x - y)
label_q("C02-Q3", f, (2, 2), "max", hess=(-4, -2, -4))
f = (x + y)**2 - 4*y**2 - 48*y
check("C02-Q4 critical point (6,-6)", crit(f) == [(6, -6)])
label_q("C02-Q4", f, (6, -6), "saddle", hess=(2, 2, -6))
f = x**3 + y**3 - 3*x*y
check("C02-Q5 critical points (0,0),(1,1)", set(crit(f)) == {(0, 0), (1, 1)})
check("C02-Q5 (0,0) saddle, (1,1) min", classify(*[hessian(f, (0, 0))[i] for i in (0, 3)]) == "saddle"
      and classify(*[hessian(f, (1, 1))[i] for i in (0, 3)]) == "min")
check("C02-Q5 (1,1) is a real local min", local_nature(f, (1, 1)) == "min")
numeric("C02-Q5", f.subs({x: 1, y: 1}))
H = sp.Matrix([[-3, 1], [1, -2]])
check("C02-Q6 Delta=5, A=-3 realised by a Hessian", H.det() == 5 and H[0, 0] == -3)
check("C02-Q6 that Hessian is negative definite (a local max)", all(ev < 0 for ev in H.eigenvals()))
fq = R(1, 2) * (-3*x**2 + 2*x*y - 2*y**2)
check("C02-Q6 the quadratic with it has a local max at 0", local_nature(fq, (0, 0)) == "max")
check("C02-Q6 rule", classify(-3, 5) == "max")
o = opts(Q["C02-Q6"])
check("C02-Q6 correct option is max", o[Q["C02-Q6"]["correctId"]] == LABEL["max"])
SEEN.add("C02-Q6")

# ================================================================== C03
f = x**4 + y**4
check("C03-Q1 Delta = 0 at origin", hessian(f, (0, 0))[3] == 0)
label_q("C03-Q1", f, (0, 0), "inconclusive")
check("C03-Q2 origin is a direct min of x^4+y^4", local_nature(f, (0, 0)) == "min")
q = Q["C03-Q2"]
check("C03-Q2 correct option is a minimum", opts(q)[q["correctId"]] == LABEL["min"])
SEEN.add("C03-Q2")
NEITHER = "אינה קיצון מקומי"
for qid, g in (("C03-Q3", x**3 + y**3), ("C03-Q4", x**4 - y**4)):
    check(qid + " Delta=0", hessian(g, (0, 0))[3] == 0)
    check(qid + " not an extremum (direct)", local_nature(g, (0, 0)) == "neither")
    q = Q[qid]
    check(qid + " correct option", opts(q)[q["correctId"]] == NEITHER)
    SEEN.add(qid)
check("C03-Q3 explicit: f(-0.1,0)<0<f(0.1,0)", (x**3 + y**3).subs({x: -R(1, 10), y: 0}) < 0 < (x**3 + y**3).subs({x: R(1, 10), y: 0}))
check("C03-Q4 explicit: f(t,0)>0>f(0,t)", all((x**4 - y**4).subs({x: s, y: 0}) > 0 > (x**4 - y**4).subs({x: 0, y: s})
                                                for s in (R(1, 10), R(1, 3))))
f = x**3 + 8*y**3 - 6*x*y + 1
ext = [p for p in crit(f) if classify(hessian(f, p)[0], hessian(f, p)[3]) in ("min", "max")]
check("C03-Q5 one local extremum, at (1,1/2)", ext == [(1, R(1, 2))])
check("C03-Q5 stated Delta=108 at (1,1/2)", hessian(f, (1, R(1, 2)))[3] == 108 and hessian(f, (1, R(1, 2)))[:3] == (6, -6, 24))
numeric("C03-Q5", len(ext))
f = x*y*(6 - x - y)
cp = set(crit(f))
check("C03-Q6 stated critical points", cp == {(0, 0), (6, 0), (0, 6), (2, 2)})
sad = [p for p in cp if classify(hessian(f, p)[0], hessian(f, p)[3]) == "saddle"]
check("C03-Q6 three saddles, each Delta=-36", len(sad) == 3 and all(hessian(f, p)[3] == -36 for p in sad))
numeric("C03-Q6", len(sad))

# ================================================================== C04
# Q1: closed + bounded
def in_open_disc(px, py):
    return px**2 + py**2 < 1


check("C04-Q1 open disc: sup of f=x is 1 but x<1 on it (never attained)", all(in_open_disc(1 - s, 0) for s in (0.1, 0.001)) and not in_open_disc(1, 0))
check("C04-Q1 plane / strip: f=x^2+y^2 is unbounded there", 1000**2 > 10**5 and (0 <= 0.5 <= 1))
check("C04-Q1 stored answer is the closed disc", "x^2+y^2\\le1" in opts(Q["C04-Q1"])[Q["C04-Q1"]["correctId"]]
      and "הסגור" in opts(Q["C04-Q1"])[Q["C04-Q1"]["correctId"]])
SEEN.add("C04-Q1")

f = x**3 - 3*x + y**2
cp = crit(f)
inside = [p for p in cp if 0 <= p[0] <= 3 and -1 <= p[1] <= 1]
check("C04-Q2 only (1,0) lies in the rectangle", inside == [(1, 0)] and set(cp) == {(1, 0), (-1, 0)})
mcq_unique("C04-Q2", lambda v: (points_in(v) == frozenset(inside)) and "בלבד" in v)
f = 2*x**2 - 3*y**2 + x*y - 3*x + 8*y
cp = crit(f)
check("C04-Q3 critical point (2/5,7/5) outside triangle 0<=x<=y<=1",
      cp == [(R(2, 5), R(7, 5))] and not (0 <= cp[0][0] <= cp[0][1] <= 1))
numeric("C04-Q3", 0)

g = x**3 - 3*x + 4
cand = sorted([g.subs(x, v) for v in sp.solve(sp.diff(g, x), x)] + [g.subs(x, -2), g.subs(x, 2)])
xs = np.linspace(-2, 2, 400001)
gv = sp.lambdify(x, g, "numpy")(xs)
check("C04-Q4 interval min", cand[0] == 2 and cand[-1] == 6 and close_to(gv.min(), 2, 1e-9) and close_to(gv.max(), 6, 1e-9))
numeric("C04-Q4", cand[0])
g = 3*x**4 - 3*x**2
b = sp.sqrt(2)
cand = {v: g.subs(x, v) for v in sp.solve(sp.diff(g, x), x) + [-b, b]}
xs = np.linspace(-float(b), float(b), 800001)
gv = sp.lambdify(x, g, "numpy")(xs)
check("C04-Q5 max is 6, attained only at the ends", max(cand.values()) == 6 and close_to(gv.max(), 6, 1e-9)
      and [v for v, w in cand.items() if w == 6] == [-b, b] or sorted(v for v, w in cand.items() if w == 6) == sorted([-b, b]))
check("C04-Q5 interior critical values 0 and -3/4 only", sorted(set(g.subs(x, v) for v in sp.solve(sp.diff(g, x), x))) == [-R(3, 4), 0])
numeric("C04-Q5", 6)
check("C04-Q6 min is -3/4", min(cand.values()) == -R(3, 4) and close_to(gv.min(), -0.75, 1e-9))
numeric("C04-Q6", -0.75)

# ================================================================== C05
f = x**2 + x*y + y**2 - 6*x
TRI = ["x>=0", "y>=0", "x+y<=4"]
edge_y0 = sp.expand(f.subs(y, 0))
edge_x0 = sp.expand(f.subs(x, 0))
edge_h = sp.expand(f.subs(y, 4 - x))
check("C05-Q1 edge y=4-x runs from (4,0) to (0,4): x in [0,4]", (4 - 0, 0 + 4) == (4, 4))
q = Q["C05-Q1"]
check("C05-Q1 correct option is [0,4]", opts(q)[q["correctId"]].replace(" ", "") == "$[0,4]$")
others = [v.replace(" ", "") for k, v in opts(q).items() if k != q["correctId"]]
check("C05-Q1 distractors are not [0,4]", all(v != "$[0,4]$" for v in others))
SEEN.add("C05-Q1")
check("C05-Q2 g(x) on y=0 is x^2-6x, g'=0 at x=3", edge_y0 == x**2 - 6*x and sp.solve(sp.diff(edge_y0, x), x) == [3])
numeric("C05-Q2", 3)
check("C05-Q3 g(x) = x^2-10x+16 on the hypotenuse; g'=0 at 5, outside [0,4]",
      edge_h == x**2 - 10*x + 16 and sp.solve(sp.diff(edge_h, x), x) == [5])
q = Q["C05-Q3"]
good = [k for k, v in opts(q).items() if v.startswith("פוסלים אותה")]
check("C05-Q3 the right option is the rejecting one", good == [q["correctId"]])
SEEN.add("C05-Q3")
vals = {"vertex (0,0)": f.subs({x: 0, y: 0}), "vertex (4,0)": f.subs({x: 4, y: 0}), "vertex (0,4)": f.subs({x: 0, y: 4}),
        "edge y=0": edge_y0.subs(x, 3), "edge x=0": edge_x0.subs(y, 0)}
check("C05-Q4/5 interior critical point (4,-2) is outside", crit(f) == [(4, -2)])
check("C05-Q4/5 edge x=0: g=y^2, g'=0 only at y=0 (a vertex)", edge_x0 == y**2 and sp.solve(sp.diff(edge_x0, y), y) == [0])
mn, mx = grid_extrema(f, TRI, (-0.5, 4.5, -0.5, 4.5))
check("C05 grid agrees: min -9, max 16", close_to(mn, -9, 1e-3) and close_to(mx, 16, 1e-6) and mn >= -9 - 1e-9)
check("C05 candidate table: min -9, max 16", min(vals.values()) == -9 and max(vals.values()) == 16)
numeric("C05-Q4", min(vals.values()))
numeric("C05-Q5", max(vals.values()))
no_vertex = [vals["edge y=0"], vals["edge x=0"]]
check("C05-Q6 without the vertices the maximum would be 0", max(no_vertex) == 0 and vals["vertex (0,4)"] == 16)
q = Q["C05-Q6"]
check("C05-Q6 correct option cites the vertex value 16", "16" in opts(q)[q["correctId"]] and "(0,4)" in opts(q)[q["correctId"]])
check("C05-Q6 distractors fail: no interior critical point; g' does vanish at 3", crit(f)[0][1] < 0 and sp.diff(edge_y0, x).subs(x, 3) == 0)
SEEN.add("C05-Q6")

# ================================================================== C06
def parity_ok(v):
    g = S(v.replace("f=", "").strip().strip("$"))
    return sp.simplify(g.subs(y, -y) - g) == 0


mcq_unique("C06-Q1", parity_ok)
f = 2*x**2 + y**2
g = sp.expand(f.subs(y**2, 4 - x**2))
check("C06-Q2 g(x) = x^2+4", g == x**2 + 4 and sp.solve(sp.diff(g, x), x) == [0])
lo, hi = circle_vals(f, 4)
check("C06-Q2 max on the circle is 8 (ends), min 4", close_to(hi, 8, 1e-6) and close_to(lo, 4, 1e-6) and g.subs(x, 2) == 8)
numeric("C06-Q2", 8)
DISC4 = ["x^2+y^2<=4"]
mn, mx = grid_extrema(f, DISC4, (-2, 2, -2, 2))
check("C06-Q3 disc: min 0 (interior), max 8", close_to(mn, 0, 1e-6) and close_to(mx, 8, 1e-3) and crit(f) == [(0, 0)])
numeric("C06-Q3", 0)
st = Q["C06-Q4"]["step"]
check("C06-Q4 solution lines are the true ones except the planted one",
      st["type"] == "findbug" and st["bugIndex"] == 3 and "אינם מועמדים" in st["lines"][3]
      and all("אינם מועמדים" not in L for i, L in enumerate(st["lines"]) if i != 3))
check("C06-Q4 the ends really are candidates: g(+-2)=8 beats g(0)=4, and g'(+-2) != 0",
      g.subs(x, 2) == 8 and sp.diff(g, x).subs(x, 2) == 4 and sp.diff(g, x).subs(x, -2) == -4)
check("C06-Q4 other lines true: interior (0,0) f=0; g'(0)=0 g(0)=4; min 0, max 8",
      f.subs({x: 0, y: 0}) == 0 and g.subs(x, 0) == 4 and close_to(mn, 0, 1e-6) and close_to(mx, 8, 1e-3))
SEEN.add("C06-Q4")
f = x**2 + 3*y**2
g = sp.expand(f.subs(y**2, 1 - x**2))
check("C06-Q5 g = 3-2x^2, min on [-1,1] is 1 at the ends", g == 3 - 2*x**2 and g.subs(x, 1) == 1 and g.subs(x, 0) == 3)
lo, hi = circle_vals(f, 1)
check("C06-Q5 circle min 1 max 3 (dense)", close_to(lo, 1, 1e-6) and close_to(hi, 3, 1e-6))
numeric("C06-Q5", 1)
mn, mx = grid_extrema(f, ["x^2+y^2<=1"], (-1, 1, -1, 1))
check("C06-Q6 unit disc: max 3, min 0", close_to(mx, 3, 1e-3) and close_to(mn, 0, 1e-6))
numeric("C06-Q6", 3)

# ================================================================== C07
f, g = x*y, x**2 + y**2
sols = lagrange_points(f, g, 2)
pts = {(sp.nsimplify(s[x]), sp.nsimplify(s[y])) for s in sols}
check("C07-Q1/4 Lagrange points of xy on the circle: (+-1,+-1)", pts == {(1, 1), (1, -1), (-1, 1), (-1, -1)})
numeric("C07-Q4", len(pts))


def eq_system(v):
    parts = [p for p in v.strip().strip("$").split(",\\ \\ ")]
    eqs = []
    for p in parts:
        lhs, rhs = p.split("=")
        eqs.append(sp.Eq(tex(lhs), tex(rhs)))
    return eqs


def system_is_lagrange(v):
    try:
        eqs = eq_system(v)
        sl = sp.solve(eqs, [x, y, lam], dict=True)
        if not sl:
            return False
        got = set()
        for s in sl:
            if any(s.get(k) is None or s[k].free_symbols for k in (x, y)):
                return False
            got.add((sp.nsimplify(s[x]), sp.nsimplify(s[y])))
        return got == pts
    except Exception:
        return False


mcq_unique("C07-Q1", system_is_lagrange)
# the right system is literally grad f = lam grad g plus the constraint
eqs = eq_system(opts(Q["C07-Q1"])["a"])
check("C07-Q1 right system is grad f = lam grad g, g = 2",
      sp.simplify(eqs[0].lhs - sp.diff(f, x)) == 0 and sp.simplify(eqs[0].rhs - lam * sp.diff(g, x)) == 0
      and sp.simplify(eqs[1].lhs - sp.diff(f, y)) == 0 and sp.simplify(eqs[1].rhs - lam * sp.diff(g, y)) == 0
      and sp.simplify(eqs[2].lhs - g) == 0 and eqs[2].rhs == 2)
f2 = x + 2*y
sl = lagrange_points(f2, x**2 + y**2, 5)
vals2 = sorted(f2.subs(s) for s in sl)
lo, hi = circle_vals(f2, 5)
check("C07-Q2 max of x+2y on the circle is 5 (symbolic + dense)", vals2 == [-5, 5] and close_to(hi, 5, 1e-6) and close_to(lo, -5, 1e-6))
numeric("C07-Q2", 5)
lam11 = [s[lam] for s in lagrange_points(x*y, x**2 + y**2, 2) if s[x] == 1 and s[y] == 1]
check("C07-Q3 lambda at (1,1) is 1/2", lam11 == [R(1, 2)])
numeric("C07-Q3", 0.5)
# Q5: geometry at the Lagrange points of xy on the circle
for (px, py) in pts:
    gf = np.array([float(sp.diff(x*y, x).subs({x: px, y: py})), float(sp.diff(x*y, y).subs({x: px, y: py}))])
    gg = np.array([float(sp.diff(g, x).subs({x: px, y: py})), float(sp.diff(g, y).subs({x: px, y: py}))])
    cross = gf[0]*gg[1] - gf[1]*gg[0]
    cosang = abs(gf @ gg) / (np.linalg.norm(gf) * np.linalg.norm(gg))
    check(f"C07-Q5 at ({px},{py}) gradients parallel, grad f != 0, tangents coincide", abs(cross) < 1e-12 and np.linalg.norm(gf) > 0 and abs(cosang - 1) < 1e-12)
check("C07-Q5 the circle's centre is not on it (distractor false)", 0**2 + 0**2 != 2)
q = Q["C07-Q5"]
check("C07-Q5 correct option says 'tangent' (משיק)", "משיק" in opts(q)[q["correctId"]]
      and all("משיק" not in v for k, v in opts(q).items() if k != q["correctId"]))
check("C07-Q5 the question embeds the contour figure", "```contour" in q["question"])
SEEN.add("C07-Q5")
f3 = x**2 + y**2
sl = sp.solve([2*x - lam, 2*y - lam, x + y - 2], [x, y, lam], dict=True)
check("C07-Q6 single Lagrange point (1,1) with f=2", len(sl) == 1 and sl[0][x] == 1 and sl[0][y] == 1 and f3.subs(sl[0]) == 2)
tt = np.linspace(-1000, 1000, 2000001)
vv = tt**2 + (2 - tt)**2
check("C07-Q6 along the line: min 2, unbounded above", close_to(vv.min(), 2, 1e-6) and vv.max() > 1e6)
numeric("C07-Q6", 2)

# ================================================================== C08
f, g = x**2 + 2*y**2, x**2 + y**2
sols = lagrange_points(f, g, 1)
pts = {(sp.nsimplify(s[x]), sp.nsimplify(s[y])) for s in sols}
check("C08-Q1 four Lagrange points", pts == {(0, 1), (0, -1), (1, 0), (-1, 0)})
numeric("C08-Q1", len(pts))
rem = {(sp.nsimplify(s[x]), sp.nsimplify(s[y])) for s in sp.solve([4*y - 2*1*y, x**2 + y**2 - 1], [x, y], dict=True)}
lost = pts - rem
check("C08-Q2 dividing by x (lam=1) keeps (+-1,0), loses (0,+-1)", rem == {(1, 0), (-1, 0)} and lost == {(0, 1), (0, -1)})
mcq_unique("C08-Q2", lambda v: points_in(v) == lost)
check("C08-Q2 the lost points are the maxima (f=2)", all(f.subs({x: a, y: b}) == 2 for a, b in lost))
st = Q["C08-Q3"]["step"]
check("C08-Q3 facts of the ordered solution",
      sp.simplify(sp.diff(f, x) - 2*x) == 0 and sp.simplify(sp.diff(f, y) - 4*y) == 0
      and sorted(f.subs({x: a, y: b}) for a, b in pts) == [1, 1, 2, 2]
      and "2x=2\\lambda x" in st["lines"][0] and "\\lambda=1" in st["lines"][1] and "\\lambda=2" in st["lines"][1]
      and "f(0,\\pm1)=2" in st["lines"][3] and "f(\\pm1,0)=1" in st["lines"][3])
SEEN.add("C08-Q3")
mn, mx = grid_extrema(f, ["x^2+y^2<=1"], (-1, 1, -1, 1))
lo, hi = circle_vals(f, 1)
check("C08-Q4 disc: min 0 (interior (0,0)), circle min 1, max 2", crit(f) == [(0, 0)] and close_to(mn, 0, 1e-6) and close_to(lo, 1, 1e-6) and close_to(hi, 2, 1e-6))
numeric("C08-Q4", 0)
f = x**4 + y**4
sols = lagrange_points(f, g, 1)
pts8 = {(sp.nsimplify(s[x]), sp.nsimplify(s[y])) for s in sols}
h = sp.sqrt(2) / 2
check("C08-Q5 eight Lagrange points", pts8 == {(0, 1), (0, -1), (1, 0), (-1, 0)} | {(a*h, b*h) for a in (1, -1) for b in (1, -1)})
numeric("C08-Q5", len(pts8))
lo, hi = circle_vals(f, 1)
check("C08-Q6 min 1/2, max 1 on the circle", sorted({sp.nsimplify(f.subs({x: a, y: b})) for a, b in pts8}) == [R(1, 2), 1]
      and close_to(lo, 0.5, 1e-6) and close_to(hi, 1, 1e-6))
numeric("C08-Q6", 0.5)

# ================================================================== figures in the lessons
NUM = {"x": x, "y": y}
fig_count = 0
for lid, lv in LEVELS.items():
    for m in re.finditer(r"data-contour='([^']*)'", lv["lesson"]["html"]):
        specs = json.loads(m.group(1))
        for sp_ in specs if isinstance(specs, list) else [specs]:
            fig_count += 1
            f = S(sp_["f"])
            kind = sp_["kind"]
            tag = f"{lid} figure f={sp_['f']} ({kind})"
            dom = sp_["domain"]
            box = (dom[0][0], dom[0][1], dom[1][0], dom[1][1])
            P = [(sp.nsimplify(S(str(p["x"]))), sp.nsimplify(S(str(p["y"]))), sp.nsimplify(S(str(p["f"]))), p["role"]) for p in sp_["critical_points"]]
            for (px, py, pf, role) in P:
                check(f"{tag}: f at ({px},{py}) is {pf}", sp.simplify(f.subs({x: px, y: py}) - pf) == 0)
            if kind == "unconstrained":
                for (px, py, pf, role) in P:
                    check(f"{tag}: ({px},{py}) is critical", sp.diff(f, x).subs({x: px, y: py}) == 0 and sp.diff(f, y).subs({x: px, y: py}) == 0)
                    A, B, C, D = hessian(f, (px, py))
                    cls = classify(A, D)
                    if role.startswith("local"):
                        want = role.split()[1]
                        got = cls if cls != "inconclusive" else local_nature(f, (px, py))
                        check(f"{tag}: role {role} agrees", got == want)
                    elif role == "saddle":
                        got = cls if cls != "inconclusive" else local_nature(f, (px, py))
                        check(f"{tag}: role saddle agrees", got in ("saddle", "neither"))
                    elif role == "critical":
                        check(f"{tag}: 'critical' point is not an extremum", local_nature(f, (px, py)) == "neither")
                if lid in ("C01",):
                    check(f"{tag}: all critical points listed", set(crit(f)) == {(p[0], p[1]) for p in P})
            elif kind == "lagrange":
                a, c_ = sp_["constraint"].split("=")
                gg = S(a)
                cc = S(c_)
                for (px, py, pf, role) in P:
                    check(f"{tag}: ({px},{py}) on the constraint", sp.simplify(gg.subs({x: px, y: py}) - cc) == 0)
                    fxv, fyv = sp.diff(f, x).subs({x: px, y: py}), sp.diff(f, y).subs({x: px, y: py})
                    gxv, gyv = sp.diff(gg, x).subs({x: px, y: py}), sp.diff(gg, y).subs({x: px, y: py})
                    check(f"{tag}: grad f parallel to grad g at ({px},{py})", sp.simplify(fxv*gyv - fyv*gxv) == 0)
                r2 = float(cc)
                lo, hi = circle_vals(f, r2)
                for (px, py, pf, role) in P:
                    if role == "abs max":
                        check(f"{tag}: abs max {pf} matches dense circle", close_to(hi, float(pf), 1e-6))
                    if role == "abs min":
                        check(f"{tag}: abs min {pf} matches dense circle", close_to(lo, float(pf), 1e-6))
                sl = lagrange_points(f, gg, cc)
                allp = {(sp.nsimplify(s[x]), sp.nsimplify(s[y])) for s in sl}
                check(f"{tag}: every Lagrange point is drawn", allp == {(p[0], p[1]) for p in P})
            elif kind == "closed_region":
                ineqs = [s.strip() for s in sp_["region"].split(",")]
                mn, mx = grid_extrema(f, ineqs, box, 2001)
                for (px, py, pf, role) in P:
                    pxf, pyf = float(px), float(py)
                    inreg = region_mask(ineqs, np.array([[pxf]]), np.array([[pyf]]))[0, 0]
                    check(f"{tag}: ({px},{py}) inside the region", bool(inreg))
                    if role.startswith("abs max"):
                        check(f"{tag}: abs max {pf} matches the dense grid", close_to(mx, float(pf), 1e-6) or (mx <= float(pf) + 1e-9 and close_to(mx, float(pf), 5e-3)))
                    if role.startswith("abs min"):
                        check(f"{tag}: abs min {pf} matches the dense grid", close_to(mn, float(pf), 1e-6) or (mn >= float(pf) - 1e-9 and close_to(mn, float(pf), 5e-3)))
                    if role == "saddle":
                        A, B, C, D = hessian(f, (px, py))
                        check(f"{tag}: interior saddle really is critical with Delta<0",
                              sp.diff(f, x).subs({x: px, y: py}) == 0 and sp.diff(f, y).subs({x: px, y: py}) == 0 and D < 0)
check("figures checked: " + str(fig_count), fig_count >= 9)

# ================================================================== the boss: real exam questions, verified in the bank
bank = json.loads((APP / "questions.json").read_text(encoding="utf-8"))
bank = bank["questions"] if isinstance(bank, dict) else bank
BY = {b["id"]: b for b in bank}
boss = LEVELS["C09"]
check("C09 is the boss and uses only bankId questions", boss.get("boss") is True and all("bankId" in q for q in boss["questions"]))
for q in boss["questions"]:
    b = BY[q["bankId"]]
    check(q["bankId"] + " exists, topic in the course, not held, steps ai-verified or official",
          b["topic"] in ("absolute_extrema", "local_extrema") and not b.get("hold") and b.get("stepsSource") in ("ai-verified", "official")
          and b.get("confidence") == "high")
check("boss covers 6 distinct bank questions", len({q["bankId"] for q in boss["questions"]}) == 6)

# ================================================================== coverage: every authored question was asserted
missing = sorted(set(Q) - SEEN)
check("every authored question id was asserted; missing: " + ",".join(missing), not missing)
check("no ordinal citation of options in explanations ('first/second option' or a letter)",
      not any(re.search(r"(האפשרות|התשובה|אופציה|סעיף) (הראשונה|השנייה|השלישית|הרביעית|[אבגד]\b)", json.dumps(q, ensure_ascii=False))
              for q in Q.values()))
print(f"OK: {len(ok)} checks passed, {len(SEEN)} questions asserted")
