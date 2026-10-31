# -*- coding: utf-8 -*-
"""E05 · תחום מצולע: צלעות וקודקודים — video script (build: tools/video/vid.py E05).

Source: courses/extrema/C05.js (lesson + goal). Exam anchors: 24B-B-Q3d (min and max of x^2-2x(y+1)+3 on
D = {-2 <= y <= x <= 1}, a triangle) and its part c, 24B-B-Q3c (the critical point (0,-1) and its type), which no
guided quiz uses. Max 6 and min 0 both sit at vertices, which no derivative finds: the level's trap.
Not used on purpose: the C05 quiz/lesson functions on the triangle (0,0),(4,0),(0,4) (x^2+xy+y^2-6x, x^2-xy+y^2-3x)
and the boss part 24S-A-Q3b. Warm-up example (own): xy on the triangle (0,0),(2,0),(0,2).
Everything is computed with sympy; the absolute max/min are re-checked on a dense grid of the triangle.
"""
from vid import P, Scene, Video, show, hide, BANK
import numpy as np
import sympy as sp
import stage as st
import w_extrema as w
from w_extrema import X, Y

# ---------------------------------------------------------------- warm-up: xy on the triangle (0,0),(2,0),(0,2)
F0 = X * Y
assert w.crit(F0) == [(0, 0)]                                  # a vertex, not an interior point
H0 = sp.expand(F0.subs(Y, 2 - X))
assert H0 == 2 * X - X**2 and sp.solve(sp.diff(H0, X), X) == [1] and H0.subs(X, 1) == 1
assert F0.subs(Y, 0) == 0 and F0.subs(X, 0) == 0
assert [w.val(F0, v) for v in [(0, 0), (2, 0), (0, 2)]] == [0, 0, 0]

# ---------------------------------------------------------------- exam 24B-B-Q3c/d
Qc, Qd = BANK["24B-B-Q3c"], BANK["24B-B-Q3d"]
assert "x^2-2x(y+1)+3" in Qc["question"].replace(" ", "") and "-2\\le y\\le x\\le1" in Qd["question"]
F = X**2 - 2 * X * (Y + 1) + 3
A_, B_, C_ = (1, 1), (1, -2), (-2, -2)                         # y = x & x = 1, y = -2 & x = 1, y = -2 & y = x
assert w.crit(F) == [(0, -1)] and -2 <= -1 <= 0 <= 1           # the critical point is inside D
assert w.hess(F, (0, -1)) == (2, -2, 0, -4) and w.kind(2, -2, 0) == "saddle" and w.val(F, (0, -1)) == 3
EAB = sp.expand(F.subs(X, 1))                                  # x = 1, -2 <= y <= 1
EBC = sp.expand(F.subs(Y, -2))                                 # y = -2, -2 <= x <= 1
EAC = sp.expand(F.subs(Y, X))                                  # y = x, -2 <= x <= 1
assert EAB == 2 - 2 * Y and EBC == X**2 + 2 * X + 3 and EAC == -X**2 - 2 * X + 3
assert sp.solve(sp.diff(EBC, X), X) == [-1] and EBC.subs(X, -1) == 2
assert sp.solve(sp.diff(EAC, X), X) == [-1] and EAC.subs(X, -1) == 4
VALS = {(0, -1): 3, (-1, -2): 2, (-1, -1): 4, A_: 0, B_: 6, C_: 3}
assert all(w.val(F, p) == v for p, v in VALS.items())
xx, yy = np.meshgrid(np.linspace(-2, 1, 601), np.linspace(-2, 1, 601))
inside = (yy <= xx + 1e-12)
ZZ = (xx**2 - 2 * xx * (yy + 1) + 3)[inside]
assert abs(ZZ.max() - 6) < 1e-9 and abs(ZZ.min() - 0) < 1e-9

# ---------------------------------------------------------------- pictures
C0 = w.contour("c0", F0, (-0.4, 2.4), (-0.4, 2.4), w=470, n=13, region=("poly", [(0, 0), (2, 0), (0, 2)]),
               segs=[((2, 0), (0, 2), "")], points=[
                   dict(name="o", x=0, y=0, label="(0,0)", role="cand", dx=-10, dy=30, anchor="end"),
                   dict(name="a", x=2, y=0, label="(2,0)", role="cand", dy=32),
                   dict(name="b", x=0, y=2, label="(0,2)", role="cand", dx=-12, anchor="end"),
                   dict(name="m", x=1, y=1, label="(1,1)", role="max", dx=14, dy=-12)])


