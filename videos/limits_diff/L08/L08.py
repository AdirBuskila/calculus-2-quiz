# -*- coding: utf-8 -*-
"""L08 · יש נגזרות חלקיות, ובכל זאת לא דיפרנציאבילית — video script (build: tools/video/vid.py L08).

Source: courses/limits_diff/C08.js (lesson + goal). Exam anchor: 24B-A-Q1c (the total differential df at (1,1) of
yx²/(2y²+3x⁴)), which no guided quiz uses: the sufficient condition (continuous partials near the point) is exactly
what makes df legitimate there.
CAREFUL: parts a and b of the same exam question (24B-A-Q1a/b, the origin) are C09 boss-quiz questions; the video
never says anything about this function at the origin.
Avoided on purpose: the C08 quiz functions (xy/(x²+y²), x²y/(x²+y²), (x²+y²)sin(1/√(x²+y²))) and the C08-Q5
statements as such. The three counterexamples are the L02 exam function 4x³y/(3x⁶+2y²), the L07 example
(x³−2xy²)/(x²+y²), and the new x²·sin(1/x). Every value is computed below with sympy.
"""
import numpy as np
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_limits_diff as W
from w_limits_diff import x, y, r, th, h, k

kk = sp.Symbol("k", real=True)

# ---------------------------------------------------------------- A: partials exist, not continuous (L02 exam function)
A = 4 * x ** 3 * y / (3 * x ** 6 + 2 * y ** 2)
assert W.pdef(A, 0, "x") == 0 and W.pdef(A, 0, "y") == 0
assert W.along(A, x ** 3) == sp.Rational(4, 5)                      # != f(0,0) = 0: not continuous

# ---------------------------------------------------------------- B: continuous + partials, not differentiable (L07 example)
B = (x ** 3 - 2 * x * y ** 2) / (x ** 2 + y ** 2)
pb, gb = W.rpow(B)
assert pb == 1 and W.sup_abs(gb) <= 3                               # |B| <= 3r -> 0 = B(0,0): continuous
assert W.pdef(B, 0, "x") == 1 and W.pdef(B, 0, "y") == 0
QB = W.Qexpr(B, 0, 1, 0)
assert sp.simplify(sp.limit(QB.subs(k, h), h, 0, "+") + 3 / (2 * sp.sqrt(2))) == 0

# ---------------------------------------------------------------- C: differentiable, f_x not continuous: x² sin(1/x)
C = x ** 2 * sp.sin(1 / x)                                          # for x != 0; C = 0 on the line x = 0
assert sp.limit(C.subs(x, h) / h, h, 0) == 0                        # f_x(0,0) = 0
# f_y(0,0) = 0 because C(0, h) = 0 (the line x = 0)
_hk = np.random.default_rng(1).uniform(-1e-2, 1e-2, size=(4000, 2))
_hk = _hk[_hk[:, 0] != 0]
_Q = (_hk[:, 0] ** 2 * np.sin(1 / _hk[:, 0])) / np.hypot(_hk[:, 0], _hk[:, 1])
assert np.all(np.abs(_Q) <= np.hypot(_hk[:, 0], _hk[:, 1]) + 1e-15)  # |Q| <= h²/r <= r
CX = sp.diff(C, x)
assert sp.simplify(CX - (2 * x * sp.sin(1 / x) - sp.cos(1 / x))) == 0
_x = 1 / (np.pi * np.arange(200, 400))                               # x = 1/(nπ) -> 0: cos(1/x) = ±1
_v = 2 * _x * np.sin(1 / _x) - np.cos(1 / _x)
assert _v.max() > 0.99 and _v.min() < -0.99                         # f_x keeps jumping near 1 and −1: no limit

