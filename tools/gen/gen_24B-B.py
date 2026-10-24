# -*- coding: utf-8 -*-
"""Generator for tools/raw/24B-B.json -- calculus-2 (20252), semester B 2024, moed B (30/07/2024).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24B-B.py

Source: sitting 24B-B (orchestrator's code for the typed solution dated 30.7.24). There is NO separate exam file:
the typed solution file (6 pages) embeds each question above its solution, so the questions are transcribed from
the solution file. Question points are as printed there: Q1 7+7+11, Q2 10+15, Q3 4+4+7+10, Q4 10+15, Q5 8+8+7.
Header with institution only; no lecturer names are transcribed.

Transcription notes
- The text layers are garbled; everything is transcribed from page renders.
- Q2: the file prints the instruction line twice; transcribed once. Q3 has four parts (a-d).
- Q3a: the key only gives the gradient at (2,-1) and says the rate is maximal in its direction; transcribed as is.
- Q5: the three parts (a, b, c) are separate items; the key solves a and b together and then c.

Solver decisions (docs/ASK_ADIR.md; tools/verify/24B-B/solve_24B-B.py, sympy + dense grid + partial sums)
- Q3d (intermediate slip, final answer right): the key's edge line f(1,y) = 1-2(y+1)-2+3 = -2y is corrected silently to
  1-2(y+1)+3 = 2-2y, and "(0,0) is the unique critical point" to (0,-1) (part c). The interior point (0,-1), f=3, is
  listed with the candidates. Max 6 at B(1,-2) and min 0 at A(1,1) are the key's. Label kept (lecturer-solution).
- Q4b (wrong final answer): the key's final domain "[-1/2; 3/2)" has the wrong left endpoint (1 - 1/2 = 1/2), and its
  x=3/2 line says the series converges, although 1/sqrt(n+4) ~ 1/sqrt(n) diverges. Minimal fix: x=3/2 diverges,
  domain [1/2, 3/2). solutionSource "solved", official False, prefix "הפתרון הרשמי עם תיקון".

Checks (tools/verify/24B-B/check.py, sympy + numeric): all other answers match the key.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24B-B.json"


def Q(num, kind, topic, question, solution, part=None, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "solution": solution.strip("\n"),
         "solutionSource": "lecturer-solution", "official": True, "confidence": "high"}
    if part:
        q["part"] = part
    q.update(kw)
    return q


F1 = r"""נתונה הפונקציה:
$$f(x,y)=\begin{cases}\dfrac{x^3y}{x^2+y^2}, & (x,y)\neq(0,0)\\[2mm] 0, & (x,y)=(0,0)\end{cases}$$
"""

questions = []

# ===== Q1 =====
questions.append(Q(1, "computation", "partials_differentiability", F1 + r"""מצאו את $f'_x(1,0)$ ו-$f'_y(1,0)$.""",
r"""סביב נקודה $(1,0)$:
$$f'_x(x,y)=\frac{3x^2y(x^2+y^2)-2x^4y}{(x^2+y^2)^2},\qquad f'_x(1,0)=0$$
$$f'_y(x,y)=\frac{x^3(x^2+y^2)-2y^2x^3}{(x^2+y^2)^2},\qquad f'_y(1,0)=1$$""", part="א", points=7))

questions.append(Q(1, "computation", "partials_differentiability", F1 + r"""מצאו את $f'_x(0,0)$ ו-$f'_y(0,0)$.""",
r"""$$f'_x(0,0)=\lim_{h\to0}\frac{f(0+h,0)-f(0,0)}{h}=0.$$
$$f'_y(0,0)=\lim_{h\to0}\frac{f(0,0+h)-f(0,0)}{h}=0.$$""", part="ב", points=7))

questions.append(Q(1, "computation", "partials_differentiability", F1 + r"""האם $f(x,y)$ דיפרנציאבילית ב-$(0,0)$? האם $f(x,y)$ רציפה ב-$(0,0)$?""",
r"""נבדוק דיפרנציאביליות
$$\lim_{(\Delta x,\Delta y)\to(0,0)}\frac{f(0+\Delta x,0+\Delta y)-f(0,0)-f'_x(0,0)\Delta x-f'_y(0,0)\Delta y}{\sqrt{\Delta x^2+\Delta y^2}}$$
$$=\lim_{(\Delta x,\Delta y)\to(0,0)}\frac{\frac{\Delta x^3\Delta y}{\Delta x^2+\Delta y^2}}{\sqrt{\Delta x^2+\Delta y^2}}=$$
$$(\Delta x=r\cos\varphi,\ \Delta y=r\sin\varphi)$$
$$=\lim_{r\to0}\frac{r^4\cos^3\varphi\sin\varphi}{r^3}=\lim_{r\to0}r\cos^3\varphi\sin\varphi=0,$$
(כי $|\cos^3\varphi\sin\varphi|\le1$ חסומה ו-$r\to0$)
לפי ההגדרה של דיפרנציאביליות $f(x,y)$ דיפרנציאבילית בנקודה $(0,0)$.
ולכן $f(x,y)$ רציפה בנקודה $(0,0)$.""", part="ג", points=11))

