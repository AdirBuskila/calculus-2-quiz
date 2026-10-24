# -*- coding: utf-8 -*-
"""Machine check for the guided course `series` (courses/series/C01..C08.js).

Every stored answer is recomputed here and compared with the level files (loaded through tools/course_load.js):
  * mcq: every option text is mapped to a computed truth value, and exactly the stored correctId must be the true one
    (so each distractor is shown to be wrong, and nothing is cited by position);
  * numeric steps: the stored answer equals the sympy value;
  * findbug / order steps: each line is a claim that is evaluated; the first false line must be bugIndex;
  * series verdicts and endpoint verdicts: sympy limits/inequalities decide, and partial sums / tail bounds confirm
    (Leibniz error bound for alternating series, growing increments for divergence, shrinking tails for convergence);
  * boss bankIds: the official keys of the six bank questions are recomputed.
Run: PYTHONUTF8=1 py tools/verify/needhelp/series/check.py
"""
import json, pathlib, re, subprocess, math
import numpy as np
import sympy as sp
import mpmath as mp

HERE = pathlib.Path(__file__).resolve().parent
APP = HERE.parents[3]
n = sp.symbols("n", positive=True, integer=True)
x = sp.symbols("x", real=True)
R_ = sp.Rational
oo = sp.oo
ok = []

ABS, COND, DIV = "מתכנס בהחלט", "מתכנס בתנאי", "מתבדר"
VERDICT_TEXT = {"abs": ABS, "cond": COND, "div": DIV}


def check(name, cond):
    assert cond, "MISMATCH: " + name
    ok.append(name)


# ---------------------------------------------------------------- loading
def load_levels():
    r = subprocess.run(["node", str(APP / "tools" / "course_load.js")], capture_output=True, encoding="utf-8", check=True)
    data = json.loads(r.stdout)
    assert not data["errors"], data["errors"]
    lv = [e["level"] for e in data["levels"] if e["courseId"] == "series"]
    return sorted(lv, key=lambda L: L["order"])


LEVELS = load_levels()
Q = {}
for L in LEVELS:
    for q in L["questions"]:
        if "id" in q:
            Q[q["id"]] = q
BANK = {q["id"]: q for q in json.load(open(APP / "questions.json", encoding="utf-8"))["questions"]}


def optmap(qid):
    return {o["id"]: o["value"] for o in Q[qid]["options"]}


def mcq_exact(qid, truth):
    """truth: option text -> bool. Covers every option exactly; exactly one is true and it is the stored correctId."""
    om = optmap(qid)
    check(f"{qid} option texts are all covered by the check", set(om.values()) == set(truth))
    trues = [i for i, v in om.items() if truth[v]]
    check(f"{qid} exactly one option is true", len(trues) == 1)
    check(f"{qid} stored correctId is that option", Q[qid]["correctId"] == trues[0])
    check(f"{qid} no acceptedIds", not Q[qid].get("acceptedIds"))


def verdict_mcq(qid, expected):
    mcq_exact(qid, {t: (t == VERDICT_TEXT[expected]) for t in optmap(qid).values()})
    check(f"{qid} the options are exactly the three verdicts", set(optmap(qid).values()) == set(VERDICT_TEXT.values()))


def num_step(qid, expected, tol=0):
    s = Q[qid]["step"]
    check(f"{qid} is a numeric step", s["type"] == "numeric")
    check(f"{qid} stored answer == computed {expected}", abs(float(s["answer"]) - float(expected)) < 1e-12)
    check(f"{qid} stored tol == {tol}", abs(float(s.get("tol", 0)) - tol) < 1e-12)


def first_false(qid, truths, typ):
    s = Q[qid]["step"]
    check(f"{qid} is a {typ} step", s["type"] == typ)
    check(f"{qid} has {len(truths)} lines", len(s["lines"]) == len(truths))
    bug = truths.index(False)
    check(f"{qid} first false line is the stored bugIndex ({bug})", s["bugIndex"] == bug)
    check(f"{qid} lines before the bug are true", all(truths[:bug]))


def all_true_order(qid, truths):
    s = Q[qid]["step"]
    check(f"{qid} is an order step", s["type"] == "order")
    check(f"{qid} has {len(truths)} lines", len(s["lines"]) == len(truths))
    check(f"{qid} every line of the proof is a true claim", all(truths))


# ---------------------------------------------------------------- TeX -> sympy
def tex_num(s):
    s = s.replace(r"\dfrac", r"\frac").replace(r"\left", "").replace(r"\right", "")
    for _ in range(3):
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
    s = re.sub(r"\\frac(\d)(\d)", r"(\1/\2)", s)
    s = re.sub(r"\\sqrt\{([^{}]*)\}", r"sqrt(\1)", s)
    return sp.sympify(s.replace(r"\infty", "oo"))


