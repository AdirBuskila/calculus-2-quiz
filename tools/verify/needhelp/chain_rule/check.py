# -*- coding: utf-8 -*-
"""sympy checks for the guided course `chain_rule` (calculus-2, topic chain_rule_identity).

Run:  PYTHONUTF8=1 py -I tools/verify/needhelp/chain_rule/check.py

Loads the level files courses/chain_rule/C0N.js (through tools/course_load.js) and asserts, with sympy:
  * every own multiple-choice question: the stored option texts are EXACTLY the ones listed here, exactly one of them is
    mathematically true, and it is the stored correctId (option content only, never position);
  * every numeric step: the stored answer equals the sympy value (within the stored tolerance);
  * every findbug step: all lines except the stored bugIndex are true statements about the function, and that line is false;
  * every order step: each line is a true statement, in the stored (correct) order;
  * every identity is checked for an ARBITRARY g: the same claim is tested with several different g
    (sin, exp, a cubic, atan) and for f(u,v) with several different f.
All question ids of the course must be covered (coverage assertion at the end).
"""
import json, pathlib, random, subprocess, sys
import sympy as sp

ROOT = pathlib.Path(__file__).resolve().parents[4]
COURSE = "chain_rule"
rng = random.Random(20261025)

# ---- load the level files ---------------------------------------------------------------------------------------
raw = subprocess.run(["node", str(ROOT / "tools" / "course_load.js")], capture_output=True, check=True, cwd=str(ROOT)).stdout
loaded = json.loads(raw.decode("utf-8"))
assert not loaded["errors"], loaded["errors"]
LEVELS = sorted([e["level"] for e in loaded["levels"] if e["courseId"] == COURSE], key=lambda L: L["order"])
Q = {}
for L in LEVELS:
    for q in L["questions"]:
        if "bankId" not in q:
            assert q["id"] not in Q, q["id"]
            Q[q["id"]] = q
covered = set()

X, Y, Z = sp.symbols("x y z", positive=True)
U, V = sp.symbols("u v", positive=True)
K = sp.Symbol("k", positive=True)
S, T = sp.symbols("s t", positive=True)
P, R = sp.symbols("p r", positive=True)   # u, v of the C06-Q6 example (kept apart from the generic U, V)


def iszero(e, syms=(X, Y, Z, K), n=7):
    """numeric zero test of an explicit expression at n random points in [0.6, 1.8]^d"""
    f = sp.lambdify(list(syms), e, "math")
    for _ in range(n):
        vals = [rng.uniform(0.6, 1.8) for _ in syms]
        if abs(f(*vals)) > 1e-8 * (1 + abs(f(*vals))):
            return False
    return True


# a few concrete g (with g' and g''): an identity must hold for ALL of them
GS = [
    (sp.sin, sp.cos, lambda a: -sp.sin(a)),
    (sp.exp, sp.exp, sp.exp),
    (lambda a: a**3 + a, lambda a: 3*a**2 + 1, lambda a: 6*a),
    (sp.atan, lambda a: 1/(1 + a**2), lambda a: -2*a/(1 + a**2)**2),
]


def forall_g(fn):
    """fn(g, g1, g2) -> expression that should vanish identically; True iff it does for every test g"""
    return all(iszero(fn(*G)) for G in GS)


def mkF(expr):
    return (sp.Lambda((U, V), expr), sp.Lambda((U, V), sp.diff(expr, U)), sp.Lambda((U, V), sp.diff(expr, V)))


FS = [mkF(U**2*V), mkF(sp.sin(U) + V**2), mkF(sp.exp(U*V)), mkF(U*V**2 + U**3)]


def forall_f(fn):
    return all(iszero(fn(*F)) for F in FS)


def norm(s):
    return s.strip().strip("$").replace(" ", "")


def mcq(qid, items):
    """items: [(tex without the outer $, bool is_true)]. Stored options must be exactly these, one true, = correctId."""
    q = Q[qid]
    stored = {norm(o["value"]): o["id"] for o in q["options"]}
    assert len(stored) == len(q["options"]), (qid, "duplicate option text")
    assert set(stored) == {norm(t) for t, _ in items}, (qid, sorted(stored), sorted(norm(t) for t, _ in items))
    trues = [norm(t) for t, b in items if b]
    assert len(trues) == 1, (qid, "number of true options:", trues)
    assert stored[trues[0]] == q["correctId"], (qid, "correctId mismatch")
    covered.add(qid)


