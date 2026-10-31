"""E08 · לגראנז' עם מקרים ודיסק מלא — video script (build: tools/video/vid.py E08).

Source: courses/extrema/C08.js (lesson + goal). Exam-style problem (original, not from the bank, so bank={}):
absolute extrema of x^2+2y under x^2+y^2=4. The system 2x=2λx, 2=2λy splits into x(1-λ)=0: the case x=0 gives
(0,±2), the case λ=1 gives (±√3,1). Max 5 at (±√3,1), min -4 at (0,-2); dividing by x would lose (0,±2) and with them
the minimum. It replaces 25A-B-Q1b (xy on x^2+y^2=2), a content twin of the C07 quiz item 24A-A-Q4b.
Not used on purpose: E08's own quiz (x^2+2y^2 and x^4+y^4 on the unit circle), C06-Q2 (2x^2+y^2 on x^2+y^2=4) and the
boss part 26A-A-Q4b (x^3+x^2-3x+y^2 on x^2+y^2=4). Worked example (own): x^2-y^2 on the closed disk x^2+y^2<=4.
Every Lagrange solution and value is computed with sympy and asserted; both problems are re-checked numerically.
"""
from vid import P, Scene, Video, show, hide, BANK
import math
import numpy as np
import sympy as sp
import stage as st
import w_extrema as w
from w_extrema import X, Y, LAM

# ---------------------------------------------------------------- example: x^2 - y^2 on x^2 + y^2 <= 4
F0, G0 = X**2 - Y**2, X**2 + Y**2
assert w.crit(F0) == [(0, 0)] and w.val(F0, (0, 0)) == 0 and w.kind(*w.hess(F0, (0, 0))[:3]) == "saddle"
assert w.same(sp.diff(F0, X) - LAM * sp.diff(G0, X), 2 * X * (1 - LAM))
assert w.same(sp.diff(F0, Y) - LAM * sp.diff(G0, Y), -2 * Y * (1 + LAM))
S0 = w.lagrange(F0, G0, 4)
assert S0 == [(-2, 0, 1), (0, -2, -1), (0, 2, -1), (2, 0, 1)]
assert all(w.val(F0, s[:2]) == (4 if s[1] == 0 else -4) for s in S0)
# dividing 2x = 2λx by x leaves λ = 1, hence only y = 0: the minima (0, ±2) are lost
assert [s for s in S0 if s[2] == 1] == [(-2, 0, 1), (2, 0, 1)]
xx, yy = np.meshgrid(np.linspace(-2, 2, 801), np.linspace(-2, 2, 801))
Z0 = (xx**2 - yy**2)[xx**2 + yy**2 <= 4]
assert abs(Z0.max() - 4) < 1e-9 and abs(Z0.min() + 4) < 1e-9

# ---------------------------------------------------------------- exam-style problem: x^2 + 2y on x^2 + y^2 = 4
F, G = X**2 + 2 * Y, X**2 + Y**2
assert sp.diff(F, X) == 2 * X and sp.diff(F, Y) == 2 and sp.diff(G, Y) == 2 * Y
assert w.same(sp.diff(F, X) - LAM * sp.diff(G, X), 2 * X * (1 - LAM))        # x(1-λ) = 0
# 2 = 2λy: λ != 0 and y != 0.  Case x = 0: y = ±2.  Case λ = 1: y = 1, x^2 = 3.
s3 = sp.sqrt(3)
SOL = w.lagrange(F, G, 4)
assert [(s[0], s[1]) for s in SOL] == [(-s3, 1), (0, -2), (0, 2), (s3, 1)]
assert [s[2] for s in SOL] == [1, sp.Rational(-1, 2), sp.Rational(1, 2), 1]
assert [w.val(F, s[:2]) for s in SOL] == [5, -4, 4, 5]
# dividing 2x = 2λx by x keeps only λ = 1: the points (0, ±2) and the minimum -4 are lost
assert [w.val(F, s[:2]) for s in SOL if s[2] == 1] == [5, 5]
tt = np.linspace(0, 2 * math.pi, 200001)
ZT = (2 * np.cos(tt))**2 + 2 * (2 * np.sin(tt))
assert abs(ZT.max() - 5) < 1e-6 and abs(ZT.min() + 4) < 1e-6

# ---------------------------------------------------------------- pictures
def dplot(pfx, shown=(), wd=480):
    return w.contour(pfx, F0, (-2.8, 2.8), (-2.8, 2.8), w=wd, n=13, region=("disk", 0, 0, 2), shown=shown,
               curves=[(lambda s: 2 * math.cos(s), lambda s: 2 * math.sin(s), 0, 2 * math.pi)], points=[
                   dict(name="o", x=0, y=0, label="(0,0)", role="saddle", dx=12, dy=-12),
                   dict(name="r", x=2, y=0, label="(2,0)", role="max", dx=10, dy=-14),
                   dict(name="l", x=-2, y=0, label="(−2,0)", role="max", dx=-10, dy=-14, anchor="end"),
                   dict(name="u", x=0, y=2, label="(0,2)", role="min", dx=12, dy=-12),
                   dict(name="d", x=0, y=-2, label="(0,−2)", role="min", dx=12, dy=32)])


