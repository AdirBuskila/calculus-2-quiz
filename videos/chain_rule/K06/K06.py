# -*- coding: utf-8 -*-
"""K06 · שני משתני ביניים — video script (build: tools/video/vid.py K06).

Source: courses/chain_rule/C06.js (lesson + goal). Exam anchor: 24S-A-Q1b (prove z_xx + z_yy = 0 for
z = e^(x-y) sin(x+y)). The bank solution differentiates directly with the product rule; the video solves it with the
level's tool instead: two intermediate variables u = x - y, v = x + y, z = F(u,v) = e^u sin v, z_x = F_u + F_v,
z_y = -F_u + F_v, and the same rule applied once more for the second derivatives. Both routes are asserted equal.
No guided level uses this part.
Not used on purpose: the C06 quiz (f(x+y, xy) g_x; f(x^2-y, xy) g_y, the lesson's example; f = u v^2 with
g = f(x+y, x-y) at (2,1); the findbug on f(xy, z^2-x); x z_x + y z_y for f(xy, x/y); e^(xy) with x = uv, y = 1/u).
The worked example is a new one: g = f(x y^2, x + y).
Every derivative is asserted with sympy (for a general f through several concrete f).
"""
import sympy as sp
from vid import P, Scene, Video, show, hide
import stage as st
import w_chain_rule as w
from w_chain_rule import x, y

uu, vv = sp.symbols("u v", real=True)
FS = [uu * vv, sp.sin(uu) * sp.exp(vv), uu**3 - uu * vv**2, sp.atan(uu + 2 * vv)]


def chain_ok(U, V, var, claim):
    """d/dvar f(U, V) == claim(f_u, f_v) for several concrete f; claim gets f_u, f_v already evaluated at (U, V)"""
    for f in FS:
        lhs = sp.diff(f.subs({uu: U, vv: V}, simultaneous=True), var)
        fu = sp.diff(f, uu).subs({uu: U, vv: V}, simultaneous=True)
        fv = sp.diff(f, vv).subs({uu: U, vv: V}, simultaneous=True)
        assert w.zero(lhs - claim(fu, fv)), (f, var)


# ---------------------------------------------------------------- verified math
U1, V1 = x * y**2, x + y
assert (sp.diff(U1, x), sp.diff(U1, y), sp.diff(V1, x), sp.diff(V1, y)) == (y**2, 2 * x * y, 1, 1)
chain_ok(U1, V1, x, lambda fu, fv: y**2 * fu + fv)
chain_ok(U1, V1, y, lambda fu, fv: 2 * x * y * fu + fv)
# the f_u/f_v swap is wrong (f = u v: y^2 v + u  vs  y^2 u + v)
assert sp.simplify(sp.diff(U1 * V1, x) - (y**2 * U1 + V1)) != 0
assert sp.expand(sp.diff(U1 * V1, x)) == 2 * x * y**2 + y**3

