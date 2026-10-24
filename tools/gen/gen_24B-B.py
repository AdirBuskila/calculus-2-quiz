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

# ---- rubric / pitfalls / steps (ai-verified). Every expected value is re-computed in tools/verify/24B-B/steps_24B-B.py ----
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


def order(prompt, lines, explain):
    return {"type": "order", "prompt": prompt, "lines": lines, "explain": explain}


def findbug(prompt, lines, bug, explain):
    return {"type": "findbug", "prompt": prompt, "lines": lines, "bugIndex": bug, "explain": explain}


def add(n, part, **kw):
    for q in questions:
        if q["num"] == n and q.get("part") == part:
            q.update(kw)
            q["rubricSource"] = "ai-verified"
            q["stepsSource"] = "ai-verified"
            return
    raise KeyError((n, part))


add(1, "א",
    rubric=rub(("גזירת $f$ לפי $x$ בנקודה כללית בעזרת כלל המנה", 2), ("גזירת $f$ לפי $y$ בנקודה כללית בעזרת כלל המנה", 2),
               ("הצבת $(1,0)$ ב-$f'_x$: מתקבל $0$", 1), ("הצבת $(1,0)$ ב-$f'_y$: מתקבל $1$", 2)),
    pitfalls=["לגזור רק את המונה ולשכוח את האיבר $-2y^2x^3$ (או $-2x^4y$) שמגיע מגזירת המכנה בכלל המנה.",
              "להשתמש בהגדרת הגבול כאילו הנקודה היא הראשית: ב-$(1,0)$ מותר להציב בנוסחת הנגזרת הרגילה."],
    steps=[
        num(r"מהו המונה של $f'_y(x,y)$, כלומר $x^3(x^2+y^2)-2y^2x^3$, בנקודה $(1,0)$?", 1,
            r"$1^3\cdot(1+0)-0=1$."),
        num(r"מהו $f'_y(1,0)$?", 1,
            r"המכנה $(x^2+y^2)^2$ ב-$(1,0)$ שווה $1$, ולכן $f'_y(1,0)=\frac11=1$."),
        num(r"מהו $f'_x(1,0)$?", 0,
            r"המונה $3x^2y(x^2+y^2)-2x^4y$ מכיל את הגורם $y$, ולכן הוא מתאפס ב-$y=0$; המכנה שווה $1$, ולכן $f'_x(1,0)=0$."),
    ])

add(1, "ב",
    rubric=rub(("שימוש בהגדרת הנגזרת החלקית בראשית: $\\lim_{h\\to0}\\frac{f(h,0)-f(0,0)}{h}$", 2),
               ("חישוב $f(h,0)=0$ וקבלת $f'_x(0,0)=0$", 2),
               ("אותו חישוב עבור $y$: $f(0,h)=0$ ולכן $f'_y(0,0)=0$", 3)),
    pitfalls=["להציב $(0,0)$ בנוסחת הנגזרת הכללית: מתקבל $\\frac00$, והנוסחה לא תקפה בראשית.",
              "לבלבל בין שתי הנגזרות: $f'_x$ נבדקת לאורך ציר ה-$x$ ו-$f'_y$ לאורך ציר ה-$y$."],
    steps=[
        choice(r"איזה גבול מגדיר את $f'_x(0,0)$?",
               r"$\lim_{h\to0}\dfrac{f(h,0)-f(0,0)}{h}$",
               [r"$\lim_{h\to0}\dfrac{f(0,h)-f(0,0)}{h}$",
                r"הצבת $(0,0)$ בנוסחה $\dfrac{3x^2y(x^2+y^2)-2x^4y}{(x^2+y^2)^2}$",
                r"$\lim_{(x,y)\to(0,0)}f(x,y)$"],
               r"הנגזרת החלקית לפי $x$ בראשית מוגדרת כגבול של מנת ההפרשים לאורך ציר ה-$x$. הגבול עם $f(0,h)$ הוא $f'_y(0,0)$; הצבה בנוסחה נותנת $\frac00$; והגבול של $f$ עצמה עוסק ברציפות ולא בנגזרת.", pos=2),
        num(r"מהו $f(h,0)$ עבור $h\neq0$?", 0,
            r"$f(h,0)=\frac{h^3\cdot0}{h^2}=0$."),
        num(r"מהו $f'_x(0,0)$?", 0,
            r"$\lim_{h\to0}\frac{0-0}{h}=0$."),
        num(r"מהו $f'_y(0,0)$?", 0,
            r"$f(0,h)=\frac{0\cdot h}{h^2}=0$, ולכן $\lim_{h\to0}\frac{0-0}{h}=0$."),
    ])

