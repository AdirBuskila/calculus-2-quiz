# -*- coding: utf-8 -*-
"""Generator for tools/raw/25A-B.json -- calculus-2 (20252), semester A 2025, moed B (20/03/2025).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_25A-B.py

Source: sitting 25A-B. The orchestrator's ruling: 25A-B = exam 20.3.25, and the file called "winter 2025 moed B"
is the same sitting (verified: the three rendered pages are pixel-identical to the 20.3.25 exam).
Exam: 3 pages, 5 questions of 25 points (a=12, b=13), solve 4 of 5.
Solution file ("solutions 20.3.25", 8 pages): Q1 and Q4 typed, Q2 typed, Q3 handwritten on a tablet,
Q5 typed. Exam header (lecturer names) is not transcribed.

Solution labelling (orchestrator ruling 2026-10-24): the key file is handwritten/mixed with no named author, so every
item is solutionSource "student-solution", official False. Fixes of key typos start with the words
"תיקון לפתרון שבקובץ:".

Transcription notes
- The text layers are garbled; everything is transcribed from page renders.
- Q1a: the key computes the linear approximation 3.875 (exact value of the root is about 3.8665).
- Q2b: the key's inverse map prints y = (1/3)(v + 1t); with t = y - x and v = y + 2x the correct inverse is
  y = (v + 2t)/3 (sympy), and the key's Jacobian 1/3 and final answer agree with the correct inverse.
  Transcribed here with 2t plus a labelled correction line (evident typo in the key); logged in docs/ASK_ADIR.md.
- Q3b: the key writes dt/dx in the dz/dy line; it means dt/dy. Transcribed as t'_y.
- Q4a: the key's hand sketch is not copied; the region figure is drawn by the transcriber from the bounds.
- Q5b: the key's decimal "1.71166" is not the value of 5!(1/64 - 1/729) (= 3325/1944 = 1.71039...).
  The exact value is given with a labelled correction (תיקון לפתרון שבקובץ); logged in docs/ASK_ADIR.md.
- Q2b figure: drawn by the transcriber from the four printed lines.

Checks (tools/verify/25A-B/check.py, sympy + numeric): all answers match. No holds.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "25A-B.json"


def Q(num, kind, topic, question, solution, part=None, **kw):
    q = {"num": num, "kind": kind, "topic": topic, "question": question, "solution": solution.strip("\n"),
         "solutionSource": "student-solution", "official": False, "confidence": "high"}
    if part:
        q["part"] = part
    q.update(kw)
    return q


questions = []

# ===== Q1a =====
questions.append(Q(1, "computation", "partials_differentiability", r"""חשבו בקירוב את $\sqrt{41-4(2.1)^2-(2.9)^2}$
(הגדירו פונקציה מתאימה והעזרו בדיפרנציאל הראשון).""",
r"""מוגדרים הפונקציה $f(x,y)=\sqrt{41-4x^2-y^2}$ והנקודה $(x_0,y_0)=(2,3)$,
$$f(x_0,y_0)=f(2,3)=\sqrt{41-4(2)^2-(3)^2}=\sqrt{41-16-9}=\sqrt{16}=4;$$
$$x=2.1\implies\Delta x=x-x_0=0.1,\qquad y=2.9\implies\Delta y=y-y_0=-0.1;$$
הבה נחשב כעת את הנגזרות החלקיות:
$$\frac{\partial f}{\partial x}=\frac12\left(41-4x^2-y^2\right)^{-\frac12}(-8x)\implies\frac{\partial f}{\partial x}(2,3)=\frac{-16}{8}=-2$$
$$\frac{\partial f}{\partial y}=\frac12\left(41-4x^2-y^2\right)^{-\frac12}(-2y)\implies\frac{\partial f}{\partial y}(2,3)=-\frac34.$$
אנחנו יודעים ש-
$$f(x,y)=f(x_0+\Delta x,y_0+\Delta y)\approx f(x_0,y_0)+\frac{\partial f}{\partial x}(x_0,y_0)\Delta x+\frac{\partial f}{\partial y}(x_0,y_0)\Delta y$$
$$\implies\sqrt{41-4(2.1)^2-(2.9)^2}=f(2.1,2.9)\approx4-2(0.1)+\frac34(0.1)=3.875.$$""", part="א", points=12))

# ===== Q1b =====
questions.append(Q(1, "computation", "absolute_extrema", r"""מצאו אקסטרמומים מוחלטים של הפונקציה $f(x,y)=x\cdot y$ תחת האילוץ $x^2+y^2=2$""",
r"""נשתמש בשיטת כופלי לגרנז'. נבנה את הפונקציה הלגרנז'
$$L(x,y,\lambda)=f(x,y)+\lambda(x^2+y^2-2)=xy+\lambda(x^2+y^2-2)$$
ואנו נפתור את המערכת הבאה:
$$\frac{\partial L}{\partial x}=y+2\lambda x=0\implies\lambda=-\frac{y}{2x}$$
$$\frac{\partial L}{\partial y}=x+2\lambda y=0\implies\lambda=-\frac{x}{2y}\qquad\implies\qquad x^2=y^2\iff x=\pm y$$
$$\frac{\partial L}{\partial\lambda}=x^2+y^2-2=0$$
אנו מציבים בשוואה האחרונה:
$$2x^2=2\implies x^2=1\implies x=\pm1$$
לכן קיבלנו הנקודות הבאות:
$$(1,1),\quad(1,-1),\quad(-1,1),\quad(-1,-1)$$
ערך מקסימלי: $f(1,1)=f(-1,-1)=1$
ערך המינימלי: $f(-1,1)=f(1,-1)=-1$
מקסימום מוחלט: $(1,1)$, $(-1,-1)$.
מינימום מוחלט: $(-1,1)$, $(1,-1)$.""", part="ב", points=13))

# ===== Q2a =====
questions.append(Q(2, "computation", "numeric_series", r"""בדקו האם הטור מתכנס. במידה וכן חשבו את סכומו
$$\sum_{n=2}^{\infty}\frac{1}{n(n-1)}$$""",
r"""נבנה סדרת הסכומים החלקיים המתאימה לטור המקורי:
$$S_n=\sum_{k=2}^n\frac{1}{k(k-1)}=\frac{1}{2\cdot1}+\frac{1}{3\cdot2}+\cdots+\frac{1}{n(n-1)}=\left(1-\frac12\right)+\left(\frac12-\frac13\right)+\cdots+\left(\frac{1}{n-1}-\frac1n\right)=1-\frac1n$$
מכאן נובע ש-
$$\sum_{n=2}^{\infty}\frac{1}{n(n-1)}=\lim_{n\to\infty}S_n=\lim_{n\to\infty}\left(1-\frac1n\right)=1.$$""", part="א", points=12))

# ===== Q2b =====
questions.append(Q(2, "computation", "change_of_variables", r"""חשבו את ערך האינטגרל $\displaystyle\iint_D\frac{y-x}{2x+y}\,dx\,dy$
כאשר $D$ הוא התחום המישורי החסום על ידי הקווים:
$$y=1+x,\quad y=4+x,\quad y=8-2x,\quad y=6-2x$$""",
r"""אם נגדיר $\begin{cases}t=y-x\\ v=y+2x\end{cases}$, אז נקבל ש-$T:\begin{cases}x=\frac13(v-t)\\ y=\frac13(v+2t)\end{cases}$ ויעקוביאן של $T$ הוא $J=\frac13$.
תיקון לפתרון שבקובץ: בפתרון שבקובץ נכתב $y=\frac13(v+1t)$ (טעות הקלדה); הנוסחה הנכונה היא $y=\frac13(v+2t)$, וכך נעשה בהמשך.
![התחום D: מקבילית עם הקודקודים (5/3, 8/3), (7/3, 10/3), (4/3, 16/3), (2/3, 14/3)](images/exams/25A-B-Q2b-region.png)
בתחום החדש $1\le t\le4$ ו-$6\le v\le8$. כתוצאה מכך:
$$\iint_D\frac{y-x}{2x+y}\,dx\,dy=\frac13\int_1^4\int_6^8\frac tv\,dt\,dv=\frac13\left(\left.\frac{t^2}{2}\right|_1^4\right)\left(\ln v\Big|_6^8\right)=\frac13\cdot\frac{15}{2}\cdot\ln\frac43=\frac52\cdot\ln\frac43$$""", part="ב", points=13))

# ===== Q3a =====
questions.append(Q(3, "computation", "power_series", r"""עבור אילו ערכי $x$ הטור מתכנס (מצאו רדיוס התכנסות ותחום התכנסות):
$$\sum_{n=1}^{\infty}\sin^2\left(\frac1n\right)(x-1)^n$$""",
r"""רדיוס ההתכנסות נמצא לפי דלמבר:
$$\lim_{n\to\infty}\frac{|a_n|}{|a_{n+1}|}=\lim_{n\to\infty}\frac{\sin^2\left(\frac1n\right)}{\sin^2\left(\frac{1}{n+1}\right)}=$$
$$\lim_{n\to\infty}\frac{\sin^2\left(\frac1n\right)}{\left(\frac1n\right)^2}\cdot\frac{\left(\frac{1}{n+1}\right)^2}{\sin^2\left(\frac{1}{n+1}\right)}\cdot\frac{\left(\frac1n\right)^2}{\left(\frac{1}{n+1}\right)^2}=1$$
$$R=1$$
נבדוק מה קורה בקצוות, כלומר כאשר $x=0$ וכאשר $x=2$:
* $x=2$: מתקבל הטור $\sum_{n=1}^{\infty}\sin^2\left(\frac1n\right)$. הטור מתכנס, מכיוון שמבחן ההשוואה הגבולית עבור טורים חיוביים עם הטור המתכנס $\sum_{n=1}^{\infty}\frac{1}{n^2}$.
* $x=0$: מתקבל הטור $\sum_{n=1}^{\infty}\sin^2\left(\frac1n\right)(-1)^n$. הטור מתכנס כי הטור בערכים המוחלטים של האיברים שלו מתכנס (בדקנו כש-$x=2$).

