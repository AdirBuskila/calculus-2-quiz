# -*- coding: utf-8 -*-
"""Series widgets for the אינפי 2 videos (course `series`, S01..S08), plus the sympy checks the scripts assert with.

Stage widgets (HTML with $TeX$, rendered by the engine; every class is prefixed sr- so other courses are untouched):
  eqs(pfx, lines)          a column of display formulas revealed one by one: ids {pfx}-0, {pfx}-1, …  (all hidden)
  bars(pfx, values, …)     partial sums S_1..S_K as bars around a zero line, optional dashed limit line.
                           ids {pfx}-b{N} (N = 1..K, hidden), {pfx}-lim (the limit line + its label, hidden)
  numline(pfx, lo, hi, …)  a number line with the interval of convergence: ids {pfx}-band (inside, hidden),
                           {pfx}-out (the rays outside, hidden), {pfx}-{L|R}-q (a "?" over the endpoint),
                           {pfx}-{L|R}-o / -c (open / closed dot), {pfx}-{L|R}-v (verdict chip under it)
  verdict(id, text, ok)    a verdict pill (hidden)

Checks (sympy / mpmath; a script asserts every number it shows):
  lim(e), ratio(a), root(a), psums(a, K, n0), radius(c), tail_shrinks(a, n0)
"""
import html as _html
import sympy as sp
import mpmath as mp

n = sp.Symbol("n", positive=True, integer=True)
x = sp.Symbol("x", real=True)
oo = sp.oo


# ---------------------------------------------------------------- checks
_m = sp.Symbol("m", positive=True)          # sympy's limit with an integer symbol gets sin(π/n)·n wrong (0, not π):
                                            # every limit is taken in a positive real variable instead


def _lim(e):
    v = sp.limit(e.subs(n, _m), _m, oo)
    return v


def lim(e, var=n):
    return _lim(e) if var is n else sp.limit(e, var, oo)


def ratio(a):
    """lim a_{n+1}/a_n for a positive term a(n)"""
    return _lim(sp.simplify(sp.combsimp(a.subs(n, n + 1) / a)))


def root(a):
    """lim a_n^(1/n) for a positive term a(n)"""
    return _lim(a ** (1 / n))


def radius(c):
    """radius of sum c_n X^n from |c_n| (d'Alembert: lim |c_n / c_{n+1}|)"""
    return _lim(sp.simplify(sp.combsimp(c / c.subs(n, n + 1))))


def psums(a, K, n0=1):
    """exact-ish partial sums S_{n0}, …, S_{n0+K-1} of a(n) as floats (mpmath, 30 digits)"""
    f = sp.lambdify(n, a, "mpmath")
    mp.mp.dps = 30
    s, out = mp.mpf(0), []
    for k in range(n0, n0 + K):
        s += f(k)
        out.append(float(s))
    return out


def tail(a, N1, N2, n0=1):
    """S_{N2} - S_{N1} (float, mpmath nsum-free direct loop for moderate N; numpy for large)"""
    import numpy as np
    f = sp.lambdify(n, a, "numpy")
    k = np.arange(N1 + 1, N2 + 1, dtype=np.float64)
    return float(np.sum(f(k)))


# ---------------------------------------------------------------- stage widgets
def D(t):
    r"""every $…$ span is set in display style ($\displaystyle …$): big Σ limits and fractions"""
    import re
    return re.sub(r"\$(?!\\displaystyle)([^$]+)\$", lambda m: r"$\displaystyle " + m.group(1) + "$", fx(t))


def fx(t):
    r"""Chrome sets KaTeX's \ln n as 'lnn': put a thin space after \ln, \sin, \cos, \arctan before a letter/digit"""
    import re
    return re.sub(r"\\(ln|sin|cos|arctan)\s+(?=[A-Za-z0-9])", r"\\\1\\, ", t)


def eqs(pfx, lines, size=40, gap=18, shown=0):
    """display formulas, one per row; the first `shown` rows start visible"""
    rows = "".join(f'<div id="{pfx}-{i}" class="sr-eq{"" if i < shown else " h"}">{D(t)}</div>'
                   for i, t in enumerate(lines))
    return f'<div class="sr-eqs" style="font-size:{size}px;gap:{gap}px">{rows}</div>'


