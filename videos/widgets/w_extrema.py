# -*- coding: utf-8 -*-
"""Extrema widgets for the אינפי 2 videos (course "extrema", E01..E09): computed in Python, drawn as SVG/HTML.

Math helpers (sympy, used by the scripts' asserts):
  crit(f)             real critical points of f(x,y), as a list of (x, y) sympy pairs, sorted
  hess(f, p)          (A, B, C, Δ) at the point p
  kind(A, B, C)       "min" / "max" / "saddle" / "?" (Δ = 0)
  lagrange(f, g, c)   real solutions (x, y, λ) of ∇f = λ∇g, g = c
Pictures:
  contour(pfx, f, xr, yr, ...)  level curves (contourpy) + region/curve + points + gradient arrows.
      ids: {pfx}-reg region (hidden when reg_hidden), {pfx}-cv-<i> curve i, {pfx}-p-<name> point (+ label),
           {pfx}-a-<name> arrow, {pfx}-ln-<i> extra segment
  graph(pfx, g, a, b, ...)      a one-variable function on [a, b] with its marks: {pfx}-m-<name>, {pfx}-cv curve
Tables (HTML, $TeX$ inside, LTR):
  htable(pfx, rows)   point | A | B | C | Δ | verdict.  ids {pfx}-r<i> row, {pfx}-v<i> verdict
  ctable(pfx, rows)   point | where | f.               ids {pfx}-r<i> row, {pfx}-mx / {pfx}-mn tags
  lines(pfx, texs)    a column of formulas, ids {pfx}-<i>
"""
import html as _html
import math

import contourpy
import numpy as np
import sympy as sp

X, Y, LAM = sp.symbols("x y lambda", real=True)

# ----------------------------------------------------------------------------- math


def crit(f):
    sols = sp.solve([sp.diff(f, X), sp.diff(f, Y)], [X, Y], dict=True)
    pts = []
    for s in sols:
        if X not in s or Y not in s:
            raise ValueError(f"non-isolated critical set for {f}: {s}")
        px, py = sp.nsimplify(sp.simplify(s[X])), sp.nsimplify(sp.simplify(s[Y]))
        if px.is_real and py.is_real:
            pts.append((px, py))
    return sorted(set(pts), key=lambda p: (float(p[0]), float(p[1])))


def hess(f, p):
    sub = {X: p[0], Y: p[1]}
    A = sp.simplify(sp.diff(f, X, 2).subs(sub))
    B = sp.simplify(sp.diff(f, X, Y).subs(sub))
    C = sp.simplify(sp.diff(f, Y, 2).subs(sub))
    return A, B, C, sp.simplify(A * C - B ** 2)


def kind(A, B, C):
    D = sp.simplify(A * C - B ** 2)
    if D > 0:
        return "min" if A > 0 else "max"
    if D < 0:
        return "saddle"
    return "?"


def val(f, p):
    return sp.simplify(f.subs({X: p[0], Y: p[1]}))


def lagrange(f, g, c):
    eqs = [sp.diff(f, X) - LAM * sp.diff(g, X), sp.diff(f, Y) - LAM * sp.diff(g, Y), g - c]
    out = []
    for s in sp.solve(eqs, [X, Y, LAM], dict=True):
        t = (sp.simplify(s[X]), sp.simplify(s[Y]), sp.simplify(s[LAM]))
        if all(v.is_real for v in t):
            out.append(t)
    return sorted(set(out), key=lambda t: (float(t[0]), float(t[1])))


def same(a, b):
    return sp.simplify(sp.sympify(a) - sp.sympify(b)) == 0


# ----------------------------------------------------------------------------- drawing helpers
LO, HI = (56, 189, 248), (251, 146, 60)        # level colour: low values sky blue -> high values orange


def _mix(t):
    t = min(1.0, max(0.0, t))
    return "#%02x%02x%02x" % tuple(round(a + (b - a) * t) for a, b in zip(LO, HI))


def esc(s):
    return _html.escape(str(s), quote=True)


class Frame:
    """maps (x, y) in [xr] x [yr] to SVG pixels, equal scale on both axes"""

    def __init__(self, xr, yr, w, pad=34):
        self.x0, self.x1 = xr
        self.y0, self.y1 = yr
        self.pad = pad
        self.k = (w - 2 * pad) / (self.x1 - self.x0)
        self.w = w
        self.h = round((self.y1 - self.y0) * self.k + 2 * pad)

    def __call__(self, x, y):
        return (self.pad + (float(x) - self.x0) * self.k, self.pad + (self.y1 - float(y)) * self.k)


