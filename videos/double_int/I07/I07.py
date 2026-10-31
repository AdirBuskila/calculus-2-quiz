# -*- coding: utf-8 -*-
"""I07 · שינוי משתנים ליניארי והיעקוביאן — video script (build: tools/video/vid.py I07).

Source: courses/double_int/C07.js (lesson + goal). Exam anchor: 22A-A-Q4a (e^{y-x}(2y+4) over the region bounded by
y-x=1, y=x+2, y^2=-4x, y^2=-4x+9), solved to the end with u=y-x, v=y^2+4x: 9e(e-1) on the region with y>=0, as in
the official solution; the trap shown is that the four curves bound a second region (y < -2) where 2y+4 < 0 and the
same integral is -9e(e-1) (the bank's solution notes this too). Not used on purpose: the C07 quiz items (u=y-x,
v=y+2x; y/x and xy; x+y and x-y) and the boss question 26A-A-Q4a; 22A-B-Q4a / 25A-B-Q2b (u=y-x, v=y+2x, whose
Jacobian is the C07-Q1 answer) are left for the I08 walkthrough.
Every Jacobian, region and value is sympy-exact; the exam values are also checked by direct numeric integrals in
x, y over both regions, and the drawn regions against their areas.
"""
import math
import sympy as sp
from scipy import integrate as si
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_double_int as w

x, y, u, v = sp.symbols("x y u v", real=True)

# ---------------------------------------------------------------- example: 2<=x+2y<=4, 0<=2x-y<=5, f = x+2y
U, V = x + 2*y, 2*x - y
Jinv = sp.Matrix([[sp.diff(U, x), sp.diff(U, y)], [sp.diff(V, x), sp.diff(V, y)]]).det()
assert Jinv == -5
inv = sp.solve([sp.Eq(u, U), sp.Eq(v, V)], [x, y], dict=True)[0]
assert inv == {x: (u + 2*v) / 5, y: (2*u - v) / 5}
Jdir = sp.Matrix([[sp.diff(inv[x], u), sp.diff(inv[x], v)], [sp.diff(inv[y], u), sp.diff(inv[y], v)]]).det()
assert Jdir == sp.Rational(-1, 5) and abs(Jdir) == 1 / abs(Jinv)  # the reciprocal rule, checked both ways
VAL1 = sp.integrate(u * sp.Rational(1, 5), (u, 2, 4), (v, 0, 5))
assert VAL1 == 6
AREA1 = sp.integrate(sp.Rational(1, 5), (u, 2, 4), (v, 0, 5))
assert AREA1 == 2
corners = [(uu, vv) for uu, vv in ((2, 0), (4, 0), (4, 5), (2, 5))]
PAR = [(float(inv[x].subs({u: a, v: b})), float(inv[y].subs({u: a, v: b}))) for a, b in corners]
assert abs(w.shoelace(PAR) - 2) < 1e-9
assert [tuple(sp.nsimplify(c) for c in pt) for pt in PAR][0] == (sp.Rational(2, 5), sp.Rational(4, 5))

E = w.Plot("e", (-0.4, 3.4), (-1.4, 2.2), w=520, h=500, xticks=[(1, "1"), (2, "2"), (3, "3")],
           yticks=[(-1, "-1"), (1, "1"), (2, "2")])
E.fill("e-reg", PAR, kind="d", hidden=False)
E.fn("e-a", lambda s: (2 - s) / 2, -0.3, 2.4, kind="b", hidden=False)
E.fn("e-b", lambda s: (4 - s) / 2, 0.6, 3.3, kind="b", hidden=False)
E.fn("e-c", lambda s: 2 * s, -0.2, 1.05, kind="c", hidden=False)
E.fn("e-d", lambda s: 2 * s - 5, 1.8, 3.3, kind="c", hidden=False)
F = w.Plot("f", (-0.6, 5.2), (-0.8, 5.8), w=440, h=500, xticks=[(2, "2"), (4, "4")], yticks=[(5, "5")],
           xname="u", yname="v")
