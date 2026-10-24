# -*- coding: utf-8 -*-
"""Generator for tools/raw/23A-C.json -- calculus-2 (20252), semester A 2023, moed C (27/04/2023).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_23A-C.py

Source: exam 27.4.23 (3 pages, 5 questions of 25 points, a=12, b=13, solve 4 of 5).
There is NO key for this sitting. All 10 items were solved by the solver (solutionSource "solved", official False),
pending the blind refuter. Header (lecturer names) is not transcribed. Text layers are garbled; everything is
transcribed from page renders.

Transcription notes
- Q1b: the printed question asks by what factor the rate of change in the direction u is smaller than the maximal rate.
- Q2a asks for two series in one part; stored as one item. arctan^n means the n-th power of arctan.
- Q4b: the region is the part of the unit disk in the first quadrant lying between y=0 and y=sqrt(3)x.

Checks: tools/verify/23A-C/solve_23A-C.py (sympy + numeric, every computation below) and
tools/verify/23A-C/check.py (geometry; writes regions.json and contours.json).
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "23A-C.json"


def Q(num, part, kind, topic, question, solution, points):
    return {"num": num, "part": part, "kind": kind, "topic": topic, "points": points, "question": question,
            "solution": solution.strip("\n"), "solutionSource": "solved", "official": False, "confidence": "high"}


questions = []

# ===== Q1a =====
questions.append(Q(1, "א", "computation", "double_integrals",
"מצאו שטח של צורה מישורית המוגבלת בין שני המעגלים:\n$$x^2+y^2=2x,\\quad x^2+y^2=4x$$",
r"""נשלים לריבוע:
$$x^2+y^2=2x\iff(x-1)^2+y^2=1,\qquad x^2+y^2=4x\iff(x-2)^2+y^2=4.$$
המעגל הראשון (מרכז $(1,0)$, רדיוס $1$) נמצא בתוך המעגל השני (מרכז $(2,0)$, רדיוס $2$), ושניהם משיקים בראשית. הצורה היא התחום שבין שני המעגלים.
נעבור לקואורדינטות קוטביות $x=r\cos\theta,\ y=r\sin\theta$:
$$r^2=2r\cos\theta\Rightarrow r=2\cos\theta,\qquad r^2=4r\cos\theta\Rightarrow r=4\cos\theta,$$
והתחום הוא $-\frac{\pi}{2}\le\theta\le\frac{\pi}{2},\ 2\cos\theta\le r\le4\cos\theta$. היעקוביאן הוא $r$, ולכן
$$S=\int_{-\pi/2}^{\pi/2}\int_{2\cos\theta}^{4\cos\theta}r\,dr\,d\theta=\int_{-\pi/2}^{\pi/2}\frac{16\cos^2\theta-4\cos^2\theta}{2}\,d\theta=6\int_{-\pi/2}^{\pi/2}\cos^2\theta\,d\theta$$
$$=6\int_{-\pi/2}^{\pi/2}\frac{1+\cos2\theta}{2}\,d\theta=6\cdot\frac{\pi}{2}=3\pi.$$
בדיקה: שטח העיגול הגדול פחות שטח העיגול הקטן הוא $4\pi-\pi=3\pi$.""", 12))

# ===== Q1b =====
questions.append(Q(1, "ב", "computation", "gradient_directional",
r"""נתונה הפונקציה $f(x,y,z)=x^2y\sqrt{z}$. פי כמה קצב שינוי הפונקציה בנקודה $(2,1,1)$ בכיוון של הוקטור $\vec u=\vec i+2\vec j+2\vec k$ קטן מקצב השינוי המקסימלי של הפונקציה בנקודה זו?""",
r"""הנגזרות החלקיות:
$$f_x=2xy\sqrt z,\qquad f_y=x^2\sqrt z,\qquad f_z=\frac{x^2y}{2\sqrt z}.$$
בנקודה $(2,1,1)$:
$$\nabla f(2,1,1)=(4,4,2).$$
קצב השינוי המקסימלי הוא אורך הגרדיאנט:
$$|\nabla f(2,1,1)|=\sqrt{16+16+4}=6.$$
וקטור היחידה בכיוון $\vec u$: $|\vec u|=\sqrt{1+4+4}=3$, ולכן $\hat u=\left(\frac13,\frac23,\frac23\right)$. הנגזרת הכיוונית:
$$D_{\hat u}f(2,1,1)=\nabla f\cdot\hat u=\frac{4+8+4}{3}=\frac{16}{3}.$$
היחס:
$$\frac{|\nabla f|}{D_{\hat u}f}=\frac{6}{16/3}=\frac{18}{16}=\frac98.$$
קצב השינוי בכיוון $\vec u$ קטן פי $\frac98$ מקצב השינוי המקסימלי.""", 13))

# ===== Q2a =====
questions.append(Q(2, "א", "computation", "numeric_series",
r"""בדקו התכנסות בהחלט, בתנאי או התבדרות של הטורים הבאים:
$$\sum_{n=1}^{\infty}\frac{2^n\cos n}{3^n}$$
$$\sum_{n=1}^{\infty}\arctan^n\!\left(\frac{n+2}{n+3}\right)$$""",
r"""**הטור הראשון.** נכתוב $\frac{2^n\cos n}{3^n}=\left(\frac23\right)^n\cos n$. מתקיים
$$\left|\left(\frac23\right)^n\cos n\right|\le\left(\frac23\right)^n,$$
ו-$\sum_{n=1}^{\infty}\left(\frac23\right)^n$ הוא טור הנדסי עם מנה $\frac23<1$, ולכן מתכנס. לפי מבחן ההשוואה $\sum\left|\frac{2^n\cos n}{3^n}\right|$ מתכנס, כלומר הטור מתכנס בהחלט.

