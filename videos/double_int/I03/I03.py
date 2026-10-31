# -*- coding: utf-8 -*-
"""I03 · חילוף סדר האינטגרציה — video script (build: tools/video/vid.py I03).

Source: courses/double_int/C03.js (lesson + goal). No bank anchor (bank={}): the exam scene uses an ORIGINAL exam-style region, labelled "בסגנון מבחן"
(w_double_int.style_checks / style_plot): int_0^1 int_0^{x^2} f dy dx + int_1^{3/2} int_0^{3-2x} f dy dx
= int_0^1 int_{sqrt y}^{(3-y)/2} f dx dy (a parabola and a line meeting at the interior corner (1,1)). The bank's 25A-B-Q4a was dropped on purpose: it is a text twin of the C08
boss item 23A-C-Q4a. This video swaps each of the two pieces on its own (the skill of this level); I01 read the region,
I05 glues the pieces. Not used on purpose: the C03 quiz items (the triangle y<=x<=1, x^2<=y<=4 with x and
with 1, x<=y<=sqrt(x)).
Every swap is checked with sympy (same integrals of 1, x, y, xy, x^2y in both orders) and every drawn polygon
against the sympy area.
"""
import math
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_double_int as w

x, y = sp.symbols("x y", real=True)

# ---------------------------------------------------------------- example 1: int_0^4 int_{sqrt x}^2 f dy dx
D1 = [("I", 0, 4, sp.sqrt(x), 2)]
S1 = [("II", 0, 2, 0, y**2)]
assert w.same_region(D1, S1)
assert w.integrate(sp.Integer(1), D1) == sp.Rational(8, 3)
assert sp.integrate(2 - sp.sqrt(x), (x, 0, 4)) == sp.Rational(8, 3) and sp.integrate(y**2, (y, 0, 2)) == sp.Rational(8, 3)
assert sp.sqrt(x).subs(x, 4) == 2                                  # the curve meets y = 2 at (4, 2)

E = w.Plot("e", (-0.5, 4.7), (-0.45, 2.6), w=760, h=470, xticks=[(1, "1"), (2, "2"), (3, "3"), (4, "4")],
           yticks=[(1, "1")])
p1 = w.type2(lambda t: 0.0, lambda t: t * t, 0, 2)
assert abs(w.shoelace(p1) - 8 / 3) < 1e-3
E.fill("e-reg", p1, kind="a")
E.fn("e-c", lambda t: math.sqrt(t), 0, 4.5, kind="a")
E.fn("e-t", lambda t: 2.0, -0.3, 4.5, kind="b")
E.label("e-lc", 2.4, 1.05, "y = √x", kind="a")
E.label("e-lc2", 2.4, 0.62, "x = y²", kind="a")
E.label("e-lt", 2.6, 2.12, "y = 2", kind="b")
E.dot("e-v0", 0, 0, "(0,0)", dx=-14, dy=34, anchor="end")
E.dot("e-v1", 4, 2, "(4,2)", dx=16, dy=-14)
E.dot("e-v2", 0, 2, "(0,2)", dx=-14, dy=-14, anchor="end")
E.vstrip("e-sv", 1.5, math.sqrt(1.5), 2)
E.hstrip("e-sh", 1.3, 0, 1.69)

# ---------------------------------------------------------------- example 2: int_1^e int_0^{ln x} f dy dx
D2 = [("I", 1, sp.E, 0, sp.log(x))]
S2 = [("II", 0, 1, sp.exp(y), sp.E)]
assert w.same_region(D2, S2)
assert w.integrate(sp.Integer(1), D2) == 1
assert sp.integrate(sp.E - sp.exp(y), (y, 0, 1)) == 1

F = w.Plot("f", (-0.3, 3.2), (-0.4, 1.45), w=760, h=430, xticks=[(1, "1"), (2, "2"), (math.e, "e")],
           yticks=[(1, "1")])
