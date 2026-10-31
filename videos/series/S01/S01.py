# -*- coding: utf-8 -*-
"""S01 · תנאי הכרחי, טור הנדסי וטור p — video script (build: tools/video/vid.py S01).

Source: courses/series/C01.js (lesson + goal). Exam anchor: 24B-B-Q2a (cos(πn)(n²+3ln n)/((n+1)(n+2)): the term
does not tend to 0), which no guided quiz uses. Not used on purpose: the C01 quiz series (n²+1)/(2n²+3), Σ5/3^n,
Σ_{n≥2} 1/3^n, Σ(x/4)^n, the p-series of C01-Q5 and the lesson's own example Σ2/3^n; the examples here are
Σ1/2^n, Σ(3n-1)/(n+4), the harmonic series, Σ(-2/5)^n, 1/∛(n²) and 1/(n²√n).
Every limit, sum and partial sum on screen is computed below with sympy/mpmath and asserted.
"""
from vid import P, Scene, Video, show, hide, BANK
import sympy as sp
import stage as st
import w_series as ws
from w_series import n

# ---------------------------------------------------------------- checks
# idea: Σ 1/2^n, S_N = 1 - 2^-N -> 1
G = sp.Rational(1, 2) ** n
SG = ws.psums(G, 10)
assert all(abs(SG[k - 1] - (1 - 2.0 ** -k)) < 1e-12 for k in range(1, 11))
assert sp.summation(G, (n, 1, sp.oo)) == 1

# necessary condition: (3n-1)/(n+4) -> 3, partial sums grow
A1 = (3 * n - 1) / (n + 4)
assert ws.lim(A1) == 3
SA1 = ws.psums(A1, 10)
assert SA1[0] == 0.4 and all(b > a for a, b in zip(SA1, SA1[1:])) and SA1[-1] > 14

# harmonic: 1/n -> 0 but H_{2^k} >= 1 + k/2
assert ws.lim(1 / n) == 0
H = [sum(sp.Rational(1, i) for i in range(1, 2 ** k + 1)) for k in range(0, 11)]
assert all(H[k] >= 1 + sp.Rational(k, 2) for k in range(0, 11))
assert sp.Rational(1, 3) + sp.Rational(1, 4) > sp.Rational(1, 2)          # first block > 1/2
assert sum(sp.Rational(1, i) for i in range(5, 9)) > sp.Rational(1, 2)     # second block > 1/2 (4 terms >= 1/8)
SH = ws.psums(1 / n, 16)

# geometric with a negative ratio: Σ_{n>=1} (-2/5)^n = -2/7
Q = sp.Rational(-2, 5)
assert sp.summation(Q ** n, (n, 1, sp.oo)) == sp.Rational(-2, 7)
assert Q / (1 - Q) == sp.Rational(-2, 7)
SQ = ws.psums(Q ** n, 10)
assert abs(SQ[-1] + 2 / 7) < 1e-3 and SQ[0] == -0.4

# p-series examples
assert sp.simplify(1 / sp.cbrt(n ** 2) - n ** sp.Rational(-2, 3)) == 0
assert sp.simplify(1 / (n ** 2 * sp.sqrt(n)) - n ** sp.Rational(-5, 2)) == 0
assert sp.summation(1 / n ** 2, (n, 1, sp.oo)) == sp.pi ** 2 / 6           # converges (p = 2)

# exam 24B-B-Q2a
EX = BANK["24B-B-Q2a"]
assert r"\cos(\pi n)\cdot(n^2+3\ln n)" in EX["question"]
A = (n ** 2 + 3 * sp.log(n)) / ((n + 1) * (n + 2))
assert sp.simplify(sp.cos(sp.pi * n) - (-1) ** n) == 0
assert ws.lim(sp.log(n) / n ** 2) == 0
assert ws.lim(A) == 1
SE = ws.psums((-1) ** n * A, 12)
assert all((SE[k] - SE[k - 1]) * (-1) ** (k + 1) > 0.15 for k in range(1, 12))      # jumps of size > 0.15 forever
assert all(abs(SE[k] - SE[k - 1]) > abs(SE[1] - SE[0]) for k in range(2, 12))       # and they grow towards 1
assert min(SE) < -0.1 and max(SE) > 0.3

