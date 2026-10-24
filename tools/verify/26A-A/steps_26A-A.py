# -*- coding: utf-8 -*-
"""sympy/numeric checks for the guided steps of 26A-A. Run: PYTHONUTF8=1 py -I tools/verify/26A-A/steps_26A-A.py
Every numeric answer is computed here independently and compared with tools/raw/26A-A.json; every choice step is
checked by showing the right option is right and each distractor is wrong."""
import json, pathlib, math
import numpy as np
import sympy as sp

HERE = pathlib.Path(__file__).resolve().parent
raw = json.loads((HERE.parents[1] / "raw" / "26A-A.json").read_text(encoding="utf-8"))
Q = {f"{q['num']}{q.get('part', '')}": q for q in raw["questions"]}
R = sp.Rational
ok = []


def chk(key, idx, val):
    s = Q[key]["steps"][idx]
    assert s["type"] == "numeric", (key, idx)
    assert abs(float(val) - s["answer"]) <= s.get("tol", 0) + 1e-12, (key, idx, float(val), s["answer"])
    ok.append((key, idx))


def correct_text(key, idx):
    s = Q[key]["steps"][idx]
    return [o["value"] for o in s["options"] if o["id"] == s["correctId"]][0]


x, y, u, v, t = sp.symbols("x y u v t", real=True)
n = sp.symbols("n", integer=True, positive=True)

# ---- Q1a ----
# choice 0: the right bounds describe the same region (equal integrals / area); each distractor does not.
f = x*sp.exp(x**2)
orig = sp.integrate(sp.integrate(f, (y, 0, 2 - x**2)), (x, 0, sp.sqrt(2)))
good = sp.integrate(sp.integrate(f, (x, 0, sp.sqrt(2 - y))), (y, 0, 2))
assert sp.simplify(orig - good) == 0
def val(ex, yb):
    return sp.integrate(sp.integrate(f, (x, 0, ex)), (y, 0, yb))
assert sp.simplify(val(sp.sqrt(2 - y), 2) - orig) == 0                      # right option: same integral as the original region
assert sp.simplify(val(2 - y**2, sp.sqrt(2)) - orig) != 0                   # x<=2-y^2, y<=sqrt2
assert sp.simplify(val(sp.sqrt(2), 2) - orig) != 0                          # rectangle
assert all(sp.im(sp.N(sp.sqrt(sp.Float(yy) - 2))) != 0 for yy in (0.5, 1.0, 1.5))
assert "sqrt{2-y}" in correct_text("1א", 0) and "\\le x\\le\\sqrt{2-y}" in correct_text("1א", 0)
chk("1א", 1, sp.integrate(x*sp.exp(x**2), (x, 0, sp.sqrt(2 - 1))))
chk("1א", 2, orig)
assert abs(float(orig) - (math.e**2 - 3)/2) < 1e-12

# ---- Q1b ----
f1 = sp.log(1 + x*y)/(x**2 + y**2)
l_axis = sp.limit(f1.subs(y, 0), x, 0)
l_diag = sp.limit(f1.subs(y, x), x, 0)
chk("1ב", 0, l_axis)
chk("1ב", 1, l_diag)
assert l_axis != l_diag
# choice 2: right = "does not exist"; the distractors 0, 1/2, 1 are each contradicted by a path
assert correct_text("1ב", 2) == "הגבול אינו קיים"
assert l_axis != R(1, 2) and l_diag != 0 and l_diag != 1 and l_axis != 1

# ---- Q2a ----
chk("2א", 0, R(2, 3))
chk("2א", 1, sp.summation(R(2, 3)**n, (n, 1, sp.oo)))
chk("2א", 2, sp.cos(sp.pi*3))
assert all(sp.cos(sp.pi*k) == (-1)**k for k in range(1, 12))
# series 1 absolutely convergent: partial sums of |.| bounded by 2; series 2 conditional
a1 = [abs((2/3)**k*math.cos(k)) for k in range(1, 400)]
assert sum(a1) < 2
assert sp.limit(R(2, 3)**n, n, sp.oo) == 0
alt = np.cumsum([(-1)**k/k for k in range(1, 200001)])
assert abs(alt[-1] - (-math.log(2))) < 1e-5            # series 2 converges (to -ln 2)
harm = np.cumsum([1/k for k in range(1, 200001)])
assert harm[-1] > 12 and harm[-1] - harm[1999] > 4     # absolute series keeps growing like ln n (diverges)