p2 = w.type1(lambda t: 0.0, lambda t: math.log(t), 1, math.e)
assert abs(w.shoelace(p2) - 1) < 1e-3
F.fill("f-reg", p2, kind="d", hidden=False)
F.fn("f-c", lambda t: math.log(t), 0.75, 3.1, kind="d", hidden=False)
F.curve("f-r", [(math.e, -0.2), (math.e, 1.3)], kind="b", hidden=False)
F.label("f-lc", 1.55, 0.78, "y = ln x", kind="d", hidden=False, anchor="end")
F.label("f-lc2", 1.55, 0.5, "x = eʸ", kind="d", anchor="end")
F.label("f-lr", 2.8, 1.22, "x = e", kind="b", hidden=False)
F.hstrip("f-sh", 0.55, math.exp(0.55), math.e)

# ---------------------------------------------------------------- the exam-style region (original, not from the bank)
A1, A2 = w.style_checks()            # every bound, vertex, branch, area and the one-integral form, asserted
XS = w.style_plot("x3", filled=True)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נחליף סדר אינטגרציה: אותו תחום בדיוק, סרוק מהכיוון השני."),
    P("נלמד מתכון של ארבעה צעדים, נפעיל אותו על שתי דוגמאות, ונבדוק כל חילוף עם שטח."),
    P("ובסוף נחליף סדר בשני החלקים של שאלה בסגנון מבחן.", hold=0.4),
], stage='<div class="kicker">I03 · אינטגרל כפול</div><h1>חילוף סדר האינטגרציה</h1>'
         '<p>להחליף סדר אינטגרציה באינטגרל נשנה: לקרוא את התחום מהגבולות, לשרטט, ולקרוא אותו בכיוון ההפוך.</p>',
   layout="title")

idea = Scene("idea", "המתכון", [
    P("חילוף סדר אומר: האינטגרנד נשאר, התחום נשאר, ורק הגבולות משתנים.", do=show("i-eq")),
    P("למה מותר? משפט פוביני: לפונקציה רציפה על תחום כזה, שני הסדרים נותנים אותו ערך.", do=show("i-fub")),
    P("המתכון: אחת, כותבים את אי-השוויונים של האינטגרל הנתון.", do=show("i-1")),
    P("שתיים, משרטטים את התחום ומסמנים את נקודות החיתוך.", do=show("i-2")),
    P("שלוש, לכל ערך של המשתנה החיצוני **החדש**, קוראים ממה עד מה נע הפנימי.", do=show("i-3")),
    P("וארבע, בודקים עם אינטגרנד אחת שהשטח לא השתנה.", do=show("i-4"), hold=0.4),
], stage='<div class="di-col"><div id="i-eq" class="di-big h">'
         '$\\displaystyle\\int_a^b\\!\\int_{g_1(x)}^{g_2(x)} f\\,dy\\,dx=\\int_c^d\\!\\int_{h_1(y)}^{h_2(y)} f\\,dx\\,dy$'
         '</div><div id="i-fub" class="di-note h">משפט פוביני: אותו תחום, אותו ערך</div></div>',
   panel=st.card("i-1", "ex", "1. אי-השוויונים של הנתון")
         + st.card("i-2", "ex", "2. שרטוט ונקודות חיתוך")
         + st.card("i-3", "ex", "3. פס בכיוון החדש: ממה עד מה")
         + st.card("i-4", "rule", "🔑 4. בדיקה: אותו שטח"))

