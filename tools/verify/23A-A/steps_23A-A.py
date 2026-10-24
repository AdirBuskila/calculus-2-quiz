# -*- coding: utf-8 -*-
"""sympy/numeric checks for the guided steps of 23A-A. Run: PYTHONUTF8=1 py -I tools/verify/23A-A/steps_23A-A.py"""
import json, pathlib, math
import numpy as np
import sympy as sp

HERE = pathlib.Path(__file__).resolve().parent
raw = json.loads((HERE.parents[1] / "raw" / "23A-A.json").read_text(encoding="utf-8"))
Q = {f"{q['num']}{q.get('part','')}": q for q in raw["questions"]}
S = sp.Rational


def chk(key, idx, val):
    s = Q[key]["steps"][idx]
    assert s["type"] == "numeric", (key, idx)
    assert abs(float(val) - s["answer"]) <= s.get("tol", 0) + 1e-12, (key, idx, float(val), s["answer"])


x, y, z = sp.symbols("x y z", positive=True)
r, th = sp.symbols("r theta", positive=True)
n = sp.symbols("n", integer=True, positive=True)

# Q1a: theta range, integrals, brute-force check of the double integral
assert sp.atan(1) == sp.pi/4 and sp.atan(sp.sqrt(3)) == sp.pi/3
chk("1א", 1, sp.integrate(r, (r, 1, 2)))
chk("1א", 2, sp.integrate(th, (th, sp.pi/4, sp.pi/3)))
I = sp.integrate(r, (r, 1, 2))*sp.integrate(th, (th, sp.pi/4, sp.pi/3))
assert sp.simplify(I - 7*sp.pi**2/192) == 0
chk("1א", 3, I)
g = np.linspace(0.0, 2.0, 4001)
X, Y = np.meshgrid(g, g)
m = (X**2 + Y**2 >= 1) & (X**2 + Y**2 <= 4) & (Y >= X) & (Y <= math.sqrt(3)*X)
h = g[1] - g[0]
approx = np.sum(np.arctan2(Y[m], X[m]))*h*h
assert abs(approx - float(I)) < 5e-3, approx
# Q1b
u = sp.log(x**2 + y**2 + z**2)
pt = {x: 1, y: 2, z: 1}
chk("1ב", 0, (x**2 + y**2 + z**2).subs(pt))
chk("1ב", 1, sp.diff(u, y).subs(pt))
gr = sp.Matrix([sp.diff(u, v).subs(pt) for v in (x, y, z)])
assert gr == sp.Matrix([S(1, 3), S(2, 3), S(1, 3)])
# Q2a
mm = sp.symbols("mm", positive=True)
chk("2א", 0, sp.limit(sp.sin(sp.pi/mm)*mm, mm, sp.oo))
assert n*sp.cbrt(n) == n**S(4, 3) or sp.simplify(n*sp.cbrt(n) - n**S(4, 3)) == 0
chk("2א", 1, S(4, 3))
assert sp.limit(sp.log(1 + n**S(-4, 3))/n**S(-4, 3), n, sp.oo) == 1
partial_abs = sum(math.sin(math.pi/k) for k in range(2, 10**5)); partial_abs2 = sum(math.sin(math.pi/k) for k in range(2, 4*10**5))
assert partial_abs2 - partial_abs > 3.0  # sum of sin(pi/n) diverges like log
abs2 = [math.log(1 + k**(-4/3)) for k in range(1, 10**6)]
assert sum(abs2[10**5:]) < 3*(10**5)**(-1/3)*1.01  # tail bounded by the integral of n^(-4/3)
# Q2b
chk("2ב", 0, 0)
rr = sp.symbols("rr", positive=True)
assert sp.limit(rr*sp.sin(1/rr), rr, 0) == 0
assert sp.simplify(rr**2/rr - rr) == 0
chk("2ב", 1, 1)
# Q3a
a = lambda k: S(3)**k/((2*k + 1)**2*sp.sqrt(S(5)**k))
Rr = sp.limit(a(n)/a(n + 1), n, sp.oo)
assert sp.simplify(Rr - sp.sqrt(5)/3) == 0
chk("3א", 0, Rr)
assert sp.simplify((S(3)**n*(sp.sqrt(5)/3)**n/sp.sqrt(S(5)**n)) - 1) == 0
# Q3b: identity with concrete f, g_z formula and the wrong-sign variant
xx, yy, zz = sp.symbols("xx yy zz", positive=True)
uu, vv = sp.symbols("uu vv")
for f in (sp.sin(uu)*vv**2, sp.exp(uu) + vv**3*uu, uu**2*vv + sp.cos(vv)):
    U = 1/yy - 1/xx
    V = xx*yy*sp.exp(-zz**2/2)
    G = f.subs({uu: U, vv: V}, simultaneous=True)
    assert sp.simplify(xx**2*sp.diff(G, xx) + yy**2*sp.diff(G, yy) + (xx + yy)/zz*sp.diff(G, zz)) == 0
    fu = sp.diff(f, uu).subs({uu: U, vv: V}, simultaneous=True)
    fv = sp.diff(f, vv).subs({uu: U, vv: V}, simultaneous=True)
    assert sp.simplify(sp.diff(G, zz) + fv*xx*yy*zz*sp.exp(-zz**2/2)) == 0
    assert sp.simplify(sp.diff(G, yy) - (-fu/yy**2 + fv*xx*sp.exp(-zz**2/2))) == 0
    assert sp.simplify(sp.diff(G, xx) - (fu/xx**2 + fv*yy*sp.exp(-zz**2/2))) == 0
    bad = xx**2*sp.diff(G, xx) + yy**2*(fu/yy**2 + fv*xx*sp.exp(-zz**2/2))
    assert sp.simplify(bad + (xx + yy)/zz*sp.diff(G, zz)) != 0
