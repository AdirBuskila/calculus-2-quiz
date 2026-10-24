# -*- coding: utf-8 -*-
"""Generator for tools/raw/23A-C.json -- calculus-2 (20252), semester A 2023, moed C (27/04/2023).
Run: PYTHONUTF8=1 py -W error::SyntaxWarning tools/gen/gen_23A-C.py

Source: exam 27.4.23 (3 pages, 5 questions of 25 points, a=12, b=13, solve 4 of 5).
There is NO key for this sitting. All 10 items were solved by the solver (solutionSource "solved", official False),
pending the blind refuter. Header (lecturer names) is not transcribed. Text layers are garbled; everything is
transcribed from page renders.

Transcription notes
- Q1b: the printed question asks by what factor the rate of change in the direction u is smaller than the maximal rate.
- Q2a asks for two series in one part; stored as one item. arctan^n means the n-th power of arctan.
- Q4b: the region is the part of the unit disk in the first quadrant lying between y=0 and y=sqrt(3)x.

Checks: tools/verify/23A-C/solve_23A-C.py (sympy + numeric, every computation below) and
tools/verify/23A-C/check.py (geometry; writes regions.json and contours.json).
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "23A-C.json"


def Q(num, part, kind, topic, question, solution, points):
    return {"num": num, "part": part, "kind": kind, "topic": topic, "points": points, "question": question,
            "solution": solution.strip("\n"), "solutionSource": "solved", "official": False, "confidence": "high"}


questions = []

# ===== Q1a =====
questions.append(Q(1, "א", "computation", "double_integrals",
"מצאו שטח של צורה מישורית המוגבלת בין שני המעגלים:\n$$x^2+y^2=2x,\\quad x^2+y^2=4x$$",
r"""נשלים לריבוע:
$$x^2+y^2=2x\iff(x-1)^2+y^2=1,\qquad x^2+y^2=4x\iff(x-2)^2+y^2=4.$$
המעגל הראשון (מרכז $(1,0)$, רדיוס $1$) נמצא בתוך המעגל השני (מרכז $(2,0)$, רדיוס $2$), ושניהם משיקים בראשית. הצורה היא התחום שבין שני המעגלים.
נעבור לקואורדינטות קוטביות $x=r\cos\theta,\ y=r\sin\theta$:
$$r^2=2r\cos\theta\Rightarrow r=2\cos\theta,\qquad r^2=4r\cos\theta\Rightarrow r=4\cos\theta,$$
והתחום הוא $-\frac{\pi}{2}\le\theta\le\frac{\pi}{2},\ 2\cos\theta\le r\le4\cos\theta$. היעקוביאן הוא $r$, ולכן
$$S=\int_{-\pi/2}^{\pi/2}\int_{2\cos\theta}^{4\cos\theta}r\,dr\,d\theta=\int_{-\pi/2}^{\pi/2}\frac{16\cos^2\theta-4\cos^2\theta}{2}\,d\theta=6\int_{-\pi/2}^{\pi/2}\cos^2\theta\,d\theta$$
$$=6\int_{-\pi/2}^{\pi/2}\frac{1+\cos2\theta}{2}\,d\theta=6\cdot\frac{\pi}{2}=3\pi.$$
בדיקה: שטח העיגול הגדול פחות שטח העיגול הקטן הוא $4\pi-\pi=3\pi$.""", 12))

# ===== Q1b =====
questions.append(Q(1, "ב", "computation", "gradient_directional",
r"""נתונה הפונקציה $f(x,y,z)=x^2y\sqrt{z}$. פי כמה קצב שינוי הפונקציה בנקודה $(2,1,1)$ בכיוון של הוקטור $\vec u=\vec i+2\vec j+2\vec k$ קטן מקצב השינוי המקסימלי של הפונקציה בנקודה זו?""",
r"""הנגזרות החלקיות:
$$f_x=2xy\sqrt z,\qquad f_y=x^2\sqrt z,\qquad f_z=\frac{x^2y}{2\sqrt z}.$$
בנקודה $(2,1,1)$:
$$\nabla f(2,1,1)=(4,4,2).$$
קצב השינוי המקסימלי הוא אורך הגרדיאנט:
$$|\nabla f(2,1,1)|=\sqrt{16+16+4}=6.$$
וקטור היחידה בכיוון $\vec u$: $|\vec u|=\sqrt{1+4+4}=3$, ולכן $\hat u=\left(\frac13,\frac23,\frac23\right)$. הנגזרת הכיוונית:
$$D_{\hat u}f(2,1,1)=\nabla f\cdot\hat u=\frac{4+8+4}{3}=\frac{16}{3}.$$
היחס:
$$\frac{|\nabla f|}{D_{\hat u}f}=\frac{6}{16/3}=\frac{18}{16}=\frac98.$$
קצב השינוי בכיוון $\vec u$ קטן פי $\frac98$ מקצב השינוי המקסימלי.""", 13))

# ===== Q2a =====
questions.append(Q(2, "א", "computation", "numeric_series",
r"""בדקו התכנסות בהחלט, בתנאי או התבדרות של הטורים הבאים:
$$\sum_{n=1}^{\infty}\frac{2^n\cos n}{3^n}$$
$$\sum_{n=1}^{\infty}\arctan^n\!\left(\frac{n+2}{n+3}\right)$$""",
r"""**הטור הראשון.** נכתוב $\frac{2^n\cos n}{3^n}=\left(\frac23\right)^n\cos n$. מתקיים
$$\left|\left(\frac23\right)^n\cos n\right|\le\left(\frac23\right)^n,$$
ו-$\sum_{n=1}^{\infty}\left(\frac23\right)^n$ הוא טור הנדסי עם מנה $\frac23<1$, ולכן מתכנס. לפי מבחן ההשוואה $\sum\left|\frac{2^n\cos n}{3^n}\right|$ מתכנס, כלומר הטור מתכנס בהחלט.

