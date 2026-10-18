# -*- coding: utf-8 -*-
"""sympy + numeric checks for sitting 26A (calculus-2, moed A 12/02/2026).
Run: PYTHONUTF8=1 py tools/verify/26A-A/check.py
Also writes regions.json and contours.json next to this file."""
import json, pathlib, math
import sympy as sp
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
R = sp.Rational
x, y, t, u, v, h = sp.symbols("x y t u v h", real=True)
r, th = sp.symbols("r theta", positive=True)
ok = []


def check(name, cond):
    assert cond, "MISMATCH: " + name
    ok.append(name)


# ---- Q1a: swap order ----
I_orig = sp.integrate(sp.integrate(x*sp.exp(x**2), (y, 0, 2 - x**2)), (x, 0, sp.sqrt(2)))
I_swap = sp.integrate(sp.integrate(x*sp.exp(x**2), (x, 0, sp.sqrt(2 - y))), (y, 0, 2))
ans1 = (sp.exp(2) - 3)/2
check("Q1a original order", sp.simplify(I_orig - ans1) == 0)
check("Q1a swapped order", sp.simplify(I_swap - ans1) == 0)
from scipy import integrate as si
num1 = si.dblquad(lambda yy, xx: xx*math.exp(xx**2), 0, math.sqrt(2), 0, lambda xx: 2 - xx**2)[0]
check("Q1a numeric", abs(num1 - float(ans1)) < 1e-8)

# ---- Q1b: limit ln(1+xy)/(x^2+y^2) ----
f1 = sp.log(1 + x*y)/(x**2 + y**2)
l_axis = sp.limit(f1.subs(y, 0), x, 0)
l_diag = sp.limit(f1.subs(y, x), x, 0)
check("Q1b axis limit 0", l_axis == 0)
check("Q1b diagonal limit 1/2", l_diag == R(1, 2))
fp = f1.subs({x: r*sp.cos(th), y: r*sp.sin(th)})
check("Q1b polar depends on theta",
      sp.simplify(sp.limit(fp.subs(th, 0), r, 0) - sp.limit(fp.subs(th, sp.pi/4), r, 0)) != 0)

# ---- Q2a ----
n = sp.symbols("n", integer=True, positive=True)
# |2^n cos n / 3^n| <= (2/3)^n, geometric sum
check("Q2a geometric sum 2", sp.summation((R(2, 3))**n, (n, 1, sp.oo)) == 2)
check("Q2a cos(pi n)=(-1)^n", all(sp.cos(sp.pi*k) == (-1)**k for k in range(1, 12)))
# alternating harmonic sum -ln 2 ; absolute: harmonic diverges
check("Q2a alt harmonic sum", sp.summation((-1)**n/n, (n, 1, sp.oo)) == -sp.log(2))
check("Q2a harmonic diverges", sp.summation(1/n, (n, 1, sp.oo)) == sp.oo)
S = sum((2/3)**k*math.cos(k) for k in range(1, 400))
check("Q2a first series numeric converged", abs(S - sum((2/3)**k*math.cos(k) for k in range(1, 800))) < 1e-12)

# ---- Q2b: differentiability at origin ----
f2 = (x**3 + y**3)/(2*x**2 + y**2)
fx0 = sp.limit(f2.subs({x: h, y: 0})/h, h, 0)
fy0 = sp.limit(f2.subs({x: 0, y: h})/h, h, 0)
check("Q2b fx(0,0)=1/2", fx0 == R(1, 2))
check("Q2b fy(0,0)=1", fy0 == 1)
q = (f2 - (R(1, 2)*x + y))/sp.sqrt(x**2 + y**2)
qd = sp.simplify(q.subs({y: x}))
check("Q2b diag quotient = -5 x/(6 sqrt2 |x|)", sp.simplify(qd.subs(x, R(1, 100)) + 5/(6*sp.sqrt(2))) == 0)
check("Q2b diag quotient nonzero limit (x>0)", sp.limit(q.subs(y, x), x, 0, "+") == -5/(6*sp.sqrt(2)))
check("Q2b diag quotient other side", sp.limit(q.subs(y, x), x, 0, "-") == 5/(6*sp.sqrt(2)))
# polar: f continuous at 0 (f -> 0)
fpol = sp.simplify(f2.subs({x: r*sp.cos(th), y: r*sp.sin(th)}))
check("Q2b f -> 0 in polar", sp.limit(fpol, r, 0) == 0)

