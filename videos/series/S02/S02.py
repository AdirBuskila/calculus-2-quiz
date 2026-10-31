# -*- coding: utf-8 -*-
"""S02 · השוואה והשוואה גבולית — video script (build: tools/video/vid.py S02).

Source: courses/series/C02.js (lesson + goal). Exam anchor: 24S-A-Q2b (both items: cos n/∜(n⁵+2) absolutely by a
bound, (-1)^n/√(n(n+1)) not absolutely by limit comparison with 1/n, then Leibniz), which no guided quiz uses.
Not used on purpose: the C02 quiz series ((n+1)/(n³+5), (2n²+1)/(n⁴+n), (-1)^n(2+cos n)/n², 1/√(n²+n), 1/(√n+1),
sin n/n²) and the lesson's (3+sin√n)/n². The examples here: 1/(3^n+n), ln n/n and √n/(n²+1).
Every bound, limit and partial sum on screen is asserted below (sympy / mpmath / numpy).
"""
from vid import P, Scene, Video, show, hide, BANK
import numpy as np
import sympy as sp
import stage as st
import w_series as ws
from w_series import n

# ---------------------------------------------------------------- checks
# comparison, convergent side: 0 < 1/(3^n+n) < 1/3^n, Σ 1/3^n = 1/2
A1 = 1 / (3 ** n + n)
assert sp.summation(sp.Rational(1, 3) ** n, (n, 1, sp.oo)) == sp.Rational(1, 2)
k = np.arange(1, 30, dtype=np.float64)          # (exact: 3^n + n > 3^n for every n)
assert np.all(1 / (3 ** k + k) < 1 / 3 ** k)
S1 = ws.psums(A1, 8)
assert all(b > a for a, b in zip(S1, S1[1:])) and S1[-1] < 0.5          # increasing and bounded by 1/2
assert abs(S1[0] - 0.25) < 1e-12                                          # S_1 = 1/4

# comparison, divergent side: ln n / n >= 1/n for n >= 3 (ln 3 > 1)
assert sp.log(3).evalf() > 1 and sp.log(2).evalf() < 1
kk = np.arange(3, 10 ** 6, dtype=np.float64)
assert np.all(np.log(kk) / kk >= 1 / kk)

# trap: 1/n^2 <= 1/n and Σ1/n diverges, Σ1/n^2 converges
assert sp.summation(1 / n ** 2, (n, 1, sp.oo)) == sp.pi ** 2 / 6

# limit comparison: √n/(n²+1) vs 1/n^{3/2}
A2 = sp.sqrt(n) / (n ** 2 + 1)
assert ws.lim(A2 / n ** sp.Rational(-3, 2)) == 1
assert sp.simplify(A2 / n ** sp.Rational(-3, 2) - n ** 2 / (n ** 2 + 1)) == 0

# exam 24S-A-Q2b
EX = BANK["24S-A-Q2b"]
assert r"\frac{\cos(n)}{\sqrt[4]{n^5+2}}" in EX["question"] and r"\frac{(-1)^n}{\sqrt{n\cdot(n+1)}}" in EX["question"]
# item 1: |cos n| / (n^5+2)^(1/4) <= 1/n^(5/4), p = 5/4 > 1
kk = np.arange(1, 10 ** 6, dtype=np.float64)
assert np.all(np.abs(np.cos(kk)) / (kk ** 5 + 2) ** 0.25 <= kk ** -1.25)
assert sp.Rational(5, 4) > 1 and sp.simplify(sp.root(n ** 5, 4) - n ** sp.Rational(5, 4)) == 0
assert ws.tail(1 / sp.root(n ** 5 + 2, 4), 10 ** 4, 10 ** 5) < 4 * (10 ** 4) ** -0.25    # tail <= ∫ x^(-5/4)
# item 2: b_n = 1/√(n(n+1))
B = 1 / sp.sqrt(n * (n + 1))
assert ws.lim(B / (1 / n)) == 1
assert sp.simplify(B / (1 / n) - n / sp.sqrt(n ** 2 + n)) == 0
assert ws.lim(B) == 0
t = sp.Symbol("t", positive=True)
assert sp.diff(t * (t + 1), t).is_positive                                # t(t+1) strictly increasing, so b_n decreases
inc = ws.tail(B, 10 ** 4, 10 ** 5), ws.tail(B, 10 ** 5, 10 ** 6)
assert inc[0] > 2 and inc[1] > 2                                          # Σ b_n grows like ln N (≈ ln 10 per decade)
SS = ws.psums((-1) ** n * B, 12)
assert all(abs(SS[i + 1] - SS[i]) > abs(SS[i + 2] - SS[i + 1]) for i in range(10))   # jumps shrink