def _poly(pts):
    return "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts)


def _axes(F, ticks=True):
    o = []
    if F.y0 <= 0 <= F.y1:
        a, b = F(F.x0, 0), F(F.x1, 0)
        o.append(f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}" class="ax"/>')
        o.append(f'<text x="{b[0] - 4:.1f}" y="{b[1] - 10:.1f}" class="axl" text-anchor="end">x</text>')
    if F.x0 <= 0 <= F.x1:
        a, b = F(0, F.y0), F(0, F.y1)
        o.append(f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}" class="ax"/>')
        o.append(f'<text x="{b[0] + 12:.1f}" y="{b[1] + 22:.1f}" class="axl">y</text>')
    if ticks:
        for v in range(math.ceil(F.x0), math.floor(F.x1) + 1):
            if v and F.y0 <= 0 <= F.y1:
                p = F(v, 0)
                o.append(f'<path d="M{p[0]:.1f},{p[1] - 5:.1f} L{p[0]:.1f},{p[1] + 5:.1f}" class="ax"/>'
                         f'<text x="{p[0]:.1f}" y="{p[1] + 26:.1f}" class="tk">{v}</text>')
        for v in range(math.ceil(F.y0), math.floor(F.y1) + 1):
            if v and F.x0 <= 0 <= F.x1:
                p = F(0, v)
                o.append(f'<path d="M{p[0] - 5:.1f},{p[1]:.1f} L{p[0] + 5:.1f},{p[1]:.1f}" class="ax"/>'
                         f'<text x="{p[0] - 10:.1f}" y="{p[1] + 8:.1f}" class="tk" text-anchor="end">{v}</text>')
    return o


def region_path(F, reg):
    """reg: ("poly", [(x,y),...]) | ("disk", cx, cy, r) | ("sector", r, th0, th1)"""
    if reg[0] == "poly":
        return _poly([F(a, b) for a, b in reg[1]]) + " Z"
    if reg[0] == "disk":
        _, cx, cy, r = reg
        pts = [F(cx + r * math.cos(t), cy + r * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 181)]
        return _poly(pts) + " Z"
    if reg[0] == "sector":
        _, r, t0, t1 = reg
        pts = [F(0, 0)] + [F(r * math.cos(t), r * math.sin(t)) for t in np.linspace(t0, t1, 91)]
        return _poly(pts) + " Z"
    raise ValueError(reg)


