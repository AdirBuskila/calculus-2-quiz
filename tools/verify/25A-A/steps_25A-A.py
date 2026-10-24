# -*- coding: utf-8 -*-
"""Machine checks for every numeric / choice value used in the guided steps of sitting 25A-A.
Run: PYTHONUTF8=1 py tools/verify/25A-A/steps_25A-A.py   (asserts; prints the checked names)"""
import sympy as sp
import numpy as np
from scipy import integrate as si

R = sp.Rational
x, y, k, t, u, v = sp.symbols("x y k t u v", real=True)
ok = []


def check(name, cond):
    assert cond, "MISMATCH: " + name
    ok.append(name)


# ---- Q1a ----
f1 = 4*x**3*y/(3*x**6 + 2*y**2)
check("Q1a limit along y=x^3 (k=1) is 4/5", sp.limit(f1.subs(y, x**3), x, 0) == R(4, 5))
check("Q1a limit along y=0 is 0 (so the limit depends on the path)", sp.limit(f1.subs(y, 0), x, 0) == 0)
check("Q1a limit along y=x (all lines give 0)", sp.limit(f1.subs(y, x), x, 0) == 0)
h = sp.Symbol("h", real=True)
check("Q1a f_x(0,0)=0", sp.limit(f1.subs({x: h, y: 0})/h, h, 0) == 0)
check("Q1a f_y(0,0)=0", sp.limit(f1.subs({x: 0, y: h})/h, h, 0) == 0)

# ---- Q1b ----
f2 = y**4 - x**4
lam = sp.Symbol("lam")
L = f2 + lam*(x**2 + y**2 - 9)
sol = sp.solve([sp.diff(L, x), sp.diff(L, y), x**2 + y**2 - 9], [x, y, lam], dict=True)
pts = {(s[x], s[y]) for s in sol}
check("Q1b boundary points are exactly (+-3,0),(0,+-3)", pts == {(3, 0), (-3, 0), (0, 3), (0, -3)})
check("Q1b number of boundary points is 4", len(pts) == 4)
check("Q1b f(0,3)=81", f2.subs({x: 0, y: 3}) == 81)
check("Q1b f(3,0)=-81", f2.subs({x: 3, y: 0}) == -81)
check("Q1b interior critical point is (0,0) with value 0", sp.solve([sp.diff(f2, x), sp.diff(f2, y)], [x, y], dict=True) == [{x: 0, y: 0}])
g = np.linspace(-3, 3, 1201)
X, Y = np.meshgrid(g, g)
F = np.where(X**2 + Y**2 <= 9 + 1e-9, Y**4 - X**4, np.nan)
check("Q1b grid max 81 min -81", abs(np.nanmax(F) - 81) < 1e-6 and abs(np.nanmin(F) + 81) < 1e-6)

# ---- Q2a ----
n = sp.Symbol("n", positive=True)
I1 = sp.integrate(1/(x*sp.log(x)**2), (x, 2, sp.oo))
check("Q2a integral test value 1/ln2", sp.simplify(I1 - 1/sp.log(2)) == 0)
check("Q2a 1/ln2 ~ 1.442695", abs(float(1/sp.log(2)) - 1.442695) < 1e-6)
check("Q2a limit n*... : |a_n|*sqrt(n) -> 1/2",
      sp.limit(sp.sqrt(n)*(sp.sqrt(n) - sp.sqrt(n - 1)), n, sp.oo) == R(1, 2))
check("Q2a ratio test inconclusive on 1/(n ln^2 n): ratio -> 1",
      sp.limit((n*sp.log(n)**2)/((n + 1)*sp.log(n + 1)**2), n, sp.oo) == 1)
# second series: terms decrease and -> 0
vals = [float(sp.sqrt(m) - sp.sqrt(m - 1)) for m in range(1, 200)]
check("Q2a second series terms decrease", all(a > b for a, b in zip(vals, vals[1:])))

# ---- Q2b ----
X_, Y_ = sp.symbols("X_ Y_")
sx = sp.solve([u - (x - y), v - (x + y)], [x, y], dict=True)[0]
J = sp.Matrix([sx[x], sx[y]]).jacobian([u, v]).det()
check("Q2b |J|=1/2", abs(J) == R(1, 2))
check("Q2b bounds: x+y=1,3 and x-y=-1,1",
      [sp.simplify((x + y).subs(y, c - x)) for c in (1, 3)] == [1, 3]
      and [sp.simplify((x - y).subs(y, c + x)) for c in (1, -1)] == [-1, 1])
