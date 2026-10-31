# -*- coding: utf-8 -*-
"""S04 · לייבניץ: התכנסות בהחלט ובתנאי — video script (build: tools/video/vid.py S04).

Source: courses/series/C04.js (lesson + goal). Exam anchor: 23A-A-Q2a ((-1)^n sin(π/n): conditional;
(-1)^n ln(1+1/(n∛n)): absolute), which no guided quiz uses.
Not used on purpose: the C04 quiz series ((-1)^n/n, cos(πn)/n², (-1)^n n/(n+1), (-1)^n/(√n ln n), the error bound for
Σ(-1)^{n+1}/n², the non-decreasing (2+(-1)^n)/n) and the lesson's (-1)^n/n. Examples here: (-1)^n/∛n (conditional,
with the Leibniz error bound checked against the true sum) and (-1)^n(1/√n + (-1)^n/n) (terms -> 0, alternating, but
not decreasing: diverges). Every verdict, limit and bound is asserted below.
"""
from vid import P, Scene, Video, show, hide, BANK
import mpmath as mp
import numpy as np
import sympy as sp
import stage as st
import w_series as ws
from w_series import n

# ---------------------------------------------------------------- checks
# example: Σ (-1)^n / n^(1/3): |a_n| is a p-series with p = 1/3 (diverges); 1/∛n decreases to 0 -> conditional
A = n ** sp.Rational(-1, 3)
assert ws.lim(A) == 0 and sp.diff(A, n).is_negative
mp.mp.dps = 30
S_true = -mp.altzeta(mp.mpf(1) / 3)                     # Σ_{n>=1} (-1)^n n^(-1/3) = -η(1/3)
SN = ws.psums((-1) ** n * A, 10)
for N in range(1, 11):                                  # Leibniz: |S - S_N| <= a_{N+1}
    assert abs(S_true - SN[N - 1]) <= (N + 1) ** (-1 / 3)
assert abs(S_true - SN[9]) < 0.45 and abs(float(11 ** (-1 / 3)) - 0.4497) < 1e-4
assert ws.tail(A, 10 ** 4, 10 ** 5) > 100                # Σ|a_n| grows without bound (like N^(2/3))
S_true = float(S_true)

# trap: a_n = 1/√n + (-1)^n/n (n >= 2): positive, -> 0, not decreasing; Σ(-1)^n a_n = Σ(-1)^n/√n + Σ1/n diverges
T = 1 / sp.sqrt(n) + (-1) ** n / n
vals = [float(T.subs(n, j)) for j in range(2, 200)]
assert all(v > 0 for v in vals) and vals[2] > vals[1]   # a_4 > a_3
assert ws.lim(1 / sp.sqrt(n) + 1 / n) == 0 and ws.lim(1 / sp.sqrt(n) - 1 / n) == 0
assert sp.expand((-1) ** n * T - ((-1) ** n / sp.sqrt(n) + (-1) ** (2 * n) / n)) == 0
ST = ws.psums((-1) ** n * T, 2000, n0=2)
assert ST[1999] - ST[199] > 1.5                          # the partial sums keep climbing (harmonic part)

# exam 23A-A-Q2a
EX = BANK["23A-A-Q2a"]
assert r"(-1)^n\cdot\sin\left(\frac{\pi}{n}\right)" in EX["question"]
assert r"\ln\left(1+\frac{1}{n\sqrt[3]{n}}\right)" in EX["question"]
# item 1
S1 = sp.sin(sp.pi / n)
assert ws.lim(S1 / (1 / n)) == sp.pi
assert ws.lim(S1) == 0
t = sp.Symbol("t", positive=True)
assert all(sp.cos(sp.pi / j) >= 0 for j in range(2, 50))  # π/n in (0, π/2]: sin is increasing there
assert all(sp.sin(sp.pi / (j + 1)) < sp.sin(sp.pi / j) for j in range(2, 200))
assert ws.tail(S1, 10 ** 4, 10 ** 5) > 7                 # Σ sin(π/n) grows like π ln N
SE = ws.psums((-1) ** n * S1, 14, n0=2)
# item 2
L2 = sp.log(1 + 1 / (n * sp.cbrt(n)))
assert sp.simplify(n * sp.cbrt(n) - n ** sp.Rational(4, 3)) == 0
assert ws.lim(L2 / n ** sp.Rational(-4, 3)) == 1
assert sp.Rational(4, 3) > 1
assert ws.tail(L2, 10 ** 4, 10 ** 5) < 3 * (10 ** 4) ** (-1 / 3)   # tail of Σ|a_n| <= ∫ x^(-4/3) = 3 N^(-1/3)

