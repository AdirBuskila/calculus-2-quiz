# -*- coding: utf-8 -*-
"""sympy/numeric checks for the guided steps of 22A-B. Run: PYTHONUTF8=1 py -I tools/verify/22A-B/steps_22A-B.py
Every numeric answer is computed here independently and compared with tools/raw/22A-B.json; choice steps are
checked by showing each distractor fails."""
import json, pathlib, math
import numpy as np
import sympy as sp

HERE = pathlib.Path(__file__).resolve().parent
raw = json.loads((HERE.parents[1] / "raw" / "22A-B.json").read_text(encoding="utf-8"))
Q = {f"{q['num']}{q.get('part', '')}": q for q in raw["questions"]}
R = sp.Rational
ok = []


def chk(key, idx, val):
    s = Q[key]["steps"][idx]
    assert s["type"] == "numeric", (key, idx)
    assert abs(float(val) - s["answer"]) <= s.get("tol", 0) + 1e-12, (key, idx, float(val), s["answer"])
    ok.append((key, idx))


x, y, z, r, th, u, v, h, k = sp.symbols("x y z r theta u v h k", real=True)
n = sp.symbols("n", integer=True, positive=True)

# ---- Q1a ----
f = sp.log(x**2 + y**2 + z**2)
P = {x: 1, y: 2, z: 1}
g = [sp.diff(f, s).subs(P) for s in (x, y, z)]
assert g == [R(1, 3), R(2, 3), R(1, 3)]
chk("1א", 0, g[1])
nrm = sp.sqrt(sum(c**2 for c in g))
assert sp.simplify(nrm - sp.sqrt(6)/3) == 0
chk("1א", 2, nrm)
# choice: gradient gives max directional derivative; check by brute force over unit vectors
rng = np.random.default_rng(1)
V = rng.normal(size=(200000, 3)); V /= np.linalg.norm(V, axis=1)[:, None]
dd = V @ np.array([float(c) for c in g])
best = V[dd.argmax()]
assert np.allclose(best, np.array([1, 2, 1])/math.sqrt(6), atol=2e-2) and abs(dd.max() - float(nrm)) < 1e-3
for bad in ((-R(1, 3), -R(2, 3), -R(1, 3)), (R(2, 3), R(1, 3), R(1, 3)), (R(1, 3), R(1, 3), R(1, 3))):
    b = np.array([float(c) for c in bad]); b /= np.linalg.norm(b)
    assert abs(float(np.dot(b, [float(c) for c in g])) - float(nrm)) > 1e-3     # not the max direction

# ---- Q1b ----
Irad = sp.integrate(sp.sin(2 + r**2)*r, (r, 0, 3))
chk("1ב", 1, Irad)
tot = sp.pi*Irad
assert sp.simplify(tot - sp.pi/2*(sp.cos(2) - sp.cos(11))) == 0
chk("1ב", 2, tot)
# brute force of the original half-disc integral
G = np.linspace(-3, 3, 4001)
X, Y = np.meshgrid(G, G[G >= 0])
mask = X**2 + Y**2 <= 9
dA = (G[1] - G[0])**2
brute = (np.sin(2 + X**2 + Y**2)*mask).sum()*dA
assert abs(brute - float(tot)) < 5e-3
# distractor limits give other values
full = 2*math.pi*float(Irad); quarter = (math.pi/2)*float(Irad)
big = math.pi*float(sp.integrate(sp.sin(2 + r**2)*r, (r, 0, 9)))
assert all(abs(w - float(tot)) > 1e-3 for w in (full, quarter, big))

# ---- Q2a ----
a = lambda m: 1/(m - sp.log(m))**3
f1 = x - sp.log(x)
chk("2א", 1, sp.diff(f1, x).subs(x, 2))
assert all(sp.diff(f1, x).subs(x, t) > 0 for t in (2, 3, 5, 10))
terms = [1/(m - math.log(m))**3 for m in range(2, 4000)]
assert all(terms[i] > terms[i + 1] for i in range(len(terms) - 1)) and terms[-1] < 1e-8
chk("2א", 2, sp.summation(R(1, 2)**n, (n, 1, sp.oo)))
# ratio and root tests are inconclusive (limit 1) on the first series
m = sp.symbols("m", positive=True)
assert sp.limit(a(m + 1)/a(m), m, sp.oo) == 1
assert abs(float(a(10**6 + 1)/a(10**6)) - 1) < 1e-4
assert abs(float(abs(a(10**6))**(1/10**6)) - 1) < 1e-4
# second series: positive and bounded by (1/2)^n, partial sums converge below 1
tt = [(1 + math.cos(j))/2**(j + 1) for j in range(1, 200)]
assert all(t_ >= 0 for t_ in tt) and all(tt[j - 1] <= 0.5**j + 1e-15 for j in range(1, 200)) and sum(tt) < 1
# first series converges: alternating partial sums settle
ps = np.cumsum([(-1)**j/(j - math.log(j))**3 for j in range(2, 100001)])
assert abs(ps[-1] - ps[-2]) < 1e-12 and abs(ps[-1] - ps[50000]) < 1e-4

