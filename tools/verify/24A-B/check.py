# -*- coding: utf-8 -*-
"""sympy + numeric checks for sitting 24A-B (calculus-2, semester A, moed B, 6.5.2024).
Key = the solution file misnamed "6.5.25" (really the 6.5.24 solution).
Run: PYTHONUTF8=1 py tools/verify/24A-B/check.py
Also writes contours.json next to this file."""
import json, pathlib, math
import sympy as sp
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
R = sp.Rational
x, y, z, h, lam, k, a, b = sp.symbols("x y z h lam k a b", real=True)
n = sp.symbols("n", integer=True, positive=True)
ok = []


def check(name, cond):
    assert cond, "MISMATCH: " + name
    ok.append(name)


# ---- Q1a: x^2 y^2/(x^6+y^3)
f1 = x**2*y**2/(x**6 + y**3)
check("Q1a along y=x^2 limit 1/2", sp.limit(f1.subs(y, x**2), x, 0, "+") == R(1, 2))
check("Q1a along y=kx limit 0 (k=1,2,-3)", all(sp.limit(f1.subs(y, kk*x), x, 0, "+") == 0 for kk in (1, 2, -3)))
check("Q1a so no limit, not continuous at 0 (1/2 != f(0,0)=0)", R(1, 2) != 0)
check("Q1a denominator vanishes on y=-x^2 (f undefined there)", sp.simplify((x**6 + y**3).subs(y, -x**2)) == 0)

# ---- Q1b: f = x + xy, direction derivative 1/sqrt2 at (1,-1)
f1b = x + x*y
g = sp.Matrix([sp.diff(f1b, x), sp.diff(f1b, y)])
check("Q1b grad = (1+y, x)", list(g) == [1 + y, x])
gp = g.subs({x: 1, y: -1})
check("Q1b grad(1,-1) = (0,1)", list(gp) == [0, 1])
sol = sp.solve([gp[0]*a + gp[1]*b - 1/sp.sqrt(2), a**2 + b**2 - 1], [a, b], dict=True)
got = {(sp.simplify(s[a]), sp.simplify(s[b])) for s in sol}
check("Q1b unit vectors (+-1/sqrt2, 1/sqrt2)",
      got == {(1/sp.sqrt(2), 1/sp.sqrt(2)), (-1/sp.sqrt(2), 1/sp.sqrt(2))})

# ---- Q2a(1): sum (-1)^n /((n+1) ln(n+1)): conditional
xx = sp.symbols("xx", positive=True)
check("Q2a(1) integral antiderivative ln ln (x+1)",
      sp.simplify(sp.integrate(1/((xx + 1)*sp.log(xx + 1)), xx) - sp.log(sp.log(xx + 1))) == 0)
check("Q2a(1) integral diverges", sp.limit(sp.log(sp.log(xx + 1)), xx, sp.oo) == sp.oo)
check("Q2a(1) 1/(2 ln2) > 1/(3 ln3) > 1/(4 ln4)",
      1/(2*math.log(2)) > 1/(3*math.log(3)) > 1/(4*math.log(4)))
check("Q2a(1) a_n -> 0", sp.limit(1/((n + 1)*sp.log(n + 1)), n, sp.oo) == 0)

# ---- Q2a(2): sum ((-1)^n + n)/3^n, terms >= 0 (zero at n=1), root test 1/3
t = ((-1)**n + n)/3**n
check("Q2a(2) terms nonnegative (n=1..60)", all(((-1)**m + m)/3**m >= 0 for m in range(1, 60)))
check("Q2a(2) root limit 1/3", sp.limit(sp.root(n + 1, n)/3, n, sp.oo) == R(1, 3))
check("Q2a(2) sandwich (n-1)/3^n <= t <= (n+1)/3^n (n=1..60)",
      all((m - 1)/3**m <= ((-1)**m + m)/3**m <= (m + 1)/3**m for m in range(1, 60)))