L1C = r"מציבים $f'_x(0,0)=f'_y(0,0)=0$ ובודקים את הגבול $\lim\dfrac{f(\Delta x,\Delta y)}{\sqrt{\Delta x^2+\Delta y^2}}$"
L2C = r"עוברים לקואורדינטות קוטביות: $\Delta x=r\cos\varphi$, $\Delta y=r\sin\varphi$"
L3C = r"מקבלים $\lim_{r\to0}r\cos^3\varphi\sin\varphi$"
L4C = r"הביטוי חסום כפול $r\to0$, ולכן הגבול הוא $0$ ו-$f$ דיפרנציאבילית ב-$(0,0)$; לכן היא גם רציפה שם"
add(1, "ג",
    rubric=rub(("הצבת $f'_x(0,0)=f'_y(0,0)=0$ בהגדרת הדיפרנציאביליות", 2),
               ("מעבר לקואורדינטות קוטביות וחישוב המנה $r\\cos^3\\varphi\\sin\\varphi$", 4),
               ("חסימה $|\\cos^3\\varphi\\sin\\varphi|\\le1$ והגבול $0$", 2),
               ("מסקנה: $f$ דיפרנציאבילית ב-$(0,0)$", 1),
               ("דיפרנציאבילית גוררת רציפה, ולכן $f$ רציפה", 2)),
    pitfalls=["לבדוק דיפרנציאביליות לאורך מסלולים בלבד: גבול לאורך מסלולים לא מוכיח שהגבול הדו-ממדי קיים.",
              "לבדוק את הגבול של $f$ עצמה ולשכוח לחלק ב-$\\sqrt{\\Delta x^2+\\Delta y^2}$.",
              "להסיק שרציפות גוררת דיפרנציאביליות; הכיוון הנכון הוא דיפרנציאביליות גוררת רציפות."],
    steps=[
        num(r"לאחר ההצבה הקוטבית, המנה שווה ל-$r^k\cos^3\varphi\sin\varphi$. מהו $k$?", 1,
            r"המונה $\Delta x^3\Delta y=r^4\cos^3\varphi\sin\varphi$, המכנה $\Delta x^2+\Delta y^2=r^2$, כך ש-$f=r^2\cos^3\varphi\sin\varphi$; חלוקה ב-$\sqrt{\Delta x^2+\Delta y^2}=r$ נותנת $r^1$."),
        num(r"מהו הגבול $\lim_{r\to0}r\cos^3\varphi\sin\varphi$?", 0,
            r"הגורם $\cos^3\varphi\sin\varphi$ חסום בערך מוחלט ב-$1$ ו-$r\to0$, ולכן הגבול $0$."),
        choice(r"מה נכון לגבי $f$ ב-$(0,0)$?",
               r"דיפרנציאבילית, ולכן גם רציפה",
               [r"רציפה אך לא דיפרנציאבילית", r"דיפרנציאבילית אך לא רציפה", r"לא רציפה ולא דיפרנציאבילית"],
               r"הגבול שחישבנו הוא $0$, וזו בדיוק ההגדרה של דיפרנציאביליות. דיפרנציאבילית גוררת רציפה, ולכן שתי האפשרויות שמתארות אי-רציפות או רציפות בלבד נפסלות.", pos=1),
        order(r"סדרו את שלבי בדיקת הדיפרנציאביליות:", [L1C, L2C, L3C, L4C],
              r"קודם כותבים את הגבול מההגדרה, אחר כך עוברים לקוטביות, מפשטים לביטוי עם $r$, ורק אז אפשר להסיק."),
        findbug(r"באחד השלבים יש טעות. איזה?",
                [L1C, L2C, r"מקבלים $\lim_{r\to0}\cos^3\varphi\sin\varphi$", L4C], 2,
                r"אחרי החלוקה ב-$r$ נשאר הגורם $r$: $r\cos^3\varphi\sin\varphi$. בלעדיו הגבול לא היה מתאפס."),
    ])

