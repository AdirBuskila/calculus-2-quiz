# -*- coding: utf-8 -*-
"""Step-author checks for 24S-A: every expected value used in the guided steps of tools/gen/gen_24S-A.py
is recomputed independently here with sympy (and numerics where noted). Run:
  PYTHONUTF8=1 py tools/verify/24S-A/steps_24S-A.py
"""
import numpy as np
import sympy as sp

R = sp.Rational
x, y, z, t, a, b = sp.symbols("x y z t a b", real=True)
r, ph = sp.symbols("r phi", positive=True)
n = sp.symbols("n", integer=True, positive=True)


def ok(label, cond):
    assert cond, label
    print("OK", label)


# ---- Q1a: f = y cos(xy) at (1,0)
f = y*sp.cos(x*y)
fx1, fy1 = sp.diff(f, x).subs({x: 1, y: 0}), sp.diff(f, y).subs({x: 1, y: 0})
ok("Q1a f_x(1,0)=0", fx1 == 0)
ok("Q1a f_y(1,0)=1", fy1 == 1)
for u, val in [((0, 1), 1), ((1, 0), 0), ((0, -1), -1), ((1/sp.sqrt(2), 1/sp.sqrt(2)), 1/sp.sqrt(2))]:
    ok(f"Q1a D_u f for u={u} equals {val}", sp.simplify(fx1*u[0] + fy1*u[1] - val) == 0)
ok("Q1a only (0,1) gives 1", sp.solve([fx1*a + fy1*b - 1, a**2 + b**2 - 1], [a, b], dict=True) == [{a: 0, b: 1}])

# ---- Q1b: z = e^{x-y} sin(x+y)
zf = sp.exp(x - y)*sp.sin(x + y)
zxx, zyy = sp.diff(zf, x, 2), sp.diff(zf, y, 2)
ok("Q1b z_xx(0,0)=2", zxx.subs({x: 0, y: 0}) == 2)
ok("Q1b z_yy(0,0)=-2", zyy.subs({x: 0, y: 0}) == -2)
ok("Q1b z_x line", sp.simplify(sp.diff(zf, x) - sp.exp(x - y)*(sp.sin(x + y) + sp.cos(x + y))) == 0)
ok("Q1b z_xx line", sp.simplify(zxx - 2*sp.exp(x - y)*sp.cos(x + y)) == 0)
ok("Q1b z_y line", sp.simplify(sp.diff(zf, y) - sp.exp(x - y)*(sp.cos(x + y) - sp.sin(x + y))) == 0)
ok("Q1b z_yy line (minus)", sp.simplify(zyy + 2*sp.exp(x - y)*sp.cos(x + y)) == 0)
ok("Q1b bug line (plus sign) is wrong", sp.simplify(zyy - 2*sp.exp(x - y)*sp.cos(x + y)) != 0)
ok("Q1b sum is 0", sp.simplify(zxx + zyy) == 0)

# ---- Q2a
F = x*y**3/(x**2 + y**2)
Fp = sp.simplify(F.subs({x: r*sp.cos(ph), y: r*sp.sin(ph)}))
ok("Q2a polar f = r^2 cos sin^3", sp.simplify(Fp - r**2*sp.cos(ph)*sp.sin(ph)**3) == 0)
ok("Q2a f/rho = r cos sin^3 (exponent 1)", sp.simplify(Fp/r - r*sp.cos(ph)*sp.sin(ph)**3) == 0)
h = sp.symbols("h", real=True)
ok("Q2a f(h,0)=0", sp.simplify(F.subs({x: h, y: 0})) == 0)
ok("Q2a f(0,h)=0", sp.simplify(F.subs({x: 0, y: h})) == 0)
phis = np.linspace(0, 2*np.pi, 20001)
ok("Q2a |cos sin^3| <= 1 on grid", np.max(np.abs(np.cos(phis)*np.sin(phis)**3)) <= 1)
# numeric: f/rho -> 0 along several rays
for th in [0.3, 1.0, 2.0, 4.0]:
    rr = 1e-6
    val = (rr*np.cos(th))*(rr*np.sin(th))**3/rr**2/rr
    ok(f"Q2a f/rho small at theta={th}", abs(val) < 1e-5)