**הטור השני.** לכל $n\ge1$ מתקיים $0<\frac{n+2}{n+3}<1$, ולכן $0<\arctan\left(\frac{n+2}{n+3}\right)<\frac{\pi}{4}$ והאיברים חיוביים. נשתמש במבחן השורש (קושי):
$$\sqrt[n]{a_n}=\arctan\left(\frac{n+2}{n+3}\right)\xrightarrow[n\to\infty]{}\arctan1=\frac{\pi}{4}<1.$$
לכן הטור מתכנס, ומכיוון שאיבריו חיוביים הוא מתכנס בהחלט.""", 12))

# ===== Q2b =====
questions.append(Q(2, "ב", "computation", "partials_differentiability",
r"""נתונה הפונקציה
$$f(x,y)=\begin{cases}\dfrac{x^3+y^3}{2x^2+y^2}, & (x,y)\neq(0,0)\\[2mm] 0, & (x,y)=(0,0)\end{cases}$$
האם $f(x,y)$ דיפרנציאבילית ב-$(0,0)$?""",
r"""**נגזרות חלקיות בראשית (לפי ההגדרה).**
$$f_x(0,0)=\lim_{h\to0}\frac{f(h,0)-f(0,0)}{h}=\lim_{h\to0}\frac{h^3/(2h^2)}{h}=\frac12,$$
$$f_y(0,0)=\lim_{h\to0}\frac{f(0,h)-f(0,0)}{h}=\lim_{h\to0}\frac{h^3/h^2}{h}=1.$$
**תנאי הדיפרנציאביליות.** $f$ דיפרנציאבילית ב-$(0,0)$ אם ורק אם
$$\lim_{(x,y)\to(0,0)}\frac{f(x,y)-f(0,0)-\frac12x-y}{\sqrt{x^2+y^2}}=0.$$
נחשב את המונה:
$$\frac{x^3+y^3}{2x^2+y^2}-\frac x2-y=\frac{2x^3+2y^3-x(2x^2+y^2)-2y(2x^2+y^2)}{2(2x^2+y^2)}=\frac{-xy(4x+y)}{2(2x^2+y^2)}.$$
לכן יש לבדוק את
$$\lim_{(x,y)\to(0,0)}\frac{-xy(4x+y)}{2(2x^2+y^2)\sqrt{x^2+y^2}}.$$
לאורך $y=0$ הביטוי שווה ל-$0$, והגבול $0$.
לאורך $y=x$ עם $x>0$:
$$\frac{-x^2\cdot5x}{2\cdot3x^2\cdot\sqrt2\,x}=-\frac{5}{6\sqrt2}\neq0.$$
קיבלנו שני גבולות שונים לאורך שני מסלולים, ולכן הגבול אינו קיים (ובפרט אינו $0$).
**מסקנה:** $f$ אינה דיפרנציאבילית ב-$(0,0)$ (אף על פי שהיא רציפה שם ויש לה נגזרות חלקיות).""", 13))

# ===== Q3a =====
questions.append(Q(3, "א", "computation", "power_series",
r"""עבור אילו ערכי $x$ הטור מתכנס (מצאו רדיוס התכנסות ותחום התכנסות):
$$\sum_{n=1}^{\infty}x^n\,\frac{1}{2^n+3^n}$$""",
r"""**רדיוס ההתכנסות.** $a_n=\frac{1}{2^n+3^n}$. לפי נוסחת קושי-הדמר:
$$\frac1R=\lim_{n\to\infty}\sqrt[n]{|a_n|}=\lim_{n\to\infty}\frac{1}{\sqrt[n]{2^n+3^n}}=\lim_{n\to\infty}\frac{1}{3\sqrt[n]{1+\left(\frac23\right)^n}}=\frac13,$$
ולכן $R=3$: הטור מתכנס בהחלט עבור $|x|<3$ ומתבדר עבור $|x|>3$.

**קצוות.**
* $x=3$: האיבר הכללי $\frac{3^n}{2^n+3^n}=\frac{1}{1+\left(\frac23\right)^n}\to1\neq0$, ולכן הטור מתבדר (התנאי ההכרחי אינו מתקיים).
* $x=-3$: האיבר הכללי $(-1)^n\frac{3^n}{2^n+3^n}$, והערך המוחלט שלו שואף ל-$1$, ולכן הוא אינו שואף ל-$0$ והטור מתבדר.

**תחום ההתכנסות:** $(-3,3)$.""", 12))

# ===== Q3b =====
questions.append(Q(3, "ב", "proof", "chain_rule_identity",
r"""הראו כי הפונקציה $z=y\cdot g\left(x^2-y^2\right)$ כאשר $g(t)$ גזירה עבור כל $t$ ו-$x,y\neq0$ מקיימת את המשוואה:
$$\frac{1}{x}\cdot\frac{\partial z}{\partial x}+\frac{1}{y}\cdot\frac{\partial z}{\partial y}=\frac{z}{y^2}.$$""",
r"""נסמן $t=x^2-y^2$, כך ש-$z=y\,g(t)$, $\frac{\partial t}{\partial x}=2x$ ו-$\frac{\partial t}{\partial y}=-2y$.
לפי כלל השרשרת:
$$\frac{\partial z}{\partial x}=y\cdot\frac{dg}{dt}\cdot\frac{\partial t}{\partial x}=2xy\,g'(t),$$
$$\frac{\partial z}{\partial y}=g(t)+y\cdot\frac{dg}{dt}\cdot\frac{\partial t}{\partial y}=g(t)-2y^2g'(t).$$
נציב באגף שמאל (מותר לחלק כי $x,y\neq0$):
$$\frac1x\cdot2xy\,g'(t)+\frac1y\left(g(t)-2y^2g'(t)\right)=2y\,g'(t)+\frac{g(t)}{y}-2y\,g'(t)=\frac{g(t)}{y}.$$
מצד שני
$$\frac{z}{y^2}=\frac{y\,g(t)}{y^2}=\frac{g(t)}{y}.$$
שני האגפים שווים, כנדרש.""", 13))

# ===== Q4a =====
questions.append(Q(4, "א", "computation", "double_integrals",
r"""החליפו את סדר האינטגרציה באינטגרל
$$\int_{-4}^{0}dx\int_{0}^{\sqrt{x+4}}f(x,y)\,dy+\int_{0}^{2}dx\int_{0}^{2-x}f(x,y)\,dy$$""",
r"""**תיאור התחום.** האינטגרל הראשון: $-4\le x\le0,\ 0\le y\le\sqrt{x+4}$ (מתחת לחצי העליון של הפרבולה $y^2=x+4$). האינטגרל השני: $0\le x\le2,\ 0\le y\le2-x$ (מתחת לישר $x+y=2$). שני החלקים נפגשים בנקודה $(0,2)$, כי $\sqrt{0+4}=2=2-0$. האיחוד הוא תחום אחד עם הקודקודים $(-4,0)$, $(2,0)$, $(0,2)$, החסום מלמטה על ידי $y=0$, משמאל על ידי הפרבולה ומימין על ידי הישר.
**בסדר ההפוך.** עבור $y$ קבוע בין $0$ ל-$2$:
* הגבול השמאלי הוא הפרבולה: $y=\sqrt{x+4}\iff x=y^2-4$ (עבור $y\ge0$);
* הגבול הימני הוא הישר: $y=2-x\iff x=2-y$.

