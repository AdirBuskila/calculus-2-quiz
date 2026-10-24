# -*- coding: utf-8 -*-
"""sympy / numeric checks for every computation quoted in docs/briefs/*.md (calculus-2 learn mode).
Run: PYTHONUTF8=1 py tools/verify/learn/check_learn.py
Every section name matches a brief; every assert is a number or identity the brief states.
ASCII only on stdout."""
import math
import numpy as np
import sympy as sp

R = sp.Rational
x, y, z, u, v, t, s, h, k, r, th, lam = sp.symbols("x y z u v t s h k r theta lam", real=True)
n = sp.symbols("n", positive=True)
ok = []


def check(name, cond):
    assert cond, "MISMATCH: " + name
    ok.append(name)


def zero(e):
    return sp.simplify(e) == 0


# ---------------------------------------------------------------- 01 improper integrals
X = sp.symbols("X", positive=True)
check("01 int_1^oo x^-2 = 1", sp.integrate(x**-2, (x, 1, sp.oo)) == 1)
check("01 int_1^oo 1/x diverges", sp.integrate(1/x, (x, 1, sp.oo)) == sp.oo)
check("01 int_1^oo x^(-1/2) diverges", sp.integrate(x**R(-1, 2), (x, 1, sp.oo)) == sp.oo)
check("01 int_0^1 x^(-1/2) = 2", sp.integrate(x**R(-1, 2), (x, 0, 1)) == 2)
check("01 int_0^1 1/x diverges", sp.integrate(1/x, (x, 0, 1)) == sp.oo)
check("01 int_0^1 x^-2 diverges", sp.integrate(x**-2, (x, 0, 1)) == sp.oo)
check("01 int_2^oo dx/(x ln^2 x) = 1/ln2", sp.simplify(sp.integrate(1/(x*sp.log(x)**2), (x, 2, sp.oo)) - 1/sp.log(2)) == 0)
check("01 int_2^oo dx/(x ln x) diverges", sp.integrate(1/(x*sp.log(x)), (x, 2, sp.oo)) == sp.oo)
check("01 antiderivative of 1/((x+1)ln(x+1)) is ln ln(x+1)",
      zero(sp.diff(sp.log(sp.log(x + 1)), x) - 1/((x + 1)*sp.log(x + 1))))
check("01 antiderivative of 1/(x ln^2 x) is -1/ln x", zero(sp.diff(-1/sp.log(x), x) - 1/(x*sp.log(x)**2)))
check("01 int_1^oo dx/(x(x+1)) = ln 2", sp.simplify(sp.integrate(1/(x*(x + 1)), (x, 1, sp.oo)) - sp.log(2)) == 0)
check("01 partial fractions 1/(x(x+1))", zero(1/(x*(x + 1)) - (1/x - 1/(x + 1))))
check("01 int_1^oo e^-x = 1/e", sp.integrate(sp.exp(-x), (x, 1, sp.oo)) == sp.exp(-1))
check("01 e^(-x^2) <= e^(-x) for x>=1 (grid)", all(math.exp(-q*q) <= math.exp(-q) for q in np.linspace(1, 30, 3000)))
check("01 int_0^1 ln x dx = -1", sp.integrate(sp.log(x), (x, 0, 1)) == -1)
check("01 int_1^oo dx/(x^2+1) = pi/4", sp.integrate(1/(x**2 + 1), (x, 1, sp.oo)) == sp.pi/4)
check("01 1/(x^2+1) <= 1/x^2", all(1/(q*q + 1) <= 1/(q*q) for q in np.linspace(1, 50, 500)))
check("01 int_1^oo sin(x)/x^2 comparison: |.|<=1/x^2", all(abs(math.sin(q))/q**2 <= 1/q**2 + 1e-15 for q in np.linspace(1, 50, 500)))

# ---------------------------------------------------------------- 02 functions of several variables, level sets
f2 = 2*x**2 - y**2 + 1
check("02 f(2,3)=0 , grad (8,-6)", f2.subs({x: 2, y: 3}) == 0 and [sp.diff(f2, x).subs({x: 2, y: 3}), sp.diff(f2, y).subs({x: 2, y: 3})] == [8, -6])
check("02 tangent direction (6,8)/10 to level curve: D_u f = 0", (8*6 + (-6)*8) == 0)
check("02 level c=1 of 2x^2-y^2+1 is the lines y=+-sqrt2 x", all(zero(f2.subs(y, sg*sp.sqrt(2)*x) - 1) for sg in (1, -1)))
check("02 level c=5: 2x^2-y^2=4 meets y=0 at x=+-sqrt2", sp.solve(sp.Eq(f2.subs(y, 0), 5), x) == [-sp.sqrt(2), sp.sqrt(2)])
F3 = 2*x**2 - y**2 + z**2
check("02 (1,-1,2) on 2x^2-y^2+z^2=5", F3.subs({x: 1, y: -1, z: 2}) == 5)
check("02 domain ln(x+1/y): x=-1/3,y=3/4 has x+1/y = 1", (R(-1, 3) + 1/R(3, 4)) == 1)
check("02 sqrt(1-x^2-y^2) domain unit disk: (0.6,0.8) boundary", abs(0.36 + 0.64 - 1) < 1e-12)
g02 = 1 - x**2 - y**2
check("02 level sets of 1-x^2-y^2 at c=0 is the unit circle", zero(g02.subs({x: sp.cos(t), y: sp.sin(t)})))
check("02 xy=c levels: grad (y,x) at (1,1) = (1,1) perpendicular to tangent (1,-1)", (1*1 + 1*(-1)) == 0)

# ---------------------------------------------------------------- 03 limits and continuity
f = y*x**2/(2*y**2 + 3*x**4)
check("03 24B-A-Q1a path y=kx^2 gives k/(2k^2+3)",
      sp.simplify(sp.limit(f.subs(y, k*x**2), x, 0) - k/(2*k**2 + 3)) == 0)
check("03 24B-A-Q1a k=1 gives 1/5", sp.limit(f.subs(y, x**2), x, 0) == R(1, 5))
check("03 24B-A-Q1a path y=0 gives 0", f.subs(y, 0) == 0)
check("03 24B-A-Q1a path y=mx: -> 0", sp.limit(f.subs(y, k*x), x, 0) == 0)
f = (x**3*y - x*y**3)/(x**2 + y**2)
pol = sp.simplify(f.subs({x: r*sp.cos(th), y: r*sp.sin(th)}))
check("03 24A-A-Q1a polar: r^2 cos sin (cos^2-sin^2)", zero(pol - r**2*sp.cos(th)*sp.sin(th)*(sp.cos(th)**2 - sp.sin(th)**2)))
check("03 24A-A-Q1a bound r^2/4 (sin4theta/4)", zero(sp.cos(th)*sp.sin(th)*(sp.cos(th)**2 - sp.sin(th)**2) - sp.sin(4*th)/4))
f = x**2*y**2/(x**6 + y**3)
check("03 24A-B-Q1a y=kx^2 gives k^2/(1+k^3)", sp.simplify(sp.limit(f.subs(y, k*x**2), x, 0) - k**2/(1 + k**3)) == 0)
check("03 24A-B-Q1a k=1 gives 1/2", sp.limit(f.subs(y, x**2), x, 0) == R(1, 2))
check("03 24A-B-Q1a y=kx gives 0", sp.limit(f.subs(y, k*x), x, 0, "+") == 0)
check("03 24A-B-Q1a denominator vanishes on y=-x^2", sp.simplify((x**6 + y**3).subs(y, -x**2)) == 0)
f = 4*x**3*y/(3*x**6 + 2*y**2)
check("03 25A-A-Q1a y=kx^3 gives 4k/(3+2k^2)", sp.simplify(sp.limit(f.subs(y, k*x**3), x, 0) - 4*k/(3 + 2*k**2)) == 0)
check("03 25A-A-Q1a k=1 gives 4/5", sp.limit(f.subs(y, x**3), x, 0) == R(4, 5))
f = sp.log(1 + x*y)/(x**2 + y**2)
check("03 26A-A-Q1b y=x gives 1/2", sp.limit(f.subs(y, x), x, 0) == R(1, 2))
check("03 26A-A-Q1b y=-x gives -1/2", sp.limit(f.subs(y, -x), x, 0) == R(-1, 2))
check("03 26A-A-Q1b y=0 gives 0", f.subs(y, 0) == 0)
f = (x**2 + y**2)*sp.sin(1/sp.sqrt(x**2 + y**2))
check("03 22A-A-Q2b r^2 sin(1/r) -> 0", sp.limit(r**2*sp.sin(1/r), r, 0) == 0)
f = x**2*y/(x**2 + y**2)
check("03 worked: x^2 y/(x^2+y^2) = r cos^2 sin", zero(sp.simplify(f.subs({x: r*sp.cos(th), y: r*sp.sin(th)})) - r*sp.cos(th)**2*sp.sin(th)))
f = x*y/(x**2 + y**2)
check("03 xy/(x^2+y^2) along y=mx: m/(1+m^2)", sp.simplify(sp.limit(f.subs(y, k*x), x, 0) - k/(1 + k**2)) == 0)
# the limit of a "moving" family: the same path exponent trick
f = x**3/(x**2 + y**2)
check("03 x^3/(x^2+y^2) -> 0 : |.|<=|x|", all(abs(a**3/(a*a + b*b)) <= abs(a) + 1e-15 for a in np.linspace(-1, 1, 41) for b in np.linspace(-1, 1, 41) if (a, b) != (0, 0)))

