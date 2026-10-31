# -*- coding: utf-8 -*-
"""K07 · חישוב בנקודה, הרכבה קבועה והומוגניות — video script (build: tools/video/vid.py K07).

Source: courses/chain_rule/C07.js (lesson + goal). Exam anchor: 24S-A-Q5a (5z^3 + 3xyz - x^2y^2 + 1 = 0 defines z(x,y)
near (1,-1,0); compute z_x(1,-1) + z_y(1,-1)). F(x, y, z(x,y)) = 0 for all (x,y) is a constant composite, so its
derivative is 0, and everything is evaluated at one point: the two ideas of this level. No guided level uses it.
Not used on purpose: the C07 quiz (z = u^2 + 3uv with u = x^2 y, v = x - y at (1,1), z_x and z_y, the lesson's own
table; f(t^2, 3t) = 5 with f_x(4,6) = 3; Euler's identity for x^3 F(z/x, y/x) and its findbug) and 24A-A-Q3b (the
Euler proof, a C07 quiz question): the homogeneity part of the level is only named in the recap, not solved.
The worked examples are new ones: z = uv + v^2 with u = x^2 - y, v = xy at (1,1); f(t^3, 2t) = c with f_y(1,2) = 6.
Every number is asserted with sympy.
"""
import sympy as sp
from vid import P, Scene, Video, show, hide
import stage as st
import w_chain_rule as w
from w_chain_rule import x, y, z

# ---------------------------------------------------------------- verified math
u, v, t = sp.symbols("u v t", real=True)
ZUV = u * v + v**2
UX, VX = x**2 - y, x * y
P0 = {x: 1, y: 1}
u0, v0 = UX.subs(P0), VX.subs(P0)
assert (u0, v0) == (0, 1)
zu0, zv0 = sp.diff(ZUV, u).subs({u: u0, v: v0}), sp.diff(ZUV, v).subs({u: u0, v: v0})
assert (zu0, zv0) == (1, 2)
ders = [sp.diff(UX, x).subs(P0), sp.diff(UX, y).subs(P0), sp.diff(VX, x).subs(P0), sp.diff(VX, y).subs(P0)]
assert ders == [2, -1, 1, 1]
zx0, zy0 = zu0 * ders[0] + zv0 * ders[2], zu0 * ders[1] + zv0 * ders[3]
assert (zx0, zy0) == (4, 1)
DIRECT = ZUV.subs({u: UX, v: VX})
assert (sp.diff(DIRECT, x).subs(P0), sp.diff(DIRECT, y).subs(P0)) == (4, 1)
# "substitute first" gives the derivative of a constant: wrong
assert sp.diff(DIRECT.subs(P0), x) == 0

# constant composite f(t^3, 2t) = c: 3t^2 f_x + 2 f_y = 0; at t = 1 the point is (1, 2)
fx, fy = sp.symbols("f_x f_y")
eq = 3 * t**2 * fx + 2 * fy
assert (t**3, 2 * t) == (t**3, 2 * t) and ((t**3).subs(t, 1), (2 * t).subs(t, 1)) == (1, 2)
assert sp.solve(eq.subs({t: 1, fy: 6}), fx) == [-4]
# check the rule on a concrete f with f(t^3, 2t) constant: f = x - (y/2)^3 + 7
fc = x - (y / 2)**3 + 7
assert sp.simplify(fc.subs({x: t**3, y: 2 * t}) - 7) == 0
at_curve = {x: t**3, y: 2 * t}
assert sp.simplify(sp.diff(fc, x).subs(at_curve) * 3 * t**2 + sp.diff(fc, y).subs(at_curve) * 2) == 0

