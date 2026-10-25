/* chain_rule, level 2 - the chain rule with ONE intermediate variable: z = g(t) */
COURSE_LEVEL("chain_rule", {
  id: "C02", order: 2, icon: "🔗", title: "כלל השרשרת: משתנה ביניים אחד",
  goal: "לגזור $z=g(t)$ לפי $x$ ולפי $y$ ולכתוב את התוצאה בלי לטעות בארגומנט של $g'$.",
  source: "ai-verified",
  lesson: { html: String.raw`
<p>אם $z=g(t)$ ו-$t=t(x,y)$, מכפילים את נגזרת $g$ בנגזרת הפנימית, לאורך המסלול בעץ התלויות:</p>
<div class="lesson-formula">$z_x=g'(t)\cdot t_x\qquad\qquad z_y=g'(t)\cdot t_y$</div>
<p>$g'(t)$ היא נגזרת רגילה של $g$ לפי המשתנה היחיד שלה, ולכן זה אותו ביטוי בשתי הנוסחאות. מה שמשתנה בין $z_x$ ל-$z_y$ הוא רק הגורם הפנימי $t_x$ או $t_y$.</p>
<div class="lesson-ex"><b>דוגמה:</b> $z=g(x^2y)$. נסמן $t=x^2y$, אז $t_x=2xy$ ו-$t_y=x^2$. לכן
$$z_x=2xy\;g'(x^2y),\qquad z_y=x^2\;g'(x^2y).$$
בדיקה עם $g=\sin$: $z=\sin(x^2y)$ נותנת $z_x=2xy\cos(x^2y)$, וזה אותו דבר.</div>
<div class="lesson-rule">🔑 <b>הארגומנט של $g'$ נשאר $t$.</b> כותבים $g'(x^2y)$, לא $g'(x)$ ולא $g'(2xy)$. אנחנו לא יודעים מי $g$, ולכן אסור לגעת בארגומנט.</div>
<div class="lesson-trap">⚠️ <b>$g'$ ולא $g$.</b> נגזרת של $g(t)$ היא $g'(t)\cdot t_x$. אם נשאר $g(t)\cdot t_x$ לא גזרתם את $g$ בכלל.</div>
<div class="lesson-trap">⚠️ <b>$g_x$ הוא סימון מטעה.</b> ל-$g$ יש משתנה אחד, ולכן נגזרתה היא $\dfrac{dg}{dt}=g'(t)$. הנגזרת החלקית היא של $z$.</div>
<div class="lesson-rule">🔑 <b>בדיקת שפיות:</b> מכיוון ש-$z_x$ ו-$z_y$ חולקים את אותו $g'(t)$, תמיד מתקיים $z_x\,t_y=z_y\,t_x$.</div>
` },
  questions: [
    { id: "C02-Q1",
      question: String.raw`נתון $z=g(x^2+y^2)$. מהו $z_x$ ?`,
      options: [
        { id: "a", value: String.raw`$2x\,g'(x^2+y^2)$` },
        { id: "b", value: String.raw`$g'(2x)$` },
        { id: "c", value: String.raw`$2x\,g(x^2+y^2)$` },
        { id: "d", value: String.raw`$g'(x^2+y^2)$` },
      ],
      correctId: "a",
      explanation: String.raw`$t=x^2+y^2$ ו-$t_x=2x$, ולכן $z_x=g'(t)\cdot2x$. הערך $g'(2x)$ מחליף את הארגומנט של $g'$ בנגזרת הפנימית. $2x\,g(x^2+y^2)$ לא גזר את $g$. ו-$g'(x^2+y^2)$ שוכח את הגורם הפנימי $2x$.`,
      recap: String.raw`$z_x=g'(t)\cdot t_x$, והארגומנט נשאר $t$` },
    { id: "C02-Q2",
      step: { type: "numeric", prompt: String.raw`תהי $z=g(xy)$ כאשר $g(t)=t^3$. חשבו את $z_x$ בנקודה $(1,2)$.`, answer: 24, tol: 0,
              explain: String.raw`$g'(t)=3t^2$, $t=xy=2$ ו-$t_x=y=2$. לכן $z_x=3\cdot2^2\cdot2=24$. בדיקה: $z=x^3y^3$ ו-$z_x=3x^2y^3=24$.` },
      recap: String.raw`מחשבים $t$, $g'(t)$ ו-$t_x$ בנקודה, וכופלים` },
    { id: "C02-Q3",
      question: String.raw`נתון $z=g\!\left(\dfrac{x}{y}\right)$. מהו $z_y$ ?`,
      options: [
        { id: "a", value: String.raw`$-\dfrac{x}{y^2}\,g'\!\left(\dfrac xy\right)$` },
        { id: "b", value: String.raw`$\dfrac1y\,g'\!\left(\dfrac xy\right)$` },
        { id: "c", value: String.raw`$-\dfrac{x}{y^2}\,g\!\left(\dfrac xy\right)$` },
        { id: "d", value: String.raw`$-\dfrac{x}{y^2}\,g'\!\left(-\dfrac{x}{y^2}\right)$` },
      ],
      correctId: "a",
      explanation: String.raw`$t_y=-\dfrac{x}{y^2}$, ולכן $z_y=g'(t)\,t_y$ עם $t=\dfrac xy$. הערך $\dfrac1y\,g'$ משתמש ב-$t_x$ במקום ב-$t_y$. הערך עם $g$ (בלי גרש) לא גזר את $g$. והערך שבו הארגומנט של $g'$ הוא $-\dfrac{x}{y^2}$ מציב את הנגזרת הפנימית גם בתוך הארגומנט של $g'$, וזה אסור.`,
      recap: String.raw`הארגומנט של $g'$ הוא $t$ עצמו, לא $t_y$` },
    { id: "C02-Q4",
      step: { type: "findbug",
              prompt: String.raw`הפתרון הבא מחשב את $z_x$ ו-$z_y$ עבור $z=g(x^2y)$. באיזו שורה כתוב משהו שאינו נכון לגבי הפונקציה $z$ ?`,
              lines: [
                String.raw`נסמן $t=x^2y$, ולכן $z=g(t)$.`,
                String.raw`$t_x=2xy$ וגם $t_y=x^2$.`,
                String.raw`$z_x=g'(t)\cdot2xy$`,
                String.raw`$z_y=g'(t)\cdot2xy$`,
              ],
              bugIndex: 3,
              explain: String.raw`ב-$z_y$ צריך להכפיל ב-$t_y=x^2$ ולא ב-$t_x=2xy$. הנכון: $z_y=g'(t)\cdot x^2$. זו טעות ה"נגזרת הפנימית של המשתנה השני".` },
      recap: String.raw`$z_y$ משתמש ב-$t_y$, ו-$z_x$ משתמש ב-$t_x$` },
    { id: "C02-Q5",
      step: { type: "numeric", prompt: String.raw`תהי $z=g(x^2-3y)$ כאשר $g(t)=t^2$. חשבו את $z_y$ בנקודה $(2,1)$.`, answer: -6, tol: 0,
              explain: String.raw`$t=x^2-3y=1$, $g'(t)=2t=2$ ו-$t_y=-3$. לכן $z_y=2\cdot(-3)=-6$.` },
      recap: String.raw`לא לשכוח את המינוס שב-$t_y$` },
    { id: "C02-Q6",
      question: String.raw`נתון $z=g(t)$ עם $t=t(x,y)$ כלשהו (ו-$g$ גזירה). איזו משוואה מתקיימת תמיד?`,
      options: [
        { id: "a", value: String.raw`$z_x\,t_y=z_y\,t_x$` },
        { id: "b", value: String.raw`$z_x\,t_x=z_y\,t_y$` },
        { id: "c", value: String.raw`$z_x=z_y$` },
        { id: "d", value: String.raw`$z_x+z_y=g'(t)$` },
      ],
      correctId: "a",
      explanation: String.raw`$z_x\,t_y=g'\,t_x\,t_y$ ו-$z_y\,t_x=g'\,t_y\,t_x$: שניהם שווים. שלוש המשוואות האחרות נכשלות כבר ב-$t=xy$ עם $g=\sin$ (למשל $z_x=y\cos(xy)$ ו-$z_y=x\cos(xy)$ שונים זה מזה).`,
      recap: String.raw`$z_x$ ו-$z_y$ חולקים את אותו $g'(t)$` },
  ],
});