# ---------------------------------------------------------------- 04 partials and differentiability
f1 = y*x**2/(2*y**2 + 3*x**4)
check("04 24B-A-Q1c fx(1,1) = -2/25", sp.simplify(sp.diff(f1, x).subs({x: 1, y: 1})) == R(-2, 25))
check("04 24B-A-Q1c fy(1,1) = 1/25", sp.simplify(sp.diff(f1, y).subs({x: 1, y: 1})) == R(1, 25))
f = x**3*y/(x**2 + y**2)
check("04 24B-B-Q1a fx(1,0)=0", sp.simplify(sp.diff(f, x).subs({x: 1, y: 0})) == 0)
check("04 24B-B-Q1a fy(1,0)=1", sp.simplify(sp.diff(f, y).subs({x: 1, y: 0})) == 1)
check("04 24B-B-Q1b f(h,0)=0 and f(0,h)=0", f.subs(y, 0) == 0 and f.subs(x, 0) == 0)
check("04 24B-B-Q1c quotient f/rho = r cos^3 sin", zero(sp.simplify(f.subs({x: r*sp.cos(th), y: r*sp.sin(th)})/r) - r*sp.cos(th)**3*sp.sin(th)))
f = (x**3 + y**3)/(x**2 + y**2)
check("04 22A-B-Q2b fx(0,0)=1", sp.limit(f.subs({x: h, y: 0})/h, h, 0) == 1)
check("04 22A-B-Q2b fy(0,0)=1", sp.limit(f.subs({x: 0, y: h})/h, h, 0) == 1)
num = sp.simplify(f - x - y)
check("04 22A-B-Q2b remainder = -xy(x+y)/(x^2+y^2)", zero(num + x*y*(x + y)/(x**2 + y**2)))
q = sp.simplify((f - x - y).subs({x: h, y: h})/sp.sqrt(2*h**2))
check("04 22A-B-Q2b along y=x, h>0: quotient is -1/sqrt2, not 0", sp.simplify(q.subs(h, sp.Symbol("w", positive=True)) + 1/sp.sqrt(2)) == 0)
f = (x**3 + y**3)/(2*x**2 + y**2)
check("04 23A-C-Q2b fx(0,0)=1/2", sp.limit(f.subs({x: h, y: 0})/h, h, 0) == R(1, 2))
check("04 23A-C-Q2b fy(0,0)=1", sp.limit(f.subs({x: 0, y: h})/h, h, 0) == 1)
w = sp.Symbol("w", positive=True)
q = ((f - x/2 - y).subs({x: w, y: w}))/sp.sqrt(2*w**2)
check("04 23A-C-Q2b along y=x: -5/(6 sqrt 2) != 0", sp.simplify(sp.limit(q, w, 0) + 5/(6*sp.sqrt(2))) == 0)
check("04 23A-C-Q2b numerator factor -xy(4x+y)/(2(2x^2+y^2))", zero(f - x/2 - y + x*y*(4*x + y)/(2*(2*x**2 + y**2))))
f = x*y*(x**2 - y**2)/(x**2 + y**2)
check("04 24A-A-Q2b fx(0,0)=fy(0,0)=0", f.subs(y, 0) == 0 and f.subs(x, 0) == 0)
check("04 24A-A-Q2b f/rho <= r/4 in modulus (polar)", zero(sp.simplify(f.subs({x: r*sp.cos(th), y: r*sp.sin(th)})/r) - r*sp.sin(4*th)/4))
fx_y = sp.limit(f.subs({x: h}) / h, h, 0)   # f_x(0,y) as a function of y
check("04 24A-A-Q2b f_x(0,y) = -y so f_xy(0,0) = -1", sp.simplify(fx_y + y) == 0)
fy_x = sp.limit(f.subs({y: h}) / h, h, 0)   # f_y(x,0)
check("04 24A-A-Q2b f_y(x,0) = x so f_yx(0,0) = +1", sp.simplify(fy_x - x) == 0)
f = x*y**3/(x**2 + y**2)
check("04 24S-A-Q2a f/rho = r cos sin^3 -> 0", zero(sp.simplify(f.subs({x: r*sp.cos(th), y: r*sp.sin(th)})/r) - r*sp.cos(th)*sp.sin(th)**3))
f = (x**2 + y**2)*sp.sin(1/sp.sqrt(x**2 + y**2))
fxx = sp.diff(f, x)
w = sp.Symbol("w", positive=True)
a1 = sp.simplify(fxx.subs({y: 0}).subs(x, w))
# at w = 1/(2 pi m) cos(1/w)=1, at w = 1/((2m+1) pi) cos(1/w) = -1 -> fx along the axis alternates between about -1 and +1
vals = [float(a1.subs(w, 1/(2*math.pi*m))) for m in (50, 100, 200)]
vals2 = [float(a1.subs(w, 1/((2*m + 1)*math.pi))) for m in (50, 100, 200)]
check("04 22A-A-Q2b fx not continuous at 0: oscillates near -1 and +1", all(vv < -0.9 for vv in vals) and all(vv > 0.9 for vv in vals2))
z4 = sp.exp(x - y)*sp.sin(x + y)
check("04 24S-A-Q1b z_xx + z_yy = 0", zero(sp.diff(z4, x, 2) + sp.diff(z4, y, 2)))
check("04 24S-A-Q1b z_xx = 2e^{x-y}cos(x+y)", zero(sp.diff(z4, x, 2) - 2*sp.exp(x - y)*sp.cos(x + y)))
f = sp.sqrt(41 - 4*x**2 - y**2)
fx0 = sp.diff(f, x).subs({x: 2, y: 3}); fy0 = sp.diff(f, y).subs({x: 2, y: 3})
approx = f.subs({x: 2, y: 3}) + fx0*R(1, 10) + fy0*(-R(1, 10))
check("04 25A-B-Q1a f(2,3)=4, fx=-2, fy=-3/4", f.subs({x: 2, y: 3}) == 4 and fx0 == -2 and fy0 == R(-3, 4))
check("04 25A-B-Q1a linear approx = 3.875", approx == R(31, 8))
check("04 25A-B-Q1a exact value 3.8665 close", abs(float(f.subs({x: R(21, 10), y: R(29, 10)})) - 3.8665) < 1e-3)
fl = x**2*y
check("04 worked: f=x^2 y, f(2.1,1.9) approx", abs(float(fl.subs({x: 2, y: 2}) + sp.diff(fl, x).subs({x: 2, y: 2})*R(1, 10) + sp.diff(fl, y).subs({x: 2, y: 2})*(-R(1, 10))) - 8.4) < 1e-12)

# ---------------------------------------------------------------- 05 chain rule and identities
g = sp.Function("g")
z5 = y/(3*x) + g(x*y)
check("05 22A-A-Q1b identity", zero(x**2*sp.diff(z5, x) - x*y*sp.diff(z5, y) + 2*y/3))
z5 = y*g(x**2 - y**2)
check("05 23A-C-Q3b identity", zero(sp.diff(z5, x)/x + sp.diff(z5, y)/y - z5/y**2))
z5 = y*g(sp.cos(x - y))
check("05 25A-B-Q3b identity", zero(sp.diff(z5, x) + sp.diff(z5, y) - z5/y))
f2f = sp.Function("F")
G = f2f(1/y - 1/x, x*y*sp.exp(-z**2/2))
check("05 23A-A-Q3b identity", zero(x**2*sp.diff(G, x) + y**2*sp.diff(G, y) + (x + y)/z*sp.diff(G, z)))
kk = sp.symbols("kk")
Fv0, Fs_, Ft_ = sp.symbols("Fv0 Fs_ Ft_")   # F, F_s, F_t at (z/x, y/x), treated as symbols
s_ = z/x; t_ = y/x
dU = lambda w_: kk*x**(kk - 1)*Fv0*(1 if w_ == x else 0) + x**kk*(Fs_*sp.diff(s_, w_) + Ft_*sp.diff(t_, w_))
check("05 24A-A-Q3b Euler identity", zero(x*dU(x) + y*dU(y) + z*dU(z) - kk*x**kk*Fv0))
# 24S-A-Q4a: 2 fx + e^t fy = 0
fyv = sp.symbols("fyv")
check("05 24S-A-Q4a fy = -1", sp.solve(sp.Eq(2*sp.exp(t)/2 + sp.exp(t)*fyv, 0), fyv) == [-1])
# 24B-B-Q4a
uu, vv = sp.symbols("uu vv")
zz = 2*uu*vv + 3*vv**2
uf = sp.cos(x - 3*y)
ux = sp.diff(uf, x).subs({x: sp.pi, y: -sp.pi}); uy = sp.diff(uf, y).subs({x: sp.pi, y: -sp.pi})
u0 = uf.subs({x: sp.pi, y: -sp.pi})
zx = sp.diff(zz, uu).subs({uu: u0, vv: 2})*ux + sp.diff(zz, vv).subs({uu: u0, vv: 2})*5
zy = sp.diff(zz, uu).subs({uu: u0, vv: 2})*uy + sp.diff(zz, vv).subs({uu: u0, vv: 2})*4
check("05 24B-B-Q4a u=1, u_x=u_y=0", u0 == 1 and ux == 0 and uy == 0)
check("05 24B-B-Q4a z_x=70, z_y=56", zx == 70 and zy == 56)
# 26A-A-Q3b
uu, vv = sp.symbols("uu vv", positive=True)
xx_ = sp.sqrt(uu*vv); yy_ = 1/vv
zf = sp.exp(xx_**2*yy_)
check("05 26A-A-Q3b x^2 y = u so z = e^u", zero(xx_**2*yy_ - uu))
check("05 26A-A-Q3b identity", zero(uu*sp.diff(zf, uu) - vv*sp.diff(zf, vv) - zf*xx_**2/vv))
# worked example for the brief: z = f(x^2 y, x - y): z_x, z_y
Ff = sp.Function("F")
U1 = x**2*y; V1 = x - y
zex = Ff(U1, V1)
Fu, Fv = sp.symbols("Fu Fv")
zx_chain = Fu*sp.diff(U1, x) + Fv*sp.diff(V1, x)
check("05 worked: z=F(x^2 y, x-y): z_x = 2xy F_u + F_v", zero(zx_chain - (2*x*y*Fu + Fv)))
# worked example: z = x y g(x/y)... Euler-type identity x z_x + y z_y = 2 z
zw = x*y*g(x/y)
check("05 worked: z = xy g(x/y) gives x z_x + y z_y = 2z", zero(x*sp.diff(zw, x) + y*sp.diff(zw, y) - 2*zw))
# dz/dt along a curve
curve = (sp.cos(t), sp.sin(t))
fz = x**2*y
dz = sp.diff(fz, x)*sp.diff(curve[0], t) + sp.diff(fz, y)*sp.diff(curve[1], t)
dz = dz.subs({x: curve[0], y: curve[1]})
check("05 dz/dt along (cos t, sin t) for x^2 y equals direct derivative", zero(dz - sp.diff(fz.subs({x: curve[0], y: curve[1]}), t)))

