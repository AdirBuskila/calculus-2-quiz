# -*- coding: utf-8 -*-
"""L03 · ישרים לא מספיקים — video script (build: tools/video/vid.py L03).

Source: courses/limits_diff/C03.js (lesson + goal). Exam anchor: 24A-A-Q1a ((x³y−xy³)/(x²+y²): continuous at the
origin?), which no guided quiz uses. All lines give 0 there AND the limit really is 0; the point is that the lines
prove nothing and the proof is a bound in polar coordinates.
Avoided on purpose: the C03 quiz function 2x²y/(x⁴+y²) and the C09 boss parts. The worked example x⁴y²/(x⁸+y⁴)
is new. Every value is computed below with sympy.
"""
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_limits_diff as W
from w_limits_diff import x, y, r, th

m = sp.Symbol("m", real=True)

# ---------------------------------------------------------------- example: x⁴y²/(x⁸+y⁴)
V = x ** 4 * y ** 2 / (x ** 8 + y ** 4)
assert sp.simplify(V.subs(y, m * x) - m ** 2 * x ** 2 / (x ** 4 + m ** 4)) == 0
assert all(W.along(V, c * x) == 0 for c in (1, -1, 2, sp.Rational(1, 3)))
assert sp.simplify(V.subs(y, 0)) == 0 and sp.simplify(V.subs(x, 0)) == 0
assert sp.simplify(V.subs(y, x ** 2)) == sp.Rational(1, 2)
kk = sp.Symbol("k", real=True)
assert sp.simplify(V.subs(y, kk * x ** 2) - kk ** 2 / (1 + kk ** 4)) == 0     # every parabola: depends on k

# ---------------------------------------------------------------- exam 24A-A-Q1a
Q = BANK["24A-A-Q1a"]
assert "x^3y-xy^3" in Q["question"]
FE = (x ** 3 * y - x * y ** 3) / (x ** 2 + y ** 2)
assert sp.simplify(FE.subs(y, m * x) - x ** 2 * (m - m ** 3) / (1 + m ** 2)) == 0
assert all(W.along(FE, c * x) == 0 for c in (1, -1, 2, 5))
p, g = W.rpow(FE)
BR = sp.cos(th) ** 3 * sp.sin(th) - sp.cos(th) * sp.sin(th) ** 3
assert p == 2 and sp.simplify(g - BR) == 0                       # f = r² (cos³θ sinθ − cosθ sin³θ)
assert W.sup_abs(BR) <= 2 + 1e-12                                 # each term is at most 1 in absolute value
assert sp.simplify(sp.expand_trig(sp.sin(4 * th) / 4) - BR) == 0  # (the exact bracket: sin4θ/4, not needed)
assert sp.limit(2 * r ** 2, r, 0) == 0

# ---------------------------------------------------------------- stage pieces
PV = W.plane("pv", [
    ("a", "y", lambda t: 0.0, "", None, "a"),
    ("b", "y", lambda t: t, "", None, "a"),
    ("c", "y", lambda t: -t, "", None, "a"),
    ("d", "y", lambda t: 2 * t, "", None, "a"),
    ("f", "y", lambda t: -0.4 * t, "", None, "a"),
    ("e", "y", lambda t: t * t, "y = x²", "→ ½", "e", {"lab": (-0.55, 0.85), "tag": (0.12, 0.62)}),
], w=420, hgt=420)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר אסימטריה חשובה בגבולות של שני משתנים."),
    P("מסלולים יודעים להפיל גבול, אבל הם לא יודעים להוכיח שהוא קיים."),
    P("ובסוף נפתור שאלה ממבחן שבה כל הישרים מסכימים.", hold=0.4),
], stage='<div class="kicker">L03 · גבולות, רציפות ודיפרנציאביליות</div><h1>ישרים לא מספיקים</h1>'
         '<p>מה שני מסלולים מוכיחים, ומה שאף מספר סופי של מסלולים לא יכול להוכיח.</p>', layout="title")

asym = Scene("asym", "האסימטריה", [
    P("כדי להוכיח שהגבול **אינו קיים**, מספיקים שני מסלולים עם ערכים שונים.", do=show("a-1", "cm-0")),
    P("כי אם הגבול היה קיים, כל המסלולים היו חייבים לתת אותו ערך.", hold=0.3),
    P("ובבדיקת רציפות מספיק אפילו מסלול אחד, שבו הערך שונה מהערך של הפונקציה בראשית.", do=show("a-2")),
    P("אבל כדי להוכיח שהגבול **קיים**, שום מספר של מסלולים לא מספיק.", do=show("a-3", "cm-1")),
    P("בדקתם עשרה ישרים? מאה? תמיד נשאר עקום שעוד לא בדקתם.", hold=0.4),
], stage=W.compare("cm", [("להפיל גבול", "שני מסלולים עם ערכים שונים", "✓ מספיק", True),
                          ("להוכיח שגבול קיים", "עשרה מסלולים, מאה, כל הישרים", "✗ לא מספיק", False)]),
   panel=st.card("a-1", "rule", "🔑 אי-קיום: <b>שני מסלולים</b> עם ערכים שונים")
         + st.card("a-2", "ex", "אי-רציפות: מסלול אחד שבו הערך שונה מ-$f(0,0)$")
         + st.card("a-3", "trap", "⚠️ קיום: <b>אף מספר</b> של מסלולים לא מספיק"))