תשובה סופית:
תחום ההתכנסות: $0\le x\le2$
רדיוס ההתכנסות: $R=1$""", part="א", points=12))

# ===== Q3b =====
questions.append(Q(3, "proof", "chain_rule_identity", r"""הראו כי הפונקציה $z=y\cdot g(\cos(x-y))$ כאשר $g(t)$ גזירה עבור כל $t$ ו-$x,y\ne0$ מקיימת את המשוואה: $\dfrac{\partial z}{\partial x}+\dfrac{\partial z}{\partial y}=\dfrac zy$.""",
r"""נסמן $t=\cos(x-y)$:
$$\frac{\partial z}{\partial x}=y\cdot\frac{dg}{dt}\cdot\frac{\partial t}{\partial x}=y\cdot\frac{dg}{dt}\cdot(-\sin(x-y))$$
$$\frac{\partial z}{\partial y}=1\cdot g(t)+y\cdot\frac{dg}{dt}\cdot\frac{\partial t}{\partial y}=g(t)+y\cdot\frac{dg}{dt}\cdot(+\sin(x-y))$$
תיקון לפתרון שבקובץ: בפתרון שבקובץ נכתב כאן $\frac{\partial t}{\partial x}$ במקום $\frac{\partial t}{\partial y}$.
נציב באגף שמאל של המשוואה:
$$\frac{\partial z}{\partial x}+\frac{\partial z}{\partial y}=y\cdot\frac{dg}{dt}\cdot(-\sin(x-y))+g(t)+y\cdot\frac{dg}{dt}\cdot\sin(x-y)=g(t)=\frac zy$$
כנדרש.""", part="ב", points=13))

# ===== Q4a =====
questions.append(Q(4, "computation", "double_integrals", r"""החליפו את סדר האינטגרציה באינטגרל
$$\int_{-4}^0dx\int_0^{\sqrt{x+4}}f(x,y)\,dy+\int_0^2dx\int_0^{2-x}f(x,y)\,dy$$""",
r"""נתחיל עם ציור התחום:
![תחום האינטגרציה: מתחת ל-$y=\sqrt{x+4}$ עבור $-4\le x\le0$, ומתחת ל-$y=2-x$ עבור $0\le x\le2$](images/exams/25A-B-Q4a-region.png)
כאשר נשנה את סדר האינטגרציה, גבולות האינטגרציה ישתנו בהתאם:
שטח ראשון:
$$0\le y\le\sqrt{x+4},\qquad-4\le x\le0$$
ולאחר החלפת משתנים: $y^2-4\le x\le0,\quad0\le y\le2$
שטח שני:
$$0\le y\le2-x,\qquad0\le x\le2$$
ולאחר החלפת משתנים: $0\le x\le2-y,\quad0\le y\le2$
נוכל לאחד בין גבולות אילו ולקבל את האינטגרל:
$$\int_0^2\int_{y^2-4}^{2-y}f(x,y)\,dx\,dy$$""", part="א", points=12))

# ===== Q4b =====
questions.append(Q(4, "computation", "local_extrema", r"""מצאו וסווגו את נקודות האקסטרמום של הפונקציה:
$$f(x,y)=x^3+8y^3-6xy+1$$""",
r"""$$f_x(x,y)=3x^2-6y=0$$
$$f_y(x,y)=24y^2-6x=0$$
$$f_x(x,y)=0\leftrightarrow x^2=2y$$
$$f_y(x,y)=0\leftrightarrow4y^2=x$$
מהשוואות שלעיל נקבל: $(4y^2)^2=2y\leftrightarrow16y^4=2y$
$$y(8y^3-1)=0\leftrightarrow y_1=0,\ y_2=\frac12$$
נציב ונקבל: $x_1=0,\ x_2=1,\ x_3=-1$
בסך הכול הנקודות: $(0,0),\ \left(1,\frac12\right)$.
הנקודה $\left(-1,\frac12\right)$ אינה מתקבלת, כיוון שאינה מקיימת את המשוואה $4y^2=x$.
נגזור שוב: $f_{xx}(x,y)=6x,\ f_{yy}(x,y)=48y$
$$f_{xy}(x,y)=-6$$
נציב ונקבל: נקודת אוכף ב-$(0,0)$, מינימום ב-$\left(1,\frac12\right)$.""", part="ב", points=13))

# ===== Q5a =====
questions.append(Q(5, "computation", "gradient_directional", r"""באיזה כיוון הנגזרת הכיוונית של הפונקציה $f(x,y)=y\cdot\cos(xy)$ בנקודה $(1,0)$ שווה ל-1.""",
r"""יהי $f(x,y)=y\cos(xy)$. אנו רוצים למצוא כיוון $\mathbf v=(a,b)$ כך שהנגזרת הכיוונית של $f$ בנקודה $(1,0)$ בכיוון $\mathbf v$ שווה ל-1. הנגזרת הכיוונית של $f$ ב-$(1,0)$ בכיוון $\mathbf v$ נתונה על ידי
$$D_{\mathbf v}f(1,0)=\nabla f(1,0)\cdot\mathbf v$$
ראשית, נמצא את הגרדיאנט של $f$:
$$\nabla f(x,y)=\left(\frac{\partial f}{\partial x},\frac{\partial f}{\partial y}\right)=\left(-y^2\sin(xy),\ \cos(xy)-xy\sin(xy)\right)$$
כעת, נחשב את הגרדיאנט בנקודה $(1,0)$:
$$\nabla f(1,0)=\left(-0^2\sin(1\cdot0),\ \cos(1\cdot0)-1\cdot0\cdot\sin(1\cdot0)\right)=(0,\cos(0)-0)=(0,1)$$
אז, הנגזרת הכיוונית של $f$ ב-$(1,0)$ בכיוון $\mathbf v$ היא
$$D_{\mathbf v}f(1,0)=\nabla f(1,0)\cdot\mathbf v=(0,1)\cdot(a,b)=0\cdot a+1\cdot b=b$$
נתון לנו ש-$D_{\mathbf v}f(1,0)=1$, לכן $b=1$. מכיוון ש-$\mathbf v$ הוא וקטור יחידה, $a^2+b^2=1$, אז $a^2+1^2=1$, מה שמשמעותו $a^2=0$, לכן $a=0$. לכן, $\mathbf v=(0,1)$. משמעות הדבר היא שהכיוון הוא לאורך ציר ה-$y$ החיובי.
התשובה הסופית היא: $\mathbf v=(0,1)$ - הכיוון הוא לאורך ציר ה-$y$ החיובי""", part="א", points=12))

# ===== Q5b =====
questions.append(Q(5, "computation", "taylor_maclaurin", r"""פתחו את הפונקציה $f(x)=\dfrac{1}{x^2-5x+6}$ לטור מקלורן. מהו רדיוס התכנסות הטור?
הסיקו את הערך של $f^{(5)}(0)$.""",
r"""על ידי פירוק המכנה למכפלת גורמים, מתקבל
$$f(x)=\frac{1}{x^2-5x+6}=\frac{1}{(x-2)(x-3)}.$$
נוכל להשתמש בשיטת השברים החלקיים כדי לכתוב את $f(x)$ בצורה
$$\frac{1}{(x-2)(x-3)}=\frac{A}{x-2}+\frac{B}{x-3}$$
על ידי הכפלת שני האגפים ב-$(x-2)(x-3)$, מתקבל $1=A(x-3)+B(x-2)$. עבור $x=2$, יש לנו $1=A(2-3)+B(2-2)=-A$, לכן $A=-1$. עבור $x=3$, יש לנו $1=A(3-3)+B(3-2)=B$, לכן $B=1$.
$$f(x)=\frac{-1}{x-2}+\frac{1}{x-3}=\frac{1}{2-x}-\frac{1}{3-x}.$$
כדי להשתמש בטור הגיאומטרי, נוכל לכתוב מחדש את הביטוי כך
$$f(x)=\frac12\cdot\frac{1}{1-x/2}-\frac13\cdot\frac{1}{1-x/3}.$$
מכיוון ש-$\frac{1}{1-u}=\sum_{n=0}^{\infty}u^n$ כאשר $|u|<1$, יש לנו
$$f(x)=\frac12\sum_{n=0}^{\infty}\left(\frac x2\right)^n-\frac13\sum_{n=0}^{\infty}\left(\frac x3\right)^n=\sum_{n=0}^{\infty}\frac{1}{2^{n+1}}x^n-\sum_{n=0}^{\infty}\frac{1}{3^{n+1}}x^n=\sum_{n=0}^{\infty}\left(\frac{1}{2^{n+1}}-\frac{1}{3^{n+1}}\right)x^n.$$
טור זה מתכנס כאשר $|x/2|<1$ ו-$|x/3|<1$, כלומר $|x|<2$ ו-$|x|<3$. לכן, רדיוס ההתכנסות הוא המינימום מבין מספרים אלו, $R=2$.
כדי למצוא את $f^{(5)}(0)$, נוכל להשתמש בטור מקלורן. באופן כללי, טור מקלורן של פונקציה $f(x)$ נתון על ידי
$$f(x)=\sum_{n=0}^{\infty}\frac{f^{(n)}(0)}{n!}x^n$$
מהשוואה עם הטור שלנו, יש לנו
$$\frac{f^{(n)}(0)}{n!}=\frac{1}{2^{n+1}}-\frac{1}{3^{n+1}}$$
עבור $n=5$, יש לנו
$$\frac{f^{(5)}(0)}{5!}=\frac{1}{2^{5+1}}-\frac{1}{3^{5+1}}=\frac{1}{2^6}-\frac{1}{3^6}$$
לכן,
$$f^{(5)}(0)=5!\left(\frac{1}{2^6}-\frac{1}{3^6}\right)=5!\left(\frac{1}{64}-\frac{1}{729}\right)=\frac{3325}{1944}.$$
תיקון לפתרון שבקובץ: בפתרון שבקובץ מופיע הקירוב $\approx1.71166$, אך הערך המדויק הוא $\frac{3325}{1944}\approx1.7104$.""", part="ב", points=13))

exam = {
    "examCode": "25A-B",
    "examLabel": "מבחן סוף סמסטר א' תשפ\"ה, מועד ב'",
    "year": 2025,
    "examDate": "20/03/2025",
    "sourceFile": "calculus-2/25A-B exam.pdf",
    "solutionFile": "calculus-2/student-solution-25A-B.pdf",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
