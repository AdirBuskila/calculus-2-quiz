# -*- coding: utf-8 -*-
"""L07 · גבול הדיפרנציאביליות — video script (build: tools/video/vid.py L07).

Source: courses/limits_diff/C07.js (lesson + goal). Exam anchor: 24A-A-Q2b (xy(x²−y²)/(x²+y²): partial derivatives
at the origin, differentiable?), which no guided quiz uses.
Avoided on purpose: the C07 quiz functions (x³/(x²+y²), x²y²/(x²+y²), and (x³+y³)/(x²+y²) — the last one is also the
exam part 22A-B-Q2b, so it waits for the L09 boss walkthrough), the lesson/C08 example x²y/(x²+y²), and the C09
boss parts. Worked examples (x³−2xy²)/(x²+y²) and x+2y+(x⁴+y⁴)/(x²+y²) are new.
Every value is computed below with sympy (w_limits_diff.pdef / Qexpr / rpow).
"""
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_limits_diff as W
from w_limits_diff import x, y, r, th, h, k

# ---------------------------------------------------------------- example 1: (x³−2xy²)/(x²+y²): f_x = 1, not differentiable
G = (x ** 3 - 2 * x * y ** 2) / (x ** 2 + y ** 2)
assert W.pdef(G, 0, "x") == 1 and W.pdef(G, 0, "y") == 0
QG = W.Qexpr(G, 0, 1, 0)
assert sp.simplify(QG + 3 * h * k ** 2 / (h ** 2 + k ** 2) ** sp.Rational(3, 2)) == 0
pg, gg = W.rpow(QG.subs({h: x, k: y}))
assert pg == 0 and sp.simplify(gg + 3 * sp.cos(th) * sp.sin(th) ** 2) == 0
QG_diag = sp.limit(QG.subs(k, h), h, 0, "+")
assert sp.simplify(QG_diag + 3 / (2 * sp.sqrt(2))) == 0              # along k = h > 0: −3/(2√2) ≠ 0
assert sp.limit(QG.subs(k, 0), h, 0, "+") == 0                      # along k = 0: 0

# ---------------------------------------------------------------- example 2: x + 2y + (x⁴+y⁴)/(x²+y²): the subtraction decides
F = x + 2 * y + (x ** 4 + y ** 4) / (x ** 2 + y ** 2)
assert W.pdef(F, 0, "x") == 1 and W.pdef(F, 0, "y") == 2
QF = W.Qexpr(F, 0, 1, 2)
pf, gf = W.rpow(QF.subs({h: x, k: y}))
assert pf == 1 and sp.simplify(gf - (sp.cos(th) ** 4 + sp.sin(th) ** 4)) == 0 and W.sup_abs(gf) <= 1
BAD = W.polar(F) / r                                                 # forgetting f_x h + f_y k
assert sp.simplify(BAD - (sp.cos(th) + 2 * sp.sin(th) + r * (sp.cos(th) ** 4 + sp.sin(th) ** 4))) == 0
assert sp.limit(BAD.subs(th, 0), r, 0) == 1 and sp.limit(BAD.subs(th, sp.pi / 2), r, 0) == 2

