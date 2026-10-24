# -*- coding: utf-8 -*-
"""Generator for tools/raw/22A-A.json -- calculus-2 (20252), semester A 2022, moed A (06/02/2022).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_22A-A.py

Source: sitting 22A-A (orchestrator ruling: second letter = moed). Exam: 3 pages, 5 questions of 25 points, solve 4
of 5 (per-part points are not printed, so none are stored). Solution file: 10 pages; Q1-Q3b typed (pages 1-5),
Q4 on a tablet (pages 6-7), Q5 on squared paper (pages 8-10). Author unclear; handwritten keys accepted by the
orchestrator. Exam header (lecturer names) not transcribed. No handwriting is cropped.
The exam prints "z=f(x.y)" in Q3b (a typo for f(x,y)); transcribed as f(x,y).

FINAL-ANSWER ERROR in the key (Q4b): the key finds the nine interior critical points and the boundary critical
points x=0 and x=+-1/sqrt2, but never evaluates the boundary endpoints x=+-sqrt2 (y=0), where f=6. So the key's
"max f = 0" is wrong; the maximum is 6 at (+-sqrt2,0). Per the standing ruling, Q4b ships with the minimal fix,
solutionSource "solved", official False and the Hebrew prefix "הפתרון הרשמי עם תיקון" (sympy + dense-grid verified in
tools/verify/22A-A/check.py). Logged in docs/ASK_ADIR.md.

Slips in intermediate lines of the key, corrected (logged in docs/ASK_ADIR.md):
- Q1b: the key's first line writes "+y^2" where the exam has "+2y/3" (the next lines use 2y/3).
- Q2b: the key drops the division by h in f_x(0,0) (writes h^2 sin(1/|h|), should be h sin(1/|h|)) and writes
  "h->0" in the f_y line.
- Q3a: the key says the sequence sin(pi/sqrt n) decreases from n=2; it decreases from n=4 (a2<a3<a4, sympy/numeric).
  Leibniz needs only eventual monotonicity, so the conclusion stands.

Checks (tools/verify/22A-A/check.py, sympy + numeric): all other values match the key.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "22A-A.json"
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
questions.append(Q(1, "computation", "gradient_directional", r"""מצאו את הכיוון בו מתקבלת הנגזרת הכיוונית הגדולה ביותר של הפונקציה $f(x,y)=2\sin(2x+2y)$ בנקודה $\left(\dfrac{\pi}{2},\dfrac{\pi}{2}\right)$.
מה הוא ערכה של הנגזרת המקסימאלית?""",
r"""כידוע, הנגזרת הכיוונית תהי מקסימאלית בכיוון של ווקטור גרדיינט בנקודה. נחשב את הנגזרות החלקיות הנדרשות
$$\begin{cases}\dfrac{\partial f}{\partial x}=4\cos(2x+2y)\Big|_{\left(\frac{\pi}{2},\frac{\pi}{2}\right)}=4\\[2mm]\dfrac{\partial f}{\partial y}=4\cos(2x+2y)\Big|_{\left(\frac{\pi}{2},\frac{\pi}{2}\right)}=4\end{cases}\ \Longleftarrow\ \vec\nabla f\Big|_{\left(\frac{\pi}{2},\frac{\pi}{2}\right)}=(4,4)$$
וזה בדיוק הכיוון בו הנגזרת הכיוונית היא מקסימאלית (ניתן גם לומר שהכיוון נקבע ע"י הווקטור המנורמל $\dfrac{(4,4)}{\sqrt{32}}$). הערך המקסימלי של הנגזרת הכיוונית בנקודה הנתונה נקבע ע"י הנורמה של ווקטור גרדיינט בנקודה ששווה $\sqrt{32}$.""", part="א"))

# ===== Q1b =====
questions.append(Q(1, "proof", "chain_rule_identity", r"""הראו כי הפונקציה $z=\dfrac{y}{3x}+g(xy)$ כאשר $g(t)$ גזירה עבור כל $t$ ו-$x\neq0$ מקיימת את המשוואה:
$$x^2\frac{\partial z}{\partial x}-xy\frac{\partial z}{\partial y}+\frac{2y}{3}=0.$$""",
r"""נגדיר $t=xy$ ונרשום את הפונקציה בצורה $z(x,y)=\dfrac{y}{3x}+g(t)$. מכאן נובע ש-
$$\begin{cases}\dfrac{\partial z}{\partial x}=-\dfrac{y}{3x^2}+\dfrac{dg}{dt}\cdot\dfrac{\partial t}{\partial x}=-\dfrac{y}{3x^2}+g'(t)\,y\\[2mm]\dfrac{\partial z}{\partial y}=\dfrac{1}{3x}+\dfrac{dg}{dt}\cdot\dfrac{\partial t}{\partial y}=\dfrac{1}{3x}+g'(t)\,x\end{cases}$$
ואם נציב אותן במשוואה הנתונה, אז נקבל
$$x^2\frac{\partial z}{\partial x}-xy\frac{\partial z}{\partial y}+\frac{2y}{3}=x^2\left(-\frac{y}{3x^2}+g'(t)\,y\right)-xy\left(\frac{1}{3x}+g'(t)\,x\right)+\frac{2y}{3}=$$
$$=-\frac{2y}{3}+\frac{2y}{3}=0$$
ולכן המשוואה מתקיימת.""", part="ב"))

# ===== Q2a =====
questions.append(Q(2, "computation", "numeric_series", r"""בדקו התכנסות הטורים הבאים:
$$\sum_{n=2}^{\infty}\frac{\sin n}{n(\ln n)^2}$$
$$\sum_{n=1}^{\infty}\frac{(-1)^n+n}{3^n}$$""",
r"""**הטור הראשון.** נראה שהטור $\sum_{n=2}^{\infty}\dfrac{\sin n}{n(\ln n)^2}$ מתכנס בהחלט. הבה נבחין ש-
$$\left|\frac{\sin n}{n(\ln n)^2}\right|\le\frac{1}{n(\ln n)^2}$$
עכשיו נשתמש בקריטריון האינטגרל להתכנסות טורים חיוביים עבור להוכיח שהטור $\sum_{n=2}^{\infty}\dfrac{1}{n(\ln n)^2}$ מתכנס. אכן:
$$\int_2^{\infty}\frac{dx}{x(\ln x)^2}=\lim_{M\to\infty}\int_2^M\frac{dx}{x(\ln x)^2}=\lim_{M\to\infty}\int_2^M(\ln x)^{-2}\,\frac{dx}{x}$$
$$=\lim_{M\to\infty}\left.\left(\frac{-1}{\ln x}\right)\right|_2^M=\lim_{M\to\infty}\left(\frac{-1}{\ln M}+\frac{1}{\ln 2}\right)=\frac{1}{\ln 2}$$
לכן הטור $\sum_{n=2}^{\infty}\dfrac{1}{n(\ln n)^2}$ מתכנס והטור המקורי מתכנס בהחלט.

**הטור השני.** עבור הטור $\sum_{n=1}^{\infty}\dfrac{(-1)^n+n}{3^n}$, ברור שהטור $\sum_{n=1}^{\infty}\dfrac{(-1)^n}{3^n}$ הוא טור שמחליף סימן והסדרה $\left\{\dfrac{1}{3^n}\right\}_{n\in\mathbb{N}}$ היא מונוטונית יורדת לכן לפי משפט לייבניץ הטור $\sum_{n=1}^{\infty}\dfrac{(-1)^n}{3^n}$ מתכנס.
כעת, עבור הטור $\sum_{n=1}^{\infty}\dfrac{n}{3^n}$ יש לנו ש-
$$\lim_{n\to\infty}\frac{a_{n+1}}{a_n}=\lim_{n\to\infty}\frac{\frac{n+1}{3^{n+1}}}{\frac{n}{3^n}}=\lim_{n\to\infty}\frac{(n+1)\,3^n}{3^{n+1}n}=\frac{1}{3}\lim_{n\to\infty}\frac{n+1}{n}=\frac{1}{3}<1$$
ולפי קריטריון דלמבר הטור $\sum_{n=1}^{\infty}\dfrac{n}{3^n}$ מתכנס. מאז
$$\sum_{n=1}^{\infty}\frac{(-1)^n+n}{3^n}=\sum_{n=1}^{\infty}\frac{(-1)^n}{3^n}+\sum_{n=1}^{\infty}\frac{n}{3^n}$$
הטור המקורי מתכנס.""", part="א"))

# ===== Q2b =====
questions.append(Q(2, "computation", "partials_differentiability", r"""נתונה הפונקציה
$$f(x,y)=\begin{cases}\left(x^2+y^2\right)\sin\dfrac{1}{\sqrt{x^2+y^2}}, & (x,y)\neq(0,0)\\[2mm] 0, & (x,y)=(0,0)\end{cases}$$
* האם $f(x,y)$ רציפה ב-$(0,0)$?
* מצאו את $f'_x(0,0)$ ו-$f'_y(0,0)$.
* האם $f(x,y)$ דיפרנציאבילית ב-$(0,0)$?""",
r"""**רציפות.** נראה שהפונקציה רציפה ב-$(0,0)$:
$$\lim_{(x,y)\to(0,0)}\left(x^2+y^2\right)\sin\frac{1}{\sqrt{x^2+y^2}}=\lim_{r\to0}r^2\sin\frac{1}{r}=0=f(0,0)$$
כי $\sin\dfrac{1}{r}$ היא פונקציה חסומה.

**נגזרות חלקיות** ב-$(0,0)$:
$$f'_x(0,0)=\lim_{h\to0}\frac{f(h,0)-f(0,0)}{h}=\lim_{h\to0}h\sin\frac{1}{|h|}=0;$$
$$f'_y(0,0)=\lim_{k\to0}\frac{f(0,k)-f(0,0)}{k}=\lim_{k\to0}k\sin\frac{1}{|k|}=0.$$
(בשני המקרים: פונקציה שואפת ל-0 כפול פונקציה חסומה).

**דיפרנציאביליות.** נראה אם הפונקציה דיפרנציאבילית:
$$\lim_{(h,k)\to(0,0)}\frac{f(h,k)-f(0,0)-hf'_x(0,0)-kf'_y(0,0)}{\sqrt{h^2+k^2}}=\lim_{(h,k)\to(0,0)}\frac{\left(h^2+k^2\right)\sin\frac{1}{\sqrt{h^2+k^2}}}{\sqrt{h^2+k^2}}$$
$$=\lim_{(h,k)\to(0,0)}\sqrt{h^2+k^2}\,\sin\frac{1}{\sqrt{h^2+k^2}}=0$$
לכן הפונקציה היא דיפרנציאבילית ב-$(0,0)$.""", part="ב"))

# ===== Q3a =====
questions.append(Q(3, "computation", "power_series", r"""עבור אילו ערכי $x$ הטור מתכנס (מצאו רדיוס התכנסות ותחום התכנסות):
$$\sum_{n=1}^{\infty}(x+1)^n\,\sin\frac{\pi}{\sqrt{n}}$$""",
r"""נסמן $X=x+1$.
$$D=\lim_{n\to\infty}\left|\frac{a_n}{a_{n+1}}\right|=\lim_{n\to\infty}\left|\frac{\sin\left(\frac{\pi}{\sqrt{n}}\right)}{\sin\left(\frac{\pi}{\sqrt{n+1}}\right)}\right|=\lim_{n\to\infty}\left|\frac{\cos\left(\frac{\pi}{\sqrt{n}}\right)\cdot\frac{-\pi}{2n\sqrt{n}}}{\cos\left(\frac{\pi}{\sqrt{n+1}}\right)\cdot\frac{-\pi}{2(n+1)\sqrt{n+1}}}\right|$$
$$=\lim_{n\to\infty}\left|\frac{\cos\left(\frac{\pi}{\sqrt{n}}\right)\cdot(n+1)\sqrt{n+1}}{\cos\left(\frac{\pi}{\sqrt{n+1}}\right)\cdot n\sqrt{n}}\right|=1$$
אז רדיוס ההתכנסות הוא $R=1$.

**עבור $X=1$** הטור: $\sum_{n=1}^{\infty}\sin\left(\dfrac{\pi}{\sqrt{n}}\right)$.
נבצע מבחן השוואה השני עם הטור $b_n=\dfrac{1}{\sqrt{n}}$:
$$\lim_{n\to\infty}\frac{\sin\left(\frac{\pi}{\sqrt{n}}\right)}{\frac{1}{\sqrt{n}}}=\pi\in(0,\infty)$$
(ניתן בגבול פשוט להשתמש בגבול הידוע מאינפי 1).
כיוון שהטור $\sum_{n=1}^{\infty}\dfrac{1}{\sqrt{n}}$ מתבדר, גם הטור שלנו מתבדר.

**עבור $X=-1$** הטור: $\sum_{n=1}^{\infty}(-1)^n\sin\left(\dfrac{\pi}{\sqrt{n}}\right)$ זהו טור מחליף סימן ומתקיימים בו תנאי משפט לייבניץ:
הסדרה $a_n=\sin\left(\dfrac{\pi}{\sqrt{n}}\right)$ יורדת מ-$n=4$ והלאה שכן $\sin\left(\dfrac{\pi}{\sqrt{n}}\right)>\sin\left(\dfrac{\pi}{\sqrt{n+1}}\right)$ (כאשר $\frac{\pi}{\sqrt{n}}\le\frac{\pi}{2}$), ו-
$$\lim_{n\to\infty}\sin\left(\frac{\pi}{\sqrt{n}}\right)=0$$
כלומר, הטור מתכנס בתנאי.

בסך הכול, $-1\le x+1<1$, כלומר $-2\le x<0$.""", part="א"))

# ===== Q3b =====
questions.append(Q(3, "computation", "implicit_function", r"""נתונה המשוואה: $y^3+xz+y^2+e^z-3=0$
נמקו מדוע משוואה זו מגדירה פונקציה סתומה $z=f(x,y)$ בסביבת הנקודה $(1,1,0)$ וחשבו את משוואת המישור המשיק לפונקציה $z=f(x,y)$ בנקודה $(1,1)$.""",
r"""נגדיר את הפונקציה $F(x,y,z)=y^3+xz+y^2+e^z-3$ ונראה כי תנאי משפט הפונקציה הסתומה מתקיימים:
א. $F(1,1,0)=0$.
ב. $F(x,y,z)$ רציפה ובעלת נגזרות חלקיות רציפות בסביבת הנקודה $(1,1,0)$.
ג. $F_z(x,y,z)=e^z+x$, $F_z(1,1,0)\neq0$.
ולכן על פי משפט הפונקציה הסתומה קיימת סביבה של הנקודה $(1,1,0)$ כך שבסביבה זו מוגדרת פונקציה יחידה $f(x,y)$ המקיימת $F(x,y,f(x,y))=0$ כך ש:
$f(1,1)=0$, $f(x,y)$ רציפה ב-$(1,1)$ ו-$f(x,y)$ גזירה ומתקיים:
$$f_x(x,y)=-\frac{F_x(x,y,z)}{F_z(x,y,z)}=-\frac{z}{e^z+x},\qquad f_y(x,y)=-\frac{F_y(x,y,z)}{F_z(x,y,z)}=-\frac{3y^2+2y}{e^z+x}$$
$$f_y(1,1)=-\frac{5}{2},\qquad f_x(1,1)=0$$
משוואת המישור המשיק: $0=-\dfrac{5}{2}(y-1)-(z-0)$, כלומר: $0=5-5y-2z$.""", part="ב"))

# ===== Q4a =====
questions.append(Q(4, "computation", "change_of_variables", r"""חשבו את האינטגרל $\iint_De^{y-x}(2y+4)\,dx\,dy$ כאשר $D$ חסום ע"י הקווים הבאים: $y-x=1;\ y=x+2;\ y^2=-4x;\ y^2=-4x+9$""",
r"""נגדיר את ההעתקה $T$:
$$u=y-x,\qquad v=y^2+4x$$
(ב-$D$ מתקיים $y\ge0$.)
$$G=\left\{(u,v):\ 1\le u\le2,\ 0\le v\le9\right\},\qquad T(D)=G$$
$$J^{-1}=\begin{vmatrix}\frac{\partial u}{\partial x}&\frac{\partial u}{\partial y}\\ \frac{\partial v}{\partial x}&\frac{\partial v}{\partial y}\end{vmatrix}=\begin{vmatrix}-1&1\\4&2y\end{vmatrix}=-2y-4$$
$$|J|=\left|\frac{1}{-2y-4}\right|=\frac{1}{2y+4}$$
$$\iint_De^{y-x}(2y+4)\,dx\,dy=\iint_Ge^u\,du\,dv=\int_1^2e^u\,du\int_0^9dv=\left(\left.e^u\right|_1^2\right)\left(\left.v\right|_0^9\right)=9e(e-1).$$""", part="א"))

