# -*- coding: utf-8 -*-
"""Generator for tools/raw/24A-A.json -- calculus-2 (20252), semester A 2024, moed A (4/4/2024).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24A-A.py

Source: "questions 4.4.2024" (3 pages, 5 questions of 25 points, a=12, b=13, solve 4 of 5).
Key: "answers 4.4.2024" (13 pages, mixed: Q1 handwritten on a tablet, Q2 handwritten on squared paper, Q3 and Q4 typed,
Q5 handwritten on dotted paper). Header (lecturer names) is not transcribed.

Transcription notes
- Text layers are garbled; everything is transcribed from page renders.
- Q2a asks for two series in one part; stored as one item.
- Q1b: the key only gives grad f(1,0)=(-4/e,0) and says the maximal rate is in the gradient direction; the unit
  vector (-1,0) is the obvious normalisation and is stated as such.
- Q2b: the key writes the increment as Delta f = f_x dx + f_y dy + eps*sqrt(dx^2+dy^2) and shows eps -> 0 in polar form.
- Q5a: the key names the Hessian determinant Delta.

Key labelling (orchestrator ruling 2026-10-24): the key is handwritten/mixed with no named author, so every item is
solutionSource "student-solution", official False.

Checks (tools/verify/24A-A/check.py, sympy + numeric): every limit, series test, partial derivative, Hessian,
Lagrange point, series sum and Maclaurin coefficient matches the key. No disagreement; nothing is held.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24A-A.json"


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
$$f(x,y)=\begin{cases}\dfrac{x^3y-xy^3}{x^2+y^2}, & (x,y)\neq(0,0)\\[2mm] 0, & (x,y)=(0,0)\end{cases}$$
האם היא רציפה בנקודה $(x,y)=(0,0)$? נמקו את תשובתכם.""",
r"""נעבור לקואורדינטות קוטביות:
$$\lim_{(x,y)\to(0,0)}\frac{x^3y-xy^3}{x^2+y^2}=\lim_{r\to0}\frac{r^4\left(\cos^3\theta\sin\theta-\cos\theta\sin^3\theta\right)}{r^2}$$
$$=\lim_{r\to0}r^2\left(\cos^3\theta\sin\theta-\cos\theta\sin^3\theta\right)=0$$
(אפס כפול פונקציה חסומה).
$$\lim_{(x,y)\to(0,0)}f(x,y)=0=f(0,0)$$
ערך הגבול ב-$(0,0)$ שווה לערך הפונקציה ב-$(0,0)$, ולכן הפונקציה **רציפה** ב-$(0,0)$.""", part="א", points=12))

# ===== Q1b =====
questions.append(Q(1, "computation", "gradient_directional", r"""מצאו את הכיוון בו קצב ההשתנות של הפונקציה $f(x,y)=2e^{-x^2}+e^{-3y^2}$ בנקודה $(1,0)$ הוא מקסימלי. נמקו את תשובתכם.""",
r"""הכיוון בו קצב ההשתנות של הפונקציה הוא מקסימלי בנקודה $(1,0)$ הוא כיוון הגרדיאנט בנקודה $(1,0)$.
$$\nabla f(x,y)=(f'_x,f'_y)=\left(-4x\cdot e^{-x^2},\ -6y\,e^{-3y^2}\right)$$
$$\nabla f(1,0)=\left(-\frac{4}{e},0\right)$$
נימוק:
$$\frac{\partial f(x,y)}{\partial\vec u}=\left|\nabla f(x,y)\right|\cdot\cos\delta$$
כאשר $\delta$ היא הזווית בין הוקטור $\vec u$ לבין הגרדיאנט.
מכאן בכיוון הגרדיאנט מתקבל הערך המקסימלי של הנגזרת הכיוונית. לכן הכיוון המבוקש הוא כיוון $\left(-\frac{4}{e},0\right)$, כלומר הוקטור היחידה $(-1,0)$.""", part="ב", points=13))

# ===== Q2a =====
questions.append(Q(2, "computation", "numeric_series", r"""בדקו התכנסות בהחלט, בתנאי או התבדרות של הטורים הבאים:
$$\sum_{n=1}^{\infty}(-1)^n\sin\frac{1}{\sqrt{n}}$$
$$\sum_{n=1}^{\infty}(-1)^n\left(\sqrt{n}-\sqrt{n-1}\right)$$""",
r"""**הטור הראשון.** נבדוק את ההתכנסות בהחלט:
$$\sum_{n=1}^{\infty}\left|(-1)^n\sin\frac{1}{\sqrt{n}}\right|=\sum_{n=1}^{\infty}\sin\frac{1}{\sqrt{n}}\sim\frac{1}{\sqrt{n}}=b_n$$
$$\lim_{n\to\infty}\frac{a_n}{b_n}=\lim_{n\to\infty}\frac{\sin\frac{1}{\sqrt{n}}}{\frac{1}{\sqrt{n}}}=1$$
הטור $\sum b_n$ מתבדר כטור הרמוני מוכלל עם $p=\frac{1}{2}<1$, לכן לפי מבחן ההשוואה הטור המקורי אינו מתכנס בהחלט.
נבדוק את ההתכנסות בתנאי: $\sum_{n=1}^{\infty}(-1)^n\sin\frac{1}{\sqrt{n}}$. לפי מבחן לייבניץ נבדוק את הסדרה $\{a_n\}=\left\{\sin\frac{1}{\sqrt{n}}\right\}$.
הסדרה מונוטונית יורדת: $y=\sin x$ היא פונקציה מונוטונית עולה בקטע $\left[0,\frac{\pi}{2}\right]$ ומתקיים $\frac{1}{\sqrt{n+1}}<\frac{1}{\sqrt{n}}$, לכן $\sin\frac{1}{\sqrt{n+1}}<\sin\frac{1}{\sqrt{n}}$.
הסדרה $\{a_n\}$ שואפת לאפס:
$$\lim_{n\to\infty}\sin\frac{1}{\sqrt{n}}=\sin0=0$$
לכן לפי מבחן לייבניץ הטור מתכנס $\Rightarrow$ הטור המקורי **מתכנס בתנאי**.

**הטור השני.** $\sum_{n=1}^{\infty}(-1)^n\left(\sqrt{n}-\sqrt{n-1}\right)$. נבדוק את ההתכנסות בהחלט של הטור:
$$\sum_{n=1}^{\infty}\left|(-1)^n\frac{1}{\sqrt{n}+\sqrt{n-1}}\right|=\sum_{n=1}^{\infty}\frac{1}{\sqrt{n}+\sqrt{n-1}}\sim\sum\frac{1}{\sqrt{n}}=\sum b_n$$
לפי מבחן ההשוואה, נקבל
$$\lim_{n\to\infty}\frac{a_n}{b_n}=\lim_{n\to\infty}\frac{\frac{1}{\sqrt{n}+\sqrt{n-1}}}{\frac{1}{\sqrt{n}}}=\lim_{n\to\infty}\frac{\sqrt{n}}{\sqrt{n}+\sqrt{n-1}}=\lim_{n\to\infty}\frac{1}{1+\sqrt{1-\frac{1}{n}}}=\frac{1}{2}.$$
הטורים מתבדרים ביחד, לכן אין התכנסות בהחלט.
נבדוק את ההתכנסות בתנאי: $\sum_{n=1}^{\infty}(-1)^n\frac{1}{\sqrt{n}+\sqrt{n-1}}$. נסמן $\{a_n\}=\left\{\frac{1}{\sqrt{n}+\sqrt{n-1}}\right\}$, הסדרה מונוטונית יורדת:
$$a_{n+1}=\frac{1}{\sqrt{n+1}+\sqrt{n}}<\frac{1}{\sqrt{n}+\sqrt{n-1}}=a_n$$
$$\lim_{n\to\infty}a_n=\lim_{n\to\infty}\frac{1}{\sqrt{n+1}+\sqrt{n}}=0$$
לכן לפי מבחן לייבניץ הטור המקורי **מתכנס בתנאי**.""", part="א", points=12))

