# -*- coding: utf-8 -*-
"""sympy checks for the guided steps of 24A-A. Run: PYTHONUTF8=1 py tools/verify/24A-A/steps_24A-A.py
Re-computes every numeric step answer and the facts behind the choice / findbug steps, then compares with raw JSON."""
import json, pathlib, math
import sympy as sp

HERE = pathlib.Path(__file__).resolve().parent
raw = json.loads((HERE.parents[1] / "raw" / "24A-A.json").read_text(encoding="utf-8"))
Q = {f"{q['num']}{q.get('part','')}": q for q in raw["questions"]}
x, y, z = sp.symbols("x y z", positive=True)
k = sp.symbols("k", real=True)
n = sp.symbols("n", integer=True, positive=True)
r, th = sp.symbols("r theta", positive=True)
S = sp.Rational


def nums(key):
    return [s for s in Q[key]["steps"] if s["type"] == "numeric"]


def chk(key, idx, val):
    s = [s for s in Q[key]["steps"]][idx]
    assert s["type"] == "numeric", (key, idx)
    assert abs(float(val) - s["answer"]) <= max(s.get("tol", 0), 1e-12) + 1e-12, (key, idx, float(val), s["answer"])


# Q1a
f = (x**3*y - x*y**3)/(x**2 + y**2)
fp = sp.simplify(f.subs({x: r*sp.cos(th), y: r*sp.sin(th)}))
assert sp.degree(sp.simplify(fp/(sp.cos(th)**3*sp.sin(th) - sp.cos(th)*sp.sin(th)**3)), r) == 2
chk("1א", 0, 2)
g = sp.cos(th)**3*sp.sin(th) - sp.cos(th)*sp.sin(th)**3
assert sp.simplify(g - sp.sin(4*th)/4) == 0
chk("1א", 1, S(1, 4))
# Q1b
f1 = 2*sp.exp(-x**2) + sp.exp(-3*y**2)
chk("1ב", 0, sp.diff(f1, x).subs({x: 1, y: 0}).evalf())
chk("1ב", 1, sp.diff(f1, y).subs({x: 1, y: 0}))
# Q2a
chk("2א", 0, sp.limit(sp.sin(1/sp.sqrt(n))*sp.sqrt(n), n, sp.oo))
chk("2א", 1, sp.limit(sp.sqrt(n)/(sp.sqrt(n) + sp.sqrt(n - 1)), n, sp.oo))
# Q2b
fb = x*y*(x**2 - y**2)/(x**2 + y**2)
h = sp.symbols("h", real=True)
chk("2ב", 0, 0)
assert fb.subs(y, 0) == 0
eps = sp.simplify((fb/sp.sqrt(x**2 + y**2)).subs({x: r*sp.cos(th), y: r*sp.sin(th)}))
assert sp.simplify(eps - r*sp.sin(4*th)/4) == 0
chk("2ב", 1, S(1, 4))
# Q3a
s_ = sp.symbols("s")
an = 2**n/(n**2 + 1)
chk("3א", 0, sp.limit(an/an.subs(n, n + 1), n, sp.oo))
assert sp.simplify(an*S(1, 2)**n - 1/(n**2 + 1)) == 0
assert Q["3א"]["steps"][2]["options"][0]["value"] == "$\\left[-\\frac32,-\\frac12\\right]$"
assert sp.Sum(1/(n**2 + 1), (n, 1, sp.oo)).is_convergent()
# Q3b: identity with concrete F, and the claimed formulas
s, t = sp.symbols("s t")
for F in (sp.sin(s)*t**2, sp.exp(s) + t**3*s, s**2*t + sp.cos(t)):
    u = x**k*F.subs({s: z/x, t: y/x}, simultaneous=True)
    assert sp.simplify(x*sp.diff(u, x) + y*sp.diff(u, y) + z*sp.diff(u, z) - k*u) == 0
    Fs, Ft = sp.diff(F, s).subs({s: z/x, t: y/x}, simultaneous=True), sp.diff(F, t).subs({s: z/x, t: y/x}, simultaneous=True)
    Fv = F.subs({s: z/x, t: y/x}, simultaneous=True)
    good = k*x**(k - 1)*Fv - x**(k - 2)*(z*Fs + y*Ft)
    bad = k*x**(k - 1)*Fv + x**(k - 2)*(z*Fs + y*Ft)
    assert sp.simplify(sp.diff(u, x) - good) == 0
    assert sp.simplify(sp.diff(u, y) - x**(k - 1)*Ft) == 0 and sp.simplify(sp.diff(u, z) - x**(k - 1)*Fs) == 0
    assert sp.simplify(x*bad + y*x**(k - 1)*Ft + z*x**(k - 1)*Fs - k*u) != 0
assert sp.diff(z/x, x) == -z/x**2
# Q4a
assert sp.simplify(1/((n + 2)*(n + 4)) - S(1, 2)*(1/(n + 2) - 1/(n + 4))) == 0
chk("4א", 0, S(1, 2))
chk("4א", 1, S(1, 3) + S(1, 4))
Ssum = sp.summation(1/(n**2 + 6*n + 8), (n, 1, sp.oo))
assert Ssum == S(7, 24)
chk("4א", 2, Ssum)
# Q4b
X, Y, lam = sp.symbols("X Y lam", real=True)
sol = sp.solve([Y - 2*lam*X, X - 2*lam*Y, X**2 + Y**2 - 2], [X, Y, lam], dict=True)
pts = {(d[X], d[Y]) for d in sol}
assert len(pts) == 4
vals = [a*b for a, b in pts]
chk("4ב", 1, len(pts)); chk("4ב", 2, max(vals)); chk("4ב", 3, min(vals))
# Q5a
x, y = sp.symbols("x y", real=True)
f5 = x**3 + 8*y**3 - 6*x*y + 1
crit = sp.solve([sp.diff(f5, x), sp.diff(f5, y)], [x, y], dict=True)
crit = [c for c in crit if all(v.is_real for v in c.values())]
assert {(c[x], c[y]) for c in crit} == {(0, 0), (1, S(1, 2))}
D = lambda p: (sp.diff(f5, x, 2)*sp.diff(f5, y, 2) - sp.diff(f5, x, y)**2).subs({x: p[0], y: p[1]})
chk("5א", 0, D((0, 0))); chk("5א", 1, D((1, S(1, 2))))
assert sp.diff(f5, x, 2).subs({x: 1}) == 6
# Q5b
fm = 1/(1 - 3*x**2)
chk("5ב", 0, 1/sp.sqrt(3))
ser = sp.series(fm, x, 0, 8).removeO()
chk("5ב", 1, ser.coeff(x, 4))
assert sp.diff(fm, x, 5).subs(x, 0) == 0
chk("5ב", 3, sp.diff(fm, x, 5).subs(x, 0))
print("steps_24A-A: all checks passed")