def tri(pfx, shown=(), wd=500):
    return w.contour(pfx, F, (-2.9, 1.8), (-2.7, 1.6), w=wd, n=16, region=("poly", [A_, B_, C_]),
                     segs=[(A_, B_, ""), (B_, C_, ""), (C_, A_, "")], shown=shown, points=[
                         dict(name="A", x=1, y=1, label="A(1,1)", role="cand", dx=14, dy=-10),
                         dict(name="B", x=1, y=-2, label="B(1,−2)", role="cand", dx=14, dy=26),
                         dict(name="C", x=-2, y=-2, label="C(−2,−2)", role="cand", dx=-4, dy=36, anchor="start"),
                         dict(name="s", x=0, y=-1, label="(0,−1)", role="saddle", dx=14, dy=-12, anchor="start"),
                         dict(name="d", x=-1, y=-2, label="(−1,−2)", role="cand", dx=0, dy=-18, anchor="middle"),
                         dict(name="e", x=-1, y=-1, label="(−1,−1)", role="cand", dx=-16, dy=-6, anchor="end")])


TX = tri("tx")
TY = tri("ty", shown=("p-A", "p-B", "p-C", "p-s"), wd=440)
TZ = tri("tz", shown=("p-A", "p-B", "p-C", "p-s", "p-d", "p-e"), wd=420)
CT = w.ctable("ct", [("(0,{-1})", "פנים", "3"), ("({-1},{-2})", r"צלע $BC$", "2"), ("({-1},{-1})", r"צלע $AC$", "4"),
                     ("A(1,1)", "קודקוד", "0"), ("B(1,{-2})", "קודקוד", "6"), ("C({-2},{-2})", "קודקוד", "3")],
              mx=4, mn=3)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("כשהתחום הוא משולש או מצולע, השפה בנויה מכמה קטעים ישרים."),
    P("בסרטון הזה נלמד לטפל בכל צלע לחוד, ונראה למה הקודקודים הם המועמדים הכי חשובים."),
    P("ובסוף שאלת מבחן שבה גם המקסימום וגם המינימום יושבים בקודקודים.", hold=0.4),
], stage='<div class="kicker">E05 · אקסטרמום</div><h1>תחום מצולע: צלעות וקודקודים</h1>'
         '<p>לפרמטר כל צלע, למצוא בה נקודות קריטיות, ולא לשכוח את הקודקודים.</p>', layout="title")

recipe = Scene("recipe", "המתכון", [
    P("המתכון למצולע: פנים, כל צלע בנפרד, הקודקודים, ובסוף טבלה.", do=show("m-1")),
    P("דוגמה קצרה: $xy$ במשולש שקודקודיו בראשית, ב-$(2,0)$ וב-$(0,2)$.",
      say="דוגמה קצרה: אִקְס וַואי במשולש שקודקודיו בראשית, בשתיים, אפס, ובאפס, שתיים."),
    P("הנקודה הקריטית היחידה היא הראשית, והיא קודקוד. אז בפנים אין כלום.", do=show("c0-p-o")),
    P("על שני הניצבים אחד המשתנים אפס, ולכן $f=0$ לכל אורכם.",
      say="על שני הניצבים אחד המשתנים אפס, ולכן אֶף שווה אפס לכל אורכם."),
    P("על היתר מציבים $y=2-x$, ו-$x$ רץ מאפס עד שתיים. מקבלים $g=2x-x^2$.", do=show("c0-ln-0", "mm-0"),
      say="על היתר מציבים וַואי שווה שתיים פחות אִקְס, ואִקְס רץ מאפס עד שתיים. מקבלים גִ'י שווה שתיים אִקְס פחות אִקְס בריבוע."),
    P("הנגזרת מתאפסת ב-$x=1$, בתוך הקטע. זו הנקודה $(1,1)$, וערכה אחת.", do=show("c0-p-m"),
      say="הנגזרת מתאפסת באִקְס שווה אחת, בתוך הקטע. זו הנקודה אחת, אחת, וערכה אחת."),
    P("ובקודקודים: אפס בכולם. אז המקסימום אחת, והמינימום אפס.", do=show("c0-p-a", "c0-p-b", "mm-1"), hold=0.4),
    P("שימו לב: את הקטע של הצלע קובעים שני הקודקודים שלה, כולל אותם.", do=show("m-t")),
], stage=C0,
   panel=st.card("m-1", "rule", "🔑 פנים ⟵ כל צלע ⟵ קודקודים ⟵ טבלה")
         + w.lines("mm", [r"$y=2-x,\ \ 0\le x\le2:\ \ g=2x-x^2$", r"$f(0,0)=f(2,0)=f(0,2)=0$"], cls="sm")
         + st.card("m-t", "trap", "⚠️ קטע הצלע: מקודקוד לקודקוד, כולל הקצוות"))

