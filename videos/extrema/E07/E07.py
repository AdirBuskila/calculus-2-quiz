# -*- coding: utf-8 -*-
"""E07 · כופלי לגראנז': אילוץ אחד — video script (build: tools/video/vid.py E07).

Source: courses/extrema/C07.js (lesson + goal). Exam anchor: 23A-A-Q4b (absolute extrema of 1-x^2-y^2 on the disk
(x-1)^2+(y-1)^2 <= 1): the interior has no candidate ((0,0) is outside), and the whole answer is one Lagrange
system on the circle, with the case λ=-1 ruled out by a contradiction. Max -2+2√2, min -2-2√2. (The same exam part
was set again as 22A-B-Q4b, which E06 solves by a parametrization; the video says the question appeared twice.)
Not used on purpose: the C07 quiz functions (xy on x^2+y^2=2 = 24A-A-Q4b / 25A-B-Q1b, x+2y on x^2+y^2=5,
x^2+y^2 on x+y=2) and the lesson's x+y on the unit circle. Worked example (own): 3x+4y on x^2+y^2=25.
Every Lagrange solution is computed with sympy (w_extrema.lagrange) and asserted; the parallel-gradient picture
is drawn from the same numbers.
"""
from vid import P, Scene, Video, show, hide, BANK
import math
import sympy as sp
import stage as st
import w_extrema as w
from w_extrema import X, Y, LAM

# ---------------------------------------------------------------- example: 3x + 4y on x^2 + y^2 = 25
F0, G0 = 3 * X + 4 * Y, X**2 + Y**2
SOL0 = w.lagrange(F0, G0, 25)
assert [(s[0], s[1]) for s in SOL0] == [(-3, -4), (3, 4)]
assert [s[2] for s in SOL0] == [sp.Rational(-1, 2), sp.Rational(1, 2)]
assert w.val(F0, (3, 4)) == 25 and w.val(F0, (-3, -4)) == -25
# at (5, 0) the gradients are not parallel: (3,4) vs (10,0)
assert 3 * 0 - 4 * 10 != 0


def unit(vx, vy, k):
    n = math.hypot(vx, vy)
    return k * vx / n, k * vy / n


# ---------------------------------------------------------------- exam 23A-A-Q4b
Q = BANK["23A-A-Q4b"]
assert "1-x^2-y^2" in Q["question"].replace(" ", "") and "(x-1)^2+(y-1)^2\\le1" in Q["question"].replace(" ", "")
assert BANK["22A-B-Q4b"]["question"] == Q["question"]                  # the same part, set twice
F = 1 - X**2 - Y**2
G = (X - 1)**2 + (Y - 1)**2
assert w.crit(F) == [(0, 0)] and G.subs({X: 0, Y: 0}) == 2             # (0,0) is outside the disk
# -2x = λ·2(x-1)  <=>  x(1+λ) = λ ;  same for y
assert w.same(sp.expand(-2 * X - LAM * sp.diff(G, X)), -2 * (X * (1 + LAM) - LAM))
assert w.same(sp.expand(-2 * Y - LAM * sp.diff(G, Y)), -2 * (Y * (1 + LAM) - LAM))
assert (X * (1 + LAM) - LAM).subs(LAM, -1) == 1                        # λ = -1 would give 0 = -1 (no solution)
r2 = sp.sqrt(2)
SOL = w.lagrange(F, G, 1)
assert [(s[0], s[1]) for s in SOL] == [(1 - r2 / 2, 1 - r2 / 2), (1 + r2 / 2, 1 + r2 / 2)]
assert all(s[0] == s[1] and s[2] != -1 for s in SOL)
assert w.same(w.val(F, SOL[0][:2]), -2 + 2 * r2) and w.same(w.val(F, SOL[1][:2]), -2 - 2 * r2)

# ---------------------------------------------------------------- pictures
pts = [(3, 4), (-3, -4), (5, 0)]
ARR = []
for nm, (px, py) in zip(["a", "b", "c"], pts):
    ARR.append((f"f{nm}", px, py, *unit(3, 4, 2.4), "gf"))
    ARR.append((f"g{nm}", px, py, *unit(2 * px, 2 * py, 2.4), "gg"))
C0 = w.contour("c0", F0, (-7.5, 7.5), (-7.5, 7.5), w=520, n=13, ticks=False,
               curves=[(lambda s: 5 * math.cos(s), lambda s: 5 * math.sin(s), 0, 2 * math.pi)], arrows=ARR, points=[
                   dict(name="a", x=3, y=4, label="(3,4)", role="max", dx=-14, dy=-12, anchor="end"),
                   dict(name="b", x=-3, y=-4, label="(−3,−4)", role="min", dx=14, dy=30),
                   dict(name="c", x=5, y=0, label="(5,0)", role="cand", dx=12, dy=34)])
