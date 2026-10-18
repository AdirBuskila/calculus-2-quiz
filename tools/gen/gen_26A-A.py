# -*- coding: utf-8 -*-
"""Generator for tools/raw/26A-A.json -- calculus-2 (20252), semester A 2026, moed A (12/02/2026).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_26A-A.py

Source: sitting 26A. Exam: 3 pages, 5 questions of 25 points (a=12, b=13), solve 4 of 5.
Solution: the lecturers' corrected solution, 9 pages: Q1-Q3 typed, Q4 handwritten on a tablet, Q5 handwritten on squared paper.
Exam header (lecturer names) is not transcribed.

Transcription notes
- The text layers are garbled; everything is transcribed from page renders.
- Q2a asks for two series in one part; stored as one item.
- Q4a: the official solution gives only the substitution u=y-x, v=xy and its Jacobian and result; the sketch of the
  region is not drawn in the official solution (the region is recorded in tools/verify/26A-A/regions.json).
  The official solution writes "in the first quadrant" and the limits 0<=u<=1, 1<=v<=2, which is what is transcribed.
- Q4b: the official page is a handwritten tablet note; transcribed in full (reduction to one variable on the circle).
- Q5a: handwritten; the Hessian determinant is called Delta and written Delta(2,1) etc.
- Q5b: the handwritten value reads 3^21 in the last line (the exponent is badly formed); sympy confirms 3^21.

HOLD
- Q3b: the exam prints the right-hand side as z*x^2/v, and the official solution's own computation reaches
  e^{x^2 y} x^2 / v (sympy: the identity holds with RHS z*x^2/v), but the final printed line is "= z x^2/v^2".
  The official final line therefore disagrees with the printed statement. Held; see docs/ASK_ADIR.md.

Checks (tools/verify/26A-A/check.py, sympy + numeric): every integral, limit, partial derivative, Hessian,
Lagrange point, Jacobian, series coefficient matches the official answers, except the Q3b final line above.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "26A-A.json"


def Q(num, kind, topic, question, solution, part=None, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "solution": solution.strip("\n"),
         "solutionSource": "official-pdf", "official": True, "confidence": "high"}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ===== Q1a =====
questions.append(Q(1, "computation", "double_integrals", r"""החליפו את סדר האינטגרציה וחשבו את האינטגרל
$$\int_0^{\sqrt{2}}\left(\int_0^{2-x^2}xe^{x^2}\,dy\right)dx$$""",
r"""תחום האינטגרציה הוא $0\le y\le 2-x^2,\ 0\le x\le\sqrt{2}$.
זה אותו דבר ש-$0\le x\le\sqrt{2-y},\ 0\le y\le 2$.
![תחום האינטגרציה: מתחת לפרבולה y=2-x^2 ברביע הראשון](images/exams/26A-A-Q1a-region.png)
אז
$$\int_0^{\sqrt{2}}\left(\int_0^{2-x^2}xe^{x^2}dy\right)dx=\int_0^{2}\left(\int_0^{\sqrt{2-y}}xe^{x^2}dx\right)dy$$
$$=\int_0^{2}\left(\left.\frac{e^{x^2}}{2}\right|_0^{\sqrt{2-y}}\right)dy=\int_0^{2}\frac{1}{2}\left(e^{2-y}-1\right)dy=\frac{1}{2}\left.\left(-e^{2-y}-y\right)\right|_0^2$$
$$=\frac{1}{2}\left((-1-2)-(-e^2)\right)=\frac{e^2-3}{2}.$$""", part="א", points=12))

# ===== Q1b =====
questions.append(Q(1, "computation", "limits_continuity", r"""בדקו האם הגבול הבא קיים
$$\lim_{(x,y)\to(0,0)}\frac{\ln(1+xy)}{x^2+y^2}$$""",
r"""בואו נבחן שני מסלולים:
1) לפי ציר $x$ ($y=0$).
2) לפי קו ישר $y=x$.
הגבול לפי המסלול הראשון שווה ל-0:
$$\lim_{x\to0}\frac{\ln 1}{x^2}=\lim_{x\to0}0=0$$
הגבול לפי המסלול השני שווה ל-$\frac{1}{2}$:
$$\lim_{x\to0}\frac{\ln(1+x^2)}{2x^2}=\frac{1}{2}$$
$0\ne\frac{1}{2}$ אז הגבול $\lim_{(x,y)\to(0,0)}\frac{\ln(1+xy)}{x^2+y^2}$ לא קיים.""", part="ב", points=13))

# ===== Q2a =====
questions.append(Q(2, "computation", "numeric_series", r"""בדקו התכנסות בהחלט, בתנאי או התבדרות של הטורים הבאים:
$$\sum_{n=1}^{\infty}\frac{2^n\cos(n)}{3^n}$$
$$\sum_{n=1}^{\infty}\frac{\cos(\pi n)}{n}$$""",
r"""**הטור הראשון.** נכתוב
$$\sum_{n=1}^{\infty}\left(\frac{2}{3}\right)^n\cos n.$$
התכנסות בהחלט:
$$\left|\left(\frac{2}{3}\right)^n\cos n\right|\le\left(\frac{2}{3}\right)^n$$
ו-$\sum_{n=1}^{\infty}\left(\frac{2}{3}\right)^n$ הוא טור הנדסי עם מנה $0<2/3<1$, ולכן הוא מתכנס. לכן לפי משפט ההשוואה הטור המקורי מתכנס בהחלט.

