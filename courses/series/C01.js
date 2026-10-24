/* Series course, level 1: partial sums, the necessary condition, geometric and p-series.
   Every answer is asserted in tools/verify/needhelp/series/check.py */
const R = String.raw;
COURSE_LEVEL("series", {
  id: "C01", order: 1, icon: "🧱", title: "תנאי הכרחי, טור הנדסי וטור p",
  goal: "להכריע מיד כשהאיבר הכללי לא שואף ל-0, ולזהות טור הנדסי וטור p.",
  source: "ai-verified",
  lesson: { html: R`
    <p><b>טור</b> $\sum_{n=1}^{\infty}a_n$ הוא הגבול של הסכומים החלקיים $S_N=a_1+\dots+a_N$. אם הגבול קיים וסופי, הטור <b>מתכנס</b>; אחרת הוא <b>מתבדר</b>.</p>
    <div class="lesson-rule">🔑 <b>התנאי ההכרחי:</b> אם $\sum a_n$ מתכנס אז $a_n\to0$. לכן אם $a_n\not\to0$ הטור <b>מתבדר</b>, וזה הצעד הראשון בכל סיווג.</div>
    <div class="lesson-trap">⚠️ ההפך לא נכון: $\frac1n\to0$ ובכל זאת $\sum\frac1n$ מתבדר. אם $a_n\to0$ עדיין לא ידוע כלום, וצריך מבחן נוסף.</div>
    <h3>שני טורים שמכירים בעל פה</h3>
    <ul>
    <li><b>טור הנדסי</b> $\sum q^n$: מתכנס אם ורק אם $|q|<1$. הסכום הוא $\dfrac{a_1}{1-q}$, כאשר $a_1$ הוא האיבר הראשון בטור.</li>
    <li><b>טור p</b> $\sum\dfrac1{n^p}$: מתכנס אם ורק אם $p>1$. למשל $\sum\frac1{\sqrt n}$ ו-$\sum\frac1n$ מתבדרים, ו-$\sum\frac1{n^2}$ מתכנס.</li>
    </ul>
    <div class="lesson-ex">דוגמה: $\sum_{n=1}^{\infty}\dfrac{2}{3^n}$ הוא הנדסי עם איבר ראשון $\frac23$ ומנה $q=\frac13$, ולכן סכומו $\dfrac{2/3}{1-1/3}=1$. ואילו $\sum\dfrac{n}{n+1}$ מתבדר כי $\frac{n}{n+1}\to1\ne0$.</div>
    <div class="lesson-rule">🔑 שינוי של מספר סופי של איברים (או התחלה מ-$n$ אחר) לא משנה את ההתכנסות, אבל כן משנה את הסכום. בסכום תמיד מתחילים מהאיבר הראשון שבטור.</div>` },
  questions: [
    { id: "C01-Q1",
      question: R`מה הסיווג של הטור $\displaystyle\sum_{n=1}^{\infty}\frac{n^2+1}{2n^2+3}$ ?`,
      options: [{ id: "a", value: "מתכנס בהחלט" }, { id: "b", value: "מתכנס בתנאי" }, { id: "c", value: "מתבדר" }],
      correctId: "c",
      explanation: R`האיבר הכללי שואף ל-$\frac12$ ולא ל-$0$, ולכן התנאי ההכרחי לא מתקיים והטור מתבדר. הטור גם לא מתכנס בהחלט וגם לא בתנאי, כי בשני המקרים הוא היה צריך להתכנס.`,
      recap: R`אם $a_n\not\to0$ הטור מתבדר` },
    { id: "C01-Q2",
      step: { type: "numeric", prompt: R`מהו הסכום $\displaystyle\sum_{n=1}^{\infty}\frac{5}{3^n}$ ?`, answer: 2.5, tol: 0,
        explain: R`זה טור הנדסי עם איבר ראשון $\frac53$ ומנה $\frac13$. הסכום הוא $\dfrac{5/3}{1-1/3}=\dfrac52=2.5$.` },
      recap: R`הנדסי: איבר ראשון חלקי $(1-q)$` },
    { id: "C01-Q3",
      step: { type: "numeric", prompt: R`מהו הסכום $\displaystyle\sum_{n=2}^{\infty}\frac{1}{3^n}$ ? (שימו לב: הטור מתחיל מ-$n=2$. אפשר לכתוב שבר, למשל 1/6).`, answer: 0.16666666666666666, tol: 0.001,
        explain: R`האיבר הראשון הוא $\frac19$ (ולא $\frac13$) והמנה $\frac13$, ולכן הסכום הוא $\dfrac{1/9}{1-1/3}=\dfrac16$. התוצאה $\frac12$ מתקבלת אם מתחילים מ-$n=1$ בטעות.` },
      recap: R`האיבר הראשון הוא זה שבטור, לא $q^1$` },
    { id: "C01-Q4",
      question: R`עבור אילו ערכי $x$ מתכנס הטור $\displaystyle\sum_{n=0}^{\infty}\left(\frac{x}{4}\right)^n$ ?`,
      options: [{ id: "a", value: R`$|x|\le4$` }, { id: "b", value: R`$|x|<\frac14$` }, { id: "c", value: R`$x<4$` }, { id: "d", value: R`$|x|<4$` }],
      correctId: "d",
      explanation: R`הטור הנדסי עם מנה $q=\frac x4$, ומתכנס בדיוק כש-$|q|<1$, כלומר $|x|<4$. ב-$x=4$ כל האיברים שווים ל-$1$ וב-$x=-4$ הם $(-1)^n$: האיבר לא שואף ל-$0$, ולכן הקצוות מתבדרים ו-$|x|\le4$ שגוי. התנאי $x<4$ שגוי כי לדוגמה $x=-10$ נותן $q=-2.5$.`,
      recap: R`הנדסי מתכנס רק כש-$|q|<1$ (קצוות מתבדרים)` },
    { id: "C01-Q5",
      question: R`איזה מהטורים הבאים מתכנס?`,
      options: [{ id: "a", value: R`$\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\sqrt n}$` }, { id: "b", value: R`$\displaystyle\sum_{n=1}^{\infty}\frac{1}{\sqrt n}$` },
                { id: "c", value: R`$\displaystyle\sum_{n=1}^{\infty}\frac{1}{n}$` }, { id: "d", value: R`$\displaystyle\sum_{n=1}^{\infty}\frac{n}{n+1}$` }],
      correctId: "a",
      explanation: R`$\frac1{n\sqrt n}=\frac1{n^{3/2}}$ הוא טור p עם $p=\frac32>1$, ולכן מתכנס. הטור $\sum\frac1{\sqrt n}$ הוא טור p עם $p=\frac12\le1$, $\sum\frac1n$ הוא הטור ההרמוני ($p=1$), ושניהם מתבדרים. האיבר $\frac n{n+1}$ שואף ל-$1$, ולכן הטור האחרון מתבדר כבר מהתנאי ההכרחי.`,
      recap: R`טור p מתכנס רק אם $p>1$` },
    { id: "C01-Q6",
      step: { type: "findbug", prompt: R`בנימוק הבא מנסים להכריע בהתכנסות של $\sum\frac1n$. מצאו את השורה הראשונה שבה הנימוק שגוי.`,
        lines: [
          R`נבדוק אם הטור $\sum_{n=1}^{\infty}\frac1n$ מתכנס.`,
          R`האיבר הכללי $\frac1n$ שואף ל-$0$.`,
          R`לפי המשפט, אם האיבר הכללי שואף ל-$0$ אז הטור מתכנס.`,
          R`לכן הטור $\sum\frac1n$ מתכנס.`,
        ],
        bugIndex: 2,
        explain: R`המשפט הנכון הוא ההפוך: אם הטור מתכנס אז האיבר הכללי שואף ל-$0$. שאיפת האיבר ל-$0$ היא תנאי הכרחי בלבד, ו-$\sum\frac1n$ מתבדר (טור p עם $p=1$), כך שהשורה האחרונה היא רק תוצאה של הטעות.` },
      recap: R`$a_n\to0$ הכרחי, לא מספיק` },
  ],
});