h = 1 / math.sqrt(2)
XA = []
for nm, (px, py) in zip(["p", "q"], [(1 - h, 1 - h), (1 + h, 1 + h)]):
    XA.append((f"f{nm}", px, py, *unit(-2 * px, -2 * py, 0.8), "gf"))
    XA.append((f"g{nm}", px, py, *unit(2 * (px - 1), 2 * (py - 1), 0.8), "gg"))
def dplot(pfx, shown=()):
    return w.contour(pfx, F, (-1.1, 2.6), (-1.1, 2.6), w=480, shown=shown, n=14, region=("disk", 1, 1, 1),
               curves=[(lambda s: 1 + math.cos(s), lambda s: 1 + math.sin(s), 0, 2 * math.pi)], arrows=XA, points=[
                   dict(name="o", x=0, y=0, label="(0,0)", role="out", dx=-12, dy=30, anchor="end"),
                   dict(name="p", x=1 - h, y=1 - h, label="M₂", role="max", dx=16, dy=30),
                   dict(name="q", x=1 + h, y=1 + h, label="M₁", role="min", dx=14, dy=-12)])


CX = dplot("cx")
CY = dplot("cy", shown=("p-o", "p-p", "p-q", "cv-0"))
LEG = ('<div class="lgd"><span><i style="background:#2dd4bf"></i>$\\nabla f$</span>'
       '<span><i style="background:#f0abfc"></i>$\\nabla g$</span></div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("עד עכשיו הפכנו את השפה לפונקציה של משתנה אחד. היום שיטה אחרת: כופלי לגראנז'."),
    P("נבין למה בנקודת קיצון על עקום הגרדיאנטים מקבילים, ונכתוב מזה מערכת משוואות."),
    P("ובסוף שאלת מבחן שבה כל התשובה היא מערכת לגראנז' אחת.", hold=0.4),
], stage='<div class="kicker">E07 · אקסטרמום</div><h1>כופלי לגראנז\': אילוץ אחד</h1>'
         r'<p>לכתוב ולפתור את $\nabla f=\lambda\nabla g$, ולהבין למה הגרדיאנטים מקבילים.</p>', layout="title")

idea = Scene("idea", "למה מקבילים", [
    P("הבעיה: קיצון של $f$, אבל רק על עקום $g=c$. כאן $f=3x+4y$, והעקום הוא מעגל ברדיוס חמש.", do=show("c0-cv-0"),
      say="הבעיה: קיצון של אֶף, אבל רק על עקום גִ'י שווה סִי. כאן אֶף שווה שלוש אִקְס ועוד ארבע וַואי, והעקום הוא מעגל ברדיוס חמש."),
    P("קווי הגובה של $f$ הם ישרים. ‏$\\nabla f$ ניצב להם, ומצביע לכיוון שבו $f$ עולה.", do=show("c0-p-c", "c0-a-fc"),
      say="קווי הגובה של אֶף הם ישרים. הגרדיאנט של אֶף ניצב להם, ומצביע לכיוון שבו אֶף עולה."),
    P("ו-$\\nabla g$ ניצב למעגל עצמו.", do=show("c0-a-gc"), say="והגרדיאנט של גִ'י ניצב למעגל עצמו."),
    P("בנקודה $(5,0)$ החצים לא מקבילים. אז אפשר לזוז על המעגל ולהגדיל את $f$: זה לא קיצון.", do=show("i-1"),
      say="בנקודה חמש, אפס, החצים לא מקבילים. אז אפשר לזוז על המעגל ולהגדיל את אֶף: זה לא קיצון."),
    P("קיצון יכול להיות רק במקום שבו קו הגובה **משיק** למעגל.", do=hide("c0-p-c", "c0-a-fc", "c0-a-gc"),
      say="קיצון יכול להיות רק במקום שבו קו הגובה משיק למעגל."),
    P("ושם שני הניצבים על אותו קו: $\\nabla f=\\lambda\\nabla g$.",
      do=show("c0-p-a", "c0-a-fa", "c0-a-ga", "c0-p-b", "c0-a-fb", "c0-a-gb", "i-2"),
      say="ושם שני הניצבים על אותו קו: הגרדיאנט של אֶף שווה למדא כפול הגרדיאנט של גִ'י."),
    P("למדא הוא רק מספר שמותח או הופך את החץ. הוא עזר, ובסוף זורקים אותו.", hold=0.4),
], stage=f'<div class="xcol">{C0}{LEG}</div>',
   panel=st.card("i-1", "trap", "⚠️ חצים לא מקבילים: אפשר להמשיך לטפס על העקום")
         + st.card("i-2", "rule", r"🔑 בקיצון: קו הגובה משיק לעקום, ולכן $\nabla f=\lambda\nabla g$"))

