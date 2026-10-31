# -*- coding: utf-8 -*-
"""E06 · תחום עגול: פנים ומעגל — video script (build: tools/video/vid.py E06).

Source: courses/extrema/C06.js (lesson + goal). Exam anchor: 22A-B-Q4b (absolute extrema of 1-x^2-y^2 on the disk
(x-1)^2+(y-1)^2 <= 1), an open part that no guided quiz uses: the only critical point (0,0) lies outside the disk,
and on the circle x=1+cos t, y=1+sin t gives -2-2(cos t+sin t), whose derivative vanishes at t=π/4 and t=5π/4.
Max -2+2√2, min -2-2√2. (The same exam part appears again as 23A-A-Q4b; E07 solves that one with Lagrange.)
Not used on purpose: the C06 quiz functions (2x^2+y^2 on x^2+y^2<=4, x^2+3y^2 on the unit disk), the lesson's
x^4-2x^2+y^2, and the boss parts 22A-A-Q4b / 26A-A-Q4b. Worked example (own): x^2+y^2+2x on x^2+y^2<=4, where the
circle gives g(x)=4+2x: no critical point at all, only the endpoints.
Everything is computed with sympy and re-checked on a dense grid of the disk.
"""
from vid import P, Scene, Video, show, hide, BANK
import math
import numpy as np
import sympy as sp
import stage as st
import w_extrema as w
from w_extrema import X, Y, T

# ---------------------------------------------------------------- example: x^2 + y^2 + 2x on x^2 + y^2 <= 4
F0 = X**2 + Y**2 + 2 * X
assert w.crit(F0) == [(-1, 0)] and (-1)**2 + 0**2 < 4 and w.val(F0, (-1, 0)) == -1
G0 = sp.expand(F0.subs(Y**2, 4 - X**2))
assert G0 == 2 * X + 4 and sp.solve(sp.diff(G0, X), X) == []          # g' = 2: never zero
assert G0.subs(X, -2) == 0 and G0.subs(X, 2) == 8
xx, yy = np.meshgrid(np.linspace(-2, 2, 801), np.linspace(-2, 2, 801))
m = xx**2 + yy**2 <= 4
Z0 = (xx**2 + yy**2 + 2 * xx)[m]
assert abs(Z0.max() - 8) < 1e-9 and abs(Z0.min() + 1) < 1e-9

# ---------------------------------------------------------------- exam 22A-B-Q4b
Q = BANK["22A-B-Q4b"]
assert "1-x^2-y^2" in Q["question"].replace(" ", "") and "(x-1)^2+(y-1)^2\\le1" in Q["question"].replace(" ", "")
F = 1 - X**2 - Y**2
assert w.crit(F) == [(0, 0)] and (0 - 1)**2 + (0 - 1)**2 == 2 > 1          # outside the disk
FT = sp.expand(F.subs({X: 1 + sp.cos(T), Y: 1 + sp.sin(T)}))
assert w.same(sp.trigsimp(FT), -2 - 2 * sp.cos(T) - 2 * sp.sin(T))
DT = sp.diff(-2 - 2 * sp.cos(T) - 2 * sp.sin(T), T)
assert w.same(DT, 2 * sp.sin(T) - 2 * sp.cos(T))
ROOTS = sp.solveset(DT, T, sp.Interval.Ropen(0, 2 * sp.pi))
assert ROOTS == sp.FiniteSet(sp.pi / 4, 5 * sp.pi / 4)
r2 = sp.sqrt(2)
P1 = (1 + 1 / r2, 1 + 1 / r2)        # t = π/4
P2 = (1 - 1 / r2, 1 - 1 / r2)        # t = 5π/4
assert w.same(w.val(F, P1), -2 - 2 * r2) and w.same(w.val(F, P2), -2 + 2 * r2)
assert w.same(FT.subs(T, 0), -4)                                     # t = 0 (= 2π): just a point in between
th = np.linspace(0, 1, 401)
rr, tt = np.meshgrid(np.linspace(0, 1, 401), np.linspace(0, 2 * math.pi, 801))
ZZ = 1 - (1 + rr * np.cos(tt))**2 - (1 + rr * np.sin(tt))**2
assert abs(ZZ.max() - (-2 + 2 * math.sqrt(2))) < 1e-4 and abs(ZZ.min() - (-2 - 2 * math.sqrt(2))) < 1e-4

