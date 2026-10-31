# -*- coding: utf-8 -*-
"""Double-integral widgets for the אינפי 2 videos (course `double_int`, I01..I08). Every class is prefixed di-.

Plot(pfx, xr, yr, ...)   an SVG plane with equal scale on both axes, grid, ticks and axis names. Everything drawn on it
                         is computed in Python from the functions the script asserts with sympy, so the picture is
                         the verified region and nothing else. Methods add elements (hidden unless hidden=False):
    fill(id, pts)             a region (polygon in data coordinates)       -> id
    curve(id, pts)            a boundary curve (polyline)                  -> id
    fn(id, f, a, b)           the graph y = f(x), a <= x <= b
    gx(id, g, c, d)           the graph x = g(y), c <= y <= d
    polar(id, rf, t1, t2)     the curve r = rf(theta)
    ray(id, theta, r1, r2)    a ray segment from the origin direction
    vstrip(id, x, ylo, yhi)   a vertical strip with its entry / exit dots
    hstrip(id, y, xlo, xhi)   a horizontal strip
    wedge(id, t, rlo, rhi)    a thin polar wedge (the "r strip" at angle t)
    dot(id, x, y, label)      a vertex with its coordinates
    label(id, x, y, text)     a curve name (plain text with unicode: √, ², θ — never TeX)
  Plot.svg() returns the markup. Colors: kind = a (blue), b (amber), c (pink), d (violet), ink.

Region polygons (data coordinates) and checks:
  type1(lo, hi, a, b)        a <= x <= b, lo(x) <= y <= hi(x)
  type2(lo, hi, c, d)        c <= y <= d, lo(y) <= x <= hi(y)
  polar_region(rlo, rhi, t1, t2)
  shoelace(pts)              the polygon's area: scripts assert it against the sympy area, so the drawing is right

HTML helpers: eqs(pfx, lines) a column of formulas revealed one by one ({pfx}-0, {pfx}-1, …), stem(qid, html).
"""
import html as _html
import math

KIND = ("a", "b", "c", "d", "ink")


def esc(s):
    return _html.escape(s, quote=True)


def _f(v):
    return f"{v:.1f}"


# ---------------------------------------------------------------- polygons
def type1(lo, hi, a, b, n=160):
    xs = [a + (b - a) * i / n for i in range(n + 1)]
    return [(x, lo(x)) for x in xs] + [(x, hi(x)) for x in reversed(xs)]


def type2(lo, hi, c, d, n=160):
    ys = [c + (d - c) * i / n for i in range(n + 1)]
    return [(lo(y), y) for y in ys] + [(hi(y), y) for y in reversed(ys)]


def polar_region(rlo, rhi, t1, t2, n=160):
    ts = [t1 + (t2 - t1) * i / n for i in range(n + 1)]
    out = [(rlo(t) * math.cos(t), rlo(t) * math.sin(t)) for t in ts]
    out += [(rhi(t) * math.cos(t), rhi(t) * math.sin(t)) for t in reversed(ts)]
    return out


def shoelace(pts):
    s = 0.0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