# ---------------------------------------------------------------- exam 24A-A-Q2b
Q = BANK["24A-A-Q2b"]
assert "xy\\cdot\\dfrac{x^2-y^2}{x^2+y^2}" in Q["question"]
FE = x * y * (x ** 2 - y ** 2) / (x ** 2 + y ** 2)
assert sp.simplify(FE.subs(y, 0)) == 0 and sp.simplify(FE.subs(x, 0)) == 0
assert W.pdef(FE, 0, "x") == 0 and W.pdef(FE, 0, "y") == 0
QE = W.Qexpr(FE, 0, 0, 0)
pe, ge = W.rpow(QE.subs({h: x, k: y}))
assert pe == 1
assert sp.simplify(ge - sp.cos(th) * sp.sin(th) * (sp.cos(th) ** 2 - sp.sin(th) ** 2)) == 0
assert sp.simplify(ge - sp.sin(4 * th) / 4) == 0 and W.sup_abs(ge) <= 1

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נבדוק אם פונקציה דיפרנציאבילית בראשית."),
    P("נבנה את הביטוי שצריך לשאוף לאפס, ונראה איך שוכחים בו דבר אחד והופכים את התשובה."),
    P("ובסוף נפתור שאלה ממבחן עד הסוף.", hold=0.4),
], stage='<div class="kicker">L07 · גבולות, רציפות ודיפרנציאביליות</div><h1>גבול הדיפרנציאביליות</h1>'
         '<p>לבנות את $Q(h,k)$, ולהכריע אם הוא שואף ל-$0$.</p>', layout="title")

DEF = [
    "$f(h,k)\\approx f(0,0)+f_x(0,0)\\,h+f_y(0,0)\\,k$",
    "$\\displaystyle Q(h,k)=\\frac{f(h,k)-f(0,0)-f_x(0,0)\\,h-f_y(0,0)\\,k}{\\sqrt{h^2+k^2}}$",
    "$\\displaystyle \\lim_{(h,k)\\to(0,0)}Q(h,k)=0$",
]
idea = Scene("idea", "ההגדרה", [
    P("דיפרנציאבילית בראשית פירושו: ליד הראשית, הפונקציה כמעט שווה למישור המשיק.", do=show("d-0")),
    P("המישור המשיק בנוי מהערך בראשית ומשתי הנגזרות החלקיות שם.", hold=0.2),
    P("השגיאה היא ההפרש בין הפונקציה למישור. מחלקים אותה במרחק מהראשית, ומקבלים את $Q$.", do=show("d-1"),
      say="השגיאה היא ההפרש בין הפונקציה למישור. מחלקים אותה במרחק מהראשית, ומקבלים את קְיוּ."),
    P("הפונקציה דיפרנציאבילית בדיוק כש-$Q$ שואף לאפס: השגיאה קטנה יותר מהמרחק.", do=show("d-2", "i-c1"),
      say="הפונקציה דיפרנציאבילית בדיוק כשקְיוּ שואף לאפס: השגיאה קטנה יותר מהמרחק."),
    P("סדר העבודה: נגזרות חלקיות לפי ההגדרה. מציבים ב-$Q$, **כולל החיסור**. ועוברים לקוטביות.", do=show("i-c2"),
      say="סדר העבודה: נגזרות חלקיות לפי ההגדרה. מציבים בקְיוּ, כולל החיסור. ועוברים לקוטביות."),
    P("חסם בלי זווית שהולך לאפס: דיפרנציאבילית. מסלול שבו $Q$ לא שואף לאפס: לא דיפרנציאבילית.", do=show("i-c3"),
      say="חסם בלי זווית שהולך לאפס: דיפרנציאבילית. מסלול שבו קְיוּ לא שואף לאפס: לא דיפרנציאבילית.", hold=0.4),
], stage=W.eqs("d", DEF, size=36, gap=36),
   panel=st.card("i-c1", "rule", "🔑 דיפרנציאבילית $\\iff Q\\to0$")
         + st.card("i-c2", "ex", "1. $f_x, f_y$ לפי ההגדרה &nbsp; 2. $Q$ עם החיסור &nbsp; 3. קוטביות")
         + st.card("i-c3", "rule", "🔑 $|Q|\\le Cr$: כן. מסלול עם $Q\\not\\to0$: לא"))