# ===== Q2b =====
questions.append(Q(2, "computation", "partials_differentiability", r"""נתונה הפונקציה
$$f(x,y)=\begin{cases}xy\cdot\dfrac{x^2-y^2}{x^2+y^2}, & (x,y)\neq(0,0)\\[2mm] 0, & (x,y)=(0,0)\end{cases}$$
מצאו את $f'_x(0,0)$ ו-$f'_y(0,0)$. האם $f(x,y)$ דיפרנציאבילית ב-$(0,0)$?""",
r"""$$f'_x(0,0)=\lim_{\Delta x\to0}\frac{f(0+\Delta x,0)-f(0,0)}{\Delta x}=\lim_{\Delta x\to0}\frac{\Delta x\cdot0\cdot\frac{\Delta x^2-0^2}{\Delta x^2+0^2}-0}{\Delta x}=\lim_{\Delta x\to0}\frac{0}{\Delta x}=0$$
באופן דומה $f'_y(0,0)=0$.
נבדוק את ההגדרה של דיפרנציאביליות:
$$\Delta f(0,0)=\Delta x\cdot\Delta y\,\frac{\Delta x^2-\Delta y^2}{\Delta x^2+\Delta y^2}$$
$$\Delta f(0,0)=f'_x(0,0)\cdot\Delta x+f'_y(0,0)\cdot\Delta y+\varepsilon\sqrt{\Delta x^2+\Delta y^2}\qquad(f'_x(0,0)=0,\ f'_y(0,0)=0)$$
אפשר לכתוב
$$\Delta x\,\Delta y\,\frac{\Delta x^2-\Delta y^2}{\Delta x^2+\Delta y^2}=\varepsilon\sqrt{\Delta x^2+\Delta y^2}\ \Rightarrow$$
$$\lim_{\substack{\Delta x\to0\\ \Delta y\to0}}\varepsilon(\Delta x,\Delta y)=\lim_{\substack{\Delta x\to0\\ \Delta y\to0}}\frac{\Delta x\cdot\Delta y\left(\Delta x^2-\Delta y^2\right)}{\left(\Delta x^2+\Delta y^2\right)^{3/2}}=$$
נציב $\{\Delta x=\rho\cos\theta,\ \Delta y=\rho\sin\theta\}$:
$$=\lim_{\rho\to0}\frac{\rho^4\cos\theta\sin\theta\left(\cos^2\theta-\sin^2\theta\right)}{\left(\rho^2\right)^{3/2}}=\lim_{\rho\to0}\rho\,\frac{1}{2}\sin2\theta\cdot\cos2\theta=\lim_{\rho\to0}\rho\,\frac{1}{4}\sin4\theta=0$$
(אפס כפול פונקציה חסומה).
לכן הפונקציה $f(x,y)$ **דיפרנציאבילית** ב-$(0,0)$.""", part="ב", points=13))

# ===== Q3a =====
questions.append(Q(3, "computation", "power_series", r"""עבור אילו ערכי $x$ הטור מתכנס (מצאו רדיוס התכנסות ותחום התכנסות).
$$\sum_{n=1}^{\infty}\frac{2^n(x+1)^n}{n^2+1}$$""",
r"""בוא נכתוב $s=x+1$ וננתח את הטור $\sum_{n=1}^{\infty}\frac{2^n}{n^2+1}s^n$. אזי $a_n=\dfrac{2^n}{n^2+1}$,
$$R=\lim_{n\to\infty}\left|\frac{a_n}{a_{n+1}}\right|=\frac{2^n}{n^2+1}\cdot\frac{(n+1)^2+1}{2^{n+1}}=\frac{1}{2}\cdot\frac{n^2+2n+2}{n^2+1}=\frac{1}{2}$$
לכן הטור מתכנס כאשר $s\in\left(-\frac{1}{2},\frac{1}{2}\right)$.
כאשר $s=-\frac{1}{2}$ מקבלים הטור
$$\sum_{n=1}^{\infty}\frac{2^n}{n^2+1}\left(-\frac{1}{2}\right)^n$$
ושימוש במשפט לייבניץ הטור מתכנס. עכשיו, עבור $s=\frac{1}{2}$ מקבלים הטור
$$\sum_{n=1}^{\infty}\frac{2^n}{n^2+1}\frac{1}{2^n}=\sum_{n=1}^{\infty}\frac{1}{n^2+1}$$
מאז $\frac{1}{n^2+1}\le\frac{1}{n^2}$ אנו מסיקים שהטור מתכנס. אזי התחום התכנסות של הטור $\sum_{n=1}^{\infty}\frac{2^n}{n^2+1}s^n$ הוא $\left[-\frac{1}{2},\frac{1}{2}\right]$ וזה מרמז על כך התחום התכנסות של הטור המקורי הוא $\left[-\frac{3}{2},-\frac{1}{2}\right]$.""", part="א", points=12))

