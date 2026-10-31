# -*- coding: utf-8 -*-
"""I01 · קוראים תחום מהגבולות — video script (build: tools/video/vid.py I01).

Source: courses/double_int/C01.js (lesson + goal). No bank anchor (bank={}): the exam scene uses an ORIGINAL exam-style region, labelled "בסגנון מבחן"
(w_double_int.style_checks / style_plot): int_0^1 int_0^{x^2} f dy dx + int_1^{3/2} int_0^{3-2x} f dy dx
= int_0^1 int_{sqrt y}^{(3-y)/2} f dx dy (a parabola and a line meeting at the interior corner (1,1)). The bank's 25A-B-Q4a was dropped on purpose: it is a text twin of the C08
boss item 23A-C-Q4a. This video does the first step: reading the region from the bounds (two pieces, the meeting point
(1,1), the vertices) and the area 1/3 + 1/4 = 7/12 in the given order; I03 swaps each piece, I05 merges.
Not used on purpose: the C01 quiz items (x^2<=y<=x, 0<=y<=x<=2, xy on a rectangle, the (x+y) bug hunt).
Every bound, vertex, area and integral below is asserted with sympy; every drawn region is checked by its polygon
area against the sympy area.
"""
import math
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_double_int as w

x, y = sp.symbols("x y", real=True)

# ---------------------------------------------------------------- example: int_0^1 int_{x^2}^1 2x dy dx
lo1, hi1 = x**2, sp.Integer(1)
inner1 = sp.integrate(2*x, (y, lo1, hi1))
assert sp.expand(inner1 - (2*x - 2*x**3)) == 0
val1 = sp.integrate(inner1, (x, 0, 1))
assert val1 == sp.Rational(1, 2)
area1 = sp.integrate(hi1 - lo1, (x, 0, 1))
assert area1 == sp.Rational(2, 3)
# vertices: the boundary curves y=x^2, y=1, x=0 meet pairwise at (0,0), (1,1), (0,1) (x>=0 branch)
assert sp.solve([y - x**2, x], [x, y], dict=True) == [{x: 0, y: 0}]
assert {(s[x], s[y]) for s in sp.solve([y - x**2, y - 1], [x, y], dict=True) if s[x] >= 0} == {(1, 1)}
# the strip at x = 1/2 runs from y = 1/4 to y = 1
assert lo1.subs(x, sp.Rational(1, 2)) == sp.Rational(1, 4)

E1 = w.Plot("e1", (-0.25, 1.45), (-0.25, 1.4), w=560, h=540, xticks=[], yticks=[])
poly1 = w.type1(lambda t: t * t, lambda t: 1.0, 0, 1)
assert abs(w.shoelace(poly1) - float(area1)) < 1e-3
E1.fn("e1-par", lambda t: t * t, -0.05, 1.18, kind="a")
E1.fn("e1-top", lambda t: 1.0, -0.15, 1.3, kind="b")
E1.curve("e1-ax0", [(0, -0.2), (0, 1.3)], kind="c")
E1.label("e1-lpar", 1.05, 0.62, "y = x²", kind="a")
E1.label("e1-ltop", 1.2, 1.08, "y = 1", kind="b")
E1.label("e1-lax0", 0.05, 1.3, "x = 0", kind="c")
E1.fill("e1-reg", poly1, kind="a")
E1.dot("e1-v1", 0, 0, "(0,0)", dx=14, dy=34)
E1.dot("e1-v2", 1, 1, "(1,1)", dx=14, dy=34)
E1.dot("e1-v3", 0, 1, "(0,1)", dx=-14, dy=-16, anchor="end")
E1.vstrip("e1-s", 0.5, 0.25, 1.0)