S = sp.summation(((-1)**n + n)/3**n, (n, 1, sp.oo))
check("Q2a(2) sum = -1/4 + 3/4 = 1/2", sp.simplify(S - R(1, 2)) == 0)

# ---- Q2b: (x^3+y^3)/(2x^2+y^2)
f2 = (x**3 + y**3)/(2*x**2 + y**2)
check("Q2b fx(0,0)=1/2", sp.limit(f2.subs({x: h, y: 0})/h, h, 0) == R(1, 2))
check("Q2b fy(0,0)=1", sp.limit(f2.subs({x: 0, y: h})/h, h, 0) == 1)
eps_num = f2 - (x/2 + y)
eps_key = -(x*y**2 + 4*x**2*y)/(2*(2*x**2 + y**2))
check("Q2b numerator of eps as in key", sp.simplify(eps_num - eps_key) == 0)
eps = eps_key/sp.sqrt(x**2 + y**2)
lim_k = sp.simplify(sp.limit(sp.simplify(eps.subs(y, k*x)), x, 0, "+"))
check("Q2b along dy=k dx (dx>0): -(k^2+4k)/(2(2+k^2) sqrt(1+k^2))",
      sp.simplify(lim_k + (k**2 + 4*k)/(2*(2 + k**2)*sp.sqrt(1 + k**2))) == 0)
check("Q2b limit depends on k (not 0) so not differentiable", lim_k.subs(k, 1) != 0 and lim_k.subs(k, 2) != lim_k.subs(k, 1))
check("Q2b with k=1 along the diagonal limit = -5/(6 sqrt2)", sp.simplify(lim_k.subs(k, 1) + 5/(6*sp.sqrt(2))) == 0)

# ---- Q3a: radius and endpoints of sum (x+5)^n/(cbrt(n+1) sqrt(n^2+1))
an = 1/(sp.cbrt(n + 1)*sp.sqrt(n**2 + 1))
check("Q3a R=1", sp.limit(an/an.subs(n, n + 1), n, sp.oo) == 1)
check("Q3a terms ~ n^(-4/3): n^(4/3) a_n -> 1", sp.limit(n**R(4, 3)*an, n, sp.oo) == 1)
check("Q3a sum n^(-4/3) converges (p=4/3>1)", sp.integrate(xx**R(-4, 3), (xx, 1, sp.oo)) == 3)
check("Q3a domain: -1<=x+5<=1 -> [-6,-4]", (-1 - 5, 1 - 5) == (-6, -4))
# the key compares with 1/cbrt(n^2) (= n^(-2/3)) and then concludes n^(-3/2): inconsistent with n^(-4/3)
check("Q3a key's ratio to n^(-2/3) tends to 0 (not 1)", sp.limit(an*n**R(2, 3), n, sp.oo) == 0)

# ---- Q3b: z = y/(3x) + g(xy)
gg = sp.Function("g")
z3 = y/(3*x) + gg(x*y)
expr = sp.simplify(x**2*sp.diff(z3, x) - x*y*sp.diff(z3, y) + 2*y/3)
check("Q3b identity", expr == 0)

# ---- Q4a: sum 5/3^n - 4/((n+3)(n+4))
S4 = sp.summation(5/3**n, (n, 1, sp.oo)) - 4*sp.summation(1/((n + 3)*(n + 4)), (n, 1, sp.oo))
check("Q4a sum 5/2 - 4*(1/4) = 3/2", sp.simplify(S4 - R(3, 2)) == 0)
check("Q4a numeric", abs(sum(5/3**m - 4/((m + 3)*(m + 4)) for m in range(1, 200000)) - 1.5) < 1e-4)

