# -*- coding: utf-8 -*-
"""sympy + numeric checks for sitting 24B-A (calculus-2, semester A, moed A; typed solution 4.7.24 with the question embedded).
Run: PYTHONUTF8=1 py tools/verify/24B-A/check.py
Also writes contours.json next to this file."""
import json, pathlib, math
import sympy as sp
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
R = sp.Rational
x, y, z, h, t, lam = sp.symbols("x y z h t lam", real=True)
ok = []


def check(name, cond):
    assert cond, "MISMATCH: " + name
    ok.append(name)


# ---- Q1a: f = y x^2/(2y^2+3x^4); path y=x^2 gives 1/5 != f(0,0)=0
f1 = y*x**2/(2*y**2 + 3*x**4)
check("Q1a limit along y=x^2 is 1/5", sp.limit(f1.subs(y, x**2), x, 0) == R(1, 5))
check("Q1a 1/5 != 0 so not continuous", R(1, 5) != 0)
check("Q1a along y=0 limit 0 (two paths disagree)", sp.limit(f1.subs(y, 0), x, 0) == 0)

# ---- Q1b: partials at 0 by definition, then differentiability (fails: not continuous)
check("Q1b f(h,0)=0 and f(0,h)=0 identically", sp.simplify(f1.subs({y: 0})) == 0 and sp.simplify(f1.subs({x: 0})) == 0)
check("Q1b fx(0,0)=fy(0,0)=0", sp.limit(sp.Integer(0)/h, h, 0) == 0)
q = (f1.subs(y, x**2))/sp.sqrt(x**2 + x**4)
check("Q1b differentiability quotient f/rho along y=x^2 -> oo (not 0)", sp.limit(q, x, 0, "+") == sp.oo)

# ---- Q1c: partials at (1,1), differential
fx = sp.diff(f1, x); fy = sp.diff(f1, y)
check("Q1c fx(1,1) = -2/25", sp.simplify(fx.subs({x: 1, y: 1})) == R(-2, 25))
check("Q1c fy(1,1) = 1/25", sp.simplify(fy.subs({x: 1, y: 1})) == R(1, 25))
check("Q1c fx formula as printed",
      sp.simplify(fx - (2*y*x*(2*y**2 + 3*x**4) - 12*x**3*y*x**2)/(2*y**2 + 3*x**4)**2) == 0)
check("Q1c fy formula as printed",
      sp.simplify(fy - (x**2*(2*y**2 + 3*x**4) - 4*y**2*x**2)/(2*y**2 + 3*x**4)**2) == 0)

# ---- Q2a: sum (-1)^n (3+sin sqrt n)/n^2 absolutely convergent
n = sp.symbols("n", integer=True, positive=True)
check("Q2a bound (3+sin)/n^2 <= 4/n^2 numerically",
      all((3 + math.sin(math.sqrt(k)))/k**2 <= 4/k**2 + 1e-15 for k in range(1, 5000)))
S_a = sum((3 + math.sin(math.sqrt(k)))/k**2 for k in range(1, 400000))
S_b = sum((3 + math.sin(math.sqrt(k)))/k**2 for k in range(1, 800000))
check("Q2a absolute series numerically convergent (tail ~ 4/N)", abs(S_a - S_b) < 2e-5)

# ---- Q2b: sum (-1)^n/((n+1) ln(n+1)): integral test diverges, Leibniz converges
xx = sp.symbols("xx", positive=True)
I = sp.integrate(1/((xx + 1)*sp.log(xx + 1)), xx)
check("Q2b antiderivative is ln(ln(x+1))", sp.simplify(I - sp.log(sp.log(xx + 1))) == 0)
check("Q2b integral from 1 to oo diverges", sp.limit(sp.log(sp.log(xx + 1)), xx, sp.oo) == sp.oo)
check("Q2b a_n decreasing and -> 0",
      all(1/((k + 2)*math.log(k + 2)) < 1/((k + 1)*math.log(k + 1)) for k in range(1, 5000))
      and sp.limit(1/((n + 1)*sp.log(n + 1)), n, sp.oo) == 0)
ps = np.cumsum([(-1)**k/((k + 1)*math.log(k + 1)) for k in range(1, 200001)])
check("Q2b alternating partial sums settle", abs(ps[-1] - ps[-2]) < 1e-5 and abs(ps[-1] - ps[-1001]) < 1e-3)
S1 = sum(1/((k + 1)*math.log(k + 1)) for k in range(1, 100001))
S2 = sum(1/((k + 1)*math.log(k + 1)) for k in range(1, 2000001))
check("Q2b absolute partial sums keep growing (like ln ln N)", S2 > S1 + 0.2)