**הטור השני.** לכל $n\ge1$ מתקיים $0<\frac{n+2}{n+3}<1$, ולכן $0<\arctan\left(\frac{n+2}{n+3}\right)<\frac{\pi}{4}$ והאיברים חיוביים. נשתמש במבחן השורש (קושי):
$$\sqrt[n]{a_n}=\arctan\left(\frac{n+2}{n+3}\right)\xrightarrow[n\to\infty]{}\arctan1=\frac{\pi}{4}<1.$$
לכן הטור מתכנס, ומכיוון שאיבריו חיוביים הוא מתכנס בהחלט.""", 12))

# ===== Q2b =====
questions.append(Q(2, "ב", "computation", "partials_differentiability",
r"""נתונה הפונקציה
$$f(x,y)=\begin{cases}\dfrac{x^3+y^3}{2x^2+y^2}, & (x,y)\neq(0,0)\\[2mm] 0, & (x,y)=(0,0)\end{cases}$$
האם $f(x,y)$ דיפרנציאבילית ב-$(0,0)$?""",
r"""**נגזרות חלקיות בראשית (לפי ההגדרה).**
$$f_x(0,0)=\lim_{h\to0}\frac{f(h,0)-f(0,0)}{h}=\lim_{h\to0}\frac{h^3/(2h^2)}{h}=\frac12,$$
$$f_y(0,0)=\lim_{h\to0}\frac{f(0,h)-f(0,0)}{h}=\lim_{h\to0}\frac{h^3/h^2}{h}=1.$$
**תנאי הדיפרנציאביליות.** $f$ דיפרנציאבילית ב-$(0,0)$ אם ורק אם
$$\lim_{(x,y)\to(0,0)}\frac{f(x,y)-f(0,0)-\frac12x-y}{\sqrt{x^2+y^2}}=0.$$
נחשב את המונה:
$$\frac{x^3+y^3}{2x^2+y^2}-\frac x2-y=\frac{2x^3+2y^3-x(2x^2+y^2)-2y(2x^2+y^2)}{2(2x^2+y^2)}=\frac{-xy(4x+y)}{2(2x^2+y^2)}.$$
לכן יש לבדוק את
$$\lim_{(x,y)\to(0,0)}\frac{-xy(4x+y)}{2(2x^2+y^2)\sqrt{x^2+y^2}}.$$
לאורך $y=0$ הביטוי שווה ל-$0$, והגבול $0$.
לאורך $y=x$ עם $x>0$:
$$\frac{-x^2\cdot5x}{2\cdot3x^2\cdot\sqrt2\,x}=-\frac{5}{6\sqrt2}\neq0.$$
קיבלנו שני גבולות שונים לאורך שני מסלולים, ולכן הגבול אינו קיים (ובפרט אינו $0$).
**מסקנה:** $f$ אינה דיפרנציאבילית ב-$(0,0)$ (אף על פי שהיא רציפה שם ויש לה נגזרות חלקיות).""", 13))

# ===== Q3a =====
questions.append(Q(3, "א", "computation", "power_series",
r"""עבור אילו ערכי $x$ הטור מתכנס (מצאו רדיוס התכנסות ותחום התכנסות):
$$\sum_{n=1}^{\infty}x^n\,\frac{1}{2^n+3^n}$$""",
r"""**רדיוס ההתכנסות.** $a_n=\frac{1}{2^n+3^n}$. לפי נוסחת קושי-הדמר:
$$\frac1R=\lim_{n\to\infty}\sqrt[n]{|a_n|}=\lim_{n\to\infty}\frac{1}{\sqrt[n]{2^n+3^n}}=\lim_{n\to\infty}\frac{1}{3\sqrt[n]{1+\left(\frac23\right)^n}}=\frac13,$$
ולכן $R=3$: הטור מתכנס בהחלט עבור $|x|<3$ ומתבדר עבור $|x|>3$.

