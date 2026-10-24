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

Corrected by the solver (standing ruling, wrong final answer)
- Q3b: the exam prints the right-hand side as z*x^2/v. The official solution's penultimate line
  x^2 v e^{x^2y}/v^2 is right, but its concluding line "= e^{x^2y} x^2/v^2 = z x^2/v^2" simplifies it wrongly, so the
  proof as printed concludes a false identity. For a proof the concluding line is the final answer, so this is
  treated as a wrong final answer: minimal fix of that line, solutionSource "solved", official False, prefix
  "הפתרון הרשמי עם תיקון". Verified in tools/verify/26A-A/solve_26A-A.py (sympy + numeric).

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

# ===== Q3b (official key with a corrected final line; solver) =====
questions.append(Q(3, "proof", "chain_rule_identity", r"""הוכיחו כי השוויון הבא מתקיים:
$$u\cdot\frac{\partial z}{\partial u}-v\cdot\frac{\partial z}{\partial v}=z\,\frac{x^2}{v}$$
כאשר: $y=\dfrac{1}{v}$ , $x=\sqrt{uv}$ , $z=e^{x^2y}$""",
r"""**הפתרון הרשמי עם תיקון:** בשורה האחרונה של הפתרון הרשמי נכתב $e^{x^2y}\frac{x^2}{v^2}=z\frac{x^2}{v^2}$, וזו טעות בצמצום: $x^2v\,e^{x^2y}\frac{1}{v^2}=e^{x^2y}\frac{x^2}{v}$, כלומר מתקבל בדיוק אגף ימין של השוויון שבשאלה. יתר השורות כבפתרון הרשמי.
$$\frac{\partial x}{\partial u}=\frac{v}{2\sqrt{uv}};\qquad\frac{\partial x}{\partial v}=\frac{u}{2\sqrt{uv}};\qquad\frac{\partial y}{\partial u}=0;\qquad\frac{\partial y}{\partial v}=-\frac{1}{v^2};$$
$$\frac{\partial z}{\partial x}=2xye^{x^2y};\qquad\frac{\partial z}{\partial y}=x^2e^{x^2y};$$
לכן
$$\frac{\partial z}{\partial u}=\frac{\partial z}{\partial x}\frac{\partial x}{\partial u}+\frac{\partial z}{\partial y}\frac{\partial y}{\partial u}=2xye^{x^2y}\frac{v}{2\sqrt{uv}}+x^2e^{x^2y}\cdot0=2xye^{x^2y}\frac{v}{2\sqrt{uv}};$$
$$\frac{\partial z}{\partial v}=\frac{\partial z}{\partial x}\frac{\partial x}{\partial v}+\frac{\partial z}{\partial y}\frac{\partial y}{\partial v}=2xye^{x^2y}\frac{u}{2\sqrt{uv}}-x^2e^{x^2y}\frac{1}{v^2}$$
ומכאן
$$u\frac{\partial z}{\partial u}-v\frac{\partial z}{\partial v}=2xye^{x^2y}\frac{uv}{2\sqrt{uv}}-2xye^{x^2y}\frac{uv}{2\sqrt{uv}}+x^2v\,e^{x^2y}\frac{1}{v^2}=$$
$$=e^{x^2y}\frac{x^2}{v}=z\,\frac{x^2}{v}.$$""", part="ב", points=13,
    solutionSource="solved", official=False))

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

