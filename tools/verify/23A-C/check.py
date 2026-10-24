# -*- coding: utf-8 -*-
"""Geometry checks and region/contour data for sitting 23A-C (calculus-2, semester A, moed C, 27.4.2023).
This sitting has NO key: every item is solved (solutionSource "solved", official false). This script checks the
geometry of the regions and the critical points of Q4b/Q5a, so the app's region/contour figures have verified data.
The values below are solver-verified (sympy, tools/verify/23A-C/solve_23A-C.py); there is no official key.
Run: PYTHONUTF8=1 py tools/verify/23A-C/check.py
Writes regions.json and contours.json next to this file."""
import json, pathlib, math
import sympy as sp
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
R = sp.Rational
x, y, lam = sp.symbols("x y lam", real=True)
ok = []


def check(name, cond):
    assert cond, "MISMATCH: " + name
    ok.append(name)


# ---- Q1a: region between x^2+y^2=2x (circle centre (1,0) r=1) and x^2+y^2=4x (centre (2,0) r=2)
check("Q1a circles tangent at the origin, small inside large (centre distance 1 = 2-1)", 2 - 1 == 1)
check("Q1a area between = 4pi - pi = 3pi", 4*sp.pi - sp.pi == 3*sp.pi)
r, th = sp.symbols("r theta", positive=True)
A = sp.integrate(r, (r, 2*sp.cos(th), 4*sp.cos(th)), (th, -sp.pi/2, sp.pi/2))
check("Q1a polar area integral = 3pi", sp.simplify(A - 3*sp.pi) == 0)

# ---- Q4a: swap order. Region: -4<=x<=0, 0<=y<=sqrt(x+4)  union  0<=x<=2, 0<=y<=2-x
# in y-slices: 0<=y<=2, y^2-4<=x<=2-y
f = sp.Function("f")
t = sp.symbols("t")
# compare areas (f = 1)
a1 = sp.integrate(sp.sqrt(x + 4), (x, -4, 0)) + sp.integrate(2 - x, (x, 0, 2))
a2 = sp.integrate(2 - y - (y**2 - 4), (y, 0, 2))
check("Q4a area same in both orders (32/3 = 8*... )", sp.simplify(a1 - a2) == 0)
check("Q4a boundary curves meet at (0,2): sqrt(0+4)=2=2-0", sp.sqrt(4) == 2)
# a non-symmetric test integrand to confirm the swapped limits describe the same region
g = x**2*y + y**3
b1 = sp.integrate(sp.integrate(g, (y, 0, sp.sqrt(x + 4))), (x, -4, 0)) + sp.integrate(sp.integrate(g, (y, 0, 2 - x)), (x, 0, 2))
b2 = sp.integrate(sp.integrate(g, (x, y**2 - 4, 2 - y)), (y, 0, 2))
check("Q4a swapped order gives same integral for a test integrand", sp.simplify(b1 - b2) == 0)

# ---- Q4b: f = x^2+y^2+4xy on the sector 0<=theta<=pi/3, r<=1 (first quadrant, y=0, y=sqrt3 x, unit circle)
f4 = x**2 + y**2 + 4*x*y
check("Q4b interior critical point only the origin (a vertex of the sector)",
      sp.solve([sp.diff(f4, x), sp.diff(f4, y)], [x, y], dict=True) == [{x: 0, y: 0}])
check("Q4b edge y=0: f = x^2", sp.expand(f4.subs(y, 0) - x**2) == 0)
check("Q4b edge y=sqrt3 x: f = (4+4 sqrt3) x^2", sp.expand(f4.subs(y, sp.sqrt(3)*x) - (4 + 4*sp.sqrt(3))*x**2) == 0)
check("Q4b arc: f = 1 + 2 sin 2theta", sp.simplify(f4.subs({x: sp.cos(th), y: sp.sin(th)}) - 1 - 2*sp.sin(2*th)) == 0)
fvals = {"origin": 0, "(1,0)": 1, "(1/2,sqrt3/2)": 1 + sp.sqrt(3), "(1/sqrt2,1/sqrt2)": 3}
check("Q4b arc values", f4.subs({x: 1, y: 0}) == 1
      and sp.simplify(f4.subs({x: R(1, 2), y: sp.sqrt(3)/2}) - (1 + sp.sqrt(3))) == 0
      and sp.simplify(f4.subs({x: 1/sp.sqrt(2), y: 1/sp.sqrt(2)}) - 3) == 0)
