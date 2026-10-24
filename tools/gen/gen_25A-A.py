# -*- coding: utf-8 -*-
"""Generator for tools/raw/25A-A.json -- calculus-2 (20252), semester A 2025, moed A (20/02/2025).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_25A-A.py

Source: sitting 25A-A. Exam: 3 pages, 5 questions of 25 points (a=12, b=13), solve 4 of 5.
Solution file: 10 pages. Q1 is handwritten on squared paper (author unclear), Q2 and Q3a typed, Q3b handwritten
on a tablet, Q4 and Q5 typed. Used as the key per GATE1 (handwritten keys allowed; no handwriting is cropped).
Exam header (lecturer names) is not transcribed.

Solution labelling (orchestrator ruling 2026-10-24): the key file is handwritten/mixed with no named author, so every
item is solutionSource "student-solution", official False. Fixes of key typos start with the words
"תיקון לפתרון שבקובץ:".

Transcription notes
- The text layers are garbled; everything is transcribed from page renders.
- Q1a: the handwritten key shows the path y=kx^3 (limit 4k/(3+2k^2)) and the two partials by definition. The
  line stating the conclusion is cursive; the conclusion written here (limit does not exist, so f is not continuous
  at the origin) follows directly from the key's own limit. Checked in tools/verify/25A-A/check.py.
- Q1b: the key's case analysis of the Lagrange system is transcribed as four cases; the key's values are
  f(0,+-3)=81 (max) and f(+-3,0)=-81 (min), and f(0,0)=0.
- Q2a: one item (two series), as printed in one part.
- Q4a: the key's hand sketch of the region is not copied; the region figure below is drawn by the transcriber
  from the bounds (tools/verify/25A-A/check.py).
- Q4a: the key's change of order gives the iterated integral over 0<=y<=x<=1.
- Q4b: the key states the Hessian classification in words ("saddle at (0,0), max at (-4,-2)").
- Q2b figure: drawn by the transcriber from the four printed lines.

Checks (tools/verify/25A-A/check.py, sympy + numeric): every limit, integral, Lagrange point, Hessian,
Jacobian, series test and coefficient matches the official answers. No holds.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "25A-A.json"


def Q(num, kind, topic, question, solution, part=None, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "solution": solution.strip("\n"),
         "solutionSource": "student-solution", "official": False, "confidence": "high"}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ===== Q1a =====
questions.append(Q(1, "computation", "limits_continuity", r"""נתונה פונקציה
$$f(x,y)=\begin{cases}\dfrac{4x^3y}{3x^6+2y^2}, & (x,y)\neq(0,0)\\[2mm] 0, & (x,y)=(0,0)\end{cases}$$
האם היא רציפה בנקודה $(x,y)=(0,0)$?
חשבו נגזרות חלקיות $\dfrac{\partial f}{\partial x}$ ו-$\dfrac{\partial f}{\partial y}$ בנקודה $(0,0)$.""",
r"""נבחר מסלול $y=kx^3$:
$$\lim_{\substack{x\to0\\y\to0}}\frac{4x^3y}{3x^6+2y^2}=\lim_{x\to0}\frac{4x^3\cdot kx^3}{3x^6+2k^2x^6}=\frac{4k}{3+2k^2}$$
הגבול תלוי ב-$k$, ולכן הגבול ב-$(0,0)$ לא קיים והפונקציה אינה רציפה ב-$(0,0)$.
נגזרות חלקיות לפי ההגדרה:
$$f'_x(0,0)=\lim_{\Delta x\to0}\frac{f(0+\Delta x,0)-f(0,0)}{\Delta x}=\lim_{\Delta x\to0}\frac{\frac{0}{3\Delta x^6}-0}{\Delta x}=\lim_{\Delta x\to0}\frac{0}{3\Delta x^7}=0$$
$$f'_y(0,0)=\lim_{\Delta y\to0}\frac{f(0,\Delta y)-f(0,0)}{\Delta y}=\lim_{\Delta y\to0}\frac{\frac{0}{2\Delta y^2}-0}{\Delta y}=0$$""", part="א", points=12))

# ===== Q1b =====
questions.append(Q(1, "computation", "absolute_extrema", r"""מצאו את הערך הגדול ביותר ואת הערך הקטן ביותר של הפונקציה $f(x,y)=y^4-x^4$ בתוך התחום $x^2+y^2\le9$.""",
r"""$f(x,y)=y^4-x^4$ ו-$g(x,y)=x^2+y^2-9=0$.
נקודות קריטיות בפנים התחום:
$$\begin{cases}f'_x=-4x^3=0\\ f'_y=4y^3=0\end{cases}\qquad M_0(0,0),\quad f(0,0)=0$$
על השפה, בשיטת לגראנז':
$$L(x,y,\lambda)=y^4-x^4+\lambda(x^2+y^2-9)$$
$$\begin{cases}L'_x=-4x^3+2\lambda x=0\\ L'_y=4y^3+2\lambda y=0\\ L'_\lambda=x^2+y^2-9=0\end{cases}$$
$$\begin{cases}-2x(2x^2-\lambda)=0\\ 2y(2y^2+\lambda)=0\\ x^2+y^2=9\end{cases}$$
מהמשוואה הראשונה $x=0$ או $\lambda=2x^2$, ומהשנייה $y=0$ או $\lambda=-2y^2$. ארבעה מקרים:
1. $x=0$ ו-$y^2=-\lambda$: מהאילוץ $y^2=9$, כלומר $y=\pm3$.
2. $x=0$ ו-$y=0$: האילוץ לא מתקיים ($0\ne9$), אין פתרון.
3. $\lambda=2x^2$ ו-$y=0$: מהאילוץ $x^2=9$, כלומר $x=\pm3$.
4. $\lambda=2x^2$ ו-$\lambda=-2y^2$: $x^2=-y^2$, אין פתרון.
נקודות החשודות: $M_1(3,0),\ M_2(-3,0),\ M_3(0,3),\ M_4(0,-3)$.
נחשב את ערכי הפונקציה בנקודות אלו ובנקודה הקריטית שבפנים התחום:
$$f(0,0)=0$$
מקסימום: $f(0,3)=3^4-0^4=81$ ו-$f(0,-3)=(-3)^4-0^4=81$.
מינימום: $f(3,0)=-81$ ו-$f(-3,0)=-81$.
הערך הגדול ביותר הוא $81$ והערך הקטן ביותר הוא $-81$.""", part="ב", points=13))

