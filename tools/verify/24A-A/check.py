# -*- coding: utf-8 -*-
"""sympy + numeric checks for sitting 24A-A (calculus-2, semester A, moed A, 4.4.2024; key = "answers 4.4.2024").
Run: PYTHONUTF8=1 py tools/verify/24A-A/check.py
Also writes contours.json next to this file."""
import json, pathlib, math
import sympy as sp
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
R = sp.Rational
x, y, z, h = sp.symbols("x y z h", real=True)
r, th = sp.symbols("r theta", positive=True)
n = sp.symbols("n", integer=True, positive=True)
ok = []


def check(name, cond):
    assert cond, "MISMATCH: " + name
    ok.append(name)


# ---- Q1a: continuity of (x^3 y - x y^3)/(x^2+y^2)
f1 = (x**3*y - x*y**3)/(x**2 + y**2)
fp = sp.simplify(f1.subs({x: r*sp.cos(th), y: r*sp.sin(th)}))
check("Q1a polar form r^2 (cos^3 sin - cos sin^3)",
      sp.simplify(fp - r**2*(sp.cos(th)**3*sp.sin(th) - sp.cos(th)*sp.sin(th)**3)) == 0)
check("Q1a |f| <= r^2/2 -> 0 (bounded angular factor)", sp.limit(r**2/2, r, 0) == 0)
gx, gy = np.meshgrid(np.linspace(-1e-3, 1e-3, 801), np.linspace(-1e-3, 1e-3, 801))
with np.errstate(all="ignore"):
    fn = np.where((gx == 0) & (gy == 0), 0.0, (gx**3*gy - gx*gy**3)/(gx**2 + gy**2))
check("Q1a numeric |f| tiny near origin", np.nanmax(np.abs(fn)) < 1e-6)

# ---- Q1b: f = 2 exp(-x^2) + exp(-3 y^2); gradient at (1,0)
f1b = 2*sp.exp(-x**2) + sp.exp(-3*y**2)
gr = sp.Matrix([sp.diff(f1b, x), sp.diff(f1b, y)])
check("Q1b grad = (-4x e^{-x^2}, -6y e^{-3y^2})",
      sp.simplify(gr[0] + 4*x*sp.exp(-x**2)) == 0 and sp.simplify(gr[1] + 6*y*sp.exp(-3*y**2)) == 0)
check("Q1b grad f(1,0) = (-4/e, 0)", sp.simplify(gr.subs({x: 1, y: 0}) - sp.Matrix([-4/sp.E, 0])) == sp.zeros(2, 1))
g0 = np.array([float(-4/sp.E), 0.0])
ang = np.linspace(0, 2*np.pi, 360001)
dd = g0[0]*np.cos(ang) + g0[1]*np.sin(ang)
check("Q1b directional derivative max at u=(-1,0)", abs(ang[np.argmax(dd)] - np.pi) < 1e-3)

# ---- Q2a: two series
check("Q2a(1) sin(1/sqrt n)/(1/sqrt n) -> 1", sp.limit(sp.sin(1/sp.sqrt(n))*sp.sqrt(n), n, sp.oo) == 1)
check("Q2a(1) sum 1/sqrt n diverges (p=1/2)", sp.integrate(1/sp.sqrt(x), (x, 1, sp.oo)) == sp.oo)
check("Q2a(1) a_n = sin(1/sqrt n) decreasing, -> 0",
      all(math.sin(1/math.sqrt(k + 1)) < math.sin(1/math.sqrt(k)) for k in range(1, 5000)) and sp.limit(sp.sin(1/sp.sqrt(n)), n, sp.oo) == 0)
check("Q2a(2) sqrt n - sqrt(n-1) = 1/(sqrt n + sqrt(n-1))", sp.simplify(sp.sqrt(n) - sp.sqrt(n - 1) - 1/(sp.sqrt(n) + sp.sqrt(n - 1))) == 0)
check("Q2a(2) ratio to 1/sqrt n -> 1/2", sp.limit(sp.sqrt(n)/(sp.sqrt(n) + sp.sqrt(n - 1)), n, sp.oo) == R(1, 2))
check("Q2a(2) a_n decreasing, -> 0",
      all(1/(math.sqrt(k + 1) + math.sqrt(k)) < 1/(math.sqrt(k) + math.sqrt(k - 1)) for k in range(2, 5000))
      and sp.limit(1/(sp.sqrt(n + 1) + sp.sqrt(n)), n, sp.oo) == 0)
