# -*- coding: utf-8 -*-
"""I02 · סוג I וסוג II: פס אנכי ופס אופקי — video script (build: tools/video/vid.py I02).

Source: courses/double_int/C02.js (lesson + goal). Exam anchor: 25A-A-Q2b (the integral of (x-y)e^{x^2-y^2} over
the square bounded by y=1-x, y=3-x, y=x+1, y=x-1). This video does the region part: the square in vertical strips
and in horizontal strips (two pieces each, the area 2 both ways) and why that pushes the official solution to new
variables; the integral itself is finished in I04. Not used on purpose: the C02 quiz region (between y=x^2 and y=x,
with the integrands 1, y and x) and the bank's boss questions.
Every description is checked with sympy (same integrals of 1, x, y, xy, x^2y in both orders), every area asserted,
and every drawn polygon is checked against the sympy area.
"""
import math
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_double_int as w

x, y = sp.symbols("x y", real=True)

# ---------------------------------------------------------------- example: between y = x^2 and y = 2x
assert set(sp.solve(sp.Eq(x**2, 2*x), x)) == {0, 2}                    # meeting points x = 0, 2 -> (0,0), (2,4)
T1 = [("I", 0, 2, x**2, 2*x)]
T2 = [("II", 0, 4, y/2, sp.sqrt(y))]
assert w.same_region(T1, T2)
A = w.integrate(sp.Integer(1), T1)
assert A == sp.Rational(4, 3)
assert sp.integrate(2*x - x**2, (x, 0, 2)) == sp.Rational(4, 3)
assert sp.integrate(sp.sqrt(y) - y/2, (y, 0, 4)) == sp.Rational(4, 3)
assert sp.integrate(sp.sqrt(y), (y, 0, 4)) == sp.Rational(16, 3)
# in (0,2) the line is above the parabola (vertical strip: enters through the parabola) ...
assert all((2*x - x**2).subs(x, t) > 0 for t in (sp.Rational(1, 2), 1, sp.Rational(3, 2)))
# ... and in (0,4) the line x = y/2 is left of the parabola x = sqrt(y) (horizontal strip: enters through the line)
assert all((sp.sqrt(y) - y/2).subs(y, t) > 0 for t in (1, 2, 3))

poly = w.type1(lambda t: t * t, lambda t: 2 * t, 0, 2)
assert abs(w.shoelace(poly) - float(A)) < 1e-3


def example_plot(pfx):
    E = w.Plot(pfx, (-0.45, 2.75), (-0.4, 4.6), w=520, h=600, xticks=[(1, "1"), (2, "2")],
               yticks=[(1, "1"), (2, "2"), (3, "3"), (4, "4")])
    e = pfx + "-"
    E.fill(e + "reg", poly, kind="a", hidden=False)
    E.fn(e + "par", lambda t: t * t, -0.2, 2.12, kind="a", hidden=False)
    E.fn(e + "lin", lambda t: 2 * t, -0.15, 2.25, kind="b", hidden=False)
    E.label(e + "lp1", 1.65, 1.55, "y = x²", kind="a", hidden=False)
    E.label(e + "ll1", 1.1, 2.6, "y = 2x", kind="b", hidden=False, anchor="end")
    E.label(e + "lp2", 1.65, 1.0, "x = √y", kind="a")
    E.label(e + "ll2", 1.45, 3.4, "x = y/2", kind="b", anchor="end")
    E.dot(e + "v1", 0, 0, "(0,0)", dx=-14, dy=34, anchor="end", hidden=False)
    E.dot(e + "v2", 2, 4, "(2,4)", dx=16, dy=8, hidden=False)
    E.vstrip(e + "sv", 1, 1, 2)
    E.hstrip(e + "sh", 1, 0.5, 1)
    return E.svg()


E1, E2 = example_plot("e"), example_plot("f")

# ---------------------------------------------------------------- exam 25A-A-Q2b: the tilted square
Q = BANK["25A-A-Q2b"]
assert "y=1-x" in Q["question"] and "y=x-1" in Q["question"]
lines = {"a": 1 - x, "b": 3 - x, "c": x + 1, "d": x - 1}
verts = set()
for p in lines:
    for q in lines:
        if p < q:
            s = sp.solve(sp.Eq(lines[p], lines[q]), x)
            if s:
                verts.add((s[0], lines[p].subs(x, s[0])))
