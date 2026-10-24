"use strict";
/* Region-of-integration diagrams (window.Region) -- calculus-2 only, app-local. Adapted from
   probability-quiz/region.js (its expression language, column-interval shading and hydrate hook).
   A region spec is an entry of tools/verify/<CODE>/regions.json (tools/RAW_SCHEMA.md, "Region and contour diagrams"):
     { "id": "26A-A-Q1a",
       "inequalities": ["x>=0", "y<=2-x^2", ...],              the region (AND); the only required key
       "boundary_curves": ["y=2-x^2", ...],                     listed under the figure
       "orderXY" | "orderYX": {"x":[a,b], "y":[g1(x), g2(x)]}   an order of integration; the OUTER variable is the
                    one whose bounds are constants (the key name is not trusted); {"pieces":[{..},{..}]} = a sum
       "polar": {"r":[r1(theta), r2(theta)], "theta":[a,b]},
       "substitution": {"u":"y-x", "v":"x*y", "u_range":[..], "v_range":[..], "abs_jacobian_xy_over_uv":"1/(x+y)"},
       "vertices": [[x,y],...], "integrand": "x*exp(x^2)", "value": "(e^2-3)/2", "area": "3*pi", "view": {"x":[..],"y":[..]} }
   The region is shaded from the inequalities (columns refined by bisection) and outlined by marching squares.
   Views (a toggle): vertical strips (dy dx), horizontal strips (dx dy), polar rays (r, theta) and the u,v grid.
   Strips come from the data's bounds when that order is given, else from the inequalities. A polygon (every
   boundary linear, vertices given) gets the missing order's bounds computed from its vertices, marked as such.
   API: Region.figure(spec|[spec..]) -> HTML string;  Region.hydrate(el) renders .region-fig[data-region] inside el
        (the attribute holds the JSON spec, or a question id whose bank item carries `region`);
        Region.analyze(spec) -> numbers for tools/test_extras.js. Never uses eval / Function. Loadable in Node. */