EX1 = [
    "$\\displaystyle g(x,y)=\\frac{x^3-2xy^2}{x^2+y^2},\\qquad g(0,0)=0$",
    "$g(h,0)=h\\ \\Rightarrow\\ g_x(0,0)=1,\\qquad g(0,h)=0\\ \\Rightarrow\\ g_y(0,0)=0$",
    "$\\displaystyle Q=\\frac{g(h,k)-h}{\\sqrt{h^2+k^2}}=\\frac{-3hk^2}{\\left(h^2+k^2\\right)^{3/2}}=-3\\cos\\theta\\,\\sin^2\\theta$",
    "$k=0:\\ 0\\qquad k=h>0:\\ -\\frac{3}{2\\sqrt2}$",
]
ex1 = Scene("ex1", "דוגמה", [
    P("דוגמה: $g=\\frac{x^3-2xy^2}{x^2+y^2}$, ובראשית $g(0,0)=0$.", say="דוגמה: אִקְס בשלישית פחות פעמיים אִקְס וַואי בריבוע, חלקי אִקְס בריבוע ועוד וַואי בריבוע. ובראשית, אפס.", do=show("a-0")),
    P("על ציר $x$ הפונקציה היא $h$, ולכן $g_x=1$. על ציר $y$ היא אפס, ולכן $g_y=0$.", do=show("a-1"),
      say="על ציר אִקְס הפונקציה היא אֵייץ', ולכן הנגזרת לפי אִקְס היא אחת. על ציר וַואי היא אפס, ולכן הנגזרת לפי וַואי היא אפס."),
    P("בונים את $Q$: מחסרים אחת כפול $h$, ועוד אפס כפול $k$. אחרי כינוס, המונה הוא מינוס שלוש $h$ $k$ בריבוע.", do=show("a-2"),
      say="בונים את קְיוּ: מחסרים אחת כפול אֵייץ', ועוד אפס כפול קֵיי. אחרי כינוס, המונה הוא מינוס שלוש אֵייץ' קֵיי בריבוע."),
    P("מונה מדרגה שלוש, ומכנה מדרגה שלוש. בקוטביות $r$ נעלם לגמרי, ונשאר ביטוי של זווית בלבד.",
      say="מונה מדרגה שלוש, ומכנה מדרגה שלוש. בקוטביות אָר נעלם לגמרי, ונשאר ביטוי של זווית בלבד."),
    P("על ציר $x$ הוא אפס, ועל האלכסון הוא מינוס שלוש חלקי פעמיים שורש שתיים.", do=show("a-3"),
      say="על ציר אִקְס הוא אפס, ועל האלכסון הוא מינוס שלוש חלקי פעמיים שורש שתיים."),
    P("$Q$ לא שואף לאפס, ולכן הפונקציה **אינה דיפרנציאבילית** בראשית.", do=show("a-v"),
      say="קְיוּ לא שואף לאפס, ולכן הפונקציה אינה דיפרנציאבילית בראשית.", hold=0.4),
], stage='<div class="ld-col" style="width:100%">' + W.eqs("a", EX1, size=32, gap=26)
         + W.verdict("a-v", "לא דיפרנציאבילית", ok=False) + '</div>')

