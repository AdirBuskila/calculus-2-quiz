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
$$\int_1^{\infty}\frac{dx}{(x+1)\ln(x+1)}=\left|\,t=\ln(x+1),\ dt=\frac{dx}{x+1}\right|=\int_{\ln2}^{\infty}\frac{dt}{t}=\infty$$
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

# ---- rubric / pitfalls / steps (ai-verified); expected values are machine-checked in tools/verify/24B-A/steps_24B-A.py ----
IDS = "abcdefgh"


def opts(*vals):
    return [{"id": IDS[i], "type": "text", "value": v} for i, v in enumerate(vals)]


def rub(*items):
    return [{"text": t, "points": p} for t, p in items]


def add(num, part, **kw):
    for q in questions:
        if q["num"] == num and q.get("part") == part:
            q.update(kw)
            return
    raise KeyError((num, part))


add(1, "א",
    rubric=rub((r"בחירת מסלול מתאים, $y=x^2$", 3),
               (r"חישוב הגבול לאורכו: $\frac15$", 2),
               (r"השוואה ל-$f(0,0)=0$ והמסקנה שהפונקציה אינה רציפה", 2)),
    rubricSource="ai-verified",
    pitfalls=[r"לבדוק רק ישרים $y=kx$: לאורכם הגבול הוא $0$ ומתקבלת מסקנה שגויה של רציפות.",
              r"לסיים אחרי מציאת גבול שונה בלי להשוות במפורש ל-$f(0,0)=0$.",
              r"לחשוב שהגדרת $f(0,0)=0$ לבדה מבטיחה רציפות."],
    steps=[
        {"type": "numeric", "prompt": r"לאורך המסלול $y=x^2$, לאיזה גבול שואפת $f$ כאשר $x\to0$ (עשרוני)?", "answer": 0.2, "tol": 0.001,
         "explain": r"$\frac{x^4}{2x^4+3x^4}=\frac15$ (sympy)."},
        {"type": "choice", "prompt": r"לאורך הישרים $y=kx$ הגבול הוא $0$, ולאורך $y=x^2$ הוא $\frac15$. מה המסקנה?",
         "options": opts(r"הגבול בראשית אינו קיים (או שונה מ-$0$), ולכן $f$ אינה רציפה ב-$(0,0)$",
                         "הגבול בראשית הוא $0$, ולכן $f$ רציפה",
                         r"הגבול הוא $\frac15$, ולכן $f$ רציפה בראשית",
                         "לא ניתן להכריע בלי לבדוק גם קואורדינטות קוטביות"),
         "correctId": "a",
         "explain": r"מסלול אחד שנותן ערך שונה מ-$f(0,0)=0$ מספיק כדי להפריך רציפות."},
    ],
    stepsSource="ai-verified")

add(1, "ב",
    rubric=rub((r"$f'_x(0,0)=0$ לפי ההגדרה", 2),
               (r"$f'_y(0,0)=0$ לפי ההגדרה", 2),
               ("פונקציה דיפרנציאבילית בנקודה חייבת להיות רציפה בה, ולכן אינה דיפרנציאבילית", 3)),
    rubricSource="ai-verified",
    pitfalls=["להסיק דיפרנציאביליות מעצם קיום הנגזרות החלקיות.",
              "לחשב את הנגזרת החלקית בראשית בנוסחאות גזירה רגילות במקום לפי ההגדרה.",
              "לא להשתמש בתוצאת הסעיף הקודם, ולנסות לבדוק את הגבול הדיפרנציאלי מההתחלה."],
    steps=[
        {"type": "numeric", "prompt": r"מהו $f'_x(0,0)$ לפי ההגדרה?", "answer": 0, "tol": 0,
         "explain": r"$f(h,0)=0$ לכל $h\neq0$, ולכן הגבול הוא $0$. גם $f'_y(0,0)=0$ (sympy)."},
        {"type": "choice", "prompt": "שתי הנגזרות החלקיות בראשית קיימות. האם $f$ דיפרנציאבילית ב-$(0,0)$?",
         "options": opts("לא, כי היא אינה רציפה בראשית", "כן, כי שתי הנגזרות החלקיות קיימות",
                         "כן, כי שתי הנגזרות החלקיות שוות ל-$0$", "כן, כי $f$ רציפה בראשית וגם הנגזרות החלקיות קיימות"),
         "correctId": "a",
         "explain": r"דיפרנציאביליות גוררת רציפות, ו-$f$ אינה רציפה (הסעיף הקודם). קיום הנגזרות החלקיות אינו מספיק."},
    ],
    stepsSource="ai-verified")

