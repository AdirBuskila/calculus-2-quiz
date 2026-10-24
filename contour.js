"use strict";
/* Contour plots for extrema and Lagrange questions (window.Contour) -- calculus-2 only, app-local, no dependencies.
   A contour spec is an entry of tools/verify/<CODE>/contours.json (tools/RAW_SCHEMA.md, "Region and contour diagrams"):
     { "id": "26A-A-Q4b", "f": "x^3+x^2-3*x+y^2", "domain": [[x0,x1],[y0,y1]],
       "kind": "unconstrained" | "lagrange" | "closed_region",      ("closed-region" is accepted)
       "constraint": "x^2+y^2=4" | "x^2+y^2<=2 (closed disk)" | null,
       "region": "x>=0, y<=1, y>=x" | [ineq, ...],                  closed_region: the region (else an inequality constraint)
       "critical_points": [{"x": "1/2", "y": 1, "f": -1.125, "role": "abs min"}, ...] }
   Draws: level curves of f (marching squares on a grid, levels at quantiles of f plus every critical value), the
   constraint curve (lagrange) or the shaded closed region and its boundary, the critical points (marker by
   classification, numbered, listed under the plot) and, at each point on the constraint / region boundary,
   the gradient arrows grad f (solid) and grad g (dashed): at a Lagrange point they are parallel.
   f is evaluated by the small parser below (numbers, x, y, + - * / ^, unary minus, parentheses, sqrt exp ln log
   sin cos tan atan abs sinh cosh, pi, e). Never eval / Function.
   API: Contour.figure(spec|[spec..]) -> HTML; Contour.hydrate(el) renders .contour-fig[data-contour] (JSON or a
   question id whose bank item carries `contour`); Contour.compile(src, vars) -> env => number. Loadable in Node. */