# exam 24S-A-Q1b
Z = sp.exp(x - y) * sp.sin(x + y)
U, V = x - y, x + y
assert (sp.diff(U, x), sp.diff(U, y), sp.diff(V, x), sp.diff(V, y)) == (1, -1, 1, 1)
FF = sp.exp(uu) * sp.sin(vv)
FU, FV = sp.diff(FF, uu), sp.diff(FF, vv)
assert FU == FF and FV == sp.exp(uu) * sp.cos(vv)
back = lambda e: e.subs({uu: U, vv: V}, simultaneous=True)
ZX = sp.exp(uu) * (sp.sin(vv) + sp.cos(vv))
ZY = sp.exp(uu) * (sp.cos(vv) - sp.sin(vv))
assert sp.simplify(sp.diff(Z, x) - back(FU + FV)) == 0 and sp.simplify(back(FU + FV) - back(ZX)) == 0
assert sp.simplify(sp.diff(Z, y) - back(-FU + FV)) == 0 and sp.simplify(back(-FU + FV) - back(ZY)) == 0
# second derivatives with the same rule: (.)_x = (.)_u + (.)_v, (.)_y = -(.)_u + (.)_v
GU, GV = sp.diff(ZX, uu), sp.diff(ZX, vv)
assert sp.simplify(GU - ZX) == 0 and sp.simplify(GV - sp.exp(uu) * (sp.cos(vv) - sp.sin(vv))) == 0
ZXX = sp.simplify(GU + GV)
assert sp.simplify(ZXX - 2 * sp.exp(uu) * sp.cos(vv)) == 0
HU, HV = sp.diff(ZY, uu), sp.diff(ZY, vv)
assert sp.simplify(HU - ZY) == 0 and sp.simplify(HV - sp.exp(uu) * (-sp.sin(vv) - sp.cos(vv))) == 0
ZYY = sp.simplify(-HU + HV)
assert sp.simplify(ZYY + 2 * sp.exp(uu) * sp.cos(vv)) == 0
assert sp.simplify(sp.diff(Z, x, 2) - back(ZXX)) == 0 and sp.simplify(sp.diff(Z, y, 2) - back(ZYY)) == 0
assert sp.simplify(sp.diff(Z, x, 2) + sp.diff(Z, y, 2)) == 0
# the bank pitfall: u_y = +1 (forgetting the minus of e^(x-y)) gives z_yy = +2 e^u cos v, and the sum is not 0
ZYp = FU + FV                                            # z_y with the sign slip
ZYYp = sp.diff(ZYp, uu) + sp.diff(ZYp, vv)
assert sp.simplify(ZYYp - 2 * sp.exp(uu) * sp.cos(vv)) == 0 and sp.simplify(ZXX + ZYYp) != 0

# ---------------------------------------------------------------- stage pieces
NODES = {"g": (250, 50, "g"), "u": (110, 190, "u"), "v": (390, 190, "v"), "x": (110, 340, "x"), "y": (390, 340, "y")}
OFF = {("g", "u"): (-48, -10), ("g", "v"): (48, -10), ("u", "x"): (-42, 0), ("v", "y"): (42, 0),
       ("u", "y"): (-58, -36), ("v", "x"): (58, -36)}
TREE = w.tree("t1", NODES, [("g", "u", "f_u"), ("g", "v", "f_v"), ("u", "x", "u_x"), ("u", "y", "u_y"),
                            ("v", "x", "v_x"), ("v", "y", "v_y")], w=500, h=390, label_off=OFF)
NODES2 = dict(NODES, g=(250, 50, "z"))
OFF2 = {("g", "u"): (-50, -10), ("g", "v"): (50, -10), ("u", "x"): (-34, 0), ("v", "y"): (34, 0),
        ("u", "y"): (-50, -36), ("v", "x"): (50, -36)}
ETREE = w.tree("t2", NODES2, [("g", "u", "F_u"), ("g", "v", "F_v"), ("u", "x", "1"), ("u", "y", "-1"),
                              ("v", "x", "1"), ("v", "y", "1")], w=500, h=390, label_off=OFF2, hidden=True)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("עד עכשיו היה בתוך הפונקציה ביטוי אחד. בסרטון הזה יהיו שניים."),
    P("נצייר עץ עם שני משתני ביניים, ונראה שהכלל נשאר אותו כלל: כופלים לאורך מסלול, ומחברים בין מסלולים."),
    P("ובסוף נוכיח זהות מסדר שני מתוך מבחן, בעזרת שני משתני ביניים.", hold=0.4),
], stage='<div class="kicker">K06 · כלל השרשרת והוכחת זהויות</div><h1>שני משתני ביניים</h1>'
         '<p>לגזור $f(u,v)$ כאשר $u$ ו-$v$ תלויים ב-$x,y$, ולצמצם את הנגזרות החלקיות של $f$.</p>', layout="title")