# ---------------------------------------------------------------- exam 24B-A-Q1c: df at (1, 1)
Q = BANK["24B-A-Q1c"]
assert "yx^2" in Q["question"] and "(1,1)" in Q["question"]
FE = y * x ** 2 / (2 * y ** 2 + 3 * x ** 4)
FX, FY = sp.diff(FE, x), sp.diff(FE, y)
assert sp.simplify(FX - (2 * x * y * (2 * y ** 2 + 3 * x ** 4) - 12 * x ** 5 * y) / (2 * y ** 2 + 3 * x ** 4) ** 2) == 0
assert sp.simplify(FY - (x ** 2 * (2 * y ** 2 + 3 * x ** 4) - 4 * x ** 2 * y ** 2) / (2 * y ** 2 + 3 * x ** 4) ** 2) == 0
assert FX.subs({x: 1, y: 1}) == sp.Rational(-2, 25) and FY.subs({x: 1, y: 1}) == sp.Rational(1, 25)
assert (2 * y ** 2 + 3 * x ** 4).subs({x: 1, y: 1}) == 5            # the denominator is 5 there, never 0 nearby

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נסדר את הקשרים בין רציפות, נגזרות חלקיות ודיפרנציאביליות."),
    P("נראה איזה כיוון של כל חץ נכון, ושלוש דוגמאות נגדיות שמראות למה."),
    P("ובסוף נחשב דיפרנציאל שלם בשאלה ממבחן.", hold=0.4),
], stage='<div class="kicker">L08 · גבולות, רציפות ודיפרנציאביליות</div><h1>יש נגזרות חלקיות, ובכל זאת לא דיפרנציאבילית</h1>'
         '<p>איזו תכונה גוררת איזו, ואיך מזהים את הדוגמאות הנגדיות.</p>', layout="title")

ROWS = [
    ("דיפרנציאבילית", "⟵ גוררת", "רציפה, <b>וגם</b> יש נגזרות חלקיות"),
    ("נגזרות חלקיות קיימות", "✗ לא גוררות", "רציפות"),
    ("רציפה, ויש נגזרות חלקיות", "✗ לא גוררות", "דיפרנציאביליות"),
    ("נגזרות חלקיות <b>רציפות</b> בסביבה", "⟵ גוררות", "דיפרנציאביליות"),
]
ladder = Scene("ladder", "מה גורר מה", [
    P("בשני משתנים יש שלוש רמות: רציפות, נגזרות חלקיות, ודיפרנציאביליות. והן לא שקולות."),
    P("דיפרנציאבילית בנקודה? אז היא גם רציפה שם, וגם יש לה שם נגזרות חלקיות.", do=show("l-0")),
    P("אבל הכיוון ההפוך לא נכון: נגזרות חלקיות לבד לא מבטיחות אפילו רציפות.", do=show("l-1")),
    P("וגם רציפות ונגזרות חלקיות ביחד עדיין לא מבטיחות דיפרנציאביליות.", do=show("l-2")),
    P("מה כן מבטיח? נגזרות חלקיות שהן **רציפות** בסביבת הנקודה. זה תנאי מספיק.", do=show("l-3"), hold=0.4),
], stage=W.ladder("l", ROWS),
   panel=st.card("ld-c1", "rule", "🔑 דיפרנציאבילית: הכי חזקה. גוררת את שתי האחרות")
         + st.card("ld-c2", "trap", "⚠️ החצים לא הולכים אחורה"),
)
ladder.phrases[1].do += show("ld-c1")
ladder.phrases[2].do += show("ld-c2")

CA = [
    "$\\displaystyle f=\\frac{4x^3y}{3x^6+2y^2}:\\quad f_x(0,0)=f_y(0,0)=0,\\quad f\\left(x,x^3\\right)=\\frac45$",
    "$\\displaystyle g=\\frac{x^3-2xy^2}{x^2+y^2}:\\quad |g|\\le3r,\\quad g_x=1,\\ g_y=0,\\quad Q\\left(h,h\\right)=-\\frac{3}{2\\sqrt2}$",
]
counter = Scene("counter", "שתי דוגמאות נגדיות", [
    P("דוגמה נגדית ראשונה, מהסרטון השני: הפונקציה ממבחן עם $x^6$ ועם $y^2$ במכנה.", do=show("c-0"),
      say="דוגמה נגדית ראשונה, מהסרטון השני: הפונקציה ממבחן עם אִקְס בשישית ועם וַואי בריבוע במכנה."),
    P("על הצירים היא אפס, ולכן שתי הנגזרות החלקיות קיימות ושוות לאפס.", hold=0.2),
    P("אבל על $y=x^3$ הערך הוא ארבע חמישיות. היא לא רציפה, ולכן גם לא דיפרנציאבילית.", do=show("c-c1"),
      say="אבל על וַואי שווה אִקְס בשלישית הערך הוא ארבע חמישיות. היא לא רציפה, ולכן גם לא דיפרנציאבילית."),
    P("דוגמה שנייה, מהסרטון הקודם: $g$ עם $x^3$ פחות פעמיים $xy^2$.", do=show("c-1"),
      say="דוגמה שנייה, מהסרטון הקודם: גִ'י, עם אִקְס בשלישית פחות פעמיים אִקְס וַואי בריבוע."),
    P("בקוטביות היא חסומה בשלוש $r$, ולכן רציפה. ויש לה נגזרות חלקיות: אחת ואפס.",
      say="בקוטביות היא חסומה בשלוש אָר, ולכן רציפה. ויש לה נגזרות חלקיות: אחת ואפס."),
    P("ובכל זאת, על האלכסון $Q$ שואף למינוס שלוש חלקי פעמיים שורש שתיים. לא דיפרנציאבילית.", do=show("c-c2"),
      say="ובכל זאת, על האלכסון קְיוּ שואף למינוס שלוש חלקי פעמיים שורש שתיים. לא דיפרנציאבילית.", hold=0.4),
], stage=W.eqs("c", CA, size=30, gap=50),
   panel=st.card("c-c1", "trap", "⚠️ נגזרות חלקיות קיימות, ולא רציפה")
         + st.card("c-c2", "trap", "⚠️ רציפה ועם נגזרות, ולא דיפרנציאבילית"))