add(2, "א",
    rubric=rub(("חישוב $|a_n|=\\frac{n^2+3\\ln n}{(n+1)(n+2)}$ (כי $|\\cos\\pi n|=1$)", 2),
               ("חילוק במונה ובמכנה ב-$n^2$ וחישוב הגבול $1$", 4),
               ("מסקנה: $a_n\\not\\to0$", 2),
               ("התנאי ההכרחי להתכנסות לא מתקיים, ולכן הטור מתבדר", 2)),
    pitfalls=["לראות $\\cos(\\pi n)=(-1)^n$ ולהפעיל את מבחן לייבניץ בלי לבדוק שהאיבר שואף ל-$0$.",
              "לחשב את הגבול בלי להצדיק ש-$\\frac{\\ln n}{n}\\to0$."],
    steps=[
        num(r"מהו $\lim_{n\to\infty}\dfrac{\ln n}{n}$?", 0,
            r"$\ln n$ גדל לאט מ-$n$, ולכן המנה שואפת ל-$0$."),
        num(r"מהו $\lim_{n\to\infty}|a_n|$?", 1,
            r"$\frac{1+\frac{3\ln n}{n}}{1+\frac3n+\frac2{n^2}}\to\frac11=1$."),
        choice(r"מה דינו של הטור?",
               r"מתבדר",
               [r"מתכנס בהחלט", r"מתכנס בתנאי"],
               r"$|a_n|\to1\ne0$, ולכן גם $a_n\not\to0$; התנאי ההכרחי להתכנסות נכשל. לכן אין התכנסות כלל, לא בהחלט ולא בתנאי (בפרט, לייבניץ דורש שהאיבר ישאף ל-$0$).", pos=2),
    ])

add(2, "ב",
    rubric=rub(("חסימת המונה: $1+\\frac1{\\sqrt n}\\le2$", 3), ("קבלת $|a_n|\\le\\frac2{n^3}$", 3),
               ("הטור $\\sum\\frac1{n^3}$ מתכנס (טור $p$ עם $p=3>1$)", 3),
               ("משפט ההשוואה: $\\sum|a_n|$ מתכנס", 3), ("מסקנה: הטור מתכנס בהחלט", 3)),
    pitfalls=["להפעיל את מבחן לייבניץ ולהסיק \"מתכנס בתנאי\" בלי לבדוק את טור הערכים המוחלטים.",
              "להשוות ל-$\\frac1{n^3}$ בלי החסם $1+\\frac1{\\sqrt n}\\le2$: האי-שוויון $|a_n|\\le\\frac1{n^3}$ שגוי."],
    steps=[
        num(r"מהו הערך המקסימלי של $1+\dfrac1{\sqrt n}$ עבור $n\ge1$?", 2,
            r"הביטוי יורד ב-$n$, ולכן המקסימום ב-$n=1$: $1+1=2$."),
        num(r"עבור איזה $p$ משווים לטור $\sum\dfrac1{n^p}$?", 3,
            r"$|a_n|\le\frac2{n^3}$, והטור $\sum\frac1{n^3}$ הוא טור $p$ עם $p=3>1$, שמתכנס."),
        choice(r"באיזו שיטה משתמש הפתרון הרשמי?",
               r"משפט ההשוואה של $|a_n|$ מול $\dfrac2{n^3}$",
               [r"מבחן לייבניץ לטור החילופי", r"התנאי ההכרחי $a_n\to0$", r"מבחן האינטגרל"],
               r"הפתרון חוסם את $|a_n|$ ב-$\frac2{n^3}$ ומסיק התכנסות בהחלט לפי משפט ההשוואה. לא נעשה שימוש בלייבניץ, בתנאי ההכרחי או במבחן האינטגרל.", pos=1),
        choice(r"מה דינו של הטור?",
               r"מתכנס בהחלט",
               [r"מתכנס בתנאי בלבד", r"מתבדר"],
               r"$\sum|a_n|$ מתכנס לפי ההשוואה, ולכן הטור מתכנס בהחלט (ובפרט אינו מתכנס \"בתנאי בלבד\" ואינו מתבדר)."),
    ])

