# -*- coding: utf-8 -*-
"""I06 · קואורדינטות קוטביות והיעקוביאן r — video script (build: tools/video/vid.py I06).

Source: courses/double_int/C06.js (lesson + goal). Exam anchor: 23A-A-Q1a (arctan(y/x) over the part of the ring
1<=x^2+y^2<=4 between the rays y=x and y=sqrt(3)x), solved to the end: 7*pi^2/192. Not used on purpose: the C06 quiz
items (half disk of radius 3, x^2+y^2 on the unit disk, the quarter ring, x^2+y^2=4x, xy on the quarter disk) and
the boss questions 23A-C-Q1a and 22A-B-Q1b.
Every polar value is sympy-exact; the exam value is also checked by a direct numeric integral in x, y, and the
drawn sector against its area.
"""
import math
import sympy as sp
from scipy import integrate as si
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_double_int as w

x, y = sp.symbols("x y", real=True)
r, th = sp.symbols("r theta", positive=True)

# ---------------------------------------------------------------- the Jacobian of (r, theta) -> (x, y)
J = sp.Matrix([[sp.diff(r * sp.cos(th), r), sp.diff(r * sp.cos(th), th)],
               [sp.diff(r * sp.sin(th), r), sp.diff(r * sp.sin(th), th)]]).det()
assert sp.simplify(J - r) == 0
assert sp.simplify((r * sp.cos(th))**2 + (r * sp.sin(th))**2 - r**2) == 0

# ---------------------------------------------------------------- example: e^{-(x^2+y^2)} on the disk of radius 2
inner = sp.integrate(sp.exp(-r**2) * r, (r, 0, 2))
assert sp.simplify(inner - (1 - sp.exp(-4)) / 2) == 0
VAL1 = sp.integrate(inner, (th, 0, 2 * sp.pi))
assert sp.simplify(VAL1 - sp.pi * (1 - sp.exp(-4))) == 0
assert sp.integrate(sp.exp(-r**2), r).has(sp.erf)                  # without the factor r: no elementary antiderivative
num1 = si.dblquad(lambda yy, xx: math.exp(-(xx * xx + yy * yy)), -2, 2, lambda s: -math.sqrt(4 - s * s),
                  lambda s: math.sqrt(4 - s * s))[0]
assert abs(num1 - float(VAL1)) < 1e-7

# ---------------------------------------------------------------- exam 23A-A-Q1a
Q = BANK["23A-A-Q1a"]
assert r"\arctan" in Q["question"] and r"\sqrt{3}" in Q["question"]
t1, t2 = sp.atan(1), sp.atan(sp.sqrt(3))
assert t1 == sp.pi / 4 and t2 == sp.pi / 3                        # the rays y = x and y = sqrt(3) x (x > 0)
assert sp.simplify(sp.atan(sp.tan(th)).subs(th, sp.pi / 4 + sp.Rational(1, 10)) - (sp.pi / 4 + sp.Rational(1, 10))) == 0
VAL = sp.integrate(sp.integrate(th * r, (r, 1, 2)), (th, sp.pi / 4, sp.pi / 3))
assert sp.simplify(VAL - 7 * sp.pi**2 / 192) == 0
assert sp.integrate(r, (r, 1, 2)) == sp.Rational(3, 2)
assert sp.simplify(sp.integrate(th, (th, sp.pi / 4, sp.pi / 3)) - 7 * sp.pi**2 / 288) == 0
NO_R = sp.integrate(sp.integrate(th, (r, 1, 2)), (th, sp.pi / 4, sp.pi / 3))   # forgetting r
assert sp.simplify(NO_R - 7 * sp.pi**2 / 288) == 0 and NO_R != VAL


def _band(xx):
    lo = max(xx, math.sqrt(max(0.0, 1 - xx * xx)))
    hi = min(math.sqrt(3) * xx, math.sqrt(max(0.0, 4 - xx * xx)))
    return lo, max(lo, hi)


num = si.dblquad(lambda yy, xx: math.atan(yy / xx), 0.3, 1.6, lambda s: _band(s)[0], lambda s: _band(s)[1],
                 epsabs=1e-10)[0]
assert abs(num - float(VAL)) < 1e-6, (num, float(VAL))
assert abs(float(VAL) - 0.3598) < 1e-3

