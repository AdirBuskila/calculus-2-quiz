# -*- coding: utf-8 -*-
"""L09 · בוס: שאלות אמיתיות מהמבחנים — exam walkthrough (build: tools/video/vid.py L09).

Source: courses/limits_diff/C09.js (boss: the piecewise f at the origin, start to finish). Exam parts walked through,
none of them used by any guided quiz or boss quiz:
  (original, exam style) ∛(x³+y³): continuous, f_x = f_y = 1, NOT differentiable (Q on k = h > 0 is (∛2−2)/√2).
             It replaces 22A-B-Q2b after review: (x³+y³)/(x²+y²) is the C07 find-the-bug quiz item and a near twin
             of the boss part 26A-A-Q2b.
  25A-B-Q1a  √(41−4·2.1²−2.9²) by the first differential: 3.875
Avoided on purpose: all six C09 boss-quiz parts (24B-A-Q1a/b, 26A-A-Q1b, 24B-B-Q1b/c, 26A-A-Q2b) and the
same-function parts 23A-C-Q2b / 24A-B-Q2b (identical to the boss question 26A-A-Q2b). Every value is computed below with sympy.
"""
import sympy as sp
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_limits_diff as W
from w_limits_diff import x, y, r, th, h, k

# ---------------------------------------------------------------- exam-style problem (original, bank={}): ∛(x³+y³)
# Replaces 22A-B-Q2b ((x³+y³)/(x²+y²)) after review: that function is the C07 find-the-bug quiz item and a near twin
# of boss part 26A-A-Q2b. Same three steps, different structure: a real cube root, not a quotient.
FB = sp.real_root(x ** 3 + y ** 3, 3)
FBP = r * sp.real_root(sp.cos(th) ** 3 + sp.sin(th) ** 3, 3)                 # f in polar (r > 0 factors out)
for t0 in (0.1, 0.7, 1.9, 2.6, 4.0, 5.5):                                     # the polar form agrees with f
    for r0 in (0.3, 0.05):
        assert abs(float(FB.subs({x: r0 * sp.cos(t0), y: r0 * sp.sin(t0)}) - FBP.subs({r: r0, th: t0}))) < 1e-12
assert W.sup_abs(sp.cos(th) ** 3 + sp.sin(th) ** 3) <= 2                    # |cos³θ+sin³θ| <= 2, so |f| <= ∛2·r
for h0 in (sp.Rational(1, 10), sp.Rational(-1, 10), sp.Rational(-3, 1000), sp.Rational(7, 1000)):
    assert FB.subs({x: h0, y: 0}) == h0 and FB.subs({x: 0, y: h0}) == h0     # ∛(h³) = h for h of both signs
    assert FB.subs({x: h0, y: 0}) / h0 == 1                                  # so (f(h,0) − 0)/h = 1: f_x = f_y = 1
_num, _den = sp.fraction(sp.together(sp.diff(sp.cbrt(x ** 3 + y ** 3), x)))
assert _num.subs({x: 0, y: 0}) == 0 and _den.subs({x: 0, y: 0}) == 0       # the formula's f_x at the origin: 0/0
hp = sp.Symbol("hp", positive=True)
QBD = sp.simplify((sp.cbrt(2 * hp ** 3) - 2 * hp) / sp.sqrt(2 * hp ** 2))   # Q on k = h > 0 (no limit needed: constant)
assert sp.simplify(QBD - (sp.cbrt(2) - 2) / sp.sqrt(2)) == 0 and float(QBD) < -0.5
assert abs(float(QBD) + 0.5233) < 1e-3
assert sp.simplify(sp.real_root(hp ** 3, 3) - hp - 0) == 0                   # Q on k = 0: (h − h)/|h| = 0

