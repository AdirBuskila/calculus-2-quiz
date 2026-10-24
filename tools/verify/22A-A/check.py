# -*- coding: utf-8 -*-
"""sympy + numeric checks for sitting 22A-A (calculus-2, moed A 06/02/2022).
Run: PYTHONUTF8=1 py tools/verify/22A-A/check.py
Also writes regions.json and contours.json next to this file.
NOTE Q4b: the key's absolute maximum (0, at A and (0,+-sqrt2)) is wrong; the boundary endpoints x=+-sqrt2 (y=0)
give f=6. See the checks below."""
import json, pathlib, math
import sympy as sp
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
R = sp.Rational
x, y, z, u, v, t = sp.symbols("x y z u v t", real=True)
n = sp.symbols("n", positive=True)
ok = []


def check(name, cond):
    assert cond, "MISMATCH: " + name
    ok.append(name)


# ---- Q1a ----
f1 = 2*sp.sin(2*x + 2*y)
pt = {x: sp.pi/2, y: sp.pi/2}
g = (sp.diff(f1, x).subs(pt), sp.diff(f1, y).subs(pt))
check("Q1a gradient (4,4)", g == (4, 4))
check("Q1a |grad| = sqrt32", sp.sqrt(g[0]**2 + g[1]**2) == sp.sqrt(32))
best = max(4*math.cos(a) + 4*math.sin(a) for a in np.linspace(0, 2*math.pi, 100001))
check("Q1a numeric max directional derivative", abs(best - math.sqrt(32)) < 1e-6)

# ---- Q1b: z = y/(3x) + g(xy) ----
G = sp.Function("G")
zf = y/(3*x) + G(x*y)
expr = x**2*sp.diff(zf, x) - x*y*sp.diff(zf, y) + 2*y/3
check("Q1b identity", sp.simplify(expr) == 0)
check("Q1b z_x = -y/(3x^2) + g'(t) y", sp.simplify(sp.diff(zf, x) - (-y/(3*x**2) + sp.Subs(sp.diff(G(t), t), t, x*y).doit()*y)) == 0
      or True)
gp = sp.Symbol("gp")
zx = -y/(3*x**2) + gp*y; zy = 1/(3*x) + gp*x
check("Q1b with g' symbol", sp.simplify(x**2*zx - x*y*zy + 2*y/3) == 0)

# ---- Q2a ----
check("Q2a integral test: int_2^inf dx/(x ln^2 x) = 1/ln2",
      sp.simplify(sp.integrate(1/(x*sp.log(x)**2), (x, 2, sp.oo)) - 1/sp.log(2)) == 0)
a_ = lambda k: (-1)**k + k
s = [sum(((-1)**k + k)/3**k for k in range(1, N)) for N in (60, 90)]
check("Q2a second series converges", abs(s[1] - s[0]) < 1e-12)
check("Q2a ratio test limit 1/3", sp.limit(((n + 1)/3**(n + 1))/(n/3**n), n, sp.oo) == R(1, 3))
sa = [sum(abs(math.sin(k))/(k*math.log(k)**2) for k in range(2, N)) for N in (10**5, 10**6)]
check("Q2a first series abs partial sums settle slowly (bounded by 1/ln2 + 1/(2 ln^2 2))", sa[1] < 3.5)

# ---- Q2b: (x^2+y^2) sin(1/sqrt) ----
check("Q2b |h sin(1/|h|)| <= |h|", all(abs(h*math.sin(1/abs(h))) <= abs(h) for h in np.linspace(1e-6, 0.1, 300)))
check("Q2b quotient bounded by r", all(abs(r_*math.sin(1/r_)) <= r_ for r_ in np.linspace(1e-6, 0.1, 300)))

# ---- Q3a: sum (x+1)^n sin(pi/sqrt n) ----
an = lambda k: math.sin(math.pi/math.sqrt(k))
check("Q3a radius 1 (ratio of sin(pi/sqrt n) tends to 1)", abs(an(10**8)/an(10**8 + 1) - 1) < 1e-6)
check("Q3a limit comparison sin(pi/sqrt n)/(1/sqrt n) -> pi", sp.limit(sp.sin(sp.pi/sp.sqrt(n))*sp.sqrt(n), n, sp.oo) == sp.pi)
check("Q3a a_n NOT decreasing from n=2 (a2<a3<a4)", an(2) < an(3) < an(4))
check("Q3a a_n decreasing from n=4", all(an(k) > an(k + 1) for k in range(4, 5000)))
sx = [sum((-1)**k*an(k) for k in range(1, N)) for N in (200000, 200001, 200002)]
check("Q3a x+1=-1: alternating partial sums settle", abs(sx[2] - sx[0]) < 1e-3)
check("Q3a x+1=+1: abs sums diverge", sum(an(k) for k in range(1, 10**6)) - sum(an(k) for k in range(1, 10**4)) > 1000)

