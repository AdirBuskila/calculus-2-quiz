# -*- coding: utf-8 -*-
"""I04 · בוחרים את הסדר הקל — video script (build: tools/video/vid.py I04).

Source: courses/double_int/C04.js (lesson + goal). Exam anchor: 25A-A-Q2b, solved up to the area factor: the official
substitution u=x-y, v=x+y turns the tilted square (I02 drew it) into the rectangle -1<=u<=1, 1<=v<=3; the area factor (1/2, asserted below) is NOT named on screen, it is the C07-Q5
answer: the video writes dA = c du dv, 'computed in level 7', and stops at c(2/3 sinh 3 - 2 sinh 1)
and the integrand u e^{uv}; the choice of order is the point of this level: dv first makes the factor u cancel.
The substitution itself is level 7 material and is only stated and checked here. Not used on purpose: the C04
quiz integrands (e^{x^2} with y/2<=x<=1, sin(y)/y, e^{y^2}, sin(y^2)) and the boss questions 26A-A-Q1a, 25A-A-Q4a.
All values are sympy-exact, the exam value is also checked by a direct numeric integral over the square in x, y.
"""
import math
import sympy as sp
from scipy import integrate as si
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_double_int as w

x, y, u, v, t = sp.symbols("x y u v t", real=True)

# ---------------------------------------------------------------- example: int_0^1 int_{sqrt y}^1 e^{x^3} dx dy
G = [("II", 0, 1, sp.sqrt(y), 1)]
N = [("I", 0, 1, 0, x**2)]
assert w.same_region(G, N)
inner = sp.integrate(sp.exp(x**3), (y, 0, x**2))
assert sp.simplify(inner - x**2 * sp.exp(x**3)) == 0
val = sp.integrate(inner, (x, 0, 1))
assert sp.simplify(val - (sp.E - 1) / 3) == 0
assert sp.diff(sp.exp(x**3) / 3, x) == x**2 * sp.exp(x**3)          # the antiderivative after the swap
# e^{x^3} has no elementary antiderivative in x: sympy answers with a special function
assert sp.integrate(sp.exp(x**3), x).has(sp.lowergamma, sp.uppergamma, sp.gamma)

E = w.Plot("e", (-0.3, 1.45), (-0.3, 1.35), w=520, h=520, xticks=[(1, "1")], yticks=[(1, "1")])
pe = w.type1(lambda s: 0.0, lambda s: s * s, 0, 1)
assert abs(w.shoelace(pe) - 1 / 3) < 1e-3
E.fill("e-reg", pe, kind="a", hidden=False)
E.fn("e-c", lambda s: s * s, -0.1, 1.15, kind="a", hidden=False)
E.curve("e-r", [(1, -0.15), (1, 1.25)], kind="b", hidden=False)
E.label("e-lc", 0.5, 0.62, "x = √y", kind="a", hidden=False, anchor="end")
E.label("e-lc2", 0.5, 0.45, "y = x²", kind="a", anchor="end")
E.label("e-lr", 1.08, 0.15, "x = 1", kind="b", hidden=False)
E.hstrip("e-sh", 0.36, 0.6, 1)
E.vstrip("e-sv", 0.75, 0, 0.5625)