add(1, "ג",
    rubric=rub(("נגזרת חלקית לפי $x$ בכלל המנה", 3),
               ("נגזרת חלקית לפי $y$ בכלל המנה", 3),
               (r"הצבה ב-$(1,1)$: $-\frac2{25}$ ו-$\frac1{25}$", 2),
               (r"הדיפרנציאל $df=\frac{-2\,dx+dy}{25}$", 3)),
    rubricSource="ai-verified",
    pitfalls=["לשכוח את הנגזרת הפנימית $12x^3$ של המכנה בגזירה לפי $x$.",
              "להחליף בין המקדמים של $dx$ ו-$dy$.",
              r"לטעות בחישוב המכנה בנקודה: $(2+3)^2=25$."],
    steps=[
        {"type": "numeric", "prompt": r"מהו $f'_x(1,1)$ (עשרוני)?", "answer": -0.08, "tol": 0.001,
         "explain": r"$-\frac2{25}=-0.08$ (sympy)."},
        {"type": "numeric", "prompt": r"מהו $f'_y(1,1)$ (עשרוני)?", "answer": 0.04, "tol": 0.001,
         "explain": r"$\frac1{25}=0.04$ (sympy)."},
        {"type": "choice", "prompt": r"מהו הדיפרנציאל השלם $df$ בנקודה $(1,1)$?",
         "options": opts(r"$\frac{-2\,dx+dy}{25}$", r"$\frac{dx-2\,dy}{25}$", r"$\frac{2\,dx+dy}{25}$", r"$\frac{-2\,dx-dy}{25}$"),
         "correctId": "a",
         "explain": r"$df=f'_x\,dx+f'_y\,dy$ עם $f'_x(1,1)=-\frac2{25}$ ו-$f'_y(1,1)=\frac1{25}$."},
    ],
    stepsSource="ai-verified")

add(2, "א",
    rubric=rub((r"הערך המוחלט $|a_n|=\frac{3+\sin\sqrt n}{n^2}$", 4),
               (r"החסם $|a_n|\le\frac4{n^2}$", 3),
               (r"$\sum\frac4{n^2}$ מתכנס ($\alpha=2>1$), לכן מתכנס בהחלט", 3)),
    rubricSource="ai-verified",
    pitfalls=[r"להשוות ל-$\frac4n$: החסם נכון אבל הטור ההרמוני מתבדר, ולכן אין מסקנה.",
              "להשתמש במבחן לייבניץ ולהסיק רק התכנסות בתנאי, בלי לבדוק התכנסות בהחלט.",
              r"לחשוב שהגורם $\sin\sqrt n$ משנה את סוג ההתכנסות: הוא חסום ולכן $3+\sin\sqrt n\le4$."],
    steps=[
        {"type": "numeric", "prompt": r"מהו החסם העליון הטוב ביותר ל-$3+\sin\sqrt n$?", "answer": 4, "tol": 0,
         "explain": r"$\sin\sqrt n\le1$ ולכן $3+\sin\sqrt n\le4$ (ונבדק מספרית שהחסם כמעט מושג)."},
        {"type": "choice", "prompt": r"עם החסם $|a_n|\le\frac{4}{n^2}$, לאיזה טור כדאי להשוות כדי להסיק מסקנה?",
         "options": opts(r"$\sum\frac4{n^2}$, שמתכנס כטור-$p$ עם $p=2>1$", r"$\sum\frac4n$, שמתבדר ולכן אין ממנו מסקנה",
                         r"$\sum\frac{(-1)^n}{n}$, שמתכנס בתנאי", r"$\sum 4$"),
         "correctId": "a",
         "explain": r"רק ההשוואה לטור מתכנס חסם מלמעלה נותנת מסקנה. הטור $\sum\frac4n$ מתבדר, ולכן אי-השוויון איתו אינו מוכיח כלום."},
        {"type": "choice", "prompt": "מה המסקנה לגבי הטור הנתון?",
         "options": opts("מתכנס בהחלט", "מתכנס בתנאי", "מתבדר", "אי אפשר להכריע"), "correctId": "a",
         "explain": r"$\sum|a_n|$ מתכנס לפי מבחן ההשוואה, ולכן הטור מתכנס בהחלט."},
    ],
    stepsSource="ai-verified")