# ---- rubric / pitfalls / steps (ai-draft). Every expected value is re-computed in tools/verify/26A-A/steps_26A-A.py ----
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
    rubric=rub((r"זיהוי התחום $0\le y\le2-x^2,\ 0\le x\le\sqrt2$ וכתיבתו כ-$0\le x\le\sqrt{2-y},\ 0\le y\le2$", 4),
               (r"אינטגרציה פנימית לפי $x$: $\int xe^{x^2}dx=\frac{e^{x^2}}{2}$ עם הצבת הגבולות", 3),
               (r"אינטגרציה חיצונית לפי $y$ של $\frac12\left(e^{2-y}-1\right)$", 3),
               (r"תוצאה סופית: $\frac{e^2-3}{2}$", 2)),
    pitfalls=[r"לנסות לחשב את האינטגרל בסדר המקורי: ל-$e^{x^2}$ אין פונקציה קדומה אלמנטרית לפי $x$ כשהגבולות תלויים ב-$y$. לכן מחליפים סדר.",
              r"לרשום את גבולות $x$ החדשים כ-$2-y^2$ במקום $\sqrt{2-y}$, כלומר לא להפוך נכון את הפרבולה $y=2-x^2$."],
    steps=[
        choice("מהם גבולות האינטגרציה אחרי החלפת הסדר (האינטגרל הפנימי לפי $x$)?",
               r"$0\le x\le\sqrt{2-y},\quad0\le y\le2$",
               [r"$0\le x\le2-y^2,\quad0\le y\le\sqrt2$",
                r"$0\le x\le\sqrt{2},\quad0\le y\le2$",
                r"$0\le x\le\sqrt{y-2},\quad0\le y\le2$"],
               r"מהפרבולה $y=2-x^2$ מקבלים $x=\sqrt{2-y}$, ו-$y$ רץ מ-$0$ עד $2$ (הערך של $y$ ב-$x=0$).", pos=1),
        num(r"מהו האינטגרל הפנימי $\int_0^{\sqrt{2-y}}xe^{x^2}dx$ עבור $y=1$ (תשובה עשרונית, דיוק $0.001$)?", 0.8591,
            r"$\left.\frac{e^{x^2}}{2}\right|_0^{1}=\frac{e-1}{2}\approx0.8591$.", tol=0.001),
        num(r"מהו ערך האינטגרל הכפול (תשובה עשרונית, דיוק $0.001$)?", 2.1945,
            r"$\frac12\int_0^2\left(e^{2-y}-1\right)dy=\frac12\left(e^2-3\right)\approx2.1945$.", tol=0.001),
    ])

add(1, "ב",
    rubric=rub((r"בחירת שני מסלולים שונים לכיוון $(0,0)$ (ציר $x$ והישר $y=x$)", 3),
               (r"מסלול $y=0$: הגבול שווה ל-$0$", 3),
               (r"מסלול $y=x$: $\frac{\ln(1+x^2)}{2x^2}\to\frac12$", 4),
               (r"מסקנה: שני גבולות שונים, ולכן הגבול אינו קיים", 3)),
    pitfalls=[r"לבדוק מסלול אחד בלבד ולהסיק שהגבול קיים. מסלולים מראים רק שהגבול אינו קיים, לא שהוא קיים.",
              r"לשכוח שב-$y=x$ המכנה הוא $x^2+x^2=2x^2$ ולקבל $1$ במקום $\frac12$."],
    steps=[
        num(r"מהו הגבול לאורך ציר $x$ ($y=0$)?", 0,
            r"$\ln(1+0)=0$, ולכן הביטוי שווה $0$ לכל $x\ne0$."),
        num(r"מהו הגבול לאורך הישר $y=x$ (תשובה עשרונית, דיוק $0.001$)?", 0.5,
            r"$\frac{\ln(1+x^2)}{2x^2}\to\frac12$, כי $\ln(1+t)\sim t$.", tol=0.001),
        choice("מה מסקנת הפתרון לגבי הגבול?",
               "הגבול אינו קיים",
               ["הגבול קיים ושווה $0$", r"הגבול קיים ושווה $\frac12$", "הגבול קיים ושווה $1$"],
               r"שני מסלולים נותנים $0$ ו-$\frac12$. אילו הגבול היה קיים כל מסלול היה נותן את אותו ערך.", pos=2),
    ])

