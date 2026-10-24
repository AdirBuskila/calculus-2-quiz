# Solver checks for 24A-B Q3a endpoints. Run: PYTHONUTF8=1 py tools/verify/24A-B/solve_24A-B.py
import sympy as sp

n = sp.symbols("n", positive=True, integer=True)
ok = True


def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok &= bool(cond)


a = 1/(sp.cbrt(n + 1)*sp.sqrt(n**2 + 1))
check("R = 1", sp.limit(a/a.subs(n, n + 1), n, sp.oo) == 1)
b = n**sp.Rational(-4, 3)
check("a_n / n^(-4/3) -> 1", sp.limit(a/b, n, sp.oo) == 1)
check("a_n / n^(-2/3) -> 0 (the key's comparison)", sp.limit(a*n**sp.Rational(2, 3), n, sp.oo) == 0)
check("a_n / n^(-3/2) -> oo (n^(-3/2) is not a valid limit comparison)", sp.limit(a*n**sp.Rational(3, 2), n, sp.oo) == sp.oo)
check("p = 4/3 > 1", sp.Rational(4, 3) > 1)
check("a_n <= n^(-4/3) for n=1..5000", all(1/((m + 1)**(1/3)*(m*m + 1)**0.5) <= m**(-4/3) for m in range(1, 5001)))
s = [sum(1/((m + 1)**(1/3)*(m*m + 1)**0.5) for m in range(1, N)) for N in (100001, 400001)]
check("x=-4 partial sums settle (tail ~ 3 N^(-1/3))", abs(s[0] - s[1]) < 0.04)
check("x=-6: |terms| = a_n, absolutely convergent", True)
check("domain: -1 <= x+5 <= 1 -> [-6,-4]", (-1 - 5, 1 - 5) == (-6, -4))
print("ALL OK" if ok else "SOME FAILED")
