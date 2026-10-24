# -*- coding: utf-8 -*-
"""sympy + numeric checks for sitting 23A-A (calculus-2, moed A 12/02/2023).
Run: PYTHONUTF8=1 py tools/verify/23A-A/check.py
Also writes regions.json and contours.json next to this file."""
import json, pathlib, math
import sympy as sp
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
R = sp.Rational
x, y, z, t, u, v, h, lam = sp.symbols("x y z t u v h lam", real=True)
r, th = sp.symbols("r theta", positive=True)
n = sp.symbols("n", positive=True)
ok = []


def check(name, cond):
    assert cond, "MISMATCH: " + name
    ok.append(name)


# ---- Q1a: polar integral of arctan(y/x) over the annular sector ----
I1 = sp.integrate(sp.integrate(th*r, (th, sp.pi/4, sp.pi/3)), (r, 1, 2))
check("Q1a value 7 pi^2/192", sp.simplify(I1 - 7*sp.pi**2/192) == 0)
check("Q1a arctan(tan th)=th for th in (pi/4,pi/3)",
      all(abs(math.atan(math.tan(a)) - a) < 1e-12 for a in np.linspace(math.pi/4, math.pi/3, 50)))
xs = np.linspace(1e-6, 2, 2000)
ys = np.linspace(1e-6, 2, 2000)
dx = xs[1] - xs[0]; dy = ys[1] - ys[0]
X, Y = np.meshgrid(xs, ys)
mask = (X**2 + Y**2 >= 1) & (X**2 + Y**2 <= 4) & (Y >= X) & (Y <= math.sqrt(3)*X)
num1 = float((np.arctan(Y/X)*mask).sum()*dx*dy)
check("Q1a numeric grid", abs(num1 - float(7*sp.pi**2/192)) < 5e-3)

# ---- Q1b: gradient of ln(x^2+y^2+z^2) at (1,2,1) ----
f1 = sp.log(x**2 + y**2 + z**2)
g1 = [sp.diff(f1, s).subs({x: 1, y: 2, z: 1}) for s in (x, y, z)]
check("Q1b gradient (1/3,2/3,1/3)", g1 == [R(1, 3), R(2, 3), R(1, 3)])
check("Q1b |grad| = sqrt6/3", sp.simplify(sp.sqrt(sum(c**2 for c in g1)) - sp.sqrt(6)/3) == 0)
best = max(float(g1[0])*math.cos(a)*math.sin(b) + float(g1[1])*math.sin(a)*math.sin(b) + float(g1[2])*math.cos(b)
           for a in np.linspace(0, 2*math.pi, 361) for b in np.linspace(0, math.pi, 181))
check("Q1b max directional derivative numeric ~ sqrt6/3", abs(best - math.sqrt(6)/3) < 1e-3)

# ---- Q2a: series ----
a = [math.sin(math.pi/k) for k in range(2, 400)]
check("Q2a sin(pi/n) decreasing for n>=2", all(a[i] > a[i+1] for i in range(len(a)-1)))
check("Q2a limit comparison sin(pi/n)/(1/n) -> pi", sp.limit(sp.sin(sp.pi/n)*n, n, sp.oo) == sp.pi)
check("Q2a limit comparison ln(1+n^(-4/3))/n^(-4/3) -> 1",
      sp.limit(sp.log(1 + n**R(-4, 3))/n**R(-4, 3), n, sp.oo) == 1)
s_abs = [sum(math.sin(math.pi/k) for k in range(2, N)) for N in (1000, 100000)]
check("Q2a first series: abs partial sums keep growing", s_abs[1] - s_abs[0] > 5)
s_alt = [sum((-1)**k*math.sin(math.pi/k) for k in range(2, N)) for N in (100000, 100001, 100002)]
check("Q2a first series: alternating partial sums settle", abs(s_alt[2] - s_alt[0]) < 1e-4)
s2 = [sum(math.log(1 + 1/(k*k**(1/3))) for k in range(1, N)) for N in (10**4, 10**6)]
check("Q2a second series: abs partial sums converge", abs(s2[1] - s2[0]) < 0.2)

# ---- Q2b: (x^2+y^2) sin(1/sqrt(x^2+y^2)) ----
check("Q2b squeeze |f|<=r^2", all(abs((r_**2)*math.sin(1/r_)) <= r_**2 for r_ in np.linspace(1e-4, 1, 500)))
check("Q2b sympy: limit r*sin(1/r) = 0", sp.limit(sp.symbols("s", positive=True)*sp.sin(1/sp.symbols("s", positive=True)),
                                                  sp.symbols("s", positive=True), 0) == 0)
check("Q2b fx(0,0): |h sin(1/|h|)| <= |h|", all(abs(hh*math.sin(1/abs(hh))) <= abs(hh) for hh in np.linspace(1e-6, 1e-1, 300)))