# ===== Q4b (corrected final answer) =====
questions.append(Q(4, "computation", "absolute_extrema", r"""מצאו אקסטרמומים מוחלטים של הפונקציה
$$f(x,y)=2x^4+y^4-x^2-2y^2$$
בתחום $\left\{(x,y):x^2+y^2\le2\right\}$""",
r"""**הפתרון הרשמי עם תיקון:** בפתרון הרשמי לא נבדקו נקודות הקצה $x=\pm\sqrt{2}$ של הפרמטריזציה של השפה (הנקודות $(\pm\sqrt{2},0)$), ולכן הערך המקסימלי $0$ שם אינו נכון. להלן הפתרון עם הוספת הבדיקה הזו (ערך המקסימום הנכון הוא $6$); יתר השורות כבפתרון הרשמי.

**בתוך התחום:**
$$\begin{cases}\dfrac{\partial f}{\partial x}=8x^3-2x=0\\[2mm]\dfrac{\partial f}{\partial y}=4y^3-4y=0\end{cases}\iff\begin{cases}x\left(4x^2-1\right)=0\\ y\left(y^2-1\right)=0\end{cases}$$
$$x\in\left\{0,\pm\tfrac{1}{2}\right\},\qquad y\in\{0,\pm1\}$$
מקבלים תשע נקודות חשודות: $A(0,0)$, $B(0,1)$, $C(0,-1)$, $D\left(\tfrac{1}{2},0\right)$, $E\left(\tfrac{1}{2},1\right)$, $F\left(\tfrac{1}{2},-1\right)$, $G\left(-\tfrac{1}{2},0\right)$, $H\left(-\tfrac{1}{2},1\right)$, $J\left(-\tfrac{1}{2},-1\right)$.
כולן מקיימות $x^2+y^2\le2$, ולכן כולן בתחום. הערכים:
$$f(A)=0,\qquad f(B)=f(C)=-1,\qquad f(D)=f(G)=-\frac{1}{8},\qquad f(E)=f(F)=f(H)=f(J)=-\frac{9}{8}$$
**על השפה** $x^2+y^2=2$, נציב $y^2=2-x^2$:
$$\tilde f(x)=2x^4+(2-x^2)^2-x^2-2\left(2-x^2\right)=3x^4-3x^2,\qquad-\sqrt{2}\le x\le\sqrt{2}$$
$$\tilde f'(x)=12x^3-6x=6x\left(2x^2-1\right)=0\ \Longrightarrow\ x=0,\ y=\pm\sqrt{2}$$
או
$$x=\pm\frac{1}{\sqrt{2}},\ y=\pm\sqrt{\frac{3}{2}}$$
$$f\left(0,\pm\sqrt{2}\right)=\tilde f(0)=0$$
$$f\left(\pm\frac{1}{\sqrt{2}},\pm\sqrt{\frac{3}{2}}\right)=\tilde f\left(\pm\frac{1}{\sqrt{2}}\right)=-\frac{3}{4}$$
**נקודות הקצה** של הקטע $-\sqrt{2}\le x\le\sqrt{2}$ (התיקון):
$$f\left(\pm\sqrt{2},0\right)=\tilde f\left(\pm\sqrt{2}\right)=3\cdot4-3\cdot2=6$$
**מסקנה:** בנקודות $E,F,H,J$ מתקבל מינימום מוחלט, $\min f=-\dfrac{9}{8}$.
בנקודות $\left(\pm\sqrt{2},0\right)$ מתקבל מקסימום מוחלט, $\max f=6$ (בפתרון הרשמי נרשם, בטעות, $\max f=0$ ב-$A$ ובנקודות $\left(0,\pm\sqrt{2}\right)$).""", part="ב",
    solutionSource="solved", official=False))