add(2, "ב",
    rubric=rub((r"תנאי לייבניץ: $a_n>0$, יורד ושואף ל-$0$", 5),
               ("מסקנה: הטור המתחלף מתכנס", 2),
               (r"הגדרת $f(x)=\frac1{(x+1)\ln(x+1)}$ וטענה שהיא חיובית ויורדת", 2),
               ("מבחן האינטגרל: האינטגרל מתבדר ולכן הטור בערכים מוחלטים מתבדר", 4),
               ("מסקנה: הטור מתכנס בתנאי", 2)),
    rubricSource="ai-verified",
    pitfalls=["להסתפק במבחן לייבניץ ולהסיק התכנסות בלי לבדוק אם היא בהחלט או בתנאי.",
              r"להשתמש במבחן המנה על הטור בערכים מוחלטים: המנה שואפת ל-$1$ ואין מסקנה.",
              "להפעיל מבחן אינטגרל בלי לוודא שהפונקציה חיובית ויורדת."],
    steps=[
        {"type": "choice", "prompt": r"עבור $a_n=\frac1{(n+1)\ln(n+1)}$, אילו תנאים של לייבניץ מתקיימים?",
         "options": opts(r"$a_n>0$, הסדרה יורדת ו-$a_n\to0$, ולכן הטור המתחלף מתכנס",
                         r"$a_n>0$ ו-$a_n\to0$ אך הסדרה אינה יורדת",
                         r"הסדרה יורדת אך אינה שואפת ל-$0$",
                         "הסדרה אינה חיובית"),
         "correctId": "a",
         "explain": r"המכנה $(n+1)\ln(n+1)$ חיובי ועולה ושואף ל-$\infty$ (נבדק מספרית ובגבול ב-sympy)."},
        {"type": "choice", "prompt": r"מה קורה לטור בערכים מוחלטים $\sum\frac1{(n+1)\ln(n+1)}$?",
         "options": opts(r"מתבדר, כי $\int_1^\infty\frac{dx}{(x+1)\ln(x+1)}$ מתבדר", r"מתכנס, כי $a_n\to0$",
                         r"מתכנס, כי הוא קטן מ-$\frac1{n^2}$", "מתכנס לפי מבחן המנה"),
         "correctId": "a",
         "explain": r"הפונקציה חיובית ויורדת, והאינטגרל הוא $\ln\ln(T+1)-\ln\ln2\to\infty$ (sympy), ולכן הטור מתבדר."},
        {"type": "choice", "prompt": "מה המסקנה הסופית לגבי הטור המתחלף?",
         "options": opts("מתכנס בתנאי", "מתכנס בהחלט", "מתבדר", "אי אפשר להכריע"), "correctId": "a",
         "explain": "הטור המתחלף מתכנס, אך הטור בערכים מוחלטים מתבדר."},
    ],
    stepsSource="ai-verified")

add(3, "א",
    rubric=rub(("חישוב הגרדיאנט $(4x,-2y)$", 2),
               ("הצבה בנקודה: $(8,-6)$, והכיוון הוא כיוון הגרדיאנט", 2)),
    rubricSource="ai-verified",
    pitfalls=["לטעות בסימן המרכיב השני: $f_y=-2y=-6$.",
              "להשאיר את הגרדיאנט כפונקציה בלי להציב את הנקודה $(2,3)$."],
    steps=[
        {"type": "numeric", "prompt": r"מהו $f'_x(2,3)$ עבור $f=2x^2-y^2+1$?", "answer": 8, "tol": 0,
         "explain": r"$f'_x=4x=8$."},
        {"type": "numeric", "prompt": r"מהו $f'_y(2,3)$?", "answer": -6, "tol": 0,
         "explain": r"$f'_y=-2y=-6$, ולכן הגרדיאנט הוא $(8,-6)$."},
    ],
    stepsSource="ai-verified")