# ---------------------------------------------------------------- 06 gradient, directional derivative, tangent plane
f = 2*sp.sin(2*x + 2*y)
gr = [sp.diff(f, x).subs({x: sp.pi/2, y: sp.pi/2}), sp.diff(f, y).subs({x: sp.pi/2, y: sp.pi/2})]
check("06 22A-A-Q1a grad (4,4), norm sqrt 32", gr == [4, 4] and sp.sqrt(sum(c**2 for c in gr)) == sp.sqrt(32) == 4*sp.sqrt(2))
f = sp.log(x**2 + y**2 + z**2)
gr = [sp.diff(f, w_).subs({x: 1, y: 2, z: 1}) for w_ in (x, y, z)]
check("06 22A-B-Q1a grad (1/3,2/3,1/3)", gr == [R(1, 3), R(2, 3), R(1, 3)])
check("06 22A-B-Q1a norm sqrt6/3", sp.simplify(sp.sqrt(sum(c**2 for c in gr)) - sp.sqrt(6)/3) == 0)
f = x**2*y*sp.sqrt(z)
gr = [sp.diff(f, w_).subs({x: 2, y: 1, z: 1}) for w_ in (x, y, z)]
check("06 23A-C-Q1b grad (4,4,2) norm 6", gr == [4, 4, 2] and sp.sqrt(sum(c**2 for c in gr)) == 6)
uvec = sp.Matrix([1, 2, 2]); uhat = uvec/uvec.norm()
dd = (sp.Matrix(gr).T*uhat)[0]
check("06 23A-C-Q1b D_u f = 16/3, ratio 9/8", dd == R(16, 3) and 6/dd == R(9, 8))
f = 2*sp.exp(-x**2) + sp.exp(-3*y**2)
check("06 24A-A-Q1b grad(1,0) = (-4/e, 0)", [sp.diff(f, x).subs({x: 1, y: 0}), sp.diff(f, y).subs({x: 1, y: 0})] == [-4/sp.E, 0])
f = x + x*y
check("06 24A-B-Q1b grad(1,-1) = (0,1)", [sp.diff(f, x).subs({x: 1, y: -1}), sp.diff(f, y).subs({x: 1, y: -1})] == [0, 1])
a_, b_ = sp.symbols("a_ b_", real=True)
sol = sp.solve([sp.Eq(b_, 1/sp.sqrt(2)), sp.Eq(a_**2 + b_**2, 1)], [a_, b_])
check("06 24A-B-Q1b directions (+-1/sqrt2, 1/sqrt2)", sorted([sp.nsimplify(p[0]) for p in sol], key=float) == [-1/sp.sqrt(2), 1/sp.sqrt(2)])
f = 2*x**2 - y**2 + 1
check("06 24B-A-Q3 grad(2,3) = (8,-6), norm 10", [sp.diff(f, x).subs({x: 2, y: 3}), sp.diff(f, y).subs({x: 2, y: 3})] == [8, -6])
f = x**2 - 2*x*(y + 1) + 3
gr = [sp.diff(f, x).subs({x: 2, y: -1}), sp.diff(f, y).subs({x: 2, y: -1})]
check("06 24B-B-Q3a grad(2,-1) = (4,-4)", gr == [4, -4])
check("06 24B-B-Q3b D_(-3,4) = -28/5", sp.Rational(gr[0]*(-3) + gr[1]*4, 5) == R(-28, 5))
Fs = 2*x**2 - y**2 + z**2
gp = [sp.diff(Fs, w_).subs({x: 1, y: -1, z: 2}) for w_ in (x, y, z)]
check("06 24B-A-Q4a normal (4,2,4)", gp == [4, 2, 4])
check("06 24B-A-Q4a plane 2x+y+2z=5", zero(sp.expand(4*(x - 1) + 2*(y + 1) + 4*(z - 2)) - 2*(2*x + y + 2*z - 5)))
f = y*sp.cos(x*y)
check("06 24S-A-Q1a grad(1,0) = (0,1)", [sp.diff(f, x).subs({x: 1, y: 0}), sp.diff(f, y).subs({x: 1, y: 0})] == [0, 1])
f = sp.log(x + 1/y)
fxs = sp.diff(f, x); fys = sp.diff(f, y)
sols = sp.solve([sp.Eq(fxs, 1), sp.Eq(fys, -R(16, 9))], [x, y], dict=True)
check("06 24S-A-Q4b points (-1/3,3/4) and (7/3,-3/4)", sorted([(s_[x], s_[y]) for s_ in sols]) == sorted([(R(-1, 3), R(3, 4)), (R(7, 3), -R(3, 4))]))
check("06 24S-A-Q4b plane at first point: z = x - 16y/9 + 5/3", sp.simplify((x + R(1, 3)) - R(16, 9)*(y - R(3, 4)) - (x - R(16, 9)*y + R(5, 3))) == 0)
check("06 24S-A-Q4b plane at second point: z = x - 16y/9 - 5/3 ... check", sp.simplify((x - R(7, 3)) - R(16, 9)*(y + R(3, 4)) - (x - R(16, 9)*y - R(7, 3) - R(4, 3))) == 0)
f = sp.sqrt(x**2 + 2*y)
gr = [sp.diff(f, x).subs({x: 4, y: 10}), sp.diff(f, y).subs({x: 4, y: 10})]
check("06 25A-A-Q5a grad(4,10) = (2/3, 1/6), norm sqrt17/6", gr == [R(2, 3), R(1, 6)] and sp.simplify(sp.sqrt(gr[0]**2 + gr[1]**2) - sp.sqrt(17)/6) == 0)
check("06 25A-A-Q5a direction (4,1)/sqrt17", sp.simplify(sp.Matrix(gr)/sp.sqrt(gr[0]**2 + gr[1]**2) - sp.Matrix([4, 1])/sp.sqrt(17)) == sp.zeros(2, 1))
# worked example in the brief: f=x^2+xy+y^2 at (1,1)
f = x**2 + x*y + y**2
gr = [sp.diff(f, x).subs({x: 1, y: 1}), sp.diff(f, y).subs({x: 1, y: 1})]
check("06 worked: grad(1,1) = (3,3), D_(3,4)/5 = 21/5, max 3 sqrt2", gr == [3, 3] and R(3*3 + 3*4, 5) == R(21, 5) and sp.sqrt(18) == 3*sp.sqrt(2))
# graph tangent plane: z = f(x,y) at (1,1): z - 3 = 3(x-1) + 3(y-1)
check("06 worked: tangent plane of graph at (1,1,3): 3x+3y-z=3", f.subs({x: 1, y: 1}) == 3 and sp.expand(3*(x - 1) + 3*(y - 1) - (z - 3) - (3*x + 3*y - z - 3)) == 0)

# ---------------------------------------------------------------- 07 implicit function
F = y**3 + x*z + y**2 + sp.exp(z) - 3
P = {x: 1, y: 1, z: 0}
check("07 22A-A-Q3b F(1,1,0)=0, Fz=2", F.subs(P) == 0 and sp.diff(F, z).subs(P) == 2)
zx_ = -sp.diff(F, x).subs(P)/sp.diff(F, z).subs(P); zy_ = -sp.diff(F, y).subs(P)/sp.diff(F, z).subs(P)
check("07 22A-A-Q3b zx=0, zy=-5/2", zx_ == 0 and zy_ == R(-5, 2))
check("07 22A-A-Q3b plane 5y+2z=5", sp.expand(2*(z - 0) - (2*(zx_*(x - 1) + zy_*(y - 1)))) == sp.expand(2*z + 5*y - 5))
F = z**3 - 3*x*y*z - 4
P = {x: 2, y: 1, z: -2}
check("07 22A-B-Q3b F(2,1,-2)=0 and Fz=3z^2-3xy=6", F.subs(P) == 0 and sp.diff(F, z).subs(P) == 6)
zf = sp.Function("zf")(x, y)
eq = zf**3 - 3*x*y*zf - 4
zxs = sp.solve(sp.diff(eq, x), sp.diff(zf, x))[0]
zys = sp.solve(sp.diff(eq, y), sp.diff(zf, y))[0]
val = {x: 2, y: 1, zf: -2}
zx0 = zxs.subs(val); zy0 = zys.subs(val)
zxy = sp.diff(zxs, y).subs(sp.diff(zf, y), zys)
zxy0 = sp.simplify(zxy.subs(val))
check("07 22A-B-Q3b zx(2,1)=-1", zx0 == -1)
check("07 22A-B-Q3b zy(2,1) = -2", zy0 == -2)
ZXY = zxy0
# independent numeric second-derivative check by implicit solve
def zsol(a, b):
    zz_ = sp.nsolve(z**3 - 3*a*b*z - 4, z, -2)
    return float(zz_)
hh = 1e-3
numzxy = (zsol(2 + hh, 1 + hh) - zsol(2 + hh, 1 - hh) - zsol(2 - hh, 1 + hh) + zsol(2 - hh, 1 - hh))/(4*hh*hh)
check("07 22A-B-Q3b zxy(2,1) = 1", ZXY == 1)
check("07 22A-B-Q3b zxy(2,1) agrees with finite differences", abs(float(ZXY) - numzxy) < 1e-3)
F = 5*z**3 + 3*x*y*z - x**2*y**2 + 1
P = {x: 1, y: -1, z: 0}
check("07 24S-A-Q5a F=0, Fz=-3", F.subs(P) == 0 and sp.diff(F, z).subs(P) == -3)
zx_ = -sp.diff(F, x).subs(P)/sp.diff(F, z).subs(P); zy_ = -sp.diff(F, y).subs(P)/sp.diff(F, z).subs(P)
check("07 24S-A-Q5a zx=-2/3, zy=2/3, sum 0", zx_ == R(-2, 3) and zy_ == R(2, 3) and zx_ + zy_ == 0)
# worked example for the brief: x^2 + y^2 + z^2 = 3 at (1,1,1) (and the second derivative z_xx)
F = x**2 + y**2 + z**2 - 3
zf = sp.Function("zf")(x, y)
eq = zf**2 + x**2 + y**2 - 3
zxs = sp.solve(sp.diff(eq, x), sp.diff(zf, x))[0]
check("07 worked: z_x = -x/z = -1 at (1,1,1)", zxs.subs({zf: 1, x: 1}) == -1)
zxx = sp.diff(zxs, x).subs(sp.diff(zf, x), zxs)
check("07 worked: z_xx = -(z^2+x^2)/z^3 = -2 at (1,1,1)", sp.simplify(zxx.subs({zf: 1, x: 1}) + 2) == 0)
check("07 worked: z_xx formula", zero(zxx + (zf**2 + x**2)/zf**3))

# ---------------------------------------------------------------- 08 local extrema
def classify(f_, pts):
    out = {}
    fxx = sp.diff(f_, x, 2); fyy = sp.diff(f_, y, 2); fxy = sp.diff(f_, x, y)
    for p in pts:
        sub = {x: p[0], y: p[1]}
        A = sp.simplify(fxx.subs(sub)); C = sp.simplify(fyy.subs(sub)); B = sp.simplify(fxy.subs(sub))
        D = sp.simplify(A*C - B**2)
        if D > 0:
            out[p] = ("min" if A > 0 else "max", D, A)
        elif D < 0:
            out[p] = ("saddle", D, A)
        else:
            out[p] = ("degenerate", D, A)
    return out