**קצוות.**
* $x=3$: האיבר הכללי $\frac{3^n}{2^n+3^n}=\frac{1}{1+\left(\frac23\right)^n}\to1\neq0$, ולכן הטור מתבדר (התנאי ההכרחי אינו מתקיים).
* $x=-3$: האיבר הכללי $(-1)^n\frac{3^n}{2^n+3^n}$, והערך המוחלט שלו שואף ל-$1$, ולכן הוא אינו שואף ל-$0$ והטור מתבדר.

**תחום ההתכנסות:** $(-3,3)$.""", 12))

# ===== Q3b =====
questions.append(Q(3, "ב", "proof", "chain_rule_identity",
r"""הראו כי הפונקציה $z=y\cdot g\left(x^2-y^2\right)$ כאשר $g(t)$ גזירה עבור כל $t$ ו-$x,y\neq0$ מקיימת את המשוואה:
$$\frac{1}{x}\cdot\frac{\partial z}{\partial x}+\frac{1}{y}\cdot\frac{\partial z}{\partial y}=\frac{z}{y^2}.$$""",
r"""נסמן $t=x^2-y^2$, כך ש-$z=y\,g(t)$, $\frac{\partial t}{\partial x}=2x$ ו-$\frac{\partial t}{\partial y}=-2y$.
לפי כלל השרשרת:
$$\frac{\partial z}{\partial x}=y\cdot\frac{dg}{dt}\cdot\frac{\partial t}{\partial x}=2xy\,g'(t),$$
$$\frac{\partial z}{\partial y}=g(t)+y\cdot\frac{dg}{dt}\cdot\frac{\partial t}{\partial y}=g(t)-2y^2g'(t).$$
נציב באגף שמאל (מותר לחלק כי $x,y\neq0$):
$$\frac1x\cdot2xy\,g'(t)+\frac1y\left(g(t)-2y^2g'(t)\right)=2y\,g'(t)+\frac{g(t)}{y}-2y\,g'(t)=\frac{g(t)}{y}.$$
מצד שני
$$\frac{z}{y^2}=\frac{y\,g(t)}{y^2}=\frac{g(t)}{y}.$$
שני האגפים שווים, כנדרש.""", 13))

# ===== Q4a =====
questions.append(Q(4, "א", "computation", "double_integrals",
r"""החליפו את סדר האינטגרציה באינטגרל
$$\int_{-4}^{0}dx\int_{0}^{\sqrt{x+4}}f(x,y)\,dy+\int_{0}^{2}dx\int_{0}^{2-x}f(x,y)\,dy$$""",
r"""**תיאור התחום.** האינטגרל הראשון: $-4\le x\le0,\ 0\le y\le\sqrt{x+4}$ (מתחת לחצי העליון של הפרבולה $y^2=x+4$). האינטגרל השני: $0\le x\le2,\ 0\le y\le2-x$ (מתחת לישר $x+y=2$). שני החלקים נפגשים בנקודה $(0,2)$, כי $\sqrt{0+4}=2=2-0$. האיחוד הוא תחום אחד עם הקודקודים $(-4,0)$, $(2,0)$, $(0,2)$, החסום מלמטה על ידי $y=0$, משמאל על ידי הפרבולה ומימין על ידי הישר.
**בסדר ההפוך.** עבור $y$ קבוע בין $0$ ל-$2$:
* הגבול השמאלי הוא הפרבולה: $y=\sqrt{x+4}\iff x=y^2-4$ (עבור $y\ge0$);
* הגבול הימני הוא הישר: $y=2-x\iff x=2-y$.