(function (root) {
  /* =============================== tiny expression language (from probability) =============================== */
  const FUNCS = Object.assign(Object.create(null), { abs: Math.abs, sqrt: Math.sqrt, exp: Math.exp, log: Math.log, ln: Math.log, floor: Math.floor,
    ceil: Math.ceil, min: Math.min, max: Math.max, sin: Math.sin, cos: Math.cos, tan: Math.tan, atan: Math.atan,
    arctan: Math.atan, asin: Math.asin, acos: Math.acos, atan2: Math.atan2, sinh: Math.sinh, cosh: Math.cosh, tanh: Math.tanh });
  const CONSTS = Object.assign(Object.create(null), { pi: Math.PI, e: Math.E });   // null prototypes: "constructor" is not a name
  const CMP = new Set(["<", "<=", ">", ">=", "==", "!="]);
  function tokenize(src) {
    const out = []; let i = 0;
    const re = /\s*(?:(\d+\.?\d*(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?)|([A-Za-z_][A-Za-z0-9_]*)|(<=|>=|==|!=|&&|\|\||\*\*|[-+*/^(),<>!]))/y;
    while (i < src.length) {
      if (/^\s*$/.test(src.slice(i))) break;
      re.lastIndex = i;
      const m = re.exec(src);
      if (!m) throw new Error(`expression "${src}": unexpected character at ${i}`);
      i = re.lastIndex;
      if (m[1] != null) out.push({ t: "num", v: parseFloat(m[1]) });
      else if (m[2] != null) out.push({ t: "id", v: m[2] });
      else out.push({ t: "op", v: m[3] === "**" ? "^" : m[3] });
    }
    return out;
  }
  /* allowed: Set of variable names. Returns env => number. */
  function compile(src, allowed) {
    src = String(src);
    const toks = tokenize(src); let i = 0;
    const err = msg => new Error(`expression "${src}": ${msg}`);
    const isOp = v => toks[i] && toks[i].t === "op" && toks[i].v === v;
    const expect = v => { if (!isOp(v)) throw err(`expected "${v}"`); i++; };
    function pCmp() {
      const first = pAdd(), parts = []; let left = first;
      while (toks[i] && toks[i].t === "op" && CMP.has(toks[i].v)) {
        const op = toks[i++].v, a = left, b = pAdd();
        parts.push(op === "<" ? e => a(e) < b(e) ? 1 : 0 : op === "<=" ? e => a(e) <= b(e) ? 1 : 0 : op === ">" ? e => a(e) > b(e) ? 1 : 0
          : op === ">=" ? e => a(e) >= b(e) ? 1 : 0 : op === "==" ? e => a(e) === b(e) ? 1 : 0 : e => a(e) !== b(e) ? 1 : 0);
        left = b;
      }
      return !parts.length ? first : e => { for (const p of parts) if (!p(e)) return 0; return 1; };
    }
    function pAdd() {
      let a = pMul();
      while (isOp("+") || isOp("-")) { const op = toks[i++].v, x = a, b = pMul(); a = op === "+" ? e => x(e) + b(e) : e => x(e) - b(e); }
      return a;
    }
    function pMul() {
      let a = pUnary();
      while (isOp("*") || isOp("/")) { const op = toks[i++].v, x = a, b = pUnary(); a = op === "*" ? e => x(e) * b(e) : e => x(e) / b(e); }
      return a;
    }
    function pUnary() {
      if (isOp("-")) { i++; const a = pUnary(); return e => -a(e); }
      if (isOp("+")) { i++; return pUnary(); }
      return pPow();
    }
    function pPow() {
      const a = pAtom();
      if (isOp("^")) { i++; const b = pUnary(); return e => Math.pow(a(e), b(e)); }
      return a;
    }
    function pAtom() {
      const t = toks[i++];
      if (!t) throw err("unexpected end");
      if (t.t === "num") { const v = t.v; return () => v; }
      if (t.t === "id") {
        if (isOp("(")) {
          const f = FUNCS[t.v];
          if (!f) throw err(`unknown function ${t.v}()`);
          i++;
          const args = [];
          if (!isOp(")")) { args.push(pCmp()); while (isOp(",")) { i++; args.push(pCmp()); } }
          expect(")");
          if (args.length === 1) { const a0 = args[0]; return e => f(a0(e)); }
          return e => f.apply(null, args.map(a => a(e)));
        }
        const name = t.v;
        if (allowed && allowed.has(name)) return e => { const v = e[name]; if (v === undefined) throw err(`no value for ${name}`); return v; };
        if (name in CONSTS) { const v = CONSTS[name]; return () => v; }
        throw err(`unknown name ${name}`);
      }
      if (t.v === "(") { const a = pCmp(); expect(")"); return a; }
      throw err(`unexpected "${t.v}"`);
    }
    const fn = pCmp();
    if (i < toks.length) throw err(`unexpected "${toks[i].v}" after the end`);
    return fn;
  }
  const NOVARS = new Set(), XY = new Set(["x", "y"]), TH = new Set(["theta"]);
  const constant = v => typeof v === "number" ? v : compile(v, NOVARS)({});
  const Expr = { compile, constant, tokenize };

  /* "y-x>=1" -> g(x,y) with g >= 0 inside;  "y=x+1" -> h(x,y) = lhs - rhs */
  const stripNote = s => String(s).replace(/\(\s*[A-Za-z][A-Za-z ]*\)\s*$/, "").trim();
  function ineqFn(s) {
    s = stripNote(s);
    const m = s.match(/^(.*?)(<=|>=|<|>)(.*)$/);
    if (!m) throw new Error(`not an inequality: ${s}`);
    const a = compile(m[1], XY), b = compile(m[3], XY), env = { x: 0, y: 0 };
    return m[2][0] === "<" ? (x, y) => { env.x = x; env.y = y; return b(env) - a(env); } : (x, y) => { env.x = x; env.y = y; return a(env) - b(env); };
  }
  function curveFn(s) {
    const m = stripNote(s).match(/^([^<>=]*)=([^<>=]*)$/);
    if (!m) throw new Error(`not a curve: ${s}`);
    const a = compile(m[1], XY), b = compile(m[2], XY), env = { x: 0, y: 0 };
    return (x, y) => { env.x = x; env.y = y; return a(env) - b(env); };
  }
  function splitTop(s) {
    const out = []; let d = 0, cur = "";
    for (const ch of String(s)) { if (ch === "(") d++; else if (ch === ")") d--; if (ch === "," && d === 0) { out.push(cur); cur = ""; } else cur += ch; }
    out.push(cur); return out.map(t => t.trim()).filter(Boolean);
  }
  const fn1 = (src, name) => { const f = compile(src, new Set([name])), env = {}; return t => { env[name] = t; return f(env); }; };

  /* =============================== geometry helpers =============================== */
  function scanBox(pred, box, n) {
    let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
    const hx = (box[1] - box[0]) / (n - 1), hy = (box[3] - box[2]) / (n - 1);
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
      const x = box[0] + hx * i, y = box[2] + hy * j;
      if (pred(x, y)) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
    }
    return x0 > x1 ? null : [x0 - hx, x1 + hx, y0 - hy, y1 + hy];
  }
  function columnIntervals(pred, x, y0, y1, ny) {      // the y-intervals of {pred} on the line x = const
    const out = [], h = (y1 - y0) / ny;
    let prevIn = pred(x, y0 + h * 0.5), start = prevIn ? y0 : null;
    for (let j = 1; j < ny; j++) {
      const y = y0 + h * (j + 0.5), on = pred(x, y);
      if (on !== prevIn) {
        let lo = y - h, hi = y;
        for (let k = 0; k < 30; k++) { const m = (lo + hi) / 2; if (pred(x, m) === prevIn) lo = m; else hi = m; }
        const b = (lo + hi) / 2;
        if (on) start = b; else { out.push([start, b]); start = null; }
        prevIn = on;
      }
    }
    if (prevIn) out.push([start, y1]);
    return out;
  }
  /* marching squares: segments of {fn = 0} on an nx*ny grid over box, in data coordinates */
  function march(fn, box, nx, ny) {
    const [x0, x1, y0, y1] = box, hx = (x1 - x0) / nx, hy = (y1 - y0) / ny, V = [];
    for (let j = 0; j <= ny; j++) { const row = []; for (let i = 0; i <= nx; i++) row.push(fn(x0 + hx * i, y0 + hy * j)); V.push(row); }
    const segs = [];
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const a = V[j][i], b = V[j][i + 1], c = V[j + 1][i + 1], d = V[j + 1][i];
      if (![a, b, c, d].every(isFinite)) continue;
      const X = x0 + hx * i, Y = y0 + hy * j, P = [];
      const cut = (p, q, P1, P2) => { if ((p > 0) !== (q > 0)) { const t = p / (p - q); P.push([P1[0] + t * (P2[0] - P1[0]), P1[1] + t * (P2[1] - P1[1])]); } };
      const A = [X, Y], B = [X + hx, Y], C = [X + hx, Y + hy], D = [X, Y + hy];
      cut(a, b, A, B); cut(b, c, B, C); cut(c, d, C, D); cut(d, a, D, A);
      if (P.length === 2) segs.push([P[0][0], P[0][1], P[1][0], P[1][1]]);
      else if (P.length === 4) {
        const ctr = fn(X + hx / 2, Y + hy / 2);
        if ((ctr > 0) === (a > 0)) { segs.push([...P[0], ...P[3]]); segs.push([...P[1], ...P[2]]); }
        else { segs.push([...P[0], ...P[1]]); segs.push([...P[2], ...P[3]]); }
      }
    }
    return segs;
  }

  /* =============================== formatting =============================== */
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));
  const SUP = { 0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹", "-": "⁻" };
  /* an ASCII formula from the data -> readable text: sqrt(9-y^2) -> √(9−y²), 2*x -> 2x, pi -> π */
  function pretty(s) {
    s = String(s == null ? "" : s).replace(/\s+/g, "").replace(/\*\*/g, "^");
    // sqrt(...) with matching parens
    let out = "", i = 0;
    while (i < s.length) {
      if (s.startsWith("sqrt(", i)) {
        let d = 0, j = i + 4;
        for (; j < s.length; j++) { if (s[j] === "(") d++; else if (s[j] === ")") { d--; if (!d) break; } }
        const inner = pretty(s.slice(i + 5, j));
        out += /^[\w.π²³]+$/.test(inner) ? "√" + inner : "√(" + inner + ")";
        i = j + 1;
      } else { out += s[i]; i++; }
    }
    s = out
      .replace(/\btheta\b/g, "θ").replace(/\bpi\b/g, "π")
      .replace(/\^(?:\((-?\d+)\)|(\d+))/g, (m, a, b) => (a || b).split("").map(c => SUP[c]).join(""))
      .replace(/(^|[^√\w.])(\d+(?:\.\d+)?)\*(?=[A-Za-zθπ(√])/g, "$1$2")
      .replace(/\*/g, "·").replace(/-/g, "−")
      .replace(/<=/g, " ≤ ").replace(/>=/g, " ≥ ").replace(/(?<![≤≥ ])([<>])(?![ ])/g, " $1 ").replace(/(?<![≤≥<> ])=(?! )/g, " = ");
    return s.replace(/([^\s(])([+−])(?=[^\s)])/g, "$1$2");
  }
  function frac(v, maxDen) {
    maxDen = maxDen || 60;
    if (!isFinite(v)) return null;
    if (Math.abs(v - Math.round(v)) < 1e-9) return String(Math.round(v));
    for (let d = 2; d <= maxDen; d++) { const n = Math.round(v * d); if (Math.abs(v - n / d) < 1e-9) return `${n}/${d}`; }
    return null;
  }
  const dec = (v, k) => String(Math.round(v * Math.pow(10, k)) / Math.pow(10, k));
  const numTxt = v => { const f = frac(v); return (f || dec(v, 3)).replace(/-/g, "−"); };
  const ltr = h => `<bdi dir="ltr" class="rg-math">${h}</bdi>`;
  function ticksFor(a, b) {
    const r = b - a, steps = [0.1, 0.2, 0.25, 0.5, 1, 2, 2.5, 5, 10, 20, 25, 50];
    const st = steps.find(t => r / t <= 6) || r / 5, out = [];
    for (let v = Math.ceil(a / st - 1e-9) * st; v <= b + 1e-9; v += st) out.push(Math.round(v * 1e9) / 1e9);
    return out;
  }

  /* =============================== the spec =============================== */
  /* an order object -> [{outer, inner, a, b, lo(t), hi(t), src}] (outer = the variable with constant bounds) */
  function orderParts(o) {
    const pieces = Array.isArray(o.pieces) ? o.pieces : [o];
    return pieces.map(pc => {
      if (!Array.isArray(pc.x) || !Array.isArray(pc.y)) throw new Error("an order needs x and y bounds");
      const dep = (arr, v) => arr.some(t => typeof t === "string" && new RegExp(`\\b${v}\\b`).test(t));
      const outer = !dep(pc.x, "y") ? "x" : !dep(pc.y, "x") ? "y" : null;
      if (!outer) throw new Error("neither variable has constant bounds");
      const inner = outer === "x" ? "y" : "x", ob = pc[outer], ib = pc[inner];
      return { outer, inner, a: constant(ob[0]), b: constant(ob[1]), lo: fn1(ib[0], outer), hi: fn1(ib[1], outer),
        src: { outer: ob.map(String), inner: ib.map(String) } };
    });
  }
  function prepare(spec) {
    if (!spec || typeof spec !== "object") throw new Error("region must be an object");
    const list = Array.isArray(spec.inequalities) ? spec.inequalities : typeof spec.inequalities === "string" ? splitTop(spec.inequalities) : null;
    if (!list || !list.length) throw new Error("region needs inequalities");
    const gs = list.map(ineqFn);
    const pred = (x, y) => { for (const g of gs) { const v = g(x, y); if (!(v >= 0)) return false; } return true; };
    const curves = (spec.boundary_curves || []).map(String);
    const orders = { v: null, h: null }, given = [];
    for (const key of Object.keys(spec)) if (key === "orderXY" || key === "orderYX") {
      const parts = orderParts(spec[key]), view = parts[0].outer === "x" ? "v" : "h";
      if (parts.some(p => p.outer !== parts[0].outer)) throw new Error(`${key}: pieces mix outer variables`);
      orders[view] = { parts, derived: false }; given.push(view);
    }
    let polar = null;
    if (spec.polar) {
      const p = spec.polar;
      polar = { r1: fn1(p.r[0], "theta"), r2: fn1(p.r[1], "theta"), t1: constant(p.theta[0]), t2: constant(p.theta[1]), src: p };
      given.push("p");
    }
    let sub = null;
    if (spec.substitution) {
      const s = spec.substitution;
      sub = { U: (() => { const f = compile(s.u, XY), e = {}; return (x, y) => { e.x = x; e.y = y; return f(e); }; })(),
        V: (() => { const f = compile(s.v, XY), e = {}; return (x, y) => { e.x = x; e.y = y; return f(e); }; })(),
        u: s.u_range.map(constant), v: s.v_range.map(constant), src: s };
      given.push("uv");
    }
    // view box: spec.view, else the region's bounding box (scanned), padded, with equal scales
    let tight;
    if (spec.view) tight = [constant(spec.view.x[0]), constant(spec.view.x[1]), constant(spec.view.y[0]), constant(spec.view.y[1])];
    else {
      let b = scanBox(pred, [-12, 12, -12, 12], 241);
      if (!b) throw new Error("the inequalities describe an empty region");
      for (let k = 0; k < 2; k++) b = scanBox(pred, b, 161) || b;
      tight = b;
    }
    let [x0, x1, y0, y1] = tight;
    const pad = 0.14 * Math.max(x1 - x0, y1 - y0);
    x0 -= pad; x1 += pad; y0 -= pad; y1 += pad;
    const near = (a, b2) => a <= 0 && b2 >= 0 || Math.min(Math.abs(a), Math.abs(b2)) < 0.35 * (b2 - a);
    if (polar || near(x0, x1)) { x0 = Math.min(x0, -pad * 0.6); x1 = Math.max(x1, pad * 0.6); }
    if (polar || near(y0, y1)) { y0 = Math.min(y0, -pad * 0.6); y1 = Math.max(y1, pad * 0.6); }
    const rx = x1 - x0, ry = y1 - y0, LIM = 1.25;   // keep circles round: widen the short side, never squash
    if (ry / rx > LIM) { const w = ry / LIM, c = (x0 + x1) / 2; x0 = c - w / 2; x1 = c + w / 2; }
    else if (rx / ry > LIM) { const h = rx / LIM, c = (y0 + y1) / 2; y0 = c - h / 2; y1 = c + h / 2; }
    const R = { spec, gs, pred, curves, orders, given, polar, sub, tight, box: [x0, x1, y0, y1] };
    for (const view of ["v", "h"]) if (!orders[view]) orders[view] = derivePolygon(R, view);
    return R;
  }

  /* a polygon region (every inequality linear, vertices given): the bounds of an order the data does not give */
  function isLinear(g, box) {
    const pts = [[0.13, 0.71], [0.62, 0.27], [0.91, 0.55], [0.35, 0.18]].map(([a, b]) => [box[0] + a * (box[1] - box[0]), box[2] + b * (box[3] - box[2])]);
    const s = Math.max(1, ...pts.map(p => Math.abs(g(p[0], p[1]))));
    for (let i = 0; i < pts.length; i++) for (let j = i + 1; j < pts.length; j++) {
      const p = pts[i], q = pts[j], m = g((p[0] + q[0]) / 2, (p[1] + q[1]) / 2);
      if (Math.abs(g(p[0], p[1]) + g(q[0], q[1]) - 2 * m) > 1e-9 * s) return false;
    }
    return true;
  }
  function derivePolygon(R, view) {
    const vs = (R.spec.vertices || []).map(p => [constant(p[0]), constant(p[1])]);
    if (vs.length < 3 || !R.gs.every(g => isLinear(g, R.box))) return null;
    const cx = vs.reduce((s, p) => s + p[0], 0) / vs.length, cy = vs.reduce((s, p) => s + p[1], 0) / vs.length;
    const hull = vs.slice().sort((p, q) => Math.atan2(p[1] - cy, p[0] - cx) - Math.atan2(q[1] - cy, q[0] - cx));
    const [o, n] = view === "v" ? [0, 1] : [1, 0];          // outer / inner coordinate index
    const cuts = [...new Set(hull.map(p => +p[o].toFixed(12)))].sort((a, b) => a - b);
    const edges = hull.map((p, i) => [p, hull[(i + 1) % hull.length]]).filter(([p, q]) => Math.abs(p[o] - q[o]) > 1e-12);
    const line = ([p, q]) => { const m = (q[n] - p[n]) / (q[o] - p[o]); return { m, c: p[n] - m * p[o] }; };
    const parts = [];
    for (let k = 0; k + 1 < cuts.length; k++) {
      const a = cuts[k], b = cuts[k + 1], mid = (a + b) / 2;
      const hits = edges.filter(([p, q]) => Math.min(p[o], q[o]) <= mid && Math.max(p[o], q[o]) >= mid).map(line)
        .map(L => ({ ...L, at: L.m * mid + L.c })).sort((u, w) => u.at - w.at);
      if (hits.length < 2) return null;
      const lo = hits[0], hi = hits[hits.length - 1], ov = view === "v" ? "x" : "y";
      const txt = L => { const m = frac(L.m), c = frac(L.c); if (m == null || c == null) return null;
        const [mp, mq] = m.split("/"), lead = mp === "1" ? "" : mp === "-1" ? "-" : mp;
        const mt = m === "0" ? "" : mq ? `${lead}${lead && lead !== "-" ? "*" : ""}${ov}/${mq}` : `${lead}${lead && lead !== "-" ? "*" : ""}${ov}`;   // -1/2 -> -y/2
        if (!mt) return c;
        if (c === "0") return mt;
        return mt[0] === "-" ? `${c}${mt}` : `${mt}${c[0] === "-" ? "" : "+"}${c}`; };   // 6-2*x, x+1
      const ta = frac(a), tb = frac(b), tl = txt(lo), th = txt(hi);
      if ([ta, tb, tl, th].some(t => t == null)) return null;
      parts.push({ outer: ov, inner: ov === "x" ? "y" : "x", a, b, lo: t => lo.m * t + lo.c, hi: t => hi.m * t + hi.c, src: { outer: [ta, tb], inner: [tl, th] } });
    }
    return parts.length ? { parts, derived: true } : null;
  }

  /* numbers the node test checks: area of the inequality set vs. the area of each description */
  function analyze(spec) {
    const R = prepare(spec), [x0, x1, y0, y1] = R.tight, NX = 600, w = (x1 - x0) / NX;
    let area = 0;
    for (let i = 0; i < NX; i++) for (const [p, q] of columnIntervals(R.pred, x0 + w * (i + 0.5), y0, y1, 400)) area += (q - p) * w;
    const simpson = (f, a, b, n) => { n = n || 400; const h = (b - a) / n; let s = f(a) + f(b); for (let k = 1; k < n; k++) s += (k % 2 ? 4 : 2) * f(a + k * h); return s * h / 3; };
    const out = { area, orders: {}, polar: null };
    for (const view of ["v", "h"]) if (R.orders[view]) out.orders[view] = { derived: R.orders[view].derived,
      area: R.orders[view].parts.reduce((s, p) => s + simpson(t => p.hi(t) - p.lo(t), p.a, p.b), 0) };
    if (R.polar) out.polar = simpson(t => (R.polar.r2(t) ** 2 - R.polar.r1(t) ** 2) / 2, R.polar.t1, R.polar.t2);
    out.views = viewsOf(R);
    return out;
  }
  const viewsOf = R => ["v", "h", "p", "uv"].filter(v => v === "v" || v === "h" || (v === "p" && R.polar) || (v === "uv" && R.sub));

  /* =============================== SVG =============================== */
  let UID = 0;
  const VIEW_LABEL = { v: "רצועות אנכיות", h: "רצועות אופקיות", p: "קוטבי", uv: "u, v" };
  function svgOf(R) {
    const id = "rg" + (++UID), [x0, x1, y0, y1] = R.box, rx = x1 - x0, ry = y1 - y0;
    const PW = ry > rx ? 280 * rx / ry : 280, PH = PW * ry / rx;
    const ML = 34, MR = 14, MT = 18, MB = 28, W = ML + PW + MR, H = MT + PH + MB;
    const X = x => ML + (x - x0) / rx * PW, Y = y => MT + (y1 - y) / ry * PH;
    const f1 = v => Math.round(v * 10) / 10;
    let g = "";
    for (const v of ticksFor(x0, x1)) g += `<line class="rg-grid" x1="${f1(X(v))}" y1="${MT}" x2="${f1(X(v))}" y2="${f1(MT + PH)}"/><text class="rg-tl" x="${f1(X(v))}" y="${f1(MT + PH + 13)}" text-anchor="middle">${esc(numTxt(v))}</text>`;
    for (const v of ticksFor(y0, y1)) g += `<line class="rg-grid" x1="${ML}" y1="${f1(Y(v))}" x2="${f1(ML + PW)}" y2="${f1(Y(v))}"/><text class="rg-tl" x="${ML - 5}" y="${f1(Y(v) + 3.5)}" text-anchor="end">${esc(numTxt(v))}</text>`;
    if (x0 < 0 && x1 > 0) g += `<line class="rg-axis" x1="${f1(X(0))}" y1="${MT}" x2="${f1(X(0))}" y2="${f1(MT + PH)}"/>`;
    if (y0 < 0 && y1 > 0) g += `<line class="rg-axis" x1="${ML}" y1="${f1(Y(0))}" x2="${f1(ML + PW)}" y2="${f1(Y(0))}"/>`;
    // shading (columns) and outline (each inequality's zero set, kept where the others hold)
    const NX = 150, cw = rx / NX;
    let shade = "";
    for (let i = 0; i < NX; i++) {
      const xa = x0 + cw * i, xl = f1(X(xa)), xr = f1(X(xa + cw) + 0.6);
      for (const [p, q] of columnIntervals(R.pred, xa + cw / 2, y0, y1, 160)) shade += `M${xl} ${f1(Y(q))}H${xr}V${f1(Y(p))}H${xl}Z`;
    }
    const segPath = segs => segs.map(s => `M${f1(X(s[0]))} ${f1(Y(s[1]))}L${f1(X(s[2]))} ${f1(Y(s[3]))}`).join("");
    const scale = R.gs.map(gf => { let m = 1e-12; for (let i = 0; i <= 8; i++) for (let j = 0; j <= 8; j++) m = Math.max(m, Math.abs(gf(x0 + rx * i / 8, y0 + ry * j / 8)) || 0); return m; });
    const okAt = (px, py, skip) => R.gs.every((gf, k) => k === skip || gf(px, py) >= -2e-3 * scale[k]);
    let outline = "";
    R.gs.forEach((gf, k) => { outline += segPath(march(gf, R.box, 140, 140).filter(s => okAt((s[0] + s[2]) / 2, (s[1] + s[3]) / 2, k))); });
    let curves = "";
    for (const c of R.curves) { try { curves += segPath(march(curveFn(c), R.box, 120, 120)); } catch (e) { /* listed only */ } }
    // layers
    const [tx0, tx1, ty0, ty1] = R.tight, N = 7;
    function strips(view) {
      const o = R.orders[view], vert = view === "v", out = [];
      const a = vert ? tx0 : ty0, b = vert ? tx1 : ty1;
      for (let k = 0; k < N; k++) {
        const t = a + (b - a) * (k + 0.5) / N;
        let ivs;
        if (o) { ivs = o.parts.filter(p => t >= p.a - 1e-12 && t <= p.b + 1e-12).map(p => [p.lo(t), p.hi(t)]); }
        else ivs = vert ? columnIntervals(R.pred, t, y0, y1, 200) : columnIntervals((yy, xx) => R.pred(xx, yy), t, x0, x1, 200);
        for (const iv of ivs.slice(0, 1)) out.push([t, iv[0], iv[1]]);
      }
      const wd = (vert ? PW : PH) * 0.28 / N;
      return out.map(([t, p, q]) => vert
        ? `<rect class="rg-strip" x="${f1(X(t) - wd / 2)}" y="${f1(Y(q))}" width="${f1(wd)}" height="${f1(Math.max(0.5, Y(p) - Y(q)))}"/><circle class="rg-end" cx="${f1(X(t))}" cy="${f1(Y(p))}" r="2.3"/><circle class="rg-end" cx="${f1(X(t))}" cy="${f1(Y(q))}" r="2.3"/>`
        : `<rect class="rg-strip" x="${f1(X(p))}" y="${f1(Y(t) - wd / 2)}" width="${f1(Math.max(0.5, X(q) - X(p)))}" height="${f1(wd)}"/><circle class="rg-end" cx="${f1(X(p))}" cy="${f1(Y(t))}" r="2.3"/><circle class="rg-end" cx="${f1(X(q))}" cy="${f1(Y(t))}" r="2.3"/>`).join("");
    }
    let layers = `<g class="rg-l rg-l-v">${strips("v")}</g><g class="rg-l rg-l-h">${strips("h")}</g>`;
    if (R.polar) {
      const P = R.polar, big = 2 * Math.hypot(Math.max(-x0, x1), Math.max(-y0, y1));
      let s = "";
      for (const t of [P.t1, P.t2]) s += `<line class="rg-ray" x1="${f1(X(0))}" y1="${f1(Y(0))}" x2="${f1(X(big * Math.cos(t)))}" y2="${f1(Y(big * Math.sin(t)))}"/>`;
      for (const src of P.src.r) if (typeof src === "number" || !/theta/.test(String(src))) { const rr = constant(src); if (rr > 0) s += `<circle class="rg-ray" cx="${f1(X(0))}" cy="${f1(Y(0))}" r="${f1(rr / rx * PW)}"/>`; }
      for (let k = 0; k < N; k++) {
        const t = P.t1 + (P.t2 - P.t1) * (k + 0.5) / N, a = P.r1(t), b = P.r2(t);
        s += `<line class="rg-rstrip" x1="${f1(X(a * Math.cos(t)))}" y1="${f1(Y(a * Math.sin(t)))}" x2="${f1(X(b * Math.cos(t)))}" y2="${f1(Y(b * Math.sin(t)))}"/>` +
          `<circle class="rg-end" cx="${f1(X(a * Math.cos(t)))}" cy="${f1(Y(a * Math.sin(t)))}" r="2.3"/><circle class="rg-end" cx="${f1(X(b * Math.cos(t)))}" cy="${f1(Y(b * Math.sin(t)))}" r="2.3"/>`;
      }
      s += `<circle class="rg-origin" cx="${f1(X(0))}" cy="${f1(Y(0))}" r="2.6"/>`;
      layers += `<g class="rg-l rg-l-p">${s}</g>`;
    }
    if (R.sub) {
      const S = R.sub, lv = (r, k) => r[0] + (r[1] - r[0]) * k / 4;
      const inside = s => R.pred((s[0] + s[2]) / 2, (s[1] + s[3]) / 2) || okAt((s[0] + s[2]) / 2, (s[1] + s[3]) / 2, -1);
      let su = "", sv = "";
      for (let k = 1; k < 4; k++) {
        const cu = lv(S.u, k), cv = lv(S.v, k);
        su += segPath(march((xx, yy) => S.U(xx, yy) - cu, R.box, 140, 140).filter(inside));
        sv += segPath(march((xx, yy) => S.V(xx, yy) - cv, R.box, 140, 140).filter(inside));
      }
      layers += `<g class="rg-l rg-l-uv"><path class="rg-ucurve" d="${su}"/><path class="rg-vcurve" d="${sv}"/></g>`;
    }
    const svg =
      `<svg class="rg-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${f1(W)} ${f1(H)}" width="${f1(W)}" height="${f1(H)}" direction="ltr" role="img" aria-label="region">` +
      `<defs><clipPath id="${id}c"><rect x="${ML}" y="${MT}" width="${f1(PW)}" height="${f1(PH)}"/></clipPath></defs>` +
      `<rect class="rg-space" x="${ML}" y="${MT}" width="${f1(PW)}" height="${f1(PH)}"/>` + g +
      `<g clip-path="url(#${id}c)"><path class="rg-region" d="${shade}"/><path class="rg-curve" d="${curves}"/>${layers}<path class="rg-outline" d="${outline}"/></g>` +
      `<rect class="rg-frame" x="${ML}" y="${MT}" width="${f1(PW)}" height="${f1(PH)}"/>` +
      `<text class="rg-ax" x="${f1(ML + PW)}" y="${f1(MT + PH + 25)}" text-anchor="end">x</text>` +
      `<text class="rg-ax" x="${ML - 22}" y="${MT + 4}" text-anchor="middle">y</text></svg>`;
    return svg;
  }

  /* the bounds rows (each description; the active view is highlighted) */
  function rowsOf(R) {
    const rows = [];
    for (const view of ["v", "h"]) {
      const o = R.orders[view], d = view === "v" ? "dy dx" : "dx dy";
      let body;
      // each piece: "a ≤ x ≤ b," and "g1 ≤ y ≤ g2" are unbreakable halves, so a narrow screen wraps between them only
      if (o) body = o.parts.map((p, k) => ltr((k ? `<span class="rg-cup">∪</span>` : "") +
        `<span class="rg-nw">${esc(`${pretty(p.src.outer[0])} ≤ ${p.outer} ≤ ${pretty(p.src.outer[1])},`)}</span> ` +
        `<span class="rg-nw">${esc(`${pretty(p.src.inner[0])} ≤ ${p.inner} ≤ ${pretty(p.src.inner[1])}`)}</span>`)).join("");
      rows.push(`<div class="rg-row" data-view="${view}"><span class="rg-rl">${VIEW_LABEL[view]} ${ltr(d)}${o && o.derived ? `<span class="rg-derived">מחושב מהקודקודים</span>` : ""}</span>` +
        (o ? `<span class="rg-rx">${body}</span>` : `<span class="rg-rx rg-none">אין בפתרון גבולות בסדר הזה; הרצועות בציור מחושבות מהאי-שוויונות.</span>`) + `</div>`);
    }
    if (R.polar) {
      const p = R.polar.src;
      rows.push(`<div class="rg-row" data-view="p"><span class="rg-rl">קואורדינטות קוטביות ${ltr("r dr dθ")}</span><span class="rg-rx">${ltr(esc(`${pretty(p.theta[0])} ≤ θ ≤ ${pretty(p.theta[1])},  ${pretty(p.r[0])} ≤ r ≤ ${pretty(p.r[1])}`))}</span></div>`);
    }
    if (R.sub) {
      const s = R.sub.src;
      rows.push(`<div class="rg-row" data-view="uv"><span class="rg-rl">החלפת משתנים ${ltr("du dv")}</span><span class="rg-rx">${ltr(esc(`u = ${pretty(s.u)},  v = ${pretty(s.v)}`))}` +
        `${ltr(esc(`${pretty(s.u_range[0])} ≤ u ≤ ${pretty(s.u_range[1])},  ${pretty(s.v_range[0])} ≤ v ≤ ${pretty(s.v_range[1])}`))}` +
        `${ltr(esc(`|J| = ${pretty(s.abs_jacobian_xy_over_uv)}`))}</span></div>`);
    }
    return rows.join("");
  }

  function figureOne(spec) {
    try {
      const R = prepare(spec), views = viewsOf(R);
      const first = R.given[0] || "v";
      const tabs = `<div class="rg-tabs" role="group" aria-label="תצוגה">` + views.map(v =>
        `<button type="button" class="rg-tab" data-rg-view="${v}" aria-pressed="${v === first}">${VIEW_LABEL[v] === "u, v" ? ltr("u, v") : VIEW_LABEL[v]}</button>`).join("") + `</div>`;
      const s = R.spec;
      const val = s.value != null && s.integrand && !/f\(/.test(s.integrand) ? `<div class="rg-val">${ltr(esc(`∬ ${pretty(s.integrand)} dA = ${pretty(s.value)}`))}</div>`
        : s.area != null ? `<div class="rg-val">שטח התחום: ${ltr(esc(pretty(s.area)))}</div>` : "";
      const curves = R.curves.length ? `<div class="rg-curves"><span class="rg-cl">שפת התחום:</span> ${R.curves.map(c => ltr(esc(pretty(c)))).join("")}</div>` : "";
      return `<div class="region-fig" data-rg="1" data-view="${first}">` +
        `<div class="rg-title">תחום האינטגרציה</div>${tabs}<div class="rg-plot" dir="ltr">${svgOf(R)}</div>` +
        `<div class="rg-rows">${rowsOf(R)}</div>${curves}${val}</div>`;
    } catch (e) {
      return `<div class="region-fig" data-rg="1"><div class="rg-error">לא ניתן לצייר את התחום (${esc(e.message)})</div></div>`;
    }
  }
  function figure(spec) { return (Array.isArray(spec) ? spec : [spec]).map(figureOne).join(""); }

  /* a hook's value: JSON, or the id of a bank item that carries `region` */
  function lookup(val, key) {
    const v = String(val || "").trim();
    if (v[0] === "{" || v[0] === "[") return JSON.parse(v);
    const qs = (root.OPEN_BANK && root.OPEN_BANK.questions) || [];
    for (const q of qs) for (const s of [].concat(q[key] || [])) if (s && s.id === v) return s;
    throw new Error(`unknown id ${v}`);
  }
  function hydrate(el) {
    if (!el || !el.querySelectorAll) return 0;
    const hosts = [...el.querySelectorAll(".region-fig[data-region]:not([data-rg])")];
    if (el.matches && el.matches(".region-fig[data-region]:not([data-rg])")) hosts.unshift(el);
    for (const h of hosts) {
      let html;
      try { html = figure(lookup(h.getAttribute("data-region"), "region")); }
      catch (e) { html = `<div class="region-fig" data-rg="1"><div class="rg-error">לא ניתן לצייר את התחום (${esc(e.message)})</div></div>`; }
      const tmp = h.ownerDocument.createElement("div"); tmp.innerHTML = html;
      h.replaceWith(...tmp.childNodes);
    }
    return hosts.length;
  }
  if (typeof document !== "undefined") {
    document.addEventListener("click", e => {
      const b = e.target.closest && e.target.closest("[data-rg-view]");
      if (!b) return;
      const fig = b.closest(".region-fig");
      fig.dataset.view = b.dataset.rgView;
      fig.querySelectorAll("[data-rg-view]").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
    });
    if (typeof MutationObserver !== "undefined") {
      const start = () => {
        hydrate(document.body);
        new MutationObserver(ms => { for (const m of ms) for (const n of m.addedNodes) if (n.nodeType === 1) hydrate(n); })
          .observe(document.body, { childList: true, subtree: true });
      };
      if (document.body) start(); else document.addEventListener("DOMContentLoaded", start);
    }
  }

  const Region = { figure, hydrate, analyze, pretty, Expr, _: { prepare, march, columnIntervals, ineqFn, curveFn, splitTop, lookup } };
  root.Region = Region;
  if (typeof module !== "undefined" && module.exports) module.exports = Region;
})(typeof window !== "undefined" ? window : globalThis);
