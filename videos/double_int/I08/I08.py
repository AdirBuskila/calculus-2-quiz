# -*- coding: utf-8 -*-
"""I08 · בוס: שאלות מבחן אמיתיות — video script (build: tools/video/vid.py I08).

Source: courses/double_int/C08.js (boss: the method table and the final checks). A walkthrough of two parts: an ORIGINAL
exam-style part ((x-3y)e^{x+y} over the parallelogram x+y=1,2, x-3y=0,4: 2e(e-1); 22A-B-Q4a / 25A-B-Q2b were dropped
because their substitution and factor 1/3 are the answer of quiz C07-Q1) and the bank part 23A-A-Q4a ((x^2+2xy) over the first-quadrant region of y=1/x^2, y=4/x^2, y=x+1, y=x-1: 6). Not used on purpose: the
six boss questions of C08 (26A-A-Q1a, 25A-A-Q4a, 23A-C-Q4a, 23A-C-Q1a, 22A-B-Q1b, 26A-A-Q4a) and the anchors of
I01..I07.
Every Jacobian, bound and value is sympy-exact, each value is also checked by a direct numeric integral in x, y,
and each drawn region against its area.
"""
import math
import numpy as np
import sympy as sp
from scipy import integrate as si
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_double_int as w

x, y, u, v = sp.symbols("x y u v", real=True)


def jinv(U, V):
    return sp.Matrix([[sp.diff(U, x), sp.diff(U, y)], [sp.diff(V, x), sp.diff(V, y)]]).det()


# ---------------------------------------------------------------- exam 1: an ORIGINAL exam-style part ("בסגנון מבחן")
# (22A-B-Q4a was dropped: its substitution u=y-x, v=y+2x and factor 1/3 are the C07-Q1 answer.)
# int int_D (x-3y) e^{x+y} dA, D bounded by x+y=1, x+y=2, x-3y=0, x-3y=4  ->  u=x+y, v=x-3y, |J|=1/4, value 2e(e-1)
U1, V1 = x + y, x - 3*y
assert jinv(U1, V1) == -4
assert sp.simplify((x - 3*y) * sp.exp(x + y) - V1 * sp.exp(U1)) == 0
VAL1 = sp.Rational(1, 4) * sp.integrate(v * sp.exp(u), (u, 1, 2), (v, 0, 4))
assert sp.simplify(VAL1 - 2 * sp.E * (sp.E - 1)) == 0
assert sp.integrate(v, (v, 0, 4)) == 8 and sp.simplify(sp.integrate(sp.exp(u), (u, 1, 2)) - (sp.E**2 - sp.E)) == 0
AREA1 = sp.Rational(1, 4) * 1 * 4
assert AREA1 == 1
# separable: the value is exactly area x (mean of v = 2) x (mean of e^u = e^2 - e)
assert sp.simplify(VAL1 - AREA1 * 2 * (sp.E**2 - sp.E)) == 0
V1s = {}
for a in (1, 2):
    for b in (0, 4):
        s_ = sp.solve([sp.Eq(x + y, a), sp.Eq(x - 3*y, b)], [x, y], dict=True)[0]
        V1s[(a, b)] = (s_[x], s_[y])
assert set(V1s.values()) == {(sp.Rational(3, 4), sp.Rational(1, 4)), (sp.Rational(3, 2), sp.Rational(1, 2)),
                             (sp.Rational(7, 4), sp.Rational(-3, 4)), (sp.Rational(5, 2), sp.Rational(-1, 2))}
assert sorted({px for px, _ in V1s.values()}) == [sp.Rational(3, 4), sp.Rational(3, 2), sp.Rational(7, 4), sp.Rational(5, 2)]
band1 = lambda s: (max((s - 4) / 3, 1 - s), max(max((s - 4) / 3, 1 - s), min(s / 3, 2 - s)))
num1 = si.dblquad(lambda yy, xx: (xx - 3 * yy) * math.exp(xx + yy), 0.75, 2.5, lambda s: band1(s)[0],
                  lambda s: band1(s)[1], epsabs=1e-11)[0]
assert abs(num1 - float(VAL1)) < 1e-7, (num1, float(VAL1))
assert abs(float(VAL1) - 9.34) < 0.01

