# -*- coding: utf-8 -*-
"""sympy + numeric checks for sitting 25A-A (calculus-2, moed A 20/02/2025).
Run: PYTHONUTF8=1 py tools/verify/25A-A/check.py
Writes regions.json, contours.json and the region figures in images/exams/."""
import json, pathlib, math
import sympy as sp
import numpy as np
from scipy import integrate as si
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).resolve().parent
IMG = HERE.parents[2] / "images" / "exams"
IMG.mkdir(parents=True, exist_ok=True)
R = sp.Rational
x, y, u, v, t, h, k = sp.symbols("x y u v t h k", real=True)
r, th = sp.symbols("r theta", positive=True)
ok = []


def check(name, cond):
    assert cond, "MISMATCH: " + name
    ok.append(name)


# ---- Q1a: f = 4x^3 y/(3x^6+2y^2) ----
f1 = 4*x**3*y/(3*x**6 + 2*y**2)
along = sp.simplify(f1.subs(y, k*x**3))
check("Q1a along y=kx^3 equals 4k/(3+2k^2)", sp.simplify(along - 4*k/(3 + 2*k**2)) == 0)
check("Q1a k=0 gives 0, k=1 gives 4/5 (limit does not exist)", along.subs(k, 0) == 0 and along.subs(k, 1) == R(4, 5))
check("Q1a f(h,0)=0 so fx(0,0)=0", sp.simplify(f1.subs(y, 0)) == 0)
check("Q1a f(0,h)=0 so fy(0,0)=0", sp.simplify(f1.subs(x, 0)) == 0)

# ---- Q1b: abs extrema of y^4-x^4 on x^2+y^2<=9 ----
f2 = y**4 - x**4
lam = sp.Symbol("lam")
L = f2 + lam*(x**2 + y**2 - 9)
sol = sp.solve([sp.diff(L, x), sp.diff(L, y), x**2 + y**2 - 9], [x, y, lam], dict=True)
bpts = {(s[x], s[y]): f2.subs(s) for s in sol}
check("Q1b Lagrange points (+-3,0),(0,+-3) only",
      set(bpts) == {(3, 0), (-3, 0), (0, 3), (0, -3)})
check("Q1b values", bpts[(0, 3)] == 81 and bpts[(0, -3)] == 81 and bpts[(3, 0)] == -81 and bpts[(-3, 0)] == -81)
check("Q1b interior critical point only origin", sp.solve([sp.diff(f2, x), sp.diff(f2, y)], [x, y], dict=True) == [{x: 0, y: 0}])
g = np.linspace(-3, 3, 3001)
X, Y = np.meshgrid(g, g)
m = X**2 + Y**2 <= 9 + 1e-12
fv = (Y**4 - X**4)[m]
check("Q1b numeric max 81 / min -81", abs(fv.max() - 81) < 1e-6 and abs(fv.min() + 81) < 1e-6)

# ---- Q2a ----
n = sp.symbols("n", integer=True, positive=True)
F = 1/(x*sp.log(x)**2)
integral = sp.limit(sp.integrate(F, (x, 2, t)), t, sp.oo)
check("Q2a integral test value 1/ln2", sp.simplify(integral - 1/sp.log(2)) == 0)
check("Q2a F decreasing for x>=2", sp.simplify(sp.diff(F, x)).subs(x, 5).evalf() < 0 and sp.simplify(sp.diff(F, x)).subs(x, 50).evalf() < 0)
check("Q2a 1/(sqrt n+sqrt(n-1)) = sqrt n - sqrt(n-1)",
      all(abs(1/(math.sqrt(i) + math.sqrt(i - 1)) - (math.sqrt(i) - math.sqrt(i - 1))) < 1e-12 for i in range(1, 200)))
check("Q2a limit ratio to 1/sqrt(n) is 1/2",
      sp.limit((1/(sp.sqrt(n) + sp.sqrt(n - 1)))/(1/sp.sqrt(n)), n, sp.oo) == R(1, 2))
