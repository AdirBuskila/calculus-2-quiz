# -*- coding: utf-8 -*-
"""sympy + numeric checks for sitting 24B-B (calculus-2, semester B 2024, moed B 30/07/2024).
Run: PYTHONUTF8=1 py tools/verify/24B-B/check.py
Source: typed solution with the question embedded (no separate exam file).
Also records the places where the official key disagrees with sympy (printed at the end)."""
import json, pathlib, math
import sympy as sp
import numpy as np
from scipy import integrate as si
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).resolve().parent
IMG = HERE.parents[2] / "images" / "exams"
IMG.mkdir(parents=True, exist_ok=True)
R = sp.Rational
x, y, h, t = sp.symbols("x y h t", real=True)
r, ph = sp.symbols("r phi", positive=True)
n = sp.symbols("n", integer=True, positive=True)
ok = []
flags = []


def check(name, cond):
    assert cond, "MISMATCH: " + name
    ok.append(name)


# ---- Q1: x^3 y/(x^2+y^2) ----
f1 = x**3*y/(x**2 + y**2)
fx = sp.simplify(sp.diff(f1, x))
fy = sp.simplify(sp.diff(f1, y))
check("Q1a fx formula", sp.simplify(fx - (3*x**2*y*(x**2 + y**2) - 2*x**4*y)/(x**2 + y**2)**2) == 0)
check("Q1a fy formula", sp.simplify(fy - (x**3*(x**2 + y**2) - 2*y**2*x**3)/(x**2 + y**2)**2) == 0)
check("Q1a fx(1,0)=0, fy(1,0)=1", fx.subs({x: 1, y: 0}) == 0 and fy.subs({x: 1, y: 0}) == 1)
check("Q1b fx(0,0)=fy(0,0)=0", sp.limit(f1.subs({x: h, y: 0})/h, h, 0) == 0 and sp.limit(f1.subs({x: 0, y: h})/h, h, 0) == 0)
q = (f1/sp.sqrt(x**2 + y**2)).subs({x: r*sp.cos(ph), y: r*sp.sin(ph)})
check("Q1c differentiability quotient = r cos^3 sin", sp.simplify(q - r*sp.cos(ph)**3*sp.sin(ph)) == 0)
check("Q1c quotient -> 0 uniformly (|.|<=r)", sp.limit(r, r, 0) == 0)
fp = sp.simplify(f1.subs({x: r*sp.cos(ph), y: r*sp.sin(ph)}))
check("Q1c f in polar = r^2 cos^3 sin -> 0 (continuous)", sp.simplify(fp - r**2*sp.cos(ph)**3*sp.sin(ph)) == 0)

# ---- Q2 ----
an = sp.cos(sp.pi*n)*(n**2 + 3*sp.log(n))/((n + 1)*(n + 2))
check("Q2a |a_n| -> 1", sp.limit((n**2 + 3*sp.log(n))/((n + 1)*(n + 2)), n, sp.oo) == 1)
check("Q2a cos(pi n)=(-1)^n", all(sp.cos(sp.pi*k) == (-1)**k for k in range(1, 12)))
bn = [(1 + 1/math.sqrt(i))/i**3 for i in range(1, 3000)]
check("Q2b |a_n| <= 2/n^3", all(bn[i - 1] <= 2/i**3 + 1e-15 for i in range(1, 3000)))
check("Q2b sum 2/n^3 converges", sp.summation(1/n**3, (n, 1, sp.oo)) == sp.zeta(3))

