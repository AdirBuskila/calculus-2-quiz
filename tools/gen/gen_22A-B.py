# -*- coding: utf-8 -*-
"""Generator for tools/raw/22A-B.json -- calculus-2 (20252), semester A 2022, moed B (08/03/2022).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_22A-B.py

Source: sitting 22A-B (orchestrator ruling: second letter = moed). Exam: 3 pages, 5 questions of 25 points, solve 4
of 5 (per-part points are not printed on this exam, so none are stored). Solution file: 8 pages; Q1-Q3b typed
(pages 1-4), Q4 on a tablet (pages 5-6), Q5 on squared paper (pages 7-8). Author unclear; handwritten keys accepted by
the orchestrator. Exam header (lecturer names) not transcribed. No handwriting is cropped.

Solved by the solver (no key)
- Q3a: the solution file has no solution for it (page 4 starts with Q3b). Written by the solver: solutionSource
  "solved", official False. Verified in tools/verify/22A-B/solve_22A-B.py (sympy + numeric partial sums).

Slips in intermediate lines of the key, corrected (logged in docs/ASK_ADIR.md):
- Q1a: the third partial derivative is printed as df/dx; it is df/dz.
- Q2a: the key's heading prints the second series as (1+cos n)/(2^n+1) but the exam (and the key's own bound)
  use 2^(n+1). The exam's series is transcribed. The monotonicity line writes the exponent 2 for the first series;
  the exam's exponent is 3.
- Q2b: the last limit is written 2h^3/(2^{3/2} h^3); the value is +-2/2^{3/2} by the sign of h, nonzero either way.
- Q4b: the key writes the Lagrange solution with 1+lambda = +-sqrt2 and labels the two points x1 (max), x2 (min).

Checks (tools/verify/22A-B/check.py, sympy + numeric): all values match the key.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "22A-B.json"
SRC = "student-solution"   # solution file of unclear authorship, accepted as the key
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
questions.append(Q(1, "computation", "gradient_directional", r"""מצאו את הכיוון בו מתקבלת הנגזרת הכיוונית הגדולה ביותר של הפונקציה $f(x,y,z)=\ln\left(x^2+y^2+z^2\right)$ בנקודה $(1,2,1)$.
מה הוא ערכה של הנגזרת המקסימאלית?""",
r"""כידוע, הכיוון בו הנגזרת הכיוונית תהיה מקסימאלית נקבע ע"י ווקטור גרדיינט של הפונקציה. לכן, נחשב את הנגזרות החלקיות בנקודה הנתונה ונקבל
$$\frac{\partial f}{\partial x}=\left.\frac{2x}{x^2+y^2+z^2}\right|_{(1,2,1)}=\frac{2}{1+4+1}=\frac{1}{3}$$
$$\frac{\partial f}{\partial y}=\left.\frac{2y}{x^2+y^2+z^2}\right|_{(1,2,1)}=\frac{4}{1+4+1}=\frac{2}{3}$$
$$\frac{\partial f}{\partial z}=\left.\frac{2z}{x^2+y^2+z^2}\right|_{(1,2,1)}=\frac{2}{1+4+1}=\frac{1}{3}$$
ומכאן נובע שהכיוון הנדרש נקבע ע"י $\vec\nabla f(1,2,1)=\left(\dfrac{1}{3},\dfrac{2}{3},\dfrac{1}{3}\right)$ וערכה המקסימאלי של הנגזרת הכיוונית הוא נורמה של וקטור גרדיינט בנקודה, כלומר
$$\left\|\vec\nabla f(1,2,1)\right\|=\sqrt{\frac{1}{9}+\frac{4}{9}+\frac{1}{9}}=\frac{\sqrt{6}}{3}.$$""", part="א"))

# ===== Q1b =====
questions.append(Q(1, "computation", "change_of_variables", r"""חשבו את ערך האינטגרל
$$\int_0^3\int_{-\sqrt{9-y^2}}^{\sqrt{9-y^2}}\sin\left(2+x^2+y^2\right)dx\,dy$$""",
r"""התחום הוא חצי עיגול $x^2+y^2\le9,\ y\ge0$. נעבור לקואורדינטות קוטביות $x=r\cos\theta,\ y=r\sin\theta$, $0\le r\le3,\ 0\le\theta\le\pi$:
$$\int_0^3\int_{-\sqrt{9-y^2}}^{\sqrt{9-y^2}}\sin\left(2+x^2+y^2\right)dx\,dy=\int_0^{\pi}\int_0^3\sin\left(2+r^2\right)r\,dr\,d\theta$$
$$=\int_0^{\pi}d\theta\cdot\int_0^3\sin\left(2+r^2\right)r\,dr=\left.\theta\right|_0^{\pi}\cdot\left.\left(-\frac{1}{2}\cos\left(2+r^2\right)\right)\right|_0^3=\pi\cdot\left(-\frac{1}{2}\cos(11)+\frac{1}{2}\cos(2)\right)$$
$$=\frac{\pi}{2}\left(\cos 2-\cos 11\right).$$""", part="ב"))

# ===== Q2a =====
questions.append(Q(2, "computation", "numeric_series", r"""בדקו התכנסות הטורים הבאים:
$$\sum_{n=2}^{\infty}\frac{(-1)^n}{(n-\ln n)^3}$$
$$\sum_{n=1}^{\infty}\frac{1+\cos(n)}{2^{n+1}}$$""",
r"""**הטור הראשון.** נבחן את הפונקציה $f_1(x)=x-\ln x$, שהנגזרת שלה $f_1'(x)=1-\dfrac{1}{x}>0$ עבור כל $x\ge2$. אזי $f_1(x)$ היא פונקציה עולה ולכן הפונקציה $f_2(x)=\dfrac{1}{(x-\ln x)^3}$ יורדת, זה אומר שהסדרה $\left\{\dfrac{1}{(n-\ln n)^3}\right\}$ יורדת (ושואפת ל-0). הטור המקורי הוא טור מחליף סימן ולפי משפט לייבניץ הטור מתכנס.