bn = [1/(math.sqrt(i) + math.sqrt(i - 1)) for i in range(1, 5000)]
check("Q2a b_n strictly decreasing numerically", all(bn[i + 1] < bn[i] for i in range(len(bn) - 1)))
check("Q2a (n+1)-form inequality sqrt(n^2-1)<n", all(math.sqrt(i*i - 1) < i for i in range(2, 1000)))

# ---- Q2b: (x-y) e^(x^2-y^2) over the square x+y in[1,3], x-y in [-1,1] ----
Jm = sp.Matrix([[R(1, 2), R(1, 2)], [-R(1, 2), R(1, 2)]])
check("Q2b Jacobian 1/2", Jm.det() == R(1, 2))
I2 = sp.integrate(sp.integrate(u*sp.exp(u*v)*R(1, 2), (v, 1, 3)), (u, -1, 1))
ans2 = sp.sinh(3)/3 - sp.sinh(1)
check("Q2b value sinh3/3 - sinh1", sp.simplify((I2 - ans2).rewrite(sp.exp)) == 0)
def f2b(yy, xx):
    return (xx - yy)*math.exp(xx**2 - yy**2)
# integrate in x,y over the rotated square: x from 0 to 2; y between max(1-x, x-1) and min(3-x, x+1)
def lo(xx): return max(1 - xx, xx - 1)
def hi(xx): return min(3 - xx, xx + 1)
num2 = sum(si.dblquad(f2b, a, b, lo, hi)[0] for a, b in ((0, 1), (1, 2)))
check("Q2b numeric double integral in x,y", abs(num2 - float(ans2)) < 1e-7)

# ---- Q3a ----
a_n = 2**n/sp.sqrt(5*n**2 + 1)
ratio = sp.limit(a_n/a_n.subs(n, n + 1), n, sp.oo)
check("Q3a |a_n/a_{n+1}| -> 1/2 so R=1/2", ratio == R(1, 2))
check("Q3a x-1=1/2 terms ~ 1/(sqrt5 n) (diverges)", sp.limit((1/sp.sqrt(5*n**2 + 1))/(1/n), n, sp.oo) == 1/sp.sqrt(5))
chk = [1/math.sqrt(5*i*i + 1) for i in range(1, 4000)]
check("Q3a Leibniz at x-1=-1/2: decreasing", all(chk[i + 1] < chk[i] for i in range(len(chk) - 1)))
check("Q3a Leibniz limit 0", sp.limit(1/sp.sqrt(5*n**2 + 1), n, sp.oo) == 0)

# ---- Q3b: chain rule ----
G = sp.Function("g")
zz = y*G(x**2 - y**2)
lhs = sp.diff(zz, x)/x + sp.diff(zz, y)/y
check("Q3b identity (1/x)z_x+(1/y)z_y = z/y^2", sp.simplify(lhs - zz/y**2) == 0)

# ---- Q4a: swap order ----
Ia = sp.integrate(sp.integrate(sp.sin(sp.pi*x**2/2), (y, 0, x)), (x, 0, 1))
check("Q4a value 1/pi", sp.simplify(Ia - 1/sp.pi) == 0)
num4 = si.dblquad(lambda yy, xx: math.sin(math.pi*xx**2/2), 0, 1, 0, lambda xx: xx)[0]
check("Q4a numeric", abs(num4 - 1/math.pi) < 1e-9)
# original order dxdy: y from 0..1, x from y..1 (same region 0<=y<=x<=1), integrate numerically
num4b = si.dblquad(lambda xx, yy: math.sin(math.pi*xx**2/2), 0, 1, lambda yy: yy, lambda yy: 1)[0]
check("Q4a original order numeric", abs(num4b - 1/math.pi) < 1e-9)
check("Q4a substitution t=x^2/2: int_0^{1/2} sin(pi t) dt", sp.simplify(sp.integrate(sp.sin(sp.pi*t), (t, 0, R(1, 2))) - 1/sp.pi) == 0)