add(3, "ב",
    rubric=rub(("הערך המקסימלי של הנגזרת הכיוונית שווה לאורך הגרדיאנט", 2),
               (r"חישוב $\sqrt{8^2+(-6)^2}=10$", 2)),
    rubricSource="ai-verified",
    pitfalls=["לענות בווקטור הגרדיאנט במקום באורכו.",
              "לשכוח את השורש ולענות $100$."],
    steps=[
        {"type": "choice", "prompt": "מה שווה הערך המקסימלי של הנגזרת הכיוונית בנקודה?",
         "options": opts("אורך הגרדיאנט בנקודה", "הגרדיאנט עצמו כווקטור", r"סכום הרכיבים $f'_x+f'_y$", "ריבוע אורך הגרדיאנט"),
         "correctId": "a",
         "explain": r"הנגזרת בכיוון $\mathbf u$ היא $\|\nabla f\|\cos\theta$, והמקסימום ב-$\theta=0$. כאן סכום הרכיבים הוא $2$ וריבוע האורך הוא $100$, ושניהם אינם הערך המקסימלי."},
        {"type": "numeric", "prompt": r"מהו הערך המקסימלי?", "answer": 10, "tol": 0,
         "explain": r"$\sqrt{64+36}=10$."},
    ],
    stepsSource="ai-verified")

add(3, "ג",
    rubric=rub(("פתרון $\\nabla f=0$ וקבלת הנקודה היחידה $(0,0)$", 2),
               ("נגזרות שניות $A=4,\\ B=0,\\ C=-2$", 2),
               ("$\\Delta=AC-B^2=-8<0$ ולכן נקודת אוכף", 3)),
    rubricSource="ai-verified",
    pitfalls=["לסווג לפי הסימן של $A$ בלבד, בלי הדטרמיננטה.",
              "לטעות ב-$C=f_{yy}=-2$ (ולא $-2y$).",
              "להסיק שאין נקודה קריטית רק כי אין קיצון."],
    steps=[
        {"type": "numeric", "prompt": "כמה נקודות קריטיות יש לפונקציה $f=2x^2-y^2+1$?", "answer": 1, "tol": 0,
         "explain": r"$\nabla f=(4x,-2y)=0$ רק ב-$(0,0)$."},
        {"type": "numeric", "prompt": r"מהי $\Delta=AC-B^2$ בנקודה הקריטית?", "answer": -8, "tol": 0,
         "explain": r"$A=4,\ B=0,\ C=-2$ ולכן $\Delta=-8$."},
        {"type": "choice", "prompt": "מה סוג הנקודה הקריטית?",
         "options": opts("נקודת אוכף", "מינימום מקומי", "מקסימום מקומי", "המבחן אינו מכריע"), "correctId": "a",
         "explain": r"$\Delta<0$ ולכן נקודת אוכף."},
    ],
    stepsSource="ai-verified")

add(3, "ד",
    rubric=rub(("בפנים התחום אין קיצון מקומי (הנקודה הקריטית היא אוכף)", 2),
               (r"פונקציית לגראנז' ומערכת על השפה $(x-1)^2+y^2=1$", 3),
               (r"הנקודות החשודות $(0,0),\ (2,0),\ \left(\frac13,\pm\frac{\sqrt5}3\right)$", 2),
               ("חישוב ערכי הפונקציה בנקודות", 2),
               (r"מסקנה: המקסימום $9$ והמינימום $\frac23$", 1)),
    rubricSource="ai-verified",
    pitfalls=["לבדוק רק את הנקודה הקריטית שבפנים ולשכוח את השפה.",
              r"לאבד את הפתרון $y=0$ או את שתי הנקודות עם $x=\frac13$ בפתרון המערכת.",
              r"לחשוב ש-$(0,0)$ בפנים התחום: היא על השפה, כי $(0-1)^2+0^2=1$."],
    steps=[
        {"type": "numeric", "prompt": "כמה נקודות חשודות מתקבלות מפתרון מערכת לגראנז' על השפה?", "answer": 4, "tol": 0,
         "explain": r"$(0,0),\ (2,0),\ \left(\frac13,\pm\frac{\sqrt5}3\right)$ (sympy)."},
        {"type": "numeric", "prompt": r"מהו $f(2,0)$?", "answer": 9, "tol": 0,
         "explain": r"$2\cdot4-0+1=9$, וזהו הערך המקסימלי (נבדק על רשת צפופה בתחום)."},
        {"type": "numeric", "prompt": r"מהו $f\left(\frac13,\frac{\sqrt5}{3}\right)$ (עשרוני)?", "answer": 0.6667, "tol": 0.001,
         "explain": r"$\frac29-\frac59+1=\frac23$, וזהו הערך המינימלי. בנקודה $(0,0)$ הערך הוא $1$."},
    ],
    stepsSource="ai-verified")

