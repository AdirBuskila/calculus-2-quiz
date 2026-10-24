/* chain_rule, level 1 - the dependency tree: intermediate variable, routes, inner derivatives */
COURSE_LEVEL("chain_rule", {
  id: "C01", order: 1, icon: "🌳", title: "עץ התלויות ומשתנה ביניים",
  goal: "לזהות את משתנה הביניים, לצייר מי תלוי במי, ולחשב את הנגזרות החלקיות של הביטוי הפנימי.",
  source: "ai-verified",
  lesson: { html: String.raw`
<p>בשאלות "הראו שהפונקציה מקיימת את המשוואה" מופיעה פונקציה כמו $z=g(xy)$ או $z=y\,g(x^2-y^2)$, כש-$g$ היא פונקציה גזירה <b>כללית</b>: לא נתון מי היא. אי אפשר לפתוח אותה, אבל אפשר לגזור סביבה בעזרת כלל השרשרת. השלב הראשון הוא להבין מי תלוי במי.</p>
<h3>משתנה ביניים</h3>
<p><b>משתנה ביניים</b> הוא הביטוי שנמצא בתוך הסוגריים של $g$. נותנים לו אות חדשה, בדרך כלל $t$, וכותבים את $z$ בעזרתה. ב-$z=g(x^2-y^2)$ נסמן $t=x^2-y^2$ ואז $z=g(t)$.</p>
<h3>עץ התלויות</h3>
<p>$z$ תלוי ב-$t$, ו-$t$ תלוי ב-$x$ וב-$y$. כלומר $z$ מגיע אל $x$ ואל $y$ <b>דרך</b> $t$. כל חץ בעץ הוא נגזרת אחת. הכלל לכל העץ הוא:</p>
<div class="lesson-rule">🔑 <b>כופלים לאורך מסלול, ומחברים בין מסלולים שונים.</b> מסלול אחד מ-$z$ אל $x$ נותן מחובר אחד בנגזרת $z_x$.</div>
<div class="lesson-ex"><b>דוגמה:</b> $z=\dfrac{y}{3x}+g(xy)$ ונסמן $t=xy$. אל $y$ מגיעים שני מסלולים: מסלול ישיר דרך האיבר $\dfrac{y}{3x}$, ומסלול דרך $t$. לכן ב-$z_y$ יהיו שני מחוברים: $z_y=\dfrac1{3x}+g'(t)\cdot x$.</div>
<h3>הצעד הראשון: נגזרות של הביטוי הפנימי</h3>
<p>לפני שמשתמשים בכלל השרשרת מחשבים $t_x$ ו-$t_y$, כמו נגזרות חלקיות רגילות: גוזרים לפי משתנה אחד, והאחר נחשב קבוע. עבור $t=xy$ מקבלים $t_x=y$ ו-$t_y=x$.</p>
<div class="lesson-trap">⚠️ <b>סימנים של $x-y$.</b> ב-$t=\cos(x-y)$ הנגזרת הפנימית של $x-y$ לפי $x$ היא $+1$ ולפי $y$ היא $-1$. לכן $t_x=-\sin(x-y)$ אבל $t_y=+\sin(x-y)$. סימן של נגזרת לפי $y$ הוא <b>הפוך</b> לסימן של הנגזרת לפי $x$.</div>
<div class="lesson-trap">⚠️ <b>לא לשכוח את המסלול הישיר.</b> איבר חופשי שנמצא מחוץ ל-$g$ (כמו $\dfrac{y}{3x}$) נגזר בנפרד ונוסף.</div>
` },
  questions: [
    { id: "C01-Q1",
      question: String.raw`נתון $z=g(x^2-y^2)$ ונסמן $t=x^2-y^2$. מהו $t_y$ ?`,
      options: [
        { id: "a", value: String.raw`$-2y$` },
        { id: "b", value: String.raw`$2y$` },
        { id: "c", value: String.raw`$-2y^2$` },
        { id: "d", value: String.raw`$-2x$` },
      ],
      correctId: "a",
      explanation: String.raw`הנגזרת של $-y^2$ לפי $y$ היא $-2y$ ($x^2$ קבוע ונעלם). הערך $2y$ מאבד את המינוס. $-2y^2$ משאיר חזקה שגויה (הנגזרת של $y^2$ היא $2y$, לא $2y^2$). $-2x$ מערבב את הנגזרת לפי $x$, שהיא $2x$, עם המינוס של $y$.`,
      recap: String.raw`גוזרים לפי המשתנה המבוקש, וכל משתנה אחר הוא קבוע` },
    { id: "C01-Q2",
      question: String.raw`נתון $z=\dfrac{y}{3x}+g(xy)$ ונסמן $t=xy$. כמה מסלולים בעץ התלויות מובילים מ-$z$ אל $y$, כלומר כמה מחוברים יש ב-$z_y$ ?`,
      options: [
        { id: "a", value: String.raw`$2$` },
        { id: "b", value: String.raw`$1$` },
        { id: "c", value: String.raw`$3$` },
        { id: "d", value: String.raw`$0$` },
      ],
      correctId: "a",
      explanation: String.raw`$y$ מופיע באיבר החופשי $\dfrac{y}{3x}$ (מסלול ישיר) ובתוך $t=xy$ (מסלול דרך $g$). שני מסלולים, ולכן $z_y=\dfrac1{3x}+g'(t)\,x$. מסלול אחד היה נכון אילו היה רק אחד מהאיברים. מסלול שלישי אין: $t$ תלוי ב-$y$ פעם אחת. ואפס אי אפשר, כי $y$ בבירור משפיע על $z$.`,
      recap: String.raw`כל מסלול מ-$z$ אל המשתנה נותן מחובר אחד` },
    { id: "C01-Q3",
      step: { type: "numeric", prompt: String.raw`נתון $t=xy^2$. חשבו את $t_y$ בנקודה $(2,3)$.`, answer: 12, tol: 0,
              explain: String.raw`$t_y=2xy$ ובנקודה $(2,3)$ זה $2\cdot2\cdot3=12$. אותו חישוב עם $t_x=y^2$ היה נותן $9$.` },
      recap: String.raw`$t_y$ מחשבים כנגזרת חלקית רגילה, ואז מציבים` },
    { id: "C01-Q4",
      question: String.raw`נתון $z=g\!\left(\dfrac{x}{y}\right)$ ונסמן $t=\dfrac xy$. מהו $t_y$ ?`,
      options: [
        { id: "a", value: String.raw`$-\dfrac{x}{y^2}$` },
        { id: "b", value: String.raw`$\dfrac1y$` },
        { id: "c", value: String.raw`$-\dfrac1y$` },
        { id: "d", value: String.raw`$\dfrac{x}{y^2}$` },
      ],
      correctId: "a",
      explanation: String.raw`$t=x\cdot y^{-1}$, ולכן $t_y=-x\,y^{-2}=-\dfrac{x}{y^2}$. הערך $\dfrac1y$ הוא $t_x$ (הנגזרת לפי המשתנה השני). $-\dfrac1y$ שוכח שה-$x$ נשאר כגורם. $\dfrac{x}{y^2}$ מאבד את המינוס של חזקה $-1$.`,
      recap: String.raw`$\dfrac{x}{y}$ נגזר לפי $y$ כ-$-\dfrac{x}{y^2}$` },
    { id: "C01-Q5",
      question: String.raw`נתון $z=g(t)$ עם $t=\cos(x-y)$. מהו $t_y$ ?`,
      options: [
        { id: "a", value: String.raw`$\sin(x-y)$` },
        { id: "b", value: String.raw`$-\sin(x-y)$` },
        { id: "c", value: String.raw`$\cos(x-y)$` },
        { id: "d", value: String.raw`$-\cos(x-y)$` },
      ],
      correctId: "a",
      explanation: String.raw`הנגזרת של $\cos(w)$ היא $-\sin(w)$, ובנוסף כופלים בנגזרת הפנימית $w_y=-1$ של $w=x-y$. שני המינוסים מתבטלים: $t_y=+\sin(x-y)$. הערך $-\sin(x-y)$ שוכח את הנגזרת הפנימית (זה בדיוק $t_x$). $\cos$ ו-$-\cos$ לא נגזרו בכלל.`,
      recap: String.raw`נגזרת פנימית של $x-y$ לפי $y$ היא $-1$` },
  ],
});
