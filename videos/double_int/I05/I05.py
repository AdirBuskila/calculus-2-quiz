# -*- coding: utf-8 -*-
"""I05 · תחום שמתפצל לשני חלקים — video script (build: tools/video/vid.py I05).

Source: courses/double_int/C05.js (lesson + goal). No bank anchor (bank={}): the exam scene uses an ORIGINAL exam-style region, labelled "בסגנון מבחן"
(w_double_int.style_checks / style_plot): int_0^1 int_0^{x^2} f dy dx + int_1^{3/2} int_0^{3-2x} f dy dx
= int_0^1 int_{sqrt y}^{(3-y)/2} f dx dy (a parabola and a line meeting at the interior corner (1,1)). The bank's 25A-B-Q4a was dropped on purpose: it is a text twin of the C08
boss item 23A-C-Q4a. Finished here: the sum becomes the single integral (I01 read the region, I03 swapped each piece).
Not used on purpose: the C05 quiz triangles ((-1,0),(1,0),(0,1) and (0,0),(2,0),(1,1)).
Every description is checked with sympy (same integrals of 1, x, y, xy, x^2y), every drawn polygon against the area.
"""
import math
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_double_int as w

x, y = sp.symbols("x y", real=True)

# ---------------------------------------------------------------- example: the triangle (0,0), (1,1), (3,0)
top_r = (3 - x) / 2
assert top_r.subs(x, 1) == 1 and top_r.subs(x, 3) == 0           # the line through (1,1) and (3,0)
assert sp.solve(sp.Eq(x, top_r), x) == [1]                        # the corner: y = x meets it at x = 1
SPLIT = [("I", 0, 1, 0, x), ("I", 1, 3, 0, top_r)]
ONE = [("II", 0, 1, y, 3 - 2*y)]
assert sp.solve(sp.Eq(y, (3 - x) / 2), x) == [3 - 2*y]
assert w.same_region(SPLIT, ONE)
assert w.integrate(sp.Integer(1), SPLIT) == sp.Rational(3, 2)
assert sp.integrate(x, (x, 0, 1)) == sp.Rational(1, 2) and sp.integrate(top_r, (x, 1, 3)) == 1
assert sp.integrate(3 - 3*y, (y, 0, 1)) == sp.Rational(3, 2)

E = w.Plot("e", (-0.4, 3.5), (-0.4, 1.6), w=780, h=430, xticks=[(1, "1"), (2, "2"), (3, "3")], yticks=[(1, "1")])
pa = w.type1(lambda s: 0.0, lambda s: s, 0, 1)
pb = w.type1(lambda s: 0.0, lambda s: (3 - s) / 2, 1, 3)
assert abs(w.shoelace(pa) - 0.5) < 1e-6 and abs(w.shoelace(pb) - 1) < 1e-6
E.fill("e-a", pa, kind="a")
E.fill("e-b", pb, kind="d")
E.fill("e-all", [(0, 0), (3, 0), (1, 1)], kind="b")
E.fn("e-l1", lambda s: s, -0.2, 1.3, kind="a", hidden=False)
E.fn("e-l2", lambda s: (3 - s) / 2, 0.6, 3.3, kind="d", hidden=False)
E.label("e-t1", 0.35, 0.95, "y = x", kind="a", hidden=False, anchor="end")
E.label("e-t2", 2.1, 0.9, "y = (3−x)/2", kind="d", hidden=False)
E.label("e-t1b", 0.35, 0.72, "x = y", kind="a", anchor="end")
E.label("e-t2b", 2.1, 0.62, "x = 3 − 2y", kind="d")
E.dot("e-v", 1, 1, "(1,1)", dx=0, dy=-20, anchor="middle", kind="b", hidden=False)
E.curve("e-cut", [(1, -0.2), (1, 1.4)], kind="ink", dash=True)
E.vstrip("e-s1", 0.6, 0, 0.6)
E.vstrip("e-s2", 2.0, 0, 0.5)
E.hstrip("e-h", 0.45, 0.45, 2.1)

