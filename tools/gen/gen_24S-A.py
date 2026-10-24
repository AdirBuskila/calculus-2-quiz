# -*- coding: utf-8 -*-
"""Generator for tools/raw/24S-A.json -- calculus-2 (20252), summer moed 2024 (03/11/2024).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24S-A.py

Source: sitting 24S-A (orchestrator's code for exam 3.11.24). Exam: 3 pages, 5 questions of 25 points
(a=12, b=13), solve 4 of 5. NO answer key exists for this sitting (GATE1: the solver writes the solution and
the refuter checks it). Exam header (lecturer and TA names) is not transcribed.

Transcription notes
- The text layers are garbled; everything is transcribed from page renders (tools/raw/24S-A-SRC/).
- Q1a is printed "f(x,y,) = y cos(xy)" (stray comma); transcribed as f(x,y).
- Q2a: parts 1 (3 pts, continuity) and 2 (9 pts, partials and differentiability) are one item (12 pts).
- Q2b: the two series are one item (6 + 7 pts).
- Q3: the page break leaves a stray "ב." label at the bottom of page 2, and the extremum question is printed
  as "1." (13 pts). It is the second part of Q3 and is transcribed as Q3b (solver re-checked against page 2).
- Q5a: the two sub-questions (6 + 6 pts) are one item.

Solutions: written by the solver (solutionSource "solved", official False), pending the blind refuter.
Every computation is verified in tools/verify/24S-A/solve_24S-A.py (sympy + numeric: unit-direction solve,
polar limit and difference quotients, comparison/limit-comparison and Leibniz conditions, radius and endpoints,
triangle edges + dense grid, implicit derivatives + root-finding, Hessians + local grids).
tools/verify/24S-A/check.py holds the transcriber's earlier workings (hints only; they agree).
Contour data for Q3b and Q5b: tools/verify/24S-A/contours.json (values asserted by solve_24S-A.py).
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24S-A.json"


def Q(num, kind, topic, question, solution, part, points):
    return {"num": num, "part": part, "kind": kind, "topic": topic, "points": points, "question": question,
            "solution": solution.strip("\n"), "solutionSource": "solved", "official": False, "confidence": "high"}


questions = []

# ===== Q1a =====
questions.append(Q(1, "computation", "gradient_directional", r"""באיזה כיוון הנגזרת הכיוונית של הפונקציה $f(x,y)=y\cdot\cos(xy)$ בנקודה $(1,0)$ שווה ל-1.""",
r"""הפונקציה גזירה ברציפות בכל המישור, ולכן הנגזרת הכיוונית בכיוון וקטור יחידה $\vec u=(a,b)$ היא $D_{\vec u}f=\nabla f\cdot\vec u$.
$$f'_x=-y^2\sin(xy),\qquad f'_y=\cos(xy)-xy\sin(xy)$$
$$\nabla f(1,0)=\left(0,\ \cos0-0\right)=(0,1)$$
לכן
$$D_{\vec u}f(1,0)=0\cdot a+1\cdot b=b.$$
נדרוש $b=1$ יחד עם $a^2+b^2=1$, ומכאן $a=0$.
הכיוון היחיד הוא $\vec u=(0,1)$, כלומר בכיוון החיובי של ציר $y$ (זה גם כיוון הגרדיאנט, ו-$1=|\nabla f(1,0)|$ הוא הערך המקסימלי של הנגזרת הכיוונית).""", "א", 12))

# ===== Q1b =====
questions.append(Q(1, "proof", "partials_differentiability", r"""הוכיחו כי עבור הפונקציה הבאה:
$$z(x,y)=e^{x-y}\cdot\sin(x+y)$$
לכל $(x,y)$ בתחום הגדרתה, מתקיים: $z''_{xx}(x,y)+z''_{yy}(x,y)=0$""",
r"""הפונקציה מוגדרת וגזירה כמה פעמים שרוצים בכל המישור.
**לפי $x$:**
$$z'_x=e^{x-y}\sin(x+y)+e^{x-y}\cos(x+y)=e^{x-y}\left(\sin(x+y)+\cos(x+y)\right)$$
$$z''_{xx}=e^{x-y}\left(\sin(x+y)+\cos(x+y)\right)+e^{x-y}\left(\cos(x+y)-\sin(x+y)\right)=2e^{x-y}\cos(x+y)$$
**לפי $y$:** (הנגזרת של $e^{x-y}$ לפי $y$ היא $-e^{x-y}$)
$$z'_y=-e^{x-y}\sin(x+y)+e^{x-y}\cos(x+y)=e^{x-y}\left(\cos(x+y)-\sin(x+y)\right)$$
$$z''_{yy}=-e^{x-y}\left(\cos(x+y)-\sin(x+y)\right)+e^{x-y}\left(-\sin(x+y)-\cos(x+y)\right)=-2e^{x-y}\cos(x+y)$$
**סיכום:**
$$z''_{xx}+z''_{yy}=2e^{x-y}\cos(x+y)-2e^{x-y}\cos(x+y)=0$$
לכל $(x,y)$ במישור, כנדרש.""", "ב", 13))

# ===== Q2a =====
questions.append(Q(2, "computation", "partials_differentiability", r"""נתונה הפונקציה
$$f(x,y)=\begin{cases}\dfrac{xy^3}{x^2+y^2}, & (x,y)\neq(0,0)\\[2mm] 0, & (x,y)=(0,0)\end{cases}$$
1. (3 נקודות) האם הפונקציה רציפה בנקודה $(0,0)$?
2. (9 נקודות) האם $f'_x(0,0)$ ו-$f'_y(0,0)$ קיימים? אם כן חשבו אותם.
האם הפונקציה דיפרנציאבילית בנקודה $(0,0)$?""",
r"""**1. רציפות.** נעבור לקואורדינטות קוטביות $x=r\cos\varphi,\ y=r\sin\varphi$:
$$f=\frac{r\cos\varphi\cdot r^3\sin^3\varphi}{r^2}=r^2\cos\varphi\sin^3\varphi$$
$$|f(x,y)-0|\le r^2\xrightarrow[r\to0]{}0$$
החסם אינו תלוי ב-$\varphi$, ולכן $\lim_{(x,y)\to(0,0)}f(x,y)=0=f(0,0)$ והפונקציה **רציפה** ב-$(0,0)$.