L1 = w.lines("e1", [r"$f_x=\lambda g_x,\quad f_y=\lambda g_y,\quad g=c$",
                    r"$3=2\lambda x,\qquad 4=2\lambda y$",
                    r"$\lambda\ne0:\quad y=\tfrac43x$",
                    r"$x^2+\tfrac{16}{9}x^2=25\ \Rightarrow\ x=\pm3$",
                    r"$f(3,4)=25,\qquad f({-3},{-4})=-25$"], cls="sm")
system = Scene("system", "המערכת", [
    P("המערכת: שתי משוואות מהגרדיאנטים, ועוד משוואת האילוץ. שלוש משוואות, שלושה נעלמים.", do=show("e1-0", "s-1")),
    P("בדוגמה: $3=2\\lambda x$ ו-$4=2\\lambda y$.", do=show("e1-1"),
      say="בדוגמה: שלוש שווה שתיים למדא אִקְס, וארבע שווה שתיים למדא וַואי."),
    P("למדא לא יכול להיות אפס, אחרת שלוש שווה אפס. אז מותר לחלק בו, ומקבלים $y$ שווה ארבע שלישים $x$.",
      do=show("e1-2"),
      say="למדא לא יכול להיות אפס, אחרת שלוש שווה אפס. אז מותר לחלק בו, ומקבלים וַואי שווה ארבע שלישים אִקְס."),
    P("מציבים באילוץ, ומקבלים $x$ שווה שלוש או מינוס שלוש.", do=show("e1-3"),
      say="מציבים באילוץ, ומקבלים אִקְס שווה שלוש או מינוס שלוש."),
    P("שתי נקודות: $(3,4)$ עם הערך עשרים וחמש, ו-$({-3},{-4})$ עם מינוס עשרים וחמש.", do=show("e1-4"),
      say="שתי נקודות: שלוש, ארבע, עם הערך עשרים וחמש, ומינוס שלוש, מינוס ארבע, עם מינוס עשרים וחמש."),
    P("המעגל סגור וחסום, אז יש מקסימום ומינימום, והם בין המועמדים: עשרים וחמש, ומינוס עשרים וחמש.", do=show("s-2")),
    P("זהירות: על עקום לא חסום, כמו ישר, ייתכן שרק אחד מהם קיים.", do=show("s-3"), hold=0.4),
], stage=L1,
   panel=st.card("s-1", "rule", r"🔑 $\nabla f=\lambda\nabla g$ ועוד $g=c$")
         + st.card("s-2", "ex", "עקום סגור וחסום: הגדול והקטן מבין הפתרונות")
         + st.card("s-3", "trap", "⚠️ עקום לא חסום: לבדוק בנפרד"))

QSTEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>מצאו אקסטרמומים מוחלטים של $f(x,y)=1-x^2-y^2$ '
         r'בתחום $(x-1)^2+(y-1)^2\le1$.</div>')
LX = w.lines("x1", [r"$(0,0):\ \ (0-1)^2+(0-1)^2=2>1$",
                    r"$-2x=2\lambda(x-1),\quad -2y=2\lambda(y-1)$",
                    r"$x(1+\lambda)=\lambda,\qquad y(1+\lambda)=\lambda$",
                    r"$\lambda=-1:\ \ 0=-1$",
                    r"$x=y=\tfrac{\lambda}{1+\lambda}\ \Rightarrow\ x=y$",
                    r"$2(x-1)^2=1\ \Rightarrow\ x=1\pm\tfrac{1}{\sqrt2}$"], cls="sm")
exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה שהופיעה בשני מבחנים שונים: אחת פחות $x^2$ פחות $y^2$, בדיסק שמרכזו $(1,1)$.",
      say="שאלה שהופיעה בשני מבחנים שונים: אחת פחות אִקְס בריבוע פחות וַואי בריבוע, בדיסק שמרכזו אחת, אחת."),
    P("פנים: הנקודה הקריטית היחידה היא הראשית, והיא מחוץ לדיסק. אז הכול על המעגל.", do=show("x1-0", "cx-p-o")),
    P("על המעגל, לגראנז'. הנגזרות של $f$: מינוס $2x$ ומינוס $2y$. של האילוץ: $2(x-1)$ ו-$2(y-1)$.",
      do=show("x1-1"),
      say="על המעגל, לגראנז'. הנגזרות של אֶף: מינוס שתיים אִקְס ומינוס שתיים וַואי. של האילוץ: שתיים כפול אִקְס פחות אחת, ושתיים כפול וַואי פחות אחת."),
    P("מסדרים: $x$ כפול אחת ועוד למדא, שווה למדא. ואותו דבר עם $y$.", do=show("x1-2"),
      say="מסדרים: אִקְס כפול אחת ועוד למדא, שווה למדא. ואותו דבר עם וַואי."),
    P("לפני שמחלקים באחת ועוד למדא, בודקים מתי הוא אפס: למדא מינוס אחת נותן אפס שווה מינוס אחת. סתירה.",
      do=show("x1-3", "x-c")),
    P("אז מותר לחלק, ו-$x$ ו-$y$ שווים לאותו ביטוי. כלומר $x=y$.", do=show("x1-4"),
      say="אז מותר לחלק, ואִקְס ווַואי שווים לאותו ביטוי. כלומר אִקְס שווה וַואי."),
    P("מציבים באילוץ: אחת ועוד או פחות אחת חלקי שורש שתיים. שתי נקודות על האלכסון.",
      do=show("x1-5", "cx-p-p", "cx-p-q"), hold=0.4),
], stage=f'<div class="xrow"><div style="width:540px">{LX}</div>{CX}</div>',
   panel=QSTEM + st.card("x-c", "trap", r"⚠️ לפני חילוק ב-$1+\lambda$: בודקים את $\lambda=-1$ בנפרד"))

exam2 = Scene("exam2", "התשובה", [
    P("בשתי הנקודות החצים באמת על אותו קו: האלכסון שעובר דרך הראשית ודרך מרכז המעגל.",
      do=show("cy-a-fp", "cy-a-gp", "cy-a-fq", "cy-a-gq")),
    P("בנקודה הקרובה לראשית, $f$ שווה מינוס שתיים ועוד שני שורש שתיים. זה המקסימום.", do=show("v-1"),
      say="בנקודה הקרובה לראשית, אֶף שווה מינוס שתיים ועוד שני שורש שתיים. זה המקסימום."),
    P("ובנקודה הרחוקה, מינוס שתיים פחות שני שורש שתיים. זה המינימום.", do=show("v-2")),
    P("המעגל סגור וחסום, ואין מועמדים בפנים. לכן אלה הקיצונים המוחלטים של כל הדיסק.", do=show("v-3")),
    P("ואם כבר פתרתם את זה בפרמטריזציה, קיבלתם בדיוק את אותן שתי נקודות. שתי דרכים, תשובה אחת.", hold=0.5),
], stage=f'<div class="xcol">{CY}{LEG}</div>',
   panel=QSTEM + st.card("v-1", "ex", r"$M_2=\left(1-\tfrac1{\sqrt2},1-\tfrac1{\sqrt2}\right)$: מקסימום $-2+2\sqrt2$")
         + st.card("v-2", "ex", r"$M_1=\left(1+\tfrac1{\sqrt2},1+\tfrac1{\sqrt2}\right)$: מינימום $-2-2\sqrt2$")
         + st.card("v-3", "rule", "🔑 פנים ריק + מעגל סגור: אלה הקיצונים המוחלטים"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: בקיצון על עקום, קו הגובה משיק לעקום, ולכן הגרדיאנטים מקבילים.", do=show("r-1")),
    P("כותבים שתי משוואות מהגרדיאנטים, ומוסיפים את האילוץ עצמו.", do=show("r-2")),
    P("לפני שמחלקים בביטוי, בודקים בנפרד מתי הוא אפס.", do=show("r-3")),
    P("ובסוף משווים את ערכי $f$ בכל הפתרונות. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6,
      say="ובסוף משווים את ערכי אֶף בכל הפתרונות. נתראה ברמה הבאה."),
], stage=r'<div class="xbig">$\nabla f=\lambda\,\nabla g,\qquad g=c$</div>',
   panel=st.card("r-1", "rule", "🔑 משיק ⇐ גרדיאנטים מקבילים")
         + st.card("r-2", "rule", "🔑 שלוש משוואות: שתיים + האילוץ")
         + st.card("r-3", "trap", "⚠️ חילוק רק אחרי בדיקת האפס")
         + st.card("r-4", "ex", r"$\lambda$ הוא עזר: זורקים אותו בסוף"))

VIDEO = Video("E07", "extrema", "כופלי לגראנז': אילוץ אחד", [title, idea, system, exam, exam2, recap],
              bank={"23A-A-Q4b": None})
