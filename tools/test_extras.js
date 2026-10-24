// Headless render test for the calculus-2 diagrams (region.js / contour.js):  node tools/test_extras.js
// Renders EVERY spec: the verify data as the build attaches it (py tools/extras.py --dump), every item's
// region/contour in questions.json, and every data-region / data-contour hook in questions.json, learn.js and
// courses.js. Each figure must render without an error box, parse as SVG (jsdom), shade/outline its region,
// draw level curves, one marker per critical point and gradient arrows at the Lagrange points. Region areas from
// every description (orders, polar, polygon-derived bounds) must match the area of the inequalities. Also:
// hydrate() + the view toggle in a DOM, and the expression parsers refuse anything but arithmetic.
const assert = require("assert"), fs = require("fs"), path = require("path"), cp = require("child_process");
const { JSDOM } = require("jsdom");
const APP = path.join(__dirname, "..");
global.window = globalThis;
const Region = require(path.join(APP, "region.js")), Contour = require(path.join(APP, "contour.js"));

let fails = 0, nR = 0, nC = 0;
const bad = (w, m) => { fails++; console.log(`FAIL ${w}: ${m}`); };

function dump() {
  for (const exe of ["py", "python", "python3"]) {
    const r = cp.spawnSync(exe, [path.join(__dirname, "extras.py"), "--dump"], { encoding: "utf8", env: { ...process.env, PYTHONUTF8: "1" } });
    if (r.status === 0 && r.stdout) return JSON.parse(r.stdout);
  }
  throw new Error("could not run tools/extras.py --dump");
}
const dom = new JSDOM("<!doctype html><body></body>");
function parseSvg(w, html) {
  const d = dom.window.document.createElement("div");
  d.innerHTML = html;
  const svg = d.querySelector("svg");
  if (!svg) { bad(w, "no <svg>"); return null; }
  const x = new dom.window.DOMParser().parseFromString(svg.outerHTML, "image/svg+xml");
  if (x.querySelector("parsererror")) bad(w, "SVG is not well-formed");
  return d;
}
function checkRegion(w, spec) {
  nR++;
  const html = Region.figure(spec);
  if (/rg-error/.test(html)) return bad(w, "error box: " + (html.match(/\(([^<]*)\)<\/div>/) || [])[1]);
  const d = parseSvg(w, html); if (!d) return;
  const region = d.querySelector(".rg-region"), outline = d.querySelector(".rg-outline");
  if (!region || (region.getAttribute("d") || "").length < 20) bad(w, "region not shaded");
  if (!outline || (outline.getAttribute("d") || "").length < 20) bad(w, "region not outlined");
  const views = [...d.querySelectorAll("[data-rg-view]")].map(b => b.getAttribute("data-rg-view"));
  for (const v of views) {
    const layer = d.querySelector(`.rg-l-${v}`);
    if (!layer || !layer.innerHTML.length) bad(w, `view ${v} has an empty layer`);
    if (!d.querySelector(`.rg-row[data-view="${v}"]`)) bad(w, `view ${v} has no bounds row`);
  }
  if (!views.includes("v") || !views.includes("h")) bad(w, "both strip views must be offered");
  if (spec.polar && !views.includes("p")) bad(w, "polar data but no polar view");
  if (spec.substitution && !views.includes("uv")) bad(w, "substitution data but no u,v view");
  if (/NaN|undefined|Infinity/.test(d.querySelector("svg").outerHTML)) bad(w, "NaN/undefined/Infinity in the SVG");
  const a = Region.analyze(spec), tol = 0.015 * a.area;
  for (const [v, o] of Object.entries(a.orders)) if (Math.abs(o.area - a.area) > tol) bad(w, `${o.derived ? "derived " : ""}${v} bounds give area ${o.area.toFixed(4)}, inequalities ${a.area.toFixed(4)}`);
  if (a.polar != null && Math.abs(a.polar - a.area) > tol) bad(w, `polar bounds give area ${a.polar.toFixed(4)}, inequalities ${a.area.toFixed(4)}`);
}
function checkContour(w, spec) {
  nC++;
  const html = Contour.figure(spec);
  if (/ct-error/.test(html)) return bad(w, "error box: " + (html.match(/\(([^<]*)\)<\/div>/) || [])[1]);
  const d = parseSvg(w, html); if (!d) return;
  const lv = [...d.querySelectorAll(".ct-level")].filter(p => (p.getAttribute("d") || "").length > 10);
  if (lv.length < 4) bad(w, `only ${lv.length} level curves drawn`);
  const C = Contour._.prepare(spec);
  if (d.querySelectorAll(".ct-pt").length !== C.pts.length) bad(w, "one marker per critical point expected");
  if (d.querySelectorAll(".ct-pts li").length !== C.pts.length) bad(w, "one list row per critical point expected");
  const [x0, x1, y0, y1] = C.box;
  for (const p of C.pts) if (!(p.x >= x0 && p.x <= x1 && p.y >= y0 && p.y <= y1)) bad(w, `point (${p.x}, ${p.y}) is outside the plot`);
  if (C.kind !== "unconstrained" && (d.querySelector(".ct-cons").getAttribute("d") || "").length < 20) bad(w, "constraint / boundary not drawn");
  const lag = C.pts.filter(p => { const a = Contour._.activeAt(C, p); return a && a.length === 1; }).length;
  if (C.kind === "lagrange" && !lag) bad(w, "no point lies on the constraint");
  if (lag && d.querySelectorAll(".ct-gf").length < 1) bad(w, "no gradient arrows at the Lagrange points");
  if (/NaN|undefined|Infinity/.test(d.querySelector("svg").outerHTML)) bad(w, "NaN/undefined/Infinity in the SVG");
}

