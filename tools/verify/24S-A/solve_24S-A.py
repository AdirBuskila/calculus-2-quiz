# -*- coding: utf-8 -*-
"""Solver's independent sympy + numeric verification for sitting 24S-A (no key).
Run: PYTHONUTF8=1 py tools/verify/24S-A/solve_24S-A.py   (asserts; prints OK lines)"""
import math
import numpy as np
import sympy as sp

R = sp.Rational
x, y, z, t, h = sp.symbols("x y z t h", real=True)
r, ph = sp.symbols("r phi", positive=True)
n = sp.symbols("n", integer=True, positive=True)


def ok(label, cond):
    assert cond, label
    print("OK", label)


# ---------- Q1a ----------
f = y*sp.cos(x*y)
g = sp.Matrix([sp.diff(f, x), sp.diff(f, y)]).subs({x: 1, y: 0})
ok("Q1a grad(1,0)=(0,1)", list(g) == [0, 1])
a, b = sp.symbols("a b", real=True)
sol = sp.solve([g[0]*a + g[1]*b - 1, a**2 + b**2 - 1], [a, b], dict=True)
ok("Q1a unique unit direction (0,1)", sol == [{a: 0, b: 1}])
# numeric directional derivative along (0,1)
fl = sp.lambdify((x, y), f)
ok("Q1a numeric D_u f = 1", abs((fl(1, 1e-6) - fl(1, -1e-6))/2e-6 - 1) < 1e-8)

# ---------- Q1b ----------
zf = sp.exp(x - y)*sp.sin(x + y)
zxx, zyy = sp.diff(zf, x, 2), sp.diff(zf, y, 2)
ok("Q1b z_xx = 2e^{x-y}cos(x+y)", sp.simplify(zxx - 2*sp.exp(x - y)*sp.cos(x + y)) == 0)
ok("Q1b z_yy = -2e^{x-y}cos(x+y)", sp.simplify(zyy + 2*sp.exp(x - y)*sp.cos(x + y)) == 0)
ok("Q1b z_x = e^{x-y}(sin+cos)", sp.simplify(sp.diff(zf, x) - sp.exp(x - y)*(sp.sin(x + y) + sp.cos(x + y))) == 0)
ok("Q1b z_y = e^{x-y}(cos-sin)", sp.simplify(sp.diff(zf, y) - sp.exp(x - y)*(sp.cos(x + y) - sp.sin(x + y))) == 0)

# ---------- Q2a ----------
F = x*y**3/(x**2 + y**2)
Fp = sp.simplify(F.subs({x: r*sp.cos(ph), y: r*sp.sin(ph)}))
ok("Q2a polar r^2 cos sin^3", sp.simplify(Fp - r**2*sp.cos(ph)*sp.sin(ph)**3) == 0)
ok("Q2a limit 0 (|f|<=r^2)", sp.limit(r**2, r, 0) == 0)
ok("Q2a path y=x", sp.limit(F.subs(y, x), x, 0) == 0)
ok("Q2a path y=x^2", sp.limit(F.subs(y, x**2), x, 0) == 0)
fx0 = sp.limit((F.subs({x: h, y: 0}) - 0)/h, h, 0)
fy0 = sp.limit((F.subs({x: 0, y: h}) - 0)/h, h, 0)
ok("Q2a fx(0,0)=0, fy(0,0)=0", fx0 == 0 and fy0 == 0)
ok("Q2a f(h,0)=0 and f(0,h)=0 exactly", F.subs({x: h, y: 0}) == 0 and F.subs({x: 0, y: h}) == 0)
q = sp.simplify(Fp/r)
ok("Q2a diff quotient = r cos sin^3", sp.simplify(q - r*sp.cos(ph)*sp.sin(ph)**3) == 0)
# numeric: sup over angles of |quotient| at small r
angs = np.linspace(0, 2*np.pi, 2001)
for rr in [1e-2, 1e-4]:
    ok(f"Q2a numeric |quotient|<=r at r={rr}", np.max(np.abs(rr*np.cos(angs)*np.sin(angs)**3)) <= rr)

