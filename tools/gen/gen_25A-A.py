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
![תחום האינטגרציה: המשולש $0\le y\le x\le1$](images/exams/25A-A-Q4a-region.png)
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