**2. נגזרות חלקיות.** לפי ההגדרה, ומכיוון ש-$f(h,0)=0$ ו-$f(0,h)=0$:
$$f'_x(0,0)=\lim_{h\to0}\frac{f(h,0)-f(0,0)}{h}=\lim_{h\to0}\frac{0}{h}=0$$
$$f'_y(0,0)=\lim_{h\to0}\frac{f(0,h)-f(0,0)}{h}=\lim_{h\to0}\frac{0}{h}=0$$
שתיהן קיימות ושוות ל-0.

**דיפרנציאביליות.** צריך לבדוק ש
$$\lim_{(x,y)\to(0,0)}\frac{f(x,y)-f(0,0)-f'_x(0,0)x-f'_y(0,0)y}{\sqrt{x^2+y^2}}=\lim_{(x,y)\to(0,0)}\frac{f(x,y)}{\sqrt{x^2+y^2}}=0.$$
בקוטביות:
$$\left|\frac{f(x,y)}{\sqrt{x^2+y^2}}\right|=\frac{r^2|\cos\varphi\sin^3\varphi|}{r}\le r\xrightarrow[r\to0]{}0$$
הגבול שווה ל-0, ולכן הפונקציה **דיפרנציאבילית** ב-$(0,0)$.""", "א", 12))

# ===== Q2b =====
questions.append(Q(2, "computation", "numeric_series", r"""קבעו לגבי כל אחד מהטורים הבאים אם הוא מתכנס בהחלט, מתכנס בתנאי או מתבדר, נמקו!
1. (6 נקודות) $\displaystyle\sum_{n=1}^{\infty}\frac{\cos(n)}{\sqrt[4]{n^5+2}}$
2. (7 נקודות) $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^n}{\sqrt{n\cdot(n+1)}}$""",
r"""**1.** נבדוק את טור הערכים המוחלטים. מכיוון ש-$|\cos n|\le1$ ו-$n^5+2>n^5$:
$$\left|\frac{\cos n}{\sqrt[4]{n^5+2}}\right|\le\frac{1}{\sqrt[4]{n^5}}=\frac{1}{n^{5/4}}$$
הטור $\sum\frac{1}{n^{5/4}}$ מתכנס (טור $p$ עם $p=\frac54>1$), ולכן לפי מבחן ההשוואה $\sum\left|\frac{\cos n}{\sqrt[4]{n^5+2}}\right|$ מתכנס.
הטור **מתכנס בהחלט**.

**2.** נסמן $b_n=\dfrac{1}{\sqrt{n(n+1)}}>0$.
*התכנסות בהחלט:* $\sum|(-1)^nb_n|=\sum b_n$. לפי מבחן ההשוואה הגבולי עם $\frac1n$:
$$\lim_{n\to\infty}\frac{b_n}{1/n}=\lim_{n\to\infty}\frac{n}{\sqrt{n^2+n}}=\lim_{n\to\infty}\frac{1}{\sqrt{1+\frac1n}}=1$$
הגבול סופי וחיובי ו-$\sum\frac1n$ מתבדר, לכן $\sum b_n$ מתבדר: הטור **אינו** מתכנס בהחלט.
*לייבניץ:* $n(n+1)$ עולה ממש, ולכן $b_n$ יורדת מונוטונית, ו-$b_n\to0$. לפי משפט לייבניץ הטור $\sum(-1)^nb_n$ מתכנס.
הטור **מתכנס בתנאי**.""", "ב", 13))

# ===== Q3a =====
questions.append(Q(3, "computation", "power_series", r"""מצאו את תחום ההתכנסות של הטור $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot4^n}(x-2)^n$.""",
r"""זה טור חזקות סביב $x_0=2$ עם $a_n=\dfrac{1}{n\cdot4^n}$.
**רדיוס:**
$$R=\lim_{n\to\infty}\left|\frac{a_n}{a_{n+1}}\right|=\lim_{n\to\infty}\frac{(n+1)4^{n+1}}{n\cdot4^n}=\lim_{n\to\infty}4\cdot\frac{n+1}{n}=4$$
לכן הטור מתכנס (בהחלט) עבור $|x-2|<4$, כלומר $-2<x<6$, ומתבדר עבור $|x-2|>4$.
**קצוות:**
* $x=6$: $(x-2)^n=4^n$ והטור הוא $\sum_{n=1}^{\infty}\frac{1}{n}$, הטור ההרמוני, **מתבדר**.
* $x=-2$: $(x-2)^n=(-4)^n$ והטור הוא $\sum_{n=1}^{\infty}\frac{(-1)^n}{n}$. האיברים $\frac1n$ יורדים מונוטונית ל-0, ולכן לפי לייבניץ הוא **מתכנס** (בתנאי).

תחום ההתכנסות: $[-2,6)$.""", "א", 12))

# ===== Q3b =====
questions.append(Q(3, "computation", "absolute_extrema", r"""נתונה הפונקציה:
$$f(x,y)=2x^2-3y^2+xy-3x+8y$$
מצאו את נקודות המקסימום והמינימום המוחלטים של הפונקציה בתחום $D$ כאשר $D$ הוא משולש שקודקודיו $A(0,0),B(0,1),C(1,1)$""",
r"""$D$ הוא המשולש הסגור $0\le x\le y\le1$ (צלעות: $AB$ על $x=0$, $BC$ על $y=1$, $AC$ על $y=x$). $f$ רציפה ו-$D$ סגור וחסום, ולכן יש מקסימום ומינימום מוחלטים.