**הטור השני.** עבור הטור $\sum_{n=1}^{\infty}\frac{\cos(\pi n)}{n}$ נשתמש ב-$\cos(\pi n)=(-1)^n$. אז
$$\sum_{n=1}^{\infty}\frac{\cos(\pi n)}{n}=\sum_{n=1}^{\infty}\frac{(-1)^n}{n},$$
טור הרמוני מתחלף הוא מתכנס לפי מבחן לייבניץ (האיברים $1/n$ יורדים מונוטונית ל-0). הוא אינו מתכנס במוחלט משום ש
$$\sum_{n=1}^{\infty}\left|\frac{(-1)^n}{n}\right|=\sum_{n=1}^{\infty}\frac{1}{n}$$
מתבדר. לכן הוא מתכנס בתנאי.""", part="א", points=12))

# ===== Q2b =====
questions.append(Q(2, "computation", "partials_differentiability", r"""נתונה הפונקציה
$$f(x,y)=\begin{cases}\dfrac{x^3+y^3}{2x^2+y^2}, & (x,y)\neq(0,0)\\[2mm] 0, & (x,y)=(0,0)\end{cases}$$
האם $f(x,y)$ דיפרנציאבילית ב-$(0,0)$?""",
r"""נגזרות חלקיות בנקודה $(0,0)$:
$$f_x(0,0)=\lim_{h\to0}\frac{f(h,0)-0}{h}=\lim_{h\to0}\frac{\frac{h^3}{2h^2}}{h}=\lim_{h\to0}\frac{h/2}{h}=\frac{1}{2}.$$
$$f_y(0,0)=\lim_{h\to0}\frac{f(0,h)-0}{h}=\lim_{h\to0}\frac{\frac{h^3}{h^2}}{h}=\lim_{h\to0}\frac{h}{h}=1.$$
פונקציה דיפרנציאבילית אם
$$\frac{f(x,y)-\left(\frac{1}{2}x+y\right)}{\sqrt{x^2+y^2}}\to0$$ כאשר $(x,y)\to(0,0)$.
לאורך הקו $y=x$:
$$f(x,x)=\frac{x^3+x^3}{2x^2+x^2}=\frac{2x^3}{3x^2}=\frac{2}{3}x,\qquad\frac{1}{2}x+y=\frac{1}{2}x+x=\frac{3}{2}x.$$
אז
$$\frac{f(x,x)-\left(\frac{1}{2}x+x\right)}{\sqrt{x^2+x^2}}=\frac{\left(\frac{2}{3}-\frac{3}{2}\right)x}{|x|\sqrt{2}}=-\frac{5}{6}\,\frac{x}{|x|\sqrt{2}}=\mp\frac{5}{6\sqrt{2}}\ne0.$$
בגלל שהגבול שונה מאפס (אפילו הוא לא קיים) הפונקציה $f(x,y)$ לא דיפרנציאבילית ב-$(0,0)$.""", part="ב", points=13))

# ===== Q3a =====
questions.append(Q(3, "computation", "power_series", r"""ידוע שתחום ההתכנסות של הטור $\sum_{n=0}^{\infty}a_nx^n$ הוא $[-3,3)$. מצאו את תחום ההתכנסות של הטור
$$\sum_{n=0}^{\infty}a_n(x+2)^n$$""",
r"""בואו נכתוב $y=x+2$, מכיוון שהטור $\sum_{n=0}^{\infty}a_ny^n$ מתכנס עבור $-3\le y<3$ הטור $\sum_{n=0}^{\infty}a_n(x+2)^n$ מתכנס עבור $-3\le x+2<3$, כלומר $-5\le x<1$.
התחום ההתכנסות הוא $[-5,1)$.""", part="א", points=12))

# ===== Q3b (HELD) =====
questions.append({
    "num": 3, "part": "ב", "kind": "proof", "topic": "chain_rule_identity", "points": 13,
    "question": r"""הוכיחו כי השוויון הבא מתקיים:
