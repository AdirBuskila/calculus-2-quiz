# -*- coding: utf-8 -*-
"""S08 · בוס: שאלות אמיתיות מהמבחנים — video script (build: tools/video/vid.py S08). Boss level: exam walkthroughs.

Source: courses/series/C08.js (boss; its quiz is 24B-A-Q2b, 26A-A-Q2a, 24B-A-Q4b, 26A-A-Q3a, 24B-A-Q5b, 24B-A-Q5c,
none of them solved here). Exam anchors, all series-topic parts no guided quiz uses:
  24A-A-Q2a  (-1)^n sin(1/√n) and (-1)^n(√n - √(n-1)): both conditionally convergent
  25A-B-Q3a  Σ sin²(1/n)(x-1)^n: R = 1, both endpoints converge (absolutely): [0, 2]
  26A-A-Q5b  (16-5x)/(x²-5x+6): partial fractions, Maclaurin series, |x| < 2, f^(20)(0) = 20!(3/2^20 - 1/3^21)
Avoided on purpose: 23A-C-Q2a, whose first series (2^n cos n/3^n) is the boss quiz's 26A-A-Q2a.
Every limit, endpoint verdict, coefficient and derivative is asserted below.
"""
from vid import P, Scene, Video, show, hide, BANK
import sympy as sp
import stage as st
import w_series as ws
from w_series import n

x = sp.Symbol("x", real=True)

# ---------------------------------------------------------------- 24A-A-Q2a
Q1 = BANK["24A-A-Q2a"]
assert r"(-1)^n\sin\frac{1}{\sqrt{n}}" in Q1["question"] and r"\sqrt{n}-\sqrt{n-1}" in Q1["question"]
S1 = sp.sin(1 / sp.sqrt(n))
assert ws.lim(S1 / (1 / sp.sqrt(n))) == 1 and ws.lim(S1) == 0
assert all(sp.sin(1 / sp.sqrt(j + 1)) < sp.sin(1 / sp.sqrt(j)) for j in range(1, 300))   # 1/√n in (0,1] ⊂ (0,π/2]
assert ws.tail(S1, 10 ** 4, 10 ** 5) > 400                                               # Σ|a_n| grows like 2√N
A2 = sp.sqrt(n) - sp.sqrt(n - 1)
assert sp.simplify(A2 - 1 / (sp.sqrt(n) + sp.sqrt(n - 1))) == 0
assert ws.lim(A2) == 0
assert all((sp.sqrt(j + 1) - sp.sqrt(j)) < (sp.sqrt(j) - sp.sqrt(j - 1)) for j in range(1, 300))
assert sum(sp.sqrt(j) - sp.sqrt(j - 1) for j in range(1, 101)) == 10                     # telescopes: S_N = √N
assert ws.lim(A2 / (1 / sp.sqrt(n))) == sp.Rational(1, 2)
SE = ws.psums((-1) ** n * S1, 14)

# ---------------------------------------------------------------- 25A-B-Q3a
Q2 = BANK["25A-B-Q3a"]
assert r"\sin^2\left(\frac1n\right)(x-1)^n" in Q2["question"]
C = sp.sin(1 / n) ** 2
assert ws.radius(C) == 1
assert ws.lim(C / (1 / n ** 2)) == 1
assert ws.tail(C, 10 ** 4, 10 ** 5) < 1e-4                                                # tail ≈ 1/N1 - 1/N2
# endpoints x = 1 ± 1: x = 2 -> Σ sin²(1/n); x = 0 -> Σ (-1)^n sin²(1/n), |term| the same -> absolutely
D2 = sp.Interval(0, 2)

