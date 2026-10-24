# -*- coding: utf-8 -*-
"""sympy checks for the guided steps of 23A-C. Run: PYTHONUTF8=1 py tools/verify/23A-C/steps_23A-C.py
Independently re-computes every numeric step answer and the facts behind the choice / findbug steps,
then compares with the stored raw JSON (steps are addressed by index)."""
import json, pathlib, math
import numpy as np
import sympy as sp

HERE = pathlib.Path(__file__).resolve().parent
raw = json.loads((HERE.parents[1] / "raw" / "23A-C.json").read_text(encoding="utf-8"))
Q = {f"{q['num']}{q.get('part','')}": q for q in raw["questions"]}
x, y, z, t = sp.symbols("x y z t", real=True)
n = sp.symbols("n", integer=True, positive=True)
r, th = sp.symbols("r theta", positive=True)
S = sp.Rational


def chk(key, idx, val):
    s = Q[key]["steps"][idx]
    assert s["type"] == "numeric", (key, idx)
    assert abs(float(val) - s["answer"]) <= max(s.get("tol", 0), 1e-12) + 1e-12, (key, idx, float(val), s["answer"])


def right(key, idx):
    s = Q[key]["steps"][idx]
    return [o for o in s["options"] if o["id"] == s["correctId"]][0]["value"]


# ---- Q1a ----
inner = sp.integrate(r, (r, 2*sp.cos(th), 4*sp.cos(th)))
chk("1א", 1, sp.simplify(inner/sp.cos(th)**2))
A = sp.integrate(inner, (th, -sp.pi/2, sp.pi/2))
chk("1א", 2, sp.simplify(A/sp.pi))
# distractor bounds give a different area
alt = sp.integrate(sp.integrate(r, (r, 2, 4)), (th, -sp.pi/2, sp.pi/2))
assert sp.simplify(alt - 3*sp.pi) != 0
alt2 = sp.integrate(sp.integrate(r, (r, sp.cos(th), 2*sp.cos(th))), (th, -sp.pi/2, sp.pi/2))
assert sp.simplify(alt2 - 3*sp.pi) != 0
# 0..2pi with r from 2cos to 4cos gives a signed area 0 for the negative half
alt3 = sp.integrate(inner, (th, 0, 2*sp.pi))
assert sp.simplify(alt3 - 3*sp.pi) != 0
# the circles in polar form
assert sp.simplify((r**2 - 2*r*sp.cos(th)).subs(r, 2*sp.cos(th))) == 0
assert sp.simplify((r**2 - 4*r*sp.cos(th)).subs(r, 4*sp.cos(th))) == 0

# ---- Q1b ----
z_ = sp.symbols("z_", positive=True)
f = x**2*y*sp.sqrt(z_)
pt = {x: 2, y: 1, z_: 1}
g = [sp.diff(f, v).subs(pt) for v in (x, y, z_)]
chk("1ב", 0, g[2])
chk("1ב", 1, sp.sqrt(sum(c**2 for c in g)))
u = sp.Matrix([1, 2, 2]); uh = u/u.norm()
D = (sp.Matrix(g).T*uh)[0]
chk("1ב", 2, D)
chk("1ב", 3, sp.sqrt(sum(c**2 for c in g))/D)

# ---- Q2a ----
chk("2א", 0, S(2, 3))
chk("2א", 1, sp.limit(sp.atan((n + 2)/(n + 3)), n, sp.oo))
assert sp.simplify(sp.limit(sp.atan((n + 2)/(n + 3)), n, sp.oo) - sp.pi/4) == 0
# numeric: partial sums of both abs series converge (tail tiny)
ns = np.arange(1, 400)
a1 = (2/3)**ns*np.abs(np.cos(ns)); a2 = np.arctan((ns + 2)/(ns + 3))**ns
assert a1[-50:].sum() < 1e-6 and a2[-50:].sum() < 1e-6
assert (a2 > 0).all() and np.arctan((ns + 2)/(ns + 3)).max() < math.pi/4

