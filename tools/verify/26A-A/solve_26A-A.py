# Solver checks for 26A-A Q3b (chain-rule identity). Run: PYTHONUTF8=1 py tools/verify/26A-A/solve_26A-A.py
import sympy as sp
import random

u, v = sp.symbols("u v", positive=True)
X, Y = sp.symbols("x y")
ok = True


def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok &= bool(cond)


x = sp.sqrt(u*v); y = 1/v
Z = sp.exp(X**2*Y)
z = Z.subs({X: x, Y: y})
lhs = sp.simplify(u*sp.diff(z, u) - v*sp.diff(z, v))
check("z = e^u (x^2 y = u)", sp.simplify(z - sp.exp(u)) == 0)
check("u z_u - v z_v = z x^2/v", sp.simplify(lhs - z*x**2/v) == 0)
check("u z_u - v z_v != z x^2/v^2 (key's last line)", sp.simplify(lhs - z*x**2/v**2) != 0)
# key's chain-rule pieces
check("x_u = v/(2 sqrt(uv))", sp.simplify(sp.diff(x, u) - v/(2*sp.sqrt(u*v))) == 0)
check("x_v = u/(2 sqrt(uv))", sp.simplify(sp.diff(x, v) - u/(2*sp.sqrt(u*v))) == 0)
check("y_v = -1/v^2", sp.diff(y, v) == -1/v**2)
# key's penultimate line: x^2 v e^{x^2y} / v^2 = e^{x^2y} x^2 / v
pen = (X**2*v*Z/v**2).subs({X: x, Y: y})
check("x^2 v e/v^2 simplifies to e x^2/v", sp.simplify(pen - z*x**2/v) == 0)
# numeric spot check
for _ in range(5):
    uu, vv = random.uniform(0.2, 3), random.uniform(0.2, 3)
    a = float(lhs.subs({u: uu, v: vv})); b = float((z*x**2/v).subs({u: uu, v: vv}))
    check(f"numeric u={uu:.2f} v={vv:.2f}", abs(a - b) < 1e-9*max(1, abs(b)))
print("ALL OK" if ok else "SOME FAILED")