B1 = ws.bars("g1", SG, w=800, h=300, limit=1.0, limit_tex="$S=1$", label="$S_N$", ymin=0)
B2 = ws.bars("d1", SA1, w=880, h=210, label="$S_N$")
B3 = ws.bars("h1", SH, w=880, h=190, label="$H_N$", nlabels={1, 4, 8, 12, 16})
B4 = ws.bars("q1", SQ, w=800, h=210, limit=-2 / 7, limit_tex="$S=-\\frac{2}{7}$", label="$S_N$")
B5 = ws.bars("e1", SE, w=880, h=200, label="$S_N$")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד מה זה טור, ומה הצעד הראשון בכל שאלת סיווג."),
    P("נכיר שני טורים שצריך לדעת בעל פה: הטור ההנדסי וטור $p$.",
      say="נכיר שני טורים שצריך לדעת בעל פה: הטור ההנדסי וטור פִּי."),
    P("ובסוף נפתור יחד שאלה ממבחן.", hold=0.4),
], stage='<div class="kicker">S01 · טורים</div><h1>תנאי הכרחי, טור הנדסי וטור p</h1>'
         '<p>להכריע מיד כשהאיבר הכללי לא שואף לאפס, ולזהות טור הנדסי וטור p.</p>', layout="title")

idea = Scene("idea", "מה זה טור", [
    P("טור הוא סכום אינסופי. אבל אי אפשר לחבר אינסוף מספרים בבת אחת.", do=show("i-0")),
    P("לכן מגדירים **סכום חלקי**: $S_N$ הוא סכום $N$ האיברים הראשונים.", do=show("i-1"),
      say="לכן מגדירים סכום חלקי: אֶס אֶן הוא סכום אֶן האיברים הראשונים."),
    P("הטור **מתכנס** אם לסדרה $S_N$ יש גבול סופי. הגבול הזה הוא סכום הטור.", do=show("c-def"),
      say="הטור מתכנס אם לסדרה אֶס אֶן יש גבול סופי. הגבול הזה הוא סכום הטור."),
    P("נראה את זה על הטור: אחת חלקי שתיים בחזקת $n$.", do=show("i-2"),
      say="נראה את זה על הטור: אחת חלקי שתיים בחזקת אֶן."),
    P("$S_1$ הוא חצי. $S_2$ הוא שלושה רבעים. $S_3$ הוא שבע שמיניות.", do=show(*ws.bars_do("g1", 1, 3)),
      say="אֶס אחת הוא חצי. אֶס שתיים הוא שלושה רבעים. אֶס שלוש הוא שבע שמיניות."),
    P("בכל צעד חסר בדיוק אחת חלקי שתיים בחזקת $N$ עד אחת.", do=show(*ws.bars_do("g1", 4, 10)),
      say="בכל צעד חסר בדיוק אחת חלקי שתיים בחזקת אֶן עד אחת."),
    P("והחסר הזה שואף לאפס. לכן הסכומים החלקיים שואפים לאחת, והטור מתכנס לאחת.", do=show("g1-lim", "g1-limt", "c-ex")),
    P("ואם הגבול אינסופי, או לא קיים בכלל, הטור **מתבדר**.", do=show("c-div"), hold=0.4),
], stage='<div class="sr-col">'
         '<div id="i-0" class="sr-mid h">$\\sum_{n=1}^{\\infty} a_n = a_1 + a_2 + a_3 + \\cdots$</div>'
         '<div id="i-1" class="sr-mid h">$S_N = a_1 + a_2 + \\cdots + a_N$</div>'
         f'<div id="i-2" class="h" style="margin-top:50px">{B1}</div></div>',
   panel=st.card("c-def", "rule", "🔑 מתכנס $\\iff$ $\\lim S_N$ קיים וסופי")
         + st.card("c-ex", "ex", "$\\sum\\frac{1}{2^n}$: $S_N = 1-\\frac{1}{2^N} \\to 1$")
         + st.card("c-div", "plain", "גבול אינסופי, או שאין גבול: מתבדר"))

