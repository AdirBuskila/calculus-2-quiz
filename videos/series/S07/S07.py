# -*- coding: utf-8 -*-
"""S07 · מקלורן מהטבלה ונגזרות ב-0 מהמקדמים — video script (build: tools/video/vid.py S07).

Source: courses/series/C07.js (lesson + goal). Exam anchor: 24A-B-Q5b (x/(25+x²): Maclaurin series by substitution
in 1/(1+u), domain |x|<5 with both endpoints divergent, f^(5)(0) = 5!/5^6 = 4!/5^5), which no guided quiz uses.
Not used on purpose: the C07 quiz functions (1/(1+2x), x²e^x, sin(x²), ln(1+3x), 1/((1-x)(1-2x))), the lesson's e^{2x},
and the boss's ln(2x²+3x+1). Examples here: e^{-x²} with f^(4)(0) = 12, and ln(1 - x/2) with domain [-2, 2) (the
substitution flips which end is closed). Every coefficient, derivative and interval is asserted below with sympy.
"""
from vid import P, Scene, Video, show, hide, BANK
import sympy as sp
import stage as st
import w_series as ws
from w_series import n

x = sp.Symbol("x", real=True)
u = sp.Symbol("u", real=True)

# ---------------------------------------------------------------- checks
# the table (first terms against sympy's own series)
for f, gen in ((sp.exp(x), 1 / sp.factorial(n) * x ** n),
               (sp.sin(x), (-1) ** n * x ** (2 * n + 1) / sp.factorial(2 * n + 1)),
               (sp.cos(x), (-1) ** n * x ** (2 * n) / sp.factorial(2 * n)),
               (1 / (1 - x), x ** n)):
    assert sp.expand(sp.series(f, x, 0, 9).removeO() - sum(gen.subs(n, k) for k in range(0, 9)).series(x, 0, 9).removeO()) == 0
assert sp.expand(sp.series(sp.log(1 + x), x, 0, 9).removeO()
                 - sum((-1) ** (k + 1) * x ** k / k for k in range(1, 9))) == 0

# example 1: e^{-x²} = Σ (-1)^n x^{2n}/n!, f^(4)(0) = 4! · (1/2) = 12
E = sp.exp(-x ** 2)
assert sp.expand(sp.series(E, x, 0, 9).removeO() - sum((-1) ** k * x ** (2 * k) / sp.factorial(k) for k in range(5))) == 0
assert sp.diff(E, x, 4).subs(x, 0) == 12 == sp.factorial(4) * sp.Rational(1, 2)

# example 2: ln(1 - x/2): u = -x/2 in (-1, 1] <=> x in [-2, 2)
assert sp.solve_univariate_inequality(-x / 2 > -1, x, relational=False) == sp.Interval.open(-sp.oo, 2)
assert sp.solve_univariate_inequality(-x / 2 <= 1, x, relational=False) == sp.Interval(-2, sp.oo)
D2 = sp.Interval.Ropen(-2, 2)
# endpoints: x = -2 -> u = 1: Σ (-1)^{n+1}/n converges (Leibniz); x = 2 -> u = -1: Σ (-1)^{n+1}(-1)^n/n = -Σ 1/n diverges
assert sp.simplify((-1) ** (n + 1) * (-1) ** n / n + 1 / n) == 0
assert ws.tail(1 / n, 10 ** 4, 10 ** 5) > 2.2

# exam 24A-B-Q5b
EX = BANK["24A-B-Q5b"]
assert r"f(x)=\dfrac{x}{25+x^2}" in EX["question"]
F = x / (25 + x ** 2)
GEN = (-1) ** n * x ** (2 * n + 1) / 5 ** (2 * n + 2)
assert sp.simplify(x / 25 * (-1) ** n * (x / 5) ** (2 * n) - GEN) == 0
assert sp.expand(sp.series(F, x, 0, 12).removeO() - sum(GEN.subs(n, k) for k in range(6))) == 0
# domain: (x/5)^2 < 1 <=> |x| < 5; at x = ±5 the term is ±(-1)^n/5, not -> 0
assert sp.solve_univariate_inequality((x / 5) ** 2 < 1, x, relational=False) == sp.Interval.open(-5, 5)
assert sp.simplify(GEN.subs(x, 5) - (-1) ** n / 5) == 0 and sp.simplify(GEN.subs(x, -5) + (-1) ** n / 5) == 0
# f^(5)(0): 2n+1 = 5 -> n = 2, coefficient 1/5^6
c5 = GEN.subs(n, 2) / x ** 5
assert c5 == sp.Rational(1, 5 ** 6)
d5 = sp.diff(F, x, 5).subs(x, 0)
assert d5 == sp.factorial(5) * c5 == sp.Rational(24, 3125) == sp.factorial(4) / sp.Integer(5) ** 5

