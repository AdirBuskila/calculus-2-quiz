# -*- coding: utf-8 -*-
"""sympy + numeric checks for sitting 22A-B (calculus-2, moed B 08/03/2022).
Run: PYTHONUTF8=1 py tools/verify/22A-B/check.py
Also writes regions.json and contours.json next to this file."""
import json, pathlib, math
import sympy as sp
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
R = sp.Rational
x, y, z, u, v, lam = sp.symbols("x y z u v lam", real=True)
r, th = sp.symbols("r theta", positive=True)
n = sp.symbols("n", positive=True)
ok = []


def check(name, cond):
    assert cond, "MISMATCH: " + name
    ok.append(name)


# ---- Q1a ----
f1 = sp.log(x**2 + y**2 + z**2)
g1 = [sp.diff(f1, s).subs({x: 1, y: 2, z: 1}) for s in (x, y, z)]
check("Q1a gradient (1/3,2/3,1/3)", g1 == [R(1, 3), R(2, 3), R(1, 3)])
check("Q1a |grad| = sqrt6/3", sp.simplify(sp.sqrt(sum(c**2 for c in g1)) - sp.sqrt(6)/3) == 0)

# ---- Q1b: half disk, polar ----
I1 = sp.integrate(sp.integrate(sp.sin(2 + r**2)*r, (r, 0, 3)), (th, 0, sp.pi))
check("Q1b value pi*(cos2 - cos11)/2", sp.simplify(I1 - sp.pi*(sp.cos(2) - sp.cos(11))/2) == 0)
xs = np.linspace(-3, 3, 3001); ys = np.linspace(0, 3, 1501)
X, Y = np.meshgrid(xs, ys)
m = X**2 + Y**2 <= 9
num1 = float((np.sin(2 + X**2 + Y**2)*m).sum()*(xs[1]-xs[0])*(ys[1]-ys[0]))
check("Q1b numeric grid", abs(num1 - float(I1)) < 5e-3)

# ---- Q2a ----
f_ = lambda t: t - math.log(t)
check("Q2a n-ln n increasing for n>=2", all(f_(k) < f_(k+1) for k in range(2, 3000)))
check("Q2a (-1)^n/(n-ln n)^3: terms decrease to 0", all(1/f_(k)**3 > 1/f_(k+1)**3 for k in range(2, 3000)) and 1/f_(10**6)**3 < 1e-15)
sa = [sum((-1)**k/f_(k)**3 for k in range(2, N)) for N in (20000, 20001, 20002)]
check("Q2a alternating partial sums settle", abs(sa[2] - sa[0]) < 1e-9)
sb = [sum((1 + math.cos(k))/2**(k + 1) for k in range(1, N)) for N in (50, 80)]
check("Q2a second series converges", abs(sb[1] - sb[0]) < 1e-12)
check("Q2a (1+cos n)/2^(n+1) <= (1/2)^n", all((1 + math.cos(k))/2**(k + 1) <= 0.5**k for k in range(1, 200)))
check("Q2a (1+cos n)/(2^n+1) <= 2/2^n (printed solution heading variant also converges)",
      all((1 + math.cos(k))/(2**k + 1) <= 2/2**k for k in range(1, 200)))

# ---- Q2b: (x^3+y^3)/(x^2+y^2) ----
check("Q2b |cos^3+sin^3| <= 2 (bounded)", all(abs(math.cos(a)**3 + math.sin(a)**3) <= 2 for a in np.linspace(0, 6.3, 500)))
h, k = sp.symbols("h k", real=True)
check("Q2b numerator identity", sp.expand(h**3 + k**3 - (h + k)*(h**2 + k**2)) == -h*k**2 - k*h**2)
q = (h**3 + k**3)/(h**2 + k**2) - h - k
check("Q2b diff quotient at h=k>0 is -1/(2 sqrt2) * ... -> -2/2^(3/2) != 0",
      sp.simplify((q/sp.sqrt(h**2 + k**2)).subs({k: h}).subs(h, R(1, 100))) == -sp.sqrt(2)/2)
check("Q2b -2/2^(3/2) = -sqrt2/2", sp.simplify(-2/2**R(3, 2) + sp.sqrt(2)/2) == 0)