PAR = [tuple(float(c) for c in V1s[k]) for k in ((1, 0), (2, 0), (2, 4), (1, 4))]
assert abs(w.shoelace(PAR) - 1) < 1e-9
A = w.Plot("a", (0.3, 2.9), (-1.1, 1.0), w=560, h=480, xticks=[(1, "1"), (2, "2")], yticks=[(-1, "-1")])
A.fill("a-reg", PAR, kind="d")
A.fn("a-l1", lambda s: 1 - s, 0.4, 2.0, kind="b")
A.fn("a-l2", lambda s: 2 - s, 1.0, 2.8, kind="b")
A.fn("a-l3", lambda s: s / 3, 0.4, 2.0, kind="c")
A.fn("a-l4", lambda s: (s - 4) / 3, 1.3, 2.8, kind="c")
A.label("a-t1", 0.35, 0.72, "x+y = 1", kind="b")
A.label("a-t2", 1.3, 0.95, "x+y = 2", kind="b")
A.label("a-t3", 2.05, 0.6, "x−3y = 0", kind="c")
A.label("a-t4", 2.25, -0.97, "x−3y = 4", kind="c")
for i, xv in enumerate((1.5, 1.75)):
    A.curve(f"a-cut{i}", [(xv, -0.95), (xv, 0.75)], kind="ink", dash=True)

# ---------------------------------------------------------------- exam 2: 23A-A-Q4a
Q2 = BANK["23A-A-Q4a"]
assert r"y=\frac{1}{x^2}" in Q2["question"] and "y=x-1" in Q2["question"]
U2, V2 = x**2 * y, y - x
assert sp.simplify(U2.subs(y, 1 / x**2)) == 1 and sp.simplify(U2.subs(y, 4 / x**2)) == 4
assert sp.simplify(V2.subs(y, x + 1)) == 1 and sp.simplify(V2.subs(y, x - 1)) == -1
J2 = jinv(U2, V2)
assert sp.expand(J2 - (2*x*y + x**2)) == 0
assert sp.expand((x**2 + 2*x*y) - J2) == 0                         # the integrand IS the inverse Jacobian
VAL2 = sp.integrate(1, (u, 1, 4), (v, -1, 1))
assert VAL2 == 6
# for u in [1,4], v in [-1,1] there is exactly one point with x > 0, y > 0: x^3 + v x^2 = u has one positive root
for a in (1, 2.5, 4):
    for b in (-1, -0.3, 0, 0.6, 1):
        rts = [r.real for r in np.roots([1, b, 0, -a]) if abs(r.imag) < 1e-9 and r.real > 0]
        assert len(rts) == 1 and rts[0] + b > 0


def pt2(a, b):
    xx = [r.real for r in np.roots([1, b, 0, -a]) if abs(r.imag) < 1e-9 and r.real > 0][0]
    return xx, xx + b


band2 = lambda s: (max(1 / s**2, s - 1), max(max(1 / s**2, s - 1), min(4 / s**2, s + 1)))
num2 = si.dblquad(lambda yy, xx: xx * xx + 2 * xx * yy, 0.4, 3.0, lambda s: band2(s)[0], lambda s: band2(s)[1],
                  epsabs=1e-10)[0]
assert abs(num2 - 6) < 1e-6, num2
n = 50
edge = ([(1 + 3 * k / n, -1) for k in range(n + 1)] + [(4, -1 + 2 * k / n) for k in range(n + 1)]
        + [(4 - 3 * k / n, 1) for k in range(n + 1)] + [(1, 1 - 2 * k / n) for k in range(n + 1)])
REG2 = [pt2(a, b) for a, b in edge]
area2 = si.dblquad(lambda yy, xx: 1.0, 0.4, 3.0, lambda s: band2(s)[0], lambda s: band2(s)[1])[0]
assert abs(w.shoelace(REG2) - area2) < 2e-3
B = w.Plot("b", (-0.2, 2.9), (-0.2, 3.6), w=520, h=600, xticks=[(1, "1"), (2, "2")], yticks=[(1, "1"), (2, "2"), (3, "3")])
B.fill("b-reg", REG2, kind="a")
B.fn("b-h1", lambda s: 1 / s**2, 0.55, 2.8, kind="c")
B.fn("b-h4", lambda s: 4 / s**2, 1.07, 2.8, kind="c")
B.fn("b-l1", lambda s: s + 1, -0.1, 2.5, kind="b")
B.fn("b-l2", lambda s: s - 1, 1.0, 2.8, kind="b")
B.label("b-t1", 2.85, 0.24, "y = 1/x²", kind="c")
B.label("b-t4", 2.85, 0.66, "y = 4/x²", kind="c")
B.label("b-t2", 2.55, 3.4, "y = x+1", kind="b")
B.label("b-t3", 2.85, 1.72, "y = x−1", kind="b")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("זה סרטון הבוס של האינטגרל הכפול."),
    P("נפתור שתי שאלות, אחת בסגנון מבחן ואחת ממבחן, ובכל אחת נתחיל מהשאלה החשובה ביותר: איזו שיטה."),
    P("ובסוף כל פתרון, נבדוק שהתשובה הגיונית.", hold=0.4),
], stage='<div class="kicker">I08 · אינטגרל כפול</div><h1>בוס: שאלות מבחן אמיתיות</h1>'
         '<p>לפתור שאלות אינטגרל כפול ממבחנים אמיתיים: חילוף סדר, תחום מתפצל, קואורדינטות קוטביות ושינוי משתנים.</p>',
   layout="title")