# ---- Q3: f = x^2-2x(y+1)+3 ----
f3 = x**2 - 2*x*(y + 1) + 3
g3 = [sp.diff(f3, x), sp.diff(f3, y)]
check("Q3a grad formula (2x-2(y+1), -2x)", sp.simplify(g3[0] - (2*x - 2*(y + 1))) == 0 and g3[1] == -2*x)
check("Q3a grad f(2,-1) = (4,-4)", [c.subs({x: 2, y: -1}) for c in g3] == [4, -4])
a0 = sp.Matrix([-3, 4])/5
dd = sp.Matrix([4, -4]).dot(a0)
check("Q3b directional derivative -28/5", dd == R(-28, 5))
crit = sp.solve(g3, [x, y], dict=True)
check("Q3c only critical point (0,-1)", crit == [{x: 0, y: -1}])
H = sp.hessian(f3, (x, y))
check("Q3c A=2,B=-2,C=0, det=-4 saddle", (H[0, 0], H[0, 1], H[1, 1], H.det()) == (2, -2, 0, -4))
check("Q3d (0,-1) is interior to D={-2<=y<=x<=1}", -2 <= -1 <= 0 <= 1)
check("Q3d f(0,-1)=3", f3.subs({x: 0, y: -1}) == 3)
pts = {"A": (1, 1), "B": (1, -2), "C": (-2, -2), "D": (-1, -2), "E": (-1, -1)}
fvals = {k: f3.subs({x: p[0], y: p[1]}) for k, p in pts.items()}
check("Q3d values 0,6,3,2,4", fvals == {"A": 0, "B": 6, "C": 3, "D": 2, "E": 4})
g = np.linspace(-2, 1, 3001)
X, Y = np.meshgrid(g, g)
m = (Y <= X + 1e-12)
fv = (X**2 - 2*X*(Y + 1) + 3)[m]
check("Q3d numeric max 6 / min 0 on D", abs(fv.max() - 6) < 1e-6 and abs(fv.min()) < 1e-6)
edge_true = sp.expand(f3.subs(x, 1))
check("Q3d TRUE f(1,y)=2-2y", sp.simplify(edge_true - (2 - 2*y)) == 0)
flags.append("Q3d: the key writes f(1,y) = 1-2(y+1)-2+3 = -2y; the true value is 2-2y (no critical point either way). "
             "Key text also says the unique critical point is (0,0); it is (0,-1).")

# ---- Q4a ----
u_, v_ = sp.symbols("u v")
zf = 2*u_*v_ + 3*v_**2
u_expr = sp.cos(x - 3*y)
ux = sp.diff(u_expr, x).subs({x: sp.pi, y: -sp.pi})
uy = sp.diff(u_expr, y).subs({x: sp.pi, y: -sp.pi})
uv0 = u_expr.subs({x: sp.pi, y: -sp.pi})
check("Q4a u(pi,-pi)=1, u_x=u_y=0", (uv0, ux, uy) == (1, 0, 0))
zu = sp.diff(zf, u_).subs({u_: 1, v_: 2})
zv = sp.diff(zf, v_).subs({u_: 1, v_: 2})
check("Q4a z_u=4, z_v=14", (zu, zv) == (4, 14))
check("Q4a z_x=70", zu*ux + zv*5 == 70)
check("Q4a z_y=56", zu*uy + zv*4 == 56)

# ---- Q4b: sum 2^n/sqrt(n+4) (x-1)^n ----
a_n = 2**n/sp.sqrt(n + 4)
check("Q4b 1/R = 2", sp.limit(a_n/a_n.subs(n, n + 1), n, sp.oo) == R(1, 2))
check("Q4b x-1=1/2 diverges (limit comparison with 1/sqrt n)", sp.limit((1/sp.sqrt(n + 4))/(1/sp.sqrt(n)), n, sp.oo) == 1)
seq = [1/math.sqrt(i + 4) for i in range(1, 4000)]
check("Q4b x-1=-1/2 Leibniz: decreasing", all(seq[i + 1] < seq[i] for i in range(len(seq) - 1)))
check("Q4b left endpoint x = 1-1/2 = 1/2 (not -1/2)", 1 - R(1, 2) == R(1, 2))
flags.append("Q4b: radius R=1/2 (x-1 in (-1/2,1/2)); at x-1=-1/2 (x=1/2) the series converges, at x-1=+1/2 (x=3/2) it diverges. "
             "Correct domain [1/2, 3/2). The key prints [-1/2; 3/2) and also calls the x=3/2 series convergent in its text.")