ex1 = Scene("ex1", "דוגמה ראשונה", [
    P("נתון האינטגרל מאפס עד ארבע, של האינטגרל משורש $x$ עד שתיים, לפי $y$ ואז לפי $x$.", do=show("a-0"),
      say="נתון האינטגרל מאפס עד ארבע, של האינטגרל משורש אִקְס עד שתיים, לפי וַואי ואז לפי אִקְס."),
    P("צעד אחד: $x$ בין אפס לארבע, ו-$y$ בין $\\sqrt{x}$ לשתיים.", do=show("a-1"),
      say="צעד אחד: אִקְס בין אפס לארבע, ווַואי בין שורש אִקְס לשתיים."),
    P("צעד שתיים: משרטטים את העקום, שורש $x$, ואת הישר $y=2$.", do=show("e-c", "e-lc", "e-t", "e-lt"),
      say="צעד שתיים: משרטטים את העקום, שורש אִקְס, ואת הישר וַואי שווה שתיים."),
    P("הם נפגשים ב-$(4,2)$. התחום הוא מה שמעל העקום ומתחת לישר, משמאל לארבע.",
      do=show("e-v0", "e-v1", "e-v2", "e-reg", "e-sv"),
      say="הם נפגשים בנקודה ארבע שתיים. התחום הוא מה שמעל העקום ומתחת לישר, משמאל לארבע."),
    P("צעד שלוש: עכשיו $y$ בחוץ. הוא נע מאפס עד שתיים, ואלה מספרים.", do=hide("e-sv") + show("a-2"),
      say="צעד שלוש: עכשיו וַואי בחוץ. הוא נע מאפס עד שתיים, ואלה מספרים."),
    P("פס אופקי נכנס בציר ה-$y$, כלומר $x=0$.", do=show("e-sh"),
      say="פס אופקי נכנס בציר הוַואי, כלומר אִקְס שווה אפס."),
    P("ויוצא דרך העקום. מבודדים ממנו את $x$: מ-$y=\\sqrt{x}$ מקבלים $x=y^2$.", do=show("e-lc2"),
      say="ויוצא דרך העקום. מבודדים ממנו את אִקְס: מוַואי שווה שורש אִקְס, מקבלים אִקְס שווה וַואי בריבוע."),
    P("אז הסדר החדש: $y$ מאפס עד שתיים, ו-$x$ מאפס עד $y^2$.", do=show("a-3"),
      say="אז הסדר החדש: וַואי מאפס עד שתיים, ואִקְס מאפס עד וַואי בריבוע."),
    P("צעד ארבע: השטח. בסדר הנתון יוצא שמונה שלישים, ובסדר החדש גם שמונה שלישים.", do=show("a-4", "a-ok"),
      hold=0.4),
], stage=f'<div class="di-col">{E.svg()}</div>',
   panel=w.eqs("a", [
       "$\\displaystyle\\int_0^4\\!\\int_{\\sqrt{x}}^{2} f\\,dy\\,dx$",
       "$0\\le x\\le 4,\\ \\ \\sqrt{x}\\le y\\le 2$",
       "$0\\le y\\le 2$",
       "$\\displaystyle=\\int_0^2\\!\\int_{0}^{y^2} f\\,dx\\,dy$",
       "$\\displaystyle\\int_0^4(2-\\sqrt{x})\\,dx=\\int_0^2 y^2\\,dy=\\frac{8}{3}$",
   ], size=36, gap=18) + w.chip("a-ok", "✓ אותו שטח"))

ex2 = Scene("ex2", "דוגמה שנייה", [
    P("עוד אחת: האינטגרל מאחת עד $e$, של האינטגרל מאפס עד לן $x$.", do=show("b-0"),
      say="עוד אחת: האינטגרל מאחת עד אֵי, של האינטגרל מאפס עד לָן אִקְס."),
    P("התחום הוא מתחת לגרף של לן $x$, מעל ציר ה-$x$, בין אחת ל-$e$.",
      say="התחום הוא מתחת לגרף של לָן אִקְס, מעל ציר האִקְס, בין אחת לאֵי."),
    P("הגרף עולה מאפס, בנקודה אחת, ועד אחת, בנקודה $e$. אז בסדר החדש $y$ בין אפס לאחת.", do=show("b-1"),
      say="הגרף עולה מאפס, בנקודה אחת, ועד אחת, בנקודה אֵי. אז בסדר החדש וַואי בין אפס לאחת."),
    P("פס אופקי נכנס דרך הגרף. מבודדים: מ-$y=\\ln x$ יוצא $x=e^y$.", do=show("f-sh", "f-lc2"),
      say="פס אופקי נכנס דרך הגרף. מבודדים: מוַואי שווה לָן אִקְס, יוצא אִקְס שווה אֵי בחזקת וַואי."),
    P("והוא יוצא בישר $x=e$. כלומר $x$ נע מ-$e^y$ עד $e$.", do=show("b-2"),
      say="והוא יוצא בישר אִקְס שווה אֵי. כלומר אִקְס נע מאֵי בחזקת וַואי עד אֵי."),
    P("בדיקה: השטח בסדר החדש הוא $e$ פחות $(e-1)$, כלומר אחת. כמו בסדר הנתון.", do=show("b-3"), hold=0.4,
      say="בדיקה: השטח בסדר החדש הוא אֵי, פחות, בסוגריים, אֵי פחות אחת. כלומר אחת. כמו בסדר הנתון."),
], stage=f'<div class="di-col">{F.svg()}</div>',
   panel=w.eqs("b", [
       "$\\displaystyle\\int_1^e\\!\\int_0^{\\ln\\,x} f\\,dy\\,dx$",
       "$0\\le y\\le 1$",
       "$\\displaystyle=\\int_0^1\\!\\int_{e^y}^{e} f\\,dx\\,dy$",
       "$\\displaystyle\\int_0^1(e-e^y)\\,dy=e-(e-1)=1$",
   ], size=36, gap=20))