# ===== Q3b =====
questions.append(Q(3, "proof", "chain_rule_identity", r"""הוכיחו שהפונקציה $u=x^kF\left(\dfrac{z}{x};\dfrac{y}{x}\right)$ כאשר $F$ בעלת נגזרות חלקיות ורציפות מקיימת את המשוואה $x\dfrac{\partial u}{\partial x}+y\dfrac{\partial u}{\partial y}+z\dfrac{\partial u}{\partial z}=ku$.""",
r"""$F=F(s,t)$ כאשר $s(x,y,z)=\dfrac{z}{x},\quad t(x,y,z)=\dfrac{y}{x}$.
$$\frac{\partial s}{\partial x}=-\frac{z}{x^2};\quad\frac{\partial s}{\partial y}=0;\quad\frac{\partial s}{\partial z}=\frac{1}{x};$$
$$\frac{\partial t}{\partial x}=-\frac{y}{x^2};\quad\frac{\partial t}{\partial y}=\frac{1}{x};\quad\frac{\partial t}{\partial z}=0;$$
$\Longrightarrow$
$$\frac{\partial F}{\partial x}=\frac{\partial F}{\partial s}\frac{\partial s}{\partial x}+\frac{\partial F}{\partial t}\frac{\partial t}{\partial x}=\frac{\partial F}{\partial s}\left(-\frac{z}{x^2}\right)+\frac{\partial F}{\partial t}\left(-\frac{y}{x^2}\right)=-\frac{1}{x^2}\left(\frac{\partial F}{\partial s}z+\frac{\partial F}{\partial t}y\right);$$
$$\frac{\partial F}{\partial y}=\frac{\partial F}{\partial s}\frac{\partial s}{\partial y}+\frac{\partial F}{\partial t}\frac{\partial t}{\partial y}=\frac{\partial F}{\partial s}\cdot0+\frac{\partial F}{\partial t}\frac{1}{x}=\frac{1}{x}\frac{\partial F}{\partial t};$$
$$\frac{\partial F}{\partial z}=\frac{\partial F}{\partial s}\frac{\partial s}{\partial z}+\frac{\partial F}{\partial t}\frac{\partial t}{\partial z}=\frac{\partial F}{\partial s}\frac{1}{x}+\frac{\partial F}{\partial t}\cdot0=\frac{1}{x}\frac{\partial F}{\partial s};$$
$\Longrightarrow$
$$\frac{\partial u}{\partial x}=kx^{k-1}F\left(\frac{z}{x},\frac{y}{x}\right)+x^k\frac{\partial F}{\partial x}=kx^{k-1}F\left(\frac{z}{x},\frac{y}{x}\right)-x^{k-2}\left(\frac{\partial F}{\partial s}z+\frac{\partial F}{\partial t}y\right);$$
$$\frac{\partial u}{\partial y}=x^k\frac{\partial F}{\partial y}=x^k\frac{1}{x}\frac{\partial F}{\partial t}=x^{k-1}\frac{\partial F}{\partial t};$$
$$\frac{\partial u}{\partial z}=x^k\frac{\partial F}{\partial z}=x^k\frac{1}{x}\frac{\partial F}{\partial s}=x^{k-1}\frac{\partial F}{\partial s};$$
$\Longrightarrow$
$$x\frac{\partial u}{\partial x}+y\frac{\partial u}{\partial y}+z\frac{\partial u}{\partial z}=x\left(kx^{k-1}F\left(\frac{z}{x},\frac{y}{x}\right)-x^{k-2}z\frac{\partial F}{\partial s}-x^{k-2}y\frac{\partial F}{\partial t}\right)+$$
$$+\ yx^{k-1}\frac{\partial F}{\partial t}+zx^{k-1}\frac{\partial F}{\partial s}=kx^kF\left(\frac{z}{x},\frac{y}{x}\right)=ku.$$""", part="ב", points=13))

# ===== Q4a =====
questions.append(Q(4, "computation", "numeric_series", r"""חשבו את סכום הטור
$$\sum_{n=1}^{\infty}\frac{1}{n^2+6n+8}$$""",
r"""נציג את הטור בצורה
$$\sum_{n=1}^{\infty}\frac{1}{(n+2)(n+4)}=\frac{1}{2}\sum_{n=1}^{\infty}\left[\frac{1}{n+2}-\frac{1}{n+4}\right].$$
אז סדרת הסכומים החלקיים שלו תתנהג באופן הבא:
$$S_n=\frac{1}{2}\sum_{k=1}^{n}\left[\frac{1}{k+2}-\frac{1}{k+4}\right]=\frac{1}{2}\left[\left(\frac{1}{3}-\frac{1}{5}\right)+\left(\frac{1}{4}-\frac{1}{6}\right)+\left(\frac{1}{5}-\frac{1}{7}\right)+\left(\frac{1}{6}-\frac{1}{8}\right)+\left(\frac{1}{7}-\frac{1}{9}\right)+\cdots+\left(\frac{1}{n+2}-\frac{1}{n+4}\right)\right]$$
$$=\frac{1}{2}\left(\frac{1}{3}+\frac{1}{4}-\frac{1}{n+3}-\frac{1}{n+4}\right)=\frac{1}{2}\left(\frac{7}{12}-\frac{2n+7}{(n+3)(n+4)}\right)$$
$$\Rightarrow\ S=\lim_{n\to\infty}S_n=\frac{7}{24}$$""", part="א", points=12))