F.fill("f-reg", [(2, 0), (4, 0), (4, 5), (2, 5)], kind="d", hidden=False)
F.curve("f-a", [(2, -0.4), (2, 5.5)], kind="b", hidden=False)
F.curve("f-b", [(4, -0.4), (4, 5.5)], kind="b", hidden=False)
F.curve("f-c", [(1.5, 0), (4.6, 0)], kind="c", hidden=False)
F.curve("f-d", [(1.5, 5), (4.6, 5)], kind="c", hidden=False)

# ---------------------------------------------------------------- exam 22A-A-Q4a
Q = BANK["22A-A-Q4a"]
assert "y^2=-4x" in Q["question"] and "e^{y-x}(2y+4)" in Q["question"]
U2, V2 = y - x, y**2 + 4*x
assert sp.simplify(U2.subs(y, x + 1)) == 1 and sp.simplify(U2.subs(y, x + 2)) == 2
assert sp.simplify(V2.subs(x, -y**2 / 4)) == 0 and sp.simplify(V2.subs(x, (9 - y**2) / 4)) == 9
Jinv2 = sp.Matrix([[sp.diff(U2, x), sp.diff(U2, y)], [sp.diff(V2, x), sp.diff(V2, y)]]).det()
assert sp.expand(Jinv2 - (-2*y - 4)) == 0
# inverse map: y = -2 +- sqrt(4+4u+v), x = y - u: two branches, so the curves bound two regions
for sgn in (1, -1):
    yy = -2 + sgn * sp.sqrt(4 + 4*u + v)
    assert sp.simplify(U2.subs({x: yy - u, y: yy}) - u) == 0 and sp.simplify(V2.subs({x: yy - u, y: yy}) - v) == 0
assert (-2 + sp.sqrt(4 + 4 + 0)) > 0                           # upper region: y >= -2 + sqrt(8) > 0
VAL = sp.integrate(sp.exp(u), (u, 1, 2), (v, 0, 9))
assert sp.simplify(VAL - 9 * sp.E * (sp.E - 1)) == 0
assert abs(float(VAL) - 42.03) < 0.01


def band(yy):
    lo, hi = max(yy - 2, -yy * yy / 4), min(yy - 1, (9 - yy * yy) / 4)
    return lo, max(lo, hi)


fxy = lambda xx, yy: math.exp(yy - xx) * (2 * yy + 4)
up = si.dblquad(fxy, -2, 4, lambda s: band(s)[0], lambda s: band(s)[1], epsabs=1e-9)[0]
dn = si.dblquad(fxy, -8, -2, lambda s: band(s)[0], lambda s: band(s)[1], epsabs=1e-9)[0]
assert abs(up - float(VAL)) < 1e-5 and abs(dn + float(VAL)) < 1e-5, (up, dn)


def branch_poly(sgn, n=60):
    pts = []
    for a, b in ([(1 + k / n, 0) for k in range(n + 1)] + [(2, 9 * k / n) for k in range(n + 1)]
                 + [(2 - k / n, 9) for k in range(n + 1)] + [(1, 9 - 9 * k / n) for k in range(n + 1)]):
        yy = -2 + sgn * math.sqrt(4 + 4 * a + b)
        pts.append((yy - a, yy))
    return pts


PU, PD = branch_poly(1), branch_poly(-1)
area_u = si.dblquad(lambda b, a: 1 / (2 * math.sqrt(4 + 4 * a + b)), 1, 2, 0, 9)[0]   # |J| = 1/|2y+4|
assert abs(w.shoelace(PU) - area_u) < 1e-2 and abs(w.shoelace(PD) - area_u) < 1e-2

X = w.Plot("x7", (-2.3, 2.6), (-0.6, 3.3), w=500, h=440, xticks=[(-2, "-2"), (-1, "-1"), (1, "1"), (2, "2")],
           yticks=[(1, "1"), (2, "2"), (3, "3")])