assert verts == {(0, 1), (1, 0), (2, 1), (1, 2)}
V2 = [("I", 0, 1, 1 - x, 1 + x), ("I", 1, 2, x - 1, 3 - x)]
H2 = [("II", 0, 1, 1 - y, 1 + y), ("II", 1, 2, y - 1, 3 - y)]
assert w.same_region(V2, H2)
assert w.integrate(sp.Integer(1), V2) == 2
assert sp.integrate(2*x, (x, 0, 1)) == 1 and sp.integrate(4 - 2*x, (x, 1, 2)) == 1
# the region really is the square between the four lines: a point inside satisfies 1<=x+y<=3, -1<=x-y<=1
assert w.integrate(sp.Integer(1), [("I", 0, 2, sp.Max(1 - x, x - 1), sp.Min(1 + x, 3 - x))]) == 2

X = w.Plot("x2", (-0.5, 2.8), (-0.5, 2.8), w=560, h=560, xticks=[], yticks=[])
pv1 = w.type1(lambda t: 1 - t, lambda t: 1 + t, 0, 1)
pv2 = w.type1(lambda t: t - 1, lambda t: 3 - t, 1, 2)
ph1 = w.type2(lambda t: 1 - t, lambda t: 1 + t, 0, 1)
ph2 = w.type2(lambda t: t - 1, lambda t: 3 - t, 1, 2)
assert all(abs(w.shoelace(p) - 1) < 1e-6 for p in (pv1, pv2, ph1, ph2))
X.fill("x2-sq", pv1 + pv2[::-1], kind="ink", hidden=False)
X.fill("x2-v1", pv1, kind="a")
X.fill("x2-v2", pv2, kind="d")
X.fill("x2-h1", ph1, kind="a")
X.fill("x2-h2", ph2, kind="d")
X.fn("x2-la", lambda t: 1 - t, -0.3, 1.25, kind="b", hidden=False)
X.fn("x2-lb", lambda t: 3 - t, 0.75, 2.4, kind="b", hidden=False)
X.fn("x2-lc", lambda t: t + 1, -0.3, 1.25, kind="c", hidden=False)
X.fn("x2-ld", lambda t: t - 1, 0.75, 2.4, kind="c", hidden=False)
X.curve("x2-cut", [(1, -0.35), (1, 2.6)], kind="ink", dash=True)
X.curve("x2-cuth", [(-0.35, 1), (2.6, 1)], kind="ink", dash=True)
X.vstrip("x2-s1", 0.5, 0.5, 1.5)
X.vstrip("x2-s2", 1.5, 0.5, 1.5)
X.hstrip("x2-t1", 0.5, 0.5, 1.5)
X.hstrip("x2-t2", 1.5, 0.5, 1.5)
X.dot("x2-p1", 1, 0, "(1,0)", dx=16, dy=34, kind="b")
X.dot("x2-p2", 1, 2, "(1,2)", dx=16, dy=-16, kind="b")
X.dot("x2-p3", 0, 1, "(0,1)", dx=-14, dy=-16, anchor="end", kind="b")
X.dot("x2-p4", 2, 1, "(2,1)", dx=16, dy=-16, kind="b")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נסרוק את אותו תחום בשתי דרכים: בפסים אנכיים ובפסים אופקיים."),
    P("נכתוב כל תיאור, נחשב עם שניהם, ונראה שיוצא אותו דבר."),
    P("ובסוף ניקח תחום ממבחן, ונגלה למה שתי הדרכים שם לא נוחות.", hold=0.4),
], stage='<div class="kicker">I02 · אינטגרל כפול</div><h1>סוג I וסוג II: פס אנכי ופס אופקי</h1>'
         '<p>לתאר אותו תחום גם כפסים אנכיים וגם כפסים אופקיים, ולחשב עם שניהם.</p>', layout="title")