# ---- Q2b ----
F = lambda X_, Y_: (X_**3 + Y_**3)/(X_**2 + Y_**2)
hp = sp.symbols("hp", positive=True)
chk("2ב", 0, sp.limit(F(hp, 0)/hp, hp, 0))
chk("2ב", 1, sp.limit(F(0, hp)/hp, hp, 0))
quot = -(h*k**2 + k*h**2)/(h**2 + k**2)**sp.Rational(3, 2)
L = sp.limit(quot.subs({h: hp, k: hp}), hp, 0, "+")
chk("2ב", 2, L)
# the quotient equals the differentiability quotient with fx=fy=1
dq = (F(h, k) - h - k)/sp.sqrt(h**2 + k**2)
assert sp.simplify(dq - quot) == 0
# continuity: |r(cos^3+sin^3)| <= 2r
assert max(abs(math.cos(t)**3 + math.sin(t)**3) for t in np.linspace(0, 2*math.pi, 10001)) <= 2

# ---- Q3a ----
an = lambda m: m/((m**2 + 1)*3**m)
mm = sp.symbols("mm", positive=True)
Rr = 1/sp.limit(sp.simplify(an(mm + 1)/an(mm)), mm, sp.oo)
chk("3א", 0, Rr)
chk("3א", 1, sp.limit((mm/(mm**2 + 1))/(1/mm), mm, sp.oo))
p3 = np.cumsum([j/(j**2 + 1) for j in range(1, 400001)])
assert p3[-1] - p3[39999] > 2                                       # x=3: grows like ln n (diverges)
p3m = np.cumsum([(-1)**j*j/(j**2 + 1) for j in range(1, 400001)])
assert abs(p3m[-1] - p3m[-2]) < 1e-5 and abs(p3m[-1] - p3m[200000]) < 1e-5   # x=-3: converges
dec = [j/(j**2 + 1) for j in range(1, 2000)]
assert all(dec[i] >= dec[i + 1] for i in range(len(dec) - 1))
# x=-3 absolutely: terms j/(j^2+1) are the divergent series -> conditional only (above)

# ---- Q3b ----
Fz = z**3 - 3*x*y*z - 4
Pt = {x: 2, y: 1, z: -2}
assert Fz.subs(Pt) == 0
chk("3ב", 0, sp.diff(Fz, z).subs(Pt))
zx = -sp.diff(Fz, x)/sp.diff(Fz, z)
zy = -sp.diff(Fz, y)/sp.diff(Fz, z)
chk("3ב", 1, zx.subs(Pt))
chk("3ב", 2, zy.subs(Pt))
zxy = sp.diff(zx, y) + sp.diff(zx, z)*zy
chk("3ב", 3, zxy.subs(Pt))
# numerical cross-check: solve z(x,y) near -2 by Newton and take a central finite difference of z_x in y
def zsolve(X_, Y_):
    zz = -2.0
    for _ in range(60):
        zz -= (zz**3 - 3*X_*Y_*zz - 4)/(3*zz**2 - 3*X_*Y_)
    return zz
e = 1e-4
def zxn(Y_):
    return (zsolve(2 + e, Y_) - zsolve(2 - e, Y_))/(2*e)
zxy_num = (zxn(1 + 1e-3) - zxn(1 - 1e-3))/(2e-3)
assert abs(zxy_num - 1) < 1e-4, zxy_num