**נקודות קריטיות בפנים:**
$$\begin{cases}f'_x=4x+y-3=0\\ f'_y=-6y+x+8=0\end{cases}\ \Rightarrow\ x=6y-8,\quad 4(6y-8)+y=3\ \Rightarrow\ y=\frac75,\ x=\frac25$$
הנקודה $\left(\frac25,\frac75\right)$ אינה ב-$D$ (כי $y>1$), ולכן אין נקודות חשודות בפנים.

**השפה:**
* $AB$: $x=0,\ 0\le y\le1$: $g(y)=-3y^2+8y$, $g'(y)=-6y+8=0\Rightarrow y=\frac43\notin[0,1]$. נשארים הקודקודים.
* $BC$: $y=1,\ 0\le x\le1$: $g(x)=2x^2-2x+5$, $g'(x)=4x-2=0\Rightarrow x=\frac12$, $f\left(\frac12,1\right)=\frac92$.
* $AC$: $y=x,\ 0\le x\le1$: $g(x)=2x^2-3x^2+x^2-3x+8x=5x$, עולה ממש, ללא נקודות קריטיות פנימיות.

**קודקודים:**
$$f(A)=f(0,0)=0,\qquad f(B)=f(0,1)=5,\qquad f(C)=f(1,1)=2-3+1-3+8=5$$
**השוואה** בין $0,\ 5,\ 5,\ \frac92$:
* מקסימום מוחלט $5$, המתקבל בשתי נקודות: $B(0,1)$ ו-$C(1,1)$.
* מינימום מוחלט $0$, המתקבל ב-$A(0,0)$.""", "ב", 13))

# ===== Q4a =====
questions.append(Q(4, "computation", "chain_rule_identity", r"""תהי $f(x,y)$ פונקציה דיפרנציאבילית בכל המישור כך שלכל $t$ ממשי מתקיים $f(2t+1,e^t)=3$.
כמו כן, מתקיים כי $f'_x(2t+1,e^t)=\dfrac{e^t}{2}$. חשבו את $f'_y(2t+1,e^t)$""",
r"""נסמן $x(t)=2t+1,\ y(t)=e^t$ ו-$g(t)=f(x(t),y(t))$. נתון $g(t)=3$ לכל $t$, ולכן $g'(t)=0$.
$f$ דיפרנציאבילית, ולכן לפי כלל השרשרת:
$$g'(t)=f'_x(x(t),y(t))\cdot x'(t)+f'_y(x(t),y(t))\cdot y'(t)=2f'_x(2t+1,e^t)+e^tf'_y(2t+1,e^t)$$
נציב את הנתון $f'_x(2t+1,e^t)=\dfrac{e^t}{2}$:
$$0=2\cdot\frac{e^t}{2}+e^tf'_y(2t+1,e^t)=e^t\left(1+f'_y(2t+1,e^t)\right)$$
מכיוון ש-$e^t\ne0$:
$$f'_y(2t+1,e^t)=-1$$""", "א", 12))

# ===== Q4b =====
questions.append(Q(4, "computation", "gradient_directional", r"""כתבו את משוואת המישור המשיק למשטח $f(x,y)=\ln\left(x+\dfrac1y\right)$ בכל הנקודות $(x,y)$ בהם $\nabla f(x,y)=\vec i-\dfrac{16}{9}\vec j$""",
r"""תחום ההגדרה: $y\ne0$ ו-$x+\frac1y>0$.
$$f'_x=\frac{1}{x+\frac1y},\qquad f'_y=\frac{-\frac{1}{y^2}}{x+\frac1y}$$
**מציאת הנקודות:**
$f'_x=1$ נותן $x+\frac1y=1$. אז $f'_y=-\frac{1}{y^2}$, ו-$-\frac{1}{y^2}=-\frac{16}{9}$ נותן $y^2=\frac{9}{16}$, כלומר $y=\pm\frac34$.
* $y=\frac34$: $x=1-\frac43=-\frac13$. הנקודה $\left(-\frac13,\frac34\right)$.
* $y=-\frac34$: $x=1+\frac43=\frac73$. הנקודה $\left(\frac73,-\frac34\right)$.
בשתיהן $x+\frac1y=1>0$, ולכן הן בתחום, ו-$f=\ln1=0$.

**מישור משיק:** $z=f(x_0,y_0)+f'_x(x_0,y_0)(x-x_0)+f'_y(x_0,y_0)(y-y_0)$.
* בנקודה $\left(-\frac13,\frac34,0\right)$:
$$z=\left(x+\frac13\right)-\frac{16}{9}\left(y-\frac34\right)=x-\frac{16}{9}y+\frac53$$
* בנקודה $\left(\frac73,-\frac34,0\right)$:
$$z=\left(x-\frac73\right)-\frac{16}{9}\left(y+\frac34\right)=x-\frac{16}{9}y-\frac{11}{3}$$
(ובכתיב שלם: $9x-16y-9z+15=0$ ו-$9x-16y-9z-33=0$.)""", "ב", 13))

# ===== Q5a =====
questions.append(Q(5, "computation", "implicit_function", r"""נתונה המשוואה: $5z^3+3xyz-x^2\cdot y^2+1=0$
1. (6 נקודות) הראו כי המשוואה מגדירה בסביבת הנקודה $(1,-1,0)$ פונקציה יחידה $z=z(x,y)$.
2. (6 נקודות) חשבו את ערך הביטוי $z_x(1,-1)+z_y(1,-1)$""",
r"""נסמן $F(x,y,z)=5z^3+3xyz-x^2y^2+1$.
**1.** נבדוק את תנאי משפט הפונקציה הסתומה:
* $F(1,-1,0)=0+0-1+1=0$, כלומר הנקודה מקיימת את המשוואה.
* $F$ פולינום, ולכן $F$ ונגזרותיה החלקיות רציפות בכל מקום.
* $F'_z=15z^2+3xy$, ו-$F'_z(1,-1,0)=0-3=-3\ne0$.
לפי משפט הפונקציה הסתומה, בסביבת $(1,-1)$ קיימת פונקציה יחידה $z=z(x,y)$, גזירה ברציפות, עם $z(1,-1)=0$, המקיימת את המשוואה.

**2.**
$$F'_x=3yz-2xy^2\ \Rightarrow\ F'_x(1,-1,0)=0-2=-2$$
$$F'_y=3xz-2x^2y\ \Rightarrow\ F'_y(1,-1,0)=0+2=2$$
$$z_x(1,-1)=-\frac{F'_x}{F'_z}=-\frac{-2}{-3}=-\frac23,\qquad z_y(1,-1)=-\frac{F'_y}{F'_z}=-\frac{2}{-3}=\frac23$$
$$z_x(1,-1)+z_y(1,-1)=-\frac23+\frac23=0$$""", "א", 12))

