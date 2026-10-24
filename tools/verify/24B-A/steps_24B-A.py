# -*- coding: utf-8 -*-
"""Machine checks for every numeric / choice value used in the guided steps of sitting 24B-A.
Run: PYTHONUTF8=1 py tools/verify/24B-A/steps_24B-A.py"""
import sympy as sp
import numpy as np

R = sp.Rational
x, y, z, k, n = sp.symbols("x y z k n", real=True)
ok = []


def check(name, cond):
    assert cond, "MISMATCH: " + name
    ok.append(name)


# ---- Q1 ----
f1 = y*x**2/(2*y**2 + 3*x**4)
check("Q1a limit along y=x^2 is 1/5", sp.limit(f1.subs(y, x**2), x, 0) == R(1, 5))
check("Q1a limits along y=kx are 0", sp.limit(f1.subs(y, k*x), x, 0) == 0)
h = sp.Symbol("h", real=True)
check("Q1b f_x(0,0)=0", sp.limit(f1.subs({x: h, y: 0})/h, h, 0) == 0)
check("Q1b f_y(0,0)=0", sp.limit(f1.subs({x: 0, y: h})/h, h, 0) == 0)
fx = sp.diff(f1, x).subs({x: 1, y: 1})
fy = sp.diff(f1, y).subs({x: 1, y: 1})
check("Q1c f_x(1,1)=-2/25", fx == R(-2, 25))
check("Q1c f_y(1,1)=1/25", fy == R(1, 25))
check("Q1c -2/25=-0.08, 1/25=0.04", float(fx) == -0.08 and float(fy) == 0.04)

# ---- Q2a ----
m = np.arange(1, 200001)
check("Q2a (3+sin sqrt n) <= 4 and the bound is attained near 1", np.max(3 + np.sin(np.sqrt(m))) <= 4 and np.max(3 + np.sin(np.sqrt(m))) > 3.999)
check("Q2a sum 4/n^2 converges (p=2): value 2*pi^2/3", sp.summation(4/n**2, (n, 1, sp.oo)) == 2*sp.pi**2/3)
check("Q2a terms |a_n| <= 4/n^2 numerically", bool(np.all((3 + np.sin(np.sqrt(m)))/m**2 <= 4/m**2 + 1e-15)))
# the harmonic bound 4/n would also hold but gives no conclusion (diverges)
check("Q2a sum 4/n diverges", sp.summation(1/n, (n, 1, sp.oo)) == sp.oo)

# ---- Q2b ----
a = lambda q: 1/((q + 1)*sp.log(q + 1))
vals = [float(a(q)) for q in range(1, 400)]
check("Q2b a_n positive, decreasing", all(v > 0 for v in vals) and all(p > q for p, q in zip(vals, vals[1:])))
check("Q2b a_n -> 0", sp.limit(a(n), n, sp.oo) == 0)
T = sp.Symbol("T", positive=True)
Iabs = sp.integrate(1/((x + 1)*sp.log(x + 1)), (x, 1, T))
check("Q2b int_1^T dx/((x+1)ln(x+1)) = lnln(T+1)-lnln2 -> infinity",
      sp.simplify(Iabs - (sp.log(sp.log(T + 1)) - sp.log(sp.log(2)))) == 0 and sp.limit(Iabs, T, sp.oo) == sp.oo)
check("Q2b alternating partial sums converge numerically (diff of consecutive sums tiny)",
      abs(sum((-1)**q*float(a(q)) for q in range(1, 20001)) - sum((-1)**q*float(a(q)) for q in range(1, 20002))) < 1e-3)
check("Q2b ratio test inconclusive (->1)", sp.limit(a(n + 1)/a(n), n, sp.oo) == 1)

# ---- Q3 ----
f3 = 2*x**2 - y**2 + 1
gr = sp.Matrix([sp.diff(f3, x), sp.diff(f3, y)]).subs({x: 2, y: 3})
check("Q3a grad (8,-6)", gr == sp.Matrix([8, -6]))
check("Q3b norm 10, squared 100", gr.norm() == 10 and gr.dot(gr) == 100)
check("Q3b directional derivative along (3,4)/5 is 0 < 10", (gr.T*sp.Matrix([3, 4])/5)[0] == 0)
crit = sp.solve([sp.diff(f3, x), sp.diff(f3, y)], [x, y], dict=True)
check("Q3c exactly one critical point (0,0)", crit == [{x: 0, y: 0}])
H = sp.hessian(f3, (x, y))
check("Q3c AC-B^2 = -8, saddle", H.det() == -8)
lam = sp.Symbol("lam")
L = f3 - lam*((x - 1)**2 + y**2 - 1)
sol = sp.solve([sp.diff(L, x), sp.diff(L, y), (x - 1)**2 + y**2 - 1], [x, y, lam], dict=True)
pts = {(q[x], q[y]) for q in sol}
want = {(0, 0), (2, 0), (R(1, 3), sp.sqrt(5)/3), (R(1, 3), -sp.sqrt(5)/3)}
check("Q3d Lagrange points M1..M4", pts == want)
check("Q3d four points", len(pts) == 4)
vals = {p: sp.simplify(f3.subs({x: p[0], y: p[1]})) for p in pts}
check("Q3d f(2,0)=9", vals[(2, 0)] == 9)
check("Q3d f(1/3,sqrt5/3)=2/3 and f(0,0)=1", vals[(R(1, 3), sp.sqrt(5)/3)] == R(2, 3) and vals[(0, 0)] == 1)
g = np.linspace(-0.001, 2.001, 1201)
gy = np.linspace(-1.001, 1.001, 1201)
X, Y = np.meshgrid(g, gy)
F = np.where((X - 1)**2 + Y**2 <= 1, 2*X**2 - Y**2 + 1, np.nan)
check("Q3d grid max 9, min 2/3", abs(np.nanmax(F) - 9) < 1e-2 and abs(np.nanmin(F) - 2/3) < 1e-3)
check("Q3d (0,0) is on the boundary", (0 - 1)**2 + 0 == 1)

