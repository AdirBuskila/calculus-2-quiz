# -*- coding: utf-8 -*-
"""Solver checks for sitting 23A-C (no key). Every computation in the solved solutions of gen_23A-C.py.
Run: PYTHONUTF8=1 py tools/verify/23A-C/solve_23A-C.py"""
import math
import numpy as np
import sympy as sp
from scipy import integrate as si

x, y, z, t, n = sp.symbols("x y z t n", real=True)
r, th = sp.symbols("r theta", real=True)
R = sp.Rational
ok = []


def check(name, cond):
    assert cond, "MISMATCH: " + name
    ok.append(name)
    print("ok", name)


# ===== Q1a: area between x^2+y^2=2x and x^2+y^2=4x =====
A = sp.integrate(sp.integrate(r, (r, 2*sp.cos(th), 4*sp.cos(th))), (th, -sp.pi/2, sp.pi/2))
check("Q1a polar area 3pi", sp.simplify(A - 3*sp.pi) == 0)
check("Q1a inner integral = 6cos^2", sp.simplify(sp.integrate(r, (r, 2*sp.cos(th), 4*sp.cos(th))) - 6*sp.cos(th)**2) == 0)
check("Q1a polar form r=2cos", sp.simplify((r**2 - 2*r*sp.cos(th)).subs(r, 2*sp.cos(th))) == 0)
# cartesian order dx dy: for |y|<=1 between the two circles' right halves... use numeric instead
num = si.dblquad(lambda yy, xx: 1.0, 0, 4,
                 lambda xx: -math.sqrt(max(4*xx - xx*xx, 0)), lambda xx: math.sqrt(max(4*xx - xx*xx, 0)))[0] \
    - si.dblquad(lambda yy, xx: 1.0, 0, 2,
                 lambda xx: -math.sqrt(max(2*xx - xx*xx, 0)), lambda xx: math.sqrt(max(2*xx - xx*xx, 0)))[0]
check("Q1a numeric area (cartesian) = 3pi", abs(num - 3*math.pi) < 1e-6)
gx, gy = np.meshgrid(np.linspace(0, 4, 4001), np.linspace(-2, 2, 4001))
mk = (gx**2 + gy**2 <= 4*gx) & (gx**2 + gy**2 >= 2*gx)
check("Q1a grid area ~ 3pi", abs(mk.sum()*(4/4000)**2 - 3*math.pi) < 0.02)

# ===== Q1b =====
f = x**2*y*sp.sqrt(z)
pt = {x: 2, y: 1, z: 1}
grad = [sp.diff(f, v).subs(pt) for v in (x, y, z)]
check("Q1b grad = (4,4,2)", grad == [4, 4, 2])
gnorm = sp.sqrt(sum(g**2 for g in grad))
check("Q1b |grad| = 6", gnorm == 6)
u = sp.Matrix([1, 2, 2]) / 3
Du = sum(grad[i]*u[i] for i in range(3))
check("Q1b D_u f = 16/3", Du == R(16, 3))
check("Q1b ratio = 9/8", sp.simplify(gnorm/Du) == R(9, 8))

# ===== Q2a =====
check("Q2a(1) |a_n| <= (2/3)^n, geometric sum = 2", sp.summation((R(2, 3))**n, (n, 1, sp.oo)) == 2)
s1 = sum((2/3)**k*math.cos(k) for k in range(1, 200))
check("Q2a(1) partial sums settle", abs(s1 - sum((2/3)**k*math.cos(k) for k in range(1, 400))) < 1e-12)
lim_root = sp.limit(sp.atan((n + 2)/(n + 3)), n, sp.oo)
check("Q2a(2) root-test limit = pi/4 < 1", lim_root == sp.pi/4 and float(lim_root) < 1)
check("Q2a(2) terms positive (arg in (0,1))", all(0 < (k + 2)/(k + 3) < 1 for k in range(1, 1000)))

# ===== Q2b =====
fp = (x**3 + y**3)/(2*x**2 + y**2)
h = sp.symbols("h", real=True)
fx0 = sp.limit(fp.subs({x: h, y: 0})/h, h, 0)
fy0 = sp.limit(fp.subs({x: 0, y: h})/h, h, 0)
check("Q2b f_x(0,0)=1/2, f_y(0,0)=1", fx0 == R(1, 2) and fy0 == 1)
numer = sp.simplify(fp - x/2 - y)
check("Q2b f - x/2 - y = -xy(4x+y)/(2(2x^2+y^2))",
      sp.simplify(numer + x*y*(4*x + y)/(2*(2*x**2 + y**2))) == 0)