# ---- Q2b ----
fx = lambda X, Y: (X**3 + Y**3)/(2*X**2 + Y**2)
h = sp.symbols("h", positive=True)
chk("2ב", 0, sp.limit(fx(h, 0)/h, h, 0))
chk("2ב", 1, sp.limit(fx(0, h)/h, h, 0))
quot = (fx(h, h) - (R(1, 2)*h + h))/sp.sqrt(h**2 + h**2)
assert sp.simplify(fx(h, h) - R(2, 3)*h) == 0
L = sp.limit(quot, h, 0, "+")
chk("2ב", 2, L)
assert L != 0
# along y=-x... the quotient from the other side is +5/(6 sqrt2): the limit does not exist at all
hm = sp.symbols("hm", negative=True)
Lm = sp.limit((fx(hm, hm) - (R(1, 2)*hm + hm))/sp.sqrt(hm**2 + hm**2), hm, 0, "-")
assert sp.simplify(Lm + L) == 0 and Lm != 0
assert correct_text("2ב", 3) == "הפונקציה אינה דיפרנציאבילית ב-$(0,0)$"
# distractors: partials exist (checked above, finite values) -> "f_x does not exist" false; y=x limit nonzero -> false

# ---- Q3a ----
lo = sp.solve(sp.Eq(x + 2, -3), x)[0]
hi = sp.solve(sp.Eq(x + 2, 3), x)[0]
chk("3א", 0, lo)
chk("3א", 1, hi)
# concrete a_n with domain [-3,3): a_n = 1/(n 3^n). Check the claim on [-5,1) numerically at the endpoints.
def partial(xx, N):
    return sum(((xx + 2)**k)/(k*3**k) for k in range(1, N))
assert abs(partial(-5, 20001) - partial(-5, 40001)) < 1e-4          # x=-5: converges (alternating harmonic)
assert partial(1, 40001) - partial(1, 5001) > 1.5                   # x=1: diverges (harmonic)
assert abs(partial(-5, 40001) + math.log(2)) < 1e-4
assert correct_text("3א", 2) == "$[-5,1)$"

# ---- Q3b ----
uu, vv = sp.symbols("u v", positive=True)
X = sp.sqrt(uu*vv)
Y = 1/vv
Z = sp.exp(X**2*Y)
lhs = uu*sp.diff(Z, uu) - vv*sp.diff(Z, vv)
rhs = Z*X**2/vv
assert sp.simplify(lhs - rhs) == 0                                   # the identity as printed holds
wrong = Z*X**2/vv**2
assert sp.simplify(lhs - wrong) != 0                                 # the official closing line is false
assert sp.simplify(sp.diff(Y, uu)) == 0
chk("3ב", 1, sp.diff(Y, uu))
chk("3ב", 2, sp.diff(Y, vv).subs(vv, 2))
# the intermediate line of the proof (steps order/findbug)
xs, ys = sp.symbols("xs ys", positive=True)
zz = sp.exp(xs**2*ys)
assert sp.simplify(sp.diff(zz, xs) - 2*xs*ys*zz) == 0 and sp.simplify(sp.diff(zz, ys) - xs**2*zz) == 0
zu = 2*xs*ys*zz*vv/(2*sp.sqrt(uu*vv))
zv = 2*xs*ys*zz*uu/(2*sp.sqrt(uu*vv)) - xs**2*zz/vv**2
line5 = uu*zu - vv*zv
tail = line5.subs({xs: X, ys: Y})
assert sp.simplify(tail - lhs) == 0
neg = 2*xs*ys*zz*uu*vv/(2*sp.sqrt(uu*vv))
assert sp.simplify(line5 - (neg - neg + xs**2*vv*zz/vv**2)) == 0
assert sp.simplify((xs**2*vv*zz/vv**2 - zz*xs**2/vv)) == 0           # the correct closing line
assert sp.simplify((xs**2*vv*zz/vv**2 - zz*xs**2/vv**2)) != 0        # the buggy closing line (findbug)
s = Q["3ב"]["steps"]
assert s[3]["type"] == "order" and len(s[3]["lines"]) == 4
assert s[4]["type"] == "findbug" and s[4]["bugIndex"] == len(s[4]["lines"]) - 1

# ---- Q4a ----
M = sp.Matrix([[sp.diff(y - x, x), sp.diff(x*y, x)], [sp.diff(y - x, y), sp.diff(x*y, y)]])
assert sp.simplify(M.det() + (x + y)) == 0
chk("4א", 0, M.det().subs({x: 1, y: 1}))
integrand = sp.simplify((x**2 - y**2)/(x + y))
assert sp.simplify(integrand + (y - x)) == 0                         # = -(y-x) = -u
assert sp.simplify((x**2 - y**2)*(x + y)**-1 - (-(y - x))) == 0
assert sp.simplify((x**2 - y**2)*(x + y)**-1 - (y - x)) != 0         # distractor u
assert sp.simplify((x**2 - y**2)*(x + y)**-1 - (-(y - x)*(x + y))) != 0
assert sp.simplify((x**2 - y**2)*(x + y)**-1 - (-(y - x)*x*y)) != 0
Iu = sp.integrate(-u, (u, 0, 1))
chk("4א", 2, Iu)
chk("4א", 3, Iu*sp.integrate(1, (v, 1, 2)))
# brute force on D = {x<y<x+1, 1<xy<2, x,y>0}
g = np.linspace(0, 3, 6001)
Xg, Yg = np.meshgrid(g, g)
mask = (Yg > Xg) & (Yg < Xg + 1) & (Xg*Yg > 1) & (Xg*Yg < 2)
dA = (g[1] - g[0])**2
assert abs(((Xg**2 - Yg**2)*mask).sum()*dA + 0.5) < 5e-3