לכן
$$\int_{-4}^{0}dx\int_{0}^{\sqrt{x+4}}f\,dy+\int_{0}^{2}dx\int_{0}^{2-x}f\,dy=\int_{0}^{2}dy\int_{y^2-4}^{2-y}f(x,y)\,dx.$$
בדיקה עם $f\equiv1$: בשני הסדרים השטח הוא $\frac{16}{3}+2=\int_0^2\left(6-y-y^2\right)dy=\frac{22}{3}$.""", 12))

# ===== Q4b =====
questions.append(Q(4, "ב", "computation", "absolute_extrema",
r"""מצאו אקסטרמומים מוחלטים של הפונקציה $f(x,y)=x^2+y^2+4xy$ בתחום המוגבל ע"י $x^2+y^2=1,\ \ y=0,\ \ y=\sqrt{3}x$ ברביע הראשון $(x\ge0,\ y\ge0)$.""",
r"""התחום $D$ הוא גזרה של עיגול היחידה: $0\le\theta\le\frac{\pi}{3},\ 0\le r\le1$. הוא סגור וחסום ו-$f$ רציפה, ולכן לפי ויירשטראס יש לה מקסימום ומינימום מוחלטים ב-$D$. קודקודי התחום: $(0,0)$, $(1,0)$, $\left(\frac12,\frac{\sqrt3}{2}\right)$.

**פנים התחום.**
$$f_x=2x+4y=0,\qquad f_y=2y+4x=0\ \Rightarrow\ (x,y)=(0,0),$$
וזה קודקוד של התחום ולא נקודה פנימית. אין נקודות קריטיות בפנים.

**השפה.**
* הקטע $y=0,\ 0\le x\le1$: $f=x^2$, עולה. ערכים: $f(0,0)=0$, $f(1,0)=1$.
* הקטע $y=\sqrt3x,\ 0\le x\le\frac12$: $f=x^2+3x^2+4\sqrt3x^2=\left(4+4\sqrt3\right)x^2$, עולה. ערכים: $0$ ו-$f\left(\frac12,\frac{\sqrt3}{2}\right)=1+\sqrt3$.
* הקשת $x=\cos\theta,\ y=\sin\theta,\ 0\le\theta\le\frac{\pi}{3}$:
$$f=1+4\sin\theta\cos\theta=1+2\sin2\theta,\qquad \frac{df}{d\theta}=4\cos2\theta=0\Rightarrow\theta=\frac{\pi}{4}.$$
נקבל את הנקודה $\left(\frac{1}{\sqrt2},\frac{1}{\sqrt2}\right)$ עם $f=1+2=3$. (בשיטת לגראנז' $\nabla f=\lambda\nabla(x^2+y^2)$ עם $x^2+y^2=1$ מתקבלים $y=\pm x$, והנקודה היחידה בגזרה היא אותה נקודה.)

**השוואת ערכים:**
$$f(0,0)=0,\quad f(1,0)=1,\quad f\left(\tfrac12,\tfrac{\sqrt3}{2}\right)=1+\sqrt3\approx2.73,\quad f\left(\tfrac{1}{\sqrt2},\tfrac{1}{\sqrt2}\right)=3.$$
**מסקנה:** המקסימום המוחלט הוא $3$ בנקודה $\left(\frac{1}{\sqrt2},\frac{1}{\sqrt2}\right)$, והמינימום המוחלט הוא $0$ בנקודה $(0,0)$.""", 13))

# ===== Q5a =====
questions.append(Q(5, "א", "computation", "local_extrema",
r"""מצאו וסווגו את נקודות האקסטרמום של הפונקציה:
$$f(x,y)=\left(x^2-2y^2\right)e^{x-y}$$""",
r"""**נקודות קריטיות.**
$$f_x=\left(x^2+2x-2y^2\right)e^{x-y},\qquad f_y=\left(-x^2-4y+2y^2\right)e^{x-y}.$$
מכיוון ש-$e^{x-y}>0$, יש לפתור
$$\begin{cases}x^2+2x-2y^2=0&\text{(I)}\\-x^2-4y+2y^2=0&\text{(II)}\end{cases}$$
חיבור (I) ו-(II) נותן $2x-4y=0$, כלומר $x=2y$. נציב ב-(I): $4y^2+4y-2y^2=2y(y+2)=0$, ולכן $y=0$ או $y=-2$.
הנקודות הקריטיות: $(0,0)$ ו-$(-4,-2)$.

**נגזרות שניות.**
$$f_{xx}=\left(x^2+4x+2-2y^2\right)e^{x-y},\quad f_{yy}=\left(x^2-2y^2+8y-4\right)e^{x-y},\quad f_{xy}=\left(2y^2-x^2-2x-4y\right)e^{x-y}.$$
* הנקודה $(0,0)$: $f_{xx}=2,\ f_{yy}=-4,\ f_{xy}=0$, ולכן $D=2\cdot(-4)-0=-8<0$: **נקודת אוכף**.
* הנקודה $(-4,-2)$: $e^{x-y}=e^{-2}$ ו-
$$f_{xx}=-6e^{-2},\quad f_{yy}=-12e^{-2},\quad f_{xy}=8e^{-2},$$
$$D=(-6)(-12)e^{-4}-64e^{-4}=8e^{-4}>0,\qquad f_{xx}<0,$$
ולכן זו **נקודת מקסימום מקומי**, עם $f(-4,-2)=(16-8)e^{-2}=\frac{8}{e^2}$.""", 12))