add(3, "א",
    rubric=rub(("גרדיאנט כללי $\\nabla f=(2x-2(y+1),-2x)$", 2), ("הצבה ב-$(2,-1)$ ו-$\\nabla f(2,-1)=(4,-4)$", 1),
               ("הנימוק: קצב ההשתנות המקסימלי הוא בכיוון הגרדיאנט", 1)),
    pitfalls=["לבחור את הכיוון $-\\nabla f$: זה כיוון הירידה המהירה ביותר, שבו הנגזרת הכיוונית מינימלית.",
              "לשכוח את הנגזרת של $-2x(y+1)$ לפי $x$, שהיא $-2(y+1)$."],
    steps=[
        num(r"מהו $f'_x(2,-1)$?", 4,
            r"$f'_x=2x-2(y+1)=4-0=4$."),
        num(r"מהו $f'_y(2,-1)$?", -4,
            r"$f'_y=-2x=-4$."),
        choice(r"באיזה כיוון קצב ההשתנות מקסימלי?",
               r"בכיוון הגרדיאנט $(4,-4)$",
               [r"בכיוון $(-4,4)$", r"בכיוון $(1,1)$", r"בכיוון $(4,4)$"],
               r"הנגזרת הכיוונית בכיוון $\vec u$ היא $\nabla f\cdot\vec u$ והיא מקסימלית כש-$\vec u$ בכיוון הגרדיאנט. בכיוון $(-4,4)$ היא שלילית (מינימלית), ובכיוונים $(1,1)$ ו-$(4,4)$ היא $0$.", pos=3),
    ])

add(3, "ב",
    rubric=rub(("נורמת הכיוון: $\\|(-3,4)\\|=5$", 1), ("וקטור יחידה $\\left(-\\frac35,\\frac45\\right)$", 1),
               ("מכפלה סקלרית עם $\\nabla f(2,-1)=(4,-4)$", 1), ("תוצאה $-\\frac{28}5$", 1)),
    pitfalls=["לחשב את המכפלה הסקלרית עם הוקטור $(-3,4)$ בלי לנרמל, ולקבל $-28$.",
              "טעות סימן במכפלה הסקלרית: $4\\cdot(-3)-4\\cdot4$."],
    steps=[
        num(r"מהי הנורמה $\|(-3,4)\|$?", 5, r"$\sqrt{9+16}=5$."),
        num(r"מהי המכפלה הסקלרית $(4,-4)\cdot(-3,4)$ (לפני הנרמול)?", -28, r"$-12-16=-28$."),
        num(r"מהי הנגזרת הכיוונית $\frac{\partial f}{\partial\vec a}(2,-1)$?", -5.6,
            r"מנרמלים: $\frac{-28}{5}=-5.6$."),
    ])

add(3, "ג",
    rubric=rub(("$f'_y=-2x=0$ ולכן $x=0$", 2), ("הצבה ב-$f'_x=0$: $y=-1$, ולכן הנקודה הקריטית היחידה היא $(0,-1)$", 2),
               ("נגזרות שניות $A=2$, $B=-2$, $C=0$", 1), ("$\\Delta=AC-B^2=-4<0$, ולכן נקודת אוכף", 2)),
    pitfalls=["להניח ש-$y=0$ גם כן: מ-$f'_y=0$ מקבלים רק $x=0$, ואת $y$ מוצאים מ-$f'_x=0$.",
              "לסווג לפי סימן $A$ בלבד ולא לפי $\\Delta$."],
    steps=[
        num(r"מהו ערך $y$ של הנקודה הקריטית?", -1,
            r"$f'_y=-2x=0$ נותן $x=0$; אז $f'_x=2x-2(y+1)=-2(y+1)=0$ נותן $y=-1$."),
        num(r"מהו $\Delta=AC-B^2$ בנקודה הקריטית?", -4,
            r"$A=2$, $B=-2$, $C=0$, ולכן $\Delta=0-4=-4$."),
        choice(r"איך מסווגים את הנקודה הקריטית?",
               r"נקודת אוכף",
               [r"מינימום מקומי", r"מקסימום מקומי", r"המבחן אינו מכריע"],
               r"$\Delta<0$, ולכן הנקודה היא נקודת אוכף. המבחן אינו מכריע רק כש-$\Delta=0$, ומינימום או מקסימום דורשים $\Delta>0$.", pos=3),
    ])