# ---- Q4a ----
F = 2*x**2 - y**2 + z**2
P = {x: 1, y: -1, z: 2}
check("Q4a point on surface", F.subs(P) == 5)
check("Q4a gradient (4,2,4)", [sp.diff(F, v).subs(P) for v in (x, y, z)] == [4, 2, 4])
plane = 4*(x - 1) + 2*(y + 1) + 4*(z - 2)
check("Q4a plane passes through the point", plane.subs(P) == 0)
bad1 = 4*(x - 1) - 2*(y + 1) + 4*(z - 2)
bad2 = 4*(x + 1) + 2*(y - 1) + 4*(z + 2)
bad3 = 2*(x - 1) + 4*(y + 1) + 4*(z - 2)
check("Q4a distractors are different planes (normals not parallel to (4,2,4) or not through the point)",
      sp.Matrix([4, -2, 4]).cross(sp.Matrix([4, 2, 4])) != sp.zeros(3, 1)
      and bad2.subs(P) != 0
      and sp.Matrix([2, 4, 4]).cross(sp.Matrix([4, 2, 4])) != sp.zeros(3, 1))

# ---- Q4b ----
an = 2**n*sp.factorial(n)/sp.factorial(2*n)
check("Q4b a_2 = 1/3", an.subs(n, 2) == R(1, 3))
ratio = sp.simplify(sp.combsimp(an/an.subs(n, n + 1)))
check("Q4b a_n/a_(n+1) = 2n+1", sp.simplify(ratio - (2*n + 1)) == 0)
check("Q4b ratio at n=3 is 7", ratio.subs(n, 3) == 7)
check("Q4b radius infinity", sp.limit(ratio, n, sp.oo) == sp.oo)

# ---- Q5 ----
f5 = sp.log(2*x**2 + 3*x + 1)
check("Q5a factor (x+1)(2x+1)", sp.expand((x + 1)*(2*x + 1)) == 2*x**2 + 3*x + 1)
ser = sp.series(f5, x, 0, 7).removeO()
check("Q5a coefficient formula (-1)^(n+1)(1+2^n)/n for n=1..6",
      all(ser.coeff(x, q) == R((-1)**(q + 1)*(1 + 2**q), q) for q in range(1, 7)))
check("Q5a a_3 = 3", ser.coeff(x, 3) == 3)
check("Q5a a_2 = -5/2", ser.coeff(x, 2) == R(-5, 2))
check("Q5b root test: ((1+2^n)/n)^(1/n) -> 2",
      sp.limit(((1 + 2**n)/n)**(1/n), n, sp.oo) == 2)
S = sum((-1)**(q + 1)*(1 + 2.0**(-q))/q for q in range(1, 40001))
check("Q5b right endpoint x=1/2: alternating sum converges to ln3 (slowly)", abs(S - float(sp.log(3))) < 1e-3)
check("Q5b value at x=1/2 is ln(3)", sp.simplify(f5.subs(x, R(1, 2)) - sp.log(3)) == 0)
check("Q5b left endpoint x=-1/2: 2x+1=0, ln(2x+1) undefined (series diverges)", (2*(-R(1, 2)) + 1) == 0)
terms = [float((1 + 2**q)/q*R(1, 2)**q) for q in range(1, 60)]
check("Q5b left endpoint terms ~ 1/n (harmonic, diverges): n*term -> 1", abs(terms[-1]*59 - 1) < 0.05)
check("Q5c a_5 = 33/5", ser.coeff(x, 5) == R(33, 5) if False else sp.series(f5, x, 0, 7).removeO().coeff(x, 5) == R(33, 5))
check("Q5c f^(5)(0)=792", sp.diff(f5, x, 5).subs(x, 0) == 792)
check("Q5c 33*4! = 792", 33*24 == 792)

print(f"{len(ok)} checks passed")
for q in ok:
    print(" -", q)