# ---- Q4a ----
M = sp.Matrix([[sp.diff(y - x, x), sp.diff(y - x, y)], [sp.diff(y + 2*x, x), sp.diff(y + 2*x, y)]])
chk("4א", 0, M.det())
# image of the four lines: u=y-x in {1,4}; v=y+2x in {6,8}; the other candidate ranges do not match
assert [(y - x).subs(y, 1 + x), (y - x).subs(y, 4 + x)] == [1, 4]
assert [(y + 2*x).subs(y, 6 - 2*x), (y + 2*x).subs(y, 8 - 2*x)] == [6, 8]
chk("4א", 2, sp.integrate(u, (u, 1, 4)))
val = R(1, 3)*sp.integrate(1/v, (v, 6, 8))*sp.integrate(u, (u, 1, 4))
assert sp.simplify(val - R(5, 2)*sp.log(R(4, 3))) == 0
chk("4א", 3, val)
Gx = np.linspace(0, 8, 8001)
X, Y = np.meshgrid(Gx, np.linspace(0, 12, 12001))
inD = (Y > 1 + X) & (Y < 4 + X) & (Y > 6 - 2*X) & (Y < 8 - 2*X)
brute = np.where(inD, (Y - X)/np.where(inD, 2*X + Y, 1), 0).sum()*(Gx[1]*(12/12000))
assert abs(brute - float(val)) < 5e-3, brute

# ---- Q4b ----
chk("4ב", 0, (0 - 1)**2 + (0 - 1)**2)
assert 2 > 1
f4 = 1 - x**2 - y**2
c = 1 - 1/sp.sqrt(2)
chk("4ב", 1, c)
chk("4ב", 2, f4.subs({x: c, y: c}))
chk("4ב", 3, f4.subs({x: 1 + 1/sp.sqrt(2), y: 1 + 1/sp.sqrt(2)}))
# dense-grid check on the closed disc (centre (1,1), radius 1)
Gd = np.linspace(0, 2, 4001)
Xd, Yd = np.meshgrid(Gd, Gd)
md = (Xd - 1)**2 + (Yd - 1)**2 <= 1 + 1e-12
fd = np.where(md, 1 - Xd**2 - Yd**2, np.nan)
assert abs(np.nanmax(fd) - 2*(math.sqrt(2) - 1)) < 1e-3 and abs(np.nanmin(fd) + 2*(math.sqrt(2) + 1)) < 1e-3

# ---- Q5a ----
S = sp.Sum((-1)**(n + 1)*x**(2*n - 1)/(2*n - 1), (n, 1, sp.oo))
q = sp.symbols("q")
d = sp.diff(sp.atan(x), x)
assert sp.simplify(d - 1/(1 + x**2)) == 0
chk("5א", 1, d.subs(x, 1))
# geometric ratio is -x^2
assert sp.simplify(sp.Sum((-x**2)**n, (n, 0, 40)).doit().subs(x, R(1, 2)) - 1/(1 + R(1, 4))) == sp.simplify(-(-R(1, 4))**41/(1 + R(1, 4)))
def part(xx, N):
    return sum((-1)**(j + 1)*xx**(2*j - 1)/(2*j - 1) for j in range(1, N))
xv = 0.7
val_ = part(xv, 400)
assert abs(val_ - math.atan(xv)) < 1e-9
for bad in (math.log(1 + xv), math.asin(xv), math.log(1 + xv**2)):
    assert abs(val_ - bad) > 1e-3
chk("5א", 3, sp.atan(1))
assert abs(part(1.0, 2000001) - math.pi/4) < 1e-5

# ---- Q5b ----
fb = x**3 + 8*y**3 - 6*x*y + 1
crit = sp.solve([sp.diff(fb, x), sp.diff(fb, y)], [x, y], dict=True)
real = {(c_[x], c_[y]) for c_ in crit if all(sp.im(t) == 0 for t in c_.values())}
assert real == {(0, 0), (1, R(1, 2))}
for bad in ((1, 2), (2, 2)):
    sub = {x: bad[0], y: bad[1]}
    assert (sp.diff(fb, x).subs(sub), sp.diff(fb, y).subs(sub)) != (0, 0)
H = sp.hessian(fb, (x, y))
Dd = lambda p_: H.subs({x: p_[0], y: p_[1]}).det()
chk("5ב", 1, Dd((0, 0)))
chk("5ב", 2, Dd((1, R(1, 2))))
assert H.subs({x: 1, y: R(1, 2)})[0, 0] > 0
loc = lambda p_: np.array([[float(fb.subs({x: p_[0] + a_, y: p_[1] + b_})) - float(fb.subs({x: p_[0], y: p_[1]})) for a_ in np.linspace(-0.05, 0.05, 41)] for b_ in np.linspace(-0.05, 0.05, 41)])
assert loc((1, 0.5)).min() >= -1e-12                                 # local min at B
assert loc((0, 0)).max() > 0 and loc((0, 0)).min() < 0               # saddle at A

print("22A-B steps OK:", len(ok), "numeric answers machine-checked")