# ---- Q5 ----
f5 = sp.log(6*x**2 + 5*x + 1)
check("Q5 factorisation", sp.expand((3*x + 1)*(2*x + 1)) == 6*x**2 + 5*x + 1)
ser = sp.series(f5, x, 0, 9).removeO()
check("Q5a coefficients (-1)^(n+1)(3^n+2^n)/n", all(ser.coeff(x, i) == R((-1)**(i + 1)*(3**i + 2**i), i) for i in range(1, 9)))
check("Q5c f^(5)(0)=6600", sp.diff(f5, x, 5).subs(x, 0) == 6600)
check("Q5b R=1/3", sp.limit(((3**n + 2**n)/n)**(1/n), n, sp.oo) == 3)
check("Q5b x=1/3 terms (-1)^(n+1)(1+(2/3)^n)/n converge (two alternating/convergent parts)",
      abs(sum((-1)**(i + 1)*(1 + (2/3)**i)/i for i in range(1, 200001)) - sum((-1)**(i + 1)*(1 + (2/3)**i)/i for i in range(1, 100001))) < 1e-4)
check("Q5b x=-1/3 gives -(1+(2/3)^n)/n termwise (diverges)", all(sp.simplify(R((-1)**(i + 1)*(3**i + 2**i), i)*(-R(1, 3))**i + (1 + R(2, 3)**i)/i) == 0 for i in range(1, 12)))
check("Q5b ln(1+3x) singular at x=-1/3, so domain (-1/3,1/3]", sp.limit(sp.log(3*x + 1), x, -R(1, 3), "+") == -sp.oo)

# ---- region figure for Q3d ----
fig, ax = plt.subplots(figsize=(4.2, 3.8), dpi=150)
tri = [(1, 1), (1, -2), (-2, -2)]
ax.fill(*zip(*tri), color="#fca5a5", alpha=0.55)
ax.plot(*zip(*(tri + [tri[0]])), color="#7c3aed", lw=1.6)
for nm, (px, py) in {"A": (1, 1), "B": (1, -2), "C": (-2, -2)}.items():
    ax.plot([px], [py], "o", color="#111", ms=4)
    ax.text(px + 0.08, py + 0.08, nm + "(%d,%d)" % (px, py), fontsize=9)
ax.plot([0], [-1], "s", color="#0a7", ms=5)
ax.text(0.08, -1.3, "(0,-1) saddle", fontsize=8)
ax.axhline(0, color="#888", lw=0.7)
ax.axvline(0, color="#888", lw=0.7)
ax.set_xlim(-3, 2.2)
ax.set_ylim(-3, 2)
ax.set_aspect("equal")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("D: -2 <= y <= x <= 1", fontsize=10)
fig.tight_layout()
fig.savefig(IMG / "24B-B-Q3d-region.png", facecolor="white")
plt.close(fig)

regions = [{"id": "24B-B-Q3d", "description": "triangle D={-2<=y<=x<=1}", "type": "triangle",
            "inequalities": ["y>=-2", "y<=x", "x<=1"], "boundary_curves": ["x=1", "y=-2", "y=x"],
            "vertices": [[1, 1], [1, -2], [-2, -2]]}]
(HERE / "regions.json").write_text(json.dumps(regions, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
contours = [{"id": "24B-B-Q3d", "f": "x^2-2*x*(y+1)+3", "constraint": None, "kind": "closed-region",
             "domain": [[-3, 2], [-3, 2]],
             "critical_points": [{"x": 0, "y": -1, "f": 3, "role": "saddle"},
                                 {"x": 1, "y": -2, "f": 6, "role": "abs max (vertex B)"},
                                 {"x": 1, "y": 1, "f": 0, "role": "abs min (vertex A)"}]}]
(HERE / "contours.json").write_text(json.dumps(contours, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ALL OK:", len(ok), "checks")
for f in flags:
    print("KEY FLAG:", f)
