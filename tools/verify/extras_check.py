# -*- coding: utf-8 -*-
"""sympy checks for the calculus-2 "extra" data: every region and every contour spec the app draws.

Sources: tools/verify/<CODE>/regions.json and contours.json (written by each sitting's check.py), plus any
inline ```region / ```contour fence (JSON body) in tools/raw/*.json, docs/briefs/*.md and the
data-region / data-contour hooks in courses/*/*.js. A fence or hook whose body is just an id refers to an
entry of the verify files and is checked there.

Regions (tools/RAW_SCHEMA.md, "Region and contour diagrams"):
  - every order of integration given (orderXY / orderYX, with `pieces`), the polar description and the
    u,v substitution gives the SAME area, exactly (sympy), and that area matches a numeric area of the
    `inequalities` (fine grid) and `area` when given;
  - each description describes the same SET as the inequalities (random points: membership agrees);
  - with a numeric integrand and a `value`: every description integrates to `value` (scipy quadrature,
    sympy for the u,v form when it finds a closed form);
  - substitution: |d(x,y)/d(u,v)| * |d(u,v)/d(x,y)| == 1 exactly, and the region maps into the u,v box;
  - vertices satisfy every inequality and lie on two boundary curves.
Contours:
  - f(point) equals the stated f (exactly when both are exact);
  - an interior point has grad f = 0 exactly; a point on the constraint (lagrange) or on one edge of a
    closed region satisfies the Lagrange system (grad f parallel to grad g, grad g != 0); a corner is a corner;
  - the classification is the Hessian's (saddle / local max / local min); an "abs max/min" equals the
    max/min of f over the feasible set (dense sampling) and every stated f is within it.
  - completeness (warning only): a polynomial f's real critical points inside `domain` all appear.

Run: PYTHONUTF8=1 py tools/verify/extras_check.py      (exit 1 on any failure; ASCII output)
"""
import json, math, pathlib, re, sys
import numpy as np
import sympy as sp
from scipy import integrate as si

HERE = pathlib.Path(__file__).resolve().parent
APP = HERE.parent.parent
x, y, u, v = sp.symbols("x y u v", real=True)
r, th = sp.symbols("r theta", real=True)
LOC = {"x": x, "y": y, "r": r, "theta": th, "e": sp.E, "pi": sp.pi, "ln": sp.log, "u": u, "v": v,
       "atan": sp.atan, "arctan": sp.atan, "sqrt": sp.sqrt, "exp": sp.exp, "log": sp.log}
fails, warns, oks = [], [], []
RNG = np.random.default_rng(7)


def P(s):
    return sp.parse_expr(str(s).replace("^", "**"), local_dict=LOC)


def num(s):
    return float(sp.N(P(s), 30))


def fail(w, m):
    fails.append(f"{w}: {m}")


def ok(w, m):
    oks.append(f"{w}: {m}")


OPS = ("<=", ">=", "<", ">")


def ineq(s):
    """'lhs op rhs' -> (g, sense) meaning g >= 0 (sense ignored: strictness does not matter here)."""
    s = re.sub(r"\(\s*[A-Za-z][A-Za-z ]*\)\s*$", "", str(s)).strip()   # "x^2+y^2<=2 (closed disk)"
    for op in OPS:
        if op in s:
            a, b = s.split(op, 1)
            return (P(b) - P(a)) if op[0] == "<" else (P(a) - P(b))
    raise ValueError(f"not an inequality: {s}")


def curve(s):
    a, b = str(s).split("=", 1)
    return P(a) - P(b)


def split_top(s):
    out, d, cur = [], 0, ""
    for ch in s:
        if ch == "(":
            d += 1
        elif ch == ")":
            d -= 1
        if ch == "," and d == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [p.strip() for p in out if p.strip()]


def lam(e, vars_=(x, y)):
    return sp.lambdify(vars_, e, modules="numpy")


def as_arr(fn, X, Y):
    with np.errstate(all="ignore"):
        z = fn(X, Y)
    return np.broadcast_to(np.asarray(z, dtype=float), np.shape(X))