# ---------------------------------------------------------------- pictures
G = w.Plot("g", (-0.4, 3.4), (-0.4, 3.4), w=540, h=540, xticks=[(1, "1"), (2, "2"), (3, "3")], yticks=[])
for k in (1, 2, 3):
    G.polar(f"g-c{k}", lambda s, k=k: k, 0, math.pi / 2, kind="ink", hidden=False, dash=True)
for k, a in enumerate((math.pi / 6, math.pi / 3)):
    G.ray(f"g-r{k}", a, 0, 3.3, kind="ink", hidden=False, dash=True)
cell = w.polar_region(lambda s: 2.0, lambda s: 2.5, math.radians(30), math.radians(42))
G.fill("g-cell", cell, kind="b")
G.polar("g-arc", lambda s: 2.5, math.radians(30), math.radians(42), kind="b")
G.ray("g-dr", math.radians(30), 2.0, 2.5, kind="a")
G.label("g-ldr", 2.45, 0.95, "dr", kind="a")
G.label("g-lrd", 1.55, 2.25, "r·dθ", kind="b")
G.ray("g-rr", math.radians(36), 0, 2.0, kind="c")
G.label("g-lr", 0.55, 0.85, "r", kind="c")

D = w.Plot("d", (-2.6, 2.6), (-2.6, 2.6), w=520, h=520, xticks=[], yticks=[])
D.fill("d-reg", w.polar_region(lambda s: 0.0, lambda s: 2.0, 0, 2 * math.pi), kind="a", hidden=False)
D.polar("d-c", lambda s: 2.0, 0, 2 * math.pi, kind="a", hidden=False)
D.label("d-l", 1.45, 1.75, "r = 2", kind="a", hidden=False)
D.wedge("d-w", 0.75, 0, 2)

X = w.Plot("x6", (-0.4, 2.4), (-0.4, 2.4), w=430, h=430, xticks=[(1, "1"), (2, "2")], yticks=[(1, "1"), (2, "2")])
sector = w.polar_region(lambda s: 1.0, lambda s: 2.0, math.pi / 4, math.pi / 3)
assert abs(w.shoelace(sector) - 3 / 2 * (math.pi / 3 - math.pi / 4)) < 1e-3
X.polar("x6-c1", lambda s: 1.0, 0, math.pi / 2, kind="a")
X.polar("x6-c2", lambda s: 2.0, 0, math.pi / 2, kind="a")
X.ray("x6-r1", math.pi / 4, 0, 2.3, kind="b")
X.ray("x6-r2", math.pi / 3, 0, 2.3, kind="c")
X.label("x6-l1", 0.12, 0.6, "r = 1", kind="a")
X.label("x6-l2", 2.05, 0.35, "r = 2", kind="a")
X.label("x6-l3", 1.72, 1.45, "y = x", kind="b")
X.label("x6-l4", 1.25, 2.1, "y = √3·x", kind="c", anchor="end")
X.fill("x6-reg", sector, kind="d")
X.wedge("x6-w", 0.93, 1, 2)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נעבור לקואורדינטות קוטביות: מרחק מהראשית וזווית."),
    P("נבין מאיפה מגיע הגורם $r$ שתמיד צריך להוסיף, ונראה איך הוא הופך אינטגרל בלתי אפשרי לקל.",
      say="נבין מאיפה מגיע הגורם אָר שתמיד צריך להוסיף, ונראה איך הוא הופך אינטגרל בלתי אפשרי לקל."),
    P("ובסוף נפתור שאלה ממבחן על חלק של טבעת.", hold=0.4),
], stage='<div class="kicker">I06 · אינטגרל כפול</div><h1>קואורדינטות קוטביות והיעקוביאן r</h1>'
         '<p>לעבור לקואורדינטות קוטביות בתחום מעגלי, לכתוב את הגבולות, לא לשכוח את הגורם r, ולחשב.</p>',
   layout="title")