לכן
$$\int_{-4}^{0}dx\int_{0}^{\sqrt{x+4}}f\,dy+\int_{0}^{2}dx\int_{0}^{2-x}f\,dy=\int_{0}^{2}dy\int_{y^2-4}^{2-y}f(x,y)\,dx.$$
בדיקה עם $f\equiv1$: בשני הסדרים השטח הוא $\frac{16}{3}+2=\int_0^2\left(6-y-y^2\right)dy=\frac{22}{3}$.""", 12))

# ===== Q4b =====
questions.append(Q(4, "ב", "computation", "absolute_extrema",
r"""מצאו אקסטרמומים מוחלטים של הפונקציה $f(x,y)=x^2+y^2+4xy$ בתחום המוגבל ע"י $x^2+y^2=1,\ \ y=0,\ \ y=\sqrt{3}x$ ברביע הראשון $(x\ge0,\ y\ge0)$.""",
r"""התחום $D$ הוא גזרה של עיגול היחידה: $0\le\theta\le\frac{\pi}{3},\ 0\le r\le1$. הוא סגור וחסום ו-$f$ רציפה, ולכן לפי ויירשטראס יש לה מקסימום ומינימום מוחלטים ב-$D$. קודקודי התחום: $(0,0)$, $(1,0)$, $\left(\frac12,\frac{\sqrt3}{2}\right)$.

**פנים התחום.**
$$f_x=2x+4y=0,\qquad f_y=2y+4x=0\ \Rightarrow\ (x,y)=(0,0),$$
וזה קודקוד של התחום ולא נקודה פנימית. אין נקודות קריטיות בפנים.

**השפה.**
* הקטע $y=0,\ 0\le x\le1$: $f=x^2$, עולה. ערכים: $f(0,0)=0$, $f(1,0)=1$.
* הקטע $y=\sqrt3x,\ 0\le x\le\frac12$: $f=x^2+3x^2+4\sqrt3x^2=\left(4+4\sqrt3\right)x^2$, עולה. ערכים: $0$ ו-$f\left(\frac12,\frac{\sqrt3}{2}\right)=1+\sqrt3$.
* הקשת $x=\cos\theta,\ y=\sin\theta,\ 0\le\theta\le\frac{\pi}{3}$:
$$f=1+4\sin\theta\cos\theta=1+2\sin2\theta,\qquad \frac{df}{d\theta}=4\cos2\theta=0\Rightarrow\theta=\frac{\pi}{4}.$$
נקבל את הנקודה $\left(\frac{1}{\sqrt2},\frac{1}{\sqrt2}\right)$ עם $f=1+2=3$. (בשיטת לגראנז' $\nabla f=\lambda\nabla(x^2+y^2)$ עם $x^2+y^2=1$ מתקבלים $y=\pm x$, והנקודה היחידה בגזרה היא אותה נקודה.)

**השוואת ערכים:**
$$f(0,0)=0,\quad f(1,0)=1,\quad f\left(\tfrac12,\tfrac{\sqrt3}{2}\right)=1+\sqrt3\approx2.73,\quad f\left(\tfrac{1}{\sqrt2},\tfrac{1}{\sqrt2}\right)=3.$$
**מסקנה:** המקסימום המוחלט הוא $3$ בנקודה $\left(\frac{1}{\sqrt2},\frac{1}{\sqrt2}\right)$, והמינימום המוחלט הוא $0$ בנקודה $(0,0)$.""", 13))