method = Scene("method", "בוחרים שיטה", [
    P("לפני שמחשבים, מזהים את השיטה לפי הסימנים בשאלה."),
    P("אינטגרנד כמו $e^{x^2}$ או סינוס של $x^2$, או בקשה מפורשת: מחליפים סדר.", do=show("m-1"),
      say="אינטגרנד כמו אֵי בחזקת אִקְס בריבוע, או סינוס של אִקְס בריבוע, או בקשה מפורשת: מחליפים סדר."),
    P("סכום של שני אינטגרלים: מוצאים את נקודת המפגש, וקוראים בכיוון ההפוך.", do=show("m-2")),
    P("מעגלים, קרניים מהראשית, או $x^2+y^2$ באינטגרנד: קוטביות, ולא שוכחים את $r$.", do=show("m-3"),
      say="מעגלים, קרניים מהראשית, או אִקְס בריבוע ועוד וַואי בריבוע באינטגרנד: קוטביות, ולא שוכחים את אָר."),
    P("וארבעה עקומים בשני זוגות: משתנים חדשים שהופכים אותם למלבן.", do=show("m-4")),
    P("בשתי השאלות של היום יש ארבעה עקומים. אבל נראה שהבחירה של $u$ ו-$v$ שונה מאוד.", hold=0.4,
      say="בשתי השאלות של היום יש ארבעה עקומים. אבל נראה שהבחירה של יוּ ווִי שונה מאוד."),
], stage='<div class="di-col">'
         + st.card("m-1", "ex", "$e^{x^2},\\ \\sin(x^2)$ או ״החליפו סדר״: <b>חילוף סדר</b>")
         + st.card("m-2", "ex", "סכום של שני אינטגרלים: <b>איחוד</b>")
         + st.card("m-3", "ex", "מעגלים, קרניים, $x^2+y^2$: <b>קוטביות</b>, $dA=r\\,dr\\,d\\theta$")
         + st.card("m-4", "ex", "ארבעה עקומים: <b>$u,v$</b> ו-$|J|=\\dfrac{1}{|J^{-1}|}$") + '</div>',
   panel=st.card("m-r", "rule", "🔑 שיטה קודם, חישוב אחר כך").replace(" h\"", "\""))