# ---------------------------------------------------------------- exam 25A-A-Q2b, to the end
Q = BANK["25A-A-Q2b"]
assert "e^{x^2-y^2}" in Q["question"]
U, V = x - y, x + y
# the four lines in u, v: y=x+1 -> u=-1, y=x-1 -> u=1, y=1-x -> v=1, y=3-x -> v=3
assert sp.simplify(U.subs(y, x + 1)) == -1 and sp.simplify(U.subs(y, x - 1)) == 1
assert sp.simplify(V.subs(y, 1 - x)) == 1 and sp.simplify(V.subs(y, 3 - x)) == 3
Jinv = sp.Matrix([[sp.diff(U, x), sp.diff(U, y)], [sp.diff(V, x), sp.diff(V, y)]]).det()
assert Jinv == 2                                                   # so |dx dy| = 1/2 du dv
assert sp.expand((x - y) * (x + y) - (x**2 - y**2)) == 0           # x^2-y^2 = uv
# order dv first: the u cancels
in_v = sp.integrate(u * sp.exp(u * v), (v, 1, 3))
assert sp.simplify(in_v - (sp.exp(3*u) - sp.exp(u))) == 0
VAL = sp.Rational(1, 2) * sp.integrate(sp.exp(3*u) - sp.exp(u), (u, -1, 1))
assert sp.simplify(VAL - ((sp.exp(3) - sp.exp(-3)) / 6 - (sp.E - sp.exp(-1)) / 2)) == 0
assert sp.simplify((VAL - (sp.sinh(3) / 3 - sp.sinh(1))).rewrite(sp.exp)) == 0
# order du first: integration by parts, and pieces like e^v / v that have no elementary antiderivative alone
vp = sp.Symbol("v", positive=True)                                 # v runs over [1, 3]
in_u = sp.integrate(u * sp.exp(u * vp), (u, -1, 1))
assert sp.simplify(in_u - (sp.exp(vp) * (1 / vp - 1 / vp**2) + sp.exp(-vp) * (1 / vp + 1 / vp**2))) == 0
assert sp.integrate(sp.exp(vp) / vp, vp).has(sp.Ei)
# the value checked directly in x, y over the square (two vertical pieces), numerically
fnum = lambda yy, xx: (xx - yy) * math.exp(xx * xx - yy * yy)
num = (si.dblquad(fnum, 0, 1, lambda s: 1 - s, lambda s: 1 + s)[0]
       + si.dblquad(fnum, 1, 2, lambda s: s - 1, lambda s: 3 - s)[0])
assert abs(num - float(VAL)) < 1e-8, (num, float(VAL))
assert abs(float(VAL) - 2.1638) < 1e-3
INNER = sp.integrate(sp.exp(3*u) - sp.exp(u), (u, -1, 1))          # what the video shows, times the factor c
assert sp.simplify((INNER - (sp.Rational(2, 3) * sp.sinh(3) - 2 * sp.sinh(1))).rewrite(sp.exp)) == 0

S = w.Plot("sq", (-0.4, 2.6), (-0.4, 2.6), w=330, h=330, xticks=[], yticks=[])
S.fill("sq-r", [(0, 1), (1, 0), (2, 1), (1, 2)], kind="d", hidden=False)
for i, (f, a, b, k) in enumerate([(lambda s: 1 - s, -0.2, 1.2, "b"), (lambda s: 3 - s, 0.8, 2.2, "b"),
                                  (lambda s: s + 1, -0.2, 1.2, "c"), (lambda s: s - 1, 0.8, 2.2, "c")]):
    S.fn(f"sq-l{i}", f, a, b, kind=k, hidden=False)
R = w.Plot("uv", (-1.7, 1.7), (-0.4, 3.6), w=360, h=380, xticks=[(-1, "-1"), (1, "1")],
           yticks=[(1, "1"), (3, "3")], xname="u", yname="v")