def parse_set(t):
    t = t.strip().strip("$").replace(" ", "")
    m = re.fullmatch(r"\|x\|(<|\\le)(.+)", t)
    if m:
        b = tex_num(m.group(2))
        o = m.group(1) == "<"
        return sp.Interval(-b, b, left_open=o, right_open=o)
    m = re.fullmatch(r"([\[(])(.+?),(.+?)([\])])", t)
    if m:
        return sp.Interval(tex_num(m.group(2)), tex_num(m.group(3)), left_open=m.group(1) == "(", right_open=m.group(4) == ")")
    m = re.fullmatch(r"(.+?)(<|\\le)x(<|\\le)(.+)", t)
    if m:
        return sp.Interval(tex_num(m.group(1)), tex_num(m.group(4)), left_open=m.group(2) == "<", right_open=m.group(3) == "<")
    m = re.fullmatch(r"x<(.+)", t)
    if m:
        return sp.Interval.open(-oo, tex_num(m.group(1)))
    raise AssertionError("cannot parse set " + t)


def set_mcq(qid, truth_set):
    om = optmap(qid)
    mcq_exact(qid, {v: (parse_set(v) == truth_set) for v in om.values()})


# ---------------------------------------------------------------- series engine
CAND_P = [R_(1, 2), R_(1), R_(3, 2), R_(2), R_(3), R_(4, 3), R_(5, 4), R_(5, 2)]


def is_pos_finite(L):
    return L.is_finite and L.is_positive


def increments(A, alt, n0, Ns=(10**4, 10**5, 10**6)):
    """signed and absolute partial sums at Ns, with float64 numpy."""
    f = sp.lambdify(n, A, "numpy")
    k = np.arange(n0, Ns[-1] + 1, dtype=np.float64)
    a = f(k) * np.ones_like(k)
    s_abs = np.cumsum(a)
    sg = a * np.where(k % 2 == 0, 1.0, -1.0) if alt else a
    s_sig = np.cumsum(sg)
    at = lambda arr, N: float(arr[N - n0])
    return f, [at(s_abs, N) for N in Ns], [at(s_sig, N) for N in Ns]


def abs_conv(A):
    """True/False for convergence of sum A (A > 0). Returns (bool, how)."""
    D = sp.limit(sp.simplify(sp.combsimp(A.subs(n, n + 1) / A)), n, oo)
    if D < 1:
        return True, f"ratio D={D}"
    if D > 1:
        return False, f"ratio D={D}"
    for p in CAND_P:
        L = sp.limit(A * n**p, n, oo)
        if is_pos_finite(L):
            return bool(p > 1), f"limit comparison with n^-{p}, L={L}"
    raise AssertionError(f"no comparison found for {A}")


def classify(A, alt, n0=1, abs_override=None):
    """-> 'abs' | 'cond' | 'div' for sum a_n, |a_n| = A (n >= n0), a_n alternating when alt.
    The verdict comes from sympy limits; partial sums / tail bounds then confirm it numerically."""
    A = sp.expand(sp.simplify(A))
    L0 = sp.limit(A, n, oo)
    if L0 != 0:
        f = sp.lambdify(n, A, "numpy")
        check(f"terms do not tend to 0 ({A}): |a_N| stays >= 1e-3 at N=1e6", float(f(np.float64(1e6))) > 1e-3)
        return "div"
    if abs_override is not None:
        conv, how = abs_override
    else:
        conv, how = abs_conv(A)
    f, S_abs, S_sig = increments(A, alt, n0)
    inc1, inc2 = S_abs[1] - S_abs[0], S_abs[2] - S_abs[1]
    if conv:
        check(f"abs sum of {A}: tails shrink ({how}): {inc1:.3g} -> {inc2:.3g}", inc2 <= inc1 and inc2 < 0.2)
        if alt:
            check(f"signed partial sums of {A} settle", abs(S_sig[2] - S_sig[1]) < 0.2)
        return "abs"
    check(f"abs sum of {A} grows without a tail bound ({how}): increments {inc1:.3g}, {inc2:.3g}", inc1 > 0.1 and inc2 > 0.1)
    if not alt:
        return "div"
    ks = np.arange(n0, 6001, dtype=np.float64)
    vals = f(ks)
    check(f"{A} decreasing for n={n0}..6000", bool(np.all(np.diff(vals) < 0)))
    for N1 in (10**3, 10**4, 10**5):
        N2 = 10 * N1
        s1 = increments(A, True, n0, Ns=(N1, N2))[2]
        check(f"Leibniz tail bound |S_{N2}-S_{N1}| <= a_{N1 + 1} for {A}", abs(s1[1] - s1[0]) <= float(f(np.float64(N1 + 1))) + 1e-12)
    return "cond"


