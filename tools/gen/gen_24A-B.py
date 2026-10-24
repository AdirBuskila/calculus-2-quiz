# -*- coding: utf-8 -*-
"""Generator for tools/raw/24A-B.json -- calculus-2 (20252), semester A 2024, moed B (6/5/2024).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_24A-B.py

Source: exam 6.5.24 (3 pages, 5 questions of 25 points, solve 4 of 5).
Key: the solution file misnamed "6.5.25" (11 pages; it is the solution of the 6.5.24 exam, as its Q1-Q5 content shows).
That mislabel is recorded here and in solutionFile. The key is mixed handwriting (tablet, squared paper) and typed pages.
Header (lecturer names) is not transcribed.

Transcription notes
- Text layers are garbled; everything is transcribed from page renders.
- Q1b prints "f(x) = x + xy" for a function of two variables; transcribed as printed (it is f(x,y) in the key).
- Q1a: the function's denominator x^6+y^3 vanishes on y=-x^2; the exam does not mention it. The key's two-path argument
  (y=kx gives 0, y=x^2 gives 1/2) is transcribed unchanged.
- Q2a asks for two series in one part; stored as one item.
- Q2b: the key computes eps along dy=k dx with "dx^3/dx^3"; this holds for dx>0 (for dx<0 the sign flips, still nonzero).
  The transcription adds "dx>0" so the limit statement is exact; the conclusion (not differentiable) is the key's.
- Q4a: printed as the sum of (5/3^n) - 4/((n+3)(n+4)); the key reads it as sum 5/3^n minus 4 sum 1/((n+3)(n+4)).

Intermediate slip corrected silently (logged in docs/ASK_ADIR.md)
- Q3a: the key's radius (R=1) and final domain [-6,-4] are correct (sympy), but its endpoint comparison step writes
  1/cuberoot(n^2) as the comparison term and then cites sum 1/n^(3/2); the terms behave like n^(-4/3). Re-derived: at
  x=-4 the series is sum 1/(cuberoot(n+1) sqrt(n^2+1)), limit-comparable to 1/n^(4/3) (p=4/3>1), so it converges; at
  x=-6 it converges absolutely. The final answer holds, so the endpoint step is written with n^(-4/3) and the label
  stays student-solution. Verified in tools/verify/24A-B/solve_24A-B.py.

Key labelling (orchestrator ruling 2026-10-24): the key is handwritten/mixed with no named author, so every item is
solutionSource "student-solution", official False.

Checks (tools/verify/24A-B/check.py, sympy + numeric): every other limit, test, partial derivative, Hessian, Lagrange
point, series sum and Maclaurin coefficient matches the key.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "24A-B.json"


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
$$f(x,y)=\begin{cases}\dfrac{x^2y^2}{x^6+y^3}, & (x,y)\neq(0,0)\\[2mm] 0, & (x,y)=(0,0)\end{cases}$$
האם היא רציפה בנקודה $(x,y)=(0,0)$? נמקו את תשובתכם.""",
r"""לפי המסלולים $x\to0^+$, $y=kx$:
$$\lim_{x\to0}f(x,y)=0$$
לפי המסלולים $x\to0^+$, $y=x^2$:
$$\lim_{x\to0}f(x,y)=\frac{1}{2}$$
ולכן הגבול של $f(x,y)$ כאשר $(x,y)\to(0,0)$ אינו קיים, ומכאן $f$ אינה רציפה ב-$(0,0)$.

**הערה:** הפונקציה אינה מוגדרת על העקום $y=-x^2$ (עבור $x\neq0$), שבו המכנה $x^6+y^3$ מתאפס, והעקום הזה עובר דרך הראשית. לאורך העקום $y=-x^2+x^4$ הפונקציה גדלה בלי גבול כשהנקודה מתקרבת לראשית. המסלולים בפתרון ($y=kx$ ו-$y=x^2$) נמצאים בתחום ההגדרה, ולכן המסקנה נשארת: הגבול אינו קיים.""", part="א", points=12))

# ===== Q1b =====
questions.append(Q(1, "computation", "gradient_directional", r"""מצאו את הכיוון שבו נגזרת הפונקציה $f(x)=x+xy$ בנקודה $(1,-1)$ שווה ל-$\dfrac{1}{\sqrt{2}}$.""",
r"""$$\nabla f(x,y)=\left(\frac{\partial f}{\partial x},\frac{\partial f}{\partial y}\right)=(1+y,\ x)\ \Leftarrow\ f(x,y)=x+xy$$
$$\nabla f\Big|_{(1,-1)}=(0,1)$$
בנקודה $(1,-1)$ מתקיים:
נסמן $\vec u=(a,b)$ כאשר $\sqrt{a^2+b^2}=1$.
$$D_{\vec u}f(1,-1)=(0,1)\cdot(a,b)=b=\frac{1}{\sqrt{2}}$$
$$\Leftarrow\ a^2+b^2=1\ \Leftarrow\ a^2=\frac{1}{2}\ \Leftarrow\ a=\pm\frac{1}{\sqrt{2}}$$
(מתקבל מכך)
לכן הכיוונים בהם $\dfrac{1}{\sqrt{2}}=D_{\vec u}f(1,-1)$ הם $\left(\dfrac{1}{\sqrt{2}},\dfrac{1}{\sqrt{2}}\right)$ וגם $\left(\dfrac{-1}{\sqrt{2}},\dfrac{1}{\sqrt{2}}\right)$.""", part="ב", points=13))