def region_pred(gs):
    fns = [lam(g) for g in gs]

    def pred(X, Y, tol=0.0):
        m = np.ones(np.shape(X), dtype=bool)
        for f in fns:
            m &= as_arr(f, X, Y) >= -tol
        return m
    return pred


def bbox(pred, box=(-12, 12, -12, 12), n=481):
    for _ in range(3):
        xs, ys = np.linspace(box[0], box[1], n), np.linspace(box[2], box[3], n)
        X, Y = np.meshgrid(xs, ys)
        m = pred(X, Y)
        if not m.any():
            return None
        px, py = X[m], Y[m]
        hx, hy = (box[1] - box[0]) / (n - 1), (box[3] - box[2]) / (n - 1)
        box = (px.min() - 2 * hx, px.max() + 2 * hx, py.min() - 2 * hy, py.max() + 2 * hy)
    return box


# ---------------------------------------------------------------- orders of integration
def order_parts(o):
    """orderXY/orderYX object -> list of (outer, (a, b), inner, (g1, g2)) with sympy bounds."""
    pieces = o["pieces"] if "pieces" in o else [o]
    out = []
    for pc in pieces:
        keys = [k for k in pc if k in ("x", "y")]
        if sorted(keys) != ["x", "y"]:
            raise ValueError("an order needs x and y bounds")
        bx, by = [P(t) for t in pc["x"]], [P(t) for t in pc["y"]]
        x_const = not any(b.has(y) for b in bx)
        y_const = not any(b.has(x) for b in by)
        if x_const:
            outer = "x"
        elif y_const:
            outer = "y"
        else:
            raise ValueError("neither variable has constant bounds")
        # both constant (a rectangle): either order; take x outer
        out.append(("x", bx, "y", by) if outer == "x" else ("y", by, "x", bx))
    return out


def order_area_exact(parts):
    tot = 0
    for outer, (a, b), inner, (g1, g2) in parts:
        o, i = (x, y) if outer == "x" else (y, x)
        tot += sp.integrate(sp.integrate(1, (i, g1, g2)), (o, a, b))
    return sp.simplify(tot)


def order_member(parts, X, Y):
    m = np.zeros(np.shape(X), dtype=bool)
    for outer, (a, b), inner, (g1, g2) in parts:
        O, I = (X, Y) if outer == "x" else (Y, X)
        ov = sp.Symbol(outer, real=True)
        lo, hi = lam(g1, (ov,)), lam(g2, (ov,))
        with np.errstate(all="ignore"):
            L = np.broadcast_to(np.asarray(lo(O), dtype=float), O.shape)
            H = np.broadcast_to(np.asarray(hi(O), dtype=float), O.shape)
        m |= (O >= float(a)) & (O <= float(b)) & (I >= L) & (I <= H)
    return m


def order_integral(parts, fxy):
    tot = 0.0
    f = lam(fxy)
    for outer, (a, b), inner, (g1, g2) in parts:
        ov = sp.Symbol(outer, real=True)
        lo, hi = lam(g1, (ov,)), lam(g2, (ov,))
        if outer == "x":
            val = si.dblquad(lambda yy, xx: f(xx, yy), float(a), float(b), lambda xx: float(lo(xx)), lambda xx: float(hi(xx)), epsabs=1e-11, epsrel=1e-11)[0]
        else:
            val = si.dblquad(lambda xx, yy: f(xx, yy), float(a), float(b), lambda yy: float(lo(yy)), lambda yy: float(hi(yy)), epsabs=1e-11, epsrel=1e-11)[0]
        tot += val
    return tot


def polar_member(pol, X, Y):
    (r1, r2), (t1, t2) = [P(t) for t in pol["r"]], [P(t) for t in pol["theta"]]
    R = np.hypot(X, Y)
    T0 = np.arctan2(Y, X)
    a, b = float(t1), float(t2)
    lo, hi = lam(r1, (th,)), lam(r2, (th,))
    m = np.zeros(np.shape(X), dtype=bool)
    for k in (-1, 0, 1):
        T = T0 + 2 * math.pi * k
        with np.errstate(all="ignore"):
            L = np.broadcast_to(np.asarray(lo(T), dtype=float), T.shape)
            H = np.broadcast_to(np.asarray(hi(T), dtype=float), T.shape)
        m |= (T >= a) & (T <= b) & (R >= L) & (R <= H)
    return m