add(2, "א",
    rubric=rub((r"רישום הטור הראשון כ-$\sum\left(\frac23\right)^n\cos n$ וחסימה $\left|\left(\frac23\right)^n\cos n\right|\le\left(\frac23\right)^n$", 4),
               (r"הטור ההנדסי עם מנה $\frac23$ מתכנס, ולכן הטור הראשון מתכנס בהחלט (משפט ההשוואה)", 2),
               (r"$\cos(\pi n)=(-1)^n$, ולכן הטור השני הוא $\sum\frac{(-1)^n}{n}$ ומתכנס לפי לייבניץ", 3),
               (r"טור הערכים המוחלטים הוא הטור ההרמוני המתבדר, ולכן הטור השני מתכנס בתנאי בלבד", 3)),
    pitfalls=[r"להשאיר $\cos(\pi n)$ ללא פישוט ל-$(-1)^n$ ולא לזהות שהטור מחליף סימן.",
              r"להסיק ממבחן לייבניץ בלבד שהטור השני מתכנס בהחלט. צריך לבדוק גם את טור הערכים המוחלטים.",
              r"להתעלם מהגורם $\cos n$ בטור הראשון, שאינו חיובי: ההשוואה נעשית לערך מוחלט."],
    steps=[
        num(r"מהי מנת הטור ההנדסי $\sum\left(\frac23\right)^n$ שאליו משווים את הטור הראשון (תשובה עשרונית, דיוק $0.001$)?", 0.6667,
            r"$\frac{2^n}{3^n}=\left(\frac23\right)^n$, והמנה $\frac23<1$, ולכן הטור ההנדסי מתכנס.", tol=0.001),
        num(r"מהו סכום הטור ההנדסי $\sum_{n=1}^{\infty}\left(\frac23\right)^n$ שחוסם את הטור הראשון?", 2,
            r"$\frac{2/3}{1-2/3}=2$."),
        num(r"מהו $\cos(\pi n)$ עבור $n=3$?", -1,
            r"$\cos(\pi n)=(-1)^n$, ולכן עבור $n=3$ מקבלים $-1$."),
        choice("מה מסקנת הפתרון לגבי שני הטורים?",
               "הטור הראשון מתכנס בהחלט, והטור השני מתכנס בתנאי",
               ["שני הטורים מתכנסים בהחלט",
                "הטור הראשון מתכנס בתנאי, והטור השני מתכנס בהחלט",
                "הטור הראשון מתכנס בהחלט, והטור השני מתבדר"],
               r"הראשון חסום בערך מוחלט על ידי טור הנדסי מתכנס. השני הוא $\sum\frac{(-1)^n}{n}$: מתכנס לפי לייבניץ, וטור הערכים המוחלטים $\sum\frac1n$ מתבדר.", pos=1),
    ])

add(2, "ב",
    rubric=rub((r"חישוב $f_x(0,0)=\frac12$ מההגדרה", 3),
               (r"חישוב $f_y(0,0)=1$ מההגדרה", 3),
               (r"הצבה בהגדרת הדיפרנציאביליות לאורך $y=x$: $f(x,x)=\frac23x$ ומנה השווה ל-$\mp\frac{5}{6\sqrt2}$", 5),
               (r"מסקנה: הגבול שונה מ-$0$, ולכן הפונקציה אינה דיפרנציאבילית", 2)),
    pitfalls=[r"לגזור את הנוסחה ולהציב $(0,0)$. הנקודה עצמה מוגדרת בנפרד, ולכן הנגזרות החלקיות מחושבות מההגדרה כגבול.",
              r"לחשוב שקיום הנגזרות החלקיות מבטיח דיפרנציאביליות."],
    steps=[
        num(r"מהו $f_x(0,0)$ (תשובה עשרונית, דיוק $0.001$)?", 0.5,
            r"$\frac{f(h,0)}{h}=\frac{h^3/(2h^2)}{h}=\frac12$.", tol=0.001),
        num(r"מהו $f_y(0,0)$?", 1,
            r"$\frac{f(0,h)}{h}=\frac{h^3/h^2}{h}=1$."),
        num(r"בהגדרת הדיפרנציאביליות מציבים $y=x$ עבור $x>0$. מהו הגבול של $\dfrac{f(x,x)-\left(\frac12x+x\right)}{\sqrt{x^2+x^2}}$ (תשובה עשרונית, דיוק $0.001$)?", -0.5893,
            r"$f(x,x)=\frac23x$, ולכן המונה הוא $\left(\frac23-\frac32\right)x=-\frac56x$ והמכנה $\sqrt2\,x$. המנה היא $-\frac{5}{6\sqrt2}\approx-0.5893$.", tol=0.001),
        choice("מה מסקנת הפתרון?",
               "הפונקציה אינה דיפרנציאבילית ב-$(0,0)$",
               [r"הפונקציה דיפרנציאבילית ב-$(0,0)$ כי הנגזרות החלקיות קיימות",
                r"הפונקציה אינה דיפרנציאבילית כי $f_x(0,0)$ אינה קיימת",
                r"הפונקציה דיפרנציאבילית כי הגבול לאורך $y=x$ שווה ל-$0$"],
               r"הגבול לאורך $y=x$ שונה מ-$0$ (בערך מוחלט $\frac{5}{6\sqrt2}$), ולכן המנה אינה שואפת ל-$0$. שתי הנגזרות החלקיות כן קיימות.", pos=3),
    ])