# ===== Q2a =====
questions.append(Q(2, "computation", "numeric_series", r"""בדקו התכנסות בהחלט, בתנאי או התבדרות של הטורים הבאים:
$$\sum_{n=1}^{\infty}\frac{(-1)^n}{(n+1)\ln(n+1)}$$
$$\sum_{n=1}^{\infty}\frac{(-1)^n+n}{3^n}$$""",
r"""**הטור הראשון.** $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^n}{(n+1)\ln(n+1)}$.
נבדוק התכנסות בהחלט: נטפל בטור בערכים המוחלטים
$$\sum_{n=1}^{\infty}\frac{1}{(n+1)\ln(n+1)}$$
נשתמש במבחן האינטגרל:
$$\int_1^{\infty}\frac{1}{(x+1)\ln(x+1)}\,dx=\lim_{b\to\infty}\int_1^{b}\frac{1}{(x+1)\ln(x+1)}\,dx=\left[\begin{array}{l}t=\ln(x+1)\\ dt=\frac{1}{x+1}\,dx\end{array}\right]=$$
$$=\lim_{b\to\infty}\int_{\ln2}^{\ln(b+1)}\frac{dt}{t}=\lim_{b\to\infty}\left(-\ln(\ln2)+\ln(\ln(b+1))\right)=\infty$$
לכן הטור אינו מתכנס בהחלט.
נבדוק התכנסות בתנאי:
1) $\displaystyle\lim_{n\to\infty}\frac{1}{(n+1)\ln(n+1)}=0$
2) $\dfrac{1}{2\ln2}>\dfrac{1}{3\ln3}>\dfrac{1}{4\ln4}>\cdots$
לכן הטור הוא **מתכנס בתנאי**.

**הטור השני.** $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^n+n}{3^n}$.
שימו לב שהטור חיובי. נשתמש במבחן השורש:
$$\lim_{n\to\infty}\sqrt[n]{\frac{(-1)^n+n}{3^n}}=\frac{1}{3}$$
לפי כלל הסנדוויץ':
$$\sqrt[n]{\frac{n-1}{3^n}}\le\sqrt[n]{\frac{(-1)^n+n}{3^n}}\le\sqrt[n]{\frac{n+1}{3^n}}$$
שני הצדדים שואפים ל-$\frac{1}{3}$.
מסקנה: הטור מתכנס (ומכיוון שהוא חיובי, מתכנס בהחלט).""", part="א", points=12))

# ===== Q2b =====
questions.append(Q(2, "computation", "partials_differentiability", r"""נתונה הפונקציה
$$f(x,y)=\begin{cases}\dfrac{x^3+y^3}{2x^2+y^2}, & (x,y)\neq(0,0)\\[2mm] 0, & (x,y)=(0,0)\end{cases}$$
מצאו את $f'_x(0,0)$ ו-$f'_y(0,0)$. האם $f(x,y)$ דיפרנציאבילית ב-$(0,0)$?""",
r"""$$f'_x(0,0)=\lim_{\Delta x\to0}\frac{f(\Delta x+0,0)-f(0,0)}{\Delta x}=\lim_{\Delta x\to0}\frac{\frac{\Delta x^3}{2\Delta x^2}-0}{\Delta x}=\frac{1}{2}$$
$$f'_y(0,0)=\lim_{\Delta y\to0}\frac{f(0,0+\Delta y)-f(0,0)}{\Delta y}=\lim_{\Delta y\to0}\frac{\frac{\Delta y^3}{\Delta y^2}-0}{\Delta y}=1$$
בדיקת דיפרנציאביליות:
$$\frac{\Delta x^3+\Delta y^3}{2\Delta x^2+\Delta y^2}-0=\frac{1}{2}\Delta x+1\cdot\Delta y+\varepsilon\cdot\sqrt{\Delta x^2+\Delta y^2}$$
$$\Rightarrow\ \varepsilon=-\frac{\Delta x\,(\Delta y)^2+4\Delta x^2\Delta y}{2\left(2\Delta x^2+\Delta y^2\right)\sqrt{\Delta x^2+\Delta y^2}}$$
נציב $\Delta y=k\,\Delta x$ ($\Delta x\to0^{+}$):
$$\lim_{\substack{\Delta x\to0\\ \Delta y=k\Delta x}}-\frac{k^2\Delta x^3+4k\Delta x^3}{2\left(2\Delta x^2+k^2\Delta x^2\right)\sqrt{\Delta x^2\left(1+k^2\right)}}=\lim_{\Delta x\to0}-\frac{\Delta x^3\left(k^2+4k\right)}{\Delta x^3\left(2\left(2+k^2\right)\sqrt{1+k^2}\right)}=-\frac{k^2+4k}{2\left(2+k^2\right)\sqrt{1+k^2}}$$
הגבול לא קיים (הוא תלוי ב-$k$), לכן הפונקציה **לא דיפרנציאבילית** ב-$(0,0)$.""", part="ב", points=13))