NLE = ws.numline("ne", -8, 8, [(-5, "$-5$"), (0, "$0$"), (5, "$5$")], -5, 5, w=860,
                 verdicts={"L": ("$a_n \\not\\to 0$", False), "R": ("$a_n \\not\\to 0$", False)})
NL2 = ws.numline("nl", -4, 4, [(-2, "$-2$"), (0, "$0$"), (2, "$2$")], -2, 2, w=860,
                 verdicts={"L": ("$u=1$: מתכנס", True), "R": ("$u=-1$: מתבדר", False)})

TAB = ('<table class="sr-tab" style="font-size:30px"><thead><tr><th>הפונקציה</th><th>הטור</th><th>תחום</th></tr></thead><tbody>'
       '<tr id="t-1" class="h"><td class="l">$e^x$</td><td class="l">$\\sum\\frac{x^n}{n!}$</td><td>כל $x$</td></tr>'
       '<tr id="t-2" class="h"><td class="l">$\\sin x$</td><td class="l">$\\sum\\frac{(-1)^n x^{2n+1}}{(2n+1)!}$</td><td>כל $x$</td></tr>'
       '<tr id="t-3" class="h"><td class="l">$\\cos x$</td><td class="l">$\\sum\\frac{(-1)^n x^{2n}}{(2n)!}$</td><td>כל $x$</td></tr>'
       '<tr id="t-4" class="h"><td class="l">$\\frac{1}{1-x}$</td><td class="l">$\\sum x^n$</td><td class="l">$|x|<1$</td></tr>'
       '<tr id="t-5" class="h"><td class="l">$\\ln(1+x)$</td><td class="l">$\\sum\\frac{(-1)^{n+1}x^n}{n}$</td>'
       '<td class="l">$-1<x\\le 1$</td></tr></tbody></table>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נפתח פונקציות לטור מקלורן, בלי לגזור שוב ושוב."),
    P("נשתמש בטבלה, נמצא את תחום ההתכנסות, ונחלץ נגזרת מסדר גבוה באפס מתוך מקדם אחד."),
    P("ובסוף נפתור שאלה ממבחן.", hold=0.4),
], stage='<div class="kicker">S07 · טורים</div><h1>מקלורן מהטבלה ונגזרות ב-0 מהמקדמים</h1>'
         '<p>לפתח פונקציה לטור מקלורן מהטבלה, לקבוע את תחום ההתכנסות, ולחלץ נגזרת מסדר גבוה ב-0 מהמקדם.</p>',
   layout="title")

table = Scene("table", "הטבלה", [
    P("טור מקלורן של פונקציה הוא טור החזקות שלה סביב אפס. חמשת הטורים האלה הם כל מה שצריך.", do=show("t-tab")),
    P("אקספוננט: $x$ בחזקת $n$ חלקי $n$ עצרת. מתכנס לכל $x$.", do=show("t-1"),
      say="אקספוננט: אִקְס בחזקת אֶן חלקי אֶן עצרת. מתכנס לכל אִקְס."),
    P("סינוס וקוסינוס: רק החזקות האי-זוגיות, או רק הזוגיות, עם סימנים מתחלפים. גם הם לכל $x$.", do=show("t-2", "t-3"),
      say="סינוס וקוסינוס: רק החזקות האי זוגיות, או רק הזוגיות, עם סימנים מתחלפים. גם הם לכל אִקְס."),
    P("אחת חלקי אחת פחות $x$: הטור ההנדסי, רק כשהערך המוחלט של $x$ קטן מאחת.", do=show("t-4"),
      say="אחת חלקי אחת פחות אִקְס: הטור ההנדסי, רק כשהערך המוחלט של אִקְס קטן מאחת."),
    P("ולן של אחת ועוד $x$: מתכנס ממינוס אחת לא כולל, עד אחת כולל.", do=show("t-5"),
      say="ולן של אחת ועוד אִקְס: מתכנס ממינוס אחת לא כולל, עד אחת כולל."),
    P("הכלי המרכזי: **הצבה**. מחליפים את $x$ בטבלה בביטוי אחר, והתחום מגיע מאותה הצבה.", do=show("t-r"),
      say="הכלי המרכזי: הצבה. מחליפים את אִקְס בטבלה בביטוי אחר, והתחום מגיע מאותה הצבה.", hold=0.4),
], stage=f'<div class="sr-col"><div id="t-tab" class="h">{TAB}</div></div>',
   panel=st.card("t-r", "rule", "🔑 מציבים $u = cx$ או $u = x^2$ בטבלה, והתחום: $u$ בתחום של הטבלה"))