QSTEM = (f'<div class="qstem"><span class="qid">{Qd["id"]}</span>נתונה $f(x,y)=x^2-2x(y+1)+3$. '
         r'מצאו את הערך המינימלי והמקסימלי של $f$ בתחום $D=\{-2\le y\le x\le1\}$.</div>')
LA = w.lines("x1", [r"$-2\le y\le x\le 1$", r"$A(1,1),\ \ B(1,{-2}),\ \ C({-2},{-2})$",
                    r"$f_x=2x-2y-2=0$", r"$f_y=-2x=0$",
                    r"$(0,{-1})\in D,\quad f(0,{-1})=3$"], cls="sm")
exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: הערך הגדול והקטן של הפונקציה בתחום שעל המסך."),
    P("קודם מפענחים את התחום. שלושה אי-שוויונים: $y$ לפחות מינוס שתיים, $y$ לכל היותר $x$, ו-$x$ לכל היותר אחת.",
      do=show("x1-0"),
      say="קודם מפענחים את התחום. שלושה אי שוויונים: וַואי לפחות מינוס שתיים, וַואי לכל היותר אִקְס, ואִקְס לכל היותר אחת."),
    P("שלושה ישרים, ולכן משולש. הקודקודים הם החיתוכים של כל זוג ישרים.", do=show("x1-1", "tx-p-A", "tx-p-B", "tx-p-C")),
    P("משולש סגור וחסום, ופולינום רציף. לכן הקיצון קיים."),
    P("פנים: $f_y=-2x$, ולכן $x=0$. ומ-$f_x=0$ מקבלים $y=-1$.", do=show("x1-2", "x1-3"),
      say="פנים: אֶף וַואי שווה מינוס שתיים אִקְס, ולכן אִקְס שווה אפס. ומאֶף אִקְס שווה אפס מקבלים וַואי שווה מינוס אחת."),
    P("האם $(0,{-1})$ בתוך המשולש? מציבים: מינוס שתיים, מינוס אחת, אפס, אחת. סדר עולה, אז כן.",
      do=show("x1-4", "tx-p-s"),
      say="האם אפס, מינוס אחת, בתוך המשולש? מציבים: מינוס שתיים, מינוס אחת, אפס, אחת. סדר עולה, אז כן."),
    P("בסעיף הקודם במבחן סיווגו אותה: $\\Delta=-4$, נקודת אוכף. ובכל זאת נכניס את ערכה, שלוש, לטבלה.", hold=0.4,
      say="בסעיף הקודם במבחן סיווגו אותה: דֶּלְתָא שווה מינוס ארבע, נקודת אוכף. ובכל זאת נכניס את ערכה, שלוש, לטבלה."),
], stage=f'<div class="xrow"><div style="width:470px">{LA}</div>{TX}</div>',
   panel=QSTEM + st.card("x-c", "ex", r"סעיף ג׳ (24B-B-Q3c): $(0,{-1})$ עם $A=2,\ B=-2,\ C=0$: אוכף")
   .replace('class="card ex h"', 'class="card ex"'))