# ===== Q4b =====
questions.append(Q(4, "computation", "absolute_extrema", r"""מצאו אקסטרמומים מוחלטים של הפונקציה $f(x,y)=x\cdot y$ תחת האילוץ $x^2+y^2=2$""",
r"""נגדיר את האילוץ כ-$g(x,y)=x^2+y^2=2$ ונבנה מערכת של לגרנז' המתאימה לבעיה הזאת:
$$\begin{cases}f(x,y)=xy\to\min/\max\\ g(x,y)=x^2+y^2=2\end{cases}\Leftarrow\begin{cases}\nabla f(x,y)=\lambda\nabla g(x,y)\\ g(x,y)=x^2+y^2=2\end{cases}\Leftarrow\begin{cases}y=2\lambda x\\ x=2\lambda y\\ x^2+y^2=2\end{cases}$$
ברור שאם $\lambda=0$, אז $x=y=0$ והאילוץ לא יכול להתקיים. לכן, $\lambda\neq0$ ואז
$$\begin{cases}\dfrac{y}{2x}=\lambda\\[2mm] \dfrac{x}{2y}=\lambda\end{cases}\Rightarrow\frac{y}{2x}=\frac{x}{2y}\Rightarrow x^2=y^2.$$
אם נציב את הקשר הזה באילוץ, אז נקבל $x^2+x^2=2\Rightarrow x^2=1\Rightarrow x=\pm1$ ומכאן גם $y=\pm1$.
כתוצאה מכך, נקבל 4 נקודות חשודות: $(1,1),(1,-1),(-1,1),(-1,-1)$ ולכן
$$\begin{cases}f(1,1)=f(-1,-1)=1=f_{max}\\ f(1,-1)=f(-1,1)=-1=f_{min}\end{cases}$$""", part="ב", points=13))

# ===== Q5a =====
questions.append(Q(5, "computation", "local_extrema", r"""מצאו וסווגו את נקודות האקסטרמום של הפונקציה:
$$f(x,y)=x^3+8y^3-6xy+1$$""",
r"""$$\begin{cases}f'_x=3x^2-6y=0\\ f'_y=24y^2-6x=0\end{cases}\Rightarrow\begin{cases}x=4y^2\\ 3\cdot(4y^2)^2-6y=0\Rightarrow y\left(8y^3-1\right)=0\end{cases}$$
נקודות קריטיות:
$$\begin{cases}y_1=0\Rightarrow x_1=0\\ y_2=\frac{1}{2}\Rightarrow x_2=1\end{cases}$$
$$f''_{xx}=6x,\quad f''_{xy}=f''_{yx}=-6,\quad f''_{yy}=48y$$
בנקודה $(0,0)$: $\Delta=f''_{xx}\cdot f''_{yy}-\left(f''_{xy}\right)^2=-36<0$.
אז $(0,0)$ היא **נקודת אוכף**.
בנקודה $\left(1,\frac{1}{2}\right)$: $\Delta=f''_{xx}\cdot f''_{yy}-\left(f''_{xy}\right)^2=6\cdot24-36>0$, $f''_{xx}=6>0$.
אז $\left(1,\frac{1}{2}\right)$ היא **נקודת מינימום**.""", part="א", points=12))

# ===== Q5b =====
questions.append(Q(5, "computation", "taylor_maclaurin", r"""פתחו את הפונקציה $f(x)=\dfrac{1}{1-3x^2}$ לטור מקלורן. מהו תחום התכנסות הטור?
הסיקו את הערך של $f^{(5)}(0)$.""",
r"""$$f(x)=\frac{1}{1-3x^2}=\sum_{n=0}^{\infty}\left(3x^2\right)^n=\sum_{n=0}^{\infty}3^nx^{2n}$$
הטור מתכנס עבור $\left|3x^2\right|<1\iff|x|^2<\frac{1}{3}\iff|x|<\frac{1}{\sqrt{3}}$.
עבור $3x^2=1\iff x=\frac{1}{\sqrt{3}}$ הטור מתבדר.
עבור $3x^2=1\iff x=-\frac{1}{\sqrt{3}}$ הטור מתבדר.
$$f(x)=\sum_{n=0}^{\infty}\frac{f^{(n)}(0)}{n!}x^n=\sum_{n=0}^{\infty}c_nx^n$$
(ישנן חזקות זוגיות בלבד) $0=5!\,c_5=f^{(5)}(0)$.""", part="ב", points=13))

# ---- rubric / pitfalls / steps (ai-verified). Every expected value is re-computed in tools/verify/24A-A/steps_24A-A.py ----
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
            q["rubricSource"] = "ai-verified"
            q["stepsSource"] = "ai-verified"
            return
    raise KeyError((n, part))


