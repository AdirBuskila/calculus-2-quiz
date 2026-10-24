/* double_int, level 3 - swapping the order of integration (single piece) */
COURSE_LEVEL("double_int", {
  id: "C03", order: 3, icon: "🔄", title: "חילוף סדר האינטגרציה",
  goal: "להחליף סדר אינטגרציה באינטגרל נשנה: לקרוא את התחום מהגבולות, לשרטט, ולקרוא אותו בכיוון ההפוך.",
  source: "ai-verified",
  lesson: { html: String.raw`
<p>חילוף סדר אומר: אותו תחום בדיוק, אבל סורקים אותו בפסים מהכיוון השני. האינטגרנד נשאר, והגבולות משתנים. ההצדקה היא משפט פוביני: לפונקציה רציפה על תחום כזה שני הסדרים נותנים אותו ערך.</p>
<div class="lesson-rule">🔑 <b>מתכון בארבעה צעדים:</b>
<ul>
<li>כתבו את אי-השוויונים של האינטגרל הנתון;</li>
<li>שרטטו את התחום וסמנו את כל העקומים ואת נקודות החיתוך;</li>
<li>לכל ערך של המשתנה החיצוני החדש, ראו ממה עד מה נע המשתנה הפנימי החדש (מבודדים אותו מכל עקום);</li>
<li>כתבו את האינטגרל החדש ובדקו עם $f\equiv1$ שהשטח לא השתנה.</li>
</ul></div>
<h3>דוגמה 1: משולש</h3>
<p>$\int_0^1\int_y^1 f\,dx\,dy$: התחום $0\le y\le1$, $y\le x\le1$ הוא המשולש $0\le y\le x\le 1$. לכל $x$ קבוע, $y$ נע מ-$0$ עד $x$, ולכן הסדר ההפוך הוא $\int_0^1\int_0^x f\,dy\,dx$.</p>
<div class="region-fig" data-region='{"inequalities":["x>=y","y>=0","1>=x"],"boundary_curves":["y=x","y=0","x=1"],"orderXY":{"x":[0,1],"y":[0,"x"]},"orderYX":{"y":[0,1],"x":["y",1]},"vertices":[[0,0],[1,0],[1,1]],"area":"1/2"}'></div>
<h3>דוגמה 2: פרבולה</h3>
<p>$\int_0^2\int_{x^2}^{4} f\,dy\,dx$: התחום $0\le x\le2$, $x^2\le y\le4$. כש-$y$ קבוע בין $0$ ל-$4$, הקו האופקי נכנס דרך הציר $x=0$ ויוצא דרך הפרבולה $x=\sqrt y$. לכן $\int_0^4\int_0^{\sqrt y} f\,dx\,dy$.</p>
<div class="region-fig" data-region='{"inequalities":["x>=0","y>=x^2","4>=y"],"boundary_curves":["y=x^2","y=4","x=0"],"orderXY":{"x":[0,2],"y":["x^2",4]},"orderYX":{"y":[0,4],"x":[0,"sqrt(y)"]},"area":"16/3"}'></div>
<div class="lesson-trap">⚠️ בסדר החדש גם הגבולות החיצוניים חייבים להיות קבועים. אם נשארה בהם נעלם, התחום נקרא לא נכון. בדקו גם שהגבול התחתון קטן מהעליון בכל הטווח.</div>
` },
  questions: [
    { id: "C03-Q1", question: String.raw`מהו האינטגרל המתקבל מחילוף הסדר ב-$\int_0^1\int_y^1 f(x,y)\,dx\,dy$ ?`,
      options: [
        { id: "a", value: String.raw`$\int_0^1\int_x^1 f\,dy\,dx$` },
        { id: "b", value: String.raw`$\int_0^1\int_0^{1-x} f\,dy\,dx$` },
        { id: "c", value: String.raw`$\int_0^1\int_0^1 f\,dy\,dx$` },
        { id: "d", value: String.raw`$\int_0^1\int_0^x f\,dy\,dx$` },
      ],
      correctId: "d",
      explanation: String.raw`התחום הוא $0\le y\le x\le1$ (משולש מתחת לאלכסון). לכל $x$ קבוע בין $0$ ל-$1$, $y$ נע מ-$0$ עד $x$. התיאור $x\le y\le1$ הוא המשולש שמעל האלכסון, $0\le y\le1-x$ הוא משולש אחר, וה-$0\le y\le1$ הוא כל הריבוע (שטח $1$ במקום $\tfrac12$).`,
      recap: "משולש מתחת לאלכסון: $dy$ הפנימי מ-0 עד $x$." },
    { id: "C03-Q2",
      step: { type: "fillblank", prompt: String.raw`משלימים את חילוף הסדר של $\int_0^2\int_{x^2}^{4} f\,dy\,dx$. מה הגבול העליון של $x$ בסדר החדש?`,
              lines: [
                String.raw`התחום הנתון הוא $0\le x\le 2$ ו-$x^2\le y\le 4$, ולכן $y$ נע מ-$0$ עד $4$.`,
                String.raw`בגובה $y$ קבוע, $x$ נע מ-$0$ עד הפרבולה, כלומר עד $x=$ ___`,
              ],
              blankIndex: 1,
              options: [
                { id: "a", value: String.raw`$y^2$` },
                { id: "b", value: String.raw`$\sqrt y$` },
                { id: "c", value: String.raw`$\tfrac y2$` },
                { id: "d", value: "$2$" },
              ],
              correctId: "b",
              explain: String.raw`הפרבולה $y=x^2$ נותנת $x=\sqrt y$ (בענף $x\ge0$). $x=y^2$ הוא ההפוך המוטעה, $x=\tfrac y2$ מתאים רק ב-$y=0$ וב-$y=4$ ולא בגבהים שביניהם (ב-$y=1$ הפרבולה בנקודה $x=1$ ולא $\tfrac12$), ו-$x=2$ הוא כל המלבן $0\le x\le2$.` },
      recap: "מבודדים $x$ מהעקום: $y=x^2$ נותן $x=\\sqrt y$." },
    { id: "C03-Q3",
      step: { type: "findbug", prompt: String.raw`נתון $\int_0^2\int_{x^2}^{4}f\,dy\,dx$ ומוצגת הדרך להחליף סדר. כל שורה נבחנת כאמירה בפני עצמה, ובדיוק אחת מהן שגויה. סמנו אותה.`,
              lines: [
                String.raw`התחום: $0\le x\le 2$ ו-$x^2\le y\le 4$`,
                String.raw`לכן $y$ נע בין $0$ ל-$4$`,
                String.raw`עבור $y$ קבוע, $x$ נע מהציר $x=0$ עד הפרבולה $x=y^2$`,
                String.raw`לכן האינטגרל החדש הוא $\int_0^4\int_0^{\sqrt y}f\,dx\,dy$`,
              ],
              bugIndex: 2,
              explain: String.raw`הפרבולה $y=x^2$ היא $x=\sqrt y$ ולא $x=y^2$. (הפרבולה $x=y^2$ היא פרבולה אחרת, מסובבת.) השורה האחרונה נכונה.` },
      recap: "ההפוך של $y=x^2$ הוא $x=\\sqrt y$." },
    { id: "C03-Q4",
      step: { type: "numeric", prompt: String.raw`חשבו את $\int_0^2\int_{x^2}^{4} x\,dy\,dx$. ענו כמספר.`,
              answer: 4, tol: 0,
              explain: String.raw`$\int_{x^2}^{4}x\,dy=x(4-x^2)$ ואז $\int_0^2(4x-x^3)\,dx=8-4=4$. בסדר ההפוך: $\int_0^4\int_0^{\sqrt y}x\,dx\,dy=\int_0^4\tfrac y2\,dy=4$, אותו ערך.` },
      recap: "שני הסדרים מתלכדים: בדיקה עצמית טובה." },
    { id: "C03-Q5", question: String.raw`מהו הסדר ההפוך של $\int_0^1\int_x^{\sqrt x} f\,dy\,dx$ ?`,
      options: [
        { id: "a", value: String.raw`$\int_0^1\int_{y^2}^{y} f\,dx\,dy$` },
        { id: "b", value: String.raw`$\int_0^1\int_{y}^{y^2} f\,dx\,dy$` },
        { id: "c", value: String.raw`$\int_0^1\int_{y}^{\sqrt y} f\,dx\,dy$` },
        { id: "d", value: String.raw`$\int_0^1\int_{y^2}^{\sqrt y} f\,dx\,dy$` },
      ],
      correctId: "a",
      explanation: String.raw`התחום $x\le y\le\sqrt x$ חסום בין הישר $y=x$ לפרבולה $y=\sqrt x$ (כלומר $x=y^2$), ו-$y$ נע מ-$0$ עד $1$. בגובה $y$ הקו האופקי נכנס דרך הפרבולה $x=y^2$ ויוצא דרך הישר $x=y$, כי $y^2\le y$ ב-$[0,1]$. לכן $y^2\le x\le y$. הגבולות ההפוכים ($y\le x\le y^2$) נותנים תחום ריק, $y\le x\le\sqrt y$ הוא התחום שבין הישר $x=y$ לפרבולה $x=\sqrt y$ (התחום המשתקף), ו-$y^2\le x\le\sqrt y$ הוא תחום גדול יותר.`,
      recap: "בגובה $y$ קבוע: נכנסים בגבול השמאלי ויוצאים בימני." },
    { id: "C03-Q6",
      step: { type: "numeric", prompt: String.raw`חשבו את שטח התחום $0\le x\le2,\ x^2\le y\le4$ בסדר ההפוך: $\int_0^4\int_0^{\sqrt y}1\,dx\,dy$. ענו כמספר עשרוני.`,
              answer: 5.3333, tol: 0.005,
              explain: String.raw`$\int_0^{\sqrt y}1\,dx=\sqrt y$ ואז $\int_0^4\sqrt y\,dy=\tfrac23\cdot 8=\tfrac{16}3\approx5.333$. בסדר המקורי: $\int_0^2(4-x^2)\,dx=8-\tfrac83=\tfrac{16}3$.` },
      recap: "שטח זהה בשני הסדרים: בדיקה שהחילוף נכון." },
  ],
});