# ---- Q2b (sympy limits, numeric partial sums as evidence)
p = R(5, 4)
ok("Q2b series1 bound exponent 5/4", sp.simplify(sp.root(n**5, 4) - n**p) == 0 and p > 1)
bn = 1/sp.sqrt(n*(n + 1))
ok("Q2b limit comparison b_n/(1/n) = 1", sp.limit(bn*n, n, sp.oo) == 1)
ok("Q2b b_n -> 0", sp.limit(bn, n, sp.oo) == 0)
ok("Q2b b_n decreasing (n(n+1) increasing)", all((1/np.sqrt(k*(k + 1))) > (1/np.sqrt((k + 1)*(k + 2))) for k in range(1, 5000)))
S = np.cumsum(1/np.sqrt(np.arange(1, 2_000_001)*(np.arange(1, 2_000_001) + 1.0)))
ok("Q2b abs partial sums grow like log (diverge)", S[-1] - S[1999] > 6)
k = np.arange(1, 400001).astype(float)
A = np.cumsum(np.abs(np.cos(k))/(k**5 + 2.0)**0.25)
ok("Q2b series1 abs partial sums bounded (<= zeta(5/4)~4.6)", A[-1] < 4.6 and A[-1] - A[39999] < 0.5)

# ---- Q3a: sum (x-2)^n / (n 4^n)
an = 1/(n*4**n)
ok("Q3a R=4", sp.limit(an/an.subs(n, n + 1), n, sp.oo) == 4)
ok("Q3a x=6 term 1/n", sp.simplify((4**n)/(n*4**n) - 1/n) == 0)
ok("Q3a x=-2 term (-1)^n/n", sp.simplify(((-4)**n)/(n*4**n) - (-1)**n/n) == 0)
ok("Q3a harmonic diverges", sp.summation(1/n, (n, 1, sp.oo)) == sp.oo)
ok("Q3a alternating harmonic converges", sp.summation((-1)**n/n, (n, 1, sp.oo)) == -sp.log(2))

# ---- Q3b: f = 2x^2-3y^2+xy-3x+8y on triangle (0,0),(0,1),(1,1)
g = 2*x**2 - 3*y**2 + x*y - 3*x + 8*y
crit = sp.solve([sp.diff(g, x), sp.diff(g, y)], [x, y], dict=True)
ok("Q3b critical point (2/5,7/5)", crit == [{x: R(2, 5), y: R(7, 5)}])
ok("Q3b critical y = 1.4 > 1 (outside)", float(crit[0][y]) == 1.4 and crit[0][y] > 1)
ok("Q3b f(1/2,1)=9/2", g.subs({x: R(1, 2), y: 1}) == R(9, 2))
ok("Q3b f on AC is 5x", sp.expand(g.subs(y, x) - 5*x) == 0)
ok("Q3b vertices 0,5,5", [g.subs({x: 0, y: 0}), g.subs({x: 0, y: 1}), g.subs({x: 1, y: 1})] == [0, 5, 5])
ok("Q3b AB crit y=4/3 outside", sp.solve(sp.diff(g.subs(x, 0), y), y) == [R(4, 3)])
gx = np.linspace(0, 1, 801)
X, Y = np.meshgrid(gx, gx)
mask = X <= Y + 1e-12
G = sp.lambdify((x, y), g, "numpy")(X, Y)
Gm = np.where(mask, G, np.nan)
ok("Q3b grid max = 5", abs(np.nanmax(Gm) - 5) < 1e-9)
ok("Q3b grid min = 0", abs(np.nanmin(Gm) - 0) < 1e-9)
iy, ix = np.where(np.isclose(Gm, 5))
pts = sorted({(round(float(X[i, j]), 6), round(float(Y[i, j]), 6)) for i, j in zip(iy, ix)})
ok("Q3b max attained only at (0,1),(1,1)", pts == [(0.0, 1.0), (1.0, 1.0)])