# ---------------------------------------------------------------- the exam-style region (original, not from the bank)
A1, A2 = w.style_checks()            # every bound, vertex, branch, area and the one-integral form, asserted
XS = w.style_plot("x1")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לקרוא תחום מתוך הגבולות של אינטגרל נשנה."),
    P("נכתוב את אי-השוויונים, נשרטט, נמצא קודקודים, ונחשב."),
    P("ובסוף נקרא את התחום של שאלה בסגנון מבחן.", hold=0.4),
], stage='<div class="kicker">I01 · אינטגרל כפול</div><h1>קוראים תחום מהגבולות</h1>'
         '<p>לקרוא מהגבולות של אינטגרל נשנה איזה תחום מדובר, לשרטט אותו, ולחשב אינטגרל נשנה פשוט.</p>',
   layout="title")

idea = Scene("idea", "הרעיון", [
    P("אינטגרל כפול סוכם את הערכים של פונקציה על תחום במישור.", do=show("i-f")),
    P("מחשבים אותו כ**אינטגרל נשנה**: קודם האינטגרל הפנימי, ואז החיצוני על התוצאה.", do=show("i-in", "i-out")),
    P("כאן הפנימי הוא לפי $y$, והחיצוני לפי $x$.",
      say="כאן הפנימי הוא לפי וַואי, והחיצוני לפי אִקְס."),
    P("הגבולות של החיצוני הם **מספרים**: $a$ ו-$b$.", do=show("i-c1"),
      say="הגבולות של החיצוני הם מספרים: אֵיי ובִּי."),
    P("הגבולות של הפנימי יכולים להיות פונקציות, אבל רק של המשתנה החיצוני.", do=show("i-c2")),
    P("וכל זוג גבולות הוא בעצם אי-שוויון. ביחד, אי-השוויונים האלה **הם** התחום.", do=show("i-c3"), hold=0.4),
], stage='<div class="di-col">'
         '<div id="i-f" class="di-big h">$\\iint_R f\\,dA$</div>'
         '<div class="di-big">$\\displaystyle\\int_a^b\\!\\left(\\int_{g_1(x)}^{g_2(x)} f(x,y)\\,dy\\right)dx$</div>'
         '<div class="di-row"><div id="i-in" class="di-chip ok h">פנימי: לפי $y$</div>'
         '<div id="i-out" class="di-chip warn h">חיצוני: לפי $x$</div></div></div>',
   panel=st.card("i-c1", "rule", "🔑 גבולות חיצוניים: <b>קבועים</b>")
         + st.card("i-c2", "rule", "🔑 גבולות פנימיים: פונקציות של המשתנה <b>החיצוני</b> בלבד")
         + st.card("i-c3", "ex", "$a\\le x\\le b,\\ \\ g_1(x)\\le y\\le g_2(x)$"))