add(1, "א",
    rubric=rub(("מעבר לקואורדינטות קוטביות והצגת הביטוי בצורה $r^2\\cdot g(\\theta)$", 4),
               ("הצדקה שהגבול הוא $0$: אפס כפול פונקציה חסומה", 4),
               ("השוואת הגבול לערך הפונקציה $f(0,0)=0$ ומסקנה שהפונקציה רציפה", 4)),
    pitfalls=["לבדוק רק לאורך מסלולים בודדים (למשל ציר $x$) ולהסיק רציפות. הגבול צריך להתקיים לכל כיוון, ולכן עוברים לקואורדינטות קוטביות.",
              "לשכוח להשוות את הגבול לערך $f(0,0)$ לפני שמסיקים רציפות."],
    steps=[
        num(r"אחרי ההצבה $x=r\cos\theta,\ y=r\sin\theta$ הביטוי הנתון שווה ל-$r^k\cdot g(\theta)$. מהו $k$?", 2,
            r"המונה הוא $r^4\left(\cos^3\theta\sin\theta-\cos\theta\sin^3\theta\right)$ והמכנה $r^2$, ולכן נשאר $r^2$."),
        num(r"הגורם הזוויתי הוא $g(\theta)=\cos^3\theta\sin\theta-\cos\theta\sin^3\theta$, והוא שווה ל-$\frac14\sin4\theta$. מהו הערך המקסימלי של $|g(\theta)|$?", 0.25,
            r"$|\sin4\theta|\le1$, ולכן $|g|\le\frac14$. הגורם הזוויתי חסום, ולכן הביטוי כולו חסום על ידי $\frac{r^2}{4}$ ושואף ל-$0$."),
        choice("מה מסקנת הפתרון לגבי רציפות הפונקציה ב-$(0,0)$?",
               "הפונקציה רציפה, כי הגבול $0$ שווה ל-$f(0,0)$",
               ["הפונקציה אינה רציפה, כי הגבול תלוי בזווית $\\theta$",
                "הפונקציה אינה רציפה, כי המכנה מתאפס ב-$(0,0)$",
                "אי אפשר להכריע, כי הגבול לא קיים"],
               "הגבול הוא $r^2$ כפול פונקציה חסומה, כלומר $0$, והוא שווה ל-$f(0,0)=0$. המכנה מתאפס רק בנקודה עצמה והפונקציה מוגדרת שם בנפרד.", pos=2),
    ])

add(1, "ב",
    rubric=rub(("חישוב הנגזרות החלקיות $f'_x$ ו-$f'_y$", 4),
               ("הצבה ב-$(1,0)$ וקבלת $\\nabla f(1,0)=\\left(-\\frac4e,0\\right)$", 4),
               ("נימוק: $\\frac{\\partial f}{\\partial\\vec u}=|\\nabla f|\\cos\\delta$ ולכן הערך המקסימלי בכיוון הגרדיאנט", 3),
               ("ניסוח הכיוון כוקטור יחידה $(-1,0)$", 2)),
    pitfalls=["לחשב את הגרדיאנט אך לשכוח לנמק מדוע הכיוון המקסימלי הוא כיוון הגרדיאנט (הזווית $\\delta=0$).",
              "טעות סימן: הנגזרת של $e^{-x^2}$ היא $-2xe^{-x^2}$, ולכן מקבלים גרדיאנט שמצביע בכיוון השלילי של ציר $x$."],
    steps=[
        num(r"חשבו את $f'_x(1,0)$ עבור $f(x,y)=2e^{-x^2}+e^{-3y^2}$ (תשובה עשרונית, דיוק $0.001$).", -1.4715,
            r"$f'_x=-4xe^{-x^2}$, ולכן $f'_x(1,0)=-\frac{4}{e}\approx-1.4715$.", tol=0.001),
        num(r"חשבו את $f'_y(1,0)$.", 0,
            r"$f'_y=-6ye^{-3y^2}$, ולכן $f'_y(1,0)=0$."),
        choice("איזה וקטור יחידה נותן את קצב ההשתנות המקסימלי ב-$(1,0)$?",
               "$(-1,0)$", ["$(1,0)$", "$(0,1)$", "$(0,-1)$"],
               "הגרדיאנט הוא $\\left(-\\frac4e,0\\right)$, כלומר מצביע בכיוון השלילי של ציר $x$, ולכן וקטור היחידה בכיוונו הוא $(-1,0)$.", pos=1),
    ])

add(2, "א",
    rubric=rub(("הטור $\\sum(-1)^n\\sin\\frac1{\\sqrt n}$: השוואה גבולית ל-$\\sum\\frac1{\\sqrt n}$ המתבדר, ולכן אין התכנסות בהחלט", 3),
               ("הטור $\\sum(-1)^n\\sin\\frac1{\\sqrt n}$: מבחן לייבניץ (הסדרה יורדת ושואפת ל-$0$), ולכן מתכנס בתנאי", 3),
               ("הטור $\\sum(-1)^n\\left(\\sqrt n-\\sqrt{n-1}\\right)$: הצגה כ-$\\frac1{\\sqrt n+\\sqrt{n-1}}$ והשוואה גבולית ל-$\\sum\\frac1{\\sqrt n}$, ולכן אין התכנסות בהחלט", 3),
               ("הטור $\\sum(-1)^n\\left(\\sqrt n-\\sqrt{n-1}\\right)$: מבחן לייבניץ ולכן מתכנס בתנאי", 3)),
    pitfalls=["לעצור אחרי מבחן לייבניץ ולהכריז על התכנסות, בלי לבדוק התכנסות בהחלט. ההבחנה בין בהחלט לבתנאי היא חלק מהשאלה.",
              "לבלבל בין התבדרות של $\\sum|a_n|$ להתבדרות של הטור עצמו: טור מתחלף יכול להתכנס גם כשטור הערכים המוחלטים מתבדר."],
    steps=[
        num(r"בבדיקת התכנסות בהחלט של $\sum(-1)^n\sin\frac1{\sqrt n}$ משווים את $\sin\frac1{\sqrt n}$ ל-$\frac1{\sqrt n}$. לְמה שואף היחס $\dfrac{\sin\frac1{\sqrt n}}{\frac1{\sqrt n}}$?", 1,
            r"זהו הגבול הידוע $\frac{\sin t}{t}\to1$ עבור $t=\frac1{\sqrt n}\to0$. הגבול חיובי וסופי, ולכן שני הטורים מתכנסים או מתבדרים יחד, והטור $\sum\frac1{\sqrt n}$ מתבדר ($p=\frac12<1$)."),
        num(r"בטור $\sum(-1)^n\left(\sqrt n-\sqrt{n-1}\right)$ מציגים $\sqrt n-\sqrt{n-1}=\frac1{\sqrt n+\sqrt{n-1}}$ ומשווים ל-$\frac1{\sqrt n}$. לְמה שואף היחס $\dfrac{\frac1{\sqrt n+\sqrt{n-1}}}{\frac1{\sqrt n}}$?", 0.5,
            r"היחס שווה ל-$\frac{1}{1+\sqrt{1-\frac1n}}\to\frac12$. הגבול חיובי וסופי, ולכן $\sum|a_n|$ מתבדר."),
        choice("מה מסקנת הפתרון לגבי שני הטורים?",
               "שניהם מתכנסים בתנאי ואינם מתכנסים בהחלט",
               ["שניהם מתכנסים בהחלט",
                "שניהם מתבדרים",
                "הטור עם $\\sin$ מתכנס בתנאי והטור עם השורשים מתכנס בהחלט"],
               "בשני הטורים סדרת הגורמים יורדת ושואפת ל-$0$ (מתכנס לפי לייבניץ), אבל טור הערכים המוחלטים מתבדר בהשוואה ל-$\\sum\\frac1{\\sqrt n}$. לכן שניהם מתכנסים בתנאי בלבד.", pos=3),
    ])