idea = Scene("idea", "שתי סריקות", [
    P("**סוג I** הוא סריקה בפסים **אנכיים**: לכל $x$ קבוע, $y$ נע בין שני עקומים.", do=show("i-0"),
      say="סוג אחת הוא סריקה בפסים אנכיים: לכל אִקְס קבוע, וַואי נע בין שני עקומים."),
    P("אז הפנימי הוא לפי $y$, והחיצוני לפי $x$, בין מספרים.",
      say="אז הפנימי הוא לפי וַואי, והחיצוני לפי אִקְס, בין מספרים."),
    P("**סוג II** הוא סריקה בפסים **אופקיים**: לכל $y$ קבוע, $x$ נע בין שני עקומים.", do=show("i-1"),
      say="סוג שתיים הוא סריקה בפסים אופקיים: לכל וַואי קבוע, אִקְס נע בין שני עקומים."),
    P("ואז הפנימי לפי $x$, והחיצוני לפי $y$.", say="ואז הפנימי לפי אִקְס, והחיצוני לפי וַואי."),
    P("איך קוראים פס? מעבירים קו דרך התחום, ורואים באיזה עקום הוא נכנס ובאיזה הוא יוצא.", do=show("i-r")),
    P("הכניסה היא הגבול התחתון, והיציאה היא הגבול העליון.", do=show("i-key"), hold=0.4),
], stage=w.eqs("i", [
    "$\\displaystyle\\int_a^b\\!\\int_{g_1(x)}^{g_2(x)} f\\,dy\\,dx$",
    "$\\displaystyle\\int_c^d\\!\\int_{h_1(y)}^{h_2(y)} f\\,dx\\,dy$",
], size=50, gap=60),
   panel=st.card("i-r", "rule", "🔑 קו דרך התחום: נכנס בגבול התחתון, יוצא בגבול העליון")
         + '<div id="i-key" class="di-key h"><i class="in"></i>כניסה<i class="out"></i>יציאה</div>')

vert = Scene("vert", "פס אנכי", [
    P("הדוגמה: התחום שבין הפרבולה $y=x^2$ לישר $y=2x$.",
      say="הדוגמה: התחום שבין הפרבולה וַואי שווה אִקְס בריבוע, לישר וַואי שווה שתיים אִקְס."),
    P("קודם נקודות המפגש: $x^2=2x$ נותן $x=0$ או $x=2$, כלומר אפס אפס ושתיים ארבע.", do=show("v-0"),
      say="קודם נקודות המפגש: אִקְס בריבוע שווה שתיים אִקְס נותן אִקְס שווה אפס או שתיים, כלומר אפס אפס ושתיים ארבע."),
    P("עכשיו פס אנכי: הוא נכנס דרך הפרבולה, ויוצא דרך הישר.", do=show("e-sv")),
    P("לכן ב**סוג I**: $x$ בין אפס לשתיים, ו-$y$ מ-$x^2$ עד $2x$.", do=show("v-1"),
      say="לכן בסוג אחת: אִקְס בין אפס לשתיים, ווַואי מאִקְס בריבוע עד שתיים אִקְס."),
    P("השטח: האינטגרל מאפס עד שתיים של $2x-x^2$.", do=show("v-2"),
      say="השטח: האינטגרל מאפס עד שתיים של שתיים אִקְס פחות אִקְס בריבוע."),
    P("זה ארבע פחות שמונה שלישים, כלומר ארבעה שלישים.", do=show("v-3"), hold=0.4),
], stage=f'<div class="di-col">{E1}</div>',
   panel=w.eqs("v", [
       "$x^2=2x\\ \\Rightarrow\\ x=0,\\ 2$",
       "$0\\le x\\le 2,\\ \\ x^2\\le y\\le 2x$",
       "$\\displaystyle\\int_0^2 (2x-x^2)\\,dx$",
       "$=4-\\dfrac{8}{3}=\\dfrac{4}{3}$",
   ], size=40, gap=26))