$$u\cdot\frac{\partial z}{\partial u}-v\cdot\frac{\partial z}{\partial v}=z\,\frac{x^2}{v}$$
כאשר: $y=\dfrac{1}{v}$ , $x=\sqrt{uv}$ , $z=e^{x^2y}$""",
    "hold": "the official solution's final line is z x^2/v^2, which disagrees with the printed right-hand side z x^2/v "
            "(sympy confirms the printed identity); needs Adir's decision",
})

# ===== Q4a =====
questions.append(Q(4, "computation", "change_of_variables", r"""חשבו את האינטגרל $\iint_D(x^2-y^2)\,dx\,dy$ כאשר $D$ חסום ע"י הקווים הבאים: $y-x=1;\ y=x;\ xy=1;\ xy=2$ $\ (x>0,\ y>0)$""",
r"""נעשה החלפת משתנים הבאה:
$$u=y-x,\qquad 0\le u\le1$$
$$v=xy,\qquad 1\le v\le2$$
היעקוביאן ההפוך:
$$\frac{1}{J}=\begin{vmatrix}u'_x&v'_x\\u'_y&v'_y\end{vmatrix}=\begin{vmatrix}-1&y\\1&x\end{vmatrix}=-x-y=-(x+y)$$
$$|J|=\frac{1}{x+y}$$
$$\iint_D(x^2-y^2)\,dx\,dy=\iint_D(x-y)(x+y)\,dx\,dy=\int_1^2dv\int_0^1(-u)\,du$$
$$=\int_1^2\left(\left.-\frac{u^2}{2}\right|_0^1\right)dv=\int_1^2-\frac{1}{2}\,dv=\left.-\frac{v}{2}\right|_1^2=-1+\frac{1}{2}=-\frac{1}{2}.$$""", part="א", points=12))

# ===== Q4b =====
questions.append(Q(4, "computation", "absolute_extrema", r"""מצאו אקסטרמומים מוחלטים של הפונקציה
$$f(x,y)=x^3+x^2-3x+y^2$$
במעגל
$$x^2+y^2=4$$""",
r"""נציב בפונקציה $y^2=4-x^2$ (מהמעגל $x^2+y^2=4$):
$$f(x,y)=x^3+x^2-3x+\underbrace{(4-x^2)}_{y^2}=4+x^3-3x$$
ויש למצוא מקסימום ומינימום מוחלטים לפונקציה
$$\tilde f(x)=4+x^3-3x$$
בקטע הסגור $-2\le x\le2$.
נבדוק את החשודות:
* קצוות הקטע: $x=2,\ x=-2$.
* בתוך הקטע: $\tilde f'(x)=3x^2-3=0$, כלומר $x=1,\ x=-1$.
נבדוק את ערכי הפונקציה בנקודות החשודות:
$$\tilde f(1)=2,\quad\tilde f(-1)=6,\quad\tilde f(2)=6,\quad\tilde f(-2)=2$$
בנקודות $(-1,-\sqrt{3}),\ (2,0),\ (-1,\sqrt{3})$ מתקבל הערך $6$ (המקסימלי).
בנקודות $(1,-\sqrt{3}),\ (1,\sqrt{3}),\ (-2,0)$ מתקבל הערך $2$ (המינימלי).""", part="ב", points=13))

