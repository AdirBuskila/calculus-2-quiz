# -*- coding: utf-8 -*-
"""Generator for tools/raw/24B-A.json -- calculus-2 (20252), semester A, moed A, exam of 04/07/2024.
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24B-A.py

Sitting code 24B-A: the orchestrator's ruling is that the course runs in semester A and the second letter is the
moed. The source is the typed solution file dated 4.7.24 (5 pages), which carries each question and then its solution.
There is no separate exam file, so the question text is TRANSCRIBED FROM THE SOLUTION FILE (stated in sourceFile).
Five questions, 25 points each (a/b/c/d parts as printed). Header (institute logo, lecturer names) not transcribed.

Transcription notes
- The text layers are garbled; everything is transcribed from page renders.
- Q1c: the official solution labels both derivatives "f'_x" (the second line is meant to be f'_y); transcribed as f'_y.
- Q3d: the official solution lists M1(0,0), M2(2,0), M3, M4 and takes the max and min among them. (0,0) lies on the
  boundary circle (it satisfies (x-1)^2+y^2=1), so the Lagrange points cover it; the solution's value list is kept.
- All keys are official-pdf (typed solution); nothing is held.

Checks (tools/verify/24B-A/check.py, sympy + numeric): every limit, partial derivative, gradient, Hessian, Lagrange
point, tangent plane, radius and Maclaurin coefficient matches the official answers.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24B-A.json"


def Q(num, kind, topic, question, solution, part=None, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "solution": solution.strip("\n"),
         "solutionSource": "official-pdf", "official": True, "confidence": "high"}
    if part:
        q["part"] = part
    q.update(kw)
    return q


F1 = r"""$$f(x,y)=\begin{cases}\dfrac{yx^2}{2y^2+3x^4}, & (x,y)\neq(0,0)\\[2mm] 0, & (x,y)=(0,0)\end{cases}$$"""

questions = []

# ===== Q1a =====
questions.append(Q(1, "computation", "limits_continuity", "נתונה הפונקציה:\n" + F1 + "\nהאם $f(x,y)$ רציפה ב-$(0,0)$?",
r"""ננסה להתקרב אל הראשית לפי מסלול $y=x^2,\ x\to0$. מקבלים
$$\lim_{y=x^2,\,x\to0}\frac{yx^2}{2y^2+3x^4}=\lim_{x\to0}\frac{x^4}{2x^4+3x^4}=\frac{1}{5}\neq0=f(0,0),$$
לכן $f(x,y)$ **אינה רציפה** ב-$(0,0)$.""", part="א", points=7))

# ===== Q1b =====
questions.append(Q(1, "computation", "partials_differentiability", "נתונה הפונקציה:\n" + F1 + "\nמצאו את $f'_x(0,0)$ ו-$f'_y(0,0)$. האם $f(x,y)$ דיפרנציאבילית ב-$(0,0)$?",
r"""$$f'_x(0,0)=\lim_{h\to0}\frac{f(0+h,0)-f(0,0)}{h}=0.$$
$$f'_y(0,0)=\lim_{h\to0}\frac{f(0,0+h)-f(0,0)}{h}=0.$$
מכיוון שהפונקציה $f(x,y)$ היא לא רציפה ב-$(0,0)$, אז היא **אינה דיפרנציאבילית** ב-$(0,0)$.""", part="ב", points=7))

# ===== Q1c =====
questions.append(Q(1, "computation", "partials_differentiability", "נתונה הפונקציה:\n" + F1 + "\nמצאו את הדיפרנציאל השלם $df$ בנקודה $(1,1)$.",
r"""סביב הנקודה $(1,1)$:
$$f'_x(x,y)=\frac{2yx(2y^2+3x^4)-12x^3yx^2}{(2y^2+3x^4)^2},\qquad f'_x(1,1)=-\frac{2}{25}$$
$$f'_y(x,y)=\frac{x^2(2y^2+3x^4)-4y^2x^2}{(2y^2+3x^4)^2},\qquad f'_y(1,1)=\frac{1}{25}$$
מקבלים
$$df=f'_x(1,1)\,dx+f'_y(1,1)\,dy=\frac{-2\,dx+dy}{25}$$""", part="ג", points=11))

# ===== Q2a =====
questions.append(Q(2, "computation", "numeric_series", r"""בדקו התכנסות בהחלט, בתנאי או התבדרות של הטור הבא:
$$\sum_{n=1}^{\infty}(-1)^n\cdot\frac{3+\sin\sqrt{n}}{n^2}$$""",
r"""נסמן
$$a_n:=(-1)^n\frac{3+\sin\sqrt{n}}{n^2}$$
$$|a_n|=\frac{3+\sin\sqrt{n}}{n^2}\le\frac{4}{n^2}$$
הטור $\sum_{n=1}^{\infty}\frac{4}{n^2}$ מתכנס ($\alpha=2>1$), לכן לפי מבחן ההשוואה הטור $\sum|a_n|$ גם מתכנס.
זה אומר שהטור הנתון **מתכנס בהחלט**.""", part="א", points=10))

# ===== Q2b =====
questions.append(Q(2, "computation", "numeric_series", r"""בדקו התכנסות בהחלט, בתנאי או התבדרות של הטור הבא:
$$\sum_{n=1}^{\infty}\frac{(-1)^n}{(n+1)\ln(n+1)}$$""",
r"""נסמן $a_n:=\dfrac{1}{(n+1)\ln(n+1)}$.
נשים לב ש:
1. $n\in\mathbb{N},\ a_n>0$.
2. $n\in\mathbb{N},\ a_{n+1}=\dfrac{1}{(n+2)\ln(n+2)}<\dfrac{1}{(n+1)\ln(n+1)}=a_n$.
3. $\displaystyle\lim_{n\to\infty}a_n=\lim_{n\to\infty}\frac{1}{(n+1)\ln(n+1)}=0$.