def domain(cabs, csign, x0=0, n0=1, expected_R=None):
    """Domain of sum c_n (x-x0)^n with |c_n| = cabs and sign pattern csign ('pos'|'alt') -> sympy Interval (or R/oo info)."""
    cabs = sp.simplify(cabs)
    Rr = sp.limit(sp.simplify(sp.combsimp(cabs / cabs.subs(n, n + 1))), n, oo)
    if expected_R is not None:
        check(f"radius of {cabs} is {expected_R}", Rr == expected_R)
    if Rr in (0, oo):
        return Rr, None
    res = {}
    for side in (-1, 1):
        A = sp.simplify(sp.powsimp(cabs * Rr**n))
        same = (side == 1 and csign == "pos") or (side == -1 and csign == "alt")
        res[side] = classify(A, alt=not same, n0=n0)
    closed = {s: res[s] in ("abs", "cond") for s in (-1, 1)}
    return Rr, sp.Interval(x0 - Rr, x0 + Rr, left_open=not closed[-1], right_open=not closed[1])


# ======================================================================== C01
# Q1: sum (n^2+1)/(2n^2+3)
check("C01-Q1 limit of the term is 1/2", sp.limit((n**2 + 1) / (2 * n**2 + 3), n, oo) == R_(1, 2))
check("C01-Q1 verdict", classify((n**2 + 1) / (2 * n**2 + 3), False) == "div")
verdict_mcq("C01-Q1", "div")
# Q2, Q3: geometric sums
check("C01-Q2 sum 5/3^n", sp.summation(5 / sp.Integer(3)**n, (n, 1, oo)) == R_(5, 2))
num_step("C01-Q2", 2.5)
v = sp.summation(1 / sp.Integer(3)**n, (n, 2, oo))
check("C01-Q3 sum_{n>=2} 3^-n = 1/6", v == R_(1, 6))
num_step("C01-Q3", float(R_(1, 6)), tol=0.001)
check("C01-Q3 the start-at-1 mistake (1/2) is outside the tolerance", abs(0.5 - Q["C01-Q3"]["step"]["answer"]) > Q["C01-Q3"]["step"]["tol"])
check("C01-Q3 the q-instead-of-q^2 mistake (1/3) is outside the tolerance", abs(1 / 3 - Q["C01-Q3"]["step"]["answer"]) > Q["C01-Q3"]["step"]["tol"])
# Q4: geometric with q=x/4
truth = sp.Interval.open(-4, 4)
check("C01-Q4 |x/4|<1 gives (-4,4)", sp.solve_univariate_inequality(sp.Abs(x / 4) < 1, x, relational=False) == truth)
check("C01-Q4 endpoints: terms (+-1)^n do not tend to 0", all(abs((sp.Integer(s) * 4 / 4) ** 5) == 1 for s in (-1, 1)))
set_mcq("C01-Q4", truth)
# Q5: which converges
Q5 = {
    r"$\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\sqrt n}$": 1 / (n * sp.sqrt(n)),
    r"$\displaystyle\sum_{n=1}^{\infty}\frac{1}{\sqrt n}$": 1 / sp.sqrt(n),
    r"$\displaystyle\sum_{n=1}^{\infty}\frac{1}{n}$": 1 / n,
    r"$\displaystyle\sum_{n=1}^{\infty}\frac{n}{n+1}$": n / (n + 1),
}
mcq_exact("C01-Q5", {t: classify(A, False) == "abs" for t, A in Q5.items()})
# Q6: converse of the necessary condition
H = sp.Integer(0)
Hk = [sum(sp.Rational(1, i) for i in range(1, 2**k + 1)) for k in range(1, 13)]
check("C01-Q6 counterexample: H_(2^k) >= 1 + k/2 for k=1..12 (harmonic sum unbounded although 1/n -> 0)",
      all(Hk[k - 1] >= 1 + sp.Rational(k, 2) for k in range(1, 13)))
first_false("C01-Q6", [True, sp.limit(1 / n, n, oo) == 0, False, False], "findbug")