# ===== Q5b =====
questions.append(Q(5, "ב", "computation", "taylor_maclaurin",
r"""פתחו את הפונקציה $f(x)=\dfrac{1}{x^2+x-2}$ לטור מקלורן. מהו תחום התכנסות הטור?
הסיקו את הערך של $f^{(10)}(0)$.""",
r"""**פירוק לשברים חלקיים.** $x^2+x-2=(x-1)(x+2)$, ולכן
$$\frac{1}{x^2+x-2}=\frac13\left(\frac{1}{x-1}-\frac{1}{x+2}\right).$$
**פיתוח כל שבר** בעזרת הטור ההנדסי:
$$\frac{1}{x-1}=-\frac{1}{1-x}=-\sum_{n=0}^{\infty}x^n,\qquad|x|<1;$$
$$\frac{1}{x+2}=\frac12\cdot\frac{1}{1+\frac x2}=\frac12\sum_{n=0}^{\infty}(-1)^n\frac{x^n}{2^n}=\sum_{n=0}^{\infty}\frac{(-1)^n}{2^{n+1}}x^n,\qquad|x|<2.$$
לכן
$$f(x)=-\frac13\sum_{n=0}^{\infty}\left(1+\frac{(-1)^n}{2^{n+1}}\right)x^n.$$
**תחום ההתכנסות.** שני הטורים מתכנסים יחד עבור $|x|<1$. עבור $1\le|x|<2$ הטור השני מתכנס והראשון מתבדר, ולכן הסכום מתבדר. בקצוות $x=\pm1$ הערך המוחלט של האיבר הכללי שואף ל-$\frac13\neq0$, ולכן הטור מתבדר. תחום ההתכנסות: $(-1,1)$.

**הנגזרת העשירית.** מקדם $x^{n}$ בטור מקלורן הוא $\frac{f^{(n)}(0)}{n!}$. עבור $n=10$:
$$\frac{f^{(10)}(0)}{10!}=-\frac13\left(1+\frac{1}{2^{11}}\right)=-\frac{2049}{6144},$$
$$f^{(10)}(0)=-\frac{10!}{3}\left(1+\frac{1}{2^{11}}\right)=-\frac{10!\cdot2049}{3\cdot2^{11}}=-\frac{9681525}{8}=-1210190.625.$$""", 13))

# ---- rubric / pitfalls / steps (ai-draft). Every expected value is re-computed in tools/verify/23A-C/steps_23A-C.py ----
IDS = "abcdefgh"


def opts(*vals):
    return [{"id": IDS[i], "type": "text", "value": v} for i, v in enumerate(vals)]


def rub(*items):
    return [{"text": t, "points": p} for t, p in items]


def choice(prompt, right, wrong, explain, pos=0):
    vals = list(wrong)
    vals.insert(pos, right)
    return {"type": "choice", "prompt": prompt, "options": opts(*vals), "correctId": IDS[pos], "explain": explain}


def num(prompt, answer, explain, tol=0):
    return {"type": "numeric", "prompt": prompt, "answer": answer, "tol": tol, "explain": explain}


def add(n, part, **kw):
    for q in questions:
        if q["num"] == n and q.get("part") == part:
            q.update(kw)
            q["rubricSource"] = "ai-draft"
            q["stepsSource"] = "ai-draft"
            return
    raise KeyError((n, part))


add(1, "א",
    rubric=rub(("השלמה לריבוע וזיהוי שני המעגלים המשיקים בראשית", 3),
               ("מעבר לקואורדינטות קוטביות: $2\\cos\\theta\\le r\\le4\\cos\\theta$ ו-$-\\frac{\\pi}{2}\\le\\theta\\le\\frac{\\pi}{2}$", 3),
               ("בניית האינטגרל עם היעקוביאן $r$ וחישוב האינטגרל הפנימי", 3),
               ("חישוב האינטגרל על $\\theta$ וקבלת $3\\pi$", 3)),
    pitfalls=["לשכוח את היעקוביאן $r$ במעבר לקואורדינטות קוטביות.",
              "לבחור תחום זווית שגוי: עבור $\\theta$ מחוץ ל-$\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]$ מתקבל $\\cos\\theta<0$ ולכן $r<0$."],
    steps=[
        choice("מהם גבולות האינטגרציה בקואורדינטות קוטביות לתחום שבין שני המעגלים?",
               "$-\\frac{\\pi}{2}\\le\\theta\\le\\frac{\\pi}{2},\\ 2\\cos\\theta\\le r\\le4\\cos\\theta$",
               ["$0\\le\\theta\\le2\\pi,\\ 2\\cos\\theta\\le r\\le4\\cos\\theta$",
                "$-\\frac{\\pi}{2}\\le\\theta\\le\\frac{\\pi}{2},\\ 2\\le r\\le4$",
                "$-\\frac{\\pi}{2}\\le\\theta\\le\\frac{\\pi}{2},\\ \\cos\\theta\\le r\\le2\\cos\\theta$"],
               "המעגל $x^2+y^2=2x$ הופך ל-$r=2\\cos\\theta$ והמעגל $x^2+y^2=4x$ ל-$r=4\\cos\\theta$. שניהם נמצאים ב-$x\\ge0$, ולכן $-\\frac{\\pi}{2}\\le\\theta\\le\\frac{\\pi}{2}$. הגבולות $2\\le r\\le4$ מתארים טבעת סביב הראשית, וזה לא התחום.", pos=2),
        num("האינטגרל הפנימי $\\int_{2\\cos\\theta}^{4\\cos\\theta}r\\,dr$ שווה ל-$c\\cos^2\\theta$. מהו $c$?", 6,
            "$\\frac{(4\\cos\\theta)^2-(2\\cos\\theta)^2}{2}=\\frac{12\\cos^2\\theta}{2}=6\\cos^2\\theta$."),
        num("מהו השטח, מחולק ב-$\\pi$ (כלומר $S/\\pi$)?", 3,
            "$6\\int_{-\\pi/2}^{\\pi/2}\\cos^2\\theta\\,d\\theta=6\\cdot\\frac{\\pi}{2}=3\\pi$. זה גם שטח העיגול הגדול פחות שטח העיגול הקטן, $4\\pi-\\pi$."),
    ])

