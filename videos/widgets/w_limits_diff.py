# -*- coding: utf-8 -*-
"""Widgets + sympy checks for the limits_diff videos (L01..L09: limits, continuity, differentiability at the origin).

Every class is prefixed ld- so other courses are untouched.

Checks (a script asserts every value it shows):
  along(f, path)        limit of f along y = path(x) as x -> 0, both sides (asserts the sides agree)
  along_y(f, path)      the same along x = path(y), y -> 0
  polar(f)              f(r cos t, r sin t), simplified
  rpow(f)               (p, g) with polar(f) == r**p * g(theta)
  sup_abs(g)            max |g(theta)| on a fine grid (for a bound |g| <= C)
  pdef(f, f0, wrt)      partial derivative at the origin BY DEFINITION (f is the formula off the origin)
  Qexpr(f, f0, fx, fy)  the differentiability quotient in h, k
Stage widgets:
  eqs(pfx, lines)       display formulas one per row, ids {pfx}-0, {pfx}-1, ... (hidden unless shown=)
  plane(pfx, curves)    the xy-plane near the origin; each curve a hidden group {pfx}-c-<name> with its label and
                        an optional value tag; {pfx}-o is the origin dot (shown)
  polar_pic(pfx)        a point at distance r and angle theta from the origin, with shrinking circles
                        ids {pfx}-pt, {pfx}-r1, {pfx}-r2, {pfx}-r3 (circles, hidden)
  ladder(pfx, rows)     the implication table of L08: ids {pfx}-<i>
  verdict(id, text, ok) a verdict pill (hidden);  stem(qid, html) the exam statement for the panel
"""
import html as _html
import math
import numpy as np
import sympy as sp

x, y, h, k = sp.symbols("x y h k", real=True)
r = sp.symbols("r", positive=True)
th = sp.symbols("theta", real=True)


# ---------------------------------------------------------------- checks
def along(f, path):
    g = sp.simplify(f.subs(y, path))
    a, b = sp.limit(g, x, 0, "+"), sp.limit(g, x, 0, "-")
    assert sp.simplify(a - b) == 0, (f, path, a, b)
    return sp.nsimplify(a)


def along_y(f, path):
    g = sp.simplify(f.subs(x, path))
    a, b = sp.limit(g, y, 0, "+"), sp.limit(g, y, 0, "-")
    assert sp.simplify(a - b) == 0, (f, path, a, b)
    return sp.nsimplify(a)


def polar(f):
    return sp.simplify(sp.trigsimp(sp.simplify(f.subs({x: r * sp.cos(th), y: r * sp.sin(th)}))))


def rpow(f):
    """(p, g): polar(f) == r**p * g(theta), g free of r"""
    e = polar(f)
    for p in [sp.Rational(n, 2) for n in range(-4, 13)]:
        g = sp.simplify(e / r ** p)
        if r not in g.free_symbols:
            return p, g
    raise AssertionError(f"no r-power form for {f}")


def sup_abs(g, n=20001):
    fn = sp.lambdify(th, g, "numpy")
    t = np.linspace(0, 2 * np.pi, n)
    return float(np.max(np.abs(fn(t) * np.ones_like(t))))


def pdef(f, f0, wrt="x"):
    """partial derivative at (0,0) by definition: lim_{h->0} (f(h,0)-f0)/h, f is the formula for points != origin"""
    pt = {x: h, y: 0} if wrt == "x" else {x: 0, y: h}
    q = sp.simplify((f.subs(pt) - f0) / h)
    a, b = sp.limit(q, h, 0, "+"), sp.limit(q, h, 0, "-")
    assert sp.simplify(a - b) == 0, (f, wrt, a, b)
    return a


def Qexpr(f, f0, fx, fy):
    return sp.simplify((f.subs({x: h, y: k}) - f0 - fx * h - fy * k) / sp.sqrt(h ** 2 + k ** 2))


# ---------------------------------------------------------------- stage widgets
def esc(s):
    return _html.escape(s, quote=True)


def eqs(pfx, lines, size=40, gap=20, shown=0):
    rows = "".join(f'<div id="{pfx}-{i}" class="ld-eq{"" if i < shown else " h"}">{t}</div>'
                   for i, t in enumerate(lines))
    return f'<div class="ld-eqs" style="font-size:{size}px;gap:{gap}px">{rows}</div>'