# ---- Q3: f = 2x^2 - y^2 + 1
f3 = 2*x**2 - y**2 + 1
g3 = sp.Matrix([sp.diff(f3, x), sp.diff(f3, y)])
check("Q3a grad f = (4x,-2y)", list(g3) == [4*x, -2*y])
check("Q3a grad f(2,3) = (8,-6)", list(g3.subs({x: 2, y: 3})) == [8, -6])
check("Q3b ||grad f(2,3)|| = 10", sp.sqrt(sum(c**2 for c in g3.subs({x: 2, y: 3}))) == 10)
crit = sp.solve(list(g3), [x, y], dict=True)
check("Q3c only critical point (0,0)", crit == [{x: 0, y: 0}])
H = sp.hessian(f3, (x, y))
check("Q3c A=4,B=0,C=-2, Delta=-8<0 (saddle)", H == sp.Matrix([[4, 0], [0, -2]]) and H.det() == -8)
check("Q3d (0,0) is on the boundary circle", (0 - 1)**2 + 0 == 1)
L = f3 - lam*((x - 1)**2 + y**2 - 1)
sols = sp.solve([sp.diff(L, x), sp.diff(L, y), (x - 1)**2 + y**2 - 1], [x, y, lam], dict=True)
pts = {(sp.nsimplify(s[x]), sp.nsimplify(s[y])) for s in sols}
exp_pts = {(0, 0), (2, 0), (R(1, 3), sp.sqrt(5)/3), (R(1, 3), -sp.sqrt(5)/3)}
check("Q3d Lagrange points = M1..M4", pts == exp_pts)
vals = {p: sp.simplify(f3.subs({x: p[0], y: p[1]})) for p in pts}
check("Q3d values 1, 9, 2/3, 2/3",
      vals[(0, 0)] == 1 and vals[(2, 0)] == 9 and vals[(R(1, 3), sp.sqrt(5)/3)] == R(2, 3)
      and vals[(R(1, 3), -sp.sqrt(5)/3)] == R(2, 3))
ang = np.linspace(0, 2*np.pi, 2000001)
fb = 2*(1 + np.cos(ang))**2 - np.sin(ang)**2 + 1
check("Q3d numeric boundary max 9, min 2/3", abs(fb.max() - 9) < 1e-6 and abs(fb.min() - 2/3) < 1e-6)
gx, gy = np.meshgrid(np.linspace(0, 2, 1601), np.linspace(-1, 1, 1601))
mk = (gx - 1)**2 + gy**2 <= 1
fv = (2*gx**2 - gy**2 + 1)[mk]
check("Q3d grid over disk: max 9, min 2/3", abs(fv.max() - 9) < 1e-3 and abs(fv.min() - 2/3) < 1e-3)

# ---- Q4a: tangent plane
F = 2*x**2 - y**2 + z**2
Fg = [sp.diff(F, v) for v in (x, y, z)]
pt = {x: 1, y: -1, z: 2}
check("Q4a point on surface", F.subs(pt) == 5)
check("Q4a gradient (4,2,4)", [c.subs(pt) for c in Fg] == [4, 2, 4])
plane = 4*(x - 1) + 2*(y + 1) + 4*(z - 2)
check("Q4a plane expands to 4x+2y+4z=10", sp.expand(plane) == 4*x + 2*y + 4*z - 10)

# ---- Q4b: radius of convergence of sum 2^n n!/(2n)! x^n
an = 2**n*sp.factorial(n)/sp.factorial(2*n)
ratio = sp.simplify(sp.combsimp(an/an.subs(n, n + 1)))
check("Q4b a_n/a_{n+1} = 2n+1", sp.simplify(ratio - (2*n + 1)) == 0)
check("Q4b R = oo", sp.limit(2*n + 1, n, sp.oo) == sp.oo)

# ---- Q5: f = ln(2x^2+3x+1) = ln(x+1)+ln(2x+1)
f5 = sp.log(2*x**2 + 3*x + 1)
check("Q5a factorisation", sp.expand((x + 1)*(2*x + 1)) == 2*x**2 + 3*x + 1)
ser = sp.series(f5, x, 0, 12).removeO()
check("Q5a coefficients (-1)^(n+1)(1+2^n)/n, n<=11",
      all(sp.simplify(ser.coeff(x, k) - R((-1)**(k + 1)*(1 + 2**k), k)) == 0 for k in range(1, 12)))
check("Q5b radius 1/2 (root test: 1/R = 2)", sp.limit(sp.root(R(1)*(1 + 2**n)/n, n), n, sp.oo) == 2)
check("Q5b x=1/2: f(1/2)=ln 3 finite", sp.simplify(f5.subs(x, R(1, 2)) - sp.log(3)) == 0)
check("Q5b x=-1/2: f -> -oo (diverges)", sp.limit(f5, x, R(-1, 2), "+") == -sp.oo)
check("Q5b partial sum at x=1/2 matches ln3",
      abs(sum((-1)**(k + 1)*(0.5**k + 1)/k for k in range(1, 200001)) - math.log(3)) < 1e-4)
check("Q5c f^(5)(0) = 792", sp.diff(f5, x, 5).subs(x, 0) == 792)
check("Q5c a_5 = 33/5 and 33*4! = 792", R((-1)**6*(1 + 2**5), 5) == R(33, 5) and 33*sp.factorial(4) == 792)

# ---- contours.json
contours = [
    {"id": "24B-A-Q3c", "f": "2*x^2-y^2+1", "constraint": None, "kind": "unconstrained",
     "domain": [[-3, 3], [-3, 3]],
     "critical_points": [{"x": 0, "y": 0, "f": 1, "role": "saddle"}]},
    {"id": "24B-A-Q3d", "f": "2*x^2-y^2+1", "constraint": "(x-1)^2+y^2=1", "kind": "closed_region",
     "region": "(x-1)^2+y^2<=1",
     "domain": [[-1, 3], [-2, 2]],
     "critical_points": [
         {"x": 2, "y": 0, "f": 9, "role": "abs max"},
         {"x": "1/3", "y": "sqrt(5)/3", "f": "2/3", "role": "abs min"},
         {"x": "1/3", "y": "-sqrt(5)/3", "f": "2/3", "role": "abs min"},
         {"x": 0, "y": 0, "f": 1, "role": "boundary point"}]},
]
(HERE / "contours.json").write_text(json.dumps(contours, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ALL OK:", len(ok), "checks")