# ---------------------------------------------------------------- the plane
class Plot:
    def __init__(self, pfx, xr, yr, w=600, h=560, xticks=None, yticks=None, xname="x", yname="y", pad=44,
                 grid=True):
        (x0, x1), (y0, y1) = xr, yr
        k = min((w - 2 * pad) / (x1 - x0), (h - 2 * pad) / (y1 - y0))
        self.pfx, self.k, self.x0, self.y1 = pfx, k, x0, y1
        self.pad = pad
        self.w = round((x1 - x0) * k + 2 * pad)
        self.h = round((y1 - y0) * k + 2 * pad)
        self.xr, self.yr = xr, yr
        self.layers = {"fill": [], "strip": [], "curve": [], "dot": [], "label": []}
        self.xticks = xticks if xticks is not None else [(i, str(i)) for i in range(math.ceil(x0), math.floor(x1) + 1)
                                                         if i != 0]
        self.yticks = yticks if yticks is not None else [(i, str(i)) for i in range(math.ceil(y0), math.floor(y1) + 1)
                                                         if i != 0]
        self.xname, self.yname, self.grid = xname, yname, grid

    def X(self, x):
        return self.pad + (x - self.x0) * self.k

    def Y(self, y):
        return self.pad + (self.y1 - y) * self.k

    def _d(self, pts, close=False):
        s = "M" + " L".join(f"{_f(self.X(x))},{_f(self.Y(y))}" for x, y in pts)
        return s + (" Z" if close else "")

    @staticmethod
    def _h(hidden):
        return " h" if hidden else ""

    # -- elements
    def fill(self, id_, pts, kind="a", hidden=True):
        self.layers["fill"].append(f'<path id="{id_}" class="di-fill k-{kind}{self._h(hidden)}" d="{self._d(pts, True)}"/>')
        return id_

    def curve(self, id_, pts, kind="ink", hidden=True, dash=False):
        cls = f"di-cv k-{kind}" + (" dash" if dash else "") + self._h(hidden)
        self.layers["curve"].append(f'<path id="{id_}" class="{cls}" d="{self._d(pts)}"/>')
        return id_

    def fn(self, id_, f, a, b, n=200, **kw):
        return self.curve(id_, [(a + (b - a) * i / n, f(a + (b - a) * i / n)) for i in range(n + 1)], **kw)

    def gx(self, id_, g, c, d, n=200, **kw):
        return self.curve(id_, [(g(c + (d - c) * i / n), c + (d - c) * i / n) for i in range(n + 1)], **kw)

    def polar(self, id_, rf, t1, t2, n=200, **kw):
        ts = [t1 + (t2 - t1) * i / n for i in range(n + 1)]
        return self.curve(id_, [(rf(t) * math.cos(t), rf(t) * math.sin(t)) for t in ts], **kw)

    def ray(self, id_, t, r1, r2, **kw):
        return self.curve(id_, [(r1 * math.cos(t), r1 * math.sin(t)), (r2 * math.cos(t), r2 * math.sin(t))], **kw)

    def vstrip(self, id_, x, ylo, yhi, hidden=True, half=None):
        """a vertical strip at x from ylo to yhi; the entry dot (bottom) and exit dot (top)"""
        hw = half if half is not None else 7 / self.k
        pts = [(x - hw, ylo), (x + hw, ylo), (x + hw, yhi), (x - hw, yhi)]
        g = (f'<g id="{id_}" class="{self._h(hidden).strip()}"><path class="di-strip" d="{self._d(pts, True)}"/>'
             f'<circle class="di-in" cx="{_f(self.X(x))}" cy="{_f(self.Y(ylo))}" r="9"/>'
             f'<circle class="di-out" cx="{_f(self.X(x))}" cy="{_f(self.Y(yhi))}" r="9"/></g>')
        self.layers["strip"].append(g)
        return id_

    def hstrip(self, id_, y, xlo, xhi, hidden=True, half=None):
        hw = half if half is not None else 7 / self.k
        pts = [(xlo, y - hw), (xhi, y - hw), (xhi, y + hw), (xlo, y + hw)]
        g = (f'<g id="{id_}" class="{self._h(hidden).strip()}"><path class="di-strip" d="{self._d(pts, True)}"/>'
             f'<circle class="di-in" cx="{_f(self.X(xlo))}" cy="{_f(self.Y(y))}" r="9"/>'
             f'<circle class="di-out" cx="{_f(self.X(xhi))}" cy="{_f(self.Y(y))}" r="9"/></g>')
        self.layers["strip"].append(g)
        return id_

    def wedge(self, id_, t, rlo, rhi, dt=0.035, hidden=True):
        pts = polar_region(lambda _: rlo, lambda _: rhi, t - dt, t + dt, n=12)
        c = lambda r: (_f(self.X(r * math.cos(t))), _f(self.Y(r * math.sin(t))))
        (ix, iy), (ox, oy) = c(rlo), c(rhi)
        g = (f'<g id="{id_}" class="{self._h(hidden).strip()}"><path class="di-strip" d="{self._d(pts, True)}"/>'
             f'<circle class="di-in" cx="{ix}" cy="{iy}" r="9"/><circle class="di-out" cx="{ox}" cy="{oy}" r="9"/></g>')
        self.layers["strip"].append(g)
        return id_

    def dot(self, id_, x, y, text=None, dx=12, dy=-14, anchor="start", hidden=True, kind="ink"):
        px, py = self.X(x), self.Y(y)
        t = (f'<text class="di-pt" x="{_f(px + dx)}" y="{_f(py + dy)}" text-anchor="{anchor}">{esc(text)}</text>'
             if text else "")
        self.layers["dot"].append(f'<g id="{id_}" class="{self._h(hidden).strip()}">'
                                  f'<circle class="di-dot k-{kind}" cx="{_f(px)}" cy="{_f(py)}" r="8"/>{t}</g>')
        return id_

    def label(self, id_, x, y, text, kind="ink", anchor="start", hidden=True, size=None):
        st = f' style="font-size:{size}px"' if size else ""
        self.layers["label"].append(f'<text id="{id_}" class="di-lb k-{kind}{self._h(hidden)}" x="{_f(self.X(x))}" '
                                    f'y="{_f(self.Y(y))}" text-anchor="{anchor}"{st}>{esc(text)}</text>')
        return id_

    def raw(self, layer, svg):
        self.layers[layer].append(svg)

    # -- the frame
    def _axes(self):
        (x0, x1), (y0, y1) = self.xr, self.yr
        ax_y = min(max(0, y0), y1)            # where the x axis is drawn
        ax_x = min(max(0, x0), x1)
        o = []
        if self.grid:
            for v, _ in self.xticks:
                o.append(f'<line class="di-grid" x1="{_f(self.X(v))}" x2="{_f(self.X(v))}" y1="{_f(self.Y(y0))}" '
                         f'y2="{_f(self.Y(y1))}"/>')
            for v, _ in self.yticks:
                o.append(f'<line class="di-grid" y1="{_f(self.Y(v))}" y2="{_f(self.Y(v))}" x1="{_f(self.X(x0))}" '
                         f'x2="{_f(self.X(x1))}"/>')
        m = f"{self.pfx}-ah"
        o.append(f'<defs><marker id="{m}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" '
                 f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#9aa0cf"/></marker></defs>')
        o.append(f'<line class="di-ax" x1="{_f(self.X(x0) - 10)}" x2="{_f(self.X(x1) + 18)}" y1="{_f(self.Y(ax_y))}" '
                 f'y2="{_f(self.Y(ax_y))}" marker-end="url(#{m})"/>')
        o.append(f'<line class="di-ax" y1="{_f(self.Y(y0) + 10)}" y2="{_f(self.Y(y1) - 18)}" x1="{_f(self.X(ax_x))}" '
                 f'x2="{_f(self.X(ax_x))}" marker-end="url(#{m})"/>')
        o.append(f'<text class="di-an" x="{_f(self.X(x1) + 24)}" y="{_f(self.Y(ax_y) + 9)}">{esc(self.xname)}</text>')
        o.append(f'<text class="di-an" x="{_f(self.X(ax_x))}" y="{_f(self.Y(y1) - 28)}" text-anchor="middle">'
                 f'{esc(self.yname)}</text>')
        for v, t in self.xticks:
            o.append(f'<line class="di-tk" x1="{_f(self.X(v))}" x2="{_f(self.X(v))}" y1="{_f(self.Y(ax_y) - 6)}" '
                     f'y2="{_f(self.Y(ax_y) + 6)}"/><text class="di-tl" x="{_f(self.X(v))}" y="{_f(self.Y(ax_y) + 32)}" '
                     f'text-anchor="middle">{esc(t)}</text>')
        for v, t in self.yticks:
            o.append(f'<line class="di-tk" y1="{_f(self.Y(v))}" y2="{_f(self.Y(v))}" x1="{_f(self.X(ax_x) - 6)}" '
                     f'x2="{_f(self.X(ax_x) + 6)}"/><text class="di-tl" x="{_f(self.X(ax_x) - 12)}" '
                     f'y="{_f(self.Y(v) + 9)}" text-anchor="end">{esc(t)}</text>')
        return o

    def svg(self, scale=1.0, cls=""):
        body = self._axes()
        for k in ("fill", "strip", "curve", "dot", "label"):
            body += self.layers[k]
        return (f'<svg class="di-plot {cls}" id="{self.pfx}" viewBox="-30 -50 {self.w + 80} {self.h + 70}" '
                f'width="{(self.w + 80) * scale:.0f}" height="{(self.h + 70) * scale:.0f}" direction="ltr">'
                + "".join(body) + "</svg>")


# ---------------------------------------------------------------- sympy: the same region in two descriptions
def _sp():
    import sympy as sp
    return sp


def integrate(f, desc):
    """desc: list of pieces ("I", a, b, lo(x), hi(x)) = dy dx, or ("II", c, d, lo(y), hi(y)) = dx dy (sympy exprs in
    the symbols x, y of this module). Returns the exact sum."""
    sp = _sp()
    X, Y = sp.symbols("x y", real=True)
    tot = 0
    for kind, a, b, lo, hi in desc:
        if kind == "I":
            tot += sp.integrate(sp.integrate(f, (Y, lo, hi)), (X, a, b))
        else:
            tot += sp.integrate(sp.integrate(f, (X, lo, hi)), (Y, a, b))
    return sp.simplify(tot)


def same_region(d1, d2):
    """two descriptions give the same integral for 1, x, y, xy, x^2 y (the region, as far as integrals can tell)"""
    sp = _sp()
    X, Y = sp.symbols("x y", real=True)
    for f in (sp.Integer(1), X, Y, X * Y, X**2 * Y):
        if sp.simplify(integrate(f, d1) - integrate(f, d2)) != 0:
            return False
    return True


# ---------------------------------------------------------------- the exam-style running example of I01/I03/I05
# An ORIGINAL region ("בסגנון מבחן"), not a bank question (the bank's 25A-B-Q4a is a text twin of a boss item, and
# its shape, sqrt on the left + falling line, is avoided too): under the parabola y=x^2 on [0,1], under the line
# y=3-2x on [1,3/2]; they meet at the interior corner (1,1).
#   int_0^1 int_0^{x^2} f dy dx + int_1^{3/2} int_0^{3-2x} f dy dx  =  int_0^1 int_{sqrt y}^{(3-y)/2} f dx dy
STYLE_TAG = "בסגנון מבחן"
STYLE_SUM = [
    "$\\displaystyle\\int_{0}^{1}\\!\\int_{0}^{x^2}\\!f\\,dy\\,dx$",
    "$\\displaystyle+\\int_{1}^{3/2}\\!\\int_{0}^{3-2x}\\!f\\,dy\\,dx$",
]
STYLE_SUM_LINE = ("$\\displaystyle\\int_{0}^{1}\\!\\int_{0}^{x^2}\\!f\\,dy\\,dx"
                  "+\\int_{1}^{3/2}\\!\\int_{0}^{3-2x}\\!f\\,dy\\,dx$")


def style_checks():
    """asserts every fact the three videos state about the exam-style region; returns the two sympy areas"""
    sp = _sp()
    X, Y = sp.symbols("x y", real=True)
    g1, g2 = X**2, 3 - 2 * X
    assert sp.solve(sp.Eq(g1, g2), X) == [-3, 1]   # meet at x=1 (x=-3 is outside [0, 3/2])
    assert g1.subs(X, 1) == 1 == g2.subs(X, 1)                    # the corner (1, 1)
    assert g1.subs(X, 0) == 0 and g2.subs(X, sp.Rational(3, 2)) == 0   # vertices (0, 0) and (3/2, 0)
    assert set(sp.solve(sp.Eq(X**2, Y), X)) == {-sp.sqrt(Y), sp.sqrt(Y)}   # x = +-sqrt(y): the region has x >= 0
    assert sp.solve(sp.Eq(3 - 2 * X, Y), X) == [(3 - Y) / 2]
    P1, P2 = [("I", 0, 1, 0, g1)], [("I", 1, sp.Rational(3, 2), 0, g2)]
    S1, S2 = [("II", 0, 1, sp.sqrt(Y), 1)], [("II", 0, 1, 1, (3 - Y) / 2)]
    ONE = [("II", 0, 1, sp.sqrt(Y), (3 - Y) / 2)]
    assert same_region(P1, S1) and same_region(P2, S2) and same_region(P1 + P2, ONE)
    a1, a2 = integrate(sp.Integer(1), P1), integrate(sp.Integer(1), P2)
    assert a1 == sp.Rational(1, 3) and a2 == sp.Rational(1, 4) and a1 + a2 == sp.Rational(7, 12)
    assert sp.integrate(1 - sp.sqrt(Y), (Y, 0, 1)) == sp.Rational(1, 3)
    assert sp.integrate((3 - Y) / 2 - 1, (Y, 0, 1)) == sp.Rational(1, 4)
    assert sp.integrate((3 - Y) / 2 - sp.sqrt(Y), (Y, 0, 1)) == sp.Rational(7, 12)
    assert all(((3 - Y) / 2 - sp.sqrt(Y)).subs(Y, sp.Rational(k, 10)) > 0 for k in range(10))
    return a1, a2


def style_plot(pfx, filled=False):
    """the region. Ids: {pfx}-ra/-rb pieces, -all whole, -cs/-cl curves, -ls/-ll/-ls2/-ll2 labels, -sa/-sb vertical
    strips, -ha/-hb horizontal strips per piece (y=0.5), -h0..-h2 full horizontal strips, -v1..-v3 vertices.
    filled=True shows the pieces, curves, labels and vertices from the start."""
    import math as m
    P = Plot(pfx, (-0.35, 2.0), (-0.35, 1.45), w=900, h=480, xticks=[(0.5, "0.5"), (1, "1")], yticks=[(0.5, "0.5")])
    pa = type1(lambda t: 0.0, lambda t: t * t, 0, 1)
    pb = type1(lambda t: 0.0, lambda t: 3 - 2 * t, 1, 1.5)
    pall = type2(lambda t: m.sqrt(t), lambda t: (3 - t) / 2, 0, 1)
    assert abs(shoelace(pa) - 1 / 3) < 1e-4 and abs(shoelace(pb) - 0.25) < 1e-9 and abs(shoelace(pall) - 7 / 12) < 2e-3
    hid = not filled
    P.fill(f"{pfx}-ra", pa, kind="a", hidden=hid)
    P.fill(f"{pfx}-rb", pb, kind="d", hidden=hid)
    P.fill(f"{pfx}-all", pall, kind="b")
    P.fn(f"{pfx}-cs", lambda t: t * t, -0.15, 1.15, kind="a", hidden=hid)
    P.fn(f"{pfx}-cl", lambda t: 3 - 2 * t, 0.78, 1.6, kind="d", hidden=hid)
    P.label(f"{pfx}-ls", 0.0, 1.0, "y = x²", kind="a", hidden=hid)
    P.label(f"{pfx}-ls2", 0.0, 0.8, "x = √y", kind="a")
    P.label(f"{pfx}-ll", 1.35, 0.95, "y = 3 − 2x", kind="d", hidden=hid)
    P.label(f"{pfx}-ll2", 1.35, 0.75, "x = (3 − y)/2", kind="d")
    P.vstrip(f"{pfx}-sa", 0.6, 0, 0.36)
    P.vstrip(f"{pfx}-sb", 1.25, 0, 0.5)
    P.hstrip(f"{pfx}-ha", 0.5, m.sqrt(0.5), 1)
    P.hstrip(f"{pfx}-hb", 0.5, 1, 1.25)
    for i, yy in enumerate((0.2, 0.5, 0.8)):
        P.hstrip(f"{pfx}-h{i}", yy, m.sqrt(yy), (3 - yy) / 2)
    P.dot(f"{pfx}-v1", 0, 0, "(0,0)", dx=-14, dy=36, anchor="end", hidden=hid)
    P.dot(f"{pfx}-v2", 1.5, 0, "(3/2,0)", dx=0, dy=40, anchor="middle", hidden=hid)
    P.dot(f"{pfx}-v3", 1, 1, "(1,1)", dx=-16, dy=-18, anchor="end", kind="b", hidden=hid)
    return P.svg()


# ---------------------------------------------------------------- HTML helpers
def eqs(pfx, lines, size=38, gap=14, shown=0):
    rows = "".join(f'<div id="{pfx}-{i}" class="di-eq{"" if i < shown else " h"}">{t}</div>' for i, t in enumerate(lines))
    return f'<div class="di-eqs" style="font-size:{size}px;gap:{gap}px">{rows}</div>'


def stem(qid, html_):
    return f'<div class="qstem"><span class="qid">{esc(qid)}</span>{html_}</div>'


def chip(id_, html_, kind="ok", hidden=True):
    return f'<div id="{id_}" class="di-chip {kind}{" h" if hidden else ""}">{html_}</div>'
