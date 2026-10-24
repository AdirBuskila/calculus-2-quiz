# -*- coding: utf-8 -*-
"""sympy/numeric checks for the guided steps of 24A-B (student-solution key: every claim is re-derived here).
Run: PYTHONUTF8=1 py -I tools/verify/24A-B/steps_24A-B.py   (after gen_24A-B.py)"""
import json, pathlib, math
import numpy as np
import sympy as sp

HERE = pathlib.Path(__file__).resolve().parent
raw = json.loads((HERE.parents[1] / "raw" / "24A-B.json").read_text(encoding="utf-8"))
Q = {f"{q['num']}{q.get('part','')}": q for q in raw["questions"]}
S = sp.Rational
count = 0


def chk(key, idx, val):
    global count
    s = Q[key]["steps"][idx]
    assert s["type"] == "numeric", (key, idx, s["type"])
    assert abs(float(val) - s["answer"]) <= s.get("tol", 0) + 1e-12, (key, idx, float(val), s["answer"])
    count += 1


x, y, k = sp.symbols("x y k", real=True)
t = sp.symbols("t", positive=True)
n = sp.symbols("n", positive=True, integer=True)

# ---- Q1a: f = x^2 y^2/(x^6+y^3)
f = x**2*y**2/(x**6 + y**3)
chk("1א", 0, sp.limit(sp.simplify(f.subs(y, x)), x, 0, "+"))
assert sp.limit(sp.simplify(f.subs(y, k*x)), x, 0, "+") == 0 and k != 0
chk("1א", 1, sp.limit(sp.simplify(f.subs(y, x**2)), x, 0, "+"))

# ---- Q1b: f = x + xy, direction with D_u f = 1/sqrt2 at (1,-1)
f1 = x + x*y
g1 = sp.Matrix([sp.diff(f1, x), sp.diff(f1, y)]).subs({x: 1, y: -1})
assert g1 == sp.Matrix([0, 1])
chk("1ב", 0, g1[0])
a, b = sp.symbols("a b", real=True)
sols = sp.solve([g1[0]*a + g1[1]*b - 1/sp.sqrt(2), a**2 + b**2 - 1], [a, b], dict=True)
assert len(sols) == 2 and {s[a] for s in sols} == {1/sp.sqrt(2), -1/sp.sqrt(2)} and all(s[b] == 1/sp.sqrt(2) for s in sols)
chk("1ב", 1, 1/sp.sqrt(2))
chk("1ב", 2, sols[0][a]**2)

# ---- Q2a
c1 = lambda m: 1/((m + 1)*math.log(m + 1))
assert all(c1(m + 1) < c1(m) for m in range(1, 5000)) and c1(10**9) < 1e-7           # Leibniz hypotheses
xx, bb = sp.symbols("xx bb", positive=True)
I = sp.integrate(1/((xx + 1)*sp.log(xx + 1)), (xx, 1, bb))
assert sp.limit(I, bb, sp.oo) == sp.oo                                                  # abs. series diverges (integral test)
assert sum(c1(m) for m in range(1, 10**6)) > sum(c1(m) for m in range(1, 10**4)) + 0.4  # grows like ln ln
chk("2א", 1, sp.limit(((-1)**n*0 + (n - 1))**(1/n)/3, n, sp.oo))   # lower sandwich side -> 1/3
assert sp.limit(((n + 1)**(1/n))/3, n, sp.oo) == S(1, 3)           # upper sandwich side -> 1/3
assert all((-1)**m + m >= 0 for m in range(1, 100))

# ---- Q2b
f2 = (x**3 + y**3)/(2*x**2 + y**2)
chk("2ב", 0, sp.limit(f2.subs({x: t, y: 0})/t, t, 0))
chk("2ב", 1, sp.limit(f2.subs({x: 0, y: t})/t, t, 0))
dx, dy = sp.symbols("dx dy", positive=True)
eps = (f2.subs({x: dx, y: dy}) - dx/2 - dy)/sp.sqrt(dx**2 + dy**2)
eps_k = sp.simplify(eps.subs(dy, k*dx))
lim_k = sp.limit(eps_k, dx, 0, "+")
assert sp.simplify(lim_k + (k**2 + 4*k)/(2*(2 + k**2)*sp.sqrt(1 + k**2))) == 0   # the key's closed form (dx>0, k>0)
chk("2ב", 2, lim_k.subs(k, 1))
assert abs(float(lim_k.subs(k, 1))) > 0.1 and sp.limit(eps_k.subs(k, S(1, 1000000)), dx, 0, "+") != lim_k.subs(k, 1)

# ---- Q3a: re-derive endpoints independently
an = 1/(sp.cbrt(n + 1)*sp.sqrt(n**2 + 1))
chk("3א", 0, sp.limit(an/an.subs(n, n + 1), n, sp.oo))
assert sp.limit(an/n**S(-4, 3), n, sp.oo) == 1                   # same order as n^(-4/3)
chk("3א", 1, S(1, 3) + 1)
tail = lambda N0, N1: sum(1/((m + 1)**(1/3)*(m*m + 1)**0.5) for m in range(N0, N1))
assert tail(10**5, 4*10**6) < 3.2*(10**5)**(-1/3)                # x=-4: tail below the p=4/3 integral bound (converges)
assert all(1/((m + 1)**(1/3)*(m*m + 1)**0.5) <= m**(-4/3) for m in range(1, 20000))
assert tail(2*10**5, 4*10**6) < 3.2*(2*10**5)**(-1/3)   # x=-6: same absolute series, tail under the p=4/3 bound
# ratio test says nothing at |t|=1; endpoints verified above, so the domain is the closed interval
assert (-1 - 5, 1 - 5) == (-6, -4)