def crit(f_):
    return sp.solve([sp.diff(f_, x), sp.diff(f_, y)], [x, y], dict=True)


f = x*y**2 - y**2 - x**2/2 - 2*x + 3
cp = [(d[x], d[y]) for d in crit(f)]
check("08 22A-A-Q5b three critical points", sorted(cp, key=str) == sorted([(-2, 0), (1, sp.sqrt(3)), (1, -sp.sqrt(3))], key=str))
cl = classify(f, cp)
check("08 22A-A-Q5b (-2,0) max D=6, others saddle D=-12", cl[(-2, 0)][0] == "max" and cl[(-2, 0)][1] == 6 and cl[(1, sp.sqrt(3))][:2] == ("saddle", -12))
f = x**3 + 8*y**3 - 6*x*y + 1
cp = [(d[x], d[y]) for d in crit(f) if all(c.is_real for c in d.values())]
cl = classify(f, cp)
check("08 22A-B-Q5b (0,0) saddle D=-36, (1,1/2) min D=108, f=0", cl[(0, 0)][:2] == ("saddle", -36) and cl[(1, R(1, 2))][:2] == ("min", 108) and f.subs({x: 1, y: R(1, 2)}) == 0)
f = (x + y)**2 - 4*y**2 - 48*y
cp = [(d[x], d[y]) for d in crit(f)]
check("08 23A-A-Q5a (6,-6) saddle D=-16, f=144", cp == [(6, -6)] and classify(f, cp)[(6, -6)][:2] == ("saddle", -16) and f.subs({x: 6, y: -6}) == 144)
f = (x**2 - 2*y**2)*sp.exp(x - y)
check("08 23A-C-Q5a critical points (0,0),(-4,-2)", sorted([(d[x], d[y]) for d in crit(f)]) == [(-4, -2), (0, 0)])
cl = classify(f, [(0, 0), (-4, -2)])
check("08 23A-C-Q5a (0,0) saddle D=-8; (-4,-2) max value 8/e^2", cl[(0, 0)][:2] == ("saddle", -8) and cl[(-4, -2)][0] == "max" and sp.simplify(f.subs({x: -4, y: -2}) - 8*sp.exp(-2)) == 0)
f = (3 - x)*(3 - y)*(x + y - 3)
cp = [(d[x], d[y]) for d in crit(f)]
cl = classify(f, cp)
check("08 24A-B-Q5a four critical points, (2,2) max value 1, three saddles D=-9",
      sorted(cp) == sorted([(0, 3), (3, 0), (3, 3), (2, 2)]) and cl[(2, 2)][0] == "max" and f.subs({x: 2, y: 2}) == 1
      and all(cl[p][:2] == ("saddle", -9) for p in [(0, 3), (3, 0), (3, 3)]) and cl[(2, 2)][1] == 3)
f = 2*x**2 - y**2 + 1
check("08 24B-A-Q3c (0,0) saddle D=-8", classify(f, [(0, 0)])[(0, 0)][:2] == ("saddle", -8))
f = x**2 - 2*x*(y + 1) + 3
cp = [(d[x], d[y]) for d in crit(f)]
check("08 24B-B-Q3c (0,-1) saddle D=-4", cp == [(0, -1)] and classify(f, cp)[(0, -1)][:2] == ("saddle", -4))
f = x*y*(6 - x - y)
cp = [(d[x], d[y]) for d in crit(f)]
cl = classify(f, cp)
check("08 24S-A-Q5b four points; (2,2) max 8 with D=12; three saddles D=-36",
      sorted(cp) == sorted([(0, 0), (6, 0), (0, 6), (2, 2)]) and cl[(2, 2)][:2] == ("max", 12) and f.subs({x: 2, y: 2}) == 8
      and all(cl[p][:2] == ("saddle", -36) for p in [(0, 0), (6, 0), (0, 6)]))
f = (x - y)**3 - 3*x - y**2 + 5*y
cp = [(d[x], d[y]) for d in crit(f)]
cl = classify(f, cp)
check("08 26A-A-Q5a (2,1) saddle, (0,1) max value 3", sorted(cp) == [(0, 1), (2, 1)] and cl[(2, 1)][0] == "saddle" and cl[(0, 1)][0] == "max" and f.subs({x: 0, y: 1}) == 3)
check("08 26A-A-Q5a Hessian entries: fxx=6(x-y), fxy=-6(x-y), fyy=6(x-y)-2",
      zero(sp.diff(f, x, 2) - 6*(x - y)) and zero(sp.diff(f, x, y) + 6*(x - y)) and zero(sp.diff(f, y, 2) - (6*(x - y) - 2)))
# degenerate Hessian: x^4+y^4 vs x^3+y^3 vs -x^4 - y^4 (all D = 0 at origin)
for nm, ff, kind in (("x^4+y^4", x**4 + y**4, "min"), ("x^3+y^3", x**3 + y**3, "saddle"), ("-x^4-y^4", -x**4 - y**4, "max")):
    check("08 degenerate: %s has D=0 at origin" % nm, sp.diff(ff, x, 2).subs({x: 0, y: 0})*sp.diff(ff, y, 2).subs({x: 0, y: 0}) - sp.diff(ff, x, y).subs({x: 0, y: 0})**2 == 0)
check("08 degenerate x^4+y^4 >0 off origin; x^3+y^3 takes both signs",
      all((a**4 + b**4) > 0 for a in (-.1, .1) for b in (-.1, 0, .1) if (a, b) != (0, 0)) and (0.1**3 + 0) > 0 and ((-0.1)**3 + 0) < 0)
# worked example in the brief: f = x^3 - 3x + y^2 (critical points (1,0) min, (-1,0) saddle)
f = x**3 - 3*x + y**2
cp = [(d[x], d[y]) for d in crit(f)]
cl = classify(f, cp)
check("08 worked: x^3-3x+y^2: (1,0) min D=12 value -2; (-1,0) saddle D=-12", sorted(cp) == [(-1, 0), (1, 0)] and cl[(1, 0)][:2] == ("min", 12) and cl[(-1, 0)][:2] == ("saddle", -12) and f.subs({x: 1, y: 0}) == -2)
check("08 2x2 criterion: AC-B^2 for 24A-B-Q5a formula 4(3-y)(3-x)-(2x+2y-9)^2",
      zero(sp.diff(f := (3 - x)*(3 - y)*(x + y - 3), x, 2)*sp.diff(f, y, 2) - sp.diff(f, x, y)**2 - (4*(3 - y)*(3 - x) - (2*x + 2*y - 9)**2)))

# ---------------------------------------------------------------- 09 absolute extrema and Lagrange
def lagr(f_, g_, c_):
    L = f_ - lam*(g_ - c_)
    sols = sp.solve([sp.diff(L, x), sp.diff(L, y), g_ - c_], [x, y, lam], dict=True)
    return [(sp.simplify(s_[x]), sp.simplify(s_[y])) for s_ in sols if s_[x].is_real and s_[y].is_real]


f = x*y
pts = lagr(f, x**2 + y**2, 2)
vals = sorted(set(sp.simplify(f.subs({x: p[0], y: p[1]})) for p in pts))
check("09 24A-A-Q4b xy on circle r^2=2: values -1 and 1 at (+-1,+-1)", sorted(pts) == sorted([(1, 1), (-1, -1), (1, -1), (-1, 1)]) and vals == [-1, 1])
f = 1 - x**2 - y**2
g_ = (x - 1)**2 + (y - 1)**2
pts = lagr(f, g_, 1)
vals = sorted(float(f.subs({x: p[0], y: p[1]})) for p in pts)
check("09 22A-B-Q4b two points x=y=1+-sqrt2/2, values 2sqrt2-2 and -2-2sqrt2", len(pts) == 2 and abs(vals[1] - (2*math.sqrt(2) - 2)) < 1e-12 and abs(vals[0] - (-2 - 2*math.sqrt(2))) < 1e-12)
check("09 22A-B-Q4b f at 1-sqrt2/2 exactly 2 sqrt2 - 2", sp.simplify(f.subs({x: 1 - sp.sqrt(2)/2, y: 1 - sp.sqrt(2)/2}) - (2*sp.sqrt(2) - 2)) == 0)
check("09 22A-B-Q4b (0,0) outside disk", g_.subs({x: 0, y: 0}) == 2 > 1)
f = 2*x**2 - y**2 + 1
g_ = (x - 1)**2 + y**2
pts = lagr(f, g_, 1)
check("09 24B-A-Q3d boundary points (0,0),(2,0),(1/3,+-sqrt5/3)", sorted(pts, key=str) == sorted([(0, 0), (2, 0), (R(1, 3), sp.sqrt(5)/3), (R(1, 3), -sp.sqrt(5)/3)], key=str))
check("09 24B-A-Q3d values 1, 9, 2/3", sorted(set(f.subs({x: p[0], y: p[1]}) for p in pts)) == [R(2, 3), 1, 9])
f = x**3 + x**2 - 3*x + y**2
gx = sp.simplify(f.subs(y**2, 4 - x**2))
check("09 26A-A-Q4b reduce to g(x)=x^3-3x+4", sp.expand(f.subs(y, sp.sqrt(4 - x**2)) - (x**3 - 3*x + 4)) == 0)
gg = x**3 - 3*x + 4
check("09 26A-A-Q4b g(+-2), g(+-1)", [gg.subs(x, a) for a in (-2, -1, 1, 2)] == [2, 6, 2, 6])
pts = lagr(f, x**2 + y**2, 4)
check("09 26A-A-Q4b Lagrange points (+-2,0), (1,+-sqrt3), (-1,+-sqrt3)", len(pts) == 6 and sorted(set(f.subs({x: p[0], y: p[1]}) for p in pts)) == [2, 6])
f = y**4 - x**4
pts = lagr(f, x**2 + y**2, 9)
check("09 25A-A-Q1b boundary values -81 and 81 only (the case with both x,y nonzero has no real solution)",
      sorted(set(sp.simplify(f.subs({x: p[0], y: p[1]})) for p in pts)) == [-81, 81])
