# -*- coding: utf-8 -*-
"""Generator for tools/raw/22A-B.json -- calculus-2 (20252), semester A 2022, moed B (08/03/2022).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_22A-B.py

Source: sitting 22A-B (orchestrator ruling: second letter = moed). Exam: 3 pages, 5 questions of 25 points, solve 4
of 5 (per-part points are not printed on this exam, so none are stored). Solution file: 8 pages; Q1-Q3b typed
(pages 1-4), Q4 on a tablet (pages 5-6), Q5 on squared paper (pages 7-8). Author unclear; handwritten keys accepted by
the orchestrator. Exam header (lecturer names) not transcribed. No handwriting is cropped.

HOLD
- Q3a: the solution file has no solution for it (page 4 starts with Q3b). Held, reason no-key; the verify script
  computes R=3 and the endpoints as a hint for the solver.

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
SRC = "lecturer-solution"   # solution file of unclear authorship, accepted as the key
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

# ===== Q3a (HELD: no key) =====
questions.append({
    "num": 3, "part": "א", "kind": "computation", "topic": "power_series",
    "question": r"""עבור אילו ערכי $x$ הטור מתכנס (מצאו רדיוס התכנסות ותחום התכנסות):
$$\sum_{n=1}^{\infty}\frac{n}{\left(n^2+1\right)\cdot3^n}\,x^n$$""",
    "hold": "no-key: the solution file for this sitting has no solution for Q3a (its page 4 starts with Q3b)",
})

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
