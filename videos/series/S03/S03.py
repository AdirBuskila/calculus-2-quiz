# -*- coding: utf-8 -*-
"""S03 · מבחן המנה, השורש והאינטגרל — video script (build: tools/video/vid.py S03).

Source: courses/series/C03.js (lesson + goal). Exam anchor: 22A-A-Q2a (Σ sin n/(n ln²n): bound + integral test;
Σ ((-1)^n + n)/3^n: bound + ratio test), which no guided quiz uses. The bank's solution (official: false) of the second series
splits it and uses Leibniz on Σ(-1)^n/3^n; here the bound |(-1)^n+n| <= n+1 and the ratio test give absolute
convergence directly (same verdict, stronger).
Not used on purpose: the C03 quiz series (n²/2^n, (-1)^n 3^n/n!, (n/(2n+1))^n, the D=1 question, 1/(n ln³n), the
order proof for 1/(n ln n)). Worked examples here: (2n)!/((n!)² 5^n) (ratio, D=4/5) and (1+1/n)^{n²}/3^n (root,
c=e/3). Every limit, integral and bound on screen is asserted below.
"""
from vid import P, Scene, Video, show, hide, BANK
import numpy as np
import sympy as sp
import stage as st
import w_series as ws
from w_series import n

xx = sp.Symbol("x", positive=True)
M = sp.Symbol("M", positive=True)

# ---------------------------------------------------------------- checks
# ratio example: a_n = (2n)!/((n!)^2 5^n), a_{n+1}/a_n = 2(2n+1)/(5(n+1)) -> 4/5
AR = sp.factorial(2 * n) / (sp.factorial(n) ** 2 * 5 ** n)
q = sp.simplify(sp.combsimp(AR.subs(n, n + 1) / AR))
assert sp.simplify(q - 2 * (2 * n + 1) / (5 * (n + 1))) == 0
assert ws.ratio(AR) == sp.Rational(4, 5)

# root example: a_n = (1+1/n)^(n^2)/3^n, n-th root = (1+1/n)^n/3 -> e/3 < 1
assert ws.lim((1 + 1 / n) ** n / 3) == sp.E / 3
assert (sp.E / 3).evalf() < 1 and abs(float(sp.E / 3) - 0.906) < 1e-3

# p-series by the integral test: ∫_1^∞ x^(-p) dx is finite exactly when p > 1
for pp in (sp.Rational(1, 2), 1, sp.Rational(3, 2), 2):
    assert (sp.integrate(xx ** (-pp), (xx, 1, sp.oo)).is_finite is True) == (pp > 1)
# D = 1 for both 1/n and 1/n^2
assert ws.ratio(1 / n) == 1 and ws.ratio(1 / n ** 2) == 1

# exam 22A-A-Q2a
EX = BANK["22A-A-Q2a"]
assert r"\frac{\sin n}{n(\ln n)^2}" in EX["question"] and r"\frac{(-1)^n+n}{3^n}" in EX["question"]
# item 1: |sin n|/(n ln^2 n) <= 1/(n ln^2 n); f(x) = 1/(x ln^2 x) positive, continuous, decreasing on [2, oo)
f = 1 / (xx * sp.log(xx) ** 2)
fp = sp.simplify(sp.diff(f, xx))
assert sp.simplify(fp + (sp.log(xx) + 2) / (xx ** 2 * sp.log(xx) ** 3)) == 0     # f' = -(ln x + 2)/(x² ln³x) < 0
I = sp.integrate(f, (xx, 2, M))
assert sp.simplify(I - (1 / sp.log(2) - 1 / sp.log(M))) == 0
assert sp.limit(I, M, sp.oo) == 1 / sp.log(2)
assert ws.ratio(1 / (n * sp.log(n) ** 2)) == 1                                  # the ratio test does not decide here
kk = np.arange(2, 10 ** 6, dtype=np.float64)
assert np.all(np.abs(np.sin(kk)) / (kk * np.log(kk) ** 2) <= 1 / (kk * np.log(kk) ** 2))
# item 2: |(-1)^n + n| <= n + 1, ratio of (n+1)/3^n -> 1/3
B = (n + 1) / 3 ** n
assert ws.ratio(B) == sp.Rational(1, 3)
assert sp.simplify(B.subs(n, n + 1) / B - (n + 2) / (3 * (n + 1))) == 0
assert all(abs((-1) ** j + j) <= j + 1 for j in range(1, 1000))
assert sp.summation(((-1) ** n + n) / 3 ** n, (n, 1, sp.oo)) == sp.Rational(1, 2)   # it converges (sum = 1/2)