# ---- Q2b ----
h = sp.symbols("h", real=True)
f2 = lambda a, b: (a**3 + b**3)/(2*a**2 + b**2)
chk("2ב", 0, sp.limit(f2(h, 0)/h, h, 0))
chk("2ב", 1, sp.limit(f2(0, h)/h, h, 0))
ex = sp.simplify((f2(x, y) - x/2 - y) - (-x*y*(4*x + y))/(2*(2*x**2 + y**2)))
assert ex == 0
xx = sp.symbols("xx", positive=True)
E = lambda a, b: (-a*b*(4*a + b))/(2*(2*a**2 + b**2)*sp.sqrt(a**2 + b**2))
chk("2ב", 2, sp.simplify(E(xx, xx)))
assert sp.simplify(E(xx, 0)) == 0
# continuity at 0: |f| <= |x|+|y| holds on a grid, so f is continuous
gx, gy = np.meshgrid(np.linspace(-1, 1, 801), np.linspace(-1, 1, 801))
m = (gx**2 + gy**2) > 0
fv = (gx**3 + gy**3)[m]/(2*gx**2 + gy**2)[m]
assert (np.abs(fv) <= np.abs(gx[m]) + np.abs(gy[m]) + 1e-12).all()

# ---- Q3a ----
an = 1/(2**n + 3**n)
chk("3א", 0, 1/sp.limit(sp.exp(sp.log(an)/n), n, sp.oo))
chk("3א", 1, sp.limit(3**n/(2**n + 3**n), n, sp.oo))
assert sp.limit(3**n/(2**n + 3**n), n, sp.oo) != 0
assert right("3א", 2) == "$(-3,3)$"

# ---- Q3b ----
for G in (sp.Function("G"), ):
    tt = x**2 - y**2
    zz = y*G(tt)
    lhs = sp.diff(zz, x)/x + sp.diff(zz, y)/y
    assert sp.simplify((lhs - zz/y**2).doit()) == 0
Gt = lambda w: w**2
zz = y*Gt(x**2 - y**2)
sub = {x: 2, y: 1}
chk("3ב", 0, sp.diff(zz, x).subs(sub))
chk("3ב", 1, sp.diff(zz, y).subs(sub))
chk("3ב", 2, (sp.diff(zz, x)/x + sp.diff(zz, y)/y).subs(sub))
assert (zz/y**2).subs(sub) == 9
# findbug: the stored wrong line (+2y g') breaks the identity, the right one keeps it
G_, g1, yy = sp.symbols("G g1 yy")
good = 2*yy*g1 + G_/yy - 2*yy*g1
bad = 2*yy*g1 + G_/yy + 2*yy*g1
assert sp.simplify(good - G_/yy) == 0 and sp.simplify(bad - G_/yy) != 0
fb = Q["3ב"]["steps"][3]
assert fb["bugIndex"] == 3
assert "+2y\\,g'(t)" in fb["lines"][3]

# ---- Q4a ----
chk("4א", 0, sp.sqrt(0 + 4))
assert sp.sqrt(4) == 2 and 2 - 0 == 2
A_orig = sp.integrate(sp.sqrt(x + 4), (x, -4, 0)) + sp.integrate(2 - x, (x, 0, 2))
A_new = sp.integrate(sp.integrate(1, (x, y**2 - 4, 2 - y)), (y, 0, 2))
assert A_orig == A_new == S(22, 3)
chk("4א", 2, A_new)
bad_bounds = [(4 - y**2, 2 - y), (-4, 2 - y), (y**2 - 4, y - 2)]
for lo, hi in bad_bounds:
    assert sp.integrate(sp.integrate(1, (x, lo, hi)), (y, 0, 2)) != S(22, 3)