# ===== Q3a (HELD) =====
questions.append(Q(3, "computation", "power_series", r"""עבור אילו ערכי $x$ הטור מתכנס (מצאו רדיוס התכנסות ותחום התכנסות):
$$\sum_{n=1}^{\infty}\frac{(x+5)^n}{\sqrt[3]{n+1}\sqrt{n^2+1}}$$""",
r"""נציב $t=x+5$ ונבחן את הטור $\sum_{n=1}^{\infty}\dfrac{t^n}{\sqrt[3]{n+1}\sqrt{n^2+1}}$.
$$\frac{a_n}{a_{n+1}}=\frac{\frac{1}{\sqrt[3]{n+1}\sqrt{n^2+1}}}{\frac{1}{\sqrt[3]{n+2}\sqrt{(n+1)^2+1}}}=\frac{\sqrt[3]{n+2}\sqrt{n^2+2n+2}}{\sqrt[3]{n+1}\sqrt{n^2+1}}=\frac{\sqrt[3]{\frac1n(n+2)}\sqrt{\frac{1}{n^2}\left(n^2+2n+2\right)}}{\sqrt[3]{\frac1n(n+1)}\sqrt{\frac{1}{n^2}\left(n^2+1\right)}}$$
$$\lim_{n\to\infty}\frac{\sqrt[3]{1+\frac2n}\sqrt{1+\frac2n+\frac{2}{n^2}}}{\sqrt[3]{1+\frac1n}\sqrt{1+\frac{1}{n^2}}}=1=R$$
לכן $R=1$ הוא רדיוס ההתכנסות, והטור מתכנס עבור $|x+5|<1$.

**נקודות הקצה $t=\pm1$.** עבור $t=1$ (כלומר $x=-4$) מקבלים את הטור החיובי $\sum_{n=1}^{\infty}\frac{1}{\sqrt[3]{n+1}\sqrt{n^2+1}}$. האיבר מתנהג כמו $\frac{1}{n^{1/3}\cdot n}=\frac{1}{n^{4/3}}$, ובמבחן ההשוואה הגבולי:
$$\lim_{n\to\infty}\frac{\frac{1}{\sqrt[3]{n+1}\sqrt{n^2+1}}}{\frac{1}{n\sqrt[3]{n}}}=\lim_{n\to\infty}\frac{n\sqrt[3]{n}}{\sqrt[3]{n+1}\sqrt{n^2+1}}=\lim_{n\to\infty}\frac{1}{\sqrt[3]{1+\frac1n}\sqrt{1+\frac{1}{n^2}}}=1.$$
הטור $\sum_{n=1}^{\infty}\frac{1}{n^{4/3}}$ מתכנס ($p=\frac43>1$), ולכן הטור מתכנס ב-$x=-4$.
עבור $t=-1$ (כלומר $x=-6$) מקבלים $\sum_{n=1}^{\infty}\frac{(-1)^n}{\sqrt[3]{n+1}\sqrt{n^2+1}}$, שטור הערכים המוחלטים שלו הוא הטור של $x=-4$, שמתכנס; לכן הטור מתכנס בהחלט ב-$x=-6$.

**תחום ההתכנסות:** $-1\le x+5\le1$, כלומר $[-6,-4]$.""", part="א", points=12))

# ===== Q3b =====
questions.append(Q(3, "proof", "chain_rule_identity", r"""הראו כי הפונקציה $z=\dfrac{y}{3x}+g(xy)$ כאשר $g(t)$ גזירה עבור כל $t$ ו-$x\neq0$ מקיימת את המשוואה:
$$x^2\frac{\partial z}{\partial x}-xy\frac{\partial z}{\partial y}+\frac{2y}{3}=0$$""",
r"""$g(xy)=g(t)$;
$$\frac{\partial z}{\partial x}=-\frac{y}{3x^2}+g'_t(xy)\,t'_x=-\frac{y}{3x^2}+g'_t(xy)\,y;$$
$$\frac{\partial z}{\partial y}=\frac{1}{3x}+g'_t(xy)\,t'_y=\frac{1}{3x}+g'_t(xy)\,x;$$
$$x^2\frac{\partial z}{\partial x}-xy\frac{\partial z}{\partial y}+\frac{2y}{3}=$$
$$=x^2\left(-\frac{y}{3x^2}+g'_t(xy)\,y\right)-xy\left(\frac{1}{3x}+g'_t(xy)\,x\right)+\frac{2y}{3}$$
$$=-\frac{y}{3}+x^2y\,g'_t(xy)-\frac{y}{3}-x^2y\,g'_t(xy)+\frac{2y}{3}=0$$""", part="ב", points=13))

# ===== Q4a =====
questions.append(Q(4, "computation", "numeric_series", r"""חשבו את סכום הטור
$$\sum_{n=1}^{\infty}\frac{5}{3^n}-\frac{4}{(n+3)(n+4)}$$""",
r"""$$\sum_{n=1}^{\infty}\frac{5}{3^n}=5\sum_{n=1}^{\infty}\left(\frac{1}{3}\right)^n=5\cdot\frac{\frac{1}{3}}{1-\frac{1}{3}}=\frac{5}{3}\cdot\frac{3}{2}=\frac{5}{2}$$
$$\frac{1}{(n+3)(n+4)}=\frac{1}{n+3}-\frac{1}{n+4}\ \Rightarrow\ \sum_{n=1}^{\infty}\frac{1}{(n+3)(n+4)}=\lim_{N\to\infty}\sum_{n=1}^{N}\left(\frac{1}{n+3}-\frac{1}{n+4}\right)$$
$$=\lim_{N\to\infty}\left(\frac{1}{4}-\frac{1}{5}+\frac{1}{5}-\frac{1}{6}+\frac{1}{6}-\frac{1}{7}+\frac{1}{7}-\cdots+\frac{1}{N+3}-\frac{1}{N+4}\right)=\lim_{N\to\infty}\left(\frac{1}{4}-\frac{1}{N+4}\right)=\frac{1}{4}$$
$$S=\frac{5}{2}-4\cdot\frac{1}{4}=\frac{3}{2}$$""", part="א", points=12))