C0 = dplot("c0")
C1 = dplot("c1", shown=("cv-0", "p-r", "p-l", "p-u", "p-d"), wd=440)
s3f = math.sqrt(3)


def xplot(pfx, shown=()):
    return w.contour(pfx, F, (-2.8, 2.8), (-2.8, 2.8), w=480, n=15, shown=shown,
               curves=[(lambda s: 2 * math.cos(s), lambda s: 2 * math.sin(s), 0, 2 * math.pi)], points=[
                   dict(name="a", x=s3f, y=1, label="(√3,1)", role="max", dx=12, dy=-12),
                   dict(name="b", x=-s3f, y=1, label="(−√3,1)", role="max", dx=-12, dy=-12, anchor="end"),
                   dict(name="c", x=0, y=2, label="(0,2)", role="cand", dx=12, dy=-14),
                   dict(name="d", x=0, y=-2, label="(0,−2)", role="min", dx=12, dy=32)])


CX = xplot("cx")
CY = xplot("cy", shown=("cv-0", "p-a", "p-b", "p-c", "p-d"))
CT0 = w.ctable("ct", [("(0,0)", "פנים", "0"), (r"({\pm2},0)", "מעגל", "4"), (r"(0,{\pm2})", "מעגל", "-4")],
               mx=1, mn=2, hidden=True)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("במבחן, משוואות לגראנז' כמעט תמיד מתפרקות לגורמים."),
    P("בסרטון הזה נלמד לפצל אותן למקרים בלי לאבד אף נקודה, ולשלב את הפנים עם לגראנז' בדיסק מלא."),
    P("ובסוף שאלה בסגנון מבחן, שבה חילוק במשתנה מאבד בדיוק את המינימום.", hold=0.4),
], stage='<div class="kicker">E08 · אקסטרמום</div><h1>לגראנז\' עם מקרים ודיסק מלא</h1>'
         '<p>לפצל למקרים בלי לחלק במשתנה, ולשלב פנים ולגראנז\' בדיסק.</p>', layout="title")

L1 = w.lines("e1", [r"$2x=2\lambda x\ \Rightarrow\ x(1-\lambda)=0$",
                    r"$-2y=2\lambda y\ \Rightarrow\ y(1+\lambda)=0$",
                    r"$x=0:\ \ y=\pm2,\ \ f=-4$",
                    r"$\lambda=1:\ \ y=0,\ x=\pm2,\ \ f=4$"], cls="sm")
cases = Scene("cases", "מקרים", [
    P("דוגמה: $x^2-y^2$ בדיסק המלא שרדיוסו שתיים. נתחיל מהשפה, המעגל, עם לגראנז'.", do=show("c0-cv-0"),
      say="דוגמה: אִקְס בריבוע פחות וַואי בריבוע, בדיסק המלא שרדיוסו שתיים. נתחיל מהשפה, המעגל, עם לגראנז'."),
    P("המשוואה הראשונה: $2x=2\\lambda x$. מעבירים אגף: $x$ כפול אחת פחות למדא, שווה אפס.", do=show("e1-0"),
      say="המשוואה הראשונה: שתיים אִקְס שווה שתיים למדא אִקְס. מעבירים אגף: אִקְס כפול, בסוגריים, אחת פחות למדא, שווה אפס."),
    P("והשנייה: $y$ כפול אחת ועוד למדא, שווה אפס.", do=show("e1-1"),
      say="והשנייה: וַואי כפול, בסוגריים, אחת ועוד למדא, שווה אפס."),
    P("מקרה ראשון: $x=0$. מהאילוץ $y$ שווה שתיים או מינוס שתיים, והערך מינוס ארבע.", do=show("e1-2", "c0-p-u", "c0-p-d"),
      say="מקרה ראשון: אִקְס שווה אפס. מהאילוץ וַואי שווה שתיים או מינוס שתיים, והערך מינוס ארבע."),
    P("מקרה שני: למדא שווה אחת. אז מהמשוואה השנייה $y=0$, ו-$x$ שווה פלוס או מינוס שתיים. הערך ארבע.",
      do=show("e1-3", "c0-p-r", "c0-p-l"),
      say="מקרה שני: למדא שווה אחת. אז מהמשוואה השנייה וַואי שווה אפס, ואִקְס שווה פלוס או מינוס שתיים. הערך ארבע."),
    P("ואם $x$ ו-$y$ שניהם אפס? הראשית לא על המעגל, אז המקרה נפסל במפורש.", do=show("k-1"),
      say="ואם אִקְס ווַואי שניהם אפס? הראשית לא על המעגל, אז המקרה נפסל במפורש."),
    P("ועכשיו הטעות: מי שמחלק את המשוואה הראשונה ב-$x$, מקבל ישר למדא שווה אחת.", do=show("k-t"),
      say="ועכשיו הטעות: מי שמחלק את המשוואה הראשונה באִקְס, מקבל ישר למדא שווה אחת."),
    P("והוא מאבד את שתי הנקודות שבהן $x=0$, שהן בדיוק המינימום.", do=hide("c0-p-u", "c0-p-d"),
      say="והוא מאבד את שתי הנקודות שבהן אִקְס שווה אפס, שהן בדיוק המינימום."),
    P("אז כל גורם פותח מקרה, וכל מקרה מסתיים בנקודות, או בסתירה מפורשת.", do=show("c0-p-u", "c0-p-d", "k-2"), hold=0.4),
], stage=f'<div class="xrow"><div style="width:520px">{L1}</div>{C0}</div>',
   panel=st.card("k-1", "ex", "מקרה שמוביל לנקודה שלא על העקום: נפסל")
         + st.card("k-t", "trap", r"⚠️ חילוק ב-$x$ מוחק את הפתרונות עם $x=0$")
         + st.card("k-2", "rule", r"🔑 $x\cdot(\ldots)=0$: או $x=0$, או הסוגריים אפס"))

