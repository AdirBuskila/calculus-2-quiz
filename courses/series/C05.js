/* Series course, level 5: radius of convergence by ratio and root */
const R = String.raw;
COURSE_LEVEL("series", {
  id: "C05", order: 5, icon: "📏", title: "רדיוס התכנסות: דלאמבר וקושי-הדמר",
  goal: "לחשב רדיוס התכנסות ומרכז של טור חזקות, כולל טורים עם הזזה וחזקות זוגיות בלבד.",
  source: "ai-verified",
  lesson: { html: R`
    <p><b>טור חזקות</b> סביב $x_0$ הוא $\sum a_n(x-x_0)^n$. יש לו <b>רדיוס התכנסות</b> $R$ ($0\le R\le\infty$) כך שהטור מתכנס בהחלט כש-$|x-x_0|<R$ ומתבדר כש-$|x-x_0|>R$. מה קורה בקצוות $x_0\pm R$ נבדק בנפרד (השלב הבא).</p>
    <div class="lesson-rule">🔑 <b>דלאמבר:</b> $R=\lim\left|\dfrac{a_n}{a_{n+1}}\right|$ (איבר $n$ חלקי איבר $n+1$). <b>קושי-הדמר:</b> $\dfrac1R=\lim\sqrt[n]{|a_n|}$. משתמשים בדלאמבר כשיש עצרת או חזקות, ובקושי-הדמר כשכל האיבר בחזקת $n$.</div>
    <div class="lesson-trap">⚠️ בדלאמבר המנה היא $\frac{a_n}{a_{n+1}}$, ולכן מקבלים את $R$ עצמו. אם התהפך לכם הכיוון, התקבל $\frac1R$ ולא $R$.</div>
    <h3>שלוש טכניקות</h3>
    <ul>
    <li><b>הזזה:</b> בטור $\sum\frac{(x+1)^n}{n2^n}$ המרכז הוא $-1$. מסמנים $X=x+1$ ומחשבים רדיוס ב-$X$.</li>
    <li><b>חזקות זוגיות בלבד:</b> בטור $\sum a_nx^{2n}$ מציבים $t=x^2$, מחשבים $R_t$, ואז $R_x=\sqrt{R_t}$.</li>
    <li><b>מקרים קיצוניים:</b> אם $\frac{a_n}{a_{n+1}}\to\infty$ אז $R=\infty$ (מתכנס לכל $x$). אם $\to0$ אז $R=0$ (מתכנס רק במרכז).</li>
    </ul>
    <div class="lesson-ex">דוגמה: $\sum\frac{x^n}{n\,2^n}$. כאן $a_n=\frac1{n2^n}$ ולכן $\frac{a_n}{a_{n+1}}=\frac{(n+1)2^{n+1}}{n2^n}=2\cdot\frac{n+1}{n}\to2$, כלומר $R=2$.</div>` },
  questions: [
    { id: "C05-Q1",
      step: { type: "numeric", prompt: R`מהו רדיוס ההתכנסות של $\displaystyle\sum_{n=1}^{\infty}\frac{x^n}{n\cdot3^n}$ ?`, answer: 3, tol: 0,
        explain: R`$a_n=\frac1{n3^n}$ ולכן $\frac{a_n}{a_{n+1}}=\frac{(n+1)3^{n+1}}{n\,3^n}=3\cdot\frac{n+1}{n}\to3$. הרדיוס הוא $3$.` },
      recap: R`דלאמבר: $R=\lim\left|\frac{a_n}{a_{n+1}}\right|$` },
    { id: "C05-Q2",
      question: R`מהו רדיוס ההתכנסות של $\displaystyle\sum_{n=1}^{\infty}\frac{n!}{n^n}\,x^n$ ?`,
      options: [{ id: "a", value: R`$\dfrac1e$` }, { id: "b", value: R`$1$` }, { id: "c", value: R`$e$` }, { id: "d", value: R`$\infty$` }],
      correctId: "c",
      explanation: R`$\dfrac{a_n}{a_{n+1}}=\dfrac{n!}{n^n}\cdot\dfrac{(n+1)^{n+1}}{(n+1)!}=\dfrac{(n+1)^n}{n^n}=\left(1+\frac1n\right)^n\to e$, ולכן $R=e$. התוצאה $\frac1e$ מתקבלת אם הופכים את המנה (זה $\frac1R$), ואילו $1$ ו-$\infty$ אינם מתאימים לגבול שחישבנו.`,
      recap: R`$\left(1+\frac1n\right)^n\to e$` },
    { id: "C05-Q3",
      step: { type: "numeric", prompt: R`מהו רדיוס ההתכנסות של $\displaystyle\sum_{n=1}^{\infty}\frac{4^n+1}{5^n}\,x^n$ ? (אפשר לכתוב שבר או עשרוני).`, answer: 1.25, tol: 0,
        explain: R`$\sqrt[n]{a_n}=\frac{\sqrt[n]{4^n+1}}{5}=\frac{4\sqrt[n]{1+4^{-n}}}{5}\to\frac45$. לכן $\frac1R=\frac45$ ו-$R=\frac54=1.25$.` },
      recap: R`קושי-הדמר: $R=\frac{1}{\lim\sqrt[n]{|a_n|}}$` },
    { id: "C05-Q4",
      question: R`מה המרכז ומה הרדיוס של הטור $\displaystyle\sum_{n=1}^{\infty}\frac{(x+1)^n}{n\cdot2^n}$ ?`,
      options: [
        { id: "a", value: R`מרכז $1$, רדיוס $2$` },
        { id: "b", value: R`מרכז $-1$, רדיוס $\frac12$` },
        { id: "c", value: R`מרכז $-1$, רדיוס $2$` },
        { id: "d", value: R`מרכז $1$, רדיוס $\frac12$` }],
      correctId: "c",
      explanation: R`הטור הוא $\sum\frac{X^n}{n2^n}$ עם $X=x+1=x-(-1)$, ולכן המרכז הוא $-1$. מדלאמבר $R=2$ (כמו בדוגמה בשיעור). המרכז $1$ מתקבל אם שוכחים שהסימן ב-$(x-x_0)$ מתהפך, והרדיוס $\frac12$ מתקבל אם הופכים את המנה.`,
      recap: R`$(x+1)^n$: המרכז הוא $-1$` },
    { id: "C05-Q5",
      question: R`מהו רדיוס ההתכנסות של $\displaystyle\sum_{n=1}^{\infty}\frac{x^{2n}}{4^n}$ ?`,
      options: [{ id: "a", value: R`$R=4$` }, { id: "b", value: R`$R=\frac14$` }, { id: "c", value: R`$R=2$` }, { id: "d", value: R`$R=\frac12$` }],
      correctId: "c",
      explanation: R`הטור הוא $\sum t^n/4^n$ עם $t=x^2$, ומתכנס כש-$|t|<4$. כלומר $x^2<4$, ולכן $|x|<2$ ו-$R=2$. התשובה $4$ היא הרדיוס ב-$t$ ולא ב-$x$.`,
      recap: R`חזקות זוגיות: $t=x^2$ ואז שורש` },
    { id: "C05-Q6",
      question: R`מהו רדיוס ההתכנסות של $\displaystyle\sum_{n=1}^{\infty}n^n\,x^n$ ?`,
      options: [{ id: "a", value: R`$R=\infty$` }, { id: "b", value: R`$R=1$` }, { id: "c", value: R`$R=e$` }, { id: "d", value: R`$R=0$` }],
      correctId: "d",
      explanation: R`$\sqrt[n]{n^n}=n\to\infty$, ולכן $\frac1R=\infty$ ו-$R=0$: הטור מתכנס רק ב-$x=0$. אכן לכל $x\ne0$ האיבר $n^nx^n=(nx)^n$ לא שואף ל-$0$.`,
      recap: R`$\frac1R=\infty$ אומר $R=0$` },
  ],
});