# ===== Q5b =====
questions.append(Q(5, "computation", "local_extrema", r"""מצאו וסווגו את נקודות האקסטרמום של הפונקציה
$$f(x,y)=xy(6-x-y)$$""",
r"""$f(x,y)=6xy-x^2y-xy^2$.
**נקודות קריטיות:**
$$\begin{cases}f'_x=6y-2xy-y^2=y(6-2x-y)=0\\ f'_y=6x-x^2-2xy=x(6-x-2y)=0\end{cases}$$
* $y=0,\ x=0$: $(0,0)$.
* $y=0,\ 6-x-2y=0$: $(6,0)$.
* $6-2x-y=0,\ x=0$: $(0,6)$.
* $6-2x-y=0,\ 6-x-2y=0$: מחיסור $x=y$, ואז $6-3x=0$: $(2,2)$.

**נגזרות שניות:**
$$f''_{xx}=-2y,\qquad f''_{yy}=-2x,\qquad f''_{xy}=6-2x-2y,\qquad D=f''_{xx}f''_{yy}-\left(f''_{xy}\right)^2$$
* $(0,0)$: $D=0\cdot0-6^2=-36<0$, נקודת אוכף.
* $(6,0)$: $D=0\cdot(-12)-(-6)^2=-36<0$, נקודת אוכף.
* $(0,6)$: $D=(-12)\cdot0-(-6)^2=-36<0$, נקודת אוכף.
* $(2,2)$: $D=(-4)(-4)-(-2)^2=12>0$ ו-$f''_{xx}=-4<0$, **מקסימום מקומי**, $f(2,2)=2\cdot2\cdot2=8$.

סיכום: נקודת האקסטרמום היחידה היא מקסימום מקומי ב-$(2,2)$ עם ערך $8$. שלוש הנקודות האחרות הן נקודות אוכף.""", "ב", 13))

# ---- rubric / pitfalls / steps (ai-verified). Every expected value is re-computed in tools/verify/24S-A/steps_24S-A.py ----
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


def findbug(prompt, lines, bug, explain):
    return {"type": "findbug", "prompt": prompt, "lines": lines, "bugIndex": bug, "explain": explain}


def add(n, part, **kw):
    for q in questions:
        if q["num"] == n and q.get("part") == part:
            q.update(kw)
            q["rubricSource"] = "ai-verified"
            q["stepsSource"] = "ai-verified"
            return
    raise KeyError((n, part))


add(1, "א",
    rubric=rub((r"חישוב הנגזרות החלקיות $f'_x$ ו-$f'_y$", 4),
               (r"הצבה ב-$(1,0)$ וקבלת $\nabla f(1,0)=(0,1)$", 3),
               (r"שימוש ב-$D_{\vec u}f=\nabla f\cdot\vec u$ יחד עם התנאי $a^2+b^2=1$", 3),
               (r"מסקנה: הכיוון היחיד הוא $\vec u=(0,1)$", 2)),
    pitfalls=[r"לשכוח את הגורם הפנימי בנגזרת של $\cos(xy)$ (כלל השרשרת), ולקבל $f'_y$ שגוי.",
              r"לדרוש רק $D_{\vec u}f=1$ ולשכוח שהווקטור $\vec u$ חייב להיות וקטור יחידה."],
    steps=[
        num(r"חשבו את $f'_x(1,0)$ עבור $f(x,y)=y\cos(xy)$.", 0,
            r"$f'_x=-y^2\sin(xy)$, ולכן $f'_x(1,0)=0$."),
        num(r"חשבו את $f'_y(1,0)$.", 1,
            r"$f'_y=\cos(xy)-xy\sin(xy)$, ולכן $f'_y(1,0)=\cos0-0=1$."),
        choice(r"איזה וקטור יחידה $\vec u$ נותן $D_{\vec u}f(1,0)=1$?",
               r"$(0,1)$",
               [r"$(1,0)$", r"$(0,-1)$", r"$\left(\frac1{\sqrt2},\frac1{\sqrt2}\right)$"],
               r"$\nabla f(1,0)=(0,1)$, ולכן עבור $\vec u=(a,b)$ מתקבל $D_{\vec u}f=b$. הכיוון $(1,0)$ נותן $0$, הכיוון $(0,-1)$ נותן $-1$ והכיוון האלכסוני נותן $\frac1{\sqrt2}$. רק $(0,1)$ נותן $1$.", pos=2),
    ])

