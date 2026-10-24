# Solver checks for 24B-B Q3d and Q4b. Run: PYTHONUTF8=1 py tools/verify/24B-B/solve_24B-B.py
import numpy as np
import sympy as sp

x, y = sp.symbols("x y", real=True)
n = sp.symbols("n", positive=True, integer=True)
ok = True


def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok &= bool(cond)


# ---- Q3d: f = x^2 - 2x(y+1) + 3 on D = {-2 <= y <= x <= 1}
f = x**2 - 2*x*(y + 1) + 3
crit = sp.solve([sp.diff(f, x), sp.diff(f, y)], [x, y], dict=True)
check("only critical point (0,-1)", crit == [{x: 0, y: -1}])
check("(0,-1) inside D", -2 <= -1 <= 0 <= 1)
check("f(1,y) = 2-2y", sp.expand(f.subs(x, 1) - (2 - 2*y)) == 0)
check("f(x,-2) = x^2+2x+3", sp.expand(f.subs(y, -2) - (x**2 + 2*x + 3)) == 0)
check("f(x,x) = -x^2-2x+3", sp.expand(f.subs(y, x) - (-x**2 - 2*x + 3)) == 0)
pts = {"A": (1, 1), "B": (1, -2), "C": (-2, -2), "D": (-1, -2), "E": (-1, -1), "P": (0, -1)}
vals = {k: f.subs({x: a, y: b}) for k, (a, b) in pts.items()}
print(vals)
check("values A0 B6 C3 D2 E4 P3", vals == {"A": 0, "B": 6, "C": 3, "D": 2, "E": 4, "P": 3})
xs = np.linspace(-2, 1, 1501)
X, Y = np.meshgrid(xs, xs)
F = X**2 - 2*X*(Y + 1) + 3
F = np.where(Y <= X, F, np.nan)
check("grid max 6", abs(np.nanmax(F) - 6) < 1e-9)
check("grid min 0", abs(np.nanmin(F)) < 1e-9)

# ---- Q4b: sum 2^n/sqrt(n+4) (x-1)^n
a = 2**n/sp.sqrt(n + 4)
check("1/R = 2, R = 1/2", sp.limit(a.subs(n, n + 1)/a, n, sp.oo) == 2)
check("x=1/2: term = (-1)^n/sqrt(n+4)", sp.simplify(a*sp.Rational(-1, 2)**n - (-1)**n/sp.sqrt(n + 4)) == 0)
check("x=3/2: term = 1/sqrt(n+4)", sp.simplify(a*sp.Rational(1, 2)**n - 1/sp.sqrt(n + 4)) == 0)
check("limit comparison with 1/sqrt n = 1", sp.limit((1/sp.sqrt(n + 4))/(1/sp.sqrt(n)), n, sp.oo) == 1)
check("1 - 1/2 = 1/2 (left endpoint), 1 + 1/2 = 3/2", (1 - sp.Rational(1, 2), 1 + sp.Rational(1, 2)) == (sp.Rational(1, 2), sp.Rational(3, 2)))
s = sum(1/np.sqrt(m + 4) for m in range(1, 1000001))
check("x=3/2 partial sum diverges (S_1e6 > 1900)", s > 1900)
alt = [sum((-1)**m/np.sqrt(m + 4) for m in range(1, N)) for N in (100001, 200001)]
check("x=1/2 partial sums settle", abs(alt[0] - alt[1]) < 5e-3)
print("ALL OK" if ok else "SOME FAILED")