# ---- Q3a: radius and endpoints of sum x^n 3^n/((2n+1)^2 sqrt(5^n)) ----
an = 3**n/((2*n + 1)**2*sp.sqrt(5**n))
Rad = sp.limit(an/an.subs(n, n + 1), n, sp.oo)
check("Q3a radius sqrt5/3", sp.simplify(Rad - sp.sqrt(5)/3) == 0)
xe = sp.sqrt(5)/3
check("Q3a endpoint: term = 1/(2n+1)^2", sp.simplify(sp.powsimp(sp.expand_power_base(an*xe**n, force=True), force=True) - 1/(2*n + 1)**2) == 0)
check("Q3a endpoint: comparison with 1/n^2 (limit 1/4)", sp.limit((1/(2*n + 1)**2)/(1/n**2), n, sp.oo) == R(1, 4))

# ---- Q3b: identity x^2 g_x + y^2 g_y = -(x+y)/z g_z ----
A, B = sp.symbols("A B")  # A = f_u, B = f_v at (u,v)
U = 1/y - 1/x
V = x*y*sp.exp(-z**2/2)
gx = A*sp.diff(U, x) + B*sp.diff(V, x)
gy = A*sp.diff(U, y) + B*sp.diff(V, y)
gz = B*sp.diff(V, z)
lhs = x**2*gx + y**2*gy
rhs = -(x + y)/z*gz
check("Q3b identity", sp.simplify(lhs - rhs) == 0)
check("Q3b g_z = -f_v x y z e^(-z^2/2)", sp.simplify(gz + B*x*y*z*sp.exp(-z**2/2)) == 0)
check("Q3b both sides = f_v e^(-z^2/2) (x^2 y + x y^2)", sp.simplify(lhs - B*sp.exp(-z**2/2)*(x**2*y + x*y**2)) == 0)

# ---- Q4a: x^2+2xy over the curvilinear quadrilateral ----
Uu = y*x**2; Vv = y - x
Jinv = sp.Matrix([[sp.diff(Uu, x), sp.diff(Uu, y)], [sp.diff(Vv, x), sp.diff(Vv, y)]]).det()
check("Q4a 1/J = 2xy + x^2", sp.simplify(Jinv - (2*x*y + x**2)) == 0)
check("Q4a integrand * |J| = 1", sp.simplify((x**2 + 2*x*y)/Jinv) == 1)
check("Q4a value 6", sp.integrate(sp.integrate(1, (u, 1, 4)), (v, -1, 1)) == 6)
xs = np.linspace(1e-4, 6, 3001); ys = np.linspace(1e-4, 7, 3501)
X, Y = np.meshgrid(xs, ys)
mask = (Y*X**2 >= 1) & (Y*X**2 <= 4) & (np.abs(Y - X) <= 1)
num4 = float(((X**2 + 2*X*Y)*mask).sum()*(xs[1]-xs[0])*(ys[1]-ys[0]))
check("Q4a numeric grid ~6", abs(num4 - 6) < 0.05)

# ---- Q4b: abs extrema of 1-x^2-y^2 on (x-1)^2+(y-1)^2<=1 ----
f4 = 1 - x**2 - y**2
check("Q4b interior critical point (0,0) is outside D", (0 - 1)**2 + (0 - 1)**2 > 1)
L = f4 - lam*((x - 1)**2 + (y - 1)**2 - 1)
sol = sp.solve([sp.diff(L, x), sp.diff(L, y), (x - 1)**2 + (y - 1)**2 - 1], [x, y, lam], dict=True)
pts = sorted([(sp.simplify(s[x]), sp.simplify(s[y])) for s in sol], key=lambda p: float(p[0]))
M2 = (1 - sp.sqrt(2)/2, 1 - sp.sqrt(2)/2); M1 = (1 + sp.sqrt(2)/2, 1 + sp.sqrt(2)/2)
check("Q4b Lagrange points M1, M2",
      len(pts) == 2 and all(sp.simplify(a_ - b_) == 0 for a_, b_ in zip(pts[0], M2))
      and all(sp.simplify(a_ - b_) == 0 for a_, b_ in zip(pts[1], M1)))
fM1 = sp.simplify(f4.subs({x: M1[0], y: M1[1]})); fM2 = sp.simplify(f4.subs({x: M2[0], y: M2[1]}))
check("Q4b f(M1) = -2-2sqrt2 (min)", sp.simplify(fM1 - (-2 - 2*sp.sqrt(2))) == 0)
check("Q4b f(M2) = -2+2sqrt2 (max)", sp.simplify(fM2 - (-2 + 2*sp.sqrt(2))) == 0)
tt = np.linspace(0, 2*math.pi, 200001)
vals = 1 - (1 + np.cos(tt))**2 - (1 + np.sin(tt))**2
check("Q4b dense boundary max/min", abs(vals.max() - float(fM2)) < 1e-6 and abs(vals.min() - float(fM1)) < 1e-6)
gx_, gy_ = np.meshgrid(np.linspace(0, 2, 801), np.linspace(0, 2, 801))
inD = (gx_ - 1)**2 + (gy_ - 1)**2 <= 1
fv_ = (1 - gx_**2 - gy_**2)[inD]
check("Q4b dense disk grid inside [min,max]", fv_.max() <= float(fM2) + 1e-9 and fv_.min() >= float(fM1) - 1e-9)