# ===== Q4b =====
questions.append(Q(4, "computation", "absolute_extrema", r"""מצאו אקסטרמומים מוחלטים של הפונקציה $f(x,y)=2x^4+y^4-x^2-2y^2$ בתחום $\{(x,y):x^2+y^2\le2\}$""",
r"""$$\begin{cases}f'_x=8x^3-2x=0\\ f'_y=4y^3-4y=0\end{cases}\iff\begin{cases}x\left(4x^2-1\right)=0\\ y\left(y^2-1\right)=0\end{cases}$$
$$\Longleftarrow\begin{cases}x=0,\ x=\pm\frac{1}{2}\\ y=0,\ y=\pm1\end{cases}$$
נקודות קריטיות:
$(0,0),(0,1),(0,-1)$
$\left(\frac{1}{2},0\right),\left(\frac{1}{2},1\right),\left(\frac{1}{2},-1\right)$
$\left(-\frac{1}{2},0\right),\left(-\frac{1}{2},1\right),\left(-\frac{1}{2},-1\right)$
כל הנקודות נמצאות בתוך התחום $x^2+y^2<2$:
$$f(0,0)=0,\quad f(0,1)=f(0,-1)=-1$$
$$f\left(\frac{1}{2},0\right)=-\frac{1}{8},\quad f\left(\frac{1}{2},1\right)=f\left(\frac{1}{2},-1\right)=-\frac{9}{8}$$
$$f\left(-\frac{1}{2},0\right)=-\frac{1}{8},\quad f\left(-\frac{1}{2},1\right)=f\left(-\frac{1}{2},-1\right)=-\frac{9}{8}$$
בשפה $x^2+y^2=2$ נשתמש בשיטת לגרנז':
$$L=f(x,y)+\lambda\left(x^2+y^2-2\right)$$
$$L'_x=8x^3-2x+2\lambda x,\quad L'_y=4y^3-4y+2\lambda y,\quad L'_\lambda=x^2+y^2-2$$
$$\Rightarrow\ \nabla L=0\iff x\left(4x^2+\lambda-1\right)=0,\quad y\left(2y^2+\lambda-2\right)=0,\quad x^2+y^2=2$$
פתרונות:
(1) $\lambda=-2,\ y=\pm\sqrt{2},\ x=0$
(2) $\lambda=-7,\ x=\pm\sqrt{2},\ y=0$
(3) $y\neq0,\ x\neq0\ \Leftarrow\ \lambda=1-4x^2=2-2y^2\ \Leftarrow\ y^2=\frac{1}{2}+2x^2$
$$x^2+\frac{1}{2}+2x^2=2\iff3x^2=\frac{3}{2}\ \Rightarrow\ x=\pm\frac{1}{\sqrt{2}},\ y=\pm\sqrt{\frac{3}{2}}$$
$$f\left(\pm\frac{1}{\sqrt{2}},\pm\sqrt{\frac{3}{2}}\right)=\frac{9}{4}-3=-\frac{3}{4},\qquad f\left(0,\pm\sqrt{2}\right)=0$$
$$f\left(\pm\sqrt{2},0\right)=6$$
המקסימום בנקודות $(\pm\sqrt{2},0)$:
$$\max_{x^2+y^2\le2}f(x,y)=6$$
המינימום בנקודות $\left(\pm\frac{1}{2},\pm1\right)$:
$$\min_{x^2+y^2\le2}f(x,y)=-\frac{9}{8}$$""", part="ב", points=13))

# ===== Q5a =====
questions.append(Q(5, "computation", "local_extrema", r"""מצאו וסווגו את נקודות האקסטרמום של הפונקציה:
$$f(x,y)=(3-x)(3-y)(x+y-3)$$""",
r"""$$f'_x=(3-y)\left(-2x-y+6\right)=0$$
$$f'_y=(3-x)\left(-x-2y+6\right)=0$$
$y=3$ או $-2x-y+6=0$, ובנוסף $x=3$ או $-x-2y+6=0$
$$\begin{cases}x=0\\ y=3\end{cases}\qquad\begin{cases}x=3\\ y=0\end{cases}\qquad\begin{cases}x=3\\ y=3\end{cases}\qquad\begin{cases}x=2\\ y=2\end{cases}$$
$$f''_{xx}=-6+2y,\qquad f''_{xy}=2x+2y-9,\qquad f''_{yy}=-6+2x$$
$$\Delta=4(3-y)(3-x)-(2x+2y-9)^2$$
$\Delta(0,3)=-9<0$ לכן נקודת אוכף $M_1(0,3)$.
$\Delta(3,0)=-9<0$ לכן נקודת אוכף $M_2(3,0)$.
$\Delta(3,3)=-9<0$ לכן נקודת אוכף $M_3(3,3)$.
$\Delta(2,2)=3>0$, $f''_{xx}(2,2)=-2<0$, לכן נקודת מקסימום $M_4(2,2)$.""", part="א", points=12))

# ===== Q5b =====
questions.append(Q(5, "computation", "taylor_maclaurin", r"""פתחו את הפונקציה $f(x)=\dfrac{x}{25+x^2}$ לטור מקלורן. מהו תחום התכנסות הטור?
הסיקו את הערך של $f^{(5)}(0)$.""",
r"""$$f(x)=\frac{x}{25+x^2}=\frac{x}{25\left(1+\left(\frac{x}{5}\right)^2\right)}=\frac{1}{25}\sum_{n=0}^{\infty}x\cdot(-1)^n\left(\frac{x}{5}\right)^{2n}=\sum_{n=0}^{\infty}(-1)^n\frac{x^{2n+1}}{5^{2n+2}}$$
הטור מתכנס עבור $|x|<5\iff\left|\frac{x}{5}\right|<1$ (טור הנדסי). עבור $x=\pm5$ הטור מתבדר.
$$f(x)=\sum_{n=0}^{\infty}\frac{f^{(n)}(0)}{n!}x^n=\sum_{n=0}^{\infty}c_nx^n$$
$$f^{(5)}(0)=c_5\cdot5!\ \{n=2\}=\frac{1}{5^6}\cdot5!=\frac{4!}{5^5}$$""", part="ב", points=13))