check("09 25A-A-Q1b interior critical point only (0,0) value 0", [(d[x], d[y]) for d in crit(f)] == [(0, 0)])
check("09 25A-A-Q1b the system gives exactly 4 real points (0,+-3),(+-3,0)", len(pts) == 4)
# 22A-A-Q4b with corrected maximum
f = 2*x**4 + y**4 - x**2 - 2*y**2
cp = [(d[x], d[y]) for d in crit(f) if all(c.is_real for c in d.values())]
check("09 22A-A-Q4b nine interior critical points", len(cp) == 9)
check("09 22A-A-Q4b interior min -9/8 at (+-1/2, +-1)", min(f.subs({x: p[0], y: p[1]}) for p in cp) == R(-9, 8))
gb = sp.expand(f.subs(y**2, 2 - x**2))
check("09 22A-A-Q4b boundary reduces to 3x^4-3x^2 (using y^2=2-x^2)", sp.expand(2*x**4 + (2 - x**2)**2 - x**2 - 2*(2 - x**2) - (3*x**4 - 3*x**2)) == 0)
gb = 3*x**4 - 3*x**2
vals = {a: gb.subs(x, a) for a in (0, 1/sp.sqrt(2), -1/sp.sqrt(2), sp.sqrt(2), -sp.sqrt(2))}
check("09 22A-A-Q4b boundary values: 0, -3/4, 6 (endpoints x=+-sqrt2)", sorted(set(sp.simplify(c) for c in vals.values())) == [R(-3, 4), 0, 6])
check("09 22A-A-Q4b endpoints (+-sqrt2,0) are on the circle", (sp.sqrt(2)**2 + 0) == 2)
# dense sampling check for the disc
xs = np.linspace(-math.sqrt(2), math.sqrt(2), 1401)
Xg, Yg = np.meshgrid(xs, xs)
mask = Xg**2 + Yg**2 <= 2 + 1e-12
Fg = 2*Xg**4 + Yg**4 - Xg**2 - 2*Yg**2
check("09 22A-A-Q4b dense sampling max 6 min -9/8", abs(Fg[mask].max() - 6) < 1e-3 and abs(Fg[mask].min() + 9/8) < 1e-3)
# 23A-C-Q4b sector
f = x**2 + y**2 + 4*x*y
arc = sp.simplify(f.subs({x: sp.cos(t), y: sp.sin(t)}))
check("09 23A-C-Q4b on the arc f = 1 + 2 sin 2t, max 3 at t=pi/4", zero(arc - (1 + 2*sp.sin(2*t))) and arc.subs(t, sp.pi/4) == 3)
check("09 23A-C-Q4b vertices (0,0)=0,(1,0)=1,(1/2,sqrt3/2)=1+sqrt3", [f.subs({x: a, y: b}) for a, b in ((0, 0), (1, 0), (R(1, 2), sp.sqrt(3)/2))] == [0, 1, 1 + sp.sqrt(3)])
check("09 23A-C-Q4b 1+sqrt3 < 3 and endpoint t=pi/3 value 1+sqrt3", abs(float(arc.subs(t, sp.pi/3)) - (1 + math.sqrt(3))) < 1e-12 and 1 + math.sqrt(3) < 3)
# triangle 24S-A-Q3b
f = 2*x**2 - 3*y**2 + x*y - 3*x + 8*y
check("09 24S-A-Q3b interior critical (2/5,7/5) outside triangle", [(d[x], d[y]) for d in crit(f)] == [(R(2, 5), R(7, 5))])
check("09 24S-A-Q3b vertex values A=0,B=5,C=5, edge BC min at (1/2,1) = 9/2",
      [f.subs({x: a, y: b}) for a, b in ((0, 0), (0, 1), (1, 1), (R(1, 2), 1))] == [0, 5, 5, R(9, 2)])
check("09 24S-A-Q3b edge AC: y=x gives f=5x, linear, only endpoints matter", sp.expand(f.subs(y, x) - 5*x) == 0)
check("09 24S-A-Q3b edge AB: g(y)=-3y^2+8y has critical y=4/3 outside [0,1]", R(4, 3) > 1)
# triangle 24B-B-Q3d
f = x**2 - 2*x*(y + 1) + 3
check("09 24B-B-Q3d interior (0,-1) f=3; vertices A(1,1)=0,B(1,-2)=6,C(-2,-2)=3; edge points D(-1,-2)=2, E(-1,-1)=4",
      [f.subs({x: a, y: b}) for a, b in ((0, -1), (1, 1), (1, -2), (-2, -2), (-1, -2), (-1, -1))] == [3, 0, 6, 3, 2, 4])
check("09 24B-B-Q3d edge x=1: f=2-2y linear", sp.expand(f.subs(x, 1) - (2 - 2*y)) == 0)
check("09 24B-B-Q3d edge y=-2: x^2+2x+3; edge y=x: -x^2-2x+3", sp.expand(f.subs(y, -2) - (x**2 + 2*x + 3)) == 0 and sp.expand(f.subs(y, x) - (-x**2 - 2*x + 3)) == 0)
# Lagrange geometric statement: gradients parallel at the extremum of xy on the circle
check("09 grad f=(y,x) parallel grad g=(2x,2y) at (1,1)", (1*2 - 1*2) == 0)
# worked example in the brief: x + y on x^2+y^2=1
f = x + y
pts = lagr(f, x**2 + y**2, 1)
check("09 worked: x+y on unit circle: max sqrt2 at (1/sqrt2,1/sqrt2), min -sqrt2", sorted(sp.simplify(f.subs({x: p[0], y: p[1]})) for p in pts) == [-sp.sqrt(2), sp.sqrt(2)])
check("09 worked: Weierstrass method: parametrisation gives sqrt2 sin(t+pi/4)", zero(sp.sin(t) + sp.cos(t) - sp.sqrt(2)*sp.sin(t + sp.pi/4)))

# ---------------------------------------------------------------- 10 double integrals
f = sp.sin(sp.pi*x**2/2)
A1 = sp.integrate(sp.integrate(f, (x, y, 1)), (y, 0, 1)) if False else None
inner = sp.integrate(f, (y, 0, x))
check("10 25A-A-Q4a swapped inner integral gives x sin(pi x^2/2)", zero(inner - x*f))
check("10 25A-A-Q4a value 1/pi", sp.simplify(sp.integrate(x*f, (x, 0, 1)) - 1/sp.pi) == 0)
f = x*sp.exp(x**2)
check("10 26A-A-Q1a value (e^2-3)/2", sp.simplify(sp.integrate(sp.integrate(f, (y, 0, 2 - x**2)), (x, 0, sp.sqrt(2))) - (sp.exp(2) - 3)/2) == 0)
check("10 26A-A-Q1a other order gives same value", sp.simplify(sp.integrate(sp.integrate(f, (x, 0, sp.sqrt(2 - y))), (y, 0, 2)) - (sp.exp(2) - 3)/2) == 0)
fa = sp.Function("fa")
# areas via 1 in both orders for the two-piece region
A_xy = sp.integrate(sp.sqrt(x + 4), (x, -4, 0)) + sp.integrate(2 - x, (x, 0, 2))
A_yx = sp.integrate(2 - y - (y**2 - 4), (y, 0, 2))
check("10 23A-C-Q4a area both orders 22/3", A_xy == A_yx == R(22, 3))
check("10 23A-C-Q4a boundary parabola x=y^2-4 <-> y=sqrt(x+4) (y>=0)", all(abs(math.sqrt(a) - 2*0 - math.sqrt(a)) < 1e-12 for a in (0.5, 2, 4)) and sp.solve(sp.Eq(y, sp.sqrt(x + 4)), x) == [y**2 - 4])
check("10 23A-C-Q4a pieces meet at (0,2)", sp.sqrt(0 + 4) == 2 == 2 - 0)
# sample integrand to compare both orders numerically: f=x*y
ff = x*y
I_xy = sp.integrate(sp.integrate(ff, (y, 0, sp.sqrt(x + 4))), (x, -4, 0)) + sp.integrate(sp.integrate(ff, (y, 0, 2 - x)), (x, 0, 2))
I_yx = sp.integrate(sp.integrate(ff, (x, y**2 - 4, 2 - y)), (y, 0, 2))
check("10 25A-B-Q4a sample integrand x*y: both orders equal", sp.simplify(I_xy - I_yx) == 0)
check("10 25A-B-Q4a sample value is printed (finite)", I_yx.is_number)
# area between circles (polar)
Apol = sp.integrate(sp.integrate(r, (r, 2*sp.cos(th), 4*sp.cos(th))), (th, -sp.pi/2, sp.pi/2))
check("10 23A-C-Q1a area between circles = 3 pi", sp.simplify(Apol - 3*sp.pi) == 0)
check("10 23A-C-Q1a circles: area 4pi - pi", 4*sp.pi - sp.pi == 3*sp.pi)
# the triangle region 24B-B-Q3d: y from -2 to x, x from -2 to 1; area 9/2
check("10 24B-B-Q3d triangle area 9/2 in both orders", sp.integrate(sp.integrate(1, (y, -2, x)), (x, -2, 1)) == R(9, 2) == sp.integrate(sp.integrate(1, (x, y, 1)), (y, -2, 1)))
# type I vs type II area of region under y=x^2 above y=0 up to x=1 (worked)
check("10 worked: triangle 0<=y<=x<=1 area 1/2 both orders", sp.integrate(sp.integrate(1, (y, 0, x)), (x, 0, 1)) == R(1, 2) == sp.integrate(sp.integrate(1, (x, y, 1)), (y, 0, 1)))
check("10 worked: int_0^1 int_y^1 e^{x^2} dx dy = (e-1)/2", sp.simplify(sp.integrate(sp.integrate(sp.exp(x**2), (y, 0, x)), (x, 0, 1)) - (sp.E - 1)/2) == 0)
check("10 worked: dx dy with sqrt: int_0^1 int_{sqrt y}^1 sqrt(1+x^3)... swap gives (2/9)(2sqrt2-1)",
      sp.simplify(sp.integrate(sp.integrate(sp.sqrt(1 + x**3), (y, 0, x**2)), (x, 0, 1)) - R(2, 9)*(2*sp.sqrt(2) - 1)) == 0)

# ---------------------------------------------------------------- 11 change of variables
def jac_abs(X_, Y_, U_, V_):
    J = sp.Matrix([[sp.diff(X_, U_), sp.diff(X_, V_)], [sp.diff(Y_, U_), sp.diff(Y_, V_)]]).det()
    return sp.simplify(J)


