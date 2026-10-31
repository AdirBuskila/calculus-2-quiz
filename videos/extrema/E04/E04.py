# -*- coding: utf-8 -*-
"""E04 · תחום סגור: פנים וקטע סגור — video script (build: tools/video/vid.py E04).

Source: courses/extrema/C04.js (lesson + goal). Exam anchor: 23A-C-Q4b (absolute extrema of x^2+y^2+4xy on the
sector bounded by x^2+y^2=1, y=0, y=sqrt(3)x in the first quadrant), an open part that no guided quiz uses. It shows
all three ideas of the level: the only critical point (0,0) is a corner, not an interior point; each straight edge is
a closed interval whose endpoints are candidates; the arc is the closed interval 0<=θ<=π/3. Max 3 at
(1/√2,1/√2), min 0 at (0,0).
Not used on purpose: the C04 quiz items (g=x^3-3x+4 on [-2,2], g=3x^4-3x^2 on [-√2,√2], the triangle of 24S-A-Q3b)
and the boss parts 22A-A-Q4b / 24S-A-Q3b that the lesson mentions. Worked 1-D example (own): x^3-3x^2 on [-1,4].
Everything is computed with sympy and the absolute max/min are re-checked on a dense grid of the sector.
"""
from vid import P, Scene, Video, show, hide, BANK
import math
import numpy as np
import sympy as sp
import stage as st
import w_extrema as w
from w_extrema import X, Y, T

# ---------------------------------------------------------------- 1-D example: g = x^3 - 3x^2 on [-1, 4]
G = T**3 - 3 * T**2
assert sp.solve(sp.diff(G, T), T) == [0, 2]
GV = {v: G.subs(T, v) for v in (-1, 0, 2, 4)}
assert GV == {-1: -4, 0: 0, 2: -4, 4: 16}
assert sp.diff(G, T).subs(T, 4) == 24                      # the max sits at an endpoint where g' != 0

# ---------------------------------------------------------------- exam 23A-C-Q4b
Q = BANK["23A-C-Q4b"]
assert "x^2+y^2+4xy" in Q["question"].replace(" ", "") and "y=\\sqrt{3}x" in Q["question"]
F = X**2 + Y**2 + 4 * X * Y
s3, r2 = sp.sqrt(3), sp.sqrt(2)
assert w.crit(F) == [(0, 0)]                                # a corner of the sector, not an interior point
TH = sp.symbols("theta", real=True)
E1 = sp.expand(F.subs(Y, 0))                                # y = 0, 0 <= x <= 1
E2 = sp.expand(F.subs(Y, s3 * X))                           # y = sqrt3 x, 0 <= x <= 1/2
assert E1 == X**2 and w.same(E2, (4 + 4 * s3) * X**2)
ARC = sp.simplify(sp.expand_trig(F.subs({X: sp.cos(TH), Y: sp.sin(TH)})))
assert w.same(ARC - (1 + 2 * sp.sin(2 * TH)), 0)
assert sp.solveset(sp.diff(1 + 2 * sp.sin(2 * TH), TH), TH, sp.Interval(0, sp.pi / 3)) == sp.FiniteSet(sp.pi / 4)
CAND = {(0, 0): 0, (1, 0): 1, (sp.Rational(1, 2), s3 / 2): 1 + s3, (1 / r2, 1 / r2): 3}
for p, v in CAND.items():
    assert w.same(w.val(F, p), v)
# dense grid of the closed sector: max 3, min 0
rr, tt = np.meshgrid(np.linspace(0, 1, 401), np.linspace(0, math.pi / 3, 401))
ZZ = (rr * np.cos(tt))**2 + (rr * np.sin(tt))**2 + 4 * rr**2 * np.cos(tt) * np.sin(tt)
assert abs(ZZ.max() - 3) < 1e-4 and abs(ZZ.min()) < 1e-12

