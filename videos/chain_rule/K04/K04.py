# -*- coding: utf-8 -*-
"""K04 · הצבה בזהות: ה-g' מצטמצם — video script (build: tools/video/vid.py K04).

Source: courses/chain_rule/C04.js (lesson + goal). No bank anchor (bank={}): the only unused identity parts of the
bank are twins of a quiz or boss question (24A-B-Q3b = boss 22A-A-Q1b, 23A-C-Q3b = C04 quiz 25A-A-Q3b), and the other
unused chain-rule parts (gradients, implicit functions) do not exercise this level's skill. Coordinator decision:
the "exam" scene is an original exam-style identity, z = y^2/(2x) + g(y/x) satisfies x z_x + y z_y = y^2/(2x),
built like the real exam parts (a free term + g of a ratio), and it is labelled as exam-style, not as a bank question.
Not used on purpose: the C04 quiz (order proof for x^2 g(y/x); g(x^2+y^2) twice; k for x^3 g(y/x^2)), 25A-A-Q3b and
its twin 23A-C-Q3b, and 24A-B-Q3b (twin of the boss question 22A-A-Q1b).
The worked example is a new one: z = e^y g(x - y) satisfies z_x + z_y = z.
Every derivative and identity is asserted with sympy for several concrete g.
"""
import sympy as sp
from vid import P, Scene, Video, show, hide
import stage as st
import w_chain_rule as w
from w_chain_rule import x, y

# ---------------------------------------------------------------- verified math
T = x - y
assert (sp.diff(T, x), sp.diff(T, y)) == (1, -1)
Z1 = lambda g: sp.exp(y) * g(T)
w.for_all_g(lambda g, gp, gpp: sp.diff(Z1(g), x) - sp.exp(y) * gp(T))
w.for_all_g(lambda g, gp, gpp: sp.diff(Z1(g), y) - (sp.exp(y) * g(T) - sp.exp(y) * gp(T)))
w.for_all_g(lambda g, gp, gpp: sp.diff(Z1(g), x) + sp.diff(Z1(g), y) - Z1(g))                # z_x + z_y = z
# the sign slip t_y = +1 leaves 2 e^y g'(t): the g' does not cancel
w.for_all_g(lambda g, gp, gpp: (sp.exp(y) * gp(T)) + (sp.exp(y) * g(T) + sp.exp(y) * gp(T))
            - (Z1(g) + 2 * sp.exp(y) * gp(T)))

# exam-style identity (no bank anchor): z = y^2/(2x) + g(y/x),  x z_x + y z_y = y^2/(2x)
TE = y / x
assert sp.simplify(sp.diff(TE, x) + y / x**2) == 0 and sp.simplify(sp.diff(TE, y) - 1 / x) == 0
Z = lambda g: y**2 / (2 * x) + g(TE)
w.for_all_g(lambda g, gp, gpp: sp.diff(Z(g), x) - (-y**2 / (2 * x**2) - y / x**2 * gp(TE)))
w.for_all_g(lambda g, gp, gpp: sp.diff(Z(g), y) - (y / x + gp(TE) / x))
w.for_all_g(lambda g, gp, gpp: x * (-y**2 / (2 * x**2) - y / x**2 * gp(TE)) - (-y**2 / (2 * x) - y / x * gp(TE)))
w.for_all_g(lambda g, gp, gpp: y * (y / x + gp(TE) / x) - (y**2 / x + y / x * gp(TE)))
w.for_all_g(lambda g, gp, gpp: x * sp.diff(Z(g), x) + y * sp.diff(Z(g), y) - y**2 / (2 * x))      # the identity
assert sp.simplify(-y**2 / (2 * x) + y**2 / x - y**2 / (2 * x)) == 0                               # what is left
# the trap: t_x = +y/x^2 (lost minus) leaves 2(y/x) g'(t)
w.for_all_g(lambda g, gp, gpp: (x * (-y**2 / (2 * x**2) + y / x**2 * gp(TE)) + y * sp.diff(Z(g), y))
            - (y**2 / (2 * x) + 2 * y / x * gp(TE)))

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נסגור את שאלת הוכחת הזהות מההתחלה ועד הסוף."),
    P("נכיר מתכון של חמישה צעדים, ונראה את הסימן הכי חשוב בדרך: ה-$g'$ שמצטמצם.",
      say="נכיר מתכון של חמישה צעדים, ונראה את הסימן הכי חשוב בדרך: הגִ'י תָּג שמצטמצם."),
    P("ובסוף נפתור שאלה מלאה בסגנון המבחנים.", hold=0.4),
], stage='<div class="kicker">K04 · כלל השרשרת והוכחת זהויות</div><h1>הצבה בזהות: ה-g\' מצטמצם</h1>'
         '<p>להציב את $z_x$ ו-$z_y$ באגף שמאל של המשוואה, לראות את $g\'$ מצטמצם, ולהשוות את מה שנשאר לאגף ימין.</p>',
   layout="title")