add(3, "א",
    rubric=rub((r"הצבת $y=x+2$ והסקה שהטור $\sum a_ny^n$ מתכנס עבור $-3\le y<3$", 4),
               (r"כתיבת התנאי $-3\le x+2<3$ כולל סוג כל קצה (סגור משמאל, פתוח מימין)", 4),
               (r"פתרון האי-שוויון: $-5\le x<1$", 2),
               (r"ניסוח התשובה: התחום $[-5,1)$", 2)),
    pitfalls=[r"להזיז את הקטע לכיוון הלא נכון ולקבל $[-1,5)$ במקום $[-5,1)$.",
              r"לשנות את סוג הקצוות, למשל לכתוב קטע פתוח או סגור משני הצדדים."],
    steps=[
        num(r"עבור איזה $x$ מתקבל הקצה השמאלי $y=-3$ (כאשר $y=x+2$)?", -5,
            r"$x+2=-3$, ולכן $x=-5$. בקצה זה הטור מתכנס (הקצה $y=-3$ שייך לתחום)."),
        num(r"עבור איזה $x$ מתקבל הקצה הימני $y=3$?", 1,
            r"$x+2=3$, ולכן $x=1$. בקצה זה הטור מתבדר (הקצה $y=3$ אינו שייך לתחום)."),
        choice(r"מהו תחום ההתכנסות של $\sum a_n(x+2)^n$?",
               r"$[-5,1)$",
               [r"$(-5,1]$", r"$[-5,1]$", r"$[-1,5)$"],
               r"הקצה $y=-3$ כלול והקצה $y=3$ אינו כלול, ולכן $x=-5$ כלול ו-$x=1$ אינו כלול.", pos=0),
    ])

add(3, "ב",
    rubric=rub((r"חישוב הנגזרות החלקיות של $x,y$ לפי $u,v$ ושל $z$ לפי $x,y$", 3),
               (r"כלל השרשרת עבור $\frac{\partial z}{\partial u}$ ו-$\frac{\partial z}{\partial v}$", 4),
               (r"הצבה בביטוי $u\frac{\partial z}{\partial u}-v\frac{\partial z}{\partial v}$ וצמצום שני האיברים המכילים $2xye^{x^2y}$", 3),
               (r"שורה אחרונה נכונה: $x^2v\,e^{x^2y}\frac1{v^2}=e^{x^2y}\frac{x^2}{v}=z\frac{x^2}{v}$", 3)),
    pitfalls=[r"שגיאת צמצום בשורה האחרונה: $x^2v\cdot\frac1{v^2}=\frac{x^2}{v}$ ולא $\frac{x^2}{v^2}$. כך מתקבל $z\frac{x^2}{v^2}$, שאינו אגף ימין של הטענה.",
              r"לשכוח את האיבר $\frac{\partial z}{\partial y}\frac{\partial y}{\partial v}$ ב-$\frac{\partial z}{\partial v}$, בעוד ש-$\frac{\partial y}{\partial u}=0$ מבטל את האיבר המקביל ב-$\frac{\partial z}{\partial u}$."],
    steps=[
        choice("באיזו שיטה הפתרון מוכיח את השוויון?",
               r"כלל השרשרת: $z$ תלוי ב-$x,y$, ואלה תלויים ב-$u,v$",
               [r"הצבה ישירה של $x,y$ ב-$z$ וגזירה של $z$ כפונקציה של $u$ ו-$v$",
                r"גזירה סתומה של המשוואה $z=e^{x^2y}$ לפי $u$ ו-$v$",
                r"גזירה לוגריתמית של $z$ לפי $u$ ובנפרד לפי $v$"],
               r"הפתרון מחשב את $\frac{\partial z}{\partial x},\frac{\partial z}{\partial y}$ ואת הנגזרות של $x,y$ לפי $u,v$, ומרכיב אותן לפי כלל השרשרת.", pos=0),
        num(r"מהו $\dfrac{\partial y}{\partial u}$?", 0,
            r"$y=\frac1v$ אינו תלוי ב-$u$, ולכן האיבר $\frac{\partial z}{\partial y}\frac{\partial y}{\partial u}$ מתאפס."),
        num(r"מהו $\dfrac{\partial y}{\partial v}$ עבור $v=2$ (תשובה עשרונית, דיוק $0.001$)?", -0.25,
            r"$\frac{\partial y}{\partial v}=-\frac1{v^2}=-\frac14$.", tol=0.001),
        {"type": "order", "prompt": "סדרו את שלבי ההוכחה.", "lines": [
            r"מחשבים את הנגזרות החלקיות: של $x,y$ לפי $u,v$ ושל $z$ לפי $x,y$",
            r"כלל השרשרת נותן את $\frac{\partial z}{\partial u}$ ואת $\frac{\partial z}{\partial v}$",
            r"מציבים בביטוי $u\frac{\partial z}{\partial u}-v\frac{\partial z}{\partial v}$: שני האיברים עם $2xye^{x^2y}\frac{uv}{2\sqrt{uv}}$ מצטמצמים ונשאר $x^2v\,e^{x^2y}\frac1{v^2}$",
            r"מפשטים ל-$e^{x^2y}\frac{x^2}{v}$ וזה שווה ל-$z\frac{x^2}{v}$"],
         "explain": "כל שלב נשען על הקודם: אי אפשר ליישם את כלל השרשרת לפני שיש את הנגזרות, ואי אפשר להציב בביטוי לפני שיש את $z_u$ ו-$z_v$."},
        {"type": "findbug", "prompt": "בהוכחה הבאה שורה אחת שגויה. מצאו אותה.", "lines": [
            r"$\frac{\partial x}{\partial u}=\frac{v}{2\sqrt{uv}},\ \frac{\partial x}{\partial v}=\frac{u}{2\sqrt{uv}},\ \frac{\partial y}{\partial u}=0,\ \frac{\partial y}{\partial v}=-\frac1{v^2}$",
            r"$\frac{\partial z}{\partial x}=2xye^{x^2y},\ \frac{\partial z}{\partial y}=x^2e^{x^2y}$",
            r"$\frac{\partial z}{\partial u}=2xye^{x^2y}\frac{v}{2\sqrt{uv}}$",
            r"$\frac{\partial z}{\partial v}=2xye^{x^2y}\frac{u}{2\sqrt{uv}}-x^2e^{x^2y}\frac1{v^2}$",
            r"$u\frac{\partial z}{\partial u}-v\frac{\partial z}{\partial v}=2xye^{x^2y}\frac{uv}{2\sqrt{uv}}-2xye^{x^2y}\frac{uv}{2\sqrt{uv}}+x^2v\,e^{x^2y}\frac1{v^2}$",
            r"$=e^{x^2y}\frac{x^2}{v^2}=z\frac{x^2}{v^2}$"],
         "bugIndex": 5,
         "explain": r"השורה האחרונה שגויה: $x^2v\,e^{x^2y}\frac1{v^2}=e^{x^2y}\frac{x^2}{v}$ ולא $e^{x^2y}\frac{x^2}{v^2}$. כך מתקבל $z\frac{x^2}{v}$, בדיוק אגף ימין של הטענה."},
    ])