# ---------- Q2b ----------
# series 1: |cos n|/(n^5+2)^(1/4) <= n^(-5/4); p=5/4>1
ok("Q2b-1 (n^5+2)^(1/4) >= n^(5/4)", all((k**5 + 2)**0.25 >= k**1.25 for k in range(1, 2000)))
s1 = sum(abs(math.cos(k))/(k**5 + 2)**0.25 for k in range(1, 200001))
print("  partial sum |terms| to 2e5:", s1)
# series 2: b_n = 1/sqrt(n(n+1)), compare with 1/n
bn = 1/sp.sqrt(n*(n + 1))
ok("Q2b-2 b_n/(1/n) -> 1", sp.limit(bn*n, n, sp.oo) == 1)
ok("Q2b-2 b_n -> 0", sp.limit(bn, n, sp.oo) == 0)
ok("Q2b-2 b_n decreasing (n(n+1) increasing)", sp.simplify((n + 1)*(n + 2) - n*(n + 1)) == 2*n + 2)
ok("Q2b-2 b_n >= 1/(n+1)", all(1/math.sqrt(k*(k + 1)) >= 1/(k + 1) for k in range(1, 5000)))

# ---------- Q3a ----------
an = 1/(n*4**n)
Rr = sp.limit(an/an.subs(n, n + 1), n, sp.oo)
ok("Q3a R=4", Rr == 4)
ok("Q3a x=6 gives sum 1/n", sp.simplify(an*4**n - 1/n) == 0)
ok("Q3a x=-2 gives (-1)^n/n", sp.simplify(an*(-4)**n - (-1)**n/n) == 0)
ok("Q3a x=-2 sum = -ln 2 (converges)", sp.summation((-1)**n/n, (n, 1, sp.oo)) == -sp.log(2))
ok("Q3a x=6 diverges", sp.summation(1/n, (n, 1, sp.oo)) == sp.oo)

# ---------- Q3b ----------
f3 = 2*x**2 - 3*y**2 + x*y - 3*x + 8*y
crit = sp.solve([sp.diff(f3, x), sp.diff(f3, y)], [x, y], dict=True)
ok("Q3b interior critical (2/5,7/5) only", crit == [{x: R(2, 5), y: R(7, 5)}])
ok("Q3b (2/5,7/5) outside D (y>1)", R(7, 5) > 1)
# D: 0<=x<=y<=1. Edges AB: x=0, BC: y=1, AC: y=x
eAB = f3.subs(x, 0); eBC = f3.subs(y, 1); eAC = f3.subs(y, x)
ok("Q3b AB: -3y^2+8y, crit y=4/3 outside", sp.solve(sp.diff(eAB, y), y) == [R(4, 3)])
ok("Q3b BC: 2x^2-2x+5, crit x=1/2", sp.expand(eBC - (2*x**2 - 2*x + 5)) == 0 and sp.solve(sp.diff(eBC, x), x) == [R(1, 2)])
ok("Q3b AC: 5x (monotone)", sp.expand(eAC - 5*x) == 0)
vals = {"A": f3.subs({x: 0, y: 0}), "B": f3.subs({x: 0, y: 1}), "C": f3.subs({x: 1, y: 1}), "M": f3.subs({x: R(1, 2), y: 1})}
ok("Q3b values A=0,B=5,C=5,(1/2,1)=9/2", vals == {"A": 0, "B": 5, "C": 5, "M": R(9, 2)})
gx = np.linspace(0, 1, 3001)
X, Y = np.meshgrid(gx, gx)
m = Y >= X - 1e-12
fv = (2*X**2 - 3*Y**2 + X*Y - 3*X + 8*Y)[m]
ok("Q3b grid max 5, min 0", abs(fv.max() - 5) < 1e-9 and abs(fv.min()) < 1e-9)
iy = np.argmax(np.where(m, 2*X**2 - 3*Y**2 + X*Y - 3*X + 8*Y, -1e9))
print("  grid argmax at", X.flat[iy], Y.flat[iy])

# ---------- Q4a ----------
fx_, fy_ = sp.symbols("fx fy")
eq = sp.Eq(2*fx_ + sp.exp(t)*fy_, 0)  # d/dt f(2t+1,e^t) = 0
ok("Q4a f_y = -1", sp.simplify(sp.solve(eq.subs(fx_, sp.exp(t)/2), fy_)[0]) == -1)
# an explicit f satisfying both hypotheses (shows the data are consistent)
on = {x: 2*t + 1, y: sp.exp(t)}
fe3 = 3 + (y/2)*(x - 1 - 2*sp.log(y))   # fx = y/2 = e^t/2 on the curve
ok("Q4a explicit f3: f=3 on curve", sp.simplify(fe3.subs(on)) == 3)
ok("Q4a explicit f3: fx=e^t/2", sp.simplify(sp.diff(fe3, x).subs(on) - sp.exp(t)/2) == 0)
ok("Q4a explicit f3: fy=-1", sp.simplify(sp.diff(fe3, y).subs(on)) == -1)

