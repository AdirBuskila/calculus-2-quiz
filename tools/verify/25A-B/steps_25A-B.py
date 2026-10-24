# -*- coding: utf-8 -*-
"""Machine checks for every numeric / choice value used in the guided steps of sitting 25A-B.
Run: PYTHONUTF8=1 py tools/verify/25A-B/steps_25A-B.py"""
import sympy as sp
import numpy as np
from scipy import integrate as si

R = sp.Rational
x, y, t, v, n, s = sp.symbols("x y t v n s", real=True)
ok = []


def check(name, cond):
    assert cond, "MISMATCH: " + name
    ok.append(name)


# ---- Q1a ----
f = sp.sqrt(41 - 4*x**2 - y**2)
p = {x: 2, y: 3}
check("Q1a f(2,3)=4", f.subs(p) == 4)
check("Q1a f_x(2,3)=-2", sp.diff(f, x).subs(p) == -2)
check("Q1a f_y(2,3)=-3/4", sp.diff(f, y).subs(p) == R(-3, 4))
approx = 4 + (-2)*R(1, 10) + R(-3, 4)*R(-1, 10)
check("Q1a linear approximation 3.875", approx == R(31, 8) and float(approx) == 3.875)
check("Q1a exact value differs (~3.8665)", abs(float(f.subs({x: 2.1, y: 2.9})) - 3.8665) < 1e-3)

# ---- Q1b ----
g = x*y
lam = sp.Symbol("lam")
L = g + lam*(x**2 + y**2 - 2)
sol = sp.solve([sp.diff(L, x), sp.diff(L, y), x**2 + y**2 - 2], [x, y, lam], dict=True)
pts = {(q[x], q[y]) for q in sol}
check("Q1b four points", pts == {(1, 1), (1, -1), (-1, 1), (-1, -1)})
vals = {pt: g.subs({x: pt[0], y: pt[1]}) for pt in pts}
check("Q1b max 1 at (1,1),(-1,-1)", {k for k, val in vals.items() if val == 1} == {(1, 1), (-1, -1)})
check("Q1b min -1 at (1,-1),(-1,1)", {k for k, val in vals.items() if val == -1} == {(1, -1), (-1, 1)})
th = np.linspace(0, 2*np.pi, 100001)
gv = 2*np.cos(th)*np.sin(th)
check("Q1b numeric on circle max 1 min -1", abs(gv.max() - 1) < 1e-6 and abs(gv.min() + 1) < 1e-6)

# ---- Q2a ----
S5 = sum(R(1, k*(k - 1)) for k in range(2, 6))
check("Q2a S_5 = 0.8", S5 == R(4, 5))
check("Q2a partial fractions", sp.apart(1/(s*(s - 1)), s) == 1/(s - 1) - 1/s)
check("Q2a sum is 1", sp.summation(1/(n*(n - 1)), (n, 2, sp.oo)) == 1)
check("Q2a S_n=1-1/n", all(sum(R(1, k*(k - 1)) for k in range(2, m + 1)) == 1 - R(1, m) for m in range(2, 30)))

# ---- Q2b ----
tt, vv = sp.symbols("tt vv")
inv = sp.solve([tt - (y - x), vv - (y + 2*x)], [x, y], dict=True)[0]
check("Q2b inverse x=(v-t)/3", sp.simplify(inv[x] - (vv - tt)/3) == 0)
check("Q2b inverse y=(v+2t)/3 (corrected)", sp.simplify(inv[y] - (vv + 2*tt)/3) == 0)
check("Q2b typo y=(v+t)/3 is wrong", sp.simplify(inv[y] - (vv + tt)/3) != 0)
vertex = {x: R(5, 3), y: R(8, 3)}
check("Q2b vertex (5/3,8/3): t=1, v=6", (y - x).subs(vertex) == 1 and (y + 2*x).subs(vertex) == 6)
check("Q2b |J|=1/3", abs(sp.Matrix([inv[x], inv[y]]).jacobian([tt, vv]).det()) == R(1, 3))
check("Q2b forward det is -3", sp.Matrix([y - x, y + 2*x]).jacobian([x, y]).det() == -3)
check("Q2b bounds: y-x in {1,4}; y+2x in {6,8}",
      sp.simplify((y - x).subs(y, 1 + x)) == 1 and sp.simplify((y - x).subs(y, 4 + x)) == 4
      and sp.simplify((y + 2*x).subs(y, 6 - 2*x)) == 6 and sp.simplify((y + 2*x).subs(y, 8 - 2*x)) == 8)