# ---- rubric / pitfalls / steps (ai-verified). Every expected value is re-computed in tools/verify/24A-B/steps_24A-B.py ----
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
    rubric=rub(("מסלול $y=kx$: הגבול הוא $0$", 3), ("מסלול $y=x^2$: הגבול הוא $\\frac12$", 4),
               ("שני גבולות שונים לאורך מסלולים שונים: הגבול הדו-ממדי אינו קיים", 3),
               ("מסקנה: $f$ אינה רציפה ב-$(0,0)$", 2)),
    pitfalls=["לבדוק רק ישרים $y=kx$ ולהסיק רציפות: גבול $0$ לאורך כל ישר אינו מוכיח שהגבול קיים.",
              "לבדוק רק מסלולים שבהם אחד ממחוברי המכנה $x^6+y^3$ שולט, ולדלג על מסלול מאוזן: דווקא ב-$y=x^2$ שני המחוברים שווים בסדר גודל, ושם מתקבל גבול שונה."],
    steps=[
        num(r"מהו הגבול של $f$ לאורך הישר $y=x$ כאשר $x\to0^+$?", 0,
            r"$f(x,x)=\frac{x^4}{x^6+x^3}=\frac{x}{x^3+1}\to0$."),
        num(r"מהו הגבול של $f$ לאורך המסלול $y=x^2$ כאשר $x\to0^+$?", 0.5,
            r"$f(x,x^2)=\frac{x^2\cdot x^4}{x^6+x^6}=\frac{x^6}{2x^6}=\frac12$."),
        choice(r"מה דין הרציפות של $f$ ב-$(0,0)$?",
               r"לא רציפה: לאורך מסלולים שונים מתקבלים גבולות שונים ($0$ ו-$\frac12$)",
               [r"רציפה, כי הגבול לאורך כל ישר הוא $0$",
                r"רציפה, כי $f(0,0)=0$ מוגדרת",
                r"לא רציפה, כי המכנה מתאפס בראשית"],
               r"הגבול הדו-ממדי קיים רק אם כל המסלולים נותנים אותו ערך; כאן מתקבלים $0$ ו-$\frac12$, ולכן הגבול לא קיים והפונקציה אינה רציפה. גבול $0$ לאורך ישרים בלבד אינו מספיק, הגדרת $f(0,0)$ אינה מבטיחה רציפות, ומכנה שמתאפס לבדו אינו סיבה לאי-רציפות.", pos=3),
    ])

add(1, "ב",
    rubric=rub(("גרדיאנט $\\nabla f=(1+y,x)$ ובנקודה $(1,-1)$: $(0,1)$", 4),
               ("הנגזרת הכיוונית בכיוון $\\vec u=(a,b)$ היא $b$", 3),
               ("$b=\\frac1{\\sqrt2}$ ומהאילוץ $a^2+b^2=1$: $a=\\pm\\frac1{\\sqrt2}$", 4), ("שני הכיוונים", 2)),
    pitfalls=["לשכוח את הפתרון $a=-\\frac1{\\sqrt2}$ ולהציג כיוון אחד בלבד.",
              "לא לדרוש $a^2+b^2=1$ (וקטור כיוון חייב להיות וקטור יחידה)."],
    steps=[
        num(r"מהו $f'_x(1,-1)=1+y$ בנקודה?", 0, r"$1+(-1)=0$."),
        num(r"מהו $b$ (תשובה עשרונית, דיוק $0.001$)?", 0.7071,
            r"$D_{\vec u}f=(0,1)\cdot(a,b)=b=\frac1{\sqrt2}\approx0.7071$.", tol=0.001),
        num(r"מהו $a^2$?", 0.5, r"$a^2=1-b^2=1-\frac12=\frac12$."),
        choice(r"מהם הכיוונים המתאימים?",
               r"$\left(\frac1{\sqrt2},\frac1{\sqrt2}\right)$ וגם $\left(-\frac1{\sqrt2},\frac1{\sqrt2}\right)$",
               [r"רק $\left(\frac1{\sqrt2},\frac1{\sqrt2}\right)$",
                r"$\left(\frac1{\sqrt2},-\frac1{\sqrt2}\right)$ וגם $\left(-\frac1{\sqrt2},-\frac1{\sqrt2}\right)$"],
               r"$a$ יכול להיות חיובי או שלילי, ולכן יש שני כיוונים עם $b=\frac1{\sqrt2}$. כיוון יחיד מחמיץ פתרון, ובכיוונים עם $b=-\frac1{\sqrt2}$ הנגזרת היא $-\frac1{\sqrt2}$ ולא $\frac1{\sqrt2}$.", pos=1),
    ])