horiz = Scene("horiz", "פס אופקי", [
    P("עכשיו אותו תחום, בפסים אופקיים. בשביל זה צריך לבודד את $x$ מכל עקום.", do=show("f-lp2", "f-ll2"),
      say="עכשיו אותו תחום, בפסים אופקיים. בשביל זה צריך לבודד את אִקְס מכל עקום."),
    P("הישר $y=2x$ הופך ל-$x=\\tfrac{y}{2}$, והפרבולה הופכת ל-$x=\\sqrt{y}$.", do=show("h-0"),
      say="הישר וַואי שווה שתיים אִקְס הופך לאִקְס שווה וַואי חלקי שתיים, והפרבולה הופכת לאִקְס שווה שורש וַואי."),
    P("פס אופקי נכנס משמאל דרך **הישר**, ויוצא מימין דרך **הפרבולה**.", do=show("f-sh")),
    P("שימו לב: בפס האנכי הישר היה הגבול העליון, ועכשיו הוא הגבול התחתון.", do=show("h-c")),
    P("לכן ב**סוג II**: $y$ בין אפס לארבע, ו-$x$ מ-$\\tfrac{y}{2}$ עד $\\sqrt{y}$.", do=show("h-1"),
      say="לכן בסוג שתיים: וַואי בין אפס לארבע, ואִקְס מוַואי חלקי שתיים עד שורש וַואי."),
    P("השטח: האינטגרל מאפס עד ארבע של $\\sqrt{y}-\\tfrac{y}{2}$.", do=show("h-2"),
      say="השטח: האינטגרל מאפס עד ארבע של שורש וַואי פחות וַואי חלקי שתיים."),
    P("שישה-עשר שלישים פחות ארבע: שוב ארבעה שלישים. אותו תחום, אותו שטח.", do=show("h-3", "h-ok"), hold=0.3),
    P("המלכודת: מ-$y=x^2$ יוצא $x=\\pm\\sqrt{y}$. לוקחים רק את הענף החיובי, כי התחום כולו ב-$x\\ge0$.",
      do=show("h-t"),
      say="המלכודת: מוַואי שווה אִקְס בריבוע יוצא אִקְס שווה פלוס מינוס שורש וַואי. לוקחים רק את הענף החיובי, כי התחום כולו באִקְס חיובי.",
      hold=0.4),
], stage=f'<div class="di-col">{E2}</div>',
   panel=w.eqs("h", [
       "$x=\\dfrac{y}{2},\\qquad x=\\sqrt{y}$",
       "$0\\le y\\le 4,\\ \\ \\dfrac{y}{2}\\le x\\le \\sqrt{y}$",
       "$\\displaystyle\\int_0^4 \\left(\\sqrt{y}-\\dfrac{y}{2}\\right)dy$",
       "$=\\dfrac{16}{3}-4=\\dfrac{4}{3}$",
   ], size=38, gap=18) + w.chip("h-ok", "✓ אותו שטח בשני הסדרים")
         + st.card("h-c", "rule", "🔑 עליון בסוג I יכול להיות שמאלי בסוג II")
         + st.card("h-t", "trap", "⚠️ $x=\\sqrt{y}$: רק הענף $x\\ge 0$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: אינטגרל על התחום שחסום בארבעה ישרים.", do=show("x-int")),
    P("הצעד הראשון הוא התחום: מחשבים את נקודות החיתוך של הישרים.", do=show("x2-p1", "x2-p2", "x2-p3", "x2-p4")),
    P("יוצא ריבוע מסובב, עם קודקודים בשתיים אחת, אחת שתיים, אפס אחת ואחת אפס."),
    P("פסים אנכיים: משמאל ל-$x=1$ הפס נכנס בישר $y=1-x$ ויוצא בישר $y=1+x$.",
      do=show("x2-v1", "x2-s1", "x2-cut", "x-v1"),
      say="פסים אנכיים: משמאל לאִקְס שווה אחת, הפס נכנס בישר וַואי שווה אחת פחות אִקְס, ויוצא בישר וַואי שווה אחת ועוד אִקְס."),
    P("אבל מימין ל-$x=1$ שני הגבולות משתנים: הפינות למטה ולמעלה שוברות את הנוסחה.",
      do=show("x2-v2", "x2-s2", "x-v2"),
      say="אבל מימין לאִקְס שווה אחת, שני הגבולות משתנים: הפינות למטה ולמעלה שוברות את הנוסחה."),
    P("אז בפסים אנכיים צריך **שני** אינטגרלים, וכל אחד מהם נותן שטח של אחת.", hold=0.3),
    P("ובפסים אופקיים? אותו דבר: הפינות משמאל ומימין שוברות ב-$y=1$.",
      do=hide("x2-v1", "x2-v2", "x2-s1", "x2-s2", "x2-cut") + show("x2-h1", "x2-h2", "x2-t1", "x2-t2", "x2-cuth", "x-h"),
      say="ובפסים אופקיים? אותו דבר: הפינות משמאל ומימין שוברות בוַואי שווה אחת."),
    P("שוב שני חלקים, ושוב שטח כולל שתיים. שני התיאורים נכונים, ושניהם מתפצלים.", do=show("x-a")),
    P("ועם אינטגרנד כמו $(x-y)\\,e^{x^2-y^2}$, גם שני אינטגרלים כאלה הם עבודה קשה מאוד.", do=show("x-t"),
      say="ועם אינטגרנד כמו אִקְס פחות וַואי, כפול אֵי בחזקת אִקְס בריבוע פחות וַואי בריבוע, גם שני אינטגרלים כאלה הם עבודה קשה מאוד."),
    P("לכן הפתרון הרשמי עובר למשתנים חדשים, שבהם הריבוע הופך למלבן. את זה נסיים בסרטון של רמה ארבע.",
      do=show("x-n"), hold=0.4),
], stage=f'<div class="di-col">{X.svg()}<div id="x-n" class="di-note h">ההמשך: משתנים חדשים, בסרטון של רמה 4</div></div>',
   panel=w.stem(Q["id"], "חשבו את $\\iint_R(x-y)e^{x^2-y^2}\\,dx\\,dy$, כאשר $R$ חסום על ידי "
                "$y=1-x,\\ y=3-x,\\ y=x+1,\\ y=x-1$")
         + '<span id="x-int"></span>'
         + st.card("x-sv", "ex", '<span id="x-v1" class="h">$0\\le x\\le1:\\ 1-x\\le y\\le 1+x$</span><br>'
                   '<span id="x-v2" class="h">$1\\le x\\le2:\\ x-1\\le y\\le 3-x$</span>').replace('card ex h', 'card ex')
         + st.card("x-h", "ex", "אופקי: גם שני חלקים, שבירה ב-$y=1$")
         + w.chip("x-a", "שטח: $1+1=2$ בשני הסדרים")
         + st.card("x-t", "trap", "⚠️ פינה בגבול: עוד אינטגרל")
)