add(3, "ד",
    rubric=rub(("הנקודה הקריטית בפנים התחום $(0,-1)$ וערך הפונקציה בה $3$", 2),
               ("הצלע $x=1$: $f(1,y)=2-2y$ ליניארית, לכן הקצוות $A,B$", 2),
               ("הצלע $y=-2$: $g(x)=x^2+2x+3$ עם נקודה קריטית $x=-1$", 2),
               ("הצלע $y=x$: $h(x)=-x^2-2x+3$ עם נקודה קריטית $x=-1$", 2),
               ("השוואת הערכים: מקסימום $6$, מינימום $0$", 2)),
    pitfalls=["לשכוח לבדוק את קודקודי המשולש ואת הנקודות הקריטיות של כל צלע בנפרד.",
              "לא לבדוק שהנקודה הקריטית $(0,-1)$ אכן בתוך התחום לפני שמוסיפים אותה לרשימת המועמדים."],
    steps=[
        num(r"מהו $f(0,-1)$?", 3, r"$0-0+3=3$."),
        num(r"על הצלע $y=-2$ מתקבל $g(x)=x^2+2x+3$. מהו $x$ שבו $g'(x)=0$?", -1, r"$g'(x)=2x+2=0$ נותן $x=-1$."),
        num(r"מהו $f(-1,-1)$ (הנקודה הקריטית על הצלע $y=x$)?", 4, r"$f(x,x)=-x^2-2x+3$, ובהצבת $x=-1$: $-1+2+3=4$."),
        num(r"מהו הערך המקסימלי של $f$ ב-$D$?", 6,
            r"המועמדים: $f(A)=0$, $f(B)=6$, $f(C)=3$, $f(D)=2$, $f(E)=4$, $f(0,-1)=3$. הגדול ביותר הוא $6$ ב-$B(1,-2)$."),
        num(r"מהו הערך המינימלי של $f$ ב-$D$?", 0, r"הקטן ביותר מבין המועמדים הוא $0$ ב-$A(1,1)$."),
    ])

add(4, "א",
    rubric=rub(("כלל השרשרת $z'_x=z'_uu'_x+z'_vv'_x$ ו-$z'_y$ באופן דומה", 2), ("$z'_u=2v$ ו-$z'_v=2u+6v$", 2),
               ("$u'_x=-\\sin(x-3y)$, $u'_y=3\\sin(x-3y)$, ובנקודה $u=1$ ושתי הנגזרות $0$", 2),
               ("$z'_x(\\pi,-\\pi)=70$", 2), ("$z'_y(\\pi,-\\pi)=56$", 2)),
    pitfalls=["להתעלם מהתלות הישירה של $z$ ב-$v$ ולגזור רק דרך $u$.",
              "בנקודה $x-3y=4\\pi$, ולכן $\\cos(4\\pi)=1$ ו-$\\sin(4\\pi)=0$; טעות בערכים אלה הורסת את שני הסעיפים."],
    steps=[
        num(r"מהו $u(\pi,-\pi)=\cos(x-3y)$ בנקודה?", 1, r"$x-3y=\pi+3\pi=4\pi$ ו-$\cos4\pi=1$."),
        num(r"מהו $z'_v=2u+6v$ בנקודה?", 14, r"$2\cdot1+6\cdot2=14$."),
        num(r"מהו $z'_x(\pi,-\pi)$?", 70, r"$u'_x=-\sin4\pi=0$, ולכן $z'_x=2v\cdot0+14\cdot5=70$."),
        num(r"מהו $z'_y(\pi,-\pi)$?", 56, r"$u'_y=3\sin4\pi=0$, ולכן $z'_y=2v\cdot0+14\cdot4=56$."),
    ])

