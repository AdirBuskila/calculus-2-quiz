# -*- coding: utf-8 -*-
"""sympy/numeric checks for the guided steps of 22A-A. Run: PYTHONUTF8=1 py -I tools/verify/22A-A/steps_22A-A.py"""
import json, pathlib, math
import numpy as np
import sympy as sp

HERE = pathlib.Path(__file__).resolve().parent
raw = json.loads((HERE.parents[1] / "raw" / "22A-A.json").read_text(encoding="utf-8"))
Q = {f"{q['num']}{q.get('part','')}": q for q in raw["questions"]}
S = sp.Rational


def chk(key, idx, val):
    s = Q[key]["steps"][idx]
    assert s["type"] == "numeric", (key, idx)
    assert abs(float(val) - s["answer"]) <= s.get("tol", 0) + 1e-12, (key, idx, float(val), s["answer"])


x, y = sp.symbols("x y", real=True)
# Q1a
f = 2*sp.sin(2*x + 2*y)
p = {x: sp.pi/2, y: sp.pi/2}
chk("1א", 0, sp.diff(f, x).subs(p))
assert sp.diff(f, y).subs(p) == 4
chk("1א", 1, sp.sqrt(sp.diff(f, x).subs(p)**2 + sp.diff(f, y).subs(p)**2))
ang = np.linspace(0, 2*np.pi, 360001)
dd = 4*np.cos(ang) + 4*np.sin(ang)
assert abs(ang[np.argmax(dd)] - np.pi/4) < 1e-3 and abs(dd.max() - math.sqrt(32)) < 1e-6
# Q1b: identity with concrete g, formula z_x, z_y, bug variant
xp, yp = sp.symbols("xp yp", positive=True)
for gfun in (sp.sin, sp.exp, lambda t: t**3 + t):
    z = yp/(3*xp) + gfun(xp*yp)
    gp = sp.diff(gfun(sp.Symbol("t")), sp.Symbol("t")).subs(sp.Symbol("t"), xp*yp)
    assert sp.simplify(xp**2*sp.diff(z, xp) - xp*yp*sp.diff(z, yp) + 2*yp/3) == 0
    assert sp.simplify(sp.diff(z, xp) - (-yp/(3*xp**2) + yp*gp)) == 0
    assert sp.simplify(sp.diff(z, yp) - (1/(3*xp) + xp*gp)) == 0
    bad_zy = -1/(3*xp) + xp*gp
    assert sp.simplify(xp**2*sp.diff(z, xp) - xp*yp*bad_zy + 2*yp/3) != 0