recap = Scene("recap", "סיכום", [
    P("לסיכום: סוג I הוא פס אנכי, $dy\\,dx$. סוג II הוא פס אופקי, $dx\\,dy$.", do=show("z-1"),
      say="לסיכום: סוג אחת הוא פס אנכי, דִּי וַואי דִּי אִקְס. סוג שתיים הוא פס אופקי, דִּי אִקְס דִּי וַואי."),
    P("קוראים את הפס: נכנס בגבול התחתון, יוצא בגבול העליון.", do=show("z-2")),
    P("לסוג II מבודדים את $x$ מכל עקום, ובוחרים את הענף הנכון.", do=show("z-3"),
      say="לסוג שתיים מבודדים את אִקְס מכל עקום, ובוחרים את הענף הנכון."),
    P("ופינה בגבול מפצלת את האינטגרל לשניים. נתראה ברמה הבאה.", do=show("z-4"), hold=0.6),
], stage=w.eqs("zz", [
    "$\\displaystyle\\int_a^b\\!\\int_{g_1(x)}^{g_2(x)} f\\,dy\\,dx$",
    "$\\displaystyle\\int_c^d\\!\\int_{h_1(y)}^{h_2(y)} f\\,dx\\,dy$",
], size=46, gap=50, shown=2),
   panel=st.card("z-1", "rule", "🔑 סוג I: אנכי. סוג II: אופקי")
         + st.card("z-2", "rule", "🔑 כניסה = תחתון, יציאה = עליון")
         + st.card("z-3", "rule", "🔑 מבודדים $x$, ענף נכון")
         + st.card("z-4", "trap", "⚠️ פינה בגבול: שני אינטגרלים"))

VIDEO = Video("I02", "double_int", "סוג I וסוג II: פס אנכי ופס אופקי", [title, idea, vert, horiz, exam, recap],
              bank={"25A-A-Q2b": None})