COLORS = {"a": "#38bdf8", "b": "#fbbf24", "c": "#f472b6", "d": "#a78bfa", "e": "#34d399"}


def plane(pfx, curves, w=560, hgt=560, span=1.0, shown=()):
    """curves: [(name, kind, fn, label, tag, color[, {"lab": (u, v), "tag": (u, v)}])] with kind 'y' (y = fn(x)) or 'x' (x = fn(y)).
    label: plain text drawn near the end of the curve (no TeX in SVG); tag: e.g. '→ 0' (or None)."""
    pad = 18
    X = lambda u: pad + (u + span) / (2 * span) * (w - 2 * pad)
    Y = lambda v: pad + (span - v) / (2 * span) * (hgt - 2 * pad)
    o = [f'<svg class="ld-plane" id="{pfx}" viewBox="0 0 {w} {hgt}" width="{w}" height="{hgt}" direction="ltr">',
         f'<rect x="1" y="1" width="{w - 2}" height="{hgt - 2}" rx="18" class="ld-pbg"/>']
    for g in (-0.5, 0.5):
        o.append(f'<line class="ld-grid" x1="{X(g * span):.1f}" x2="{X(g * span):.1f}" y1="{pad}" y2="{hgt - pad}"/>'
                 f'<line class="ld-grid" y1="{Y(g * span):.1f}" y2="{Y(g * span):.1f}" x1="{pad}" x2="{w - pad}"/>')
    o.append(f'<line class="ld-axis" x1="{pad}" x2="{w - pad}" y1="{Y(0):.1f}" y2="{Y(0):.1f}"/>'
             f'<line class="ld-axis" x1="{X(0):.1f}" x2="{X(0):.1f}" y1="{pad}" y2="{hgt - pad}"/>'
             f'<text class="ld-axl" x="{w - pad - 8}" y="{Y(0) - 12:.1f}">x</text>'
             f'<text class="ld-axl" x="{X(0) + 14:.1f}" y="{pad + 30}">y</text>')
    for cv in curves:
        name, kind, fn, label, tag, color = cv[:6]
        opt = cv[6] if len(cv) > 6 else {}
        col = COLORS.get(color, color)
        pts = []
        for t in np.linspace(-span, span, 401):
            u, v = (t, fn(t)) if kind == "y" else (fn(t), t)
            if abs(u) <= span * 1.0001 and abs(v) <= span * 1.0001:
                pts.append((X(u), Y(v)))
        d = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
        if "lab" in opt:
            lx, ly = X(opt["lab"][0]), Y(opt["lab"][1])
        else:
            lx, ly = pts[int(len(pts) * 0.9)]
            lx, ly = lx - 40, ly - 16
        lx = min(max(lx, 60), w - 60)
        ly = min(max(ly, 40), hgt - 20)
        cls = "" if name in shown else ' class="h"'
        o.append(f'<g id="{pfx}-c-{name}"{cls}><polyline points="{d}" class="ld-curve" style="stroke:{col}"/>'
                 f'<text x="{lx:.1f}" y="{ly:.1f}" class="ld-clab" style="fill:{col}">{esc(label)}</text></g>')
        if tag:
            if "tag" in opt:
                tx, ty = X(opt["tag"][0]), Y(opt["tag"][1])
            else:
                tx, ty = pts[int(len(pts) * 0.7)]
                tx, ty = tx + 10, ty + 34
            tw = 26 + 21 * len(tag)
            o.append(f'<g id="{pfx}-t-{name}" class="h"><rect x="{tx:.1f}" y="{ty - 22:.1f}" width="{tw}" '
                     f'height="44" rx="12" class="ld-tagbg" style="stroke:{col}"/>'
                     f'<text x="{tx + 13:.1f}" y="{ty + 11:.1f}" class="ld-tag">{esc(tag)}</text></g>')
    o.append(f'<circle id="{pfx}-o" cx="{X(0):.1f}" cy="{Y(0):.1f}" r="9" class="ld-orig"/>')
    o.append("</svg>")
    return "".join(o)