def check_region(w, spec):
    try:
        gs = [ineq(s) for s in spec["inequalities"]]
    except Exception as e:
        return fail(w, f"inequalities do not parse ({e})")
    pred = region_pred(gs)
    box = bbox(pred)
    if box is None:
        return fail(w, "the inequalities describe an empty set")
    # numeric area of the inequality set (midpoint grid)
    n = 2400
    xs = np.linspace(box[0], box[1], n + 1)
    ys = np.linspace(box[2], box[3], n + 1)
    xc, yc = (xs[:-1] + xs[1:]) / 2, (ys[:-1] + ys[1:]) / 2
    X, Y = np.meshgrid(xc, yc)
    M = pred(X, Y)
    cell = (xs[1] - xs[0]) * (ys[1] - ys[0])
    a_num = M.sum() * cell
    pts = np.column_stack([RNG.uniform(box[0], box[1], 60000), RNG.uniform(box[2], box[3], 60000)])
    inside = pred(pts[:, 0], pts[:, 1])
    areas = {}
    fxy = None
    integrand = spec.get("integrand")
    if integrand and "f(" not in integrand:
        fxy = P(integrand)
    value = P(spec["value"]) if spec.get("value") not in (None, "") else None
    integrals = {}

    def agree(name, member):
        bad = np.count_nonzero(member != inside)
        if bad > 0.004 * len(inside):
            fail(w, f"{name} does not describe the same set as the inequalities ({bad} of {len(inside)} sample points disagree)")
        else:
            ok(w, f"{name} = inequality set ({bad} boundary disagreements)")

    for key in ("orderXY", "orderYX"):
        if key not in spec:
            continue
        try:
            parts = order_parts(spec[key])
        except Exception as e:
            fail(w, f"{key} does not parse ({e})")
            continue
        areas[key] = order_area_exact(parts)
        agree(key, order_member(parts, pts[:, 0], pts[:, 1]))
        if fxy is not None:
            integrals[key] = order_integral(parts, fxy)
    if "polar" in spec:
        pol = spec["polar"]
        (r1, r2), (t1, t2) = [P(t) for t in pol["r"]], [P(t) for t in pol["theta"]]
        areas["polar"] = sp.simplify(sp.integrate(sp.integrate(r, (r, r1, r2)), (th, t1, t2)))
        agree("polar", polar_member(pol, pts[:, 0], pts[:, 1]))
        if fxy is not None:
            g = lam(fxy.subs({x: r * sp.cos(th), y: r * sp.sin(th)}) * r, (r, th))
            lo, hi = lam(r1, (th,)), lam(r2, (th,))
            integrals["polar"] = si.dblquad(lambda rr, tt: g(rr, tt), float(t1), float(t2), lambda tt: float(lo(tt)), lambda tt: float(hi(tt)), epsabs=1e-11, epsrel=1e-11)[0]
    if "substitution" in spec:
        sb = spec["substitution"]
        U, V = P(sb["u"]), P(sb["v"])
        J = P(sb["abs_jacobian_xy_over_uv"])
        D = sp.Matrix([[sp.diff(U, x), sp.diff(U, y)], [sp.diff(V, x), sp.diff(V, y)]]).det()
        if sp.simplify((J * D) ** 2 - 1) != 0:
            fail(w, f"|d(x,y)/d(u,v)| = {J} is not 1/|d(u,v)/d(x,y)| = 1/|{D}|")
        else:
            ok(w, "Jacobian exact")
        (u1, u2), (v1, v2) = [P(t) for t in sb["u_range"]], [P(t) for t in sb["v_range"]]
        Uf, Vf = lam(U), lam(V)
        uu, vv = as_arr(Uf, pts[:, 0], pts[:, 1]), as_arr(Vf, pts[:, 0], pts[:, 1])
        inbox = (uu >= float(u1)) & (uu <= float(u2)) & (vv >= float(v1)) & (vv <= float(v2))
        bad = np.count_nonzero(inside & ~inbox)
        if bad > 0.004 * len(inside):
            fail(w, f"{bad} region points map outside the u,v box")
        else:
            ok(w, "region maps into the u,v box")
        # x,y as functions of u,v: pick the branch that lands in the region
        try:
            sols = sp.solve([U - u, V - v], [x, y], dict=True)
        except Exception:
            sols = []
        uc, vc = (float(u1) + float(u2)) / 2, (float(v1) + float(v2)) / 2
        good = None
        for s in sols:
            try:
                xv, yv = complex(s[x].subs({u: uc, v: vc})), complex(s[y].subs({u: uc, v: vc}))
            except Exception:
                continue
            if abs(xv.imag) < 1e-12 and abs(yv.imag) < 1e-12 and pred(np.array([xv.real]), np.array([yv.real]), 1e-9)[0]:
                good = s
                break
        if good is None:
            warns.append(f"{w}: no x(u,v), y(u,v) branch found; u,v integral not checked")
            areas_uv = None
        else:
            Juv = sp.simplify(J.subs({x: good[x], y: good[y]}))
            areas_uv = sp.simplify(sp.integrate(Juv, (u, u1, u2), (v, v1, v2)))
            areas["substitution"] = areas_uv
            if fxy is not None:
                F = sp.simplify(fxy.subs({x: good[x], y: good[y]}, simultaneous=True) * Juv)
                ex = sp.integrate(F, (u, u1, u2), (v, v1, v2))
                if value is not None and not ex.has(sp.Integral) and sp.simplify(ex - value) == 0:
                    ok(w, "u,v integral = value exactly")
                Fl = lam(F, (u, v))
                integrals["substitution"] = si.dblquad(lambda vv_, uu_: Fl(uu_, vv_), float(u1), float(u2), float(v1), float(v2), epsabs=1e-11, epsrel=1e-11)[0]
    if "area" in spec:
        areas["area"] = P(spec["area"])
    # every exact area equal; and equal to the numeric inequality area
    ks = list(areas)
    for k in ks[1:]:
        if sp.simplify(areas[k] - areas[ks[0]]) != 0:
            fail(w, f"area by {k} = {areas[k]} != area by {ks[0]} = {areas[ks[0]]}")
    for k in ks:
        av = float(sp.N(areas[k]))
        if abs(av - a_num) > 3e-3 * max(1.0, abs(av)):
            fail(w, f"area by {k} = {av:.6f} but the inequalities give {a_num:.6f}")
    if ks:
        ok(w, f"areas agree ({', '.join(ks)}) = {areas[ks[0]]}")
    if fxy is not None and value is not None:
        vn = float(sp.N(value))
        for k, iv in integrals.items():
            if abs(iv - vn) > 1e-7 * max(1.0, abs(vn)):
                fail(w, f"integral by {k} = {iv:.10f} != value {spec['value']} = {vn:.10f}")
        if integrals:
            ok(w, f"integral = {spec['value']} by {', '.join(integrals)}")
        # and by the inequalities directly (grid)
        Fg = as_arr(lam(fxy), X, Y)
        ig = float(np.where(M, Fg, 0).sum() * cell)
        if abs(ig - vn) > 5e-3 * max(1.0, abs(vn)):
            fail(w, f"grid integral over the inequalities {ig:.5f} != value {vn:.5f}")
    elif value is not None and fxy is None:
        warns.append(f"{w}: value given but the integrand is symbolic; not checked")
    if not any(k in spec for k in ("orderXY", "orderYX", "polar", "substitution")):
        warns.append(f"{w}: no order / polar / substitution bounds; only the inequalities are drawn")
    # vertices
    curves = [curve(c) for c in spec.get("boundary_curves", [])]
    for vx in spec.get("vertices", []):
        px, py = P(vx[0]), P(vx[1])
        vals = [float(sp.N(g.subs({x: px, y: py}))) for g in gs]
        if min(vals) < -1e-9:
            fail(w, f"vertex ({vx[0]}, {vx[1]}) violates an inequality")
        on = sum(1 for c in curves if abs(float(sp.N(c.subs({x: px, y: py})))) < 1e-9)
        if curves and on < 2:
            fail(w, f"vertex ({vx[0]}, {vx[1]}) lies on {on} boundary curve(s), not 2")
    if spec.get("vertices"):
        ok(w, f"{len(spec['vertices'])} vertices on the boundary")
    for c in spec.get("boundary_curves", []):
        try:
            curve(c)
        except Exception as e:
            fail(w, f"boundary curve {c!r} does not parse ({e})")


