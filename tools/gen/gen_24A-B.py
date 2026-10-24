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

HOLD
- Q3a: the key's radius (R=1) and final domain [-6,-4] are correct (sympy), but its endpoint comparison step divides by
  1/cuberoot(n^2) (= n^(-2/3), limit 0, not 1) and then concludes convergence "like sum 1/n^(3/2)"; the terms behave like
  n^(-4/3). The official comparison is internally inconsistent, so the question is held (see docs/ASK_ADIR.md).

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
ולכן הגבול של $f(x,y)$ כאשר $(x,y)\to(0,0)$ אינו קיים, ומכאן $f$ אינה רציפה ב-$(0,0)$.""", part="א", points=12))

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
questions.append({
    "num": 3, "part": "א", "kind": "computation", "topic": "power_series", "points": 12,
    "question": r"""עבור אילו ערכי $x$ הטור מתכנס (מצאו רדיוס התכנסות ותחום התכנסות):
$$\sum_{n=1}^{\infty}\frac{(x+5)^n}{\sqrt[3]{n+1}\sqrt{n^2+1}}$$""",
    "hold": "the key's R=1 and final domain [-6,-4] are right (sympy), but its endpoint step compares with 1/cuberoot(n^2) "
            "(ratio tends to 0, not 1) and then cites sum 1/n^(3/2); the terms behave like n^(-4/3). The official comparison "
            "is inconsistent; needs Adir's decision",
})

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