add(1, "ב",
    rubric=rub((r"חישוב $z'_x$ בכלל המכפלה", 2),
               (r"חישוב $z''_{xx}=2e^{x-y}\cos(x+y)$", 3),
               (r"חישוב $z'_y$ בתשומת לב לנגזרת $-e^{x-y}$ של הגורם המעריכי לפי $y$", 3),
               (r"חישוב $z''_{yy}=-2e^{x-y}\cos(x+y)$", 3),
               (r"סכימה וקבלת $z''_{xx}+z''_{yy}=0$ לכל $(x,y)$", 2)),
    pitfalls=[r"לשכוח שהנגזרת של $e^{x-y}$ לפי $y$ היא $-e^{x-y}$, וכך לקבל $z''_{yy}=+2e^{x-y}\cos(x+y)$ במקום סימן מינוס, והסכום לא מתאפס.",
              r"להציב נקודה מסוימת בלבד. נדרש להוכיח את השוויון לכל $(x,y)$, ולכן הנגזרות מחושבות כביטויים כלליים."],
    steps=[
        num(r"חשבו את $z''_{xx}(0,0)$ עבור $z=e^{x-y}\sin(x+y)$.", 2,
            r"$z''_{xx}=2e^{x-y}\cos(x+y)$, ולכן בנקודה $(0,0)$ הערך הוא $2$."),
        num(r"חשבו את $z''_{yy}(0,0)$.", -2,
            r"$z''_{yy}=-2e^{x-y}\cos(x+y)$, ולכן בנקודה $(0,0)$ הערך הוא $-2$."),
        findbug("בגרסה הבאה של ההוכחה שורה אחת שגויה. מצאו אותה.",
                [r"$z'_x=e^{x-y}\left(\sin(x+y)+\cos(x+y)\right)$",
                 r"$z''_{xx}=2e^{x-y}\cos(x+y)$",
                 r"$z'_y=e^{x-y}\left(\cos(x+y)-\sin(x+y)\right)$",
                 r"$z''_{yy}=2e^{x-y}\cos(x+y)$",
                 r"$z''_{xx}+z''_{yy}=0$"],
                3,
                r"בנגזרת לפי $y$ הגורם $e^{x-y}$ משאיר סימן מינוס: $z''_{yy}=-2e^{x-y}\cos(x+y)$. עם הסימן השגוי הסכום היה $4e^{x-y}\cos(x+y)$ ולא $0$."),
    ])

add(2, "א",
    rubric=rub((r"מעבר לקואורדינטות קוטביות וקבלת $f=r^2\cos\varphi\sin^3\varphi$, חסם על ידי $r^2$ ומסקנה שהפונקציה רציפה ב-$(0,0)$", 3),
               (r"חישוב $f'_x(0,0)=0$ ו-$f'_y(0,0)=0$ מההגדרה, כי $f(h,0)=f(0,h)=0$", 3),
               (r"ניסוח תנאי הדיפרנציאביליות: הגבול של $\frac{f(x,y)}{\sqrt{x^2+y^2}}$ צריך להיות $0$", 3),
               (r"חסם $r$ על המנה בקואורדינטות קוטביות ומסקנה שהפונקציה דיפרנציאבילית", 3)),
    pitfalls=[r"לבדוק רציפות רק לאורך הצירים או ישרים. החסם צריך להיות בלתי תלוי בזווית $\varphi$, ולכן עוברים לקואורדינטות קוטביות.",
              r"להסיק דיפרנציאביליות מעצם קיום הנגזרות החלקיות או מהרציפות. צריך לבדוק את הגבול של $\frac{f(x,y)-f(0,0)-f'_x x-f'_y y}{\sqrt{x^2+y^2}}$."],
    steps=[
        num(r"אחרי ההצבה $x=r\cos\varphi,\ y=r\sin\varphi$ הפונקציה שווה ל-$r^k\cos\varphi\sin^3\varphi$ בכל נקודה שונה מהראשית. מהו $k$?", 2,
            r"המונה הוא $r^4\cos\varphi\sin^3\varphi$ והמכנה $r^2$, ולכן $k=2$. מכיוון ש-$\left|\cos\varphi\sin^3\varphi\right|\le1$, מתקבל $|f|\le r^2\to0$ והפונקציה רציפה."),
        num(r"חשבו את $f'_x(0,0)$ מההגדרה.", 0,
            r"$f(h,0)=0$ לכל $h$, ולכן המנה $\frac{f(h,0)-f(0,0)}{h}$ שווה ל-$0$ והגבול הוא $0$. באותו אופן $f'_y(0,0)=0$."),
        num(r"בבדיקת הדיפרנציאביליות מחלקים את $f$ ב-$\sqrt{x^2+y^2}=r$. נקבל ביטוי שחסום בערכו המוחלט על ידי $r^m$. מהו $m$?", 1,
            r"$\frac{f}{r}=r\cos\varphi\sin^3\varphi$, ולכן $\left|\frac fr\right|\le r$."),
        choice(r"האם $f$ דיפרנציאבילית ב-$(0,0)$?",
               r"כן, כי $\frac{f(x,y)}{\sqrt{x^2+y^2}}\to0$",
               [r"לא, כי הגבול של $\frac{f(x,y)}{\sqrt{x^2+y^2}}$ תלוי בזווית $\varphi$",
                r"לא, כי המכנה $x^2+y^2$ מתאפס בראשית",
                r"אי אפשר לדעת, כי לא ידוע אם הפונקציה רציפה"],
               r"הנגזרות החלקיות הן $0$, ולכן הפונקציה דיפרנציאבילית בדיוק כאשר $\frac{f}{\sqrt{x^2+y^2}}\to0$. החסם $r$ אינו תלוי בזווית, והפונקציה אכן רציפה כפי שנבדק קודם.", pos=1),
    ])