BA = ws.bars("c1", S1, w=760, h=230, limit=0.5, limit_tex="$\\frac{1}{2}$", label="$S_N$", ymin=0)
BX = ws.bars("x2", SS, w=860, h=190, label="$S_N$")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד להשוות טור לא מוכר לטור שכבר מכירים."),
    P("נראה את מבחן ההשוואה, את ההשוואה הגבולית, ואיך מטפלים בגורם חסום כמו קוסינוס."),
    P("ובסוף נפתור שאלה ממבחן עם שני טורים.", hold=0.4),
], stage='<div class="kicker">S02 · טורים</div><h1>השוואה והשוואה גבולית</h1>'
         '<p>לבחור טור p או טור הנדסי להשוואה, ולהכריע בהתכנסות בהחלט של טור עם גורם חסום.</p>', layout="title")

cmp_ = Scene("cmp", "מבחן ההשוואה", [
    P("שני המבחנים של היום עובדים רק על טורים עם איברים **אי-שליליים**.", do=show("m-c0")),
    P("ולמה זה חשוב? בטור כזה הסכומים החלקיים רק עולים. אז הם מתכנסים בדיוק כשהם חסומים.", do=show("m-c1")),
    P("מכאן מבחן ההשוואה: אם כל איבר של הטור הקטן קטן מהאיבר המתאים של הטור הגדול.", do=show("m-0")),
    P("והגדול מתכנס, אז הסכומים החלקיים של הקטן חסומים בסכום של הגדול, וגם הקטן מתכנס.", do=show("m-r1")),
    P("דוגמה: אחת חלקי שלוש בחזקת $n$ ועוד $n$. האיבר קטן מאחת חלקי שלוש בחזקת $n$.", do=show("m-1"),
      say="דוגמה: אחת חלקי שלוש בחזקת אֶן ועוד אֶן. האיבר קטן מאחת חלקי שלוש בחזקת אֶן."),
    P("וזה טור הנדסי עם מנה שליש, שסכומו חצי.", do=show("m-2")),
    P("אז הסכומים החלקיים עולים, אבל אף פעם לא עוברים את החצי. הטור מתכנס.",
      do=show("m-b", *ws.bars_do("c1", 1, 8), "c1-lim", "c1-limt")),
    P("והכיוון השני: אם הקטן **מתבדר**, גם הגדול מתבדר.", do=show("m-r2")),
    P("למשל לן $n$ חלקי $n$. מ-$n$ שווה שלוש, לן $n$ גדול מאחת, אז האיבר גדול מאחת חלקי $n$.", do=show("m-3"),
      say="למשל לן אֶן חלקי אֶן. מאֶן שווה שלוש, לן אֶן גדול מאחת, אז האיבר גדול מאחת חלקי אֶן."),
    P("הטור ההרמוני מתבדר, ולכן גם הטור הזה מתבדר.", do=show("m-4"), hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("m", ["$0 \\le a_n \\le b_n$",
                        "$0 < \\frac{1}{3^n+n} < \\frac{1}{3^n}$",
                        "$\\sum_{n=1}^{\\infty}\\frac{1}{3^n} = \\frac{1/3}{1-1/3} = \\frac{1}{2}$",
                        "$n \\ge 3: \\quad \\frac{\\ln n}{n} \\ge \\frac{1}{n}$",
                        "$\\sum\\frac{1}{n}$ מתבדר $\\Rightarrow$ $\\sum\\frac{\\ln n}{n}$ מתבדר"], size=30, gap=6)
         + f'<div id="m-b" class="h" style="margin-top:44px">{BA}</div></div>',
   panel=st.card("m-c0", "plain", "רק כש-$a_n \\ge 0$")
         + st.card("m-c1", "ex", "$S_N$ עולה: מתכנס $\\iff$ חסום")
         + st.card("m-r1", "rule", "🔑 הגדול מתכנס $\\Rightarrow$ הקטן מתכנס")
         + st.card("m-r2", "rule", "🔑 הקטן מתבדר $\\Rightarrow$ הגדול מתבדר"))

trap = Scene("trap", "חסם לא שימושי", [
    P("ועכשיו המלכודת: חסם **מלמעלה** על ידי טור **מתבדר** לא אומר כלום.", do=show("t-t")),
    P("אחת חלקי $n$ בריבוע קטן מאחת חלקי $n$, והטור ההרמוני מתבדר.", do=show("t-0"),
      say="אחת חלקי אֶן בריבוע קטן מאחת חלקי אֶן, והטור ההרמוני מתבדר."),
    P("אבל סכום אחת חלקי $n$ בריבוע דווקא מתכנס: זה טור $p$ עם $p$ שווה שתיים.", do=show("t-1"),
      say="אבל סכום אחת חלקי אֶן בריבוע דווקא מתכנס: זה טור פִּי עם פִּי שווה שתיים."),
    P("אז כשרוצים להוכיח התכנסות, חוסמים מלמעלה בטור **מתכנס**.", do=show("t-r1")),
    P("וכשרוצים להוכיח התבדרות, חוסמים מלמטה בטור **מתבדר**.", do=show("t-r2"), hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("t", ["$\\frac{1}{n^2} \\le \\frac{1}{n}, \\quad \\sum\\frac{1}{n} = \\infty$",
                        "$\\sum\\frac{1}{n^2} = \\frac{\\pi^2}{6}$"], size=44, gap=30)
         + '</div>',
   panel=st.card("t-t", "trap", "⚠️ קטן מטור מתבדר: <b>אין מסקנה</b>")
         + st.card("t-r1", "rule", "🔑 התכנסות: $a_n \\le b_n$, ו-$\\sum b_n$ מתכנס")
         + st.card("t-r2", "rule", "🔑 התבדרות: $a_n \\ge b_n$, ו-$\\sum b_n$ מתבדר"))

limc = Scene("limc", "השוואה גבולית", [
    P("לפעמים קשה למצוא אי-שוויון מדויק. אז משתמשים ב**השוואה גבולית**."),
    P("אם $a_n$ ו-$b_n$ חיוביים, והגבול של המנה שלהם חיובי וסופי, שני הטורים מתנהגים אותו דבר.", do=show("l-0", "l-r"),
      say="אם אֵיי אֶן ובִּי אֶן חיוביים, והגבול של המנה שלהם חיובי וסופי, שני הטורים מתנהגים אותו דבר."),
    P("הסיבה: מאיזשהו מקום המנה בין חצי הגבול לפעמיים הגבול, וזה מחזיר אותנו להשוואה רגילה.", do=show("l-why")),
    P("איך בוחרים את $b_n$? לוקחים מהמונה ומהמכנה רק את האיבר הדומיננטי.", do=show("l-pick"),
      say="איך בוחרים את בִּי אֶן? לוקחים מהמונה ומהמכנה רק את האיבר הדומיננטי."),
    P("למשל שורש $n$, חלקי $n$ בריבוע ועוד אחת. במכנה $n$ בריבוע שולט.", do=show("l-1"),
      say="למשל שורש אֶן, חלקי אֶן בריבוע ועוד אחת. במכנה אֶן בריבוע שולט."),
    P("אז האיבר דומה לשורש $n$ חלקי $n$ בריבוע, כלומר אחת חלקי $n$ בחזקת שלוש חצאים.", do=show("l-2"),
      say="אז האיבר דומה לשורש אֶן חלקי אֶן בריבוע, כלומר אחת חלקי אֶן בחזקת שלוש חצאים."),
    P("המנה היא $n$ בריבוע חלקי $n$ בריבוע ועוד אחת, והיא שואפת לאחת: חיובי וסופי.", do=show("l-3"),
      say="המנה היא אֶן בריבוע חלקי אֶן בריבוע ועוד אחת, והיא שואפת לאחת: חיובי וסופי."),
    P("ושלוש חצאים גדול מאחת, אז טור ההשוואה מתכנס, ולכן גם הטור שלנו מתכנס.", do=show("l-v"), hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("l", ["$\\lim\\frac{a_n}{b_n} = L, \\quad 0 < L < \\infty$",
                        "$a_n = \\frac{\\sqrt{n}}{n^2+1}$",
                        "$b_n = \\frac{\\sqrt{n}}{n^2} = \\frac{1}{n^{3/2}}$",
                        "$\\frac{a_n}{b_n} = \\frac{n^2}{n^2+1} \\to 1$"], size=38, gap=14)
         + ws.verdict("l-v", "מתכנס") + '</div>',
   panel=st.card("l-r", "rule", "🔑 $a_n, b_n > 0$ ו-$0<L<\\infty$: מתכנסים יחד או מתבדרים יחד")
         + st.card("l-why", "ex", "$\\frac{L}{2} b_n \\le a_n \\le 2L\\, b_n$ מ-$n$ מסוים")
         + st.card("l-pick", "plain", "$b_n$ = הדומיננטי במונה חלקי הדומיננטי במכנה"))

ex1 = Scene("ex1", "שאלה ממבחן: טור 1", [
    P("שאלה ממבחן: לקבוע לכל טור אם הוא מתכנס בהחלט, בתנאי, או מתבדר."),
    P("הטור הראשון: קוסינוס $n$, חלקי השורש הרביעי של $n$ בחזקת חמש ועוד שתיים.",
      say="הטור הראשון: קוסינוס אֶן, חלקי השורש הרביעי של אֶן בחזקת חמש ועוד שתיים."),
    P("לקוסינוס $n$ יש סימנים שמשתנים, אז אי אפשר להשוות ישירות. עוברים לערך מוחלט.", do=show("a-0"),
      say="לקוסינוס אֶן יש סימנים שמשתנים, אז אי אפשר להשוות ישירות. עוברים לערך מוחלט."),
    P("הערך המוחלט של קוסינוס לכל היותר אחת, והמכנה גדול מהשורש הרביעי של $n$ בחזקת חמש.", do=show("a-1"),
      say="הערך המוחלט של קוסינוס לכל היותר אחת, והמכנה גדול מהשורש הרביעי של אֶן בחזקת חמש."),
    P("זה אחת חלקי $n$ בחזקת חמש רבעים. טור $p$ עם $p$ גדול מאחת, ולכן מתכנס.", do=show("a-2"),
      say="זה אחת חלקי אֶן בחזקת חמש רבעים. טור פִּי עם פִּי גדול מאחת, ולכן מתכנס."),
    P("לפי מבחן ההשוואה, טור הערכים המוחלטים מתכנס. הטור **מתכנס בהחלט**.", do=show("a-v")),
    P("המלכודת: לראות סימנים שמתחלפים ולכתוב ״בתנאי״. אבל אם הערכים המוחלטים מתכנסים, זה בהחלט.",
      do=show("a-t"), hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("a", ["$\\left|\\frac{\\cos n}{\\sqrt[4]{n^5+2}}\\right|$",
                        "$\\le \\frac{1}{\\sqrt[4]{n^5}}$",
                        "$= \\frac{1}{n^{5/4}}, \\quad p = \\frac{5}{4} > 1$"], size=44, gap=16)
         + ws.verdict("a-v", "מתכנס בהחלט") + '</div>',
   panel=ws.stem(EX["id"], "קבעו לכל טור אם הוא מתכנס בהחלט, בתנאי או מתבדר:"
                 '<div class="sr-mid" style="font-size:32px">$\\displaystyle \\sum_{n=1}^{\\infty}\\frac{\\cos n}{\\sqrt[4]{n^5+2}}'
                 ' \\qquad \\sum_{n=1}^{\\infty}\\frac{(-1)^n}{\\sqrt{n(n+1)}}$</div>')
         + st.card("a-t", "trap", "⚠️ סימנים מתחלפים לא אומרים ״בתנאי״: קודם בודקים $\\sum|a_n|$"))

ex2 = Scene("ex2", "שאלה ממבחן: טור 2", [
    P("הטור השני: מינוס אחת בחזקת $n$, חלקי שורש של $n$ כפול $n$ ועוד אחת.",
      say="הטור השני: מינוס אחת בחזקת אֶן, חלקי שורש של אֶן כפול אֶן ועוד אחת."),
    P("קודם התכנסות בהחלט: הערך המוחלט הוא אחת חלקי השורש הזה.", do=show("b-0")),
    P("מתחת לשורש יש $n$ בריבוע ועוד $n$, אז השורש מתנהג כמו $n$. משווים לאחת חלקי $n$.", do=show("b-1"),
      say="מתחת לשורש יש אֶן בריבוע ועוד אֶן, אז השורש מתנהג כמו אֶן. משווים לאחת חלקי אֶן."),
    P("המנה היא $n$ חלקי שורש $n$ בריבוע ועוד $n$, והיא שואפת לאחת.", do=show("b-2"),
      say="המנה היא אֶן חלקי שורש אֶן בריבוע ועוד אֶן, והיא שואפת לאחת."),
    P("הטור ההרמוני מתבדר, אז גם טור הערכים המוחלטים מתבדר. **אין** התכנסות בהחלט.", do=show("b-3")),
    P("טעות נפוצה: להשוות את השורש ל-$n$ בריבוע. אבל שורש של $n$ בריבוע הוא רק $n$.", do=show("b-t"),
      say="טעות נפוצה: להשוות את השורש לאֶן בריבוע. אבל שורש של אֶן בריבוע הוא רק אֶן."),
    P("עכשיו הסימנים. $n$ כפול $n$ ועוד אחת עולה, אז האיבר יורד, והוא שואף לאפס.", do=show("b-4"),
      say="עכשיו הסימנים. אֶן כפול אֶן ועוד אחת עולה, אז האיבר יורד, והוא שואף לאפס."),
    P("לפי משפט לייבניץ, שנלמד ברמה ארבע, טור מתחלף כזה מתכנס. רואים שהקפיצות קטנות.",
      do=show("b-b", *ws.bars_do("x2", 1, 12))),
    P("מתכנס, אבל לא בהחלט: הטור **מתכנס בתנאי**.", do=show("b-v"), hold=0.6),
], stage='<div class="sr-col">'
         + ws.eqs("b", ["$|a_n| = \\frac{1}{\\sqrt{n(n+1)}}$",
                        "$b_n = \\frac{1}{n}$",
                        "$\\frac{|a_n|}{b_n} = \\frac{n}{\\sqrt{n^2+n}} \\to 1$",
                        "$\\sum\\frac{1}{n} = \\infty \\;\\Rightarrow\\; \\sum|a_n| = \\infty$",
                        "$\\frac{1}{\\sqrt{n(n+1)}} \\searrow 0$"], size=30, gap=6)
         + f'<div id="b-b" class="h" style="margin-top:40px">{BX}</div>'
         + '</div>',
   panel=ws.stem(EX["id"], "הטור השני:"
                 '<div class="sr-mid" style="font-size:34px">$\\displaystyle \\sum_{n=1}^{\\infty}\\frac{(-1)^n}{\\sqrt{n(n+1)}}$</div>')
         + st.card("b-t", "trap", "⚠️ $\\sqrt{n(n+1)} \\approx n$, לא $n^2$")
         + ws.verdict("b-v", "מתכנס בתנאי"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: השוואה עובדת רק על איברים אי-שליליים. בטור עם סימנים בודקים את הערך המוחלט.", do=show("r-1")),
    P("הגדול מתכנס, אז הקטן מתכנס. הקטן מתבדר, אז הגדול מתבדר. ולא להפך.", do=show("r-2")),
    P("בהשוואה גבולית לוקחים את האיברים הדומיננטיים, ודורשים גבול חיובי וסופי.", do=show("r-3")),
    P("וגורם חסום כמו קוסינוס חוסמים באחת. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="sr-col"><div class="sr-big">$0 \\le a_n \\le b_n$</div></div>',
   panel=st.card("r-1", "rule", "🔑 רק $a_n \\ge 0$, אחרת $\\sum|a_n|$")
         + st.card("r-2", "rule", "🔑 גדול מתכנס $\\Rightarrow$ קטן. קטן מתבדר $\\Rightarrow$ גדול")
         + st.card("r-3", "rule", "🔑 $\\frac{a_n}{b_n} \\to L$, $0<L<\\infty$")
         + st.card("r-4", "rule", "🔑 $|\\cos n| \\le 1$, $|\\sin n| \\le 1$"))

VIDEO = Video("S02", "series", "השוואה והשוואה גבולית", ws.fix_scenes([title, cmp_, trap, limc, ex1, ex2, recap]),
              bank={"24S-A-Q2b": None})