check("Q2b int_1^4 t dt = 15/2", sp.integrate(t, (t, 1, 4)) == R(15, 2))
val = R(1, 3)*R(15, 2)*sp.log(R(8, 6))
check("Q2b value (5/2)ln(4/3)", sp.simplify(val - R(5, 2)*sp.log(R(4, 3))) == 0)
check("Q2b numeric 0.7192", abs(float(val) - 0.71922) < 1e-4)
# direct numeric check in (x,y): parallelogram; integrate in (t,v) after mapping
num, _ = si.dblquad(lambda vq, tq: tq/vq/3, 1, 4, lambda tq: 6, lambda tq: 8)
check("Q2b numeric (t,v) integral", abs(num - float(val)) < 1e-9)

# ---- Q3a ----
check("Q3a R=1 via ratio of sin^2", sp.limit(sp.sin(1/n)**2/sp.sin(1/(n + 1))**2, n, sp.oo) == 1)
check("Q3a sin^2(1/n)*n^2 -> 1", sp.limit(sp.sin(1/n)**2*n**2, n, sp.oo) == 1)
check("Q3a sum sin^2(1/n) converges numerically (partial sums bounded by pi^2/6)",
      float(sum(np.sin(1/np.arange(1, 200001))**2)) < float(sp.pi**2/6))

# ---- Q3b ----
for gg in (sp.sin, sp.exp, lambda w: w**3 + w):
    tfun = sp.cos(x - y)
    Z = y*gg(tfun)
    gp = lambda w, gg=gg: sp.diff(gg(s), s).subs(s, w)
    zx = -y*sp.sin(x - y)*gp(tfun)
    zy = gg(tfun) + y*sp.sin(x - y)*gp(tfun)
    check("Q3b z_x formula", sp.simplify(sp.diff(Z, x) - zx) == 0)
    check("Q3b z_y formula", sp.simplify(sp.diff(Z, y) - zy) == 0)
    check("Q3b identity z_x+z_y = z/y", sp.simplify(sp.diff(Z, x) + sp.diff(Z, y) - Z/y) == 0)
    bad_x = y*sp.sin(x - y)*gp(tfun)
    check("Q3b sign-bug z_x breaks identity", sp.simplify(bad_x + zy - Z/y) != 0)
    check("Q3b distractor z_y=g - y sin g' differs", sp.simplify(gg(tfun) - y*sp.sin(x - y)*gp(tfun) - zy) != 0)
    check("Q3b distractor z_y=g + y cos g' differs", sp.simplify(gg(tfun) + y*sp.cos(x - y)*gp(tfun) - zy) != 0)
    check("Q3b distractor z_y=y sin g' differs", sp.simplify(y*sp.sin(x - y)*gp(tfun) - zy) != 0)

# ---- Q4a ----
areaA = sp.integrate(sp.sqrt(x + 4), (x, -4, 0)) + sp.integrate(2 - x, (x, 0, 2))
areaB = sp.integrate((2 - y) - (y**2 - 4), (y, 0, 2))
check("Q4a area 22/3 in both orders", areaA == R(22, 3) and areaB == R(22, 3))
check("Q4a 22/3 ~ 7.3333", abs(float(areaA) - 7.3333) < 1e-4)
check("Q4a y max is 2 (curve meets x=0 at y=2)", sp.sqrt(0 + 4) == 2)
wrong = [sp.integrate((2 + y) - (y**2 - 4), (y, 0, 2)), sp.integrate((2 - y) - y**2, (y, 0, 2)),
         sp.integrate((2 - y) - (y - 4), (y, 0, 2))]
