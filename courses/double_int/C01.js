/* double_int, level 1 - reading a region from the bounds of an iterated integral */
COURSE_LEVEL("double_int", {
  id: "C01", order: 1, icon: "✏️", title: "קוראים תחום מהגבולות",
  goal: "לקרוא מהגבולות של אינטגרל נשנה איזה תחום מדובר, לשרטט אותו, ולחשב אינטגרל נשנה פשוט.",
  source: "ai-verified",
  lesson: { html: String.raw`
<p>אינטגרל כפול $\iint_R f\,dA$ מסכם את הערכים של $f$ על תחום $R$ במישור. את החישוב עושים כ<b>אינטגרל נשנה</b>: קודם אינטגרל פנימי, ואז אינטגרל חיצוני על התוצאה.</p>
<div class="lesson-formula">$$\int_a^b\left(\int_{g_1(x)}^{g_2(x)} f(x,y)\,dy\right)dx$$</div>
<div class="lesson-rule">🔑 הגבולות של האינטגרל <b>החיצוני</b> הם מספרים קבועים. הגבולות של האינטגרל <b>הפנימי</b> יכולים להיות פונקציות של המשתנה החיצוני, ורק שלו.</div>
<p>הגבולות הם אי-שוויונים שמגדירים את התחום. ב-$\int_0^2\int_0^x f\,dy\,dx$ מתקבל $0\le x\le 2$ ו-$0\le y\le x$. כך משרטטים:</p>
<ul>
<li>כותבים את אי-השוויונים: $0\le x\le 2$, $0\le y\le x$;</li>
<li>מציירים כל עקום גבול: $y=0$, $y=x$, $x=2$;</li>
<li>מוצאים את הקודקודים (נקודות החיתוך): $(0,0)$, $(2,0)$, $(2,2)$;</li>
<li>מצלילים את השטח שהעקומים סוגרים.</li>
</ul>
<div class="region-fig" data-region='{"inequalities":["x>=y","y>=0","2>=x"],"boundary_curves":["y=x","y=0","x=2"],"orderXY":{"x":[0,2],"y":[0,"x"]},"orderYX":{"y":[0,2],"x":["y",2]},"vertices":[[0,0],[2,0],[2,2]],"area":"2"}'></div>
<div class="lesson-ex">דוגמה: שטח התחום הזה הוא $\int_0^2\int_0^x 1\,dy\,dx=\int_0^2 x\,dx=2$. האינטגרל הפנימי נותן את אורך הפס, והחיצוני סוכם את האורכים.</div>
<div class="lesson-trap">⚠️ לכל משתנה צריך גבול תחתון וגבול עליון. גבול חיצוני שתלוי במשתנה (כמו $\int_0^{x}\ldots dx$ בחוץ) הוא שגיאה.</div>
` },
  questions: [
    { id: "C01-Q1", question: String.raw`מהו התחום של האינטגרל $\int_0^1\int_{x^2}^{x} f\,dy\,dx$ ?`,
      options: [
        { id: "a", value: String.raw`$0\le x\le 1,\ x\le y\le x^2$` },
        { id: "b", value: String.raw`$0\le x\le 1,\ x^2\le y\le x$` },
        { id: "c", value: String.raw`$0\le x\le 1,\ x^2\le y\le 1$` },
        { id: "d", value: String.raw`$0\le x\le 1,\ 0\le y\le x^2$` },
      ],
      correctId: "b",
      explanation: String.raw`המשתנה החיצוני הוא $x$ ונע מ-$0$ עד $1$, ובתוכו $y$ נע מהגבול התחתון $x^2$ עד העליון $x$. התחום הוא הפס שבין הפרבולה לישר. התיאור שבו הגבולות הפוכים ($x\le y\le x^2$) ריק, כי ב-$(0,1)$ מתקיים $x^2<x$. התיאור עם $y\le 1$ הוא האזור שמעל הפרבולה עד הישר $y=1$, והתיאור עם $0\le y\le x^2$ הוא האזור שמתחת לפרבולה, ושניהם תחומים אחרים.`,
      recap: "האינטגרל החיצוני קובע את הטווח הקבוע, והפנימי את הגבולות שמשתנים." },
    { id: "C01-Q2",
      step: { type: "numeric", prompt: String.raw`חשבו את $\int_0^2\int_0^x 1\,dy\,dx$, כלומר את שטח התחום $0\le y\le x\le 2$. ענו כמספר.`,
              answer: 2, tol: 0,
              explain: String.raw`האינטגרל הפנימי $\int_0^x 1\,dy=x$, והחיצוני $\int_0^2 x\,dx=\left[\tfrac{x^2}{2}\right]_0^2=2$. זה גם שטח משולש ישר-זווית עם ניצבים באורך $2$: $\tfrac12\cdot2\cdot2=2$.` },
      recap: "אינטגרל של 1 על תחום הוא השטח שלו." },
    { id: "C01-Q3",
      step: { type: "numeric", prompt: String.raw`חשבו את $\int_0^2\int_0^3 xy\,dy\,dx$ (תחום מלבני). ענו כמספר.`,
              answer: 9, tol: 0,
              explain: String.raw`בתחום מלבני עם אינטגרנד מכפלה אפשר להפריד: $\int_0^2 x\,dx\cdot\int_0^3 y\,dy=2\cdot\tfrac92=9$. מי שמחשב רק אחד מהגורמים מקבל $2$ או $\tfrac92$.` },
      recap: "מלבן ומכפלה של פונקציות נפרדות: מפרידים לשני אינטגרלים." },
    { id: "C01-Q4", question: String.raw`מהם הקודקודים של התחום $0\le y\le x\le 2$ ?`,
      options: [
        { id: "a", value: String.raw`$(0,0),\ (2,0),\ (0,2)$` },
        { id: "b", value: String.raw`$(0,0),\ (0,2),\ (2,2)$` },
        { id: "c", value: String.raw`$(0,0),\ (2,0),\ (2,2)$` },
        { id: "d", value: String.raw`$(0,0),\ (2,2),\ (4,0)$` },
      ],
      correctId: "c",
      explanation: String.raw`הקודקודים הם חיתוכי הגבולות: $y=0$ עם $y=x$ נותן $(0,0)$, $y=0$ עם $x=2$ נותן $(2,0)$, ו-$y=x$ עם $x=2$ נותן $(2,2)$. הצורה $(0,0),(2,0),(0,2)$ היא התחום $x+y\le2$. הצורה $(0,0),(0,2),(2,2)$ היא התחום $y\ge x$ (מעל האלכסון). ו-$(4,0)$ אינו על אף גבול של התחום.`,
      recap: "הקודקודים הם נקודות החיתוך של זוגות עקומי הגבול." },
    { id: "C01-Q5", question: String.raw`איזה מהאינטגרלים הנשנים הבאים כתוב נכון (בלי גבול שתלוי במשתנה שאינו חיצוני)?`,
      options: [
        { id: "a", value: String.raw`$\int_0^{x}\int_0^{1} f\,dy\,dx$` },
        { id: "b", value: String.raw`$\int_0^1\int_0^{y} f\,dy\,dx$` },
        { id: "c", value: String.raw`$\int_0^1\int_0^{x} f\,dy\,dx$` },
        { id: "d", value: String.raw`$\int_0^{y}\int_0^{1} f\,dx\,dy$` },
      ],
      correctId: "c",
      explanation: String.raw`רק באינטגרל $\int_0^1\int_0^{x}f\,dy\,dx$ הגבולות החיצוניים קבועים והגבול הפנימי תלוי ב-$x$, המשתנה החיצוני. ב-$\int_0^{x}\ldots dx$ ובאינטגרל החיצוני $\int_0^{y}\ldots dy$ הגבול החיצוני תלוי במשתנה האינטגרציה עצמו, ולכן אינו מספר. ב-$\int_0^{y}f\,dy$ הפנימי הגבול העליון הוא המשתנה שמשתנה בתוך האינטגרל עצמו, וגם זה חסר משמעות.`,
      recap: "חיצוני: קבועים. פנימי: פונקציה של החיצוני בלבד." },
    { id: "C01-Q6",
      step: { type: "findbug", prompt: String.raw`הפתרון של $\int_0^1\int_0^x (x+y)\,dy\,dx$ מוצג בארבע שורות. כל שורה נבחנת כאמירה בפני עצמה, ובדיוק אחת מהן שגויה מבחינה חשבונית. סמנו אותה.`,
              lines: [
                String.raw`$\int_0^x (x+y)\,dy=\left[xy+\tfrac{y^2}{2}\right]_0^x$`,
                String.raw`$=x^2+\tfrac{x^2}{2}=2x^2$`,
                String.raw`$\int_0^1 \tfrac{3x^2}{2}\,dx=\left[\tfrac{x^3}{2}\right]_0^1$`,
                String.raw`$=\tfrac12$`,
              ],
              bugIndex: 1,
              explain: String.raw`$x^2+\tfrac{x^2}{2}=\tfrac{3x^2}{2}$ ולא $2x^2$. שאר השורות נכונות: הקדומה של $x+y$ לפי $y$ היא $xy+\tfrac{y^2}{2}$, האינטגרל של $\tfrac{3x^2}{2}$ מאפס עד אחד הוא $\tfrac12$.` },
      recap: "בפנימי מציבים את הגבולות ומאחדים איברים לפני שעוברים לחיצוני." },
  ],
});
