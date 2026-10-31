# -*- coding: utf-8 -*-
"""Stage widgets for the chain_rule videos (אינפי 2, K01-K08).

The SVG holds only geometry (lines, circles, arrows); every label is an absolutely positioned HTML box with $TeX$,
rendered later by the bank's KaTeX pipeline. Absolute boxes are overlays for layout_lint, so labels may sit on lines.

  tree(pfx, nodes, edges)    dependency tree z -> t -> x, y.  Ids: {pfx}-n-<k> node, {pfx}-e-<a>-<b> edge,
                             {pfx}-l-<a>-<b> edge label, {pfx}-he-<a>-<b> highlighted edge (route).
  vecplot(pfx, arrows)       unit circle + vectors from the origin (gradient, directions). Ids: {pfx}-a-<k> arrow,
                             {pfx}-al-<k> its label, {pfx}-circ the unit circle.
  lines(pfx, rows)           a stack of derivation lines revealed one by one. Ids: {pfx}-<key>.
"""
import math
import sympy as sp

NODE_R = 38

# ---------------------------------------------------------------- verification helpers (sympy)
x, y, z = sp.symbols("x y z", real=True)
# concrete g with g' and g'': an identity "for every g" is asserted for all of them (and for a symbolic g where useful)
GS = [(sp.sin, sp.cos, lambda a: -sp.sin(a)),
      (sp.exp, sp.exp, sp.exp),
      (lambda a: a**3 + a, lambda a: 3 * a**2 + 1, lambda a: 6 * a),
      (sp.atan, lambda a: 1 / (1 + a**2), lambda a: -2 * a / (1 + a**2)**2)]


def zero(e):
    """symbolic zero test (simplify), with a numeric fallback at a few points away from singularities"""
    if sp.simplify(e) == 0:
        return True
    syms = sorted(e.free_symbols, key=str)
    f = sp.lambdify(syms, e, "mpmath")
    import random
    rnd = random.Random(7)
    for _ in range(8):
        v = [rnd.uniform(0.6, 1.7) for _ in syms]
        if abs(complex(f(*v))) > 1e-10:
            return False
    return True


def for_all_g(check):
    """check(g, gp, gpp) -> expression that must vanish for every differentiable g"""
    for g, gp, gpp in GS:
        assert zero(check(g, gp, gpp)), (check(g, gp, gpp))
    return True


def _ids(pfx, a, b):
    return f"{pfx}-e-{a}-{b}", f"{pfx}-l-{a}-{b}"


def E(pfx, a, b):
    """ids of an edge and its label (for show/hide)"""
    return _ids(pfx, a, b)


def tree(pfx, nodes, edges, w=560, h=400, hidden=False, label_off=None, bend=None):
    """nodes: {key: (x, y, tex)}; edges: [(a, b, label_tex)] = a depends on b (drawn from a down to b).
    hidden=True: nodes and edges start invisible too (labels and highlights always start invisible).
    label_off: {(a, b): (dx, dy)} label offset from the edge midpoint; bend: {(a, b): k} quadratic bend (px)."""
    label_off = dict(label_off or {})
    bend = dict(bend or {})
    h_cls = " h" if hidden else ""
    svg = [f'<svg class="cr-tsvg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">']
    hi, labs = [], []
    for a, b, lab in edges:
        x1, y1, _ = nodes[a]
        x2, y2, _ = nodes[b]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy)
        ux, uy = dx / d, dy / d
        sx, sy = x1 + ux * NODE_R, y1 + uy * NODE_R
        ex, ey = x2 - ux * (NODE_R + 2), y2 - uy * (NODE_R + 2)
        k = bend.get((a, b), 0)
        mx, my = (sx + ex) / 2, (sy + ey) / 2
        nx, ny = -uy, ux
        cx, cy = mx + nx * k, my + ny * k
        path = f"M{sx:.1f},{sy:.1f} Q{cx:.1f},{cy:.1f} {ex:.1f},{ey:.1f}"
        eid, lid = _ids(pfx, a, b)
        svg.append(f'<path id="{eid}" class="cr-edge{h_cls}" d="{path}"/>')
        hi.append(f'<path id="{pfx}-he-{a}-{b}" class="cr-ehi h" d="{path}"/>')
        if lab:
            qx, qy = 0.25 * sx + 0.5 * cx + 0.25 * ex, 0.25 * sy + 0.5 * cy + 0.25 * ey
            ox, oy = label_off.get((a, b), (46 if x2 >= x1 else -46, 0))
            labs.append(f'<div id="{lid}" class="cr-elab h" style="left:{qx + ox:.0f}px;top:{qy + oy:.0f}px">${lab}$</div>')
    svg += hi + ["</svg>"]
    nd = []
    for k_, (x, y, tex) in nodes.items():
        nd.append(f'<div id="{pfx}-n-{k_}" class="cr-node{h_cls}" style="left:{x - NODE_R}px;top:{y - NODE_R}px">${tex}$</div>')
    return (f'<div class="cr-tree" id="{pfx}" style="width:{w}px;height:{h}px">' + "".join(svg) + "".join(nd)
            + "".join(labs) + "</div>")