ps = np.cumsum([(-1)**k*math.sin(1/math.sqrt(k)) for k in range(1, 400001)])
check("Q2a(1) alternating partial sums settle", abs(ps[-1] - ps[-2]) < 3e-3 and abs(ps[-1] - ps[-1001]) < 3e-3)
ps2 = np.cumsum([(-1)**k*(math.sqrt(k) - math.sqrt(k - 1)) for k in range(1, 400001)])
check("Q2a(2) alternating partial sums settle", abs(ps2[-1] - ps2[-2]) < 1e-3)
sa1 = sum(math.sin(1/math.sqrt(k)) for k in range(1, 10**5)); sa2 = sum(math.sin(1/math.sqrt(k)) for k in range(1, 4*10**5))
check("Q2a(1) absolute partial sums grow like sqrt(N)", sa2 > 1.8*sa1)

# ---- Q2b: f = x y (x^2-y^2)/(x^2+y^2); partials at 0, differentiability
f2 = x*y*(x**2 - y**2)/(x**2 + y**2)
check("Q2b f(h,0)=f(0,h)=0 so fx(0,0)=fy(0,0)=0", sp.simplify(f2.subs(y, 0)) == 0 and sp.simplify(f2.subs(x, 0)) == 0)
eps = sp.simplify(f2.subs({x: r*sp.cos(th), y: r*sp.sin(th)})/r)
check("Q2b eps = r sin(4 theta)/4 (the official's (1/4) sin 4theta)",
      sp.simplify(eps - r*sp.sin(4*th)/4) == 0)
check("Q2b eps -> 0 so differentiable", sp.limit(r/4, r, 0) == 0)

# ---- Q3a: sum 2^n (x+1)^n/(n^2+1)
an = 2**n/(n**2 + 1)
check("Q3a R = 1/2", sp.limit(an/an.subs(n, n + 1), n, sp.oo) == R(1, 2))
check("Q3a s=-1/2: alternating, converges (Leibniz, 1/(n^2+1) decreasing -> 0)",
      all(1/((k + 1)**2 + 1) < 1/(k**2 + 1) for k in range(1, 3000)))
check("Q3a s=1/2: sum 1/(n^2+1) converges", abs(sum(1/(m*m + 1) for m in range(1, 3000000)) - float((sp.pi*sp.coth(sp.pi) - 1)/2)) < 1e-6)
check("Q3a x-interval [-3/2,-1/2]", (-R(1, 2) - 1, R(1, 2) - 1) == (R(-3, 2), R(-1, 2)))
check("Q3a numeric: terms at x=-1/2 and -3/2 tend to 0 slowly, x=-1/2 terms 1/(n^2+1)",
      abs(sum(2**k*(-0.5 + 1)**k/(k**2 + 1) for k in range(1, 60)) - sum(1/(k**2 + 1) for k in range(1, 60))) < 1e-12)

# ---- Q3b: u = x^k F(z/x, y/x); homogeneity of degree k (Euler). F symbolic function
k = sp.symbols("k", real=True)
Ff = sp.Function("F")
s_, t_ = sp.symbols("s t")
u = x**k*Ff(z/x, y/x)
lhs = sp.simplify(x*sp.diff(u, x) + y*sp.diff(u, y) + z*sp.diff(u, z))
check("Q3b x u_x + y u_y + z u_z = k u", sp.simplify(lhs - k*u) == 0)

# ---- Q4a: sum 1/(n^2+6n+8) = 7/24
S4 = sp.summation(1/(n**2 + 6*n + 8), (n, 1, sp.oo))
check("Q4a sum = 7/24", S4 == R(7, 24))
check("Q4a factorisation (n+2)(n+4)", sp.expand((n + 2)*(n + 4)) == n**2 + 6*n + 8)
Sn = lambda N: R(1, 2)*(R(7, 12) - R(2*N + 7, (N + 3)*(N + 4)))
check("Q4a S_n formula (n=1..40)", all(Sn(N) == sum(R(1, kk**2 + 6*kk + 8) for kk in range(1, N + 1)) for N in range(1, 41)))
check("Q4a numeric sum", abs(sum(1/(m*m + 6*m + 8) for m in range(1, 2000000)) - 7/24) < 1e-6)