# ---------------------------------------------------------------- 25A-B-Q1a
Q2 = BANK["25A-B-Q1a"]
assert "41-4(2.1)^2-(2.9)^2" in Q2["question"]
G = sp.sqrt(41 - 4 * x ** 2 - y ** 2)
GX, GY = sp.diff(G, x), sp.diff(G, y)
assert G.subs({x: 2, y: 3}) == 4
assert GX.subs({x: 2, y: 3}) == -2 and GY.subs({x: 2, y: 3}) == sp.Rational(-3, 4)
APPROX = 4 + (-2) * sp.Rational(1, 10) + sp.Rational(-3, 4) * sp.Rational(-1, 10)
assert APPROX == sp.Rational(31, 8)                                 # 3.875
TRUE = sp.N(G.subs({x: sp.Rational(21, 10), y: sp.Rational(29, 10)}))
assert abs(TRUE - 3.8665) < 1e-3 and abs(TRUE - sp.N(APPROX)) < 0.01

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("זה סרטון הבוס של הקורס: שאלות מבחן אמיתיות, מההתחלה ועד הסוף."),
    P("קודם שאלה בסגנון מבחן על פונקציה בראשית, בשלושה סעיפים, ואחר כך שאלה ממבחן אמיתי: חישוב בקירוב בעזרת הדיפרנציאל."),
    P("בואו נתחיל.", hold=0.4),
], stage='<div class="kicker">L09 · גבולות, רציפות ודיפרנציאביליות</div><h1>בוס: שאלות אמיתיות מהמבחנים</h1>'
         '<p>רציפות, נגזרות חלקיות ודיפרנציאביליות בראשית, ואז הדיפרנציאל בפעולה.</p>', layout="title")

ROAD = [
    ("1. רציפות", "", "מסלולים כדי להפיל, קוטביות וחסם בלי $\\theta$ כדי להוכיח"),
    ("2. נגזרות חלקיות", "", "תמיד לפי ההגדרה, על הצירים"),
    ("3. דיפרנציאביליות", "", "לא רציפה? נגמר. אחרת: $Q$ עם החיסור, וקוטביות"),
]
road = Scene("road", "המסלול", [
    P("כמעט כל מבחן שואל את אותם שלושה דברים על פונקציה המוגדרת בחלקים.", hold=0.2),
    P("אחת: רציפות. מסלולים כדי להפיל, וחסם בקוטביות כדי להוכיח.", do=show("m-0")),
    P("שתיים: נגזרות חלקיות בראשית. תמיד לפי ההגדרה.", do=show("m-1")),
    P("ושלוש: דיפרנציאביליות. אם הפונקציה לא רציפה, התשובה מיד ״לא״. ואם היא רציפה, בונים את $Q$.", do=show("m-2"),
      say="ושלוש: דיפרנציאביליות. אם הפונקציה לא רציפה, התשובה מיד לא. ואם היא רציפה, בונים את קְיוּ.", hold=0.4),
], stage=W.ladder("m", ROAD).replace('<span class="ld-larr"></span>', ''))

S1 = [
    "$f=\\sqrt[3]{r^3\\left(\\cos^3\\theta+\\sin^3\\theta\\right)}=r\\,\\sqrt[3]{\\cos^3\\theta+\\sin^3\\theta}$",
    "$|f-0|\\le r\\,\\sqrt[3]{2}\\ \\to\\ 0=f(0,0)$",
    "$\\displaystyle f_x(0,0)=\\lim_{h\\to0}\\frac{\\sqrt[3]{h^3}-0}{h}=\\lim_{h\\to0}\\frac{h}{h}=1,\\qquad f_y(0,0)=1$",
]
PANEL1 = (W.stem("בסגנון מבחן", "האם $f$ רציפה ב-$(0,0)$? מצאו את $f_x(0,0)$ ו-$f_y(0,0)$. האם $f$ דיפרנציאבילית ב-$(0,0)$?")
          + '<div class="ld-pw" style="font-size:36px">$f(x,y)=\\sqrt[3]{x^3+y^3}$</div>')