def vecplot(pfx, arrows, R=170, size=440, axes=("x", "y"), hidden=False):
    """unit circle of radius R px and vectors from the origin. arrows: [(key, vx, vy, cls, label_tex, (dx, dy))]
    in units (1 = R px); cls: 'grad' | 'dir' | 'bad'. Everything but the axes starts hidden when hidden=True."""
    c = size / 2
    h_cls = " h" if hidden else ""
    out = [f'<div class="cr-plot" id="{pfx}" style="width:{size}px;height:{size}px">',
           f'<svg class="cr-psvg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">',
           '<defs>']
    for cls, col in (("grad", "#2dd4bf"), ("dir", "#fbbf24"), ("bad", "#fb7185")):
        out.append(f'<marker id="{pfx}-m-{cls}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" '
                   f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>')
    out.append('</defs>')
    out.append(f'<line class="cr-axis" x1="10" y1="{c}" x2="{size - 10}" y2="{c}"/>'
               f'<line class="cr-axis" x1="{c}" y1="{size - 10}" x2="{c}" y2="10"/>')
    out.append(f'<circle id="{pfx}-circ" class="cr-circ{h_cls}" cx="{c}" cy="{c}" r="{R}"/>')
    labs = []
    for key, vx, vy, cls, lab, (dx, dy) in arrows:
        ex, ey = c + vx * R, c - vy * R
        out.append(f'<line id="{pfx}-a-{key}" class="cr-arrow {cls} h" x1="{c}" y1="{c}" x2="{ex:.1f}" y2="{ey:.1f}" '
                   f'marker-end="url(#{pfx}-m-{cls})"/>')
        if lab:
            labs.append(f'<div id="{pfx}-al-{key}" class="cr-alab {cls} h" style="left:{ex + dx:.0f}px;top:{ey + dy:.0f}px">'
                        f'${lab}$</div>')
    out.append("</svg>")
    ax, ay = axes
    out.append(f'<div class="cr-axl" style="left:{size - 30}px;top:{c + 6}px">${ax}$</div>'
               f'<div class="cr-axl" style="left:{c + 10}px;top:0px">${ay}$</div>')
    out += labs + ["</div>"]
    return "".join(out)


def lines(pfx, rows, cls="", hidden=True):
    """rows: [(key, tex)] -> one line each, inline display-style math. Ids: {pfx}-<key>."""
    h_cls = " h" if hidden else ""
    body = "".join(f'<div id="{pfx}-{k}" class="cr-ln{h_cls}">$\\displaystyle {t}$</div>' for k, t in rows)
    return f'<div class="cr-lines {cls}">{body}</div>'


def big(id_, tex, hidden=True, size=None):
    st = f' style="font-size:{size}px"' if size else ""
    return f'<div id="{id_}" class="cr-big{" h" if hidden else ""}"{st}>$\\displaystyle {tex}$</div>'


def stack(*parts, gap=None):
    st = f' style="gap:{gap}px"' if gap else ""
    return f'<div class="cr-stack"{st}>' + "".join(parts) + "</div>"


def row(*parts):
    return '<div class="cr-row">' + "".join(parts) + "</div>"