add(4, "א",
    rubric=rub((r"בחירת ההחלפה $u=y-x$, $v=xy$ וקביעת התחום $0\le u\le1$, $1\le v\le2$", 3),
               (r"חישוב היעקוביאן ההפוך $-(x+y)$ והיעקוביאן $|J|=\frac1{x+y}$", 3),
               (r"פירוק $x^2-y^2=(x-y)(x+y)$ ופישוט האינטגרנד ל-$-u$", 3),
               (r"חישוב האינטגרל והתוצאה $-\frac12$", 3)),
    pitfalls=[r"לשכוח את היעקוביאן ולהשאיר את האינטגרנד $-u(x+y)$, שאינו פונקציה של $u,v$ בלבד.",
              r"טעות סימן: $x^2-y^2=(x-y)(x+y)=-u(x+y)$ כי $u=y-x$."],
    steps=[
        num(r"מהו הדטרמיננט $\begin{vmatrix}u'_x&v'_x\\u'_y&v'_y\end{vmatrix}$ בנקודה $(1,1)$?", -2,
            r"הדטרמיננט הוא $-(x+y)$, ובנקודה $(1,1)$ הוא $-2$."),
        choice(r"במשתנים החדשים, למה שווה $(x^2-y^2)\cdot|J|$?",
               r"$-u$",
               [r"$u$", r"$-u(x+y)$", r"$-uv$"],
               r"$x^2-y^2=(x-y)(x+y)=-u(x+y)$, וכפל ב-$|J|=\frac1{x+y}$ משאיר $-u$.", pos=0),
        num(r"מהו $\int_0^1(-u)\,du$ (תשובה עשרונית, דיוק $0.001$)?", -0.5,
            r"$\left.-\frac{u^2}{2}\right|_0^1=-\frac12$.", tol=0.001),
        num(r"מהו ערך האינטגרל הכפול $\iint_D(x^2-y^2)\,dx\,dy$ (תשובה עשרונית, דיוק $0.001$)?", -0.5,
            r"$\int_1^2dv\cdot\int_0^1(-u)\,du=1\cdot\left(-\frac12\right)=-\frac12$.", tol=0.001),
    ])