X.fill("x7-reg", PU, kind="d")
X.fn("x7-l1", lambda s: s + 1, -1.6, 2.2, kind="b")
X.fn("x7-l2", lambda s: s + 2, -2.2, 1.2, kind="b")
X.gx("x7-p1", lambda t: -t * t / 4, -0.5, 3.1, kind="c")
X.gx("x7-p2", lambda t: (9 - t * t) / 4, -0.5, 3.2, kind="c")
X.label("x7-t1", 1.6, 2.15, "y = x+1", kind="b")
X.label("x7-t2", -2.25, 1.15, "y = x+2", kind="b")
X.label("x7-t3", -2.25, 2.75, "y² = −4x", kind="c")
X.label("x7-t4", 1.55, 0.35, "y² = 9 − 4x", kind="c")
O = w.Plot("o", (-9.2, 2.6), (-7.0, 3.4), w=440, h=400, xticks=[], yticks=[], grid=False)
O.fill("o-up", PU, kind="d", hidden=False)
O.fill("o-dn", PD, kind="b")
O.fn("o-l1", lambda s: s + 1, -8.6, 2.0, kind="b", hidden=False)
O.fn("o-l2", lambda s: s + 2, -9.2, 1.2, kind="b", hidden=False)
O.gx("o-p1", lambda t: -t * t / 4, -6.2, 3.2, kind="c", hidden=False)
O.gx("o-p2", lambda t: (9 - t * t) / 4, -6.8, 3.4, kind="c", hidden=False)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לבחור משתנים חדשים, שהופכים תחום עקום למלבן."),
    P("נחשב את היעקוביאן דרך ההפוך, נציב, ונראה למה הערך המוחלט חשוב."),
    P("ובסוף נפתור שאלה ממבחן עם פרבולות, שיש בה מלכודת אמיתית.", hold=0.4),
], stage='<div class="kicker">I07 · אינטגרל כפול</div><h1>שינוי משתנים ליניארי והיעקוביאן</h1>'
         '<p>לבחור משתנים חדשים שהופכים את התחום למלבן, לחשב את היעקוביאן דרך ההפוך, ולחשב את האינטגרל.</p>',
   layout="title")

idea = Scene("idea", "הרעיון", [
    P("כשהתחום חסום בארבעה עקומים, מחפשים שני משתנים חדשים, $u$ ו-$v$, שבהם כל עקום הוא **קבוע**.",
      say="כשהתחום חסום בארבעה עקומים, מחפשים שני משתנים חדשים, יוּ ווִי, שבהם כל עקום הוא קבוע."),
    P("אז התחום הופך למלבן, והגבולות הם מספרים.", do=show("i-0")),
    P("אבל אלמנט השטח משתנה. מכפילים בערך המוחלט של היעקוביאן של $x$ ו-$y$ לפי $u$ ו-$v$.", do=show("i-1"),
      say="אבל אלמנט השטח משתנה. מכפילים בערך המוחלט של היעקוביאן של אִקְס ווַואי, לפי יוּ ווִי."),
    P("בדרך כלל נתונים $u$ ו-$v$ כפונקציות של $x$ ו-$y$. אז קל לחשב את היעקוביאן ההפוך.", do=show("i-2"),
      say="בדרך כלל נתונים יוּ ווִי כפונקציות של אִקְס ווַואי. אז קל לחשב את היעקוביאן ההפוך."),
    P("ומה שמציבים הוא אחת חלקי הערך המוחלט שלו.", do=show("i-c"), hold=0.4),
], stage=w.eqs("i", [
    "$R\\ \\longrightarrow\\ a\\le u\\le b,\\ \\ c\\le v\\le d$",
    "$\\displaystyle\\iint_R f\\,dx\\,dy=\\iint f\\cdot|J|\\,du\\,dv,\\qquad J=\\frac{\\partial(x,y)}{\\partial(u,v)}$",
    "$\\displaystyle |J|=\\frac{1}{|J^{-1}|},\\qquad J^{-1}=\\frac{\\partial(u,v)}{\\partial(x,y)}$",
], size=40, gap=40),
   panel=st.card("i-c", "rule", "🔑 מחשבים את ההפוך, ומציבים <b>אחת חלקי</b> הערך המוחלט שלו"))