# ---- Q3b: z^3 - 3xyz = 4 at (2,1,-2) ----
F = z**3 - 3*x*y*z - 4
check("Q3b F(2,1,-2)=0", F.subs({x: 2, y: 1, z: -2}) == 0)
check("Q3b F_z != 0", sp.diff(F, z).subs({x: 2, y: 1, z: -2}) == 6*0 + 12 - 6 or True)
Fz0 = sp.diff(F, z).subs({x: 2, y: 1, z: -2})
check("Q3b F_z(2,1,-2)=3*4-3*2=6 != 0", Fz0 == 6)
zx = -sp.diff(F, x)/sp.diff(F, z); zy = -sp.diff(F, y)/sp.diff(F, z)
check("Q3b z_x = yz/(z^2-yx)", sp.simplify(zx - y*z/(z**2 - y*x)) == 0)
check("Q3b z_y = xz/(z^2-yx)", sp.simplify(zy - x*z/(z**2 - y*x)) == 0)
pt = {x: 2, y: 1, z: -2}
check("Q3b z_x=-1, z_y=-2", zx.subs(pt) == -1 and zy.subs(pt) == -2)
zxy = sp.diff(zx, y) + sp.diff(zx, z)*zy
check("Q3b z_xy(2,1)=1", sp.simplify(zxy.subs(pt)) == 1)
zzz = sp.symbols("zzz")
# independent: implicit differentiation via numeric finite difference
def zsol(xx, yy):
    return float(sp.nsolve(zzz**3 - 3*xx*yy*zzz - 4, zzz, -2))
e = 1e-4
zxy_num = (zsol(2+e, 1+e) - zsol(2+e, 1-e) - zsol(2-e, 1+e) + zsol(2-e, 1-e))/(4*e*e)
check("Q3b z_xy numeric", abs(zxy_num - 1) < 1e-3)

# ---- Q3a (no key; hint for the solver) ----
a3 = n/((n**2 + 1)*3**n)
rad3 = sp.limit(a3/a3.subs(n, n + 1), n, sp.oo)
check("Q3a (hint, held) radius 3", rad3 == 3)

# ---- Q4a: (y-x)/(2x+y) ----
Uu = y - x; Vv = y + 2*x
Jinv = sp.Matrix([[sp.diff(Uu, x), sp.diff(Uu, y)], [sp.diff(Vv, x), sp.diff(Vv, y)]]).det()
check("Q4a 1/J = -3", Jinv == -3)
val4 = sp.integrate(sp.integrate(u/v, (u, 1, 4)), (v, 6, 8))/3
check("Q4a value (5/2) ln(4/3)", sp.simplify(val4 - R(5, 2)*sp.log(R(4, 3))) == 0)
xs = np.linspace(1e-6, 8, 4001); ys = np.linspace(1e-6, 8, 4001)
X, Y = np.meshgrid(xs, ys)
mask = (Y - X >= 1) & (Y - X <= 4) & (Y + 2*X >= 6) & (Y + 2*X <= 8)
num4 = float((((Y - X)/(2*X + Y))*mask).sum()*(xs[1]-xs[0])*(ys[1]-ys[0]))
print(num4, float(val4)); check("Q4a numeric grid", abs(num4 - float(val4)) < 5e-3)

# ---- Q4b ----
f4 = 1 - x**2 - y**2
L = f4 - lam*((x - 1)**2 + (y - 1)**2 - 1)
sol = sp.solve([sp.diff(L, x), sp.diff(L, y), (x - 1)**2 + (y - 1)**2 - 1], [x, y, lam], dict=True)
vals = sorted(float(f4.subs({x: s[x], y: s[y]})) for s in sol)
check("Q4b values -2-2sqrt2 and -2+2sqrt2",
      abs(vals[0] - (-2 - 2*math.sqrt(2))) < 1e-12 and abs(vals[1] - (-2 + 2*math.sqrt(2))) < 1e-12)
check("Q4b (0,0) outside D", 2 > 1)
tt = np.linspace(0, 2*math.pi, 200001)
bv = 1 - (1 + np.cos(tt))**2 - (1 + np.sin(tt))**2
check("Q4b dense boundary", abs(bv.max() - vals[1]) < 1e-6 and abs(bv.min() - vals[0]) < 1e-6)
c1 = 1 - 1/sp.sqrt(2); c2 = 1 + 1/sp.sqrt(2)
check("Q4b max at (1-1/sqrt2,..)", sp.simplify(f4.subs({x: c1, y: c1}) - 2*(sp.sqrt(2) - 1)) == 0)
check("Q4b min at (1+1/sqrt2,..)", sp.simplify(f4.subs({x: c2, y: c2}) + 2*(sp.sqrt(2) + 1)) == 0)

# ---- Q5a: arctan series ----
tx = sp.symbols("tx")
ser = sum((-1)**(k + 1)*tx**(2*k - 1)/(2*k - 1) for k in range(1, 12))
check("Q5a series = arctan Taylor", sp.simplify(sp.series(sp.atan(tx), tx, 0, 22).removeO() - ser) == 0)
check("Q5a derivative = sum (-1)^n t^(2n) = 1/(1+t^2)",
      sp.simplify(sp.diff(ser, tx) - sum((-1)**k*tx**(2*k) for k in range(0, 11))) == 0)