# ---- Q3a: interval [-3,3) shifted by 2 => [-5,1) ----
check("Q3a shift", (-3 - 2, 3 - 2) == (-5, 1))

# ---- Q3b: chain rule identity ----
uu, vv = sp.symbols("u v", positive=True)
X = sp.sqrt(uu*vv)
Y = 1/vv
Z = sp.exp(X**2*Y)
lhs = uu*sp.diff(Z, uu) - vv*sp.diff(Z, vv)
rhs_printed = Z*X**2/vv
rhs_solution_last = Z*X**2/vv**2
check("Q3b identity with printed RHS z x^2/v", sp.simplify(lhs - rhs_printed) == 0)
check("Q3b solution's last line x^2/v^2 does NOT equal LHS", sp.simplify(lhs - rhs_solution_last) != 0)
# z_u, z_v as in the official solution
xs, ys = sp.symbols("xs ys", positive=True)
zxy = sp.exp(xs**2*ys)
zx, zy = sp.diff(zxy, xs), sp.diff(zxy, ys)
check("Q3b z_x = 2xy e^(x2 y)", sp.simplify(zx - 2*xs*ys*zxy) == 0)
check("Q3b z_y = x^2 e^(x2 y)", sp.simplify(zy - xs**2*zxy) == 0)

# ---- Q4a: parallelogram substitution u=y-x, v=xy ----
J = sp.Matrix([[sp.diff(y - x, x), sp.diff(x*y, x)], [sp.diff(y - x, y), sp.diff(x*y, y)]]).det()
check("Q4a 1/J = -(x+y)", sp.simplify(J + (x + y)) == 0)
I4 = sp.integrate(sp.integrate(-u, (u, 0, 1)), (v, 1, 2))
check("Q4a uv result -1/2", I4 == R(-1, 2))
# direct, order x-slices: for each y>0? region: y = x, y = x+1, xy in [1,2]. Use numeric on fine grid
def inD(px, py):
    return (px > 0) & (py > 0) & (py - px >= 0) & (py - px <= 1) & (px*py >= 1) & (px*py <= 2)
N = 6000
xs_ = np.linspace(0, 3, N)
ys_ = np.linspace(0, 3.5, N)
X_, Y_ = np.meshgrid(xs_, ys_)
mask = inD(X_, Y_)
val = ((X_**2 - Y_**2)*mask).sum()*(xs_[1]-xs_[0])*(ys_[1]-ys_[0])
check("Q4a numeric grid ~ -1/2", abs(val + 0.5) < 0.01)
# exact, vertical strips: y from x to x+1 and xy in [1,2] => y in [max(x,1/x), min(x+1,2/x)]
def inner(px):
    lo = max(px, 1/px)
    hi = min(px + 1, 2/px)
    if hi <= lo: return 0.0
    return ((px**2)*(hi - lo) - (hi**3 - lo**3)/3)
# breakpoints in x: x=1 (x=1/x), x+1=2/x -> x=1, x=sqrt2 (x=2/x), x=0.5 (x+1=... ) etc.
pts = sorted(set([0.3, 0.5, 1/ (2) ,1.0, math.sqrt(2), 2.0]))
xs_roots = [float(s) for s in sp.solve(sp.Eq(x + 1, 2/x), x) if s > 0]
xs_roots2 = [float(s) for s in sp.solve(sp.Eq(x**2 + x, 1), x) if s > 0]  # x(x+1)=1 -> y=x+1 meets xy=1
brk = sorted(set([0.0, 1.0, math.sqrt(2)] + xs_roots + xs_roots2 + [3.0]))
tot = sum(si.quad(inner, a, b, limit=200)[0] for a, b in zip(brk[:-1], brk[1:]))
check("Q4a numeric integral vertical strips = -1/2", abs(tot + 0.5) < 1e-6)