# ===== Q2a =====
questions.append(Q(2, "computation", "numeric_series", r"""בדקו התכנסות בהחלט, בתנאי או התבדרות של הטורים הבאים:
$$\sum_{n=2}^{\infty}\frac{(-1)^n}{n\cdot(\ln(n))^2}$$
$$\sum_{n=1}^{\infty}(-1)^n\left(\sqrt{n}-\sqrt{n-1}\right)$$""",
r"""**הטור הראשון.** תחילה נבדוק התכנסות בהחלט של הטור. נתבונן ב-
$$\sum_{n=2}^{\infty}\left|\frac{(-1)^n}{n(\ln n)^2}\right|=\sum_{n=2}^{\infty}\frac{1}{n(\ln n)^2}$$
נשתמש במבחן האינטגרל. נגדיר $f(x)=\frac{1}{x(\ln x)^2}$. ידוע ש-$f(x)$ חיובית, רציפה ויורדת עבור $x\ge2$. נתבונן ב-
$$\int_2^{\infty}\frac{1}{x(\ln x)^2}dx=\lim_{t\to\infty}\int_2^t\frac{1}{x(\ln x)^2}dx$$
נגדיר $u=\ln x$, אז $du=\frac{1}{x}dx$. כאשר $x=2$, $u=\ln2$. כאשר $x=t$, $u=\ln t$. לכן
$$\int_2^t\frac{1}{x(\ln x)^2}dx=\int_{\ln2}^{\ln t}\frac{1}{u^2}du=\left[-\frac{1}{u}\right]_{\ln2}^{\ln t}=-\frac{1}{\ln t}+\frac{1}{\ln2}$$
אז
$$\lim_{t\to\infty}\int_2^t\frac{1}{x(\ln x)^2}dx=\lim_{t\to\infty}\left(-\frac{1}{\ln t}+\frac{1}{\ln2}\right)=0+\frac{1}{\ln2}=\frac{1}{\ln2}$$
מכיוון שהאינטגרל מתכנס, הטור $\sum_{n=2}^{\infty}\frac{1}{n(\ln n)^2}$ מתכנס. לכן, הטור $\sum_{n=2}^{\infty}\frac{(-1)^n}{n(\ln n)^2}$ מתכנס בהחלט.
התשובה הסופית היא **הטור מתכנס בהחלט**.

**הטור השני.** נגדיר $a_n=(-1)^n\left(\sqrt{n}-\sqrt{n-1}\right)$. תחילה נבדוק התכנסות בהחלט.
$$|a_n|=\left|\sqrt{n}-\sqrt{n-1}\right|=\sqrt{n}-\sqrt{n-1}=\frac{\left(\sqrt{n}-\sqrt{n-1}\right)\left(\sqrt{n}+\sqrt{n-1}\right)}{\sqrt{n}+\sqrt{n-1}}=\frac{n-(n-1)}{\sqrt{n}+\sqrt{n-1}}=\frac{1}{\sqrt{n}+\sqrt{n-1}}.$$
כעת, נשווה זאת ל-$\frac{1}{\sqrt{n}}$:
$$\lim_{n\to\infty}\frac{\frac{1}{\sqrt{n}+\sqrt{n-1}}}{\frac{1}{\sqrt{n}}}=\lim_{n\to\infty}\frac{\sqrt{n}}{\sqrt{n}+\sqrt{n-1}}=\lim_{n\to\infty}\frac{1}{1+\sqrt{1-\frac{1}{n}}}=\frac{1}{1+\sqrt{1-0}}=\frac{1}{2}$$
מכיוון שהטור $\sum_{n=1}^{\infty}\frac{1}{\sqrt{n}}$ מתבדר (טור-$p$ עם $p=\frac{1}{2}\le1$), על פי מבחן ההשוואה הגבולי, גם הטור $\sum_{n=1}^{\infty}\frac{1}{\sqrt{n}+\sqrt{n-1}}$ מתבדר. לכן, הטור הנתון אינו מתכנס בהחלט.

כעת, נבדוק התכנסות בתנאי באמצעות מבחן לייבניץ. יש לנו
$$a_n=(-1)^n\left(\sqrt{n}-\sqrt{n-1}\right)=\frac{(-1)^n}{\sqrt{n}+\sqrt{n-1}}.$$
עלינו להראות ש-$b_n=|a_n|$ יורד ו-$\lim_{n\to\infty}b_n=0$. יש לנו
$$\lim_{n\to\infty}\frac{1}{\sqrt{n}+\sqrt{n-1}}=0.$$
כדי להראות ש-$b_n$ יורד, עלינו להראות ש-$b_{n+1}<b_n$, כלומר,
$$\sqrt{n+1}-\sqrt{n}<\sqrt{n}-\sqrt{n-1}\iff\sqrt{n+1}+\sqrt{n-1}<2\sqrt{n}$$
נעלה את שני האגפים בריבוע:
$$(n+1)+(n-1)+2\sqrt{(n+1)(n-1)}<4n\iff2n+2\sqrt{n^2-1}<4n$$
$$2\sqrt{n^2-1}<2n\iff\sqrt{n^2-1}<n\iff n^2-1<n^2\iff-1<0$$
מכיוון שזה נכון, יש לנו $b_{n+1}<b_n$, כך ש-$b_n$ יורד. לכן, על פי מבחן לייבניץ, הטור מתכנס בתנאי.
התשובה הסופית היא **מתכנס בתנאי**.""", part="א", points=12))

# ===== Q2b =====
questions.append(Q(2, "computation", "change_of_variables", r"""חשבו את האינטגרל
$$\iint_R(x-y)e^{x^2-y^2}\,dx\,dy$$
כאשר $R$ הוא התחום החסום על ידי הישרים $y=1-x,\ y=3-x,\ y=x+1,\ y=x-1$.""",
r"""נגדיר $u=x-y$ ו-$v=x+y$. אז $x=\frac{u+v}{2}$ ו-$y=\frac{v-u}{2}$. היעקוביאן הוא
$$\frac{\partial(x,y)}{\partial(u,v)}=\begin{vmatrix}\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\ \frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}\end{vmatrix}=\begin{vmatrix}\frac12&\frac12\\-\frac12&\frac12\end{vmatrix}=\frac14-\left(-\frac14\right)=\frac12$$
לכן, $|J|=\left|\frac12\right|=\frac12$. האזור $R$ חסום על ידי $y=1-x,\ y=3-x,\ y=x+1,\ y=x-1$.
![התחום R: ריבוע מסובב עם הקודקודים (0,1), (1,0), (2,1), (1,2)](images/exams/25A-A-Q2b-region.png)
הגבולות הופכים ל:
$$x+y=1\Rightarrow v=1,\quad x+y=3\Rightarrow v=3,$$
$$x-y=-1\Rightarrow u=-1,\quad x-y=1\Rightarrow u=1,$$
לכן האזור במישור $uv$ הוא
$$S=\{(u,v):-1\le u\le1,\ 1\le v\le3\}$$
לכן
$$\iint_R(x-y)e^{x^2-y^2}\,dx\,dy=\iint_Sue^{(x-y)(x+y)}|J|\,du\,dv=\int_{-1}^1\int_1^3ue^{uv}\frac12\,dv\,du$$
$$=\frac12\int_{-1}^1u\int_1^3e^{uv}\,dv\,du=\frac12\int_{-1}^1u\left[\frac1ue^{uv}\right]_{v=1}^{v=3}du=\frac12\int_{-1}^1\left(e^{3u}-e^u\right)du$$
$$=\frac12\left[\frac13e^{3u}-e^u\right]_{-1}^1=\frac12\left[\left(\frac13e^3-e\right)-\left(\frac13e^{-3}-e^{-1}\right)\right]$$
$$=\frac12\left[\frac13\left(e^3-e^{-3}\right)-\left(e-e^{-1}\right)\right]=\frac16\left(e^3-e^{-3}\right)-\frac12\left(e-e^{-1}\right)=\frac13\sinh3-\sinh1.$$
התשובה הסופית היא $I=\frac13\sinh(3)-\sinh(1)$.""", part="ב", points=13))