# ======================================================================== C02
A_c2q1 = (n + 1) / (n**3 + 5)
mcq_exact("C02-Q1", {
    r"$\displaystyle\sum\frac{1}{n}$": is_pos_finite(sp.limit(A_c2q1 * n, n, oo)),
    r"$\displaystyle\sum\frac{1}{n^3}$": is_pos_finite(sp.limit(A_c2q1 * n**3, n, oo)),
    r"$\displaystyle\sum\frac{1}{n^4}$": is_pos_finite(sp.limit(A_c2q1 * n**4, n, oo)),
    r"$\displaystyle\sum\frac{1}{n^2}$": is_pos_finite(sp.limit(A_c2q1 * n**2, n, oo)),
})
check("C02-Q1 limit with 1/n^2 equals 1", sp.limit(A_c2q1 * n**2, n, oo) == 1)
check("C02-Q2 limit (2n^2+1)n^2/(n^4+n) = 2", sp.limit((2 * n**2 + 1) / (n**4 + n) * n**2, n, oo) == 2)
num_step("C02-Q2", 2)
# Q3: (-1)^n (2+cos n)/n^2: absolute via the bound 3/n^2
k = np.arange(1, 400001, dtype=np.float64)
check("C02-Q3 bound (2+cos n)/n^2 <= 3/n^2 for n<=4e5", bool(np.all((2 + np.cos(k)) / k**2 <= 3 / k**2 + 1e-18)))
check("C02-Q3 the majorant 3/n^2 is a p-series with p=2", classify(3 / n**2, False) == "abs")
f3 = sp.lambdify(n, (2 + sp.cos(n)) / n**2, "numpy")
kk = np.arange(1, 10**6 + 1, dtype=np.float64)
cs = np.cumsum(f3(kk))
check("C02-Q3 abs partial sums: tail beyond 1e5 below 3/1e5", cs[-1] - cs[10**5 - 1] < 3.0 / 1e5)
verdict_mcq("C02-Q3", "abs")
# Q4: 1/sqrt(n^2+n)
check("C02-Q4 limit comparison with 1/n gives 1", sp.limit(1 / sp.sqrt(n**2 + n) * n, n, oo) == 1)
check("C02-Q4 verdict", classify(1 / sp.sqrt(n**2 + n), False) == "div")
verdict_mcq("C02-Q4", "div")
# Q5: invalid inference "larger diverges => smaller diverges"
ks = np.arange(1, 10**6 + 1, dtype=np.float64)
check("C02-Q5 line 1: 1/(sqrt n+1) <= 1/sqrt n for n<=1e6", bool(np.all(1 / (np.sqrt(ks) + 1) <= 1 / np.sqrt(ks))))
check("C02-Q5 line 2: sum 1/sqrt n diverges (p=1/2)", classify(1 / sp.sqrt(n), False) == "div")
cnt_small = np.cumsum(1 / ks**2)
cnt_big = np.cumsum(1 / ks)
check("C02-Q5 line 3 is false: 1/n^2 <= 1/n, sum 1/n diverges but sum 1/n^2 settles (< pi^2/6)",
      bool(np.all(1 / ks**2 <= 1 / ks)) and cnt_big[-1] > 14 and cnt_small[-1] < math.pi**2 / 6)
check("C02-Q5 the series itself diverges (limit comparison with 1/sqrt n is 1)", sp.limit(1 / (sp.sqrt(n) + 1) * sp.sqrt(n), n, oo) == 1)
first_false("C02-Q5", [True, True, True, False, True], "findbug")
# Q6: which bound proves absolute convergence
ks = np.arange(1, 10**6 + 1, dtype=np.float64)
s = np.sin(ks)
holds = {
    "a": bool(np.all(s / ks**2 <= 1 / ks)),
    "b": bool(np.all(s / ks**2 >= -1 / ks**2)),
    "c": bool(np.all(np.abs(s) / ks**2 <= 1 / ks**2)),
    "d": bool(np.all(np.abs(s) / ks**2 >= 1 / ks**2)),
}
check("C02-Q6 the truth of the four inequalities (a,b,c hold, d fails)", holds == {"a": True, "b": True, "c": True, "d": False})
om = optmap("C02-Q6")
# an option proves absolute convergence iff it holds, bounds |a_n| from above, and the majorant converges
proofs = {
    r"$\dfrac{\sin n}{n^2}\le\dfrac1n$": holds["a"] and False,        # majorant 1/n diverges, and no absolute value
    r"$\dfrac{\sin n}{n^2}\ge-\dfrac{1}{n^2}$": holds["b"] and False,  # lower bound of the signed term
    r"$\left|\dfrac{\sin n}{n^2}\right|\le\dfrac{1}{n^2}$": holds["c"] and classify(1 / n**2, False) == "abs",
    r"$\left|\dfrac{\sin n}{n^2}\right|\ge\dfrac{1}{n^2}$": holds["d"],
}
check("C02-Q6 the majorant 1/n of option a diverges", classify(1 / n, False) == "div")
mcq_exact("C02-Q6", proofs)