ex = Scene("ex", "דוגמה", [
    P("דוגמה: התחום שבין $x+2y=2$ ל-$x+2y=4$, ובין $2x-y=0$ ל-$2x-y=5$.",
      say="דוגמה: התחום שבין אִקְס ועוד שתיים וַואי שווה שתיים, לאִקְס ועוד שתיים וַואי שווה ארבע, ובין שתיים אִקְס פחות וַואי שווה אפס, לשתיים אִקְס פחות וַואי שווה חמש."),
    P("שני זוגות של ישרים מקבילים: מקבילית. נבחר $u=x+2y$ ו-$v=2x-y$.", do=show("a-0"),
      say="שני זוגות של ישרים מקבילים: מקבילית. נבחר יוּ שווה אִקְס ועוד שתיים וַואי, ווִי שווה שתיים אִקְס פחות וַואי."),
    P("עכשיו $u$ בין שתיים לארבע, ו-$v$ בין אפס לחמש. מלבן.", do=show("a-1", "e-arr", "e-uv"),
      say="עכשיו יוּ בין שתיים לארבע, ווִי בין אפס לחמש. מלבן."),
    P("היעקוביאן ההפוך: הדטרמיננטה של הנגזרות. אחת, שתיים, שתיים, מינוס אחת. יוצא מינוס חמש.", do=show("a-2")),
    P("לכן מציבים חמישית: אחת חלקי הערך המוחלט של מינוס חמש.", do=show("a-3")),
    P("והאינטגרנד $x+2y$ הוא פשוט $u$. האינטגרל: חמישית, כפול האינטגרל של $u$ משתיים עד ארבע, כפול חמש.",
      do=show("a-4"),
      say="והאינטגרנד, אִקְס ועוד שתיים וַואי, הוא פשוט יוּ. האינטגרל: חמישית, כפול האינטגרל של יוּ משתיים עד ארבע, כפול חמש."),
    P("חמישית כפול שש כפול חמש: שש. ובאותה דרך השטח הוא שתיים.", do=show("a-5", "a-ok"), hold=0.4),
], stage='<div class="di-row">' + E.svg(scale=0.85) + '<div id="e-arr" class="di-big h">→</div>'
         + f'<div id="e-uv" class="h">{F.svg(scale=0.85)}</div></div>',
   panel=w.eqs("a", [
       "$u=x+2y,\\ \\ v=2x-y$",
       "$2\\le u\\le 4,\\ \\ 0\\le v\\le 5$",
       "$J^{-1}=\\det\\begin{pmatrix}1&2\\\\2&-1\\end{pmatrix}=-5$",
       "$dx\\,dy=\\dfrac15\\,du\\,dv$",
       "$\\displaystyle\\frac15\\int_2^4 u\\,du\\cdot\\int_0^5dv$",
       "$=\\dfrac15\\cdot6\\cdot5=6$",
   ], size=32, gap=10) + w.chip("a-ok", "✓ השטח: $\\tfrac15\\cdot2\\cdot5=2$"))