add(4, "ב",
    rubric=rub(("רדיוס ההתכנסות: $\\frac1R=2$ ולכן $R=\\frac12$", 3), ("הקטע הפתוח $\\frac12<x<\\frac32$ ומעבר לבדיקת שני הקצוות", 2),
               ("$x=\\frac12$: טור לייבניץ $\\sum\\frac{(-1)^n}{\\sqrt{n+4}}$ מתכנס", 4),
               ("$x=\\frac32$: השוואה גבולית ל-$\\sum\\frac1{\\sqrt n}$ מראה שהטור מתבדר", 4),
               ("תחום ההתכנסות $[\\frac12,\\frac32)$", 2)),
    pitfalls=["לחשב את הקצה השמאלי כ-$-\\frac12$; הקצוות הם $1\\pm\\frac12$.",
              "להסיק שגם ב-$x=\\frac32$ הטור מתכנס; $\\sum\\frac1{\\sqrt{n+4}}$ דומה ל-$\\sum\\frac1{\\sqrt n}$, שמתבדר."],
    steps=[
        num(r"מהו רדיוס ההתכנסות $R$?", 0.5, r"$\frac1R=\lim\frac{a_{n+1}}{a_n}=2$, ולכן $R=\frac12$."),
        num(r"מהו הקצה השמאלי של קטע ההתכנסות (מרכז $1$)?", 0.5, r"$1-R=1-\frac12=\frac12$."),
        choice(r"מה קורה בקצה השמאלי $x=\frac12$ (הטור $\sum\frac{(-1)^n}{\sqrt{n+4}}$)?",
               r"מתכנס בתנאי",
               [r"מתבדר", r"מתכנס בהחלט"],
               r"האיברים $\frac1{\sqrt{n+4}}$ חיוביים, יורדים ושואפים ל-$0$, ולכן לפי לייבניץ הטור מתכנס. טור הערכים המוחלטים $\sum\frac1{\sqrt{n+4}}$ מתבדר (כמו $\sum\frac1{\sqrt n}$), ולכן ההתכנסות אינה בהחלט.", pos=1),
        choice(r"מה קורה בקצה הימני $x=\frac32$ (הטור $\sum\frac1{\sqrt{n+4}}$)?",
               r"מתבדר",
               [r"מתכנס בתנאי", r"מתכנס בהחלט"],
               r"$\lim\frac{1/\sqrt{n+4}}{1/\sqrt n}=1$ ו-$\sum\frac1{\sqrt n}$ מתבדר ($p=\frac12\le1$), ולכן הטור מתבדר. הטור חיובי, ולכן אין הבדל בין התכנסות להתכנסות בהחלט, ושתי האפשרויות האחרות נפסלות.", pos=2),
        choice(r"מהו תחום ההתכנסות?",
               r"$\left[\frac12,\frac32\right)$",
               [r"$\left[-\frac12,\frac32\right)$", r"$\left[\frac12,\frac32\right]$", r"$\left(\frac12,\frac32\right)$"],
               r"הקצה השמאלי $\frac12$ נכלל (לייבניץ) והימני $\frac32$ לא (התבדרות). הקצה השמאלי הוא $1-\frac12=\frac12$ ולא $-\frac12$."),
    ])

