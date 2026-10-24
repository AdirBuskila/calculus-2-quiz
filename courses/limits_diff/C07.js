/* limits_diff, level 7: differentiability at the origin via the remainder limit Q(h,k) */
COURSE_LEVEL("limits_diff", {
  id: "C07", order: 7, icon: "📐", title: "גבול הדיפרנציאביליות",
  goal: "לבדוק דיפרנציאביליות בראשית: לבנות את $Q(h,k)$, ולהכריע אם הוא שואף ל-$0$.",
  source: "ai-verified",
  lesson: { html: String.raw`
    <p>$f$ דיפרנציאבילית ב-$(0,0)$ אם היא "כמעט לינארית" בסביבתה: ההפרש בינה לבין המישור המשיק קטן יותר מהמרחק לראשית.</p>
    <div class="lesson-formula">$$Q(h,k)=\frac{f(h,k)-f(0,0)-f_x(0,0)\,h-f_y(0,0)\,k}{\sqrt{h^2+k^2}}.$$
    <p>$f$ דיפרנציאבילית בראשית בדיוק כאשר $\lim_{(h,k)\to(0,0)}Q(h,k)=0$.</p></div>
    <div class="lesson-rule">🔑 <b>סדר העבודה.</b> (1) נגזרות חלקיות בראשית לפי ההגדרה. (2) מציבים אותן ב-$Q$, <b>כולל החיסור</b> $f_xh+f_yk$. (3) עוברים לקוטביות. אם $|Q|\le Cr$ (חסם בלי $\theta$), אז $Q\to0$ ו-$f$ דיפרנציאבילית. אם יש מסלול שבו $Q$ לא שואף ל-$0$, אז $f$ אינה דיפרנציאבילית.</div>
    <div class="lesson-ex">דוגמה: $f=\dfrac{x^2y}{x^2+y^2}$, $f(0,0)=0$. מההגדרה $f_x(0,0)=f_y(0,0)=0$, ולכן
    $$Q=\frac{f(h,k)}{\sqrt{h^2+k^2}}=\frac{r\cos^2\theta\sin\theta}{r}=\cos^2\theta\sin\theta,$$
    ואין בו $r$ בכלל: הערך תלוי בכיוון. לאורך $k=h>0$ הוא $\frac{1}{2\sqrt2}\neq0$. לכן $f$ <b>אינה</b> דיפרנציאבילית בראשית, אף שהיא רציפה שם.</div>
    <div class="lesson-trap">⚠️ כשהנגזרות החלקיות אינן אפס, אסור לשכוח לחסר $f_xh+f_yk$ בכותרת של $Q$. בלי זה נוצר ביטוי אחר, והמסקנה עלולה להיות הפוכה.</div>` },
  questions: [
    { id: "C07-Q1",
      step: { type: "numeric", prompt: String.raw`נתונה $f(x,y)=\dfrac{x^3}{x^2+y^2}$ ו-$f(0,0)=0$. מההגדרה $f_x(0,0)=1$ ו-$f_y(0,0)=0$. מהו הגבול של $Q(h,h)$ כאשר $h\to0^+$ (עשרוני, ארבע ספרות)?`,
              answer: -0.3536, tol: 0.001,
              explain: String.raw`$Q(h,h)=\frac{\frac{h^3}{2h^2}-0-1\cdot h-0}{\sqrt2\,h}=\frac{h/2-h}{\sqrt2\,h}=-\frac{1}{2\sqrt2}\approx-0.3536$.` },
      recap: "לא לשכוח לחסר $f_x h$." },
    { id: "C07-Q2",
      question: String.raw`מה אפשר להסיק מהתוצאה של השאלה הקודמת על $f(x,y)=\dfrac{x^3}{x^2+y^2}$?`,
      options: [
        { id: "a", value: "$f$ דיפרנציאבילית בראשית, כי יש לה נגזרות חלקיות" },
        { id: "b", value: "$f$ אינה דיפרנציאבילית, כי לאורך $k=h$ הגבול של $Q$ אינו $0$" },
        { id: "c", value: "$f$ דיפרנציאבילית, כי לאורך הצירים $Q\\to0$" },
        { id: "d", value: "אי אפשר להכריע בלי לבדוק עוד מסלול" },
      ],
      correctId: "b",
      explanation: String.raw`דיפרנציאביליות דורשת $Q\to0$ בכל מסלול. מסלול אחד עם ערך שונה מ-$0$ מפיל אותה. קיום נגזרות חלקיות אינו מספיק, ובדיקה של הצירים בלבד אינה מוכיחה כלום (לאורך הצירים $Q\equiv0$ כאן). אין צורך במסלול נוסף.`,
      recap: "מסלול אחד עם $Q\\not\\to0$ מספיק." },
    { id: "C07-Q3",
      step: { type: "numeric", prompt: String.raw`נתונה $f(x,y)=\dfrac{x^2y^2}{x^2+y^2}$ ו-$f(0,0)=0$. אפשר לראות ש-$f_x(0,0)=f_y(0,0)=0$, ולכן $Q=\dfrac{f(h,k)}{\sqrt{h^2+k^2}}=r^p\cos^2\theta\sin^2\theta$. מהו $p$?`,
              answer: 1, tol: 0,
              explain: String.raw`$f=r^2\cos^2\theta\sin^2\theta$, וחלוקה ב-$r$ נותנת $r^1$. כיוון ש-$|Q|\le r\to0$, הפונקציה דיפרנציאבילית בראשית.` },
      recap: "חזקה חיובית של $r$ ב-$Q$: דיפרנציאבילית." },
    { id: "C07-Q4",
      step: { type: "order", prompt: String.raw`סדרו את בדיקת הדיפרנציאביליות של $f(x,y)=\dfrac{x^2y^2}{x^2+y^2}$ עם $f(0,0)=0$ בראשית.`,
              lines: [
                String.raw`לפי ההגדרה: $f(h,0)=f(0,h)=0$, ולכן $f_x(0,0)=f_y(0,0)=0$.`,
                String.raw`בונים $Q(h,k)=\frac{f(h,k)-0-0\cdot h-0\cdot k}{\sqrt{h^2+k^2}}=\frac{f(h,k)}{\sqrt{h^2+k^2}}$.`,
                String.raw`עוברים לקוטביות: $Q=r\cos^2\theta\sin^2\theta$.`,
                String.raw`$|Q|\le r$, חסם שאינו תלוי ב-$\theta$ ושואף ל-$0$.`,
                String.raw`לכן $Q\to0$ ו-$f$ דיפרנציאבילית בראשית.`,
              ],
              explain: "כל שורה משתמשת בתוצאה של הקודמת: צריך את הנגזרות כדי לבנות את Q, את Q כדי לעבור לקוטביות, את הקוטביות כדי לחסום, ואת החסם כדי להסיק." },
      recap: "נגזרות, Q, קוטביות, חסם, מסקנה." },
    { id: "C07-Q5",
      step: { type: "findbug", prompt: String.raw`בבדיקת הדיפרנציאביליות של $f=\dfrac{x^3+y^3}{x^2+y^2}$ (עם $f(0,0)=0$) שורה אחת סותרת את ההגדרה של $Q$. איזו?`,
              lines: [
                String.raw`$f(h,0)=h$ ו-$f(0,h)=h$, ולכן $f_x(0,0)=f_y(0,0)=1$.`,
                String.raw`$Q(h,k)=\frac{f(h,k)}{\sqrt{h^2+k^2}}$.`,
                String.raw`בקוטביות: $Q=\cos^3\theta+\sin^3\theta-\cos\theta-\sin\theta$.`,
                String.raw`עבור $\theta=\frac\pi4$: $Q=\frac1{\sqrt2}-\sqrt2=-\frac1{\sqrt2}\neq0$.`,
                String.raw`לכן $Q\not\to0$ ו-$f$ אינה דיפרנציאבילית בראשית.`,
              ],
              bugIndex: 1,
              explain: String.raw`לפי ההגדרה יש לחסר את $f_x(0,0)\,h+f_y(0,0)\,k=h+k$ במונה: $Q=\frac{f(h,k)-h-k}{\sqrt{h^2+k^2}}$. השורה השנייה השמיטה אותו. שורות 3 ו-4 כבר משתמשות בצורה הנכונה.` },
      recap: "במונה של $Q$ מחסרים גם $f_xh+f_yk$." },
    { id: "C07-Q6",
      question: "איזה טיעון מוכיח שפונקציה מוגדרת בחלקים דיפרנציאבילית בראשית?",
      options: [
        { id: "a", value: "$Q\\to0$ לאורך ציר $x$, ציר $y$ והישר $y=x$" },
        { id: "b", value: "הפונקציה רציפה בראשית ויש לה שם נגזרות חלקיות" },
        { id: "c", value: "חסם $|Q|\\le Cr^p$ עם $p>0$ בקוטביות, הנכון לכל $\\theta$" },
        { id: "d", value: "הגבול של $f$ בראשית שווה ל-$f(0,0)$" },
      ],
      correctId: "c",
      explanation: String.raw`רק חסם שאינו תלוי ב-$\theta$ מכסה את כל המסלולים. שלושה מסלולים אינם מספיקים. רציפות ונגזרות חלקיות הן תנאים הכרחיים אבל לא מספיקים: ל-$\frac{x^2y}{x^2+y^2}$ יש את שניהם והיא אינה דיפרנציאבילית. ושוויון הגבול ל-$f(0,0)$ הוא רציפות בלבד.`,
      recap: "דיפרנציאביליות: חסם על $Q$ בקוטביות." },
  ],
});