ex1 = Scene("ex1", "שאלה ראשונה", [
    P("שאלה ראשונה, בסגנון מבחן: $x-3y$ כפול $e^{x+y}$, על התחום שחסום בארבעה ישרים.",
      do=show("a-l1", "a-l2", "a-l3", "a-l4", "a-reg", "a-t1", "a-t2", "a-t3", "a-t4"),
      say="שאלה ראשונה, בסגנון מבחן: אִקְס פחות שלוש וַואי, כפול אֵי בחזקת אִקְס ועוד וַואי, על התחום שחסום בארבעה ישרים."),
    P("בפסים אנכיים התחום נחתך בשני מקומות, בקודקודים: שלושה אינטגרלים. זו לא הדרך.", do=show("a-cut0", "a-cut1")),
    P("אבל הישרים באים בזוגות מקבילים: $x+y$ שווה אחת ושתיים, ו-$x-3y$ שווה אפס וארבע.",
      do=hide("a-cut0", "a-cut1") + show("p-0"),
      say="אבל הישרים באים בזוגות מקבילים: אִקְס ועוד וַואי, שווה אחת ושתיים, ואִקְס פחות שלוש וַואי, שווה אפס וארבע."),
    P("אז $u=x+y$ בין אחת לשתיים, ו-$v=x-3y$ בין אפס לארבע.", do=show("p-1"),
      say="אז יוּ שווה אִקְס ועוד וַואי, בין אחת לשתיים, ווִי שווה אִקְס פחות שלוש וַואי, בין אפס לארבע."),
    P("ושימו לב: האינטגרנד הוא בדיוק $v$ כפול $e^u$. זה רמז שהבחירה נכונה.",
      say="ושימו לב: האינטגרנד הוא בדיוק וִי כפול אֵי בחזקת יוּ. זה רמז שהבחירה נכונה."),
    P("היעקוביאן ההפוך: אחת, אחת, אחת, מינוס שלוש. מינוס שלוש פחות אחת: מינוס ארבע.", do=show("p-2")),
    P("לכן הגורם הוא רבע, והאינטגרל נפרד: רבע, כפול האינטגרל של $e^u$, כפול האינטגרל של $v$.",
      do=show("p-3"),
      say="לכן הגורם הוא רבע, והאינטגרל נפרד: רבע, כפול האינטגרל של אֵי בחזקת יוּ, כפול האינטגרל של וִי."),
    P("האינטגרל של $e^u$ מאחת עד שתיים: $e^2-e$. של $v$ מאפס עד ארבע: שמונה.", do=show("p-4"),
      say="האינטגרל של אֵי בחזקת יוּ מאחת עד שתיים: אֵי בריבוע פחות אֵי. של וִי מאפס עד ארבע: שמונה."),
    P("התוצאה: שתיים $e$, כפול, בסוגריים, $e$ פחות אחת. בערך תשע נקודה שלוש.", do=show("p-ok"),
      say="התוצאה: שתיים אֵי, כפול, בסוגריים, אֵי פחות אחת. בערך תשע נקודה שלוש."),
    P("בדיקת סבירות: השטח הוא רבע כפול אחת כפול ארבע, כלומר אחת.", do=show("p-5")),
    P("הממוצע של $v$ הוא שתיים, והממוצע של $e^u$ הוא $e^2-e$. שטח כפול שני הממוצעים: בדיוק התשובה.",
      hold=0.4,
      say="הממוצע של וִי הוא שתיים, והממוצע של אֵי בחזקת יוּ הוא אֵי בריבוע פחות אֵי. שטח כפול שני הממוצעים: בדיוק התשובה."),
], stage=f'<div class="di-col">{A.svg()}' + '<div class="di-row">'
         + w.chip("p-5", "שטח: $\\tfrac14\\cdot1\\cdot4=1$", kind="warn")
         + w.chip("p-ok", "$=2e(e-1)\\approx 9.34$") + '</div></div>',
   panel=w.stem(w.STYLE_TAG, "חשבו את $\\iint_D(x-3y)\\,e^{x+y}\\,dx\\,dy$, כאשר $D$ חסום על ידי "
                "$x+y=1$, $x+y=2$, $x-3y=0$, $x-3y=4$")
         + w.eqs("p", [
             "$u=x+y,\\ \\ v=x-3y$",
             "$1\\le u\\le 2,\\ \\ 0\\le v\\le 4$",
             "$J^{-1}=\\det\\begin{pmatrix}1&1\\\\1&-3\\end{pmatrix}=-4$",
             "$\\displaystyle\\frac14\\int_1^2e^u\\,du\\int_0^4v\\,dv$",
             "$=\\dfrac14\\cdot\\left(e^2-e\\right)\\cdot 8$",
         ], size=30, gap=4))