add(1, "ב",
    rubric=rub(("חישוב הנגזרות החלקיות $f_x,f_y,f_z$", 3),
               ("הצבה בנקודה וקבלת $\\nabla f(2,1,1)=(4,4,2)$", 2),
               ("קצב השינוי המקסימלי הוא $|\\nabla f|=6$", 3),
               ("נרמול הוקטור $\\vec u$ וחישוב הנגזרת הכיוונית $\\frac{16}{3}$", 3),
               ("היחס $\\frac{6}{16/3}=\\frac98$", 2)),
    pitfalls=["לחשב את הנגזרת הכיוונית עם $\\vec u$ בלי לנרמל אותו (כאן $|\\vec u|=3$), ולקבל $16$ במקום $\\frac{16}{3}$.",
              "להפוך את היחס: השאלה היא פי כמה הקצב בכיוון $\\vec u$ קטן מהמקסימלי, ולכן מחלקים את המקסימלי בקצב בכיוון $\\vec u$."],
    steps=[
        num("מהו $f_z(2,1,1)$ עבור $f=x^2y\\sqrt z$?", 2,
            "$f_z=\\frac{x^2y}{2\\sqrt z}$, ולכן $f_z(2,1,1)=\\frac{4}{2}=2$. שני הרכיבים האחרים הם $f_x=f_y=4$."),
        num("מהו קצב השינוי המקסימלי $|\\nabla f(2,1,1)|$?", 6,
            "$\\sqrt{4^2+4^2+2^2}=\\sqrt{36}=6$."),
        num("מהי הנגזרת הכיוונית בכיוון $\\vec u=\\vec i+2\\vec j+2\\vec k$ (תשובה עשרונית, דיוק $0.001$)?", 5.3333,
            "$|\\vec u|=3$, ולכן $\\hat u=\\left(\\frac13,\\frac23,\\frac23\\right)$ והנגזרת היא $\\frac{4+8+4}{3}=\\frac{16}{3}$.", tol=0.001),
        num("פי כמה קצב השינוי בכיוון $\\vec u$ קטן מהמקסימלי (תשובה עשרונית)?", 1.125,
            "$\\frac{6}{16/3}=\\frac{18}{16}=\\frac98=1.125$."),
    ])

add(2, "א",
    rubric=rub(("הטור הראשון: חסימה $\\left|\\left(\\frac23\\right)^n\\cos n\\right|\\le\\left(\\frac23\\right)^n$", 3),
               ("הטור הראשון: טור הנדסי מתכנס ומבחן ההשוואה, ולכן התכנסות בהחלט", 3),
               ("הטור השני: האיברים חיוביים כי $0<\\arctan\\frac{n+2}{n+3}<\\frac{\\pi}{4}$", 2),
               ("הטור השני: מבחן השורש עם הגבול $\\arctan1=\\frac{\\pi}{4}<1$", 3),
               ("הטור השני: מסקנה שהטור מתכנס בהחלט", 1)),
    pitfalls=["לטעות ב-$\\arctan^n$ ולהבין את זה כפונקציה הפוכה או כהרכבה, במקום חזקה $n$ של $\\arctan$.",
              "לשכוח שהגורם $\\cos n$ חסום בערכו המוחלט על ידי $1$, ולכן אינו משנה את ההתכנסות."],
    steps=[
        num("בטור הראשון מחסמים את הערך המוחלט של האיבר על ידי טור הנדסי. מהי מנת הטור ההנדסי (תשובה עשרונית, דיוק $0.001$)?", 0.6667,
            "$\\left|\\frac{2^n\\cos n}{3^n}\\right|\\le\\left(\\frac23\\right)^n$, ומנה $\\frac23<1$ נותנת טור מתכנס.", tol=0.001),
        num("במבחן השורש לטור השני, לְמה שואף $\\sqrt[n]{a_n}=\\arctan\\frac{n+2}{n+3}$ (תשובה עשרונית, דיוק $0.001$)?", 0.7854,
            "$\\frac{n+2}{n+3}\\to1$ ו-$\\arctan1=\\frac{\\pi}{4}\\approx0.7854$.", tol=0.001),
        choice("מה מסקנת הפתרון לגבי שני הטורים?",
               "שניהם מתכנסים בהחלט",
               ["הראשון מתכנס בהחלט והשני מתבדר",
                "שניהם מתכנסים בתנאי בלבד",
                "הראשון מתכנס בתנאי והשני מתכנס בהחלט"],
               "בטור הראשון מתקבל חסם הנדסי מתכנס, ובשני הגבול $\\frac{\\pi}{4}<1$. בשני הטורים האיברים בערך מוחלט מתכנסים, ולכן ההתכנסות בהחלט.", pos=1),
    ])

