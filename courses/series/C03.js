/* Series course, level 3: ratio test, root test, integral test */
const R = String.raw;
COURSE_LEVEL("series", {
  id: "C03", order: 3, icon: "🔬", title: "מבחן המנה, השורש והאינטגרל",
  goal: "לבחור בין מבחן המנה, השורש והאינטגרל לפי צורת האיבר הכללי, ולדעת מתי המבחן לא מכריע.",
  source: "ai-verified",
  lesson: { html: R`
    <p>כשאין טור p או טור הנדסי ברור להשוות אליו, בוחרים מבחן לפי <b>צורת האיבר הכללי</b>.</p>
    <table><thead><tr><th>צורת האיבר</th><th>המבחן</th></tr></thead><tbody>
    <tr><td>עצרת $n!$ או חזקה $c^n$</td><td>מנה (דלאמבר)</td></tr>
    <tr><td>הכול בחזקת $n$, כמו $\left(\frac{n}{2n+1}\right)^n$</td><td>שורש (קושי)</td></tr>
    <tr><td>$\ln n$ במכנה, כמו $\frac1{n\ln n}$</td><td>אינטגרל</td></tr>
    </tbody></table>
    <div class="lesson-rule">🔑 <b>מנה:</b> $D=\lim\left|\dfrac{a_{n+1}}{a_n}\right|$. <b>שורש:</b> $c=\lim\sqrt[n]{|a_n|}$. בשניהם: הערך קטן מ-$1$ $\Rightarrow$ מתכנס בהחלט, גדול מ-$1$ $\Rightarrow$ מתבדר, שווה ל-$1$ $\Rightarrow$ <b>אין מידע</b>.</div>
    <div class="lesson-trap">⚠️ כש-$D=1$ או $c=1$ המבחן לא מכריע. גם $\sum\frac1n$ וגם $\sum\frac1{n^2}$ נותנים $D=1$, ובכל זאת הראשון מתבדר והשני מתכנס. עוברים אז להשוואה או לאינטגרל.</div>
    <div class="lesson-rule">🔑 <b>מבחן האינטגרל:</b> אם $f$ חיובית, רציפה ויורדת ב-$[N,\infty)$ ו-$a_n=f(n)$, אז $\sum a_n$ ו-$\int_N^{\infty}f(x)\,dx$ מתכנסים או מתבדרים יחד.</div>
    <div class="lesson-ex">דוגמה: $\sum_{n=2}^{\infty}\dfrac{1}{n\ln n}$. נציב $t=\ln x$ ונקבל $\int_2^M\frac{dx}{x\ln x}=\ln\ln M-\ln\ln2\to\infty$, ולכן הטור מתבדר. לעומת זאת $\int_2^M\frac{dx}{x(\ln x)^2}=\frac1{\ln2}-\frac1{\ln M}\to\frac1{\ln2}$, ולכן $\sum\frac1{n(\ln n)^2}$ מתכנס.</div>` },
  questions: [
    { id: "C03-Q1",
      step: { type: "numeric", prompt: R`מהו $\displaystyle D=\lim_{n\to\infty}\frac{a_{n+1}}{a_n}$ עבור $a_n=\dfrac{n^2}{2^n}$ ?`, answer: 0.5, tol: 0,
        explain: R`$\dfrac{a_{n+1}}{a_n}=\dfrac{(n+1)^2}{2^{n+1}}\cdot\dfrac{2^n}{n^2}=\dfrac12\left(\dfrac{n+1}{n}\right)^2\to\dfrac12$. מכיוון ש-$D<1$, הטור מתכנס בהחלט.` },
      recap: R`במנה החזקות $c^n$ נותנות את הגבול` },
    { id: "C03-Q2",
      question: R`מה הסיווג של הטור $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^n\,3^n}{n!}$ ?`,
      options: [{ id: "a", value: "מתכנס בהחלט" }, { id: "b", value: "מתכנס בתנאי" }, { id: "c", value: "מתבדר" }],
      correctId: "a",
      explanation: R`נבדוק את הערך המוחלט במבחן המנה: $\dfrac{3^{n+1}/(n+1)!}{3^n/n!}=\dfrac{3}{n+1}\to0<1$. לכן $\sum\frac{3^n}{n!}$ מתכנס, והטור המקורי מתכנס בהחלט. אין צורך בלייבניץ.`,
      recap: R`עצרת וחזקה: מנה, ובערך מוחלט` },
    { id: "C03-Q3",
      question: R`מה נותן מבחן השורש לטור $\displaystyle\sum_{n=1}^{\infty}\left(\frac{n}{2n+1}\right)^n$ ?`,
      options: [
        { id: "a", value: R`$c=2$, ולכן הטור מתבדר` },
        { id: "b", value: R`$c=1$, ולכן אין מידע` },
        { id: "c", value: R`$c=\frac12$, ולכן הטור מתבדר` },
        { id: "d", value: R`$c=\frac12$, ולכן הטור מתכנס` }],
      correctId: "d",
      explanation: R`$\sqrt[n]{\left(\frac{n}{2n+1}\right)^n}=\frac{n}{2n+1}\to\frac12<1$, ולכן הטור מתכנס. התוצאה $c=2$ היא ההפוך של התוצאה הנכונה, ו-$c=1$ מתקבל רק אם שוכחים את ה-$2$ שבמכנה. עם $c=\frac12$ הטור לא יכול להתבדר, כי מתבדרים רק כש-$c>1$.`,
      recap: R`הכול בחזקת $n$: שורש, ו-$c<1$ מתכנס` },
    { id: "C03-Q4",
      question: R`במבחן המנה התקבל $D=1$. מה אפשר להסיק?`,
      options: [
        { id: "a", value: "הטור מתכנס, כי $D\\le1$" },
        { id: "b", value: "הטור מתבדר, כי $D\\ge1$" },
        { id: "c", value: "הטור מתכנס בתנאי" },
        { id: "d", value: "אי אפשר להסיק: יש גם טורים מתכנסים וגם טורים מתבדרים עם $D=1$" }],
      correctId: "d",
      explanation: R`עבור $\sum\frac1n$ וגם עבור $\sum\frac1{n^2}$ מתקבל $D=1$, אבל הראשון מתבדר והשני מתכנס, ולכן $D=1$ לא קובע. הכללים "מתכנס אם $D<1$" ו-"מתבדר אם $D>1$" הם עם אי-שוויון חזק. המבחן גם לא עוסק בהתכנסות בתנאי.`,
      recap: R`$D=1$ או $c=1$: אין מידע` },
    { id: "C03-Q5",
      question: R`מה הסיווג של הטור $\displaystyle\sum_{n=2}^{\infty}\frac{1}{n(\ln n)^3}$ ?`,
      options: [{ id: "a", value: "מתבדר" }, { id: "b", value: "מתכנס בתנאי" }, { id: "c", value: "מתכנס בהחלט" }],
      correctId: "c",
      explanation: R`האיברים חיוביים ו-$f(x)=\frac1{x(\ln x)^3}$ יורדת. $\int_2^M\frac{dx}{x(\ln x)^3}=\frac1{2(\ln2)^2}-\frac1{2(\ln M)^2}$ שואף למספר סופי, ולכן הטור מתכנס. הטור חיובי, ולכן מתכנס בהחלט ולא "בתנאי". מבחן המנה לא עוזר כאן ($D=1$).`,
      recap: R`$\ln$ במכנה: אינטגרל, והחזקה של $\ln$ קובעת` },
    { id: "C03-Q6",
      step: { type: "order", prompt: R`סדרו את ההוכחה ש-$\sum_{n=2}^{\infty}\frac{1}{n\ln n}$ מתבדר, לפי מבחן האינטגרל.`,
        lines: [
          R`נגדיר $f(x)=\frac1{x\ln x}$ ב-$[2,\infty)$: היא חיובית, רציפה ויורדת, ו-$f(n)=a_n$.`,
          R`נחשב $\int_2^M\frac{dx}{x\ln x}=\ln\ln M-\ln\ln2$.`,
          R`כש-$M\to\infty$ מתקבל $\ln\ln M\to\infty$, כלומר האינטגרל $\int_2^{\infty}f$ מתבדר.`,
          R`לפי מבחן האינטגרל גם הטור $\sum_{n=2}^{\infty}\frac1{n\ln n}$ מתבדר.`,
        ],
        explain: R`קודם בודקים שמותר להשתמש במבחן (חיובית, רציפה, יורדת), אחר כך מחשבים את האינטגרל, אחר כך לוקחים גבול, ורק בסוף מסיקים על הטור.` },
      recap: R`אינטגרל: תנאים, חישוב, גבול, מסקנה` },
  ],
});