def contour(pfx, f, xr, yr, w=640, n=13, levels=None, region=None, reg_hidden=False, curves=(), points=(),
            arrows=(), segs=(), ticks=True, clip_region=False, shown=()):
    """level curves of the sympy expression f over xr x yr.
    points: [dict(name, x, y, label, role in min/max/saddle/cand/out, hidden=True, dx=14, dy=-14, anchor="start")]
    curves: [(xs(t), ys(t), t0, t1)] numeric callables -> {pfx}-cv-<i> (hidden)
    arrows: [(name, x, y, dx, dy, cls)] in plot units ("gf" solid, "gg" dashed) -> {pfx}-a-<name> (hidden)
    segs:   [((x0,y0),(x1,y1), cls)] -> {pfx}-ln-<i> (hidden)
    shown:  id suffixes drawn visible from the start ("cv-0", "ln-1", "a-p", "p-o"), for a second copy of a plot"""
    hid = lambda suf: "" if suf in shown else " h"
    F = Frame(xr, yr, w)
    fn = sp.lambdify((X, Y), f, "numpy")
    gx = np.linspace(F.x0, F.x1, 241)
    gy = np.linspace(F.y0, F.y1, round(241 * (F.y1 - F.y0) / (F.x1 - F.x0)) + 1)
    XX, YY = np.meshgrid(gx, gy)
    Z = np.asarray(fn(XX, YY), dtype=float) * np.ones_like(XX)
    if levels is None:
        qs = np.quantile(Z[np.isfinite(Z)], np.linspace(0.04, 0.96, n))
        levels = sorted(set(np.round(qs, 6)))
        for p in points:
            if p.get("role") in ("min", "max", "saddle"):
                levels.append(float(val(f, (p["x"], p["y"]))))
        levels = sorted(set(levels))
    levels = sorted(levels)
    gen = contourpy.contour_generator(gx, gy, Z)
    o = [f'<svg class="ctr" id="{pfx}" viewBox="0 0 {F.w} {F.h}" width="{F.w}" height="{F.h}" direction="ltr">',
         '<defs>'
         f'<marker id="{pfx}-ahf" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
         '<path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker>'
         f'<marker id="{pfx}-ahg" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
         '<path d="M0,0 L10,5 L0,10 z" fill="#f0abfc"/></marker>'
         f'<clipPath id="{pfx}-clip"><rect x="{F.pad}" y="{F.pad}" width="{F.w - 2 * F.pad}" height="{F.h - 2 * F.pad}"/></clipPath>'
         '</defs>',
         f'<rect x="{F.pad}" y="{F.pad}" width="{F.w - 2 * F.pad}" height="{F.h - 2 * F.pad}" class="bgr"/>']
    o += _axes(F, ticks)
    lv = []
    for k, L in enumerate(levels):          # colour by rank, so a fast-growing f still uses the whole palette
        col = _mix(k / (len(levels) - 1) if len(levels) > 1 else 0.5)
        for line in gen.lines(L):
            if len(line) < 2:
                continue
            lv.append(f'<path d="{_poly([F(a, b) for a, b in line])}" class="lv" style="stroke:{col}"/>')
    o.append(f'<g clip-path="url(#{pfx}-clip)">{"".join(lv)}</g>')
    if region is not None:
        o.append(f'<path id="{pfx}-reg" d="{region_path(F, region)}" class="reg{" h" if reg_hidden else ""}"/>')
    for i, (fx, fy, t0, t1) in enumerate(curves):
        pts = [F(fx(t), fy(t)) for t in np.linspace(t0, t1, 241)]
        o.append(f'<path id="{pfx}-cv-{i}" d="{_poly(pts)}" class="cv{hid(f'cv-{i}')}"/>')
    for i, ((a, b), (c, d), cls) in enumerate(segs):
        p, q = F(a, b), F(c, d)
        o.append(f'<path id="{pfx}-ln-{i}" d="M{p[0]:.1f},{p[1]:.1f} L{q[0]:.1f},{q[1]:.1f}" class="sg {cls}{hid(f'ln-{i}')}"/>')
    for name, ax_, ay_, dx, dy, cls in arrows:
        p, q = F(ax_, ay_), F(ax_ + dx, ay_ + dy)
        m = "ahf" if cls == "gf" else "ahg"
        o.append(f'<path id="{pfx}-a-{name}" d="M{p[0]:.1f},{p[1]:.1f} L{q[0]:.1f},{q[1]:.1f}" class="ar {cls}{hid('a-' + name)}" '
                 f'marker-end="url(#{pfx}-{m})"/>')
    for p in points:
        c = F(p["x"], p["y"])
        hid_ = " h" if p.get("hidden", True) and ("p-" + p["name"]) not in shown else ""
        lab = ""
        if p.get("label"):
            anc = p.get("anchor", "start")
            lab = (f'<text x="{c[0] + p.get("dx", 14):.1f}" y="{c[1] + p.get("dy", -14):.1f}" class="pl" '
                   f'text-anchor="{anc}">{esc(p["label"])}</text>')
        mark = (f'<path d="M{c[0] - 10:.1f},{c[1] - 10:.1f} L{c[0] + 10:.1f},{c[1] + 10:.1f} M{c[0] - 10:.1f},{c[1] + 10:.1f} '
                f'L{c[0] + 10:.1f},{c[1] - 10:.1f}" class="px"/>' if p.get("role") == "out"
                else f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="11" class="pt {p.get("role", "cand")}"/>')
        o.append(f'<g id="{pfx}-p-{p["name"]}" class="{hid_.strip()}">{mark}{lab}</g>')
    o.append("</svg>")
    return "".join(o)


def graph(pfx, g, a, b, w=620, h=300, marks=(), yr=None, tlabel="t", ticks=()):
    """y = g(t) on [a, b] (g a sympy expr in the symbol T below, or a numeric callable).
    marks: [dict(name, t, label, role in end/crit/min/max, dy)] -> {pfx}-m-<name> (hidden); the curve is {pfx}-cv.
    ticks: [(t, text)] labels under the axis."""
    fn = g if callable(g) else sp.lambdify(T, g, "numpy")
    ts = np.linspace(float(a), float(b), 301)
    vs = np.asarray([float(fn(t)) for t in ts])
    y0, y1 = yr or (vs.min(), vs.max())
    pad, top, bot = 50, 46, 56
    sx = (w - 2 * pad) / (float(b) - float(a))
    sy = (h - top - bot) / (y1 - y0)
    P = lambda t, v: (pad + (float(t) - float(a)) * sx, top + (y1 - float(v)) * sy)
    o = [f'<svg class="g1" id="{pfx}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" direction="ltr">']
    base = P(a, y0)[1] + 18
    o.append(f'<path d="M{pad - 10},{base:.1f} L{w - pad + 10},{base:.1f}" class="ax"/>')
    o.append(f'<text x="{w - pad + 16}" y="{base + 8:.1f}" class="axl">{esc(tlabel)}</text>')
    for t, txt in ticks:
        px = P(t, y0)[0]
        o.append(f'<path d="M{px:.1f},{base - 6:.1f} L{px:.1f},{base + 6:.1f}" class="ax"/>'
                 f'<text x="{px:.1f}" y="{base + 32:.1f}" class="tk">{esc(txt)}</text>')
    o.append(f'<path id="{pfx}-cv" d="{_poly([P(t, v) for t, v in zip(ts, vs)])}" class="gc h"/>')
    for m in marks:
        px, py = P(m["t"], float(fn(float(m["t"]))))
        lab = (f'<text x="{px:.1f}" y="{py + m.get("dy", -20):.1f}" class="pl" text-anchor="middle">{esc(m["label"])}</text>'
               if m.get("label") else "")
        o.append(f'<g id="{pfx}-m-{m["name"]}" class="h"><path d="M{px:.1f},{py:.1f} L{px:.1f},{base:.1f}" class="gd"/>'
                 f'<circle cx="{px:.1f}" cy="{py:.1f}" r="10" class="pt {m.get("role", "crit")}"/>{lab}</g>')
    o.append("</svg>")
    return "".join(o)


T = sp.symbols("t", real=True)

# ----------------------------------------------------------------------------- tables
VERDICT = {"min": ("מינימום מקומי", "min"), "max": ("מקסימום מקומי", "max"), "saddle": ("אוכף", "saddle"),
           "?": ("לא מכריע", "unk")}


def htable(pfx, rows, head=("נקודה", "A", "B", "C", r"\Delta")):
    """rows: [(point_tex, A_tex, B_tex, C_tex, D_tex, kind)]"""
    th = "".join(f"<th>{h if i == 0 else '$' + h + '$'}</th>" for i, h in enumerate(head)) + "<th>סוג</th>"
    body = []
    for i, (pt, a, b, c, d, k) in enumerate(rows):
        txt, cls = VERDICT[k]
        body.append(f'<tr id="{pfx}-r{i}" class="h"><td>${pt}$</td><td>${a}$</td><td>${b}$</td><td>${c}$</td>'
                    f'<td>${d}$</td><td><span id="{pfx}-v{i}" class="vd {cls} h">{txt}</span></td></tr>')
    return f'<table class="xt" id="{pfx}" dir="ltr"><thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table>'


def ctable(pfx, rows, mx=None, mn=None, head=("נקודה", "מאיפה", "f"), hidden=False):
    """rows: [(point_tex, where_text, value_tex)]; mx / mn: row indices (or lists) of the absolute max / min"""
    as_list = lambda v: [] if v is None else (v if isinstance(v, (list, tuple)) else [v])
    mxs, mns = as_list(mx), as_list(mn)
    nowhere = all(r[1] is None for r in rows)
    th = f"<th>{head[0]}</th>" + ("" if nowhere else f"<th>{head[1]}</th>") + f"<th>${head[2]}$</th><th></th>"
    body = []
    for i, (pt, where, v) in enumerate(rows):
        tag = ""
        if i in mxs:
            tag = f'<span id="{pfx}-mx{"" if mxs.index(i) == 0 else mxs.index(i)}" class="vd max h">מקסימום</span>'
        elif i in mns:
            tag = f'<span id="{pfx}-mn{"" if mns.index(i) == 0 else mns.index(i)}" class="vd min h">מינימום</span>'
        body.append(f'<tr id="{pfx}-r{i}" class="h"><td>${pt}$</td>{"" if nowhere else f'<td class="wh">{where}</td>'}<td>${v}$</td><td>{tag}</td></tr>')
    return f'<table class="xt ct{" h" if hidden else ""}" id="{pfx}" dir="ltr"><thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table>'


def lines(pfx, texs, cls="", hidden=True):
    """a column of formulas/notes; each item is HTML that may hold $TeX$ (an item starting with "<rtl>" is a
    Hebrew line, written right to left). ids {pfx}-<i>"""
    h = " h" if hidden else ""
    out = []
    for i, t in enumerate(texs):
        rtl = t.startswith("<rtl>")
        out.append(f'<div id="{pfx}-{i}" class="ml{" rtl" if rtl else ""}{h}">{t[5:] if rtl else t}</div>')
    return f'<div class="mlines {cls}" id="{pfx}">' + "".join(out) + "</div>"