CC = [
    "$f(x,y)=\\begin{cases}x^2\\sin\\frac1x, & x\\neq0\\\\ 0, & x=0\\end{cases}$",
    "$|Q|=\\dfrac{|f(h,k)|}{\\sqrt{h^2+k^2}}\\le\\dfrac{h^2}{r}\\le r\\ \\to\\ 0$",
    "$f_x=2x\\sin\\frac1x-\\cos\\frac1x\\qquad(x\\neq0)$",
]
suff = Scene("suff", "רק תנאי מספיק", [
    P("והתנאי המספיק: נגזרות חלקיות רציפות מבטיחות דיפרנציאביליות. אבל הוא **לא** הכרחי.", do=show("s-c1")),
    P("דוגמה: $x^2\\sin\\frac1x$, ואפס על הקו $x=0$.", say="דוגמה: אִקְס בריבוע כפול סינוס של אחת חלקי אִקְס, ואפס על הקו שבו אִקְס הוא אפס.", do=show("d-0")),
    P("בראשית שתי הנגזרות החלקיות אפס, ו-$Q$ חסום ב-$r$: הפונקציה דיפרנציאבילית.", do=show("d-1"),
      say="בראשית שתי הנגזרות החלקיות אפס, וקְיוּ חסום באָר: הפונקציה דיפרנציאבילית."),
    P("אבל הנגזרת לפי $x$, מחוץ לקו, כוללת את $-\\cos\\frac1x$.", do=show("d-2"),
      say="אבל הנגזרת לפי אִקְס, מחוץ לקו, כוללת מינוס קוסינוס של אחת חלקי אִקְס."),
    P("כשמתקרבים לראשית הקוסינוס מתנדנד בין מינוס אחת לאחת, ולנגזרת אין גבול. היא לא רציפה.", do=show("s-c2")),
    P("אז דיפרנציאבילית בלי נגזרות רציפות: אפשרי. התנאי עובד רק בכיוון אחד.", hold=0.4),
], stage=W.eqs("d", CC, size=36, gap=34),
   panel=st.card("s-c1", "rule", "🔑 נגזרות חלקיות רציפות: <b>מספיק</b>, לא הכרחי")
         + st.card("s-c2", "trap", "⚠️ דיפרנציאבילית, ו-$f_x$ לא רציפה בראשית"))

