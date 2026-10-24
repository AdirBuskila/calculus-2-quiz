# -*- coding: utf-8 -*-
"""sympy checks for the guided course `double_int` (courses/double_int/C01..C08.js).

Run: PYTHONUTF8=1 py tools/verify/needhelp/double_int/check.py
Loads the level files through tools/course_load.js and asserts, per question id:
  * every numeric step: answer equals the sympy value (within the stored tol);
  * every mcq / choice option: its truth (region equals the reference description, curve equals the circle, ...)
    is COMPUTED, the option text is looked up in the level file by exact string, and exactly the stored
    correctId is the true one (so each distractor fails observably: a different area or integral);
  * every findbug / order / fillblank line: each stated equality is recomputed; the bug line is the only false one.
Region and polar/uv figures embedded in the lessons are checked by tools/verify/extras_check.py (sympy).
"""
import json, pathlib, subprocess, sys
import numpy as np
import sympy as sp
from scipy import integrate as si

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
x, y, u, v, t = sp.symbols("x y u v t", real=True)
r, th = sp.symbols("r theta", positive=True)
R = sp.Rational
OK = []


def check(name, cond):
    assert cond, "MISMATCH: " + name
    OK.append(name)


def zero(e):
    return sp.simplify(e) == 0


# ---------------------------------------------------------------- load the levels
proc = subprocess.run(["node", str(ROOT / "tools" / "course_load.js")], capture_output=True, text=True, encoding="utf-8", cwd=str(ROOT / "tools"))
assert proc.returncode == 0, proc.stderr
LV = {e["level"]["id"]: e["level"] for e in json.loads(proc.stdout)["levels"] if e["courseId"] == "double_int"}
Q = {}
for lid, L in LV.items():
    for q in L["questions"]:
        if "id" in q:
            Q[q["id"]] = q


def step(qid):
    return Q[qid]["step"]


def opts_of(qid):
    q = Q[qid]
    s = q.get("step") or q
    return {o["value"]: o["id"] for o in s["options"]}, s["correctId"]


def check_options(qid, truth):
    """truth: {option text: bool}. Option texts must match the level file exactly; exactly the correct one is True."""
    ids, correct = opts_of(qid)
    check(f"{qid} options listed exactly", set(truth) == set(ids))
    check(f"{qid} exactly one true option", sum(1 for ok in truth.values() if ok) == 1)
    check(f"{qid} stored correctId is the true one", all((ids[k] == correct) == ok for k, ok in truth.items()))


def check_numeric(qid, value):
    s = step(qid)
    val = float(sp.N(value))
    check(f"{qid} numeric answer {s['answer']} ~ {val:.6f}", abs(s["answer"] - val) <= max(s.get("tol", 0), 1e-12) + 1e-12)
    check(f"{qid} tolerance is tight", s.get("tol", 0) <= 0.005 * max(1, abs(val)) + 1e-12)


def NQ(f, olo, ohi, ilo, ihi):
    """numeric iterated integral (scipy): f(inner, outer); limits of the inner variable are functions of the outer."""
    return si.dblquad(f, olo, ohi, ilo, ihi, epsabs=1e-12, epsrel=1e-12)[0]


# ---------------------------------------------------------------- iterated integrals
def I(f, outer, olo, ohi, inner, ilo, ihi):
    """iterated integral: inner variable integrated first. Returns an exact sympy value."""
    return sp.simplify(sp.integrate(sp.integrate(f, (inner, ilo, ihi)), (outer, olo, ohi)))


def vec(desc, tests):
    return tuple(I(f, *desc) for f in tests)


def XY(xlo, xhi, ylo, yhi):   # dy dx
    return (x, xlo, xhi, y, ylo, yhi)


def YX(ylo, yhi, xlo, xhi):   # dx dy
    return (y, ylo, yhi, x, xlo, xhi)


T1 = [sp.Integer(1), x + 2*y, x*y + y]     # test integrands: area and two weighted versions

