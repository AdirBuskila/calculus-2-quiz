# -*- coding: utf-8 -*-
"""S06 · הקצוות: המלכודת הקלאסית — video script (build: tools/video/vid.py S06).

Source: courses/series/C06.js (lesson + goal). Exam anchor: 24B-B-Q4b (Σ 2^n (x-1)^n/√(n+4): R = 1/2, center 1,
x = 1/2 converges by Leibniz, x = 3/2 diverges by limit comparison with 1/√n: domain [1/2, 3/2)), which no guided
quiz uses. Its official key wrote the left endpoint as -1/2 and said x = 3/2 converges; the bank's solution already
carries the correction, and the video shows the trap.
Not used on purpose: the C06 quiz series (x^n/n, x^n/n², n x^n/(n+1), the (-3,3] shift, (x-2)^n/(n3^n), x^n/√n) and the
lesson's x^n/n. Examples here: (-1)^n x^n/(n 5^n) -> (-5, 5], (x+1)^n/(n² 2^n) -> [-3, 1], and the shift of [-2,2) by
x+3 -> [-5,-1). Every radius, endpoint verdict and interval is asserted below.
"""
from vid import P, Scene, Video, show, hide, BANK
import sympy as sp
import stage as st
import w_series as ws
from w_series import n

X = sp.Symbol("X", real=True)
xs = sp.Symbol("x", real=True)

# ---------------------------------------------------------------- checks
# A: Σ (-1)^n x^n/(n 5^n): R = 5; x = 5 -> Σ(-1)^n/n converges (Leibniz), x = -5 -> Σ 1/n diverges
CA = 1 / (n * 5 ** n)
assert ws.radius(CA) == 5
assert sp.simplify(((-1) ** n * 5 ** n * CA) - (-1) ** n / n) == 0                 # x = 5
assert sp.simplify(((-1) ** n * (-5) ** n * CA) - 1 / n) == 0                      # x = -5: (-1)^n (-1)^n = 1
assert ws.lim(1 / n) == 0 and sp.diff(1 / n, n).is_negative                       # Leibniz at x = 5
assert ws.tail(1 / n, 10 ** 4, 10 ** 5) > 2.2                                      # harmonic grows (≈ ln 10)
# B: Σ (x+1)^n/(n² 2^n): center -1, R = 2; at both ends |term| = 1/n², p = 2: absolutely -> [-3, 1]
CB = 1 / (n ** 2 * 2 ** n)
assert ws.radius(CB) == 2
assert sp.simplify(2 ** n * CB - 1 / n ** 2) == 0
assert (-1 - 2, -1 + 2) == (-3, 1)
# shift: domain of Σ a_n X^n is [-2, 2) -> Σ a_n (x+3)^n: -2 <= x+3 < 2 -> [-5, -1)
assert sp.Interval.Ropen(-2, 2).intersect(sp.Interval(-10, 10)) == sp.imageset(sp.Lambda(xs, xs + 3), sp.Interval.Ropen(-5, -1))

# exam 24B-B-Q4b
EX = BANK["24B-B-Q4b"]
assert r"\frac{2^n}{\sqrt{n+4}}(x-1)^n" in EX["question"]
A = 2 ** n / sp.sqrt(n + 4)
assert ws.ratio(A) == 2
assert ws.radius(A) == sp.Rational(1, 2)
R, x0 = sp.Rational(1, 2), 1
assert (x0 - R, x0 + R) == (sp.Rational(1, 2), sp.Rational(3, 2))
# x = 1/2: (x-1)^n = (-1/2)^n -> Σ (-1)^n/√(n+4)
c = 1 / sp.sqrt(n + 4)
assert sp.simplify(A * (-sp.Rational(1, 2)) ** n - (-1) ** n * c) == 0
assert ws.lim(c) == 0 and sp.diff(c, n).is_negative
SL = ws.psums((-1) ** n * c, 400)
assert abs(SL[399] - SL[398]) < 0.06                                               # partial sums settle
# x = 3/2: Σ 1/√(n+4) ~ Σ 1/√n (p = 1/2) diverges
assert sp.simplify(A * sp.Rational(1, 2) ** n - c) == 0
assert ws.lim(c / (1 / sp.sqrt(n))) == 1
assert ws.tail(c, 10 ** 4, 10 ** 5) > 400                                          # grows like 2√N
DOM = sp.Interval.Ropen(sp.Rational(1, 2), sp.Rational(3, 2))
# the official slip: x0 - R is 1/2, not -1/2
assert x0 - R != -sp.Rational(1, 2)