recipe = Scene("recipe", "המתכון", [
    P("השאלה נראית תמיד אותו דבר: הראו שהפונקציה, עם $g$ כללית, מקיימת משוואה מסוימת.",
      say="השאלה נראית תמיד אותו דבר: הראו שהפונקציה, עם גִ'י כללית, מקיימת משוואה מסוימת."),
    P("צעד ראשון: מסמנים את משתנה הביניים $t$, וכותבים $t_x$ ו-$t_y$.", do=show("r-1"),
      say="צעד ראשון: מסמנים את משתנה הביניים טִי, וכותבים טִי אִקְס וטִי וַואי."),
    P("צעד שני: גוזרים את $z$ לפי $x$ ולפי $y$. כלל שרשרת, וכלל מכפלה אם יש גורם חופשי.", do=show("r-2"),
      say="צעד שני: גוזרים את זֶד לפי אִקְס ולפי וַואי. כלל שרשרת, וכלל מכפלה אם יש גורם חופשי."),
    P("צעד שלישי: מציבים באגף שמאל של המשוואה.", do=show("r-3")),
    P("צעד רביעי: מצמצמים. כל המחוברים עם $g'$ חייבים להתבטל זה בזה.", do=show("r-4"),
      say="צעד רביעי: מצמצמים. כל המחוברים עם גִ'י תָּג חייבים להתבטל זה בזה."),
    P("צעד חמישי: משווים את מה שנשאר לאגף ימין. לפעמים צריך להחליף את $z$ בביטוי שלו.", do=show("r-5"), hold=0.4,
      say="צעד חמישי: משווים את מה שנשאר לאגף ימין. לפעמים צריך להחליף את זֶד בביטוי שלו."),
], stage='<div class="cr-stack" style="gap:16px;align-items:stretch;width:900px">'
         + st.card("r-1", "ex", "<b>1. מסמנים</b> $t$, וכותבים $t_x$, $t_y$")
         + st.card("r-2", "ex", "<b>2. גוזרים</b> $z_x$, $z_y$ (שרשרת + מכפלה)")
         + st.card("r-3", "ex", "<b>3. מציבים</b> באגף שמאל")
         + st.card("r-4", "rule", "<b>4. מצמצמים:</b> ה-$g'$ חייב להתבטל")
         + st.card("r-5", "ex", "<b>5. משווים</b> לאגף ימין") + "</div>",
   layout="full")