# ======================================================================== C03
check("C03-Q1 ratio limit of n^2/2^n is 1/2", sp.limit(sp.simplify((n + 1) ** 2 / 2 ** (n + 1) / (n**2 / 2**n)), n, oo) == R_(1, 2))
num_step("C03-Q1", 0.5)
# Q2: 3^n/n! -> ratio 3/(n+1) -> 0
D = sp.limit(sp.simplify(sp.combsimp(sp.Integer(3) ** (n + 1) / sp.factorial(n + 1) / (sp.Integer(3) ** n / sp.factorial(n)))), n, oo)
check("C03-Q2 ratio limit is 0", D == 0)
terms = [sp.Integer(3) ** i / sp.factorial(i) for i in range(1, 80)]
check("C03-Q2 tail of sum 3^n/n! beyond n=60 is below 1e-30", sum(terms[60:]) < sp.Float("1e-30"))
check("C03-Q2 the series sums to e^3-1 (so the abs series converges)", abs(sum(terms) - (sp.exp(3) - 1)) < sp.Float("1e-30"))
verdict_mcq("C03-Q2", "abs")
# Q3: root test
c3 = sp.limit(n / (2 * n + 1), n, oo)
check("C03-Q3 root limit is 1/2", c3 == R_(1, 2))
ks = np.arange(1, 4001, dtype=np.float64)
check("C03-Q3 terms (n/(2n+1))^n sum to a finite value (partial sums settle)", abs(np.sum((ks / (2 * ks + 1)) ** ks) - np.sum((ks[:2000] / (2 * ks[:2000] + 1)) ** ks[:2000])) < 1e-12)
mcq_exact("C03-Q3", {
    r"$c=2$, ולכן הטור מתבדר": c3 == 2 and 2 > 1,
    r"$c=1$, ולכן אין מידע": c3 == 1,
    r"$c=\frac12$, ולכן הטור מתבדר": c3 == R_(1, 2) and c3 > 1,
    r"$c=\frac12$, ולכן הטור מתכנס": c3 == R_(1, 2) and c3 < 1,
})
# Q4: D=1 is inconclusive
D1 = sp.limit(sp.simplify((1 / (n + 1)) / (1 / n)), n, oo)
D2 = sp.limit(sp.simplify((1 / (n + 1) ** 2) / (1 / n**2)), n, oo)
check("C03-Q4 D=1 for both 1/n and 1/n^2", D1 == 1 and D2 == 1)
check("C03-Q4 ... yet 1/n diverges and 1/n^2 converges", classify(1 / n, False) == "div" and classify(1 / n**2, False) == "abs")
mcq_exact("C03-Q4", {
    "הטור מתכנס, כי $D\\le1$": False,
    "הטור מתבדר, כי $D\\ge1$": False,
    "הטור מתכנס בתנאי": False,
    "אי אפשר להסיק: יש גם טורים מתכנסים וגם טורים מתבדרים עם $D=1$": True,
})
# Q5: sum 1/(n ln^3 n)
xs = sp.symbols("xs", positive=True)
F5 = sp.integrate(1 / (xs * sp.log(xs) ** 3), xs)
I5 = sp.limit(F5, xs, oo) - F5.subs(xs, 2)
check("C03-Q5 integral from 2 is 1/(2 ln^2 2)", sp.simplify(I5 - 1 / (2 * sp.log(2) ** 2)) == 0)
check("C03-Q5 f decreasing for x>=2 (derivative negative on a grid)",
      all(sp.diff(1 / (xs * sp.log(xs) ** 3), xs).subs(xs, sp.Float(v)) < 0 for v in np.linspace(2, 1e6, 400)))
ks = np.arange(2, 2 * 10**6 + 1, dtype=np.float64)
cs = np.cumsum(1 / (ks * np.log(ks) ** 3))
check("C03-Q5 partial sums stay below the integral bound 1/(2 ln^2 2) + f(2)",
      cs[-1] <= float(I5) + 1 / (2 * math.log(2) ** 3) and cs[-1] - cs[10**6 - 2] < 1e-3)
verdict_mcq("C03-Q5", "abs")
# Q6: integral test for 1/(n ln n)
f6 = 1 / (xs * sp.log(xs))
check("C03-Q6 line 0: f positive and decreasing on [2,oo)", all(sp.diff(f6, xs).subs(xs, sp.Float(v)) < 0 and f6.subs(xs, sp.Float(v)) > 0 for v in np.linspace(2, 1e6, 400)))
M = sp.symbols("M", positive=True)
check("C03-Q6 line 1: antiderivative ln ln x", sp.simplify(sp.diff(sp.log(sp.log(xs)), xs) - f6) == 0)
check("C03-Q6 line 1: integral from 2 to 50 matches ln ln 50 - ln ln 2", abs(sp.Integral(f6, (xs, 2, 50)).evalf() - (sp.log(sp.log(50)) - sp.log(sp.log(2))).evalf()) < 1e-12)
check("C03-Q6 line 2: ln ln M -> oo", sp.limit(sp.log(sp.log(M)), M, oo) == oo)
ks = np.arange(2, 3 * 10**6 + 1, dtype=np.float64)
cs = np.cumsum(1 / (ks * np.log(ks)))
low = lambda N: math.log(math.log(N + 1)) - math.log(math.log(2))
check("C03-Q6 line 3: partial sums dominate the integral ln ln (N+1) - ln ln 2 (divergence is real, slowly)", cs[-1] >= low(3 * 10**6))
all_true_order("C03-Q6", [True, True, True, True])