E = numer/sp.sqrt(x**2 + y**2)
s = sp.symbols("s", positive=True)
check("Q2b along y=x (x>0): E -> -5/(6sqrt2)", sp.simplify(sp.limit(E.subs({x: s, y: s}), s, 0) + 5/(6*sp.sqrt(2))) == 0)
check("Q2b along y=0: E -> 0", sp.limit(E.subs({x: s, y: 0}), s, 0) == 0)
check("Q2b continuity: |f| <= |x|+|y| (polar limit 0)",
      sp.limit((fp.subs({x: r*sp.cos(th), y: r*sp.sin(th)})).subs(th, R(7, 10)), r, 0) == 0)
# numeric bound: |f| <= (|x|^3+|y|^3)/(x^2+y^2/...) check on a grid
pts = np.random.default_rng(1).uniform(-1, 1, (20000, 2))
fv = (pts[:, 0]**3 + pts[:, 1]**3)/(2*pts[:, 0]**2 + pts[:, 1]**2)
check("Q2b numeric |f| <= |x|+|y|", np.all(np.abs(fv) <= np.abs(pts[:, 0]) + np.abs(pts[:, 1]) + 1e-12))

# ===== Q3a =====
an = 1/(2**n + 3**n)
check("Q3a root: (2^n+3^n)^(1/n) -> 3", sp.limit((2**n + 3**n)**(1/n), n, sp.oo) == 3)
check("Q3a ratio: a_n/a_(n+1) -> 3", sp.limit(an/an.subs(n, n + 1), n, sp.oo) == 3)
check("Q3a x=3: |term| -> 1 (not 0)", sp.limit(3**n/(2**n + 3**n), n, sp.oo) == 1)

# ===== Q3b =====
g = sp.Function("g")
zz = y*g(x**2 - y**2)
lhs = sp.diff(zz, x)/x + sp.diff(zz, y)/y
check("Q3b identity holds", sp.simplify(lhs - zz/y**2) == 0)

# ===== Q4a =====
F = x**2*y + sp.exp(y)*x + y**3   # non-symmetric test integrand
b1 = sp.integrate(sp.integrate(F, (y, 0, sp.sqrt(x + 4))), (x, -4, 0)) + sp.integrate(sp.integrate(F, (y, 0, 2 - x)), (x, 0, 2))
b2 = sp.integrate(sp.integrate(F, (x, y**2 - 4, 2 - y)), (y, 0, 2))
check("Q4a swapped order equals original (test integrand)", sp.simplify(b1 - b2) == 0)
check("Q4a y=sqrt(x+4) <=> x=y^2-4 (y>=0)", sp.simplify(sp.sqrt((y**2 - 4) + 4).subs(y, 2) - 2) == 0)
check("Q4a area 22/3 both orders",
      sp.integrate(sp.sqrt(x + 4), (x, -4, 0)) + sp.integrate(2 - x, (x, 0, 2)) == R(22, 3)
      and sp.integrate(2 - y - (y**2 - 4), (y, 0, 2)) == R(22, 3))

# ===== Q4b =====
f4 = x**2 + y**2 + 4*x*y
check("Q4b grad=0 only at (0,0)", sp.solve([sp.diff(f4, x), sp.diff(f4, y)], [x, y], dict=True) == [{x: 0, y: 0}])
check("Q4b edge y=0: f=x^2 on [0,1]", sp.expand(f4.subs(y, 0)) == x**2)
check("Q4b edge y=sqrt3 x: f=(4+4sqrt3)x^2 on [0,1/2]", sp.expand(f4.subs(y, sp.sqrt(3)*x) - (4 + 4*sp.sqrt(3))*x**2) == 0)
farc = sp.simplify(f4.subs({x: sp.cos(th), y: sp.sin(th)}))
check("Q4b arc f=1+2sin2theta", sp.simplify(farc - 1 - 2*sp.sin(2*th)) == 0)
crit = sp.solve(sp.diff(1 + 2*sp.sin(2*th), th), th)
check("Q4b arc critical theta in [0,pi/3] = pi/4", [c for c in crit if 0 <= c <= sp.pi/3] == [sp.pi/4])
# Lagrange cross-check on the arc
lam = sp.symbols("lam", real=True)
L = sp.solve([2*x + 4*y - 2*lam*x, 2*y + 4*x - 2*lam*y, x**2 + y**2 - 1], [x, y, lam], dict=True)
inside = [s_ for s_ in L if s_[x] >= 0 and s_[y] >= 0 and s_[y] <= sp.sqrt(3)*s_[x]]
check("Q4b Lagrange on arc: only (1/sqrt2,1/sqrt2) in the sector, f=3",
      len(inside) == 1 and sp.simplify(f4.subs(inside[0]) - 3) == 0)
vals = {"(0,0)": f4.subs({x: 0, y: 0}), "(1,0)": f4.subs({x: 1, y: 0}),
        "(1/2,sqrt3/2)": sp.simplify(f4.subs({x: R(1, 2), y: sp.sqrt(3)/2})),
        "(1/sqrt2,1/sqrt2)": sp.simplify(f4.subs({x: 1/sp.sqrt(2), y: 1/sp.sqrt(2)}))}