# ===== Q3a =====
questions.append(Q(3, "computation", "power_series", r"""עבור אילו ערכי $x$ הטור מתכנס (מצאו רדיוס התכנסות ותחום התכנסות):
$$\sum_{n=1}^{\infty}\frac{2^n}{\sqrt{5n^2+1}}(x-1)^n$$""",
r"""נשתמש במשפט דלמבר כדי למצוא את רדיוס ההתכנסות:
$$R=\lim_{n\to\infty}\frac{|a_n|}{|a_{n+1}|}=\lim_{n\to\infty}\left(\frac{2^n}{\sqrt{5n^2+1}}:\frac{2^{n+1}}{\sqrt{5(n+1)^2+1}}\right)=\lim_{n\to\infty}\frac{\sqrt{5(n+1)^2+1}}{2\sqrt{5n^2+1}}=\frac12$$
נבדוק כעת מה קורה בקצוות, כלומר כאשר $(x-1)=\frac12$ וכאשר $(x-1)=-\frac12$:
* אם $x-1=\frac12$ מקבלים את הטור $\sum_{n=1}^{\infty}\frac{1}{\sqrt{5n^2+1}}$. זה טור מתבדר לפי מבחן ההשוואה הגבולי עם הטור ההרמוני המתבדר $\sum_{n=1}^{\infty}\frac1n$.
* אם $x-1=-\frac12$ מקבלים את הטור $\sum_{n=1}^{\infty}\frac{(-1)^n}{\sqrt{5n^2+1}}$. הטור מתכנס לפי מבחן לייבניץ.

תשובה סופית:
רדיוס ההתכנסות: $R=\frac12$.
$$-\frac12\le x-1<\frac12$$
תחום ההתכנסות: $\frac12\le x<\frac32$.""", part="א", points=12))

# ===== Q3b =====
questions.append(Q(3, "proof", "chain_rule_identity", r"""הראו כי הפונקציה $z=y\cdot g(x^2-y^2)$ כאשר $g(t)$ גזירה עבור כל $t$ ו-$x,y\ne0$ מקיימת את המשוואה:
$$\frac1x\cdot\frac{\partial z}{\partial x}+\frac1y\cdot\frac{\partial z}{\partial y}=\frac{z}{y^2}.$$""",
r"""נסמן $u=x^2-y^2$ ונשתמש בכלל השרשרת:
$$\frac{\partial z}{\partial x}=y\cdot\frac{\partial g}{\partial x}=y\cdot\frac{dg}{du}\cdot\frac{\partial u}{\partial x}=y\cdot\frac{dg}{du}\cdot2x=2xy\cdot\frac{dg}{du}$$
$$\frac{\partial z}{\partial y}=g(u)+y\cdot\frac{\partial g}{\partial y}=g(u)+y\cdot\frac{dg}{du}\cdot\frac{\partial u}{\partial y}=g(u)+y\cdot\frac{dg}{du}\cdot(-2y)=g(u)-2y^2\frac{dg}{du}$$
נציב באגף שמאל של המשוואה:
$$\frac1x\cdot\frac{\partial z}{\partial x}+\frac1y\cdot\frac{\partial z}{\partial y}=\frac1x\cdot2xy\cdot\frac{dg}{du}+\frac1y\left[g(u)-2y^2\frac{dg}{du}\right]=$$
$$=2y\frac{dg}{du}+\frac{g(u)}{y}-2y\frac{dg}{du}=\frac{g(u)}{y}=\frac{z}{y^2}.$$
כנדרש.""", part="ב", points=13))

# ===== Q4a =====
questions.append(Q(4, "computation", "double_integrals", r"""נתון האינטגרל $\displaystyle\int_0^1\int_y^1\sin\left(\frac{\pi x^2}{2}\right)dx\,dy$
שרטטו את תחום האינטגרציה וחשבו את ערכו של האינטגרל, שימו לב לשינוי סדר האינטגרציה.""",
r"""כפי שניתן לראות, לא ניתן לחשב את האינטגרל כפי שהוא רשום, לא ניתן לבצע אינטגרציה לפי המשתנה $x$.
לכן, נשנה את סדר האינטגרציה, לשם כך, נשרטט את התחום:
![תחום האינטגרציה: המשולש שבין הצירים לישר האלכסון](images/exams/25A-A-Q4a-region.png)
לאחר שינוי סדר האינטגרל, נקבל את האינטגרל:
$$\int_0^1\int_y^1\sin\left(\frac{\pi x^2}{2}\right)dx\,dy=\int_0^1\int_0^x\sin\left(\frac{\pi x^2}{2}\right)dy\,dx$$
$$\int_0^1y\sin\left(\frac{\pi x^2}{2}\right)\Big|_0^xdx=\int_0^1x\sin\left(\frac{\pi x^2}{2}\right)dx=\int_0^{0.5}\sin(\pi t)\,dt$$
$$\frac{-\cos(\pi t)}{\pi}\Big|_0^{0.5}=\frac1\pi,\qquad t=\frac{x^2}{2},\ dt=x\,dx$$""", part="א", points=12))