R.fill("uv-r", [(-1, 1), (1, 1), (1, 3), (-1, 3)], kind="d", hidden=False)
R.curve("uv-b", [(-1.4, 1), (1.4, 1)], kind="b", hidden=False)
R.curve("uv-t", [(-1.4, 3), (1.4, 3)], kind="b", hidden=False)
R.curve("uv-l", [(-1, 0.7), (-1, 3.3)], kind="c", hidden=False)
R.curve("uv-rr", [(1, 0.7), (1, 3.3)], kind="c", hidden=False)
R.vstrip("uv-s", 0.45, 1, 3)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("שני סדרי האינטגרציה נותנים אותו ערך, אבל לא באותה קלות."),
    P("בסרטון הזה נלמד לזהות אינטגרנד שאי אפשר לחשב בסדר הנתון, ולבחור את הסדר שכן עובד."),
    P("ובסוף נפתור עד הסוף שאלה ממבחן, שבה הבחירה הנכונה חוסכת את כל העבודה.", hold=0.4),
], stage='<div class="kicker">I04 · אינטגרל כפול</div><h1>בוחרים את הסדר הקל</h1>'
         '<p>לזהות אינטגרנד שאין לו פונקציה קדומה אלמנטרית בסדר הנתון, להחליף סדר ולחשב.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("יש פונקציות שאין להן פונקציה קדומה אלמנטרית: אין נוסחה סגורה לאינטגרל שלהן.", do=show("i-0")),
    P("הדוגמאות המוכרות: $e^{x^2}$, סינוס של $x^2$, קוסינוס של $x^2$, וסינוס $x$ חלקי $x$.", do=show("i-1"),
      say="הדוגמאות המוכרות: אֵי בחזקת אִקְס בריבוע, סינוס של אִקְס בריבוע, קוסינוס של אִקְס בריבוע, וסינוס אִקְס חלקי אִקְס."),
    P("ואם אינטגרל פנימי מבקש לאנטגרל אחת מהן לפי המשתנה שלה, נתקענו.", do=show("i-c1")),
    P("הפתרון: להחליף סדר, כך שהפנימי יהיה לפי **המשתנה השני**.", do=show("i-c2")),
    P("אז הפונקציה הבעייתית קבועה בתוך הפנימי, והוא רק כופל אותה באורך הפס.", do=show("i-2")),
    P("ואורך הפס הזה הוא בדיוק הגורם שחסר כדי שתהיה פונקציה קדומה.", hold=0.4),
], stage=w.eqs("i", [
    "$\\displaystyle\\int e^{x^2}\\,dx=\\ ?$",
    "$e^{x^2},\\quad \\sin(x^2),\\quad \\cos(x^2),\\quad \\dfrac{\\sin x}{x}$",
    "$\\displaystyle\\int_0^{g(x)} e^{x^2}\\,dy=g(x)\\,e^{x^2}$",
], size=46, gap=40),
   panel=st.card("i-c1", "trap", "⚠️ אין פונקציה קדומה אלמנטרית בסדר הנתון")
         + st.card("i-c2", "rule", "🔑 הפנימי לפי <b>המשתנה השני</b>: הבעייתית קבועה בו"))