// 1. the verify data, as the build attaches it
const D = dump();
for (const [id, specs] of Object.entries(D.regions)) specs.forEach((s, i) => checkRegion(`${id} region${specs.length > 1 ? "[" + i + "]" : ""}`, s));
for (const [id, specs] of Object.entries(D.contours)) specs.forEach((s, i) => checkContour(`${id} contour${specs.length > 1 ? "[" + i + "]" : ""}`, s));
// 2. what ships: bank items and hooks in every built file
const bankFile = path.join(APP, "questions.json");
const bank = fs.existsSync(bankFile) ? JSON.parse(fs.readFileSync(bankFile, "utf8")) : { questions: [] };
global.OPEN_BANK = bank;
let shipped = 0;
for (const q of bank.questions) {
  for (const s of [].concat(q.region || [])) { checkRegion(`${q.id} (bank) region`, s); shipped++; }
  for (const s of [].concat(q.contour || [])) { checkContour(`${q.id} (bank) contour`, s); shipped++; }
}
const he = s => s.replace(/&quot;/g, '"').replace(/&#x27;|&#39;/g, "'").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&");
let hooks = 0;
for (const f of ["questions.json", "learn.js", "courses.js"]) {
  const fp = path.join(APP, f);
  if (!fs.existsSync(fp)) continue;
  let t = fs.readFileSync(fp, "utf8");
  if (f.endsWith(".json") || f.endsWith(".js")) t = t.replace(/\\"/g, '"');
  for (const m of t.matchAll(/data-(region|contour)="([^"]*)"/g)) {
    hooks++;
    let spec;
    try { spec = (m[1] === "region" ? Region : Region)._.lookup(he(m[2]), m[1]); } catch (e) { bad(`${f} hook`, e.message); continue; }
    for (const s of [].concat(spec)) (m[1] === "region" ? checkRegion : checkContour)(`${f} data-${m[1]} ${s.id || ""}`, s);
  }
}

// 3. hydrate + toggle in a DOM
{
  const w = new JSDOM(`<!doctype html><body><div id="m"></div></body>`, { runScripts: "outside-only" }).window;
  w.OPEN_BANK = bank;
  for (const f of ["region.js", "contour.js"]) w.eval(fs.readFileSync(path.join(APP, f), "utf8"));
  const anyR = Object.values(D.regions).flat().find(s => s.polar) || Object.values(D.regions).flat()[0];
  const anyC = Object.values(D.contours).flat()[0];
  const m = w.document.getElementById("m");
  m.innerHTML = `<div class="region-fig" data-region='${JSON.stringify(anyR).replace(/'/g, "&#39;")}'></div><div class="contour-fig" data-contour='${JSON.stringify(anyC).replace(/'/g, "&#39;")}'></div>`;
  w.Region.hydrate(m); w.Contour.hydrate(m);
  assert.ok(m.querySelector(".region-fig[data-rg] svg"), "region hook hydrated");
  assert.ok(m.querySelector(".contour-fig[data-ct] svg"), "contour hook hydrated");
  const fig = m.querySelector(".region-fig[data-rg]"), btns = [...fig.querySelectorAll("[data-rg-view]")];
  const other = btns.find(b => b.getAttribute("aria-pressed") !== "true");
  other.dispatchEvent(new w.MouseEvent("click", { bubbles: true }));
  assert.strictEqual(fig.dataset.view, other.dataset.rgView, "toggle switches the view");
  assert.strictEqual(btns.filter(b => b.getAttribute("aria-pressed") === "true").length, 1, "one view pressed");
  // a hook by id resolves through the bank
  const withR = bank.questions.find(q => q.region);
  if (withR) {
    m.innerHTML = `<div class="region-fig" data-region="${withR.region[0].id}"></div>`;
    w.Region.hydrate(m);
    assert.ok(m.querySelector(".region-fig svg"), "id hook resolves through OPEN_BANK");
  }
}

// 3b. the build path: a ```region / ```contour fence (by id and inline JSON) in rich text -> a hook that hydrates
{
  const rid = Object.keys(D.regions)[0], cid = Object.keys(D.contours)[0];
  const src = "a\n```region\n" + rid + "\n```\nb\n```contour\n" + JSON.stringify(D.contours[cid][0]) + "\n```\n```region\nNO-SUCH-ID\n```";
  const py = `import sys, json; sys.path.insert(0, ${JSON.stringify(__dirname)}); import richtext as rt\n` +
    `errs = []; h = rt.rich_html(json.loads(sys.stdin.read()), rt.MathBank(), "T", errs)\nprint(json.dumps({"h": h, "errs": [e[2] for e in errs]}))`;
  let out = null;
  for (const exe of ["py", "python", "python3"]) {
    const r = cp.spawnSync(exe, ["-c", py], { input: JSON.stringify(src), encoding: "utf8", env: { ...process.env, PYTHONUTF8: "1" } });
    if (r.status === 0 && r.stdout) { out = JSON.parse(r.stdout); break; }
  }
  assert.ok(out, "richtext fence check ran");
  assert.strictEqual(out.errs.length, 1, "an unknown id fails the build: " + out.errs.join("; "));
  assert.ok(/unknown region id/.test(out.errs[0]), "unknown id message");
  const w = new JSDOM(`<!doctype html><body><div id="m"></div></body>`, { runScripts: "outside-only" }).window;
  for (const f of ["region.js", "contour.js"]) w.eval(fs.readFileSync(path.join(APP, f), "utf8"));
  const m = w.document.getElementById("m");
  m.innerHTML = out.h;
  w.Region.hydrate(m); w.Contour.hydrate(m);
  assert.ok(m.querySelector(".region-fig[data-rg] .rg-svg"), "fence by id renders a region");
  assert.ok(m.querySelector(".contour-fig[data-ct] .ct-svg"), "inline JSON fence renders a contour");
  assert.ok(!m.querySelector(".rg-error,.ct-error"), "fence figures render without errors");
}

// 4. the parsers evaluate arithmetic only
for (const evil of ["constructor", "x.constructor", "this", "Function('return 1')()", "alert(1)", "x;1", "[1]", "process", "x=1", "`1`"]) {
  assert.throws(() => Contour.compile(evil, ["x", "y"]), `contour parser accepted ${evil}`);
  assert.throws(() => Region.Expr.compile(evil, new Set(["x", "y"])), `region parser accepted ${evil}`);
}
assert.strictEqual(Contour.compile("x^2+2*y-sqrt(4)", ["x", "y"])({ x: 3, y: 1 }), 9);
assert.ok(Math.abs(Contour.compile("(x^2-2*y^2)*exp(x-y)", ["x", "y"])({ x: -4, y: -2 }) - 1.0826822658929016) < 1e-12);
assert.strictEqual(Region.Expr.compile("y*x^2>=1", new Set(["x", "y"]))({ x: 1, y: 2 }), 1);

console.log(`test_extras: ${nR} region figure(s), ${nC} contour figure(s) (${shipped} from the bank, ${hooks} hook(s)); ${fails} failure(s)`);
process.exit(fails ? 1 : 0);