# exam 24S-A-Q5a
F = 5 * z**3 + 3 * x * y * z - x**2 * y**2 + 1
PT = {x: 1, y: -1, z: 0}
assert F.subs(PT) == 0
FX, FY, FZ = (sp.diff(F, s) for s in (x, y, z))
assert FX == 3 * y * z - 2 * x * y**2 and FY == 3 * x * z - 2 * x**2 * y and FZ == 15 * z**2 + 3 * x * y
assert (FX.subs(PT), FY.subs(PT), FZ.subs(PT)) == (-2, 2, -3)
ZX, ZY = -FX.subs(PT) / FZ.subs(PT), -FY.subs(PT) / FZ.subs(PT)
assert (ZX, ZY) == (sp.Rational(-2, 3), sp.Rational(2, 3)) and ZX + ZY == 0
# the chain-rule derivation of z_x = -F_x/F_z: d/dx F(x, y, Z(x,y)) = F_x + F_z Z_x
Zf = sp.Function("Z")(x, y)
d = sp.diff(F.subs(z, Zf), x)
assert sp.simplify(d - (FX.subs(z, Zf) + FZ.subs(z, Zf) * sp.Derivative(Zf, x))) == 0
# the sign slip z_x = F_x / F_z would give +2/3 and -2/3: the sum is still 0 (the question does not catch it),
# so the video stresses the sign on z_x and z_y themselves
assert FX.subs(PT) / FZ.subs(PT) == sp.Rational(2, 3)

# ---------------------------------------------------------------- stage pieces
TREE = w.tree("t1", {"F": (250, 50, "F"), "z": (250, 195, "z"), "x": (90, 340, "x"), "y": (410, 340, "y")},
              [("F", "x", "F_x"), ("F", "y", "F_y"), ("F", "z", "F_z"), ("z", "x", "z_x"), ("z", "y", "z_y")],
              w=500, h=390, hidden=True, bend={("F", "x"): 55, ("F", "y"): -55},
              label_off={("F", "x"): (-46, -10), ("F", "y"): (46, -10), ("F", "z"): (36, 0),
                         ("z", "x"): (10, 30), ("z", "y"): (-10, 30)})

ROWS = [("u,\\ v", "0,\\ 1"), ("z_u,\\ z_v", "1,\\ 2"), ("u_x,\\ u_y", "2,\\ -1"), ("v_x,\\ v_y", "1,\\ 1")]
TABLE = ('<table class="delta" dir="ltr"><tbody>'
         + "".join(f'<tr id="tb-{i}" class="h"><th>${a}$</th><td>${b}$</td></tr>' for i, (a, b) in enumerate(ROWS))
         + "</tbody></table>")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה כלל השרשרת יוצא מהוכחת הזהויות, ופוגש מספרים."),
    P("נחשב נגזרת בנקודה מתוך טבלה, ונגזור הרכבה שערכה קבוע."),
    P("ובסוף נפתור סעיף ממבחן, שבו שני הרעיונות נפגשים בפונקציה סתומה.", hold=0.4),
], stage='<div class="kicker">K07 · כלל השרשרת והוכחת זהויות</div><h1>חישוב בנקודה, הרכבה קבועה והומוגניות</h1>'
         '<p>לחשב נגזרות חלקיות של הרכבה בנקודה מתוך נתונים, ולגזור הרכבה קבועה.</p>', layout="title")