def numeric(qid, value):
    st = Q[qid]["step"]
    assert st["type"] == "numeric", qid
    assert abs(float(value) - st["answer"]) <= st.get("tol", 0) + 1e-12, (qid, float(value), st["answer"])
    covered.add(qid)


def lines_claims(qid, kind, claims):
    """findbug / order: claims = one bool per stored line (is the line a TRUE statement?)."""
    st = Q[qid]["step"]
    assert st["type"] == kind, qid
    assert len(st["lines"]) == len(claims), (qid, len(st["lines"]), len(claims))
    if kind == "findbug":
        expected = [i != st["bugIndex"] for i in range(len(claims))]
        assert list(claims) == expected, (qid, claims, "bugIndex", st["bugIndex"])
    else:
        assert all(claims), (qid, claims)
    covered.add(qid)


def mc_g(qid, truth, options):
    """options: [(tex, claim(g, g1, g2))]; truth(g) -> sympy expression. True iff equal for every test g."""
    mcq(qid, [(tex, forall_g(lambda g, g1, g2, c=c: truth(g) - c(g, g1, g2))) for tex, c in options])


def mc_f(qid, truth, options):
    mcq(qid, [(tex, forall_f(lambda f, fu, fv, c=c: truth(f) - c(f, fu, fv))) for tex, c in options])


# =================================================================================================================
# C01  dependency tree, inner derivatives
# =================================================================================================================
t_ = X**2 - Y**2
mcq("C01-Q1", [(r"-2y", sp.simplify(sp.diff(t_, Y) + 2*Y) == 0), (r"2y", sp.simplify(sp.diff(t_, Y) - 2*Y) == 0),
               (r"-2y^2", sp.simplify(sp.diff(t_, Y) + 2*Y**2) == 0), (r"-2x", sp.simplify(sp.diff(t_, Y) + 2*X) == 0)])

# routes from z to y in z = y/(3x) + g(xy): the direct one (the free term) and the one through t; both contribute
# to z_y and nothing else does (z_y = direct + g'(t) * t_y exactly, for every test g)
for g, g1, g2 in GS:
    direct = sp.diff(Y/(3*X), Y)
    via_t = sp.diff(g(X*Y), Y)
    assert direct != 0 and via_t != 0
    assert iszero(sp.diff(Y/(3*X) + g(X*Y), Y) - (direct + g1(X*Y)*X))
mcq("C01-Q2", [(r"2", True), (r"1", False), (r"3", False), (r"0", False)])

numeric("C01-Q3", sp.diff(X*Y**2, Y).subs({X: 2, Y: 3}))

t_ = X/Y
mcq("C01-Q4", [(r"-\dfrac{x}{y^2}", sp.simplify(sp.diff(t_, Y) + X/Y**2) == 0), (r"\dfrac1y", sp.simplify(sp.diff(t_, Y) - 1/Y) == 0),
               (r"-\dfrac1y", sp.simplify(sp.diff(t_, Y) + 1/Y) == 0), (r"\dfrac{x}{y^2}", sp.simplify(sp.diff(t_, Y) - X/Y**2) == 0)])
assert sp.simplify(sp.diff(t_, X) - 1/Y) == 0        # the "1/y" distractor really is t_x

t_ = sp.cos(X - Y)
mcq("C01-Q5", [(r"\sin(x-y)", sp.simplify(sp.diff(t_, Y) - sp.sin(X - Y)) == 0), (r"-\sin(x-y)", sp.simplify(sp.diff(t_, Y) + sp.sin(X - Y)) == 0),
               (r"\cos(x-y)", sp.simplify(sp.diff(t_, Y) - sp.cos(X - Y)) == 0), (r"-\cos(x-y)", sp.simplify(sp.diff(t_, Y) + sp.cos(X - Y)) == 0)])
assert sp.simplify(sp.diff(t_, X) + sp.sin(X - Y)) == 0   # the -sin(x-y) distractor is t_x

