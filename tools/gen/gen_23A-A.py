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
SRC = "lecturer-solution"   # solution file of unclear authorship (handwritten + typed), accepted as the key
OFFICIAL = True


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