ex = Scene("ex", "דוגמה", [
    P("נתון האינטגרל מאפס עד אחת, של האינטגרל משורש $y$ עד אחת, של $e^{x^3}$, לפי $x$.", do=show("a-0"),
      say="נתון האינטגרל מאפס עד אחת, של האינטגרל משורש וַואי עד אחת, של אֵי בחזקת אִקְס בשלישית, לפי אִקְס."),
    P("הפנימי לפי $x$, ול-$e^{x^3}$ אין פונקציה קדומה אלמנטרית. אז מחליפים סדר.", do=show("a-x"),
      say="הפנימי לפי אִקְס, ולאֵי בחזקת אִקְס בשלישית אין פונקציה קדומה אלמנטרית. אז מחליפים סדר."),
    P("התחום: $y$ בין אפס לאחת, ו-$x$ משורש $y$ עד אחת. זה פס אופקי מהעקום עד הישר $x=1$.", do=show("e-sh"),
      say="התחום: וַואי בין אפס לאחת, ואִקְס משורש וַואי עד אחת. זה פס אופקי מהעקום עד הישר אִקְס שווה אחת."),
    P("העקום $x=\\sqrt{y}$ הוא גם $y=x^2$. אז בפסים אנכיים: $x$ מאפס עד אחת, ו-$y$ מאפס עד $x^2$.",
      do=hide("e-sh") + show("e-sv", "e-lc2", "a-1"),
      say="העקום אִקְס שווה שורש וַואי, הוא גם וַואי שווה אִקְס בריבוע. אז בפסים אנכיים: אִקְס מאפס עד אחת, ווַואי מאפס עד אִקְס בריבוע."),
    P("עכשיו הפנימי לפי $y$. האינטגרנד לא תלוי ב-$y$, אז הוא רק כופל את אורך הפס, $x^2$.", do=show("a-2"),
      say="עכשיו הפנימי לפי וַואי. האינטגרנד לא תלוי בוַואי, אז הוא רק כופל את אורך הפס, אִקְס בריבוע."),
    P("ונשאר $x^2e^{x^3}$. ואת זה כבר יודעים: הצבה $t=x^3$, כי $x^2$ הוא כמעט הנגזרת של $x^3$.", do=show("a-3"),
      say="ונשאר אִקְס בריבוע, כפול אֵי בחזקת אִקְס בשלישית. ואת זה כבר יודעים: הצבה טִי שווה אִקְס בשלישית, כי אִקְס בריבוע הוא כמעט הנגזרת של אִקְס בשלישית."),
    P("הפונקציה הקדומה היא שליש $e^{x^3}$, ובין אפס לאחת מקבלים $e$ פחות אחת, חלקי שלוש.", do=show("a-4", "a-ok"),
      say="הפונקציה הקדומה היא שליש אֵי בחזקת אִקְס בשלישית, ובין אפס לאחת מקבלים אֵי פחות אחת, חלקי שלוש."),
    P("שימו לב מאיפה הגיע ה-$x^2$: מאורך הפס. החילוף הוא שיצר את הגורם שהיה חסר.", do=show("a-c"), hold=0.4,
      say="שימו לב מאיפה הגיע האִקְס בריבוע: מאורך הפס. החילוף הוא שיצר את הגורם שהיה חסר."),
], stage=f'<div class="di-col">{E.svg()}</div>',
   panel=w.eqs("a", [
       "$\\displaystyle\\int_0^1\\!\\int_{\\sqrt{y}}^{1} e^{x^3}\\,dx\\,dy$",
       "$\\displaystyle=\\int_0^1\\!\\int_{0}^{x^2} e^{x^3}\\,dy\\,dx$",
       "$\\displaystyle=\\int_0^1 x^2e^{x^3}\\,dx$",
       "$=\\dfrac{e^{1}}{3}-\\dfrac{e^{0}}{3}$",
       "$\\displaystyle=\\frac{e-1}{3}$",
   ], size=36, gap=12)
         + '<div class="di-row"><span id="a-x" class="di-chip bad h">✗ לפי $x$ קודם</span>'
           '<span id="a-ok" class="di-chip ok h">✓ לפי $y$ קודם</span></div>'
         + st.card("a-c", "rule", "🔑 אורך הפס $x^2$ הוא הגורם שהיה חסר"))