ex2 = Scene("ex2", "שאלה שנייה", [
    P("שאלה שנייה: $x^2+2xy$, על התחום ברביע הראשון שבין שתי עקומות לשני ישרים.",
      do=show("b-h1", "b-h4", "b-l1", "b-l2", "b-t1", "b-t2", "b-t3", "b-t4"),
      say="שאלה שנייה: אִקְס בריבוע ועוד שתיים אִקְס וַואי, על התחום ברביע הראשון, שבין שתי עקומות לשני ישרים."),
    P("העקומות הן $y$ שווה אחת חלקי $x^2$ וארבע חלקי $x^2$. כלומר $x^2y$ שווה אחת וארבע.", do=show("b-reg", "q-0"),
      say="העקומות הן, וַואי שווה אחת חלקי אִקְס בריבוע, וארבע חלקי אִקְס בריבוע. כלומר אִקְס בריבוע וַואי, שווה אחת וארבע."),
    P("והישרים הם $y-x$ שווה מינוס אחת ואחת. אז $u=x^2y$ ו-$v=y-x$.", do=show("q-1"),
      say="והישרים הם, וַואי פחות אִקְס, שווה מינוס אחת ואחת. אז יוּ שווה אִקְס בריבוע וַואי, ווִי שווה וַואי פחות אִקְס."),
    P("לכל זוג כזה יש בדיוק נקודה אחת ברביע הראשון. אז המלבן מתאר כל נקודה של התחום בדיוק פעם אחת.",
      say="לכל זוג כזה יש בדיוק נקודה אחת ברביע הראשון. אז המלבן מתאר כל נקודה של התחום בדיוק פעם אחת."),
    P("היעקוביאן ההפוך: שתיים $x$ $y$, $x^2$, מינוס אחת, אחת. יוצא $x^2+2xy$.", do=show("q-2"),
      say="היעקוביאן ההפוך: שתיים אִקְס וַואי, אִקְס בריבוע, מינוס אחת, אחת. יוצא אִקְס בריבוע ועוד שתיים אִקְס וַואי."),
    P("הוא חיובי ברביע הראשון, אז הגורם הוא אחת חלקי $x^2+2xy$.", do=show("q-3"),
      say="הוא חיובי ברביע הראשון, אז הגורם הוא אחת חלקי אִקְס בריבוע ועוד שתיים אִקְס וַואי."),
    P("וזה בדיוק האינטגרנד! הם מצטמצמים, ונשאר האינטגרל של אחת על המלבן.", do=show("q-4")),
    P("כלומר שטח המלבן: שלוש כפול שתיים, שש.", do=show("q-ok")),
    P("המלכודת כאן: לנסות לבטא את $x$ ו-$y$ דרך $u$ ו-$v$. אין צורך, ויוצאת משוואה ממעלה שלישית.", do=show("q-t"),
      say="המלכודת כאן: לנסות לבטא את אִקְס ווַואי דרך יוּ ווִי. אין צורך, ויוצאת משוואה ממעלה שלישית."),
    P("כשהיעקוביאן מצטמצם עם האינטגרנד, לא צריך את הנוסחה ההפוכה בכלל.", hold=0.4),
], stage=f'<div class="di-col">{B.svg(scale=0.95)}</div>',
   panel=w.stem(Q2["id"], "חשבו את $\\iint_D\\left(x^2+2xy\\right)dx\\,dy$, כאשר $D$ ברביע הראשון חסום על ידי "
                "$y=\\dfrac{1}{x^2}$, $y=\\dfrac{4}{x^2}$, $y=x+1$, $y=x-1$")
         + w.eqs("q", [
             "$u=x^2y\\in[1,4]$",
             "$v=y-x\\in[-1,1]$",
             "$J^{-1}=\\det\\begin{pmatrix}2xy&x^2\\\\-1&1\\end{pmatrix}=x^2+2xy$",
             "$|J|=\\dfrac{1}{x^2+2xy}$",
             "$\\displaystyle\\int_1^4\\!\\int_{-1}^{1}1\\,dv\\,du$",
         ], size=30, gap=4)
         + '<div class="di-row">' + w.chip("q-ok", "$=3\\cdot2=6$")
         + w.chip("q-t", "⚠️ לא צריך את $x(u,v)$", kind="warn") + '</div>')

recap = Scene("recap", "סיכום", [
    P("לסיכום הקורס: קודם מזהים שיטה, ורק אחר כך מחשבים.", do=show("z-1")),
    P("תחום משרטטים תמיד, עם נקודות החיתוך.", do=show("z-2")),
    P("בשינוי משתנים: אחת חלקי היעקוביאן ההפוך, בערך מוחלט. ובקוטביות: הגורם $r$.", do=show("z-3"),
      say="בשינוי משתנים: אחת חלקי היעקוביאן ההפוך, בערך מוחלט. ובקוטביות: הגורם אָר."),
    P("ובסוף בודקים: אותו שטח בשני הסדרים, ותשובה בגודל סביר. בהצלחה בבוס!", do=show("z-4"), hold=0.6),
], stage='<div class="di-big">$\\displaystyle |J|=\\frac{1}{|J^{-1}|},\\qquad dA=r\\,dr\\,d\\theta$</div>',
   panel=st.card("z-1", "rule", "🔑 שיטה קודם")
         + st.card("z-2", "rule", "🔑 שרטוט ונקודות חיתוך")
         + st.card("z-3", "trap", "⚠️ $\\tfrac{1}{|J^{-1}|}$, והגורם $r$")
         + st.card("z-4", "rule", "🔑 בדיקת שטח וסבירות"))

VIDEO = Video("I08", "double_int", "בוס: שאלות מבחן אמיתיות", [title, method, ex1, ex2, recap],
              bank={"23A-A-Q4a": None})