disk = Scene("disk", "דיסק מלא", [
    P("אבל השאלה הייתה על הדיסק המלא, לא רק על המעגל. אז מוסיפים את הפנים.", do=show("c1-p-o")),
    P("בפנים הנקודה הקריטית היחידה היא הראשית. היא אוכף, אבל הערך שלה, אפס, נכנס לטבלה.", do=show("ct", "ct-r0")),
    P("ועכשיו כל המועמדים: ארבע בשתי הנקודות על ציר $x$, ומינוס ארבע על ציר $y$.", do=show("ct-r1", "ct-r2"),
      say="ועכשיו כל המועמדים: ארבע בשתי הנקודות על ציר אִקְס, ומינוס ארבע על ציר וַואי."),
    P("המקסימום ארבע, והמינימום מינוס ארבע. שניהם על השפה.", do=show("ct-mx", "ct-mn")),
    P("בדיסק: פנים ועוד לגראנז' על המעגל, וטבלה אחת. ובשאלה \"תחת האילוץ\" בודקים רק את העקום.", do=show("d-1"),
      hold=0.4, say="בדיסק: פנים ועוד לגראנז' על המעגל, וטבלה אחת. ובשאלה תחת האילוץ בודקים רק את העקום."),
], stage=f'<div class="xrow">{C1}{CT0}</div>',
   panel=st.card("d-1", "rule", "🔑 ״בתחום״: פנים + שפה. ״תחת האילוץ״: רק העקום"))

QSTEM = ('<div class="qstem"><span class="qid">בסגנון מבחן</span>מצאו אקסטרמומים מוחלטים של הפונקציה '
         r'$f(x,y)=x^2+2y$ תחת האילוץ $x^2+y^2=4$.</div>')
LX = w.lines("x1", [r"$2x=2\lambda x,\qquad 2=2\lambda y$",
                    r"$x(1-\lambda)=0$",
                    r"$x=0:\ \ y=\pm2$",
                    r"$\lambda=1:\ \ y=1,\ \ x^2=3$",
                    r"$x=\pm\sqrt3$"], cls="sm")