part12 = Scene("p12", "רציפות ונגזרות", [
    P("שאלה ראשונה, בסגנון מבחן: $f(x,y)=\\sqrt[3]{x^3+y^3}$, השורש השלישי של $x^3+y^3$.",
      say="שאלה ראשונה, בסגנון מבחן: אֶף שווה השורש השלישי של אִקְס בשלישית ועוד וַואי בשלישית."),
    P("רציפות. בקוטביות, מתחת לשורש יש $r^3$ כפול סוגריים, ולכן יוצא $r$ כפול שורש שלישי של הסוגריים.", do=show("a-0"),
      say="רציפות. בקוטביות, מתחת לשורש יש אָר בשלישית כפול סוגריים, ולכן יוצא אָר כפול שורש שלישי של הסוגריים."),
    P("קוסינוס בשלישית ועוד סינוס בשלישית: לכל היותר שתיים בערך מוחלט. אז השורש השלישי לכל היותר שורש שלישי של שתיים.", hold=0.2),
    P("החסם הוא קבוע כפול $r$. הוא לא תלוי בזווית, ושואף לאפס, שזה הערך בראשית. **רציפה**.", do=show("a-1", "a-v1"),
      say="החסם הוא קבוע כפול אָר. הוא לא תלוי בזווית, ושואף לאפס, שזה הערך בראשית. רציפה."),
    P("נגזרות חלקיות. אם גוזרים את הנוסחה ומציבים אפס, יוצא אפס חלקי אפס. לכן לפי ההגדרה.", do=show("a-c2")),
    P("על ציר $x$ הפונקציה היא השורש השלישי של $h^3$, כלומר $h$. מחלקים ב-$h$, ויוצא אחת.", do=show("a-2"),
      say="על ציר אִקְס הפונקציה היא השורש השלישי של אֵייץ' בשלישית, כלומר אֵייץ'. מחלקים באֵייץ', ויוצא אחת."),
    P("ובגלל הסימטריה, גם הנגזרת לפי $y$ שווה לאחת. שימו לב: אחת, לא אפס. זה ישנה את $Q$.", do=show("a-c1"),
      say="ובגלל הסימטריה, גם הנגזרת לפי וַואי שווה לאחת. שימו לב: אחת, לא אפס. זה ישנה את קְיוּ.", hold=0.4),
], stage='<div class="ld-col" style="width:100%">' + W.eqs("a", S1, size=32, gap=30)
         + W.verdict("a-v1", "רציפה", ok=True) + '</div>',
   panel=PANEL1 + st.card("a-c2", "trap", "⚠️ גזירת הנוסחה בראשית: אפס חלקי אפס")
         + st.card("a-c1", "ex", "$f_x=f_y=1$: יש מה לחסר ב-$Q$"))