# ---- Q4b: 2x^4 + y^4 - x^2 - 2y^2 on x^2+y^2<=2
f4 = 2*x**4 + y**4 - x**2 - 2*y**2
crit = sp.solve([sp.diff(f4, x), sp.diff(f4, y)], [x, y], dict=True)
cps = sorted((s[x], s[y]) for s in crit)
exp_c = sorted([(xv, yv) for xv in (0, R(1, 2), -R(1, 2)) for yv in (0, 1, -1)])
check("Q4b nine critical points", cps == exp_c)
check("Q4b all critical points inside the disk", all(p[0]**2 + p[1]**2 < 2 for p in cps))
vals = {p: f4.subs({x: p[0], y: p[1]}) for p in cps}
check("Q4b interior values 0,-1,-1/8,-9/8",
      vals[(0, 0)] == 0 and vals[(0, 1)] == -1 and vals[(R(1, 2), 0)] == R(-1, 8) and vals[(R(1, 2), 1)] == R(-9, 8))
L = f4 + lam*(x**2 + y**2 - 2)
bs = sp.solve([sp.diff(L, x), sp.diff(L, y), x**2 + y**2 - 2], [x, y, lam], dict=True)
bpts = {(sp.nsimplify(s[x]), sp.nsimplify(s[y])) for s in bs}
exp_b = {(0, sp.sqrt(2)), (0, -sp.sqrt(2)), (sp.sqrt(2), 0), (-sp.sqrt(2), 0),
         (R(1, 2)*sp.sqrt(2), sp.sqrt(R(3, 2))), (R(1, 2)*sp.sqrt(2), -sp.sqrt(R(3, 2))),
         (-R(1, 2)*sp.sqrt(2), sp.sqrt(R(3, 2))), (-R(1, 2)*sp.sqrt(2), -sp.sqrt(R(3, 2)))}
check("Q4b boundary Lagrange points", {(sp.simplify(p[0]), sp.simplify(p[1])) for p in bpts} == {(sp.simplify(p[0]), sp.simplify(p[1])) for p in exp_b})
bv = {p: sp.simplify(f4.subs({x: p[0], y: p[1]})) for p in bpts}
check("Q4b boundary values 0, 6, -3/4", set(bv.values()) == {0, 6, R(-3, 4)})
gx, gy = np.meshgrid(np.linspace(-1.5, 1.5, 3001), np.linspace(-1.5, 1.5, 3001))
mk = gx**2 + gy**2 <= 2
fv = (2*gx**4 + gy**4 - gx**2 - 2*gy**2)[mk]
check("Q4b grid max 6 min -9/8", abs(fv.max() - 6) < 0.05 and abs(fv.min() + 9/8) < 1e-3)

# ---- Q5a: (3-x)(3-y)(x+y-3)
f5 = (3 - x)*(3 - y)*(x + y - 3)
crit5 = sp.solve([sp.diff(f5, x), sp.diff(f5, y)], [x, y], dict=True)
c5 = sorted((s[x], s[y]) for s in crit5)
check("Q5a critical points (0,3),(2,2),(3,0),(3,3)", c5 == [(0, 3), (2, 2), (3, 0), (3, 3)])
check("Q5a fx = (3-y)(-2x-y+6)", sp.expand(sp.diff(f5, x) - (3 - y)*(-2*x - y + 6)) == 0)
check("Q5a fy = (3-x)(-x-2y+6)", sp.expand(sp.diff(f5, y) - (3 - x)*(-x - 2*y + 6)) == 0)
check("Q5a fxx=-6+2y, fxy=2x+2y-9, fyy=-6+2x",
      sp.expand(sp.diff(f5, x, 2) - (-6 + 2*y)) == 0 and sp.expand(sp.diff(f5, x, y) - (2*x + 2*y - 9)) == 0
      and sp.expand(sp.diff(f5, y, 2) - (-6 + 2*x)) == 0)
Hs = sp.hessian(f5, (x, y))
dets = {p: Hs.subs({x: p[0], y: p[1]}).det() for p in c5}
check("Q5a Delta = -9,-9,-9 at the three boundary points and 3 at (2,2)",
      dets[(0, 3)] == -9 and dets[(3, 0)] == -9 and dets[(3, 3)] == -9 and dets[(2, 2)] == 3)
