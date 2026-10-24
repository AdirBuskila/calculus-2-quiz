# Refuter: writes tools/raw/_verify_<CODE>.json for 22A-A, 23A-A, 24A-A (verdicts from refute_*.py runs + page review).
import json, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
TOOLS = HERE.parent
sys.path.insert(0, str(TOOLS))
from richtext import part_suffix  # noqa: E402

RAW = TOOLS / "raw"
STEPS = "agree (every numeric answer/tol, choice correctId and unique-correct option, order sequence, findbug index re-derived)"


def build(code, my, extra):
    src = json.load(open(RAW / f"{code}.json", encoding="utf8"))
    items, answers = [], {}
    for q in src["questions"]:
        k = f"{q['num']}{part_suffix(q.get('part')) or ''}"
        label = f"{q['num']}{q['part']}"
        m = my[label]
        it = {"item": label, "verdict": "agree", "myAnswer": m["ans"], "steps": m.get("steps", STEPS), "firstDivergence": None}
        if m.get("note"):
            it["note"] = m["note"]
        items.append(it)
        answers[k] = {"answer": None, "agrees": True, "confident": True, "transcriptionIssues": ""}
    out = {
        "examCode": code,
        "refuter": f"calculus-2 {code}",
        "summary": {"agree": len(items), "disagree": 0, "unclear": 0},
        "transcription": f"matches page renders for all items (tools/raw/{code}-SRC)",
        "optionText": "no positional option citations; no 'הפתרון הרשמי' in any item (all non-official); every choice has exactly one correct option and a valid correctId; rubric sums = 12/13 per part",
        **extra,
        "items": items,
        "answers": answers,
    }
    json.dump(out, open(RAW / f"_verify_{code}.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)


my22 = {
    "1א": {"ans": "direction (1,1)/sqrt2, max D_u = 4*sqrt2 = sqrt32 ~5.657"},
    "1ב": {"ans": "identity holds (z_x=-y/(3x^2)+y g', z_y=1/(3x)+x g'; sum = -2y/3 + 2y/3 = 0; sympy simplify = 0)",
           "note": "silent fix confirmed: key's '+y^2' should be '+2y/3'; raw has +2y/3, correct"},
    "2א": {"ans": "series 1 absolutely convergent (integral test, 1/ln2); series 2 absolutely convergent (sum = 1/2)",
           "note": "key only says 'converges' for series 2 (true: it is absolutely convergent); not wrong"},
    "2ב": {"ans": "continuous; fx=fy=0; differentiable (f/r = r sin(1/r) -> 0)",
           "note": "silent fix confirmed: division by h present in raw"},
    "3א": {"ans": "R=1; x+1=1 diverges (~pi/sqrt n); x+1=-1 converges (Leibniz, decreasing from n=4); domain -2<=x<0",
           "note": "silent fix confirmed: a_3=0.971 < a_4=1.000, so decreasing starts at n=4 (n=2 in the key file is wrong; page 4 of the key shows 'from n=2'); numeric partial sums checked"},
    "3ב": {"ans": "F_z=2!=0 at (1,1,0), z_x=0, z_y=-5/2; tangent plane 5y+2z=5"},
    "4א": {"ans": "9e(e-1)=42.037 for the y>=0 piece; the y<=-4.83 piece gives -9e(e-1); whole D (both pieces) = 0",
           "steps": STEPS + "; step answers all refer to the y>=0 piece",
           "note": "VALUE AGREES BUT THE STATEMENT IS AMBIGUOUS: see flags.Q4a_ambiguity. A visible 'הערה:' is required."},
    "4ב": {"ans": "abs max 6 at (+-sqrt2,0); abs min -9/8 at (+-1/2,+-1)",
           "note": "corrected values confirmed (sympy; boundary in t=y^2 is 3t^2-9t+6, max 6 at t=0, min -3/4; interior values 0,-1,-1/8,-9/8; dense grid max 5.9958, min -1.125). Prefix 'תיקון לפתרון שבקובץ' is correct (official:false, no 'הפתרון הרשמי')."},
    "5א": {"ans": "-(1/3) sum (1 + (-1)^n/2^(n+1)) x^n, |x|<1 (coefficients checked to n=7)"},
    "5ב": {"ans": "(-2,0) local max f=5; (1,+-sqrt3) saddles f=1/2"},
}
flags22 = {
    "Q4a_ambiguity": {
        "finding": "Read literally, y-x=1, y=x+2, y^2=-4x, y^2=-4x+9 bound TWO pieces: y>=0.83 (the key's piece, integral +9e(e-1)=42.037) and y in [-6.58,-4.83] (there 2y+4<0, signed integral -9e(e-1)). Nothing in the statement picks one. The key's hand note (circled) says 'y>=0 in D', and the app solution carries it only as the parenthetical '(ב-D מתקיים y≥0.)', an unmarked assumption.",
        "needsVisibleNote": True,
        "noteText": "הערה: ארבעת העקומים חוסמים שני תחומים נפרדים, אחד עם y ≥ 0 ואחד עם y < −4.8 בקירוב. כמו בפתרון המקורי, מחשבים כאן את התחום העליון (y ≥ 0). באינטגרל על התחום התחתון מתקבל −9e(e−1).",
        "placement": "visible in Q4a (question or head of the solution); regions.json description already says 'the part with y>=0', keep the diagram and value consistent with the note",
    },
    "rubric_points": "22A-A prints '25 נק'' per question and no per-part split. 12/13 (a/b) is reasonable and matches the 12/13 printed in 23A-A, but it is an estimate (rubricSource ai-draft) and must not be shown as the exam's own split. Every rubric sums to 12 or 13 as claimed.",
    "contours_json": "All f values and Hessian classes are correct. INCOMPLETE: 22A-A-Q4b omits interior critical points (+-1/2,0) f=-1/8 (saddle) and (0,+-1) f=-1 (saddle) and the boundary local min -3/4 at (+-1/sqrt2,+-sqrt(3/2)); nothing wrong, but 'every critical point' is not literally true.",
    "regions_json": "22A-A-Q4a: inequalities, substitution and value correct for the y>=0 piece (grid 42.025 vs 42.037). Should mention the second piece like the app note.",
    "docs_stale": "docs/ASK_ADIR.md (22A-A Q4b entry) says the prefix is 'הפתרון הרשמי עם תיקון' while the raw correctly uses 'תיקון לפתרון שבקובץ' (GATE1 ruling, QA 4b). The doc text is stale. Item solutionSource is 'solved' (not 'student-solution'), acceptable because the shown solution is the corrected one.",
}
build("22A-A", my22, {"flags": flags22})

my23 = {
    "1א": {"ans": "7*pi^2/192 ~0.35983 (polar r in [1,2], theta in [pi/4,pi/3]; grid 0.3600)"},
    "1ב": {"ans": "direction (1,2,1)/sqrt6 (grad = (1/3,2/3,1/3))"},
    "2א": {"ans": "series 1 conditionally convergent; series 2 absolutely convergent"},
    "2ב": {"ans": "continuous; fx=fy=0; differentiable"},
    "3א": {"ans": "R=sqrt5/3; both endpoints converge (terms 1/(2n+1)^2); domain [-sqrt5/3, sqrt5/3]"},
    "3ב": {"ans": "identity holds (sympy simplify of x^2 g_x + y^2 g_y + (x+y)/z g_z = 0)",
           "note": "silent fix confirmed against key page 7: key writes df/dt where df/du belongs; raw has f_u, correct (the cancellation needs f_u)"},
    "4א": {"ans": "6 (u=x^2 y in [1,4], v=y-x in [-1,1], |d(u,v)/d(x,y)|=x(x+2y)=integrand; numeric 5.996)"},
    "4ב": {"ans": "abs max 2*sqrt2-2 at (1-1/sqrt2,1-1/sqrt2); abs min -2-2*sqrt2 at (1+1/sqrt2,1+1/sqrt2); (0,0) is outside the disc"},
    "5א": {"ans": "single critical point (6,-6), D=-16, saddle",
           "note": "silent fix confirmed against key page 11: key writes (6,-6) then (-6,6); raw uses (6,-6) throughout (second derivatives are constants, classification unaffected)"},
    "5ב": {"ans": "(1/5) sum(-1/2^(n+1) - (-1)^n/3^(n+1)) x^n, |x|<2; f^(10)(0)=-6271825/17496 ~ -358.47 (sympy 10th derivative agrees)",
           "note": "silent fix confirmed: domain |x|<2 not stated in the key; added in raw, correct (nearest pole x=2)"},
}
flags23 = {
    "rubric_points": "23A-A prints 12/13 per part on the exam; raw 'points' and rubric sums match.",
    "regions_json": "Q1a and Q4a agree (grid within 0.06%).",
    "contours_json": "Q4b (abs max/min on the disc boundary) and Q5a (saddle f=144) agree; no interior critical point because (0,0) is outside the disc.",
}
build("23A-A", my23, {"flags": flags23})

my24 = {
    "1א": {"ans": "continuous (|f|<=r^2/4 -> 0 = f(0,0))"},
    "1ב": {"ans": "direction (-1,0) (grad = (-4/e,0))"},
    "2א": {"ans": "both series conditionally convergent (Leibniz; abs terms ~1/sqrt n and ~1/(2 sqrt n) diverge)"},
    "2ב": {"ans": "fx=fy=0; differentiable (eps = rho*sin(4 theta)/4 -> 0)"},
    "3א": {"ans": "R=1/2 in s=x+1; both endpoints converge; domain [-3/2,-1/2]"},
    "3ב": {"ans": "Euler homogeneity identity holds: x u_x+y u_y+z u_z = k u (chain+product rule; the F_s, F_t terms cancel; sympy leaves Subs forms, cancellation checked by inspection)"},
    "4א": {"ans": "7/24 (telescoping; sympy sum 7/24)"},
    "4ב": {"ans": "max 1 at (1,1),(-1,-1); min -1 at (1,-1),(-1,1)"},
    "5א": {"ans": "(0,0) saddle (D=-36); (1,1/2) local min (D=108, f_xx=6), f=0"},
    "5ב": {"ans": "sum 3^n x^(2n), |x|<1/sqrt3 (ends diverge); f^(5)(0)=0"},
}
flags24 = {
    "rubric_points": "24A-A raw 'points' 12/13 and rubric sums match.",
    "regions_json": "none needed (no double integral in 24A-A); no regions.json exists, which is correct.",
    "contours_json": "Q4b (xy on the circle: +-1) and Q5a (saddle f=1, min f=0) agree.",
}
build("24A-A", my24, {"flags": flags24})