add(2, "ב",
    rubric=rub(("חישוב $f'_x(0,0)=0$ ו-$f'_y(0,0)=0$ מההגדרה", 3),
               ("ניסוח תנאי הדיפרנציאביליות: $\\Delta f=f'_x\\Delta x+f'_y\\Delta y+\\varepsilon\\sqrt{\\Delta x^2+\\Delta y^2}$ עם $\\varepsilon\\to0$", 3),
               ("מעבר לקואורדינטות קוטביות וחישוב $\\varepsilon=\\rho\\cdot\\frac14\\sin4\\theta$", 4),
               ("אפס כפול פונקציה חסומה, ולכן $\\varepsilon\\to0$ והפונקציה דיפרנציאבילית", 3)),
    pitfalls=["להסיק דיפרנציאביליות מעצם קיום הנגזרות החלקיות. קיומן הכרחי בלבד, ויש לבדוק את הגבול של $\\varepsilon$.",
              "לבדוק את הגבול של $\\varepsilon$ רק לאורך מסלולים ספציפיים ולא לכל הזוויות."],
    steps=[
        num(r"חשבו את $f'_x(0,0)$ מההגדרה.", 0,
            r"$f(\Delta x,0)=0$ לכל $\Delta x$, ולכן המנה $\frac{f(\Delta x,0)-f(0,0)}{\Delta x}=0$ וגם הגבול הוא $0$."),
        num(r"בקואורדינטות קוטביות $\varepsilon=\rho\cdot\sin\theta\cos\theta\cos2\theta=\frac{\rho}{4}\sin4\theta$. מהו הערך המקסימלי האפשרי של $\left|\frac14\sin4\theta\right|$?", 0.25,
            r"$|\sin4\theta|\le1$, ולכן הגורם הזוויתי חסום על ידי $\frac14$, ו-$|\varepsilon|\le\frac{\rho}{4}\to0$."),
        choice("האם $f$ דיפרנציאבילית ב-$(0,0)$?",
               "כן, כי $\\varepsilon\\to0$ כאשר $\\rho\\to0$ (אפס כפול פונקציה חסומה)",
               ["לא, כי הנגזרות החלקיות ב-$(0,0)$ מתאפסות",
                "לא, כי $\\varepsilon$ תלוי בזווית $\\theta$",
                "כן, כי הנגזרות החלקיות קיימות, ואין צורך בבדיקה נוספת"],
               "תנאי הדיפרנציאביליות הוא $\\varepsilon\\to0$. כאן $\\varepsilon=\\frac{\\rho}{4}\\sin4\\theta\\to0$ ללא תלות בזווית. קיום הנגזרות החלקיות בלבד אינו מספיק.", pos=1),
    ])

add(3, "א",
    rubric=rub(("הצבה $s=x+1$ ומבחן המנה לטור $\\sum\\frac{2^n}{n^2+1}s^n$, ומציאת $R=\\frac12$", 4),
               ("בדיקת הקצה $s=-\\frac12$: הטור מתכנס", 2),
               ("בדיקת הקצה $s=\\frac12$: הטור $\\sum\\frac1{n^2+1}$ מתכנס בהשוואה ל-$\\sum\\frac1{n^2}$", 3),
               ("חזרה למשתנה $x$ וכתיבת תחום ההתכנסות $\\left[-\\frac32,-\\frac12\\right]$", 3)),
    pitfalls=["לשכוח לבדוק את הקצוות ולכתוב קטע פתוח.",
              "לחשב את הרדיוס עבור $s=x+1$ ולהשאיר את התשובה במשתנה $s$, בלי לחזור ל-$x$ (המרכז הוא $x=-1$)."],
    steps=[
        num(r"נסמן $s=x+1$ ו-$a_n=\frac{2^n}{n^2+1}$. מהו רדיוס ההתכנסות $R=\lim\left|\frac{a_n}{a_{n+1}}\right|$?", 0.5,
            r"$\frac{a_n}{a_{n+1}}=\frac12\cdot\frac{n^2+2n+2}{n^2+1}\to\frac12$."),
        choice("איזה טור מתקבל בקצה $s=\\frac12$?",
               "$\\sum_{n=1}^{\\infty}\\frac{1}{n^2+1}$",
               ["$\\sum_{n=1}^{\\infty}\\frac{2^n}{n^2+1}$", "$\\sum_{n=1}^{\\infty}\\frac{1}{n}$", "$\\sum_{n=1}^{\\infty}\\frac{(-1)^n}{n^2+1}$"],
               "מציבים $s=\\frac12$: $\\frac{2^n}{n^2+1}\\cdot\\frac1{2^n}=\\frac1{n^2+1}\\le\\frac1{n^2}$, ולכן הטור מתכנס.", pos=2),
        choice("מהו תחום ההתכנסות של הטור המקורי?",
               "$\\left[-\\frac32,-\\frac12\\right]$",
               ["$\\left(-\\frac32,-\\frac12\\right)$", "$\\left[-\\frac12,\\frac12\\right]$", "$\\left[-\\frac12,\\frac32\\right]$"],
               "שני הקצוות $s=\\pm\\frac12$ מתכנסים, ולכן התחום ב-$s$ הוא $\\left[-\\frac12,\\frac12\\right]$. מכיוון ש-$x=s-1$ מקבלים $\\left[-\\frac32,-\\frac12\\right]$.", pos=0),
    ])