add(2, "א",
    rubric=rub(("הטור הראשון: מבחן האינטגרל לטור הערכים המוחלטים; האינטגרל מתבדר ($\\ln\\ln(b+1)\\to\\infty$)", 3),
               ("הטור הראשון: תנאי לייבניץ (האיבר יורד ושואף ל-$0$), ולכן מתכנס בתנאי", 3),
               ("הטור השני: מבחן השורש, $\\sqrt[n]{\\frac{(-1)^n+n}{3^n}}\\to\\frac13$", 3),
               ("סנדוויץ' ומסקנה: הטור החיובי מתכנס, ולכן בהחלט", 3)),
    pitfalls=["להסיק התכנסות בהחלט מלייבניץ בלבד: צריך לבדוק גם את טור הערכים המוחלטים.",
              "לחשוב ש-$(-1)^n$ משנה את הגבול בשורש: $\\sqrt[n]{n\\pm1}\\to1$, והטור כולו חיובי."],
    steps=[
        choice(r"מה דינו של הטור הראשון $\sum\frac{(-1)^n}{(n+1)\ln(n+1)}$?",
               r"מתכנס בתנאי",
               [r"מתכנס בהחלט", r"מתבדר"],
               r"טור הערכים המוחלטים מתבדר לפי מבחן האינטגרל ($\int\frac{dx}{(x+1)\ln(x+1)}=\ln\ln(x+1)\to\infty$), אבל האיברים יורדים ושואפים ל-$0$, ולכן לפי לייבניץ הטור עצמו מתכנס.", pos=2),
        num(r"מהו $\lim_{n\to\infty}\sqrt[n]{\dfrac{(-1)^n+n}{3^n}}$ (תשובה עשרונית, דיוק $0.001$)?", 0.3333,
            r"$\sqrt[n]{(-1)^n+n}\to1$ ו-$\sqrt[n]{3^n}=3$, ולכן הגבול $\frac13$.", tol=0.001),
        choice(r"מה דינו של הטור השני $\sum\frac{(-1)^n+n}{3^n}$?",
               r"מתכנס בהחלט",
               [r"מתכנס בתנאי בלבד", r"מתבדר"],
               r"הגבול $\frac13<1$ ולכן הטור מתכנס; כל איבריו חיוביים ($n\ge1$ ולכן $(-1)^n+n\ge0$), ולכן התכנסות פירושה התכנסות בהחלט.", pos=1),
    ])

add(2, "ב",
    rubric=rub(("$f'_x(0,0)=\\frac12$ לפי הגדרת הגבול", 3), ("$f'_y(0,0)=1$ לפי הגדרת הגבול", 3),
               ("בניית $\\varepsilon$ והצבת המסלול $\\Delta y=k\\Delta x$", 3), ("הגבול תלוי ב-$k$", 2),
               ("מסקנה: $f$ לא דיפרנציאבילית ב-$(0,0)$", 2)),
    pitfalls=["להסיק דיפרנציאביליות מעצם קיום הנגזרות החלקיות בראשית.",
              "לבדוק רק את המסלול $k=0$ (ציר ה-$x$), שבו הגבול $0$: צריך מסלול נוסף כדי להראות תלות ב-$k$."],
    steps=[
        num(r"מהו $f'_x(0,0)$?", 0.5, r"$\frac{f(\Delta x,0)}{\Delta x}=\frac{\Delta x^3/(2\Delta x^2)}{\Delta x}=\frac12$."),
        num(r"מהו $f'_y(0,0)$?", 1, r"$\frac{f(0,\Delta y)}{\Delta y}=\frac{\Delta y^3/\Delta y^2}{\Delta y}=1$."),
        num(r"מהו הגבול של $\varepsilon$ לאורך $\Delta y=\Delta x$ ($\Delta x\to0^+$), כלומר $k=1$ (דיוק $0.001$)?", -0.5893,
            r"$-\frac{k^2+4k}{2(2+k^2)\sqrt{1+k^2}}$ ב-$k=1$ נותן $-\frac{5}{6\sqrt2}\approx-0.589$, בעוד שב-$k=0$ הגבול הוא $0$.", tol=0.001),
        choice(r"מה דין הדיפרנציאביליות של $f$ ב-$(0,0)$?",
               r"לא דיפרנציאבילית: הגבול של $\varepsilon$ תלוי ב-$k$",
               [r"דיפרנציאבילית, כי שתי הנגזרות החלקיות קיימות",
                r"דיפרנציאבילית, כי $f$ רציפה בראשית"],
               r"דיפרנציאביליות דורשת $\varepsilon\to0$ לכל מסלול. כאן הגבול משתנה עם $k$ ואינו $0$, ולכן הפונקציה אינה דיפרנציאבילית; קיום נגזרות חלקיות או רציפות אינם מספיקים.", pos=2),
    ])

add(3, "א",
    rubric=rub(("הצבה $t=x+5$ ומבחן המנה: $R=1$", 4),
               ("הקצה $x=-4$: השוואה גבולית ל-$\\frac1{n^{4/3}}$, מתכנס ($p=\\frac43>1$)", 4),
               ("הקצה $x=-6$: טור הערכים המוחלטים הוא טור הקצה הקודם, ולכן מתכנס בהחלט", 2),
               ("תחום ההתכנסות $[-6,-4]$", 2)),
    pitfalls=["לחשב את החזקה של האיבר בצורה שגויה: $\\sqrt[3]{n}\\cdot\\sqrt{n^2}=n^{1/3}\\cdot n$, כלומר החזקה הכוללת היא $\\frac43$.",
              "להסיק מ-$R=1$ משהו על הקצוות: מבחן המנה אינו מכריע שם, ובודקים כל קצה לחוד."],
    steps=[
        num(r"מהו רדיוס ההתכנסות בהצבה $t=x+5$?", 1,
            r"$\frac{a_n}{a_{n+1}}\to1$, ולכן $R=1$."),
        num(r"האיבר $\frac1{\sqrt[3]{n+1}\sqrt{n^2+1}}$ מתנהג כמו $\frac1{n^p}$. מהו $p$ (דיוק $0.001$)?", 1.3333,
            r"$\sqrt[3]{n+1}\approx n^{1/3}$ ו-$\sqrt{n^2+1}\approx n$, ולכן $p=\frac13+1=\frac43\approx1.333$.", tol=0.001),
        choice(r"מה קורה בקצה $x=-4$ (הטור החיובי)?",
               r"מתכנס, כי $p=\frac43>1$",
               [r"מתבדר, כי האיבר דומה ל-$\frac1{\sqrt[3]n}$", r"מתבדר, כי $R=1$ ולכן הקצוות תמיד מתבדרים"],
               r"ההשוואה הגבולית מול $\sum\frac1{n^{4/3}}$ נותנת גבול $1$, והטור מתכנס. האיבר קטן בהרבה מ-$\frac1{\sqrt[3]n}$ (יש גם גורם $\frac1n$), ו-$R=1$ אינו קובע דבר לגבי הקצוות.", pos=1),
        choice(r"מהו תחום ההתכנסות?",
               r"$[-6,-4]$",
               [r"$(-6,-4)$", r"$[-6,-4)$", r"$(-6,-4]$"],
               r"שני הקצוות מתכנסים: ב-$x=-4$ הטור מתכנס והוא חיובי, וב-$x=-6$ טור הערכים המוחלטים שלו הוא אותו טור. לכן שני הקצוות נכללים.", pos=0),
    ])

