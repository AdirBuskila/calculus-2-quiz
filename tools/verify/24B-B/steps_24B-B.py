# -*- coding: utf-8 -*-
"""sympy/numeric checks for the guided steps of 24B-B. Run: PYTHONUTF8=1 py -I tools/verify/24B-B/steps_24B-B.py
Checks every numeric step answer against the stored raw JSON (run gen_24B-B.py first)."""
import json, pathlib, math
import sympy as sp

HERE = pathlib.Path(__file__).resolve().parent
raw = json.loads((HERE.parents[1] / "raw" / "24B-B.json").read_text(encoding="utf-8"))
Q = {f"{q['num']}{q.get('part','')}": q for q in raw["questions"]}
S = sp.Rational
count = 0


def chk(key, idx, val):
    global count
    s = Q[key]["steps"][idx]
    assert s["type"] == "numeric", (key, idx, s["type"])
    assert abs(float(val) - s["answer"]) <= s.get("tol", 0) + 1e-12, (key, idx, float(val), s["answer"])
    count += 1


x, y = sp.symbols("x y", real=True)
n = sp.symbols("n", positive=True, integer=True)

# ---- Q1: f = x^3 y/(x^2+y^2)
f = x**3*y/(x**2 + y**2)
fx, fy = sp.diff(f, x), sp.diff(f, y)
num_fy = x**3*(x**2 + y**2) - 2*y**2*x**3
assert sp.simplify(fy - num_fy/(x**2 + y**2)**2) == 0
chk("1א", 0, num_fy.subs({x: 1, y: 0}))
chk("1א", 1, fy.subs({x: 1, y: 0}))
chk("1א", 2, fx.subs({x: 1, y: 0}))
h = sp.symbols("h", real=True, nonzero=True)
chk("1ב", 1, sp.simplify(f.subs({x: h, y: 0})))
chk("1ב", 2, sp.limit(sp.simplify(f.subs({x: h, y: 0}))/h, h, 0))
chk("1ב", 3, sp.limit(sp.simplify(f.subs({x: 0, y: h}))/h, h, 0))
r, ph = sp.symbols("r phi", positive=True)
quo = sp.simplify((f/sp.sqrt(x**2 + y**2)).subs({x: r*sp.cos(ph), y: r*sp.sin(ph)}))
assert sp.simplify(quo - r*sp.cos(ph)**3*sp.sin(ph)) == 0
chk("1ג", 0, 1)   # exponent of r
chk("1ג", 1, sp.limit(r*sp.cos(ph)**3*sp.sin(ph), r, 0))
# brute force: |quotient| <= r on a grid of angles
assert all(abs(float(quo.subs({r: 1e-3, ph: t}))) <= 1e-3 + 1e-15 for t in [i*0.1 for i in range(63)])

# ---- Q2a
a = sp.cos(sp.pi*n)*(n**2 + 3*sp.log(n))/((n + 1)*(n + 2))
chk("2א", 0, sp.limit(sp.log(n)/n, n, sp.oo))
chk("2א", 1, sp.limit((n**2 + 3*sp.log(n))/((n + 1)*(n + 2)), n, sp.oo))
assert abs(float(a.subs(n, 10**6))) > 0.99   # terms stay near +-1: series diverges
# ---- Q2b
b = (1 + 1/sp.sqrt(n))/n**3
chk("2ב", 0, max(float(b.subs(n, k))*k**3 for k in range(1, 10000)))
assert all((1 + 1/math.sqrt(k))/k**3 <= 2/k**3 for k in range(1, 10000))
chk("2ב", 1, 3)
assert sp.Sum(1/n**3, (n, 1, sp.oo)).is_convergent()

# ---- Q3
f3 = x**2 - 2*x*(y + 1) + 3
g3 = sp.Matrix([sp.diff(f3, x), sp.diff(f3, y)])
chk("3א", 0, g3[0].subs({x: 2, y: -1}))
chk("3א", 1, g3[1].subs({x: 2, y: -1}))
gp = g3.subs({x: 2, y: -1})
assert gp.dot(sp.Matrix([1, 1])) == 0 and gp.dot(sp.Matrix([4, 4])) == 0 and gp.dot(sp.Matrix([-4, 4])) < 0
a_ = sp.Matrix([-3, 4])
chk("3ב", 0, a_.norm())
chk("3ב", 1, gp.dot(a_))
chk("3ב", 2, gp.dot(a_)/a_.norm())
sol = sp.solve([sp.diff(f3, x), sp.diff(f3, y)], [x, y], dict=True)
assert sol == [{x: 0, y: -1}], sol
chk("3ג", 0, sol[0][y])
A, B, C = sp.diff(f3, x, 2), sp.diff(f3, x, y), sp.diff(f3, y, 2)
D3 = (A*C - B**2).subs(sol[0])
assert D3 < 0
chk("3ג", 1, D3)
chk("3ד", 0, f3.subs({x: 0, y: -1}))
gx = f3.subs(y, -2)
chk("3ד", 1, sp.solve(sp.diff(gx, x), x)[0])
hx = f3.subs(y, x)
chk("3ד", 2, hx.subs(x, -1))
pts = {"A": (1, 1), "B": (1, -2), "C": (-2, -2), "D": (-1, -2), "E": (-1, -1), "I": (0, -1)}
vals = {k: f3.subs({x: p[0], y: p[1]}) for k, p in pts.items()}
assert vals == {"A": 0, "B": 6, "C": 3, "D": 2, "E": 4, "I": 3}, vals
chk("3ד", 3, max(vals.values()))
chk("3ד", 4, min(vals.values()))
# dense-grid check of the extrema over D = {-2 <= y <= x <= 1}
import numpy as np
g = np.linspace(-2, 1, 1201)
X, Y = np.meshgrid(g, g)
m = (Y >= -2) & (Y <= X) & (X <= 1)
F = X**2 - 2*X*(Y + 1) + 3
assert abs(F[m].max() - 6) < 1e-9 and abs(F[m].min() - 0) < 1e-9