# ===== Q2 =====
questions.append(Q(2, "computation", "numeric_series", r"""בדקו התכנסות בהחלט, בתנאי או התבדרות של הטור הבא:
$$\sum_{n=1}^{\infty}\frac{\cos(\pi n)\cdot(n^2+3\ln n)}{(n+1)(n+2)}.$$""",
r"""נסמן
$$a_n:=\frac{\cos(\pi n)\cdot(n^2+3\ln n)}{(n+1)(n+2)}$$
$$|a_n|=\frac{n^2+3\ln n}{(n+1)(n+2)}$$
$$\lim_{n\to\infty}|a_n|=\lim_{n\to\infty}\frac{n^2+3\ln n}{(n+1)(n+2)}=\lim_{n\to\infty}\frac{1+\frac{3\ln n}{n}}{1+\frac3n+\frac{2}{n^2}}=1\not\to0$$
לכן גם $\lim_{n\to\infty}a_n\not\to0$
תנאי הכרחי להתכנסות טורים לא מתקיים, אזי **טור מתבדר**""", part="א", points=10))

questions.append(Q(2, "computation", "numeric_series", r"""בדקו התכנסות בהחלט, בתנאי או התבדרות של הטור הבא:
$$\sum_{n=1}^{\infty}(-1)^n\frac{1+\frac{1}{\sqrt n}}{n^3};$$""",
r"""נסמן $a_n:=(-1)^n\dfrac{1+\frac{1}{\sqrt n}}{n^3}$
$$0\le|a_n|=\frac{1+\frac{1}{\sqrt n}}{n^3}\le\frac{2}{n^3}$$
$\sum_{n=1}^{\infty}\frac{1}{n^3}$ מתכנס, לכן, לפי משפט ההשוואה, הטור $\sum_{n=1}^{\infty}|a_n|$ גם מתכנס, מקבלים שהטור $\sum(-1)^n\frac{1+\frac{1}{\sqrt n}}{n^3}$ **מתכנס בהחלט**.""", part="ב", points=15))

# ===== Q3 =====
F3 = r"""נתונה הפונקציה: $f(x,y)=x^2-2x(y+1)+3$.
"""
questions.append(Q(3, "computation", "gradient_directional", F3 + r"""מצאו את הכיוון בו קצב ההשתנות של הפונקציה $f(x,y)$ בנקודה $(2,-1)$ הוא מקסימלי.""",
r"""$$\nabla f(x,y)=(2x-2(y+1),-2x);$$
קצב ההשתנות של הפונקציה מקסימלי בכיוון של גרדיינט הפונקציה בנקודה:
$$\nabla f(2,-1)=(4,-4)$$""", part="א", points=4))

questions.append(Q(3, "computation", "gradient_directional", F3 + r"""מצאו את הנגזרת הכיוונית של הפונקציה $f(x,y)$ בנקודה $(2,-1)$ בכיוון $(-3,4)$.""",
r"""$$\vec a=(-3,4)$$
$$\|\vec a\|=\sqrt{9+16}=5,$$
וקטור יחידה שמתארת אותו כיוון הוא
$$\vec a^0=\left(-\frac35,\frac45\right)$$
לכן
$$\frac{\partial f}{\partial\vec a}(2,-1)=\vec\nabla f(2,-1)\cdot\vec a^0=4\cdot\left(-\frac35\right)-4\cdot\frac45=-\frac{28}{5}=-5.6$$""", part="ב", points=4))

questions.append(Q(3, "computation", "local_extrema", F3 + r"""מצאו את כל הנקודות הקריטיות של $f(x,y)$ וסווגו אותן.""",
r"""נקודות קריטיות:
$$\nabla f(x,y)=0,$$
$$x=0,\ y=-1,$$
$$A=f''_{xx}(0,-1)=2,\quad B=f''_{xy}(0,-1)=-2,\quad C=f''_{yy}(0,-1)=0,$$
$$\Delta=AC-B^2=-4<0,$$
אז **נקודה $(0,-1)$ היא נקודת אוכף** (ואינה נקודת קיצון מקומי).""", part="ג", points=7))