# ---------------------------------------------------------------- 26A-A-Q5b
Q3 = BANK["26A-A-Q5b"]
assert r"f(x)=\dfrac{16-5x}{x^2-5x+6}" in Q3["question"]
F = (16 - 5 * x) / (x ** 2 - 5 * x + 6)
assert sp.factor(x ** 2 - 5 * x + 6) == (x - 3) * (x - 2)
assert sp.simplify(F - (-6 / (x - 2) + 1 / (x - 3))) == 0
assert sp.simplify(F - (6 / (2 - x) - 1 / (3 - x))) == 0
COEF = 3 / sp.Integer(2) ** n - 1 / sp.Integer(3) ** (n + 1)
ser = sp.series(F, x, 0, 21).removeO()
assert all(sp.simplify(ser.coeff(x, k) - COEF.subs(n, k)) == 0 for k in range(0, 21))
d20 = sp.factorial(20) * COEF.subs(n, 20)
assert d20 == sp.factorial(20) * (sp.Rational(3, 2 ** 20) - sp.Rational(1, 3 ** 21))
assert sp.diff(F, x, 6).subs(x, 0) == sp.factorial(6) * COEF.subs(n, 6)                  # the k!·a_k rule, checked at k=6
# domain: 6/(2-x) needs |x|<2, 1/(3-x) needs |x|<3: intersection |x|<2; at x = ±2 the first part's terms 3(±1)^n
# do not tend to 0 while the second converges, so the sum diverges there
assert ws.lim(COEF * 2 ** n) == 3                                                         # |a_n|·2^n -> 3 ≠ 0
assert ws.radius(COEF) == 2

NL2 = ws.numline("na", -1.5, 3.5, [(0, "$0$"), (1, "$1$"), (2, "$2$")], 0, 2, w=860,
                 verdicts={"L": ("בהחלט: מתכנס", True), "R": ("$\\frac{1}{n^2}$: מתכנס", True)})
NL3 = ws.numline("nb", -4, 4, [(-3, "$-3$"), (-2, "$-2$"), (0, "$0$"), (2, "$2$"), (3, "$3$")], -2, 2, w=860,
                 verdicts={"L": ("$a_n \\not\\to 0$", False), "R": ("$a_n \\not\\to 0$", False)})
B1 = ws.bars("e1", SE, w=860, h=120, label="$S_N$")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("זה מבחן הגמר של הפרק על טורים."),
    P("נפתור יחד שלוש שאלות אמיתיות: סיווג של טורים, תחום התכנסות, ופיתוח מקלורן עם נגזרת."),
    P("ובכל אחת נחפש איפה קל לאבד נקודות.", hold=0.4),
], stage='<div class="kicker">S08 · טורים</div><h1>בוס: שאלות אמיתיות מהמבחנים</h1>'
         '<p>סיווג, רדיוס וקצוות, ומקלורן עם הנגזרת באפס, כפי שהם מופיעים במבחן.</p>', layout="title")