# ---------------------------------------------------------------- pictures
C0 = w.contour("c0", F0, (-2.6, 2.6), (-2.6, 2.6), w=480, n=14, region=("disk", 0, 0, 2),
               curves=[(lambda s: 2 * math.cos(s), lambda s: 2 * math.sin(s), 0, 2 * math.pi)], points=[
                   dict(name="i", x=-1, y=0, label="(−1,0)", role="min", dx=0, dy=-18, anchor="middle"),
                   dict(name="l", x=-2, y=0, label="(−2,0)", role="end", dx=-10, dy=36, anchor="end"),
                   dict(name="r", x=2, y=0, label="(2,0)", role="max", dx=10, dy=36)])
s2 = 1 / math.sqrt(2)


def disk(pfx, shown=(), wd=470):
    return w.contour(pfx, F, (-1.2, 2.4), (-1.2, 2.4), w=wd, n=14, region=("disk", 1, 1, 1), shown=shown,
                     curves=[(lambda s: 1 + math.cos(s), lambda s: 1 + math.sin(s), 0, 2 * math.pi)], points=[
                         dict(name="o", x=0, y=0, label="(0,0)", role="out", dx=-12, dy=30, anchor="end"),
                         dict(name="a", x=1 + s2, y=1 + s2, label="t=π/4", role="min", dx=10, dy=-12),
                         dict(name="b", x=1 - s2, y=1 - s2, label="t=5π/4", role="max", dx=14, dy=26)])


DX, DY = disk("dx"), disk("dy", shown=("p-o", "cv-0"), wd=420)
CT = w.ctable("ct", [(r"\left(1-\tfrac1{\sqrt2},\,1-\tfrac1{\sqrt2}\right)", None, r"-2+2\sqrt2"),
                     (r"\left(1+\tfrac1{\sqrt2},\,1+\tfrac1{\sqrt2}\right)", None, r"-2-2\sqrt2")], mx=0, mn=1, hidden=True)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("הפעם התחום עגול: דיסק, כלומר עיגול מלא יחד עם המעגל שמקיף אותו."),
    P("נראה שתי דרכים להפוך את המעגל לפונקציה של משתנה אחד, ואיפה מסתתרות הנקודות שאסור לשכוח."),
    P("ובסוף שאלת מבחן שבה הנקודה הקריטית בכלל לא בתחום.", hold=0.4),
], stage='<div class="kicker">E06 · אקסטרמום</div><h1>תחום עגול: פנים ומעגל</h1>'
         '<p>נקודות קריטיות בפנים, הצבה על המעגל, ונקודות הקצה של ההצבה.</p>', layout="title")

idea = Scene("idea", "שתי דרכים", [
    P("דיסק זה פנים ועוד מעגל. הפנים כמו תמיד: נקודות קריטיות, ורק אלה שבאמת בתוך הדיסק.", do=show("i-0")),
    P("על המעגל יש שתי דרכים. הראשונה: **הצבה**.", do=show("i-1"),
      say="על המעגל יש שתי דרכים. הראשונה: הצבה."),
    P("אם $y$ מופיע רק בחזקות זוגיות, מציבים $y^2=R^2-x^2$, ומקבלים פונקציה של $x$ בלבד.",
      say="אם וַואי מופיע רק בחזקות זוגיות, מציבים וַואי בריבוע שווה אָר בריבוע פחות אִקְס בריבוע, ומקבלים פונקציה של אִקְס בלבד."),
    P("אבל $x$ לא חופשי: על המעגל הוא רק בין מינוס $R$ ל-$R$. זה קטע סגור, והקצוות שלו הם מועמדים.",
      do=show("i-t"),
      say="אבל אִקְס לא חופשי: על המעגל הוא רק בין מינוס אָר לאָר. זה קטע סגור, והקצוות שלו הם מועמדים."),
    P("הדרך השנייה: **פרמטריזציה**. כותבים את הנקודה על המעגל בעזרת זווית $t$.", do=show("i-2"),
      say="הדרך השנייה: פרמטריזציה. כותבים את הנקודה על המעגל בעזרת זווית טִי."),
    P("כאן אין קצוות, כי המעגל נסגר. אבל צריך לאסוף את **כל** הפתרונות של הנגזרת, לאורך סיבוב שלם.",
      do=show("i-k"), hold=0.4,
      say="כאן אין קצוות, כי המעגל נסגר. אבל צריך לאסוף את כל הפתרונות של הנגזרת, לאורך סיבוב שלם."),
], stage='<div class="xcol" style="gap:20px;width:920px">'
         + st.card("i-0", "plain", '<div style="font-size:40px;text-align:center"><b>דיסק = פנים + מעגל</b></div>')
         + st.card("i-1", "ex", r"<b>הצבה</b>: $y^2=R^2-x^2$, ואז $g(x)$ עבור $-R\le x\le R$")
         + st.card("i-2", "ex", r"<b>פרמטריזציה</b>: $x=R\cos t,\ y=R\sin t$, ‏$0\le t\le2\pi$")
         + "</div>",
   panel=st.card("i-t", "trap", r"⚠️ בהצבה: הקצוות $x=\pm R$ הם מועמדים")
         + st.card("i-k", "rule", "🔑 בפרמטריזציה: כל הפתרונות בסיבוב שלם"))

