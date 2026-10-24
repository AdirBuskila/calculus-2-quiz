/* Series course, level 2: comparison and limit comparison (positive terms) */
const R = String.raw;
COURSE_LEVEL("series", {
  id: "C02", order: 2, icon: "⚖️", title: "השוואה והשוואה גבולית",
  goal: "לבחור טור p או טור הנדסי להשוואה, ולהכריע בהתכנסות בהחלט של טור עם גורם חסום.",
  source: "ai-verified",
  lesson: { html: R`
    <p>שני המבחנים הבאים עובדים <b>רק על טורים עם איברים אי-שליליים</b>. כדי להשתמש בהם על טור עם סימנים עוברים לערך מוחלט: בודקים את $\sum|a_n|$.</p>
    <div class="lesson-rule">🔑 <b>השוואה:</b> אם $0\le a_n\le b_n$ אז: $\sum b_n$ מתכנס $\Rightarrow$ $\sum a_n$ מתכנס, ו-$\sum a_n$ מתבדר $\Rightarrow$ $\sum b_n$ מתבדר. <b>הקטן נגרר אחרי הגדול כשהגדול מתכנס, והגדול נגרר אחרי הקטן כשהקטן מתבדר.</b></div>
    <div class="lesson-rule">🔑 <b>השוואה גבולית:</b> אם $a_n,b_n>0$ ו-$\lim\frac{a_n}{b_n}=L$ עם $0<L<\infty$, אז שני הטורים מתכנסים יחד או מתבדרים יחד.</div>
    <h3>המתכון</h3>
    <ul>
    <li>מוצאים את האיבר <b>הדומיננטי</b> במונה ובמכנה: $\frac{n+1}{n^3+5}\approx\frac{n}{n^3}=\frac1{n^2}$.</li>
    <li>בוחרים $b_n=\frac1{n^p}$ בהתאם, ומחשבים את $\lim\frac{a_n}{b_n}$.</li>
    <li>גורם חסום כמו $\sin n$, $\cos n$, $(-1)^n$ או $2+\cos n$ לא מפריע: חוסמים אותו. למשל $2+\cos n\le3$.</li>
    </ul>
    <div class="lesson-ex">דוגמה: $\sum\dfrac{3+\sin\sqrt n}{n^2}$. מכיוון ש-$3+\sin\sqrt n\le4$ מתקיים $\frac{3+\sin\sqrt n}{n^2}\le\frac4{n^2}$, והטור $\sum\frac4{n^2}$ מתכנס (טור p עם $p=2$). לכן הטור מתכנס.</div>
    <div class="lesson-trap">⚠️ חסם מלמעלה על ידי טור <b>מתבדר</b> לא אומר כלום: $\frac1{n^2}\le\frac1n$ ו-$\sum\frac1n$ מתבדר, אבל $\sum\frac1{n^2}$ מתכנס. מי שרוצה להוכיח התבדרות חייב חסם <b>מלמטה</b> על ידי טור מתבדר.</div>` },
  questions: [
    { id: "C02-Q1",
      question: R`עם איזה טור כדאי להשוות גבולית את הטור $\displaystyle\sum_{n=1}^{\infty}\frac{n+1}{n^3+5}$ ?`,
      options: [{ id: "a", value: R`$\displaystyle\sum\frac{1}{n}$` }, { id: "b", value: R`$\displaystyle\sum\frac{1}{n^3}$` }, { id: "c", value: R`$\displaystyle\sum\frac{1}{n^4}$` }, { id: "d", value: R`$\displaystyle\sum\frac{1}{n^2}$` }],
      correctId: "d",
      explanation: R`הדומיננטי במונה הוא $n$ ובמכנה $n^3$, ולכן הטור דומה ל-$\frac1{n^2}$. אכן $\frac{(n+1)/(n^3+5)}{1/n^2}\to1$, גבול חיובי וסופי. עם $\frac1n$ הגבול הוא $0$ ועם $\frac1{n^3}$ ועם $\frac1{n^4}$ הוא $\infty$, ולכן שם ההשוואה הגבולית לא חלה.`,
      recap: R`בוחרים $b_n$ מהאיברים הדומיננטיים, כך שהגבול חיובי וסופי` },
    { id: "C02-Q2",
      step: { type: "numeric", prompt: R`מהו הגבול $\displaystyle\lim_{n\to\infty}\frac{a_n}{1/n^2}$ עבור $a_n=\dfrac{2n^2+1}{n^4+n}$ ?`, answer: 2, tol: 0,
        explain: R`$\dfrac{a_n}{1/n^2}=\dfrac{(2n^2+1)\,n^2}{n^4+n}=\dfrac{2n^4+n^2}{n^4+n}\to2$. הגבול חיובי וסופי, וגם $\sum\frac1{n^2}$ מתכנס, ולכן $\sum a_n$ מתכנס.` },
      recap: R`הגבול בהשוואה גבולית צריך להיות בין $0$ ל-$\infty$` },
    { id: "C02-Q3",
      question: R`מה הסיווג של הטור $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^n(2+\cos n)}{n^2}$ ?`,
      options: [{ id: "a", value: "מתכנס בתנאי" }, { id: "b", value: "מתכנס בהחלט" }, { id: "c", value: "מתבדר" }],
      correctId: "b",
      explanation: R`בודקים את הערך המוחלט: $\left|\frac{(-1)^n(2+\cos n)}{n^2}\right|=\frac{2+\cos n}{n^2}\le\frac3{n^2}$, והטור $\sum\frac3{n^2}$ מתכנס. לפי מבחן ההשוואה הטור מתכנס בהחלט. מכיוון שכבר יש התכנסות בהחלט, "בתנאי" שגוי, ואין צורך בלייבניץ.`,
      recap: R`גורם חסום במונה: חוסמים ומשווים לטור p` },
    { id: "C02-Q4",
      question: R`מה הסיווג של הטור $\displaystyle\sum_{n=1}^{\infty}\frac{1}{\sqrt{n^2+n}}$ ?`,
      options: [{ id: "a", value: "מתכנס בהחלט" }, { id: "b", value: "מתכנס בתנאי" }, { id: "c", value: "מתבדר" }],
      correctId: "c",
      explanation: R`האיברים חיוביים. $\frac{1/\sqrt{n^2+n}}{1/n}=\frac{n}{\sqrt{n^2+n}}\to1$, ו-$\sum\frac1n$ מתבדר, ולכן לפי השוואה גבולית הטור מתבדר. הטור חיובי, לכן אין אפשרות ל"התכנסות בתנאי".`,
      recap: R`$\sqrt{n^2+n}\sim n$, ולכן משווים ל-$\frac1n$` },
    { id: "C02-Q5",
      step: { type: "findbug", prompt: R`בנימוק הבא מנסים להוכיח ש-$\sum\frac{1}{\sqrt n+1}$ מתבדר. מצאו את השורה הראשונה שבה הנימוק שגוי.`,
        lines: [
          R`נבדוק את הטור $\sum_{n=1}^{\infty}\frac{1}{\sqrt n+1}$.`,
          R`לכל $n\ge1$ מתקיים $\frac{1}{\sqrt n+1}\le\frac{1}{\sqrt n}$.`,
          R`הטור $\sum\frac1{\sqrt n}$ מתבדר (טור p עם $p=\frac12\le1$).`,
          R`מכיוון שהטור הגדול מתבדר, גם הטור הקטן ממנו מתבדר.`,
          R`לכן $\sum\frac{1}{\sqrt n+1}$ מתבדר.`,
        ],
        bugIndex: 3,
        explain: R`התבדרות עוברת רק מהקטן אל הגדול ולא להפך: $\frac1{n^2}\le\frac1n$ ו-$\sum\frac1n$ מתבדר, אבל $\sum\frac1{n^2}$ מתכנס. הדרך הנכונה כאן היא השוואה גבולית עם $\frac1{\sqrt n}$: $\frac{\sqrt n}{\sqrt n+1}\to1$, ולכן הטור מתבדר.` },
      recap: R`רוצים התבדרות? חסם מלמטה על ידי טור מתבדר` },
    { id: "C02-Q6",
      question: R`איזה חסם מוכיח שהטור $\sum_{n=1}^{\infty}\frac{\sin n}{n^2}$ מתכנס בהחלט?`,
      options: [
        { id: "a", value: R`$\dfrac{\sin n}{n^2}\le\dfrac1n$` },
        { id: "b", value: R`$\dfrac{\sin n}{n^2}\ge-\dfrac{1}{n^2}$` },
        { id: "c", value: R`$\left|\dfrac{\sin n}{n^2}\right|\le\dfrac{1}{n^2}$` },
        { id: "d", value: R`$\left|\dfrac{\sin n}{n^2}\right|\ge\dfrac{1}{n^2}$` }],
      correctId: "c",
      explanation: R`צריך חסם מלמעלה על הערך המוחלט על ידי טור מתכנס: $|\sin n|\le1$ נותן $\left|\frac{\sin n}{n^2}\right|\le\frac1{n^2}$, ו-$\sum\frac1{n^2}$ מתכנס. החסם $\le\frac1n$ נכון אך הטור $\sum\frac1n$ מתבדר, ולכן הוא לא מוכיח כלום. החסם $\ge-\frac1{n^2}$ הוא חסם מלמטה על הטור עצמו, ללא ערך מוחלט, ולכן אינו מועיל. החסם $\ge\frac1{n^2}$ לא נכון (למשל $\sin n$ קרוב ל-$0$ בחלק מהערכים).`,
      recap: R`חוסמים את $|a_n|$ מלמעלה על ידי טור מתכנס` },
  ],
});