deriv = Scene("deriv", "נגזרת מהמקדם", [
    P("ועכשיו הקשר בין מקדם לנגזרת. אם $f$ שווה לטור חזקות, המקדם של $x$ בחזקת $k$ הוא הנגזרת ה-$k$ באפס, חלקי $k$ עצרת.",
      do=show("d-0"), say="ועכשיו הקשר בין מקדם לנגזרת. אם אֶף שווה לטור חזקות, המקדם של אִקְס בחזקת קֵיי הוא הנגזרת הקֵיי באפס, חלקי קֵיי עצרת."),
    P("אז הנגזרת היא $k$ עצרת כפול המקדם. מוצאים מקדם אחד, וכופלים.", do=show("d-r"),
      say="אז הנגזרת היא קֵיי עצרת כפול המקדם. מוצאים מקדם אחד, וכופלים."),
    P("דוגמה: $e$ בחזקת מינוס $x$ בריבוע. מציבים מינוס $x$ בריבוע בטור של האקספוננט.", do=show("d-1"),
      say="דוגמה: אִי בחזקת מינוס אִקְס בריבוע. מציבים מינוס אִקְס בריבוע בטור של האקספוננט."),
    P("מקבלים מינוס אחת בחזקת $n$, כפול $x$ בחזקת שתיים $n$, חלקי $n$ עצרת.", do=show("d-2"),
      say="מקבלים מינוס אחת בחזקת אֶן, כפול אִקְס בחזקת שתיים אֶן, חלקי אֶן עצרת."),
    P("הנגזרת הרביעית באפס? צריך $x$ בחזקת ארבע, כלומר שתיים $n$ שווה ארבע, ו-$n$ שווה שתיים.", do=show("d-3"),
      say="הנגזרת הרביעית באפס? צריך אִקְס בחזקת ארבע, כלומר שתיים אֶן שווה ארבע, ואֶן שווה שתיים."),
    P("המקדם הוא חצי. כפול ארבע עצרת, עשרים וארבע, יוצא שתים עשרה.", do=show("d-4")),
    P("המלכודת: לענות חצי. המקדם הוא לא הנגזרת. צריך לכפול ב-$k$ עצרת.", do=show("d-t"),
      say="המלכודת: לענות חצי. המקדם הוא לא הנגזרת. צריך לכפול בקֵיי עצרת.", hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("d", ["$a_k = \\frac{f^{(k)}(0)}{k!}$",
                        "$e^{u}, \\quad u = -x^2$",
                        "$e^{-x^2} = \\sum_{n=0}^{\\infty}\\frac{(-1)^n x^{2n}}{n!}$",
                        "$x^4: \\quad 2n = 4, \\quad n = 2, \\quad a_4 = \\frac{1}{2!} = \\frac{1}{2}$",
                        "$f^{(4)}(0) = 4!\\cdot\\frac{1}{2} = 12$"], size=34, gap=14)
         + '</div>',
   panel=st.card("d-r", "rule", "🔑 $f^{(k)}(0) = k!\\cdot a_k$")
         + st.card("d-t", "trap", "⚠️ $a_k$ הוא לא $f^{(k)}(0)$: כופלים ב-$k!$"))

dom = Scene("dom", "תחום מהצבה", [
    P("עכשיו תחום. לן של אחת פחות $x$ חלקי שתיים: מציבים $u$ שווה מינוס $x$ חלקי שתיים.", do=show("m-0"),
      say="עכשיו תחום. לן של אחת פחות אִקְס חלקי שתיים: מציבים יוּ שווה מינוס אִקְס חלקי שתיים."),
    P("הטור של לן מתכנס כש-$u$ גדול ממינוס אחת, וקטן או שווה לאחת.", do=show("m-1"),
      say="הטור של לן מתכנס כשיוּ גדול ממינוס אחת, וקטן או שווה לאחת."),
    P("כופלים במינוס שתיים, והאי-שוויונות מתהפכים: $x$ קטן משתיים, וגדול או שווה למינוס שתיים.", do=show("m-2", "m-t"),
      say="כופלים במינוס שתיים, והאי שוויונות מתהפכים: אִקְס קטן משתיים, וגדול או שווה למינוס שתיים."),
    P("שימו לב: הקצה הסגור עבר שמאלה. ב-$x$ שווה מינוס שתיים, $u$ שווה אחת, וזה הקצה הטוב של הלן.",
      do=show("m-nl", "nl-band", "nl-L-c", "nl-L-v"), say="שימו לב: הקצה הסגור עבר שמאלה. באִקְס שווה מינוס שתיים, יוּ שווה אחת, וזה הקצה הטוב של הלן."),
    P("וב-$x$ שווה שתיים, $u$ שווה מינוס אחת: מקבלים מינוס הטור ההרמוני, שמתבדר.", do=show("nl-R-o", "nl-R-v", "m-v"),
      say="ובאִקְס שווה שתיים, יוּ שווה מינוס אחת: מקבלים מינוס הטור ההרמוני, שמתבדר.", hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("m", ["$\\ln\\left(1 - \\frac{x}{2}\\right), \\quad u = -\\frac{x}{2}$",
                        "$-1 < u \\le 1$",
                        "$-1 < -\\frac{x}{2} \\le 1 \\iff -2 \\le x < 2$"], size=38, gap=18)
         + f'<div id="m-nl" class="h" style="margin-top:24px">{NL2}</div>'
         + ws.verdict("m-v", "התחום: $[-2, 2)$") + '</div>',
   panel=st.card("m-t", "trap", "⚠️ כפל במספר שלילי הופך את האי-שוויון, ואיתו את הקצה הסגור"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: פתחו את $x$ חלקי עשרים וחמש ועוד $x$ בריבוע לטור מקלורן. מה התחום, ומה הנגזרת החמישית באפס?",
      say="שאלה ממבחן: פתחו את אִקְס חלקי עשרים וחמש ועוד אִקְס בריבוע לטור מקלורן. מה התחום, ומה הנגזרת החמישית באפס?"),
    P("מוציאים עשרים וחמש מהמכנה. נשאר אחת חלקי אחת ועוד הריבוע של $x$ חלקי חמש.", do=show("x-0"),
      say="מוציאים עשרים וחמש מהמכנה. נשאר אחת חלקי אחת ועוד הריבוע של אִקְס חלקי חמש."),
    P("זה הטור ההנדסי, עם מנה: מינוס הריבוע של $x$ חלקי חמש. ואת ה-$x$ שבמונה כופלים פנימה.", do=show("x-1"),
      say="זה הטור ההנדסי, עם מנה: מינוס הריבוע של אִקְס חלקי חמש. ואת האִקְס שבמונה כופלים פנימה."),
    P("התוצאה: מינוס אחת בחזקת $n$, כפול $x$ בחזקת שתיים $n$ ועוד אחת, חלקי חמש בחזקת שתיים $n$ ועוד שתיים.", do=show("x-2"),
      say="התוצאה: מינוס אחת בחזקת אֶן, כפול אִקְס בחזקת שתיים אֶן ועוד אחת, חלקי חמש בחזקת שתיים אֶן ועוד שתיים."),
    P("התחום: המנה בערך מוחלט קטנה מאחת, כלומר $x$ בין מינוס חמש לחמש.", do=show("x-nl", "ne-band"),
      say="התחום: המנה בערך מוחלט קטנה מאחת, כלומר אִקְס בין מינוס חמש לחמש."),
    P("ובקצוות האיבר הוא פלוס או מינוס חמישית. הוא לא שואף לאפס, אז שני הקצוות מתבדרים.",
      do=show("ne-L-o", "ne-R-o", "ne-L-v", "ne-R-v")),
    P("עכשיו הנגזרת. החזקות הן שתיים $n$ ועוד אחת. בשביל $x$ בחזקת חמש צריך $n$ שווה **שתיים**, לא חמש.",
      do=show("x-3", "x-t"), say="עכשיו הנגזרת. החזקות הן שתיים אֶן ועוד אחת. בשביל אִקְס בחזקת חמש צריך אֶן שווה שתיים, לא חמש."),
    P("המקדם הוא אחת חלקי חמש בחזקת שש. כפול חמש עצרת, מאה עשרים: הנגזרת היא ארבע עצרת חלקי חמש בחזקת חמש.",
      do=show("x-4", "x-v"), say="המקדם הוא אחת חלקי חמש בחזקת שש. כפול חמש עצרת, מאה עשרים: הנגזרת היא ארבע עצרת חלקי חמש בחזקת חמש.",
      hold=0.6),
], stage='<div class="sr-col">'
         + ws.eqs("x", ["$\\frac{x}{25+x^2} = \\frac{x}{25}\\cdot\\frac{1}{1+\\left(\\frac{x}{5}\\right)^2}$",
                        "$= \\frac{x}{25}\\sum_{n=0}^{\\infty}(-1)^n\\left(\\frac{x}{5}\\right)^{2n}$",
                        "$= \\sum_{n=0}^{\\infty}\\frac{(-1)^n x^{2n+1}}{5^{2n+2}}$",
                        "$2n+1 = 5 \\;\\Rightarrow\\; n = 2, \\quad a_5 = \\frac{1}{5^6}$",
                        "$f^{(5)}(0) = 5!\\cdot\\frac{1}{5^6} = \\frac{4!}{5^5} = \\frac{24}{3125}$"], size=27, gap=0)
         + f'<div id="x-nl" class="h" style="margin-top:0px">{NLE}</div></div>',
   panel=ws.stem(EX["id"], "פתחו לטור מקלורן. מהו תחום ההתכנסות? הסיקו את $f^{(5)}(0)$."
                 '<div class="sr-mid" style="font-size:36px">$f(x) = \\dfrac{x}{25+x^2}$</div>')
         + st.card("x-t", "trap", "⚠️ $x^5$ מגיע מ-$n=2$, כי החזקה היא $2n+1$")
         + ws.verdict("x-v", "$|x|<5, \\quad f^{(5)}(0) = \\frac{24}{3125}$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: לא גוזרים. לוקחים טור מהטבלה ומציבים.", do=show("r-1")),
    P("התחום מגיע מאותה הצבה, ואת הקצוות בודקים, כי הצבה יכולה להפוך את הקצה הסגור.", do=show("r-2")),
    P("והנגזרת ה-$k$ באפס היא $k$ עצרת כפול המקדם של $x$ בחזקת $k$.", do=show("r-3"),
      say="והנגזרת הקֵיי באפס היא קֵיי עצרת כפול המקדם של אִקְס בחזקת קֵיי."),
    P("ושימו לב איזה $n$ נותן את החזקה שמחפשים. ברמה הבאה: שאלות מבחן מלאות.", do=show("r-4"),
      say="ושימו לב איזה אֶן נותן את החזקה שמחפשים. ברמה הבאה: שאלות מבחן מלאות.", hold=0.6),
], stage='<div class="sr-col"><div class="sr-big">$f^{(k)}(0) = k!\\cdot a_k$</div></div>',
   panel=st.card("r-1", "rule", "🔑 טבלה + הצבה")
         + st.card("r-2", "rule", "🔑 התחום מההצבה, והקצוות בנפרד")
         + st.card("r-3", "rule", "🔑 $f^{(k)}(0) = k!\\cdot a_k$")
         + st.card("r-4", "trap", "⚠️ $x^{2n+1}$: $x^5$ מ-$n=2$"))

VIDEO = Video("S07", "series", "מקלורן מהטבלה ונגזרות ב-0 מהמקדמים", ws.fix_scenes([title, table, deriv, dom, exam, recap]),
              bank={"24A-B-Q5b": None})