idea = Scene("idea", "הרעיון", [
    P("כשהתחום בנוי ממעגלים סביב הראשית ומקרניים שיוצאות ממנה, נוח לתאר נקודה במרחק ובזווית.", do=show("i-0")),
    P("$x$ שווה $r$ קוסינוס תטא, $y$ שווה $r$ סינוס תטא, ולכן $x^2+y^2=r^2$.", do=show("i-1"),
      say="אִקְס שווה אָר קוסינוס תטא, וַואי שווה אָר סינוס תטא, ולכן אִקְס בריבוע ועוד וַואי בריבוע, שווה אָר בריבוע."),
    P("מעגל סביב הראשית הוא פשוט $r$ קבוע, וקרן מהראשית היא תטא קבועה.",
      say="מעגל סביב הראשית הוא פשוט אָר קבוע, וקרן מהראשית היא תטא קבועה."),
    P("ועכשיו החלק החשוב: מה השטח של תא קטן ברשת הזאת?", do=show("g-cell")),
    P("בכיוון הרדיאלי הוא באורך $dr$.", do=show("g-dr", "g-ldr"), say="בכיוון הרדיאלי הוא באורך דִּי אָר."),
    P("אבל בכיוון הזווית, אורך הקשת הוא $r$ כפול $d\\theta$: ככל שמתרחקים, הקשת ארוכה יותר.",
      do=show("g-arc", "g-lrd", "g-rr", "g-lr"),
      say="אבל בכיוון הזווית, אורך הקשת הוא אָר כפול דִּי תטא: ככל שמתרחקים, הקשת ארוכה יותר."),
    P("לכן השטח של התא הוא $r\\,dr\\,d\\theta$. זה היעקוביאן של המעבר: $r$.", do=show("i-2", "i-c"),
      say="לכן השטח של התא הוא אָר, דִּי אָר, דִּי תטא. זה היעקוביאן של המעבר: אָר.", hold=0.4),
], stage=f'<div class="di-col">{G.svg()}</div>',
   panel=w.eqs("i", [
       "$x=r\\,\\cos\\theta,\\ \\ y=r\\,\\sin\\theta$",
       "$x^2+y^2=r^2$",
       "$dx\\,dy=r\\,dr\\,d\\theta$",
   ], size=40, gap=22) + st.card("i-c", "rule", "🔑 היעקוביאן הוא $r$: הקשת באורך $r\\,d\\theta$"))

ex = Scene("ex", "דוגמה", [
    P("דוגמה: האינטגרל של $e$ בחזקת מינוס $x^2+y^2$, על הדיסק ברדיוס שתיים.", do=show("a-0"),
      say="דוגמה: האינטגרל של אֵי בחזקת מינוס, אִקְס בריבוע ועוד וַואי בריבוע, על הדיסק ברדיוס שתיים."),
    P("בקוטביות: $r$ מאפס עד שתיים, תטא מאפס עד שתיים פאי, והאינטגרנד הוא $e^{-r^2}$.", do=show("a-1", "d-w"),
      say="בקוטביות: אָר מאפס עד שתיים, תטא מאפס עד שתיים פאי, והאינטגרנד הוא אֵי בחזקת מינוס אָר בריבוע."),
    P("ולא שוכחים את $r$. הוא נכנס לאינטגרל הפנימי.", do=show("a-2"),
      say="ולא שוכחים את אָר. הוא נכנס לאינטגרל הפנימי."),
    P("ועכשיו הפלא: ל-$e^{-r^2}$ לבד אין פונקציה קדומה אלמנטרית. אבל ל-$r\\,e^{-r^2}$ יש.", do=show("a-c"),
      say="ועכשיו הפלא: לאֵי בחזקת מינוס אָר בריבוע לבד, אין פונקציה קדומה אלמנטרית. אבל לאָר כפול אֵי בחזקת מינוס אָר בריבוע, יש."),
    P("הקדומה היא מינוס חצי $e^{-r^2}$. בין אפס לשתיים: חצי, כפול אחת פחות $e^{-4}$.", do=show("a-3"),
      say="הקדומה היא מינוס חצי, אֵי בחזקת מינוס אָר בריבוע. בין אפס לשתיים: חצי, כפול אחת פחות אֵי בחזקת מינוס ארבע."),
    P("והאינטגרל על תטא רק כופל בשתיים פאי. התוצאה: פאי, כפול אחת פחות $e^{-4}$.", do=show("a-4", "a-ok"),
      say="והאינטגרל על תטא רק כופל בשתיים פאי. התוצאה: פאי, כפול אחת פחות אֵי בחזקת מינוס ארבע.", hold=0.4),
], stage=f'<div class="di-col">{D.svg()}</div>',
   panel=w.eqs("a", [
       "$\\displaystyle\\iint_{x^2+y^2\\le 4} e^{-(x^2+y^2)}\\,dA$",
       "$0\\le r\\le 2,\\ \\ 0\\le\\theta\\le 2\\pi$",
       "$\\displaystyle=\\int_0^{2\\pi}\\!\\int_0^2 e^{-r^2}\\,r\\,dr\\,d\\theta$",
       "$\\displaystyle\\int_0^2 r\\,e^{-r^2}dr=\\frac{1-e^{-4}}{2}$",
       "$=\\pi\\left(1-e^{-4}\\right)$",
   ], size=34, gap=12) + w.chip("a-ok", "✓ ה-$r$ עשה את העבודה")
         + st.card("a-c", "rule", "🔑 $r\\,e^{-r^2}$ = נגזרת של $-\\tfrac12e^{-r^2}$"))