# the tilted square of level 2 (corners on all four sides): split in both orders
SQV = [("I", 0, 1, 1 - x, 1 + x), ("I", 1, 2, x - 1, 3 - x)]
SQH = [("II", 0, 1, 1 - y, 1 + y), ("II", 1, 2, y - 1, 3 - y)]
assert w.same_region(SQV, SQH) and w.integrate(sp.Integer(1), SQV) == 2
T = w.Plot("sq", (-0.4, 2.6), (-0.4, 2.6), w=520, h=520, xticks=[], yticks=[])
T.fill("sq-r", [(0, 1), (1, 0), (2, 1), (1, 2)], kind="d", hidden=False)
T.curve("sq-cv", [(1, -0.25), (1, 2.3)], kind="b", dash=True)
T.curve("sq-ch", [(-0.25, 1), (2.3, 1)], kind="c", dash=True)
for nm, (px, py) in {"a": (0, 1), "b": (1, 0), "c": (2, 1), "d": (1, 2)}.items():
    T.dot(f"sq-{nm}", px, py, hidden=False, kind="b")

# ---------------------------------------------------------------- the exam-style region (original, not from the bank)
A1, A2 = w.style_checks()            # every bound, vertex, branch, area and the one-integral form, asserted
XS = w.style_plot("x5", filled=True)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("לפעמים סדר אחד דורש שני אינטגרלים, והסדר ההפוך רק אחד."),
    P("בסרטון הזה נבין מתי זה קורה, ונלמד לאחד סכום של שני אינטגרלים לאינטגרל אחד."),
    P("ובסוף נסיים את השאלה בסגנון מבחן, שקראנו והפכנו בסרטונים הקודמים.", hold=0.4),
], stage='<div class="kicker">I05 · אינטגרל כפול</div><h1>תחום שמתפצל לשני חלקים</h1>'
         '<p>לזהות מתי סדר אינטגרציה מחייב שני אינטגרלים, ולאחד סכום של שני אינטגרלים לאינטגרל אחד בסדר ההפוך.</p>',
   layout="title")

idea = Scene("idea", "מתי מתפצל", [
    P("כל פס נכנס בעקום אחד ויוצא בעקום אחר. כל עוד אלה אותם עקומים, נוסחה אחת מספיקה."),
    P("אבל אם באמצע הדרך הגבול העליון, או התחתון, מחליף נוסחה, צריך לחתוך שם.", do=show("i-c1")),
    P("וזה קורה בדיוק ב**פינה** של הגבול: נקודה שבה עקום אחד נגמר ועקום אחר מתחיל.", do=show("i-c2")),
    P("לכן כדי לאחד סכום של שני אינטגרלים, יש מתכון.", do=show("i-0")),
    P("כותבים את שני התחומים ומשרטטים, מוצאים את נקודת המפגש,", do=show("i-1")),
    P("וקוראים את כל התחום בכיוון ההפוך. ובסוף בודקים את השטח.", do=show("i-2"), hold=0.4),
], stage='<div class="di-col">' + st.card("i-0", "ex", "1. שני התחומים על שרטוט אחד")
         + st.card("i-1", "ex", "2. נקודת המפגש של החלקים")
         + st.card("i-2", "rule", "🔑 3. פס בכיוון ההפוך על כל התחום, ובדיקת שטח") + '</div>',
   panel=st.card("i-c1", "rule", "🔑 גבול שמחליף נוסחה = חותכים שם")
         + st.card("i-c2", "ex", "פינה בגבול העליון או התחתון = עוד אינטגרל"))