add(4, "א",
    rubric=rub(("הגדרת $F(x,y,z)=2x^2-y^2+z^2$ (המשטח הוא משטח רמה)", 2),
               ("הנגזרות החלקיות $4x,\\ -2y,\\ 2z$", 3),
               ("הצבה בנקודה $(1,-1,2)$: $(4,2,4)$", 2),
               ("משוואת המישור $4(x-1)+2(y+1)+4(z-2)=0$", 3)),
    rubricSource="ai-verified",
    pitfalls=["להציב את הנקודה בסימן שגוי: $y=-1$ נותן $-2y=+2$.",
              "לכתוב $(x+1)$ במקום $(x-1)$ במשוואת המישור.",
              "לא לוודא שהנקודה נמצאת על המשטח: $2-1+4=5$."],
    steps=[
        {"type": "numeric", "prompt": r"מהו $F'_y(1,-1,2)$ עבור $F=2x^2-y^2+z^2$?", "answer": 2, "tol": 0,
         "explain": r"$F'_y=-2y=-2\cdot(-1)=2$."},
        {"type": "numeric", "prompt": r"מהו $F'_z(1,-1,2)$?", "answer": 4, "tol": 0,
         "explain": r"$F'_z=2z=4$, ו-$F'_x=4x=4$ (sympy)."},
        {"type": "choice", "prompt": "מהי משוואת המישור המשיק?",
         "options": opts(r"$4(x-1)+2(y+1)+4(z-2)=0$", r"$4(x-1)-2(y+1)+4(z-2)=0$",
                         r"$4(x+1)+2(y-1)+4(z+2)=0$", r"$2(x-1)+4(y+1)+4(z-2)=0$"),
         "correctId": "a",
         "explain": "הוקטור הנורמלי הוא $(4,2,4)$ והמישור עובר דרך הנקודה $(1,-1,2)$. שאר האפשרויות הן עם נורמל אחר או שאינן עוברות בנקודה (נבדק ב-sympy)."},
    ],
    stepsSource="ai-verified")

add(4, "ב",
    rubric=rub((r"בחירת מבחן המנה והצבת $a_n$ ו-$a_{n+1}$", 5),
               (r"פישוט עם $(2n+2)!=(2n+2)(2n+1)(2n)!$ וקבלת $2n+1$", 5),
               (r"הגבול $\infty$ ולכן $R=\infty$", 3),
               (r"תחום ההתכנסות $(-\infty,\infty)$", 2)),
    rubricSource="ai-verified",
    pitfalls=[r"לפרוס את $(2n+2)!$ בצורה שגויה ולשכוח את הגורם $(2n+1)$.",
              r"להפוך את המנה (לחשב $\frac{a_{n+1}}{a_n}$ ולהסיק $R=0$).",
              r"לשכוח את הגורמים $2^{n+1}$ ו-$(n+1)!$ במכנה של $a_{n+1}$."],
    steps=[
        {"type": "numeric", "prompt": r"מהו $a_2=\frac{2^2\cdot2!}{4!}$ (עשרוני)?", "answer": 0.3333, "tol": 0.001,
         "explain": r"$\frac{8}{24}=\frac13$."},
        {"type": "numeric", "prompt": r"אחרי פישוט, $\frac{a_n}{a_{n+1}}=2n+1$. מה הערך שלו עבור $n=3$?", "answer": 7, "tol": 0,
         "explain": r"$\frac{(2n+2)(2n+1)}{2(n+1)}=2n+1$ (sympy), ועבור $n=3$ מתקבל $7$."},
        {"type": "choice", "prompt": "מהו תחום ההתכנסות של הטור?",
         "options": opts(r"$(-\infty,\infty)$, כי $R=\infty$", r"$\{0\}$ בלבד", r"$(-1,1)$", r"$[-2,2]$"), "correctId": "a",
         "explain": r"$\lim(2n+1)=\infty$, ולכן הרדיוס אינסופי והטור מתכנס לכל $x$."},
    ],
    stepsSource="ai-verified")

