/* limits_diff, level 2: choosing the path that breaks the limit (match the orders of numerator and denominator) */
COURSE_LEVEL("limits_diff", {
  id: "C02", order: 2, icon: "🛤️", title: "לבחור מסלול שמפיל את הגבול",
  goal: "לבחור מסלול מהצורה $y=kx^a$ (או $x=ky^a$) שבו המונה והמכנה מאותו סדר גודל, ולחשב איתו את הגבול.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>ברוב השאלות הישרים $y=mx$ נותנים $0$ ואינם עוזרים. הטריק: לבחור מסלול שבו המונה והמכנה "באותו סדר גודל", כך שהמנה לא מתאפסת.</p>
    <div class="lesson-rule">🔑 <b>מתכון.</b> מציבים $y=kx^a$ ובודקים את החזקה הנמוכה ביותר של $x$ במונה ובמכנה. בוחרים את $a$ כך שהן שוות. אם נשאר ביטוי התלוי ב-$k$, הגבול אינו קיים.</div>
    <div class="lesson-ex">דוגמה: $f(x,y)=\dfrac{x^2y}{x^4+y^2}$. במונה, אחרי ההצבה $y=kx^a$, החזקה היא $x^{2+a}$. במכנה יש $x^4$ ו-$k^2x^{2a}$, והחזקה הנמוכה מביניהן היא $x^{\min(4,\,2a)}$. השוויון $2+a=2a$ נותן $a=2$, ואז גם $2a=4$:
    $$f\left(x,kx^2\right)=\frac{kx^4}{x^4+k^2x^4}=\frac{k}{1+k^2}.$$
    הערך תלוי ב-$k$ ($k=1$ נותן $\frac12$, ו-$y=0$ נותן $0$), ולכן הגבול אינו קיים.</div>
    <div class="lesson-trap">⚠️ לפעמים החזקה היא במשתנה השני. ב-$\dfrac{xy^2}{x^2+y^4}$ המכנה מכיל $y^4$ ו-$x^2$, ולכן המסלול הנכון הוא $x=ky^2$ ולא $y=kx^a$.</div>` },
  questions: [
    { id: "C02-Q1",
      question: String.raw`עבור $f(x,y)=\dfrac{x^2y}{x^4+y^2}$, איזה מסלול מביא את המונה והמכנה לאותו סדר גודל ונותן ערך שאינו $0$?`,
      options: [
        { id: "a", value: "$y=kx$" },
        { id: "b", value: "$y=kx^3$" },
        { id: "c", value: "$y=kx^2$" },
        { id: "d", value: "$x=ky$" },
      ],
      correctId: "c",
      explanation: String.raw`רק $y=kx^2$ נותן $\frac{k}{1+k^2}\neq0$. לאורך $y=kx$ הערך הוא $\frac{kx}{x^2+k^2}\to0$. לאורך $y=kx^3$ המונה קטן מהמכנה ולכן הערך שואף ל-$0$. גם $x=ky$ נותן $0$.`,
      recap: "סדר הגודל של המונה והמכנה צריך להתאים." },
    { id: "C02-Q2",
      step: { type: "numeric", prompt: String.raw`באותה פונקציה $f(x,y)=\dfrac{x^2y}{x^4+y^2}$: מהו הגבול לאורך $y=x^2$ כאשר $x\to0$ (עשרוני)?`,
              answer: 0.5, tol: 0.001,
              explain: String.raw`$f(x,x^2)=\frac{x^4}{x^4+x^4}=\frac12$.` },
      recap: "אחרי ההצבה המכנה והמונה נשארים עם $x^4$." },
    { id: "C02-Q3",
      step: { type: "numeric", prompt: String.raw`ועכשיו לאורך $y=2x^2$ (כלומר $k=2$): מהו הגבול של אותה פונקציה (עשרוני)?`,
              answer: 0.4, tol: 0.001,
              explain: String.raw`$\frac{k}{1+k^2}$ עבור $k=2$ הוא $\frac25=0.4$.` },
      recap: "כל $k$ נותן ערך אחר: $\\frac{k}{1+k^2}$." },
    { id: "C02-Q4",
      question: String.raw`באותה פונקציה לאורך $y=0$ הערך הוא $0$, ולאורך $y=x^2$ הוא $\frac12$. מה אפשר לומר על הרציפות של $f$ בראשית, כש-$f(0,0)=0$?`,
      options: [
        { id: "a", value: "אינה רציפה, כי הגבול בראשית אינו קיים" },
        { id: "b", value: "רציפה, כי לאורך ציר $x$ הגבול הוא $0=f(0,0)$" },
        { id: "c", value: "רציפה, כי הערך $\\frac12$ הוא חריג יחיד" },
        { id: "d", value: "רציפה, כי $f$ מוגדרת בראשית ו-$f(0,0)=0$" },
      ],
      correctId: "a",
      explanation: String.raw`שני מסלולים נותנים $0$ ו-$\frac12$, ולכן הגבול אינו קיים, ובפרט אינו שווה ל-$f(0,0)$. רציפות דורשת שהגבול יהיה קיים ושווה לערך בנקודה. בדיקה של מסלול אחד, כמו ציר $x$, אינה מספיקה.`,
      recap: "רציפות דורשת גבול קיים: מסלול אחד לא מספיק." },
    { id: "C02-Q5",
      step: { type: "numeric", prompt: String.raw`נתונה $g(x,y)=\dfrac{x^3y}{x^6+2y^2}$. לאורך $y=kx^3$ מתקבל $\dfrac{k}{1+2k^2}$. מהו הגבול לאורך $y=x^3$ (עשרוני, שלוש ספרות)?`,
              answer: 0.333, tol: 0.001,
              explain: String.raw`$k=1$: $\frac{1}{1+2}=\frac13\approx0.333$. הערך שונה מ-$0$ (ציר $x$) ולכן הגבול אינו קיים.` },
      recap: "כאן המסלול הוא $y=kx^3$, כי $x^3y$ ו-$x^6$ מאותו סדר." },
    { id: "C02-Q6",
      step: { type: "numeric", prompt: String.raw`נתונה $p(x,y)=\dfrac{xy^2}{x^2+y^4}$. החזקות כאן במשתנה $y$, ולכן מתאים המסלול $x=ky^2$. מהו הגבול לאורך $x=y^2$ (כלומר $k=1$) כאשר $y\to0$ (עשרוני)?`,
              answer: 0.5, tol: 0.001,
              explain: String.raw`$p(y^2,y)=\frac{y^2\cdot y^2}{y^4+y^4}=\frac12$. לאורך ציר $y$ ($x=0$) הערך הוא $0$, ולכן הגבול אינו קיים.` },
      recap: "אם החזקות במשתנה $y$, המסלול הוא $x=ky^a$." },
  ],
});