NLA = ws.numline("na", -8, 8, [(-5, "$-5$"), (0, "$0$"), (5, "$5$")], -5, 5, w=860,
                 verdicts={"L": ("$\\sum\\frac{1}{n}$ מתבדר", False), "R": ("לייבניץ: מתכנס", True)})
NLB = ws.numline("nb", -5, 3, [(-3, "$-3$"), (-1, "$-1$"), (1, "$1$")], -3, 1, w=860,
                 verdicts={"L": ("$\\frac{1}{n^2}$: מתכנס", True), "R": ("$\\frac{1}{n^2}$: מתכנס", True)})
NLX = ws.numline("nx", -0.5, 2.5, [(0.5, "$\\frac{1}{2}$"), (1, "$1$"), (1.5, "$\\frac{3}{2}$")], 0.5, 1.5, w=860,
                 verdicts={"L": ("לייבניץ: מתכנס", True), "R": ("$p=\\frac{1}{2}$: מתבדר", False)})

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נסגור את השאלה הכי שכיחה בפרק: תחום ההתכנסות."),
    P("הרדיוס כבר ידוע. מה שנשאר זה שתי נקודות הקצה, ושם מאבדים הכי הרבה נקודות במבחן."),
    P("ובסוף נפתור שאלה ממבחן, שבה גם הפתרון הרשמי טעה.", hold=0.4),
], stage='<div class="kicker">S06 · טורים</div><h1>הקצוות: המלכודת הקלאסית</h1>'
         '<p>לבדוק כל קצה בנפרד, לבחור את הכלי הנכון, ולכתוב את תחום ההתכנסות עם הסוגריים הנכונים.</p>',
   layout="title")