L0 = w.lines("e0", [r"$f_x=2x+2,\ f_y=2y\ \Rightarrow\ ({-1},0)$", r"$y^2=4-x^2:\quad g(x)=2x+4$",
                    r"$g'(x)=2\ne0$", r"$g(-2)=0,\qquad g(2)=8$"], cls="sm")
ex = Scene("ex", "דוגמה", [
    P("דוגמה: $x^2+y^2+2x$ בדיסק שרדיוסו שתיים.", do=show("c0-cv-0"),
      say="דוגמה: אִקְס בריבוע ועוד וַואי בריבוע ועוד שתיים אִקְס, בדיסק שרדיוסו שתיים."),
    P("בפנים: הנקודה $({-1},0)$, והיא בתוך הדיסק. הערך שם מינוס אחת.", do=show("e0-0", "c0-p-i"),
      say="בפנים: הנקודה מינוס אחת, אפס, והיא בתוך הדיסק. הערך שם מינוס אחת."),
    P("על המעגל: $y$ מופיע רק בריבוע, אז מציבים ארבע פחות $x^2$. נשאר $g=2x+4$.", do=show("e0-1"),
      say="על המעגל: וַואי מופיע רק בריבוע, אז מציבים ארבע פחות אִקְס בריבוע. נשאר גִ'י שווה שתיים אִקְס ועוד ארבע."),
    P("הנגזרת היא שתיים. היא **אף פעם** לא מתאפסת!", do=show("e0-2"),
      say="הנגזרת היא שתיים. היא אף פעם לא מתאפסת!"),
    P("מי שמחפש רק איפה שהנגזרת אפס, יחשוב שעל המעגל אין כלום.", do=show("e-t")),
    P("אבל $x$ חי בקטע ממינוס שתיים עד שתיים. בקצוות: אפס, ושמונה.", do=show("e0-3", "c0-p-l", "c0-p-r"),
      say="אבל אִקְס חי בקטע ממינוס שתיים עד שתיים. בקצוות: אפס, ושמונה."),
    P("אז המקסימום הוא שמונה בנקודה $(2,0)$, והמינימום מינוס אחת, בפנים.", hold=0.4,
      say="אז המקסימום הוא שמונה בנקודה שתיים, אפס, והמינימום מינוס אחת, בפנים."),
], stage=f'<div class="xrow"><div style="width:500px">{L0}</div>{C0}</div>',
   panel=st.card("e-t", "trap", r"⚠️ $g'\ne0$ בכל מקום: הקיצון על המעגל נמצא <b>רק</b> בקצוות $x=\pm2$"))

QSTEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>מצאו אקסטרמומים מוחלטים של $f(x,y)=1-x^2-y^2$ '
         r'בתחום $(x-1)^2+(y-1)^2\le1$.</div>')
LX = w.lines("x1", [r"$\nabla f=({-2x},{-2y})=0\ \Rightarrow\ (0,0)$", r"$(0-1)^2+(0-1)^2=2>1$",
                    r"$x=1+\cos t,\quad y=1+\sin t$", r"$f=-2-2\cos t-2\sin t$"], cls="sm")
exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: אקסטרמום מוחלט של אחת פחות $x^2$ פחות $y^2$, בדיסק שמרכזו $(1,1)$ ורדיוסו אחת.",
      say="שאלה ממבחן: אקסטרמום מוחלט של אחת פחות אִקְס בריבוע פחות וַואי בריבוע, בדיסק שמרכזו אחת, אחת, ורדיוסו אחת."),
    P("פנים: הנגזרות מתאפסות רק בראשית.", do=show("x1-0")),
    P("אבל האם הראשית בתוך הדיסק? מציבים: יוצא שתיים, וזה גדול מאחת. היא בחוץ, ונפסלת.",
      do=show("x1-1", "dx-p-o")),
    P("אז אין מועמדים בפנים, והתשובה כולה על המעגל.", do=show("x-1")),
    P("כאן הצבה לא נוחה, כי המעגל לא סביב הראשית. אז פרמטריזציה סביב המרכז.", do=show("x1-2", "dx-cv-0")),
    P("מציבים ומפתחים. הריבועים של קוסינוס וסינוס מתחברים לאחת, ונשארת פונקציה פשוטה של $t$.",
      do=show("x1-3"), hold=0.4,
      say="מציבים ומפתחים. הריבועים של קוסינוס וסינוס מתחברים לאחת, ונשארת פונקציה פשוטה של טִי."),
], stage=f'<div class="xrow"><div style="width:520px">{LX}</div>{DX}</div>',
   panel=QSTEM + st.card("x-1", "trap", "⚠️ נקודה קריטית מחוץ לתחום נפסלת"))