(function (root) {
  /* ---------------- tiny expression parser ---------------- */
  const FN = Object.assign(Object.create(null), { sqrt: Math.sqrt, exp: Math.exp, ln: Math.log, log: Math.log, sin: Math.sin, cos: Math.cos, tan: Math.tan,
    atan: Math.atan, arctan: Math.atan, abs: Math.abs, sinh: Math.sinh, cosh: Math.cosh });
  const K = Object.assign(Object.create(null), { pi: Math.PI, e: Math.E });   // null prototypes: "constructor" is not a name
  function compile(src, vars) {
    src = String(src);
    const toks = [], re = /\s*(?:(\d+\.?\d*(?:[eE][+-]?\d+)?|\.\d+)|([A-Za-z_]\w*)|(\*\*|[-+*/^(),]))/y;
    for (let i = 0; i < src.length;) {
      if (/^\s*$/.test(src.slice(i))) break;
      re.lastIndex = i; const m = re.exec(src);
      if (!m) throw new Error(`f "${src}": unexpected character at ${i}`);
      i = re.lastIndex;
      toks.push(m[1] != null ? { n: +m[1] } : m[2] != null ? { id: m[2] } : { op: m[3] === "**" ? "^" : m[3] });
    }
    let i = 0;
    const is = o => toks[i] && toks[i].op === o, err = m => new Error(`f "${src}": ${m}`);
    const add = () => { let a = mul(); while (is("+") || is("-")) { const o = toks[i++].op, l = a, r = mul(); a = o === "+" ? e => l(e) + r(e) : e => l(e) - r(e); } return a; };
    const mul = () => { let a = un(); while (is("*") || is("/")) { const o = toks[i++].op, l = a, r = un(); a = o === "*" ? e => l(e) * r(e) : e => l(e) / r(e); } return a; };
    const un = () => { if (is("-")) { i++; const a = un(); return e => -a(e); } if (is("+")) { i++; return un(); } return pw(); };
    const pw = () => { const a = atom(); if (is("^")) { i++; const b = un(); return e => Math.pow(a(e), b(e)); } return a; };
    function atom() {
      const t = toks[i++];
      if (!t) throw err("unexpected end");
      if (t.n != null) return () => t.n;
      if (t.op === "(") { const a = add(); if (!is(")")) throw err('expected ")"'); i++; return a; }
      if (t.id != null) {
        if (is("(")) {
          const f = FN[t.id]; if (!f) throw err(`unknown function ${t.id}()`);
          i++; const a = add(); if (!is(")")) throw err('expected ")"'); i++;
          return e => f(a(e));
        }
        if (vars.includes(t.id)) return e => e[t.id];
        if (t.id in K) return () => K[t.id];
        throw err(`unknown name ${t.id}`);
      }
      throw err(`unexpected "${t.op}"`);
    }
    const fn = add();
    if (i < toks.length) throw err(`unexpected "${toks[i].op || toks[i].id || toks[i].n}"`);
    return fn;
  }
  const xyFn = src => { const f = compile(src, ["x", "y"]), e = {}; return (x, y) => { e.x = x; e.y = y; return f(e); }; };
  const num = v => typeof v === "number" ? v : compile(v, [])({});
  const strip = s => String(s).replace(/\(\s*[A-Za-z][A-Za-z ;]*\)\s*$/, "").trim();
  function ineq(s) {   // g >= 0 inside
    const m = strip(s).match(/^(.*?)(<=|>=|<|>)(.*)$/);
    if (!m) throw new Error(`not an inequality: ${s}`);
    const a = xyFn(m[1]), b = xyFn(m[3]);
    return m[2][0] === "<" ? (x, y) => b(x, y) - a(x, y) : (x, y) => a(x, y) - b(x, y);
  }
  function eqn(s) { const m = strip(s).match(/^([^<>=]*)=([^<>=]*)$/); if (!m) throw new Error(`not an equation: ${s}`); const a = xyFn(m[1]), b = xyFn(m[2]); return (x, y) => a(x, y) - b(x, y); }
  function splitTop(s) { const out = []; let d = 0, c = ""; for (const ch of String(s)) { if (ch === "(") d++; else if (ch === ")") d--; if (ch === "," && !d) { out.push(c); c = ""; } else c += ch; } out.push(c); return out.map(t => t.trim()).filter(Boolean); }

  /* ---------------- marching squares ---------------- */
  function grid(fn, box, n, m) {
    const V = new Float64Array((n + 1) * (m + 1)), hx = (box[1] - box[0]) / n, hy = (box[3] - box[2]) / m;
    for (let j = 0; j <= m; j++) for (let i = 0; i <= n; i++) V[j * (n + 1) + i] = fn(box[0] + hx * i, box[2] + hy * j);
    return { V, n, m, hx, hy, box, fn };
  }
  function march(G, level) {
    const { V, n, m, hx, hy, box, fn } = G, segs = [];
    for (let j = 0; j < m; j++) for (let i = 0; i < n; i++) {
      const a = V[j * (n + 1) + i] - level, b = V[j * (n + 1) + i + 1] - level, c = V[(j + 1) * (n + 1) + i + 1] - level, d = V[(j + 1) * (n + 1) + i] - level;
      if (!(isFinite(a) && isFinite(b) && isFinite(c) && isFinite(d))) continue;
      const X = box[0] + hx * i, Y = box[2] + hy * j, P = [];
      const cut = (p, q, x1, y1, x2, y2) => { if ((p > 0) !== (q > 0)) { const t = p / (p - q); P.push([x1 + t * (x2 - x1), y1 + t * (y2 - y1)]); } };
      cut(a, b, X, Y, X + hx, Y); cut(b, c, X + hx, Y, X + hx, Y + hy); cut(c, d, X + hx, Y + hy, X, Y + hy); cut(d, a, X, Y + hy, X, Y);
      if (P.length === 2) segs.push([P[0], P[1]]);
      else if (P.length === 4) {
        if ((fn(X + hx / 2, Y + hy / 2) - level > 0) === (a > 0)) segs.push([P[0], P[3]], [P[1], P[2]]);
        else segs.push([P[0], P[1]], [P[2], P[3]]);
      }
    }
    return segs;
  }

  /* ---------------- spec ---------------- */
  const KIND = k => String(k || "unconstrained").replace(/-/g, "_");
  function roleOf(role) {
    const s = String(role || "").toLowerCase();
    if (/saddle/.test(s)) return "saddle";
    if (/max/.test(s)) return /abs|global/.test(s) ? "absmax" : "max";
    if (/min/.test(s)) return /abs|global/.test(s) ? "absmin" : "min";
    return "other";
  }
  const ROLE_HE = { absmax: "מקסימום מוחלט", absmin: "מינימום מוחלט", max: "מקסימום מקומי", min: "מינימום מקומי", saddle: "נקודת אוכף" };
  function roleHe(role) {
    const c = roleOf(role), s = String(role || "").toLowerCase();
    if (ROLE_HE[c]) return ROLE_HE[c];
    if (/boundary|vertex|edge/.test(s)) return "נקודה על השפה";
    if (/interior/.test(s)) return "נקודה קריטית פנימית";
    return "נקודה קריטית";
  }
  function prepare(spec) {
    if (!spec || typeof spec !== "object") throw new Error("contour must be an object");
    const f = xyFn(spec.f), kind = KIND(spec.kind);
    if (!["unconstrained", "lagrange", "closed_region"].includes(kind)) throw new Error(`unknown kind ${spec.kind}`);
    if (!Array.isArray(spec.domain) || spec.domain.length !== 2) throw new Error("domain must be [[x0,x1],[y0,y1]]");
    let [[x0, x1], [y0, y1]] = spec.domain.map(d => d.map(num));
    const rx = x1 - x0, ry = y1 - y0, LIM = 1.25;   // equal scales: widen the short side
    if (ry / rx > LIM) { const w = ry / LIM, c = (x0 + x1) / 2; x0 = c - w / 2; x1 = c + w / 2; }
    else if (rx / ry > LIM) { const h = rx / LIM, c = (y0 + y1) / 2; y0 = c - h / 2; y1 = c + h / 2; }
    let g = null, gs = [];
    const cons = spec.constraint ? String(spec.constraint) : "";
    const isIneq = /[<>]/.test(cons);
    if (kind === "lagrange") { if (!cons || isIneq) throw new Error("lagrange needs an equality constraint"); g = eqn(cons); }
    if (kind === "closed_region") {
      const reg = spec.region != null ? spec.region : isIneq ? cons : null;
      if (reg == null) throw new Error("closed_region needs a region");
      gs = (Array.isArray(reg) ? reg : splitTop(reg)).map(ineq);
    }
    const pts = (spec.critical_points || []).map(p => ({ x: num(p.x), y: num(p.y), fv: num(p.f), role: p.role, src: p }));
    return { spec, f, kind, g, gs, pts, box: [x0, x1, y0, y1] };
  }
  const grad = (fn, x, y, h) => [(fn(x + h, y) - fn(x - h, y)) / (2 * h), (fn(x, y + h) - fn(x, y - h)) / (2 * h)];
  /* which constraint is active at a point: [fn] for a Lagrange / boundary point, [] inside, null = corner */
  function activeAt(C, p) {
    const sc = Math.max(C.box[1] - C.box[0], C.box[3] - C.box[2]), tol = 1e-7 * Math.max(1, sc * sc);
    if (C.kind === "lagrange") return Math.abs(C.g(p.x, p.y)) < tol ? [C.g] : [];
    if (C.kind === "closed_region") { const a = C.gs.filter(h => Math.abs(h(p.x, p.y)) < tol); return a.length > 1 ? null : a; }
    return [];
  }
  function levelsOf(C, G) {
    const vals = Array.from(G.V).filter(isFinite).sort((a, b) => a - b);
    if (!vals.length) throw new Error("f is not finite on the domain");
    const q = t => vals[Math.min(vals.length - 1, Math.floor(t * (vals.length - 1)))];
    const lo = q(0.01), hi = q(0.99);
    // levels evenly spaced in asinh((f - c)/s) around the critical values: an exponential f still gets curves
    // near its critical points (where |f| is small) and a few far out; the quantiles cover the bulk
    const cv = C.pts.map(p => p.fv).filter(isFinite), c = cv.length ? (Math.min(...cv) + Math.max(...cv)) / 2 : (lo + hi) / 2;
    const sc = cv.length ? (Math.max(...cv) - Math.min(...cv)) / 2 : 0, s = Math.max(sc > 0 ? sc : (q(0.75) - q(0.25)) / 6, 1e-9 * Math.max(1, Math.abs(hi - lo)));
    const T = v => Math.asinh((v - c) / s), Ti = t => c + s * Math.sinh(t);
    const L = [];
    for (let k = 1; k <= 11; k++) L.push(q(k / 12));
    const ta = T(lo), tb = T(hi);
    for (let k = 1; k <= 13; k++) L.push(Ti(ta + (tb - ta) * k / 14));
    for (const v of cv) if (v > vals[0] && v < vals[vals.length - 1]) L.push(v);
    L.sort((a, b) => a - b);
    const gap = (tb - ta) / 34, out = [];
    for (const v of L) {
      if (!out.length || T(v) - T(out[out.length - 1]) > gap) out.push(v);
      else if (cv.some(x => Math.abs(x - v) < 1e-12)) out[out.length - 1] = v;   // a critical level wins its slot
    }
    // a local max / min is a single point at its own level: two rings just inside it make the extremum visible
    for (const p of C.pts) { const r = roleOf(p.role); if (!isFinite(p.fv) || (r !== "max" && r !== "min")) continue;
      const sg = r === "max" ? -1 : 1, d = sc > 0 ? sc : s;
      for (const k of [0.1, 0.3]) out.push(p.fv + sg * k * d); }
    out.sort((a, b) => a - b);
    return { levels: out, lo, hi };
  }

  /* ---------------- formatting ---------------- */
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));
  const pretty = s => (root.Region && root.Region.pretty) ? root.Region.pretty(s) : String(s);
  function frac(v) { if (Math.abs(v - Math.round(v)) < 1e-9) return String(Math.round(v)); for (let d = 2; d <= 24; d++) { const n = Math.round(v * d); if (Math.abs(v - n / d) < 1e-9) return `${n}/${d}`; } return null; }
  const coord = (src, v) => typeof src === "string" ? pretty(src) : (frac(v) || String(Math.round(v * 1000) / 1000)).replace(/-/g, "−");
  const ltr = h => `<bdi dir="ltr" class="ct-math">${h}</bdi>`;
  function ticksFor(a, b) { const r = b - a, st = [0.1, 0.2, 0.25, 0.5, 1, 2, 2.5, 5, 10, 20].find(t => r / t <= 6) || r / 5, out = []; for (let v = Math.ceil(a / st - 1e-9) * st; v <= b + 1e-9; v += st) out.push(Math.round(v * 1e9) / 1e9); return out; }

  /* ---------------- SVG ---------------- */
  let UID = 0;
  function svgOf(C) {
    const id = "ct" + (++UID), [x0, x1, y0, y1] = C.box, rx = x1 - x0, ry = y1 - y0;
    const PW = ry > rx ? 280 * rx / ry : 280, PH = PW * ry / rx, ML = 34, MR = 14, MT = 14, MB = 28, W = ML + PW + MR, H = MT + PH + MB;
    const X = x => ML + (x - x0) / rx * PW, Y = y => MT + (y1 - y) / ry * PH, f1 = v => Math.round(v * 10) / 10;
    const path = segs => segs.map(s => `M${f1(X(s[0][0]))} ${f1(Y(s[0][1]))}L${f1(X(s[1][0]))} ${f1(Y(s[1][1]))}`).join("");
    let g = "";
    for (const v of ticksFor(x0, x1)) g += `<line class="ct-grid" x1="${f1(X(v))}" y1="${MT}" x2="${f1(X(v))}" y2="${f1(MT + PH)}"/><text class="ct-tl" x="${f1(X(v))}" y="${f1(MT + PH + 13)}" text-anchor="middle">${esc(String(v).replace("-", "−"))}</text>`;
    for (const v of ticksFor(y0, y1)) g += `<line class="ct-grid" x1="${ML}" y1="${f1(Y(v))}" x2="${f1(ML + PW)}" y2="${f1(Y(v))}"/><text class="ct-tl" x="${ML - 5}" y="${f1(Y(v) + 3.5)}" text-anchor="end">${esc(String(v).replace("-", "−"))}</text>`;
    if (x0 < 0 && x1 > 0) g += `<line class="ct-axis" x1="${f1(X(0))}" y1="${MT}" x2="${f1(X(0))}" y2="${f1(MT + PH)}"/>`;
    if (y0 < 0 && y1 > 0) g += `<line class="ct-axis" x1="${ML}" y1="${f1(Y(0))}" x2="${f1(ML + PW)}" y2="${f1(Y(0))}"/>`;
    // level curves, coloured low -> high
    const G = grid(C.f, C.box, 110, Math.max(30, Math.round(110 * ry / rx)));
    const { levels } = levelsOf(C, G);
    let lv = "";
    levels.forEach((L, k) => {
      const t = levels.length > 1 ? Math.round(100 * k / (levels.length - 1)) : 50;
      const crit = C.pts.some(p => Math.abs(p.fv - L) < 1e-9);
      lv += `<path class="ct-level${crit ? " ct-crit" : ""}" style="stroke:color-mix(in srgb,var(--ct-hi) ${t}%,var(--ct-lo))" d="${path(march(G, L))}"/>`;
    });
    // constraint / region
    let cons = "";
    if (C.kind === "lagrange") cons = `<path class="ct-cons" d="${path(march(grid(C.g, C.box, 160, 160), 0))}"/>`;
    if (C.kind === "closed_region") {
      const inside = (x, y) => C.gs.every(h => h(x, y) >= 0);
      const NX = 140, cw = rx / NX, ch = ry / 160;
      let sh = "";
      for (let i = 0; i < NX; i++) {
        const xc = x0 + cw * (i + 0.5); let start = null;
        for (let j = 0; j <= 160; j++) {
          const yy = y0 + ch * (j + 0.5), on = j < 160 && inside(xc, yy);
          if (on && start == null) start = yy - ch / 2;
          if (!on && start != null) { sh += `M${f1(X(xc - cw / 2))} ${f1(Y(yy - ch / 2))}H${f1(X(xc + cw / 2) + 0.6)}V${f1(Y(start))}H${f1(X(xc - cw / 2))}Z`; start = null; }
        }
      }
      const sc = C.gs.map(h => { let m = 1e-12; for (let i = 0; i <= 8; i++) for (let j = 0; j <= 8; j++) m = Math.max(m, Math.abs(h(x0 + rx * i / 8, y0 + ry * j / 8)) || 0); return m; });
      let ol = "";
      C.gs.forEach((h, k) => {
        ol += path(march(grid(h, C.box, 160, 160), 0).filter(s => { const mx = (s[0][0] + s[1][0]) / 2, my = (s[0][1] + s[1][1]) / 2; return C.gs.every((o, j) => j === k || o(mx, my) >= -2e-3 * sc[j]); }));
      });
      cons = `<path class="ct-region" d="${sh}"/><path class="ct-cons" d="${ol}"/>`;
    }
    // gradient arrows at the constraint points; markers
    const arrow = (px, py, vx, vy, cls, AL) => {
      const n = Math.hypot(vx, -vy); if (!(n > 1e-9)) return "";
      const ux = vx / n, uy = -vy / n, ex = px + ux * AL, ey = py + uy * AL;   // screen y grows downward
      const hx = ex - ux * 7, hy = ey - uy * 7;
      return `<line class="${cls}" x1="${f1(px)}" y1="${f1(py)}" x2="${f1(hx)}" y2="${f1(hy)}"/><path class="${cls}-head" d="M${f1(ex)} ${f1(ey)}L${f1(hx - uy * 3.6)} ${f1(hy + ux * 3.6)}L${f1(hx + uy * 3.6)} ${f1(hy - ux * 3.6)}Z"/>`;
    };
    let arrows = "", marks = "";
    const hstep = 1e-5 * Math.max(rx, ry);
    C.pts.forEach((p, k) => {
      const px = X(p.x), py = Y(p.y), act = activeAt(C, p);
      if (act && act.length === 1) {
        const [fx, fy] = grad(C.f, p.x, p.y, hstep), [gx, gy] = grad(act[0], p.x, p.y, hstep);
        arrows += arrow(px, py, gx, gy, "ct-gg", 36) + arrow(px, py, fx, fy, "ct-gf", 22);   // grad g longer: parallel arrows both show
      }
      const r = roleOf(p.role), s = 5.2;
      const shape = r === "absmax" || r === "max" ? `<path class="ct-pt ct-${r}" d="M${f1(px)} ${f1(py - s)}L${f1(px + s)} ${f1(py + s * 0.8)}L${f1(px - s)} ${f1(py + s * 0.8)}Z"/>`
        : r === "absmin" || r === "min" ? `<path class="ct-pt ct-${r}" d="M${f1(px)} ${f1(py + s)}L${f1(px + s)} ${f1(py - s * 0.8)}L${f1(px - s)} ${f1(py - s * 0.8)}Z"/>`
        : r === "saddle" ? `<path class="ct-pt ct-saddle" d="M${f1(px - s)} ${f1(py)}L${f1(px)} ${f1(py - s)}L${f1(px + s)} ${f1(py)}L${f1(px)} ${f1(py + s)}Z"/>`
        : `<circle class="ct-pt ct-other" cx="${f1(px)}" cy="${f1(py)}" r="${s - 1}"/>`;
      const lx = px + 7 > ML + PW - 8 ? px - 8 : px + 7, anchor = px + 7 > ML + PW - 8 ? "end" : "start";
      marks += shape + `<text class="ct-num" x="${f1(lx)}" y="${f1(py - 6 < MT + 8 ? py + 13 : py - 6)}" text-anchor="${anchor}">${k + 1}</text>`;
    });
    return `<svg class="ct-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${f1(W)} ${f1(H)}" width="${f1(W)}" height="${f1(H)}" direction="ltr" role="img" aria-label="contour plot">` +
      `<defs><clipPath id="${id}c"><rect x="${ML}" y="${MT}" width="${f1(PW)}" height="${f1(PH)}"/></clipPath></defs>` +
      `<rect class="ct-space" x="${ML}" y="${MT}" width="${f1(PW)}" height="${f1(PH)}"/>` + g +
      `<g clip-path="url(#${id}c)">${cons.replace(/<path class="ct-cons"[^>]*\/>/, "")}${lv}${(cons.match(/<path class="ct-cons"[^>]*\/>/) || [""])[0]}${arrows}</g>${marks}` +
      `<rect class="ct-frame" x="${ML}" y="${MT}" width="${f1(PW)}" height="${f1(PH)}"/>` +
      `<text class="ct-ax" x="${f1(ML + PW)}" y="${f1(MT + PH + 25)}" text-anchor="end">x</text><text class="ct-ax" x="${ML - 22}" y="${MT + 4}" text-anchor="middle">y</text></svg>`;
  }

  function figureOne(spec) {
    try {
      const C = prepare(spec);
      const svg = svgOf(C);
      const hasArrows = C.pts.some(p => { const a = activeAt(C, p); return a && a.length === 1; });
      const consTxt = C.kind === "lagrange" ? `האילוץ ${ltr(esc(pretty(spec.constraint)))}`
        : C.kind === "closed_region" ? `התחום ${ltr(esc((Array.isArray(spec.region) ? spec.region : splitTop(spec.region != null ? spec.region : strip(spec.constraint))).map(pretty).join(",  ")))}` : "";
      const legend = `<div class="ct-legend">` +
        `<span class="ct-key"><i class="ct-sw ct-sw-lv"></i>קווי גובה של ${ltr("f")} (כחול: נמוך, צהוב: גבוה)</span>` +
        (consTxt ? `<span class="ct-key"><i class="ct-sw ct-sw-cons"></i>${consTxt}</span>` : "") +
        (hasArrows ? `<span class="ct-key"><i class="ct-sw ct-sw-gf"></i>${ltr("∇f")}</span><span class="ct-key"><i class="ct-sw ct-sw-gg"></i>${ltr("∇g")} (בנקודת לגראנז' החצים מקבילים)</span>` : "") + `</div>`;
      const list = `<ol class="ct-pts">` + C.pts.map(p => {
        const r = roleOf(p.role);
        return `<li><span class="ct-li-role ct-r-${r}">${roleHe(p.role)}</span> ${ltr(esc(`(${coord(p.src.x, p.x)}, ${coord(p.src.y, p.y)})`))}` +
          `<span class="ct-li-f">${ltr(esc(`f = ${typeof p.src.f === "string" ? pretty(p.src.f) : (frac(p.fv) || String(Math.round(p.fv * 1000) / 1000)).replace(/-/g, "−")}`))}</span></li>`;
      }).join("") + `</ol>`;
      return `<div class="contour-fig" data-ct="1"><div class="ct-title">קווי גובה ${ltr(esc(`f(x,y) = ${pretty(spec.f)}`))}</div>` +
        `<div class="ct-plot" dir="ltr">${svg}</div>${legend}${list}</div>`;
    } catch (e) {
      return `<div class="contour-fig" data-ct="1"><div class="ct-error">לא ניתן לצייר את קווי הגובה (${esc(e.message)})</div></div>`;
    }
  }
  function figure(spec) { return (Array.isArray(spec) ? spec : [spec]).map(figureOne).join(""); }
  function lookup(val) {
    const v = String(val || "").trim();
    if (v[0] === "{" || v[0] === "[") return JSON.parse(v);
    for (const q of ((root.OPEN_BANK && root.OPEN_BANK.questions) || [])) for (const s of [].concat(q.contour || [])) if (s && s.id === v) return s;
    throw new Error(`unknown id ${v}`);
  }
  function hydrate(el) {
    if (!el || !el.querySelectorAll) return 0;
    const hosts = [...el.querySelectorAll(".contour-fig[data-contour]:not([data-ct])")];
    if (el.matches && el.matches(".contour-fig[data-contour]:not([data-ct])")) hosts.unshift(el);
    for (const h of hosts) {
      let html;
      try { html = figure(lookup(h.getAttribute("data-contour"))); }
      catch (e) { html = `<div class="contour-fig" data-ct="1"><div class="ct-error">לא ניתן לצייר את קווי הגובה (${esc(e.message)})</div></div>`; }
      const tmp = h.ownerDocument.createElement("div"); tmp.innerHTML = html;
      h.replaceWith(...tmp.childNodes);
    }
    return hosts.length;
  }
  if (typeof document !== "undefined" && typeof MutationObserver !== "undefined") {
    const start = () => {
      hydrate(document.body);
      new MutationObserver(ms => { for (const m of ms) for (const n of m.addedNodes) if (n.nodeType === 1) hydrate(n); }).observe(document.body, { childList: true, subtree: true });
    };
    if (document.body) start(); else document.addEventListener("DOMContentLoaded", start);
  }
  const Contour = { figure, hydrate, compile, roleOf, _: { prepare, activeAt, levelsOf, grid, march } };
  root.Contour = Contour;
  if (typeof module !== "undefined" && module.exports) module.exports = Contour;
})(typeof window !== "undefined" ? window : globalThis);