# =================================================================================================================
# C02  one intermediate variable
# =================================================================================================================
mc_g("C02-Q1", lambda g: sp.diff(g(X**2 + Y**2), X), [
    (r"2x\,g'(x^2+y^2)", lambda g, g1, g2: 2*X*g1(X**2 + Y**2)),
    (r"g'(2x)", lambda g, g1, g2: g1(2*X)),
    (r"2x\,g(x^2+y^2)", lambda g, g1, g2: 2*X*g(X**2 + Y**2)),
    (r"g'(x^2+y^2)", lambda g, g1, g2: g1(X**2 + Y**2))])

numeric("C02-Q2", sp.diff((X*Y)**3, X).subs({X: 1, Y: 2}))
assert sp.diff((X*Y)**3, X).subs({X: 1, Y: 2}) == 3*(1*2)**2*2     # = g'(t) t_x with g = t^3

xy = X/Y
mc_g("C02-Q3", lambda g: sp.diff(g(X/Y), Y), [
    (r"-\dfrac{x}{y^2}\,g'\!\left(\dfrac xy\right)", lambda g, g1, g2: -X/Y**2*g1(X/Y)),
    (r"\dfrac1y\,g'\!\left(\dfrac xy\right)", lambda g, g1, g2: g1(X/Y)/Y),
    (r"-\dfrac{x}{y^2}\,g\!\left(\dfrac xy\right)", lambda g, g1, g2: -X/Y**2*g(X/Y)),
    (r"-\dfrac{x}{y^2}\,g'\!\left(-\dfrac{x}{y^2}\right)", lambda g, g1, g2: -X/Y**2*g1(-X/Y**2))])

# findbug: z = g(x^2 y)
t_ = X**2*Y
zx = lambda g: sp.diff(g(t_), X)
zy = lambda g: sp.diff(g(t_), Y)
lines_claims("C02-Q4", "findbug", [
    True,
    sp.simplify(sp.diff(t_, X) - 2*X*Y) == 0 and sp.simplify(sp.diff(t_, Y) - X**2) == 0,
    forall_g(lambda g, g1, g2: zx(g) - g1(t_)*2*X*Y),
    forall_g(lambda g, g1, g2: zy(g) - g1(t_)*2*X*Y)])
assert forall_g(lambda g, g1, g2: zy(g) - g1(t_)*X**2)      # the corrected line

numeric("C02-Q5", sp.diff((X**2 - 3*Y)**2, Y).subs({X: 2, Y: 1}))

# C02-Q6: z_x t_y = z_y t_x always; the others fail for some t
def stmt_holds(fn):
    for tt in (X*Y, X**2 - Y**2, X/Y, sp.cos(X - Y)):
        for g, g1, g2 in GS:
            z = g(tt)
            if not iszero(fn(sp.diff(z, X), sp.diff(z, Y), sp.diff(tt, X), sp.diff(tt, Y), g1(tt))):
                return False
    return True
mcq("C02-Q6", [(r"z_x\,t_y=z_y\,t_x", stmt_holds(lambda zx_, zy_, tx, ty, g1t: zx_*ty - zy_*tx)),
               (r"z_x\,t_x=z_y\,t_y", stmt_holds(lambda zx_, zy_, tx, ty, g1t: zx_*tx - zy_*ty)),
               (r"z_x=z_y", stmt_holds(lambda zx_, zy_, tx, ty, g1t: zx_ - zy_)),
               (r"z_x+z_y=g'(t)", stmt_holds(lambda zx_, zy_, tx, ty, g1t: zx_ + zy_ - g1t))])

# =================================================================================================================
# C03  free factor / free term
# =================================================================================================================
t_ = X**2 - Y**2
mc_g("C03-Q1", lambda g: sp.diff(Y*g(t_), Y), [
    (r"g(t)-2y^2\,g'(t)", lambda g, g1, g2: g(t_) - 2*Y**2*g1(t_)),
    (r"-2y^2\,g'(t)", lambda g, g1, g2: -2*Y**2*g1(t_)),
    (r"g(t)+2y^2\,g'(t)", lambda g, g1, g2: g(t_) + 2*Y**2*g1(t_)),
    (r"g(t)-2y\,g'(t)", lambda g, g1, g2: g(t_) - 2*Y*g1(t_))])