# ---------------------------------------------------------------- pictures
GR = w.graph("g1", G, -1, 4, w=600, h=330, tlabel="x", ticks=[(-1, "−1"), (0, "0"), (2, "2"), (4, "4")], marks=[
    dict(name="c0", t=0, label="0", role="crit"), dict(name="c2", t=2, label="−4", role="crit", dy=-22),
    dict(name="ea", t=-1, label="−4", role="end", dy=-22), dict(name="eb", t=4, label="16", role="end", dy=6)])
def sector(pfx, shown=(), wd=480):
    return w.contour(pfx, F, (-0.25, 1.25), (-0.3, 1.1), w=wd, n=16, region=("sector", 1, 0, math.pi / 3), ticks=False,
               segs=[((0, 0), (1, 0), ""), ((0, 0), (0.5, math.sqrt(3) / 2), "")],
               curves=[(lambda s: math.cos(s), lambda s: math.sin(s), 0, math.pi / 3)],
               points=[dict(name="o", x=0, y=0, label="(0,0)", role="cand", dx=-12, dy=30, anchor="end"),
                       dict(name="a", x=1, y=0, label="(1,0)", role="cand", dx=-4, dy=34),
                       dict(name="b", x=0.5, y=math.sqrt(3) / 2, label="(½, √3/2)", role="cand", dx=-14, dy=-8, anchor="end"),
                       dict(name="m", x=1 / math.sqrt(2), y=1 / math.sqrt(2), label="(1/√2, 1/√2)", role="cand", dx=14, dy=-12)],
               shown=shown)


CX = sector("cx")
CY = sector("cy", shown=("ln-0", "ln-1", "p-o", "p-a", "p-b"), wd=400)
CT = w.ctable("ct", [("(0,0)", "קודקוד", "0"), ("(1,0)", "קודקוד", "1"),
                     (r"\left(\tfrac12,\tfrac{\sqrt3}{2}\right)", "קודקוד", r"1+\sqrt3"),
                     (r"\left(\tfrac1{\sqrt2},\tfrac1{\sqrt2}\right)", "קשת", "3")], mx=3, mn=0)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("עד עכשיו חיפשנו קיצון מקומי. מהיום נחפש את הערך הגדול ביותר והקטן ביותר בתחום שלם."),
    P("נלמד מתי הם בכלל קיימים, אילו נקודות קריטיות נספרות, ואיך מטפלים בקטע סגור עם הקצוות שלו."),
    P("ובסוף נפתור שאלת מבחן על גזרה של עיגול.", hold=0.4),
], stage='<div class="kicker">E04 · אקסטרמום</div><h1>תחום סגור: פנים וקטע סגור</h1>'
         '<p>מתי קיים אקסטרמום מוחלט, אילו נקודות קריטיות נספרות, וקטע סגור כולל הקצוות.</p>', layout="title")

idea = Scene("idea", "מתי קיים", [
    P("אקסטרמום מוחלט הוא הערך הגדול ביותר, או הקטן ביותר, בכל התחום. לא רק בסביבה קטנה."),
    P("משפט ויירשטראס: פונקציה רציפה על תחום **סגור וחסום** מקבלת בו מקסימום ומינימום.", do=show("i-1"),
      say="משפט ויירשטראס: פונקציה רציפה על תחום סגור וחסום מקבלת בו מקסימום ומינימום."),
    P("סגור פירושו שהשפה שייכת לתחום. חסום פירושו שהתחום לא בורח לאינסוף."),
    P("בלי זה, אין הבטחה. הפונקציה $x$ בעיגול הפתוח מתקרבת לאחת, אבל אף פעם לא מגיעה אליה.", do=show("i-2"),
      say="בלי זה, אין הבטחה. הפונקציה אִקְס בעיגול הפתוח מתקרבת לאחת, אבל אף פעם לא מגיעה אליה."),
    P("במבחן מספיק לכתוב משפט אחד: התחום סגור וחסום והפונקציה רציפה, ולכן הקיצון קיים.", do=show("i-3"), hold=0.3),
    P("ואיפה מחפשים? בשלושה מקומות.", do=show("i-r")),
    P("בפנים: נקודות קריטיות שנמצאות **בתוך** התחום. נקודה קריטית מחוץ לתחום נפסלת.", do=show("i-r1"),
      say="בפנים: נקודות קריטיות שנמצאות בתוך התחום. נקודה קריטית מחוץ לתחום נפסלת."),
    P("על השפה: שם הפונקציה הופכת לפונקציה של משתנה אחד.", do=show("i-r2")),
    P("ובסוף טבלה של כל המועמדים. הגדול ביותר הוא המקסימום, והקטן ביותר הוא המינימום.", do=show("i-r3"), hold=0.4),
], stage='<div class="xcol" style="gap:18px;width:900px">'
         + st.card("i-r", "plain", '<div style="font-size:40px;text-align:center"><b>שלושה חלקים, תמיד</b></div>')
         + st.card("i-r1", "ex", "<b>1. פנים</b>: $\\nabla f=0$, רק נקודות שבתוך התחום")
         + st.card("i-r2", "ex", "<b>2. שפה</b>: פונקציה של משתנה אחד, על קטע סגור")
         + st.card("i-r3", "ex", "<b>3. טבלה</b>: הגדול והקטן מבין כל המועמדים")
         + "</div>",
   panel=st.card("i-1", "rule", "🔑 רציפה + סגור + חסום ⇐ מקסימום ומינימום קיימים")
         + st.card("i-2", "trap", r"⚠️ $f=x$ בעיגול הפתוח $x^2+y^2&lt;1$: אין מקסימום")
         + st.card("i-3", "ex", "במבחן: משפט אחד שמצטט את ויירשטראס"))