EX2 = [
    "$\\displaystyle f(x,y)=x+2y+\\frac{x^4+y^4}{x^2+y^2},\\qquad f(0,0)=0$",
    "$f_x(0,0)=1,\\qquad f_y(0,0)=2$",
    "$\\displaystyle \\frac{f(h,k)}{r}=\\cos\\theta+2\\sin\\theta+r\\left(\\cos^4\\theta+\\sin^4\\theta\\right)\\ \\ \\text{✗}$",
    "$\\displaystyle Q=\\frac{f(h,k)-h-2k}{r}=r\\left(\\cos^4\\theta+\\sin^4\\theta\\right),\\quad |Q|\\le r\\to0$",
]
trap = Scene("trap", "המלכודת: החיסור", [
    P("ועכשיו המלכודת. הפונקציה: $x+2y+\\frac{x^4+y^4}{x^2+y^2}$, ובראשית אפס.", do=show("b-0"),
      say="ועכשיו המלכודת. הפונקציה: אִקְס ועוד פעמיים וַואי, ועוד אִקְס ברביעית ועוד וַואי ברביעית, חלקי אִקְס בריבוע ועוד וַואי בריבוע. ובראשית, אפס."),
    P("לפי ההגדרה, הנגזרות החלקיות הן אחת ושתיים. הן **לא** אפס.", do=show("b-1")),
    P("מי ששוכח לחסר אותן, מחלק את $f$ ב-$r$, ומקבל קוסינוס ועוד פעמיים סינוס. זה תלוי בזווית.", do=show("b-2", "b-c1"),
      say="מי ששוכח לחסר אותן, מחלק את אֶף באָר, ומקבל קוסינוס ועוד פעמיים סינוס. זה תלוי בזווית."),
    P("והמסקנה שלו: ״לא דיפרנציאבילית״. וזו מסקנה **שגויה**.", hold=0.3),
    P("עם החיסור, החלק הלינארי נמחק לגמרי, ונשאר $r$ כפול ביטוי חסום באחת.", do=show("b-3"),
      say="עם החיסור, החלק הלינארי נמחק לגמרי, ונשאר אָר כפול ביטוי חסום באחת."),
    P("$Q$ שואף לאפס, והפונקציה **דיפרנציאבילית**. החיסור הפך את התשובה.", do=show("b-v", "b-c2"),
      say="קְיוּ שואף לאפס, והפונקציה דיפרנציאבילית. החיסור הפך את התשובה.", hold=0.4),
], stage='<div class="ld-col" style="width:100%">' + W.eqs("b", EX2, size=30, gap=26)
         + W.verdict("b-v", "דיפרנציאבילית", ok=True) + '</div>',
   panel=st.card("b-c1", "trap", "⚠️ בלי החיסור: מסקנה הפוכה")
         + st.card("b-c2", "rule", "🔑 נגזרות שאינן אפס: מחסרים $f_x h+f_y k$"))