מכאן נובע (לפי משפט לייבניץ) שהטור $\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{(n+1)\ln(n+1)}$ מתכנס.
האם הוא מתכנס בהחלט או בתנאי? נגדיר $f(x)=\dfrac{1}{(x+1)\ln(x+1)}$, היא פונקציה חיובית ומונוטונית יורדת עבור $x>1$.
$$\int_1^{\infty}\frac{dx}{(x+1)\ln(x+1)}=\left|\,t=\ln(x+1),\ dt=\frac{dx}{x+1}\right|=\int_{\ln2}^{\infty}\frac{dt}{t\ln t}=\infty$$
לפי מבחן אינטגרלי הטור $\sum\frac{1}{(n+1)\ln(n+1)}$ הוא מתבדר, מקבלים שהטור $\sum\frac{(-1)^n}{(n+1)\ln(n+1)}$ **מתכנס בתנאי**.""", part="ב", points=15))

# ===== Q3a =====
F3 = r"""נתונה הפונקציה: $f(x,y)=2x^2-y^2+1$."""
questions.append(Q(3, "computation", "gradient_directional", F3 + "\nמצאו את הכיוון בו קצב ההשתנות של הפונקציה $f(x,y)$ בנקודה $(2,3)$ הוא מקסימלי.",
r"""$$\nabla f(x,y)=(4x,-2y);$$
קצב ההשתנות של הפונקציה מקסימלי בכיוון של גרדיינט של הפונקציה בנקודה:
$$\nabla f(2,3)=(\mathbf{8},-\mathbf{6})$$""", part="א", points=4))

# ===== Q3b =====
questions.append(Q(3, "computation", "gradient_directional", F3 + "\nמה הוא הערך המקסימלי של נגזרת כיוונית של הפונקציה $f(x,y)$ בנקודה $(2,3)$?",
r"""הערך המקסימלי של נגזרת כיוונית של הפונקציה $f(x,y)$ בנקודה שווה לאורך של גרדיינט:
$$\|\nabla f(2,3)\|=\sqrt{8^2+(-6)^2}=\mathbf{10}.$$""", part="ב", points=4))

# ===== Q3c =====
questions.append(Q(3, "computation", "local_extrema", F3 + "\nמצאו את כל הנקודות הקריטיות של $f(x,y)$ וסווגו אותן.",
r"""נקודות קריטיות:
$$\nabla f(x,y)=0,$$
$$x=0,\ y=0,$$
$$A=f''_{xx}(0,0)=4,\quad B=f''_{xy}(0,0)=0,\quad C=f''_{yy}(0,0)=-2,$$
$$\Delta=AC-B^2=-8<0,$$
אז **נקודה $(0,0)$ היא נקודת אוכף** (ואינה נקודת קיצון מקומי).""", part="ג", points=7))

# ===== Q3d =====
questions.append(Q(3, "computation", "absolute_extrema", F3 + "\nמצאו את הערך המינימלי והערך המקסימלי של הפונקציה $f(x,y)$ בתחום $D=\\{(x,y):(x-1)^2+y^2\\le1\\}$.",
r"""מהסעיף הקודם נובע שבנקודה הקריטית היחידה $(0,0)$ אין קיצון מקומי.
נטפל בנקודות של שפת $\partial D=\{(x,y):(x-1)^2+y^2=1\}$:
נמצא נקודות של אקסטרמום בתנאי. נבנה פונקצית לגרנז':
$$L(x,y,\lambda)=2x^2-y^2+1-\lambda\left((x-1)^2+y^2-1\right)$$
$$\begin{cases}L'_x=4x-2\lambda(x-1)=0\\ L'_y=-2y-2\lambda y=0\\ (x-1)^2+y^2=1\end{cases}$$
נפתור את המערכת ונקבל נקודות חשודות $M_1(0,0),\ M_2(2,0),\ M_3\left(\frac{1}{3},\frac{\sqrt{5}}{3}\right),\ M_4\left(\frac{1}{3},-\frac{\sqrt{5}}{3}\right)$
ערך מקסימלי
$$f_{max}=f(2,0)=9.$$
ערך מינימלי
$$f_{min}=f\left(\frac{1}{3},\frac{\sqrt{5}}{3}\right)=f\left(\frac{1}{3},-\frac{\sqrt{5}}{3}\right)=\frac{2}{3}.$$""", part="ד", points=10))

# ===== Q4a =====
questions.append(Q(4, "computation", "gradient_directional", r"""מצאו את משוואת המישור המשיק למשטח $2x^2-y^2+z^2=5$ בנקודה $(1,-1,2)$.""",
r"""נסמן $F(x,y,z):=2x^2-y^2+z^2$
$$F'_x=4x,\quad F'_y=-2y,\quad F'_z=2z.$$
$$F'_x(1,-1,2)=4,\quad F'_y(1,-1,2)=2,\quad F'_z(1,-1,2)=4.$$
מישור משיק
$$\mathbf{4(x-1)+2(y+1)+4(z-2)=0}.$$""", part="א", points=10))

# ===== Q4b =====
questions.append(Q(4, "computation", "power_series", r"""עבור אילו ערכי $x$ הטור מתכנס (מצאו רדיוס התכנסות ותחום התכנסות):
$$\sum_{n=1}^{\infty}\frac{2^nn!}{(2n)!}x^n.$$""",
r"""נסמן $a_n:=\dfrac{2^nn!}{(2n)!}$
$$R=\lim_{n\to\infty}\left|\frac{a_n}{a_{n+1}}\right|=\lim_{n\to\infty}\frac{2^nn!}{(2n)!}\cdot\frac{(2n+2)!}{2^{n+1}(n+1)!}=\lim_{n\to\infty}\frac{(2n+2)(2n+1)}{2(n+1)}=\infty.$$
**רדיוס התכנסות $R=\infty$, תחום התכנסות $(-\infty,\infty)$**""", part="ב", points=15))

# ===== Q5a =====
F5 = r"""נתונה הפונקציה $f(x)=\ln(2x^2+3x+1)$."""
questions.append(Q(5, "computation", "taylor_maclaurin", F5 + "\nפתחו את הפונקציה $f(x)$ לטור מקלורן.",
r"""$$f(x)=\ln(2x^2+3x+1)=\ln\left((x+1)(2x+1)\right)=\ln(x+1)+\ln(2x+1).$$
עבור $-1<x\le1$
$$\ln(x+1)=\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}x^n$$
עבור $-1<2x\le1$
$$\ln(2x+1)=\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}(2x)^n$$
לכן עבור $-1/2<x\le1/2$
$$f(x)=\sum_{n=1}^{\infty}\frac{(-1)^{n+1}x^n}{n}+\sum_{n=1}^{\infty}\frac{(-1)^{n+1}(2x)^n}{n}=\sum_{n=1}^{\infty}\frac{(-1)^{n+1}(1+2^n)}{n}x^n$$""", part="א", points=8))

# ===== Q5b =====
questions.append(Q(5, "computation", "power_series", F5 + "\nמהו תחום התכנסות של הטור מהסעיף (א)?",
r"""תחום ההתכנסות הוא $\left(-\frac{1}{2},\frac{1}{2}\right]$:
$$\frac{1}{R}=\lim_{n\to\infty}\sqrt[n]{\frac{1+2^n}{n}}=\lim_{n\to\infty}2\cdot\frac{\sqrt[n]{2^{-n}+1}}{\sqrt[n]{n}}=2.$$""", part="ב", points=8))

# ===== Q5c =====
questions.append(Q(5, "computation", "taylor_maclaurin", F5 + "\nהסיקו את הערך של $f^{(5)}(0)$.",
r"""$$\frac{f^{(n)}(0)}{n!}=\frac{(-1)^{n+1}(1+2^n)}{n}$$
$$\frac{f^{(5)}(0)}{5!}=\frac{(-1)^{5+1}(1+2^5)}{5}=\frac{33}{5}$$
$$f^{(5)}(0)=33\cdot4!=792.$$""", part="ג", points=9))

exam = {
    "examCode": "24B-A",
    "examLabel": "מבחן סוף סמסטר ב' תשפ\"ד, מועד א'",
    "year": 2024,
    "examDate": "04/07/2024",
    "sourceFile": "calculus-2/24B-A typed solution 4.7.24 (question embedded; question transcribed from the solution file, no separate exam file)",
    "solutionFile": "calculus-2/24B-A typed solution 4.7.24",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