tree = Scene("tree", "העץ", [
    P("נתון $g=f(u,v)$, ו-$f$ כללית. עכשיו ל-$f$ יש שני משתנים, ולכן שתי נגזרות חלקיות: $f_u$ ו-$f_v$.", do=show("k-1"),
      say="נתון גִ'י שווה אֶף של יוּ ווִי, ואֶף כללית. עכשיו לאֶף יש שני משתנים, ולכן שתי נגזרות חלקיות: אֶף יוּ ואֶף וִי."),
    P("ו-$u$ ו-$v$ תלויים שניהם ב-$x$ וב-$y$. מכל משתנה יש **שני** מסלולים אל $g$.", do=show("t1-l-g-u", "t1-l-g-v"),
      say="ויוּ ווִי תלויים שניהם באִקְס ובוַואי. מכל משתנה יש שני מסלולים אל גִ'י."),
    P("אל $x$: מסלול דרך $u$, שנותן $f_u\\,u_x$.", do=show("t1-he-g-u", "t1-he-u-x", "t1-l-u-x"),
      say="אל אִקְס: מסלול דרך יוּ, שנותן אֶף יוּ כפול יוּ אִקְס."),
    P("ומסלול דרך $v$, שנותן $f_v\\,v_x$. מחברים.", do=show("t1-he-g-v", "t1-he-v-x", "t1-l-v-x", "k-2"),
      say="ומסלול דרך וִי, שנותן אֶף וִי כפול וִי אִקְס. מחברים."),
    P("ולפי $y$ אותו דבר: $g_y=f_u\\,u_y+f_v\\,v_y$.", do=hide("t1-he-u-x", "t1-he-v-x") + show("t1-he-u-y", "t1-he-v-y", "t1-l-u-y", "t1-l-v-y", "k-3"),
      say="ולפי וַואי אותו דבר: גִ'י וַואי שווה אֶף יוּ כפול יוּ וַואי, ועוד אֶף וִי כפול וִי וַואי."),
    P("$f_u$ ו-$f_v$ נשארים סימנים. אין צורך לדעת מי $f$.", do=show("k-c1"), hold=0.4,
      say="אֶף יוּ ואֶף וִי נשארים סימנים. אין צורך לדעת מי אֶף."),
], stage=w.row(TREE, w.lines("k", [("1", "g=f(u,v)"), ("2", "g_x=f_u\\,u_x+f_v\\,v_x"), ("3", "g_y=f_u\\,u_y+f_v\\,v_y")],
                             cls="sm")),
   panel=st.card("k-c1", "rule", "🔑 שני מסלולים לכל משתנה: שני מחוברים"))