# Q4a
uvx = sp.Matrix([[2*x*y, -1], [x**2, 1]])
assert sp.expand(uvx.det() - (2*x*y + x**2)) == 0
chk("4א", 1, 4 - 1)
chk("4א", 2, 6)
gx = np.linspace(0.001, 6, 6001)
X, Y = np.meshgrid(gx, np.linspace(0.001, 8, 8001)[::1])
m = (Y*X**2 >= 1) & (Y*X**2 <= 4) & (Y - X <= 1) & (Y - X >= -1)
dx = gx[1] - gx[0]; dy = 8/8000
val = np.sum((X[m]**2 + 2*X[m]*Y[m]))*dx*dy
assert abs(val - 6) < 0.05, val
# Q4b
ff = lambda a_, b_: 1 - a_**2 - b_**2
chk("4ב", 0, (0 - 1)**2 + (0 - 1)**2)
M2 = 1 - sp.sqrt(2)/2
chk("4ב", 1, ff(M2, M2))
M1 = 1 + sp.sqrt(2)/2
chk("4ב", 2, ff(M1, M1))
t = np.linspace(0, 2*np.pi, 2000001)
bx, by = 1 + np.cos(t), 1 + np.sin(t)
vals = ff(bx, by)
assert abs(vals.max() - float(ff(M2, M2))) < 1e-6 and abs(vals.min() - float(ff(M1, M1))) < 1e-6
# Q5a
X_, Y_ = sp.symbols("X_ Y_", real=True)
f5 = (X_ + Y_)**2 - 4*Y_**2 - 48*Y_
crit = sp.solve([sp.diff(f5, X_), sp.diff(f5, Y_)], [X_, Y_], dict=True)
assert crit == [{X_: 6, Y_: -6}]
chk("5א", 0, crit[0][Y_])
chk("5א", 1, sp.diff(f5, X_, 2)*sp.diff(f5, Y_, 2) - sp.diff(f5, X_, Y_)**2)
# Q5b
x5 = sp.symbols("x5")
f = 1/(x5**2 + x5 - 6)
pf = sp.apart(f, x5)
assert sp.simplify(pf - (-S(1, 5)/(x5 + 3) + S(1, 5)/(x5 - 2))) == 0
chk("5ב", 0, S(1, 5))
assert sp.singularities(f, x5) == {-3, 2}   # nearest pole at distance 2 -> radius 2
d10 = sp.diff(f, x5, 10).subs(x5, 0)
assert d10 == -sp.factorial(10)/5*(S(1, 3**11) + S(1, 2**11))
chk("5ב", 2, d10)
print("steps_23A-A: all checks passed")