add(3, "ב",
    rubric=rub(("הגדרת $s=\\frac zx$, $t=\\frac yx$ וחישוב הנגזרות החלקיות שלהן", 3),
               ("כלל השרשרת: חישוב $F_x,F_y,F_z$", 4),
               ("כלל המכפלה: חישוב $u_x,u_y,u_z$", 3),
               ("הצבה ב-$xu_x+yu_y+zu_z$, צמצום האיברים עם $F_s,F_t$ וקבלת $ku$", 3)),
    pitfalls=["לשכוח את האיבר $kx^{k-1}F$ שמתקבל מגזירת הגורם $x^k$ בכלל המכפלה.",
              "לבלבל בין הנגזרות החלקיות של $s=\\frac zx$ ו-$t=\\frac yx$: רק $s$ תלוי ב-$z$ ורק $t$ תלוי ב-$y$."],
    steps=[
        choice("מהי $\\frac{\\partial s}{\\partial x}$ עבור $s=\\frac zx$?",
               "$-\\frac{z}{x^2}$", ["$\\frac{1}{x}$", "$\\frac{z}{x^2}$", "$-\\frac{1}{x^2}$"],
               "גוזרים לפי $x$: $\\left(zx^{-1}\\right)'=-zx^{-2}$.", pos=1),
        {"type": "order", "prompt": "סדרו את שלבי ההוכחה.", "lines": [
            r"נסמן $s=\frac zx$, $t=\frac yx$, כך ש-$u=x^kF(s,t)$.",
            r"כלל השרשרת: $F_x=-\frac1{x^2}\left(zF_s+yF_t\right)$, $F_y=\frac1xF_t$, $F_z=\frac1xF_s$.",
            r"כלל המכפלה: $u_x=kx^{k-1}F-x^{k-2}\left(zF_s+yF_t\right)$, $u_y=x^{k-1}F_t$, $u_z=x^{k-1}F_s$.",
            r"מציבים ב-$xu_x+yu_y+zu_z$: האיברים עם $F_s$ ועם $F_t$ מצטמצמים, ונשאר $kx^kF=ku$."],
         "explain": "קודם מגדירים את המשתנים הפנימיים, אחר כך גוזרים את $F$ בכלל השרשרת, אחר כך את $u$ בכלל המכפלה, ובסוף מציבים במשוואה."},
        {"type": "findbug", "prompt": "בהוכחה הבאה שורה אחת שגויה. מצאו אותה.", "lines": [
            r"נסמן $s=\frac zx$, $t=\frac yx$.",
            r"$F_x=-\frac1{x^2}\left(zF_s+yF_t\right)$",
            r"$F_y=\frac1xF_t$",
            r"$F_z=\frac1xF_s$",
            r"$u_x=kx^{k-1}F+x^{k-2}\left(zF_s+yF_t\right)$",
            r"$u_y=x^{k-1}F_t,\quad u_z=x^{k-1}F_s$",
            r"$xu_x+yu_y+zu_z=kx^kF=ku$"], "bugIndex": 4,
         "explain": "$u_x=kx^{k-1}F+x^k F_x$, ו-$F_x$ שלילי, ולכן האיבר $x^{k-2}\\left(zF_s+yF_t\\right)$ צריך להופיע עם סימן מינוס. עם סימן פלוס האיברים לא מצטמצמים."},
    ])

add(4, "א",
    rubric=rub(("פירוק לשברים חלקיים: $\\frac1{(n+2)(n+4)}=\\frac12\\left[\\frac1{n+2}-\\frac1{n+4}\\right]$", 4),
               ("כתיבת הסכום החלקי $S_n$ וצמצום טלסקופי: נשארים ארבעה איברים", 5),
               ("מעבר לגבול: $S=\\frac7{24}$", 3)),
    pitfalls=["שגיאת ההפרש בפירוק: ההפרש בין המחוברים הוא $2$, ולכן חייבים את המקדם $\\frac12$ מלפנים.",
              "לצמצם לא נכון ולהשאיר רק איבר ראשון אחד. בטלסקופ עם הפרש $2$ נשארים שני האיברים הראשונים ושני האחרונים."],
    steps=[
        num(r"בפירוק $\frac1{(n+2)(n+4)}=c\left[\frac1{n+2}-\frac1{n+4}\right]$ מהו $c$?", 0.5,
            r"$\frac1{n+2}-\frac1{n+4}=\frac{2}{(n+2)(n+4)}$, ולכן $c=\frac12$."),
        num(r"אחרי הצמצום הטלסקופי $S_n=\frac12\left(\frac13+\frac14-\frac1{n+3}-\frac1{n+4}\right)$. מהו הערך $\frac13+\frac14$ (תשובה עשרונית, דיוק $0.0001$)?", 0.5833,
            r"$\frac13+\frac14=\frac7{12}\approx0.5833$.", tol=0.0001),
        num(r"מהו סכום הטור $\sum_{n=1}^{\infty}\frac1{n^2+6n+8}$ (תשובה עשרונית, דיוק $0.0001$)?", 0.2917,
            r"כש-$n\to\infty$ האיברים $\frac1{n+3},\frac1{n+4}$ שואפים ל-$0$, ולכן $S=\frac12\cdot\frac7{12}=\frac7{24}\approx0.2917$.", tol=0.0001),
    ])