trap = Scene("trap", "המלכודת", [
    P("והמלכודת: להחליף רק את $dx$ ו-$dy$, ולהשאיר את הגבולות.", do=show("t-0", "t-x"),
      say="והמלכודת: להחליף רק את דִּי אִקְס ודִּי וַואי, ולהשאיר את הגבולות."),
    P("החילוף הוא של **התחום**, לא של האינטגרנד. בלי שרטוט, הגבולות החדשים יוצאים שגויים.", do=show("t-c1")),
    P("והבדיקה: אחרי חילוף נכון, הפנימי צריך להיות קל, ולתת בדיוק את הגורם שחסר.", do=show("t-c2"),
      hold=0.4),
], stage='<div class="di-col"><div id="t-0" class="di-big h">'
         '$\\displaystyle\\int_0^1\\!\\int_{\\sqrt{y}}^{1} e^{x^3}\\,dy\\,dx$</div>'
         '<div id="t-x" class="di-chip bad h">✗ אותם גבולות, רק סדר אחר: לא חילוף</div></div>',
   panel=st.card("t-c1", "trap", "⚠️ מחליפים את <b>התחום</b>: משרטטים וקוראים מחדש")
         + st.card("t-c2", "rule", "🔑 אחרי החילוף: פנימי קל, והגורם החסר מופיע"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: האינטגרל של $(x-y)\\,e^{x^2-y^2}$ על הריבוע המסובב שראינו ברמה שתיים.",
      say="שאלה ממבחן: האינטגרל של אִקְס פחות וַואי, כפול אֵי בחזקת אִקְס בריבוע פחות וַואי בריבוע, על הריבוע המסובב שראינו ברמה שתיים."),
    P("בפסים אנכיים ובפסים אופקיים הוא מתפצל. לכן הפתרון עובר למשתנים $u=x-y$ ו-$v=x+y$.", do=show("xs-0"),
      say="בפסים אנכיים ובפסים אופקיים הוא מתפצל. לכן הפתרון עובר למשתנים יוּ שווה אִקְס פחות וַואי, ווִי שווה אִקְס ועוד וַואי."),
    P("את הבחירה של המשתנים נלמד ברמה שבע. מה שחשוב עכשיו: הישרים הופכים לקבועים.", do=show("uv"),
      say="את הבחירה של המשתנים נלמד ברמה שבע. מה שחשוב עכשיו: הישרים הופכים לקבועים."),
    P("$u$ בין מינוס אחת לאחת, $v$ בין אחת לשלוש: מלבן. אלמנט השטח מקבל גורם קבוע $c$, שנחשב ברמה שבע.",
      do=show("xs-1"),
      say="יוּ בין מינוס אחת לאחת, וִי בין אחת לשלוש: מלבן. אלמנט השטח מקבל גורם קבוע, סִי, שנחשב ברמה שבע."),
    P("והאינטגרנד? $x^2-y^2$ הוא $(x-y)(x+y)$, כלומר $uv$. אז מקבלים $u\\,e^{uv}$.", do=show("xs-2"),
      say="והאינטגרנד? אִקְס בריבוע פחות וַואי בריבוע, הוא אִקְס פחות וַואי כפול אִקְס ועוד וַואי, כלומר יוּ וִי. אז מקבלים יוּ כפול אֵי בחזקת יוּ וִי."),
    P("ועכשיו השאלה של הרמה הזאת: לפי איזה משתנה קודם?", hold=0.3),
    P("אם לפי $u$ קודם, צריך אינטגרציה בחלקים, ויוצאים איברים כמו $e^v$ חלקי $v$, שאין להם פונקציה קדומה אלמנטרית לבד.",
      do=show("x-bad"),
      say="אם לפי יוּ קודם, צריך אינטגרציה בחלקים, ויוצאים איברים כמו אֵי בחזקת וִי חלקי וִי, שאין להם פונקציה קדומה אלמנטרית לבד."),
    P("אבל לפי $v$ קודם, $u$ הוא קבוע. הפונקציה הקדומה של $u\\,e^{uv}$ לפי $v$ היא פשוט $e^{uv}$.",
      do=show("uv-s", "xp-0"),
      say="אבל לפי וִי קודם, יוּ הוא קבוע. הפונקציה הקדומה של יוּ כפול אֵי בחזקת יוּ וִי, לפי וִי, היא פשוט אֵי בחזקת יוּ וִי."),
    P("ה-$u$ מצטמצם. בין אחת לשלוש מקבלים $e^{3u}-e^{u}$.",
      say="היוּ מצטמצם. בין אחת לשלוש מקבלים אֵי בחזקת שלוש יוּ, פחות אֵי בחזקת יוּ."),
    P("ונשאר $c$ כפול האינטגרל ממינוס אחת עד אחת של $e^{3u}-e^{u}$: שתי אקספוננטות פשוטות.", do=show("xp-1"),
      say="ונשאר סִי, כפול האינטגרל ממינוס אחת עד אחת, של אֵי בחזקת שלוש יוּ פחות אֵי בחזקת יוּ: שתי אקספוננטות פשוטות."),
    P("יוצא $c$ כפול, בסוגריים, שני שלישים סינוס היפרבולי של שלוש, פחות פעמיים סינוס היפרבולי של אחת.",
      do=show("xp-2", "x-ok"),
      say="יוצא סִי כפול, בסוגריים, שני שלישים סינוס היפרבולי של שלוש, פחות פעמיים סינוס היפרבולי של אחת."),
    P("את $c$ נחשב ברמה שבע, ואז הסעיף נגמר. מה שחשוב כאן: הסדר הנכון הפך את החישוב לקצר.",
      say="את סִי נחשב ברמה שבע, ואז הסעיף נגמר. מה שחשוב כאן: הסדר הנכון הפך את החישוב לקצר."),
    P("המלכודת: לבחור את הסדר מתוך הרגל. בדקו קודם איזה סדר מצמצם את הגורם שמפריע.", hold=0.4),
], stage='<div class="di-col"><div class="di-row">' + S.svg(cls="") + '<div id="x-arrow" class="di-big">→</div>'
         + f'<div id="uv" class="h">{R.svg()}</div></div>'
         + w.eqs("xs", [
             "$u=x-y,\\ \\ v=x+y$",
             "$-1\\le u\\le 1,\\ \\ 1\\le v\\le 3,\\ \\ dA=c\\,du\\,dv$",
             "$\\displaystyle c\\int_{-1}^{1}\\!\\int_{1}^{3} u\\,e^{uv}\\,dv\\,du$",
         ], size=34, gap=8) + '</div>',
   panel=w.stem(Q["id"], "חשבו את $\\iint_R(x-y)e^{x^2-y^2}\\,dx\\,dy$, כאשר $R$ חסום על ידי "
                "$y=1-x,\\ y=3-x,\\ y=x+1,\\ y=x-1$")
         + st.card("x-bad", "trap", "⚠️ לפי $u$ קודם: חלקים, ו-$\\frac{e^v}{v}$")
         + w.eqs("xp", [
             "$\\displaystyle\\int_1^3 u\\,e^{uv}\\,dv=e^{3u}-e^{u}$",
             "$\\displaystyle c\\int_{-1}^{1}\\left(e^{3u}-e^{u}\\right)du$",
             "$=c\\left(\\tfrac23\\sinh(3)-2\\sinh(1)\\right)$",
         ], size=32, gap=8)
         + w.chip("x-ok", "✓ לפי $v$ קודם"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: ל-$e^{x^2}$, לסינוס ולקוסינוס של $x^2$, ולסינוס $x$ חלקי $x$ אין פונקציה קדומה אלמנטרית.",
      do=show("z-1"),
      say="לסיכום: לאֵי בחזקת אִקְס בריבוע, לסינוס ולקוסינוס של אִקְס בריבוע, ולסינוס אִקְס חלקי אִקְס, אין פונקציה קדומה אלמנטרית."),
    P("כשהן מופיעות בפנימי, מחליפים סדר כך שהפנימי יהיה לפי המשתנה השני.", do=show("z-2")),
    P("החילוף הוא של התחום: משרטטים וקוראים מחדש.", do=show("z-3")),
    P("ובכל אינטגרל, שואלים קודם: איזה סדר מצמצם את מה שמפריע? נתראה ברמה הבאה.", do=show("z-4"), hold=0.6),
], stage='<div class="di-big">$\\displaystyle\\int_0^{g(x)} e^{x^2}\\,dy=g(x)\\,e^{x^2}$</div>',
   panel=st.card("z-1", "rule", "🔑 $e^{x^2},\\ \\sin x^2,\\ \\cos x^2,\\ \\frac{\\sin x}{x}$: בלי קדומה")
         + st.card("z-2", "rule", "🔑 הפנימי לפי המשתנה השני")
         + st.card("z-3", "trap", "⚠️ מחליפים תחום, לא אותיות")
         + st.card("z-4", "rule", "🔑 הסדר שמצמצם"))

VIDEO = Video("I04", "double_int", "בוחרים את הסדר הקל", [title, idea, ex, trap, exam, recap],
              bank={"25A-A-Q2b": None})