I2 = sp.integrate(sp.integrate(u*sp.exp(u*v)*R(1, 2), (v, 1, 3)), (u, -1, 1))
check("Q2b value (1/3)sinh3 - sinh1", sp.simplify(I2 - (sp.sinh(3)/3 - sp.sinh(1))) == 0)
val2 = float(sp.sinh(3)/3 - sp.sinh(1))
check("Q2b numeric 2.1642", abs(val2 - 2.1642) < 1e-3)
# numeric cross-check in x,y directly (rotated square vertices (0,1),(1,0),(2,1),(1,2))
# region in x: lower y = |x-1|, upper y = 2-|x-1|... check shape: square with vertices (0,1),(1,0),(2,1),(1,2)
num, _ = si.dblquad(lambda yy, xx: (xx - yy)*np.exp(xx**2 - yy**2), 0, 2,
                    lambda xx: abs(xx - 1), lambda xx: 2 - abs(xx - 1))
check("Q2b numeric cross-check in (x,y)", abs(num - val2) < 1e-6)
check("Q2b u*e^(uv) from (x-y)e^(x^2-y^2)", sp.simplify(((x - y)*sp.exp(x**2 - y**2)).subs({x: (u + v)/2, y: (v - u)/2}) - u*sp.exp(u*v)) == 0)
check("Q2b inner integral e^(3u)-e^u at u=1 is e^3-e ~ 17.367",
      abs(float(sp.integrate(u*sp.exp(u*v), (v, 1, 3)).subs(u, 1) - (sp.exp(3) - sp.exp(1)))) < 1e-9 and abs(float(sp.exp(3) - sp.E) - 17.3673) < 1e-3)

# ---- Q3a ----
a = lambda m: 2**m/sp.sqrt(5*m**2 + 1)
check("Q3a radius 1/2", sp.limit(a(n)/a(n + 1), n, sp.oo) == R(1, 2))
check("Q3a endpoint x-1=1/2: n*a_n -> 1/sqrt5 (compare with harmonic, diverges)",
      sp.limit(n/sp.sqrt(5*n**2 + 1), n, sp.oo) == 1/sp.sqrt(5))
check("Q3a 1/sqrt5 ~ 0.4472", abs(float(1/sp.sqrt(5)) - 0.4472) < 1e-4)
check("Q3a left endpoint terms 1/sqrt(5n^2+1) decrease to 0",
      sp.limit(1/sp.sqrt(5*n**2 + 1), n, sp.oo) == 0)
check("Q3a x=1/2 -> x-1=-1/2, x=3/2 -> x-1=1/2", R(1, 2) - 1 == -R(1, 2) and R(3, 2) - 1 == R(1, 2))

# ---- Q3b ----
gf = sp.Function("g")
U = x**2 - y**2
z = y*gf(U)
zx, zy = sp.diff(z, x), sp.diff(z, y)
gp = sp.Function("gp")  # g'(u) placeholder
uu = sp.Symbol("uu")
zx_c = zx.subs(sp.Derivative(gf(U), x), 0)  # not used
Z = sp.Function("g")(sp.Symbol("w"))
w = sp.Symbol("w")
gx = sp.diff(z, x).doit()
# express with g'(u): substitute Subs form
gu = sp.Function("G")  # G = g
Zf = y*gu(x**2 - y**2)
zxf, zyf = sp.diff(Zf, x), sp.diff(Zf, y)
lhs = zxf/x + zyf/y
check("Q3b identity (1/x)zx+(1/y)zy - z/y^2 = 0", sp.simplify(lhs - Zf/y**2) == 0)
# check the stored partial formulas by plugging g = sin, g = exp, g = t^3
for gg in (sp.sin, sp.exp, lambda s: s**3):
    Zc = y*gg(x**2 - y**2)
    gprime = lambda s, gg=gg: sp.diff(gg(w), w).subs(w, s)
    check("Q3b zx formula 2xy g'(u)", sp.simplify(sp.diff(Zc, x) - 2*x*y*gprime(x**2 - y**2)) == 0)
    check("Q3b zy formula g(u)-2y^2 g'(u)", sp.simplify(sp.diff(Zc, y) - (gg(x**2 - y**2) - 2*y**2*gprime(x**2 - y**2))) == 0)
    # the bugged variants must fail the identity
    bad_y = gg(x**2 - y**2) + 2*y**2*gprime(x**2 - y**2)
    bad = sp.simplify(sp.diff(Zc, x)/x + bad_y/y - Zc/y**2)
    check("Q3b sign-bug variant breaks the identity", bad != 0)