check("Q4a distractor bounds give other areas", all(w != R(22, 3) for w in wrong))
# the solved boundary: y=sqrt(x+4) <=> x=y^2-4 (y>=0)
check("Q4a x=y^2-4", sp.solve(sp.Eq(y, sp.sqrt(x + 4)), x) == [y**2 - 4])

# ---- Q4b ----
f4 = x**3 + 8*y**3 - 6*x*y + 1
cr = sp.solve([sp.diff(f4, x), sp.diff(f4, y)], [x, y], dict=True)
cs = {(q[x], q[y]) for q in cr if q[x].is_real and q[y].is_real}
check("Q4b real critical points (0,0),(1,1/2)", cs == {(0, 0), (1, R(1, 2))})
check("Q4b (-1,1/2) not critical: f_y=24/4-6*(-1)=12 != 0", sp.diff(f4, y).subs({x: -1, y: R(1, 2)}) == 12)
H = sp.hessian(f4, (x, y))
check("Q4b det at origin -36", H.subs({x: 0, y: 0}).det() == -36)
Hm = H.subs({x: 1, y: R(1, 2)})
check("Q4b (1,1/2): f_xx=6, det=108 -> min", Hm[0, 0] == 6 and Hm.det() == 108)

# ---- Q5a ----
f5 = y*sp.cos(x*y)
gr = sp.Matrix([sp.diff(f5, x), sp.diff(f5, y)]).subs({x: 1, y: 0})
check("Q5a gradient (0,1)", gr == sp.Matrix([0, 1]))
def D(u): return (gr.T*sp.Matrix(u))[0]
check("Q5a D along (0,1) is 1", D([0, 1]) == 1)
check("Q5a D along (1,0) is 0", D([1, 0]) == 0)
check("Q5a D along (0,-1) is -1", D([0, -1]) == -1)
check("Q5a D along (1,1)/sqrt2 is sqrt2/2 (<1)", sp.simplify(D([1/sp.sqrt(2), 1/sp.sqrt(2)]) - sp.sqrt(2)/2) == 0)
# uniqueness: b=1 and a^2+b^2=1 -> a=0
a = sp.Symbol("a", real=True)
check("Q5a unique unit vector with D=1", sp.solve([a**2 + 1 - 1], [a]) == [(0,)] or sp.solve(a**2, a) == [0])

# ---- Q5b ----
f6 = 1/(x**2 - 5*x + 6)
check("Q5b partial fractions 1/(2-x)-1/(3-x)", sp.simplify(f6 - (1/(2 - x) - 1/(3 - x))) == 0)
check("Q5b partial fractions as -1/(x-2)+1/(x-3)", sp.apart(f6, x) == -1/(x - 2) + 1/(x - 3))
ser = sp.series(f6, x, 0, 7).removeO()
a5 = ser.coeff(x, 5)
check("Q5b a5 = 1/64-1/729", a5 == R(1, 64) - R(1, 729))
check("Q5b a5 ~ 0.014253", abs(float(a5) - 0.014253) < 1e-6)
check("Q5b f^(5)(0)=3325/1944", sp.diff(f6, x, 5).subs(x, 0) == R(3325, 1944))
check("Q5b 3325/1944 ~ 1.7104 (not 1.71166)", abs(float(R(3325, 1944)) - 1.7104) < 1e-3 and abs(float(R(3325, 1944)) - 1.71166) > 1e-3)
check("Q5b radius 2 (poles at 2 and 3)", sp.solve(x**2 - 5*x + 6, x) == [2, 3])

print(f"{len(ok)} checks passed")
for q in ok:
    print(" -", q)