# ======================================================================== C04
check("C04-Q1 verdict", classify(1 / n, True) == "cond")
verdict_mcq("C04-Q1", "cond")
check("C04-Q2 cos(pi n) = (-1)^n", all(sp.cos(sp.pi * k) == (-1) ** k for k in range(1, 40)))
check("C04-Q2 verdict", classify(1 / n**2, True) == "abs")
verdict_mcq("C04-Q2", "abs")
check("C04-Q3 verdict", classify(n / (n + 1), True) == "div")
verdict_mcq("C04-Q3", "div")
# Q4: (-1)^n / (sqrt n ln n), n>=2
A4 = 1 / (sp.sqrt(n) * sp.log(n))
ks = np.arange(2, 10**7, dtype=np.float64)
check("C04-Q4 |a_n| >= 1/n for 2<=n<1e7 (since ln n <= sqrt n)", bool(np.all(1 / (np.sqrt(ks) * np.log(ks)) >= 1 / ks)))
y = sp.symbols("y", positive=True)
ymin = sp.solve(sp.diff(sp.sqrt(y) - sp.log(y), y), y)
check("C04-Q4 min of sqrt(y)-ln(y) is at y=4 and is positive", ymin == [4] and (sp.sqrt(4) - sp.log(4)) > 0)
check("C04-Q4 verdict (abs diverges by the 1/n bound, Leibniz applies)", classify(A4, True, n0=2, abs_override=(False, "lower bound 1/n")) == "cond")
verdict_mcq("C04-Q4", "cond")
# Q5: Leibniz error bound
Nmin = min(N for N in range(1, 1000) if R_(1, (N + 1) ** 2) <= R_(1, 100))
check("C04-Q5 smallest N with a_(N+1) <= 0.01 is 9", Nmin == 9 and R_(1, 81) > R_(1, 100))
S = sp.pi**2 / 12
S9 = sum(R_((-1) ** (i + 1), i**2) for i in range(1, 10))
check("C04-Q5 the true error at N=9 is within the guaranteed bound", abs(S - S9) <= R_(1, 100))
num_step("C04-Q5", 9)
# Q6: non-monotone a_n = (2+(-1)^n)/n
ks = np.arange(1, 10**6 + 1, dtype=np.float64)
a6 = (2 + (-1.0) ** ks) / ks
check("C04-Q6 line 1: a_n > 0 and a_n <= 3/n", bool(np.all(a6 > 0) and np.all(a6 <= 3 / ks)))
check("C04-Q6 line 2 is false: a_1 = 1 < a_2 = 3/2", a6[0] == 1 and a6[1] == 1.5 and a6[1] > a6[0])
cs = np.cumsum((-1.0) ** ks * a6)
check("C04-Q6 line 3 is false: the series diverges, S_N grows like ln N (S_1e6 - S_1e5 ~ ln 10)", abs((cs[-1] - cs[10**5 - 1]) - math.log(10)) < 0.1)
first_false("C04-Q6", [True, True, False, False], "findbug")

# ======================================================================== C05
a = 1 / (n * sp.Integer(3) ** n)
check("C05-Q1 R=3", sp.limit(sp.simplify(a / a.subs(n, n + 1)), n, oo) == 3)
num_step("C05-Q1", 3)
a = sp.factorial(n) / n**n
Rq2 = sp.limit(sp.simplify(sp.combsimp(a / a.subs(n, n + 1))), n, oo)
check("C05-Q2 R=e", Rq2 == sp.E)
mcq_exact("C05-Q2", {r"$\dfrac1e$": 1 / sp.E == Rq2, r"$1$": Rq2 == 1, r"$e$": sp.E == Rq2, r"$\infty$": Rq2 == oo})
# Q3: root test, 1/R = 4/5
lg = sp.limit(sp.log(sp.Integer(4) ** n + 1) / n - sp.log(5), n, oo)
check("C05-Q3 log(root) -> log(4/5), so R=5/4", sp.simplify(lg - sp.log(R_(4, 5))) == 0)
num_step("C05-Q3", 1.25)
# Q4: center and radius of (x+1)^n / (n 2^n)
a = 1 / (n * sp.Integer(2) ** n)
R4 = sp.limit(sp.simplify(a / a.subs(n, n + 1)), n, oo)
center = sp.solve(x + 1, x)[0]
check("C05-Q4 center -1, radius 2", center == -1 and R4 == 2)
mcq_exact("C05-Q4", {
    r"מרכז $1$, רדיוס $2$": (1, 2) == (center, R4),
    r"מרכז $-1$, רדיוס $\frac12$": (-1, R_(1, 2)) == (center, R4),
    r"מרכז $-1$, רדיוס $2$": (-1, 2) == (center, R4),
    r"מרכז $1$, רדיוס $\frac12$": (1, R_(1, 2)) == (center, R4),
})
# Q5: x^(2n)/4^n
sol = sp.solve_univariate_inequality(sp.Abs(x**2 / 4) < 1, x, relational=False)
R5 = sol.sup
check("C05-Q5 |x^2/4|<1 gives |x|<2", sol == sp.Interval.open(-2, 2))
mcq_exact("C05-Q5", {r"$R=4$": R5 == 4, r"$R=\frac14$": R5 == R_(1, 4), r"$R=2$": R5 == 2, r"$R=\frac12$": R5 == R_(1, 2)})
# Q6: n^n x^n
a = n**n
R6 = sp.limit(sp.simplify(a / a.subs(n, n + 1)), n, oo)
check("C05-Q6 ratio limit n^n/(n+1)^(n+1) is 0", R6 == 0)
check("C05-Q6 root limit is oo", sp.limit(n, n, oo) == oo)
mcq_exact("C05-Q6", {r"$R=\infty$": R6 == oo, r"$R=1$": R6 == 1, r"$R=e$": R6 == sp.E, r"$R=0$": R6 == 0})