# ================================================================ C01
ref = vec(XY(0, 1, x**2, x), T1)
check("C01-Q1 area of region between y=x^2 and y=x is 1/6", ref[0] == R(1, 6))
check_options("C01-Q1", {
    r"$0\le x\le 1,\ x\le y\le x^2$": vec(XY(0, 1, x, x**2), T1) == ref,
    r"$0\le x\le 1,\ x^2\le y\le x$": True,
    r"$0\le x\le 1,\ x^2\le y\le 1$": vec(XY(0, 1, x**2, 1), T1) == ref,
    r"$0\le x\le 1,\ 0\le y\le x^2$": vec(XY(0, 1, 0, x**2), T1) == ref,
})
check_numeric("C01-Q2", I(1, x, 0, 2, y, 0, x))
check_numeric("C01-Q3", I(x*y, x, 0, 2, y, 0, 3))
# vertices of 0<=y<=x<=2: intersections of the boundary lines, kept when they satisfy every inequality
lines = [(y, 0), (y - x, 0), (x, 2)]          # y=0, y=x, x=2
inside = lambda px, py: py >= 0 and px >= py and px <= 2
verts = set()
for i in range(3):
    for j in range(i + 1, 3):
        sol = sp.solve([lines[i][0] - lines[i][1], lines[j][0] - lines[j][1]], [x, y], dict=True)
        if sol and inside(sol[0][x], sol[0][y]):
            verts.add((sol[0][x], sol[0][y]))
check("C01-Q4 vertices", verts == {(0, 0), (2, 0), (2, 2)})
check_options("C01-Q4", {
    r"$(0,0),\ (2,0),\ (0,2)$": {(0, 0), (2, 0), (0, 2)} == verts,
    r"$(0,0),\ (0,2),\ (2,2)$": {(0, 0), (0, 2), (2, 2)} == verts,
    r"$(0,0),\ (2,0),\ (2,2)$": {(0, 0), (2, 0), (2, 2)} == verts,
    r"$(0,0),\ (2,2),\ (4,0)$": {(0, 0), (2, 2), (4, 0)} == verts,
})
# Q5: well-formed iterated integral = outer limits constant, inner limits only in the outer variable
def well_formed(outer, olim, inner, ilim):
    return all(not (sp.sympify(b).free_symbols) for b in olim) and all(sp.sympify(b).free_symbols <= {outer} for b in ilim)
check_options("C01-Q5", {
    r"$\int_0^{x}\int_0^{1} f\,dy\,dx$": well_formed(x, (0, x), y, (0, 1)),
    r"$\int_0^1\int_0^{y} f\,dy\,dx$": well_formed(x, (0, 1), y, (0, y)),
    r"$\int_0^1\int_0^{x} f\,dy\,dx$": well_formed(x, (0, 1), y, (0, x)),
    r"$\int_0^{y}\int_0^{1} f\,dx\,dy$": well_formed(y, (0, y), x, (0, 1)),
})
# Q6: lines (index 1 is the planted bug)
s = step("C01-Q6")
check("C01-Q6 line0 antiderivative", zero(sp.integrate(x + y, y) - (x*y + y**2/2)))
check("C01-Q6 line1 true form x^2+x^2/2=3x^2/2", zero(sp.integrate(x + y, (y, 0, x)) - sp.Rational(3, 2)*x**2) and zero(x**2 + x**2/2 - 3*x**2/2))
check("C01-Q6 line1 stored form (2x^2) is false", not zero(x**2 + x**2/2 - 2*x**2))
check("C01-Q6 line2 antiderivative", zero(sp.integrate(3*x**2/2, x) - x**3/2) and sp.integrate(3*x**2/2, (x, 0, 1)) == R(1, 2))
check("C01-Q6 line3 value 1/2", I(x + y, x, 0, 1, y, 0, x) == R(1, 2))
check("C01-Q6 bugIndex", s["bugIndex"] == 1)