add(2, "ב",
    rubric=rub((r"הסדרה $\frac{\cos n}{\sqrt[4]{n^5+2}}$: חסם $\frac1{n^{5/4}}$ באמצעות $|\cos n|\le1$ ו-$n^5+2>n^5$", 3),
               (r"הטור $\sum\frac1{n^{5/4}}$ מתכנס ($p=\frac54>1$), ולכן הטור עם $\cos n$ מתכנס בהחלט לפי מבחן ההשוואה", 3),
               (r"הטור $\sum\frac{(-1)^n}{\sqrt{n(n+1)}}$: השוואה גבולית עם $\sum\frac1n$ (הגבול $1$), ולכן אין התכנסות בהחלט", 3),
               (r"מבחן לייבניץ: $b_n$ יורדת ושואפת ל-$0$, ולכן הטור מתכנס", 3),
               (r"מסקנה: הטור עם $(-1)^n$ מתכנס בתנאי", 1)),
    pitfalls=[r"להסיק שהטור $\sum\frac{\cos n}{\sqrt[4]{n^5+2}}$ מתכנס רק בתנאי בגלל הסימנים המשתנים של $\cos n$. כאן כבר טור הערכים המוחלטים מתכנס, ולכן ההתכנסות בהחלט.",
              r"לעצור אחרי מבחן לייבניץ ולהכריז על התכנסות בתנאי בלי לבדוק שטור הערכים המוחלטים אכן מתבדר.",
              r"להשוות את $\sqrt{n(n+1)}$ ל-$n^2$ ולהסיק התכנסות. הסדר הנכון הוא $\sqrt{n(n+1)}\approx n$."],
    steps=[
        num(r"בטור $\sum\frac{\cos n}{\sqrt[4]{n^5+2}}$ חוסמים את הערך המוחלט של האיבר על ידי $\frac1{n^p}$. מהו $p$ (תשובה עשרונית)?", 1.25,
            r"$\sqrt[4]{n^5+2}>\sqrt[4]{n^5}=n^{5/4}$ ו-$|\cos n|\le1$, ולכן $p=\frac54=1.25>1$ וטור ה-$p$ מתכנס."),
        choice(r"מה מסקנת הפתרון לגבי $\sum\frac{\cos n}{\sqrt[4]{n^5+2}}$?",
               r"מתכנס בהחלט",
               [r"מתכנס בתנאי בלבד", r"מתבדר", r"אי אפשר להכריע, כי $\cos n$ אינו מונוטוני"],
               r"טור הערכים המוחלטים חסום על ידי טור ה-$p$ המתכנס $\sum\frac1{n^{5/4}}$, ולכן הטור מתכנס בהחלט, בלי צורך במונוטוניות.", pos=0),
        num(r"בטור $\sum\frac{(-1)^n}{\sqrt{n(n+1)}}$ משווים את $b_n=\frac1{\sqrt{n(n+1)}}$ ל-$\frac1n$. מהו $\lim\frac{b_n}{1/n}$?", 1,
            r"$\frac{n}{\sqrt{n^2+n}}=\frac1{\sqrt{1+\frac1n}}\to1$. הגבול חיובי וסופי, ו-$\sum\frac1n$ מתבדר, ולכן $\sum b_n$ מתבדר."),
        choice(r"מה מסקנת הפתרון לגבי $\sum\frac{(-1)^n}{\sqrt{n(n+1)}}$?",
               r"מתכנס בתנאי",
               [r"מתכנס בהחלט", r"מתבדר", r"מתכנס בהחלט, כי $b_n\to0$"],
               r"$b_n$ יורדת ושואפת ל-$0$, ולכן הטור מתכנס לפי לייבניץ. אבל $\sum b_n$ מתבדר (השוואה גבולית עם $\sum\frac1n$), ולכן ההתכנסות היא בתנאי בלבד.", pos=1),
    ])

add(3, "א",
    rubric=rub((r"חישוב רדיוס ההתכנסות $R=4$ ופירוט התחום הפתוח $-2<x<6$", 4),
               (r"קצה $x=6$: מתקבל הטור ההרמוני $\sum\frac1n$ ולכן מתבדר", 3),
               (r"קצה $x=-2$: מתקבל $\sum\frac{(-1)^n}{n}$ ולכן מתכנס לפי לייבניץ", 3),
               (r"כתיבת תחום ההתכנסות $[-2,6)$", 2)),
    pitfalls=[r"לשכוח לבדוק את הקצוות ולהסתפק בקטע הפתוח.",
              r"לחשב את הרדיוס בלבד ולשכוח שהמרכז הוא $x_0=2$, ולכן התחום הוא סביב $2$ ולא סביב $0$."],
    steps=[
        num(r"מהו רדיוס ההתכנסות של $\sum_{n=1}^{\infty}\frac{1}{n\cdot4^n}(x-2)^n$?", 4,
            r"$\left|\frac{a_n}{a_{n+1}}\right|=\frac{(n+1)4^{n+1}}{n4^n}=4\cdot\frac{n+1}{n}\to4$."),
        choice(r"איזה טור מתקבל בקצה הימני $x=6$ ומה דינו?",
               r"$\sum\frac1n$, מתבדר",
               [r"$\sum\frac{(-1)^n}{n}$, מתכנס", r"$\sum\frac1{n^2}$, מתכנס", r"$\sum\frac{4^n}{n}$, מתכנס"],
               r"$(x-2)^n=4^n$, ולכן האיבר הוא $\frac{4^n}{n4^n}=\frac1n$, הטור ההרמוני, והוא מתבדר.", pos=2),
        choice(r"מהו תחום ההתכנסות של הטור?",
               r"$[-2,6)$",
               [r"$(-2,6)$", r"$[-2,6]$", r"$(-2,6]$"],
               r"בקצה $x=6$ הטור מתבדר, ובקצה $x=-2$ מתקבל $\sum\frac{(-1)^n}{n}$ שמתכנס לפי לייבניץ. לכן הקצה השמאלי כלול והימני לא.", pos=0),
    ])