add(4, "ב",
    rubric=rub((r"הצבת $y^2=4-x^2$ והפיכת הבעיה לפונקציה $\tilde f(x)=4+x^3-3x$ על $-2\le x\le2$", 3),
               (r"נקודות חשודות: קצוות $x=\pm2$ ונקודות קריטיות $x=\pm1$ מתוך $\tilde f'(x)=3x^2-3=0$", 3),
               (r"ערכי הפונקציה בנקודות החשודות: $2,6,6,2$", 4),
               (r"הצגת הנקודות על המעגל: מקסימום $6$ בשלוש נקודות ומינימום $2$ בשלוש נקודות", 3)),
    pitfalls=[r"לשכוח את הקצוות $x=\pm2$ של הקטע, שבהם מתקבלים ערך המקסימום והמינימום.",
              r"לשכוח שלכל $x$ עם $|x|<2$ יש שתי נקודות על המעגל ($y=\pm\sqrt{4-x^2}$), ולכן לכל ערך יש כמה נקודות."],
    steps=[
        choice(r"לאחר הצבת $y^2=4-x^2$, איזו פונקציה של $x$ מתקבלת?",
               r"$\tilde f(x)=4+x^3-3x$",
               [r"$\tilde f(x)=x^3+x^2-3x+4$", r"$\tilde f(x)=x^3-3x-4$", r"$\tilde f(x)=x^3-x^2-3x+4$"],
               r"$x^3+x^2-3x+\left(4-x^2\right)=4+x^3-3x$, והאיברים $x^2$ מצטמצמים.", pos=0),
        num(r"מהו הפתרון החיובי של $\tilde f'(x)=3x^2-3=0$?", 1,
            r"$x^2=1$, ולכן $x=\pm1$. הפתרון החיובי הוא $1$."),
        num(r"מהו $\tilde f(-1)$?", 6,
            r"$4+(-1)-3(-1)=4-1+3=6$."),
        num(r"בכמה נקודות על המעגל מתקבל ערך המקסימום?", 3,
            r"הערך $6$ מתקבל ב-$x=-1$ (שתי נקודות $y=\pm\sqrt3$) וב-$x=2$ (הנקודה $(2,0)$), ובסך הכול שלוש נקודות."),
        num(r"מהו ערך המינימום של הפונקציה על המעגל?", 2,
            r"הערך $\tilde f(1)=\tilde f(-2)=2$ הוא הקטן מבין הערכים $2,6,6,2$."),
    ])

add(5, "א",
    rubric=rub((r"מערכת הנגזרות החלקיות $f'_x=3\left((x-y)^2-1\right)=0$ ו-$f'_y=-3(x-y)^2-2y+5=0$", 3),
               (r"פתרון המערכת: $y=1$ ו-$x-1=\pm1$, כלומר הנקודות $M_1(2,1)$ ו-$M_2(0,1)$", 3),
               (r"הנגזרות השניות ו-$\Delta(2,1)=-12<0$: נקודת אוכף ב-$M_1$", 3),
               (r"$\Delta(0,1)=12>0$ ו-$f''_{xx}(0,1)=-6<0$: מקסימום מקומי ב-$M_2$", 3)),
    pitfalls=[r"לפתור את המשוואה $(x-y)^2=1$ ולקבל רק את הפתרון $x-y=1$, ולשכוח את $x-y=-1$.",
              r"לסווג לפי הסימן של $f''_{xx}$ בלבד. כש-$\Delta<0$ הנקודה היא אוכף ללא תלות בסימן $f''_{xx}$."],
    steps=[
        choice("מהן נקודות הקריטיות של הפונקציה?",
               r"$(2,1)$ ו-$(0,1)$",
               [r"$(1,2)$ ו-$(1,0)$", r"$(2,1)$ ו-$(-2,1)$", r"$(0,0)$ ו-$(2,2)$"],
               r"מהמשוואה השנייה, אחרי הצבת $(x-y)^2=1$, מקבלים $y=1$. אז $x-1=\pm1$ ו-$x=2$ או $x=0$.", pos=0),
        num(r"מהו $\Delta(2,1)=f''_{xx}f''_{yy}-\left(f''_{xy}\right)^2$?", -12,
            r"$f''_{xx}=6$, $f''_{yy}=6\cdot1-2=4$, $f''_{xy}=-6$, ולכן $6\cdot4-36=-12$."),
        num(r"מהו $\Delta(0,1)$?", 12,
            r"$f''_{xx}=-6$, $f''_{yy}=-6-2=-8$, $f''_{xy}=6$, ולכן $(-6)(-8)-36=12$."),
        choice("מה הסיווג של שתי הנקודות?",
               r"$(2,1)$ אוכף, ו-$(0,1)$ מקסימום מקומי",
               [r"$(2,1)$ מקסימום מקומי, ו-$(0,1)$ אוכף",
                r"$(2,1)$ מינימום מקומי, ו-$(0,1)$ מקסימום מקומי",
                r"שתי הנקודות הן אוכף"],
               r"ב-$(2,1)$ מתקבל $\Delta<0$, כלומר אוכף. ב-$(0,1)$ מתקבל $\Delta>0$ ו-$f''_{xx}<0$, כלומר מקסימום מקומי.", pos=1),
    ])

