/* double_int, level 4 - choosing the easier order of integration */
COURSE_LEVEL("double_int", {
  id: "C04", order: 4, icon: "🧠", title: "בוחרים את הסדר הקל",
  goal: "לזהות אינטגרנד שאין לו פונקציה קדומה אלמנטרית בסדר הנתון, להחליף סדר ולחשב.",
  source: "ai-verified",
  lesson: { html: String.raw`
<p>שני הסדרים נותנים אותו ערך, אבל לא באותה קלות. הפונקציות $e^{x^2}$, $\sin(x^2)$, $\cos(x^2)$ ו-$\dfrac{\sin x}{x}$ <b>אין להן פונקציה קדומה אלמנטרית</b>, ולכן אי אפשר לאנטגרל אותן לפי המשתנה שלהן.</p>
<div class="lesson-rule">🔑 <b>כלל האצבע:</b> אם האינטגרנד הוא פונקציה "בעייתית" של משתנה אחד (למשל $e^{x^2}$), סדרו שהאינטגרל <b>הפנימי</b> יהיה לפי המשתנה השני. אז האינטגרנד קבוע בפנימי, והפנימי רק מכפיל אותו באורך הפס.</div>
<div class="lesson-ex">דוגמה: $\int_0^1\int_y^1 e^{x^2}\,dx\,dy$. הפנימי לפי $x$ בלתי אפשרי. התחום הוא $0\le y\le x\le1$, ובסדר ההפוך
$$\int_0^1\int_0^{x}e^{x^2}\,dy\,dx=\int_0^1xe^{x^2}\,dx=\left[\tfrac{e^{x^2}}{2}\right]_0^1=\tfrac{e-1}{2}.$$
אחרי החילוף נשאר $xe^{x^2}$, שיש לו פונקציה קדומה פשוטה (הצבה $t=x^2$).</div>
<div class="region-fig" data-region='{"inequalities":["x>=y","y>=0","1>=x"],"boundary_curves":["y=x","y=0","x=1"],"orderXY":{"x":[0,1],"y":[0,"x"]},"orderYX":{"y":[0,1],"x":["y",1]},"vertices":[[0,0],[1,0],[1,1]],"integrand":"exp(x^2)","value":"(e-1)/2"}'></div>
<p>עוד דוגמה: $\int_0^\pi\int_x^\pi \dfrac{\sin y}{y}\,dy\,dx$. התחום $0\le x\le y\le\pi$ ובסדר ההפוך $\int_0^\pi\int_0^{y}\dfrac{\sin y}{y}\,dx\,dy=\int_0^\pi\sin y\,dy=2$. האינטגרל הפנימי לפי $x$ נותן את הגורם $y$, והוא מצמצם את המכנה.</p>
<div class="lesson-trap">⚠️ החילוף הוא על התחום, לא על האינטגרנד. אל תחליפו רק את האותיות $dx\,dy$ והגבולות; שרטטו, וקראו את הגבולות החדשים מהציור.</div>
` },
  questions: [
    { id: "C04-Q1", question: String.raw`נתון $\int_0^1\int_y^1 e^{x^2}\,dx\,dy$. מה נכון לעשות?`,
      options: [
        { id: "a", value: String.raw`לחשב ישירות את הפנימי: $\int e^{x^2}dx$ היא פונקציה אלמנטרית` },
        { id: "b", value: String.raw`להחליף סדר ל-$\int_0^1\int_0^{y}e^{x^2}\,dx\,dy$` },
        { id: "c", value: "לוותר, כי אי אפשר לחשב את האינטגרל" },
        { id: "d", value: String.raw`להחליף סדר ל-$\int_0^1\int_0^{x}e^{x^2}\,dy\,dx$` },
      ],
      correctId: "d",
      explanation: String.raw`התחום $0\le y\le x\le1$ נקרא בסדר ההפוך כ-$0\le x\le1$, $0\le y\le x$, ואז הפנימי לפי $y$ הוא $xe^{x^2}$, שקל לאנטגרל. $\int e^{x^2}dx$ אינה אלמנטרית. האפשרות עם $\int_0^{y}e^{x^2}dx$ שוב מאנטגרלת את $e^{x^2}$ לפי $x$ (וגם גבולותיה מתארים תחום אחר). והאינטגרל כן ניתן לחישוב, בדיוק בעזרת החילוף.`,
      recap: "מחליפים כך שהפנימי יהיה לפי המשתנה שאינו בתוך הפונקציה הבעייתית." },
    { id: "C04-Q2",
      step: { type: "numeric", prompt: String.raw`חשבו את $\int_0^2\int_{y/2}^{1} e^{x^2}\,dx\,dy$ (רמז: שרטטו, והחליפו סדר). ענו כמספר עשרוני.`,
              answer: 1.71828, tol: 0.005,
              explain: String.raw`התחום: $0\le y\le2$ ו-$\tfrac y2\le x\le1$, כלומר $0\le x\le1$ ו-$0\le y\le2x$. לכן $\int_0^1\int_0^{2x}e^{x^2}\,dy\,dx=\int_0^1 2xe^{x^2}\,dx=\left[e^{x^2}\right]_0^1=e-1\approx1.718$.` },
      recap: "אחרי החילוף הפנימי נותן אורך פס: $2x$." },
    { id: "C04-Q3",
      step: { type: "numeric", prompt: String.raw`חשבו את $\int_0^\pi\int_x^\pi \dfrac{\sin y}{y}\,dy\,dx$ (הפנימי לפי $y$ בלתי אפשרי). ענו כמספר.`,
              answer: 2, tol: 0,
              explain: String.raw`התחום $0\le x\le y\le\pi$ נקרא כ-$0\le y\le\pi$, $0\le x\le y$. הפנימי לפי $x$ הוא $\int_0^{y}\tfrac{\sin y}{y}\,dx=\sin y$, ואז $\int_0^\pi\sin y\,dy=2$.` },
      recap: "הפס מכפיל ב-$y$ ומבטל את המכנה." },
    { id: "C04-Q4",
      step: { type: "order", prompt: String.raw`סדרו את שלבי החישוב של $\int_0^1\int_x^{1} e^{y^2}\,dy\,dx$.`,
              lines: [
                String.raw`התחום הוא $0\le x\le y\le1$`,
                String.raw`מחליפים סדר: $\int_0^1\int_0^{y}e^{y^2}\,dx\,dy$`,
                String.raw`הפנימי: $\int_0^{y}e^{y^2}\,dx=ye^{y^2}$`,
                String.raw`$\int_0^1ye^{y^2}\,dy=\left[\tfrac{e^{y^2}}{2}\right]_0^1$`,
                String.raw`$=\tfrac{e-1}{2}$`,
              ],
              explain: String.raw`קוראים את התחום, מחליפים סדר, מחשבים את הפנימי (כאן $e^{y^2}$ קבוע ביחס ל-$x$), ואז את החיצוני בהצבה $t=y^2$.` },
      recap: "קודם תחום, אחר כך חילוף, אחר כך פנימי וחיצוני." },
    { id: "C04-Q5",
      step: { type: "numeric", prompt: String.raw`חשבו את $\int_0^1\int_x^{1} \sin\left(y^2\right)\,dy\,dx$. ענו כמספר עשרוני.`,
              answer: 0.22985, tol: 0.001,
              explain: String.raw`התחום $0\le x\le y\le1$. בסדר ההפוך $\int_0^1\int_0^{y}\sin(y^2)\,dx\,dy=\int_0^1y\sin(y^2)\,dy=\tfrac{1-\cos1}{2}\approx0.2298$.` },
      recap: "אותו דפוס: מחליפים כדי שהפנימי יהיה לפי המשתנה שאינו בתוך הסינוס." },
    { id: "C04-Q6", question: "איזה מהאינטגרלים הבאים אפשר לחשב בסדר הנתון, בלי להחליף סדר?",
      options: [
        { id: "a", value: String.raw`$\int_0^1\int_x^{1} e^{y^2}\,dy\,dx$` },
        { id: "b", value: String.raw`$\int_0^1\int_y^{1} \sin\left(x^2\right)\,dx\,dy$` },
        { id: "c", value: String.raw`$\int_0^1\int_0^{x} e^{x^2}\,dy\,dx$` },
        { id: "d", value: String.raw`$\int_0^\pi\int_y^{\pi} \dfrac{\sin x}{x}\,dx\,dy$` },
      ],
      correctId: "c",
      explanation: String.raw`רק באינטגרל $\int_0^1\int_0^{x} e^{x^2}\,dy\,dx$ הפנימי הוא לפי $y$ והאינטגרנד קבוע ביחס אליו (התוצאה $xe^{x^2}$ ניתנת לאינטגרציה). בשלושת האחרים הפנימי מאנטגרל פונקציה בלי פונקציה קדומה אלמנטרית: $e^{y^2}$ לפי $y$, $\sin(x^2)$ לפי $x$, ו-$\tfrac{\sin x}{x}$ לפי $x$.`,
      recap: "בודקים מה הפנימי מאנטגרל: אם זה $e^{t^2}$, $\\sin t^2$ או $\\frac{\\sin t}{t}$, מחליפים." },
  ],
});