trap = Scene("trap", "המלכודת", [
    P("והמלכודת: להחליף רק את האותיות. משאירים את הגבולות ומחליפים $dy\\,dx$ ב-$dx\\,dy$.", do=show("t-bad"),
      say="והמלכודת: להחליף רק את האותיות. משאירים את הגבולות, ומחליפים דִּי וַואי דִּי אִקְס בדִּי אִקְס דִּי וַואי."),
    P("אז הגבול החיצוני הוא שורש $x$, ונשאר בו משתנה. זה סימן בטוח שמשהו נקרא לא נכון.", do=show("t-c1"),
      say="אז הגבול החיצוני הוא שורש אִקְס, ונשאר בו משתנה. זה סימן בטוח שמשהו נקרא לא נכון."),
    P("בסדר החדש גם הגבולות החיצוניים חייבים להיות מספרים, והתחתון קטן מהעליון בכל הטווח.", do=show("t-c2"),
      hold=0.4),
], stage='<div class="di-col"><div id="t-bad" class="di-big h">'
         '$\\displaystyle\\int_{\\sqrt{x}}^{2}\\!\\int_0^4 f\\,dx\\,dy$</div>'
         '<div class="di-chip bad">✗ זה לא חילוף סדר</div></div>',
   panel=st.card("t-c1", "trap", "⚠️ משתנה בגבול החיצוני = קריאה שגויה")
         + st.card("t-c2", "rule", "🔑 חיצוני: מספרים. פנימי: תחתון ≤ עליון"))

