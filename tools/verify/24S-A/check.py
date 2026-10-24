# -*- coding: utf-8 -*-
"""sympy + numeric workings for sitting 24S-A (calculus-2, summer moed, 03/11/2024).
This sitting has NO answer key: every item is held as no-key and routed to the solver.
These are the transcriber's own sympy results, kept for the solver/refuter; they are not a key.
Run: PYTHONUTF8=1 py tools/verify/24S-A/check.py"""
import json, pathlib, math
import sympy as sp
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
R = sp.Rational
x, y, h, t, z = sp.symbols("x y h t z", real=True)
n = sp.symbols("n", integer=True, positive=True)
out = {}

# Q1a
f = y*sp.cos(x*y)
out["Q1a"] = {"grad(1,0)": [str(sp.diff(f, x).subs({x: 1, y: 0})), str(sp.diff(f, y).subs({x: 1, y: 0}))]}
# Q1b
zf = sp.exp(x - y)*sp.sin(x + y)
out["Q1b"] = {"zxx+zyy": str(sp.simplify(sp.diff(zf, x, 2) + sp.diff(zf, y, 2)))}
# Q2a: x y^3/(x^2+y^2)
g = x*y**3/(x**2 + y**2)
r, ph = sp.symbols("r phi", positive=True)
gp = sp.simplify(g.subs({x: r*sp.cos(ph), y: r*sp.sin(ph)}))
out["Q2a"] = {"polar": str(gp), "fx(0,0)": str(sp.limit(g.subs({x: h, y: 0})/h, h, 0)),
              "fy(0,0)": str(sp.limit(g.subs({x: 0, y: h})/h, h, 0)),
              "diff quotient polar": str(sp.simplify(gp/r))}
# Q2b
out["Q2b"] = {"series1 comparison": "|cos n|/(n^5+2)^(1/4) <= 1/n^(5/4)",
              "series2 terms": "(-1)^n/sqrt(n(n+1)) ~ (-1)^n/n"}
# Q3a: sum (x-2)^n/(n 4^n)
out["Q3a"] = {"R": str(sp.limit(((1/(n*4**n))/(1/((n + 1)*4**(n + 1)))), n, sp.oo))}
# Q3b: triangle (0,0),(0,1),(1,1)
f3 = 2*x**2 - 3*y**2 + x*y - 3*x + 8*y
crit = sp.solve([sp.diff(f3, x), sp.diff(f3, y)], [x, y], dict=True)
verts = {"A": (0, 0), "B": (0, 1), "C": (1, 1)}
vals = {k: f3.subs({x: p[0], y: p[1]}) for k, p in verts.items()}
# edges: x=0 (A,B), y=1 (B,C), y=x (A,C)
e1 = sp.solve(sp.diff(f3.subs(x, 0), y), y)
e2 = sp.solve(sp.diff(f3.subs(y, 1), x), x)
e3 = sp.solve(sp.diff(f3.subs(y, x), x), x)
gx = np.linspace(0, 1, 2001)
X, Y = np.meshgrid(gx, gx)
m = Y >= X - 1e-12
fv = (2*X**2 - 3*Y**2 + X*Y - 3*X + 8*Y)[m]
out["Q3b"] = {"interior critical": [{str(k): str(v) for k, v in c.items()} for c in crit], "vertex values": {k: str(v) for k, v in vals.items()},
              "edge x=0 crit y": [str(c) for c in e1], "edge y=1 crit x": [str(c) for c in e2], "edge y=x crit x": [str(c) for c in e3],
              "numeric max": float(fv.max()), "numeric min": float(fv.min())}
# Q4b: f=ln(x+1/y), grad=(1,-16/9)
f4 = sp.log(x + 1/y)
sol = sp.solve([sp.diff(f4, x) - 1, sp.diff(f4, y) + R(16, 9)], [x, y], dict=True)
out["Q4b"] = {"points": [{str(k): str(v) for k, v in s.items()} for s in sol]}
tp = []
for s in sol:
    px, py = s[x], s[y]
    pz = f4.subs({x: px, y: py})
    tp.append({"point": [str(px), str(py)], "f": str(sp.simplify(pz)), "domain ok": bool(px + 1/py > 0)})
out["Q4b"]["tangent plane data"] = tp
# Q5a: 5z^3+3xyz-x^2y^2+1=0 at (1,-1,0)
F = 5*z**3 + 3*x*y*z - x**2*y**2 + 1
pt = {x: 1, y: -1, z: 0}
Fz = sp.diff(F, z).subs(pt)
zx = -sp.diff(F, x).subs(pt)/Fz
zy = -sp.diff(F, y).subs(pt)/Fz
out["Q5a"] = {"F(1,-1,0)": str(F.subs(pt)), "Fz": str(Fz), "zx": str(zx), "zy": str(zy), "zx+zy": str(zx + zy)}
# Q5b: xy(6-x-y)
f5 = x*y*(6 - x - y)
cr = sp.solve([sp.diff(f5, x), sp.diff(f5, y)], [x, y], dict=True)
H = sp.hessian(f5, (x, y))
cls = []
for c in cr:
    Hc = H.subs(c)
    cls.append({"pt": [str(c[x]), str(c[y])], "det": str(Hc.det()), "fxx": str(Hc[0, 0]), "f": str(f5.subs(c))})
out["Q5b"] = cls
(HERE / "workings.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(json.dumps(out, ensure_ascii=True, indent=1))