q1 = Scene("q1", "שאלה 1: סיווג", [
    P("שאלה ראשונה: בהחלט, בתנאי, או מתבדר. הטור הראשון: מינוס אחת בחזקת $n$, כפול סינוס של אחת חלקי שורש $n$.",
      say="שאלה ראשונה: בהחלט, בתנאי, או מתבדר. הטור הראשון: מינוס אחת בחזקת אֶן, כפול סינוס של אחת חלקי שורש אֶן."),
    P("ערך מוחלט: סינוס של משהו קטן מתנהג כמו הדבר עצמו. השוואה גבולית עם אחת חלקי שורש $n$ נותנת אחת.",
      do=show("a-0"), say="ערך מוחלט: סינוס של משהו קטן מתנהג כמו הדבר עצמו. השוואה גבולית עם אחת חלקי שורש אֶן נותנת אחת."),
    P("טור $p$ עם חצי מתבדר, אז אין התכנסות בהחלט.", do=show("a-1"), say="טור פִּי עם חצי מתבדר, אז אין התכנסות בהחלט."),
    P("לייבניץ: אחת חלקי שורש $n$ יורד ונמצא בין אפס לאחת, ושם הסינוס עולה. אז האיבר יורד לאפס.", do=show("a-2"),
      say="לייבניץ: אחת חלקי שורש אֶן יורד ונמצא בין אפס לאחת, ושם הסינוס עולה. אז האיבר יורד לאפס."),
    P("הטור הראשון **מתכנס בתנאי**.", do=show("a-v1", "a-b", *ws.bars_do("e1", 1, 14))),
    P("הטור השני: שורש $n$ פחות שורש $n$ פחות אחת. הטריק: כופלים ומחלקים בצמוד.", do=show("a-3"),
      say="הטור השני: שורש אֶן פחות שורש אֶן פחות אחת. הטריק: כופלים ומחלקים בצמוד."),
    P("מקבלים אחת חלקי סכום השורשים. בהשוואה גבולית עם אחת חלקי שורש $n$ יוצא חצי, אז אין התכנסות בהחלט.",
      do=show("a-4"), say="מקבלים אחת חלקי סכום השורשים. בהשוואה גבולית עם אחת חלקי שורש אֶן יוצא חצי, אז אין התכנסות בהחלט."),
    P("והמכנה עולה, אז האיבר יורד לאפס. לייבניץ: גם הטור השני **מתכנס בתנאי**.", do=show("a-5", "a-v2")),
    P("המלכודת בשניהם: לעצור אחרי לייבניץ. השאלה דורשת להכריע גם שאין התכנסות בהחלט.", do=show("a-t"), hold=0.5),
], stage='<div class="sr-col">'
         + ws.eqs("a", ["$\\frac{\\sin(1/\\sqrt{n})}{1/\\sqrt{n}} \\to 1$",
                        "$\\sum\\frac{1}{\\sqrt{n}} = \\infty \\;\\Rightarrow\\; \\sum|a_n| = \\infty$",
                        "$0 < \\frac{1}{\\sqrt{n}} \\le 1 < \\frac{\\pi}{2} \\;\\Rightarrow\\; \\sin\\frac{1}{\\sqrt{n}} \\searrow 0$",
                        "$\\sqrt{n} - \\sqrt{n-1} = \\frac{1}{\\sqrt{n}+\\sqrt{n-1}}$",
                        "$\\frac{1/(\\sqrt{n}+\\sqrt{n-1})}{1/\\sqrt{n}} \\to \\frac{1}{2}$",
                        "$\\frac{1}{\\sqrt{n}+\\sqrt{n-1}} \\searrow 0$"], size=27, gap=0)
         + f'<div id="a-b" class="h" style="margin-top:30px">{B1}</div></div>',
   panel=ws.stem(Q1["id"], "בדקו התכנסות בהחלט, בתנאי או התבדרות:"
                 '<div class="sr-mid" style="font-size:28px">$\\displaystyle \\sum_{n=1}^{\\infty}(-1)^n\\sin\\frac{1}{\\sqrt{n}}'
                 ' \\quad\\; \\sum_{n=1}^{\\infty}(-1)^n\\left(\\sqrt{n}-\\sqrt{n-1}\\right)$</div>')
         + ws.verdict("a-v1", "ראשון: מתכנס בתנאי")
         + ws.verdict("a-v2", "שני: מתכנס בתנאי")
         + st.card("a-t", "trap", "⚠️ לייבניץ לבד לא מספיק: בודקים גם $\\sum|a_n|$"))