chk("1ב", 1, sp.simplify((xp**2*(-1/(3*xp**2)) - xp*yp*(1/(3*xp))/yp)))
# Q2a
t = sp.symbols("t", positive=True)
I = sp.integrate(1/(t*sp.log(t)**2), (t, 2, sp.oo))
assert sp.simplify(I - 1/sp.log(2)) == 0
chk("2א", 0, I)
n = sp.symbols("n", integer=True, positive=True)
chk("2א", 1, sp.limit(((n + 1)/3**(n + 1))/(n/3**n), n, sp.oo))
assert sp.Sum(n/3**n, (n, 1, sp.oo)).doit() == S(3, 4)
# Q2b
chk("2ב", 0, 0)
r = sp.symbols("r", positive=True)
assert sp.simplify(r**2/r - r) == 0 and sp.limit(r*sp.sin(1/r), r, 0) == 0
chk("2ב", 1, 1)
# Q3a
m = sp.symbols("m", positive=True)
chk("3א", 1, sp.limit(sp.sin(sp.pi/sp.sqrt(m))*sp.sqrt(m), m, sp.oo))
chk("3א", 0, 1)
vals = [math.sin(math.pi/math.sqrt(k)) for k in range(1, 20001)]
dec_from = next(k for k in range(1, 20000) if all(vals[j] > vals[j + 1] for j in range(k - 1, k + 3000)))
assert dec_from == 4, dec_from
assert vals[2] < vals[3]   # a_3 < a_4: not decreasing before n = 4
chk("3א", 2, dec_from)
ratio = [vals[k]/vals[k + 1] for k in (10**3, 10**4)]
assert abs(ratio[0] - 1) < 1e-2
# Q3b
xx, yy, zz = sp.symbols("xx yy zz", real=True)
F = yy**3 + xx*zz + yy**2 + sp.exp(zz) - 3
pt = {xx: 1, yy: 1, zz: 0}
assert F.subs(pt) == 0
chk("3ב", 0, sp.diff(F, zz).subs(pt))
fy = (-sp.diff(F, yy)/sp.diff(F, zz)).subs(pt); fx = (-sp.diff(F, xx)/sp.diff(F, zz)).subs(pt)
assert fx == 0
chk("3ב", 1, fy)
assert sp.expand(5*(yy - 1) + 2*zz - (5*yy + 2*zz - 5)) == 0   # z = fy (y-1)  <=>  5y + 2z = 5
# Q4a
u, v = y - x, y**2 + 4*x
J = sp.Matrix([[sp.diff(u, x), sp.diff(u, y)], [sp.diff(v, x), sp.diff(v, y)]]).det()
assert sp.simplify(J + 2*y + 4) == 0
chk("4א", 1, sp.integrate(sp.exp(sp.Symbol("w")), (sp.Symbol("w"), 1, 2)))
chk("4א", 2, 9)
val = 9*sp.E*(sp.E - 1)
chk("4א", 3, val)
gx = np.linspace(-9, 3.0, 12001); gy = np.linspace(0, 6, 6001)
X, Y = np.meshgrid(gx, gy)
msk = (Y - X >= 1) & (Y - X <= 2) & (Y**2 + 4*X >= 0) & (Y**2 + 4*X <= 9)
num_ = np.sum(np.exp(Y[msk] - X[msk])*(2*Y[msk] + 4))*(gx[1] - gx[0])*(gy[1] - gy[0])
assert abs(num_ - float(val))/float(val) < 5e-3, num_
# Q4b
f4 = 2*x**4 + y**4 - x**2 - 2*y**2
crit = sp.solve([sp.diff(f4, x), sp.diff(f4, y)], [x, y], dict=True)
crit = [c for c in crit if c[x]**2 + c[y]**2 <= 2]
assert len(crit) == 9
chk("4ב", 0, len(crit))
vin = [f4.subs(c) for c in crit]
assert min(vin) == -S(9, 8)
chk("4ב", 1, min(vin))
tt = np.linspace(0, 2*np.pi, 2000001)
bx, by = math.sqrt(2)*np.cos(tt), math.sqrt(2)*np.sin(tt)
fb = 2*bx**4 + by**4 - bx**2 - 2*by**2
assert abs(fb.max() - 6) < 1e-6
g = np.linspace(-math.sqrt(2), math.sqrt(2), 3001)
X, Y = np.meshgrid(g, g)
ok = X**2 + Y**2 <= 2
ff = 2*X**4 + Y**4 - X**2 - 2*Y**2
assert 5.95 < ff[ok].max() <= 6 + 1e-9 and abs(ff[ok].min() + 9/8) < 1e-3
ft = sp.expand(f4.subs(y**2, 2 - x**2)); ft = sp.expand(2*x**4 + (2 - x**2)**2 - x**2 - 2*(2 - x**2))
assert sp.simplify(ft - (3*x**4 - 3*x**2)) == 0
chk("4ב", 3, ft.subs(x, sp.sqrt(2)))
# Q5a
f5 = 1/(x**2 + x - 2)
ser = sp.series(f5, x, 0, 4).removeO()
for k, idx in ((0, 0), (1, 1), (2, 2)):
    chk("5א", idx, ser.coeff(x, k))
    assert ser.coeff(x, k) == -S(1, 3)*(S(-1)**k/S(2)**(k + 1) + 1)
assert sp.singularities(f5, x) == {-2, 1}
# Q5b
f6 = x*y**2 - y**2 - x**2/2 - 2*x + 3
cr = sp.solve([sp.diff(f6, x), sp.diff(f6, y)], [x, y], dict=True)
assert len(cr) == 3
chk("5ב", 0, len(cr))
D = lambda c: (sp.diff(f6, x, 2)*sp.diff(f6, y, 2) - sp.diff(f6, x, y)**2).subs(c)
byp = {(c[x], c[y]): D(c) for c in cr}
chk("5ב", 1, byp[(-2, 0)])
chk("5ב", 2, byp[(1, sp.sqrt(3))])
assert byp[(1, -sp.sqrt(3))] == -12 and sp.diff(f6, x, 2) == -1
print("steps_22A-A: all checks passed")