ex = Scene("ex", "דוגמה", [
    P("דוגמה: המשולש עם הקודקודים אפס אפס, אחת אחת, ושלוש אפס."),
    P("בפסים אנכיים: משמאל ל-$x=1$ הפס יוצא בישר $y=x$, ומימין לו בישר השני.", do=show("e-s1", "e-s2", "e-cut"),
      say="בפסים אנכיים: משמאל לאִקְס שווה אחת, הפס יוצא בישר וַואי שווה אִקְס, ומימין לו בישר השני."),
    P("הגבול העליון מחליף נוסחה בפינה אחת אחת. לכן שני אינטגרלים.", do=show("e-a", "e-b", "a-0")),
    P("ועכשיו בפסים אופקיים: לכל $y$ בין אפס לאחת, הפס נכנס בישר $x=y$.",
      do=hide("e-s1", "e-s2", "e-cut", "e-a", "e-b") + show("e-h", "e-t1b", "e-all"),
      say="ועכשיו בפסים אופקיים: לכל וַואי בין אפס לאחת, הפס נכנס בישר אִקְס שווה וַואי."),
    P("ויוצא בישר השני, אחרי שמבודדים ממנו את $x$: $x=3-2y$.", do=show("e-t2b"),
      say="ויוצא בישר השני, אחרי שמבודדים ממנו את אִקְס: אִקְס שווה שלוש פחות שתיים וַואי."),
    P("משמאל תמיד אותו ישר, ומימין תמיד אותו ישר. אין פינה בצדדים, אז מספיק אינטגרל **אחד**.", do=show("a-1")),
    P("בדיקת שטח: בפיצול חצי ועוד אחת, ובאינטגרל האחד גם שלושה חצאים.", do=show("a-2", "a-ok"), hold=0.4),
], stage=f'<div class="di-col">{E.svg()}</div>',
   panel=w.eqs("a", [
       "$\\displaystyle\\int_0^1\\!\\int_0^{x}\\!f\\,dy\\,dx+\\int_1^3\\!\\int_0^{\\frac{3-x}{2}}\\!f\\,dy\\,dx$",
       "$\\displaystyle=\\int_0^1\\!\\int_{y}^{3-2y}\\!f\\,dx\\,dy$",
       "$\\dfrac12+1=\\displaystyle\\int_0^1(3-3y)\\,dy=\\dfrac32$",
   ], size=32, gap=26) + w.chip("a-ok", "✓ אותו שטח"))

trap = Scene("trap", "המלכודת", [
    P("ומה אם גם בכיוון ההפוך יצאו שני חלקים?"),
    P("קודם בודקים שהתחום נקרא נכון: פינה בצדדים מופיעה בשרטוט, לא בניחוש.", do=show("t-c1")),
    P("ויש תחומים שמתפצלים באמת בשני הכיוונים. למשל הריבוע המסובב של רמה שתיים.", do=show("t-sq")),
    P("יש לו פינה למטה ולמעלה, אז פסים אנכיים נחתכים ב-$x=1$.", do=show("sq-cv"),
      say="יש לו פינה למטה ולמעלה, אז פסים אנכיים נחתכים באִקְס שווה אחת."),
    P("ויש לו פינה משמאל ומימין, אז גם פסים אופקיים נחתכים, ב-$y=1$.", do=show("sq-ch"),
      say="ויש לו פינה משמאל ומימין, אז גם פסים אופקיים נחתכים, בוַואי שווה אחת."),
    P("לתחום כזה אין סדר עם אינטגרל אחד. שם עוברים למשתנים אחרים, ברמה שבע.", do=show("t-c2"), hold=0.4),
], stage=f'<div class="di-col"><div id="t-sq" class="h">{T.svg()}</div></div>',
   panel=st.card("t-c1", "trap", "⚠️ שוב שני חלקים? בדקו את השרטוט")
         + st.card("t-c2", "ex", "פינות בכל הכיוונים: משתנים חדשים (רמה 7)"))