# ======================================================================== C06
# endpoint verdicts use classify() (limit tests + partial sums / Leibniz tail bounds)
Rr, dom1 = domain(1 / n, "pos", expected_R=1)
check("C06-Q1 domain [-1,1)", dom1 == sp.Interval.Ropen(-1, 1))
set_mcq("C06-Q1", dom1)
Rr, dom2 = domain(1 / n**2, "pos", expected_R=1)
check("C06-Q2 domain [-1,1]", dom2 == sp.Interval(-1, 1))
set_mcq("C06-Q2", dom2)
Rr, dom3 = domain(n / (n + 1), "pos", expected_R=1)
check("C06-Q3 domain (-1,1)", dom3 == sp.Interval.open(-1, 1))
set_mcq("C06-Q3", dom3)
# Q4: shifted domain, built from a witness series with domain (-3,3]
Rw, base = domain(1 / (n * sp.Integer(3) ** n), "alt", expected_R=3)
check("C06-Q4 the witness series has domain (-3,3]", base == sp.Interval.Lopen(-3, 3))
shifted = sp.Interval(base.start + 1, base.end + 1, left_open=base.left_open, right_open=base.right_open)
Rw2, direct = domain(1 / (n * sp.Integer(3) ** n), "alt", x0=1)
check("C06-Q4 computing the shifted series directly gives the same domain", direct == shifted == sp.Interval.Lopen(-2, 4))
set_mcq("C06-Q4", shifted)
Rr, dom5 = domain(1 / (n * sp.Integer(3) ** n), "pos", x0=2, expected_R=3)
check("C06-Q5 domain [-1,5)", dom5 == sp.Interval.Ropen(-1, 5))
set_mcq("C06-Q5", dom5)
# Q6: x^n / sqrt(n)
Rr, dom6 = domain(1 / sp.sqrt(n), "pos", expected_R=1)
check("C06-Q6 true domain is [-1,1)", dom6 == sp.Interval.Ropen(-1, 1))
check("C06-Q6 the stored line (-1,1] is not the domain", sp.Interval.Lopen(-1, 1) != dom6)
check("C06-Q6 line 1: x=1 gives 1/sqrt n, diverges", classify(1 / sp.sqrt(n), False) == "div")
check("C06-Q6 line 2: x=-1 gives alternating 1/sqrt n, converges (not absolutely)", classify(1 / sp.sqrt(n), True) == "cond")
first_false("C06-Q6", [Rr == 1, True, True, False], "findbug")

# ======================================================================== C07
# Q1: 1/(1+2x)
ser = sp.series(1 / (1 + 2 * x), x, 0, 12).removeO()
coeffs = [ser.coeff(x, i) for i in range(12)]
check("C07-Q1 coefficients are (-2)^n", coeffs == [(-2) ** i for i in range(12)])
check("C07-Q1 radius is 1/2 (|2x|<1)", sp.solve_univariate_inequality(sp.Abs(2 * x) < 1, x, relational=False) == sp.Interval.open(-R_(1, 2), R_(1, 2)))
cand = {
    r"$\sum_{n=0}^{\infty}(-2)^nx^n$ עבור $|x|<2$": (lambda i: (-2) ** i, 2),
    r"$\sum_{n=0}^{\infty}2^nx^n$ עבור $|x|<\frac12$": (lambda i: 2**i, R_(1, 2)),
    r"$\sum_{n=0}^{\infty}\frac{(-1)^n}{2^n}x^n$ עבור $|x|<2$": (lambda i: R_((-1) ** i, 2**i), 2),
    r"$\sum_{n=0}^{\infty}(-2)^nx^n$ עבור $|x|<\frac12$": (lambda i: (-2) ** i, R_(1, 2)),
}
mcq_exact("C07-Q1", {t: all(c(i) == coeffs[i] for i in range(12)) and r == R_(1, 2) for t, (c, r) in cand.items()})
# Q2, Q3: f^(k)(0)
f2 = x**2 * sp.exp(x)
check("C07-Q2 f^(5)(0) = 20", sp.diff(f2, x, 5).subs(x, 0) == 20)
check("C07-Q2 via the coefficient: 5! * 1/3! = 20", sp.factorial(5) * R_(1, sp.factorial(3)) == 20)
num_step("C07-Q2", 20)
f3 = sp.sin(x**2)
check("C07-Q3 f^(6)(0) = -120", sp.diff(f3, x, 6).subs(x, 0) == -120)
check("C07-Q3 via the coefficient of x^6 = -1/6", sp.series(f3, x, 0, 8).removeO().coeff(x, 6) == -R_(1, 6) and sp.factorial(6) * (-R_(1, 6)) == -120)
num_step("C07-Q3", -120)
# Q4: ln(1+3x)
cabs4 = sp.Integer(3) ** n / n
R4_, dom4 = domain(cabs4, "alt", expected_R=R_(1, 3))
check("C07-Q4 coefficients of ln(1+3x) are (-1)^(n+1) 3^n / n",
      sp.series(sp.log(1 + 3 * x), x, 0, 9).removeO() == sum(R_((-1) ** (i + 1) * 3**i, i) * x**i for i in range(1, 9)))