# ===== Q4b =====
questions.append(Q(4, "computation", "local_extrema", r"""מצאו וסווגו את נקודות האקסטרמום של הפונקציה:
$$f(x,y)=(x^2-2y^2)e^{x-y}$$""",
r"""$$f_x(x,y)=2xe^{x-y}+(x^2-2y^2)e^{x-y}=0$$
$$f_y(x,y)=-4ye^{x-y}-(x^2-2y^2)e^{x-y}=0$$
לאחר חילוק בביטוי $e^{x-y}$ את שתי המשוואות, נקבל:
$$2x+x^2-2y^2=0$$
$$-4y-x^2+2y^2=0$$
לאחר חיבור המשוואות, נקבל: $2x-4y=0\leftrightarrow x=2y$
נציב במשוואה הראשונה ונקבל: $4y+4y^2-2y^2=0$
$$4y+2y^2=0\leftrightarrow y_1=0,\ y_2=-2\to x_1=0,\ x_2=-4$$
בסך הכול, קיבלנו את הנקודות: $(0,0),\ (-4,-2)$.
$$f_{xx}(x,y)=2e^{x-y}+2xe^{x-y}+2xe^{x-y}+(x^2-2y^2)e^{x-y}$$
$$f_{xy}(x,y)=-2xe^{x-y}-4ye^{x-y}-(x^2-2y^2)e^{x-y}$$
$$f_{yy}(x,y)=-4e^{x-y}+4ye^{x-y}+4ye^{x-y}+(x^2-2y^2)e^{x-y}$$
לאחר הצבה, נקבל: נקודת אוכף ב-$(0,0)$, מקסימום ב-$(-4,-2)$.""", part="ב", points=13))

# ===== Q5a =====
questions.append(Q(5, "computation", "gradient_directional", r"""מצאו את קצב ההשתנות המקסימלי של הפונקציה $f(x,y)=\sqrt{x^2+2y}$ בנקודה $(4,10)$. באיזה כיוון הוא מתקבל? נמקו את תשובתכם""",
r"""לפי ההגדרה, קצב ההשתנות של פונקציה בכיוון $\bar u=(a,b)$, $\|u\|=\sqrt{a^2+b^2}=1$ בנקודה $(x,y)$ שווה לנגזרת כיוונית
$$\frac{\partial f}{\partial\bar u}(x,y)=af'_x(x,y)+bf'_y(x,y)=\langle\bar u,\nabla f(x,y)\rangle.$$
זה אומר ש-
$$\frac{\partial f}{\partial\bar u}(x,y)=\|\nabla f(x,y)\|\cos\theta$$
איפה $\theta$ הוא זווית בין הווקטורים $\bar u$ ו-$\nabla f(x,y)$. לכן, $\frac{\partial f}{\partial\bar u}(x,y)$ המקסימלי מקבלים אם $\cos\theta=1$. זה אומר ש-$\frac{\partial f}{\partial\bar u}(x,y)$ המקסימלי בנקודה $(x,y)$ שווה ל-$\|\nabla f(x,y)\|$ והכיוון צריך להיות $u=\frac{\nabla f(x,y)}{\|\nabla f(x,y)\|}$.
במקרה שלנו
$$f'_x(x,y)=\frac{1}{2\sqrt{x^2+2y}}2x=\frac{x}{\sqrt{x^2+2y}}=\frac{4}{\sqrt{4^2+20}}=\frac46$$
$$f'_y(x,y)=\frac{1}{2\sqrt{x^2+2y}}2=\frac{1}{\sqrt{x^2+2y}}=\frac16$$
קצב ההשתנות המקסימלי של הפונקציה בנקודה $(4,10)$ שווה ל-
$$\|\nabla f(x,y)\|=\left\|\left(\frac46,\frac16\right)\right\|=\frac16\|(4,1)\|=\frac{\sqrt{17}}{6}$$
והכיוון המתאים הוא
$$u=\frac{\nabla f(x,y)}{\|\nabla f(x,y)\|}=\left(\frac{4}{\sqrt{17}},\frac{1}{\sqrt{17}}\right).$$""", part="א", points=12))

# ===== Q5b =====
questions.append(Q(5, "computation", "taylor_maclaurin", r"""פתחו את הפונקציה $f(x)=\ln(1+x^2)-e^{2x}$ לטור מקלורן. מהו רדיוס התכנסות הטור?
הסיקו את הערך של $f^{(6)}(0)$.""",
r"""$$\ln(1+x)=x-\frac12x^2+\frac13x^3-\cdots+(-1)^{n+1}\frac1nx^n+\cdots$$
לכן
$$\ln(1+x^2)=x^2-\frac12x^4+\frac13x^6-\cdots+(-1)^{n+1}\frac1nx^{2n}+\cdots$$
$$e^x=1+x+\frac12x^2+\cdots+\frac1{n!}x^n+\cdots$$
לכן
$$e^{2x}=1+2x+\frac12(2x)^2+\cdots+\frac1{n!}(2x)^n+\cdots=1+2x+2x^2+\cdots+\frac{2^n}{n!}x^n+\cdots$$
סוף-סוף, $f(x)=\sum_{k=1}^{\infty}(-1)^{k+1}\frac1kx^{2k}-\sum_{n=0}^{\infty}\frac{2^n}{n!}x^n=\sum_{n=0}^{\infty}a_nx^n$, איפה
$$a_n=\begin{cases}-\dfrac{2^n}{n!}, & n=1,3,5,\ldots\\[2mm]\left((-1)^{\frac n2+1}\cdot\dfrac2n-\dfrac{2^n}{n!}\right), & n=2,4,6,\ldots\end{cases}$$
טור של $e^{2x}$ מתכנס בכל $x\in(-\infty,+\infty)$, לכן טור של $\ln(1+x^2)-e^{2x}$ מתכנס אם ורק אם מתכנס טור של $\ln(1+x^2)$. אז רדיוס ההתכנסות $R$ של טור שלנו שווה לרדיוס ההתכנסות של $\ln(1+x^2)$. למדנו שרדיוס ההתכנסות הטור של פונקציה $\ln(1+x)$ שווה 1, זה אומר שגם **רדיוס ההתכנסות של טור שלנו $R=1$**.
לפי נוסחת מקלורן, מקדם $a_6$ של $x^6$ בטור שווה ל-$\frac{f^{(6)}(0)}{6!}$. זה אומר ש-
$$f^{(6)}(0)=a_6\cdot6!=\left(\frac13-\frac{2^6}{6!}\right)6!=\frac{2\cdot3\cdot4\cdot5\cdot6}{3}-2^6=240-64=176.$$""", part="ב", points=13))

# ---- rubric / pitfalls / steps (ai-verified); expected values are machine-checked in tools/verify/25A-A/steps_25A-A.py ----
IDS = "abcdefgh"


def opts(*vals):
    return [{"id": IDS[i], "type": "text", "value": v} for i, v in enumerate(vals)]


def rub(*items):
    return [{"text": t, "points": p} for t, p in items]


def add(num, part, **kw):
    for q in questions:
        if q["num"] == num and q.get("part") == part:
            q.update(kw)
            return
    raise KeyError((num, part))