gx, gy = np.meshgrid(np.linspace(0, 1, 2001), np.linspace(0, 1, 2001))
mk = (gx**2 + gy**2 <= 1) & (gy <= math.sqrt(3)*gx)
fv = (gx**2 + gy**2 + 4*gx*gy)[mk]
check("Q4b numeric max 3 min 0", abs(fv.max() - 3) < 1e-3 and abs(fv.min()) < 1e-9)

# ---- Q5a: f = (x^2-2y^2) e^(x-y) critical points
f5 = (x**2 - 2*y**2)*sp.exp(x - y)
crit = sp.solve([sp.diff(f5, x), sp.diff(f5, y)], [x, y], dict=True)
cps = sorted((s[x], s[y]) for s in crit)
check("Q5a critical points (0,0),(-4,-2)  (Hessian classification in solve_23A-C.py)", cps == [(-4, -2), (0, 0)])

regions = [
    {"id": "23A-C-Q1a", "description": "plane region between the circles x^2+y^2=2x (inside) and x^2+y^2=4x (outside); tangent at the origin",
     "type": "annular", "inequalities": ["x^2+y^2>=2*x", "x^2+y^2<=4*x"],
     "boundary_curves": ["x^2+y^2=2*x", "x^2+y^2=4*x"],
     "polar": {"theta": ["-pi/2", "pi/2"], "r": ["2*cos(theta)", "4*cos(theta)"]},
     "area": "3*pi", "note": "solved (no key); see solve_23A-C.py"},
    {"id": "23A-C-Q4a", "description": "region of the sum of two integrals: -4<=x<=0, 0<=y<=sqrt(x+4) and 0<=x<=2, 0<=y<=2-x",
     "type": "simple",
     "orderXY": {"pieces": [{"x": [-4, 0], "y": [0, "sqrt(x+4)"]}, {"x": [0, 2], "y": [0, "2-x"]}]},
     "orderYX": {"y": [0, 2], "x": ["y^2-4", "2-y"]},
     "inequalities": ["y>=0", "x>=y^2-4", "x<=2-y"],
     "boundary_curves": ["y=0", "x=y^2-4", "x+y=2"],
     "vertices": [[-4, 0], [2, 0], [0, 2]],
     "integrand": "f(x,y)"},
]
(HERE / "regions.json").write_text(json.dumps(regions, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

contours = [
    {"id": "23A-C-Q4b", "f": "x^2+y^2+4*x*y", "constraint": None, "kind": "closed_region",
     "region": "x>=0, y>=0, y<=sqrt(3)*x, x^2+y^2<=1", "domain": [[-0.2, 1.2], [-0.2, 1.2]],
     "critical_points": [
         {"x": 0, "y": 0, "f": 0, "role": "abs min (vertex)"},
         {"x": "1/sqrt(2)", "y": "1/sqrt(2)", "f": 3, "role": "abs max (arc)"},
         {"x": 1, "y": 0, "f": 1, "role": "boundary vertex"},
         {"x": "1/2", "y": "sqrt(3)/2", "f": "1+sqrt(3)", "role": "boundary vertex"}]},
    {"id": "23A-C-Q5a", "f": "(x^2-2*y^2)*exp(x-y)", "constraint": None, "kind": "unconstrained",
     "domain": [[-8, 3], [-6, 3]],
     "critical_points": [
         {"x": 0, "y": 0, "f": 0, "role": "saddle"},
         {"x": -4, "y": -2, "f": float(f5.subs({x: -4, y: -2})), "role": "local max"}]},
]
(HERE / "contours.json").write_text(json.dumps(contours, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ALL OK:", len(ok), "checks")