def polar_pic(pfx, w=520, hgt=520, theta_deg=35):
    c = w / 2, hgt / 2
    R = [200, 130, 70]
    o = [f'<svg class="ld-plane" id="{pfx}" viewBox="0 0 {w} {hgt}" width="{w}" height="{hgt}" direction="ltr">',
         f'<rect x="1" y="1" width="{w - 2}" height="{hgt - 2}" rx="18" class="ld-pbg"/>',
         f'<line class="ld-axis" x1="18" x2="{w - 18}" y1="{c[1]}" y2="{c[1]}"/>',
         f'<line class="ld-axis" x1="{c[0]}" x2="{c[0]}" y1="18" y2="{hgt - 18}"/>']
    t = math.radians(theta_deg)
    for i, rad in enumerate(R):
        px, py = c[0] + rad * math.cos(t), c[1] - rad * math.sin(t)
        o.append(f'<g id="{pfx}-r{i + 1}" class="h"><circle cx="{c[0]}" cy="{c[1]}" r="{rad}" class="ld-ring"/>'
                 f'<line x1="{c[0]}" y1="{c[1]}" x2="{px:.1f}" y2="{py:.1f}" class="ld-ray"/>'
                 f'<circle cx="{px:.1f}" cy="{py:.1f}" r="10" class="ld-pt"/></g>')
    px, py = c[0] + R[0] * math.cos(t), c[1] - R[0] * math.sin(t)
    ax, ay = c[0] + 60 * math.cos(t / 2), c[1] - 60 * math.sin(t / 2)
    o.append(f'<g id="{pfx}-lab" class="h"><path d="M{c[0] + 46},{c[1]} A46,46 0 0 0 {c[0] + 46 * math.cos(t):.1f},'
             f'{c[1] - 46 * math.sin(t):.1f}" class="ld-arc"/>'
             f'<text x="{ax + 18:.1f}" y="{ay + 10:.1f}" class="ld-plab">θ</text>'
             f'<text x="{(c[0] + px) / 2 - 34:.1f}" y="{(c[1] + py) / 2 - 8:.1f}" class="ld-plab">r</text></g>')
    o.append(f'<circle cx="{c[0]}" cy="{c[1]}" r="8" class="ld-orig"/></svg>')
    return "".join(o)


def ladder(pfx, rows):
    """rows: [(left html, arrow text, right html)] -> a table of implications, each row hidden: {pfx}-<i>"""
    out = []
    for i, (a, mid, b) in enumerate(rows):
        out.append(f'<div id="{pfx}-{i}" class="ld-lrow h"><span class="ld-lbox">{a}</span>'
                   f'<span class="ld-larr">{mid}</span><span class="ld-lbox">{b}</span></div>')
    return f'<div class="ld-ladder">{"".join(out)}</div>'


def compare(pfx, cols, shown=False):
    """side-by-side boxes: cols = [(head, body html, foot, ok)], ids {pfx}-<i> (hidden unless shown)"""
    out = []
    for i, (head, body, foot, ok) in enumerate(cols):
        cls = {True: "ok", False: "bad", None: "mid"}[ok]
        out.append(f'<div id="{pfx}-{i}" class="ld-cmp {cls}{"" if shown else " h"}"><div class="ld-cmph">{head}</div>'
                   f'<div class="ld-cmpb">{body}</div><div class="ld-cmpf">{foot}</div></div>')
    return f'<div class="ld-cmps">{"".join(out)}</div>'


def verdict(id_, text, ok=True):
    cls = {True: "ok", False: "bad", None: "mid"}[ok]
    return f'<div id="{id_}" class="ld-verdict {cls} h">{text}</div>'


def stem(qid, html_):
    return f'<div class="qstem"><span class="qid">{qid}</span>{html_}</div>'


def piecewise(tex, size=34):
    """the exam's piecewise f, as display math in the panel"""
    return (f'<div class="ld-pw" style="font-size:{size}px">$f(x,y)=\\begin{{cases}}\\displaystyle {tex}, & (x,y)\\neq(0,0)'
            f'\\\\ 0, & (x,y)=(0,0)\\end{{cases}}$</div>')