# ---- Q4a ----
inner_swapped = sp.integrate(sp.sin(sp.pi*x**2/2), (y, 0, x))
check("Q4a inner integral is x sin(pi x^2/2)", sp.simplify(inner_swapped - x*sp.sin(sp.pi*x**2/2)) == 0)
val4 = sp.integrate(x*sp.sin(sp.pi*x**2/2), (x, 0, 1))
check("Q4a value 1/pi", sp.simplify(val4 - 1/sp.pi) == 0)
check("Q4a 1/pi ~ 0.31831", abs(float(1/sp.pi) - 0.31831) < 1e-5)
num4, _ = si.dblquad(lambda xx, yy: np.sin(np.pi*xx**2/2), 0, 1, lambda yy: yy, lambda yy: 1)
check("Q4a numeric original order", abs(num4 - 1/np.pi) < 1e-7)
num4b, _ = si.dblquad(lambda yy, xx: np.sin(np.pi*xx**2/2), 0, 1, lambda xx: 0, lambda xx: xx)
check("Q4a numeric swapped order 0<=y<=x equals", abs(num4b - 1/np.pi) < 1e-7)
num4c, _ = si.dblquad(lambda yy, xx: np.sin(np.pi*xx**2/2), 0, 1, lambda xx: xx, lambda xx: 1)
check("Q4a wrong order (x<=y<=1) gives a different value", abs(num4c - 1/np.pi) > 1e-2)
num4d, _ = si.dblquad(lambda xx, yy: np.sin(np.pi*xx**2/2), 0, 1, lambda yy: 0, lambda yy: yy)
check("Q4a wrong order (0<=x<=y) gives a different value", abs(num4d - 1/np.pi) > 1e-2)
check("Q4a upper limit of t-integral is x^2/2 at x=1 = 1/2", R(1, 2) == (1**2)/R(2))
check("Q4a t-integral value 1/pi", sp.simplify(sp.integrate(sp.sin(sp.pi*t), (t, 0, R(1, 2))) - 1/sp.pi) == 0)

# ---- Q4b ----
f4 = (x**2 - 2*y**2)*sp.exp(x - y)
crit = sp.solve([sp.diff(f4, x), sp.diff(f4, y)], [x, y], dict=True)
cs = {(s[x], s[y]) for s in crit}
check("Q4b critical points (0,0) and (-4,-2) only", cs == {(0, 0), (-4, -2)})
check("Q4b added equations give x=2y",
      sp.simplify(((2*x + x**2 - 2*y**2) + (-4*y - x**2 + 2*y**2)) - (2*x - 4*y)) == 0)
check("Q4b y2=-2", sp.solve((4*y + 2*y**2), y) == [-2, 0] or set(sp.solve(4*y + 2*y**2, y)) == {0, -2})
H = sp.hessian(f4, (x, y))
H0 = H.subs({x: 0, y: 0})
check("Q4b Hessian at origin diag(2,-4), det -8", H0 == sp.Matrix([[2, 0], [0, -4]]) or H0.det() == -8)
check("Q4b origin det = -8", H0.det() == -8)
H1 = sp.simplify(H.subs({x: -4, y: -2}))
check("Q4b (-4,-2): det>0 and f_xx<0 (local max)", H1.det() > 0 and H1[0, 0] < 0)
check("Q4b origin is a saddle", H0.det() < 0)

# ---- Q5a ----
f5 = sp.sqrt(x**2 + 2*y)
gr = sp.Matrix([sp.diff(f5, x), sp.diff(f5, y)]).subs({x: 4, y: 10})
check("Q5a f_x(4,10)=2/3", gr[0] == R(2, 3))
check("Q5a f_y(4,10)=1/6", gr[1] == R(1, 6))
check("Q5a max rate sqrt17/6", sp.simplify(gr.norm() - sp.sqrt(17)/6) == 0)
check("Q5a sqrt17/6 ~ 0.6872", abs(float(sp.sqrt(17)/6) - 0.6872) < 1e-4)
d = gr/gr.norm()
check("Q5a unit direction (4,1)/sqrt17", sp.simplify(d - sp.Matrix([4, 1])/sp.sqrt(17)) == sp.zeros(2, 1))
check("Q5a (4,1) is not a unit vector", sp.Matrix([4, 1]).norm() != 1)
check("Q5a derivative along (-4,-1)/sqrt17 is negative", (gr.T*(-sp.Matrix([4, 1])/sp.sqrt(17)))[0] < 0)
check("Q5a derivative along (1,4)/sqrt17 is smaller than max", (gr.T*(sp.Matrix([1, 4])/sp.sqrt(17)))[0] < gr.norm())

# ---- Q5b ----
f6 = sp.log(1 + x**2) - sp.exp(2*x)
ser = sp.series(f6, x, 0, 8).removeO()
a6 = ser.coeff(x, 6)
check("Q5b ln part coefficient of x^6 is 1/3", sp.series(sp.log(1 + x**2), x, 0, 8).removeO().coeff(x, 6) == R(1, 3))
check("Q5b exp part coefficient of x^6 is 64/720", sp.series(sp.exp(2*x), x, 0, 8).removeO().coeff(x, 6) == R(64, 720))
check("Q5b a6 = 11/45", a6 == R(11, 45))
check("Q5b 11/45 ~ 0.24444", abs(float(R(11, 45)) - 0.24444) < 1e-4)
check("Q5b f^(6)(0)=176", sp.diff(f6, x, 6).subs(x, 0) == 176)
check("Q5b a6*720 = 176", a6*720 == 176)
check("Q5b radius of ln(1+x^2) series is 1",
      sp.limit(sp.Abs((-1)**(n + 1)/n)/sp.Abs((-1)**(n + 2)/(n + 1)), n, sp.oo) == 1)

print(f"{len(ok)} checks passed")
for s in ok:
    print(" -", s)