exam = Scene("exam", "שאלה בסגנון מבחן", [
    P("שאלה בסגנון מבחן: קיצון של $x^2+2y$ תחת האילוץ שעל המסך. רק המעגל, בלי פנים.",
      say="שאלה בסגנון מבחן: קיצון של אִקְס בריבוע ועוד שתיים וַואי, תחת האילוץ שעל המסך. רק המעגל, בלי פנים.",
      do=show("cx-cv-0")),
    P("הגרדיאנטים: $(2x,2)$ ו-$(2x,2y)$. אז $2x=2\\lambda x$, ו-$2=2\\lambda y$.", do=show("x1-0"),
      say="הגרדיאנטים: שתיים אִקְס, שתיים, ושתיים אִקְס, שתיים וַואי. אז שתיים אִקְס שווה שתיים למדא אִקְס, ושתיים שווה שתיים למדא וַואי."),
    P("מהמשוואה השנייה, למדא לא אפס וגם $y$ לא אפס. את הראשונה לא מחלקים, אלא מפרקים: $x(1-\\lambda)=0$.",
      do=show("x1-1", "x-t"),
      say="מהמשוואה השנייה, למדא לא אפס וגם וַואי לא אפס. את הראשונה לא מחלקים, אלא מפרקים: אִקְס כפול, בסוגריים, אחת פחות למדא, שווה אפס."),
    P("מקרה $x=0$: מהאילוץ $y$ שווה שתיים או מינוס שתיים. שתי נקודות על ציר $y$.",
      do=show("x1-2", "cx-p-c", "cx-p-d"),
      say="מקרה אִקְס שווה אפס: מהאילוץ וַואי שווה שתיים או מינוס שתיים. שתי נקודות על ציר וַואי."),
    P("מקרה למדא שווה אחת: מהמשוואה השנייה $y=1$, ומהאילוץ $x^2=3$.", do=show("x1-3"),
      say="מקרה למדא שווה אחת: מהמשוואה השנייה וַואי שווה אחת, ומהאילוץ אִקְס בריבוע שווה שלוש."),
    P("כלומר $x$ שווה שורש שלוש או מינוס שורש שלוש. בסך הכול ארבע נקודות.", do=show("x1-4", "cx-p-a", "cx-p-b"),
      say="כלומר אִקְס שווה שורש שלוש או מינוס שורש שלוש. בסך הכול ארבע נקודות.", hold=0.4),
], stage=f'<div class="xrow"><div style="width:520px">{LX}</div>{CX}</div>',
   panel=QSTEM + st.card("x-t", "trap", r"⚠️ לא מחלקים ב-$x$: מפרקים $x(1-\lambda)=0$"))

exam2 = Scene("exam2", "התשובה", [
    P("בשתי הנקודות שבהן $y=1$ הערך שלוש ועוד שתיים, כלומר חמש. זה המקסימום.", do=show("a-1"),
      say="בשתי הנקודות שבהן וַואי שווה אחת, הערך שלוש ועוד שתיים, כלומר חמש. זה המקסימום."),
    P("ב-$(0,2)$ הערך ארבע, וב-$(0,{-2})$ מינוס ארבע. זה המינימום.", do=show("a-2"),
      say="באפס, שתיים, הערך ארבע, ובאפס, מינוס שתיים, מינוס ארבע. זה המינימום."),
    P("המעגל סגור וחסום, אז חמש ומינוס ארבע הם הקיצונים המוחלטים.", do=show("a-3")),
    P("ומי שחילק ב-$x$? קיבל רק למדא שווה אחת, ואיבד את שתי הנקודות על ציר $y$, ואיתן את המינימום.",
      do=show("a-t"),
      say="ומי שחילק באִקְס? קיבל רק למדא שווה אחת, ואיבד את שתי הנקודות על ציר וַואי, ואיתן את המינימום."),
    P("אז במבחן: מפרקים, פותחים מקרה לכל גורם, ורק אז מסכמים.", hold=0.5),
], stage=CY,
   panel=QSTEM + st.card("a-1", "ex", r"$f({\pm\sqrt3},1)=5$: מקסימום")
         + st.card("a-2", "ex", r"$f(0,{-2})=-4$: מינימום, ו-$f(0,2)=4$")
         + st.card("a-3", "rule", "🔑 עקום סגור וחסום: אלה הקיצונים המוחלטים")
         + st.card("a-t", "trap", r"⚠️ חילוק ב-$x$: בלי $(0,\pm2)$, ובלי המינימום"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: משוואה מהצורה משתנה כפול סוגריים, שווה אפס, פותחת שני מקרים.", do=show("r-1")),
    P("כל מקרה מסתיים בנקודות על העקום, או בסתירה שכותבים במפורש.", do=show("r-2")),
    P("בדיסק מלא: הנקודות הקריטיות בפנים, ועוד לגראנז' על המעגל, בטבלה אחת.", do=show("r-3")),
    P("ובסרטון הבא, מבחן הגמר: שאלות אמיתיות מכל הקורס. בהצלחה!", do=show("r-4"), hold=0.6),
], stage=r'<div class="xbig">$x\,(1-\lambda)=0$</div>',
   panel=st.card("r-1", "rule", "🔑 גורם כפול גורם = 0: שני מקרים")
         + st.card("r-2", "trap", "⚠️ לא מחלקים במשתנה שיכול להתאפס")
         + st.card("r-3", "rule", "🔑 דיסק: פנים + לגראנז' על השפה")
         + st.card("r-4", "ex", "״תחת האילוץ״: רק העקום"))

VIDEO = Video("E08", "extrema", "לגראנז' עם מקרים ודיסק מלא", [title, cases, disk, exam, exam2, recap],
              bank={})