trap = Scene("trap", "המלכודות", [
    P("שתי מלכודות. הראשונה: לשכוח את $r$. אז האלמנט הוא $dr\\,d\\theta$, והתשובה שגויה.", do=show("t-1"),
      say="שתי מלכודות. הראשונה: לשכוח את אָר. אז האלמנט הוא דִּי אָר דִּי תטא, והתשובה שגויה."),
    P("השנייה: המעגל $x^2+y^2=4$ הוא $r=2$, ולא $r=4$. מוציאים שורש.", do=show("t-2"),
      say="השנייה: המעגל אִקְס בריבוע ועוד וַואי בריבוע שווה ארבע, הוא אָר שווה שתיים, ולא אָר שווה ארבע. מוציאים שורש."),
    P("וקרן $y=mx$ עם $x$ חיובי היא תטא שווה ארקטנגנס $m$. רק כש-$x$ חיובי.", do=show("t-3"),
      say="וקרן, וַואי שווה אֶם אִקְס, עם אִקְס חיובי, היא תטא שווה ארקטנגנס אֶם. רק כשאִקְס חיובי.", hold=0.4),
], stage=w.eqs("tt", [
    "$dx\\,dy=r\\,dr\\,d\\theta$",
    "$x^2+y^2=a^2\\ \\Rightarrow\\ r=a$",
    "$y=mx,\\ x>0\\ \\Rightarrow\\ \\theta=\\arctan m$",
], size=44, gap=40, shown=3),
   panel=st.card("t-1", "trap", "⚠️ בלי $r$: תשובה שגויה")
         + st.card("t-2", "trap", "⚠️ $x^2+y^2=a^2$ הוא $r=a$, לא $a^2$")
         + st.card("t-3", "trap", "⚠️ $\\theta=\\arctan\\frac yx$ רק כש-$x>0$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: האינטגרל של ארקטנגנס $y$ חלקי $x$ על התחום $D$.",
      say="שאלה ממבחן: האינטגרל של ארקטנגנס וַואי חלקי אִקְס, על התחום דִּי."),
    P("התנאי הראשון: $x^2+y^2$ בין אחת לארבע. זו טבעת: $r$ בין אחת לשתיים.", do=show("x6-c1", "x6-c2", "x6-l1", "x6-l2"),
      say="התנאי הראשון: אִקְס בריבוע ועוד וַואי בריבוע, בין אחת לארבע. זו טבעת: אָר בין אחת לשתיים."),
    P("התנאי השני: $y$ בין $x$ לשורש שלוש כפול $x$, ו-$x$ חיובי. אלה שתי קרניים.", do=show("x6-r1", "x6-r2", "x6-l3", "x6-l4"),
      say="התנאי השני: וַואי בין אִקְס לשורש שלוש כפול אִקְס, ואִקְס חיובי. אלה שתי קרניים."),
    P("$y=x$ היא זווית של פאי חלקי ארבע, ו-$y=\\sqrt3\\,x$ היא פאי חלקי שלוש, כי הטנגנס שלה שורש שלוש.", do=show("x-0", "x6-reg"),
      say="וַואי שווה אִקְס היא זווית של פאי חלקי ארבע, ווַואי שווה שורש שלוש אִקְס היא פאי חלקי שלוש, כי הטנגנס שלה שורש שלוש."),
    P("ועכשיו האינטגרנד: $y$ חלקי $x$ הוא טנגנס תטא. וכש-$x$ חיובי, ארקטנגנס של טנגנס תטא הוא תטא עצמה.", do=show("x-1"),
      say="ועכשיו האינטגרנד: וַואי חלקי אִקְס הוא טנגנס תטא. וכשאִקְס חיובי, ארקטנגנס של טנגנס תטא הוא תטא עצמה."),
    P("אז מקבלים את האינטגרל של תטא כפול $r$. ה-$r$ הזה הוא היעקוביאן.", do=show("x-2", "x6-w"),
      say="אז מקבלים את האינטגרל של תטא כפול אָר. האָר הזה הוא היעקוביאן."),
    P("המשתנים נפרדים: האינטגרל של $r$ מאחת עד שתיים הוא שלושה חצאים.", do=show("xs-0"),
      say="המשתנים נפרדים: האינטגרל של אָר מאחת עד שתיים, הוא שלושה חצאים."),
    P("והאינטגרל של תטא הוא חצי, כפול פאי בריבוע חלקי תשע, פחות פאי בריבוע חלקי שש-עשרה.", do=show("xs-1")),
    P("כלומר שבעה פאי בריבוע חלקי מאתיים שמונים ושמונה. כפול שלושה חצאים:"),
    P("שבעה פאי בריבוע חלקי מאה תשעים ושתיים.", do=show("x-ok")),
    P("המלכודת: מי ששוכח את $r$ מקבל שבעה פאי בריבוע חלקי מאתיים שמונים ושמונה, ומפסיד את הסעיף.", do=show("x-t"),
      say="המלכודת: מי ששוכח את אָר מקבל שבעה פאי בריבוע חלקי מאתיים שמונים ושמונה, ומפסיד את הסעיף.", hold=0.4),
], stage=f'<div class="di-col">{X.svg()}' + w.eqs("xs", [
             "$\\displaystyle\\int_1^2 r\\,dr=\\frac32$",
             "$\\displaystyle\\int_{\\pi/4}^{\\pi/3}\\theta\\,d\\theta=\\frac12\\left(\\frac{\\pi^2}{9}-\\frac{\\pi^2}{16}\\right)=\\frac{7\\pi^2}{288}$",
         ], size=30, gap=6) + '</div>',
   panel=w.stem(Q["id"], "חשבו את $\\iint_D\\arctan\\frac{y}{x}\\,dx\\,dy$, כאשר "
                "$D$ הוא $1\\le x^2+y^2\\le4$, $x\\le y\\le\\sqrt3\\,x$, $x\\ge0$")
         + w.eqs("x", [
             "$1\\le r\\le 2,\\ \\ \\dfrac{\\pi}{4}\\le\\theta\\le\\dfrac{\\pi}{3}$",
             "$\\arctan\\dfrac{y}{x}=\\theta$",
             "$\\displaystyle\\int_{\\pi/4}^{\\pi/3}\\!\\int_1^2\\theta\\,r\\,dr\\,d\\theta$",
         ], size=30, gap=8)
         + '<div class="di-row">' + w.chip("x-ok", "$=\\dfrac32\\cdot\\dfrac{7\\pi^2}{288}=\\dfrac{7\\pi^2}{192}$")
         + '</div>' + w.chip("x-t", "⚠️ בלי $r$ יוצא $\\tfrac{7\\pi^2}{288}$", kind="bad"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: $x$ שווה $r$ קוסינוס תטא, $y$ שווה $r$ סינוס תטא, ו-$x^2+y^2=r^2$.", do=show("z-1"),
      say="לסיכום: אִקְס שווה אָר קוסינוס תטא, וַואי שווה אָר סינוס תטא, ואִקְס בריבוע ועוד וַואי בריבוע, שווה אָר בריבוע."),
    P("אלמנט השטח הוא $r\\,dr\\,d\\theta$, כי הקשת באורך $r\\,d\\theta$.", do=show("z-2"),
      say="אלמנט השטח הוא אָר, דִּי אָר, דִּי תטא, כי הקשת באורך אָר דִּי תטא."),
    P("מעגלים הם $r$ קבוע, קרניים הן תטא קבועה.", do=show("z-3"),
      say="מעגלים הם אָר קבוע, קרניים הן תטא קבועה."),
    P("ובלי $r$ התשובה שגויה. נתראה ברמה הבאה.", do=show("z-4"), hold=0.6,
      say="ובלי אָר התשובה שגויה. נתראה ברמה הבאה."),
], stage='<div class="di-big">$dx\\,dy=r\\,dr\\,d\\theta$</div>',
   panel=st.card("z-1", "rule", "🔑 $x=r\\,\\cos\\theta,\\ y=r\\,\\sin\\theta$")
         + st.card("z-2", "rule", "🔑 $dA=r\\,dr\\,d\\theta$")
         + st.card("z-3", "rule", "🔑 מעגל: $r$ קבוע. קרן: $\\theta$ קבועה")
         + st.card("z-4", "trap", "⚠️ לא לשכוח את $r$"))

VIDEO = Video("I06", "double_int", "קואורדינטות קוטביות והיעקוביאן r", [title, idea, ex, trap, exam, recap],
              bank={"23A-A-Q1a": None})