**הטור השני.** נציין תחילה שהטור הוא טור חיובי, כי לכל $n\in\mathbb{N}$ מתקיים $1+\cos n\ge0$, ויש לנו גם ש-
$$\frac{1+\cos n}{2^{n+1}}\le\frac{2}{2^{n+1}}=\left(\frac{1}{2}\right)^n.$$
אנחנו יודעים שהטור $\sum_{n=1}^{\infty}\left(\dfrac{1}{2}\right)^n$ מתכנס, אזי גם הטור המקורי מתכנס.""", part="א"))

# ===== Q2b =====
questions.append(Q(2, "computation", "partials_differentiability", r"""נתונה הפונקציה
$$f(x,y)=\begin{cases}\dfrac{x^3+y^3}{x^2+y^2}, & (x,y)\neq(0,0)\\[2mm] 0, & (x,y)=(0,0)\end{cases}$$
* האם $f(x,y)$ רציפה ב-$(0,0)$?
* מצאו את $f'_x(0,0)$ ו-$f'_y(0,0)$.
* האם $f(x,y)$ דיפרנציאבילית ב-$(0,0)$?""",
r"""**רציפות.** נראה שהפונקציה רציפה ב-$(0,0)$:
$$\lim_{(x,y)\to(0,0)}\frac{x^3+y^3}{x^2+y^2}=\lim_{r\to0}\frac{r^3\cos^3\theta+r^3\sin^3\theta}{r^2}=\lim_{r\to0}r\left(\cos^3\theta+\sin^3\theta\right)=0=f(0,0)$$
כי $\cos^3\theta+\sin^3\theta$ היא פונקציה חסומה.

**נגזרות חלקיות** ב-$(0,0)$:
$$f'_x(0,0)=\lim_{h\to0}\frac{f(h,0)-f(0,0)}{h}=\lim_{h\to0}\frac{\frac{h^3}{h^2}}{h}=\lim_{h\to0}\frac{h^3}{h^3}=1;$$
$$f'_y(0,0)=\lim_{k\to0}\frac{f(0,k)-f(0,0)}{k}=\lim_{k\to0}\frac{\frac{k^3}{k^2}}{k}=\lim_{k\to0}\frac{k^3}{k^3}=1.$$

**דיפרנציאביליות.** נראה אם הפונקציה דיפרנציאבילית:
$$\lim_{(h,k)\to(0,0)}\frac{f(h,k)-f(0,0)-hf'_x(0,0)-kf'_y(0,0)}{\sqrt{h^2+k^2}}=\lim_{(h,k)\to(0,0)}\frac{\frac{h^3+k^3}{h^2+k^2}-h-k}{\sqrt{h^2+k^2}}$$
$$=\lim_{(h,k)\to(0,0)}\frac{\frac{h^3+k^3-h^3-hk^2-kh^2-k^3}{h^2+k^2}}{\sqrt{h^2+k^2}}=\lim_{(h,k)\to(0,0)}-\frac{hk^2+kh^2}{\left(h^2+k^2\right)^{1/2}\left(h^2+k^2\right)}=-\lim_{(h,k)\to(0,0)}\frac{hk^2+kh^2}{\left(h^2+k^2\right)^{3/2}}$$
עבור $h=k>0$ מקבלים ש-
$$-\lim_{h\to0^+}\frac{h^3+h^3}{\left(2h^2\right)^{3/2}}=-\lim_{h\to0^+}\frac{2h^3}{2^{3/2}h^3}=-\frac{2}{2^{3/2}}\neq0$$
לכן הפונקציה אינה דיפרנציאבילית ב-$(0,0)$.""", part="ב"))

# ===== Q3a (no key; solver) =====
questions.append(Q(3, "computation", "power_series", r"""עבור אילו ערכי $x$ הטור מתכנס (מצאו רדיוס התכנסות ותחום התכנסות):
$$\sum_{n=1}^{\infty}\frac{n}{\left(n^2+1\right)\cdot3^n}\,x^n$$""",
r"""נסמן $a_n=\dfrac{n}{\left(n^2+1\right)3^n}$.
**רדיוס ההתכנסות.**
$$\left|\frac{a_{n+1}}{a_n}\right|=\frac{n+1}{\left((n+1)^2+1\right)3^{n+1}}\cdot\frac{\left(n^2+1\right)3^n}{n}=\frac{1}{3}\cdot\frac{n+1}{n}\cdot\frac{n^2+1}{(n+1)^2+1}\xrightarrow[n\to\infty]{}\frac{1}{3}$$
לכן $R=3$: הטור מתכנס בהחלט עבור $|x|<3$ ומתבדר עבור $|x|>3$.

**נקודת הקצה $x=3$.** מקבלים
$$\sum_{n=1}^{\infty}\frac{n}{\left(n^2+1\right)3^n}\,3^n=\sum_{n=1}^{\infty}\frac{n}{n^2+1}.$$
זה טור חיובי, ובמבחן ההשוואה הגבולי עם $b_n=\frac{1}{n}$:
$$\lim_{n\to\infty}\frac{\frac{n}{n^2+1}}{\frac{1}{n}}=\lim_{n\to\infty}\frac{n^2}{n^2+1}=1.$$
הטור ההרמוני $\sum\frac{1}{n}$ מתבדר, ולכן גם הטור מתבדר ב-$x=3$.