# ---- Q4b: (x^2-2y^2) e^(x-y) ----
f4 = (x**2 - 2*y**2)*sp.exp(x - y)
crit = sp.solve([sp.diff(f4, x), sp.diff(f4, y)], [x, y], dict=True)
cp = sorted((s[x], s[y]) for s in crit)
check("Q4b critical points (-4,-2),(0,0)", cp == [(-4, -2), (0, 0)])
H = sp.hessian(f4, (x, y))
H0 = H.subs({x: 0, y: 0}); H1 = H.subs({x: -4, y: -2})
check("Q4b (0,0) saddle: det=-8<0", H0.det() == -8)
check("Q4b (-4,-2) local max: det>0, fxx<0", sp.simplify(H1.det()) > 0 and sp.simplify(H1[0, 0]) < 0)
check("Q4b det(-4,-2)=8 e^-4", sp.simplify(H1.det() - 8*sp.exp(-4)) == 0)
check("Q4b f(-4,-2) = 8 e^-2", sp.simplify(f4.subs({x: -4, y: -2}) - 8*sp.exp(-2)) == 0)
rng = np.random.default_rng(3)
def f4n(a, b): return (a**2 - 2*b**2)*np.exp(a - b)
d = rng.normal(size=(20000, 2))*0.1
check("Q4b (-4,-2) local max numeric", (f4n(-4 + d[:, 0], -2 + d[:, 1]) <= f4n(-4, -2) + 1e-12).all())
w = f4n(d[:, 0], d[:, 1])
check("Q4b origin saddle numeric", (w > 0).any() and (w < 0).any())

# ---- Q5a ----
f5 = sp.sqrt(x**2 + 2*y)
gr = [sp.diff(f5, x).subs({x: 4, y: 10}), sp.diff(f5, y).subs({x: 4, y: 10})]
check("Q5a gradient (2/3,1/6)", gr == [R(2, 3), R(1, 6)])
check("Q5a |grad|=sqrt(17)/6", sp.simplify(sp.sqrt(gr[0]**2 + gr[1]**2) - sp.sqrt(17)/6) == 0)
check("Q5a direction (4,1)/sqrt17", [sp.simplify(c/sp.sqrt(gr[0]**2 + gr[1]**2)) for c in gr] == [4/sp.sqrt(17), 1/sp.sqrt(17)])
th_ = np.linspace(0, 2*np.pi, 200001)
dd = (2/3)*np.cos(th_) + (1/6)*np.sin(th_)
check("Q5a numeric max directional derivative sqrt17/6", abs(dd.max() - math.sqrt(17)/6) < 1e-9)