read = Scene("read", "קוראים ומשרטטים", [
    P("ניקח את האינטגרל מאפס עד אחת, של האינטגרל מ-$x^2$ עד אחת, של $2x$.", do=show("r-int"),
      say="ניקח את האינטגרל מאפס עד אחת, של האינטגרל מאִקְס בריבוע עד אחת, של שתיים אִקְס."),
    P("שלב ראשון: כותבים את אי-השוויונים. החיצוני נותן $0\\le x\\le 1$.", do=show("r-q1"),
      say="שלב ראשון: כותבים את אי-השוויונים. החיצוני נותן: אִקְס בין אפס לאחת."),
    P("והפנימי נותן $x^2\\le y\\le 1$.", do=show("r-q2"),
      say="והפנימי נותן: וַואי בין אִקְס בריבוע לאחת."),
    P("שלב שני: מציירים כל עקום גבול. הפרבולה $y=x^2$,", do=show("e1-par", "e1-lpar"),
      say="שלב שני: מציירים כל עקום גבול. הפרבולה, וַואי שווה אִקְס בריבוע,"),
    P("הישר $y=1$,", do=show("e1-top", "e1-ltop"), say="הישר וַואי שווה אחת,"),
    P("וגם $x=0$, שמגיע מהגבול התחתון של $x$: זה ציר ה-$y$.", do=show("e1-ax0", "e1-lax0"),
      say="וגם אִקְס שווה אפס, שמגיע מהגבול התחתון של אִקְס: זה ציר הוַואי."),
    P("שלב שלישי: הקודקודים, כלומר נקודות החיתוך של זוגות העקומים.", do=show("e1-v1"), hold=0.2),
    P("הפרבולה פוגשת את הישר $y=1$ ב-$(1,1)$, וציר ה-$y$ פוגש אותו ב-$(0,1)$.", do=show("e1-v2", "e1-v3"),
      say="הפרבולה פוגשת את הישר וַואי שווה אחת בנקודה אחת אחת, וציר הוַואי פוגש אותו בנקודה אפס אחת."),
    P("שלב רביעי: מצלילים את מה שהעקומים סוגרים. זה התחום שמעל הפרבולה ומתחת לישר.", do=show("e1-reg")),
    P("ובדיקה עם פס אנכי: ב-$x$ קבוע, הפס נכנס דרך הפרבולה ויוצא דרך הישר.", do=show("e1-s", "r-key"),
      say="ובדיקה עם פס אנכי: באִקְס קבוע, הפס נכנס דרך הפרבולה ויוצא דרך הישר."),
    P("בדיוק מה שהגבולות הפנימיים אמרו: מ-$x^2$ ועד אחת.", hold=0.4,
      say="בדיוק מה שהגבולות הפנימיים אמרו: מאִקְס בריבוע ועד אחת."),
], stage=f'<div class="di-col">{E1.svg()}</div>',
   panel='<div id="r-int" class="di-big h">$\\displaystyle\\int_0^1\\!\\int_{x^2}^{1} 2x\\,dy\\,dx$</div>'
         + st.card("r-q1", "ex", "חיצוני: $0\\le x\\le 1$")
         + st.card("r-q2", "ex", "פנימי: $x^2\\le y\\le 1$")
         + '<div id="r-key" class="di-key h"><i class="in"></i>כניסה = גבול תחתון<i class="out"></i>יציאה = גבול עליון</div>')

calc = Scene("calc", "מחשבים", [
    P("עכשיו מחשבים. מתחילים בפנימי, לפי $y$. בתוכו $x$ הוא קבוע.", do=show("c-0"),
      say="עכשיו מחשבים. מתחילים בפנימי, לפי וַואי. בתוכו אִקְס הוא קבוע."),
    P("לכן $2x$ פשוט כופל את אורך הפס: אחת פחות $x^2$.", do=show("c-1"),
      say="לכן שתיים אִקְס פשוט כופל את אורך הפס: אחת פחות אִקְס בריבוע."),
    P("פותחים סוגריים ומקבלים $2x-2x^3$. נשאר רק $x$, כמו שצריך.", do=show("c-2"),
      say="פותחים סוגריים ומקבלים שתיים אִקְס פחות שתיים אִקְס בשלישית. נשאר רק אִקְס, כמו שצריך."),
    P("את זה מכניסים לאינטגרל החיצוני, מאפס עד אחת.", do=show("c-3")),
    P("הפונקציה הקדומה היא $x^2-\\tfrac{x^4}{2}$, ומציבים אחת ואפס.", do=show("c-4"),
      say="הפונקציה הקדומה היא אִקְס בריבוע פחות אִקְס ברביעית חלקי שתיים, ומציבים אחת ואפס."),
    P("התוצאה: חצי.", do=show("c-ok"), hold=0.4),
    P("שימו לב: אחרי הפנימי לא נשאר $y$, ואחרי החיצוני לא נשאר אף משתנה. יצא מספר.", do=show("c-r1"),
      say="שימו לב: אחרי הפנימי לא נשאר וַואי, ואחרי החיצוני לא נשאר אף משתנה. יצא מספר."),
    P("ואם האינטגרנד היה אחת, היינו מקבלים את השטח של התחום, שני שלישים.", do=show("c-r2"), hold=0.4),
], stage=w.eqs("c", [
    "$\\displaystyle\\int_{x^2}^{1} 2x\\,dy$",
    "$=2x\\,(1-x^2)$",
    "$=2x-2x^3$",
    "$\\displaystyle\\int_0^1 (2x-2x^3)\\,dx$",
    "$=\\left(1-\\dfrac{1}{2}\\right)-\\left(0-0\\right)$",
], size=44, gap=18) + w.chip("c-ok", "$=\\dfrac12$"),
   panel=st.card("c-r1", "rule", "🔑 הפנימי מחזיר פונקציה של המשתנה החיצוני; החיצוני מחזיר מספר")
         + st.card("c-r2", "ex", "אינטגרנד $1$ נותן שטח: $\\int_0^1(1-x^2)\\,dx=\\tfrac23$"))