# ---- Q4b: abs extrema of xy on x^2+y^2=2
lam = sp.symbols("lam")
L = x*y - lam*(x**2 + y**2 - 2)
sols = sp.solve([sp.diff(L, x), sp.diff(L, y), x**2 + y**2 - 2], [x, y, lam], dict=True)
pts4 = {(s[x], s[y]) for s in sols}
check("Q4b four points (+-1,+-1)", pts4 == {(1, 1), (1, -1), (-1, 1), (-1, -1)})
check("Q4b values +-1", {(p, (p[0]*p[1])) for p in pts4} == {((1, 1), 1), ((-1, -1), 1), ((1, -1), -1), ((-1, 1), -1)})
a_ = np.linspace(0, 2*np.pi, 1000001)
fv = 2*np.cos(a_)*np.sin(a_)
check("Q4b numeric max 1, min -1", abs(fv.max() - 1) < 1e-9 and abs(fv.min() + 1) < 1e-9)

# ---- Q5a: x^3 + 8 y^3 - 6xy + 1
f5 = x**3 + 8*y**3 - 6*x*y + 1
crit = sp.solve([sp.diff(f5, x), sp.diff(f5, y)], [x, y], dict=True)
cp = sorted((s[x], s[y]) for s in crit if all(v.is_real for v in s.values()))
check("Q5a real critical points (0,0),(1,1/2)", cp == [(0, 0), (1, R(1, 2))])
Hs = sp.hessian(f5, (x, y))
H0 = Hs.subs({x: 0, y: 0}); H1 = Hs.subs({x: 1, y: R(1, 2)})
check("Q5a det H(0,0)=-36 saddle", H0.det() == -36)
check("Q5a det H(1,1/2)=108>0 and fxx=6>0 min", H1.det() == 108 and H1[0, 0] == 6)
check("Q5a f(1,1/2)=0", f5.subs({x: 1, y: R(1, 2)}) == 0)
rng = np.random.default_rng(2)
d = rng.normal(size=(20000, 2))*0.05
f5n = lambda a, b: a**3 + 8*b**3 - 6*a*b + 1
check("Q5a (1,1/2) local min numerically", (f5n(1 + d[:, 0], 0.5 + d[:, 1]) >= f5n(1, 0.5) - 1e-12).all())
v0 = f5n(d[:, 0], d[:, 1]) - 1
check("Q5a (0,0) saddle numerically", (v0 > 0).any() and (v0 < 0).any())

# ---- Q5b: 1/(1-3x^2)
f6 = 1/(1 - 3*x**2)
ser = sp.series(f6, x, 0, 14).removeO()
check("Q5b coefficients 3^m x^(2m)", all(ser.coeff(x, 2*m) == 3**m and ser.coeff(x, 2*m + 1) == 0 for m in range(0, 7)))
check("Q5b radius 1/sqrt3", min(abs(p) for p in sp.solve(1 - 3*x**2, x)) == 1/sp.sqrt(3))
check("Q5b f^(5)(0)=0", sp.diff(f6, x, 5).subs(x, 0) == 0)
check("Q5b endpoints diverge (terms 3^m (1/sqrt3)^(2m) = 1 do not tend to 0)", sp.simplify(3**n*(1/sp.sqrt(3))**(2*n)) == 1)

# ---- contours.json
contours = [
    {"id": "24A-A-Q4b", "f": "x*y", "constraint": "x^2+y^2=2", "kind": "lagrange",
     "domain": [[-2, 2], [-2, 2]],
     "critical_points": [
         {"x": 1, "y": 1, "f": 1, "role": "abs max"},
         {"x": -1, "y": -1, "f": 1, "role": "abs max"},
         {"x": 1, "y": -1, "f": -1, "role": "abs min"},
         {"x": -1, "y": 1, "f": -1, "role": "abs min"}]},
    {"id": "24A-A-Q5a", "f": "x^3+8*y^3-6*x*y+1", "constraint": None, "kind": "unconstrained",
     "domain": [[-1.5, 2], [-1, 1.5]],
     "critical_points": [
         {"x": 0, "y": 0, "f": 1, "role": "saddle"},
         {"x": 1, "y": 0.5, "f": 0, "role": "local min"}]},
]
(HERE / "contours.json").write_text(json.dumps(contours, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ALL OK:", len(ok), "checks")