assert right("4א", 1) == "$\\int_0^2dy\\int_{y^2-4}^{2-y}f(x,y)\\,dx$"
# and with a non-constant f the swap is exact
fx = x*y + x**2
I1 = sp.integrate(sp.integrate(fx, (y, 0, sp.sqrt(x + 4))), (x, -4, 0)) + sp.integrate(sp.integrate(fx, (y, 0, 2 - x)), (x, 0, 2))
I2 = sp.integrate(sp.integrate(fx, (x, y**2 - 4, 2 - y)), (y, 0, 2))
assert sp.simplify(I1 - I2) == 0

# ---- Q4b ----
F = x**2 + y**2 + 4*x*y
chk("4ב", 0, F.subs({x: S(1, 2), y: sp.sqrt(3)/2}))
arc = sp.simplify(F.subs({x: sp.cos(th), y: sp.sin(th)}))
assert sp.simplify(arc - (1 + 2*sp.sin(2*th))) == 0
crit = [s for s in sp.solve(sp.diff(arc, th), th) if 0 <= s <= sp.pi/3]
assert crit == [sp.pi/4], crit
chk("4ב", 1, crit[0])
# dense-grid extrema over the sector
rr, tt_ = np.meshgrid(np.linspace(0, 1, 1501), np.linspace(0, math.pi/3, 1501))
vals = (rr**2)*(1 + 2*np.sin(2*tt_))
chk("4ב", 2, round(vals.max(), 6)) if abs(vals.max() - 3) < 1e-4 else (_ for _ in ()).throw(AssertionError("max"))
assert abs(vals.min() - 0) < 1e-12
chk("4ב", 3, 0)
assert sp.solve([sp.diff(F, x), sp.diff(F, y)], [x, y], dict=True) == [{x: 0, y: 0}]
cands = [F.subs({x: 0, y: 0}), F.subs({x: 1, y: 0}), F.subs({x: S(1, 2), y: sp.sqrt(3)/2}), F.subs({x: 1/sp.sqrt(2), y: 1/sp.sqrt(2)})]
assert max(cands) == 3 and min(cands) == 0

# ---- Q5a ----
F5 = (x**2 - 2*y**2)*sp.exp(x - y)
cr = sp.solve([sp.diff(F5, x), sp.diff(F5, y)], [x, y], dict=True)
cr = {(c[x], c[y]) for c in cr}
assert cr == {(0, 0), (-4, -2)}, cr
chk("5א", 0, [c for c in cr if c != (0, 0)][0][1])
Dt = lambda p: sp.simplify((sp.diff(F5, x, 2)*sp.diff(F5, y, 2) - sp.diff(F5, x, y)**2).subs({x: p[0], y: p[1]}))
chk("5א", 1, Dt((0, 0)))
assert sp.diff(F5, x, 2).subs({x: 0, y: 0}) == 2   # the lone f_xx sign would suggest a minimum
assert right("5א", 2) == "נקודת אוכף"
assert sp.simplify(Dt((-4, -2)) - 8*sp.exp(-4)) == 0
chk("5א", 3, sp.diff(F5, x, 2).subs({x: -4, y: -2}))
chk("5א", 4, F5.subs({x: -4, y: -2}))
assert sp.diff(F5, x, 2).subs({x: -4, y: -2}) < 0

# ---- Q5b ----
F6 = 1/(x**2 + x - 2)
ser = sp.series(F6, x, 0, 12).removeO()
chk("5ב", 0, ser.coeff(x, 0))
chk("5ב", 1, ser.coeff(x, 1))
chk("5ב", 3, sp.diff(F6, x, 10).subs(x, 0))
assert sp.diff(F6, x, 10).subs(x, 0) == S(-9681525, 8)
cn = lambda k: -S(1, 3)*(1 + S(-1, 2)**k/2)
assert all(sp.simplify(ser.coeff(x, k) - cn(k)) == 0 for k in range(12))
# domain: singularities at x=1 and x=-2, so radius 1; at x=+-1 the terms do not tend to 0
assert abs(float(cn(200))) > 0.3
assert right("5ב", 2) == "$(-1,1)$"

print("steps_23A-C: all checks passed")