example = Scene("example", "דוגמה", [
    P("דוגמה: הראו ש-$z=e^y\\,g(x-y)$ מקיימת $z_x+z_y=z$.", do=show("e-0"),
      say="דוגמה: הראו שזֶד, אִי בחזקת וַואי כפול גִ'י של אִקְס פחות וַואי, מקיימת זֶד אִקְס ועוד זֶד וַואי שווה זֶד."),
    P("מסמנים $t=x-y$, ואז $t_x=1$ ו-$t_y=-1$.", do=show("e-1"),
      say="מסמנים טִי שווה אִקְס פחות וַואי, ואז טִי אִקְס שווה אחת, וטִי וַואי שווה מינוס אחת."),
    P("לפי $x$ הגורם $e^y$ קבוע: $z_x=e^y\\,g'(t)$.", do=show("e-2"),
      say="לפי אִקְס הגורם אִי בחזקת וַואי קבוע: זֶד אִקְס שווה אִי בחזקת וַואי, גִ'י תָּג של טִי."),
    P("לפי $y$ הגורם משתנה, אז כלל מכפלה: $z_y=e^y\\,g(t)-e^y\\,g'(t)$.", do=show("e-3"),
      say="לפי וַואי הגורם משתנה, אז כלל מכפלה: זֶד וַואי שווה אִי בחזקת וַואי גִ'י של טִי, פחות אִי בחזקת וַואי גִ'י תָּג של טִי."),
    P("מציבים באגף שמאל, ומחברים את שתי הנגזרות.", do=show("e-4")),
    P("המחובר עם $g'$ מופיע פעם עם פלוס ופעם עם מינוס. הם מתבטלים.", do=show("e-5", "e-c1"),
      say="המחובר עם גִ'י תָּג מופיע פעם עם פלוס ופעם עם מינוס. הם מתבטלים."),
    P("נשאר $e^y\\,g(t)$, וזה בדיוק $z$. הזהות הוכחה.", do=show("e-6"), hold=0.4,
      say="נשאר אִי בחזקת וַואי גִ'י של טִי, וזה בדיוק זֶד. הזהות הוכחה."),
], stage=w.lines("e", [("0", "z=e^y\\,g(x-y)\\ \\ \\Rightarrow\\ \\ z_x+z_y=z\\ ?"),
                        ("1", "t=x-y,\\quad t_x=1,\\quad t_y=-1"),
                        ("2", "z_x=e^y\\,g'(t)"),
                        ("3", "z_y=e^y\\,g(t)-e^y\\,g'(t)"),
                        ("4", "z_x+z_y=e^y\\,g'(t)+e^y\\,g(t)-e^y\\,g'(t)"),
                        ("5", "\\phantom{z_x+z_y}=e^y\\,g(t)"),
                        ("6", "\\phantom{z_x+z_y}=z\\ \\ \\checkmark")], cls="sm"),
   panel=st.card("e-c1", "rule", "🔑 $+e^y g'(t)$ ו-$-e^y g'(t)$: מתבטלים"))

check = Scene("check", "בדיקה עצמית", [
    P("הכלל החשוב בפרק: אם ה-$g'$ לא התבטל, יש טעות.", do=show("c-c1"),
      say="הכלל החשוב בפרק: אם הגִ'י תָּג לא התבטל, יש טעות."),
    P("למה? המשוואה צריכה להתקיים לכל $g$. אילו נשאר מחובר עם $g'$, היינו יכולים לבחור $g$ שמקלקלת את השוויון.", do=show("c-1"),
      say="למה? המשוואה צריכה להתקיים לכל גִ'י. אילו נשאר מחובר עם גִ'י תָּג, היינו יכולים לבחור גִ'י שמקלקלת את השוויון."),
    P("נראה טעות אופיינית: מי שכתב $t_y=+1$ במקום מינוס אחת.", do=show("c-2"),
      say="נראה טעות אופיינית: מי שכתב טִי וַואי שווה פלוס אחת, במקום מינוס אחת."),
    P("אצלו יוצא $z_x+z_y=z+2e^y\\,g'(t)$. ה-$g'$ לא התבטל, וזה האות לחזור אחורה.", do=show("c-3"),
      say="אצלו יוצא זֶד אִקְס ועוד זֶד וַואי שווה זֶד, ועוד שתיים אִי בחזקת וַואי גִ'י תָּג. הגִ'י תָּג לא התבטל, וזה האות לחזור אחורה."),
    P("לאן חוזרים? לשורת הנגזרות: הסימנים של $t_x$ ו-$t_y$, וכלל המכפלה.", do=show("c-c2"),
      say="לאן חוזרים? לשורת הנגזרות: הסימנים של טִי אִקְס וטִי וַואי, וכלל המכפלה."),
    P("ועוד דבר: המקדמים במשוואה נבחרו בדיוק כדי שה-$g'$ יתבטל. מקדם שמוצמד לנגזרת הלא נכונה שובר הכול.", do=show("c-c3"), hold=0.4,
      say="ועוד דבר: המקדמים במשוואה נבחרו בדיוק כדי שהגִ'י תָּג יתבטל. מקדם שמוצמד לנגזרת הלא נכונה שובר הכול."),
], stage=w.lines("c", [("1", "\\forall g:\\ \\ z_x+z_y=z"),
                        ("2", "t_y=+1\\quad\\times"),
                        ("3", "z_x+z_y=z+2e^y\\,g'(t)")], cls="c"),
   panel=st.card("c-c1", "rule", "🔑 $g'$ לא התבטל? יש טעות")
         + st.card("c-c2", "ex", "חוזרים ל-$t_x$, $t_y$ ולכלל המכפלה")
         + st.card("c-c3", "trap", "⚠️ כל מקדם צמוד לנגזרת שלו"))