add(1, "א",
    rubric=rub((r"בחירת מסלול $y=kx^3$ וחישוב הגבול $\frac{4k}{3+2k^2}$", 5),
               ("מסקנה: הגבול תלוי ב-$k$, לכן אינו קיים והפונקציה אינה רציפה בראשית", 2),
               ("$f'_x(0,0)=0$ לפי ההגדרה", 3),
               ("$f'_y(0,0)=0$ לפי ההגדרה", 2)),
    rubricSource="ai-verified",
    pitfalls=["לבדוק רק מסלולים ישרים $y=kx$: כולם נותנים גבול $0$, ולהסיק בטעות שהפונקציה רציפה.",
              "לחשוב שקיום שתי הנגזרות החלקיות מבטיח רציפות. כאן שתיהן קיימות ושוות $0$ והפונקציה בכל זאת אינה רציפה.",
              "לחשב נגזרת חלקית בנקודה בעזרת כללי גזירה רגילים במקום לפי ההגדרה, כי הפונקציה מוגדרת בנפרד בראשית."],
    steps=[
        {"type": "numeric", "prompt": r"לאורך המסלול $y=x^3$ (כלומר $k=1$), לאיזה ערך שואפת $f$ כאשר $x\to0$?",
         "answer": 0.8, "tol": 0.001,
         "explain": r"מציבים $y=x^3$ ומקבלים $\frac{4x^6}{3x^6+2x^6}=\frac45$ (sympy: $0.8$)."},
        {"type": "choice", "prompt": "לאורך $y=0$ הפונקציה שווה $0$, ולאורך $y=x^3$ היא שואפת ל-$0.8$. מה המסקנה לגבי הרציפות בראשית?",
         "options": opts("הגבול אינו קיים כי הוא תלוי במסלול, ולכן $f$ אינה רציפה ב-$(0,0)$",
                         "הגבול קיים ושווה $0$, ולכן $f$ רציפה ב-$(0,0)$",
                         "הגבול קיים ושווה $0.8$, ולכן $f$ רציפה ב-$(0,0)$",
                         "$f$ רציפה כי שתי הנגזרות החלקיות בראשית קיימות"),
         "correctId": "a",
         "explain": "שני מסלולים נותנים שני ערכים שונים, ולכן הגבול אינו קיים. קיום הנגזרות החלקיות אינו מבטיח רציפות."},
        {"type": "numeric", "prompt": "מהו $f'_x(0,0)$ לפי ההגדרה?", "answer": 0, "tol": 0,
         "explain": r"$f(\Delta x,0)=0$ לכל $\Delta x\neq0$, ולכן המנה היא $0$ והגבול $0$. גם $f'_y(0,0)=0$."},
    ],
    stepsSource="ai-verified")

add(1, "ב",
    rubric=rub(("נקודה קריטית בפנים התחום: $(0,0)$ עם $f(0,0)=0$", 2),
               ("בניית פונקציית לגראנז' ומערכת המשוואות על השפה $x^2+y^2=9$", 4),
               (r"פתרון ארבעת המקרים: $x=0$ או $\lambda=2x^2$, ו-$y=0$ או $\lambda=-2y^2$", 3),
               (r"חישוב הערכים בארבע הנקודות $(\pm3,0),(0,\pm3)$", 2),
               ("מסקנה: הערך הגדול ביותר $81$ והקטן ביותר $-81$", 2)),
    rubricSource="ai-verified",
    pitfalls=["לשכוח את הנקודות הקריטיות בפנים התחום ולבדוק רק את השפה.",
              "לחלק משוואה ב-$x$ או ב-$y$ ולאבד את הפתרונות שבהם הם שווים $0$.",
              "לקבל את המקרה $x=y=0$ כנקודה על השפה, למרות שהוא לא מקיים את האילוץ."],
    steps=[
        {"type": "choice", "prompt": "איזו שיטה משמש הפתרון כדי למצוא את הערך הגדול והקטן ביותר בתחום הסגור?",
         "options": opts("נקודות קריטיות בפנים התחום, וכופלי לגראנז' על השפה $x^2+y^2=9$",
                         "כופלי לגראנז' על השפה בלבד, כי בפנים התחום אין נקודות קריטיות",
                         "נקודות קריטיות בפנים התחום בלבד, ללא בדיקת השפה",
                         "מבחן הנגזרות השניות בלבד בכל נקודה בתחום"),
         "correctId": "a",
         "explain": "בפנים התחום יש נקודה קריטית אחת $(0,0)$ (לכן אי אפשר לדלג עליה), ובשפה מחפשים אקסטרמום בתנאי."},
        {"type": "numeric", "prompt": "כמה נקודות חשודות מתקבלות מפתרון מערכת לגראנז' על השפה?", "answer": 4, "tol": 0,
         "explain": "הנקודות הן $(3,0),(-3,0),(0,3),(0,-3)$ (sympy: ארבעה פתרונות)."},
        {"type": "numeric", "prompt": "מהו הערך של $f$ בנקודה $(0,3)$?", "answer": 81, "tol": 0,
         "explain": "$f(0,3)=3^4-0=81$, וזהו הערך הגדול ביותר."},
        {"type": "numeric", "prompt": "מהו הערך של $f$ בנקודה $(3,0)$?", "answer": -81, "tol": 0,
         "explain": "$f(3,0)=0-3^4=-81$, וזהו הערך הקטן ביותר (בדיקה על רשת צפופה אישרה $81$ ו-$-81$)."},
    ],
    stepsSource="ai-verified")

add(2, "א",
    rubric=rub((r"הטור הראשון: מבחן האינטגרל על $\frac1{x(\ln x)^2}$ עם ההצבה $u=\ln x$ והערך $\frac1{\ln2}$", 4),
               ("מסקנה: הטור הראשון מתכנס בהחלט", 2),
               (r"הטור השני: $|a_n|=\frac1{\sqrt n+\sqrt{n-1}}$ ומבחן השוואה גבולי עם $\frac1{\sqrt n}$ מראה שאינו מתכנס בהחלט", 3),
               ("הטור השני: תנאי לייבניץ (שאיפה ל-$0$ וירידה) ולכן מתכנס בתנאי", 3)),
    rubricSource="ai-verified",
    pitfalls=["להשתמש במבחן המנה על הטור הראשון: המנה שואפת ל-$1$ והמבחן אינו מכריע.",
              "להסיק התכנסות בהחלט מכך שלייבניץ מתקיים, בלי לבדוק את הטור בערכים מוחלטים.",
              r"לא לצמצם את $\sqrt n-\sqrt{n-1}$ בעזרת הצמוד, ולכן לא לראות שהטור מתנהג כמו $\frac1{\sqrt n}$."],
    steps=[
        {"type": "choice", "prompt": "באיזה מבחן משתמש הפתרון כדי לבדוק התכנסות בהחלט של הטור הראשון?",
         "options": opts(r"מבחן האינטגרל על $\frac{1}{x(\ln x)^2}$", "מבחן המנה", "מבחן לייבניץ על הטור בערכים מוחלטים", "מבחן השורש"),
         "correctId": "a",
         "explain": "מבחן המנה נותן גבול $1$ ואינו מכריע, ולייבניץ מתאים לטור מתחלף ולא לטור הערכים המוחלטים."},
        {"type": "numeric", "prompt": r"מהו הערך של $\int_2^{\infty}\frac{dx}{x(\ln x)^2}$ (עשרוני)?", "answer": 1.4427, "tol": 0.001,
         "explain": r"אחרי $u=\ln x$ מתקבל $\frac{1}{\ln2}\approx1.4427$, אינטגרל מתכנס, ולכן הטור מתכנס בהחלט."},
        {"type": "numeric", "prompt": r"בטור השני, לאיזה גבול שואף $\sqrt n\,(\sqrt n-\sqrt{n-1})$ כאשר $n\to\infty$?",
         "answer": 0.5, "tol": 0.001,
         "explain": r"זהו הגבול במבחן ההשוואה הגבולי עם $\frac1{\sqrt n}$; הוא $\frac12$, ולכן הטור בערכים מוחלטים מתבדר."},
        {"type": "choice", "prompt": "מה המסקנה לגבי הטור השני?",
         "options": opts("מתכנס בתנאי", "מתכנס בהחלט", "מתבדר", "אין אפשרות להכריע"),
         "correctId": "a",
         "explain": "בערכים מוחלטים הוא מתבדר, אך האיברים יורדים ושואפים ל-$0$ ולכן לפי לייבניץ הוא מתכנס."},
    ],
    stepsSource="ai-verified")