ZX = r"$z'_x=-\dfrac{y}{3x^2}+y\,g'(xy)$ ו-$z'_y=\dfrac1{3x}+x\,g'(xy)$"
Z1 = r"גוזרים בכלל השרשרת עם $t=xy$: " + ZX
Z2 = r"מציבים באגף השמאלי: $x^2\left(-\dfrac{y}{3x^2}+y\,g'(xy)\right)-xy\left(\dfrac1{3x}+x\,g'(xy)\right)+\dfrac{2y}3$"
Z3 = r"פותחים סוגריים: $-\dfrac y3+x^2y\,g'(xy)-\dfrac y3-x^2y\,g'(xy)+\dfrac{2y}3$"
Z4 = r"האיברים עם $g'$ מצטמצמים ו-$-\dfrac y3-\dfrac y3+\dfrac{2y}3=0$, כנדרש"
add(3, "ב",
    rubric=rub(("הצבה $t=xy$ וגזירה בכלל השרשרת", 3), ("$z'_x=-\\frac{y}{3x^2}+y\\,g'(xy)$", 3),
               ("$z'_y=\\frac1{3x}+x\\,g'(xy)$", 3), ("הצבה באגף השמאלי, צמצום וקבלת $0$", 4)),
    pitfalls=["לשכוח את הנגזרת הפנימית: $t'_x=y$ ו-$t'_y=x$.",
              "טעות סימן בגזירת $\\frac{y}{3x}$ לפי $x$: מתקבל $-\\frac{y}{3x^2}$."],
    steps=[
        choice(r"מהי $\dfrac{\partial}{\partial x}g(xy)$?",
               r"$y\,g'(xy)$",
               [r"$g'(xy)$", r"$x\,g'(xy)$", r"$g'(x)\cdot y$"],
               r"לפי כלל השרשרת: $g'(xy)$ כפול הנגזרת של הפנימית $xy$ לפי $x$, שהיא $y$. הגורם $x$ הוא הנגזרת לפי $y$, ובלי הנגזרת הפנימית מקבלים תוצאה שגויה.", pos=2),
        order(r"סדרו את שלבי ההוכחה:", [Z1, Z2, Z3, Z4],
              r"קודם מחשבים את שתי הנגזרות החלקיות, אחר כך מציבים באגף השמאלי, פותחים סוגריים ורק אז מצמצמים."),
        findbug(r"באחד השלבים יש טעות. איזה?",
                [Z1, Z2, r"פותחים סוגריים: $-\dfrac y3+x^2y\,g'(xy)+\dfrac y3-x^2y\,g'(xy)+\dfrac{2y}3$", Z4], 2,
                r"בפתיחת הסוגריים של $-xy\cdot\frac1{3x}$ מקבלים $-\frac y3$ ולא $+\frac y3$."),
    ])

add(4, "א",
    rubric=rub(("סכום הטור ההנדסי $\\sum\\frac5{3^n}=\\frac52$", 4), ("פירוק $\\frac1{(n+3)(n+4)}=\\frac1{n+3}-\\frac1{n+4}$", 3),
               ("טור טלסקופי: הסכום $\\frac14$", 3), ("$S=\\frac52-4\\cdot\\frac14=\\frac32$", 2)),
    pitfalls=["לחשב את הטור ההנדסי החל מ-$n=0$ ולקבל $\\frac{15}2$ במקום $\\frac52$.",
              "לשכוח להכפיל את הסכום הטלסקופי ב-$4$ לפני החיסור."],
    steps=[
        num(r"מהו $\sum_{n=1}^{\infty}\dfrac5{3^n}$?", 2.5, r"$5\cdot\frac{1/3}{1-1/3}=5\cdot\frac12=\frac52$."),
        num(r"מהו $\sum_{n=1}^{\infty}\dfrac1{(n+3)(n+4)}$?", 0.25,
            r"הסכום הטלסקופי: $\frac14-\lim\frac1{N+4}=\frac14$."),
        num(r"מהו סכום הטור $S$?", 1.5, r"$\frac52-4\cdot\frac14=\frac52-1=\frac32$."),
    ])