exam1 = Scene("exam1", "בסגנון מבחן: הנגזרות", [
    P("ועכשיו שאלה בסגנון המבחנים: הראו ש-$z=\\frac{y^2}{2x}+g\\left(\\frac yx\\right)$ מקיימת את המשוואה שבצד.",
      say="ועכשיו שאלה בסגנון המבחנים: הראו שזֶד, וַואי בריבוע חלקי שתיים אִקְס, ועוד גִ'י של וַואי חלקי אִקְס, מקיימת את המשוואה שבצד."),
    P("צעד ראשון: $t=\\frac yx$. לפי $x$ זה $y$ כפול אִקְס בחזקת מינוס אחת, ולכן $t_x=-\\frac{y}{x^2}$.", do=show("a-1"),
      say="צעד ראשון: טִי שווה וַואי חלקי אִקְס. לפי אִקְס זה וַואי כפול אִקְס בחזקת מינוס אחת, ולכן טִי אִקְס שווה מינוס וַואי חלקי אִקְס בריבוע."),
    P("ולפי $y$: $t_y=\\frac1x$.", do=show("a-2"),
      say="ולפי וַואי: טִי וַואי שווה אחת חלקי אִקְס."),
    P("האיבר המחובר הוא מסלול ישיר, ונגזר לבד. לפי $x$ הוא נותן מינוס $\\frac{y^2}{2x^2}$.", do=show("a-c1"),
      say="האיבר המחובר הוא מסלול ישיר, ונגזר לבד. לפי אִקְס הוא נותן מינוס וַואי בריבוע חלקי שתיים אִקְס בריבוע."),
    P("ולכן $z_x=-\\frac{y^2}{2x^2}-\\frac{y}{x^2}\\,g'(t)$.", do=show("a-3"),
      say="ולכן זֶד אִקְס שווה מינוס וַואי בריבוע חלקי שתיים אִקְס בריבוע, פחות וַואי חלקי אִקְס בריבוע, גִ'י תָּג של טִי."),
    P("ולפי $y$: $z_y=\\frac yx+\\frac1x\\,g'(t)$.", do=show("a-4"), hold=0.4,
      say="ולפי וַואי: זֶד וַואי שווה וַואי חלקי אִקְס, ועוד אחת חלקי אִקְס, גִ'י תָּג של טִי."),
], stage=w.lines("a", [("1", "t=\\frac yx,\\quad t_x=-\\frac{y}{x^2}"),
                        ("2", "t_y=\\frac1x"),
                        ("3", "z_x=-\\frac{y^2}{2x^2}-\\frac{y}{x^2}\\,g'(t)"),
                        ("4", "z_y=\\frac yx+\\frac1x\\,g'(t)")], cls="c"),
   panel='<div class="qstem"><span class="qid">בסגנון מבחן</span>הראו כי $z=\\dfrac{y^2}{2x}+g\\!\\left(\\dfrac yx\\right)$, כאשר $g$ גזירה ו-$x\\ne0$, מקיימת</div>' + '<div class="cr-big" style="font-size:40px;margin-top:10px">$\\displaystyle x\\,z_x+y\\,z_y=\\frac{y^2}{2x}$</div>'
         + st.card("a-c1", "ex", "איבר מחובר: מסלול ישיר"))