trap = Scene("trap", "המלכודת", [
    P("ומה אסור? גבול חיצוני שתלוי במשתנה.", do=show("t-bad")),
    P("כאן הגבול העליון של האינטגרל החיצוני הוא $x^2$, אבל החיצוני הוא בעצמו לפי $x$.", do=show("t-x"),
      say="כאן הגבול העליון של האינטגרל החיצוני הוא אִקְס בריבוע, אבל החיצוני הוא בעצמו לפי אִקְס."),
    P("אחרי שמבצעים אותו, לא נשאר שום $x$ שאפשר להציב בגבול. הכתיבה פשוט חסרת משמעות.", do=show("t-c1"),
      say="אחרי שמבצעים אותו, לא נשאר שום אִקְס שאפשר להציב בגבול. הכתיבה פשוט חסרת משמעות."),
    P("והכלל הנכון: החיצוני בין מספרים, והפנימי תלוי רק במשתנה החיצוני.", do=show("t-good", "t-c2"), hold=0.4),
], stage='<div class="di-col">'
         '<div id="t-bad" class="di-big h">$\\displaystyle\\int_0^{x^2}\\!\\int_0^{x} f\\,dy\\,dx$</div>'
         '<div id="t-x" class="di-chip bad h">✗ גבול חיצוני שתלוי ב-$x$</div>'
         '<div id="t-good" class="di-big h">$\\displaystyle\\int_0^{1}\\!\\int_{x^2}^{x} f\\,dy\\,dx$</div></div>',
   panel=st.card("t-c1", "trap", "⚠️ גבול חיצוני עם משתנה: שגיאה, לא תחום")
         + st.card("t-c2", "rule", "🔑 חיצוני: מספרים. פנימי: רק המשתנה החיצוני"))