add(2, "ב",
    rubric=rub(("הצבה $u=x-y,\\ v=x+y$ וחישוב היעקוביאן $\\frac12$", 3),
               (r"מעבר לתחום $-1\le u\le1,\ 1\le v\le3$", 3),
               ("הצגת האינטגרנד כ-$ue^{uv}$ והכפלה ב-$|J|$", 2),
               ("אינטגרל פנימי לפי $v$ שנותן $e^{3u}-e^u$", 3),
               (r"אינטגרל חיצוני והתוצאה $\frac13\sinh3-\sinh1$", 2)),
    rubricSource="ai-verified",
    pitfalls=[r"לשכוח את גורם היעקוביאן $\frac12$, או להשתמש ב-$2$ (היעקוביאן ההפוך).",
              r"לבלבל בין הקווים: $x+y=1,3$ הם הגבולות של $v$ ו-$x-y=\pm1$ הם הגבולות של $u$.",
              r"לבצע את האינטגרל הפנימי $\int_1^3 ue^{uv}dv$ ולשכוח שהגורם $u$ מצטמצם עם המכנה $u$ של הפונקציה הקדומה, כך שמתקבל $e^{3u}-e^u$ ולא $\frac1u(e^{3u}-e^u)$."],
    steps=[
        {"type": "numeric", "prompt": r"עם $u=x-y$ ו-$v=x+y$, מהו $\left|\frac{\partial(x,y)}{\partial(u,v)}\right|$?", "answer": 0.5, "tol": 0.001,
         "explain": r"$x=\frac{u+v}2,\ y=\frac{v-u}2$, והדטרמיננטה היא $\frac14+\frac14=\frac12$."},
        {"type": "choice", "prompt": "מהו התחום במישור $uv$ המתאים לריבוע החסום בין הישרים הנתונים?",
         "options": opts(r"$-1\le u\le1,\ 1\le v\le3$", r"$1\le u\le3,\ -1\le v\le1$",
                         r"$0\le u\le2,\ 1\le v\le3$", r"$-1\le u\le1,\ -1\le v\le3$"),
         "correctId": "a",
         "explain": "$y=1-x$ ו-$y=3-x$ נותנים $v=1,3$; $y=x+1$ ו-$y=x-1$ נותנים $u=-1,1$."},
        {"type": "choice", "prompt": "איך נראה האינטגרנד $(x-y)e^{x^2-y^2}$ במשתנים החדשים?",
         "options": opts("$u\\,e^{uv}$", "$u\\,e^{u+v}$", "$e^{uv}$", "$u^2e^{uv}$"), "correctId": "a",
         "explain": "$x^2-y^2=(x-y)(x+y)=uv$, ולכן האינטגרנד הוא $ue^{uv}$."},
        {"type": "numeric", "prompt": "מהו ערך האינטגרל המבוקש (עשרוני, ארבע ספרות אחרי הנקודה)?", "answer": 2.1642, "tol": 0.001,
         "explain": r"$\frac13\sinh3-\sinh1\approx2.1642$, ותואם חישוב מספרי ישיר בקואורדינטות $x,y$."},
    ],
    stepsSource="ai-verified")

add(3, "א",
    rubric=rub((r"רדיוס ההתכנסות $R=\frac12$ בעזרת דלמבר", 4),
               (r"קצה ימני $x-1=\frac12$: הטור $\sum\frac1{\sqrt{5n^2+1}}$ מתבדר (השוואה ל-$\frac1n$)", 3),
               (r"קצה שמאלי $x-1=-\frac12$: הטור מתכנס לפי לייבניץ", 3),
               (r"תחום ההתכנסות $\frac12\le x<\frac32$", 2)),
    rubricSource="ai-verified",
    pitfalls=["לשכוח שמרכז הטור הוא $x=1$, ולכתוב את התחום סביב $0$.",
              r"להפוך את המנה בדלמבר ולקבל $R=2$ במקום $\frac12$.",
              "לא לבדוק את הקצוות, או להניח ששני הקצוות מתנהגים אותו הדבר."],
    steps=[
        {"type": "numeric", "prompt": "מהו רדיוס ההתכנסות $R$ של הטור?", "answer": 0.5, "tol": 0.001,
         "explain": r"$\lim\frac{|a_n|}{|a_{n+1}|}=\frac{1}{2}$ (sympy)."},
        {"type": "numeric", "prompt": r"בקצה $x-1=\frac12$ מתקבל $\sum\frac1{\sqrt{5n^2+1}}$. לאיזה גבול שואף $\frac{n}{\sqrt{5n^2+1}}$ (השוואה גבולית עם $\frac1n$)?",
         "answer": 0.4472, "tol": 0.001,
         "explain": r"הגבול $\frac1{\sqrt5}\approx0.4472$ חיובי וסופי, ולכן הטור מתבדר כמו הטור ההרמוני."},
        {"type": "choice", "prompt": "מהו תחום ההתכנסות?",
         "options": opts(r"$\frac12\le x<\frac32$", r"$\frac12<x\le\frac32$", r"$\frac12<x<\frac32$", r"$-\frac12\le x<\frac12$"),
         "correctId": "a",
         "explain": r"ב-$x=\frac12$ (כלומר $x-1=-\frac12$) הטור מתכנס לפי לייבניץ, וב-$x=\frac32$ הוא מתבדר."},
    ],
    stepsSource="ai-verified")