nec = Scene("nec", "התנאי ההכרחי", [
    P("הכלי הראשון בכל סיווג: **התנאי ההכרחי**. אם הטור מתכנס, האיבר הכללי שואף לאפס.", do=show("n-0")),
    P("למה? האיבר ה-$n$ הוא ההפרש בין שני סכומים חלקיים צמודים.", do=show("n-1"),
      say="למה? האיבר האֶן הוא ההפרש בין שני סכומים חלקיים צמודים."),
    P("אם הטור מתכנס לסכום $S$, שני הסכומים שואפים ל-$S$, וההפרש שלהם שואף לאפס.", do=show("n-2"),
      say="אם הטור מתכנס לסכום אֶס, שני הסכומים שואפים לאֶס, וההפרש שלהם שואף לאפס."),
    P("ומה שימושי באמת זה הכיוון ההפוך: אם האיבר **לא** שואף לאפס, הטור מתבדר.", do=show("n-r")),
    P("למשל שלוש $n$ פחות אחת, חלקי $n$ ועוד ארבע. האיבר הזה שואף לשלוש.", do=show("n-3"),
      say="למשל שלוש אֶן פחות אחת, חלקי אֶן ועוד ארבע. האיבר הזה שואף לשלוש."),
    P("אז כל איבר מוסיף לסכום בערך שלוש, והסכומים החלקיים בורחים לאינסוף.", do=show("n-4", *ws.bars_do("d1", 1, 10))),
    P("הטור מתבדר, בלי שום מבחן נוסף.", do=show("n-v"), hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("n", ["$\\sum a_n = S \\;\\Rightarrow\\; a_n \\to 0$",
                        "$a_n = S_n - S_{n-1}$",
                        "$a_n \\to S - S = 0$",
                        "$a_n = \\frac{3n-1}{n+4} \\to 3 \\ne 0$"], size=34, gap=4)
         + f'<div id="n-4" class="h" style="margin-top:44px">{B2}</div>'
         + ws.verdict("n-v", "מתבדר", ok=False) + '</div>',
   panel=st.card("n-r", "rule", "🔑 $a_n \\not\\to 0$ $\\Rightarrow$ הטור מתבדר. זה הצעד הראשון בכל סיווג"))

harm = Scene("harm", "ההפך לא נכון", [
    P("זהירות: ההפך **לא** נכון. איבר ששואף לאפס עוד לא אומר שהטור מתכנס.", do=show("h-t")),
    P("הדוגמה הקלאסית: הטור ההרמוני, סכום אחת חלקי $n$. האיבר שואף לאפס.", do=show("h-0"),
      say="הדוגמה הקלאסית: הטור ההרמוני, סכום אחת חלקי אֶן. האיבר שואף לאפס."),
    P("הסכומים החלקיים גדלים לאט מאוד.", do=show("h-b", *ws.bars_do("h1", 1, 16))),
    P("אבל נקבץ את האיברים: שליש ועוד רבע גדול מחצי, כי כל אחד מהם לפחות רבע.", do=show("h-1")),
    P("ארבעת האיברים מחמישית עד שמינית: כל אחד לפחות שמינית, ולכן יחד לפחות חצי.", do=show("h-2")),
    P("וכך כל בלוק נותן עוד חצי. אחרי $2^k$ איברים הסכום לפחות אחת ועוד $k$ חצאים.", do=show("h-3"),
      say="וכך כל בלוק נותן עוד חצי. אחרי שתיים בחזקת קֵיי איברים, הסכום לפחות אחת ועוד קֵיי חצאים."),
    P("זה שואף לאינסוף, ולכן הטור ההרמוני מתבדר, למרות שהאיבר שלו שואף לאפס.", do=show("h-v"), hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("h", ["$\\sum_{n=1}^{\\infty}\\frac{1}{n}, \\quad \\frac{1}{n} \\to 0$",
                        "$\\frac{1}{3}+\\frac{1}{4} \\ge \\frac{1}{4}+\\frac{1}{4} = \\frac{1}{2}$",
                        "$\\frac{1}{5}+\\frac{1}{6}+\\frac{1}{7}+\\frac{1}{8} \\ge 4\\cdot\\frac{1}{8} = \\frac{1}{2}$",
                        "$H_{2^k} \\ge 1 + \\frac{k}{2} \\to \\infty$"], size=32, gap=0)
         + f'<div id="h-b" class="h" style="margin-top:40px">{B3}</div></div>',
   panel=st.card("h-t", "trap", "⚠️ $a_n \\to 0$ הכרחי, אבל <b>לא מספיק</b>")
         + ws.verdict("h-v", "ההרמוני מתבדר", ok=False))

geo = Scene("geo", "טור הנדסי", [
    P("הטור הראשון שצריך להכיר: **הטור ההנדסי**. כל איבר שווה לקודם כפול מנה קבועה $q$.", do=show("g-0"),
      say="הטור הראשון שצריך להכיר: הטור ההנדסי. כל איבר שווה לקודם כפול מנה קבועה, קְיוּ."),
    P("הוא מתכנס בדיוק כשהערך המוחלט של $q$ קטן מאחת.", do=show("g-r1"),
      say="הוא מתכנס בדיוק כשהערך המוחלט של קְיוּ קטן מאחת."),
    P("ואז הסכום הוא האיבר הראשון, חלקי אחת פחות $q$.", do=show("g-r2"),
      say="ואז הסכום הוא האיבר הראשון, חלקי אחת פחות קְיוּ."),
    P("אם הערך המוחלט של $q$ לפחות אחת, האיבר לא שואף לאפס, והטור מתבדר מהתנאי ההכרחי.", do=show("g-r3"),
      say="אם הערך המוחלט של קְיוּ לפחות אחת, האיבר לא שואף לאפס, והטור מתבדר מהתנאי ההכרחי."),
    P("דוגמה: מינוס שתי חמישיות, בחזקת $n$, מ-$n$ שווה אחת.", do=show("g-1"),
      say="דוגמה: מינוס שתי חמישיות, בחזקת אֶן, מאֶן שווה אחת."),
    P("הערך המוחלט של המנה קטן מאחת, אז הטור מתכנס.", do=show("g-2")),
    P("שימו לב: האיבר הראשון הוא מה שמתקבל ב-$n$ שווה אחת, כלומר מינוס שתי חמישיות.", do=show("g-3"),
      say="שימו לב: האיבר הראשון הוא מה שמתקבל באֶן שווה אחת, כלומר מינוס שתי חמישיות."),
    P("לכן הסכום הוא מינוס שתי חמישיות, חלקי שבע חמישיות: מינוס שתי שביעיות.", do=show("g-4")),
    P("והסכומים החלקיים קופצים מעל ומתחת, ומתקרבים בדיוק לשם.", do=show("g-b", *ws.bars_do("q1", 1, 10), "q1-lim", "q1-limt"),
      hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("g", ["$a_{n+1} = q \\cdot a_n$",
                        "$\\sum_{n=1}^{\\infty}\\left(-\\frac{2}{5}\\right)^n$",
                        "$q = -\\frac{2}{5}, \\quad |q| < 1$",
                        "$a_1 = -\\frac{2}{5}$",
                        "$S = \\frac{-2/5}{1+2/5} = -\\frac{2}{7}$"], size=32, gap=0)
         + f'<div id="g-b" class="h" style="margin-top:30px">{B4}</div></div>',
   panel=st.card("g-r1", "rule", "🔑 $\\sum q^n$ מתכנס $\\iff$ $|q|<1$")
         + st.card("g-r2", "rule", "🔑 $S = \\dfrac{a_1}{1-q}$, כש-$a_1$ האיבר הראשון <b>בטור</b>")
         + st.card("g-r3", "plain", "$|q| \\ge 1$: האיבר לא שואף ל-$0$, מתבדר"))

pser = Scene("pser", "טור p", [
    P("הטור השני: **טור $p$**, סכום אחת חלקי $n$ בחזקת $p$.", do=show("p-0"),
      say="הטור השני: טור פִּי, סכום אחת חלקי אֶן בחזקת פִּי."),
    P("המשפט: הוא מתכנס אם ורק אם $p$ גדול מאחת. את ההוכחה נראה ברמה שלוש, במבחן האינטגרל.",
      do=show("p-r"), say="המשפט: הוא מתכנס אם ורק אם פִּי גדול מאחת. את ההוכחה נראה ברמה שלוש, במבחן האינטגרל."),
    P("$p$ שווה אחת זה בדיוק הטור ההרמוני, שראינו שמתבדר. זה הגבול בין המקרים.", do=show("p-h"),
      say="פִּי שווה אחת זה בדיוק הטור ההרמוני, שראינו שמתבדר. זה הגבול בין המקרים."),
    P("הטריק הוא לכתוב את האיבר כחזקה של $n$. שורש שלישי של $n$ בריבוע, זה $n$ בחזקת שתיים שלישיות.",
      do=show("p-1"), say="הטריק הוא לכתוב את האיבר כחזקה של אֶן. שורש שלישי של אֶן בריבוע, זה אֶן בחזקת שתיים שלישיות."),
    P("שתיים שלישיות קטן מאחת, ולכן הטור הזה מתבדר.", do=show("p-1v")),
    P("ו-$n$ בריבוע כפול שורש $n$, זה $n$ בחזקת חמש חצאים.", do=show("p-2"),
      say="ואֶן בריבוע כפול שורש אֶן, זה אֶן בחזקת חמש חצאים."),
    P("חמש חצאים גדול מאחת, ולכן הטור הזה מתכנס.", do=show("p-2v"), hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("p", ["$\\sum_{n=1}^{\\infty}\\frac{1}{n^p}$"], size=54)
         + '<div class="sr-row" style="margin-top:40px">'
         + '<div class="sr-col"><div id="p-1" class="sr-mid h">$\\frac{1}{\\sqrt[3]{n^2}} = \\frac{1}{n^{2/3}}$</div>'
         + ws.verdict("p-1v", "מתבדר", ok=False) + '</div>'
         + '<div class="sr-col"><div id="p-2" class="sr-mid h">$\\frac{1}{n^2\\sqrt{n}} = \\frac{1}{n^{5/2}}$</div>'
         + ws.verdict("p-2v", "מתכנס", ok=True) + '</div>'
         + '</div></div>',
   panel=st.card("p-r", "rule", "🔑 $\\sum \\frac{1}{n^p}$ מתכנס $\\iff$ $p > 1$")
         + st.card("p-h", "trap", "⚠️ $p = 1$: הטור ההרמוני, מתבדר"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן: לבדוק התכנסות בהחלט, בתנאי או התבדרות של הטור הזה."),
    P("קודם כול, קוסינוס של פאי $n$ הוא מינוס אחת בחזקת $n$. אז זה טור עם סימנים מתחלפים.", do=show("x-0"),
      say="קודם כול, קוסינוס של פאי אֶן הוא מינוס אחת בחזקת אֶן. אז זה טור עם סימנים מתחלפים."),
    P("וזו המלכודת: לראות סימנים מתחלפים ולרוץ ישר ללייבניץ.", do=show("x-t")),
    P("אבל הצעד הראשון הוא תמיד התנאי ההכרחי. נחשב את הגבול של הערך המוחלט.", do=show("x-1")),
    P("נחלק מונה ומכנה ב-$n$ בריבוע.", do=show("x-2"), say="נחלק מונה ומכנה באֶן בריבוע."),
    P("לן של $n$ חלקי $n$ בריבוע שואף לאפס, כי הלוגריתם גדל לאט יותר מכל חזקה של $n$.", do=show("x-3"),
      say="לן של אֶן חלקי אֶן בריבוע שואף לאפס, כי הלוגריתם גדל לאט יותר מכל חזקה של אֶן."),
    P("כך שהמונה שואף לאחת, וגם המכנה שואף לאחת. הגבול הוא אחת.", do=show("x-4")),
    P("הערך המוחלט שואף לאחת, אז האיבר עצמו לא שואף לאפס. הוא קופץ בין קרוב לאחת לקרוב למינוס אחת.",
      do=show("x-b", "x-c", *ws.bars_do("e1", 1, 12))),
    P("התנאי ההכרחי לא מתקיים, ולכן הטור **מתבדר**. ואין טעם לבדוק לייבניץ.", do=show("x-v"), hold=0.6),
], stage='<div class="sr-col">'
         + ws.eqs("x", ["$\\cos(\\pi n) = (-1)^n$",
                        "$|a_n| = \\frac{n^2+3\\ln n}{(n+1)(n+2)}$",
                        "$|a_n| = \\frac{1+\\frac{3\\ln n}{n^2}}{1+\\frac{3}{n}+\\frac{2}{n^2}}$"], size=32, gap=2)
         + '<div class="sr-row" style="font-size:32px">'
         + '<div id="x-3" class="sr-eq h">$\\displaystyle\\frac{\\ln n}{n^2} \\to 0$</div>'
         + '<div id="x-4" class="sr-eq h">$\\displaystyle |a_n| \\to 1 \\ne 0$</div></div>'
         + f'<div id="x-b" class="h" style="margin-top:40px">{B5}</div></div>',
   panel=ws.stem(EX["id"], "בדקו התכנסות בהחלט, בתנאי או התבדרות:"
                 "<div class=\"sr-mid\" style=\"font-size:34px;margin-top:8px\">"
                 "$\\sum_{n=1}^{\\infty}\\frac{\\cos(\\pi n)\\cdot(n^2+3\\ln n)}{(n+1)(n+2)}$</div>")
         + st.card("x-t", "trap", "⚠️ סימנים מתחלפים? קודם התנאי ההכרחי, ורק אחר כך לייבניץ")
         + st.card("x-c", "plain", "הקפיצות $|S_N - S_{N-1}| = |a_N| \\to 1$")
         + ws.verdict("x-v", "מתבדר", ok=False))

recap = Scene("recap", "סיכום", [
    P("לסיכום: טור מתכנס כשהסכומים החלקיים שואפים לגבול סופי.", do=show("r-1")),
    P("הצעד הראשון: אם האיבר לא שואף לאפס, הטור מתבדר. ההפך לא נכון, כמו בטור ההרמוני.", do=show("r-2")),
    P("טור הנדסי מתכנס כשהמנה בערך מוחלט קטנה מאחת.", do=show("r-3")),
    P("וטור $p$ מתכנס רק כש-$p$ גדול מאחת. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6,
      say="וטור פִּי מתכנס רק כשפִּי גדול מאחת. נתראה ברמה הבאה."),
], stage='<div class="sr-col"><div class="sr-big">$S = \\lim_{N\\to\\infty} S_N$</div></div>',
   panel=st.card("r-1", "rule", "🔑 מתכנס $\\iff$ $S_N$ שואף לגבול סופי")
         + st.card("r-2", "rule", "🔑 $a_n \\not\\to 0$ $\\Rightarrow$ מתבדר (ולא להפך)")
         + st.card("r-3", "rule", "🔑 הנדסי: $|q|<1$, $S=\\frac{a_1}{1-q}$")
         + st.card("r-4", "rule", "🔑 $\\sum\\frac{1}{n^p}$: מתכנס רק אם $p>1$"))

VIDEO = Video("S01", "series", "תנאי הכרחי, טור הנדסי וטור p", ws.fix_scenes([title, idea, nec, harm, geo, pser, exam, recap]),
              bank={"24B-B-Q2a": None})