add(2, "ב",
    rubric=rub(("חישוב $f_x(0,0)=\\frac12$ ו-$f_y(0,0)=1$ מההגדרה", 4),
               ("ניסוח תנאי הדיפרנציאביליות עם הגבול של $\\frac{f-f(0,0)-f_xx-f_yy}{\\sqrt{x^2+y^2}}$", 3),
               ("פישוט המונה ל-$\\frac{-xy(4x+y)}{2(2x^2+y^2)}$", 2),
               ("שני מסלולים שונים ($y=0$ ו-$y=x$) עם גבולות שונים", 3),
               ("מסקנה: $f$ אינה דיפרנציאבילית ב-$(0,0)$", 1)),
    pitfalls=["להסיק דיפרנציאביליות מעצם קיום הנגזרות החלקיות ומהרציפות. אלה תנאים הכרחיים בלבד.",
              "לחשב את הנגזרות החלקיות בראשית בעזרת כללי גזירה במקום מההגדרה, כי הפונקציה מוגדרת בנפרד בראשית."],
    steps=[
        num("מהו $f_x(0,0)$? (תשובה עשרונית)", 0.5,
            "$f(h,0)=\\frac{h^3}{2h^2}=\\frac h2$, ולכן $\\frac{f(h,0)-0}{h}=\\frac12$."),
        num("מהו $f_y(0,0)$?", 1,
            "$f(0,h)=\\frac{h^3}{h^2}=h$, ולכן $\\frac{f(0,h)-0}{h}=1$."),
        num("בבדיקת הגבול של $\\frac{-xy(4x+y)}{2(2x^2+y^2)\\sqrt{x^2+y^2}}$ לאורך $y=x$, $x>0$, מתקבל $-\\frac{5}{6\\sqrt2}$. מהו הערך העשרוני שלו (דיוק $0.001$)?", -0.5893,
            "$-\\frac{5}{6\\sqrt2}\\approx-0.5893$. הערך שונה מ-$0$, בעוד שלאורך $y=0$ הביטוי שווה ל-$0$.", tol=0.001),
        choice("מה מסקנת הפתרון לגבי דיפרנציאביליות $f$ ב-$(0,0)$?",
               "$f$ אינה דיפרנציאבילית, כי הגבול הנדרש אינו קיים (שני מסלולים נותנים ערכים שונים)",
               ["$f$ דיפרנציאבילית, כי שתי הנגזרות החלקיות קיימות בראשית",
                "$f$ דיפרנציאבילית, כי היא רציפה בראשית",
                "$f$ אינה דיפרנציאבילית, כי היא אינה רציפה בראשית"],
               "קיום נגזרות חלקיות ורציפות אינם מבטיחים דיפרנציאביליות. כאן הגבול של השארית מחולקת ב-$\\sqrt{x^2+y^2}$ אינו קיים, ולכן $f$ אינה דיפרנציאבילית. בנוסף $f$ רציפה בראשית, כי $|f|\\le|x|+|y|$.", pos=0),
    ])

add(3, "א",
    rubric=rub(("חישוב רדיוס ההתכנסות $R=3$ בעזרת $\\sqrt[n]{|a_n|}\\to\\frac13$", 5),
               ("הקצה $x=3$: האיבר הכללי שואף ל-$1$ ולכן הטור מתבדר", 3),
               ("הקצה $x=-3$: הערך המוחלט של האיבר הכללי שואף ל-$1$ ולכן הטור מתבדר", 3),
               ("ניסוח תחום ההתכנסות $(-3,3)$", 1)),
    pitfalls=["לשכוח לבדוק את הקצוות ולכתוב קטע סגור. הרדיוס אינו קובע את ההתנהגות בקצוות.",
              "לטעות בחישוב $\\sqrt[n]{2^n+3^n}$: הגורם הגדול שולט, והגבול הוא $3$ ולא $2$ ולא $5$."],
    steps=[
        num("מהו רדיוס ההתכנסות של $\\sum_{n=1}^{\\infty}\\frac{x^n}{2^n+3^n}$?", 3,
            "$\\sqrt[n]{2^n+3^n}=3\\sqrt[n]{1+\\left(\\frac23\\right)^n}\\to3$, ולכן $\\sqrt[n]{|a_n|}\\to\\frac13$ ו-$R=3$."),
        num("בקצה $x=3$ האיבר הכללי הוא $\\frac{3^n}{2^n+3^n}$. לְמה הוא שואף?", 1,
            "$\\frac{3^n}{2^n+3^n}=\\frac{1}{1+\\left(\\frac23\\right)^n}\\to1\\neq0$, ולכן התנאי ההכרחי להתכנסות אינו מתקיים."),
        choice("מהו תחום ההתכנסות של הטור?",
               "$(-3,3)$",
               ["$[-3,3]$", "$[-3,3)$", "$(-3,3]$"],
               "בשני הקצוות האיבר הכללי אינו שואף ל-$0$ (הערך המוחלט שלו שואף ל-$1$), ולכן הטור מתבדר בהם והקצוות אינם בתחום.", pos=3),
    ])

add(3, "ב",
    rubric=rub(("הצבת $t=x^2-y^2$ וחישוב $\\frac{\\partial t}{\\partial x}=2x$ ו-$\\frac{\\partial t}{\\partial y}=-2y$", 2),
               ("כלל השרשרת: $\\frac{\\partial z}{\\partial x}=2xy\\,g'(t)$", 3),
               ("כלל המכפלה והשרשרת: $\\frac{\\partial z}{\\partial y}=g(t)-2y^2g'(t)$", 3),
               ("הצבה באגף שמאל ופישוט ל-$\\frac{g(t)}{y}$", 3),
               ("חישוב אגף ימין $\\frac{z}{y^2}=\\frac{g(t)}{y}$ ומסקנה", 2)),
    pitfalls=["לשכוח את כלל המכפלה בגזירה לפי $y$: הגורם $y$ שלפני $g$ תורם את האיבר $g(t)$.",
              "טעות סימן ב-$\\frac{\\partial t}{\\partial y}=-2y$, שמובילה לכך שאיברי $g'(t)$ אינם מצטמצמים."],
    steps=[
        num("נבחר $g(t)=t^2$ ונציב $(x,y)=(2,1)$ (כך ש-$t=3$ ו-$g'(t)=6$). מהו $\\frac{\\partial z}{\\partial x}=2xy\\,g'(t)$?", 24,
            "$2\\cdot2\\cdot1\\cdot6=24$."),
        num("באותה הצבה, מהו $\\frac{\\partial z}{\\partial y}=g(t)-2y^2g'(t)$?", -3,
            "$9-2\\cdot1\\cdot6=-3$."),
        num("באותה הצבה, מהו הערך של $\\frac1x\\frac{\\partial z}{\\partial x}+\\frac1y\\frac{\\partial z}{\\partial y}$? (הוא שווה ל-$\\frac{z}{y^2}$)", 9,
            "$\\frac{24}{2}+\\frac{-3}{1}=9$, וגם $\\frac{z}{y^2}=\\frac{1\\cdot9}{1}=9$. זו בדיקה מספרית של הזהות."),
        {"type": "findbug",
         "prompt": "בהוכחה הבאה שורה אחת שגויה. סמנו אותה.",
         "lines": ["$\\frac{\\partial z}{\\partial x}=2xy\\,g'(t)$",
                   "$\\frac{\\partial z}{\\partial y}=g(t)-2y^2g'(t)$",
                   "$\\frac1x\\cdot2xy\\,g'(t)+\\frac1y\\left(g(t)-2y^2g'(t)\\right)$",
                   "$=2y\\,g'(t)+\\frac{g(t)}{y}+2y\\,g'(t)$",
                   "$=\\frac{g(t)}{y}=\\frac{z}{y^2}$"],
         "bugIndex": 3,
         "explain": "בפתיחת הסוגריים $\\frac1y\\cdot\\left(-2y^2g'(t)\\right)=-2y\\,g'(t)$, ולא $+2y\\,g'(t)$. רק עם הסימן הנכון האיברים של $g'(t)$ מצטמצמים ונשאר $\\frac{g(t)}{y}$."},
    ])