S3 = [
    "$\\displaystyle Q=\\frac{\\sqrt[3]{h^3+k^3}-h-k}{\\sqrt{h^2+k^2}}$",
    "$Q=\\sqrt[3]{\\cos^3\\theta+\\sin^3\\theta}-\\cos\\theta-\\sin\\theta$",
    "$\\displaystyle k=0:\\ \\ Q=\\frac{h-h}{|h|}=0$",
    "$\\displaystyle k=h>0:\\ \\ Q=\\frac{\\sqrt[3]{2}\\,h-2h}{\\sqrt2\\,h}=\\frac{\\sqrt[3]{2}-2}{\\sqrt2}\\approx-0.52\\neq0$",
]
part3 = Scene("p3", "דיפרנציאביליות", [
    P("סעיף שלוש. הפונקציה רציפה ויש לה נגזרות חלקיות, אבל זה **לא** מספיק. בונים את $Q$.", do=show("b-0", "b-c0"),
      say="סעיף שלוש. הפונקציה רציפה ויש לה נגזרות חלקיות, אבל זה לא מספיק. בונים את קְיוּ."),
    P("במונה: $f(h,k)$, פחות אחת כפול $h$, פחות אחת כפול $k$. ובמכנה, המרחק מהראשית.",
      say="במונה: אֶף של אֵייץ' וקֵיי, פחות אחת כפול אֵייץ', פחות אחת כפול קֵיי. ובמכנה, המרחק מהראשית."),
    P("בקוטביות כל שלושת המחוברים במונה הם $r$ כפול משהו, והמכנה הוא $r$. ה-$r$ מצטמצם לגמרי.", do=show("b-1"),
      say="בקוטביות כל שלושת המחוברים במונה הם אָר כפול משהו, והמכנה הוא אָר. האָר מצטמצם לגמרי."),
    P("נשאר ביטוי שתלוי בזווית בלבד. זה סימן שהערך תלוי בכיוון. נבדוק שני כיוונים.", hold=0.2),
    P("על ציר $x$, $k=0$: המונה הוא $h$ פחות $h$, ו-$Q$ הוא אפס.", do=show("b-2"),
      say="על ציר אִקְס, קֵיי שווה אפס: המונה הוא אֵייץ' פחות אֵייץ', וקְיוּ הוא אפס."),
    P("על האלכסון, $k=h$ חיובי: שורש שלישי של שתיים פחות שתיים, חלקי שורש שתיים. בערך מינוס חצי.", do=show("b-3"),
      say="על האלכסון, קֵיי שווה אֵייץ' חיובי: שורש שלישי של שתיים פחות שתיים, חלקי שורש שתיים. בערך מינוס חצי."),
    P("$Q$ לא שואף לאפס, ולכן הפונקציה **אינה דיפרנציאבילית** בראשית.", do=show("b-v"),
      say="קְיוּ לא שואף לאפס, ולכן הפונקציה אינה דיפרנציאבילית בראשית.", hold=0.3),
    P("שתי מלכודות כאן: להסיק דיפרנציאביליות מרציפות ונגזרות, או לשכוח לחסר את $h$ ועוד $k$.", do=show("b-t"),
      say="שתי מלכודות כאן: להסיק דיפרנציאביליות מרציפות ונגזרות, או לשכוח לחסר את אֵייץ' ועוד קֵיי.", hold=0.5),
], stage='<div class="ld-col" style="width:100%">' + W.eqs("b", S3, size=30, gap=24)
         + W.verdict("b-v", "לא דיפרנציאבילית", ok=False) + '</div>',
   panel=W.stem("בסגנון מבחן", "האם $f$ דיפרנציאבילית ב-$(0,0)$?")
         + '<div class="ld-pw" style="font-size:36px">$f(x,y)=\\sqrt[3]{x^3+y^3}$</div>'
         + st.card("b-c0", "plain", "$f_x(0,0)=f_y(0,0)=1$")
         + st.card("b-t", "trap", "⚠️ רציפה עם נגזרות: עדיין לא מספיק. ובלי החיסור, $Q$ אחר"))