EX = [
    "$\\displaystyle v(x,y)=\\frac{x^4y^2}{x^8+y^4}$",
    "$\\displaystyle v(x,mx)=\\frac{m^2x^6}{x^8+m^4x^4}=\\frac{m^2x^2}{x^4+m^4}\\ \\to\\ 0$",
    "$v(x,0)=0,\\qquad v(0,y)=0$",
    "$\\displaystyle v\\left(x,x^2\\right)=\\frac{x^8}{x^8+x^8}=\\frac12$",
    "$\\displaystyle v\\left(x,kx^2\\right)=\\frac{k^2}{1+k^4}$",
]
example = Scene("example", "כל הישרים טועים", [
    P("דוגמה: $v(x,y)=\\frac{x^4y^2}{x^8+y^4}$.", say="דוגמה: וִי שווה אִקְס ברביעית וַואי בריבוע, חלקי אִקְס בשמינית ועוד וַואי ברביעית.", do=show("x-0")),
    P("על ישר $y=mx$ נשאר $x^2$ במונה, ולכן הערך שואף לאפס, בכל שיפוע.", do=show("x-1", "pv-c-b", "pv-c-c", "pv-c-d", "pv-c-f"),
      say="על ישר וַואי שווה אֶם אִקְס נשאר אִקְס בריבוע במונה, ולכן הערך שואף לאפס, בכל שיפוע."),
    P("ועל שני הצירים הפונקציה שווה לאפס.", do=show("x-2", "pv-c-a")),
    P("כל הישרים דרך הראשית מסכימים: אפס. זה נראה משכנע מאוד.", hold=0.3),
    P("אבל על הפרבולה $y=x^2$ המונה והמכנה שניהם מסדר $x^8$, והערך הוא חצי.", do=show("x-3", "pv-c-e", "pv-t-e"),
      say="אבל על הפרבולה וַואי שווה אִקְס בריבוע, המונה והמכנה שניהם מסדר אִקְס בשמינית, והערך הוא חצי."),
    P("אפס מול חצי: הגבול **אינו קיים**, למרות שאף ישר לא גילה את זה.", do=show("x-c1"), hold=0.3),
    P("ועל כל פרבולה $y=kx^2$ יוצא $k^2$ חלקי אחת ועוד $k$ ברביעית: ערך שתלוי בפרבולה.", do=show("x-4"),
      say="ועל כל פרבולה וַואי שווה קֵיי אִקְס בריבוע, יוצא קֵיי בריבוע חלקי אחת ועוד קֵיי ברביעית: ערך שתלוי בפרבולה."),
    P("הישרים פשוט עברו ליד הבעיה, ולא דרכה.", hold=0.4),
], stage='<div class="ld-row"><div class="ld-col" style="width:580px">' + W.eqs("x", EX, size=30, gap=20)
         + f'</div>{PV}</div>',
   panel=st.card("x-c1", "trap", "⚠️ כל הישרים נתנו $0$, והגבול בכל זאת אינו קיים"))

PROVE = [
    "$x=r\\,\\cos\\theta,\\qquad y=r\\,\\sin\\theta$",
    "$\\left|f(x,y)-L\\right|\\le g(r)\\ \\xrightarrow[r\\to0]{}\\ 0$",
]
prove = Scene("prove", "אז מה כן מוכיח", [
    P("אז איך מוכיחים שגבול קיים? צריך טיעון שמכסה את **כל** הכיוונים בבת אחת."),
    P("כותבים כל נקודה בעזרת המרחק שלה מהראשית, $r$, והזווית שלה, $\\theta$.", do=show("pp-r1", "pp-lab", "q-0"),
      say="כותבים כל נקודה בעזרת המרחק שלה מהראשית, אָר, והזווית שלה, תטא."),
    P("להתקרב לראשית, בכל דרך שהיא, פירושו ש-$r$ שואף לאפס.", do=show("pp-r2", "pp-r3"),
      say="להתקרב לראשית, בכל דרך שהיא, פירושו שאָר שואף לאפס."),
    P("אם המרחק מ-$L$ חסום בביטוי שתלוי **רק** ב-$r$, ושואף לאפס, הגבול הוא $L$.", do=show("q-1", "p-c1"),
      say="אם המרחק מאֶל חסום בביטוי שתלוי רק באָר, ושואף לאפס, הגבול הוא אֶל."),
    P("החסם לא תלוי בזווית, ולכן הוא תופס כל מסלול, גם עקום שלא חשבנו עליו.", hold=0.4),
], stage='<div class="ld-row"><div class="ld-col" style="width:520px">' + W.eqs("q", PROVE, size=36, gap=40)
         + '</div>' + W.polar_pic("pp", w=440, hgt=440) + '</div>',
   panel=st.card("p-c1", "rule", "🔑 קיום: חסם $g(r)\\to0$ שאינו תלוי ב-$\\theta$"))