point = Scene("point", "חישוב בנקודה", [
    P("נתון $z=uv+v^2$, כש-$u=x^2-y$ ו-$v=xy$. מה $z_x$ בנקודה אחת, אחת?", do=show("p-1"),
      say="נתון זֶד שווה יוּ וִי ועוד וִי בריבוע, כשיוּ שווה אִקְס בריבוע פחות וַואי, ווִי שווה אִקְס וַואי. מה זֶד אִקְס בנקודה אחת, אחת?"),
    P("בונים טבלה. קודם מחשבים את $u$ ו-$v$ בנקודה: $u=0$ ו-$v=1$.", do=show("tb-0"),
      say="בונים טבלה. קודם מחשבים את יוּ ווִי בנקודה: יוּ שווה אפס, ווִי שווה אחת."),
    P("אחר כך את הנגזרות של $z$ לפי $u$ ו-$v$, בערכים האלה: $z_u=v=1$, $z_v=u+2v=2$.", do=show("tb-1"),
      say="אחר כך את הנגזרות של זֶד לפי יוּ ווִי, בערכים האלה: זֶד יוּ שווה וִי, כלומר אחת. וזֶד וִי שווה יוּ ועוד שתיים וִי, כלומר שתיים."),
    P("ואת הנגזרות הפנימיות בנקודה: $u_x=2x=2$, $u_y=-1$, $v_x=y=1$, $v_y=x=1$.", do=show("tb-2", "tb-3"),
      say="ואת הנגזרות הפנימיות בנקודה: יוּ אִקְס שווה שתיים, יוּ וַואי מינוס אחת, וִי אִקְס אחת, ווִי וַואי אחת."),
    P("כופלים לאורך המסלולים ומחברים: $z_x=1\\cdot2+2\\cdot1=4$.", do=show("p-2"),
      say="כופלים לאורך המסלולים ומחברים: זֶד אִקְס שווה אחת כפול שתיים, ועוד שתיים כפול אחת. כלומר ארבע."),
    P("ו-$z_y=1\\cdot(-1)+2\\cdot1=1$. אפשר לוודא בגזירה ישירה, ויוצא אותו דבר.", do=show("p-3"),
      say="וזֶד וַואי שווה אחת כפול מינוס אחת, ועוד שתיים כפול אחת. כלומר אחת. אפשר לוודא בגזירה ישירה, ויוצא אותו דבר."),
    P("והכלל: **גוזרים לפני שמציבים**. מי שמציב קודם, גוזר מספר, ומקבל אפס.", do=show("p-c1"), hold=0.4),
], stage=w.row(TABLE, w.lines("p", [("1", "z=uv+v^2,\\ \\ u=x^2-y,\\ \\ v=xy"),
                                     ("2", "z_x=z_u\\,u_x+z_v\\,v_x=4"),
                                     ("3", "z_y=z_u\\,u_y+z_v\\,v_y=1")], cls="sm")),
   panel=st.card("p-c1", "trap", "⚠️ גוזרים <b>לפני</b> שמציבים"))

const = Scene("const", "הרכבה קבועה", [
    P("רעיון שני: נתון שההרכבה $f(t^3,2t)$ שווה לקבוע, לכל $t$.", do=show("c-1"),
      say="רעיון שני: נתון שההרכבה, אֶף של טִי בשלישית ושתיים טִי, שווה לקבוע, לכל טִי."),
    P("פונקציה קבועה, הנגזרת שלה אפס. ובכלל השרשרת, שני מסלולים: דרך $x$ ודרך $y$.", do=show("c-2"),
      say="פונקציה קבועה, הנגזרת שלה אפס. ובכלל השרשרת, שני מסלולים: דרך אִקְס ודרך וַואי."),
    P("לכן $f_x\\cdot3t^2+f_y\\cdot2=0$, בנקודה $(t^3,2t)$.", do=show("c-3"),
      say="לכן אֶף אִקְס כפול שלוש טִי בריבוע, ועוד אֶף וַואי כפול שתיים, שווה אפס, בנקודה טִי בשלישית ושתיים טִי."),
    P("ב-$t=1$ זו הנקודה אחת, שתיים. אם נתון שם $f_y=6$, אז $3f_x+12=0$, ו-$f_x=-4$.", do=show("c-4"),
      say="בטִי שווה אחת זו הנקודה אחת, שתיים. אם נתון שם אֶף וַואי שווה שש, אז שלוש אֶף אִקְס ועוד שתים עשרה שווה אפס, ואֶף אִקְס שווה מינוס ארבע."),
    P("ולא היינו צריכים לדעת מי $f$. רק שההרכבה קבועה.", do=show("c-c1"), hold=0.4,
      say="ולא היינו צריכים לדעת מי אֶף. רק שההרכבה קבועה."),
], stage=w.lines("c", [("1", "f(t^3,2t)=c\\quad\\forall t"),
                        ("2", "\\frac{d}{dt}f(t^3,2t)=0"),
                        ("3", "f_x\\cdot 3t^2+f_y\\cdot 2=0"),
                        ("4", "t=1:\\ \\ 3f_x(1,2)+2\\cdot6=0\\ \\Rightarrow\\ f_x(1,2)=-4")], cls="c"),
   panel=st.card("c-c1", "rule", "🔑 הרכבה קבועה: הנגזרת שלה <b>אפס</b>"))