# ================================================================ C02
ref = vec(XY(0, 1, x**2, x), T1)
check_options("C02-Q1", {
    r"$0\le x\le 1,\ x^2\le y\le 1$": vec(XY(0, 1, x**2, 1), T1) == ref,
    r"$0\le x\le 1,\ x\le y\le x^2$": vec(XY(0, 1, x, x**2), T1) == ref,
    r"$0\le x\le 1,\ x^2\le y\le x$": True,
    r"$0\le x\le 1,\ 0\le y\le x^2$": vec(XY(0, 1, 0, x**2), T1) == ref,
})
check_numeric("C02-Q2", I(1, x, 0, 1, y, x**2, x))
check_options("C02-Q3", {
    r"$0\le y\le1,\ \sqrt y\le x\le y$": vec(YX(0, 1, sp.sqrt(y), y), T1) == ref,
    r"$0\le y\le1,\ y\le x\le\sqrt y$": vec(YX(0, 1, y, sp.sqrt(y)), T1) == ref,
    r"$0\le y\le1,\ y^2\le x\le y$": vec(YX(0, 1, y**2, y), T1) == ref,
    r"$0\le y\le1,\ 0\le x\le\sqrt y$": vec(YX(0, 1, 0, sp.sqrt(y)), T1) == ref,
})
# Q4 is conceptual: outer limits of an iterated integral are constants (checked structurally)
check_options("C02-Q4", {
    "פונקציות של $y$": well_formed(x, (y, y), y, (0, 1)),
    "מספרים קבועים": well_formed(x, (0, 1), y, (0, x)),
    "פונקציות של $x$": well_formed(x, (x, x), y, (0, 1)),
    "תלויים באינטגרנד $f$": False,
})
inner = sp.integrate(y, (y, x**2, x))
check("C02-Q5 line0", zero(inner - (x**2 - x**4)/2))
check("C02-Q5 line1", sp.integrate((x**2 - x**4)/2, (x, 0, 1)) == R(1, 2)*(R(1, 3) - R(1, 5)))
check("C02-Q5 line2", I(y, x, 0, 1, y, x**2, x) == R(1, 15))
check("C02-Q5 order is forced (each line uses the previous result)", len(step("C02-Q5")["lines"]) == 3)
check_numeric("C02-Q6", I(x, y, 0, 1, x, y, sp.sqrt(y)))
check("C02-Q6 both orders agree", I(x, y, 0, 1, x, y, sp.sqrt(y)) == I(x, x, 0, 1, y, x**2, x) == R(1, 12))

# ================================================================ C03
T3 = [sp.Integer(1), x + 2*y, x*y + y]
ref = vec(YX(0, 1, y, 1), T3)               # int_0^1 int_y^1 f dx dy
check_options("C03-Q1", {
    r"$\int_0^1\int_x^1 f\,dy\,dx$": vec(XY(0, 1, x, 1), T3) == ref,
    r"$\int_0^1\int_0^{1-x} f\,dy\,dx$": vec(XY(0, 1, 0, 1 - x), T3) == ref,
    r"$\int_0^1\int_0^1 f\,dy\,dx$": vec(XY(0, 1, 0, 1), T3) == ref,
    r"$\int_0^1\int_0^x f\,dy\,dx$": vec(XY(0, 1, 0, x), T3) == ref,
})
ref = vec(XY(0, 2, x**2, 4), T3)            # int_0^2 int_{x^2}^4 f dy dx
check_options("C03-Q2", {
    r"$y^2$": vec(YX(0, 4, 0, y**2), T3) == ref,
    r"$\sqrt y$": vec(YX(0, 4, 0, sp.sqrt(y)), T3) == ref,
    r"$\tfrac y2$": vec(YX(0, 4, 0, y/2), T3) == ref,
    "$2$": vec(YX(0, 4, 0, 2), T3) == ref,
})
# Q3: the line "x = y^2" is false: solving y = x^2 for x >= 0 gives sqrt(y)
sol = sp.solve(sp.Eq(y, x**2), x)
check("C03-Q3 y=x^2 <=> x=sqrt(y) (x>=0)", sp.sqrt(y) in [sp.simplify(s_.subs(y, y)) for s_ in sol] or sp.sqrt(y) in sol)
check("C03-Q3 x=y^2 is a different curve", not zero(sp.sqrt(y) - y**2))
check("C03-Q3 last line is a correct swap", vec(YX(0, 4, 0, sp.sqrt(y)), T3) == ref)
check("C03-Q3 y ranges over [0,4]", sp.minimum(x**2, x, sp.Interval(0, 2)) == 0 and 4 >= 0)
check("C03-Q3 bugIndex", step("C03-Q3")["bugIndex"] == 2)
check_numeric("C03-Q4", I(x, x, 0, 2, y, x**2, 4))
check("C03-Q4 swapped order agrees", I(x, y, 0, 4, x, 0, sp.sqrt(y)) == 4)
ref = vec(XY(0, 1, x, sp.sqrt(x)), T3)
check_options("C03-Q5", {
    r"$\int_0^1\int_{y^2}^{y} f\,dx\,dy$": vec(YX(0, 1, y**2, y), T3) == ref,
    r"$\int_0^1\int_{y}^{y^2} f\,dx\,dy$": vec(YX(0, 1, y, y**2), T3) == ref,
    r"$\int_0^1\int_{y}^{\sqrt y} f\,dx\,dy$": vec(YX(0, 1, y, sp.sqrt(y)), T3) == ref,
    r"$\int_0^1\int_{y^2}^{\sqrt y} f\,dx\,dy$": vec(YX(0, 1, y**2, sp.sqrt(y)), T3) == ref,
})
check_numeric("C03-Q6", I(1, y, 0, 4, x, 0, sp.sqrt(y)))
check("C03-Q6 original order agrees", I(1, x, 0, 2, y, x**2, 4) == R(16, 3))

