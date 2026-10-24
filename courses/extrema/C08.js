/* extrema course · level 8 - Lagrange with case splits, and a disc = interior + Lagrange on the circle */
COURSE_LEVEL("extrema", {
  id: "C08", order: 8, icon: "🧩", title: "לגראנז' עם מקרים ודיסק מלא",
  goal: "לפצל למקרים בלי לחלק במשתנה, ולשלב פנים ולגראנז' בדיסק.",
  source: "ai-verified",
  lesson: { html: String.raw`
<p>במבחן המשוואות של לגראנז' כמעט תמיד מתפרקות לגורמים, ואז חייבים לפצל למקרים.</p>
<div class="lesson-ex"><b>דוגמה.</b> $f=x^2+2y^2$ על $x^2+y^2=1$. מקבלים $2x=2\lambda x$ ו-$4y=2\lambda y$, כלומר $x(1-\lambda)=0$ ו-$y(2-\lambda)=0$.
<ul>
<li>$x=0$: מהאילוץ $y=\pm1$ (ואז $\lambda=2$), עם $f=2$.</li>
<li>$y=0$: מהאילוץ $x=\pm1$ (ואז $\lambda=1$), עם $f=1$.</li>
<li>$x=y=0$ אינו על המעגל, ו-$\lambda=1$ ו-$\lambda=2$ יחד בלתי אפשריים.</li>
</ul>
ארבע נקודות. מקסימום $2$ ב-$(0,\pm1)$ ומינימום $1$ ב-$(\pm1,0)$.</div>
<div class="contour-fig" data-contour='{"f":"x^2+2*y^2","kind":"lagrange","constraint":"x^2+y^2=1","domain":[[-1.6,1.6],[-1.6,1.6]],"critical_points":[{"x":0,"y":1,"f":2,"role":"abs max"},{"x":0,"y":-1,"f":2,"role":"abs max"},{"x":1,"y":0,"f":1,"role":"abs min"},{"x":-1,"y":0,"f":1,"role":"abs min"}]}'></div>
<div class="lesson-rule">🔑 <b>כל משוואה מהצורה $x\cdot(\ldots)=0$ מפצלת:</b> או $x=0$, או הסוגריים אפס. בכל מקרה מציבים באילוץ ומוצאים נקודות. מקרה שמוביל לסתירה (כמו $0=1$ או נקודה שאינה על העקום) נפסל במפורש.</div>
<p>דוגמה עם שמונה נקודות: $f=x^4+y^4$ על המעגל $x^2+y^2=1$. המשוואות $4x^3=2\lambda x$ ו-$4y^3=2\lambda y$ נותנות $x(2x^2-\lambda)=0$ ו-$y(2y^2-\lambda)=0$. מקרים: $x=0$ (אז $y=\pm1$), $y=0$ (אז $x=\pm1$), או שניהם שונים מאפס ואז $2x^2=\lambda=2y^2$, כלומר $x^2=y^2=\frac12$, ארבע נקודות. ב-$(\pm1,0)$ ו-$(0,\pm1)$ מתקבל $f=1$ (מקסימום), וב-$\left(\pm\frac1{\sqrt2},\pm\frac1{\sqrt2}\right)$ מתקבל $f=\frac12$ (מינימום).</p>
<div class="contour-fig" data-contour='{"f":"x^4+y^4","kind":"lagrange","constraint":"x^2+y^2=1","domain":[[-1.6,1.6],[-1.6,1.6]],"critical_points":[{"x":1,"y":0,"f":1,"role":"abs max"},{"x":-1,"y":0,"f":1,"role":"abs max"},{"x":0,"y":1,"f":1,"role":"abs max"},{"x":0,"y":-1,"f":1,"role":"abs max"},{"x":"sqrt(2)/2","y":"sqrt(2)/2","f":"1/2","role":"abs min"},{"x":"-sqrt(2)/2","y":"sqrt(2)/2","f":"1/2","role":"abs min"},{"x":"sqrt(2)/2","y":"-sqrt(2)/2","f":"1/2","role":"abs min"},{"x":"-sqrt(2)/2","y":"-sqrt(2)/2","f":"1/2","role":"abs min"}]}'></div>
<h3>דיסק מלא: פנים ועוד לגראנז' על השפה</h3>
<p>כשהתחום הוא $x^2+y^2\le1$, השפה היא המעגל, ועליה אפשר להשתמש בלגראנז' במקום בהצבה. הטבלה כוללת <b>גם את הנקודות הקריטיות בפנים</b>. בדיסק של $f=x^2+2y^2$ מוסיפים לטבלה את $(0,0)$ עם $f=0$, והמינימום המוחלט נהיה $0$ במקום $1$.</p>
<div class="lesson-trap">⚠️ <b>חילוק ב-$x$ מאבד נקודות.</b> אם מחלקים את $2x=2\lambda x$ ב-$x$ בלי לבדוק את $x=0$, מאבדים את $(0,\pm1)$, שהן בדיוק המקסימום. כמו בכל בעיה, לא מחלקים בביטוי שיכול להתאפס.</div>
` },
  questions: [
    { id: "C08-Q1", step: { type: "numeric",
        prompt: String.raw`כמה נקודות פותרות את מערכת לגראנז' של $f(x,y)=x^2+2y^2$ תחת $x^2+y^2=1$ ?`,
        answer: 4, tol: 0,
        explain: String.raw`$x(1-\lambda)=0$ ו-$y(2-\lambda)=0$. המקרה $x=0$ נותן $y=\pm1$, והמקרה $y=0$ נותן $x=\pm1$. המקרה שבו שניהם אפס לא על המעגל, והמקרה $\lambda=1=2$ סותר. סך הכול 4 נקודות.` },
      recap: "ממיינים את המקרים ופוסלים את הסתירות" },
    { id: "C08-Q2", question: String.raw`בבעיה $f=x^2+2y^2$ תחת $x^2+y^2=1$, תלמיד חילק את $2x=2\lambda x$ ב-$x$ וקיבל $\lambda=1$. אילו נקודות הוא איבד?`,
      options: [
        { id: "a", value: String.raw`$(0,1)$ ו-$(0,-1)$` },
        { id: "b", value: String.raw`$(1,0)$ ו-$(-1,0)$` },
        { id: "c", value: "את כל ארבע הנקודות" },
        { id: "d", value: "אף נקודה, כי אפשר לחלק כש-$x\\ne0$ תמיד" },
      ], correctId: "a",
      explanation: String.raw`אחרי החילוק $\lambda=1$, והמשוואה $4y=2\lambda y=2y$ נותנת $y=0$ ולכן $(\pm1,0)$ נשמרות. הנקודות שבהן $x=0$, כלומר $(0,\pm1)$, נעלמות, והן נקודות המקסימום. הטענה ש-$x\ne0$ תמיד שגויה כי $(0,1)$ נמצאת על המעגל. הנקודות $(\pm1,0)$ לא אבדו.`,
      recap: "חילוק ב-$x$ מוחק את הפתרונות עם $x=0$" },
    { id: "C08-Q3", step: { type: "order",
        prompt: String.raw`סדרו את הפתרון של $f=x^2+2y^2$ תחת $x^2+y^2=1$.`,
        lines: [
          String.raw`$\nabla f=\lambda\nabla g$ נותן $2x=2\lambda x$ ו-$4y=2\lambda y$, ועוד האילוץ $x^2+y^2=1$`,
          String.raw`מהמשוואה הראשונה $x=0$ או $\lambda=1$, ומהשנייה $y=0$ או $\lambda=2$`,
          String.raw`המקרה $x=y=0$ נפסל בגלל האילוץ, והמקרה $\lambda=1=2$ בלתי אפשרי. נשארים $x=0$ עם $y=\pm1$, ו-$y=0$ עם $x=\pm1$`,
          String.raw`הערכים: $f(0,\pm1)=2$ ו-$f(\pm1,0)=1$, ולכן מקסימום $2$ ומינימום $1$`,
        ],
        explain: String.raw`קודם כותבים את המערכת, אחר כך מפרקים כל משוואה לגורמים, פוסלים סתירות כדי להשאיר את הנקודות, ובסוף משווים ערכים.` },
      recap: "מערכת, מקרים, פסילה, השוואה" },
    { id: "C08-Q4", step: { type: "numeric",
        prompt: String.raw`מהו הערך המינימלי של $f(x,y)=x^2+2y^2$ בדיסק הסגור $x^2+y^2\le1$ ?`,
        answer: 0, tol: 0,
        explain: String.raw`על המעגל המינימום הוא $1$. אבל בפנים $f_x=2x=0$ ו-$f_y=4y=0$ נותנים $(0,0)$ בתוך הדיסק, עם $f=0$. הקטן ביותר הוא $0$.` },
      recap: "בדיסק מוסיפים את הפנים לטבלה" },
    { id: "C08-Q5", step: { type: "numeric",
        prompt: String.raw`כמה נקודות פותרות את מערכת לגראנז' של $f(x,y)=x^4+y^4$ תחת $x^2+y^2=1$ ?`,
        answer: 8, tol: 0,
        explain: String.raw`$x(2x^2-\lambda)=0$ ו-$y(2y^2-\lambda)=0$. מקרים: $x=0$ נותן $(0,\pm1)$. ‏$y=0$ נותן $(\pm1,0)$. ושניהם שונים מאפס נותנים $x^2=y^2=\frac12$ ולכן ארבע נקודות $\left(\pm\frac1{\sqrt2},\pm\frac1{\sqrt2}\right)$. סך הכול $2+2+4=8$.` },
      recap: "שלושה מקרים: $x=0$, $y=0$ ושניהם שונים מאפס" },
    { id: "C08-Q6", step: { type: "numeric",
        prompt: String.raw`מהו הערך המינימלי של $f(x,y)=x^4+y^4$ על המעגל $x^2+y^2=1$ ? (תשובה עשרונית)`,
        answer: 0.5, tol: 0,
        explain: String.raw`בנקודות $(\pm1,0)$ ו-$(0,\pm1)$ מתקבל $f=1$. בנקודות $\left(\pm\frac1{\sqrt2},\pm\frac1{\sqrt2}\right)$ מתקבל $f=\frac14+\frac14=\frac12$. הקטן הוא $\frac12=0.5$.` },
      recap: "משווים את כל שמונה המועמדים" },
  ],
});