add(4, "ב",
    rubric=rub(("נקודות קריטיות בפנים: $x\\in\\{0,\\pm\\frac12\\}$, $y\\in\\{0,\\pm1\\}$, וכולן בתוך הדיסק", 3),
               ("ערכי $f$ בפנים; המינימלי שבהם $-\\frac98$", 2),
               ("לגרנז' על השפה $x^2+y^2=2$: שלוש משפחות פתרונות", 4),
               ("ערכי $f$ בשפה: $6$, $0$ ו-$-\\frac34$", 2), ("מקסימום $6$ ומינימום $-\\frac98$", 2)),
    pitfalls=["לשכוח לבדוק את הנקודות הקריטיות שבפנים הדיסק, או את השפה.",
              "לא לוודא ש-$x^2+y^2<2$ בכל נקודה קריטית שנכללת כנקודה פנימית."],
    steps=[
        num(r"כמה נקודות קריטיות יש לפונקציה בפנים הדיסק?", 9,
            r"$x\in\{0,\pm\frac12\}$ ו-$y\in\{0,\pm1\}$ נותנים $3\cdot3=9$ נקודות, וכולן עם $x^2+y^2\le\frac14+1<2$."),
        num(r"מהו $f\left(\frac12,1\right)$?", -1.125, r"$2\cdot\frac1{16}+1-\frac14-2=-\frac98$."),
        num(r"מהו $f\left(\sqrt2,0\right)$ (נקודה על השפה)?", 6, r"$2\cdot4-2=6$."),
        num(r"מהו $f\left(\frac1{\sqrt2},\sqrt{\frac32}\right)$ (דיוק $0.001$)?", -0.75,
            r"$2\cdot\frac14+\frac94-\frac12-3=-\frac34$.", tol=0.001),
        num(r"מהו הערך המינימלי של $f$ בדיסק?", -1.125,
            r"הערכים: בפנים הקטן ביותר $-\frac98$, בשפה $6$, $0$, $-\frac34$. הקטן מכולם הוא $-\frac98$."),
    ])

add(5, "א",
    rubric=rub(("נגזרות חלקיות מפורקות לגורמים: $f'_x=(3-y)(6-2x-y)$, $f'_y=(3-x)(6-x-2y)$", 3),
               ("ארבע הנקודות הקריטיות $(0,3),(3,0),(3,3),(2,2)$", 3),
               ("נגזרות שניות ו-$\\Delta=4(3-y)(3-x)-(2x+2y-9)^2$", 3),
               ("סיווג: שלוש נקודות אוכף ומקסימום ב-$(2,2)$", 3)),
    pitfalls=["לפספס נקודות קריטיות: כל גורם מתאפס בנפרד ($y=3$ או $x=3$), וצריך לבדוק את כל הצירופים.",
              "לסווג לפי סימן $f''_{xx}$ בלבד כש-$\\Delta<0$: אז הנקודה אוכף בכל מקרה."],
    steps=[
        num(r"כמה נקודות קריטיות יש לפונקציה?", 4,
            r"מ-$(3-y)(6-2x-y)=0$ ו-$(3-x)(6-x-2y)=0$ מתקבלות $(3,3)$, $(0,3)$, $(3,0)$ ו-$(2,2)$."),
        num(r"מהו $\Delta$ בנקודה $(0,3)$?", -9, r"$4(3-3)(3-0)-(0+6-9)^2=-9$."),
        num(r"מהו $\Delta$ בנקודה $(2,2)$?", 3, r"$4\cdot1\cdot1-(4+4-9)^2=4-1=3$."),
        choice(r"איך מסווגים את $(2,2)$?",
               r"מקסימום מקומי",
               [r"מינימום מקומי", r"נקודת אוכף", r"המבחן אינו מכריע"],
               r"$\Delta=3>0$ ו-$f''_{xx}(2,2)=-6+2\cdot2=-2<0$, ולכן מקסימום. אוכף דורש $\Delta<0$, מינימום דורש $f''_{xx}>0$, והמבחן אינו מכריע רק כש-$\Delta=0$.", pos=2),
    ])

add(5, "ב",
    rubric=rub(("כתיבת $\\frac{x}{25+x^2}$ כסכום הנדסי עם $q=-\\left(\\frac x5\\right)^2$", 4),
               ("הטור $\\sum(-1)^n\\frac{x^{2n+1}}{5^{2n+2}}$", 3),
               ("תחום ההתכנסות $|x|<5$; בקצוות $x=\\pm5$ הטור מתבדר", 3),
               ("$f^{(5)}(0)=c_5\\cdot5!$ עם $n=2$: $\\frac{4!}{5^5}$", 3)),
    pitfalls=["לקחת $n=5$ כשמחפשים את המקדם של $x^5$: החזקה היא $2n+1$, ולכן $n=2$.",
              "לשכוח את הגורם $x$ במונה ולקבל טור בחזקות זוגיות."],
    steps=[
        num(r"מהו רדיוס ההתכנסות?", 5, r"הטור ההנדסי מתכנס כאשר $\left|\frac x5\right|<1$, כלומר $|x|<5$."),
        choice(r"מהו תחום ההתכנסות?",
               r"$(-5,5)$",
               [r"$[-5,5]$", r"$[-5,5)$", r"$(-5,5]$"],
               r"בקצוות $x=\pm5$ האיבר הכללי הוא $\pm\frac15$ ואינו שואף ל-$0$, ולכן הטור מתבדר בשני הקצוות.", pos=1),
        num(r"עבור איזה $n$ מתקבלת החזקה $x^5$ בטור $\sum(-1)^n\frac{x^{2n+1}}{5^{2n+2}}$?", 2, r"$2n+1=5$ נותן $n=2$."),
        num(r"מהו $f^{(5)}(0)$ (תשובה עשרונית, דיוק $0.00001$)?", 0.00768,
            r"המקדם $c_5=\frac1{5^6}$ ולכן $f^{(5)}(0)=\frac{5!}{5^6}=\frac{4!}{5^5}=\frac{24}{3125}=0.00768$.", tol=0.00001),
    ])

exam = {
    "examCode": "24A-B",
    "examLabel": "מבחן סוף סמסטר א' תשפ\"ד, מועד ב'",
    "year": 2024,
    "examDate": "06/05/2024",
    "sourceFile": "calculus-2/24A-B exam 6.5.24.pdf",
    "solutionFile": "calculus-2/24A-B solution (file misnamed 6.5.25; it is the solution of the 6.5.24 exam)",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