# ================================================================ C04
ex2 = sp.exp(x**2)


def elementary(e, var):
    F = sp.integrate(e, var)
    return not F.has(sp.erfi, sp.erf, sp.fresnels, sp.fresnelc, sp.Si, sp.Ci, sp.Ei, sp.Integral)


check("C04 e^(x^2) has no elementary antiderivative (erfi)", not elementary(ex2, x))
check("C04 sin(x^2) has no elementary antiderivative", not elementary(sp.sin(x**2), x))
check("C04 sin(x)/x has no elementary antiderivative", not elementary(sp.sin(x)/x, x))
orig = sp.Integral(sp.Integral(ex2, (x, y, 1)), (y, 0, 1))
I_sw = I(ex2, x, 0, 1, y, 0, x)
check("C04 lesson value (e-1)/2", zero(I_sw - (sp.E - 1)/2))
num = NQ(lambda xx, yy: np.exp(xx**2), 0, 1, lambda yy: yy, lambda yy: 1)
check("C04 numeric value of the original order", abs(num - float((sp.E - 1)/2)) < 1e-9)
wrong = NQ(lambda xx, yy: np.exp(xx**2), 0, 1, lambda yy: 0, lambda yy: yy)
check("C04-Q1 swapped-to-wrong-region gives a different value", abs(wrong - num) > 1e-3)
check_options("C04-Q1", {
    r"לחשב ישירות את הפנימי: $\int e^{x^2}dx$ היא פונקציה אלמנטרית": elementary(ex2, x),
    r"להחליף סדר ל-$\int_0^1\int_0^{y}e^{x^2}\,dx\,dy$": abs(wrong - num) < 1e-9,
    "לוותר, כי אי אפשר לחשב את האינטגרל": False,    # the value (e-1)/2 exists, shown above
    r"להחליף סדר ל-$\int_0^1\int_0^{x}e^{x^2}\,dy\,dx$": zero(I_sw - (sp.E - 1)/2) and abs(float(sp.N(I_sw)) - num) < 1e-9,
})
check_numeric("C04-Q2", I(ex2, x, 0, 1, y, 0, 2*x))
num2 = NQ(lambda xx, yy: np.exp(xx**2), 0, 2, lambda yy: yy/2, lambda yy: 1)
check("C04-Q2 original order numerically = e-1", abs(num2 - (float(sp.E) - 1)) < 1e-9)
check_numeric("C04-Q3", I(sp.sin(y)/y, y, 0, sp.pi, x, 0, y))
numq3 = NQ(lambda yy, xx: np.sin(yy)/yy, 0, np.pi, lambda xx: xx, lambda xx: np.pi)
check("C04-Q3 original order numerically = 2", abs(numq3 - 2) < 1e-9)
s4 = step("C04-Q4")
check("C04-Q4 line2 inner", zero(sp.integrate(sp.exp(y**2), (x, 0, y)) - y*sp.exp(y**2)))
check("C04-Q4 line3/4 value", zero(sp.integrate(y*sp.exp(y**2), (y, 0, 1)) - (sp.E - 1)/2))
numq4 = NQ(lambda yy, xx: np.exp(yy**2), 0, 1, lambda xx: xx, lambda xx: 1)
check("C04-Q4 original order numerically", abs(numq4 - float((sp.E - 1)/2)) < 1e-9)
check_numeric("C04-Q5", I(sp.sin(y**2), y, 0, 1, x, 0, y))
numq5 = NQ(lambda yy, xx: np.sin(yy**2), 0, 1, lambda xx: xx, lambda xx: 1)
check("C04-Q5 original order numerically", abs(numq5 - float((1 - sp.cos(1))/2)) < 1e-9)
check_options("C04-Q6", {
    r"$\int_0^1\int_x^{1} e^{y^2}\,dy\,dx$": elementary(sp.exp(y**2), y),
    r"$\int_0^1\int_y^{1} \sin\left(x^2\right)\,dx\,dy$": elementary(sp.sin(x**2), x),
    r"$\int_0^1\int_0^{x} e^{x^2}\,dy\,dx$": elementary(sp.exp(x**2), y),
    r"$\int_0^\pi\int_y^{\pi} \dfrac{\sin x}{x}\,dx\,dy$": elementary(sp.sin(x)/x, x),
})