B1 = ws.bars("c1", SN, w=760, h=200, limit=S_true, limit_tex="$S$", label="$S_N$", ymin=-1.0, ymax=0.1)
B2 = ws.bars("e1", SE, w=860, h=170, label="$S_N$", nlabels={2, 5, 10, 15}, n0=2)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לסווג טור עם סימנים מתחלפים לאחת משלוש תשובות."),
    P("מתכנס בהחלט, מתכנס בתנאי, או מתבדר. הכלי החדש: משפט לייבניץ."),
    P("ובסוף נפתור שאלה ממבחן עם שני טורים.", hold=0.4),
], stage='<div class="kicker">S04 · טורים</div><h1>לייבניץ: התכנסות בהחלט ובתנאי</h1>'
         '<p>לסווג טור עם סימנים לאחת משלוש התשובות: מתכנס בהחלט, מתכנס בתנאי או מתבדר.</p>', layout="title")

leib = Scene("leib", "משפט לייבניץ", [
    P("טור מתחלף הוא מינוס אחת בחזקת $n$, כפול $a_n$ חיובי.", do=show("l-0"),
      say="טור מתחלף הוא מינוס אחת בחזקת אֶן, כפול אֵיי אֶן חיובי."),
    P("משפט לייבניץ: אם $a_n$ **יורדת** ושואפת לאפס, הטור מתכנס.", do=show("l-r"),
      say="משפט לייבניץ: אם אֵיי אֶן יורדת ושואפת לאפס, הטור מתכנס."),
    P("הסיבה: הסכומים החלקיים קופצים למעלה ולמטה, וכל קפיצה קטנה מהקודמת. הם נלחצים לגבול אחד.", do=show("l-why")),
    P("ומקבלים בונוס: השגיאה אחרי $N$ איברים היא לכל היותר האיבר הבא.", do=show("l-1"),
      say="ומקבלים בונוס: השגיאה אחרי אֶן איברים היא לכל היותר האיבר הבא."),
    P("עכשיו מתכון הסיווג, בסדר הזה. צעד ראשון: אם האיבר לא שואף לאפס, הטור מתבדר.", do=show("s-1")),
    P("צעד שני: בודקים את טור הערכים המוחלטים. אם הוא מתכנס, הטור **מתכנס בהחלט**, ולא צריך את לייבניץ.",
      do=show("s-2")),
    P("צעד שלישי: אחרת, אם הערכים המוחלטים יורדים לאפס, לייבניץ נותן התכנסות. זה **מתכנס בתנאי**.", do=show("s-3"),
      hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("l", ["$\\sum (-1)^n a_n, \\quad a_n > 0$",
                        "$|S - S_N| \\le a_{N+1}$"], size=46, gap=40)
         + '</div>',
   panel=st.card("l-r", "rule", "🔑 $a_n \\searrow 0$ $\\Rightarrow$ $\\sum(-1)^n a_n$ מתכנס")
         + st.card("l-why", "ex", "הקפיצות קטנות והולכות: $S_N$ נלחץ לגבול")
         + st.card("s-1", "plain", "1. $a_n \\not\\to 0$? מתבדר")
         + st.card("s-2", "plain", "2. $\\sum|a_n|$ מתכנס? <b>בהחלט</b>")
         + st.card("s-3", "plain", "3. אחרת, $|a_n| \\searrow 0$? <b>בתנאי</b>"))

cond = Scene("cond", "דוגמה: בתנאי", [
    P("דוגמה: מינוס אחת בחזקת $n$, חלקי שורש שלישי של $n$.", do=show("c-0"),
      say="דוגמה: מינוס אחת בחזקת אֶן, חלקי שורש שלישי של אֶן."),
    P("צעד ראשון: האיבר שואף לאפס, אז עוד לא יודעים.", do=show("c-1")),
    P("צעד שני: הערכים המוחלטים הם טור $p$ עם $p$ שווה שליש. מתבדר, אז אין התכנסות בהחלט.", do=show("c-2"),
      say="צעד שני: הערכים המוחלטים הם טור פִּי עם פִּי שווה שליש. מתבדר, אז אין התכנסות בהחלט."),
    P("צעד שלישי: אחת חלקי שורש שלישי של $n$ יורדת לאפס, אז לפי לייבניץ הטור מתכנס.", do=show("c-3"),
      say="צעד שלישי: אחת חלקי שורש שלישי של אֶן יורדת לאפס, אז לפי לייבניץ הטור מתכנס."),
    P("רואים את זה בסכומים החלקיים: הם קופצים מעל ומתחת לגבול, והקפיצות מתכווצות.",
      do=show("c-b", *ws.bars_do("c1", 1, 10), "c1-lim", "c1-limt")),
    P("אחרי עשרה איברים, השגיאה לכל היותר האיבר האחד עשר: בערך ארבע וחצי עשיריות. הקפיצות קטנות, אבל לאט.",
      do=show("c-e")),
    P("מתכנס, אבל לא בהחלט: הטור **מתכנס בתנאי**.", do=show("c-v"), hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("c", ["$\\sum_{n=1}^{\\infty}\\frac{(-1)^n}{\\sqrt[3]{n}}$",
                        "$\\frac{1}{\\sqrt[3]{n}} \\to 0$",
                        "$\\sum\\frac{1}{n^{1/3}} = \\infty, \\quad p = \\frac{1}{3} \\le 1$",
                        "$\\frac{1}{\\sqrt[3]{n}} \\searrow 0$"], size=32, gap=8)
         + f'<div id="c-b" class="h" style="margin-top:44px">{B1}</div></div>',
   panel=st.card("c-e", "ex", "$|S - S_{10}| \\le \\frac{1}{\\sqrt[3]{11}} \\approx 0.45$")
         + ws.verdict("c-v", "מתכנס בתנאי"))

mono = Scene("mono", "לייבניץ דורש ירידה", [
    P("ועכשיו המלכודת: לייבניץ דורש **ירידה**, ולא רק שאיפה לאפס.", do=show("m-t")),
    P("קחו $a_n$ שווה אחת חלקי שורש $n$, ועוד מינוס אחת בחזקת $n$ חלקי $n$. מ-$n$ שווה שתיים הוא חיובי.",
      do=show("m-0"), say="קחו אֵיי אֶן שווה אחת חלקי שורש אֶן, ועוד מינוס אחת בחזקת אֶן חלקי אֶן. מאֶן שווה שתיים הוא חיובי."),
    P("הוא שואף לאפס, אבל לא יורד: האיבר הרביעי גדול מהשלישי.", do=show("m-1")),
    P("כשכופלים במינוס אחת בחזקת $n$, הטור מתפרק לשני טורים.", do=show("m-2"),
      say="כשכופלים במינוס אחת בחזקת אֶן, הטור מתפרק לשני טורים."),
    P("הראשון מתכנס לפי לייבניץ, אבל השני הוא הטור ההרמוני, שמתבדר.", do=show("m-3")),
    P("מתכנס ועוד מתבדר זה מתבדר. אז טור מתחלף, עם איבר ששואף לאפס, **מתבדר**.", do=show("m-v"), hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("m", ["$a_n = \\frac{1}{\\sqrt{n}} + \\frac{(-1)^n}{n} > 0$",
                        "$a_3 \\approx 0.24 < a_4 = 0.75$",
                        "$(-1)^n a_n = \\frac{(-1)^n}{\\sqrt{n}} + \\frac{1}{n}$",
                        "$\\sum\\frac{(-1)^n}{\\sqrt{n}} < \\infty, \\quad \\sum\\frac{1}{n} = \\infty$"], size=36, gap=22)
         + ws.verdict("m-v", "מתבדר", ok=False) + '</div>',
   panel=st.card("m-t", "trap", "⚠️ $a_n \\to 0$ בלי ירידה: לייבניץ לא חל"))

assert abs(float(T.subs(n, 3)) - 0.244) < 1e-3 and float(T.subs(n, 4)) == 0.75

ex1 = Scene("ex1", "שאלה ממבחן: טור 1", [
    P("שאלה ממבחן: בדקו התכנסות בהחלט, בתנאי או התבדרות. הטור הראשון: מינוס אחת בחזקת $n$, כפול סינוס פאי חלקי $n$.",
      say="שאלה ממבחן: בדקו התכנסות בהחלט, בתנאי או התבדרות. הטור הראשון: מינוס אחת בחזקת אֶן, כפול סינוס פאי חלקי אֶן."),
    P("צעד ראשון: סינוס פאי חלקי $n$ שואף לאפס.", do=show("a-0"), say="צעד ראשון: סינוס פאי חלקי אֶן שואף לאפס."),
    P("צעד שני: הערכים המוחלטים. השוואה גבולית עם אחת חלקי $n$: הגבול הוא פאי, חיובי וסופי.", do=show("a-1"),
      say="צעד שני: הערכים המוחלטים. השוואה גבולית עם אחת חלקי אֶן: הגבול הוא פאי, חיובי וסופי."),
    P("הטור ההרמוני מתבדר, אז אין התכנסות בהחלט.", do=show("a-2")),
    P("צעד שלישי: פאי חלקי $n$ יורד, והוא בין אפס לחצי פאי. שם הסינוס עולה, אז סינוס פאי חלקי $n$ יורד.",
      do=show("a-3"), say="צעד שלישי: פאי חלקי אֶן יורד, והוא בין אפס לחצי פאי. שם הסינוס עולה, אז סינוס פאי חלקי אֶן יורד."),
    P("יורד לאפס, אז לייבניץ נותן התכנסות. והסכומים החלקיים אכן מתייצבים.",
      do=show("a-b", *ws.bars_do("e1", 1, 14))),
    P("הטור הראשון **מתכנס בתנאי**.", do=show("a-v"), hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("a", ["$\\sin\\frac{\\pi}{n} \\to 0$",
                        "$\\frac{\\sin(\\pi/n)}{1/n} \\to \\pi, \\quad 0 < \\pi < \\infty$",
                        "$\\sum\\frac{1}{n} = \\infty \\;\\Rightarrow\\; \\sum\\left|a_n\\right| = \\infty$",
                        "$0 < \\frac{\\pi}{n} \\le \\frac{\\pi}{2} \\;\\Rightarrow\\; \\sin\\frac{\\pi}{n} \\searrow 0$"],
                  size=31, gap=6)
         + f'<div id="a-b" class="h" style="margin-top:40px">{B2}</div></div>',
   panel=ws.stem(EX["id"], "בדקו התכנסות בהחלט, בתנאי או התבדרות:"
                 '<div class="sr-mid" style="font-size:30px">$\\displaystyle \\sum_{n=2}^{\\infty}(-1)^n\\sin\\frac{\\pi}{n}'
                 ' \\qquad \\sum_{n=1}^{\\infty}(-1)^n\\ln\\left(1+\\frac{1}{n\\sqrt[3]{n}}\\right)$</div>')
         + ws.verdict("a-v", "מתכנס בתנאי"))

ex2 = Scene("ex2", "שאלה ממבחן: טור 2", [
    P("הטור השני: מינוס אחת בחזקת $n$, כפול לן של אחת ועוד אחת חלקי $n$ כפול שורש שלישי של $n$.",
      say="הטור השני: מינוס אחת בחזקת אֶן, כפול לן של אחת ועוד אחת חלקי אֶן כפול שורש שלישי של אֶן."),
    P("קודם מסדרים את החזקה: $n$ כפול שורש שלישי של $n$ זה $n$ בחזקת ארבע שלישים.", do=show("b-0"),
      say="קודם מסדרים את החזקה: אֶן כפול שורש שלישי של אֶן זה אֶן בחזקת ארבע שלישים."),
    P("ישר לצעד השני: לן של אחת ועוד $u$, חלקי $u$, שואף לאחת כש-$u$ שואף לאפס.", do=show("b-1"),
      say="ישר לצעד השני: לן של אחת ועוד יוּ, חלקי יוּ, שואף לאחת כשיוּ שואף לאפס."),
    P("אז השוואה גבולית עם אחת חלקי $n$ בחזקת ארבע שלישים נותנת גבול אחת.", do=show("b-2"),
      say="אז השוואה גבולית עם אחת חלקי אֶן בחזקת ארבע שלישים נותנת גבול אחת."),
    P("ארבע שלישים גדול מאחת, אז טור הערכים המוחלטים מתכנס. הטור **מתכנס בהחלט**, ולייבניץ מיותר.",
      do=show("b-v")),
    P("המלכודת: לקרוא את המכנה כ-$n$, ולהשוות לטור ההרמוני. אז מקבלים בטעות ״בתנאי״.", do=show("b-t"),
      say="המלכודת: לקרוא את המכנה כאֶן, ולהשוות לטור ההרמוני. אז מקבלים בטעות בתנאי.", hold=0.6),
], stage='<div class="sr-col">'
         + ws.eqs("b", ["$n\\sqrt[3]{n} = n^{4/3}$",
                        "$\\frac{\\ln(1+u)}{u} \\to 1 \\quad (u \\to 0)$",
                        "$\\frac{\\ln\\left(1+n^{-4/3}\\right)}{n^{-4/3}} \\to 1, \\quad p = \\frac{4}{3} > 1$"],
                  size=40, gap=30)
         + ws.verdict("b-v", "מתכנס בהחלט") + '</div>',
   panel=ws.stem(EX["id"], "הטור השני:"
                 '<div class="sr-mid" style="font-size:32px">$\\displaystyle \\sum_{n=1}^{\\infty}(-1)^n\\ln\\left(1+\\frac{1}{n\\sqrt[3]{n}}\\right)$</div>')
         + st.card("b-t", "trap", "⚠️ $n\\sqrt[3]{n} = n^{4/3}$, לא $n$"))

recap = Scene("recap", "סיכום", [
    P("לסיכום, מתכון בשלושה צעדים. איבר שלא שואף לאפס: מתבדר.", do=show("r-1")),
    P("טור ערכים מוחלטים שמתכנס: מתכנס בהחלט, בלי לייבניץ.", do=show("r-2")),
    P("אחרת, ערכים מוחלטים שיורדים לאפס: לייבניץ, ומתכנס בתנאי.", do=show("r-3")),
    P("ולייבניץ דורש ירידה, לא רק שאיפה לאפס. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="sr-col"><div class="sr-big">$\\sum (-1)^n a_n$</div></div>',
   panel=st.card("r-1", "rule", "🔑 $a_n \\not\\to 0$: מתבדר")
         + st.card("r-2", "rule", "🔑 $\\sum|a_n|$ מתכנס: בהחלט")
         + st.card("r-3", "rule", "🔑 $|a_n| \\searrow 0$, ו-$\\sum|a_n|$ מתבדר: בתנאי")
         + st.card("r-4", "trap", "⚠️ לייבניץ: יורדת <b>ו</b>שואפת ל-$0$"))

VIDEO = Video("S04", "series", "לייבניץ: התכנסות בהחלט ובתנאי", ws.fix_scenes([title, leib, cond, mono, ex1, ex2, recap]),
              bank={"23A-A-Q2a": None})