check("Q5a fxx(2,2)=-2 (local max), f(2,2)=1", Hs.subs({x: 2, y: 2})[0, 0] == -2 and f5.subs({x: 2, y: 2}) == 1)

# ---- Q5b: x/(25+x^2)
f6 = x/(25 + x**2)
ser = sp.series(f6, x, 0, 14).removeO()
check("Q5b coefficients (-1)^n x^(2n+1)/5^(2n+2)",
      all(ser.coeff(x, 2*m + 1) == R((-1)**m, 5**(2*m + 2)) and ser.coeff(x, 2*m) == 0 for m in range(0, 6)))
check("Q5b radius 5", min(abs(p) for p in sp.solve(25 + sp.Symbol("w")**2, sp.Symbol("w"))) == 5)
check("Q5b f^(5)(0) = 4!/5^5 = 24/3125", sp.diff(f6, x, 5).subs(x, 0) == R(24, 3125))
check("Q5b endpoints: terms (-1)^n 5^(2n+1)/5^(2n+2) = (-1)^n/5 do not tend to 0",
      sp.simplify(5**(2*n + 1)/5**(2*n + 2)) == R(1, 5))

# ---- contours.json
contours = [
    {"id": "24A-B-Q4b", "f": "2*x^4+y^4-x^2-2*y^2", "constraint": "x^2+y^2=2", "kind": "closed_region",
     "region": "x^2+y^2<=2", "domain": [[-1.7, 1.7], [-1.7, 1.7]],
     "critical_points": [
         {"x": "sqrt(2)", "y": 0, "f": 6, "role": "abs max"},
         {"x": "-sqrt(2)", "y": 0, "f": 6, "role": "abs max"},
         {"x": 0.5, "y": 1, "f": -1.125, "role": "abs min"},
         {"x": 0.5, "y": -1, "f": -1.125, "role": "abs min"},
         {"x": -0.5, "y": 1, "f": -1.125, "role": "abs min"},
         {"x": -0.5, "y": -1, "f": -1.125, "role": "abs min"},
         {"x": 0, "y": 0, "f": 0, "role": "interior critical"},
         {"x": 0, "y": 1, "f": -1, "role": "interior critical"},
         {"x": 0, "y": -1, "f": -1, "role": "interior critical"},
         {"x": 0.5, "y": 0, "f": -0.125, "role": "interior critical"},
         {"x": -0.5, "y": 0, "f": -0.125, "role": "interior critical"},
         {"x": 0, "y": "sqrt(2)", "f": 0, "role": "boundary critical"},
         {"x": 0, "y": "-sqrt(2)", "f": 0, "role": "boundary critical"},
         {"x": "1/sqrt(2)", "y": "sqrt(3/2)", "f": -0.75, "role": "boundary critical"},
         {"x": "1/sqrt(2)", "y": "-sqrt(3/2)", "f": -0.75, "role": "boundary critical"},
         {"x": "-1/sqrt(2)", "y": "sqrt(3/2)", "f": -0.75, "role": "boundary critical"},
         {"x": "-1/sqrt(2)", "y": "-sqrt(3/2)", "f": -0.75, "role": "boundary critical"}]},
    {"id": "24A-B-Q5a", "f": "(3-x)*(3-y)*(x+y-3)", "constraint": None, "kind": "unconstrained",
     "domain": [[-1, 4.5], [-1, 4.5]],
     "critical_points": [
         {"x": 0, "y": 3, "f": 0, "role": "saddle"},
         {"x": 3, "y": 0, "f": 0, "role": "saddle"},
         {"x": 3, "y": 3, "f": 0, "role": "saddle"},
         {"x": 2, "y": 2, "f": 1, "role": "local max"}]},
]
(HERE / "contours.json").write_text(json.dumps(contours, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ALL OK:", len(ok), "checks")