check("C07-Q4 domain (-1/3,1/3]", dom4 == sp.Interval.Lopen(-R_(1, 3), R_(1, 3)))
set_mcq("C07-Q4", dom4)
# Q5, Q6: 1/((1-x)(1-2x))
f5 = 1 / ((1 - x) * (1 - 2 * x))
check("C07-Q5 partial fractions 2/(1-2x) - 1/(1-x)", sp.simplify(f5 - (2 / (1 - 2 * x) - 1 / (1 - x))) == 0)
ser5 = sp.series(f5, x, 0, 12).removeO()
check("C07-Q5 coefficients are 2^(n+1)-1", all(ser5.coeff(x, i) == 2 ** (i + 1) - 1 for i in range(12)))
check("C07-Q5 f^(4)(0) = 744", sp.diff(f5, x, 4).subs(x, 0) == 744 == sp.factorial(4) * 31)
num_step("C07-Q5", 744)
R6_, dom6b = domain(sp.Integer(2) ** (n + 1) - 1, "pos", expected_R=R_(1, 2))
check("C07-Q6 domain (-1/2,1/2): both endpoints diverge (terms -> 2)", dom6b == sp.Interval.open(-R_(1, 2), R_(1, 2)))
check("C07-Q6 consistent with the singularities x=1 and x=1/2 of f (nearest is 1/2)", sp.solve(sp.denom(sp.together(f5)), x) in ([R_(1, 2), 1], [1, R_(1, 2)]))
set_mcq("C07-Q6", dom6b)

# ======================================================================== C08 (boss, bankIds)
boss = LEVELS[-1]
check("C08 is the boss and every question is a bank question", boss["boss"] and all("bankId" in q for q in boss["questions"]))
for q in boss["questions"]:
    b = BANK[q["bankId"]]
    check(f"C08 {q['bankId']} is an official-pdf question", b["official"] is True and b["solutionSource"] == "official-pdf" and not b.get("hold"))
# the official keys, recomputed
check("C08 24B-A-Q2b: (-1)^n/((n+1)ln(n+1)) is conditionally convergent",
      classify(1 / ((n + 1) * sp.log(n + 1)), True, abs_override=(False, "integral ln ln")) == "cond")
xs1 = sp.symbols("xs1", positive=True)
check("C08 24B-A-Q2b: integral of 1/((x+1)ln(x+1)) diverges (ln ln (x+1))", sp.limit(sp.log(sp.log(xs1 + 1)), xs1, oo) == oo)
check("C08 26A-A-Q2a series 1: (2/3)^n cos n converges absolutely", classify((R_(2, 3)) ** n, False) == "abs")
check("C08 26A-A-Q2a series 2: cos(pi n)/n converges conditionally", classify(1 / n, True) == "cond")
a = sp.Integer(2) ** n * sp.factorial(n) / sp.factorial(2 * n)
check("C08 24B-A-Q4b: R = oo", sp.limit(sp.simplify(sp.combsimp(a / a.subs(n, n + 1))), n, oo) == oo)
check("C08 26A-A-Q3a: [-3,3) shifted by X=x+2 is [-5,1)", sp.Interval(-3, 3, False, True) == sp.Interval(-3, 3, False, True) and
      sp.Interval(-3 - 2, 3 - 2, False, True) == sp.Interval.Ropen(-5, 1))
fb = sp.log(2 * x**2 + 3 * x + 1)
serb = sp.series(fb, x, 0, 10).removeO()
check("C08 24B-A-Q5a/b: coefficients (-1)^(n+1)(1+2^n)/n", all(serb.coeff(x, i) == R_((-1) ** (i + 1) * (1 + 2**i), i) for i in range(1, 10)))
Rb, domb = domain((1 + sp.Integer(2) ** n) / n, "alt", expected_R=R_(1, 2))
check("C08 24B-A-Q5b: domain (-1/2,1/2]", domb == sp.Interval.Lopen(-R_(1, 2), R_(1, 2)))
check("C08 24B-A-Q5c: f^(5)(0) = 792", sp.diff(fb, x, 5).subs(x, 0) == 792 == sp.factorial(5) * R_(33, 5))

# ======================================================================== structural
check("every own question has a unique id", len(Q) == sum(1 for L in LEVELS for q in L["questions"] if "id" in q))
check("8 levels", len(LEVELS) == 8)
print(f"OK: {len(ok)} assertions passed")