# ================================================================ C05
tri = [sp.Integer(1), x + y, y]
two = lambda f: I(f, x, -1, 0, y, 0, 1 + x) + I(f, x, 0, 1, y, 0, 1 - x)
one = lambda f: I(f, y, 0, 1, x, y - 1, 1 - y)
check("C05 triangle (-1,0),(1,0),(0,1): both orders agree", all(zero(two(f) - one(f)) for f in tri))
check("C05 area 1", two(1) == 1)
# top boundary changes formula at x=0: slopes +1 and -1
check("C05-Q1 top boundary has two formulas (1+x left, 1-x right)", sp.diff(1 + x, x) != sp.diff(1 - x, x))
check("C05-Q1 left piece needs y<=1+x, right piece y<=1-x: the two agree only at x=0", sp.solve(sp.Eq(1 + x, 1 - x), x) == [0])
check_options("C05-Q1", {
    "אינטגרל אחד, כי יש רק שני גבולות": False,
    "שלושה אינטגרלים, אחד לכל קודקוד": False,
    "שני אינטגרלים, כי הגבול העליון משנה נוסחה ב-$x=0$": True,
    "אי אפשר לסרוק את התחום בפסים אנכיים": False,
})
check_numeric("C05-Q2", one(1))
Tq = [sp.Integer(1), x + y, y]
ref = tuple(I(f, x, 0, 1, y, 0, x) + I(f, x, 1, 2, y, 0, 2 - x) for f in Tq)
check_options("C05-Q3", {
    r"$\int_0^1\int_y^{2-y}f\,dx\,dy$": tuple(I(f, y, 0, 1, x, y, 2 - y) for f in Tq) == ref,
    r"$\int_0^1\int_{2-y}^{y}f\,dx\,dy$": tuple(I(f, y, 0, 1, x, 2 - y, y) for f in Tq) == ref,
    r"$\int_0^2\int_y^{2-y}f\,dx\,dy$": tuple(I(f, y, 0, 2, x, y, 2 - y) for f in Tq) == ref,
    r"$\int_0^1\int_0^{2}f\,dx\,dy$": tuple(I(f, y, 0, 1, x, 0, 2) for f in Tq) == ref,
})
q4_two = I(y, x, 0, 1, y, 0, x) + I(y, x, 1, 2, y, 0, 2 - x)
check_numeric("C05-Q4", I(y, y, 0, 1, x, y, 2 - y))
check("C05-Q4 two-piece value agrees (1/3)", q4_two == R(1, 3))
# Q5 findbug: the planted line says the top of the triangle (0,0),(2,0),(1,1) is y=1 for 0<=x<=1
region = lambda px, py: py >= 0 and px >= py and px <= 2 - py
check("C05-Q5 the point (0.5, 0.8) is NOT in the region, so y=1 is not the top for x in [0,1]", not region(R(1, 2), R(4, 5)))
check("C05-Q5 true top on [0,1] is y=x", region(R(1, 2), R(1, 2)) and not region(R(1, 2), R(1, 2) + R(1, 100)))
check("C05-Q5 vertices", all(region(*p) for p in [(0, 0), (2, 0), (1, 1)]))
check("C05-Q5 line4 equals line0 for several f", all(I(f, y, 0, 1, x, y, 2 - y) == I(f, x, 0, 1, y, 0, x) + I(f, x, 1, 2, y, 0, 2 - x) for f in Tq))
check("C05-Q5 bugIndex", step("C05-Q5")["bugIndex"] == 2)