# ---------------------------------------------------------------- contours
def norm_kind(k):
    k = str(k or "unconstrained").replace("-", "_")
    return k


def role_class(role):
    s = str(role).lower()
    if "saddle" in s:
        return "saddle"
    if "max" in s:
        return "absmax" if ("abs" in s or "global" in s) else "localmax"
    if "min" in s:
        return "absmin" if ("abs" in s or "global" in s) else "localmin"
    return "other"


def is_zero(e):
    e = sp.nsimplify(e) if isinstance(e, sp.Float) else e
    z = sp.simplify(e)
    if z == 0:
        return True
    try:
        return abs(complex(sp.N(z, 40))) < 1e-25
    except Exception:
        return False


def check_contour(w, spec, regions_by_id):
    try:
        f = P(spec["f"])
    except Exception as e:
        return fail(w, f"f does not parse ({e})")
    kind = norm_kind(spec.get("kind"))
    if kind not in ("unconstrained", "lagrange", "closed_region"):
        return fail(w, f"unknown kind {spec.get('kind')!r}")
    (x0, x1), (y0, y1) = [[num(t) for t in d] for d in spec["domain"]]
    fx, fy = sp.diff(f, x), sp.diff(f, y)
    H = sp.hessian(f, (x, y))
    g = None
    gs = []
    cons = spec.get("constraint")
    if kind == "lagrange":
        if not cons or "=" not in cons or any(o in cons for o in OPS):
            return fail(w, "a lagrange spec needs an equality constraint g=c")
        g = curve(re.sub(r"\(\s*[A-Za-z][A-Za-z ]*\)\s*$", "", cons))
    if kind == "closed_region":
        reg = spec.get("region")
        if reg is None and cons and any(o in cons for o in OPS):
            reg = cons
        if reg is None and w in regions_by_id:
            reg = regions_by_id[w]["inequalities"]
        if reg is None:
            return fail(w, "closed_region needs `region` (or an inequality constraint, or a regions.json entry with this id)")
        gs = [ineq(s) for s in (split_top(reg) if isinstance(reg, str) else reg)]
    pts = spec.get("critical_points") or []
    if not pts:
        return fail(w, "no critical points")
    fvals = []
    for cp in pts:
        pw = f"{w} ({cp['x']}, {cp['y']})"
        px, py = P(cp["x"]), P(cp["y"])
        sub = {x: px, y: py}
        fv = f.subs(sub)
        given = P(cp["f"])
        exact_given = not isinstance(cp["f"], float)
        if exact_given and not isinstance(px, sp.Float) and not isinstance(py, sp.Float) and not (isinstance(cp["x"], float) or isinstance(cp["y"], float)):
            if not is_zero(fv - given):
                fail(pw, f"f = {sp.simplify(fv)}, data says {cp['f']}")
        elif abs(float(sp.N(fv - given))) > 1e-9 * max(1, abs(float(given))):
            fail(pw, f"f = {float(sp.N(fv))}, data says {cp['f']}")
        fvals.append(float(sp.N(fv)))
        gx, gy = fx.subs(sub), fy.subs(sub)
        rc = role_class(cp.get("role"))
        if kind == "closed_region":
            vals = [float(sp.N(h.subs(sub))) for h in gs]
            if min(vals) < -1e-9:
                fail(pw, "point is outside the closed region")
                continue
            active = [h for h in gs if is_zero(h.subs(sub))]
        elif kind == "lagrange":
            active = [g] if is_zero(g.subs(sub)) else []
        else:
            active = []
        if not active:
            if not (is_zero(gx) and is_zero(gy)):
                fail(pw, f"interior point but grad f = ({sp.simplify(gx)}, {sp.simplify(gy)}) != 0")
                continue
            D = sp.simplify((H[0, 0] * H[1, 1] - H[0, 1] ** 2).subs(sub))
            fxx = sp.simplify(H[0, 0].subs(sub))
            Dn, fxxn = float(sp.N(D)), float(sp.N(fxx))
            hes = "saddle" if Dn < -1e-12 else ("max" if Dn > 1e-12 and fxxn < 0 else ("min" if Dn > 1e-12 and fxxn > 0 else "degenerate"))
            want = {"saddle": "saddle", "localmax": "max", "localmin": "min"}.get(rc)
            if kind == "unconstrained" and want and hes != "degenerate" and hes != want:
                fail(pw, f"role {cp.get('role')!r} but the Hessian says {hes} (D={D}, fxx={fxx})")
            elif kind == "unconstrained" and want and hes == "degenerate":
                warns.append(f"{pw}: Hessian test inconclusive (D=0); role {cp.get('role')!r} not checked")
            ok(pw, f"grad f = 0; Hessian {hes}")
        elif len(active) == 1:
            h = active[0]
            hx, hy = sp.diff(h, x).subs(sub), sp.diff(h, y).subs(sub)
            if is_zero(hx) and is_zero(hy):
                fail(pw, "grad g = 0 at the point (Lagrange does not apply)")
            elif not is_zero(gx * hy - gy * hx):
                fail(pw, f"Lagrange system fails: grad f = ({sp.simplify(gx)}, {sp.simplify(gy)}) not parallel to grad g = ({sp.simplify(hx)}, {sp.simplify(hy)})")
            else:
                ok(pw, "Lagrange system holds")
        else:
            ok(pw, f"corner of the region ({len(active)} active constraints)")
    # abs max / min against dense sampling of the feasible set
    n = 900
    X, Y = np.meshgrid(np.linspace(x0, x1, n), np.linspace(y0, y1, n))
    F = as_arr(lam(f), X, Y)
    if kind == "closed_region":
        M = region_pred(gs)(X, Y)
        samp = F[M]
    elif kind == "lagrange":
        Gv = as_arr(lam(g), X, Y)
        sw = np.sign(Gv[:, :-1]) != np.sign(Gv[:, 1:])
        t = Gv[:, :-1] / (Gv[:, :-1] - Gv[:, 1:] + 1e-300)
        XX = X[:, :-1] + t * (X[:, 1:] - X[:, :-1])
        fl = lam(f)
        samp = as_arr(fl, XX[sw], Y[:, :-1][sw])
        sw2 = np.sign(Gv[:-1, :]) != np.sign(Gv[1:, :])
        t2 = Gv[:-1, :] / (Gv[:-1, :] - Gv[1:, :] + 1e-300)
        YY = Y[:-1, :] + t2 * (Y[1:, :] - Y[:-1, :])
        samp = np.concatenate([samp, as_arr(fl, X[:-1, :][sw2], YY[sw2])])
    else:
        samp = None
    if samp is not None and samp.size:
        # the data's own (verified feasible) points join the sample: a grid misses boundary extremes
        lo, hi = min(float(np.min(samp)), min(fvals)), max(float(np.max(samp)), max(fvals))
        scale = max(1.0, hi - lo)
        for cp, fv in zip(pts, fvals):
            rc = role_class(cp.get("role"))
            if rc == "absmax" and abs(fv - hi) > 2e-3 * scale:
                fail(f"{w} ({cp['x']}, {cp['y']})", f"called abs max (f={fv}) but f reaches {hi:.6f} on the feasible set")
            if rc == "absmin" and abs(fv - lo) > 2e-3 * scale:
                fail(f"{w} ({cp['x']}, {cp['y']})", f"called abs min (f={fv}) but f reaches {lo:.6f} on the feasible set")
            if fv > hi + 2e-3 * scale or fv < lo - 2e-3 * scale:
                fail(f"{w} ({cp['x']}, {cp['y']})", f"f={fv} is outside the sampled range [{lo:.4f}, {hi:.4f}]")
        ok(w, f"abs extrema match sampling (range [{lo:.4f}, {hi:.4f}])")
    # completeness (warning)
    if f.is_polynomial(x, y):
        try:
            sols = sp.solve([fx, fy], [x, y], dict=True)
            have = [(num(cp["x"]), num(cp["y"])) for cp in pts]
            for s in sols:
                if x not in s or y not in s:
                    continue
                cx, cy = complex(sp.N(s[x])), complex(sp.N(s[y]))
                if abs(cx.imag) > 1e-12 or abs(cy.imag) > 1e-12:
                    continue
                cx, cy = cx.real, cy.real
                if not (x0 <= cx <= x1 and y0 <= cy <= y1):
                    continue
                if kind == "closed_region" and not region_pred(gs)(np.array([cx]), np.array([cy]), 1e-9)[0]:
                    continue
                if kind == "lagrange":
                    continue   # interior points of a constraint problem need not be drawn
                if not any(abs(cx - a) < 1e-7 and abs(cy - b) < 1e-7 for a, b in have):
                    warns.append(f"{w}: critical point ({cx:.4g}, {cy:.4g}) of f is not in the data")
        except Exception:
            pass


