/* double_int, level 2 - type I (vertical strips, dy dx) and type II (horizontal strips, dx dy) */
COURSE_LEVEL("double_int", {
  id: "C02", order: 2, icon: "↕️", title: "סוג I וסוג II: פס אנכי ופס אופקי",
  goal: "לתאר אותו תחום גם כפסים אנכיים וגם כפסים אופקיים, ולחשב עם שניהם.",
  source: "ai-verified",
  lesson: { html: String.raw`
<p>את אותו תחום אפשר לסרוק בשתי דרכים:</p>
<table><thead><tr><th>סוג</th><th>הפס</th><th>התיאור</th><th>האינטגרל</th></tr></thead>
<tbody>
<tr><td><b>סוג I</b></td><td>אנכי: לכל $x$ קבוע, $y$ נע בין שני עקומים</td><td>$a\le x\le b,\ g_1(x)\le y\le g_2(x)$</td><td>$\int_a^b\int_{g_1(x)}^{g_2(x)}f\,dy\,dx$</td></tr>
<tr><td><b>סוג II</b></td><td>אופקי: לכל $y$ קבוע, $x$ נע בין שני עקומים</td><td>$c\le y\le d,\ h_1(y)\le x\le h_2(y)$</td><td>$\int_c^d\int_{h_1(y)}^{h_2(y)}f\,dx\,dy$</td></tr>
</tbody></table>
<div class="lesson-rule">🔑 איך קוראים פס: מעבירים קו דרך התחום (אנכי בסוג I, אופקי בסוג II) ורואים באיזה עקום הקו נכנס ובאיזה הוא יוצא. הכניסה היא הגבול התחתון והיציאה היא העליון.</div>
<p>דוגמה: התחום שבין $y=x^2$ ל-$y=x$. העקומים נפגשים בנקודות $x=0$ ו-$x=1$ (פותרים $x^2=x$). בתצוגת הפסים האנכיים הקו נכנס דרך הפרבולה ויוצא דרך הישר; בתצוגת הפסים האופקיים הוא נכנס דרך הישר $x=y$ ויוצא דרך הפרבולה $x=\sqrt y$. החליפו בין התצוגות כדי לראות:</p>
<div class="region-fig" data-region='{"inequalities":["y>=x^2","x>=y"],"boundary_curves":["y=x^2","y=x"],"orderXY":{"x":[0,1],"y":["x^2","x"]},"orderYX":{"y":[0,1],"x":["y","sqrt(y)"]},"vertices":[[0,0],[1,1]],"area":"1/6"}'></div>
<div class="lesson-ex">סוג I: $0\le x\le1,\ x^2\le y\le x$. סוג II: $0\le y\le1,\ y\le x\le\sqrt y$. השטח בשני הסדרים: $\int_0^1(x-x^2)\,dx=\tfrac12-\tfrac13=\tfrac16$.</div>
<div class="lesson-trap">⚠️ כדי לעבור לסוג II צריך לבודד את $x$ מכל עקום: $y=x^2$ הופך ל-$x=\sqrt y$ (בענף $x\ge0$ בלבד), ו-$y=x$ הופך ל-$x=y$.</div>
` },
  questions: [
    { id: "C02-Q1", question: String.raw`התחום חסום בין הפרבולה $y=x^2$ לישר $y=x$. כיצד כותבים אותו כסוג I (פסים אנכיים)?`,
      options: [
        { id: "a", value: String.raw`$0\le x\le 1,\ x^2\le y\le 1$` },
        { id: "b", value: String.raw`$0\le x\le 1,\ x\le y\le x^2$` },
        { id: "c", value: String.raw`$0\le x\le 1,\ x^2\le y\le x$` },
        { id: "d", value: String.raw`$0\le x\le 1,\ 0\le y\le x^2$` },
      ],
      correctId: "c",
      explanation: String.raw`העקומים נפגשים ב-$x=0$ וב-$x=1$, ובין שתי הנקודות הישר $y=x$ נמצא מעל הפרבולה, לכן $x^2\le y\le x$. התיאור עם $y\le1$ הוא האזור שמעל הפרבולה עד הישר $y=1$, וגם הוא תחום אחר. ההפוך ($x\le y\le x^2$) ריק, ו-$0\le y\le x^2$ הוא האזור שמתחת לפרבולה.`,
      recap: "מוצאים את נקודות החיתוך, ובכל טווח קובעים מי העליון ומי התחתון." },
    { id: "C02-Q2",
      step: { type: "numeric", prompt: String.raw`חשבו את שטח התחום שבין $y=x^2$ ל-$y=x$, כלומר $\int_0^1\int_{x^2}^{x}1\,dy\,dx$. ענו כמספר עשרוני.`,
              answer: 0.16667, tol: 0.001,
              explain: String.raw`$\int_{x^2}^{x}1\,dy=x-x^2$ ואז $\int_0^1(x-x^2)\,dx=\tfrac12-\tfrac13=\tfrac16\approx0.1667$.` },
      recap: "שטח התחום = אינטגרל של 1 עליו, והפנימי נותן את אורך הפס." },
    { id: "C02-Q3", question: String.raw`כיצד כותבים את אותו תחום (בין $y=x^2$ ל-$y=x$) כסוג II (פסים אופקיים)?`,
      options: [
        { id: "a", value: String.raw`$0\le y\le1,\ \sqrt y\le x\le y$` },
        { id: "b", value: String.raw`$0\le y\le1,\ y\le x\le\sqrt y$` },
        { id: "c", value: String.raw`$0\le y\le1,\ y^2\le x\le y$` },
        { id: "d", value: String.raw`$0\le y\le1,\ 0\le x\le\sqrt y$` },
      ],
      correctId: "b",
      explanation: String.raw`בגובה $y$ קבוע הקו האופקי נכנס דרך הישר $x=y$ ויוצא דרך הפרבולה $x=\sqrt y$ (כי $y=x^2$ נותן $x=\sqrt y$ ב-$x\ge0$). לכן $y\le x\le\sqrt y$. התיאור עם $\sqrt y\le x\le y$ ריק (ב-$(0,1)$ מתקיים $\sqrt y>y$). התיאור עם $y^2\le x$ מתקבל מבלבול בין $y=x^2$ ל-$x=y^2$. והתיאור $0\le x\le\sqrt y$ כולל גם את המשולש שמשמאל לישר $x=y$, שאינו בתחום.`,
      recap: "מבודדים $x$ מכל עקום ($x=\\sqrt y$, $x=y$) ובודקים מי משמאל." },
    { id: "C02-Q4", question: String.raw`באינטגרל נשנה בסדר $dy\,dx$ (האינטגרל הפנימי לפי $y$), הגבולות של האינטגרל החיצוני הם:`,
      options: [
        { id: "a", value: "פונקציות של $y$" },
        { id: "b", value: "מספרים קבועים" },
        { id: "c", value: "פונקציות של $x$" },
        { id: "d", value: "תלויים באינטגרנד $f$" },
      ],
      correctId: "b",
      explanation: String.raw`האינטגרל החיצוני סורק טווח אחד של המשתנה החיצוני ($x$ כאן), ולכן גבולותיו מספרים קבועים. הפונקציות של $x$ הן הגבולות של האינטגרל הפנימי, ואילו פונקציות של $y$ יופיעו בגבולות הפנימיים בסדר ההפוך ($dx\,dy$). האינטגרנד אינו משפיע על הגבולות: הם תלויים בתחום בלבד.`,
      recap: "חיצוני קבוע תמיד, בכל סדר." },
    { id: "C02-Q5",
      step: { type: "order", prompt: String.raw`סדרו את שלבי החישוב של $\int_0^1\int_{x^2}^{x} y\,dy\,dx$.`,
              lines: [
                String.raw`$\int_{x^2}^{x}y\,dy=\tfrac{x^2-x^4}{2}$`,
                String.raw`$\int_0^1\tfrac{x^2-x^4}{2}\,dx=\tfrac12\left(\tfrac13-\tfrac15\right)$`,
                String.raw`$=\tfrac1{15}$`,
              ],
              explain: String.raw`קודם האינטגרל הפנימי (תוצאתו פונקציה של $x$), אחר כך החיצוני על התוצאה, ובסוף הערך: $\tfrac12\cdot\tfrac{2}{15}=\tfrac1{15}$.` },
      recap: "פנימי קודם, תוצאתו נכנסת לחיצוני." },
    { id: "C02-Q6",
      step: { type: "numeric", prompt: String.raw`חשבו בפסים אופקיים את $\int_0^1\int_{y}^{\sqrt y} x\,dx\,dy$ (אותו תחום, האינטגרנד $x$). ענו כמספר עשרוני.`,
              answer: 0.08333, tol: 0.0005,
              explain: String.raw`$\int_y^{\sqrt y}x\,dx=\tfrac{y-y^2}{2}$ ואז $\int_0^1\tfrac{y-y^2}{2}\,dy=\tfrac12\left(\tfrac12-\tfrac13\right)=\tfrac1{12}$. בפסים אנכיים מתקבל אותו ערך: $\int_0^1x(x-x^2)\,dx=\tfrac13-\tfrac14=\tfrac1{12}$.` },
      recap: "שני הסדרים נותנים אותו ערך (פוביני)." },
  ],
});