recipe = Scene("recipe", "המתכון", [
    P("המתכון: מציבים כל קצה בטור. אז $x$ הוא מספר, ומקבלים **טור מספרי רגיל**.", do=show("p-1"),
      say="המתכון: מציבים כל קצה בטור. אז אִקְס הוא מספר, ומקבלים טור מספרי רגיל."),
    P("מסווגים אותו בכלים שכבר יש לנו: תנאי הכרחי, השוואה, לייבניץ.", do=show("p-2")),
    P("קצה שמתכנס נכנס לתחום, עם סוגר מרובע. קצה שמתבדר נשאר בחוץ, עם סוגר עגול.", do=show("p-3")),
    P("ושני הקצוות לא חייבים להתנהג אותו דבר.", do=show("p-4")),
    P("דוגמה: מינוס אחת בחזקת $n$, כפול $x$ בחזקת $n$, חלקי $n$ כפול חמש בחזקת $n$. הרדיוס חמש.",
      do=show("a-0", "a-nl", "na-band", "na-L-q", "na-R-q"),
      say="דוגמה: מינוס אחת בחזקת אֶן, כפול אִקְס בחזקת אֶן, חלקי אֶן כפול חמש בחזקת אֶן. הרדיוס חמש."),
    P("ב-$x$ שווה חמש, החמשות מצטמצמות, ונשאר מינוס אחת בחזקת $n$ חלקי $n$. לפי לייבניץ, מתכנס.",
      do=hide("na-R-q") + show("a-1", "na-R-c", "na-R-v"),
      say="באִקְס שווה חמש, החמשות מצטמצמות, ונשאר מינוס אחת בחזקת אֶן חלקי אֶן. לפי לייבניץ, מתכנס."),
    P("ב-$x$ שווה מינוס חמש, שני המינוסים מבטלים זה את זה, ונשאר הטור ההרמוני. מתבדר.",
      do=hide("na-L-q") + show("a-2", "na-L-o", "na-L-v"),
      say="באִקְס שווה מינוס חמש, שני המינוסים מבטלים זה את זה, ונשאר הטור ההרמוני. מתבדר."),
    P("התחום: פתוח במינוס חמש, וסגור בחמש. אל תשננו איזה צד סגור. מחשבים כל פעם.", do=show("a-v"), hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("a", ["$\\sum\\frac{(-1)^n x^n}{n\\cdot 5^n}, \\quad R = 5$",
                        "$x = 5: \\quad \\sum\\frac{(-1)^n}{n}$",
                        "$x = -5: \\quad \\sum\\frac{(-1)^n(-1)^n}{n} = \\sum\\frac{1}{n}$"], size=36, gap=14)
         + f'<div id="a-nl" class="h" style="margin-top:20px">{NLA}</div>'
         + ws.verdict("a-v", "התחום: $(-5, 5]$") + '</div>',
   panel=st.card("p-1", "rule", "🔑 מציבים קצה: מקבלים טור מספרי")
         + st.card("p-2", "plain", "תנאי הכרחי, השוואה, לייבניץ")
         + st.card("p-3", "rule", "🔑 מתכנס: $[\\;]$. מתבדר: $(\\;)$")
         + st.card("p-4", "trap", "⚠️ לכל קצה תשובה משלו"))

both = Scene("both", "שני קצוות סגורים", [
    P("דוגמה שנייה: $x$ ועוד אחת בחזקת $n$, חלקי $n$ בריבוע כפול שתיים בחזקת $n$.", do=show("b-0"),
      say="דוגמה שנייה: אִקְס ועוד אחת בחזקת אֶן, חלקי אֶן בריבוע כפול שתיים בחזקת אֶן."),
    P("המרכז מינוס אחת, והרדיוס שתיים. אז הקצוות הם מינוס אחת פחות שתיים, ומינוס אחת ועוד שתיים.",
      do=show("b-1", "b-nl", "nb-band", "nb-L-q", "nb-R-q")),
    P("כלומר מינוס שלוש ואחת. **לא** מינוס שתיים ושתיים: הקצוות זזים עם המרכז.", do=show("b-t")),
    P("בשני הקצוות הערך המוחלט של האיבר הוא אחת חלקי $n$ בריבוע. טור $p$ עם $p$ שווה שתיים.", do=show("b-2"),
      say="בשני הקצוות הערך המוחלט של האיבר הוא אחת חלקי אֶן בריבוע. טור פִּי עם פִּי שווה שתיים."),
    P("שני הקצוות מתכנסים בהחלט, אז שניהם נכנסים: הקטע הסגור ממינוס שלוש עד אחת.",
      do=hide("nb-L-q", "nb-R-q") + show("nb-L-c", "nb-R-c", "nb-L-v", "nb-R-v", "b-v")),
    P("ועוד כלל שימושי: אם התחום של הטור ב-$X$ ידוע, מזיזים אותו. בלי לחשב מחדש.", do=show("b-s1"),
      say="ועוד כלל שימושי: אם התחום של הטור באִקְס גדולה ידוע, מזיזים אותו. בלי לחשב מחדש."),
    P("למשל תחום ממינוס שתיים כולל, עד שתיים לא כולל. עם $x$ ועוד שלוש, מחסירים שלוש: ממינוס חמש עד מינוס אחת.",
      do=show("b-s2"), say="למשל תחום ממינוס שתיים כולל, עד שתיים לא כולל. עם אִקְס ועוד שלוש, מחסירים שלוש: ממינוס חמש עד מינוס אחת.",
      hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("b", ["$\\sum\\frac{(x+1)^n}{n^2\\cdot 2^n}$",
                        "$x_0 = -1, \\quad R = 2$",
                        "$x = -3, \\; x = 1: \\quad |a_n| = \\frac{1}{n^2}$"], size=36, gap=14)
         + f'<div id="b-nl" class="h" style="margin-top:20px">{NLB}</div>'
         + ws.verdict("b-v", "התחום: $[-3, 1]$") + '</div>',
   panel=st.card("b-t", "trap", "⚠️ הקצוות הם $x_0 \\pm R$, לא $\\pm R$")
         + st.card("b-s1", "rule", "🔑 $X = x - x_0$: אותו קטע, מוזז, עם אותם סוגריים")
         + st.card("b-s2", "ex", "$[-2, 2)$, $X = x+3$ $\\Rightarrow$ $[-5, -1)$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: עבור אילו $x$ הטור מתכנס? שתיים בחזקת $n$ חלקי שורש $n$ ועוד ארבע, כפול $x$ פחות אחת בחזקת $n$.",
      say="שאלה ממבחן: עבור אילו אִקְס הטור מתכנס? שתיים בחזקת אֶן חלקי שורש אֶן ועוד ארבע, כפול אִקְס פחות אחת בחזקת אֶן."),
    P("רדיוס: מנת המקדמים, המקדם הבא חלקי המקדם, שואפת לשתיים. זה אחת חלקי $R$, אז $R$ שווה חצי.", do=show("x-0"),
      say="רדיוס: מנת המקדמים, המקדם הבא חלקי המקדם, שואפת לשתיים. זה אחת חלקי אָר, אז אָר שווה חצי."),
    P("המרכז אחת, אז הקצוות הם אחת פחות חצי, ואחת ועוד חצי: חצי ושלוש חצאים.",
      do=show("x-1", "x-nl", "nx-band", "nx-L-q", "nx-R-q")),
    P("ב-$x$ שווה חצי: $x$ פחות אחת זה מינוס חצי, והשתיים בחזקת $n$ מצטמצמות.", do=show("x-2"),
      say="באִקְס שווה חצי: אִקְס פחות אחת זה מינוס חצי, והשתיים בחזקת אֶן מצטמצמות."),
    P("נשאר טור מתחלף, עם אחת חלקי שורש $n$ ועוד ארבע. הוא יורד לאפס, אז לפי לייבניץ מתכנס.",
      do=hide("nx-L-q") + show("nx-L-c", "nx-L-v"),
      say="נשאר טור מתחלף, עם אחת חלקי שורש אֶן ועוד ארבע. הוא יורד לאפס, אז לפי לייבניץ מתכנס."),
    P("ב-$x$ שווה שלוש חצאים: נשאר אחת חלקי שורש $n$ ועוד ארבע, בלי סימנים.", do=show("x-3"),
      say="באִקְס שווה שלוש חצאים: נשאר אחת חלקי שורש אֶן ועוד ארבע, בלי סימנים."),
    P("השוואה גבולית עם אחת חלקי שורש $n$ נותנת אחת. טור $p$ עם חצי, ולכן מתבדר.",
      do=hide("nx-R-q") + show("nx-R-o", "nx-R-v"),
      say="השוואה גבולית עם אחת חלקי שורש אֶן נותנת אחת. טור פִּי עם חצי, ולכן מתבדר."),
    P("התחום: מחצי כולל, עד שלוש חצאים לא כולל.", do=show("x-v")),
    P("ובפתרון הרשמי של המבחן נפלו כאן שתי טעויות: הקצה השמאלי נכתב מינוס חצי, וגם נכתב שבשלוש חצאים הטור מתכנס.",
      do=show("x-t")),
    P("שתיהן בדיוק המלכודות של היום: הקצוות הם המרכז פחות ועוד הרדיוס, וכל קצה בודקים עד הסוף.", hold=0.6),
], stage='<div class="sr-col">'
         + ws.eqs("x", ["$\\frac{a_{n+1}}{a_n} = 2\\cdot\\frac{\\sqrt{n+4}}{\\sqrt{n+5}} \\to 2, \\quad R = \\frac{1}{2}$",
                        "$x_0 \\pm R = 1 \\pm \\frac{1}{2}$",
                        "$x = \\frac{1}{2}: \\quad \\sum\\frac{(-1)^n}{\\sqrt{n+4}}$",
                        "$x = \\frac{3}{2}: \\quad \\sum\\frac{1}{\\sqrt{n+4}}, \\quad \\frac{1/\\sqrt{n+4}}{1/\\sqrt{n}} \\to 1$"],
                  size=31, gap=8)
         + f'<div id="x-nl" class="h" style="margin-top:14px">{NLX}</div></div>',
   panel=ws.stem(EX["id"], "עבור אילו ערכי $x$ הטור מתכנס? (רדיוס ותחום)"
                 '<div class="sr-mid" style="font-size:34px">$\\displaystyle \\sum_{n=1}^{\\infty}\\frac{2^n}{\\sqrt{n+4}}(x-1)^n$</div>')
         + ws.verdict("x-v", "התחום: $\\left[\\frac{1}{2}, \\frac{3}{2}\\right)$")
         + st.card("x-t", "trap", "⚠️ שתי טעויות במפתח הרשמי:<br>הקצה השמאלי נכתב $-\\frac{1}{2}$<br>"
                    "ונכתב שב-$x=\\frac{3}{2}$ הטור מתכנס"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: הקצוות הם המרכז פחות הרדיוס, והמרכז ועוד הרדיוס.", do=show("r-1")),
    P("מציבים כל קצה, ומקבלים טור מספרי. מסווגים אותו בכלים הרגילים.", do=show("r-2")),
    P("מתכנס: סוגר מרובע. מתבדר: סוגר עגול. ולכל קצה תשובה משלו.", do=show("r-3")),
    P("ואם התחום של הטור הבסיסי ידוע, הזזה פשוט מזיזה את הקטע. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="sr-col"><div class="sr-big">$x_0 - R, \\quad x_0 + R$</div></div>',
   panel=st.card("r-1", "rule", "🔑 קצוות: $x_0 \\pm R$")
         + st.card("r-2", "rule", "🔑 מציבים: טור מספרי, תנאי הכרחי / השוואה / לייבניץ")
         + st.card("r-3", "rule", "🔑 מתכנס $[\\;]$, מתבדר $(\\;)$")
         + st.card("r-4", "rule", "🔑 $X = x - x_0$: מזיזים את הקטע"))

VIDEO = Video("S06", "series", "הקצוות: המלכודת הקלאסית", ws.fix_scenes([title, recipe, both, exam, recap]),
              bank={"24B-B-Q4b": None})
