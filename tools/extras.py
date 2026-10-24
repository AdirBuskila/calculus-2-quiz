# -*- coding: utf-8 -*-
"""calculus-2 extra: the region / contour diagram data, attached to the bank at build time.

Source of truth: tools/verify/<CODE>/regions.json and contours.json (each sitting's check.py writes them;
tools/verify/extras_check.py checks every bound and critical point with sympy). Contract: RAW_SCHEMA.md,
"Region and contour diagrams".

  load()                      -> (regions_by_id, contours_by_id), each {id: [spec, ...]} (renderer keys only)
  attach(q, extras)           -> sets q["region"] / q["contour"] (a list) when the verify data has the question id
  fence_html(kind, body, ...) -> a ```region / ```contour fence body (JSON spec, or an id) as the hook
                                 <div class="region-fig" data-region="{json}"></div> (region.js / contour.js draw it)
  resolve_hooks(h, ...)       -> data-region / data-contour attributes in author HTML: an id is replaced by its JSON
A contour of kind closed_region with no `region` (and no inequality constraint) takes the inequalities of the
regions.json entry with the same id. Problems are appended to `errs` as (where, text, message), like math errors.
"""
import html, json, pathlib, re

TOOLS = pathlib.Path(__file__).resolve().parent
VERIFY = TOOLS / "verify"
REGION_KEYS = ("id", "inequalities", "boundary_curves", "orderXY", "orderYX", "polar", "substitution",
               "vertices", "integrand", "value", "area", "view")
CONTOUR_KEYS = ("id", "f", "kind", "constraint", "region", "domain", "critical_points")
_CACHE = {}


def _pick(spec, keys):
    return {k: spec[k] for k in spec if k in keys}


def load():
    if "data" in _CACHE:
        return _CACHE["data"]
    regions, contours = {}, {}
    for d in sorted(p for p in VERIFY.iterdir() if p.is_dir()):
        for name, bucket, keys in (("regions.json", regions, REGION_KEYS), ("contours.json", contours, CONTOUR_KEYS)):
            fp = d / name
            if not fp.exists():
                continue
            for s in json.loads(fp.read_text(encoding="utf-8")):
                if isinstance(s, dict) and s.get("id"):
                    bucket.setdefault(s["id"], []).append(_pick(s, keys))
    for cid, specs in contours.items():
        for s in specs:
            s["kind"] = str(s.get("kind") or "unconstrained").replace("-", "_")
            cons = str(s.get("constraint") or "")
            if s["kind"] == "closed_region" and s.get("region") is None and not re.search(r"[<>]", cons) and cid in regions:
                s["region"] = list(regions[cid][0]["inequalities"])
    _CACHE["data"] = (regions, contours)
    return _CACHE["data"]


def attach(q, extras):
    regions, contours = extras
    if q["id"] in regions:
        q["region"] = regions[q["id"]]
    if q["id"] in contours:
        q["contour"] = contours[q["id"]]


def _spec(kind, body, where, errs):
    body = body.strip()
    if body[:1] in ("{", "["):
        try:
            obj = json.loads(body)
        except ValueError as e:
            errs.append((where, body[:40], f"{kind} fence/hook is not valid JSON ({e})"))
            return None
        need = "inequalities" if kind == "region" else "f"
        for s in (obj if isinstance(obj, list) else [obj]):
            if not isinstance(s, dict) or need not in s:
                errs.append((where, body[:40], f"a {kind} spec needs `{need}`"))
                return None
        return obj
    regions, contours = load()
    table = regions if kind == "region" else contours
    if body not in table:
        errs.append((where, body, f"unknown {kind} id (not in tools/verify/*/{kind}s.json)"))
        return None
    got = table[body]
    return got[0] if len(got) == 1 else got


def hook(kind, spec):
    attr = html.escape(json.dumps(spec, ensure_ascii=False, separators=(",", ":")), quote=True)
    return f'<div class="{kind}-fig" data-{kind}="{attr}"></div>'


def fence_html(kind, body, where, errs):
    spec = _spec(kind, body, where, errs)
    return hook(kind, spec) if spec is not None else ""


HOOK_RE = re.compile(r"""data-(region|contour)=(['"])(.*?)\2""", re.S)


def resolve_hooks(h, where, errs):
    def sub(m):
        kind = m.group(1)
        spec = _spec(kind, html.unescape(m.group(3)), where, errs)
        if spec is None:
            return m.group(0)
        return f'data-{kind}="' + html.escape(json.dumps(spec, ensure_ascii=False, separators=(",", ":")), quote=True) + '"'
    return HOOK_RE.sub(sub, h)


PRE_RE = re.compile(r'<pre class="code-block" dir="ltr" data-lang="(region|contour)"><code>(.*?)</code></pre>', re.S)


def fences_in_html(h, where, errs):
    """build_learn: markdown already turned a ```region fence into <pre data-lang="region"> -> the hook."""
    return PRE_RE.sub(lambda m: fence_html(m.group(1), html.unescape(m.group(2)), where, errs), h)


if __name__ == "__main__":   # `py tools/extras.py --dump`: the specs as the build attaches them (tools/test_extras.js)
    import sys
    if "--dump" in sys.argv:
        r, c = load()
        sys.stdout.write(json.dumps({"regions": r, "contours": c}, ensure_ascii=True))