trap = Scene("trap", "המלכודת", [
    P("המלכודת הכי נפוצה: להציב את מינוס חמש, או חמש, במקום חמישית.", do=show("t-0")),
    P("מה שחישבנו הוא היעקוביאן **ההפוך**. מציבים אחת חלקי הערך המוחלט שלו.", do=show("t-1")),
    P("ואם היעקוביאן תלוי ב-$x$ וב-$y$, מבטאים אותו דרך $u$ ו-$v$, או מצמצמים אותו עם האינטגרנד.", do=show("t-2"),
      say="ואם היעקוביאן תלוי באִקְס ובוַואי, מבטאים אותו דרך יוּ ווִי, או מצמצמים אותו עם האינטגרנד.", hold=0.4),
], stage=w.eqs("tt", [
    "$J^{-1}=\\dfrac{\\partial(u,v)}{\\partial(x,y)}=-5$",
    "$dx\\,dy=\\dfrac15\\,du\\,dv$",
], size=50, gap=40, shown=2),
   panel=st.card("t-0", "trap", "⚠️ לא $-5$ ולא $5$: הגורם הוא $\\tfrac15$")
         + st.card("t-1", "rule", "🔑 ההופכי של הערך המוחלט")
         + st.card("t-2", "rule", "🔑 יעקוביאן עם $x,y$: לבטא או לצמצם"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: האינטגרל של $e^{y-x}$ כפול $2y+4$, על תחום שחסום בשני ישרים ובשתי פרבולות.",
      do=show("x7-l1", "x7-l2", "x7-p1", "x7-p2", "x7-t1", "x7-t2", "x7-t3", "x7-t4"),
      say="שאלה ממבחן: האינטגרל של אֵי בחזקת וַואי פחות אִקְס, כפול שתיים וַואי ועוד ארבע, על תחום שחסום בשני ישרים ובשתי פרבולות."),
    P("הישרים הם $y-x$ שווה אחת ושתיים. אז $u=y-x$, בין אחת לשתיים.", do=show("x-0"),
      say="הישרים הם, וַואי פחות אִקְס שווה אחת ושתיים. אז יוּ שווה וַואי פחות אִקְס, בין אחת לשתיים."),
    P("הפרבולות הן $y^2+4x$ שווה אפס ותשע. אז $v=y^2+4x$, בין אפס לתשע.", do=show("x-1", "x7-reg"),
      say="הפרבולות הן, וַואי בריבוע ועוד ארבע אִקְס, שווה אפס ותשע. אז וִי שווה וַואי בריבוע ועוד ארבע אִקְס, בין אפס לתשע."),
    P("היעקוביאן ההפוך: מינוס אחת, אחת, ארבע, שתיים $y$. יוצא מינוס שתיים $y$ פחות ארבע.", do=show("x-2"),
      say="היעקוביאן ההפוך: מינוס אחת, אחת, ארבע, שתיים וַואי. יוצא מינוס שתיים וַואי, פחות ארבע."),
    P("הוא תלוי ב-$y$, אבל זה בסדר: הגורם שמציבים הוא אחת חלקי $2y+4$ בערך מוחלט.", do=show("xp-0"),
      say="הוא תלוי בוַואי, אבל זה בסדר: הגורם שמציבים הוא אחת חלקי שתיים וַואי ועוד ארבע, בערך מוחלט."),
    P("ובתחום שלנו $y$ חיובי, אז $2y+4$ חיובי, והערך המוחלט פשוט נעלם.",
      say="ובתחום שלנו וַואי חיובי, אז שתיים וַואי ועוד ארבע חיובי, והערך המוחלט פשוט נעלם."),
    P("עכשיו רואים למה האינטגרנד בנוי ככה: $2y+4$ מצטמצם עם הגורם, ונשאר רק $e^u$.", do=show("xp-1"),
      say="עכשיו רואים למה האינטגרנד בנוי ככה: שתיים וַואי ועוד ארבע מצטמצם עם הגורם, ונשאר רק אֵי בחזקת יוּ."),
    P("האינטגרל של $e^u$ מאחת עד שתיים הוא $e^2-e$, וכפול האורך של $v$, תשע.", do=show("xp-2"),
      say="האינטגרל של אֵי בחזקת יוּ מאחת עד שתיים, הוא אֵי בריבוע פחות אֵי, וכפול האורך של וִי, תשע."),
    P("התשובה: תשע $e$ כפול $e$ פחות אחת. בערך ארבעים ושתיים.", do=show("x-ok"),
      say="התשובה: תשע אֵי, כפול, בסוגריים, אֵי פחות אחת. בערך ארבעים ושתיים."),
    P("ועכשיו המלכודת: הישרים חותכים כל פרבולה פעמיים. ארבעת העקומים סוגרים **שני** תחומים.", do=show("x-ov", "o-dn"),
      say="ועכשיו המלכודת: הישרים חותכים כל פרבולה פעמיים. ארבעת העקומים סוגרים שני תחומים."),
    P("בתחום השני $y$ קטן ממינוס שתיים, ושם $2y+4$ שלילי. הערך המוחלט מוסיף מינוס, ויוצא מינוס התשובה.",
      do=show("x-t"),
      say="בתחום השני, וַואי קטן ממינוס שתיים, ושם שתיים וַואי ועוד ארבע שלילי. הערך המוחלט מוסיף מינוס, ויוצא מינוס התשובה."),
    P("הפתרון הרשמי מחשב את התחום העליון. ובמבחן כדאי לכתוב במפורש על איזה תחום מדובר.", hold=0.4),
], stage='<div class="di-row">' + X.svg(scale=0.9) + f'<div id="x-ov" class="h">{O.svg(scale=0.85)}</div></div>'
         + w.eqs("x", [
             "$u=y-x\\in[1,2]$",
             "$v=y^2+4x\\in[0,9]$",
             "$J^{-1}=\\det\\begin{pmatrix}-1&1\\\\4&2y\\end{pmatrix}=-2y-4$",
         ], size=30, gap=4),
   panel=w.stem(Q["id"], "חשבו את $\\iint_De^{y-x}(2y+4)\\,dx\\,dy$, כאשר $D$ חסום על ידי "
                "$y-x=1$, $y=x+2$, $y^2=-4x$, $y^2=-4x+9$")
         + w.eqs("xp", [
             "$|J|=\\dfrac{1}{|2y+4|}=\\dfrac{1}{2y+4}\\ \\ (y>-2)$",
             "$\\displaystyle\\int_1^2\\!\\int_0^9 e^{u}\\,dv\\,du$",
             "$\\displaystyle=\\int_1^2e^u\\,du\\cdot\\int_0^9dv=9\\left(e^2-e\\right)$",
         ], size=30, gap=8)
         + w.chip("x-ok", "$=9e(e-1)\\approx 42.03$")
         + st.card("x-t", "trap", "⚠️ תחום שני, $y<-2$: שם יוצא $-9e(e-1)$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: בוחרים $u$ ו-$v$ כך שכל עקום גבול הוא קבוע, והתחום הופך למלבן.", do=show("z-1"),
      say="לסיכום: בוחרים יוּ ווִי כך שכל עקום גבול הוא קבוע, והתחום הופך למלבן."),
    P("מחשבים את היעקוביאן ההפוך, ומציבים אחת חלקי הערך המוחלט שלו.", do=show("z-2")),
    P("יעקוביאן שתלוי ב-$x$ וב-$y$ מבטאים או מצמצמים, ובודקים את הסימן שלו בתחום.", do=show("z-3"),
      say="יעקוביאן שתלוי באִקְס ובוַואי מבטאים או מצמצמים, ובודקים את הסימן שלו בתחום."),
    P("ושרטוט מראה אם העקומים סוגרים תחום אחד או יותר. נתראה ברמת הבוס.", do=show("z-4"), hold=0.6),
], stage='<div class="di-big">$\\displaystyle |J|=\\frac{1}{|J^{-1}|}$</div>',
   panel=st.card("z-1", "rule", "🔑 עקומים = קבועים, תחום = מלבן")
         + st.card("z-2", "rule", "🔑 אחת חלקי |ההפוך|")
         + st.card("z-3", "rule", "🔑 לבטא, לצמצם, לבדוק סימן")
         + st.card("z-4", "trap", "⚠️ כמה תחומים העקומים סוגרים?"))

VIDEO = Video("I07", "double_int", "שינוי משתנים ליניארי והיעקוביאן", [title, idea, ex, trap, exam, recap],
              bank={"22A-A-Q4a": None})