q2 = Scene("q2", "שאלה 2: תחום", [
    P("שאלה שנייה: עבור אילו $x$ מתכנס סכום סינוס בריבוע של אחת חלקי $n$, כפול $x$ פחות אחת בחזקת $n$?",
      say="שאלה שנייה: עבור אילו אִקְס מתכנס סכום סינוס בריבוע של אחת חלקי אֶן, כפול אִקְס פחות אחת בחזקת אֶן?"),
    P("רדיוס לפי דלאמבר. כותבים כל סינוס כמו הארגומנט שלו, כפול מנה ששואפת לאחת.", do=show("b-0")),
    P("נשאר $n$ ועוד אחת חלקי $n$, בריבוע, ששואף לאחת. אז הרדיוס אחת, והמרכז אחת.", do=show("b-1", "b-nl", "na-band", "na-L-q", "na-R-q"),
      say="נשאר אֶן ועוד אחת חלקי אֶן, בריבוע, ששואף לאחת. אז הרדיוס אחת, והמרכז אחת."),
    P("הקצוות: אחת פחות אחת, ואחת ועוד אחת. כלומר אפס ושתיים, ולא מינוס אחת ואחת.", do=show("b-t")),
    P("ב-$x$ שווה שתיים: סכום סינוס בריבוע של אחת חלקי $n$. השוואה גבולית עם אחת חלקי $n$ בריבוע: מתכנס.",
      do=hide("na-R-q") + show("b-2", "na-R-c", "na-R-v"),
      say="באִקְס שווה שתיים: סכום סינוס בריבוע של אחת חלקי אֶן. השוואה גבולית עם אחת חלקי אֶן בריבוע: מתכנס."),
    P("ב-$x$ שווה אפס מקבלים את אותם איברים עם סימן מתחלף. הערכים המוחלטים זהים, אז מתכנס בהחלט.",
      do=hide("na-L-q") + show("na-L-c", "na-L-v"),
      say="באִקְס שווה אפס מקבלים את אותם איברים עם סימן מתחלף. הערכים המוחלטים זהים, אז מתכנס בהחלט."),
    P("התחום: הקטע הסגור מאפס עד שתיים. שני הקצוות בפנים, ומי שמנחש קטע פתוח מפספס את זה.", do=show("b-v"),
      hold=0.5),
], stage='<div class="sr-col">'
         + ws.eqs("b", ["$\\frac{\\sin^2(1/n)}{\\sin^2(1/(n+1))} = \\left(\\frac{\\sin(1/n)}{1/n}\\right)^2\\left(\\frac{1/(n+1)}{\\sin(1/(n+1))}\\right)^2\\left(\\frac{n+1}{n}\\right)^2$",
                        "$\\to 1, \\quad R = 1, \\quad x_0 = 1$",
                        "$x = 2: \\quad \\frac{\\sin^2(1/n)}{1/n^2} \\to 1, \\quad p = 2$"], size=27, gap=10)
         + f'<div id="b-nl" class="h" style="margin-top:20px">{NL2}</div></div>',
   panel=ws.stem(Q2["id"], "עבור אילו ערכי $x$ הטור מתכנס? (רדיוס ותחום)"
                 '<div class="sr-mid" style="font-size:34px">$\\displaystyle \\sum_{n=1}^{\\infty}\\sin^2\\left(\\frac{1}{n}\\right)(x-1)^n$</div>')
         + st.card("b-t", "trap", "⚠️ המרכז הוא $1$: הקצוות $0$ ו-$2$")
         + ws.verdict("b-v", "התחום: $[0, 2]$"))