# ===== Q5a =====
questions.append(Q(5, "computation", "local_extrema", r"""מצאו וסווגו את נקודות האקסטרמום של הפונקציה:
$$f(x,y)=(x-y)^3-3x-y^2+5y$$""",
r"""$$\begin{cases}f'_x=3(x-y)^2-3=3\left((x-y)^2-1\right)=0\\ f'_y=-3(x-y)^2-2y+5=0\end{cases}$$
$$\begin{cases}(x-y)^2=1\\ -3-2y+5=0\end{cases}\qquad\begin{cases}(x-1)^2=1\\ y=1\end{cases}\qquad\begin{cases}x-1=\pm1\\ y=1\end{cases}$$
$$\begin{cases}x=2\\ y=1\end{cases}\qquad\begin{cases}x=0\\ y=1\end{cases}\qquad M_1(2,1),\ M_2(0,1)$$
$$f''_{xx}=6(x-y),\qquad f''_{xy}=-6(x-y),\qquad f''_{yy}=6(x-y)-2$$
$$\Delta(2,1)=f''_{xx}(2,1)\cdot f''_{yy}(2,1)-\left(f''_{xy}(2,1)\right)^2=6\cdot4-6^2=-12<0$$
לכן נקודת אוכף ב-$M_1(2,1)$.
$$\Delta(0,1)=-6\cdot(-8)-36=12>0$$
$$f''_{xx}(0,1)=-6<0$$
לכן נקודת מקסימום מקומי ב-$M_2(0,1)$.""", part="א", points=12))

# ===== Q5b =====
questions.append(Q(5, "computation", "taylor_maclaurin", r"""פתחו את הפונקציה $f(x)=\dfrac{16-5x}{x^2-5x+6}$ לטור מקלורן. מהו תחום התכנסות הטור?
הסיקו את הערך של $f^{(20)}(0)$.""",
r"""$$f(x)=\frac{16-5x}{x^2-5x+6}=\frac{16-5x}{(x-2)(x-3)}$$
$$\frac{16-5x}{x^2-5x+6}=\frac{A}{x-2}+\frac{B}{x-3}$$
$$16-5x=A(x-3)+B(x-2)$$
$x=3$: $B=1$.
$x=2$: $A=-6$.
$$\frac{16-5x}{x^2-5x+6}=\frac{-6}{x-2}+\frac{1}{x-3}$$
$$\frac{6}{2-x}=\frac{6}{2\left(1-\frac{x}{2}\right)}=3\sum_{n=0}^{\infty}\left(\frac{x}{2}\right)^n=\sum_{n=0}^{\infty}\frac{3x^n}{2^n},\qquad|x|<2$$
$$-\frac{1}{3-x}=-\frac{1}{3\left(1-\frac{x}{3}\right)}=-\frac{1}{3}\sum_{n=0}^{\infty}\left(\frac{x}{3}\right)^n=\sum_{n=0}^{\infty}(-1)\frac{x^n}{3^{n+1}},\qquad|x|<3$$
$$f(x)=\sum_{n=0}^{\infty}\left(\frac{3}{2^n}-\frac{1}{3^{n+1}}\right)x^n,\qquad|x|<2$$
$$a_{20}=\frac{f^{(20)}(0)}{20!}\ \Rightarrow\ f^{(20)}(0)=a_{20}\cdot20!=20!\left(\frac{3}{2^{20}}-\frac{1}{3^{21}}\right)$$""", part="ב", points=13))

exam = {
    "examCode": "26A-A",
    "examLabel": "מבחן סוף סמסטר א' תשפ\"ו, מועד א'",
    "year": 2026,
    "examDate": "12/02/2026",
    "sourceFile": "calculus-2/26A exam.pdf",
    "solutionFile": "calculus-2/26A corrected-solution.pdf",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