# ---------------------------------------------------------------- inline specs
FENCE = re.compile(r"```(region|contour)[ \t]*\n(.*?)\n```", re.S)
HOOK = re.compile(r"""data-(region|contour)=(['"])(.*?)\2""", re.S)


def inline_specs():
    out = []
    srcs = list((APP / "tools" / "raw").glob("*.json")) + list((APP / "docs" / "briefs").glob("*.md"))
    for fp in srcs:
        if fp.name.startswith("_"):
            continue
        text = fp.read_text(encoding="utf-8")
        if fp.suffix == ".json":
            try:
                text = _strings(json.loads(text))
            except Exception:
                continue
        for m in FENCE.finditer(text):
            out.append((f"{fp.name} {m.group(1)} fence", m.group(1), m.group(2).strip()))
    for fp in (APP / "courses").glob("*/*.js"):
        import html as _h
        for m in HOOK.finditer(fp.read_text(encoding="utf-8")):
            out.append((f"{fp.parent.name}/{fp.name} data-{m.group(1)}", m.group(1), _h.unescape(m.group(3)).strip()))
    return out


def _strings(o):
    if isinstance(o, str):
        return o + "\n"
    if isinstance(o, list):
        return "".join(_strings(v) for v in o)
    if isinstance(o, dict):
        return "".join(_strings(v) for v in o.values())
    return ""