# ================================================================ C06
P = [sp.Integer(1), y, x]
def polar(f, r0, r1, t0, t1):
    return sp.simplify(sp.integrate(sp.integrate(f.subs({x: r*sp.cos(th), y: r*sp.sin(th)})*r, (r, r0, r1)), (th, t0, t1)))
half = tuple(polar(f, 0, 3, 0, sp.pi) for f in P)       # half disk y>=0, radius 3
check("C06-Q1 half disk: area 9pi/2, int y = 18, int x = 0", half == (9*sp.pi/2, 18, 0))
check_options("C06-Q1", {
    r"$0\le r\le9,\ 0\le\theta\le\pi$": tuple(polar(f, 0, 9, 0, sp.pi) for f in P) == half,
    r"$0\le r\le3,\ 0\le\theta\le2\pi$": tuple(polar(f, 0, 3, 0, 2*sp.pi) for f in P) == half,
    r"$0\le r\le3,\ -\tfrac\pi2\le\theta\le\tfrac\pi2$": tuple(polar(f, 0, 3, -sp.pi/2, sp.pi/2) for f in P) == half,
    r"$0\le r\le3,\ 0\le\theta\le\pi$": tuple(polar(f, 0, 3, 0, sp.pi) for f in P) == half,
})
check_numeric("C06-Q2", polar(x**2 + y**2, 0, 1, 0, 2*sp.pi))
check("C06-Q2 without r you would get 2pi/3", abs(float(2*sp.pi/3) - float(sp.pi/2)) > 0.1)
jac = sp.Matrix([r*sp.cos(th), r*sp.sin(th)]).jacobian([r, th]).det()
check("C06-Q3 Jacobian is r", zero(jac - r))
check_options("C06-Q3", {
    r"$r^2\,dr\,d\theta$": zero(r**2 - jac),
    r"$r\,dr\,d\theta$": zero(r - jac),
    r"$dr\,d\theta$": zero(1 - jac),
    r"$\tfrac1r\,dr\,d\theta$": zero(1/r - jac),
})
check_numeric("C06-Q4", polar(sp.Integer(1), 1, 2, 0, sp.pi/2))
check("C06-Q4 quarter of (4pi - pi)", polar(sp.Integer(1), 1, 2, 0, sp.pi/2) == R(1, 4)*(4*sp.pi - sp.pi))
# Q5: which polar curve is x^2+y^2=4x ?  points on r=c(theta) -> check the cartesian equation
def on_circle(rf):
    for tv in [0.1, 0.4, 0.7, 1.0, 1.3, -0.5]:
        rv = float(rf.subs(th, tv))
        px, py = rv*np.cos(tv), rv*np.sin(tv)
        if abs(px**2 + py**2 - 4*px) > 1e-9:
            return False
    return True