add(4, "ב",
    rubric=rub(("בניית מערכת לגרנז': $y=2\\lambda x$, $x=2\\lambda y$, $x^2+y^2=2$", 4),
               ("הוכחה ש-$\\lambda\\neq0$ ומציאת הקשר $x^2=y^2$", 4),
               ("הצבה באילוץ וקבלת ארבע נקודות חשודות $(\\pm1,\\pm1)$", 2),
               ("חישוב הערכים: מקסימום $1$ ומינימום $-1$", 3)),
    pitfalls=["לפסול את $\\lambda=0$ בלי נימוק. הנימוק הוא שאז $x=y=0$ והאילוץ $x^2+y^2=2$ לא מתקיים.",
              "מהקשר $x^2=y^2$ לקחת רק $y=x$ ולהחמיץ את הנקודות $(1,-1)$ ו-$(-1,1)$, שבהן מתקבל המינימום."],
    steps=[
        choice("אחרי חלוקת שתי המשוואות $\\lambda=\\frac{y}{2x}$ ו-$\\lambda=\\frac{x}{2y}$, איזה קשר מתקבל בין $x$ ל-$y$?",
               "$x^2=y^2$", ["$x=y$ בלבד", "$x=2y$", "$xy=2$"],
               "משוויון המנות $\\frac y{2x}=\\frac x{2y}$ מקבלים $y^2=x^2$, כלומר $y=\\pm x$ (ולא רק $y=x$).", pos=0),
        num("כמה נקודות חשודות מתקבלות על המעגל $x^2+y^2=2$?", 4,
            "מ-$x^2=y^2$ ומהאילוץ $x^2=1$, ולכן $x=\\pm1$ ו-$y=\\pm1$: ארבע נקודות."),
        num("מהו הערך המקסימלי של $f=xy$ על האילוץ?", 1,
            "$f(1,1)=f(-1,-1)=1$."),
        num("מהו הערך המינימלי של $f=xy$ על האילוץ?", -1,
            "$f(1,-1)=f(-1,1)=-1$."),
    ])

add(5, "א",
    rubric=rub(("פתרון מערכת $f'_x=f'_y=0$ ומציאת הנקודות $(0,0)$ ו-$\\left(1,\\frac12\\right)$", 4),
               ("חישוב $f''_{xx},f''_{xy},f''_{yy}$ ודטרמיננטת ההסיאן", 3),
               ("$\\Delta=-36<0$ ב-$(0,0)$, ולכן נקודת אוכף", 2),
               ("$\\Delta>0$ ו-$f''_{xx}>0$ ב-$\\left(1,\\frac12\\right)$, ולכן מינימום", 3)),
    pitfalls=["לפתור את המערכת ולמצוא רק את הפתרון $y=0$ ולהחמיץ את $8y^3=1$.",
              "להסיק מינימום מ-$\\Delta>0$ בלבד, בלי לבדוק את סימן $f''_{xx}$."],
    steps=[
        num("מהו $\\Delta=f''_{xx}f''_{yy}-\\left(f''_{xy}\\right)^2$ בנקודה $(0,0)$?", -36,
            "$f''_{xx}(0,0)=0$, $f''_{yy}(0,0)=0$, $f''_{xy}=-6$, ולכן $\\Delta=0-36=-36$."),
        num("מהו $\\Delta$ בנקודה $\\left(1,\\frac12\\right)$?", 108,
            "$f''_{xx}=6$, $f''_{yy}=48\\cdot\\frac12=24$, $f''_{xy}=-6$, ולכן $\\Delta=144-36=108$."),
        choice("איך מסווגים את שתי הנקודות הקריטיות?",
               "$(0,0)$ נקודת אוכף, $\\left(1,\\frac12\\right)$ מינימום מקומי",
               ["$(0,0)$ מינימום מקומי, $\\left(1,\\frac12\\right)$ נקודת אוכף",
                "$(0,0)$ נקודת אוכף, $\\left(1,\\frac12\\right)$ מקסימום מקומי",
                "שתיהן נקודות אוכף"],
               "ב-$(0,0)$ מתקבל $\\Delta<0$ (אוכף). ב-$\\left(1,\\frac12\\right)$ מתקבל $\\Delta>0$ ו-$f''_{xx}=6>0$ (מינימום).", pos=2),
    ])

add(5, "ב",
    rubric=rub(("פיתוח לטור הנדסי: $\\frac1{1-3x^2}=\\sum3^nx^{2n}$", 4),
               ("תחום ההתכנסות $|x|<\\frac1{\\sqrt3}$", 3),
               ("בדיקת שני הקצוות: הטור מתבדר בהם", 3),
               ("שימוש בכך שיש רק חזקות זוגיות: $f^{(5)}(0)=5!\\,c_5=0$", 3)),
    pitfalls=["לשכוח לבדוק את הקצוות $x=\\pm\\frac1{\\sqrt3}$ (בשניהם האיברים הם $1$ והטור מתבדר).",
              "לחשב את $f^{(5)}(0)$ מהקואורדינטה $c_2$ או $c_{10}$ במקום לשים לב שהמקדם של $x^5$ הוא $0$."],
    steps=[
        num("מהו רדיוס ההתכנסות של $\\sum_{n=0}^{\\infty}3^nx^{2n}$ (תשובה עשרונית, דיוק $0.001$)?", 0.5774,
            "הטור ההנדסי מתכנס כש-$|3x^2|<1$, כלומר $|x|<\\frac1{\\sqrt3}\\approx0.5774$.", tol=0.001),
        num("מהו המקדם $c_4$ של $x^4$ בפיתוח?", 9,
            "$x^4=x^{2n}$ עבור $n=2$, ולכן $c_4=3^2=9$."),
        choice("מה קורה בקצוות $x=\\pm\\frac1{\\sqrt3}$?",
               "הטור מתבדר בשניהם",
               ["הטור מתכנס בשניהם", "הטור מתכנס רק ב-$x=\\frac1{\\sqrt3}$", "הטור מתכנס רק ב-$x=-\\frac1{\\sqrt3}$"],
               "בשני הקצוות $3x^2=1$, ולכן כל איברי הטור שווים ל-$1$ והטור מתבדר.", pos=1),
        num("מהו $f^{(5)}(0)$?", 0,
            "בפיתוח יש רק חזקות זוגיות, ולכן $c_5=0$ ו-$f^{(5)}(0)=5!\\,c_5=0$."),
    ])

exam = {
    "examCode": "24A-A",
    "examLabel": "מבחן סוף סמסטר א' תשפ\"ד, מועד א'",
    "year": 2024,
    "examDate": "04/04/2024",
    "sourceFile": "calculus-2/24A-A questions 4.4.2024.pdf",
    "solutionFile": "calculus-2/24A-A answers 4.4.2024 (worked answers)",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