EXE = [
    "$\\displaystyle f_x=\\frac{2xy\\left(2y^2+3x^4\\right)-12x^5y}{\\left(2y^2+3x^4\\right)^2},\\qquad f_x(1,1)=\\frac{2\\cdot5-12}{25}=-\\frac{2}{25}$",
    "$\\displaystyle f_y=\\frac{x^2\\left(2y^2+3x^4\\right)-4x^2y^2}{\\left(2y^2+3x^4\\right)^2},\\qquad f_y(1,1)=\\frac{5-4}{25}=\\frac{1}{25}$",
    "$\\displaystyle df=f_x(1,1)\\,dx+f_y(1,1)\\,dy=\\frac{-2\\,dx+dy}{25}$",
]
exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: $f=\\frac{yx^2}{2y^2+3x^4}$, ובראשית $f(0,0)=0$.", say="שאלה ממבחן: וַואי אִקְס בריבוע, חלקי פעמיים וַואי בריבוע ועוד שלוש אִקְס ברביעית. ובראשית, אפס."),
    P("מצאו את הדיפרנציאל השלם בנקודה אחת, אחת.", hold=0.3),
    P("קודם כול: למה מותר בכלל לכתוב דיפרנציאל? כי צריך שהפונקציה תהיה דיפרנציאבילית שם.", do=show("e-c1")),
    P("ליד הנקודה אחת, אחת, המכנה קרוב לחמש, רחוק מאפס. שם $f$ היא מנה של פולינומים.",
      say="ליד הנקודה אחת, אחת, המכנה קרוב לחמש, רחוק מאפס. שם אֶף היא מנה של פולינומים."),
    P("לכן הנגזרות החלקיות קיימות ורציפות בסביבה, והתנאי המספיק נותן דיפרנציאביליות.", hold=0.3),
    P("לפי $x$, בכלל המנה. מציבים אחת, אחת: המכנה הוא חמש, ובמונה פעמיים חמש פחות שתים עשרה.", do=show("e-0"),
      say="לפי אִקְס, בכלל המנה. מציבים אחת, אחת: המכנה הוא חמש, ובמונה פעמיים חמש פחות שתים עשרה."),
    P("יוצא מינוס שתיים חלקי עשרים וחמש.", hold=0.2),
    P("לפי $y$: במונה חמש פחות ארבע, כלומר אחת. יוצא אחת חלקי עשרים וחמש.", do=show("e-1"),
      say="לפי וַואי: במונה חמש פחות ארבע, כלומר אחת. יוצא אחת חלקי עשרים וחמש."),
    P("והדיפרנציאל: מינוס שתיים $dx$ ועוד $dy$, הכול חלקי עשרים וחמש.", do=show("e-2", "e-v"),
      say="והדיפרנציאל: מינוס שתיים דִּי אִקְס ועוד דִּי וַואי, הכול חלקי עשרים וחמש."),
    P("והמלכודת: בראשית אי אפשר להשתמש בכללי גזירה ובתנאי המספיק. שם בודקים לפי ההגדרה, כמו בשלב הבוס.",
      do=show("e-t"), hold=0.5),
], stage='<div class="ld-col" style="width:100%">' + W.eqs("e", EXE, size=26, gap=26)
         + W.verdict("e-v", "$df=\\frac{-2\\,dx+dy}{25}$", ok=True) + '</div>',
   panel=W.stem(Q["id"], "מצאו את הדיפרנציאל השלם $df$ בנקודה $(1,1)$.")
         + W.piecewise("\\frac{yx^2}{2y^2+3x^4}", size=32)
         + st.card("e-c1", "rule", "🔑 נגזרות רציפות בסביבה, ולכן דיפרנציאבילית")
         + st.card("e-t", "trap", "⚠️ בראשית: רק לפי ההגדרה"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: דיפרנציאבילית גוררת רציפה, וגוררת נגזרות חלקיות.", do=show("r-1")),
    P("נגזרות חלקיות לבד, או יחד עם רציפות, לא גוררות דיפרנציאביליות.", do=show("r-2")),
    P("נגזרות חלקיות רציפות בסביבה: מספיק, אבל לא הכרחי.", do=show("r-3")),
    P("בסרטון הבא, הבוס: שאלות מבחן מלאות מההתחלה ועד הסוף. נתראה.", do=show("r-4"), hold=0.6),
], stage=W.ladder("lr", ROWS).replace(' h"', '"'),
   panel=st.card("r-1", "rule", "🔑 דיפרנציאבילית: רציפה + נגזרות")
         + st.card("r-2", "trap", "⚠️ נגזרות (+ רציפות): לא מספיק")
         + st.card("r-3", "rule", "🔑 נגזרות <b>רציפות</b>: מספיק")
         + st.card("r-4", "ex", "הבא: הבוס"))

VIDEO = Video("L08", "limits_diff", "יש נגזרות חלקיות, ובכל זאת לא דיפרנציאבילית",
              [title, ladder, counter, suff, exam, recap], bank={"24B-A-Q1c": None})
