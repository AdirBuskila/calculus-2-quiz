/* limits_diff, level 5: continuity at the origin of a piecewise function */
COURSE_LEVEL("limits_diff", {
  id: "C05", order: 5, icon: "✅", title: "רציפות בראשית",
  goal: "להכריע אם פונקציה מוגדרת בחלקים רציפה בראשית, ולמצוא את הערך של הפרמטר שהופך אותה לרציפה.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>הפונקציה בשאלה כמעט תמיד מוגדרת בחלקים: נוסחה מורכבת לכל $(x,y)\neq(0,0)$, וערך נתון בראשית.</p>
    <div class="lesson-rule">🔑 $f$ רציפה ב-$(0,0)$ אם ורק אם <b>הגבול קיים</b> ו<b>שווה ל-$f(0,0)$</b>. הנוסחה הרגילה משמשת לחישוב הגבול, והערך הנתון בראשית משמש להשוואה.</div>
    <p>יש שלוש תוצאות אפשריות:</p>
    <ul>
      <li>הגבול אינו קיים (שני מסלולים שונים): <b>לא רציפה</b>, ואף ערך בראשית לא יתקן זאת.</li>
      <li>הגבול קיים ושונה מ-$f(0,0)$: <b>לא רציפה</b>, אבל אפשר לתקן אם משנים את הערך בראשית ל-$L$.</li>
      <li>הגבול קיים ושווה ל-$f(0,0)$: <b>רציפה</b>.</li>
    </ul>
    <div class="lesson-ex">דוגמה: $f=\dfrac{x^2y}{x^2+y^2}$ ו-$f(0,0)=c$. מקוטביות הגבול הוא $0$ (שלב 4), ולכן $f$ רציפה בדיוק כש-$c=0$.</div>
    <div class="lesson-ex">כשמופיע $x^2+y^2$ בתוך פונקציה מוכרת, מציבים $u=x^2+y^2\to0$ ומשתמשים בגבול של משתנה אחד: $\lim_{u\to0}\dfrac{\sin u}{u}=1$ ו-$\lim_{u\to0}\dfrac{1-\cos u}{u}=0$, וכן $\lim_{u\to0}\dfrac{1-\cos u}{u^2}=\dfrac12$.</div>
    <div class="lesson-trap">⚠️ הערך $f(0,0)$ אינו משפיע על הגבול. אם הגבול הוא $0$ והערך הנתון הוא $1$, הפונקציה לא רציפה.</div>` },
  questions: [
    { id: "C05-Q1",
      step: { type: "numeric", prompt: String.raw`נתונה $f(x,y)=\dfrac{x^2y}{x^2+y^2}$ לכל $(x,y)\neq(0,0)$ ו-$f(0,0)=c$. לאיזה $c$ הפונקציה רציפה ב-$(0,0)$?`,
              answer: 0, tol: 0,
              explain: String.raw`הגבול הוא $0$ (בקוטביות $|f|\le r$), ולכן רציפות מחייבת $c=0$.` },
      recap: "רציפה: $c$ שווה לגבול." },
    { id: "C05-Q2",
      step: { type: "numeric", prompt: String.raw`נתונה $g(x,y)=\dfrac{\sin\left(x^2+y^2\right)}{x^2+y^2}$ לכל $(x,y)\neq(0,0)$ ו-$g(0,0)=c$. לאיזה $c$ הפונקציה רציפה?`,
              answer: 1, tol: 0,
              explain: String.raw`מציבים $u=x^2+y^2\to0$: $\frac{\sin u}{u}\to1$. לכן $c=1$.` },
      recap: "מציבים $u=x^2+y^2$ וחוזרים למשתנה אחד." },
    { id: "C05-Q3",
      question: String.raw`נתונה $f(x,y)=\dfrac{x^2y}{x^2+y^2}$ לכל $(x,y)\neq(0,0)$, אבל הפעם $f(0,0)=1$. מה נכון?`,
      options: [
        { id: "a", value: "$f$ רציפה בראשית, כי הגבול קיים" },
        { id: "b", value: "$f$ אינה רציפה, כי הגבול הוא $0$ והערך בראשית הוא $1$" },
        { id: "c", value: "$f$ אינה רציפה, כי הגבול אינו קיים" },
        { id: "d", value: "$f$ רציפה, כי $f(0,0)$ מוגדר" },
      ],
      correctId: "b",
      explanation: String.raw`הגבול קיים ושווה ל-$0$ (חסם $|f|\le r$), אבל $f(0,0)=1\neq0$. קיום הגבול לבדו אינו מספיק; צריך גם שוויון לערך. התשובה על "הגבול אינו קיים" שגויה, כי הגבול כן קיים.`,
      recap: "גבול קיים אבל שונה מהערך: לא רציפה." },
    { id: "C05-Q4",
      question: String.raw`נתונה $h(x,y)=\dfrac{x^2-y^2}{x^2+y^2}$ לכל $(x,y)\neq(0,0)$ ו-$h(0,0)=c$, כאשר $c$ מספר כלשהו. מה נכון?`,
      options: [
        { id: "a", value: "אין שום $c$ שהופך את $h$ לרציפה, כי הגבול אינו קיים" },
        { id: "b", value: "$c=0$ הופך את $h$ לרציפה" },
        { id: "c", value: "$c=1$ הופך את $h$ לרציפה, כי זה הערך על ציר $x$" },
        { id: "d", value: "כל $c$ הופך את $h$ לרציפה" },
      ],
      correctId: "a",
      explanation: String.raw`לאורך ציר $x$ הערך הוא $1$ ולאורך $y=x$ הוא $0$, ולכן הגבול אינו קיים. רציפות דורשת גבול קיים, ולכן אף $c$ לא יעזור. מסלול אחד, כמו ציר $x$, אינו קובע את הגבול.`,
      recap: "בלי גבול אין ערך שמתקן." },
    { id: "C05-Q5",
      step: { type: "numeric", prompt: String.raw`נתונה $k(x,y)=\dfrac{1-\cos\left(x^2+y^2\right)}{\left(x^2+y^2\right)^2}$ לכל $(x,y)\neq(0,0)$ ו-$k(0,0)=c$. לאיזה $c$ הפונקציה רציפה (עשרוני)?`,
              answer: 0.5, tol: 0.001,
              explain: String.raw`עם $u=x^2+y^2$: $\frac{1-\cos u}{u^2}\to\frac12$.` },
      recap: "$\\frac{1-\\cos u}{u^2}\\to\\frac12$." },
    { id: "C05-Q6",
      step: { type: "numeric", prompt: String.raw`נתונה $m(x,y)=\dfrac{x^2+y^2+x^3}{x^2+y^2}$ לכל $(x,y)\neq(0,0)$ ו-$m(0,0)=c$. לאיזה $c$ הפונקציה רציפה?`,
              answer: 1, tol: 0,
              explain: String.raw`$m=1+\frac{x^3}{x^2+y^2}=1+r\cos^3\theta$, ו-$|r\cos^3\theta|\le r\to0$. הגבול הוא $1$.` },
      recap: "מפרקים ל-$1$ ועוד גורם שנחסם בקוטביות." },
  ],
});