S4 = [
    "$f(x,y)=\\sqrt{41-4x^2-y^2},\\qquad (x_0,y_0)=(2,3),\\qquad f(2,3)=\\sqrt{16}=4$",
    "$\\displaystyle f_x=\\frac{-4x}{\\sqrt{41-4x^2-y^2}}\\ \\Rightarrow\\ f_x(2,3)=-2,\\qquad f_y=\\frac{-y}{\\sqrt{41-4x^2-y^2}}\\ \\Rightarrow\\ f_y(2,3)=-\\frac34$",
    "$\\Delta x=0.1,\\qquad \\Delta y=-0.1$",
    "$f(2.1,\\,2.9)\\approx4+(-2)(0.1)+\\left(-\\frac34\\right)(-0.1)=4-0.2+0.075=3.875$",
]
diffl = Scene("diffl", "הדיפרנציאל בפעולה", [
    P("שאלה שנייה: חשבו בקירוב את השורש של ארבעים ואחת, פחות ארבע כפול שתיים נקודה אחת בריבוע, פחות שתיים נקודה תשע בריבוע."),
    P("הרעיון: פונקציה דיפרנציאבילית קרובה למישור המשיק שלה. זה בדיוק מה ש-$Q$ שואף לאפס אומר.", do=show("c-c1"),
      say="הרעיון: פונקציה דיפרנציאבילית קרובה למישור המשיק שלה. זה בדיוק מה שקְיוּ שואף לאפס אומר."),
    P("מגדירים $f=\\sqrt{41-4x^2-y^2}$, ובוחרים נקודה קרובה ונוחה: $(2,3)$. שם $f=\\sqrt{16}=4$.", say="מגדירים את השורש כפונקציה של אִקְס ווַואי, ובוחרים נקודה קרובה ונוחה: שתיים ושלוש. שם יוצא שורש שש עשרה, ארבע.", do=show("c-0")),
    P("ליד הנקודה הזאת מה שבתוך השורש חיובי, והנגזרות רציפות. לכן הפונקציה דיפרנציאבילית שם.", do=show("c-c2")),
    P("נגזרות חלקיות בשתיים ושלוש: מינוס שמונה חלקי ארבע, כלומר מינוס שתיים. ומינוס שלושה רבעים.", do=show("c-1")),
    P("ההפרשים: $x$ עולה בעשירית, ו-$y$ יורד בעשירית.", say="ההפרשים: אִקְס עולה בעשירית, ווַואי יורד בעשירית.", do=show("c-2")),
    P("ארבע, פחות שתיים כפול עשירית, ועוד שלושה רבעים כפול עשירית: שלוש נקודה שמונה שבע חמש.", do=show("c-3", "c-v")),
    P("והערך המדויק הוא בערך שלוש נקודה שמונה שש שבע. הקירוב טוב עד כמה אלפיות.", do=show("c-c3")),
    P("המלכודת: הסימן של $\\Delta y$. $2.9$ קטן מ-$3$, ולכן ההפרש **שלילי**.", say="המלכודת: הסימן של דלתא וַואי. שתיים נקודה תשע קטן משלוש, ולכן ההפרש שלילי.", do=show("c-t"), hold=0.5),
], stage='<div class="ld-col" style="width:100%">' + W.eqs("c", S4, size=25, gap=26)
         + W.verdict("c-v", "$\\approx3.875$", ok=True) + '</div>',
   panel=W.stem(Q2["id"], "חשבו בקירוב את $\\sqrt{41-4(2.1)^2-(2.9)^2}$ בעזרת הדיפרנציאל הראשון.")
         + st.card("c-c1", "rule", "🔑 $f(x_0+\\Delta x,y_0+\\Delta y)\\approx f+f_x\\Delta x+f_y\\Delta y$")
         + st.card("c-c2", "ex", "נגזרות רציפות ליד $(2,3)$: דיפרנציאבילית שם")
         + st.card("c-c3", "plain", "ערך מדויק: $\\approx3.8665$")
         + st.card("c-t", "trap", "⚠️ $\\Delta y=2.9-3=-0.1$, שלילי"))

recap = Scene("recap", "סיכום הקורס", [
    P("לסיכום הקורס: רציפות בראשית, מסלולים כדי להפיל, וחסם בקוטביות כדי להוכיח.", do=show("r-1")),
    P("נגזרות חלקיות בראשית: רק לפי ההגדרה, על הצירים.", do=show("r-2")),
    P("דיפרנציאביליות: $Q$ עם החיסור, ואז חסם, או מסלול שבו $Q$ לא שואף לאפס.", do=show("r-3"),
      say="דיפרנציאביליות: קְיוּ עם החיסור, ואז חסם, או מסלול שבו קְיוּ לא שואף לאפס."),
    P("ועכשיו תורכם: שאלות הבוס מחכות לכם באפליקציה. בהצלחה!", do=show("r-4"), hold=0.6),
], stage=W.ladder("mr", ROAD).replace(' h"', '"').replace('<span class="ld-larr"></span>', ''),
   panel=st.card("r-1", "rule", "🔑 רציפות: מסלולים מפילים, חסם מוכיח")
         + st.card("r-2", "rule", "🔑 נגזרות בראשית: לפי ההגדרה")
         + st.card("r-3", "rule", "🔑 $Q\\to0$: חסם. $Q\\not\\to0$: מסלול")
         + st.card("r-4", "ex", "עכשיו: שאלות הבוס"))

VIDEO = Video("L09", "limits_diff", "בוס: שאלות אמיתיות מהמבחנים", [title, road, part12, part3, diffl, recap],
              bank={"25A-B-Q1a": None})