# ---------- Q4b ----------
f4 = sp.log(x + 1/y)
f4x, f4y = sp.simplify(sp.diff(f4, x)), sp.simplify(sp.diff(f4, y))
pts = sp.solve([f4x - 1, f4y + R(16, 9)], [x, y], dict=True)
pts = sorted([(p[x], p[y]) for p in pts], key=lambda p: p[0])
ok("Q4b points (-1/3,3/4),(7/3,-3/4)", pts == [(R(-1, 3), R(3, 4)), (R(7, 3), R(-3, 4))])
X_, Y_, Z_ = sp.symbols("X Y Z")
planes = []
for (px, py) in pts:
    ok(f"Q4b ({px},{py}) in domain x+1/y=1>0", px + 1/py == 1)
    fz = f4.subs({x: px, y: py})
    ok(f"Q4b f({px},{py})=0", sp.simplify(fz) == 0)
    planes.append(sp.expand(fz + 1*(X_ - px) - R(16, 9)*(Y_ - py)))
ok("Q4b plane1 Z = X - 16Y/9 + 5/3", sp.expand(planes[0] - (X_ - R(16, 9)*Y_ + R(5, 3))) == 0)
ok("Q4b plane2 Z = X - 16Y/9 - 11/3", sp.expand(planes[1] - (X_ - R(16, 9)*Y_ - R(11, 3))) == 0)

# ---------- Q5a ----------
G = 5*z**3 + 3*x*y*z - x**2*y**2 + 1
P = {x: 1, y: -1, z: 0}
ok("Q5a G(1,-1,0)=0", G.subs(P) == 0)
Gx, Gy, Gz = [sp.diff(G, v).subs(P) for v in (x, y, z)]
ok("Q5a Gx=-2, Gy=2, Gz=-3", (Gx, Gy, Gz) == (-2, 2, -3))
zx, zy = -Gx/Gz, -Gy/Gz
ok("Q5a zx=-2/3, zy=2/3, sum 0", (zx, zy, zx + zy) == (R(-2, 3), R(2, 3), 0))
# numeric: solve G=0 for z near 0 at perturbed points
from scipy.optimize import brentq
def zof(xx, yy):
    return brentq(lambda zz: 5*zz**3 + 3*xx*yy*zz - xx**2*yy**2 + 1, -0.5, 0.5)
e = 1e-6
nzx = (zof(1 + e, -1) - zof(1 - e, -1))/(2*e)
nzy = (zof(1, -1 + e) - zof(1, -1 - e))/(2*e)
ok("Q5a numeric zx,zy", abs(nzx + 2/3) < 1e-6 and abs(nzy - 2/3) < 1e-6)

# ---------- Q5b ----------
f5 = x*y*(6 - x - y)
cp = sp.solve([sp.diff(f5, x), sp.diff(f5, y)], [x, y], dict=True)
cps = sorted([(c[x], c[y]) for c in cp])
ok("Q5b critical (0,0),(0,6),(2,2),(6,0)", cps == [(0, 0), (0, 6), (2, 2), (6, 0)])
Hm = sp.hessian(f5, (x, y))
exp_ = {(0, 0): (-36, 0, "saddle"), (0, 6): (-36, -12, "saddle"), (6, 0): (-36, 0, "saddle"), (2, 2): (12, -4, "max")}
for p, (dd, fxx, role) in exp_.items():
    Hp = Hm.subs({x: p[0], y: p[1]})
    ok(f"Q5b {p}: D={dd}, fxx={fxx} -> {role}", Hp.det() == dd and Hp[0, 0] == fxx)
ok("Q5b f(2,2)=8", f5.subs({x: 2, y: 2}) == 8)
# numeric: (2,2) local max on small grid; saddles take both signs nearby
gg = np.linspace(-0.05, 0.05, 101)
GX, GY = np.meshgrid(gg, gg)
fn = sp.lambdify((x, y), f5)
ok("Q5b numeric (2,2) local max", np.max(fn(2 + GX, 2 + GY)) <= 8 + 1e-12)
for p in [(0, 0), (0, 6), (6, 0)]:
    v = fn(p[0] + GX, p[1] + GY) - fn(*p)
    ok(f"Q5b numeric {p} saddle (both signs)", v.max() > 0 and v.min() < 0)

# ---------- contours.json consistency ----------
import json, pathlib
for e in json.loads((pathlib.Path(__file__).parent / "contours.json").read_text(encoding="utf-8")):
    fe_ = sp.sympify(e["f"].replace("^", "**"), locals={"x": x, "y": y})
    for c in e["critical_points"]:
        v = fe_.subs({x: sp.sympify(c["x"]), y: sp.sympify(c["y"])})
        ok(f"contours {e['id']} {c['x']},{c['y']} f={c['f']}", sp.simplify(v - sp.sympify(c["f"])) == 0)
print("ALL OK")