exam = Scene("exam", "שאלה בסגנון מבחן", [
    P("ועכשיו השאלה בסגנון מבחן: להחליף סדר בסכום של שני האינטגרלים.", do=show("x-int")),
    P("צעד אחד: שני התחומים. מתחת לפרבולה $y=x^2$, ומתחת לישר $y=3-2x$.",
      say="צעד אחד: שני התחומים. מתחת לפרבולה וַואי שווה אִקְס בריבוע, ומתחת לישר וַואי שווה שלוש פחות שתיים אִקְס."),
    P("צעד שתיים: הם נפגשים ב-$(1,1)$, כי שני הגבולות העליונים שווים שם אחת.", do=show("x-c1"),
      say="צעד שתיים: הם נפגשים בנקודה אחת אחת, כי שני הגבולות העליונים שווים שם אחת."),
    P("ובדיוק שם הגבול העליון מחליף נוסחה. זו הפינה שבגללה היו שני אינטגרלים."),
    P("צעד שלוש: פסים אופקיים על כל התחום. $y$ בין אפס לאחת.",
      do=hide("x5-ra", "x5-rb") + show("x5-all", "x5-h0", "x5-h1", "x5-h2", "x5-ls2", "x5-ll2"),
      say="צעד שלוש: פסים אופקיים על כל התחום. וַואי בין אפס לאחת."),
    P("כל פס נכנס בפרבולה, $x=\\sqrt{y}$, ויוצא בישר, $x=\\tfrac{3-y}{2}$. בכל גובה, אותם שני עקומים.", do=show("x-1"),
      say="כל פס נכנס בפרבולה, אִקְס שווה שורש וַואי, ויוצא בישר, אִקְס שווה שלוש פחות וַואי, חלקי שתיים. בכל גובה, אותם שני עקומים."),
    P("לכן התשובה היא אינטגרל אחד: $y$ מאפס עד אחת, ו-$x$ משורש $y$ עד $\\tfrac{3-y}{2}$.", do=show("x-ok"),
      say="לכן התשובה היא אינטגרל אחד: וַואי מאפס עד אחת, ואִקְס משורש וַואי, עד שלוש פחות וַואי, חלקי שתיים."),
    P("בדיקה: האינטגרל של אורך הפס נותן שבע שתים-עשרה. בדיוק שליש ועוד רבע, כמו בסכום.", do=show("x-2"),
      say="בדיקה: האינטגרל של אורך הפס נותן שבע חלקי שתים עשרה. בדיוק שליש ועוד רבע, כמו בסכום."),
    P("המלכודת: לכתוב שני אינטגרלים גם בסדר החדש. בסדר האופקי אין פינה בצדדים, ולכן אין סיבה לחתוך.",
      do=show("x-t"), hold=0.4),
], stage=f'<div class="di-col">{XS}</div>',
   panel=w.stem(w.STYLE_TAG, "החליפו את סדר האינטגרציה באינטגרל")
         + '<div id="x-int" class="h">' + w.eqs("xi", [w.STYLE_SUM_LINE], size=28, shown=1) + '</div>'
         + st.card("x-c1", "ex", "נפגשים ב-$(1,1)$: שם הפינה")
         + w.eqs("x", [
             "",
             "$\\displaystyle=\\int_{0}^{1}\\!\\int_{\\sqrt{y}}^{(3-y)/2}\\!f\\,dx\\,dy$",
             "$\\displaystyle\\int_0^1\\left(\\frac{3-y}{2}-\\sqrt{y}\\right)dy=\\frac{7}{12}=\\frac13+\\frac14$",
         ], size=32, gap=12)
         + w.chip("x-ok", "✓ אינטגרל אחד")
         + st.card("x-t", "trap", "⚠️ אין פינה בצדדים: לא חותכים"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: פינה בגבול העליון או התחתון של הפס מחייבת לחתוך לשני אינטגרלים.", do=show("z-1")),
    P("כדי לאחד: שרטוט אחד לשני החלקים, נקודת המפגש, ופס בכיוון ההפוך על כל התחום.", do=show("z-2")),
    P("אם בכיוון ההפוך אין פינה, יוצא אינטגרל אחד.", do=show("z-3")),
    P("ותמיד בודקים שהשטח לא השתנה. נתראה ברמה הבאה.", do=show("z-4"), hold=0.6),
], stage='<div class="di-big">$\\displaystyle\\int\\!\\!\\int\\ +\\ \\int\\!\\!\\int\\ =\\ \\int\\!\\!\\int$</div>',
   panel=st.card("z-1", "rule", "🔑 פינה בגבול הפס: חותכים")
         + st.card("z-2", "rule", "🔑 שרטוט, מפגש, פס הפוך")
         + st.card("z-3", "rule", "🔑 בלי פינה: אינטגרל אחד")
         + st.card("z-4", "trap", "⚠️ בדיקת שטח"))

VIDEO = Video("I05", "double_int", "תחום שמתפצל לשני חלקים", [title, idea, ex, trap, exam, recap],
              bank={})