# ---- Q4a: f(2t+1, e^t)=3, f_x = e^t/2
fx_, fy_ = sp.symbols("fx fy")
eq = sp.Eq(2*fx_ + sp.exp(t)*fy_, 0)
sol = sp.solve(eq.subs(fx_, sp.exp(t)/2), fy_)
ok("Q4a f_y = -1", sol == [-1])
ok("Q4a 2*f_x at t=0 equals 1", (2*sp.exp(t)/2).subs(t, 0) == 1)
ok("Q4a x'(t)=2, y'(t)=e^t", sp.diff(2*t + 1, t) == 2 and sp.diff(sp.exp(t), t) == sp.exp(t))
ok("Q4a wrong chain forms give wrong f_y",
   sp.solve((sp.exp(t)*fx_ + 2*fy_).subs(fx_, sp.exp(t)/2), fy_) != [-1]
   and sp.solve((2*fx_ + fy_).subs(fx_, sp.exp(t)/2), fy_) != [-1])

# ---- Q4b: f = ln(x+1/y), grad = (1, -16/9)
fb = sp.log(x + 1/y)
sols = sp.solve([sp.diff(fb, x) - 1, sp.diff(fb, y) + R(16, 9)], [x, y], dict=True)
ok("Q4b two points", sorted([(s[x], s[y]) for s in sols]) == sorted([(R(-1, 3), R(3, 4)), (R(7, 3), -R(3, 4))]))
ok("Q4b x+1/y = 1", all(sp.simplify(s[x] + 1/s[y]) == 1 for s in sols))
ok("Q4b y^2=9/16", all(s[y]**2 == R(9, 16) for s in sols))
ok("Q4b f=0 at both", all(fb.subs(s) == 0 for s in sols))
consts = []
for s in sols:
    pl = sp.expand(0 + 1*(x - s[x]) - R(16, 9)*(y - s[y]))
    consts.append(pl.subs({x: 0, y: 0}))
ok("Q4b constants 5/3 and -11/3", sorted(consts) == [-R(11, 3), R(5, 3)])
ok("Q4b y>0 plane constant 5/3", [s[y] for s in sols if s[y] > 0] == [R(3, 4)] and R(5, 3) in consts)

# ---- Q5a: F = 5z^3+3xyz-x^2y^2+1 at (1,-1,0)
Fz_ = 5*z**3 + 3*x*y*z - x**2*y**2 + 1
P = {x: 1, y: -1, z: 0}
ok("Q5a F(P)=0", Fz_.subs(P) == 0)
Fx, Fy, Fzz = [sp.diff(Fz_, v).subs(P) for v in (x, y, z)]
ok("Q5a F_z=-3, F_x=-2, F_y=2", (Fzz, Fx, Fy) == (-3, -2, 2))
zx, zy = -Fx/Fzz, -Fy/Fzz
ok("Q5a z_x=-2/3, z_y=2/3, sum 0", (zx, zy, zx + zy) == (-R(2, 3), R(2, 3), 0))

# ---- Q5b: f = xy(6-x-y)
fq = x*y*(6 - x - y)
cps = sp.solve([sp.diff(fq, x), sp.diff(fq, y)], [x, y], dict=True)
ok("Q5b 4 critical points", sorted((c[x], c[y]) for c in cps) == [(0, 0), (0, 6), (2, 2), (6, 0)])
Hs = sp.hessian(fq, (x, y))
Dd = {(c[x], c[y]): Hs.subs(c).det() for c in cps}
ok("Q5b D values", Dd == {(0, 0): -36, (6, 0): -36, (0, 6): -36, (2, 2): 12})
ok("Q5b f_xx(2,2)=-4 <0 (max)", Hs.subs({x: 2, y: 2})[0, 0] == -4)
ok("Q5b f(2,2)=8", fq.subs({x: 2, y: 2}) == 8)
fl = sp.lambdify((x, y), fq, "numpy")
ok("Q5b (2,2) local max numerically", all(fl(2 + dx, 2 + dy) < 8 for dx in (-.1, .1) for dy in (-.1, .1)))
ok("Q5b (0,0) saddle numerically", fl(.1, .1) > 0 > fl(.1, -.1))
print("ALL OK")