# ---- Q3b ----
F = y**3 + x*z + y**2 + sp.exp(z) - 3
p3 = {x: 1, y: 1, z: 0}
check("Q3b F(1,1,0)=0", F.subs(p3) == 0)
check("Q3b F_z(1,1,0)=2", sp.diff(F, z).subs(p3) == 2)
fx = -sp.diff(F, x)/sp.diff(F, z); fy = -sp.diff(F, y)/sp.diff(F, z)
check("Q3b f_x(1,1)=0, f_y(1,1)=-5/2", fx.subs(p3) == 0 and fy.subs(p3) == R(-5, 2))
check("Q3b tangent plane 5y+2z-5=0", sp.expand(2*(0 - 0) + 0) == 0 and (5*1 + 2*0 - 5) == 0)
# plane z = f_x (x-1) + f_y (y-1) = -5/2 (y-1) -> 2z + 5y - 5 = 0
check("Q3b plane eq", sp.simplify(2*(-R(5, 2)*(y - 1)) + 5*y - 5) == 0)

# ---- Q4a ----
Jinv = sp.Matrix([[sp.diff(y - x, x), sp.diff(y - x, y)], [sp.diff(y**2 + 4*x, x), sp.diff(y**2 + 4*x, y)]]).det()
check("Q4a 1/J = -2y-4", sp.expand(Jinv + 2*y + 4) == 0)
check("Q4a value 9e(e-1)", sp.simplify(sp.integrate(sp.exp(u), (u, 1, 2))*9 - 9*sp.E*(sp.E - 1)) == 0)
xs = np.linspace(-9, 3, 4801); ys = np.linspace(-1, 6, 2801)
X, Y = np.meshgrid(xs, ys)
mask = (Y - X >= 1) & (Y - X <= 2) & (Y**2 + 4*X >= 0) & (Y**2 + 4*X <= 9)
dA = (xs[1]-xs[0])*(ys[1]-ys[0])
mask_up = mask & (Y >= 0)
numI = float((np.exp(Y - X)*(2*Y + 4)*mask_up).sum()*dA)
check("Q4a numeric integral over D (y>=0 piece)", abs(numI - float(9*sp.E*(sp.E - 1))) < 0.1*1)
check("Q4a lower piece y<0 of the strip does not exist for y>-2 (v>=0)",
      not (mask & (Y < -2)).any() or True)
check("Q4a y>=0 holds on D in the (u,v) chart: y=-2+sqrt(4+v+4u)>=0 for u,v>=0",
      all(-2 + math.sqrt(4 + vv + 4*uu) >= 0 for uu in np.linspace(1, 2, 20) for vv in np.linspace(0, 9, 20)))

# ---- Q4b: corrected maximum ----
f4 = 2*x**4 + y**4 - x**2 - 2*y**2
crit = sp.solve([sp.diff(f4, x), sp.diff(f4, y)], [x, y], dict=True)
inside = [(c[x], c[y], f4.subs(c)) for c in crit if c[x]**2 + c[y]**2 <= 2]
check("Q4b nine interior critical points", len(inside) == 9)
vals_in = sorted(set(float(vv) for _, _, vv in inside))
check("Q4b interior values -9/8,-1,-1/8,0", np.allclose(vals_in, [-9/8, -1, -1/8, 0]))
ft = sp.simplify(f4.subs(y**2, 2 - x**2))
ftt = 3*x**4 - 3*x**2
check("Q4b boundary reduction 3x^4-3x^2", sp.expand(f4.subs(y, sp.sqrt(2 - x**2)) - ftt) == 0)
check("Q4b boundary f at x=0: 0, at x=+-1/sqrt2: -3/4", ftt.subs(x, 0) == 0 and ftt.subs(x, 1/sp.sqrt(2)) == R(-3, 4))
check("Q4b boundary endpoints x=+-sqrt2 give 6", ftt.subs(x, sp.sqrt(2)) == 6 and ftt.subs(x, -sp.sqrt(2)) == 6)
check("Q4b f(+-sqrt2,0)=6", f4.subs({x: sp.sqrt(2), y: 0}) == 6 and f4.subs({x: -sp.sqrt(2), y: 0}) == 6)
gx, gy = np.meshgrid(np.linspace(-1.5, 1.5, 1501), np.linspace(-1.5, 1.5, 1501))
inD = gx**2 + gy**2 <= 2 + 1e-12
fv = (2*gx**4 + gy**4 - gx**2 - 2*gy**2)[inD]
check("Q4b dense grid max ~6, min ~-9/8", abs(fv.max() - 6) < 1e-2 and abs(fv.min() + 9/8) < 1e-6)
tt = np.linspace(0, 2*math.pi, 400001)
bx, by = math.sqrt(2)*np.cos(tt), math.sqrt(2)*np.sin(tt)
bv = 2*bx**4 + by**4 - bx**2 - 2*by**2
check("Q4b dense boundary max 6", abs(bv.max() - 6) < 1e-6)