example = Scene("example", "דוגמה", [
    P("דוגמה: $g=f(xy^2,\\;x+y)$. נסמן $u=xy^2$ ו-$v=x+y$.", do=show("e-1"),
      say="דוגמה: גִ'י שווה אֶף של אִקְס וַואי בריבוע, ואִקְס ועוד וַואי. נסמן יוּ שווה אִקְס וַואי בריבוע, ווִי שווה אִקְס ועוד וַואי."),
    P("ארבע נגזרות פנימיות: $u_x=y^2$, $u_y=2xy$, $v_x=1$, $v_y=1$.", do=show("e-2"),
      say="ארבע נגזרות פנימיות: יוּ אִקְס שווה וַואי בריבוע, יוּ וַואי שווה שתיים אִקְס וַואי, וִי אִקְס שווה אחת, ווִי וַואי שווה אחת."),
    P("מציבים: $g_x=y^2f_u+f_v$, ו-$g_y=2xy\\,f_u+f_v$.", do=show("e-3", "e-4"),
      say="מציבים: גִ'י אִקְס שווה וַואי בריבוע אֶף יוּ, ועוד אֶף וִי. וגִ'י וַואי שווה שתיים אִקְס וַואי אֶף יוּ, ועוד אֶף וִי."),
    P("בדיקה עם $f=uv$: אז $g=x^2y^2+xy^3$, והנגזרת הישירה לפי $x$ היא $2xy^2+y^3$.", do=show("e-5"),
      say="בדיקה עם אֶף שווה יוּ כפול וִי: אז גִ'י שווה אִקְס בריבוע וַואי בריבוע, ועוד אִקְס וַואי בשלישית. והנגזרת הישירה לפי אִקְס היא שתיים אִקְס וַואי בריבוע, ועוד וַואי בשלישית."),
    P("והנוסחה: $f_u=v$ ו-$f_v=u$, אז $y^2(x+y)+xy^2$. אותו דבר.", do=show("e-6"),
      say="והנוסחה: אֶף יוּ שווה וִי, ואֶף וִי שווה יוּ. אז וַואי בריבוע כפול אִקְס ועוד וַואי, ועוד אִקְס וַואי בריבוע. אותו דבר."),
    P("שתי מלכודות. הראשונה: כל נגזרת פנימית יושבת ליד ה-$f$ **שלה**. $u_x$ ליד $f_u$, ו-$v_x$ ליד $f_v$.", do=show("e-c1"),
      say="שתי מלכודות. הראשונה: כל נגזרת פנימית יושבת ליד האֶף שלה. יוּ אִקְס ליד אֶף יוּ, ווִי אִקְס ליד אֶף וִי."),
    P("השנייה: $f_u$ ו-$f_v$ לא מוכפלים זה בזה. כל אחד שייך למסלול אחר, ובין מסלולים מחברים.", do=show("e-c2"), hold=0.4,
      say="השנייה: אֶף יוּ ואֶף וִי לא מוכפלים זה בזה. כל אחד שייך למסלול אחר, ובין מסלולים מחברים."),
], stage=w.lines("e", [("1", "u=xy^2,\\quad v=x+y"),
                        ("2", "u_x=y^2,\\ \\ u_y=2xy,\\ \\ v_x=1,\\ \\ v_y=1"),
                        ("3", "g_x=y^2f_u+f_v"),
                        ("4", "g_y=2xy\\,f_u+f_v"),
                        ("5", "f=uv:\\ \\ g_x=2xy^2+y^3"),
                        ("6", "y^2(x+y)+xy^2=2xy^2+y^3\\ \\checkmark")], cls="sm"),
   panel=st.card("e-c1", "trap", "⚠️ $u_x$ ליד $f_u$, ו-$v_x$ ליד $f_v$")
         + st.card("e-c2", "trap", "⚠️ $f_u$ ו-$f_v$ לא מוכפלים זה בזה"))