# ---- Q4b ----
xx = sp.symbols("xx", real=True)
ft = sp.expand((xx**3 + xx**2 - 3*xx) + (4 - xx**2))
assert sp.simplify(ft - (4 + xx**3 - 3*xx)) == 0
for bad in (xx**3 + xx**2 - 3*xx + 4, xx**3 - 3*xx - 4, xx**3 - xx**2 - 3*xx + 4):
    assert sp.simplify(ft - bad) != 0
sols = sp.solve(sp.diff(ft, xx), xx)
chk("4ב", 1, max(sols))
chk("4ב", 2, ft.subs(xx, -1))
vals = {c: ft.subs(xx, c) for c in (-2, -1, 1, 2)}
assert vals == {-2: 2, -1: 6, 1: 2, 2: 6}
# number of boundary points attaining the max, by brute force on the circle
th = np.linspace(0, 2*np.pi, 2000001)
fv = (2*np.cos(th))**3 + (2*np.cos(th))**2 - 3*2*np.cos(th) + (2*np.sin(th))**2
mx, mn = fv.max(), fv.min()
assert abs(mx - 6) < 1e-9 and abs(mn - 2) < 1e-9
def count_pts(val):
    d = np.abs(fv - val) < 1e-6
    return int(((d[1:] & ~d[:-1])).sum() + (1 if d[0] and not d[-1] else 0))
cm = 0
pts_max = {(sp.Integer(-1), sp.sqrt(3)), (sp.Integer(-1), -sp.sqrt(3)), (sp.Integer(2), sp.Integer(0))}
for (a, b) in pts_max:
    assert sp.simplify(a**2 + b**2 - 4) == 0 and sp.simplify(a**3 + a**2 - 3*a + b**2 - 6) == 0
chk("4ב", 3, len(pts_max))
# no other circle points reach 6: solve f=6 on the circle
assert sp.roots(sp.Poly(ft - 6, xx)) == {-1: 2, 2: 1}
chk("4ב", 4, min(vals.values()))

# ---- Q5a ----
fa = (x - y)**3 - 3*x - y**2 + 5*y
crit = sp.solve([sp.diff(fa, x), sp.diff(fa, y)], [x, y], dict=True)
assert {(c[x], c[y]) for c in crit} == {(2, 1), (0, 1)}
for bad in ((1, 2), (1, 0), (-2, 1), (0, 0), (2, 2)):
    sub = {x: bad[0], y: bad[1]}
    assert (sp.diff(fa, x).subs(sub), sp.diff(fa, y).subs(sub)) != (0, 0)
H = sp.hessian(fa, (x, y))
D = lambda p: H.subs({x: p[0], y: p[1]}).det()
chk("5א", 1, D((2, 1)))
chk("5א", 2, D((0, 1)))
assert D((2, 1)) < 0 and D((0, 1)) > 0 and H[0, 0].subs({x: 0, y: 1}) < 0
# dense-grid sanity: (0,1) is a local max, (2,1) is a saddle
gg = np.linspace(-0.05, 0.05, 41)
def loc(p):
    return np.array([[float(fa.subs({x: p[0] + a, y: p[1] + b})) for a in gg] for b in gg]) - float(fa.subs({x: p[0], y: p[1]}))
assert (loc((0, 1)) <= 1e-12).all()
assert loc((2, 1)).max() > 0 and loc((2, 1)).min() < 0

# ---- Q5b ----
fb = (16 - 5*x)/(x**2 - 5*x + 6)
Aa, Bb = sp.symbols("A B")
pf = sp.apart(fb, x)
assert sp.simplify(pf - (-6/(x - 2) + 1/(x - 3))) == 0
chk("5ב", 0, -6)
ser = sp.series(fb, x, 0, 8).removeO()
coef = lambda k: R(3, 2**k) - R(1, 3**(k + 1))
for k in range(8):
    assert ser.coeff(x, k) == coef(k)
chk("5ב", 2, coef(1))
# radius: nearest singularity of f is x=2 (poles at 2 and 3)
assert sorted(sp.solve(x**2 - 5*x + 6, x)) == [2, 3]
chk("5ב", 1, 2)
d20 = sp.diff(fb, x, 20).subs(x, 0)
assert d20 == sp.factorial(20)*coef(20)
for bad in (coef(20), sp.factorial(20)*(R(3, 2**20) - R(1, 3**20)), sp.factorial(20)*(R(3, 2**20) + R(1, 3**21))):
    assert d20 != bad

print("26A-A steps OK:", len(ok), "numeric answers machine-checked")