exam1 = Scene("exam1", "שאלה ממבחן: הפונקציה הסתומה", [
    P("סעיף ממבחן: הראו שהמשוואה מגדירה פונקציה יחידה ליד אחת, מינוס אחת, אפס, וחשבו את $z_x+z_y$ שם.",
      say="סעיף ממבחן: הראו שהמשוואה מגדירה פונקציה יחידה ליד אחת, מינוס אחת, אפס, וחשבו את זֶד אִקְס ועוד זֶד וַואי שם."),
    P("נסמן $F$ את אגף שמאל. בנקודה: אפס, ועוד אפס, פחות אחת, ועוד אחת. כלומר אפס.", do=show("a-1"),
      say="נסמן אֶף גדולה את אגף שמאל. בנקודה: אפס, ועוד אפס, פחות אחת, ועוד אחת. כלומר אפס."),
    P("$F$ פולינום, ולכן גזירה ברציפות. ו-$F_z=15z^2+3xy$, שבנקודה שווה מינוס שלוש. שונה מאפס.", do=show("a-2", "a-3"),
      say="אֶף גדולה היא פולינום, ולכן גזירה ברציפות. ואֶף זֶד שווה חמש עשרה זֶד בריבוע ועוד שלוש אִקְס וַואי, שבנקודה שווה מינוס שלוש. שונה מאפס."),
    P("לפי משפט הפונקציה הסתומה יש פונקציה יחידה $z(x,y)$ ליד הנקודה, עם $z(1,-1)=0$.", do=show("a-4"),
      say="לפי משפט הפונקציה הסתומה יש פונקציה יחידה, זֶד של אִקְס וַואי, ליד הנקודה, וזֶד שם שווה אפס."),
    P("ועכשיו הקשר לרמה: $F(x,y,z(x,y))=0$ לכל $x,y$. זו **הרכבה קבועה**.", do=show("t1-n-F", "t1-n-z", "t1-n-x", "t1-n-y", "t1-e-F-x", "t1-e-F-y", "t1-e-F-z", "t1-e-z-x", "t1-e-z-y", "a-c1"),
      say="ועכשיו הקשר לרמה: אֶף גדולה של אִקְס, וַואי, וזֶד של אִקְס וַואי, שווה אפס לכל אִקְס ווַואי. זו הרכבה קבועה."),
    P("בעץ, מ-$F$ אל $x$ יש שני מסלולים: ישיר, ודרך $z$.", do=show("t1-he-F-x", "t1-he-F-z", "t1-he-z-x", "t1-l-F-x", "t1-l-F-z", "t1-l-z-x"),
      say="בעץ, מאֶף גדולה אל אִקְס יש שני מסלולים: ישיר, ודרך זֶד."),
    P("לכן $F_x+F_z\\,z_x=0$, ומכאן $z_x=-\\frac{F_x}{F_z}$. אותו דבר עם $y$.", do=show("a-5"), hold=0.4,
      say="לכן אֶף אִקְס ועוד אֶף זֶד כפול זֶד אִקְס שווה אפס, ומכאן זֶד אִקְס שווה מינוס אֶף אִקְס חלקי אֶף זֶד. אותו דבר עם וַואי."),
], stage=w.row(TREE, w.lines("a", [("1", "F(1,-1,0)=0"),
                                    ("2", "F\\in C^1"),
                                    ("3", "F_z(1,-1,0)=-3\\ne0"),
                                    ("4", "z=z(x,y),\\ \\ z(1,-1)=0"),
                                    ("5", "F_x+F_z\\,z_x=0\\ \\Rightarrow\\ z_x=-\\frac{F_x}{F_z}")], cls="sm")),
   panel='<div class="qstem"><span class="qid">24S-A-Q5a</span>נתונה המשוואה $5z^3+3xyz-x^2y^2+1=0$. '
         'הראו שהיא מגדירה בסביבת $(1,-1,0)$ פונקציה יחידה $z=z(x,y)$, וחשבו את $z_x(1,-1)+z_y(1,-1)$.</div>'
         + st.card("a-c1", "rule", "🔑 $F(x,y,z(x,y))\\equiv0$: הרכבה קבועה"))