exam = Scene("exam", "שאלה בסגנון מבחן", [
    P("שאלה בסגנון מבחן: להחליף סדר בסכום של שני אינטגרלים. את התחום כבר קראנו ברמה הראשונה.", do=show("x-int")),
    P("מחליפים כל חלק בנפרד. החלק הראשון: $x$ בין אפס לאחת, ו-$y$ מאפס עד $x^2$.",
      say="מחליפים כל חלק בנפרד. החלק הראשון: אִקְס בין אפס לאחת, ווַואי מאפס עד אִקְס בריבוע."),
    P("הפרבולה עולה מאפס עד אחת, אז בסדר החדש $y$ בין אפס לאחת.",
      say="הפרבולה עולה מאפס עד אחת, אז בסדר החדש וַואי בין אפס לאחת."),
    P("מבודדים את $x$: מ-$y=x^2$ יוצא $x=\\sqrt{y}$, כי החלק הזה נמצא ב-$x$ חיובי.", do=show("x3-ls2"),
      say="מבודדים את אִקְס: מוַואי שווה אִקְס בריבוע, יוצא אִקְס שווה שורש וַואי, כי החלק הזה נמצא באִקְס חיובי."),
    P("פס אופקי בחלק הזה נכנס בפרבולה, ויוצא בישר $x=1$.", do=show("x3-ha"),
      say="פס אופקי בחלק הזה נכנס בפרבולה, ויוצא בישר אִקְס שווה אחת."),
    P("לכן החלק הראשון הופך ל-$x$ משורש $y$ עד אחת.", do=show("x-0"),
      say="לכן החלק הראשון הופך לאִקְס משורש וַואי עד אחת."),
    P("בדיקה: שטח שליש בשני הסדרים.", do=show("x-c1")),
    P("החלק השני: מתחת לישר $y=3-2x$. הפס האופקי נכנס ב-$x=1$, ויוצא בישר $x=\\tfrac{3-y}{2}$.",
      do=show("x3-hb", "x3-ll2"),
      say="החלק השני: מתחת לישר וַואי שווה שלוש פחות שתיים אִקְס. הפס האופקי נכנס באִקְס שווה אחת, ויוצא בישר אִקְס שווה שלוש פחות וַואי, חלקי שתיים."),
    P("וגם כאן $y$ בין אפס לאחת. השטח רבע, בשני הסדרים.", do=show("x-1", "x-c2"),
      say="וגם כאן וַואי בין אפס לאחת. השטח רבע, בשני הסדרים."),
    P("שני החלקים החדשים חולקים את אותו טווח של $y$, ונוגעים זה בזה ב-$x=1$.", do=show("x-n"),
      say="שני החלקים החדשים חולקים את אותו טווח של וַואי, ונוגעים זה בזה באִקְס שווה אחת."),
    P("איך מדביקים אותם לאינטגרל אחד, נראה בסרטון של רמה חמש.", hold=0.3),
    P("המלכודת: לקחת את כל הפרבולה, $x=\\pm\\sqrt{y}$. החלק כולו ב-$x\\ge0$, ולכן רק $x=\\sqrt{y}$.",
      do=show("x-t"), hold=0.4,
      say="המלכודת: לקחת את כל הפרבולה, אִקְס שווה פלוס מינוס שורש וַואי. החלק כולו באִקְס חיובי, ולכן רק אִקְס שווה שורש וַואי."),
], stage=f'<div class="di-col">{XS}</div>',
   panel=w.stem(w.STYLE_TAG, "החליפו את סדר האינטגרציה באינטגרל")
         + '<div id="x-int" class="h">' + w.eqs("xi", [w.STYLE_SUM_LINE], size=28, shown=1) + '</div>'
         + w.eqs("x", [
             "$\\displaystyle\\int_{0}^{1}\\!\\int_{0}^{x^2}\\!f\\,dy\\,dx=\\int_{0}^{1}\\!\\int_{\\sqrt{y}}^{1}\\!f\\,dx\\,dy$",
             "$\\displaystyle\\int_{1}^{3/2}\\!\\int_{0}^{3-2x}\\!f\\,dy\\,dx=\\int_{0}^{1}\\!\\int_{1}^{(3-y)/2}\\!f\\,dx\\,dy$",
         ], size=30, gap=10)
         + '<div class="di-row"><span id="x-c1" class="di-chip ok h">✓ $\\tfrac{1}{3}$</span>'
           '<span id="x-c2" class="di-chip ok h">✓ $\\tfrac{1}{4}$</span></div>'
         + st.card("x-n", "ex", "אותו $0\\le y\\le 1$, נוגעים ב-$x=1$")
         + st.card("x-t", "trap", "⚠️ $x\\ge0$, ולכן $x=\\sqrt{y}$ (בלי ±)"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: חילוף סדר משנה רק את הגבולות. האינטגרנד והתחום נשארים.", do=show("z-1")),
    P("קוראים את אי-השוויונים, משרטטים, וקוראים פסים בכיוון החדש.", do=show("z-2")),
    P("מבודדים את המשתנה הפנימי החדש מכל עקום, עם הענף הנכון.", do=show("z-3")),
    P("ובודקים שהשטח לא השתנה. נתראה ברמה הבאה.", do=show("z-4"), hold=0.6),
], stage='<div class="di-big">$\\displaystyle\\int_a^b\\!\\int_{g_1(x)}^{g_2(x)} f\\,dy\\,dx'
         '=\\int_c^d\\!\\int_{h_1(y)}^{h_2(y)} f\\,dx\\,dy$</div>',
   panel=st.card("z-1", "rule", "🔑 אותו תחום, גבולות חדשים")
         + st.card("z-2", "rule", "🔑 אי-שוויונים, שרטוט, פס חדש")
         + st.card("z-3", "rule", "🔑 מבודדים, בוחרים ענף")
         + st.card("z-4", "trap", "⚠️ חיצוני: רק מספרים. ובדיקת שטח"))

VIDEO = Video("I03", "double_int", "חילוף סדר האינטגרציה", [title, idea, ex1, ex2, trap, exam, recap],
              bank={})
