# -*- coding: utf-8 -*-
"""sympy + numeric checks for sitting 25A-B (calculus-2, moed B 20/03/2025).
Run: PYTHONUTF8=1 py tools/verify/25A-B/check.py
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
x, y = sp.symbols("x y", real=True)
n = sp.symbols("n", integer=True, positive=True)
kk = sp.Symbol("kk", integer=True)
ok = []


def check(name, cond):
    assert cond, "MISMATCH: " + name
    ok.append(name)


# ---- Q1a: linear approximation of sqrt(41-4x^2-y^2) at (2,3) ----
f1 = sp.sqrt(41 - 4*x**2 - y**2)
check("Q1a f(2,3)=4", f1.subs({x: 2, y: 3}) == 4)
fx, fy = sp.diff(f1, x).subs({x: 2, y: 3}), sp.diff(f1, y).subs({x: 2, y: 3})
check("Q1a fx=-2, fy=-3/4", fx == -2 and fy == R(-3, 4))
approx = 4 + fx*R(1, 10) + fy*R(-1, 10)
check("Q1a linear approximation 3.875", approx == R(31, 8))
exact = math.sqrt(41 - 4*2.1**2 - 2.9**2)
check("Q1a exact value 3.8665 close to 3.875", abs(exact - 3.875) < 0.01)

# ---- Q1b: abs extrema of xy on x^2+y^2=2 ----
lam = sp.Symbol("lam")
L = x*y + lam*(x**2 + y**2 - 2)
sol = sp.solve([sp.diff(L, x), sp.diff(L, y), x**2 + y**2 - 2], [x, y, lam], dict=True)
vals = {(s[x], s[y]): (x*y).subs(s) for s in sol}
check("Q1b four points (+-1,+-1)", set(vals) == {(1, 1), (1, -1), (-1, 1), (-1, -1)})
check("Q1b values +-1", vals[(1, 1)] == 1 and vals[(-1, -1)] == 1 and vals[(1, -1)] == -1 and vals[(-1, 1)] == -1)
th_ = np.linspace(0, 2*np.pi, 200001)
fv = 2*np.cos(th_)*np.sin(th_)
check("Q1b numeric max 1 / min -1", abs(fv.max() - 1) < 1e-9 and abs(fv.min() + 1) < 1e-9)

# ---- Q2a ----
Sn = sp.summation(1/(kk*(kk - 1)), (kk, 2, n))
check("Q2a S_n = 1-1/n", sp.simplify(Sn - (1 - 1/n)) == 0)
check("Q2a sum = 1", sp.summation(1/(n*(n - 1)), (n, 2, sp.oo)) == 1)

# ---- Q2b: (y-x)/(2x+y) over parallelogram ----
tt, vv = sp.symbols("tt vv")
X_ = (vv - tt)/3
Y_ = (vv + 2*tt)/3
check("Q2b inverse map: t=y-x, v=y+2x", sp.simplify((Y_ - X_) - tt) == 0 and sp.simplify((Y_ + 2*X_) - vv) == 0)
J = sp.Matrix([[sp.diff(X_, tt), sp.diff(X_, vv)], [sp.diff(Y_, tt), sp.diff(Y_, vv)]]).det()
check("Q2b |J|=1/3", abs(J) == R(1, 3))
check("Q2b integrand (y-x)/(2x+y) = t/v", sp.simplify((Y_ - X_)/(2*X_ + Y_) - tt/vv) == 0)
I2 = sp.integrate(sp.integrate(R(1, 3)*tt/vv, (tt, 1, 4)), (vv, 6, 8))
check("Q2b value (5/2) ln(4/3)", sp.simplify(I2 - R(5, 2)*sp.log(R(4, 3))) == 0)


def fxy(yy, xx):
    return (yy - xx)/(2*xx + yy)


def lo(xx):
    return max(1 + xx, 6 - 2*xx)


def hi(xx):
    return min(4 + xx, 8 - 2*xx)


brk = [2/3, 4/3, 5/3, 7/3]
num2 = sum(si.dblquad(fxy, a, b, lo, hi)[0] for a, b in zip(brk[:-1], brk[1:]))
check("Q2b numeric double integral", abs(num2 - float(R(5, 2)*sp.log(R(4, 3)))) < 1e-7)

# ---- Q3a: sum sin^2(1/n)(x-1)^n ----
an = sp.sin(1/n)**2
check("Q3a ratio a_n/a_{n+1} -> 1 so R=1", sp.limit(an/an.subs(n, n + 1), n, sp.oo) == 1)
check("Q3a sin^2(1/n)/(1/n^2) -> 1", sp.limit(an/(1/n**2), n, sp.oo) == 1)
check("Q3a sum 1/n^2 converges", sp.summation(1/n**2, (n, 1, sp.oo)) == sp.pi**2/6)

# ---- Q3b: z = y g(cos(x-y)) ----
G = sp.Function("g")
z = y*G(sp.cos(x - y))
check("Q3b z_x+z_y = z/y", sp.simplify(sp.diff(z, x) + sp.diff(z, y) - z/y) == 0)

# ---- Q4a: swap order (test integrands both ways) ----
for f in (x**2 + y, x*y + 1, sp.exp(x)*y):
    A = sp.integrate(sp.integrate(f, (y, 0, sp.sqrt(x + 4))), (x, -4, 0)) + sp.integrate(sp.integrate(f, (y, 0, 2 - x)), (x, 0, 2))
    B = sp.integrate(sp.integrate(f, (x, y**2 - 4, 2 - y)), (y, 0, 2))
    check("Q4a swapped order equals original for f=%s" % f, sp.simplify(A - B) == 0)

# ---- Q4b: x^3+8y^3-6xy+1 ----
f4 = x**3 + 8*y**3 - 6*x*y + 1
crit = sp.solve([sp.diff(f4, x), sp.diff(f4, y)], [x, y], dict=True)
cp = sorted((s[x], s[y]) for s in crit)
check("Q4b real critical points (0,0),(1,1/2)", cp == [(0, 0), (1, R(1, 2))])
check("Q4b (-1,1/2) fails 4y^2=x", 4*R(1, 4) != -1)
H = sp.hessian(f4, (x, y))
check("Q4b (0,0) saddle det=-36", H.subs({x: 0, y: 0}).det() == -36)
Hm = H.subs({x: 1, y: R(1, 2)})
check("Q4b (1,1/2) min: det=108, fxx=6", Hm.det() == 108 and Hm[0, 0] == 6)
check("Q4b f(1,1/2)=0", f4.subs({x: 1, y: R(1, 2)}) == 0)
rng = np.random.default_rng(5)


def f4n(a, b):
    return a**3 + 8*b**3 - 6*a*b + 1


d = rng.normal(size=(20000, 2))*0.05
check("Q4b (1,1/2) local min numeric", (f4n(1 + d[:, 0], 0.5 + d[:, 1]) >= f4n(1, 0.5) - 1e-12).all())
w = f4n(d[:, 0], d[:, 1]) - 1
check("Q4b origin saddle numeric", (w > 0).any() and (w < 0).any())

# ---- Q5a ----
f5 = y*sp.cos(x*y)
g5 = [sp.diff(f5, x).subs({x: 1, y: 0}), sp.diff(f5, y).subs({x: 1, y: 0})]
check("Q5a grad f(1,0)=(0,1)", g5 == [0, 1])
a_, b_ = sp.symbols("a b", real=True)
s5 = sp.solve([a_**2 + b_**2 - 1, g5[0]*a_ + g5[1]*b_ - 1], [a_, b_], dict=True)
check("Q5a unique unit v with D_v f=1 is (0,1)", s5 == [{a_: 0, b_: 1}])

# ---- Q5b ----
f6 = 1/(x**2 - 5*x + 6)
ser = sp.series(f6, x, 0, 9).removeO()
check("Q5b a_n = 1/2^(n+1) - 1/3^(n+1)", all(ser.coeff(x, i) == R(1, 2**(i + 1)) - R(1, 3**(i + 1)) for i in range(9)))
check("Q5b radius 2 (poles 2, 3)", min(sp.solve(x**2 - 5*x + 6, x)) == 2)
val = sp.factorial(5)*(R(1, 64) - R(1, 729))
check("Q5b f^(5)(0) via derivative", sp.diff(f6, x, 5).subs(x, 0) == val)
print("f^(5)(0) =", val, "=", float(val), "(official solution prints approx 1.71166)")
check("Q5b official decimal 1.71166 is not the value (flag)", abs(float(val) - 1.71166) > 1e-3)


def region_fig(name, poly, title, xlim, ylim, labels):
    fig, ax = plt.subplots(figsize=(4.4, 3.6), dpi=150)
    ax.fill(*zip(*poly), color="#fca5a5", alpha=0.55, zorder=1)
    ax.plot(*zip(*(poly + [poly[0]])), color="#7c3aed", lw=1.6, zorder=2)
    for (px, py, txt) in labels:
        ax.text(px, py, txt, fontsize=9, color="#111")
    ax.axhline(0, color="#888", lw=0.7)
    ax.axvline(0, color="#888", lw=0.7)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title, fontsize=10)
    fig.tight_layout()
    fig.savefig(IMG / name, facecolor="white")
    plt.close(fig)


region_fig("25A-B-Q2b-region.png", [(5/3, 8/3), (7/3, 10/3), (4/3, 16/3), (2/3, 14/3)],
           "D: y-x in [1,4], y+2x in [6,8]", (-0.3, 3.3), (-0.3, 6),
           [(2.35, 3.1, "y=8-2x"), (0.0, 3.6, "y=6-2x"), (0.2, 4.9, "y=x+4"), (1.9, 2.4, "y=x+1")])
ys = np.linspace(0, 2, 120)
poly = [(-4, 0)] + [(float(yy**2 - 4), float(yy)) for yy in ys[1:]] + [(2, 0)]
region_fig("25A-B-Q4a-region.png", poly,
           "x=y^2-4, y=2-x, y=0", (-4.6, 3), (-0.6, 2.8),
           [(-3.9, 1.5, "y=sqrt(x+4)"), (1.1, 1.2, "y=2-x"), (-1.5, 0.3, "I"), (0.3, 0.3, "II")])

regions = [
    {"id": "25A-B-Q2b", "description": "parallelogram between y=1+x, y=4+x, y=8-2x, y=6-2x", "type": "parallelogram",
     "inequalities": ["y-x>=1", "y-x<=4", "y+2*x>=6", "y+2*x<=8"],
     "boundary_curves": ["y=x+1", "y=x+4", "y=8-2*x", "y=6-2*x"],
     "substitution": {"u": "y-x", "v": "y+2*x", "u_range": [1, 4], "v_range": [6, 8], "abs_jacobian_xy_over_uv": "1/3"},
     "vertices": [["5/3", "8/3"], ["7/3", "10/3"], ["4/3", "16/3"], ["2/3", "14/3"]],
     "integrand": "(y-x)/(2*x+y)", "value": "(5/2)*ln(4/3)"},
    {"id": "25A-B-Q4a", "description": "two iterated integrals = one region: x in [-4,2], y>=0, x>=y^2-4, x+y<=2",
     "type": "swap",
     "orderXY": {"pieces": [{"x": [-4, 0], "y": [0, "sqrt(x+4)"]}, {"x": [0, 2], "y": [0, "2-x"]}]},
     "orderYX": {"y": [0, 2], "x": ["y^2-4", "2-y"]},
     "inequalities": ["y>=0", "x>=y^2-4", "x+y<=2"],
     "boundary_curves": ["x=y^2-4", "y=2-x", "y=0"],
     "vertices": [[-4, 0], [0, 2], [2, 0]]},
]
(HERE / "regions.json").write_text(json.dumps(regions, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
contours = [
    {"id": "25A-B-Q1b", "f": "x*y", "constraint": "x^2+y^2=2", "kind": "lagrange", "domain": [[-2, 2], [-2, 2]],
     "critical_points": [
         {"x": 1, "y": 1, "f": 1, "role": "abs max"}, {"x": -1, "y": -1, "f": 1, "role": "abs max"},
         {"x": 1, "y": -1, "f": -1, "role": "abs min"}, {"x": -1, "y": 1, "f": -1, "role": "abs min"}]},
    {"id": "25A-B-Q4b", "f": "x^3+8*y^3-6*x*y+1", "constraint": None, "kind": "unconstrained",
     "domain": [[-1.5, 2], [-1, 1.5]],
     "critical_points": [{"x": 0, "y": 0, "f": 1, "role": "saddle"}, {"x": 1, "y": 0.5, "f": 0, "role": "local min"}]},
]
(HERE / "contours.json").write_text(json.dumps(contours, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ALL OK:", len(ok), "checks")
