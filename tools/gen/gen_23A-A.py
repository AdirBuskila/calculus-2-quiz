# -*- coding: utf-8 -*-
"""Generator for tools/raw/23A-A.json -- calculus-2 (20252), semester A 2023, moed A (12/02/2023).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_23A-A.py

Source: sitting 23A-A (orchestrator ruling: second letter of the code is the moed). Exam: 3 pages, 5 questions of
25 points (a=12, b=13), solve 4 of 5. Solution file: 12 pages, a mix of tablet handwriting (Q1, Q3a, Q4), blue
handwriting on lined paper (Q2) and typed pages (Q3b, Q5). Author unclear (triage), the orchestrator accepts the
handwritten keys. The exam header (lecturer names) is not transcribed. No handwriting is cropped.

Transcription notes
- The text layers are garbled; everything is transcribed from page renders.
- Q2b has three bullets (continuity, partial derivatives, differentiability); stored as one item, as in the flagship.
- Q2a prints two series in one part; stored as one item.
- The key's answers are tagged SRC below. Flip SRC / OFFICIAL if the orchestrator rules otherwise.

Slips in intermediate lines of the key, corrected and logged in docs/ASK_ADIR.md ("Resolved-by-ruling" notes):
- Q3a: the key starts the series at n=0 (exam: n=1); does not change radius or domain.
- Q3b: the key writes the partial derivative of f by its first argument as f_t; it is f_u.
- Q5a: the key finds the critical point (6,-6) and then writes (-6,6) in the Hessian lines and in the conclusion;
  the point is (6,-6) (the second derivatives are constants, so the classification is unchanged).
- Q5b: the key never states the convergence domain; it shows |x|<3 and |x|<2 for the two pieces, so |x|<2 is
  added as a closing line (sympy: radius 2, nearest pole x=2).

Checks (tools/verify/23A-A/check.py, sympy + numeric): every integral, gradient, limit comparison, radius, Lagrange
point, Hessian, partial-fraction coefficient and f^(10)(0) matches the key. regions.json and contours.json record
the double-integral regions and the extrema data.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "23A-A.json"
SRC = "student-solution"   # solution file of unclear authorship (handwritten + typed), accepted as the key
OFFICIAL = False  # GATE1 ruling 2026-10-24: unnamed-author key


def Q(num, kind, topic, question, solution, part=None, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "solution": solution.strip("\n"),
         "solutionSource": SRC, "official": OFFICIAL, "confidence": "high"}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ===== Q1a =====
questions.append(Q(1, "computation", "change_of_variables", r"""חשבו את ערך האינטגרל $\iint_D\arctan\dfrac{y}{x}\,dx\,dy$ כאשר
$$D=\left\{1\le x^2+y^2\le4,\ \ x\le y\le\sqrt{3}\cdot x,\ \ x\ge0\right\}$$""",
r"""התחום $D$ הוא חלק מטבעת ברביע הראשון, בין הישרים $y=x$ ו-$y=\sqrt{3}x$.
נעבור לקואורדינטות קוטביות:
$$x=r\cos\theta,\quad y=r\sin\theta,\qquad 1\le r\le2,\qquad \frac{\pi}{4}\le\theta\le\frac{\pi}{3}$$
ו-$\arctan\dfrac{y}{x}=\arctan\left(\dfrac{r\sin\theta}{r\cos\theta}\right)=\theta$ בתחום זה. לכן
$$I=\iint_{D'}\arctan\left(\frac{r\sin\theta}{r\cos\theta}\right)r\,dr\,d\theta=\int_1^2dr\int_{\pi/4}^{\pi/3}\theta\cdot r\,d\theta=\frac{7\pi^2}{192}.$$""", part="א", points=12))

# ===== Q1b =====
questions.append(Q(1, "computation", "gradient_directional", r"""מצאו את הכיוון בו קצב ההשתנות של הפונקציה $u=\ln\left(x^2+y^2+z^2\right)$ בנקודה $(1,2,1)$ הוא מקסימלי. נמקו את תשובתכם.""",
r"""הנגזרת הכיוונית היא
$$\frac{\partial f}{\partial\vec u}=\left|\vec\nabla f\right|\cdot\cos\delta,$$
כאשר $\delta$ היא הזווית בין הווקטור $\vec u$ לבין וקטור הגרדיאנט.
**מסקנה:** בכיוון וקטור הגרדיאנט קצב ההשתנות הוא מקסימלי (הרי אז $\delta=0$, כלומר $\cos\delta=1$).
$$\vec\nabla f=\left(\frac{2x}{x^2+y^2+z^2},\ \frac{2y}{x^2+y^2+z^2},\ \frac{2z}{x^2+y^2+z^2}\right)$$
$$\vec\nabla f(1,2,1)=\frac{2}{6}(1,2,1)$$
הכיוון המבוקש הוא כיוון הווקטור $(1,2,1)$ (כיוון היחידה $\frac{1}{\sqrt{6}}(1,2,1)$).""", part="ב", points=13))

# ===== Q2a =====
questions.append(Q(2, "computation", "numeric_series", r"""בדקו התכנסות בהחלט, בתנאי או התבדרות של הטורים הבאים:
$$\sum_{n=2}^{\infty}(-1)^n\cdot\sin\left(\frac{\pi}{n}\right)$$
$$\sum_{n=1}^{\infty}(-1)^n\cdot\ln\left(1+\frac{1}{n\sqrt[3]{n}}\right)$$""",
r"""**הטור הראשון.** נגדיר $a_n=(-1)^n\sin\left(\dfrac{\pi}{n}\right)$.
תכונות:
1) $|a_n|=\sin\dfrac{\pi}{n}\to0$ כאשר $n\to\infty$, וגם באופן מונוטוני כי הפונקציה $\sin(x)$ מונוטונית בקטע $\left[0,\frac{\pi}{2}\right]$ וגם רציפה עם הערך $\sin(0)=0$.
2) הטור מתחלף.
אז לפי מבחן לייבניץ הטור מתכנס.
הטור לא מתכנס בהחלט כי הטור $\sum_{n=2}^{\infty}\sin\left(\dfrac{\pi}{n}\right)$ מתבדר לפי מבחן ההשוואה הגבולי:
$$\lim_{n\to\infty}\frac{\sin\left(\frac{\pi}{n}\right)}{\frac{1}{n}}=\pi\in(0,\infty)$$
ו-$\sum\dfrac{1}{n}$ מתבדר.
**תשובה סופית:** הטור מתכנס בתנאי.

**הטור השני.** נגדיר $a_n=(-1)^n\ln\left(1+\dfrac{1}{n^{4/3}}\right)$.
$$\sum_{n=1}^{\infty}|a_n|=\sum_{n=1}^{\infty}\ln\left(1+\frac{1}{n^{4/3}}\right)$$
הטור $\sum_{n=1}^{\infty}\dfrac{1}{n^{4/3}}$ מתכנס, ולפי מבחן ההשוואה הגבולי
$$\lim_{n\to\infty}\frac{\ln\left(1+n^{-4/3}\right)}{n^{-4/3}}=1\in(0,\infty)$$
גם הטור $\sum|a_n|$ מתכנס.
**תשובה סופית:** הטור מתכנס בהחלט.""", part="א", points=12))

# ===== Q2b =====
questions.append(Q(2, "computation", "partials_differentiability", r"""נתונה הפונקציה
$$f(x,y)=\begin{cases}\left(x^2+y^2\right)\sin\dfrac{1}{\sqrt{x^2+y^2}}, & (x,y)\neq(0,0)\\[2mm] 0, & (x,y)=(0,0)\end{cases}$$
* האם $f(x,y)$ רציפה ב-$(0,0)$?
* מצאו את $f'_x(0,0)$ ו-$f'_y(0,0)$.
* האם $f(x,y)$ דיפרנציאבילית ב-$(0,0)$?""",
r"""**רציפות.** נעבור לקואורדינטות קוטביות, $r=\sqrt{x^2+y^2}$:
$$\lim_{(x,y)\to(0,0)}\left(x^2+y^2\right)\sin\frac{1}{\sqrt{x^2+y^2}}=\lim_{r\to0}r^2\sin\frac{1}{r}=0=f(0,0)$$
(כפל של פונקציה שואפת ל-0 ופונקציה חסומה). אז $f(x,y)$ רציפה ב-$(0,0)$.

**נגזרות חלקיות.**
$$f'_x(0,0)=\lim_{x\to0}\frac{f(x,0)-f(0,0)}{x}=\lim_{x\to0}x^2\cdot\frac{1}{x}\sin\frac{1}{|x|}=\lim_{x\to0}x\sin\frac{1}{|x|}=0$$
(כפל של פונקציה שואפת ל-0 ופונקציה חסומה).
באופן דומה
$$f'_y(0,0)=\lim_{y\to0}\frac{f(0,y)-f(0,0)}{y}=0.$$

**דיפרנציאביליות.** נבדוק:
$$\lim_{(x,y)\to(0,0)}\frac{f(x,y)-f(0,0)-f'_x(0,0)\,x-f'_y(0,0)\,y}{\sqrt{x^2+y^2}}=\lim_{(x,y)\to(0,0)}\frac{x^2+y^2}{\sqrt{x^2+y^2}}\sin\frac{1}{\sqrt{x^2+y^2}}$$
$$=\lim_{r\to0}r\sin\frac{1}{r}=0$$
**מסקנה:** הפונקציה $f(x,y)$ דיפרנציאבילית ב-$(0,0)$.""", part="ב", points=13))

# ===== Q3a =====
questions.append(Q(3, "computation", "power_series", r"""עבור אילו ערכי $x$ הטור מתכנס (מצאו רדיוס התכנסות ותחום התכנסות):
$$\sum_{n=1}^{\infty}x^n\,\frac{3^n}{(2n+1)^2\cdot\sqrt{5^n}}$$""",
r"""לפי דלמבר, רדיוס ההתכנסות הוא
$$R=\lim_{n\to\infty}\left|\frac{a_n}{a_{n+1}}\right|=\lim_{n\to\infty}\frac{\dfrac{3^n}{(2n+1)^2\sqrt{5^n}}}{\dfrac{3^{n+1}}{(2(n+1)+1)^2\sqrt{5^{n+1}}}}=\frac{\sqrt{5}}{3}$$
$$R=\frac{\sqrt{5}}{3}$$
כדי למצוא את תחום ההתכנסות נבדוק קצוות, $x=\pm\dfrac{\sqrt{5}}{3}$:
* אם $x=\dfrac{\sqrt{5}}{3}$ מתקבל הטור $\sum\dfrac{1}{(2n+1)^2}$. הטור מתכנס לפי קריטריון ההשוואה עם הטור ההרמוני המוכלל $\sum\dfrac{1}{n^2}$.
* אם $x=-\dfrac{\sqrt{5}}{3}$ מתקבל הטור $\sum\dfrac{(-1)^n}{(2n+1)^2}$. הטור מתכנס בהחלט ולכן מתכנס.

**תשובה סופית:**
* רדיוס ההתכנסות $R=\dfrac{\sqrt{5}}{3}$.
* תחום ההתכנסות $-\dfrac{\sqrt{5}}{3}\le x\le\dfrac{\sqrt{5}}{3}$.""", part="א", points=12))

# ===== Q3b =====
questions.append(Q(3, "proof", "chain_rule_identity", r"""הוכיחו כי הפונקציה $g(x,y,z)=f\left(\dfrac{1}{y}-\dfrac{1}{x},\ xye^{-\frac{z^2}{2}}\right)$ מקיימת את המשוואה
$$x^2\cdot g'_x+y^2\cdot g'_y=-\frac{x+y}{z}\,g'_z$$
כאשר $x,y\neq0$ ו-$f(u,v)$ דיפרנציאבילית עבור כל $(u,v)$""",
r"""נסמן $u=\dfrac{1}{y}-\dfrac{1}{x}$ ו-$v=xye^{-z^2/2}$, כך ש-$g(x,y,z)=f(u,v)$. מכאן נובע ש-
$$\begin{cases}\dfrac{\partial g}{\partial x}=\dfrac{\partial f}{\partial u}\cdot\dfrac{1}{x^2}+\dfrac{\partial f}{\partial v}\cdot ye^{-z^2/2}\\[2mm]\dfrac{\partial g}{\partial y}=\dfrac{\partial f}{\partial u}\cdot\left(-\dfrac{1}{y^2}\right)+\dfrac{\partial f}{\partial v}\cdot xe^{-z^2/2}\\[2mm]\dfrac{\partial g}{\partial z}=-\dfrac{\partial f}{\partial v}\cdot xyze^{-z^2/2}\end{cases}$$
לכן
$$x^2\frac{\partial g}{\partial x}+y^2\frac{\partial g}{\partial y}=\frac{\partial f}{\partial u}+\frac{\partial f}{\partial v}\cdot x^2ye^{-z^2/2}-\frac{\partial f}{\partial u}+\frac{\partial f}{\partial v}\cdot xy^2e^{-z^2/2}=\frac{\partial f}{\partial v}\cdot e^{-z^2/2}\left(x^2y+xy^2\right)$$
$$-\frac{x+y}{z}\frac{\partial g}{\partial z}=\frac{\partial f}{\partial v}\cdot\frac{x+y}{z}\,xyze^{-z^2/2}=\frac{\partial f}{\partial v}\left(x^2y+xy^2\right)e^{-z^2/2}$$
והמשוואה באמת מתקיימת.""", part="ב", points=13))

# ===== Q4a =====
questions.append(Q(4, "computation", "change_of_variables", r"""חשבו את האינטגרל $\iint_D\left(x^2+2xy\right)dx\,dy$
כאשר $D$ הוא התחום ברביע הראשון החסום על ידי:
$$y=\frac{1}{x^2},\quad y=\frac{4}{x^2},\qquad y=x+1,\quad y=x-1$$""",
r"""נעשה החלפת משתנים כללית:
$$u=y\cdot x^2,\qquad 1\le u\le4$$
$$v=y-x,\qquad -1\le v\le1$$
היעקוביאן ההפוך:
$$\frac{1}{J}=\begin{vmatrix}u'_x&v'_x\\u'_y&v'_y\end{vmatrix}=\begin{vmatrix}2xy&-1\\x^2&1\end{vmatrix}=2xy+x^2$$
$$J=\frac{1}{2xy+x^2}$$
$$\iint_D\left(x^2+2xy\right)dx\,dy=\iint_{D_{uv}}\left(x^2+2xy\right)\cdot\frac{1}{2xy+x^2}\,du\,dv=\int_1^4du\int_{-1}^{1}dv=(4-1)(1+1)=6.$$""", part="א", points=12))

# ===== Q4b =====
questions.append(Q(4, "computation", "absolute_extrema", r"""מצאו אקסטרמומים מוחלטים של הפונקציה
$$f(x,y)=1-x^2-y^2$$
בתחום $\left\{(x,y):(x-1)^2+(y-1)^2\le1\right\}$""",
r"""$$D:\ \left\{(x,y)\ \middle|\ (x-1)^2+(y-1)^2\le1\right\}$$
**בתוך התחום $D$:**
$$\begin{cases}f'_x=-2x=0\\ f'_y=-2y=0\end{cases}\ \Longrightarrow\ (x,y)=(0,0)\notin D$$
**על השפה** $(x-1)^2+(y-1)^2=1$ נבנה פונקציית לגראנז':
$$L(x,y,\lambda)=1-x^2-y^2+\lambda\left((x-1)^2+(y-1)^2-1\right)$$
$$\begin{cases}L'_x=-2x+2\lambda(x-1)=0\\ L'_y=-2y+2\lambda(y-1)=0\\ L'_\lambda=(x-1)^2+(y-1)^2-1=0\end{cases}$$
$$\lambda=\frac{x}{x-1}=\frac{y}{y-1}\ \Longrightarrow\ x=y$$
נציב באילוץ ונקבל
$$(x-1)^2+(x-1)^2=1$$
$$x_{1,2}=1\pm\frac{\sqrt{2}}{2},\quad y_{1,2}=1\pm\frac{\sqrt{2}}{2}\ \Longrightarrow\ M_1\left(1+\frac{\sqrt{2}}{2},\,1+\frac{\sqrt{2}}{2}\right),\quad M_2\left(1-\frac{\sqrt{2}}{2},\,1-\frac{\sqrt{2}}{2}\right)$$
האילוץ מגדיר תחום סגור וחסום (כידוע, הפונקציה רציפה ולכן מקבלת מינימום ומקסימום), ולכן נבדוק את הערכים בנקודות החשודות כדי לבדוק מי נותן מקסימום מוחלט ומי מינימום מוחלט:
$$f(M_1)=-2-2\sqrt{2},\qquad f(M_2)=-2+2\sqrt{2}$$
$\Longleftarrow$ ב-$M_1$ מינימום מוחלט של $f$ בתחום $D$, וב-$M_2$ מקסימום מוחלט של $f$ בתחום $D$.""", part="ב", points=13))

# ===== Q5a =====
questions.append(Q(5, "computation", "local_extrema", r"""מצאו וסווגו את נקודות האקסטרמום של הפונקציה:
$$f(x,y)=(x+y)^2-4y^2-48y$$""",
r"""$$f_x(x,y)=2(x+y)=0\iff x=-y$$
$$f_y(x,y)=2(x+y)-8y-48;\qquad x=-y\ \Longrightarrow$$
$$f_y(-y,y)=-8y-48=0\iff y=-6.$$
קיבלנו את הנקודה $(6,-6)$.
$$f_{xx}(x,y)=2\ \Longrightarrow\ f_{xx}(6,-6)=2=A$$
$$f_{yy}(x,y)=-6\ \Longrightarrow\ f_{yy}(6,-6)=-6=C$$
$$f_{xy}(x,y)=2\ \Longrightarrow\ f_{xy}(6,-6)=2=B$$
לכן
$$\Delta=AC-B^2=-12-4=-16<0$$
ומכאן הנקודה $(6,-6)$ היא נקודת אוכף.""", part="א", points=12))

# ===== Q5b =====
questions.append(Q(5, "computation", "taylor_maclaurin", r"""פתחו את הפונקציה $y=\dfrac{1}{x^2+x-6}$ לטור מקלורן. מהו תחום התכנסות הטור?
הסיקו את הערך של $f^{10}(0)$.""",
r"""$$x^2+x-6=(x+3)(x-2)$$
בואו נתפרק לשברים חלקיים:
$$\frac{1}{x^2+x-6}=\frac{A}{x+3}+\frac{B}{x-2}\iff 1=A(x-2)+B(x+3);$$
$x=2\Longrightarrow B=\dfrac{1}{5}$;
$x=-3\Longrightarrow A=-\dfrac{1}{5}$.
$$\Longrightarrow\ \frac{1}{x^2+x-6}=-\frac{1}{5}\cdot\frac{1}{x+3}+\frac{1}{5}\cdot\frac{1}{x-2};$$
$$\frac{1}{x+3}=\frac{1}{3\left(1+\frac{x}{3}\right)}=\frac{1}{3\left(1-\left(-\frac{x}{3}\right)\right)}=\frac{1}{3}\sum_{n=0}^{\infty}(-1)^n\frac{x^n}{3^n}=\sum_{n=0}^{\infty}(-1)^n\frac{x^n}{3^{n+1}};$$
עבור $\left|\dfrac{x}{3}\right|<1\iff|x|<3$.
$$\frac{1}{x-2}=\frac{-1}{2-x}=\frac{-1}{2\left(1-\frac{x}{2}\right)}=-\frac{1}{2}\sum_{n=0}^{\infty}\frac{x^n}{2^n}=-\sum_{n=0}^{\infty}\frac{x^n}{2^{n+1}};$$
עבור $\left|\dfrac{x}{2}\right|<1\iff|x|<2$.
$$\Longrightarrow\ \frac{1}{x^2+x-6}=-\frac{1}{5}\left(\sum_{n=0}^{\infty}(-1)^n\frac{x^n}{3^{n+1}}+\sum_{n=0}^{\infty}\frac{x^n}{2^{n+1}}\right)$$
$$=-\frac{1}{5}\sum_{n=0}^{\infty}\left(\frac{(-1)^n}{3^{n+1}}+\frac{1}{2^{n+1}}\right)x^n=\sum_{n=0}^{\infty}\frac{f^{(n)}(0)}{n!}x^n$$
שני הפיתוחים מתקיימים יחד עבור $|x|<2$, ולכן תחום ההתכנסות של הטור הוא $|x|<2$.
$n=10\ \Longrightarrow$
$$\frac{f^{(10)}(0)}{10!}=\left(-\frac{1}{5}\right)\left(\frac{(-1)^{10}}{3^{11}}+\frac{1}{2^{11}}\right)=-\frac{1}{5}\left(\frac{1}{3^{11}}+\frac{1}{2^{11}}\right)$$
$$\Longrightarrow\ f^{(10)}(0)=-\frac{10!}{5}\left(\frac{1}{3^{11}}+\frac{1}{2^{11}}\right)$$""", part="ב", points=13))

# ---- rubric / pitfalls / steps (ai-verified). Every expected value is re-computed in tools/verify/23A-A/steps_23A-A.py ----
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
            q["rubricSource"] = "ai-verified"
            q["stepsSource"] = "ai-verified"
            return
    raise KeyError((n, part))


add(1, "א",
    rubric=rub(("זיהוי התחום בקואורדינטות קוטביות: $1\\le r\\le2$ ו-$\\frac\\pi4\\le\\theta\\le\\frac\\pi3$", 4),
               ("הבחנה ש-$\\arctan\\frac yx=\\theta$ בתחום, והוספת היעקוביאן $r$", 3),
               ("פיצול האינטגרל לאינטגרל על $r$ ואינטגרל על $\\theta$", 2),
               ("חישוב סופי: $\\frac{7\\pi^2}{192}$", 3)),
    pitfalls=["לשכוח את היעקוביאן $r$ במעבר לקואורדינטות קוטביות.",
              "לקבוע את גבולות הזווית לא נכון: התנאי $x\\le y$ נותן $\\theta\\ge\\frac\\pi4$ ו-$y\\le\\sqrt3x$ נותן $\\theta\\le\\frac\\pi3$."],
    steps=[
        choice("מהו טווח הזווית $\\theta$ בתחום $x\\le y\\le\\sqrt3x$, $x\\ge0$?",
               "$\\frac\\pi4\\le\\theta\\le\\frac\\pi3$",
               ["$\\frac\\pi6\\le\\theta\\le\\frac\\pi4$", "$\\frac\\pi4\\le\\theta\\le\\frac\\pi2$", "$\\frac\\pi3\\le\\theta\\le\\frac\\pi2$"],
               "הישר $y=x$ הוא $\\theta=\\frac\\pi4$ והישר $y=\\sqrt3x$ הוא $\\theta=\\frac\\pi3$ (כי $\\tan\\theta=\\sqrt3$). התחום נמצא ביניהם.", pos=1),
        num("מהו $\\int_1^2r\\,dr$?", 1.5,
            "$\\left.\\frac{r^2}{2}\\right|_1^2=\\frac{4-1}{2}=\\frac32$."),
        num("מהו $\\int_{\\pi/4}^{\\pi/3}\\theta\\,d\\theta$ (תשובה עשרונית, דיוק $0.001$)?", 0.2399,
            "$\\frac12\\left(\\frac{\\pi^2}{9}-\\frac{\\pi^2}{16}\\right)=\\frac{7\\pi^2}{288}\\approx0.2399$.", tol=0.001),
        num("מהו ערך האינטגרל הכפול (תשובה עשרונית, דיוק $0.001$)?", 0.3598,
            "המכפלה $\\frac32\\cdot\\frac{7\\pi^2}{288}=\\frac{7\\pi^2}{192}\\approx0.3598$.", tol=0.001),
    ])

add(1, "ב",
    rubric=rub(("הנימוק: $\\frac{\\partial f}{\\partial\\vec u}=|\\nabla f|\\cos\\delta$, ולכן המקסימום בכיוון הגרדיאנט", 4),
               ("חישוב הנגזרות החלקיות של $u=\\ln\\left(x^2+y^2+z^2\\right)$", 4),
               ("הצבה ב-$(1,2,1)$: $\\nabla f=\\frac26(1,2,1)$", 3),
               ("ניסוח הכיוון: וקטור היחידה $\\frac1{\\sqrt6}(1,2,1)$", 2)),
    pitfalls=["להציב את הנקודה לפני הגזירה ולקבל גרדיאנט אפס או שגוי.",
              "להשאיר את הוקטור $(1,2,1)$ שאינו וקטור יחידה, כשהשאלה מבקשת כיוון."],
    steps=[
        num("מהו $x^2+y^2+z^2$ בנקודה $(1,2,1)$?", 6,
            "$1+4+1=6$."),
        num("מהו $\\frac{\\partial u}{\\partial y}$ בנקודה $(1,2,1)$ (תשובה עשרונית, דיוק $0.001$)?", 0.6667,
            "$\\frac{\\partial u}{\\partial y}=\\frac{2y}{x^2+y^2+z^2}=\\frac46=\\frac23$.", tol=0.001),
        choice("איזה וקטור יחידה נותן את קצב ההשתנות המקסימלי ב-$(1,2,1)$?",
               "$\\frac1{\\sqrt6}(1,2,1)$",
               ["$\\frac1{\\sqrt6}(-1,-2,-1)$", "$\\frac13(1,2,1)$", "$\\frac1{\\sqrt3}(1,1,1)$"],
               "הגרדיאנט הוא $\\frac13(1,2,1)$, והכיוון המקסימלי הוא כיוונו. אורך $(1,2,1)$ הוא $\\sqrt6$, ולכן מחלקים ב-$\\sqrt6$.", pos=0),
    ])

add(2, "א",
    rubric=rub(("הטור $\\sum(-1)^n\\sin\\frac\\pi n$: מבחן לייבניץ (יורד ושואף ל-$0$)", 3),
               ("הטור $\\sum(-1)^n\\sin\\frac\\pi n$: השוואה גבולית ל-$\\sum\\frac1n$ המתבדר, ולכן מתכנס בתנאי בלבד", 3),
               ("הטור $\\sum(-1)^n\\ln\\left(1+\\frac1{n\\sqrt[3]n}\\right)$: הצגת האיבר כ-$\\ln\\left(1+n^{-4/3}\\right)$", 2),
               ("השוואה גבולית ל-$\\sum n^{-4/3}$ המתכנס ($p=\\frac43>1$), ולכן מתכנס בהחלט", 4)),
    pitfalls=["להסיק מלייבניץ בלבד שהטור מתכנס בהחלט. יש לבדוק בנפרד את טור הערכים המוחלטים.",
              "לשכוח ש-$n\\sqrt[3]n=n^{4/3}$, ולהשוות לטור $\\sum\\frac1n$ המתבדר."],
    steps=[
        num("בבדיקת התכנסות בהחלט של $\\sum(-1)^n\\sin\\frac\\pi n$ משווים ל-$\\sum\\frac1n$. מהו הגבול $\\lim\\dfrac{\\sin\\frac\\pi n}{\\frac1n}$ (תשובה עשרונית, דיוק $0.001$)?", 3.1416,
            "$\\frac{\\sin(\\pi/n)}{1/n}=\\pi\\cdot\\frac{\\sin(\\pi/n)}{\\pi/n}\\to\\pi$. הגבול חיובי וסופי, ו-$\\sum\\frac1n$ מתבדר.", tol=0.001),
        num("מהי החזקה $p$ כך ש-$n\\sqrt[3]n=n^{p}$ (תשובה עשרונית, דיוק $0.001$)?", 1.3333,
            "$n\\cdot n^{1/3}=n^{4/3}$, ולכן $p=\\frac43>1$ והטור $\\sum n^{-p}$ מתכנס.", tol=0.001),
        choice("מה מסקנת הפתרון לגבי שני הטורים?",
               "הטור עם $\\sin\\frac\\pi n$ מתכנס בתנאי, והטור עם $\\ln$ מתכנס בהחלט",
               ["שני הטורים מתכנסים בהחלט",
                "שני הטורים מתכנסים בתנאי בלבד",
                "הטור עם $\\sin\\frac\\pi n$ מתכנס בהחלט, והטור עם $\\ln$ מתכנס בתנאי"],
               "טור הערכים המוחלטים של הטור עם $\\sin$ דומה ל-$\\sum\\frac1n$ ומתבדר, ולכן רק בתנאי. טור הערכים המוחלטים של הטור עם $\\ln$ דומה ל-$\\sum n^{-4/3}$ ומתכנס.", pos=2),
    ])

add(2, "ב",
    rubric=rub(("רציפות: מעבר לקואורדינטות קוטביות, $r^2\\sin\\frac1r\\to0=f(0,0)$", 3),
               ("הנגזרות החלקיות מההגדרה: $f'_x(0,0)=f'_y(0,0)=0$", 4),
               ("הצבה בהגדרת הדיפרנציאביליות והגעה לגבול $r\\sin\\frac1r$", 3),
               ("מסקנה: הפונקציה דיפרנציאבילית", 3)),
    pitfalls=["לטעות בנגזרת החלקית: $\\frac{f(h,0)}{h}=h\\sin\\frac1{|h|}$ ולא $h^2\\sin\\frac1{|h|}$, כי יש חילוק ב-$h$.",
              "לנסות לגזור את הנוסחה ולהציב $(0,0)$. בנקודה עצמה הפונקציה מוגדרת בנפרד, ולכן הנגזרות מחושבות מההגדרה."],
    steps=[
        num("מהו $f'_x(0,0)$?", 0,
            "$\\frac{f(h,0)-f(0,0)}{h}=h\\sin\\frac1{|h|}$, וזה שואף ל-$0$ (אפס כפול פונקציה חסומה)."),
        num("בבדיקת הדיפרנציאביליות מקבלים $\\dfrac{\\left(x^2+y^2\\right)\\sin\\frac1{\\sqrt{x^2+y^2}}}{\\sqrt{x^2+y^2}}=r^m\\sin\\frac1r$. מהו $m$?", 1,
            "$\\frac{r^2}{r}=r$, ולכן $m=1$."),
        choice("מה מסקנת הפתרון לגבי הפונקציה ב-$(0,0)$?",
               "רציפה, בעלת נגזרות חלקיות השוות ל-$0$, ודיפרנציאבילית",
               ["רציפה אך אינה דיפרנציאבילית",
                "אינה רציפה",
                "בעלת נגזרות חלקיות אך אינה רציפה"],
               "הגבול $r\\sin\\frac1r\\to0$, ולכן המנה בהגדרת הדיפרנציאביליות שואפת ל-$0$. הרציפות נובעת מ-$r^2\\sin\\frac1r\\to0$.", pos=0),
    ])

add(3, "א",
    rubric=rub(("מבחן המנה (דלמבר): $R=\\lim\\left|\\frac{a_n}{a_{n+1}}\\right|=\\frac{\\sqrt5}{3}$", 5),
               ("הקצה $x=\\frac{\\sqrt5}{3}$: הטור $\\sum\\frac1{(2n+1)^2}$ מתכנס בהשוואה ל-$\\sum\\frac1{n^2}$", 3),
               ("הקצה $x=-\\frac{\\sqrt5}{3}$: הטור מתכנס בהחלט", 2),
               ("ניסוח התשובה: $R=\\frac{\\sqrt5}{3}$ והתחום הסגור $\\left[-\\frac{\\sqrt5}{3},\\frac{\\sqrt5}{3}\\right]$", 2)),
    pitfalls=["לטעות ביחס $\\frac{a_n}{a_{n+1}}$ ולהפוך אותו, וכך לקבל $R=\\frac3{\\sqrt5}$ במקום $\\frac{\\sqrt5}3$.",
              "לשכוח לבדוק את הקצוות ולכתוב קטע פתוח."],
    steps=[
        num("מהו רדיוס ההתכנסות (תשובה עשרונית, דיוק $0.001$)?", 0.7454,
            "$\\frac{a_n}{a_{n+1}}\\to\\frac{\\sqrt5}{3}\\approx0.7454$.", tol=0.001),
        choice("איזה טור מתקבל בקצה $x=\\frac{\\sqrt5}{3}$?",
               "$\\sum\\frac1{(2n+1)^2}$",
               ["$\\sum\\frac{1}{2n+1}$", "$\\sum\\frac{(-1)^n}{(2n+1)^2}$", "$\\sum\\frac{3^n}{(2n+1)^2}$"],
               "מציבים $x^n=\\left(\\frac{\\sqrt5}3\\right)^n$, והגורמים $\\frac{3^n}{\\sqrt{5^n}}$ מצטמצמים ל-$1$. נשאר $\\frac1{(2n+1)^2}$, שמתכנס בהשוואה ל-$\\sum\\frac1{n^2}$.", pos=3),
        choice("מהו תחום ההתכנסות?",
               "$-\\frac{\\sqrt5}{3}\\le x\\le\\frac{\\sqrt5}{3}$",
               ["$-\\frac{\\sqrt5}{3}< x<\\frac{\\sqrt5}{3}$", "$-\\frac{\\sqrt5}{3}\\le x<\\frac{\\sqrt5}{3}$", "$-\\frac{\\sqrt5}{3}< x\\le\\frac{\\sqrt5}{3}$"],
               "שני הקצוות מתכנסים (בקצה השלילי הטור מתכנס בהחלט), ולכן התחום סגור.", pos=0),
    ])

add(3, "ב",
    rubric=rub(("הגדרת $u=\\frac1y-\\frac1x$, $v=xye^{-z^2/2}$ וכתיבת $g=f(u,v)$", 3),
               ("כלל השרשרת: חישוב $g'_x,g'_y,g'_z$", 4),
               ("חישוב $x^2g'_x+y^2g'_y$: האיברים עם $f'_u$ מצטמצמים", 3),
               ("חישוב אגף ימין וקבלת אותו ביטוי $f'_v\\left(x^2y+xy^2\\right)e^{-z^2/2}$", 3)),
    pitfalls=["טעות סימן בנגזרת של $\\frac1y$ לפי $y$ (היא $-\\frac1{y^2}$), שמונעת את צמצום האיברים עם $f'_u$.",
              "לשכוח את גורם השרשרת $-z$ בגזירת $e^{-z^2/2}$ לפי $z$."],
    steps=[
        choice("מהי $\\frac{\\partial g}{\\partial z}$?",
               "$-\\frac{\\partial f}{\\partial v}\\cdot xyze^{-z^2/2}$",
               ["$\\frac{\\partial f}{\\partial v}\\cdot xyze^{-z^2/2}$", "$-\\frac{\\partial f}{\\partial v}\\cdot xye^{-z^2/2}$", "$-\\frac{\\partial f}{\\partial u}\\cdot xyze^{-z^2/2}$"],
               "רק $v$ תלוי ב-$z$, ו-$\\frac{\\partial}{\\partial z}e^{-z^2/2}=-ze^{-z^2/2}$.", pos=2),
        {"type": "order", "prompt": "סדרו את שלבי ההוכחה.", "lines": [
            r"נסמן $u=\frac1y-\frac1x$, $v=xye^{-z^2/2}$, כך ש-$g=f(u,v)$.",
            r"כלל השרשרת: $g'_x=f'_u\cdot\frac1{x^2}+f'_v\cdot ye^{-z^2/2}$, $g'_y=-f'_u\cdot\frac1{y^2}+f'_v\cdot xe^{-z^2/2}$, $g'_z=-f'_v\cdot xyze^{-z^2/2}$.",
            r"מציבים בשני אגפי המשוואה: באגף שמאל האיברים עם $f'_u$ מצטמצמים, ושני האגפים שווים ל-$f'_v\left(x^2y+xy^2\right)e^{-z^2/2}$."],
         "explain": "מגדירים את המשתנים, גוזרים בכלל השרשרת, ובסוף מציבים ומשווים את שני האגפים."},
        {"type": "findbug", "prompt": "בהוכחה הבאה שורה אחת שגויה. מצאו אותה.", "lines": [
            r"נסמן $u=\frac1y-\frac1x$, $v=xye^{-z^2/2}$.",
            r"$g'_x=f'_u\cdot\frac1{x^2}+f'_v\cdot ye^{-z^2/2}$",
            r"$g'_y=f'_u\cdot\frac1{y^2}+f'_v\cdot xe^{-z^2/2}$",
            r"$g'_z=-f'_v\cdot xyze^{-z^2/2}$",
            r"$x^2g'_x+y^2g'_y=f'_v\cdot e^{-z^2/2}\left(x^2y+xy^2\right)$"], "bugIndex": 2,
         "explain": "הנגזרת של $u=\\frac1y-\\frac1x$ לפי $y$ היא $-\\frac1{y^2}$, ולא $+\\frac1{y^2}$. עם הסימן השגוי האיברים עם $f'_u$ לא מצטמצמים."},
    ])

add(4, "א",
    rubric=rub(("בחירת החלפת משתנים $u=yx^2$, $v=y-x$ והגבולות $1\\le u\\le4$, $-1\\le v\\le1$", 4),
               ("חישוב היעקוביאן ההפוך $2xy+x^2$", 4),
               ("צמצום האינטגרנד ל-$1$", 2),
               ("חישוב האינטגרל: $3\\cdot2=6$", 2)),
    pitfalls=["לשכוח שהיעקוביאן שמוצג הוא ההפוך, ולכפול בו במקום לחלק.",
              "לקבוע גבולות לא נכונים: העקומות $y=\\frac{1}{x^2}$ ו-$y=\\frac4{x^2}$ הן $u=1$ ו-$u=4$."],
    steps=[
        choice("מהו הדטרמיננט $\\begin{vmatrix}u'_x&v'_x\\\\u'_y&v'_y\\end{vmatrix}$ עבור $u=yx^2$, $v=y-x$?",
               "$2xy+x^2$", ["$2xy-x^2$", "$x^2-2xy$", "$2xy$"],
               "$u'_x=2xy$, $v'_x=-1$, $u'_y=x^2$, $v'_y=1$, ולכן הדטרמיננט הוא $2xy\\cdot1-(-1)x^2=2xy+x^2$.", pos=1),
        num("מהו האורך $\\int_1^4du$?", 3, "$4-1=3$."),
        num("מהו ערך האינטגרל?", 6,
            "האינטגרנד $\\left(x^2+2xy\\right)\\cdot\\frac1{2xy+x^2}=1$, ולכן האינטגרל הוא שטח המלבן: $3\\cdot2=6$."),
    ])

add(4, "ב",
    rubric=rub(("בדיקת נקודות קריטיות בפנים התחום: $(0,0)\\notin D$", 3),
               ("בניית פונקציית לגראנז' על השפה ופתרון: $x=y$", 4),
               ("הצבה באילוץ וקבלת שתי הנקודות $M_1,M_2$", 3),
               ("השוואת הערכים: מינימום ב-$M_1$ ומקסימום ב-$M_2$", 3)),
    pitfalls=["לשכוח את הבדיקה בפנים התחום. כאן היא פוסלת את $(0,0)$ כי הנקודה מחוץ לדיסקה.",
              "להחליף בין המקסימום למינימום: $f=1-x^2-y^2$ גדולה יותר בנקודה הקרובה יותר לראשית."],
    steps=[
        num("מהו הערך $(0-1)^2+(0-1)^2$? הוא קובע אם $(0,0)$ בתוך הדיסקה $(x-1)^2+(y-1)^2\\le1$.", 2,
            "הערך $2>1$, ולכן $(0,0)$ מחוץ לתחום ואין נקודה קריטית בפנים."),
        num("מהו הערך $f(M_2)$ עבור $M_2\\left(1-\\frac{\\sqrt2}2,1-\\frac{\\sqrt2}2\\right)$ (תשובה עשרונית, דיוק $0.001$)?", 0.8284,
            "$f(M_2)=1-2\\left(1-\\frac{\\sqrt2}2\\right)^2=-2+2\\sqrt2\\approx0.8284$.", tol=0.001),
        num("מהו המינימום המוחלט של $f$ בתחום (תשובה עשרונית, דיוק $0.001$)?", -4.8284,
            "$f(M_1)=-2-2\\sqrt2\\approx-4.8284$.", tol=0.001),
    ])

add(5, "א",
    rubric=rub(("פתרון $f_x=0$, $f_y=0$ וקבלת הנקודה $(6,-6)$", 5),
               ("חישוב $A=f_{xx}$, $B=f_{xy}$, $C=f_{yy}$", 3),
               ("חישוב $\\Delta=AC-B^2=-16$", 2),
               ("מסקנה: נקודת אוכף", 2)),
    pitfalls=["טעות סימן בקואורדינטה: מ-$x=-y$ ו-$y=-6$ מקבלים $x=6$.",
              "להסיק סוג נקודה מסימן $A$ בלבד, בלי לחשב את $\\Delta$."],
    steps=[
        num("מהי קואורדינטת ה-$y$ של הנקודה הקריטית?", -6,
            "מ-$f_x=0$ נובע $x=-y$, ומ-$f_y=2(x+y)-8y-48=-8y-48=0$ נובע $y=-6$."),
        num("מהו $\\Delta=f_{xx}f_{yy}-f_{xy}^2$?", -16,
            "$f_{xx}=2$, $f_{yy}=-6$, $f_{xy}=2$, ולכן $\\Delta=-12-4=-16$."),
        choice("איזו נקודה זו?",
               "נקודת אוכף", ["מינימום מקומי", "מקסימום מקומי", "לא ניתן להכריע"],
               "$\\Delta<0$, ולכן הנקודה היא נקודת אוכף.", pos=1),
    ])

add(5, "ב",
    rubric=rub(("פירוק לשברים חלקיים: $A=-\\frac15$, $B=\\frac15$", 4),
               ("פיתוח כל שבר כטור הנדסי", 3),
               ("תחום ההתכנסות המשותף $|x|<2$", 3),
               ("חישוב $f^{(10)}(0)=10!\\cdot c_{10}$", 3)),
    pitfalls=["לכתוב את תחום ההתכנסות כ-$|x|<3$. הפיתוח של $\\frac1{x-2}$ מתכנס רק ל-$|x|<2$.",
              "לשכוח להכפיל את המקדם $c_{10}$ ב-$10!$ כדי לקבל את הנגזרת."],
    steps=[
        num("בפירוק $\\frac1{(x+3)(x-2)}=\\frac A{x+3}+\\frac B{x-2}$ מהו $B$ (תשובה עשרונית, דיוק $0.001$)?", 0.2,
            "מציבים $x=2$ ב-$1=A(x-2)+B(x+3)$ ומקבלים $1=5B$, כלומר $B=\\frac15$.", tol=0.001),
        choice("מהו תחום ההתכנסות של הטור?",
               "$|x|<2$", ["$|x|<3$", "$|x|<5$", "$|x|<1$"],
               "הפיתוח של $\\frac1{x+3}$ מתכנס ל-$|x|<3$ ושל $\\frac1{x-2}$ ל-$|x|<2$. הטור המשותף מתכנס ב-$|x|<2$.", pos=3),
        num("מהו $f^{(10)}(0)$ (תשובה עשרונית, דיוק $0.01$)?", -358.47,
            "$f^{(10)}(0)=-\\frac{10!}{5}\\left(\\frac1{3^{11}}+\\frac1{2^{11}}\\right)\\approx-358.47$.", tol=0.01),
    ])

exam = {
    "examCode": "23A-A",
    "examLabel": "מבחן סוף סמסטר א' 2023, מועד א'",
    "year": 2023,
    "examDate": "12/02/2023",
    "sourceFile": "calculus-2/23A-A exam.pdf",
    "solutionFile": "calculus-2/23A-A solution.pdf",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
