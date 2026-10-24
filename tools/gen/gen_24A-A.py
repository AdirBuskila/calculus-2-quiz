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