check("Q4b candidate values 0,1,1+sqrt3,3",
      vals["(0,0)"] == 0 and vals["(1,0)"] == 1 and sp.simplify(vals["(1/2,sqrt3/2)"] - 1 - sp.sqrt(3)) == 0
      and vals["(1/sqrt2,1/sqrt2)"] == 3)
gx, gy = np.meshgrid(np.linspace(0, 1, 3001), np.linspace(0, 1, 3001))
mk = (gx**2 + gy**2 <= 1) & (gy <= math.sqrt(3)*gx)
fv = (gx**2 + gy**2 + 4*gx*gy)[mk]
check("Q4b grid max 3, min 0", abs(fv.max() - 3) < 1e-3 and fv.min() == 0)

# ===== Q5a =====
f5 = (x**2 - 2*y**2)*sp.exp(x - y)
f5x, f5y = sp.diff(f5, x), sp.diff(f5, y)
check("Q5a f_x = (x^2+2x-2y^2)e^(x-y)", sp.simplify(f5x - (x**2 + 2*x - 2*y**2)*sp.exp(x - y)) == 0)
check("Q5a f_y = (-x^2-4y+2y^2)e^(x-y)", sp.simplify(f5y - (-x**2 - 4*y + 2*y**2)*sp.exp(x - y)) == 0)
cps = sorted((s_[x], s_[y]) for s_ in sp.solve([f5x, f5y], [x, y], dict=True))
check("Q5a critical points (-4,-2),(0,0)", cps == [(-4, -2), (0, 0)])
H = sp.hessian(f5, (x, y))
H0 = H.subs({x: 0, y: 0})
check("Q5a Hessian at (0,0) = [[2,0],[0,-4]], D=-8 saddle", H0 == sp.Matrix([[2, 0], [0, -4]]) and H0.det() == -8)
H1 = sp.simplify(H.subs({x: -4, y: -2}))
e2 = sp.exp(-2)
check("Q5a Hessian at (-4,-2) = e^-2 [[-6,8],[8,-12]]", sp.simplify(H1 - e2*sp.Matrix([[-6, 8], [8, -12]])) == sp.zeros(2))
check("Q5a D(-4,-2)=8e^-4>0, f_xx<0 -> local max", sp.simplify(H1.det() - 8*sp.exp(-4)) == 0 and H1[0, 0] < 0)
check("Q5a f(-4,-2)=8e^-2", sp.simplify(f5.subs({x: -4, y: -2}) - 8*e2) == 0)
ff = sp.lambdify((x, y), f5, "numpy")
gx, gy = np.meshgrid(np.linspace(-4.3, -3.7, 601), np.linspace(-2.3, -1.7, 601))
check("Q5a grid: (-4,-2) is a local max", abs(ff(gx, gy).max() - 8*math.exp(-2)) < 1e-9)
check("Q5a (0,0) saddle: f(x,0)=x^2e^x>0, f(0,y)=-2y^2e^-y<0 near 0",
      ff(0.01, 0) > 0 and ff(-0.01, 0) > 0 and ff(0, 0.01) < 0 and ff(0, -0.01) < 0)

# ===== Q5b =====
f6 = 1/(x**2 + x - 2)
check("Q5b partial fractions 1/3(1/(x-1) - 1/(x+2))", sp.simplify(f6 - R(1, 3)*(1/(x - 1) - 1/(x + 2))) == 0)
ser = sp.series(f6, x, 0, 12).removeO()
coef = lambda k: -R(1, 3)*(1 + R((-1)**k, 2**(k + 1)))
check("Q5b coefficients a_k = -(1/3)(1+(-1)^k/2^(k+1)) for k<12",
      all(sp.simplify(ser.coeff(x, k) - coef(k)) == 0 for k in range(12)))
d10 = sp.diff(f6, x, 10).subs(x, 0)
check("Q5b f^(10)(0) = -10!/3 * 2049/2048", sp.simplify(d10 + sp.factorial(10)*R(2049, 3*2048)) == 0)
check("Q5b f^(10)(0) = -9681525/8", d10 == R(-9681525, 8))
print("Q5b f^(10)(0) =", d10, "=", float(d10))
check("Q5b radius 1 (nearest pole x=1)", sp.limit((1 + 1/2**(n + 1))/(1 + 1/2**(n + 2)), n, sp.oo) == 1)
check("Q5b x=+-1 terms do not tend to 0 (|a_k| -> 1/3)", sp.limit(sp.Abs(-R(1, 3)*(1 + 1/2**(n + 1))), n, sp.oo) == R(1, 3))

print("ALL OK:", len(ok), "checks")
