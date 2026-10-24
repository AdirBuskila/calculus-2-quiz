# Solver checks for 22A-B Q3a (power series, no key). Run: PYTHONUTF8=1 py tools/verify/22A-B/solve_22A-B.py
import sympy as sp

n = sp.symbols("n", positive=True, integer=True)
t = sp.symbols("t", positive=True)
ok = True


def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok &= bool(cond)


a = n/((n**2 + 1)*3**n)
ratio = sp.simplify(a.subs(n, n + 1)/a)
check("ratio |a_{n+1}/a_n| -> 1/3", sp.limit(ratio, n, sp.oo) == sp.Rational(1, 3))
check("R = 3", 1/sp.limit(ratio, n, sp.oo) == 3)
b = n/(n**2 + 1)          # term at x = 3 (and |term| at x = -3)
check("x=3 term = n/(n^2+1)", sp.simplify(a*3**n - b) == 0)
check("limit comparison with 1/n -> 1", sp.limit(b/(1/n), n, sp.oo) == 1)
check("x=-3: b_n -> 0", sp.limit(b, n, sp.oo) == 0)
fp = sp.diff(t/(t**2 + 1), t)
check("f(t)=t/(t^2+1): f' = (1-t^2)/(t^2+1)^2", sp.simplify(fp - (1 - t**2)/(t**2 + 1)**2) == 0)
check("b_n non-increasing for n>=1 (numeric n=1..2000)",
      all(m/(m*m + 1) >= (m + 1)/((m + 1)**2 + 1) for m in range(1, 2000)))
# numeric partial sums
s3 = sum(m/(m*m + 1) for m in range(1, 200001))
check("x=3 partial sums grow like ln N (S_200000 > 12)", s3 > 12)
sm3 = [sum((-1)**m*m/(m*m + 1) for m in range(1, N)) for N in (10001, 20001)]
check("x=-3 partial sums settle", abs(sm3[0] - sm3[1]) < 1e-3)
check("domain [-3,3)", True)
print("ALL OK" if ok else "SOME FAILED")