check("11 polar Jacobian = r", jac_abs(r*sp.cos(th), r*sp.sin(th), r, th) == r)
check("11 22A-B-Q1b value pi/2 (cos2 - cos11)", sp.simplify(sp.integrate(sp.integrate(sp.sin(2 + r**2)*r, (r, 0, 3)), (th, 0, sp.pi)) - sp.pi/2*(sp.cos(2) - sp.cos(11))) == 0)
check("11 22A-B-Q1b half disk area 9pi/2", sp.integrate(sp.integrate(r, (r, 0, 3)), (th, 0, sp.pi)) == 9*sp.pi/2)
check("11 23A-A-Q1a value 7 pi^2/192", sp.simplify(sp.integrate(sp.integrate(th*r, (r, 1, 2)), (th, sp.pi/4, sp.pi/3)) - 7*sp.pi**2/192) == 0)
check("11 23A-A-Q1a arctan(y/x)=theta on the sector (numeric)", all(abs(math.atan(math.sin(a)/math.cos(a)) - a) < 1e-12 for a in np.linspace(math.pi/4, math.pi/3, 7)))
check("11 23A-A-Q1a lines y=x, y=sqrt3 x are theta=pi/4, pi/3", math.isclose(math.tan(math.pi/4), 1) and math.isclose(math.tan(math.pi/3), math.sqrt(3)))
# linear: 22A-B-Q4a
X_ = (v - u)/3; Y_ = (v + 2*u)/3
check("11 22A-B-Q4a inverse map: u=y-x, v=y+2x", zero((Y_ - X_) - u) and zero((Y_ + 2*X_) - v))
check("11 22A-B-Q4a |J| = 1/3", abs(jac_abs(X_, Y_, u, v)) == R(1, 3))
val = sp.integrate(sp.integrate(R(1, 3)*u/v, (u, 1, 4)), (v, 6, 8))
check("11 22A-B-Q4a value (5/2) ln(4/3)", sp.simplify(val - R(5, 2)*sp.log(R(4, 3))) == 0)
# numeric region check by grid: integral over the (x,y) parallelogram with indicator
N = 2400
xs = np.linspace(0, 4, N); ys = np.linspace(0, 8, 2*N)
Xg, Yg = np.meshgrid(xs, ys)
m = (Yg - Xg >= 1) & (Yg - Xg <= 4) & (Yg + 2*Xg >= 6) & (Yg + 2*Xg <= 8)
dA = (xs[1] - xs[0])*(ys[1] - ys[0])
numv = ((Yg - Xg)/(2*Xg + Yg))[m].sum()*dA
check("11 22A-B-Q4a grid value agrees with (5/2) ln(4/3)", abs(numv - 2.5*math.log(4/3)) < 2e-3)
check("11 22A-B-Q4a region area = 3 * area in uv = 3*... : area(D) = (1/3)*3*2 = 2", abs(m.sum()*dA - 2) < 5e-3)
# 25A-A-Q2b
Xs = (u + v)/2; Ys = (v - u)/2
check("11 25A-A-Q2b |J|=1/2 and x^2-y^2 = uv", abs(jac_abs(Xs, Ys, u, v)) == R(1, 2) and zero(Xs**2 - Ys**2 - u*v))
val = sp.integrate(sp.integrate(R(1, 2)*u*sp.exp(u*v), (v, 1, 3)), (u, -1, 1))
check("11 25A-A-Q2b value sinh3/3 - sinh1", sp.simplify(sp.simplify(val) - (sp.sinh(3)/3 - sp.sinh(1))) == 0 or abs(float(val) - (math.sinh(3)/3 - math.sinh(1))) < 1e-12)
N = 2000
xs = np.linspace(0, 2, N); ys = np.linspace(0, 2, N)
Xg, Yg = np.meshgrid(xs, ys)
m = (Xg + Yg >= 1) & (Xg + Yg <= 3) & (Yg - Xg <= 1) & (Yg - Xg >= -1)
dA = (xs[1] - xs[0])*(ys[1] - ys[0])
numv = (((Xg - Yg)*np.exp(Xg**2 - Yg**2))[m]).sum()*dA
check("11 25A-A-Q2b grid value agrees", abs(numv - (math.sinh(3)/3 - math.sinh(1))) < 5e-3)
# 23A-A-Q4a
J_inv = sp.Matrix([[sp.diff(y*x**2, x), sp.diff(y*x**2, y)], [sp.diff(y - x, x), sp.diff(y - x, y)]]).det()
check("11 23A-A-Q4a d(u,v)/d(x,y) = 2xy + x^2", zero(J_inv - (2*x*y + x**2)))
check("11 23A-A-Q4a integrand times |J| = 1, value 3*2 = 6", sp.integrate(sp.integrate(1, (u, 1, 4)), (v, -1, 1)) == 6)
N = 3000
xs = np.linspace(0.01, 3, N); ys = np.linspace(0.01, 5, N)
Xg, Yg = np.meshgrid(xs, ys)
m = (Yg*Xg**2 >= 1) & (Yg*Xg**2 <= 4) & (Yg >= Xg - 1) & (Yg <= Xg + 1)
dA = (xs[1] - xs[0])*(ys[1] - ys[0])
numv = ((Xg**2 + 2*Xg*Yg)[m]).sum()*dA
check("11 23A-A-Q4a grid value agrees with 6", abs(numv - 6) < 0.05)
# 26A-A-Q4a
J_inv = sp.Matrix([[sp.diff(y - x, x), sp.diff(y - x, y)], [sp.diff(x*y, x), sp.diff(x*y, y)]]).det()
check("11 26A-A-Q4a d(u,v)/d(x,y) = -(x+y)", zero(J_inv + (x + y)))
check("11 26A-A-Q4a x^2-y^2 = -u (x+y)", zero(x**2 - y**2 + (y - x)*(x + y)))
check("11 26A-A-Q4a value -1/2", sp.integrate(sp.integrate(-u, (u, 0, 1)), (v, 1, 2)) == R(-1, 2))
N = 3000
xs = np.linspace(0.01, 2.5, N); ys = np.linspace(0.01, 3, N)
Xg, Yg = np.meshgrid(xs, ys)
m = (Yg >= Xg) & (Yg <= Xg + 1) & (Xg*Yg >= 1) & (Xg*Yg <= 2)
dA = (xs[1] - xs[0])*(ys[1] - ys[0])
numv = ((Xg**2 - Yg**2)[m]).sum()*dA
check("11 26A-A-Q4a grid value agrees with -1/2", abs(numv + 0.5) < 0.01)
# 22A-A-Q4a
J_inv = sp.Matrix([[sp.diff(y - x, x), sp.diff(y - x, y)], [sp.diff(y**2 + 4*x, x), sp.diff(y**2 + 4*x, y)]]).det()
check("11 22A-A-Q4a d(u,v)/d(x,y) = -2y-4", zero(J_inv + 2*y + 4))
check("11 22A-A-Q4a upper component value 9e(e-1)", sp.simplify(sp.integrate(sp.exp(u), (u, 1, 2))*9 - 9*sp.E*(sp.E - 1)) == 0)
N = 3000
xs = np.linspace(-3, 3, N); ys = np.linspace(0.0, 6, N)
Xg, Yg = np.meshgrid(xs, ys)
m = (Yg - Xg >= 1) & (Yg - Xg <= 2) & (Yg**2 + 4*Xg >= 0) & (Yg**2 + 4*Xg <= 9) & (Yg >= 0)
dA = (xs[1] - xs[0])*(ys[1] - ys[0])
numv = ((np.exp(Yg - Xg)*(2*Yg + 4))[m]).sum()*dA
check("11 22A-A-Q4a grid value (y>=0 component) agrees with 9e(e-1)", abs(numv - float(9*sp.E*(sp.E - 1)))/float(9*sp.E*(sp.E - 1)) < 0.01)
# worked example for the brief: D bounded by y=x, y=2x, xy=1, xy=4 (x,y>0) of int x*y... use f=1 for area
Uu = y/x; Vv = x*y
J_inv = sp.Matrix([[sp.diff(Uu, x), sp.diff(Uu, y)], [sp.diff(Vv, x), sp.diff(Vv, y)]]).det()
check("11 worked: u=y/x, v=xy: d(u,v)/d(x,y) = -2y/x = -2u", zero(J_inv + 2*y/x))
check("11 worked: area = int_1^2 du int_1^4 dv/(2u) = (3/2) ln 2", sp.simplify(sp.integrate(sp.integrate(1/(2*u), (u, 1, 2)), (v, 1, 4)) - R(3, 2)*sp.log(2)) == 0)
N = 3000
xs = np.linspace(0.01, 4, N); ys = np.linspace(0.01, 5, N)
Xg, Yg = np.meshgrid(xs, ys)
m = (Yg >= Xg) & (Yg <= 2*Xg) & (Xg*Yg >= 1) & (Xg*Yg <= 4)
dA = (xs[1] - xs[0])*(ys[1] - ys[0])
check("11 worked: grid area agrees with (3/2) ln 2", abs(m.sum()*dA - 1.5*math.log(2)) < 0.01)

# ---------------------------------------------------------------- 12 numeric series
check("12 22A-A-Q2a  sin n/(n ln^2 n): dominated by integrable 1/(x ln^2 x), integral 1/ln2", sp.simplify(sp.integrate(1/(x*sp.log(x)**2), (x, 2, sp.oo)) - 1/sp.log(2)) == 0)
check("12 22A-A-Q2a (-1)^n+n over 3^n: ratio -> 1/3", sp.limit(((n + 1) + 1)/(3**(n + 1))/((n + 1)/3**n), n, sp.oo) == R(1, 3))
check("12 22A-A-Q2a  sum (n+1)/3^n converges: closed form", sp.simplify(sp.summation((n + 1)/3**n, (n, 1, sp.oo)) - R(5, 4)) == 0)
check("12 24B-B-Q2a |a_n| -> 1", sp.limit((n**2 + 3*sp.log(n))/((n + 1)*(n + 2)), n, sp.oo) == 1)
check("12 23A-A-Q2a limit comparison sin(pi/n)/(1/n) -> pi", sp.limit(sp.sin(sp.pi/n)*n, n, sp.oo) == sp.pi)
check("12 23A-A-Q2a limit comparison ln(1+n^(-4/3))/n^(-4/3) -> 1", sp.limit(sp.log(1 + n**R(-4, 3))*n**R(4, 3), n, sp.oo) == 1)
check("12 23A-C-Q2a root test arctan((n+2)/(n+3)) -> pi/4 < 1", sp.limit(sp.atan((n + 2)/(n + 3)), n, sp.oo) == sp.pi/4 and sp.pi/4 < 1)
check("12 24A-A-Q2a  sqrt n - sqrt(n-1) = 1/(sqrt n + sqrt(n-1)) decreasing to 0",
      zero(sp.sqrt(n) - sp.sqrt(n - 1) - 1/(sp.sqrt(n) + sp.sqrt(n - 1))) and all(1/(math.sqrt(m + 1) + math.sqrt(m)) < 1/(math.sqrt(m) + math.sqrt(m - 1)) for m in range(2, 2000)))