# ---- Q4a
u, v = sp.symbols("u v")
zz = 2*u*v + 3*v**2
uu = sp.cos(x - 3*y)
pt = {x: sp.pi, y: -sp.pi}
chk("4א", 0, uu.subs(pt))
chk("4א", 1, sp.diff(zz, v).subs({u: 1, v: 2}))
ux, uy = sp.diff(uu, x).subs(pt), sp.diff(uu, y).subs(pt)
assert ux == 0 and uy == 0
chk("4א", 2, sp.diff(zz, u).subs({u: 1, v: 2})*ux + sp.diff(zz, v).subs({u: 1, v: 2})*5)
chk("4א", 3, sp.diff(zz, u).subs({u: 1, v: 2})*uy + sp.diff(zz, v).subs({u: 1, v: 2})*4)

# ---- Q4b (corrected): sum 2^n/sqrt(n+4) (x-1)^n
an = 2**n/sp.sqrt(n + 4)
Rinv = sp.limit(an.subs(n, n + 1)/an, n, sp.oo)
assert Rinv == 2
chk("4ב", 0, 1/Rinv)
chk("4ב", 1, 1 - 1/Rinv)
# x=1/2: alternating, terms decrease to 0 (Leibniz) -> converges; absolute series 1/sqrt(n+4) diverges
c = lambda k: 1/math.sqrt(k + 4)
assert all(c(k + 1) < c(k) for k in range(1, 5000)) and c(10**8) < 1e-4
assert sp.limit((1/sp.sqrt(n + 4))/(1/sp.sqrt(n)), n, sp.oo) == 1
s1, s2 = sum(c(k) for k in range(1, 10**5)), sum(c(k) for k in range(1, 4*10**5))
assert s2 - s1 > 500                    # partial sums at x=3/2 keep growing like 2 sqrt(N): divergence
alt = lambda N: sum((-1)**k*c(k) for k in range(1, N))
assert abs(alt(10**5) - alt(10**5 + 1)) < 1e-2 and abs(alt(10**5) - alt(2*10**5)) < 5e-3   # x=1/2 settles

# ---- Q5
f5 = sp.log(6*x**2 + 5*x + 1)
assert sp.expand((3*x + 1)*(2*x + 1)) == 6*x**2 + 5*x + 1
assert sp.expand((6*x + 1)*(x + 1)) != 6*x**2 + 5*x + 1 and sp.expand((3*x + 2)*(2*x + 1)) != 6*x**2 + 5*x + 1
ser = sp.series(f5, x, 0, 7).removeO()
coef = lambda k: (-1)**(k + 1)*(3**k + 2**k)/S(k)
for k in range(1, 7):
    assert ser.coeff(x, k) == coef(k), k
chk("5א", 1, coef(1))
chk("5א", 2, coef(2))
chk("5א", 3, coef(3))
chk("5ב", 0, sp.limit((1 + (S(2)/3)**n)**(1/n), n, sp.oo))
chk("5ב", 1, S(1, 3))
assert sp.limit(((3**n + 2**n)/n)**(1/n), n, sp.oo) == 3
# endpoints: x=1/3 converges (alternating), x=-1/3 diverges (terms -(1+(2/3)^n)/n)
t = lambda k, xx: coef(k)*xx**k
pos = lambda N: sum(float(t(k, S(1, 3))) for k in range(1, N))
neg = lambda N: sum(float(t(k, -S(1, 3))) for k in range(1, N))
assert abs(pos(4000) - pos(8000)) < 1e-3 and neg(8000) - neg(4000) < -0.6
chk("5ג", 0, 3**5 + 2**5)
chk("5ג", 1, coef(5))
chk("5ג", 2, sp.diff(f5, x, 5).subs(x, 0))

print("ALL OK:", count, "numeric step answers checked")