EXE = [
    "$\\displaystyle f(x,mx)=\\frac{\\left(m-m^3\\right)x^4}{\\left(1+m^2\\right)x^2}\\ \\to\\ 0$",
    "$f=r^2\\left(\\cos^3\\theta\\,\\sin\\theta-\\cos\\theta\\,\\sin^3\\theta\\right)$",
    "$\\left|f-0\\right|\\le r^2\\,(1+1)=2r^2\\ \\to\\ 0$",
    "$\\lim_{(x,y)\\to(0,0)}f=0=f(0,0)$",
]
exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: $f=\\frac{x^3y-xy^3}{x^2+y^2}$.", say="שאלה ממבחן: אִקְס בשלישית וַואי, פחות אִקְס וַואי בשלישית, חלקי אִקְס בריבוע ועוד וַואי בריבוע."),
    P("ובראשית, אפס. האם הפונקציה רציפה בראשית? נמקו.", hold=0.3),
    P("על ישר $y=mx$ נשאר $x^2$, ולכן כל הישרים נותנים אפס.", do=show("e-0"),
      say="על ישר וַואי שווה אֶם אִקְס נשאר אִקְס בריבוע, ולכן כל הישרים נותנים אפס."),
    P("והמלכודת: לכתוב ״כל הישרים נותנים אפס, ולכן רציפה״. זו לא הוכחה, ובמבחן היא לא שווה נקודות.", do=show("e-t")),
    P("אפס הוא רק המועמד. עכשיו מוכיחים, בקוטביות.", hold=0.3),
    P("המונה מדרגה ארבע והמכנה מדרגה שתיים, ולכן נשאר $r^2$, כפול סוגריים שתלויים רק בזווית.", do=show("e-1"),
      say="המונה מדרגה ארבע והמכנה מדרגה שתיים, ולכן נשאר אָר בריבוע, כפול סוגריים שתלויים רק בזווית."),
    P("כל אחד משני המחוברים בסוגריים הוא מכפלה של סינוסים וקוסינוסים, ולכן הוא לכל היותר אחת בערך מוחלט.", do=show("e-c1")),
    P("אפשר גם לחשב שהסוגריים שווים בדיוק לסינוס של ארבע תטא חלקי ארבע. אבל לא צריך: חסם גס מספיק."),
    P("לכן הפונקציה חסומה בפעמיים $r^2$. החסם לא תלוי בזווית, והוא שואף לאפס.", do=show("e-2"),
      say="לכן הפונקציה חסומה בפעמיים אָר בריבוע. החסם לא תלוי בזווית, והוא שואף לאפס."),
    P("מסנדוויץ', הגבול הוא אפס, וזה בדיוק הערך של הפונקציה בראשית.", do=show("e-3")),
    P("לכן הפונקציה **רציפה** בראשית. הישרים רק הראו לנו את המועמד.", do=show("e-v"), hold=0.5),
], stage='<div class="ld-col" style="width:100%">' + W.eqs("e", EXE, size=38, gap=26)
         + W.verdict("e-v", "רציפה בראשית", ok=True) + '</div>',
   panel=W.stem(Q["id"], "האם הפונקציה רציפה בנקודה $(0,0)$? נמקו.")
         + W.piecewise("\\frac{x^3y-xy^3}{x^2+y^2}")
         + st.card("e-t", "trap", "⚠️ ״כל הישרים נותנים $0$״ אינו נימוק")
         + st.card("e-c1", "ex", "$|\\cos\\theta|\\le1,\\ \\ |\\sin\\theta|\\le1$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: שני מסלולים עם ערכים שונים מוכיחים שהגבול **אינו** קיים.", do=show("s-1")),
    P("אבל אף מספר של מסלולים לא מוכיח שהוא קיים, גם אם כל הישרים מסכימים.", do=show("s-2")),
    P("כדי להוכיח קיום צריך חסם שתלוי רק ב-$r$ ושואף לאפס.", do=show("s-3"), say="כדי להוכיח קיום צריך חסם שתלוי רק באָר ושואף לאפס."),
    P("ואת זה נלמד לעומק בסרטון הבא, על קואורדינטות קוטביות. נתראה.", do=show("s-4"), hold=0.6),
], stage=W.compare("cr", [("להפיל גבול", "שני מסלולים עם ערכים שונים", "✓ מספיק", True),
                          ("להוכיח שגבול קיים", "חסם שתלוי רק ב-$r$ ושואף ל-$0$", "✓ מספיק", True)], shown=True),
   panel=st.card("s-1", "rule", "🔑 שני ערכים שונים: אין גבול")
         + st.card("s-2", "trap", "⚠️ כל הישרים מסכימים: עדיין לא הוכחה")
         + st.card("s-3", "rule", "🔑 קיום: $|f-L|\\le g(r)\\to0$")
         + st.card("s-4", "ex", "הבא: קואורדינטות קוטביות"))

VIDEO = Video("L03", "limits_diff", "ישרים לא מספיקים", [title, asym, example, prove, exam, recap],
              bank={"24A-A-Q1a": None})