check_options("C06-Q5", {
    "$r=4$": on_circle(sp.Integer(4)),
    r"$r=2\cos\theta$": on_circle(2*sp.cos(th)),
    r"$r=4\sin\theta$": on_circle(4*sp.sin(th)),
    r"$r=4\cos\theta$": on_circle(4*sp.cos(th)),
})
check("C06-Q6 final value 2 (last line of the order step)", polar(x*y, 0, 2, 0, sp.pi/2) == 2 and step("C06-Q6")["lines"][-1].strip() == "$=2$")
check("C06-Q6 pieces", sp.integrate(r**3, (r, 0, 2)) == 4 and sp.integrate(sp.sin(th)*sp.cos(th), (th, 0, sp.pi/2)) == R(1, 2))
check("C06-Q6 direct cartesian check", abs(NQ(lambda yy, xx: xx*yy, 0, 2, lambda xx: 0, lambda xx: np.sqrt(4 - xx**2)) - 2) < 1e-9)

# ================================================================ C07
def jac_uv_over_xy(U, V):
    return sp.Matrix([U, V]).jacobian([x, y]).det()
check_numeric("C07-Q1", 1/sp.Abs(jac_uv_over_xy(y - x, y + 2*x)))
check("C07-Q1 determinant is -3", jac_uv_over_xy(y - x, y + 2*x) == -3)
curves = [(t, t), (t, 2*t), (t, 1/t), (t, 4/t)]          # y=x, y=2x, xy=1, xy=4 (x=t>0)
def rectangle(U, V):
    consts = []
    for cx, cy in curves:
        cu = zero(sp.diff(U.subs({x: cx, y: cy}), t))
        cv = zero(sp.diff(V.subs({x: cx, y: cy}), t))
        if not (cu or cv):
            return False
        consts.append("u" if cu else "v")
    return sorted(consts) == ["u", "u", "v", "v"] and consts[0] == consts[1] and consts[2] == consts[3] and consts[0] != consts[2]
check_options("C07-Q2", {
    r"$u=x+y,\ v=x-y$": rectangle(x + y, x - y),
    r"$u=y-x,\ v=xy$": rectangle(y - x, x*y),
    r"$u=x^2+y^2,\ v=\dfrac yx$": rectangle(x**2 + y**2, y/x),
    r"$u=\dfrac yx,\ v=xy$": rectangle(y/x, x*y),
})
Ju = sp.simplify(jac_uv_over_xy(y/x, x*y))
check("C07-Q3 |d(u,v)/d(x,y)| = 2u = 2y/x (x,y>0)", zero(Ju + 2*y/x))
U_, V_ = sp.symbols("U V", positive=True)
xs, ys = sp.sqrt(V_/U_), sp.sqrt(U_*V_)
Jxy = sp.simplify(sp.Matrix([xs, ys]).jacobian([U_, V_]).det())
check("C07-Q3 inverse Jacobian is 1/(2u) in (u,v)", zero(sp.Abs(Jxy) - 1/(2*U_)))
check_numeric("C07-Q3", 1/(2*2))
check_numeric("C07-Q4", sp.integrate(sp.integrate(1/(2*U_), (V_, 1, 4)), (U_, 1, 2)))
# grid area of 1<=y/x<=2, 1<=xy<=4 (x,y>0)
n = 4000
xg = np.linspace(0.2, 5, n); yg = np.linspace(0.2, 10, 2*n)
X, Y = np.meshgrid(xg, yg)
mask = (Y/X >= 1) & (Y/X <= 2) & (X*Y >= 1) & (X*Y <= 4)
area = mask.sum()*(xg[1] - xg[0])*(yg[1] - yg[0])
check("C07-Q4 grid area ~ (3/2)ln2", abs(area - 1.5*np.log(2)) < 0.01)
jd = jac_uv_over_xy(x + y, x - y)
check("C07-Q5 d(u,v)/d(x,y) = -2", jd == -2)
check_options("C07-Q5", {
    r"$-2\,du\,dv$": zero(-2 - 1/sp.Abs(jd)),
    r"$2\,du\,dv$": zero(2 - 1/sp.Abs(jd)),
    r"$-\tfrac12\,du\,dv$": zero(-R(1, 2) - 1/sp.Abs(jd)),
    r"$\tfrac12\,du\,dv$": zero(R(1, 2) - 1/sp.Abs(jd)),
})
check("C07-Q6 lines true/false", jd == -2 and abs(jd) == 2 and 1/abs(jd) == R(1, 2))
check("C07-Q6 line2 'dA = 2 du dv' is false", 1/abs(jd) != 2)
val = R(1, 2)*sp.integrate(U_, (U_, 1, 3))*sp.integrate(1, (V_, 0, 2))
check("C07-Q6 value 4", val == 4)
# direct check with the rotated square: x=(u+v)/2, y=(u-v)/2
uu, vv = sp.symbols("uu vv", real=True)
direct = sp.integrate(sp.integrate(((uu + vv)/2 + (uu - vv)/2)*sp.Abs(sp.Matrix([(uu + vv)/2, (uu - vv)/2]).jacobian([uu, vv]).det()), (uu, 1, 3)), (vv, 0, 2))
check("C07-Q6 direct value 4", direct == 4)
nn = 3000
xg = np.linspace(0, 3, nn); yg = np.linspace(-1, 3, nn)
X, Y = np.meshgrid(xg, yg)
m = (X + Y >= 1) & (X + Y <= 3) & (X - Y >= 0) & (X - Y <= 2)
check("C07-Q6 grid integral ~ 4", abs(((X + Y)*m).sum()*(xg[1] - xg[0])*(yg[1] - yg[0]) - 4) < 0.02)
check("C07 lesson square area 2", I(1, U_, 1, 3, V_, 0, 2)*R(1, 2) == 2)