interval = Scene("interval", "קטע סגור", [
    P("השפה נהיית קטע סגור במשתנה אחד. אז נתרגל קודם קטע סגור לבד."),
    P("$g(x)=x^3-3x^2$ בקטע ממינוס אחת עד ארבע.", do=show("g1-cv", "n-0"),
      say="גִ'י של אִקְס שווה אִקְס בשלישית פחות שלוש אִקְס בריבוע, בקטע ממינוס אחת עד ארבע."),
    P("הנגזרת $3x^2-6x$ מתאפסת באפס ובשתיים. שתיהן בתוך הקטע.", do=show("g1-m-c0", "g1-m-c2", "n-1"),
      say="הנגזרת, שלוש אִקְס בריבוע פחות שש אִקְס, מתאפסת באפס ובשתיים. שתיהן בתוך הקטע."),
    P("הערכים שם: אפס, ומינוס ארבע."),
    P("ועכשיו הקצוות, שהם תמיד מועמדים: $g(-1)=-4$ ו-$g(4)=16$.", do=show("g1-m-ea", "g1-m-eb", "n-2"),
      say="ועכשיו הקצוות, שהם תמיד מועמדים: גִ'י של מינוס אחת שווה מינוס ארבע, וגִ'י של ארבע שווה שש עשרה."),
    P("המקסימום הוא שש עשרה, **בקצה**. והנגזרת שם בכלל לא אפס.", do=show("n-t"),
      say="המקסימום הוא שש עשרה, בקצה. והנגזרת שם בכלל לא אפס."),
    P("והמינימום מינוס ארבע מתקבל פעמיים: בנקודה הקריטית, וגם בקצה השמאלי.", hold=0.4),
    P("מי שבודק רק איפה שהנגזרת מתאפסת, היה מפספס את המקסימום."),
], stage=GR,
   panel=w.lines("n", [r"$g'(x)=3x^2-6x=0$", r"$x=0,\ 2:\quad g=0,\ {-4}$", r"$g(-1)=-4,\quad g(4)=16$"], cls="sm")
         + st.card("n-t", "trap", "⚠️ הקצוות הם מועמדים גם כש-$g'\\ne0$ בהם"))

LA = w.lines("x1", [
    r"$f_x=2x+4y=0,\quad f_y=2y+4x=0$",
    r"$\Rightarrow\ (0,0)$",
    r"$y=0,\ 0\le x\le1:\quad f=x^2$",
    r"$y=\sqrt3\,x,\ 0\le x\le\tfrac12:$",
    r"$f=(4+4\sqrt3)\,x^2$",
], cls="sm")
QSTEM = (f'<div class="qstem"><span class="qid">{Q["id"]}</span>מצאו אקסטרמומים מוחלטים של '
         r'$f(x,y)=x^2+y^2+4xy$ בתחום המוגבל על ידי $x^2+y^2=1$, ‏$y=0$, ‏$y=\sqrt3\,x$ ברביע הראשון.</div>')
exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: אקסטרמום מוחלט של הפונקציה שעל המסך, בגזרה של עיגול היחידה.", do=show("cx-reg")),
    P("הגזרה תחומה בין הישר $y=0$ לישר $y=\\sqrt3\\,x$, ובקשת של מעגל היחידה. זו זווית של שישים מעלות.",
      say="הגזרה תחומה בין הישר וַואי שווה אפס לישר וַואי שווה שורש שלוש אִקְס, ובקשת של מעגל היחידה. "
          "זו זווית של שישים מעלות."),
    P("התחום סגור וחסום, והפונקציה פולינום. לכן לפי ויירשטראס יש מקסימום ומינימום.", do=show("x-w")),
    P("פנים: $f_x=2x+4y$ ו-$f_y=2y+4x$. הפתרון היחיד הוא הראשית.", do=show("x1-0", "x1-1"),
      say="פנים: אֶף אִקְס שווה שתיים אִקְס ועוד ארבע וַואי, ואֶף וַואי שווה שתיים וַואי ועוד ארבע אִקְס. "
          "הפתרון היחיד הוא הראשית."),
    P("אבל הראשית היא **קודקוד** של הגזרה, לא נקודה פנימית. אז בפנים אין מועמדים.", do=show("cx-p-o", "x-t"),
      say="אבל הראשית היא קודקוד של הגזרה, לא נקודה פנימית. אז בפנים אין מועמדים."),
    P("היא עדיין תיכנס לטבלה, אבל בתור קודקוד.", hold=0.3),
    P("צלע ראשונה: $y=0$, ו-$x$ מאפס עד אחת. נשאר $f=x^2$, שעולה כל הקטע.", do=show("cx-ln-0", "x1-2", "cx-p-a"),
      say="צלע ראשונה: וַואי שווה אפס, ואִקְס מאפס עד אחת. נשאר אִקְס בריבוע, שעולה כל הקטע."),
    P("אז על הצלע הזו המועמדים הם רק הקצוות: הראשית, ו-$(1,0)$.", say="אז על הצלע הזו המועמדים הם רק הקצוות: הראשית, ואחת, אפס."),
    P("צלע שנייה: $y=\\sqrt3\\,x$, ו-$x$ מאפס עד חצי. מקבלים קבוע חיובי כפול $x^2$.",
      do=show("cx-ln-1", "x1-3", "x1-4", "cx-p-b"),
      say="צלע שנייה: וַואי שווה שורש שלוש אִקְס, ואִקְס מאפס עד חצי. מקבלים קבוע חיובי כפול אִקְס בריבוע."),
    P("גם היא עולה, ולכן שוב רק הקצוות: הראשית, והקודקוד העליון.", hold=0.4),
], stage=f'<div class="xrow"><div style="width:470px">{LA}</div>{CX}</div>',
   panel=QSTEM + st.card("x-w", "ex", "סגור + חסום + רציף: הקיצון קיים")
         + st.card("x-t", "trap", "⚠️ נקודה קריטית על השפה אינה ״פנים״: היא נבדקת כקודקוד"))