add(3, "ב",
    rubric=rub(("סימון $u=x^2-y^2$ ושימוש בכלל השרשרת", 3),
               ("$z_x=2xy\\,g'(u)$", 3),
               ("$z_y=g(u)-2y^2g'(u)$ בעזרת כלל המכפלה", 4),
               (r"הצבה באגף שמאל, צמצום והגעה ל-$\frac{z}{y^2}$", 3)),
    rubricSource="ai-verified",
    pitfalls=["לשכוח את כלל המכפלה ב-$z_y$: גם $y$ שלפני $g$ גזור.",
              r"לטעות בסימן של $\frac{\partial u}{\partial y}=-2y$ ולקבל $+2y^2g'(u)$, שאז הביטויים לא מצטמצמים.",
              "לרשום $g'(x)$ במקום $g'(x^2-y^2)$ ולא לסמן את הנגזרת של $g$ כפונקציה של $u$."],
    steps=[
        {"type": "choice", "prompt": r"מהי הנגזרת החלקית $\frac{\partial z}{\partial y}$ של $z=y\,g(x^2-y^2)$?",
         "options": opts(r"$g(u)-2y^2g'(u)$", r"$-2y^2g'(u)$", r"$g(u)+2y^2g'(u)$", r"$g(u)+2xy\,g'(u)$"),
         "correctId": "a",
         "explain": r"כלל המכפלה נותן $g(u)+y\,g'(u)\cdot(-2y)$ (נבדק ב-sympy עבור כמה פונקציות $g$)."},
        {"type": "order", "prompt": "סדרו את שלבי ההוכחה.",
         "lines": ["נסמן $u=x^2-y^2$ כך ש-$z=y\\,g(u)$ ונשתמש בכלל השרשרת.",
                   "$z_x=2xy\\,g'(u)$ ו-$z_y=g(u)-2y^2g'(u)$",
                   r"$\frac1xz_x+\frac1yz_y=2y\,g'(u)+\frac{g(u)}{y}-2y\,g'(u)$",
                   r"האיברים עם $g'(u)$ מצטמצמים ומתקבל $\frac{g(u)}{y}=\frac{z}{y^2}$, כנדרש."]},
        {"type": "findbug", "prompt": "באחת השורות בהוכחה יש טעות. מצאו אותה.",
         "lines": ["נסמן $u=x^2-y^2$ כך ש-$z=y\\,g(u)$ ונשתמש בכלל השרשרת.",
                   "$z_x=2xy\\,g'(u)$ ו-$z_y=g(u)+2y^2g'(u)$",
                   r"$\frac1xz_x+\frac1yz_y=2y\,g'(u)+\frac{g(u)}{y}-2y\,g'(u)$",
                   r"האיברים עם $g'(u)$ מצטמצמים ומתקבל $\frac{g(u)}{y}=\frac{z}{y^2}$, כנדרש."],
         "bugIndex": 1,
         "explain": r"הסימן של $z_y$ שגוי: $\frac{\partial u}{\partial y}=-2y$ ולכן האיבר הוא $-2y^2g'(u)$. עם הסימן השגוי האיברים לא מצטמצמים (נבדק ב-sympy)."},
    ],
    stepsSource="ai-verified")

add(4, "א",
    rubric=rub(("שרטוט התחום: המשולש $0\\le y\\le x\\le1$", 3),
               (r"החלפת הסדר ל-$\int_0^1\int_0^x\sin\left(\frac{\pi x^2}{2}\right)dy\,dx$", 3),
               (r"אינטגרל פנימי: $x\sin\left(\frac{\pi x^2}{2}\right)$", 2),
               (r"הצבה $t=\frac{x^2}{2}$ והגבולות $0$ עד $\frac12$", 2),
               (r"חישוב הערך $\frac1\pi$", 2)),
    rubricSource="ai-verified",
    pitfalls=[r"לנסות לאנטגרל את $\sin\left(\frac{\pi x^2}{2}\right)$ לפי $x$ ישירות: אין לו פונקציה קדומה אלמנטרית.",
              "גבולות שגויים אחרי ההחלפה, למשל $x\\le y\\le1$ או $0\\le x\\le y$, שנותנים תחום אחר וערך אחר.",
              r"לשכוח שהאינטגרל הפנימי $\int_0^x dy=x$ מוסיף גורם $x$ שמאפשר את ההצבה."],
    steps=[
        {"type": "choice", "prompt": r"מהו האינטגרל אחרי החלפת סדר האינטגרציה (התחום $0\le y\le x\le1$)?",
         "options": opts(r"$\int_0^1\int_0^x\sin\left(\frac{\pi x^2}{2}\right)dy\,dx$",
                         r"$\int_0^1\int_x^1\sin\left(\frac{\pi x^2}{2}\right)dy\,dx$",
                         r"$\int_0^1\int_0^y\sin\left(\frac{\pi x^2}{2}\right)dx\,dy$",
                         r"$\int_0^1\int_0^x\sin\left(\frac{\pi y^2}{2}\right)dy\,dx$"),
         "correctId": "a",
         "explain": r"לכל $x$ המשתנה $y$ רץ מ-$0$ עד $x$. שאר האפשרויות נותנות תחום אחר או אינטגרנד אחר (בדיקה מספרית: ערכים שונים מ-$\frac1\pi$)."},
        {"type": "numeric", "prompt": r"אחרי האינטגרל הפנימי מתקבל $\int_0^1x\sin\left(\frac{\pi x^2}{2}\right)dx$. עם $t=\frac{x^2}{2}$, מהו הגבול העליון של $t$?",
         "answer": 0.5, "tol": 0, "explain": r"עבור $x=1$ מתקבל $t=\frac12$, והגבול התחתון הוא $0$."},
        {"type": "numeric", "prompt": "מהו ערך האינטגרל (עשרוני)?", "answer": 0.3183, "tol": 0.001,
         "explain": r"$\int_0^{1/2}\sin(\pi t)\,dt=\frac1\pi\approx0.3183$ (נבדק מספרית בשני הסדרים)."},
    ],
    stepsSource="ai-verified")