add(5, "ב",
    rubric=rub((r"פירוק לשברים חלקיים: $\frac{16-5x}{(x-2)(x-3)}=\frac{-6}{x-2}+\frac1{x-3}$", 3),
               (r"פיתוח כל שבר לטור הנדסי: $\frac6{2-x}=\sum\frac{3x^n}{2^n}$ עבור $|x|<2$ ו-$-\frac1{3-x}=-\sum\frac{x^n}{3^{n+1}}$ עבור $|x|<3$", 4),
               (r"שילוב הפיתוחים: המקדם $\frac3{2^n}-\frac1{3^{n+1}}$ ותחום ההתכנסות $|x|<2$", 3),
               (r"$f^{(20)}(0)=20!\cdot a_{20}=20!\left(\frac3{2^{20}}-\frac1{3^{21}}\right)$", 3)),
    pitfalls=[r"לקחת את תחום ההתכנסות $|x|<3$ במקום החיתוך $|x|<2$ של שני התחומים.",
              r"לשכוח את הגורם $20!$ ולכתוב את המקדם $a_{20}$ בלבד כערך הנגזרת.",
              r"לשגות בחזקה במכנה של הטור השני: $\frac1{3-x}=\frac13\sum\left(\frac x3\right)^n$ נותן $3^{n+1}$ ולא $3^n$."],
    steps=[
        num(r"בפירוק $\frac{16-5x}{(x-2)(x-3)}=\frac{A}{x-2}+\frac{B}{x-3}$, מהו $A$?", -6,
            r"מציבים $x=2$ ב-$16-5x=A(x-3)+B(x-2)$ ומקבלים $6=-A$, כלומר $A=-6$."),
        num(r"מהו רדיוס ההתכנסות של הטור המתקבל?", 2,
            r"הטור של $\frac6{2-x}$ מתכנס עבור $|x|<2$ והטור של $\frac1{3-x}$ עבור $|x|<3$. הסכום מתכנס בחיתוך, כלומר $|x|<2$."),
        num(r"מהו המקדם $a_1$ של $x$ בטור (תשובה עשרונית, דיוק $0.001$)?", 1.3889,
            r"$a_n=\frac3{2^n}-\frac1{3^{n+1}}$, ולכן $a_1=\frac32-\frac19=\frac{25}{18}\approx1.3889$.", tol=0.001),
        choice(r"מהו $f^{(20)}(0)$?",
               r"$20!\left(\frac3{2^{20}}-\frac1{3^{21}}\right)$",
               [r"$\frac3{2^{20}}-\frac1{3^{21}}$",
                r"$20!\left(\frac3{2^{20}}-\frac1{3^{20}}\right)$",
                r"$20!\left(\frac3{2^{20}}+\frac1{3^{21}}\right)$"],
               r"מתקיים $a_{20}=\frac{f^{(20)}(0)}{20!}$, ולכן $f^{(20)}(0)=20!\,a_{20}$ עם $a_{20}=\frac3{2^{20}}-\frac1{3^{21}}$.", pos=2),
    ])

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