LB = w.lines("x2", [
    r"$x=\cos\theta,\ y=\sin\theta,\quad 0\le\theta\le\tfrac{\pi}{3}$",
    r"$f=1+4\sin\theta\cos\theta=1+2\sin2\theta$",
    r"$4\cos2\theta=0\ \Rightarrow\ \theta=\tfrac{\pi}{4}$",
], cls="sm")
exam2 = Scene("exam2", "הקשת והטבלה", [
    P("נשארה הקשת. עליה המשתנה הטבעי הוא הזווית.", do=show("cy-cv-0", "x2-0")),
    P("מציבים קוסינוס וסינוס: $x^2+y^2$ הופך לאחת, ו-$4xy$ הופך לפעמיים סינוס של שתי תטא.", do=show("x2-1"),
      say="מציבים קוסינוס וסינוס: אִקְס בריבוע ועוד וַואי בריבוע הופך לאחת, וארבע אִקְס וַואי הופך לפעמיים סינוס של שתיים תטא."),
    P("זו פונקציה של תטא בקטע הסגור מאפס עד שליש פאי. הקצוות שלו הם בדיוק שני הקודקודים.",
      say="זו פונקציה של תטא בקטע הסגור מאפס עד שליש פאי. הקצוות שלו הם בדיוק שני הקודקודים."),
    P("הנגזרת מתאפסת כש-$2\\theta$ הוא תשעים מעלות, כלומר ברבע פאי. וזה בתוך הקטע.", do=show("x2-2", "cy-p-m"),
      say="הנגזרת מתאפסת כששתיים תטא הוא תשעים מעלות, כלומר ברבע פאי. וזה בתוך הקטע."),
    P("עכשיו טבלה. בראשית אפס, וב-$(1,0)$ אחת.", do=show("ct", "ct-r0", "ct-r1"),
      say="עכשיו טבלה. בראשית אפס, ובאחת, אפס, אחת."),
    P("בקודקוד העליון אחת ועוד שורש שלוש, בערך שתיים ושבעים ושלוש.", do=show("ct-r2")),
    P("ובנקודה $\\theta=\\frac{\\pi}{4}$ על הקשת, $\\left(\\tfrac1{\\sqrt2},\\tfrac1{\\sqrt2}\\right)$: אחת ועוד פעמיים אחת, כלומר שלוש.",
      do=show("ct-r3"),
      say="ובנקודה תטא שווה רבע פאי על הקשת, אחת חלקי שורש שתיים, אחת חלקי שורש שתיים: אחת ועוד פעמיים אחת, כלומר שלוש."),
    P("המקסימום המוחלט הוא שלוש, בנקודה $\\theta=\\frac{\\pi}{4}$ על הקשת. והמינימום המוחלט הוא אפס, בראשית.",
      do=show("ct-mx", "ct-mn"), hold=0.5,
      say="המקסימום המוחלט הוא שלוש, בנקודה תטא שווה רבע פאי על הקשת. והמינימום המוחלט הוא אפס, בראשית."),
], stage=f'<div class="xrow">{CY}<div class="xcol" style="width:630px">{LB}{CT}</div></div>',
   panel=QSTEM + st.card("x-k", "rule", "🔑 קשת: $0\\le\\theta\\le\\frac{\\pi}{3}$ הוא קטע סגור, והקצוות שלו הם הקודקודים")
   .replace('class="card rule h"', 'class="card rule"'))

recap = Scene("recap", "סיכום", [
    P("לסיכום: רציפה על תחום סגור וחסום, ולכן יש מקסימום ומינימום.", do=show("r-1")),
    P("בפנים סופרים רק נקודות קריטיות שבאמת בתוך התחום.", do=show("r-2")),
    P("על השפה, כל חלק הוא קטע סגור במשתנה אחד, והקצוות שלו תמיד מועמדים.", do=show("r-3")),
    P("ובסוף טבלה אחת: הגדול והקטן. נתראה ברמה הבאה, עם מצולעים.", do=show("r-4"), hold=0.6),
], stage='<div class="xbig" style="font-size:44px;direction:rtl">פנים ← שפה ← טבלה</div>',
   panel=st.card("r-1", "rule", "🔑 ויירשטראס: סגור + חסום + רציף")
         + st.card("r-2", "trap", "⚠️ נקודה קריטית מחוץ לתחום, או על השפה, אינה ״פנים״")
         + st.card("r-3", "rule", "🔑 קטע סגור: גם הקצוות")
         + st.card("r-4", "ex", "טבלה: מקסימום ומינימום מכל המועמדים"))

VIDEO = Video("E04", "extrema", "תחום סגור: פנים וקטע סגור", [title, idea, interval, exam, exam2, recap],
              bank={"23A-C-Q4b": None})