add(4, "ב",
    rubric=rub(("גזירה חלקית ראשונה ורישום מערכת המשוואות", 3),
               ("חילוק ב-$e^{x-y}$ וקבלת $x=2y$ מחיבור המשוואות", 3),
               ("נקודות קריטיות $(0,0)$ ו-$(-4,-2)$", 2),
               ("נגזרות שניות", 2),
               ("סיווג: אוכף ב-$(0,0)$ ומקסימום מקומי ב-$(-4,-2)$", 3)),
    rubricSource="ai-verified",
    pitfalls=["להשמיט את כלל המכפלה כשגוזרים את $(x^2-2y^2)e^{x-y}$.",
              "בהצבת $x=2y$ לחלק ב-$y$ ולאבד את הפתרון $y=0$.",
              "לסווג לפי הסימן של $f_{xx}$ בלבד, בלי לבדוק את הדטרמיננטה $f_{xx}f_{yy}-f_{xy}^2$."],
    steps=[
        {"type": "numeric", "prompt": "אחרי $x=2y$ מציבים במשוואה $2x+x^2-2y^2=0$ ומקבלים $4y+2y^2=0$. מהו הפתרון השלילי של $y$?",
         "answer": -2, "tol": 0, "explain": "$2y(2+y)=0$ ולכן $y=0$ או $y=-2$, עם $x=0$ או $x=-4$."},
        {"type": "numeric", "prompt": "מהי הדטרמיננטה $f_{xx}f_{yy}-f_{xy}^2$ של ההסיאן בנקודה $(0,0)$?",
         "answer": -8, "tol": 0, "explain": "$f_{xx}(0,0)=2,\\ f_{yy}(0,0)=-4,\\ f_{xy}(0,0)=0$ (sympy), ולכן $-8$ ושלילי: נקודת אוכף."},
        {"type": "choice", "prompt": "מה סוג הנקודה הקריטית $(-4,-2)$?",
         "options": opts("מקסימום מקומי", "מינימום מקומי", "נקודת אוכף", "המבחן אינו מכריע"),
         "correctId": "a",
         "explain": "בנקודה זו הדטרמיננטה חיובית ו-$f_{xx}<0$ (sympy), ולכן מקסימום מקומי."},
    ],
    stepsSource="ai-verified")

add(5, "א",
    rubric=rub((r"הקשר $\frac{\partial f}{\partial\bar u}=\langle\bar u,\nabla f\rangle=\|\nabla f\|\cos\theta$ והמקסימום כאשר $\cos\theta=1$", 3),
               ("חישוב הנגזרות החלקיות", 3),
               (r"הצבה בנקודה: $\nabla f(4,10)=\left(\frac46,\frac16\right)$", 2),
               (r"קצב ההשתנות המקסימלי $\frac{\sqrt{17}}6$", 2),
               ("הכיוון: וקטור היחידה בכיוון הגרדיאנט", 2)),
    rubricSource="ai-verified",
    pitfalls=["לתת את הגרדיאנט עצמו כתשובה לכיוון בלי לנרמל אותו לוקטור יחידה.",
              "לשכוח את הגורם $2$ בגזירת $2y$ בתוך השורש.",
              "לבלבל בין הכיוון של העלייה המקסימלית לכיוון ההפוך, שבו קצב השינוי מינימלי."],
    steps=[
        {"type": "numeric", "prompt": r"מהו $f'_x(4,10)$ עבור $f=\sqrt{x^2+2y}$ (עשרוני)?", "answer": 0.6667, "tol": 0.001,
         "explain": r"$f'_x=\frac{x}{\sqrt{x^2+2y}}=\frac46=\frac23$ וגם $f'_y=\frac16$."},
        {"type": "numeric", "prompt": "מהו קצב ההשתנות המקסימלי בנקודה $(4,10)$ (עשרוני)?", "answer": 0.6872, "tol": 0.001,
         "explain": r"זהו אורך הגרדיאנט: $\sqrt{\left(\frac23\right)^2+\left(\frac16\right)^2}=\frac{\sqrt{17}}6\approx0.6872$."},
        {"type": "choice", "prompt": "באיזה כיוון (וקטור יחידה) מתקבל קצב ההשתנות המקסימלי?",
         "options": opts(r"$\left(\frac{4}{\sqrt{17}},\frac{1}{\sqrt{17}}\right)$", "$(4,1)$",
                         r"$\left(-\frac{4}{\sqrt{17}},-\frac{1}{\sqrt{17}}\right)$", r"$\left(\frac{1}{\sqrt{17}},\frac{4}{\sqrt{17}}\right)$"),
         "correctId": "a",
         "explain": "הכיוון הוא הגרדיאנט מנורמל. הווקטור $(4,1)$ אינו וקטור יחידה, ההפוך לו נותן נגזרת שלילית, והחלפת הרכיבים נותנת נגזרת קטנה יותר (sympy)."},
    ],
    stepsSource="ai-verified")

add(5, "ב",
    rubric=rub(("טור $\\ln(1+x^2)$ מהצבת $x^2$ בטור של $\\ln(1+x)$", 3),
               ("טור $e^{2x}$ מהצבת $2x$ בטור של $e^x$", 2),
               ("איחוד הטורים והמקדם הכללי $a_n$", 3),
               (r"רדיוס ההתכנסות $R=1$ (כי $e^{2x}$ מתכנס בכל $\mathbb R$)", 2),
               ("$f^{(6)}(0)=a_6\\cdot6!=176$", 3)),
    rubricSource="ai-verified",
    pitfalls=["להסיק שרדיוס ההתכנסות הוא $\\infty$ בגלל האקספוננט: הרדיוס נקבע לפי $\\ln(1+x^2)$ ושווה $1$.",
              "לשכוח להכפיל ב-$6!$ במעבר מהמקדם של $x^6$ אל הנגזרת.",
              r"לקחת את המקדם של $x^6$ ב-$\ln(1+x^2)$ כ-$\frac16$ במקום $\frac13$ ($x^6=(x^2)^3$ ולכן $n=3$)."],
    steps=[
        {"type": "numeric", "prompt": "מהו המקדם של $x^6$ בטור המקלורן של $\\ln(1+x^2)$ (עשרוני)?", "answer": 0.3333, "tol": 0.001,
         "explain": "$x^6=(x^2)^3$ ולכן המקדם הוא $\\frac13$ (sympy)."},
        {"type": "numeric", "prompt": "מהו המקדם $a_6$ של $x^6$ בטור המקלורן של $f$ (עשרוני)?", "answer": 0.2444, "tol": 0.001,
         "explain": r"$a_6=\frac13-\frac{2^6}{6!}=\frac{11}{45}\approx0.2444$."},
        {"type": "numeric", "prompt": "מהו רדיוס ההתכנסות של הטור?", "answer": 1, "tol": 0,
         "explain": r"הטור של $e^{2x}$ מתכנס בכל $\mathbb R$, ולכן הרדיוס שווה לרדיוס של $\ln(1+x^2)$, כלומר $1$."},
        {"type": "numeric", "prompt": "מהו $f^{(6)}(0)$?", "answer": 176, "tol": 0,
         "explain": r"$f^{(6)}(0)=6!\cdot a_6=720\cdot\frac{11}{45}=176$ (נבדק גם בגזירה ישירה ב-sympy)."},
    ],
    stepsSource="ai-verified")

exam = {
    "examCode": "25A-A",
    "examLabel": "מבחן סוף סמסטר א' תשפ\"ה, מועד א'",
    "year": 2025,
    "examDate": "20/02/2025",
    "sourceFile": "calculus-2/25A-A exam.pdf",
    "solutionFile": "calculus-2/student-solution-25A-A.pdf",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