L2 = w.lines("x2", [r"$f'(t)=2\sin t-2\cos t=0$", r"$\tan t=1:\quad t=\tfrac{\pi}{4},\ \ t=\tfrac{5\pi}{4}$"], cls="sm")
exam2 = Scene("exam2", "פתרון על המעגל", [
    P("גוזרים לפי $t$, ומשווים לאפס: סינוס שווה לקוסינוס, כלומר טנגנס שווה אחת.", do=show("x2-0"),
      say="גוזרים לפי טִי, ומשווים לאפס: סינוס שווה לקוסינוס, כלומר טנגנס שווה אחת."),
    P("בסיבוב שלם יש לזה **שני** פתרונות: רבע פאי, וחמישה רבעי פאי.", do=show("x2-1", "dy-p-a", "dy-p-b"),
      say="בסיבוב שלם יש לזה שני פתרונות: רבע פאי, וחמישה רבעי פאי."),
    P("מי שלוקח רק את הפתרון הראשון של הטנגנס, מאבד חצי מהתשובה.", do=show("x-t")),
    P("רבע פאי נותן את הנקודה הרחוקה מהראשית, והערך מינוס שתיים פחות שני שורש שתיים.", do=show("ct", "ct-r1")),
    P("חמישה רבעי פאי נותן את הנקודה הקרובה לראשית, והערך מינוס שתיים ועוד שני שורש שתיים.", do=show("ct-r0")),
    P("המקסימום הוא בנקודה הקרובה לראשית, והמינימום ברחוקה.", do=show("ct-mx", "ct-mn")),
    P("וזה הגיוני: הפונקציה, אחת פחות המרחק בריבוע מהראשית, גדולה יותר ככל שהנקודה קרובה יותר.", do=show("x-k")),
    P("ומה עם $t=0$? זו סתם נקודה על המעגל. הערך שם מינוס ארבע, בין השניים.", hold=0.5,
      say="ומה עם טִי שווה אפס? זו סתם נקודה על המעגל. הערך שם מינוס ארבע, בין השניים."),
], stage=f'<div class="xrow">{DY}<div class="xcol" style="width:600px">{L2}{CT}</div></div>',
   panel=QSTEM + st.card("x-t", "trap", r"⚠️ $\tan t=1$ פעמיים בסיבוב: $\frac{\pi}{4}$ וגם $\frac{5\pi}{4}$")
         + st.card("x-k", "ex", r"$f=1-(x^2+y^2)$: גדולה ליד הראשית"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: דיסק זה פנים ועוד מעגל, ושניהם נכנסים לטבלה אחת.", do=show("r-1")),
    P("נקודה קריטית נבדקת: האם היא באמת בתוך הדיסק.", do=show("r-2")),
    P("בהצבה, הקצוות של $x$ הם מועמדים. בפרמטריזציה, אוספים את כל הפתרונות בסיבוב שלם.", do=show("r-3"),
      say="בהצבה, הקצוות של אִקְס הם מועמדים. בפרמטריזציה, אוספים את כל הפתרונות בסיבוב שלם."),
    P("ובסרטון הבא: כופלי לגראנז', דרך שלישית לטפל במעגל. נתראה.", do=show("r-4"), hold=0.6),
], stage='<div class="xbig" style="font-size:46px;direction:rtl">דיסק = פנים + מעגל</div>',
   panel=st.card("r-1", "rule", "🔑 טבלה אחת לפנים ולמעגל")
         + st.card("r-2", "trap", "⚠️ נקודה קריטית מחוץ לדיסק נפסלת")
         + st.card("r-3", "rule", r"🔑 הצבה: קצוות $\pm R$. פרמטריזציה: כל הפתרונות")
         + st.card("r-4", "ex", "הבא: לגראנז'"))

VIDEO = Video("E06", "extrema", "תחום עגול: פנים ומעגל", [title, idea, ex, exam, exam2, recap],
              bank={"22A-B-Q4b": None})