exam = Scene("exam", "שאלה בסגנון מבחן", [
    P("שאלה בסגנון מבחן: מבקשים להחליף סדר בסכום של שני אינטגרלים.", do=show("x-int")),
    P("את החילוף נלמד בהמשך. אבל הצעד הראשון בכל שאלה כזאת הוא אותו צעד: לקרוא את התחום."),
    P("החלק הראשון: $x$ בין אפס לאחת, ו-$y$ מאפס עד $x^2$.", do=show("x1-cs", "x1-ls", "x-q", "x-q1"),
      say="החלק הראשון: אִקְס בין אפס לאחת, ווַואי מאפס עד אִקְס בריבוע."),
    P("כלומר מתחת לפרבולה ומעל ציר ה-$x$. כאן הפרבולה היא הגבול **העליון**.", do=show("x1-v1", "x1-ra", "x1-sa"),
      say="כלומר מתחת לפרבולה ומעל ציר האִקְס. כאן הפרבולה היא הגבול העליון."),
    P("החלק השני: $x$ בין אחת לשלושה חצאים, ו-$y$ מאפס עד הישר $3-2x$.", do=show("x1-cl", "x1-ll", "x-q2"),
      say="החלק השני: אִקְס בין אחת לאחת וחצי, ווַואי מאפס עד הישר שלוש פחות שתיים אִקְס."),
    P("הישר יורד ופוגש את ציר ה-$x$ בנקודה שלושה חצאים, אפס.", do=show("x1-v2", "x1-rb", "x1-sb"),
      say="הישר יורד ופוגש את ציר האִקְס בנקודה אחת וחצי, אפס."),
    P("ואיפה החלקים נפגשים? ב-$x=1$ שני הגבולות העליונים שווים אחת.", do=show("x1-v3", "x-m"),
      say="ואיפה החלקים נפגשים? באִקְס שווה אחת, שני הגבולות העליונים שווים אחת."),
    P("כלומר זה תחום **אחד**, עם שלושה קודקודים: אפס אפס, שלושה חצאים אפס, ואחת אחת.", hold=0.3,
      say="כלומר זה תחום אחד, עם שלושה קודקודים: אפס אפס, אחת וחצי אפס, ואחת אחת."),
    P("בדיקת שטח בסדר הנתון: החלק הראשון נותן שליש, והשני נותן רבע.", do=show("x-a")),
    P("ביחד שבע שתים-עשרה. כל סדר אחר שנכתוב לאותו תחום חייב לתת את אותו שטח.",
      say="ביחד שבע חלקי שתים עשרה. כל סדר אחר שנכתוב לאותו תחום חייב לתת את אותו שטח."),
    P("המלכודת: לקרוא את הפרבולה כגבול התחתון. הגבולות אומרים: $y$ מאפס, כלומר מציר ה-$x$, ועד $x^2$.",
      do=show("x-t"), hold=0.4,
      say="המלכודת: לקרוא את הפרבולה כגבול התחתון. הגבולות אומרים: וַואי מאפס, כלומר מציר האִקְס, ועד אִקְס בריבוע."),
], stage=f'<div class="di-col">{XS}'
         '<div id="x-a" class="di-mid h">$\\tfrac{1}{3}+\\tfrac{1}{4}=\\tfrac{7}{12}$</div></div>',
   panel=w.stem(w.STYLE_TAG, "החליפו את סדר האינטגרציה באינטגרל")
         + '<div id="x-int" class="h">' + w.eqs("xi", w.STYLE_SUM, size=34, gap=4, shown=2) + '</div>'
         + st.card("x-q", "ex", '<span id="x-q1" class="h">$0\\le x\\le 1,\\ \\ 0\\le y\\le x^2$</span><br>'
                   '<span id="x-q2" class="h">$1\\le x\\le \\tfrac32,\\ \\ 0\\le y\\le 3-2x$</span>')
         + st.card("x-m", "rule", "🔑 נפגשים ב-$(1,1)$: תחום אחד")
         + st.card("x-t", "trap", "⚠️ $y=x^2$ הוא הגבול <b>העליון</b> של החלק"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: הגבולות הם אי-שוויונים, והם התחום.", do=show("z-1")),
    P("משרטטים כל עקום גבול, מוצאים את נקודות החיתוך, ומצלילים.", do=show("z-2")),
    P("מחשבים מבפנים החוצה: הפנימי מחזיר פונקציה של החיצוני, והחיצוני מחזיר מספר.", do=show("z-3")),
    P("וגבול חיצוני שתלוי במשתנה הוא שגיאה. נתראה ברמה הבאה.", do=show("z-4"), hold=0.6),
], stage='<div class="di-big">$\\displaystyle\\int_a^b\\!\\int_{g_1(x)}^{g_2(x)} f\\,dy\\,dx$</div>',
   panel=st.card("z-1", "rule", "🔑 גבולות = אי-שוויונים = התחום")
         + st.card("z-2", "rule", "🔑 עקומים, קודקודים, הצללה")
         + st.card("z-3", "rule", "🔑 קודם הפנימי, אחר כך החיצוני")
         + st.card("z-4", "trap", "⚠️ חיצוני: רק מספרים"))

VIDEO = Video("I01", "double_int", "קוראים תחום מהגבולות", [title, idea, read, calc, trap, exam, recap],
              bank={})