add(5, "א",
    rubric=rub(("פירוק $2x^2+3x+1=(x+1)(2x+1)$ ופירוק הלוגריתם לסכום", 2),
               (r"טור $\ln(1+x)$ וטור $\ln(1+2x)$ בהצבה", 3),
               (r"סכום הטורים והמקדם $\frac{(-1)^{n+1}(1+2^n)}{n}$", 3)),
    rubricSource="ai-verified",
    pitfalls=["לנסות לפתח ישירות את הלוגריתם של הפולינום בלי לפרק אותו למכפלה.",
              r"לשכוח להעלות את $2$ בחזקת $n$ בטור של $\ln(1+2x)$.",
              r"לטעות בסימן $(-1)^{n+1}$: המקדם של $x^2$ שלילי."],
    steps=[
        {"type": "choice", "prompt": r"כיצד מפרקים את $\ln(2x^2+3x+1)$ לשני לוגריתמים מוכרים?",
         "options": opts(r"$\ln(x+1)+\ln(2x+1)$", r"$\ln(x+1)-\ln(2x+1)$", r"$\ln(2x)+\ln(x+1)$", r"$2\ln(x+1)$"),
         "correctId": "a",
         "explain": r"$(x+1)(2x+1)=2x^2+3x+1$ (sympy), ולכן הלוגריתם הוא סכום."},
        {"type": "numeric", "prompt": r"מהו המקדם של $x^2$ בטור (עשרוני)?", "answer": -2.5, "tol": 0.001,
         "explain": r"$-\frac{1+2^2}{2}=-\frac52$."},
        {"type": "numeric", "prompt": r"מהו המקדם של $x^3$ בטור?", "answer": 3, "tol": 0,
         "explain": r"$\frac{1+2^3}{3}=3$ (נבדק מול הטור של sympy)."},
    ],
    stepsSource="ai-verified")

add(5, "ב",
    rubric=rub((r"חישוב $\frac1R=\lim\sqrt[n]{\frac{1+2^n}{n}}=2$ ולכן $R=\frac12$", 4),
               (r"קצה ימני $x=\frac12$: הטור מתכנס לפי לייבניץ", 2),
               (r"קצה שמאלי $x=-\frac12$: הטור מתבדר (דומה לטור ההרמוני)", 2)),
    rubricSource="ai-verified",
    pitfalls=[r"לקחת את הרדיוס $1$ של $\ln(1+x)$ בלבד: הגורם $\ln(1+2x)$ מקטין אותו ל-$\frac12$.",
              "לא לבדוק את הקצוות, או להניח שהטור מתכנס בשניהם.",
              r"להפוך את הגבול ולקבל $R=2$."],
    steps=[
        {"type": "numeric", "prompt": r"מהו רדיוס ההתכנסות של הטור (עשרוני)?", "answer": 0.5, "tol": 0.001,
         "explain": r"$\lim\sqrt[n]{\frac{1+2^n}{n}}=2$ ולכן $R=\frac12$ (sympy)."},
        {"type": "choice", "prompt": "מהו תחום ההתכנסות?",
         "options": opts(r"$\left(-\frac12,\frac12\right]$", r"$\left[-\frac12,\frac12\right]$",
                         r"$\left(-\frac12,\frac12\right)$", r"$\left[-\frac12,\frac12\right)$"),
         "correctId": "a",
         "explain": r"ב-$x=\frac12$ הטור המתחלף מתכנס (לייבניץ, ערכו $\ln3$), וב-$x=-\frac12$ האיברים מתנהגים כמו $\frac1n$ והטור מתבדר."},
    ],
    stepsSource="ai-verified")

add(5, "ג",
    rubric=rub((r"הקשר $\frac{f^{(n)}(0)}{n!}=a_n$", 3),
               (r"המקדם $a_5=\frac{(-1)^{6}(1+2^5)}{5}=\frac{33}5$", 3),
               (r"$f^{(5)}(0)=5!\cdot\frac{33}5=33\cdot4!=792$", 3)),
    rubricSource="ai-verified",
    pitfalls=["לשכוח להכפיל ב-$5!$ ולהסתפק ב-$\\frac{33}5$.",
              r"לטעות בסימן: עבור $n=5$ מתקבל $(-1)^{6}=+1$.",
              r"לחשב $1+2^5$ בטעות כ-$2^5$ או $31$."],
    steps=[
        {"type": "numeric", "prompt": r"מהו המקדם $a_5$ של $x^5$ בטור (עשרוני)?", "answer": 6.6, "tol": 0.001,
         "explain": r"$\frac{1+32}{5}=\frac{33}5=6.6$."},
        {"type": "numeric", "prompt": r"מהו $f^{(5)}(0)$?", "answer": 792, "tol": 0,
         "explain": r"$5!\cdot\frac{33}5=792$ (נבדק גם בגזירה ישירה ב-sympy)."},
    ],
    stepsSource="ai-verified")

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