TAB = ('<table class="sr-tab"><thead><tr><th>צורת האיבר</th><th>המבחן</th></tr></thead><tbody>'
       '<tr id="c-r1" class="h"><td class="l">$n!$, $\\;c^n$</td><td>מנה (דלאמבר)</td></tr>'
       '<tr id="c-r2" class="h"><td class="l">$\\left(\\cdots\\right)^n$</td><td>שורש (קושי)</td></tr>'
       '<tr id="c-r3" class="h"><td class="l">$\\frac{1}{n\\ln n}$</td><td>אינטגרל</td></tr>'
       '</tbody></table>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר שלושה מבחנים חזקים: מבחן המנה, מבחן השורש ומבחן האינטגרל."),
    P("נלמד לבחור ביניהם לפי צורת האיבר, ולזהות מתי מבחן לא מכריע."),
    P("ובסוף נפתור שאלה ממבחן עם שני טורים.", hold=0.4),
], stage='<div class="kicker">S03 · טורים</div><h1>מבחן המנה, השורש והאינטגרל</h1>'
         '<p>לבחור בין מבחן המנה, השורש והאינטגרל לפי צורת האיבר הכללי, ולדעת מתי המבחן לא מכריע.</p>',
   layout="title")

choose = Scene("choose", "איזה מבחן", [
    P("כשאין טור $p$ או טור הנדסי ברור להשוות אליו, מסתכלים על **צורת האיבר**.", do=show("c-tab", "c-k"),
      say="כשאין טור פִּי או טור הנדסי ברור להשוות אליו, מסתכלים על צורת האיבר."),
    P("עצרת, או מספר בחזקת $n$: מבחן המנה, של דלאמבר.", do=show("c-r1"),
      say="עצרת, או מספר בחזקת אֶן: מבחן המנה, של דלאמבר."),
    P("כל האיבר בחזקת $n$: מבחן השורש, של קושי.", do=show("c-r2"), say="כל האיבר בחזקת אֶן: מבחן השורש, של קושי."),
    P("ולן במכנה: מבחן האינטגרל.", do=show("c-r3"), hold=0.4),
], stage=f'<div class="sr-col"><div id="c-tab" class="h" style="font-size:40px">{TAB}</div></div>',
   panel=st.card("c-k", "plain", "בוחרים מבחן לפי מה שמופיע באיבר"))