questions.append(Q(3, "computation", "absolute_extrema", F3 + r"""מצאו את הערך המינימלי והערך המקסימלי של הפונקציה $f(x,y)$ בתחום
$D=\{(x,y):-2\le y\le x\le1\}$.""",
r"""מהסעיף הקודם נובע שבנקודה הקריטית היחידה $(0,-1)$, שנמצאת בתוך $D$, אין קיצון מקומי; ערך הפונקציה בה הוא $f(0,-1)=3$.
נטפל בנקודות של שפת $\partial D$, זה משולש $ABC$ שבו $A(1,1)$; $B(1,-2)$, $C(-2,-2)$.
1) נמצא נקודות קריטיות בקטע $[A,B]$:
$$x=1,\ y\in[-2,1]$$
$$f(1,y)=1-2(y+1)+3=2-2y$$
פונקציה ליניארית, ולכן הנקודות הקריטיות הן $A(1,1)$ ו-$B(1,-2)$.
2) נמצא נקודות קריטיות בקטע $[B,C]$:
$$x\in[-2,1];\ y=-2.$$
$$f(x,-2)=x^2+2x+3=g(x).$$
$$g'(x)=2x+2,\quad x_0=-1$$
נקודות קריטיות $B(1,-2)$, $C(-2,-2)$, $D(-1,-2)$.
3) נמצא נקודות קריטיות בקטע $[A,C]$:
$$y=x,\ x\in[-2,1]$$
$$f(x,x)=-x^2-2x+3=:h(x)$$
$$h'(x)=-2x-2=0\ \Rightarrow\ x_1=-1,\ y_1=-1$$
נקודות קריטיות $A(1,1)$, $C(-2,-2)$, $E(-1,-1)$.
$$f(A)=0,\ f(B)=6,\ f(C)=3,\ f(D)=2,\ f(E)=4,\ f(0,-1)=3$$
ערך מקסימלי
$$f_{max}=f(1,-2)=6.$$
ערך מינימלי
$$f_{min}=f(1,1)=0.$$""", part="ד", points=10))

# ===== Q4 =====
questions.append(Q(4, "computation", "chain_rule_identity", r"""חשבו את $\dfrac{\partial z}{\partial x},\dfrac{\partial z}{\partial y}$ בנקודה $x_0=\pi,\ y_0=-\pi$ כאשר
$$z(u,v)=2uv+3v^2;$$
$$u=\cos(x-3y);$$
$$v(\pi,-\pi)=2,\quad v'_x(\pi,-\pi)=5,\quad v'_y(\pi,-\pi)=4.$$""",
r"""$$z'_x=z'_u\cdot u'_x+z'_v\cdot v'_x=2v\cdot u'_x+(2u+6v)\cdot v'_x$$
$$z'_y=z'_u\cdot u'_y+z'_v\cdot v'_y=2v\cdot u'_y+(2u+6v)\cdot v'_y$$
$$u'_x=-\sin(x-3y),\quad u'_y=3\sin(x-3y)$$
בנקודה $x_0=\pi,\ y_0=-\pi$:
$$u(\pi,-\pi)=1,\quad u'_x(\pi,-\pi)=u'_y(\pi,-\pi)=0$$
$$z'_x(\pi,-\pi)=4\cdot0+14\cdot5=70$$
$$z'_y(\pi,-\pi)=4\cdot0+14\cdot4=56$$""", part="א", points=10))