add(3, "ב",
    rubric=rub((r"מציאת הנקודה הקריטית $\left(\frac25,\frac75\right)$ וקביעה שהיא מחוץ ל-$D$", 3),
               (r"בדיקת שלוש הצלעות: $g(y)$ על $AB$, $g(x)$ על $BC$ ונקודה קריטית $x=\frac12$, $g(x)=5x$ על $AC$", 5),
               (r"חישוב הערכים בקודקודים $0,5,5$ ובנקודה $\left(\frac12,1\right)$", 2),
               (r"השוואה: מקסימום מוחלט $5$ ב-$B$ וב-$C$, מינימום מוחלט $0$ ב-$A$", 3)),
    pitfalls=[r"לשכוח לבדוק שהנקודה הקריטית נמצאת בתוך $D$. כאן $y=\frac75>1$, ולכן היא מחוץ למשולש ואינה נחשבת.",
              r"לא לכלול את הקודקודים ואת הנקודות הקריטיות על הצלעות בהשוואה הסופית.",
              r"לעצור אחרי שמצאו מקסימום אחד. הערך $5$ מתקבל בשתי נקודות."],
    steps=[
        num(r"פתרו את המערכת $f'_x=0,\ f'_y=0$. מהו הערך של $y$ בנקודה הקריטית (תשובה עשרונית)?", 1.4,
            r"$4x+y=3$ ו-$x-6y=-8$ נותנים $y=\frac75=1.4$ ו-$x=\frac25$. מכיוון ש-$y>1$ הנקודה מחוץ ל-$D$, שכולל רק $0\le x\le y\le1$."),
        num(r"על הצלע $BC$ ($y=1$) מתקבל $g(x)=2x^2-2x+5$. מהו $f\left(\frac12,1\right)$ בנקודה הקריטית $x=\frac12$ (תשובה עשרונית)?", 4.5,
            r"$g\left(\frac12\right)=\frac12-1+5=\frac92=4.5$."),
        choice(r"מהו המקסימום המוחלט של $f$ ב-$D$ ובאילו נקודות הוא מתקבל?",
               r"הערך $5$, ב-$B(0,1)$ וב-$C(1,1)$",
               [r"הערך $5$, ב-$C(1,1)$ בלבד", r"הערך $\frac92$, ב-$\left(\frac12,1\right)$", r"הערך $5$, ב-$B(0,1)$ בלבד"],
               r"הערכים בקודקודים הם $f(A)=0$, $f(B)=5$, $f(C)=5$, ובנקודה $\left(\frac12,1\right)$ הערך $\frac92<5$. לכן המקסימום $5$ מתקבל בשתי הנקודות $B$ ו-$C$.", pos=0),
        num(r"מהו המינימום המוחלט של $f$ ב-$D$?", 0,
            r"על $AC$ מתקבל $f(x,x)=5x$ שעולה ממש, ובקודקוד $A(0,0)$ הערך $0$ הוא הקטן מבין כל הערכים שנבדקו."),
    ])

add(4, "א",
    rubric=rub((r"הגדרת $g(t)=f(x(t),y(t))$ ונימוק ש-$g'(t)=0$ כי $g$ קבועה", 3),
               (r"כלל השרשרת: $g'(t)=2f'_x+e^tf'_y$", 4),
               (r"הצבת הנתון $f'_x=\frac{e^t}{2}$ וקבלת $e^t\left(1+f'_y\right)=0$", 3),
               (r"חילוק ב-$e^t\ne0$ ומסקנה $f'_y(2t+1,e^t)=-1$", 2)),
    pitfalls=[r"לגזור את $y(t)=e^t$ בטעות כ-$1$ או כ-$t$, ולשכוח את הגורם $e^t$ בכלל השרשרת.",
              r"לשכוח שהאגף הימני $3$ קבוע, ולכן נגזרתו לפי $t$ היא $0$ ולא $3$."],
    steps=[
        choice(r"איזו משוואה מתקבלת מגזירת $f(2t+1,e^t)=3$ לפי $t$ בכלל השרשרת?",
               r"$2f'_x+e^tf'_y=0$",
               [r"$e^tf'_x+2f'_y=0$", r"$2f'_x+f'_y=0$", r"$2f'_x+e^tf'_y=3$"],
               r"$x'(t)=2$ ו-$y'(t)=e^t$, ולכן $g'=f'_x\cdot2+f'_y\cdot e^t$. האגף הימני קבוע, ולכן נגזרתו $0$.", pos=1),
        num(r"בנקודה $t=0$ נתון $f'_x(1,1)=\frac12$. מהו הערך של $2f'_x(1,1)$?", 1,
            r"$2\cdot\frac12=1$. בצורה כללית $2\cdot\frac{e^t}{2}=e^t$."),
        num(r"מהו $f'_y(2t+1,e^t)$?", -1,
            r"$0=e^t+e^tf'_y$, ולכן $f'_y=-1$ לכל $t$."),
    ])

add(4, "ב",
    rubric=rub((r"חישוב $f'_x=\frac1{x+\frac1y}$ ו-$f'_y=\frac{-\frac1{y^2}}{x+\frac1y}$", 3),
               (r"פתרון $f'_x=1$ ו-$f'_y=-\frac{16}9$: קבלת $x+\frac1y=1$ ו-$y=\pm\frac34$", 4),
               (r"שתי הנקודות $\left(-\frac13,\frac34\right)$ ו-$\left(\frac73,-\frac34\right)$ ובדיקה שהן בתחום, $f=0$ בשתיהן", 1),
               (r"נוסחת המישור המשיק $z=f(x_0,y_0)+f'_x(x-x_0)+f'_y(y-y_0)$", 2),
               (r"שתי המשוואות $z=x-\frac{16}9y+\frac53$ ו-$z=x-\frac{16}9y-\frac{11}3$", 3)),
    pitfalls=[r"לקבל רק את הפתרון $y=\frac34$ ולשכוח את $y=-\frac34$ ממשוואת $y^2=\frac9{16}$. שתי הנקודות בתחום ההגדרה, ולכן יש שני מישורים משיקים.",
              r"לשכוח לחשב את $f(x_0,y_0)$. כאן $x_0+\frac1{y_0}=1$, ולכן $f=\ln1=0$."],
    steps=[
        num(r"התנאי $f'_x=1$ נותן $\frac{1}{x+\frac1y}=1$. מהו הערך של $x+\frac1y$?", 1,
            r"$\frac1{x+\frac1y}=1$ אם ורק אם $x+\frac1y=1$. לכן גם $f(x,y)=\ln1=0$."),
        num(r"עם $x+\frac1y=1$ מתקבל $f'_y=-\frac1{y^2}=-\frac{16}9$. מהו ערך ה-$y$ החיובי (תשובה עשרונית)?", 0.75,
            r"$y^2=\frac9{16}$, ולכן $y=\pm\frac34$. הערך החיובי הוא $0.75$."),
        choice(r"בכמה נקודות של תחום ההגדרה מתקיים $\nabla f=\left(1,-\frac{16}9\right)$?",
               r"בשתי נקודות",
               [r"בנקודה אחת", r"בשלוש נקודות", r"באף נקודה"],
               r"מ-$y=\frac34$ מקבלים $x=-\frac13$, ומ-$y=-\frac34$ מקבלים $x=\frac73$. בשתיהן $x+\frac1y=1>0$, ולכן שתיהן בתחום ההגדרה.", pos=0),
        num(r"המישור המשיק בנקודה עם $y=\frac34$ הוא $z=x-\frac{16}9y+c$. מהו $c$ (תשובה עשרונית, דיוק $0.001$)?", 1.6667,
            r"$z=\left(x+\frac13\right)-\frac{16}9\left(y-\frac34\right)=x-\frac{16}9y+\frac13+\frac43$, כלומר $c=\frac53\approx1.6667$.", tol=0.001),
    ])