# ===== Q5a =====
questions.append(Q(5, "א", "computation", "local_extrema",
r"""מצאו וסווגו את נקודות האקסטרמום של הפונקציה:
$$f(x,y)=\left(x^2-2y^2\right)e^{x-y}$$""",
r"""**נקודות קריטיות.**
$$f_x=\left(x^2+2x-2y^2\right)e^{x-y},\qquad f_y=\left(-x^2-4y+2y^2\right)e^{x-y}.$$
מכיוון ש-$e^{x-y}>0$, יש לפתור
$$\begin{cases}x^2+2x-2y^2=0&\text{(I)}\\-x^2-4y+2y^2=0&\text{(II)}\end{cases}$$
חיבור (I) ו-(II) נותן $2x-4y=0$, כלומר $x=2y$. נציב ב-(I): $4y^2+4y-2y^2=2y(y+2)=0$, ולכן $y=0$ או $y=-2$.
הנקודות הקריטיות: $(0,0)$ ו-$(-4,-2)$.

**נגזרות שניות.**
$$f_{xx}=\left(x^2+4x+2-2y^2\right)e^{x-y},\quad f_{yy}=\left(x^2-2y^2+8y-4\right)e^{x-y},\quad f_{xy}=\left(2y^2-x^2-2x-4y\right)e^{x-y}.$$
* הנקודה $(0,0)$: $f_{xx}=2,\ f_{yy}=-4,\ f_{xy}=0$, ולכן $D=2\cdot(-4)-0=-8<0$: **נקודת אוכף**.
* הנקודה $(-4,-2)$: $e^{x-y}=e^{-2}$ ו-
$$f_{xx}=-6e^{-2},\quad f_{yy}=-12e^{-2},\quad f_{xy}=8e^{-2},$$
$$D=(-6)(-12)e^{-4}-64e^{-4}=8e^{-4}>0,\qquad f_{xx}<0,$$
ולכן זו **נקודת מקסימום מקומי**, עם $f(-4,-2)=(16-8)e^{-2}=\frac{8}{e^2}$.""", 12))

# ===== Q5b =====
questions.append(Q(5, "ב", "computation", "taylor_maclaurin",
r"""פתחו את הפונקציה $f(x)=\dfrac{1}{x^2+x-2}$ לטור מקלורן. מהו תחום התכנסות הטור?
הסיקו את הערך של $f^{(10)}(0)$.""",
r"""**פירוק לשברים חלקיים.** $x^2+x-2=(x-1)(x+2)$, ולכן
$$\frac{1}{x^2+x-2}=\frac13\left(\frac{1}{x-1}-\frac{1}{x+2}\right).$$
**פיתוח כל שבר** בעזרת הטור ההנדסי:
$$\frac{1}{x-1}=-\frac{1}{1-x}=-\sum_{n=0}^{\infty}x^n,\qquad|x|<1;$$
$$\frac{1}{x+2}=\frac12\cdot\frac{1}{1+\frac x2}=\frac12\sum_{n=0}^{\infty}(-1)^n\frac{x^n}{2^n}=\sum_{n=0}^{\infty}\frac{(-1)^n}{2^{n+1}}x^n,\qquad|x|<2.$$
לכן
$$f(x)=-\frac13\sum_{n=0}^{\infty}\left(1+\frac{(-1)^n}{2^{n+1}}\right)x^n.$$
**תחום ההתכנסות.** שני הטורים מתכנסים יחד עבור $|x|<1$. עבור $1\le|x|<2$ הטור השני מתכנס והראשון מתבדר, ולכן הסכום מתבדר. בקצוות $x=\pm1$ הערך המוחלט של האיבר הכללי שואף ל-$\frac13\neq0$, ולכן הטור מתבדר. תחום ההתכנסות: $(-1,1)$.

**הנגזרת העשירית.** מקדם $x^{n}$ בטור מקלורן הוא $\frac{f^{(n)}(0)}{n!}$. עבור $n=10$:
$$\frac{f^{(10)}(0)}{10!}=-\frac13\left(1+\frac{1}{2^{11}}\right)=-\frac{2049}{6144},$$
$$f^{(10)}(0)=-\frac{10!}{3}\left(1+\frac{1}{2^{11}}\right)=-\frac{10!\cdot2049}{3\cdot2^{11}}=-\frac{9681525}{8}=-1210190.625.$$""", 13))

exam = {
    "examCode": "23A-C",
    "examLabel": "מבחן סוף סמסטר א' תשפ\"ג, מועד ג'",
    "year": 2023,
    "examDate": "27/04/2023",
    "sourceFile": "calculus-2/23A-C exam 27.4.23.pdf",
    "solutionFile": "none (no key exists for this sitting; solved, pending refuter)",
    "questions": questions,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(exam, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"wrote {OUT.name}: {len(questions)} questions")