ratio_ = Scene("ratio", "מבחן המנה", [
    P("מבחן המנה: מחשבים את הגבול של איבר $n$ ועוד אחת, חלקי איבר $n$, בערך מוחלט.", do=show("q-0"),
      say="מבחן המנה: מחשבים את הגבול של איבר אֶן ועוד אחת, חלקי איבר אֶן, בערך מוחלט."),
    P("אם הגבול קטן מאחת, הטור מתכנס בהחלט. אם גדול מאחת, הוא מתבדר.", do=show("q-r")),
    P("הסיבה: מאיזשהו מקום האיברים קטנים יותר מטור הנדסי עם מנה קטנה מאחת.", do=show("q-why")),
    P("דוגמה: שתיים $n$ עצרת, חלקי $n$ עצרת בריבוע, כפול חמש בחזקת $n$.", do=show("q-1"),
      say="דוגמה: שתיים אֶן עצרת, חלקי אֶן עצרת בריבוע, כפול חמש בחזקת אֶן."),
    P("במנה כמעט הכול מצטמצם. נשארים שני הגורמים החדשים של העצרת, חלקי $n$ ועוד אחת בריבוע, וחמש.",
      do=show("q-2"), say="במנה כמעט הכול מצטמצם. נשארים שני הגורמים החדשים של העצרת, חלקי אֶן ועוד אחת בריבוע, וחמש."),
    P("הגבול הוא ארבע חמישיות. קטן מאחת, ולכן הטור מתכנס.", do=show("q-3", "q-v"), hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("q", ["$D = \\lim\\left|\\frac{a_{n+1}}{a_n}\\right|$",
                        "$a_n = \\frac{(2n)!}{(n!)^2\\, 5^n}$",
                        "$\\frac{a_{n+1}}{a_n} = \\frac{(2n+2)(2n+1)}{(n+1)^2\\cdot 5} = \\frac{2(2n+1)}{5(n+1)}$",
                        "$D = \\frac{4}{5} < 1$"], size=36, gap=18)
         + ws.verdict("q-v", "מתכנס בהחלט") + '</div>',
   panel=st.card("q-r", "rule", "🔑 $D<1$: מתכנס בהחלט. $D>1$: מתבדר")
         + st.card("q-why", "ex", "$D<r<1$ $\\Rightarrow$ $|a_{n}| \\le C\\, r^n$ מ-$n$ מסוים"))

root_ = Scene("root", "מבחן השורש", [
    P("מבחן השורש: מחשבים את הגבול של השורש ה-$n$ של הערך המוחלט של האיבר.", do=show("w-0"),
      say="מבחן השורש: מחשבים את הגבול של השורש האֶן של הערך המוחלט של האיבר."),
    P("אותם כללים: קטן מאחת מתכנס בהחלט, גדול מאחת מתבדר.", do=show("w-r")),
    P("דוגמה: אחת ועוד אחת חלקי $n$, בחזקת $n$ בריבוע, חלקי שלוש בחזקת $n$.", do=show("w-1"),
      say="דוגמה: אחת ועוד אחת חלקי אֶן, בחזקת אֶן בריבוע, חלקי שלוש בחזקת אֶן."),
    P("השורש ה-$n$ מוריד חזקה אחת של $n$: נשאר אחת ועוד אחת חלקי $n$, בחזקת $n$, חלקי שלוש.", do=show("w-2"),
      say="השורש האֶן מוריד חזקה אחת של אֶן: נשאר אחת ועוד אחת חלקי אֶן, בחזקת אֶן, חלקי שלוש."),
    P("והגבול המפורסם: אחת ועוד אחת חלקי $n$, בחזקת $n$, שואף ל-$e$.", do=show("w-3"),
      say="והגבול המפורסם: אחת ועוד אחת חלקי אֶן, בחזקת אֶן, שואף לאִי."),
    P("אז הגבול הוא $e$ חלקי שלוש, בערך אפס נקודה תשעים ואחת. קטן מאחת, ולכן מתכנס.", do=show("w-4", "w-v"),
      say="אז הגבול הוא אִי חלקי שלוש, בערך אפס נקודה תשעים ואחת. קטן מאחת, ולכן מתכנס.", hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("w", ["$c = \\lim\\sqrt[n]{|a_n|}$",
                        "$a_n = \\frac{\\left(1+\\frac{1}{n}\\right)^{n^2}}{3^n}$",
                        "$\\sqrt[n]{a_n} = \\frac{\\left(1+\\frac{1}{n}\\right)^{n}}{3}$",
                        "$\\left(1+\\frac{1}{n}\\right)^{n} \\to e$",
                        "$c = \\frac{e}{3} \\approx 0.91 < 1$"], size=36, gap=14)
         + ws.verdict("w-v", "מתכנס בהחלט") + '</div>',
   panel=st.card("w-r", "rule", "🔑 $c<1$: מתכנס בהחלט. $c>1$: מתבדר"))

one = Scene("one", "כשהמבחן לא מכריע", [
    P("ומה אם הגבול יוצא בדיוק אחת? אז המבחן **לא אומר כלום**.", do=show("o-t")),
    P("לטור ההרמוני המנה שואפת לאחת, והוא מתבדר.", do=show("o-0")),
    P("וגם לסכום אחת חלקי $n$ בריבוע המנה שואפת לאחת, והוא מתכנס.", do=show("o-1"),
      say="וגם לסכום אחת חלקי אֶן בריבוע המנה שואפת לאחת, והוא מתכנס."),
    P("אותו גבול, ותוצאות הפוכות. אז כשמקבלים אחת, עוברים להשוואה או לאינטגרל.", do=show("o-r"), hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("o", ["$\\frac{1/(n+1)}{1/n} = \\frac{n}{n+1} \\to 1, \\quad \\sum\\frac{1}{n} = \\infty$",
                        "$\\frac{1/(n+1)^2}{1/n^2} \\to 1, \\quad \\sum\\frac{1}{n^2} < \\infty$"], size=40, gap=40)
         + '</div>',
   panel=st.card("o-t", "trap", "⚠️ $D=1$ או $c=1$: <b>אין מידע</b>")
         + st.card("o-r", "rule", "🔑 אז עוברים להשוואה או לאינטגרל"))

integ = Scene("integ", "מבחן האינטגרל", [
    P("מבחן האינטגרל: לוקחים פונקציה $f$ שבמספרים השלמים נותנת בדיוק את האיברים.", do=show("g-0"),
      say="מבחן האינטגרל: לוקחים פונקציה אֶף שבמספרים השלמים נותנת בדיוק את האיברים."),
    P("אם $f$ חיובית, רציפה ויורדת, הטור והאינטגרל הלא אמיתי מתכנסים יחד או מתבדרים יחד.", do=show("g-1", "g-r"),
      say="אם אֶף חיובית, רציפה ויורדת, הטור והאינטגרל הלא אמיתי מתכנסים יחד או מתבדרים יחד."),
    P("הסיבה: בגלל שהיא יורדת, כל איבר חוסם את השטח מתחת ל-$f$ בקטע שאחריו, ונחסם על ידי השטח בקטע שלפניו.",
      do=show("g-2"), say="הסיבה: בגלל שהיא יורדת, כל איבר חוסם את השטח מתחת לאֶף בקטע שאחריו, ונחסם על ידי השטח בקטע שלפניו."),
    P("וכך מוכיחים את משפט טור $p$: האינטגרל מאחת עד אינסוף של $x$ בחזקת מינוס $p$ סופי בדיוק כש-$p$ גדול מאחת.",
      do=show("g-3"), say="וכך מוכיחים את משפט טור פִּי: האינטגרל מאחת עד אינסוף של אִקְס בחזקת מינוס פִּי סופי בדיוק כשפִּי גדול מאחת."),
    P("זה המבחן שמתאים כשיש לן במכנה. מיד נראה אותו בשאלה מהמבחן.", hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("g", ["$a_n = f(n)$",
                        "$\\sum_{n=N}^{\\infty} a_n \\;\\sim\\; \\int_N^{\\infty} f(x)\\,dx$",
                        "$\\int_{n}^{n+1} f \\;\\le\\; a_n \\;\\le\\; \\int_{n-1}^{n} f$",
                        "$\\int_1^{\\infty} x^{-p}\\,dx < \\infty \\iff p > 1$"], size=40, gap=24)
         + '</div>',
   panel=st.card("g-r", "rule", "🔑 $f$ חיובית, רציפה ויורדת: הטור והאינטגרל מתכנסים יחד"))

ex1 = Scene("ex1", "שאלה ממבחן: טור 1", [
    P("שאלה ממבחן: בדקו התכנסות של שני טורים. הראשון: סינוס $n$ חלקי $n$ כפול לן $n$ בריבוע.",
      say="שאלה ממבחן: בדקו התכנסות של שני טורים. הראשון: סינוס אֶן חלקי אֶן כפול לן אֶן בריבוע."),
    P("לסינוס $n$ יש סימנים משתנים, אז עוברים לערך מוחלט, וחוסמים את הסינוס באחת.", do=show("a-0"),
      say="לסינוס אֶן יש סימנים משתנים, אז עוברים לערך מוחלט, וחוסמים את הסינוס באחת."),
    P("נשאר הטור אחת חלקי $n$ כפול לן $n$ בריבוע. יש לן במכנה: מבחן האינטגרל.", do=show("a-1"),
      say="נשאר הטור אחת חלקי אֶן כפול לן אֶן בריבוע. יש לן במכנה: מבחן האינטגרל."),
    P("הפונקציה חיובית ורציפה החל משתיים, והנגזרת שלה שלילית, אז היא יורדת.", do=show("a-2")),
    P("נציב $t$ שווה לן $x$. אז $dt$ הוא $dx$ חלקי $x$, והאינטגרל הופך לאינטגרל של $t$ בחזקת מינוס שתיים.",
      do=show("a-3"), say="נציב טִי שווה לן אִקְס. אז דִּי טִי הוא דִּי אִקְס חלקי אִקְס, והאינטגרל הופך לאינטגרל של טִי בחזקת מינוס שתיים."),
    P("מקבלים אחת חלקי לן שתיים, פחות אחת חלקי לן $M$. כש-$M$ שואף לאינסוף, זה שואף לאחת חלקי לן שתיים.",
      do=show("a-4"), say="מקבלים אחת חלקי לן שתיים, פחות אחת חלקי לן אֶם. כשאֶם שואף לאינסוף, זה שואף לאחת חלקי לן שתיים."),
    P("האינטגרל סופי, אז טור החסם מתכנס. לפי השוואה, הטור **מתכנס בהחלט**.", do=show("a-v")),
    P("המלכודת: לנסות כאן את מבחן המנה. המנה שואפת לאחת, והמבחן לא מכריע.", do=show("a-t"), hold=0.4),
], stage='<div class="sr-col">'
         + ws.eqs("a", ["$\\left|\\frac{\\sin n}{n(\\ln n)^2}\\right| \\le \\frac{1}{n(\\ln n)^2}$",
                        "$f(x) = \\frac{1}{x(\\ln x)^2}$",
                        "$f'(x) = -\\frac{\\ln x + 2}{x^2(\\ln x)^3} < 0$",
                        "$\\int_2^M \\frac{dx}{x(\\ln x)^2} = \\int_{\\ln 2}^{\\ln M} t^{-2}\\,dt$",
                        "$= \\frac{1}{\\ln 2} - \\frac{1}{\\ln M} \\to \\frac{1}{\\ln 2}$"], size=32, gap=10)
         + ws.verdict("a-v", "מתכנס בהחלט") + '</div>',
   panel=ws.stem(EX["id"], "בדקו התכנסות של הטורים:"
                 '<div class="sr-mid" style="font-size:32px">$\\displaystyle \\sum_{n=2}^{\\infty}\\frac{\\sin n}{n(\\ln n)^2}'
                 ' \\qquad \\sum_{n=1}^{\\infty}\\frac{(-1)^n+n}{3^n}$</div>')
         + st.card("a-t", "trap", "⚠️ מנה על $\\frac{1}{n\\ln^2 n}$ נותנת $D=1$: לא מכריע"))

ex2 = Scene("ex2", "שאלה ממבחן: טור 2", [
    P("הטור השני: מינוס אחת בחזקת $n$ ועוד $n$, חלקי שלוש בחזקת $n$.",
      say="הטור השני: מינוס אחת בחזקת אֶן ועוד אֶן, חלקי שלוש בחזקת אֶן."),
    P("שוב ערך מוחלט: המונה לכל היותר $n$ ועוד אחת.", do=show("b-0"), say="שוב ערך מוחלט: המונה לכל היותר אֶן ועוד אחת."),
    P("יש שלוש בחזקת $n$, אז מבחן המנה על החסם, $n$ ועוד אחת חלקי שלוש בחזקת $n$.", do=show("b-1"),
      say="יש שלוש בחזקת אֶן, אז מבחן המנה על החסם, אֶן ועוד אחת חלקי שלוש בחזקת אֶן."),
    P("המנה היא $n$ ועוד שתיים, חלקי שלוש כפול $n$ ועוד אחת. היא שואפת לשליש.", do=show("b-2"),
      say="המנה היא אֶן ועוד שתיים, חלקי שלוש כפול אֶן ועוד אחת. היא שואפת לשליש."),
    P("שליש קטן מאחת, אז טור החסם מתכנס, ולפי השוואה הטור **מתכנס בהחלט**.", do=show("b-v")),
    P("בפתרון שבמאגר פירקו לשני טורים, והשתמשו בלייבניץ על החלק המתחלף. גם זה נכון, אבל הדרך כאן נותנת יותר: התכנסות בהחלט.",
      do=show("b-n"), hold=0.6),
], stage='<div class="sr-col">'
         + ws.eqs("b", ["$\\left|\\frac{(-1)^n+n}{3^n}\\right| \\le \\frac{n+1}{3^n}$",
                        "$b_n = \\frac{n+1}{3^n}$",
                        "$\\frac{b_{n+1}}{b_n} = \\frac{n+2}{3(n+1)} \\to \\frac{1}{3} < 1$"], size=40, gap=26)
         + ws.verdict("b-v", "מתכנס בהחלט") + '</div>',
   panel=ws.stem(EX["id"], "הטור השני:"
                 '<div class="sr-mid" style="font-size:34px">$\\displaystyle \\sum_{n=1}^{\\infty}\\frac{(-1)^n+n}{3^n}$</div>')
         + st.card("b-n", "ex", "פירוק לשני טורים + לייבניץ: נכון, אבל מוכיח רק התכנסות"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: עצרת או חזקה, מבחן המנה. הכול בחזקת $n$, מבחן השורש.", do=show("r-1"),
      say="לסיכום: עצרת או חזקה, מבחן המנה. הכול בחזקת אֶן, מבחן השורש."),
    P("בשניהם: קטן מאחת מתכנס בהחלט, גדול מאחת מתבדר, ואחת לא אומר כלום.", do=show("r-2")),
    P("לן במכנה: מבחן האינטגרל, אחרי שבודקים שהפונקציה חיובית, רציפה ויורדת.", do=show("r-3")),
    P("וכשיש גורם חסום, קודם חוסמים, ורק אז מפעילים מבחן. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage=f'<div class="sr-col"><div style="font-size:40px">{TAB.replace(' class="h"', "").replace('id="c-', 'id="rc-')}</div></div>',
   panel=st.card("r-1", "rule", "🔑 $n!$, $c^n$: מנה. $(\\cdots)^n$: שורש")
         + st.card("r-2", "rule", "🔑 $<1$ מתכנס, $>1$ מתבדר, $=1$ אין מידע")
         + st.card("r-3", "rule", "🔑 $\\ln$ במכנה: אינטגרל (חיובית, רציפה, יורדת)")
         + st.card("r-4", "rule", "🔑 גורם חסום: חוסמים ואז מבחן"))

VIDEO = Video("S03", "series", "מבחן המנה, השורש והאינטגרל", ws.fix_scenes([title, choose, ratio_, root_, one, integ, ex1, ex2, recap]),
              bank={"22A-A-Q2a": None})