exam1 = Scene("exam1", "שאלה ממבחן: נגזרות ראשונות", [
    P("סעיף ממבחן: הוכיחו ש-$z=e^{x-y}\\sin(x+y)$ מקיימת $z_{xx}+z_{yy}=0$.",
      say="סעיף ממבחן: הוכיחו שזֶד, אִי בחזקת אִקְס פחות וַואי, כפול סינוס של אִקְס ועוד וַואי, מקיימת זֶד אִקְס אִקְס ועוד זֶד וַואי וַואי שווה אפס."),
    P("אפשר לגזור ישירות בכלל המכפלה. אבל שימו לב לשני הביטויים: $x-y$ ו-$x+y$.",
      say="אפשר לגזור ישירות בכלל המכפלה. אבל שימו לב לשני הביטויים: אִקְס פחות וַואי, ואִקְס ועוד וַואי."),
    P("נסמן $u=x-y$ ו-$v=x+y$. אז $z=F(u,v)=e^u\\sin\\,v$: פונקציה פשוטה של שני משתני ביניים.", do=show("x-1", "x-1b", "t2-n-g", "t2-n-u", "t2-n-v", "t2-n-x", "t2-n-y", "t2-e-g-u", "t2-e-g-v", "t2-e-u-x", "t2-e-u-y", "t2-e-v-x", "t2-e-v-y"),
      say="נסמן יוּ שווה אִקְס פחות וַואי, ווִי שווה אִקְס ועוד וַואי. אז זֶד שווה אֶף גדולה של יוּ ווִי, אִי בחזקת יוּ כפול סינוס וִי: פונקציה פשוטה של שני משתני ביניים."),
    P("הנגזרות הפנימיות כולן אחת, חוץ מאחת: $u_y=-1$.", do=show("t2-l-u-x", "t2-l-u-y", "t2-l-v-x", "t2-l-v-y", "x-c1"),
      say="הנגזרות הפנימיות כולן אחת, חוץ מאחת: יוּ וַואי שווה מינוס אחת."),
    P("לכן הכלל פשוט: נגזרת לפי $x$ היא $F_u+F_v$, ולפי $y$ היא $-F_u+F_v$.", do=show("t2-l-g-u", "t2-l-g-v", "x-2", "x-2b"),
      say="לכן הכלל פשוט: נגזרת לפי אִקְס היא אֶף יוּ ועוד אֶף וִי, ולפי וַואי היא מינוס אֶף יוּ ועוד אֶף וִי."),
    P("כאן $F_u=e^u\\sin\\,v$, ו-$F_v=e^u\\cos\\,v$.", do=show("x-3"),
      say="כאן אֶף יוּ שווה אִי בחזקת יוּ סינוס וִי, ואֶף וִי שווה אִי בחזקת יוּ קוסינוס וִי."),
    P("ולכן $z_x=e^u(\\sin\\,v+\\cos\\,v)$, ו-$z_y=e^u(\\cos\\,v-\\sin\\,v)$.", do=show("x-4", "x-4b"), hold=0.4,
      say="ולכן זֶד אִקְס שווה אִי בחזקת יוּ, כפול סינוס וִי ועוד קוסינוס וִי. וזֶד וַואי שווה אִי בחזקת יוּ, כפול קוסינוס וִי פחות סינוס וִי."),
], stage=w.row(ETREE, w.lines("x", [("1", "u=x-y,\\ \\ v=x+y"), ("1b", "z=F(u,v)=e^u\\sin\\,v"),
                                     ("2", "(\\cdot)_x=(\\cdot)_u+(\\cdot)_v"), ("2b", "(\\cdot)_y=-(\\cdot)_u+(\\cdot)_v"),
                                     ("3", "F_u=e^u\\sin\\,v,\\ \\ F_v=e^u\\cos\\,v"),
                                     ("4", "z_x=e^u(\\sin\\,v+\\cos\\,v)"), ("4b", "z_y=e^u(\\cos\\,v-\\sin\\,v)")], cls="sm")),
   panel='<div class="qstem"><span class="qid">24S-A-Q1b</span>הוכיחו כי עבור $z(x,y)=e^{x-y}\\sin(x+y)$ '
         'מתקיים $z_{xx}+z_{yy}=0$ לכל $(x,y)$.</div>'
         + st.card("x-c1", "trap", "⚠️ $u_y=-1$: המינוס של $e^{x-y}$"))