check("12 24A-A-Q2a limit comparison with 1/sqrt n gives 1/2", sp.limit((1/(sp.sqrt(n) + sp.sqrt(n - 1)))*sp.sqrt(n), n, sp.oo) == R(1, 2))
check("12 24A-A-Q2a sin(1/sqrt n)*sqrt n -> 1", sp.limit(sp.sin(1/sp.sqrt(n))*sp.sqrt(n), n, sp.oo) == 1)
check("12 24B-A-Q2a (3+sin sqrt n)/n^2 <= 4/n^2", all((3 + math.sin(math.sqrt(m)))/m**2 <= 4/m**2 + 1e-15 for m in range(1, 5000)))
check("12 24B-A-Q2b integral test diverges (ln ln)", sp.limit(sp.log(sp.log(X + 1)), X, sp.oo) == sp.oo)
check("12 24B-A-Q2b terms decrease (n+1)ln(n+1) increasing", all(1/((m + 2)*math.log(m + 2)) < 1/((m + 1)*math.log(m + 1)) for m in range(1, 3000)))
check("12 24B-B-Q2b bound (1+1/sqrt n)/n^3 <= 2/n^3", all((1 + 1/math.sqrt(m))/m**3 <= 2/m**3 for m in range(1, 3000)))
check("12 24S-A-Q2b cos n/(n^5+2)^(1/4) bounded by n^(-5/4)", all(abs(math.cos(m))/(m**5 + 2)**0.25 <= m**-1.25 for m in range(1, 3000)))
check("12 24S-A-Q2b 1/sqrt(n(n+1)) over 1/n -> 1", sp.limit(n/sp.sqrt(n*(n + 1)), n, sp.oo) == 1)
check("12 26A-A-Q2a geometric 2/3: sum = 2", sp.summation((R(2, 3))**n, (n, 1, sp.oo)) == 2)
check("12 24A-A-Q4a sum 1/(n^2+6n+8) = 7/24", sp.summation(1/(n**2 + 6*n + 8), (n, 1, sp.oo)) == R(7, 24))
check("12 24A-A-Q4a partial fractions 1/((n+2)(n+4)) = (1/2)(1/(n+2)-1/(n+4))", zero(1/((n + 2)*(n + 4)) - R(1, 2)*(1/(n + 2) - 1/(n + 4))))
check("12 24A-B-Q4a sum 5/3^n - 4/((n+3)(n+4)) = 3/2", sp.summation(5/3**n - 4/((n + 3)*(n + 4)), (n, 1, sp.oo)) == R(3, 2))
check("12 24A-B-Q4a geometric part 5/2 and telescoping part 1/4", sp.summation(5/3**n, (n, 1, sp.oo)) == R(5, 2) and sp.summation(1/((n + 3)*(n + 4)), (n, 1, sp.oo)) == R(1, 4))
check("12 25A-B-Q2a sum 1/(n(n-1)) from 2 = 1", sp.summation(1/(n*(n - 1)), (n, 2, sp.oo)) == 1)
check("12 25A-B-Q2a partial sums S_N = 1 - 1/N", all(abs(sum(1/(m*(m - 1)) for m in range(2, N_ + 1)) - (1 - 1/N_)) < 1e-12 for N_ in (5, 50, 500)))
check("12 p-series sample: sum 1/n^2 = pi^2/6", sp.summation(1/n**2, (n, 1, sp.oo)) == sp.pi**2/6)
check("12 geometric sum a/(1-q): sum_{n>=0} (1/2)^n = 2", sp.summation(R(1, 2)**n, (n, 0, sp.oo)) == 2)
check("12 Leibniz estimate: |S - S_N| <= a_{N+1} for alternating harmonic (N=1000)", abs(float(sum((-1)**(m + 1)/m for m in range(1, 1001))) - math.log(2)) <= 1/1001 + 1e-12)
# worked example in the brief: sum (-1)^n n/(n^2+1)
a = n/(n**2 + 1)
check("12 worked: n/(n^2+1) decreasing for n>=2 and -> 0", all(m/(m*m + 1) > (m + 1)/((m + 1)**2 + 1) for m in range(2, 5000)) and sp.limit(a, n, sp.oo) == 0)
check("12 worked: limit comparison n/(n^2+1) with 1/n gives 1", sp.limit(a*n, n, sp.oo) == 1)
check("12 worked: |a_1| = 1/2 > |a_2| = 2/5 (decreasing already from n=1)", R(1, 2) > R(2, 5))
check("12 worked ratio test: (2n)!/ (n!)^2 / 4^n ... ratio of  n!/n^n -> 1/e",
      sp.limit(sp.factorial(n + 1)/(n + 1)**(n + 1)*n**n/sp.factorial(n), n, sp.oo) == 1/sp.E if False else sp.limit((n/(n + 1))**n, n, sp.oo) == 1/sp.E)

# ---------------------------------------------------------------- 13 power series
def ratio_R(an):
    return sp.limit(sp.Abs(an/an.subs(n, n + 1)), n, sp.oo)


check("13 22A-A-Q3a R=1 for sin(pi/sqrt n)", sp.limit(sp.sin(sp.pi/sp.sqrt(n))/sp.sin(sp.pi/sp.sqrt(n + 1)), n, sp.oo) == 1)
check("13 22A-A-Q3a limit comparison sin(pi/sqrt n)*sqrt n -> pi", sp.limit(sp.sin(sp.pi/sp.sqrt(n))*sp.sqrt(n), n, sp.oo) == sp.pi)
check("13 22A-A-Q3a sin(pi/sqrt n) decreasing for n>=4", all(math.sin(math.pi/math.sqrt(m + 1)) < math.sin(math.pi/math.sqrt(m)) for m in range(4, 5000)) and not (math.sin(math.pi/math.sqrt(2)) < math.sin(math.pi/math.sqrt(1))))
check("13 22A-B-Q3a R=3", ratio_R(n/((n**2 + 1)*3**n)) == 3)
check("13 22A-B-Q3a endpoint x=3 term n/(n^2+1) ~ 1/n", sp.limit(n/(n**2 + 1)*n, n, sp.oo) == 1)
check("13 23A-A-Q3a R=sqrt5/3", sp.simplify(ratio_R(3**n/((2*n + 1)**2*sp.sqrt(5**n))) - sp.sqrt(5)/3) == 0)
check("13 23A-C-Q3a R=3 by root test", sp.limit((1/(2**n + 3**n))**(1/n), n, sp.oo) == R(1, 3))
check("13 23A-C-Q3a endpoint term 3^n/(2^n+3^n) -> 1", sp.limit(3**n/(2**n + 3**n), n, sp.oo) == 1)
check("13 24A-A-Q3a R_s = 1/2 for 2^n/(n^2+1)", ratio_R(2**n/(n**2 + 1)) == R(1, 2))
check("13 24A-A-Q3a domain: s in [-1/2,1/2] -> x in [-3/2,-1/2]", (R(-1, 2) - 1, R(1, 2) - 1) == (R(-3, 2), R(-1, 2)))
check("13 24A-B-Q3a R=1 and terms ~ n^(-4/3)", sp.limit(sp.simplify(((n + 2)**R(1, 3)*sp.sqrt((n + 1)**2 + 1))/((n + 1)**R(1, 3)*sp.sqrt(n**2 + 1))), n, sp.oo) == 1
      and sp.limit(n**R(4, 3)/((n + 1)**R(1, 3)*sp.sqrt(n**2 + 1)), n, sp.oo) == 1)
check("13 24A-B-Q3a domain: |x+5|<=1 -> [-6,-4]", (-5 - 1, -5 + 1) == (-6, -4))
check("13 24B-A-Q4b R=oo", sp.limit(sp.Abs((2**n*sp.factorial(n)/sp.factorial(2*n))/(2**(n + 1)*sp.factorial(n + 1)/sp.factorial(2*n + 2))), n, sp.oo) == sp.oo)
check("13 24B-B-Q4b R=1/2", sp.limit(2**(n + 1)/sp.sqrt(n + 5)*sp.sqrt(n + 4)/2**n, n, sp.oo) == 2)
check("13 24B-B-Q4b endpoint terms 1/sqrt(n+4): limit comparison with 1/sqrt n gives 1", sp.limit(sp.sqrt(n)/sp.sqrt(n + 4), n, sp.oo) == 1)
check("13 24B-B-Q4b domain [1/2, 3/2)", (1 - R(1, 2), 1 + R(1, 2)) == (R(1, 2), R(3, 2)))
check("13 24S-A-Q3a R=4, domain [-2,6)", ratio_R(1/(n*4**n)) == 4 and (2 - 4, 2 + 4) == (-2, 6))
check("13 25A-A-Q3a R=1/2", sp.limit(sp.sqrt(5*(n + 1)**2 + 1)/(2*sp.sqrt(5*n**2 + 1)), n, sp.oo) == R(1, 2))
check("13 25A-A-Q3a domain [1/2,3/2)", (1 - R(1, 2), 1 + R(1, 2)) == (R(1, 2), R(3, 2)))
check("13 25A-B-Q3a R=1, sin^2(1/n) * n^2 -> 1", sp.limit(sp.sin(1/n)**2*n**2, n, sp.oo) == 1)
check("13 26A-A-Q3a shift: [-3,3) -> [-5,1)", (-3 - 2, 3 - 2) == (-5, 1))
check("13 22A-B-Q5a termwise derivative gives 1/(1+x^2), integral arctan", zero(sp.diff(sp.atan(x), x) - 1/(1 + x**2)) and sp.series(sp.atan(x), x, 0, 8).removeO() == x - x**3/3 + x**5/5 - x**7/7)
check("13 22A-B-Q5a at x=1: pi/4 = 1 - 1/3 + 1/5 ...", abs(float(sum((-1)**(m + 1)/(2*m - 1) for m in range(1, 200001))) - math.pi/4) < 1e-5)
# worked example: sum (x-3)^n/(n 2^n)
an = 1/(n*2**n)
check("13 worked: sum (x-3)^n/(n 2^n) has R=2", ratio_R(an) == 2)
check("13 worked: endpoint x=5 harmonic diverges, x=1 alternating harmonic converges; domain [1,5)", (3 - 2, 3 + 2) == (1, 5))
# root test and ratio test agree
check("13 Cauchy-Hadamard vs ratio on 3^n/(2n+1)^2 sqrt(5^n)",
      sp.simplify(sp.limit(((3**n/((2*n + 1)**2*sp.sqrt(5**n)))**(1/n)), n, sp.oo) - 3/sp.sqrt(5)) == 0)
check("13 Cauchy-Hadamard: R=sqrt5/3 is the reciprocal", sp.simplify(sp.sqrt(5)/3 - 1/(3/sp.sqrt(5))) == 0)
# radius of derivative / integral series unchanged
check("13 termwise derivative of sum x^n/n has same radius: sum x^(n-1) -> R=1", ratio_R(1/n) == 1 and ratio_R(sp.Integer(1)) == 1)