LB = w.lines("x2", [
    r"$AB:\ x=1,\ \ {-2}\le y\le1$", r"$f=2-2y$",
    r"$BC:\ y={-2},\ \ {-2}\le x\le1$", r"$f=x^2+2x+3$",
    r"$x={-1}:\ \ f({-1},{-2})=2$",
    r"$AC:\ y=x,\ \ {-2}\le x\le1$", r"$f=-x^2-2x+3$",
    r"$x={-1}:\ \ f({-1},{-1})=4$",
], cls="sm")
exam2 = Scene("exam2", "שלוש צלעות", [
    P("עכשיו כל צלע לחוד. הצלע $AB$: ‏$x=1$, ו-$y$ רץ ממינוס שתיים עד אחת.", do=show("ty-ln-0"),
      say="עכשיו כל צלע לחוד. הצלע אֵיי בִּי: אִקְס שווה אחת, ווַואי רץ ממינוס שתיים עד אחת."),
    P("מציבים, ומקבלים פונקציה לינארית: $2-2y$. אין לה נקודה קריטית, ולכן רק הקצוות.", do=show("x2-0", "x2-1"),
      say="מציבים, ומקבלים פונקציה לינארית: שתיים פחות שתיים וַואי. אין לה נקודה קריטית, ולכן רק הקצוות."),
    P("הצלע $BC$: ‏$y=-2$. מקבלים $x^2+2x+3$, והנגזרת מתאפסת ב-$x=-1$.", do=show("ty-ln-1", "x2-2", "x2-3"),
      say="הצלע בִּי סִי: וַואי שווה מינוס שתיים. מקבלים אִקְס בריבוע ועוד שתיים אִקְס ועוד שלוש, "
          "והנגזרת מתאפסת באִקְס שווה מינוס אחת."),
    P("מינוס אחת בתוך הקטע, אז הנקודה $({-1},{-2})$ נכנסת, עם הערך שתיים.", do=show("x2-4", "ty-p-d"),
      say="מינוס אחת בתוך הקטע, אז הנקודה מינוס אחת, מינוס שתיים, נכנסת, עם הערך שתיים."),
    P("והיתר $AC$: ‏$y=x$. מקבלים מינוס $x^2$, פחות $2x$, ועוד שלוש.", do=show("ty-ln-2", "x2-5", "x2-6"),
      say="והיתר אֵיי סִי: וַואי שווה אִקְס. מקבלים מינוס אִקְס בריבוע, פחות שתיים אִקְס, ועוד שלוש."),
    P("שוב הנגזרת מתאפסת ב-$x=-1$. הנקודה $({-1},{-1})$, עם הערך ארבע.", do=show("x2-7", "ty-p-e"), hold=0.4,
      say="שוב הנגזרת מתאפסת באִקְס שווה מינוס אחת. הנקודה מינוס אחת, מינוס אחת, עם הערך ארבע."),
], stage=f'<div class="xrow"><div style="width:500px">{LB}</div>{TY}</div>',
   panel=QSTEM + st.card("x-k", "rule", "🔑 בכל צלע: הצבה, קטע סגור, $g'=0$ בתוך הקטע")
   .replace('class="card rule h"', 'class="card rule"'))

exam3 = Scene("exam3", "הטבלה", [
    P("עכשיו הטבלה. הנקודה מהפנים: שלוש. ושתי הנקודות מהצלעות: שתיים וארבע.", do=show("ct-r0", "ct-r1", "ct-r2")),
    P("ועכשיו הקודקודים. ב-$A$ הערך אפס.", do=show("ct-r3"), say="ועכשיו הקודקודים. באֵיי הערך אפס."),
    P("ב-$B$ הערך שש, וב-$C$ הערך שלוש.", do=show("ct-r4", "ct-r5"), say="בבִּי הערך שש, ובסִי הערך שלוש."),
    P("המקסימום הוא שש, בקודקוד $B$. והמינימום הוא אפס, בקודקוד $A$.", do=show("ct-mx", "ct-mn"),
      say="המקסימום הוא שש, בקודקוד בִּי. והמינימום הוא אפס, בקודקוד אֵיי."),
    P("שתי התשובות בקודקודים, ובאף אחד מהם הנגזרת לא מתאפסת. מי שדילג על הקודקודים, טעה בשתיהן.",
      do=show("x-t"), hold=0.5),
], stage=f'<div class="xrow">{TZ}{CT}</div>',
   panel=QSTEM + st.card("x-t", "trap", "⚠️ בלי הקודקודים: מקסימום 4 ומינימום 2. שתי התשובות שגויות"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: במצולע, כל צלע היא קטע סגור במשתנה אחד.", do=show("r-1")),
    P("את הקטע קובעים שני הקודקודים, ופתרון של הנגזרת מחוץ לקטע נפסל.", do=show("r-2")),
    P("הקודקודים נבדקים תמיד, כי שם הנגזרת של הצלע לא מוצאת כלום.", do=show("r-3")),
    P("ובסוף טבלה אחת. נתראה ברמה הבאה, עם תחום עגול.", do=show("r-4"), hold=0.6),
], stage='<div class="xbig" style="font-size:44px;direction:rtl">פנים ← צלעות ← קודקודים ← טבלה</div>',
   panel=st.card("r-1", "rule", "🔑 צלע = הצבה של משוואת הישר")
         + st.card("r-2", "ex", "הקטע: בין שני הקודקודים, כולל")
         + st.card("r-3", "trap", "⚠️ קודקודים תמיד בטבלה")
         + st.card("r-4", "ex", "הגדול והקטן מכל המועמדים"))

VIDEO = Video("E05", "extrema", "תחום מצולע: צלעות וקודקודים", [title, recipe, exam, exam2, exam3, recap],
              bank={"24B-B-Q3d": None, "24B-B-Q3c": None})