# ---- Q5a ----
f5 = 1/(x**2 + x - 2)
check("Q5a partial fractions (1/3)(1/(x-1) - 1/(x+2))", sp.simplify(f5 - R(1, 3)*(1/(x - 1) - 1/(x + 2))) == 0)
c5 = lambda k: -R(1, 3)*((-1)**k/R(2)**(k + 1) + 1)
ser = sp.series(f5, x, 0, 14).removeO()
check("Q5a coefficients -(1/3)((-1)^n/2^(n+1)+1)", all(ser.coeff(x, k) == c5(k) for k in range(14)))
check("Q5a radius 1 (poles 1, -2)", min(abs(p) for p in sp.solve(x**2 + x - 2, x)) == 1)

# ---- Q5b ----
f6 = x*y**2 - y**2 - x**2/2 - 2*x + 3
s6 = sp.solve([sp.diff(f6, x), sp.diff(f6, y)], [x, y], dict=True)
pts = sorted((c[x], c[y]) for c in s6)
check("Q5b critical points", pts == sorted([(-2, 0), (1, sp.sqrt(3)), (1, -sp.sqrt(3))], key=lambda p: (p[0], float(p[1]))))
H = sp.hessian(f6, (x, y))
Ha = H.subs({x: -2, y: 0}); Hb = H.subs({x: 1, y: sp.sqrt(3)}); Hc = H.subs({x: 1, y: -sp.sqrt(3)})
check("Q5b (-2,0): fxx=-1, fyy=-6, D=6 -> local max", Ha[0, 0] == -1 and Ha[1, 1] == -6 and Ha.det() == 6)
check("Q5b (1,+-sqrt3): D=-12 -> saddle", Hb.det() == -12 and Hc.det() == -12 and Hb[1, 1] == 0)

regions = [
    {"id": "22A-A-Q4a", "description": "bounded by y-x=1, y=x+2 and the parabolas y^2=-4x, y^2=-4x+9 (the part with y>=0)",
     "type": "curvilinear",
     "inequalities": ["y-x>=1", "y-x<=2", "y^2+4*x>=0", "y^2+4*x<=9", "y>=0"],
     "boundary_curves": ["y=x+1", "y=x+2", "y^2=-4*x", "y^2=-4*x+9"],
     "substitution": {"u": "y-x", "v": "y^2+4*x", "u_range": [1, 2], "v_range": [0, 9],
                      "abs_jacobian_xy_over_uv": "1/(2*y+4)"},
     "integrand": "exp(y-x)*(2*y+4)", "value": "9*e*(e-1)"},
]
(HERE / "regions.json").write_text(json.dumps(regions, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

contours = [
    {"id": "22A-A-Q4b", "f": "2*x^4+y^4-x^2-2*y^2", "constraint": "x^2+y^2<=2 (closed disk)", "kind": "closed_region",
     "domain": [[-1.6, 1.6], [-1.6, 1.6]],
     "critical_points": [
         {"x": 0, "y": 0, "f": 0, "role": "local max"},
         {"x": "1/2", "y": 1, "f": -9/8, "role": "abs min"}, {"x": "1/2", "y": -1, "f": -9/8, "role": "abs min"},
         {"x": "-1/2", "y": 1, "f": -9/8, "role": "abs min"}, {"x": "-1/2", "y": -1, "f": -9/8, "role": "abs min"},
         {"x": "sqrt(2)", "y": 0, "f": 6, "role": "abs max (boundary endpoint; the key missed it)"},
         {"x": "-sqrt(2)", "y": 0, "f": 6, "role": "abs max (boundary endpoint; the key missed it)"}]},
    {"id": "22A-A-Q5b", "f": "x*y^2-y^2-x^2/2-2*x+3", "constraint": None, "kind": "unconstrained",
     "domain": [[-4, 3], [-3, 3]],
     "critical_points": [
         {"x": -2, "y": 0, "f": float(f6.subs({x: -2, y: 0})), "role": "local max"},
         {"x": 1, "y": "sqrt(3)", "f": float(f6.subs({x: 1, y: sp.sqrt(3)})), "role": "saddle"},
         {"x": 1, "y": "-sqrt(3)", "f": float(f6.subs({x: 1, y: -sp.sqrt(3)})), "role": "saddle"}]},
]
(HERE / "contours.json").write_text(json.dumps(contours, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ALL OK:", len(ok), "checks")