EXE = [
    "$f(h,0)=0,\\ \\ f(0,h)=0\\ \\Rightarrow\\ f_x(0,0)=f_y(0,0)=0$",
    "$\\displaystyle Q=\\frac{f(h,k)-0-0-0}{\\sqrt{h^2+k^2}}=\\frac{hk\\left(h^2-k^2\\right)}{\\left(h^2+k^2\\right)^{3/2}}$",
    "$\\displaystyle Q=\\frac{r^4\\cos\\theta\\,\\sin\\theta\\left(\\cos^2\\theta-\\sin^2\\theta\\right)}{r^3}=r\\cos\\theta\\,\\sin\\theta\\left(\\cos^2\\theta-\\sin^2\\theta\\right)$",
    "$|Q|\\le r\\cdot1\\cdot1\\cdot1=r\\ \\to\\ 0$",
]
exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: $f=xy\\cdot\\frac{x^2-y^2}{x^2+y^2}$, ובראשית $f(0,0)=0$.", say="שאלה ממבחן: אִקְס וַואי, כפול אִקְס בריבוע פחות וַואי בריבוע, חלקי אִקְס בריבוע ועוד וַואי בריבוע. ובראשית, אפס."),
    P("מצאו את הנגזרות החלקיות בראשית. האם הפונקציה דיפרנציאבילית שם?", hold=0.3),
    P("שלב אחד: על שני הצירים יש גורם $x$ $y$ שמתאפס. הפונקציה היא אפס, ושתי הנגזרות החלקיות אפס.", do=show("e-0"),
      say="שלב אחד: על שני הצירים יש גורם אִקְס וַואי שמתאפס. הפונקציה היא אפס, ושתי הנגזרות החלקיות אפס."),
    P("שלב שתיים: הנגזרות אפס, אז אין מה לחסר. $Q$ הוא $f$ חלקי השורש.", do=show("e-1"),
      say="שלב שתיים: הנגזרות אפס, אז אין מה לחסר. קְיוּ הוא אֶף חלקי השורש."),
    P("שלב שלוש: קוטביות. המונה מדרגה ארבע, והמכנה מדרגה שלוש. נשאר $r$ אחד.", do=show("e-2"),
      say="שלב שלוש: קוטביות. המונה מדרגה ארבע, והמכנה מדרגה שלוש. נשאר אָר אחד."),
    P("קוסינוס, סינוס, והסוגריים: כל אחד מהם בין מינוס אחת לאחת.", do=show("e-c1")),
    P("לכן $Q$ קטן מ-$r$, בלי שום זווית בחסם, ושואף לאפס.", do=show("e-3"),
      say="לכן קְיוּ קטן מאָר, בלי שום זווית בחסם, ושואף לאפס."),
    P("והתשובה: הפונקציה **דיפרנציאבילית** בראשית.", do=show("e-v"), hold=0.3),
    P("המלכודת כאן: לבדוק את $Q$ רק על כמה ישרים. רק חסם שלא תלוי בזווית מוכיח שהוא שואף לאפס.", do=show("e-t"),
      say="המלכודת כאן: לבדוק את קְיוּ רק על כמה ישרים. רק חסם שלא תלוי בזווית מוכיח שהוא שואף לאפס.", hold=0.5),
], stage='<div class="ld-col" style="width:100%">' + W.eqs("e", EXE, size=28, gap=22)
         + W.verdict("e-v", "דיפרנציאבילית", ok=True) + '</div>',
   panel=W.stem(Q["id"], "מצאו את $f_x(0,0)$ ו-$f_y(0,0)$. האם $f$ דיפרנציאבילית ב-$(0,0)$?")
         + '<div class="ld-pw" style="font-size:30px">$f(x,y)=xy\\cdot\\dfrac{x^2-y^2}{x^2+y^2}$, $\\ f(0,0)=0$</div>'
         + st.card("e-c1", "ex", "$|\\cos\\theta|,\\ |\\sin\\theta|,\\ |\\cos^2\\theta-\\sin^2\\theta|\\le1$")
         + st.card("e-t", "trap", "⚠️ כמה ישרים לא מוכיחים $Q\\to0$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: דיפרנציאבילית פירושו ש-$Q$ שואף לאפס.", do=show("s-1"),
      say="לסיכום: דיפרנציאבילית פירושו שקְיוּ שואף לאפס."),
    P("נגזרות חלקיות לפי ההגדרה, ואז $Q$, עם החיסור של החלק הלינארי.", do=show("s-2"),
      say="נגזרות חלקיות לפי ההגדרה, ואז קְיוּ, עם החיסור של החלק הלינארי."),
    P("נשאר $r$ כפול חסום? דיפרנציאבילית. נשאר ביטוי שתלוי בזווית בלבד? לא דיפרנציאבילית.", do=show("s-3"),
      say="נשאר אָר כפול חסום? דיפרנציאבילית. נשאר ביטוי שתלוי בזווית בלבד? לא דיפרנציאבילית."),
    P("בסרטון הבא: מה גורר מה, ושתי דוגמאות נגדיות קלאסיות. נתראה.", do=show("s-4"), hold=0.6),
], stage=W.eqs("t", DEF[1:2], size=36, shown=1),
   panel=st.card("s-1", "rule", "🔑 דיפרנציאבילית $\\iff Q\\to0$")
         + st.card("s-2", "trap", "⚠️ לא לשכוח: $-f_xh-f_yk$")
         + st.card("s-3", "rule", "🔑 $r\\cdot$חסום: כן. רק $\\theta$: לא")
         + st.card("s-4", "ex", "הבא: מה גורר מה"))

VIDEO = Video("L07", "limits_diff", "גבול הדיפרנציאביליות", [title, idea, ex1, trap, exam, recap],
              bank={"24A-A-Q2b": None})