mc_g("C03-Q2", lambda g: sp.diff(Y*g(t_), X), [
    (r"2xy\,g'(t)", lambda g, g1, g2: 2*X*Y*g1(t_)),
    (r"g(t)+2xy\,g'(t)", lambda g, g1, g2: g(t_) + 2*X*Y*g1(t_)),
    (r"2x\,g'(t)", lambda g, g1, g2: 2*X*g1(t_)),
    (r"2xy\,g(t)", lambda g, g1, g2: 2*X*Y*g(t_))])

numeric("C03-Q3", sp.diff(X*(X*Y)**2, X).subs({X: 1, Y: 2}))

t_ = X*Y
zx = lambda g: sp.diff(X*g(t_), X)
zy = lambda g: sp.diff(X*g(t_), Y)
lines_claims("C03-Q4", "findbug", [
    True,
    forall_g(lambda g, g1, g2: zx(g) - X*g1(t_)*Y),
    forall_g(lambda g, g1, g2: zy(g) - X**2*g1(t_)),
    forall_g(lambda g, g1, g2: X*zx(g) - Y*zy(g) - X*g(t_)) and forall_g(lambda g, g1, g2: X*zx(g) - Y*zy(g) - X*g(t_))])
assert forall_g(lambda g, g1, g2: zx(g) - (g(t_) + X*g1(t_)*Y))     # the corrected line

mc_g("C03-Q5", lambda g: X*zx(g) - Y*zy(g), [
    (r"z", lambda g, g1, g2: X*g(t_)),
    (r"0", lambda g, g1, g2: 0*X),
    (r"2z", lambda g, g1, g2: 2*X*g(t_)),
    (r"x\,g'(xy)", lambda g, g1, g2: X*g1(t_))])

zz = Y/(3*X) + (X*Y)**2
numeric("C03-Q6", sp.diff(zz, Y).subs({X: 1, Y: 1}))
assert sp.diff(zz, Y).subs({X: 1, Y: 1}) == sp.Rational(7, 3)

# =================================================================================================================
# C04  plugging into the identity
# =================================================================================================================
# Q1 (order): z = x^2 g(y/x), x z_x + y z_y = 2 z
t_ = Y/X
zf = lambda g: X**2*g(t_)
zx = lambda g: sp.diff(zf(g), X)
zy = lambda g: sp.diff(zf(g), Y)
claims = [
    sp.simplify(sp.diff(t_, X) + Y/X**2) == 0 and sp.simplify(sp.diff(t_, Y) - 1/X) == 0,
    forall_g(lambda g, g1, g2: zx(g) - (2*X*g(t_) - Y*g1(t_))) and forall_g(lambda g, g1, g2: zy(g) - X*g1(t_)),
    forall_g(lambda g, g1, g2: X*zx(g) + Y*zy(g) - (2*X**2*g(t_) - X*Y*g1(t_) + X*Y*g1(t_))),
    forall_g(lambda g, g1, g2: 2*X**2*g(t_) - 2*zf(g)) and forall_g(lambda g, g1, g2: X*zx(g) + Y*zy(g) - 2*zf(g))]
lines_claims("C04-Q1", "order", claims)

t_ = X**2 + Y**2
zx = lambda g: sp.diff(g(t_), X)
zy = lambda g: sp.diff(g(t_), Y)
mcq("C04-Q2", [(r"y\,z_x-x\,z_y=0", forall_g(lambda g, g1, g2: Y*zx(g) - X*zy(g))),
               (r"x\,z_x+y\,z_y=0", forall_g(lambda g, g1, g2: X*zx(g) + Y*zy(g))),
               (r"x\,z_x-y\,z_y=0", forall_g(lambda g, g1, g2: X*zx(g) - Y*zy(g))),
               (r"y\,z_x+x\,z_y=0", forall_g(lambda g, g1, g2: Y*zx(g) + X*zy(g)))])

lines_claims("C04-Q3", "findbug", [
    sp.simplify(sp.diff(t_, X) - 2*X) == 0 and sp.simplify(sp.diff(t_, Y) - 2*Y) == 0,
    forall_g(lambda g, g1, g2: zx(g) - 2*X*g1(t_)) and forall_g(lambda g, g1, g2: zy(g) - 2*Y*g(t_)),
    forall_g(lambda g, g1, g2: Y*zx(g) - X*zy(g) - (2*X*Y*g1(t_) - 2*X*Y*g1(t_))),
    forall_g(lambda g, g1, g2: Y*zx(g) - X*zy(g))])