add(5, "א",
    rubric=rub(("פירוק $6x^2+5x+1=(3x+1)(2x+1)$ ופיצול הלוגריתם לסכום", 3),
               ("פיתוח $\\ln(1+t)=\\sum\\frac{(-1)^{n+1}}{n}t^n$ עם $t=3x$ ועם $t=2x$", 3),
               ("חיבור הטורים: המקדם הוא $\\frac{(-1)^{n+1}(3^n+2^n)}{n}$", 2)),
    pitfalls=["לנסות לפתח את הלוגריתם של הפולינום כולו במקום לפרק אותו לגורמים.",
              "לשכוח שהחזקות הן $3^n$ ו-$2^n$ (כי מציבים $t=3x$ ו-$t=2x$)."],
    steps=[
        choice(r"איך נכון לפרק את $\ln(6x^2+5x+1)$?",
               r"$\ln(3x+1)+\ln(2x+1)$",
               [r"$\ln(3x+1)\cdot\ln(2x+1)$", r"$\ln(6x+1)+\ln(x+1)$", r"$\ln(3x+2)+\ln(2x+1)$"],
               r"$(3x+1)(2x+1)=6x^2+5x+1$ והלוגריתם של מכפלה הוא סכום הלוגריתמים. ב-$(6x+1)(x+1)$ מתקבל $6x^2+7x+1$ וב-$(3x+2)(2x+1)$ מתקבל $6x^2+7x+2$; ומכפלת לוגריתמים אינה שווה ללוגריתם של מכפלה.", pos=2),
        num(r"מהו מקדם $x$ בטור, כלומר $\frac{(-1)^{2}(3+2)}{1}$?", 5, r"$n=1$: $(3^1+2^1)/1=5$."),
        num(r"מהו מקדם $x^2$ בטור?", -6.5, r"$n=2$: $\frac{(-1)^3(9+4)}{2}=-\frac{13}{2}=-6.5$."),
        num(r"מהו מקדם $x^3$ בטור (תשובה עשרונית, דיוק $0.001$)?", 11.6667, r"$n=3$: $\frac{27+8}{3}=\frac{35}3\approx11.667$.", tol=0.001),
    ])

add(5, "ב",
    rubric=rub(("חישוב $\\sqrt[n]{\\frac{3^n+2^n}{n}}\\to3$ (הגורם $\\left(1+\\left(\\frac23\\right)^n\\right)^{1/n}\\to1$ ו-$\\sqrt[n]n\\to1$)", 4),
               ("רדיוס ההתכנסות $R=\\frac13$", 2), ("תחום ההתכנסות $\\left(-\\frac13,\\frac13\\right]$, כולל בדיקת הקצוות", 2)),
    pitfalls=["לשכוח לבדוק את הקצוות ולכתוב את התחום כקטע פתוח.",
              "לטעות בחישוב השורש: $\\sqrt[n]{3^n+2^n}\\to3$ ולא $\\to5$."],
    steps=[
        num(r"מהו $\lim_{n\to\infty}\sqrt[n]{1+\left(\frac23\right)^n}$?", 1,
            r"$\left(\frac23\right)^n\to0$, ולכן $1\le\sqrt[n]{1+(2/3)^n}\le\sqrt[n]2\to1$."),
        num(r"מהו רדיוס ההתכנסות (תשובה עשרונית, דיוק $0.001$)?", 0.3333,
            r"$\frac1R=3$, ולכן $R=\frac13\approx0.333$.", tol=0.001),
        choice(r"מהו תחום ההתכנסות?",
               r"$\left(-\frac13,\frac13\right]$",
               [r"$\left[-\frac13,\frac13\right]$", r"$\left(-\frac13,\frac13\right)$", r"$\left[-\frac13,\frac13\right)$"],
               r"פיתוח $\ln(1+t)$ תקף עבור $-1<t\le1$, ולכן $-\frac13<x\le\frac13$: הקצה הימני נכלל והשמאלי לא (שם הטור דומה לטור ההרמוני ומתבדר).", pos=1),
    ])

add(5, "ג",
    rubric=rub(("הקשר $\\frac{f^{(n)}(0)}{n!}=$ מקדם $x^n$ בטור", 2), ("הצבת $n=5$: $\\frac{3^5+2^5}{5}=55$", 3), ("$f^{(5)}(0)=55\\cdot5!=6600$", 2)),
    pitfalls=["לשכוח להכפיל ב-$5!$ בסוף.",
              "טעות בסימן: עבור $n=5$ הגורם $(-1)^{n+1}$ שווה $+1$."],
    steps=[
        num(r"מהו $3^5+2^5$?", 275, r"$243+32=275$."),
        num(r"מהו מקדם $x^5$ בטור, כלומר $\frac{f^{(5)}(0)}{5!}$?", 55, r"$\frac{275}{5}=55$ (הסימן $(-1)^6=+1$)."),
        num(r"מהו $f^{(5)}(0)$?", 6600, r"$55\cdot120=6600$."),
    ])

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