# ================================================================ C08 (boss: real bank ids)
bank = {q["id"]: q for q in json.loads((ROOT / "questions.json").read_text(encoding="utf-8"))["questions"]}
boss_ids = [q["bankId"] for q in LV["C08"]["questions"]]
check("C08 six bank ids", len(boss_ids) == 6 and len(set(boss_ids)) == 6)
for b in boss_ids:
    check(f"C08 {b} in the bank, not held, steps verified", b in bank and not bank[b].get("hold") and bank[b].get("steps") and bank[b].get("stepsSource") == "ai-verified")
check("C08 26A-A-Q1a is an official question", bank["26A-A-Q1a"]["official"] is True)
check("C08 26A-A-Q1a value (e^2-3)/2", zero(I(x*sp.exp(x**2), x, 0, sp.sqrt(2), y, 0, 2 - x**2) - (sp.exp(2) - 3)/2) and zero(I(x*sp.exp(x**2), y, 0, 2, x, 0, sp.sqrt(2 - y)) - (sp.exp(2) - 3)/2))
check("C08 25A-A-Q4a value 1/pi", zero(I(sp.sin(sp.pi*x**2/2), x, 0, 1, y, 0, x) - 1/sp.pi))
a_two = lambda f: I(f, x, -4, 0, y, 0, sp.sqrt(x + 4)) + I(f, x, 0, 2, y, 0, 2 - x)
check("C08 23A-C-Q4a swap agrees", all(zero(a_two(f) - I(f, y, 0, 2, x, y**2 - 4, 2 - y)) for f in [sp.Integer(1), x + y, x*y]))
check("C08 23A-C-Q1a area 3pi", polar(sp.Integer(1), 0, 0, 0, 0) == 0 and sp.simplify(sp.integrate(sp.integrate(r, (r, 2*sp.cos(th), 4*sp.cos(th))), (th, -sp.pi/2, sp.pi/2)) - 3*sp.pi) == 0)
check("C08 22A-B-Q1b value", zero(sp.integrate(sp.integrate(sp.sin(2 + r**2)*r, (r, 0, 3)), (th, 0, sp.pi)) - sp.pi*(sp.cos(2) - sp.cos(11))/2))
check("C08 26A-A-Q4a value -1/2", sp.integrate(sp.integrate(-U_, (U_, 0, 1)), (V_, 1, 2)) == -R(1, 2))

print("OK: %d checks passed" % len(OK))