assert forall_g(lambda g, g1, g2: zy(g) - 2*Y*g1(t_))

# Q4: z = x^3 g(y/x^2): x z_x + 2 y z_y = k z  -> k = 3
t_ = Y/X**2
zf = lambda g: X**3*g(t_)
for kk in (3, 2, 4):
    holds = forall_g(lambda g, g1, g2: X*sp.diff(zf(g), X) + 2*Y*sp.diff(zf(g), Y) - kk*zf(g))
    assert holds == (kk == 3), kk
numeric("C04-Q4", 3)

# =================================================================================================================
# C05  second derivatives
# =================================================================================================================
t_ = X**2 + Y**2
mc_g("C05-Q1", lambda g: sp.diff(g(t_), X, 2), [
    (r"4x^2\,g''(t)+2\,g'(t)", lambda g, g1, g2: 4*X**2*g2(t_) + 2*g1(t_)),
    (r"4x^2\,g''(t)", lambda g, g1, g2: 4*X**2*g2(t_)),
    (r"2x\,g''(t)+2\,g'(t)", lambda g, g1, g2: 2*X*g2(t_) + 2*g1(t_)),
    (r"2\,g''(t)", lambda g, g1, g2: 2*g2(t_))])

numeric("C05-Q2", sp.diff((X*Y)**3, X, Y).subs({X: 1, Y: 2}))
assert sp.diff((X*Y)**3, X, Y).subs({X: 1, Y: 2}) == 12 + 1*2*12      # g'(t) + xy g''(t), g = t^3, t = 2

t_ = X - Y
tot = lambda g: sp.diff(g(t_), X, 2) + 2*sp.diff(g(t_), X, Y) + sp.diff(g(t_), Y, 2)
mc_g("C05-Q3", tot, [
    (r"0", lambda g, g1, g2: 0*X),
    (r"4\,g''(t)", lambda g, g1, g2: 4*g2(t_)),
    (r"2\,g''(t)", lambda g, g1, g2: 2*g2(t_)),
    (r"g'(t)", lambda g, g1, g2: g1(t_))])

t_ = X**2 + Y**2
zxx = lambda g: sp.diff(g(t_), X, 2)
lines_claims("C05-Q4", "findbug", [
    forall_g(lambda g, g1, g2: sp.diff(g(t_), X) - 2*X*g1(t_)),
    forall_g(lambda g, g1, g2: zxx(g) - 2*X*g2(t_)),
    forall_g(lambda g, g1, g2: zxx(g) - (2*g1(t_) + 4*X**2*g2(t_)))])

t_ = 2*X + 3*Y
zxx = lambda g: sp.diff(g(t_), X, 2)
zyy = lambda g: sp.diff(g(t_), Y, 2)
mcq("C05-Q5", [(r"9\,z_{xx}-4\,z_{yy}=0", forall_g(lambda g, g1, g2: 9*zxx(g) - 4*zyy(g))),
               (r"3\,z_{xx}-2\,z_{yy}=0", forall_g(lambda g, g1, g2: 3*zxx(g) - 2*zyy(g))),
               (r"z_{xx}-z_{yy}=0", forall_g(lambda g, g1, g2: zxx(g) - zyy(g))),
               (r"2\,z_{xx}-3\,z_{yy}=0", forall_g(lambda g, g1, g2: 2*zxx(g) - 3*zyy(g)))])

# =================================================================================================================
# C06  two intermediate variables
# =================================================================================================================
u_, v_ = X + Y, X*Y
gg = lambda f: f(u_, v_)
mc_f("C06-Q1", lambda f: sp.diff(f(u_, v_), X), [
    (r"f_u+y\,f_v", lambda f, fu, fv: fu(u_, v_) + Y*fv(u_, v_)),
    (r"f_u+x\,f_v", lambda f, fu, fv: fu(u_, v_) + X*fv(u_, v_)),
    (r"f_u+f_v", lambda f, fu, fv: fu(u_, v_) + fv(u_, v_)),
    (r"y\,f_u+f_v", lambda f, fu, fv: Y*fu(u_, v_) + fv(u_, v_))])