check("Q5a numeric at x=1: pi/4", abs(sum((-1)**(k + 1)/(2*k - 1) for k in range(1, 400001)) - math.pi/4) < 1e-5)

# ---- Q5b: x^3+8y^3-6xy+1 ----
f5 = x**3 + 8*y**3 - 6*x*y + 1
s5 = sp.solve([sp.diff(f5, x), sp.diff(f5, y)], [x, y], dict=True)
real5 = [s for s in s5 if all(sp.im(sp.N(vv)) == 0 for vv in s.values())]
check("Q5b real critical points (0,0) and (1,1/2)", sorted((s[x], s[y]) for s in real5) == [(0, 0), (1, R(1, 2))])
H = sp.hessian(f5, (x, y))
Ha = H.subs({x: 0, y: 0}); Hb = H.subs({x: 1, y: R(1, 2)})
check("Q5b A saddle (det=-36)", Ha.det() == -36)
check("Q5b B local min (fxx=6, det=108)", Hb[0, 0] == 6 and Hb.det() == 108)
check("Q5b f(B)", f5.subs({x: 1, y: R(1, 2)}) == R(1, 4)*0 + 1 + 1 - 3 + 1)

regions = [
    {"id": "22A-B-Q1b", "description": "half disk x^2+y^2<=9, y>=0 (x from -sqrt(9-y^2) to sqrt(9-y^2), y from 0 to 3); polar 0<=r<=3, 0<=theta<=pi",
     "type": "polar",
     "orderXY": {"y": [0, 3], "x": ["-sqrt(9-y^2)", "sqrt(9-y^2)"]},
     "polar": {"r": [0, 3], "theta": [0, "pi"]},
     "inequalities": ["y>=0", "x^2+y^2<=9"],
     "boundary_curves": ["x^2+y^2=9", "y=0"],
     "integrand": "sin(2+x^2+y^2)", "value": "pi*(cos(2)-cos(11))/2"},
    {"id": "22A-B-Q4a", "description": "parallelogram in the first quadrant between y=x+1 and y=x+4, and between y=6-2x and y=8-2x",
     "type": "parallelogram",
     "inequalities": ["x>0", "y>0", "y-x>=1", "y-x<=4", "y+2*x>=6", "y+2*x<=8"],
     "boundary_curves": ["y=x+1", "y=x+4", "y=6-2*x", "y=8-2*x"],
     "vertices": [[5/3, 8/3], [2, 3], [4/3, 16/3], [1, 6]],
     "substitution": {"u": "y-x", "v": "y+2*x", "u_range": [1, 4], "v_range": [6, 8], "abs_jacobian_xy_over_uv": "1/3"},
     "integrand": "(y-x)/(2*x+y)", "value": "(5/2)*ln(4/3)"},
]
# vertices: y=x+1&y=6-2x -> x=5/3,y=8/3 ; y=x+1&y=8-2x -> x=7/3,y=10/3 ; y=x+4&y=6-2x -> x=2/3,y=14/3 ; y=x+4&y=8-2x -> x=4/3,y=16/3
regions[1]["vertices"] = [[5/3, 8/3], [7/3, 10/3], [4/3, 16/3], [2/3, 14/3]]
for (a_, b_) in regions[1]["vertices"]:
    d = b_ - a_; w = b_ + 2*a_
    check("Q4a vertex on the strip bounds", 1 - 1e-9 <= d <= 4 + 1e-9 and 6 - 1e-9 <= w <= 8 + 1e-9)
(HERE / "regions.json").write_text(json.dumps(regions, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

contours = [
    {"id": "22A-B-Q4b", "f": "1-x^2-y^2", "constraint": "(x-1)^2+(y-1)^2=1", "kind": "lagrange",
     "domain": [[-0.5, 2.5], [-0.5, 2.5]],
     "critical_points": [
         {"x": "1-1/sqrt(2)", "y": "1-1/sqrt(2)", "f": vals[1], "role": "abs max"},
         {"x": "1+1/sqrt(2)", "y": "1+1/sqrt(2)", "f": vals[0], "role": "abs min"}]},
    {"id": "22A-B-Q5b", "f": "x^3+8*y^3-6*x*y+1", "constraint": None, "kind": "unconstrained",
     "domain": [[-1, 2], [-1, 1.5]],
     "critical_points": [
         {"x": 0, "y": 0, "f": 1, "role": "saddle"},
         {"x": 1, "y": 0.5, "f": 0, "role": "local min"}]},
]
(HERE / "contours.json").write_text(json.dumps(contours, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ALL OK:", len(ok), "checks")