# ---- Q4b: abs extrema of x^3+x^2-3x+y^2 on x^2+y^2=4 ----
f4 = x**3 + x**2 - 3*x + y**2
g4 = sp.Symbol("lam")
L = f4 - g4*(x**2 + y**2 - 4)
sols = sp.solve([sp.diff(L, x), sp.diff(L, y), x**2 + y**2 - 4], [x, y, g4], dict=True)
pts4 = sorted({(s[x], s[y], f4.subs(s)) for s in sols}, key=lambda p: (p[2], p[0], p[1]))
vals4 = {(sp.nsimplify(p[0]), sp.nsimplify(p[1])): p[2] for p in pts4}
expected = {(-2, 0): 2, (1, sp.sqrt(3)): 2, (1, -sp.sqrt(3)): 2, (-1, sp.sqrt(3)): 6, (-1, -sp.sqrt(3)): 6, (2, 0): 6}
check("Q4b Lagrange critical points = 6 expected", {k: v for k, v in vals4.items()} == {k: sp.Integer(v) for k, v in expected.items()})
th_ = np.linspace(0, 2*np.pi, 2000001)
fv = (2*np.cos(th_))**3 + (2*np.cos(th_))**2 - 3*2*np.cos(th_) + (2*np.sin(th_))**2
check("Q4b numeric min 2", abs(fv.min() - 2) < 1e-6)
check("Q4b numeric max 6", abs(fv.max() - 6) < 1e-6)
ft = sp.expand(f4.subs(y**2, 4 - x**2))
check("Q4b reduced f~ = x^3 - 3x + 4", sp.expand(ft - (x**3 - 3*x + 4)) == 0)

# ---- Q5a: extrema of (x-y)^3 - 3x - y^2 + 5y ----
f5 = (x - y)**3 - 3*x - y**2 + 5*y
crit = sp.solve([sp.diff(f5, x), sp.diff(f5, y)], [x, y], dict=True)
cp = sorted((s[x], s[y]) for s in crit)
check("Q5a critical points (0,1),(2,1)", cp == [(0, 1), (2, 1)])
Hs = sp.hessian(f5, (x, y))
H21 = Hs.subs({x: 2, y: 1}); H01 = Hs.subs({x: 0, y: 1})
check("Q5a fxx, fxy, fyy formulas",
      sp.simplify(sp.diff(f5, x, 2) - 6*(x - y)) == 0 and sp.simplify(sp.diff(f5, x, y) + 6*(x - y)) == 0
      and sp.simplify(sp.diff(f5, y, 2) - (6*(x - y) - 2)) == 0)
check("Q5a det H(2,1) = -12 (saddle)", H21.det() == -12)
check("Q5a det H(0,1) = 12, fxx=-6 (local max)", H01.det() == 12 and H01[0, 0] == -6)
fvals5 = (f5.subs({x: 0, y: 1}), f5.subs({x: 2, y: 1}))
# numeric: (0,1) is a local max, (2,1) is saddle
rng = np.random.default_rng(1)
def f5n(a, b): return (a - b)**3 - 3*a - b**2 + 5*b
d = rng.normal(size=(20000, 2))*0.05
check("Q5a (0,1) local max numerically", (f5n(0 + d[:, 0], 1 + d[:, 1]) <= f5n(0, 1) + 1e-12).all())
vv_ = f5n(2 + d[:, 0], 1 + d[:, 1]) - f5n(2, 1)
check("Q5a (2,1) saddle numerically", (vv_ > 0).any() and (vv_ < 0).any())

# ---- Q5b: Maclaurin of (16-5x)/(x^2-5x+6) ----
f6 = (16 - 5*x)/(x**2 - 5*x + 6)
check("Q5b partial fractions", sp.simplify(sp.apart(f6, x) - (-6/(x - 2) + 1/(x - 3))) == 0)
ser = sp.series(f6, x, 0, 25).removeO()
coef = lambda k: ser.coeff(x, k)
check("Q5b coefficient formula a_n = 3/2^n - 1/3^(n+1), n<25",
      all(coef(k) == R(3, 2**k) - R(1, 3**(k + 1)) for k in range(25)))