exam2 = Scene("exam2", "שאלה ממבחן: נגזרות שניות", [
    P("הנגזרת השנייה היא נגזרת של $z_x$, ו-$z_x$ היא שוב פונקציה של $u$ ו-$v$. אז אותו כלל בדיוק.", do=show("y-0"),
      say="הנגזרת השנייה היא נגזרת של זֶד אִקְס, וזֶד אִקְס היא שוב פונקציה של יוּ ווִי. אז אותו כלל בדיוק."),
    P("לפי $u$: $z_x$ נשאר כמו שהוא. לפי $v$: יוצא $e^u(\\cos\\,v-\\sin\\,v)$.", do=show("y-1"),
      say="לפי יוּ: זֶד אִקְס נשאר כמו שהוא. לפי וִי: יוצא אִי בחזקת יוּ, כפול קוסינוס וִי פחות סינוס וִי."),
    P("מחברים, והסינוסים מתבטלים: $z_{xx}=2e^u\\cos\\,v$.", do=show("y-2"),
      say="מחברים, והסינוסים מתבטלים: זֶד אִקְס אִקְס שווה שתיים אִי בחזקת יוּ קוסינוס וִי."),
    P("עכשיו $z_{yy}$: מינוס הנגזרת של $z_y$ לפי $u$, ועוד הנגזרת לפי $v$.", do=show("y-3"),
      say="עכשיו זֶד וַואי וַואי: מינוס הנגזרת של זֶד וַואי לפי יוּ, ועוד הנגזרת לפי וִי."),
    P("יוצא $-e^u(\\cos\\,v-\\sin\\,v)+e^u(-\\sin\\,v-\\cos\\,v)$, כלומר $-2e^u\\cos\\,v$.", do=show("y-4"),
      say="יוצא מינוס אִי בחזקת יוּ, כפול קוסינוס וִי פחות סינוס וִי, ועוד אִי בחזקת יוּ, כפול מינוס סינוס וִי פחות קוסינוס וִי. כלומר מינוס שתיים אִי בחזקת יוּ קוסינוס וִי."),
    P("ובסכום: שתיים פחות שתיים. $z_{xx}+z_{yy}=0$, לכל $x$ ו-$y$.", do=show("y-5", "y-c1"),
      say="ובסכום: שתיים פחות שתיים. זֶד אִקְס אִקְס ועוד זֶד וַואי וַואי שווה אפס, לכל אִקְס ווַואי."),
    P("והמלכודת מהמבחן: מי ששכח את המינוס של $u_y$ קיבל $z_{yy}$ עם פלוס, והסכום לא התאפס.", do=show("y-c2"), hold=0.4,
      say="והמלכודת מהמבחן: מי ששכח את המינוס של יוּ וַואי, קיבל זֶד וַואי וַואי עם פלוס, והסכום לא התאפס."),
], stage=w.lines("y", [("0", "z_{xx}=(z_x)_u+(z_x)_v"),
                        ("1", "=e^u(\\sin\\,v+\\cos\\,v)+e^u(\\cos\\,v-\\sin\\,v)"),
                        ("2", "z_{xx}=2e^u\\cos\\,v"),
                        ("3", "z_{yy}=-(z_y)_u+(z_y)_v"),
                        ("4", "=-e^u(\\cos\\,v-\\sin\\,v)+e^u(-\\sin\\,v-\\cos\\,v)=-2e^u\\cos\\,v"),
                        ("5", "z_{xx}+z_{yy}=0\\ \\ \\checkmark")], cls="sm"),
   panel='<div class="qstem"><span class="qid">24S-A-Q1b</span>$z=e^u\\sin\\,v$, $u=x-y$, $v=x+y$</div>'
         + st.card("y-c1", "rule", "🔑 אותו כלל גם לנגזרת השנייה")
         + st.card("y-c2", "trap", "⚠️ בלי המינוס של $u_y$ הסכום לא מתאפס"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: עם שני משתני ביניים, מכל משתנה יש שני מסלולים, ולכן שני מחוברים.", do=show("s-1")),
    P("כל נגזרת פנימית יושבת ליד הנגזרת של $f$ שלה, ובין המסלולים מחברים.", do=show("s-2"),
      say="כל נגזרת פנימית יושבת ליד הנגזרת של אֶף שלה, ובין המסלולים מחברים."),
    P("וכשהביטויים הפנימיים פשוטים, הכלל נהיה קצר, ואפשר להפעיל אותו שוב לנגזרת השנייה. נתראה ברמה הבאה.", do=show("s-3"), hold=0.6),
], stage=TREE.replace("cr-elab h", "cr-elab").replace('id="t1', 'id="s1'),
   panel=st.card("s-1", "rule", "🔑 $g_x=f_u\\,u_x+f_v\\,v_x$")
         + st.card("s-2", "trap", "⚠️ $u_x$ ליד $f_u$, $v_x$ ליד $f_v$")
         + st.card("s-3", "ex", "$u=x-y$, $v=x+y$: $(\\cdot)_x=(\\cdot)_u+(\\cdot)_v$"))

VIDEO = Video("K06", "chain_rule", "שני משתני ביניים", [title, tree, example, exam1, exam2, recap],
              bank={"24S-A-Q1b": None})
