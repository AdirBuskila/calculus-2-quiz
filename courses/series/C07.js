/* Series course, level 7: Maclaurin series from the table, domain, f^(k)(0) from the coefficients */
const R = String.raw;
COURSE_LEVEL("series", {
  id: "C07", order: 7, icon: "📐", title: "מקלורן מהטבלה ו-f^(k)(0) מהמקדמים",
  goal: "לפתח פונקציה לטור מקלורן מהטבלה, לקבוע את תחום ההתכנסות, ולחלץ נגזרת מסדר גבוה ב-0 מהמקדם.",
  source: "ai-verified",
  lesson: { html: R`
    <p>טור מקלורן של $f$ הוא טור החזקות של $f$ סביב $0$. כמעט אף פעם לא גוזרים שוב ושוב: <b>משתמשים בטבלה</b> ומציבים.</p>
    <table><thead><tr><th>הפונקציה</th><th>הטור</th><th>תחום</th></tr></thead><tbody>
    <tr><td>$e^x$</td><td>$\sum_{n=0}^{\infty}\frac{x^n}{n!}$</td><td>כל $x$</td></tr>
    <tr><td>$\sin x$</td><td>$\sum_{n=0}^{\infty}\frac{(-1)^nx^{2n+1}}{(2n+1)!}$</td><td>כל $x$</td></tr>
    <tr><td>$\cos x$</td><td>$\sum_{n=0}^{\infty}\frac{(-1)^nx^{2n}}{(2n)!}$</td><td>כל $x$</td></tr>
    <tr><td>$\frac1{1-x}$</td><td>$\sum_{n=0}^{\infty}x^n$</td><td>$|x|<1$</td></tr>
    <tr><td>$\ln(1+x)$</td><td>$\sum_{n=1}^{\infty}\frac{(-1)^{n+1}x^n}{n}$</td><td>$-1<x\le1$</td></tr>
    </tbody></table>
    <div class="lesson-rule">🔑 <b>הצבה:</b> בטור של $g(u)$ מחליפים $u$ ב-$cx$ או ב-$x^2$. התחום מתקבל מהתנאי שהביטוי המוצב נמצא בתחום של הטבלה. למשל $\ln(1+3x)$ מתכנס כש-$-1<3x\le1$, כלומר $-\frac13<x\le\frac13$. <b>סכום</b> של טורים מתכנס בחיתוך התחומים, ושברים חלקיים הופכים פונקציה רציונלית לסכום של $\frac1{1-cx}$.</div>
    <div class="lesson-rule">🔑 <b>המקדם והנגזרת:</b> אם $f(x)=\sum a_nx^n$ אז $a_k=\dfrac{f^{(k)}(0)}{k!}$, כלומר $f^{(k)}(0)=k!\,a_k$. מוצאים את מקדם $x^k$ בטור ומכפילים ב-$k!$.</div>
    <div class="lesson-ex">דוגמה: $f(x)=e^{2x}=\sum\frac{2^nx^n}{n!}$ ולכן $a_5=\frac{2^5}{5!}$ ו-$f^{(5)}(0)=5!\cdot\frac{2^5}{5!}=32$.</div>
    <div class="lesson-trap">⚠️ הערך $f^{(k)}(0)$ הוא $k!\,a_k$ ולא $a_k$ עצמו. ואם החזקות בטור הן $x^{n+2}$, מקדם $x^5$ מתקבל מ-$n=3$.</div>` },
  questions: [
    { id: "C07-Q1",
      question: R`מהו טור מקלורן של $\dfrac{1}{1+2x}$ ולאילו $x$ הוא מתכנס?`,
      options: [
        { id: "a", value: R`$\sum_{n=0}^{\infty}(-2)^nx^n$ עבור $|x|<2$` },
        { id: "b", value: R`$\sum_{n=0}^{\infty}2^nx^n$ עבור $|x|<\frac12$` },
        { id: "c", value: R`$\sum_{n=0}^{\infty}\frac{(-1)^n}{2^n}x^n$ עבור $|x|<2$` },
        { id: "d", value: R`$\sum_{n=0}^{\infty}(-2)^nx^n$ עבור $|x|<\frac12$` }],
      correctId: "d",
      explanation: R`$\frac1{1+2x}=\frac1{1-(-2x)}=\sum(-2x)^n=\sum(-2)^nx^n$, בתנאי ש-$|-2x|<1$, כלומר $|x|<\frac12$. הטור עם $2^n$ מתאים ל-$\frac1{1-2x}$. הרדיוס $2$ מתקבל מטעות בהצבה: ההצבה $u=2x$ מכווצת את התחום ולא מרחיבה אותו.`,
      recap: R`$\frac{1}{1+cx}$: מנה $-cx$, ו-$|x|<\frac1{|c|}$` },
    { id: "C07-Q2",
      step: { type: "numeric", prompt: R`נתונה $f(x)=x^2e^x$. מהו $f^{(5)}(0)$ ?`, answer: 20, tol: 0,
        explain: R`$x^2e^x=\sum_{n=0}^{\infty}\frac{x^{n+2}}{n!}$. מקדם $x^5$ מתקבל מ-$n=3$ ושווה ל-$\frac1{3!}=\frac16$. לכן $f^{(5)}(0)=5!\cdot\frac16=20$.` },
      recap: R`$f^{(k)}(0)=k!\cdot$ (מקדם $x^k$)` },
    { id: "C07-Q3",
      step: { type: "numeric", prompt: R`נתונה $f(x)=\sin(x^2)$. מהו $f^{(6)}(0)$ ?`, answer: -120, tol: 0,
        explain: R`$\sin(x^2)=x^2-\frac{x^6}{3!}+\frac{x^{10}}{5!}-\cdots$. מקדם $x^6$ הוא $-\frac16$, ולכן $f^{(6)}(0)=6!\cdot\left(-\frac16\right)=-120$.` },
      recap: R`מציבים $x^2$ בטבלת $\sin$ ומחפשים את החזקה` },
    { id: "C07-Q4",
      question: R`לאילו $x$ מתכנס טור מקלורן של $\ln(1+3x)$ ?`,
      options: [
        { id: "a", value: R`$-\frac13\le x\le\frac13$` },
        { id: "b", value: R`$-1<x\le1$` },
        { id: "c", value: R`$-\frac13<x\le\frac13$` },
        { id: "d", value: R`$-\frac13\le x<\frac13$` }],
      correctId: "c",
      explanation: R`הטור של $\ln(1+u)$ מתכנס עבור $-1<u\le1$. מציבים $u=3x$ ומקבלים $-\frac13<x\le\frac13$. ב-$x=\frac13$ מתקבל $\sum\frac{(-1)^{n+1}}{n}$ שמתכנס (לייבניץ), וב-$x=-\frac13$ מתקבל מינוס הטור ההרמוני שמתבדר. לכן הקצה הימני סגור והשמאלי פתוח.`,
      recap: R`$\ln(1+u)$: $-1<u\le1$, ואז מציבים` },
    { id: "C07-Q5",
      step: { type: "numeric", prompt: R`נתונה $f(x)=\dfrac{1}{(1-x)(1-2x)}$. מהו $f^{(4)}(0)$ ? (רמז: פירוק לשברים חלקיים).`, answer: 744, tol: 0,
        explain: R`$\frac1{(1-x)(1-2x)}=\frac{2}{1-2x}-\frac1{1-x}=\sum\left(2\cdot2^n-1\right)x^n$. המקדם של $x^4$ הוא $2^5-1=31$, ולכן $f^{(4)}(0)=4!\cdot31=24\cdot31=744$.` },
      recap: R`שברים חלקיים: סכום של שני טורים הנדסיים` },
    { id: "C07-Q6",
      question: R`לאילו $x$ מתכנס טור מקלורן של $f(x)=\dfrac{1}{(1-x)(1-2x)}$ ?`,
      options: [{ id: "a", value: R`$|x|\le\frac12$` }, { id: "b", value: R`$|x|<1$` }, { id: "c", value: R`$|x|<\frac12$` }, { id: "d", value: R`$|x|<2$` }],
      correctId: "c",
      explanation: R`הטור הוא סכום של $\sum2\cdot2^nx^n$ (מתכנס עבור $|x|<\frac12$) ושל $\sum x^n$ (מתכנס עבור $|x|<1$), ולכן הסכום מתכנס בחיתוך: $|x|<\frac12$. בקצוות $x=\pm\frac12$ המקדם $(2^{n+1}-1)\cdot2^{-n}$ שואף ל-$2$ ולא ל-$0$, והטור מתבדר, ולכן $|x|\le\frac12$ שגוי.`,
      recap: R`סכום טורים: חיתוך התחומים, ובדיקת הקצוות` },
  ],
});