q3 = Scene("q3", "שאלה 3: מקלורן", [
    P("שאלה שלישית: פתחו לטור מקלורן את שש עשרה פחות חמש $x$, חלקי $x$ בריבוע פחות חמש $x$ ועוד שש. ומה הנגזרת העשרים באפס?",
      say="שאלה שלישית: פתחו לטור מקלורן את שש עשרה פחות חמש אִקְס, חלקי אִקְס בריבוע פחות חמש אִקְס ועוד שש. ומה הנגזרת העשרים באפס?"),
    P("המכנה מתפרק ל-$x$ פחות שתיים, כפול $x$ פחות שלוש. שברים חלקיים: מציבים שתיים ושלוש, ומקבלים מינוס שש ואחת.",
      do=show("c-0"), say="המכנה מתפרק לאִקְס פחות שתיים, כפול אִקְס פחות שלוש. שברים חלקיים: מציבים שתיים ושלוש, ומקבלים מינוס שש ואחת."),
    P("הופכים סימנים כדי לקבל את הצורה אחת חלקי אחת פחות משהו: שש חלקי שתיים פחות $x$, פחות אחת חלקי שלוש פחות $x$.",
      do=show("c-1"), say="הופכים סימנים כדי לקבל את הצורה אחת חלקי אחת פחות משהו: שש חלקי שתיים פחות אִקְס, פחות אחת חלקי שלוש פחות אִקְס."),
    P("הראשון הוא שלוש כפול טור הנדסי ב-$x$ חלקי שתיים. השני הוא שליש כפול טור הנדסי ב-$x$ חלקי שלוש.", do=show("c-2"),
      say="הראשון הוא שלוש כפול טור הנדסי באִקְס חלקי שתיים. השני הוא שליש כפול טור הנדסי באִקְס חלקי שלוש."),
    P("המקדם של $x$ בחזקת $n$: שלוש חלקי שתיים בחזקת $n$, פחות אחת חלקי שלוש בחזקת $n$ ועוד אחת.", do=show("c-3"),
      say="המקדם של אִקְס בחזקת אֶן: שלוש חלקי שתיים בחזקת אֶן, פחות אחת חלקי שלוש בחזקת אֶן ועוד אחת."),
    P("התחום: הראשון דורש $x$ קטן משתיים בערך מוחלט, והשני קטן משלוש. סכום מתכנס בחיתוך: קטן משתיים.",
      do=show("c-nl", "nb-band", "nb-L-o", "nb-R-o"),
      say="התחום: הראשון דורש אִקְס קטן משתיים בערך מוחלט, והשני קטן משלוש. סכום מתכנס בחיתוך: קטן משתיים."),
    P("בפלוס מינוס שתיים, החלק הראשון נותן שלוש כפול פלוס מינוס אחת בחזקת $n$, שלא שואף לאפס. הוא מתבדר.",
      do=show("nb-L-v", "nb-R-v", "c-t"),
      say="בפלוס מינוס שתיים, החלק הראשון נותן שלוש כפול פלוס מינוס אחת בחזקת אֶן, שלא שואף לאפס. הוא מתבדר."),
    P("והחלק השני שם מתכנס. מתכנס ועוד מתבדר זה מתבדר, אז שני הקצוות בחוץ."),
    P("והנגזרת העשרים: עשרים עצרת כפול המקדם של $x$ בחזקת עשרים. לא לשכוח את העצרת.", do=show("c-4", "c-v"),
      say="והנגזרת העשרים: עשרים עצרת כפול המקדם של אִקְס בחזקת עשרים. לא לשכוח את העצרת.", hold=0.5),
], stage='<div class="sr-col">'
         + ws.eqs("c", ["$\\frac{16-5x}{(x-2)(x-3)} = \\frac{-6}{x-2} + \\frac{1}{x-3}$",
                        "$= \\frac{6}{2-x} - \\frac{1}{3-x}$",
                        "$= 3\\sum\\left(\\frac{x}{2}\\right)^n - \\frac{1}{3}\\sum\\left(\\frac{x}{3}\\right)^n$",
                        "$a_n = \\frac{3}{2^n} - \\frac{1}{3^{n+1}}$",
                        "$f^{(20)}(0) = 20!\\left(\\frac{3}{2^{20}} - \\frac{1}{3^{21}}\\right)$"], size=29, gap=4)
         + f'<div id="c-nl" class="h" style="margin-top:6px">{NL3}</div></div>',
   panel=ws.stem(Q3["id"], "פתחו לטור מקלורן. מהו תחום ההתכנסות? הסיקו את $f^{(20)}(0)$."
                 '<div class="sr-mid" style="font-size:34px">$f(x) = \\dfrac{16-5x}{x^2-5x+6}$</div>')
         + st.card("c-t", "trap", "⚠️ סכום טורים: <b>חיתוך</b> התחומים, $|x|<2$ ולא $|x|<3$")
         + ws.verdict("c-v", "$|x| < 2$"))

recap = Scene("recap", "סיכום", [
    P("סיכום הפרק כולו. בסיווג: תנאי הכרחי, אחר כך התכנסות בהחלט, ורק אז לייבניץ.", do=show("r-1")),
    P("ברדיוס: דלאמבר או קושי-הדמר, ואז כל קצה בנפרד, והקצוות הם המרכז פחות ועוד הרדיוס.", do=show("r-2")),
    P("ובמקלורן: טבלה והצבה, שברים חלקיים כשצריך, תחום מהחיתוך, ונגזרת שהיא עצרת כפול מקדם.", do=show("r-3")),
    P("בהצלחה במבחן!", do=show("r-4"), hold=0.8),
], stage='<div class="sr-col"><div class="sr-big">$\\sum a_n$</div></div>',
   panel=st.card("r-1", "rule", "🔑 $a_n \\to 0$? $\\sum|a_n|$? ורק אז לייבניץ")
         + st.card("r-2", "rule", "🔑 $R$, ואז $x_0 \\pm R$ בנפרד")
         + st.card("r-3", "rule", "🔑 טבלה, חיתוך תחומים, $f^{(k)}(0) = k!\\,a_k$")
         + st.card("r-4", "plain", "בהצלחה! 🏆"))

VIDEO = Video("S08", "series", "בוס: שאלות אמיתיות מהמבחנים", ws.fix_scenes([title, q1, q2, q3, recap]),
              bank={"24A-A-Q2a": None, "25A-B-Q3a": None, "26A-A-Q5b": None})