# ===== Q5a =====
questions.append(Q(5, "computation", "taylor_maclaurin", r"""פתחו לטור חזקות של $x$ סביב $0$ את הפונקציה :
$$f(x)=\frac{1}{x^2+x-2}$$""",
r"""נפרק זאת לשברים פשוטים:
$$\frac{1}{x^2+x-2}=\frac{1}{(x+2)(x-1)}=\frac{1}{3}\left(\frac{1}{x-1}+\frac{(-1)}{x+2}\right)=\frac{1}{3}\left(-\frac{1}{2}\cdot\frac{1}{1+\frac{x}{2}}-\frac{1}{1-x}\right)$$
נשתמש בנוסחאות:
$$\frac{1}{1+x}=\sum_{n=0}^{\infty}(-1)^nx^n,\quad|x|<1;\qquad\frac{1}{1-x}=\sum_{n=0}^{\infty}x^n,\quad|x|<1$$
$$\frac{1}{x^2+x-2}=\left(-\frac{1}{3}\right)\left[\sum_{n=0}^{\infty}\frac{1}{2}\left(\frac{x}{2}\right)^n(-1)^n+\sum_{n=0}^{\infty}x^n\right]=-\frac{1}{3}\sum_{n=0}^{\infty}\left(\frac{(-1)^n}{2^{n+1}}+1\right)x^n$$
הטור מתכנס ל-$f(x)$ עבור $-1<x<1$.""", part="א"))