check("Q5b f^(20)(0) via derivative", sp.diff(f6, x, 20).subs(x, 0) == sp.factorial(20)*(R(3, 2**20) - R(1, 3**21)))
check("Q5b radius = 2 (nearest pole x=2)", min(abs(p) for p in sp.solve(x**2 - 5*x + 6, x)) == 2)
val20 = sp.factorial(20)*(R(3, 2**20) - R(1, 3**21))
print("f^(20)(0) =", val20, "~", float(val20))

# ---- regions.json ----
regions = [
    {"id": "26A-A-Q1a", "description": "x in [0,sqrt2], 0<=y<=2-x^2 (also 0<=y<=2, 0<=x<=sqrt(2-y))",
     "type": "simple",
     "orderXY": {"x": [0, "sqrt(2)"], "y": [0, "2-x^2"]},
     "orderYX": {"y": [0, 2], "x": [0, "sqrt(2-y)"]},
     "inequalities": ["x>=0", "y>=0", "y<=2-x^2"],
     "boundary_curves": ["y=2-x^2", "x=0", "y=0"],
     "vertices": [[0, 0], ["sqrt(2)", 0], [0, 2]],
     "integrand": "x*exp(x^2)", "value": "(e^2-3)/2"},
    {"id": "26A-A-Q4a", "description": "x>0,y>0 between y=x and y=x+1 and between xy=1 and xy=2",
     "type": "curvilinear",
     "inequalities": ["x>0", "y>0", "y>=x", "y<=x+1", "x*y>=1", "x*y<=2"],
     "boundary_curves": ["y=x", "y=x+1", "x*y=1", "x*y=2"],
     "substitution": {"u": "y-x", "v": "x*y", "u_range": [0, 1], "v_range": [1, 2], "abs_jacobian_xy_over_uv": "1/(x+y)"},
     "vertices": [[1, 1], ["sqrt(2)", "sqrt(2)"],
                  [float((-1 + math.sqrt(5))/2), float((1 + math.sqrt(5))/2)],
                  [float((-1 + math.sqrt(3))/2 * 1), float((1 + math.sqrt(3))/2)]],
     "integrand": "x^2-y^2", "value": "-1/2"},
]
# vertices of Q4a: y=x & xy=1 -> (1,1); y=x & xy=2 -> (sqrt2,sqrt2); y=x+1 & xy=1 -> x^2+x-1=0; y=x+1 & xy=2 -> x^2+x-2=0 -> x=1,y=2
regions[1]["vertices"] = [[1, 1], ["sqrt(2)", "sqrt(2)"], [1, 2],
                          [float((-1 + math.sqrt(5))/2), float((1 + math.sqrt(5))/2)]]
(HERE / "regions.json").write_text(json.dumps(regions, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
# check vertices
check("Q4a vertex (1,2) on y=x+1, xy=2", (2 - 1 == 1) and (1*2 == 2))
check("Q4a vertex (golden) on y=x+1, xy=1",
      abs(((-1 + math.sqrt(5))/2)*((1 + math.sqrt(5))/2) - 1) < 1e-12)

# ---- contours.json ----
contours = [
    {"id": "26A-A-Q4b", "f": "x^3+x^2-3*x+y^2", "constraint": "x^2+y^2=4", "kind": "lagrange",
     "domain": [[-3, 3], [-3, 3]],
     "critical_points": [
         {"x": 2, "y": 0, "f": 6, "role": "abs max"},
         {"x": -1, "y": "sqrt(3)", "f": 6, "role": "abs max"},
         {"x": -1, "y": "-sqrt(3)", "f": 6, "role": "abs max"},
         {"x": -2, "y": 0, "f": 2, "role": "abs min"},
         {"x": 1, "y": "sqrt(3)", "f": 2, "role": "abs min"},
         {"x": 1, "y": "-sqrt(3)", "f": 2, "role": "abs min"}]},
    {"id": "26A-A-Q5a", "f": "(x-y)^3-3*x-y^2+5*y", "constraint": None, "kind": "unconstrained",
     "domain": [[-2, 4], [-1, 3]],
     "critical_points": [
         {"x": 2, "y": 1, "f": float(fvals5[1]), "role": "saddle"},
         {"x": 0, "y": 1, "f": float(fvals5[0]), "role": "local max"}]},
]
(HERE / "contours.json").write_text(json.dumps(contours, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("f5 values", fvals5)
print("ALL OK:", len(ok), "checks")