add(5, "א",
    rubric=rub((r"בדיקה ש-$F(1,-1,0)=0$ ושהנגזרות החלקיות של $F$ רציפות (פולינום)", 3),
               (r"חישוב $F'_z(1,-1,0)=-3\ne0$ ומסקנה ממשפט הפונקציה הסתומה", 3),
               (r"חישוב $F'_x(1,-1,0)=-2$ ו-$F'_y(1,-1,0)=2$", 2),
               (r"נוסחאות $z_x=-\frac{F'_x}{F'_z}$, $z_y=-\frac{F'_y}{F'_z}$ וערכיהן $-\frac23$ ו-$\frac23$", 2),
               (r"סכום: $z_x+z_y=0$", 2)),
    pitfalls=[r"לבדוק רק ש-$F(1,-1,0)=0$ ולשכוח את תנאי המשפט $F'_z\ne0$ בנקודה.",
              r"לשכוח את סימן המינוס בנוסחה $z_x=-\frac{F'_x}{F'_z}$."],
    steps=[
        num(r"עבור $F(x,y,z)=5z^3+3xyz-x^2y^2+1$ חשבו את $F'_z(1,-1,0)$.", -3,
            r"$F'_z=15z^2+3xy$, ולכן $F'_z(1,-1,0)=0+3\cdot1\cdot(-1)=-3\ne0$, ותנאי משפט הפונקציה הסתומה מתקיים."),
        num(r"חשבו את $F'_x(1,-1,0)$.", -2,
            r"$F'_x=3yz-2xy^2$, ולכן $F'_x(1,-1,0)=0-2=-2$."),
        num(r"חשבו את $z_x(1,-1)$ (תשובה עשרונית, דיוק $0.001$).", -0.6667,
            r"$z_x=-\frac{F'_x}{F'_z}=-\frac{-2}{-3}=-\frac23$.", tol=0.001),
        num(r"חשבו את $z_x(1,-1)+z_y(1,-1)$.", 0,
            r"$F'_y(1,-1,0)=3xz-2x^2y=2$, ולכן $z_y=-\frac{2}{-3}=\frac23$. הסכום הוא $-\frac23+\frac23=0$."),
    ])

add(5, "ב",
    rubric=rub((r"קביעת הנגזרות החלקיות $f'_x=y(6-2x-y)$ ו-$f'_y=x(6-x-2y)$", 2),
               (r"פתרון המערכת וקבלת ארבע הנקודות הקריטיות $(0,0),(6,0),(0,6),(2,2)$", 3),
               (r"חישוב הנגזרות השניות $f''_{xx}=-2y,\ f''_{yy}=-2x,\ f''_{xy}=6-2x-2y$", 3),
               (r"$D=-36<0$ בשלוש הנקודות, ולכן אוכף", 3),
               (r"ב-$(2,2)$: $D=12>0$ ו-$f''_{xx}<0$, ולכן מקסימום מקומי עם ערך $8$", 2)),
    pitfalls=[r"לפתור את $y(6-2x-y)=0$ ו-$x(6-x-2y)=0$ בלי לפצל למקרים, ולהחמיץ את הנקודות $(6,0)$ ו-$(0,6)$.",
              r"לסווג לפי הסימן של $f''_{xx}$ בלבד, ללא חישוב הדטרמיננטה $D$."],
    steps=[
        num(r"כמה נקודות קריטיות יש ל-$f(x,y)=xy(6-x-y)$ במישור?", 4,
            r"המערכת $y(6-2x-y)=0,\ x(6-x-2y)=0$ נותנת $(0,0),(6,0),(0,6),(2,2)$."),
        num(r"חשבו את $D=f''_{xx}f''_{yy}-\left(f''_{xy}\right)^2$ בנקודה $(0,0)$.", -36,
            r"$f''_{xx}(0,0)=f''_{yy}(0,0)=0$ ו-$f''_{xy}(0,0)=6$, ולכן $D=-36$."),
        num(r"חשבו את $D$ בנקודה $(2,2)$.", 12,
            r"$f''_{xx}=f''_{yy}=-4$ ו-$f''_{xy}=6-8=-2$, ולכן $D=16-4=12$."),
        choice(r"מהו סוג הנקודה הקריטית $(2,2)$?",
               r"מקסימום מקומי",
               [r"מינימום מקומי", r"נקודת אוכף", r"אי אפשר להכריע"],
               r"$D=12>0$, ולכן יש אקסטרמום, ו-$f''_{xx}=-4<0$ קובע שזה מקסימום.", pos=2),
        num(r"מהו ערך הפונקציה בנקודת המקסימום המקומי?", 8,
            r"$f(2,2)=2\cdot2\cdot(6-2-2)=8$."),
    ])

exam = {
    "examCode": "24S-A",
    "examLabel": "מבחן סוף סמסטר, מועד קיץ תשפ\"ד",
    "year": 2024,
    "examDate": "03/11/2024",
    "sourceFile": "calculus-2/24S-A exam.pdf",
    "solutionFile": "none (no key)",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions (solved, pending refuter)")