def bars(pfx, values, w=900, h=300, limit=None, limit_tex=None, label="", ymax=None, ymin=None, shown=0,
         nlabels=None, n0=1):
    """S_N bars. values[i] = S_{i+1}. The y range covers 0, every value and the limit."""
    vals = list(values) + ([limit] if limit is not None else [])
    top = max([0.0] + vals) if ymax is None else ymax
    bot = min([0.0] + vals) if ymin is None else ymin
    span = (top - bot) or 1.0
    pad_l, pad_b = 10, 34
    H = h - pad_b
    y = lambda v: 8 + (top - v) / span * (H - 16)
    K = len(values)
    bw = (w - pad_l) / K
    out = [f'<div class="sr-bars" id="{pfx}" style="width:{w + (190 if limit_tex else 0)}px;height:{h}px">',
           f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
           f'<line class="sr-zero" x1="0" x2="{w}" y1="{y(0):.1f}" y2="{y(0):.1f}"/>']
    nlabels = nlabels or {n0, K + n0 - 1} | {k for k in range(5, K + n0, 5)}
    for i, v in enumerate(values):
        x0 = pad_l + i * bw + bw * 0.14
        y0, y1 = sorted((y(0), y(v)))
        cls = "sr-bar neg" if v < 0 else "sr-bar"
        out.append(f'<g id="{pfx}-b{i + 1}"{"" if i < shown else " class=\"h\""}>'
                   f'<rect class="{cls}" x="{x0:.1f}" y="{y0:.1f}" width="{bw * 0.72:.1f}" height="{max(2.0, y1 - y0):.1f}" rx="4"/>')
        if i + n0 in nlabels:
            out.append(f'<text class="sr-bn" x="{x0 + bw * 0.36:.1f}" y="{h - 6}">{i + n0}</text>')
        out.append("</g>")
    if limit is not None:
        out.append(f'<g id="{pfx}-lim" class="h"><line class="sr-limline" x1="0" x2="{w}" y1="{y(limit):.1f}" '
                   f'y2="{y(limit):.1f}"/></g>')
    out.append("</svg>")
    if limit is not None and limit_tex:
        out.append(f'<div id="{pfx}-limt" class="sr-limlab h" style="left:{w + 14}px;top:{y(limit) - 26:.0f}px">{limit_tex}</div>')
    if label:
        out.append(f'<div class="sr-barlab">{label}</div>')
    out.append("</div>")
    return "".join(out)


def bars_do(pfx, a, b):
    """ids of bars a..b (inclusive) for show()"""
    return [f"{pfx}-b{k}" for k in range(a, b + 1)]


def numline(pfx, lo, hi, ticks, left, right, w=960, verdicts=None):
    """ticks: [(value, tex)], left/right = endpoint values. verdicts: {'L': (text, ok), 'R': (text, ok)}"""
    pad = 50
    X = lambda v: pad + (v - lo) / (hi - lo) * (w - 2 * pad)
    xl, xr = X(left), X(right)
    o = [f'<div class="sr-nl" id="{pfx}" style="width:{w}px">',
         '<div class="sr-axis"></div>',
         f'<div id="{pfx}-out" class="sr-out h"><i style="left:0;width:{xl - 14:.0f}px"></i>'
         f'<i style="left:{xr + 14:.0f}px;width:{w - xr - 14:.0f}px"></i></div>',
         f'<div id="{pfx}-band" class="sr-band h" style="left:{xl:.0f}px;width:{xr - xl:.0f}px"></div>']
    for v, tex in ticks:
        o.append(f'<i class="sr-tick" style="left:{X(v):.0f}px"></i>'
                 f'<span class="sr-tl" style="left:{X(v):.0f}px">{tex}</span>')
    for side, xv in (("L", xl), ("R", xr)):
        o.append(f'<b id="{pfx}-{side}-q" class="sr-qm h" style="left:{xv:.0f}px">?</b>'
                 f'<i id="{pfx}-{side}-o" class="sr-dot open h" style="left:{xv:.0f}px"></i>'
                 f'<i id="{pfx}-{side}-c" class="sr-dot closed h" style="left:{xv:.0f}px"></i>')
        if verdicts and side in verdicts:
            t, ok = verdicts[side]
            o.append(f'<span id="{pfx}-{side}-v" class="sr-ev {"ok" if ok else "bad"} h" style="left:{xv:.0f}px">'
                     f'{t}</span>')
    o.append("</div>")
    return "".join(o)


def verdict(id_, text, ok=True):
    return f'<div id="{id_}" class="sr-verdict {"ok" if ok else "bad"} h">{text}</div>'


def stem(qid, text):
    """the exam question in the panel (bank id chip + the statement)"""
    return f'<div class="qstem"><span class="qid">{qid}</span>{fx(text)}</div>'


def esc(s):
    return _html.escape(s, quote=True)


def fix_scenes(scenes):
    """apply fx() to every stage, panel and subtitle (thin space after ln/sin/cos/arctan); returns the scenes"""
    for S in scenes:
        S.stage, S.panel = fx(S.stage), fx(S.panel)
        for p in S.phrases:
            p.sub = fx(p.sub)
    return scenes