u_, v_ = X**2 - Y, X*Y
mc_f("C06-Q2", lambda f: sp.diff(f(u_, v_), Y), [
    (r"-f_u+x\,f_v", lambda f, fu, fv: -fu(u_, v_) + X*fv(u_, v_)),
    (r"f_u+x\,f_v", lambda f, fu, fv: fu(u_, v_) + X*fv(u_, v_)),
    (r"-2y\,f_u+x\,f_v", lambda f, fu, fv: -2*Y*fu(u_, v_) + X*fv(u_, v_)),
    (r"-f_u+y\,f_v", lambda f, fu, fv: -fu(u_, v_) + Y*fv(u_, v_))])

fq = U*V**2
gq = fq.subs({U: X + Y, V: X - Y})
val = sp.diff(gq, X).subs({X: 2, Y: 1})
chain = (sp.diff(fq, U)*1 + sp.diff(fq, V)*1).subs({U: 3, V: 1})
assert val == chain == 7
numeric("C06-Q3", val)

# Q4 findbug: g = f(xy, z^2 - x)
u_, v_ = X*Y, Z**2 - X
def gof(f): return f(u_, v_)
lines_claims("C06-Q4", "findbug", [
    True,
    forall_f(lambda f, fu, fv: sp.diff(gof(f), X) - (Y*fu(u_, v_) - fv(u_, v_))),
    forall_f(lambda f, fu, fv: sp.diff(gof(f), Z) - 2*Z*fu(u_, v_)),
    forall_f(lambda f, fu, fv: sp.diff(gof(f), Y) - X*fu(u_, v_))])
assert forall_f(lambda f, fu, fv: sp.diff(gof(f), Z) - 2*Z*fv(u_, v_))      # the corrected line

u_, v_ = X*Y, X/Y
def tr(f): return X*sp.diff(f(u_, v_), X) + Y*sp.diff(f(u_, v_), Y)
mc_f("C06-Q5", tr, [
    (r"2u\,f_u", lambda f, fu, fv: 2*u_*fu(u_, v_)),
    (r"2v\,f_v", lambda f, fu, fv: 2*v_*fv(u_, v_)),
    (r"u\,f_u+v\,f_v", lambda f, fu, fv: u_*fu(u_, v_) + v_*fv(u_, v_)),
    (r"0", lambda f, fu, fv: 0*X)])

full = sp.diff(sp.exp(P*R*(1/P)), P)
chain_u = (Y*sp.exp(X*Y)).subs({X: P*R, Y: 1/P}, simultaneous=True)*R + (X*sp.exp(X*Y)).subs({X: P*R, Y: 1/P}, simultaneous=True)*(-1/P**2)
assert sp.simplify(full) == 0 and sp.simplify(chain_u) == 0
def isz(e): return iszero(e, (P, R))
mcq("C06-Q6", [(r"0", isz(full - 0)),
               (r"\dfrac{v}{u}\,e^{v}", isz(full - R/P*sp.exp(R))),
               (r"-\dfrac{v}{u}\,e^{v}", isz(full + R/P*sp.exp(R))),
               (r"e^{v}", isz(full - sp.exp(R)))])
# the two "one route only" distractors really are the two partial routes
r1 = (Y*sp.exp(X*Y)).subs({X: P*R, Y: 1/P}, simultaneous=True)*R
r2 = (X*sp.exp(X*Y)).subs({X: P*R, Y: 1/P}, simultaneous=True)*(-1/P**2)
assert isz(r1 - R/P*sp.exp(R)) and isz(r2 + R/P*sp.exp(R))

# =================================================================================================================
# C07  values at a point, constant composite, Euler
# =================================================================================================================
zz = lambda u, v: u**2 + 3*u*v
uu, vv = X**2*Y, X - Y
comp = zz(uu, vv)
pt = {X: 1, Y: 1}
numeric("C07-Q1", sp.diff(comp, X).subs(pt))
numeric("C07-Q2", sp.diff(comp, Y).subs(pt))
assert sp.diff(comp, X).subs(pt) == 7 and sp.diff(comp, Y).subs(pt) == -1
# chain-rule route, step by step, equals the direct derivative
uval, vval = uu.subs(pt), vv.subs(pt)
zu_ = sp.diff(zz(U, V), U).subs({U: uval, V: vval}); zv_ = sp.diff(zz(U, V), V).subs({U: uval, V: vval})
assert (uval, vval, zu_, zv_) == (1, 0, 2, 3)
assert zu_*sp.diff(uu, X).subs(pt) + zv_*sp.diff(vv, X).subs(pt) == 7
assert zu_*sp.diff(uu, Y).subs(pt) + zv_*sp.diff(vv, Y).subs(pt) == -1