# ===== Q5b =====
questions.append(Q(5, "computation", "local_extrema", r"""מצאו וסווגו את נקודות האקסטרמום של הפונקציה:
$$f(x,y)=xy^2-y^2-\frac{x^2}{2}-2x+3$$""",
r"""**שלב א: מציאת נקודות קריטיות.**
$$\begin{cases}f_x(x,y)=y^2-x-2=0&\text{(I)}\\ f_y(x,y)=2xy-2y=0&\text{(II)}\end{cases}$$
מ-(II): $2y(x-1)=0$.
* אם $y=0$ נקבל מ-(I) $x=-2$.
* אם $x=1$ נקבל $y=\pm\sqrt{3}$.

הנקודות הקריטיות: $(-2,0)$, $\left(1,\sqrt{3}\right)$, $\left(1,-\sqrt{3}\right)$.

**שלב ב: סיווג הנקודות הקריטיות.**
$$f_{xx}=-1,\qquad f_{yy}=2x-2,\qquad f_{xy}=2y$$
* הנקודה $(-2,0)$: $D=f_{xx}(-2,0)\cdot f_{yy}(-2,0)-f_{xy}^2(-2,0)=(-1)(-6)-0=6$. מתקיים $f_{xx}(-2,0)<0$ ו-$D>0$, לכן $(-2,0)$ נקודת מקסימום מקומי.
* הנקודה $\left(1,\sqrt{3}\right)$: $D=(-1)\cdot0-\left(2\sqrt{3}\right)^2=-12<0$, לכן נקודת אוכף.
* הנקודה $\left(1,-\sqrt{3}\right)$: $D=(-1)\cdot0-\left(-2\sqrt{3}\right)^2=-12<0$, לכן נקודת אוכף.""", part="ב"))

exam = {
    "examCode": "22A-A",
    "examLabel": "מבחן סוף סמסטר א' 2022, מועד א'",
    "year": 2022,
    "examDate": "06/02/2022",
    "sourceFile": "calculus-2/22A-A exam.pdf",
    "solutionFile": "calculus-2/22A-A solution.pdf",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
