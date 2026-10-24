/* limits_diff, level 4: polar form and the squeeze theorem */
COURSE_LEVEL("limits_diff", {
  id: "C04", order: 4, icon: "🔄", title: "קואורדינטות קוטביות וסנדוויץ'",
  goal: "להוכיח שגבול קיים: לעבור לקוטביות, לחסום בביטוי התלוי רק ב-$r$, ולהסיק שהוא $0$.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>כדי להוכיח שהגבול קיים צריך טיעון שמכסה את כל הכיוונים בבת אחת. קואורדינטות קוטביות עושות זאת: $x=r\cos\theta$, $y=r\sin\theta$, והתקרבות לראשית היא $r\to0$ עבור <b>כל</b> $\theta$.</p>
    <div class="lesson-rule">🔑 <b>משפט הסנדוויץ'.</b> אם $|f(x,y)-L|\le g(r)$ כאשר $g(r)\to0$ והחסם $g$ <b>אינו תלוי ב-$\theta$</b>, אז $\lim f=L$. הכלי העיקרי: $|\cos\theta|\le1$ ו-$|\sin\theta|\le1$.</div>
    <div class="lesson-ex">דוגמה: $f(x,y)=\dfrac{x^2y}{x^2+y^2}$.
    $$f=\frac{r^2\cos^2\theta\cdot r\sin\theta}{r^2}=r\cos^2\theta\sin\theta,\qquad |f|\le r\xrightarrow[r\to0]{}0.$$
    לכן $\lim f=0$. הסימנים: המונה מדרגה 3 והמכנה מדרגה 2, ולכן נשארת חזקה חיובית של $r$.</div>
    <div class="lesson-trap">⚠️ אם אחרי הצמצום נשארת חזקה $r^0$ (כלומר ביטוי שתלוי רק ב-$\theta$, כמו $\cos^2\theta$), הערך תלוי בכיוון והגבול אינו קיים. גורם כמו $\tan\theta$ אינו חסום, ואי אפשר לחסום איתו.</div>` },
  questions: [
    { id: "C04-Q1",
      step: { type: "numeric", prompt: String.raw`עבור $f(x,y)=\dfrac{x^2y^2}{x^2+y^2}$, אחרי המעבר לקוטביות מתקבל $f=r^p\cos^2\theta\sin^2\theta$. מהו $p$?`,
              answer: 2, tol: 0,
              explain: String.raw`$f=\frac{r^2\cos^2\theta\cdot r^2\sin^2\theta}{r^2}=r^2\cos^2\theta\sin^2\theta$, ולכן $p=2$.` },
      recap: "מונה מדרגה 4, מכנה מדרגה 2: נשאר $r^2$." },
    { id: "C04-Q2",
      question: String.raw`באותה $f(x,y)=\dfrac{x^2y^2}{x^2+y^2}=r^2\cos^2\theta\sin^2\theta$: איזה חסם מוכיח ש-$\lim f=0$?`,
      options: [
        { id: "a", value: "$|f|\\le r^2$, כי $\\cos^2\\theta\\sin^2\\theta\\le1$" },
        { id: "b", value: "$|f|\\le\\dfrac{r^2}{\\cos^2\\theta}$, כי $\\sin^2\\theta\\le1$" },
        { id: "c", value: "$|f|\\le1$, כי הפונקציה חסומה" },
        { id: "d", value: "$|f|\\le r^2\\tan^2\\theta$, כי $\\cos^2\\theta\\le1$" },
      ],
      correctId: "a",
      explanation: String.raw`רק החסם $r^2$ אינו תלוי ב-$\theta$ ושואף ל-$0$. החסם $1$ אינו שואף ל-$0$. החסמים עם $\frac{1}{\cos^2\theta}$ ועם $\tan^2\theta$ תלויים ב-$\theta$ ואינם חסומים (הם שואפים לאינסוף כש-$\theta\to\frac\pi2$), ולכן אינם מוכיחים כלום.`,
      recap: "חסם בלי $\\theta$ ששואף ל-$0$." },
    { id: "C04-Q3",
      step: { type: "numeric", prompt: String.raw`עבור $f(x,y)=\dfrac{x^2y}{x^2+y^2}=r\cos^2\theta\sin\theta$: מהו הקבוע הקטן ביותר $C$ שעבורו $|f|\le C\,r$ לכל $\theta$ (שלוש ספרות אחרי הנקודה)?`,
              answer: 0.385, tol: 0.001,
              explain: String.raw`צריך את המקסימום של $\cos^2\theta\,|\sin\theta|$. עם $s=\sin\theta$ זה $(1-s^2)s$, שמקסימומו ב-$s=\frac1{\sqrt3}$ הוא $\frac{2}{3\sqrt3}\approx0.385$. כל קבוע גדול מזה, גם $1$, מספיק כדי להוכיח את הגבול.` },
      recap: "מספיק חסם גס: $C=1$." },
    { id: "C04-Q4",
      step: { type: "findbug", prompt: String.raw`בהוכחה ש-$\lim \dfrac{xy^2}{x^2+y^2}=0$ שורה אחת שגויה. איזו?`,
              lines: [
                String.raw`נעבור לקוטביות: $x=r\cos\theta$, $y=r\sin\theta$.`,
                String.raw`$f=\frac{r\cos\theta\cdot r^2\sin^2\theta}{r^2}=r\cos\theta\sin\theta$.`,
                String.raw`$|f|\le r\cdot|\cos\theta|\cdot\sin^2\theta\le r$.`,
                String.raw`החסם $r$ שואף ל-$0$ ואינו תלוי ב-$\theta$, ולכן $\lim f=0$.`,
              ],
              bugIndex: 1,
              explain: String.raw`המונה הוא $r\cos\theta\cdot r^2\sin^2\theta=r^3\cos\theta\sin^2\theta$, ולכן $f=r\cos\theta\sin^2\theta$. בשורה השנייה הוחלף $\sin^2\theta$ ב-$\sin\theta$. שאר השורות מתאימות לביטוי הנכון.` },
      recap: "מפשטים בזהירות: $y^2$ נותן $\\sin^2\\theta$." },
    { id: "C04-Q5",
      question: String.raw`בפונקציה $g(x,y)=\dfrac{x^2}{x^2+y^2}$ המעבר לקוטביות נותן $g=\cos^2\theta$. מה זה אומר על $\lim_{(x,y)\to(0,0)}g$?`,
      options: [
        { id: "a", value: "הגבול הוא $0$, כי $r\\to0$" },
        { id: "b", value: "הגבול הוא $1$, כי $\\cos^2\\theta\\le1$" },
        { id: "c", value: "הגבול אינו קיים, כי הערך תלוי ב-$\\theta$ ואינו תלוי ב-$r$" },
        { id: "d", value: "הגבול הוא $\\frac12$, הממוצע של $\\cos^2\\theta$" },
      ],
      correctId: "c",
      explanation: String.raw`הערך $\cos^2\theta$ קבוע לאורך כל קרן, ושונה בין קרנות: $1$ ב-$\theta=0$ ו-$0$ ב-$\theta=\frac\pi2$. לכן אין גבול. ה-$r$ לא מופיע בכלל, ולכן "$r\to0$" לא משנה כלום. הממוצע והחסם $1$ אינם ערכי גבול.`,
      recap: "ביטוי שתלוי רק ב-$\\theta$: אין גבול." },
    { id: "C04-Q6",
      step: { type: "numeric", prompt: String.raw`$f(x,y)=\dfrac{x^3-3xy^2}{x^2+y^2}$ היא בקוטביות $r\cos3\theta$. אחרי החסם $|f|\le r$ והסנדוויץ', מהו $\lim_{(x,y)\to(0,0)}f$?`,
              answer: 0, tol: 0,
              explain: String.raw`$|r\cos3\theta|\le r\to0$ ללא תלות ב-$\theta$, ולכן הגבול הוא $0$.` },
      recap: "מפעילים את אותה שיטה על כל מונה הומוגני מדרגה גבוהה מהמכנה." },
  ],
});