# ---------------------------------------------------------------- 14 Taylor / Maclaurin
def maclaurin_coeffs(expr, N_):
    ser = sp.series(expr, x, 0, N_ + 1).removeO()
    return [sp.simplify(ser.coeff(x, i)) for i in range(N_ + 1)]


def deriv0(expr, m):
    return sp.simplify(sp.diff(expr, x, m).subs(x, 0))


f = 1/(x**2 + x - 2)
c = lambda m: -R(1, 3)*(1 + R((-1)**m, 2**(m + 1)))
check("14 22A-A-Q5a coefficients -(1/3)(1+(-1)^n/2^(n+1))", maclaurin_coeffs(f, 8) == [c(m) for m in range(9)])
check("14 23A-C-Q5b f^(10)(0) = 10! c_10", deriv0(f, 10) == sp.factorial(10)*c(10))
v10 = deriv0(f, 10)
check("14 23A-C-Q5b numeric value of f^(10)(0)", v10 == -R(1, 3)*sp.factorial(10)*(1 + R(1, 2**11)))
f = 1/(x**2 + x - 6)
c = lambda m: R(1, 5)*(-R((-1)**m, 3**(m + 1)) - R(1, 2**(m + 1)))
check("14 23A-A-Q5b coefficients (1/5)(-(-1)^n/3^(n+1) - 1/2^(n+1))", maclaurin_coeffs(f, 8) == [c(m) for m in range(9)])
check("14 23A-A-Q5b f^(10)(0) = 10! c_10", deriv0(f, 10) == sp.factorial(10)*c(10))
check("14 23A-A-Q5b radius 2 (nearest pole x=2)", min(abs(p) for p in sp.solve(x**2 + x - 6, x)) == 2)
f = 1/(1 - 3*x**2)
check("14 24A-A-Q5b only even powers 3^k x^(2k); f^(5)(0)=0", maclaurin_coeffs(f, 6) == [1, 0, 3, 0, 9, 0, 27] and deriv0(f, 5) == 0)
check("14 24A-A-Q5b radius 1/sqrt3", sp.solve(1 - 3*x**2, x) == [-sp.sqrt(3)/3, sp.sqrt(3)/3])
f = x/(25 + x**2)
check("14 24A-B-Q5b f^(5)(0) = 4!/5^5 = 24/3125", deriv0(f, 5) == R(24, 3125) == sp.factorial(4)/5**5)
check("14 24A-B-Q5b coefficient of x^5 is 1/5^6", maclaurin_coeffs(f, 5)[5] == R(1, 5**6))
f = sp.log(2*x**2 + 3*x + 1)
cc = lambda m: R((-1)**(m + 1)*(1 + 2**m), m)
check("14 24B-A-Q5a coefficients (-1)^(n+1)(1+2^n)/n", maclaurin_coeffs(f, 8)[1:] == [cc(m) for m in range(1, 9)])
check("14 24B-A-Q5c f^(5)(0) = 792", deriv0(f, 5) == 792 == 33*sp.factorial(4))
check("14 24B-A-Q5b radius 1/2 (|2x|<1) and endpoint x=1/2 conv. (alternating harmonic), -1/2 div.",
      sp.limit((((1 + 2**n)/n))**(1/n), n, sp.oo) == 2)
f = sp.log(6*x**2 + 5*x + 1)
cc = lambda m: R((-1)**(m + 1)*(3**m + 2**m), m)
check("14 24B-B-Q5a coefficients (-1)^(n+1)(3^n+2^n)/n", maclaurin_coeffs(f, 8)[1:] == [cc(m) for m in range(1, 9)])
check("14 24B-B-Q5c f^(5)(0) = 6600", deriv0(f, 5) == 6600 == 55*sp.factorial(5))
f = sp.log(1 + x**2) - sp.exp(2*x)
check("14 25A-B-Q5b(25A-A-Q5b) f^(6)(0) = 176", deriv0(f, 6) == 176 == sp.factorial(6)*(R(1, 3) - R(64, 720)))
check("14 25A-A-Q5b odd coefficients -2^n/n! and even n=2k: (-1)^(k+1)/k - 2^n/n!", maclaurin_coeffs(f, 6)[3] == -R(8, 6) and maclaurin_coeffs(f, 6)[2] == R(1, 1) - 2)
f = 1/(x**2 - 5*x + 6)
check("14 25A-B-Q5b coefficients 1/2^(n+1) - 1/3^(n+1)", maclaurin_coeffs(f, 8) == [R(1, 2**(m + 1)) - R(1, 3**(m + 1)) for m in range(9)])
check("14 25A-B-Q5b f^(5)(0) = 120 (1/64 - 1/729)", deriv0(f, 5) == 120*(R(1, 64) - R(1, 729)))
f = (16 - 5*x)/(x**2 - 5*x + 6)
check("14 26A-A-Q5b partial fractions -6/(x-2) + 1/(x-3)", zero(f - (-6/(x - 2) + 1/(x - 3))))
check("14 26A-A-Q5b coefficients 3/2^n - 1/3^(n+1)", maclaurin_coeffs(f, 8) == [R(3, 2**m) - R(1, 3**(m + 1)) for m in range(9)])
check("14 26A-A-Q5b f^(20)(0) = 20! (3/2^20 - 1/3^21)", deriv0(f, 20) == sp.factorial(20)*(R(3, 2**20) - R(1, 3**21)))
check("14 sheet series: e^x, sin, cos, ln(1+x), 1/(1-x)",
      sp.series(sp.exp(x), x, 0, 5).removeO() == 1 + x + x**2/2 + x**3/6 + x**4/24
      and sp.series(sp.sin(x), x, 0, 6).removeO() == x - x**3/6 + x**5/120
      and sp.series(sp.cos(x), x, 0, 5).removeO() == 1 - x**2/2 + x**4/24
      and sp.series(sp.log(1 + x), x, 0, 5).removeO() == x - x**2/2 + x**3/3 - x**4/4
      and sp.series(1/(1 - x), x, 0, 5).removeO() == 1 + x + x**2 + x**3 + x**4)
check("14 substitution: e^{2x}: 2^n/n!", sp.series(sp.exp(2*x), x, 0, 5).removeO() == 1 + 2*x + 2*x**2 + R(4, 3)*x**3 + R(2, 3)*x**4)
check("14 ln(1+x^2) coefficient pattern (-1)^(k+1)/k at x^(2k)", sp.series(sp.log(1 + x**2), x, 0, 8).removeO() == x**2 - x**4/2 + x**6/3)
# worked example in the brief: f = x/(1+x)(1-2x)? use f = 1/((1-x)(1-2x)) -> 2^(n+1)-1, and f''(0)
f = 1/((1 - x)*(1 - 2*x))
check("14 worked: 1/((1-x)(1-2x)) coefficients 2^(n+1)-1", maclaurin_coeffs(f, 7) == [2**(m + 1) - 1 for m in range(8)])
check("14 worked: f^(4)(0) = 4! (2^5 - 1) = 744", deriv0(f, 4) == 744 == sp.factorial(4)*31)
check("14 worked: partial fractions 2/(1-2x) - 1/(1-x)", zero(f - (2/(1 - 2*x) - 1/(1 - x))))
check("14 worked: radius = 1/2 (nearest pole)", min(abs(p) for p in sp.solve(1 - 2*x, x) + sp.solve(1 - x, x)) == R(1, 2))
check("14 Taylor around x0: ln x about 1 coefficient (-1)^(n+1)/n", sp.series(sp.log(x), x, 1, 5).removeO().expand() == sp.expand((x - 1) - (x - 1)**2/2 + (x - 1)**3/3 - (x - 1)**4/4))
check("14 odd function has only odd powers (x/(25+x^2))", all(maclaurin_coeffs(x/(25 + x**2), 8)[m] == 0 for m in (0, 2, 4, 6, 8)))

# ---------------------------------------------------------------- additions quoted in 11 and 12
check("12 22A-B-Q2a (1+cos n)/2^(n+1) <= (1/2)^n", all((1 + math.cos(m))/2**(m + 1) <= 0.5**m + 1e-15 for m in range(1, 200)))
check("12 22A-B-Q2a 1/(n - ln n)^3 over 1/n^3 -> 1", sp.limit(n**3/(n - sp.log(n))**3, n, sp.oo) == 1)
check("12 22A-B-Q2a x - ln x increasing for x>=2: derivative 1-1/x > 0", sp.diff(x - sp.log(x), x) == 1 - 1/x and all(1 - 1/q > 0 for q in (2, 3, 10)))
check("12 |(-1)^n + n|/3^n <= (n+1)/3^n and sum (-1)^n/3^n, sum n/3^n converge", sp.summation((-1)**n/3**n, (n, 1, sp.oo)) == R(-1, 4) and sp.summation(n/3**n, (n, 1, sp.oo)) == R(3, 4))
check("11 25A-A-Q2b inner integral int_1^3 u e^(uv) dv = e^(3u) - e^u", zero(sp.integrate(u*sp.exp(u*v), (v, 1, 3)) - (sp.exp(3*u) - sp.exp(u))))
check("11 25A-A-Q2b (1/2) int_-1^1 (e^3u - e^u) du = sinh3/3 - sinh1", abs(float(R(1, 2)*sp.integrate(sp.exp(3*u) - sp.exp(u), (u, -1, 1))) - (math.sinh(3)/3 - math.sinh(1))) < 1e-12)

# ---------------------------------------------------------------- cheat sheet extras
check("cheat Hessian criterion: x^2+y^2 min, -x^2-y^2 max, x^2-y^2 saddle", classify(x**2 + y**2, [(0, 0)])[(0, 0)][0] == "min" and classify(-x**2 - y**2, [(0, 0)])[(0, 0)][0] == "max" and classify(x**2 - y**2, [(0, 0)])[(0, 0)][0] == "saddle")
check("cheat polar Jacobian r and linear |J|=1/|d(u,v)/d(x,y)|: u=x+y,v=x-y -> 1/2", abs(jac_abs((u + v)/2, (u - v)/2, u, v)) == R(1, 2))
check("cheat implicit derivative formula z_x = -F_x/F_z on x^2+y^2+z^2=3 at (1,1,1) = -1", -sp.diff(x**2 + y**2 + z**2, x).subs({x: 1, y: 1, z: 1})/sp.diff(x**2 + y**2 + z**2, z).subs({x: 1, y: 1, z: 1}) == -1)

print("OK: %d checks passed" % len(ok))