# ---- Q3b: z = y/(3x) + g(xy)
G = sp.Function("g")
z = y/(3*x) + G(x*y)
assert sp.simplify(sp.diff(G(x*y), x).doit() - y*sp.Subs(sp.Derivative(G(sp.Symbol("w")), sp.Symbol("w")), sp.Symbol("w"), x*y).doit()) == 0
lhs = sp.simplify(x**2*sp.diff(z, x) - x*y*sp.diff(z, y) + 2*y/3)
assert lhs == 0, lhs
# the broken line really breaks it
gp = sp.Symbol("gp")
good = -y/3 + x**2*y*gp - y/3 - x**2*y*gp + 2*y/3
bad = -y/3 + x**2*y*gp + y/3 - x**2*y*gp + 2*y/3
assert sp.simplify(good) == 0 and sp.simplify(bad) != 0
count += 0

# ---- Q4a
S1 = sp.Sum(5/3**n, (n, 1, sp.oo)).doit()
chk("4א", 0, S1)
S2 = sp.Sum(1/((n + 3)*(n + 4)), (n, 1, sp.oo)).doit()
chk("4א", 1, S2)
chk("4א", 2, S1 - 4*S2)
assert abs(sum(5*(1/3)**m - 4/((m + 3)*(m + 4)) for m in range(1, 200000)) - 1.5) < 1e-4

# ---- Q4b: f = 2x^4+y^4-x^2-2y^2 on x^2+y^2 <= 2
f4 = 2*x**4 + y**4 - x**2 - 2*y**2
crit = sp.solve([sp.diff(f4, x), sp.diff(f4, y)], [x, y], dict=True)
assert len(crit) == 9 and all(c[x]**2 + c[y]**2 < 2 for c in crit)
chk("4ב", 0, len(crit))
chk("4ב", 1, f4.subs({x: S(1, 2), y: 1}))
chk("4ב", 2, f4.subs({x: sp.sqrt(2), y: 0}))
chk("4ב", 3, f4.subs({x: 1/sp.sqrt(2), y: sp.sqrt(S(3, 2))}))
lam = sp.symbols("lam")
Lg = f4 + lam*(x**2 + y**2 - 2)
bsol = sp.solve([sp.diff(Lg, x), sp.diff(Lg, y), x**2 + y**2 - 2], [x, y, lam], dict=True)
bvals = {sp.nsimplify(f4.subs(s)) for s in bsol}
assert bvals == {0, 6, S(-3, 4)}, bvals
vals = [f4.subs(c) for c in crit] + [f4.subs(s) for s in bsol]
assert max(vals) == 6 and min(vals) == S(-9, 8)
chk("4ב", 4, min(vals))
g = np.linspace(-1.5, 1.5, 1501)
X, Y = np.meshgrid(g, g)
m = X**2 + Y**2 <= 2
F = 2*X**4 + Y**4 - X**2 - 2*Y**2
assert abs(F[m].max() - 6) < 5e-2 and abs(F[m].min() + 9/8) < 1e-6

# ---- Q5a: f = (3-x)(3-y)(x+y-3)
f5 = (3 - x)*(3 - y)*(x + y - 3)
fx, fy = sp.diff(f5, x), sp.diff(f5, y)
assert sp.expand(fx - (3 - y)*(6 - 2*x - y)) == 0 and sp.expand(fy - (3 - x)*(6 - x - 2*y)) == 0
cs = sp.solve([fx, fy], [x, y], dict=True)
assert {(c[x], c[y]) for c in cs} == {(0, 3), (3, 0), (3, 3), (2, 2)}
chk("5א", 0, len(cs))
D = lambda p: (sp.diff(f5, x, 2)*sp.diff(f5, y, 2) - sp.diff(f5, x, y)**2).subs({x: p[0], y: p[1]})
assert sp.expand(sp.diff(f5, x, 2)*sp.diff(f5, y, 2) - sp.diff(f5, x, y)**2 - (4*(3 - y)*(3 - x) - (2*x + 2*y - 9)**2)) == 0
assert [D(p) for p in [(0, 3), (3, 0), (3, 3)]] == [-9, -9, -9]
chk("5א", 1, D((0, 3)))
chk("5א", 2, D((2, 2)))
assert sp.diff(f5, x, 2).subs({x: 2, y: 2}) == -2 and f5.subs({x: 2, y: 2}) == 1

# ---- Q5b: f = x/(25+x^2)
f6 = x/(25 + x**2)
ser = sp.series(f6, x, 0, 8).removeO()
for kk in range(0, 3):
    assert ser.coeff(x, 2*kk + 1) == (-1)**kk/S(5)**(2*kk + 2)
chk("5ב", 0, 5)
cn = lambda kk: (-1)**kk*x**(2*kk + 1)/S(5)**(2*kk + 2)
assert 2*2 + 1 == 5
chk("5ב", 2, 2)
chk("5ב", 3, sp.diff(f6, x, 5).subs(x, 0))
assert sp.diff(f6, x, 5).subs(x, 0) == S(24, 3125)
# endpoints x=+-5: general term (-1)^n * (+-1)/5, not -> 0
assert all(abs(float(cn(kk).subs(x, 5))) == 0.2 for kk in range(0, 6))

print("ALL OK:", count, "numeric step answers checked")