add(4, "א",
    rubric=rub(("תיאור התחום משני האינטגרלים: תחת $y=\\sqrt{x+4}$ ותחת $y=2-x$, נפגשים ב-$(0,2)$", 4),
               ("הפיכת הגבולות: $x=y^2-4$ מהפרבולה ו-$x=2-y$ מהישר, עבור $0\\le y\\le2$", 5),
               ("הצגת אינטגרל יחיד $\\int_0^2dy\\int_{y^2-4}^{2-y}f\\,dx$", 3)),
    pitfalls=["להחליף את סדר האינטגרציה בלי לשרטט, ולהשאיר שני אינטגרלים במקום אחד. כאן הבחירה ב-$dx$ פנימי מאחדת את שני החלקים.",
              "לבלבל בין הגבול השמאלי לימני: הפרבולה $x=y^2-4$ משמאל והישר $x=2-y$ מימין."],
    steps=[
        num("באיזה גובה $y$ נפגשים הפרבולה $y=\\sqrt{x+4}$ והישר $y=2-x$ (בנקודה שבה שני החלקים נוגעים)?", 2,
            "ב-$x=0$ מתקבל $\\sqrt4=2$ ו-$2-0=2$, כלומר הנקודה $(0,2)$."),
        choice("מהו האינטגרל היחיד בסדר ההפוך ($dx$ פנימי)?",
               "$\\int_0^2dy\\int_{y^2-4}^{2-y}f(x,y)\\,dx$",
               ["$\\int_0^2dy\\int_{4-y^2}^{2-y}f(x,y)\\,dx$",
                "$\\int_0^2dy\\int_{-4}^{2-y}f(x,y)\\,dx$",
                "$\\int_0^2dy\\int_{y^2-4}^{y-2}f(x,y)\\,dx$"],
               "הגבול השמאלי נובע מ-$y=\\sqrt{x+4}\\iff x=y^2-4$, והימני מ-$y=2-x\\iff x=2-y$. הגבול $4-y^2$ הוא פרבולה אחרת, הגבול $-4$ נותן תחום גדול מדי, והגבול $y-2$ אינו הישר הנתון. בכל אחת מהחלופות השטח (עבור $f\\equiv1$) שונה מ-$\\frac{22}{3}$.", pos=0),
        num("בבדיקה עם $f\\equiv1$, מהו השטח של התחום (תשובה עשרונית, דיוק $0.001$)?", 7.3333,
            "$\\int_0^2\\left(6-y-y^2\\right)dy=\\frac{22}{3}$. זהה לשטח בסדר המקורי, $\\frac{16}{3}+2$.", tol=0.001),
    ])

add(4, "ב",
    rubric=rub(("הקביעה שהתחום סגור וחסום ו-$f$ רציפה, ולכן קיימים אקסטרמומים מוחלטים", 2),
               ("פנים התחום: הנקודה הקריטית היחידה היא הראשית, והיא קודקוד ולא פנימית", 3),
               ("הקטעים הישרים: $f=x^2$ ו-$f=\\left(4+4\\sqrt3\\right)x^2$ עולות, וערכי הקצוות", 3),
               ("הקשת: $f=1+2\\sin2\\theta$ והנקודה $\\theta=\\frac{\\pi}{4}$ עם הערך $3$", 3),
               ("השוואת הערכים: מקסימום $3$ ומינימום $0$", 2)),
    pitfalls=["לבדוק רק את הקשת ולשכוח את שני הקטעים הישרים ואת הקודקודים.",
              "לכלול נקודה קריטית שאינה בתחום: הנקודות על $y=-x$ משיטת לגראנז' נמצאות מחוץ לרביע הראשון."],
    steps=[
        num("מהו $f$ בנקודה $\\left(\\frac12,\\frac{\\sqrt3}{2}\\right)$ (קודקוד התחום, תשובה עשרונית, דיוק $0.001$)?", 2.7321,
            "$\\frac14+\\frac34+4\\cdot\\frac12\\cdot\\frac{\\sqrt3}{2}=1+\\sqrt3\\approx2.7321$.", tol=0.001),
        num("על הקשת $x=\\cos\\theta,\\ y=\\sin\\theta$ מתקבל $f=1+2\\sin2\\theta$. באיזו זווית $\\theta\\in\\left[0,\\frac{\\pi}{3}\\right]$ מתאפסת הנגזרת (תשובה עשרונית ברדיאנים, דיוק $0.001$)?", 0.7854,
            "$\\frac{df}{d\\theta}=4\\cos2\\theta=0$ ב-$2\\theta=\\frac{\\pi}{2}$, כלומר $\\theta=\\frac{\\pi}{4}\\approx0.7854$, והיא בתוך הקטע.", tol=0.001),
        num("מהו המקסימום המוחלט של $f$ בתחום?", 3,
            "הערכים בנקודות המועמדות: $0$, $1$, $1+\\sqrt3\\approx2.73$ ו-$3$ בנקודה $\\left(\\frac1{\\sqrt2},\\frac1{\\sqrt2}\\right)$. הגדול ביותר הוא $3$."),
        num("מהו המינימום המוחלט של $f$ בתחום?", 0,
            "הערך הקטן ביותר מבין הערכים המועמדים הוא $f(0,0)=0$."),
    ])