exam2 = Scene("exam2", "בסגנון מבחן: ההצבה", [
    P("מציבים. $x$ כפול $z_x$: מינוס $\\frac{y^2}{2x}$, ומינוס $\\frac yx\\,g'(t)$.", do=show("b-1"),
      say="מציבים. אִקְס כפול זֶד אִקְס: מינוס וַואי בריבוע חלקי שתיים אִקְס, ומינוס וַואי חלקי אִקְס, גִ'י תָּג של טִי."),
    P("$y$ כפול $z_y$: $\\frac{y^2}{x}$, ועוד $\\frac yx\\,g'(t)$.", do=show("b-2"),
      say="וַואי כפול זֶד וַואי: וַואי בריבוע חלקי אִקְס, ועוד וַואי חלקי אִקְס, גִ'י תָּג של טִי."),
    P("המחוברים עם $g'$: מינוס $\\frac yx\\,g'$ ופלוס $\\frac yx\\,g'$. מתבטלים.", do=show("b-3", "b-c1"),
      say="המחוברים עם גִ'י תָּג: מינוס וַואי חלקי אִקְס גִ'י תָּג, ופלוס אותו דבר. מתבטלים."),
    P("ומה שנשאר: מינוס חצי $\\frac{y^2}{x}$, ועוד $\\frac{y^2}{x}$. כלומר $\\frac{y^2}{2x}$, בדיוק אגף ימין.", do=show("b-4", "b-c2"),
      say="ומה שנשאר: מינוס חצי וַואי בריבוע חלקי אִקְס, ועוד וַואי בריבוע חלקי אִקְס. כלומר וַואי בריבוע חלקי שתיים אִקְס, בדיוק אגף ימין."),
    P("ומי שאיבד את המינוס של $t_x$? אצלו נשאר $2\\frac yx\\,g'(t)$. ה-$g'$ לא התבטל, וזה האות לחזור לשורת הנגזרות.", do=show("b-c3"), hold=0.4,
      say="ומי שאיבד את המינוס של טִי אִקְס? אצלו נשאר שתיים וַואי חלקי אִקְס, גִ'י תָּג. הגִ'י תָּג לא התבטל, וזה האות לחזור לשורת הנגזרות."),
], stage=w.lines("b", [("1", "x\\,z_x=-\\frac{y^2}{2x}-\\frac yx\\,g'(t)"),
                        ("2", "y\\,z_y=\\frac{y^2}{x}+\\frac yx\\,g'(t)"),
                        ("3", "-\\frac yx\\,g'(t)+\\frac yx\\,g'(t)=0"),
                        ("4", "-\\frac{y^2}{2x}+\\frac{y^2}{x}=\\frac{y^2}{2x}\\ \\ \\checkmark")], cls="c"),
   panel='<div class="cr-big" style="font-size:40px">$\\displaystyle x\\,z_x+y\\,z_y=\\frac{y^2}{2x}$</div>'
         + st.card("b-c1", "rule", "🔑 ה-$g'$ התבטל: סימן שהנגזרות נכונות")
         + st.card("b-c2", "ex", "מה שנשאר שווה לאגף ימין")
         + st.card("b-c3", "trap", "⚠️ $t_x=-\\frac{y}{x^2}$: בלי המינוס, ה-$g'$ נשאר"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: מסמנים, גוזרים, מציבים, מצמצמים, ומשווים.", do=show("s-1")),
    P("בהוכחה נכונה כל המחוברים עם $g'$ מתבטלים.", do=show("s-2"),
      say="בהוכחה נכונה כל המחוברים עם גִ'י תָּג מתבטלים."),
    P("אם נשאר $g'$, חוזרים לשורת הנגזרות לפני שממשיכים.", do=show("s-3"),
      say="אם נשאר גִ'י תָּג, חוזרים לשורת הנגזרות לפני שממשיכים."),
    P("ומה שנשאר משווים לאגף ימין, ואם צריך מחליפים את $z$ בביטוי שלו. נתראה ברמה הבאה.", do=show("s-4"), hold=0.6,
      say="ומה שנשאר משווים לאגף ימין, ואם צריך מחליפים את זֶד בביטוי שלו. נתראה ברמה הבאה."),
], stage=w.big("s-0", "g'\\ -\\ g'=0", hidden=False, size=64),
   panel=st.card("s-1", "rule", "🔑 מסמנים, גוזרים, מציבים, מצמצמים, משווים")
         + st.card("s-2", "rule", "🔑 ה-$g'$ חייב להתבטל")
         + st.card("s-3", "trap", "⚠️ לא התבטל? בודקים סימנים וכלל מכפלה")
         + st.card("s-4", "ex", "אגף ימין עם $z$: מחליפים בביטוי"))

VIDEO = Video("K04", "chain_rule", "הצבה בזהות: ה-g' מצטמצם", [title, recipe, example, check, exam1, exam2, recap],
              bank={})