# ---- Q5b ----
f6 = sp.log(1 + x**2) - sp.exp(2*x)
ser = sp.series(f6, x, 0, 9).removeO()
a6 = ser.coeff(x, 6)
check("Q5b a6 = 1/3 - 2^6/6!", a6 == R(1, 3) - R(64, 720))
check("Q5b f^(6)(0) = 176 (series)", a6*sp.factorial(6) == 176)
check("Q5b f^(6)(0) = 176 (derivative)", sp.diff(f6, x, 6).subs(x, 0) == 176)
check("Q5b coefficient pattern odd n: -2^n/n!", all(ser.coeff(x, i) == -R(2**i, math.factorial(i)) for i in (1, 3, 5, 7)))
check("Q5b coefficient pattern even n", all(ser.coeff(x, i) == (-1)**(i//2 + 1)*R(2, i) - R(2**i, math.factorial(i)) for i in (2, 4, 6, 8)))
check("Q5b radius of ln(1+x^2) is 1 (singularities at +-i)", set(sp.solve(1 + sp.Symbol("zc")**2, sp.Symbol("zc"))) == {sp.I, -sp.I})


# ---- region figures ----
def region_fig(name, polys, curves, title, xlim, ylim, labels):
    fig, ax = plt.subplots(figsize=(4.2, 3.6), dpi=150)
    for P in polys:
        ax.fill(*zip(*P), color="#fca5a5", alpha=0.55, zorder=1)
    for xs, ys, lab in curves:
        ax.plot(xs, ys, color="#7c3aed", lw=1.6, zorder=2)
    for (px, py, txt) in labels:
        ax.text(px, py, txt, fontsize=9, color="#111")
    ax.axhline(0, color="#888", lw=0.7); ax.axvline(0, color="#888", lw=0.7)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title(title, fontsize=10)
    fig.tight_layout(); fig.savefig(IMG / name, facecolor="white"); plt.close(fig)


sq = [(0, 1), (1, 0), (2, 1), (1, 2)]
region_fig("25A-A-Q2b-region.png", [sq],
           [([0, 1], [1, 0], ""), ([1, 2], [2, 1], ""), ([0, 1], [1, 2], ""), ([1, 2], [0, 1], "")],
           "R: x+y=1, x+y=3, y-x=1, y-x=-1", (-0.5, 2.6), (-0.5, 2.6),
           [(0.1, 0.4, "x+y=1"), (1.45, 1.75, "x+y=3"), (0.0, 1.65, "y=x+1"), (1.45, 0.3, "y=x-1")])
tri = [(0, 0), (1, 1), (1, 0)]
region_fig("25A-A-Q4a-region.png", [tri],
           [([0, 1], [0, 1], ""), ([1, 1], [0, 1], ""), ([0, 1], [0, 0], "")],
           "0<=y<=x, 0<=x<=1  (same as y<=x<=1, 0<=y<=1)", (-0.3, 1.4), (-0.3, 1.4),
           [(0.15, 0.62, "y=x"), (1.03, 0.4, "x=1"), (0.4, -0.15, "y=0")])

regions = [
    {"id": "25A-A-Q2b", "description": "square (rotated) with vertices (0,1),(1,0),(2,1),(1,2)", "type": "parallelogram",
     "inequalities": ["x+y>=1", "x+y<=3", "y-x<=1", "y-x>=-1"],
     "boundary_curves": ["y=1-x", "y=3-x", "y=x+1", "y=x-1"],
     "substitution": {"u": "x-y", "v": "x+y", "u_range": [-1, 1], "v_range": [1, 3], "abs_jacobian_xy_over_uv": "1/2"},
     "vertices": [[0, 1], [1, 0], [2, 1], [1, 2]],
     "integrand": "(x-y)*exp(x^2-y^2)", "value": "sinh(3)/3-sinh(1)"},
    {"id": "25A-A-Q4a", "description": "int_0^1 int_y^1 sin(pi x^2/2) dx dy: triangle 0<=y<=x<=1",
     "type": "simple",
     "orderYX": {"y": [0, 1], "x": ["y", 1]},
     "orderXY": {"x": [0, 1], "y": [0, "x"]},
     "inequalities": ["y>=0", "y<=x", "x<=1"],
     "boundary_curves": ["y=x", "x=1", "y=0"],
     "vertices": [[0, 0], [1, 0], [1, 1]],
     "integrand": "sin(pi*x^2/2)", "value": "1/pi"},
]
(HERE / "regions.json").write_text(json.dumps(regions, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
contours = [
    {"id": "25A-A-Q1b", "f": "y^4-x^4", "constraint": "x^2+y^2=9", "kind": "lagrange", "domain": [[-4, 4], [-4, 4]],
     "critical_points": [
         {"x": 0, "y": 3, "f": 81, "role": "abs max"}, {"x": 0, "y": -3, "f": 81, "role": "abs max"},
         {"x": 3, "y": 0, "f": -81, "role": "abs min"}, {"x": -3, "y": 0, "f": -81, "role": "abs min"},
         {"x": 0, "y": 0, "f": 0, "role": "interior critical point (not extremum)"}]},
    {"id": "25A-A-Q4b", "f": "(x^2-2*y^2)*exp(x-y)", "constraint": None, "kind": "unconstrained",
     "domain": [[-7, 3], [-5, 3]],
     "critical_points": [
         {"x": 0, "y": 0, "f": 0, "role": "saddle"},
         {"x": -4, "y": -2, "f": float(8*math.exp(-2)), "role": "local max"}]},
]
(HERE / "contours.json").write_text(json.dumps(contours, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ALL OK:", len(ok), "checks")