add(5, "א",
    rubric=rub(("גזירה חלקית ופתיחת המערכת $x^2+2x-2y^2=0$, $-x^2-4y+2y^2=0$", 4),
               ("פתרון המערכת: $x=2y$ והנקודות $(0,0)$ ו-$(-4,-2)$", 3),
               ("סיווג $(0,0)$ כנקודת אוכף בעזרת $D=-8<0$", 2),
               ("סיווג $(-4,-2)$ כמקסימום מקומי ($D>0$, $f_{xx}<0$) עם הערך $\\frac{8}{e^2}$", 3)),
    pitfalls=["לשכוח את הגורם $e^{x-y}$ בגזירה, או לשכוח לגזור אותו כלל השרשרת ולקבל מערכת שגויה.",
              "לסווג לפי הסימן של $f_{xx}$ בלבד, בלי לחשב את הדטרמיננטה $D=f_{xx}f_{yy}-f_{xy}^2$."],
    steps=[
        num("מהמערכת מתקבל $x=2y$, ואחרי ההצבה $2y(y+2)=0$. מהו הערך של $y$ בנקודה הקריטית שאינה הראשית?", -2,
            "$y=0$ נותן את הראשית, ו-$y=-2$ נותן $x=2y=-4$, כלומר הנקודה $(-4,-2)$."),
        num("מהי הדטרמיננטה $D=f_{xx}f_{yy}-f_{xy}^2$ בנקודה $(0,0)$?", -8,
            "$f_{xx}(0,0)=2$, $f_{yy}(0,0)=-4$, $f_{xy}(0,0)=0$, ולכן $D=-8$."),
        choice("מהו סוג הנקודה הקריטית $(0,0)$?",
               "נקודת אוכף",
               ["מינימום מקומי", "מקסימום מקומי", "אי אפשר להכריע בעזרת מבחן הנגזרות השניות"],
               "$D=-8<0$, ולכן הנקודה אוכף. הסימן של $f_{xx}=2$ לבדו היה מטעה ומרמז על מינימום.", pos=2),
        num("מהו $f_{xx}(-4,-2)$ (תשובה עשרונית, דיוק $0.001$)?", -0.812,
            "$f_{xx}=\\left(x^2+4x+2-2y^2\\right)e^{x-y}=(16-16+2-8)e^{-2}=-6e^{-2}\\approx-0.812$. יחד עם $D=8e^{-4}>0$ זהו מקסימום מקומי.", tol=0.001),
        num("מהו ערך הפונקציה במקסימום המקומי, $f(-4,-2)$ (תשובה עשרונית, דיוק $0.001$)?", 1.0827,
            "$(16-8)e^{-2}=\\frac{8}{e^2}\\approx1.083$.", tol=0.001),
    ])

add(5, "ב",
    rubric=rub(("פירוק לשברים חלקיים $\\frac13\\left(\\frac1{x-1}-\\frac1{x+2}\\right)$", 3),
               ("פיתוח כל שבר לטור הנדסי", 3),
               ("איחוד לטור יחיד $-\\frac13\\sum\\left(1+\\frac{(-1)^n}{2^{n+1}}\\right)x^n$", 2),
               ("תחום ההתכנסות $(-1,1)$ עם נימוק לקצוות", 3),
               ("$f^{(10)}(0)=10!\\cdot c_{10}=-1210190.625$", 2)),
    pitfalls=["לקבוע תחום התכנסות $|x|<2$ לפי השבר השני בלבד. הטור הכולל מתכנס רק כששני הטורים מתכנסים, כלומר ב-$|x|<1$.",
              "לשכוח את הגורם $n!$ במעבר ממקדם הטור לנגזרת: $f^{(n)}(0)=n!\\,c_n$."],
    steps=[
        num("מהו $f(0)$, שהוא גם המקדם $c_0$ בטור? (תשובה עשרונית)", -0.5,
            "$\\frac{1}{0+0-2}=-\\frac12$, ובנוסחה $-\\frac13\\left(1+\\frac12\\right)=-\\frac12$."),
        num("מהו המקדם $c_1$ של $x$ בטור? (תשובה עשרונית)", -0.25,
            "$c_1=-\\frac13\\left(1-\\frac14\\right)=-\\frac14$."),
        choice("מהו תחום ההתכנסות של הטור?",
               "$(-1,1)$",
               ["$(-2,2)$", "$[-1,1]$", "$(-2,1)$"],
               "הטור של $\\frac1{x-1}$ מתכנס רק ב-$|x|<1$ והטור של $\\frac1{x+2}$ ב-$|x|<2$, ולכן הסכום מתכנס ב-$|x|<1$. בקצוות $x=\\pm1$ האיבר הכללי אינו שואף ל-$0$.", pos=1),
        num("מהו $f^{(10)}(0)$ (דיוק $0.001$)?", -1210190.625,
            "$f^{(10)}(0)=10!\\,c_{10}=-\\frac{10!}{3}\\left(1+\\frac1{2^{11}}\\right)=-\\frac{9681525}{8}=-1210190.625$.", tol=0.001),
    ])

exam = {
    "examCode": "23A-C",
    "examLabel": "מבחן סוף סמסטר א' תשפ\"ג, מועד ג'",
    "year": 2023,
    "examDate": "27/04/2023",
    "sourceFile": "calculus-2/23A-C exam 27.4.23.pdf",
    "solutionFile": "none (no key exists for this sitting; solved, pending refuter)",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