# Q3: f(t^2, 3t) = 5 for all t, f_x(4,6) = 3  ->  f_y(4,6) = -4, tested on several f that satisfy the hypothesis
tt, A = sp.symbols("tt A", real=True)
for hfun in (sp.Integer(1), X + Y, sp.exp(X/5), X*Y**2):
    f = 5 + (Y**2 - 9*X)*A*hfun
    assert sp.simplify(f.subs({X: tt**2, Y: 3*tt})) == 5
    a_val = sp.solve(sp.Eq(sp.diff(f, X).subs({X: 4, Y: 6}), 3), A)[0]
    fy = sp.diff(f, Y).subs({X: 4, Y: 6, A: a_val})
    assert sp.simplify(fy) == -4, (hfun, fy)
numeric("C07-Q3", -4)

# Q4: w = x^3 F(z/x, y/x)
def euler_sum(F, kk):
    w = X**kk*F(Z/X, Y/X)
    return X*sp.diff(w, X) + Y*sp.diff(w, Y) + Z*sp.diff(w, Z), w
mcq("C07-Q4", [
    (r"3w", forall_f(lambda f, fu, fv: euler_sum(f, 3)[0] - 3*euler_sum(f, 3)[1])),
    (r"w", forall_f(lambda f, fu, fv: euler_sum(f, 3)[0] - euler_sum(f, 3)[1])),
    (r"x^3", forall_f(lambda f, fu, fv: euler_sum(f, 3)[0] - X**3)),
    (r"0", forall_f(lambda f, fu, fv: euler_sum(f, 3)[0]))])

# Q5 findbug (k symbolic): w = x^k F(s, t), s = z/x, t = y/x
def wk(f): return X**K*f(Z/X, Y/X)
s_, t2 = Z/X, Y/X
lines_claims("C07-Q5", "findbug", [
    sp.simplify(sp.diff(s_, X) + Z/X**2) == 0 and sp.simplify(sp.diff(t2, X) + Y/X**2) == 0,
    forall_f(lambda f, fu, fv: sp.diff(wk(f), X) - X**K*(fu(s_, t2)*sp.diff(s_, X) + fv(s_, t2)*sp.diff(t2, X))),
    forall_f(lambda f, fu, fv: sp.diff(wk(f), Y) - X**(K - 1)*fv(s_, t2)) and forall_f(lambda f, fu, fv: sp.diff(wk(f), Z) - X**(K - 1)*fu(s_, t2)),
    forall_f(lambda f, fu, fv: X*sp.diff(wk(f), X) + Y*sp.diff(wk(f), Y) + Z*sp.diff(wk(f), Z)
             - (K*X**K*f(s_, t2) - X**(K - 1)*(Z*fu(s_, t2) + Y*fv(s_, t2)) + X**(K - 1)*(Y*fv(s_, t2) + Z*fu(s_, t2))))])
assert forall_f(lambda f, fu, fv: sp.diff(wk(f), X) - (K*X**(K - 1)*f(s_, t2) + X**K*(fu(s_, t2)*sp.diff(s_, X) + fv(s_, t2)*sp.diff(t2, X))))
assert forall_f(lambda f, fu, fv: X*sp.diff(wk(f), X) + Y*sp.diff(wk(f), Y) + Z*sp.diff(wk(f), Z) - K*wk(f))   # Euler

# =================================================================================================================
# coverage: every own question was checked; every bankId exists in the bank
# =================================================================================================================
missing = sorted(set(Q) - covered)
assert not missing, ("questions without a check:", missing)
bank = json.loads((ROOT / "questions.json").read_text(encoding="utf-8"))
bank = bank["questions"] if isinstance(bank, dict) else bank
ids = {b["id"] for b in bank}
pulls = [q["bankId"] for L in LEVELS for q in L["questions"] if "bankId" in q]
assert all(p in ids for p in pulls), [p for p in pulls if p not in ids]
print("OK: %d own questions machine-checked, %d bank pulls present (%s)" % (len(covered), len(pulls), ", ".join(pulls)))