exam2 = Scene("exam2", "שאלה ממבחן: בנקודה", [
    P("עכשיו מספרים. $F_x=3yz-2xy^2$. בנקודה $z=0$, ולכן נשאר רק מינוס שתיים.", do=show("b-1"),
      say="עכשיו מספרים. אֶף אִקְס שווה שלוש וַואי זֶד, פחות שתיים אִקְס וַואי בריבוע. בנקודה זֶד שווה אפס, ולכן נשאר רק מינוס שתיים."),
    P("$F_y=3xz-2x^2y$. שוב $z=0$ מוחק את המחובר הראשון, ונשאר פלוס שתיים.", do=show("b-2"),
      say="אֶף וַואי שווה שלוש אִקְס זֶד, פחות שתיים אִקְס בריבוע וַואי. שוב זֶד שווה אפס מוחק את המחובר הראשון, ונשאר פלוס שתיים."),
    P("שימו לב כמה מחוברים נעלמים כי $z=0$ בנקודה. כדאי לראות את זה לפני שמחשבים הכול.", do=show("b-c1"),
      say="שימו לב כמה מחוברים נעלמים כי זֶד שווה אפס בנקודה. כדאי לראות את זה לפני שמחשבים הכול."),
    P("עכשיו $z_x=-\\frac{F_x}{F_z}$: מינוס, מינוס שתיים חלקי מינוס שלוש. כלומר מינוס שני שלישים.", do=show("b-3"),
      say="עכשיו זֶד אִקְס שווה מינוס אֶף אִקְס חלקי אֶף זֶד: מינוס, מינוס שתיים חלקי מינוס שלוש. כלומר מינוס שני שלישים."),
    P("ו-$z_y$: מינוס, שתיים חלקי מינוס שלוש. כלומר שני שלישים.", do=show("b-4"),
      say="וזֶד וַואי: מינוס, שתיים חלקי מינוס שלוש. כלומר שני שלישים."),
    P("הסכום: מינוס שני שלישים ועוד שני שלישים, אפס.", do=show("b-5")),
    P("והמלכודת: המינוס בנוסחה. הוא מגיע מהעברת אגף במשוואה של ההרכבה הקבועה.", do=show("b-c2"), hold=0.4,
      say="והמלכודת: המינוס בנוסחה. הוא מגיע מהעברת אגף במשוואה של ההרכבה הקבועה."),
], stage=w.lines("b", [("1", "F_x=3yz-2xy^2\\ \\to\\ -2"),
                        ("2", "F_y=3xz-2x^2y\\ \\to\\ 2"),
                        ("3", "z_x=-\\frac{-2}{-3}=-\\frac23"),
                        ("4", "z_y=-\\frac{2}{-3}=\\frac23"),
                        ("5", "z_x+z_y=0")], cls="c"),
   panel='<div class="qstem"><span class="qid">24S-A-Q5a</span>בנקודה $(1,-1,0)$: $F_z=-3$</div>'
         + st.card("b-c1", "trap", "⚠️ $z=0$ בנקודה: מחוברים נעלמים. בודקים קודם")
         + st.card("b-c2", "trap", "⚠️ $z_x=-\\frac{F_x}{F_z}$: לא לשכוח את המינוס"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: בחישוב בנקודה בונים טבלה, וגוזרים לפני שמציבים.", do=show("s-1")),
    P("הרכבה שערכה קבוע נגזרת לאפס, וכלל השרשרת נותן ממנה משוואה על הנגזרות החלקיות.", do=show("s-2")),
    P("פונקציה סתומה היא בדיוק הרכבה כזו, ומשם מגיעה הנוסחה עם המינוס.", do=show("s-3")),
    P("ובפונקציה הומוגנית, אותו כלל שרשרת נותן את זהות אוילר. נתראה בשלב הגמר.", do=show("s-4"), hold=0.6),
], stage=TREE.replace("cr-node h", "cr-node").replace("cr-edge h", "cr-edge").replace("cr-elab h", "cr-elab")
               .replace('id="t1', 'id="s1'),
   panel=st.card("s-1", "rule", "🔑 טבלה: ערכים, נגזרות, כפל וחיבור")
         + st.card("s-2", "rule", "🔑 הרכבה קבועה: נגזרת אפס")
         + st.card("s-3", "ex", "$z_x=-\\frac{F_x}{F_z}$, $z_y=-\\frac{F_y}{F_z}$")
         + st.card("s-4", "ex", "הומוגניות: אותו כלל, זהות אוילר"))

VIDEO = Video("K07", "chain_rule", "חישוב בנקודה, הרכבה קבועה והומוגניות", [title, point, const, exam1, exam2, recap],
              bank={"24S-A-Q5a": None})