**נקודת הקצה $x=-3$.** מקבלים
$$\sum_{n=1}^{\infty}(-1)^n\frac{n}{n^2+1}.$$
זה טור מחליף סימן עם $c_n=\frac{n}{n^2+1}>0$:
* $c_n\to0$.
* $c_n$ יורדת: עבור $g(t)=\frac{t}{t^2+1}$ מתקיים $g'(t)=\frac{1-t^2}{\left(t^2+1\right)^2}\le0$ לכל $t\ge1$.

לכן לפי משפט לייבניץ הטור מתכנס ב-$x=-3$ (בתנאי בלבד, כי טור הערכים המוחלטים הוא הטור של $x=3$, שמתבדר).

**תשובה:** רדיוס ההתכנסות $R=3$, ותחום ההתכנסות $[-3,3)$.""", part="א",
    solutionSource="solved", official=False))

# ===== Q3b =====
questions.append(Q(3, "computation", "implicit_function", r"""נתונה המשוואה $z^3-3xyz=4$
הראו כי המשוואה מגדירה פונקציה סתומה $z=f(x,y)$ בסביבת נקודה $(2,1,-2)$ וחשבו את $z''_{xy}(2,1)$.""",
r"""נגדיר את הפונקציה $F(x,y,z)=z^3-3yxz-4$ ונראה כי תנאי משפט הפונקציה הסתומה מתקיימים:
א. $F(2,1,-2)=0$.
ב. $F(x,y,z)$ רציפה ובעלת נגזרות חלקיות רציפות בסביבת הנקודה $(2,1,-2)$.
ג. $F_z(x,y,z)=3z^2-3yx$, $F_z(2,1,-2)\neq0$.
ולכן על פי משפט הפונקציה הסתומה קיימת סביבה של הנקודה $(2,1,-2)$ כך שבסביבה זו מוגדרת פונקציה יחידה $f(x,y)$ המקיימת $F(x,y,f(x,y))=0$ כך ש:
$f(2,1)=-2$, $f(x,y)$ רציפה ב-$(2,1)$ ו-$f(x,y)$ גזירה ומתקיים:
$$z_x=-\frac{F'_x}{F'_z}=-\frac{-3yz}{3z^2-3yx}=\frac{3yz}{3z^2-3yx}=\frac{yz}{z^2-yx}$$
$$\Rightarrow\ z'_x(2,1,-2)=\frac{-2}{2}=-1$$
כדי לחשב את $z''_{xy}$ נגזור את $z'_x$ לפי $y$ ונתייחס ל-$z$ כאל פונקציה של $y$. תחילה נחשב את $z'_y$ בנקודה.
$$z'_y=-\frac{F'_y}{F'_z}=-\frac{-3xz}{3z^2-3yx}=\frac{3xz}{3z^2-3yx}=\frac{xz}{z^2-yx}$$
$$\Rightarrow\ z'_y(2,1,-2)=\frac{-4}{2}=-2$$
מכאן:
$$z''_{xy}=\left(z_x\right)'_y=\left.\left(\frac{yz}{z^2-yx}\right)\right|'_y=\frac{\left(z+y\cdot z'_y\right)\left(z^2-yx\right)-\left(2z\cdot z'_y-x\right)\cdot yz}{\left(z^2-yx\right)^2}$$
$$\Rightarrow\ z''_{xy}(2,1,-2)=\frac{-4\cdot2-6\cdot(-2)}{2^2}=1$$""", part="ב"))

# ===== Q4a =====
questions.append(Q(4, "computation", "change_of_variables", r"""חשבו את האינטגרל $\iint_D\dfrac{y-x}{2x+y}\,dx\,dy$
כאשר $D$ הוא התחום ברביע הראשון החסום על ידי הישרים:
$$y=4+x,\quad y=1+x,\quad y=6-2x,\quad y=8-2x$$""",
r"""נגדיר את ההעתקה
$$T:\ \begin{cases}u=y-x\\ v=y+2x\end{cases}\ \Longrightarrow\ T(D)=\left\{(u,v):\ 1\le u\le4,\ 6\le v\le8\right\}$$
$$J^{-1}=\begin{vmatrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\ \frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{vmatrix}=\begin{vmatrix}-1&1\\2&1\end{vmatrix}=-1-2=-3\ \Longrightarrow\ |J|=\frac{1}{3}$$
$$\iint_D\frac{y-x}{2x+y}\,dx\,dy=\frac{1}{3}\iint_{T(D)}\frac{u}{v}\,du\,dv=\frac{1}{3}\int_6^8\frac{dv}{v}\int_1^4u\,du=\frac{1}{3}\left.\ln v\right|_6^8\cdot\left.\frac{u^2}{2}\right|_1^4=\frac{1}{3}\cdot\frac{15}{2}\cdot\ln\frac{8}{6}=\frac{5}{2}\ln\frac{4}{3}.$$""", part="א"))

# ===== Q4b =====
questions.append(Q(4, "computation", "absolute_extrema", r"""מצאו אקסטרמומים מוחלטים של הפונקציה
$$f(x,y)=1-x^2-y^2$$
בתחום $\left\{(x,y):(x-1)^2+(y-1)^2\le1\right\}$""",
r"""**בתוך התחום:**
$$\begin{cases}\dfrac{\partial f}{\partial x}=-2x=0\\[2mm]\dfrac{\partial f}{\partial y}=-2y=0\end{cases}\ \Rightarrow\ x=y=0$$
הנקודה $(0,0)$ אינה בתחום.
**על השפה:** $g(x,y)=(x-1)^2+(y-1)^2-1=0$.
$$L(x,y,\lambda)=1-x^2-y^2-\lambda\left[(x-1)^2+(y-1)^2-1\right]$$
$$\frac{\partial L}{\partial x}=-2x-2\lambda(x-1)=0\iff2\lambda=2x(1+\lambda)\iff x=\frac{\lambda}{1+\lambda}\quad\left(x-1=\frac{-1}{1+\lambda}\right)$$
$$\frac{\partial L}{\partial y}=-2y-2\lambda(y-1)=0\iff y=\frac{\lambda}{1+\lambda}\quad\left(y-1=\frac{-1}{1+\lambda}\right)$$
$$\frac{\partial L}{\partial\lambda}=(x-1)^2+(y-1)^2-1=0\iff\frac{1}{(1+\lambda)^2}+\frac{1}{(1+\lambda)^2}=1\iff1+\lambda=\pm\sqrt{2}$$
$$x_1=\frac{-1+\sqrt{2}}{\sqrt{2}}=1-\frac{1}{\sqrt{2}}=y_1,\qquad x_2=\frac{-1-\sqrt{2}}{-\sqrt{2}}=1+\frac{1}{\sqrt{2}}=y_2$$
$$f\left(1-\frac{1}{\sqrt{2}},1-\frac{1}{\sqrt{2}}\right)=1-\left(1-\frac{1}{\sqrt{2}}\right)^2-\left(1-\frac{1}{\sqrt{2}}\right)^2=1-1+\sqrt{2}-\frac{1}{2}-1+\sqrt{2}-\frac{1}{2}=2\left(\sqrt{2}-1\right)$$
זהו המקסימום.
$$f\left(1+\frac{1}{\sqrt{2}},1+\frac{1}{\sqrt{2}}\right)=-2\left(\sqrt{2}+1\right)$$
זהו המינימום.""", part="ב"))

# ===== Q5a =====
questions.append(Q(5, "computation", "power_series", r"""מצאו את הפונקציה אליה הטור מתכנס בתחום $-1\le x\le1$ :
$$\sum_{n=1}^{\infty}\frac{(-1)^{1+n}x^{2n-1}}{2n-1}$$""",
r"""תחום ההתכנסות של הטור הוא $-1\le x\le1$ (קל לבדוק).
עבור $x$ בתחום זה הטור מתכנס ל-$f(x)$.
$$f'(x)=\left(\sum_{n=1}^{\infty}\frac{(-1)^{n+1}x^{2n-1}}{2n-1}\right)'=\sum_{n=1}^{\infty}(-1)^{n+1}x^{2n-2}=\sum_{n=1}^{\infty}(-1)^{n+1}\left(x^2\right)^{n-1}$$
$$=\sum_{n=0}^{\infty}(-1)^n\left(x^2\right)^n=\frac{1}{1+x^2}$$
מכאן
$$f(x)=\int_0^xf'(t)\,dt=\int_0^x\frac{dt}{1+t^2}=\arctan x$$
ולבסוף
$$\sum_{n=1}^{\infty}\frac{(-1)^{n+1}x^{2n-1}}{2n-1}=\arctan x.$$""", part="א"))

# ===== Q5b =====
questions.append(Q(5, "computation", "local_extrema", r"""מצאו וסווגו את נקודות האקסטרמום של הפונקציה:
$$f(x,y)=x^3+8y^3-6xy+1$$""",
r"""$$f(x,y)=z=x^3+8y^3-6xy+1$$
$$\begin{cases}z'_x=3x^2-6y\\ z'_y=24y^2-6x\end{cases}\ \Rightarrow\ \begin{cases}3x^2-6y=0\\ 24y^2-6x=0\end{cases}$$
$$\Rightarrow\ y=\frac{x^2}{2}$$
$$6x^4-6x=0,\qquad6x\left(x^3-1\right)=0\ \Rightarrow\ \begin{cases}x=0,\ y=0&A(0,0)\\ x=1,\ y=\frac{1}{2}&B\left(1,\frac{1}{2}\right)\end{cases}$$
$$z''_{xx}=6x,\qquad z''_{xy}=-6,\qquad z''_{yy}=48y$$
$$z''_{xx}\big|_A=z''_{yy}\big|_A=0$$
$$D=0-36<0$$
לכן נקודת אוכף ב-$A$.
$$z''_{xx}\big|_B=6,\qquad z''_{yy}\big|_B=24$$
$$D=6\cdot24-36>0,\quad z''_{xx}>0$$
לכן נקודת מינימום מקומי ב-$B$.""", part="ב"))

# ---- rubric / pitfalls / steps (ai-draft). Every expected value is re-computed in tools/verify/22A-B/steps_22A-B.py ----
# Per-part points are not printed on this exam; the rubric splits each 25-point question as 12 + 13 (a + b).
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
    rubric=rub((r"הנימוק שהכיוון של הנגזרת הכיוונית הגדולה ביותר הוא כיוון הגרדיאנט", 2),
               (r"חישוב שלוש הנגזרות החלקיות של $\ln\left(x^2+y^2+z^2\right)$", 4),
               (r"הצבה ב-$(1,2,1)$: $\vec\nabla f=\left(\frac13,\frac23,\frac13\right)$", 3),
               (r"הערך המקסימלי הוא הנורמה $\left\|\vec\nabla f\right\|=\frac{\sqrt6}{3}$", 3)),
    pitfalls=[r"להציב את הנקודה לפני הגזירה ולקבל גרדיאנט שגוי.",
              r"לתת כערך הנגזרת המקסימלית את הגרדיאנט עצמו (וקטור) במקום את הנורמה שלו."],
    steps=[
        num(r"מהו $\dfrac{\partial f}{\partial y}$ בנקודה $(1,2,1)$ (תשובה עשרונית, דיוק $0.001$)?", 0.6667,
            r"$\frac{2y}{x^2+y^2+z^2}=\frac46=\frac23$.", tol=0.001),
        choice(r"איזה וקטור קובע את הכיוון של הנגזרת הכיוונית הגדולה ביותר ב-$(1,2,1)$?",
               r"$\left(\frac13,\frac23,\frac13\right)$",
               [r"$\left(-\frac13,-\frac23,-\frac13\right)$",
                r"$\left(\frac23,\frac13,\frac13\right)$",
                r"$\left(\frac13,\frac13,\frac13\right)$"],
               r"הכיוון נקבע על ידי הגרדיאנט. הוקטור הנגדי נותן את הנגזרת הכיוונית הקטנה ביותר, ושני האחרים אינם הגרדיאנט.", pos=0),
        num(r"מהו הערך המקסימלי של הנגזרת הכיוונית (תשובה עשרונית, דיוק $0.001$)?", 0.8165,
            r"נורמת הגרדיאנט: $\sqrt{\frac19+\frac49+\frac19}=\frac{\sqrt6}{3}\approx0.8165$.", tol=0.001),
    ])

add(1, "ב",
    rubric=rub((r"זיהוי התחום כחצי עיגול $x^2+y^2\le9,\ y\ge0$", 3),
               (r"מעבר לקואורדינטות קוטביות: $0\le r\le3$, $0\le\theta\le\pi$ והוספת היעקוביאן $r$", 4),
               (r"פיצול ל-$\int_0^\pi d\theta\cdot\int_0^3\sin\left(2+r^2\right)r\,dr$ ואינטגרציה לפי $r$", 3),
               (r"תוצאה סופית: $\frac\pi2(\cos2-\cos11)$", 2)),
    pitfalls=[r"לשכוח את היעקוביאן $r$ במעבר לקואורדינטות קוטביות.",
              r"לקחת $0\le\theta\le2\pi$ (עיגול שלם) כשהתחום הוא חצי עיגול בלבד."],
    steps=[
        choice("מהם גבולות האינטגרציה בקואורדינטות קוטביות?",
               r"$0\le r\le3,\quad0\le\theta\le\pi$",
               [r"$0\le r\le3,\quad0\le\theta\le2\pi$",
                r"$0\le r\le9,\quad0\le\theta\le\pi$",
                r"$0\le r\le3,\quad0\le\theta\le\frac\pi2$"],
               r"הגבולות של $x$ בתחום מתארים את המעגל $x^2+y^2=9$, ו-$y$ רץ מ-$0$ עד $3$. זה חצי העיגול העליון: רדיוס $3$ וזווית מ-$0$ עד $\pi$.", pos=2),
        num(r"מהו $\int_0^3\sin\left(2+r^2\right)r\,dr$ (תשובה עשרונית, דיוק $0.001$)?", -0.2103,
            r"$\left.-\frac12\cos\left(2+r^2\right)\right|_0^3=\frac12(\cos2-\cos11)\approx-0.2103$.", tol=0.001),
        num(r"מהו ערך האינטגרל הכפול (תשובה עשרונית, דיוק $0.001$)?", -0.6606,
            r"$\pi\cdot\frac12(\cos2-\cos11)\approx-0.6606$.", tol=0.001),
    ])

add(2, "א",
    rubric=rub((r"הטור הראשון: $f_1(x)=x-\ln x$ עולה כי $f_1'(x)=1-\frac1x>0$ עבור $x\ge2$", 3),
               (r"האיברים $\frac1{(n-\ln n)^3}$ יורדים ושואפים ל-$0$, ולכן הטור מתכנס לפי לייבניץ", 3),
               (r"הטור השני חיובי וחסום: $\frac{1+\cos n}{2^{n+1}}\le\left(\frac12\right)^n$", 3),
               (r"השוואה לטור ההנדסי המתכנס $\sum\left(\frac12\right)^n$, ולכן גם הטור השני מתכנס", 3)),
    pitfalls=[r"לשכוח לבדוק שהסדרה יורדת ושואפת ל-$0$ לפני שמפעילים את משפט לייבניץ.",
              r"לחסום את $1+\cos n$ ב-$1$ במקום ב-$2$, ולקבל חסם שגוי."],
    steps=[
        choice("באיזה מבחן הפתרון משתמש לטור הראשון $\\sum_{n=2}^{\\infty}\\frac{(-1)^n}{(n-\\ln n)^3}$?",
               "משפט לייבניץ לטור מחליף סימן",
               ["מבחן המנה של דלמבר", "מבחן השורש של קושי", "מבחן האיבר הכללי: האיבר אינו שואף ל-$0$"],
               r"הטור מחליף סימן והאיברים בערך מוחלט יורדים ושואפים ל-$0$, ולכן לייבניץ מתאים. מבחן המנה והשורש נותנים כאן $1$ ואינם מכריעים.", pos=0),
        num(r"מהי $f_1'(2)$ עבור $f_1(x)=x-\ln x$ (תשובה עשרונית, דיוק $0.001$)?", 0.5,
            r"$f_1'(x)=1-\frac1x$, ולכן $f_1'(2)=\frac12>0$. הפונקציה עולה, ולכן $\frac1{f_1^3}$ יורדת.", tol=0.001),
        num(r"מהו סכום הטור ההנדסי $\sum_{n=1}^{\infty}\left(\frac12\right)^n$ שחוסם את הטור השני?", 1,
            r"$\frac{1/2}{1-1/2}=1$."),
        choice("מה מסקנת הפתרון לגבי שני הטורים?",
               "שני הטורים מתכנסים",
               ["הטור הראשון מתכנס והשני מתבדר", "הטור הראשון מתבדר והשני מתכנס", "שני הטורים מתבדרים"],
               r"הראשון מתכנס לפי לייבניץ, והשני חסום על ידי טור הנדסי מתכנס.", pos=1),
    ])

add(2, "ב",
    rubric=rub((r"רציפות: בקואורדינטות קוטביות $r\left(\cos^3\theta+\sin^3\theta\right)\to0=f(0,0)$", 3),
               (r"חישוב $f'_x(0,0)=1$ ו-$f'_y(0,0)=1$ מההגדרה", 3),
               (r"הצבה בהגדרת הדיפרנציאביליות והגעה לגבול $-\frac{hk^2+kh^2}{\left(h^2+k^2\right)^{3/2}}$", 4),
               (r"לאורך $h=k>0$ הגבול הוא $-\frac2{2^{3/2}}\ne0$, ולכן הפונקציה אינה דיפרנציאבילית", 3)),
    pitfalls=[r"להסיק מקיום הנגזרות החלקיות והרציפות שהפונקציה דיפרנציאבילית. צריך לבדוק את הגבול בהגדרה.",
              r"לשכוח את החילוק ב-$h$ בהגדרת הנגזרת החלקית: $\frac{f(h,0)}{h}=\frac{h^3/h^2}{h}=1$."],
    steps=[
        num(r"מהו $f'_x(0,0)$?", 1,
            r"$\frac{f(h,0)}{h}=\frac{h^3/h^2}{h}=1$."),
        num(r"מהו $f'_y(0,0)$?", 1,
            r"$\frac{f(0,k)}{k}=\frac{k^3/k^2}{k}=1$."),
        num(r"מהו הגבול של $-\dfrac{hk^2+kh^2}{\left(h^2+k^2\right)^{3/2}}$ לאורך $h=k>0$ (תשובה עשרונית, דיוק $0.001$)?", -0.7071,
            r"$-\frac{2h^3}{\left(2h^2\right)^{3/2}}=-\frac{2}{2^{3/2}}=-\frac1{\sqrt2}\approx-0.7071$.", tol=0.001),
        choice("מה מסקנת הפתרון לגבי הפונקציה ב-$(0,0)$?",
               "רציפה, שתי הנגזרות החלקיות קיימות, ואינה דיפרנציאבילית",
               ["רציפה ודיפרנציאבילית", "אינה רציפה", "אין לה נגזרות חלקיות"],
               r"הרציפות נובעת מהגבול $r\left(\cos^3\theta+\sin^3\theta\right)\to0$ והנגזרות החלקיות שוות $1$, אך הגבול בהגדרת הדיפרנציאביליות שונה מ-$0$.", pos=0),
    ])

add(3, "א",
    rubric=rub((r"מבחן המנה: $\left|\frac{a_{n+1}}{a_n}\right|\to\frac13$, ולכן $R=3$", 4),
               (r"הקצה $x=3$: הטור $\sum\frac{n}{n^2+1}$ מתבדר בהשוואה גבולית ל-$\sum\frac1n$", 3),
               (r"הקצה $x=-3$: הטור $\sum(-1)^n\frac{n}{n^2+1}$ מתכנס לפי לייבניץ (בתנאי)", 3),
               (r"תשובה: $R=3$ ותחום ההתכנסות $[-3,3)$", 2)),
    pitfalls=[r"לשכוח לבדוק את הקצוות ולהסתפק ב-$(-3,3)$.",
              r"להסיק שהטור מתכנס ב-$x=3$ מכך שהאיברים שואפים ל-$0$. הטור $\sum\frac{n}{n^2+1}$ דומה להרמוני ומתבדר."],
    steps=[
        num(r"מהו רדיוס ההתכנסות?", 3,
            r"היחס $\left|\frac{a_{n+1}}{a_n}\right|\to\frac13$, ולכן $R=3$."),
        num(r"בקצה $x=3$ משווים את $\sum\frac{n}{n^2+1}$ ל-$\sum\frac1n$. מהו הגבול של היחס בין האיברים?", 1,
            r"$\frac{n/(n^2+1)}{1/n}=\frac{n^2}{n^2+1}\to1$, ולכן שני הטורים מתנהגים אותו דבר, והטור ההרמוני מתבדר."),
        choice("מה קורה בשני הקצוות?",
               r"מתבדר ב-$x=3$ ומתכנס ב-$x=-3$",
               [r"מתכנס בשני הקצוות", r"מתבדר בשני הקצוות", r"מתכנס ב-$x=3$ ומתבדר ב-$x=-3$"],
               r"ב-$x=3$ הטור $\sum\frac{n}{n^2+1}$ מתבדר. ב-$x=-3$ הטור מחליף סימן עם איברים יורדים ל-$0$, ולכן מתכנס לפי לייבניץ.", pos=2),
        choice("מהו תחום ההתכנסות?",
               r"$[-3,3)$",
               [r"$(-3,3)$", r"$[-3,3]$", r"$(-3,3]$"],
               r"הקצה $-3$ כלול והקצה $3$ אינו כלול.", pos=0),
    ])

add(3, "ב",
    rubric=rub((r"הגדרת $F=z^3-3xyz-4$ ובדיקת תנאי משפט הפונקציה הסתומה: $F(2,1,-2)=0$ ו-$F_z(2,1,-2)\ne0$", 3),
               (r"חישוב $z'_x=\frac{yz}{z^2-yx}$ ו-$z'_x(2,1,-2)=-1$", 3),
               (r"חישוב $z'_y=\frac{xz}{z^2-yx}$ ו-$z'_y(2,1,-2)=-2$", 3),
               (r"גזירת $z'_x$ לפי $y$ כאשר $z$ תלוי ב-$y$, והצבה: $z''_{xy}(2,1)=1$", 4)),
    pitfalls=[r"לגזור את $z'_x$ לפי $y$ ולשכוח ש-$z$ עצמו תלוי ב-$y$ (האיבר $z'_y$ בכלל השרשרת).",
              r"לא לבדוק את התנאי $F_z\ne0$ בנקודה, שבלעדיו לא מובטחת הפונקציה הסתומה."],
    steps=[
        num(r"מהו $F_z(2,1,-2)=3z^2-3xy$?", 6,
            r"$3\cdot4-3\cdot2\cdot1=6\ne0$, ולכן תנאי משפט הפונקציה הסתומה מתקיים."),
        num(r"מהו $z'_x(2,1)$?", -1,
            r"$z'_x=\frac{yz}{z^2-yx}=\frac{-2}{4-2}=-1$."),
        num(r"מהו $z'_y(2,1)$?", -2,
            r"$z'_y=\frac{xz}{z^2-yx}=\frac{-4}{2}=-2$."),
        num(r"מהו $z''_{xy}(2,1)$?", 1,
            r"גוזרים את $\frac{yz}{z^2-yx}$ לפי $y$ עם $z'_y=-2$ ומקבלים $\frac{-4\cdot2-6\cdot(-2)}{2^2}=1$."),
    ])

add(4, "א",
    rubric=rub((r"בחירת ההחלפה $u=y-x$, $v=y+2x$ ותמונת התחום $1\le u\le4$, $6\le v\le8$", 4),
               (r"היעקוביאן ההפוך $-3$, ולכן $|J|=\frac13$", 3),
               (r"הצגת האינטגרל $\frac13\iint\frac uv\,du\,dv$ ופיצולו למכפלת אינטגרלים", 3),
               (r"תוצאה סופית: $\frac52\ln\frac43$", 2)),
    pitfalls=[r"לשכוח את היעקוביאן $\frac13$.",
              r"להחליף בין גבולות $u$ לגבולות $v$: הישרים $y-x=1,4$ הם $u$, והישרים $y+2x=6,8$ הם $v$."],
    steps=[
        num(r"מהו הדטרמיננט $\begin{vmatrix}-1&1\\2&1\end{vmatrix}$ של ההעתקה?", -3,
            r"$-1\cdot1-1\cdot2=-3$, ולכן $|J|=\frac13$."),
        choice(r"מהי תמונת התחום $D$ במשתנים $u=y-x$, $v=y+2x$?",
               r"$1\le u\le4,\quad6\le v\le8$",
               [r"$6\le u\le8,\quad1\le v\le4$", r"$1\le u\le4,\quad4\le v\le8$", r"$0\le u\le4,\quad6\le v\le8$"],
               r"הישרים $y=1+x$ ו-$y=4+x$ נותנים $u=1$ ו-$u=4$. הישרים $y=6-2x$ ו-$y=8-2x$ נותנים $v=6$ ו-$v=8$.", pos=0),
        num(r"מהו $\int_1^4u\,du$?", 7.5,
            r"$\left.\frac{u^2}{2}\right|_1^4=\frac{16-1}{2}=\frac{15}{2}$."),
        num(r"מהו ערך האינטגרל הכפול (תשובה עשרונית, דיוק $0.001$)?", 0.7192,
            r"$\frac13\cdot\frac{15}{2}\cdot\ln\frac86=\frac52\ln\frac43\approx0.7192$.", tol=0.001),
    ])

add(4, "ב",
    rubric=rub((r"נקודה קריטית פנימית: $\nabla f=0$ ב-$(0,0)$, שאינה בתחום", 3),
               (r"בניית פונקציית לגרנז' על השפה $(x-1)^2+(y-1)^2=1$ ופתרון המערכת: $1+\lambda=\pm\sqrt2$", 4),
               (r"הנקודות $\left(1\mp\frac1{\sqrt2},1\mp\frac1{\sqrt2}\right)$", 3),
               (r"מקסימום $2(\sqrt2-1)$ ומינימום $-2(\sqrt2+1)$", 3)),
    pitfalls=[r"לשכוח שהנקודה הקריטית $(0,0)$ מחוץ לתחום, ולכן אין אקסטרמום פנימי.",
              r"לבדוק רק אחת משתי נקודות לגרנז' ולהסיק מהן גם מקסימום וגם מינימום."],
    steps=[
        num(r"מהו הערך של $(x-1)^2+(y-1)^2$ בנקודה הקריטית $(0,0)$? (הנקודה בתחום רק אם הערך אינו עולה על $1$.)", 2,
            r"$(0-1)^2+(0-1)^2=2>1$, ולכן $(0,0)$ מחוץ לתחום ואין נקודה קריטית פנימית."),
        num(r"מהי הקואורדינטה $x$ של נקודת המקסימום על השפה (תשובה עשרונית, דיוק $0.001$)?", 0.2929,
            r"$x=1-\frac1{\sqrt2}\approx0.2929$ (וגם $y$ זהה).", tol=0.001),
        num(r"מהו ערך המקסימום (תשובה עשרונית, דיוק $0.001$)?", 0.8284,
            r"$2\left(\sqrt2-1\right)\approx0.8284$.", tol=0.001),
        num(r"מהו ערך המינימום (תשובה עשרונית, דיוק $0.001$)?", -4.8284,
            r"$-2\left(\sqrt2+1\right)\approx-4.8284$.", tol=0.001),
    ])

add(5, "א",
    rubric=rub((r"גזירה איבר-איבר: $f'(x)=\sum_{n=1}^{\infty}(-1)^{n+1}x^{2n-2}$", 3),
               (r"זיהוי טור הנדסי עם מנה $-x^2$ וסכומו $\frac1{1+x^2}$", 4),
               (r"אינטגרציה: $f(x)=\int_0^x\frac{dt}{1+t^2}$", 3),
               (r"תוצאה: $f(x)=\arctan x$", 2)),
    pitfalls=[r"לשכוח שהטור הנגזר מתחיל ב-$x^0$ ולטעות באינדקס ההתחלה.",
              r"לשכוח את הקבוע של האינטגרציה: $f(0)=0$ ולכן האינטגרל הוא מ-$0$ עד $x$."],
    steps=[
        choice(r"הטור הנגזר $\sum_{n=0}^{\infty}(-1)^n\left(x^2\right)^n$ הוא טור הנדסי. מהי המנה שלו?",
               r"$-x^2$",
               [r"$x^2$", r"$-x$", r"$\frac1{x^2}$"],
               r"האיבר הכללי הוא $\left(-x^2\right)^n$, ולכן המנה $-x^2$ והסכום $\frac1{1-(-x^2)}=\frac1{1+x^2}$.", pos=0),
        num(r"מהו $f'(1)=\frac1{1+x^2}$ ב-$x=1$ (תשובה עשרונית, דיוק $0.001$)?", 0.5,
            r"$\frac1{1+1}=\frac12$.", tol=0.001),
        choice(r"לאיזו פונקציה מתכנס הטור?",
               r"$\arctan x$",
               [r"$\ln(1+x)$", r"$\arcsin x$", r"$\ln\left(1+x^2\right)$"],
               r"$\int_0^x\frac{dt}{1+t^2}=\arctan x$.", pos=1),
        num(r"מהו סכום הטור ב-$x=1$ (תשובה עשרונית, דיוק $0.001$)?", 0.7854,
            r"$\arctan1=\frac\pi4\approx0.7854$.", tol=0.001),
    ])

add(5, "ב",
    rubric=rub((r"מערכת הנגזרות החלקיות והביטוי $y=\frac{x^2}{2}$", 3),
               (r"פתרון $6x\left(x^3-1\right)=0$: הנקודות $A(0,0)$ ו-$B\left(1,\frac12\right)$", 3),
               (r"נגזרות שניות ו-$D(A)=-36<0$: אוכף ב-$A$", 3),
               (r"$D(B)=6\cdot24-36>0$ ו-$z''_{xx}>0$: מינימום מקומי ב-$B$", 4)),
    pitfalls=[r"להציב $y=\frac{x^2}{2}$ ולשכוח את הפתרון $x=0$ כשמצמצמים ב-$x$.",
              r"לסווג את $A$ לפי סימן $z''_{xx}$ בלבד, שהוא $0$. כאן הדטרמיננט $D<0$ מכריע."],
    steps=[
        choice("מהן הנקודות הקריטיות?",
               r"$(0,0)$ ו-$\left(1,\frac12\right)$",
               [r"$(0,0)$ ו-$(1,2)$", r"$(0,0)$ ו-$(2,2)$", r"$\left(1,\frac12\right)$ בלבד"],
               r"מ-$3x^2-6y=0$ מקבלים $y=\frac{x^2}{2}$, ומ-$24y^2-6x=0$ מקבלים $6x\left(x^3-1\right)=0$, כלומר $x=0$ או $x=1$.", pos=1),
        num(r"מהו $D=z''_{xx}z''_{yy}-\left(z''_{xy}\right)^2$ ב-$A(0,0)$?", -36,
            r"$0\cdot0-(-6)^2=-36$."),
        num(r"מהו $D$ ב-$B\left(1,\frac12\right)$?", 108,
            r"$6\cdot24-36=108$."),
        choice("מה הסיווג של שתי הנקודות?",
               r"$A$ אוכף, ו-$B$ מינימום מקומי",
               [r"$A$ מינימום מקומי, ו-$B$ אוכף", r"$A$ אוכף, ו-$B$ מקסימום מקומי", r"שתי הנקודות הן אוכף"],
               r"ב-$A$ מתקבל $D<0$, אוכף. ב-$B$ מתקבל $D>0$ ו-$z''_{xx}=6>0$, מינימום מקומי.", pos=0),
    ])

exam = {
    "examCode": "22A-B",
    "examLabel": "מבחן סוף סמסטר א' 2022, מועד ב'",
    "year": 2022,
    "examDate": "08/03/2022",
    "sourceFile": "calculus-2/22A-B exam.pdf",
    "solutionFile": "calculus-2/22A-B solution.pdf",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
