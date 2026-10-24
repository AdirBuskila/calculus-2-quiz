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