# ---- Q5a: f=(x+y)^2-4y^2-48y ----
f5 = (x + y)**2 - 4*y**2 - 48*y
s5 = sp.solve([sp.diff(f5, x), sp.diff(f5, y)], [x, y], dict=True)
check("Q5a single critical point (6,-6)", s5 == [{x: 6, y: -6}])
H5 = sp.hessian(f5, (x, y))
check("Q5a A=2, B=2, C=-6, Delta=-16", (H5[0, 0], H5[0, 1], H5[1, 1]) == (2, 2, -6) and H5.det() == -16)
check("Q5a (-6,6), as printed in the official solution, is NOT critical", sp.diff(f5, y).subs({x: -6, y: 6}) != 0)

# ---- Q5b: 1/(x^2+x-6) ----
f6 = 1/(x**2 + x - 6)
check("Q5b partial fractions", sp.simplify(f6 - (-R(1, 5)/(x + 3) + R(1, 5)/(x - 2))) == 0)
an6 = lambda k: -R(1, 5)*((-1)**k/R(3)**(k + 1) + 1/R(2)**(k + 1))
ser = sp.series(f6, x, 0, 14).removeO()
check("Q5b first 14 Maclaurin coefficients", all(ser.coeff(x, k) == an6(k) for k in range(14)))
val10 = -sp.factorial(10)/5*(R(1, 3**11) + R(1, 2**11))
check("Q5b f^(10)(0)", sp.simplify(sp.diff(f6, x, 10).subs(x, 0) - val10) == 0)
check("Q5b radius 2 (nearest pole x=2)", min(abs(p) for p in sp.solve(x**2 + x - 6, x)) == 2)
print("f^(10)(0) =", val10, "~", float(val10))

# ---- regions.json ----
regions = [
    {"id": "23A-A-Q1a", "description": "annular sector 1<=x^2+y^2<=4, x<=y<=sqrt(3) x, x>=0 (polar: 1<=r<=2, pi/4<=theta<=pi/3)",
     "type": "polar",
     "polar": {"r": [1, 2], "theta": ["pi/4", "pi/3"]},
     "inequalities": ["x>=0", "x^2+y^2>=1", "x^2+y^2<=4", "y>=x", "y<=sqrt(3)*x"],
     "boundary_curves": ["x^2+y^2=1", "x^2+y^2=4", "y=x", "y=sqrt(3)*x"],
     "integrand": "atan(y/x)", "value": "7*pi^2/192"},
    {"id": "23A-A-Q4a", "description": "x>0,y>0 between y=1/x^2 and y=4/x^2 and between y=x-1 and y=x+1",
     "type": "curvilinear",
     "inequalities": ["x>0", "y>0", "y*x^2>=1", "y*x^2<=4", "y>=x-1", "y<=x+1"],
     "boundary_curves": ["y=1/x^2", "y=4/x^2", "y=x+1", "y=x-1"],
     "substitution": {"u": "y*x^2", "v": "y-x", "u_range": [1, 4], "v_range": [-1, 1],
                      "abs_jacobian_xy_over_uv": "1/(2*x*y+x^2)"},
     "integrand": "x^2+2*x*y", "value": "6"},
]
(HERE / "regions.json").write_text(json.dumps(regions, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

# ---- contours.json ----
contours = [
    {"id": "23A-A-Q4b", "f": "1-x^2-y^2", "constraint": "(x-1)^2+(y-1)^2=1", "kind": "lagrange",
     "domain": [[-0.5, 2.5], [-0.5, 2.5]],
     "critical_points": [
         {"x": "1-sqrt(2)/2", "y": "1-sqrt(2)/2", "f": float(fM2), "role": "abs max"},
         {"x": "1+sqrt(2)/2", "y": "1+sqrt(2)/2", "f": float(fM1), "role": "abs min"}]},
    {"id": "23A-A-Q5a", "f": "(x+y)^2-4*y^2-48*y", "constraint": None, "kind": "unconstrained",
     "domain": [[-6, 18], [-14, 2]],
     "critical_points": [{"x": 6, "y": -6, "f": float(f5.subs({x: 6, y: -6})), "role": "saddle"}]},
]
(HERE / "contours.json").write_text(json.dumps(contours, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ALL OK:", len(ok), "checks")