def main():
    regions, contours = [], []
    for d in sorted(p for p in HERE.iterdir() if p.is_dir()):
        for name, bucket in (("regions.json", regions), ("contours.json", contours)):
            fp = d / name
            if fp.exists():
                try:
                    data = json.loads(fp.read_text(encoding="utf-8"))
                except Exception as e:
                    fails.append(f"{d.name}/{name}: not valid JSON ({e})")
                    continue
                for s in data:
                    bucket.append((s.get("id") or f"{d.name}?", s))
    ids_r = {i for i, _ in regions}
    ids_c = {i for i, _ in contours}
    regions_by_id = {i: s for i, s in regions}
    for kind, w, body in [(k, w, b) for w, k, b in inline_specs()]:
        if body.startswith("{") or body.startswith("["):
            try:
                obj = json.loads(body)
            except Exception as e:
                fails.append(f"{w}: not valid JSON ({e})")
                continue
            for s in (obj if isinstance(obj, list) else [obj]):
                (regions if kind == "region" else contours).append((f"{w} {s.get('id', '')}".strip(), s))
        elif body not in (ids_r if kind == "region" else ids_c):
            fails.append(f"{w}: unknown {kind} id {body!r}")
    for w, s in regions:
        try:
            check_region(w, s)
        except Exception as e:
            fail(w, f"check crashed: {type(e).__name__}: {e}")
    for w, s in contours:
        try:
            check_contour(w, s, regions_by_id)
        except Exception as e:
            fail(w, f"check crashed: {type(e).__name__}: {e}")
    enc = lambda s: s.encode("ascii", "backslashreplace").decode()
    if "-v" in sys.argv:
        for o in oks:
            print("  ok ", enc(o))
    for wv in warns:
        print("WARN", enc(wv))
    for fv in fails:
        print("FAIL", enc(fv))
    print(f"extras-check: {len(regions)} region(s), {len(contours)} contour(s), "
          f"{sum(len(s.get('critical_points') or []) for _, s in contours)} critical point(s); "
          f"{len(oks)} checks ok, {len(warns)} warning(s), {len(fails)} failure(s)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