questions.append(Q(4, "computation", "power_series", r"""עבור אילו ערכי $x$ הטור מתכנס (מצאו רדיוס התכנסות ותחום התכנסות):
$$\sum_{n=1}^{\infty}\frac{2^n}{\sqrt{n+4}}(x-1)^n.$$""",
r"""**הפתרון הרשמי עם תיקון:** בפתרון הרשמי נכתב בסוף שהטור ב-$x=\frac32$ "הוא גם מתכנס", ותחום ההתכנסות נכתב $[-\frac12;\frac32)$. אבל לפי מבחן ההשוואה הגבולי עם $\sum\frac{1}{\sqrt n}$, שמתבדר, הטור ב-$x=\frac32$ **מתבדר**, והקצה השמאלי הוא $x=1-\frac12=\frac12$ (לא $-\frac12$). תחום ההתכנסות הנכון הוא $[\frac12,\frac32)$. יתר השורות כבפתרון הרשמי.

נסמן $a_n:=\dfrac{2^n}{\sqrt{n+4}}$
$$\frac1R=\lim_{n\to\infty}\left|\frac{a_{n+1}}{a_n}\right|=\lim_{n\to\infty}\frac{2^{n+1}}{\sqrt{n+5}}\cdot\frac{\sqrt{n+4}}{2^n}=2$$
**רדיוס התכנסות $R=0.5$**,
אם $|x-1|<0.5$, טור מתכנס, אם $|x-1|>0.5$, טור מתבדר, נטפל בנקודות שבהן $|x-1|=\frac12$.
אם $x=\frac12$ אז מקבלים
$$\sum_{n=1}^{\infty}\frac{2^n}{\sqrt{n+4}}\left(-\frac12\right)^n=\sum_{n=1}^{\infty}\frac{(-1)^n}{\sqrt{n+4}}.$$
נסמן $c_n=\frac{1}{\sqrt{n+4}}$. נשים לב ש
1. $c_n>0$ לכל $n\in\mathbb N$.
2. $c_{n+1}=\frac{1}{\sqrt{n+5}}<\frac{1}{\sqrt{n+4}}=c_n$ לכל $n\in\mathbb N$.
3. $\lim_{n\to\infty}c_n=\lim_{n\to\infty}\frac{1}{\sqrt{n+4}}=0$.

מכאן נובע (לפי משפט לייבניץ) שהטור $\sum_{n=1}^{\infty}\frac{(-1)^n}{\sqrt{n+4}}$ מתכנס.
אם $x=\frac32$ אז מקבלים
$$\sum_{n=1}^{\infty}\frac{2^n}{\sqrt{n+4}}\left(\frac12\right)^n=\sum_{n=1}^{\infty}\frac{1}{\sqrt{n+4}}.$$
נסמן $c_n=\frac{1}{\sqrt{n+4}},\ b_n=\frac{1}{\sqrt n}$, $c_n\ge0,\ b_n\ge0$
$$\lim_{n\to\infty}\frac{c_n}{b_n}=1$$
הטור $\sum_{n=1}^{\infty}b_n=\sum_{n=1}^{\infty}\frac{1}{\sqrt n}$ מתבדר (כי $\alpha=\frac12\le1$).
לכן לפי מבחן ההשוואה הגבולי $\sum_{n=1}^{\infty}\frac{1}{\sqrt{n+4}}$ הוא גם **מתבדר** (תיקון).

**תחום התכנסות $[\frac12;\frac32)$** (תיקון).""", part="ב", points=15,
    solutionSource="solved", official=False))

# ===== Q5 =====
F5 = r"""נתונה הפונקציה $f(x)=\ln(6x^2+5x+1)$.
"""
questions.append(Q(5, "computation", "taylor_maclaurin", F5 + r"""פתחו את הפונקציה $f(x)$ לטור מקלורן.""",
r"""$$f(x)=\ln(6x^2+5x+1)=\ln\left((3x+1)(2x+1)\right)=\ln(3x+1)+\ln(2x+1).$$
עבור $-1<3x\le1$
$$\ln(3x+1)=\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}(3x)^n$$
עבור $-1<2x\le1$
$$\ln(2x+1)=\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}(2x)^n$$
לכן עבור $-1/3<x\le1/3$
$$f(x)=\sum_{n=1}^{\infty}\frac{(-1)^{n+1}(3x)^n}{n}+\sum_{n=1}^{\infty}\frac{(-1)^{n+1}(2x)^n}{n}=\sum_{n=1}^{\infty}\frac{(-1)^{n+1}\left(3^n+2^n\right)}{n}x^n$$""", part="א", points=8))

questions.append(Q(5, "computation", "power_series", F5 + r"""מהו תחום ההתכנסות של הטור מהסעיף (א)?""",
r"""תחום ההתכנסות הוא $\left(-\frac13,\frac13\right]$:
$$\frac1R=\lim_{n\to\infty}\sqrt[n]{\frac{3^n+2^n}{n}}=\lim_{n\to\infty}3\cdot\frac{\sqrt[n]{1+\left(\frac23\right)^n}}{\sqrt[n]{n}}=3.$$""", part="ב", points=8))

questions.append(Q(5, "computation", "taylor_maclaurin", F5 + r"""הסיקו את הערך של $f^{(5)}(0)$.""",
r"""$$\frac{f^{(n)}(0)}{n!}=\frac{(-1)^{n+1}\left(3^n+2^n\right)}{n}$$
$$\frac{f^{(5)}(0)}{5!}=\frac{(-1)^{5+1}\left(3^5+2^5\right)}{5}=\frac{275}{5}=55$$
$$f^{(5)}(0)=55\cdot5!=6600.$$""", part="ג", points=7))

exam = {
    "examCode": "24B-B",
    "examLabel": "מבחן סוף סמסטר ב' תשפ\"ד, מועד ב'",
    "year": 2024,
    "examDate": "30/07/2024",
    "sourceFile": "calculus-2/24B-B typed solution with embedded questions.pdf",
    "solutionFile": "calculus-2/24B-B typed solution with embedded questions.pdf",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
