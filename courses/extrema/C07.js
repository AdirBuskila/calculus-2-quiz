/* extrema course · level 7 - Lagrange multipliers with one constraint, and the picture behind it */
COURSE_LEVEL("extrema", {
  id: "C07", order: 7, icon: "🧲", title: "כופלי לגראנז': אילוץ אחד",
  goal: "לכתוב ולפתור את מערכת לגראנז' $\\nabla f=\\lambda\\nabla g$, ולהבין למה הגרדיאנטים מקבילים.",
  source: "ai-verified",
  lesson: { html: String.raw`
<p>כשמבקשים אקסטרמום של $f$ <b>תחת אילוץ</b> $g(x,y)=c$ (רק על עקום, בלי הפנים), משתמשים בשיטת לגראנז'. פותרים שלוש משוואות בשלושה נעלמים $x,y,\lambda$:</p>
<div class="lesson-formula">$f_x=\lambda g_x,\qquad f_y=\lambda g_y,\qquad g(x,y)=c$</div>
<div class="lesson-rule">🔑 <b>מתכון:</b>
<ul>
<li>כותבים את $g$ בצורה $g(x,y)=c$ וגוזרים את $f$ ואת $g$.</li>
<li>משווים $\nabla f=\lambda\nabla g$ (שתי משוואות) ומוסיפים את האילוץ.</li>
<li>פותרים, ושומרים <b>כל</b> פתרון $(x,y)$. את $\lambda$ משליכים בסוף, הוא רק עזר.</li>
<li>מחשבים $f$ בכל נקודה. הגדול הוא המקסימום והקטן המינימום.</li>
</ul></div>
<div class="lesson-ex"><b>דוגמה.</b> $f=x+y$ על המעגל $x^2+y^2=1$. כאן $\nabla f=(1,1)$ ו-$\nabla g=(2x,2y)$. המערכת $1=2\lambda x$, ‏$1=2\lambda y$ נותנת $x=y$ (שניהם שווים ל-$\frac1{2\lambda}$, ו-$\lambda\ne0$). מהאילוץ $2x^2=1$, כלומר $x=y=\pm\frac1{\sqrt2}$. הערכים: $f=\sqrt2$ ו-$f=-\sqrt2$. מקסימום $\sqrt2$ ומינימום $-\sqrt2$.</div>
<div class="contour-fig" data-contour='{"f":"x+y","kind":"lagrange","constraint":"x^2+y^2=1","domain":[[-1.6,1.6],[-1.6,1.6]],"critical_points":[{"x":"sqrt(2)/2","y":"sqrt(2)/2","f":"sqrt(2)","role":"abs max"},{"x":"-sqrt(2)/2","y":"-sqrt(2)/2","f":"-sqrt(2)","role":"abs min"}]}'></div>
<p>באיור: קווי הגובה של $f$ הם ישרים, ובכל נקודה על המעגל יש חץ מלא ($\nabla f$) וחץ מקווקו ($\nabla g$). בשתי נקודות הקיצון שני החצים <b>על אותו קו</b>.</p>
<h3>למה הגרדיאנטים מקבילים?</h3>
<p>$\nabla f$ ניצב לקו הגובה של $f$, ו-$\nabla g$ ניצב לעקום האילוץ. בנקודת קיצון על העקום, קו הגובה של $f$ <b>משיק</b> לעקום (אחרת היה אפשר לזוז על העקום לערך גבוה או נמוך יותר). אם שני העקומים משיקים, הניצבים להם מקבילים: $\nabla f=\lambda\nabla g$.</p>
<div class="contour-fig" data-contour="24A-A-Q4b"></div>
<p>באיור השני $f=xy$ על $x^2+y^2=2$. בארבע הנקודות $(\pm1,\pm1)$ החצים מקבילים. בשתיים מהן $f=1$ (מקסימום) ובשתיים $f=-1$ (מינימום).</p>
<div class="lesson-trap">⚠️ <b>הפתרונות הם מועמדים.</b> על עקום סגור וחסום (מעגל) הערך הגדול והקטן שבין המועמדים הם המקסימום והמינימום. על עקום לא חסום, כמו ישר, יכול להיות רק אחד מהם.</div>
<div class="lesson-trap">⚠️ אילוץ בלי הפנים: "תחת האילוץ" אומר שלא בודקים נקודות קריטיות של $f$ בפנים.</div>
` },
  questions: [
    { id: "C07-Q1", question: String.raw`מהי מערכת לגראנז' למציאת קיצון של $f(x,y)=xy$ תחת האילוץ $x^2+y^2=2$ ?`,
      options: [
        { id: "a", value: String.raw`$y=2\lambda x,\ \ x=2\lambda y,\ \ x^2+y^2=2$` },
        { id: "b", value: String.raw`$y=\lambda x^2,\ \ x=\lambda y^2,\ \ x^2+y^2=2$` },
        { id: "c", value: String.raw`$y=2\lambda x,\ \ x=2\lambda y$` },
        { id: "d", value: String.raw`$y=2x,\ \ x=2y,\ \ x^2+y^2=2$` },
      ], correctId: "a",
      explanation: String.raw`$\nabla f=(y,x)$ ו-$\nabla g=(2x,2y)$, ולכן $\nabla f=\lambda\nabla g$ נותן $y=2\lambda x$ ו-$x=2\lambda y$, ויחד עם האילוץ. במערכת עם $\lambda x^2$ הנגזרת של $g$ חושבה לא נכון. בלי משוואת האילוץ נקבל המון פתרונות, כל נקודה על קו, ולא רק על המעגל. בלי $\lambda$ נקבל רק $(0,0)$, שאינה על המעגל.`,
      recap: "$\\nabla f=\\lambda\\nabla g$ ועוד משוואת האילוץ" },
    { id: "C07-Q2", step: { type: "numeric",
        prompt: String.raw`מהו הערך המקסימלי של $f(x,y)=x+2y$ על המעגל $x^2+y^2=5$ ?`,
        answer: 5, tol: 0,
        explain: String.raw`$\nabla f=(1,2)=\lambda(2x,2y)$ נותן $1=2\lambda x$ ו-$2=2\lambda y$, ולכן $y=2x$. מהאילוץ $5x^2=5$, כלומר $x=\pm1$ והנקודות $(1,2)$ ו-$(-1,-2)$. הערכים: $f(1,2)=5$ ו-$f(-1,-2)=-5$. המקסימום הוא $5$.` },
      recap: "מציבים את המועמדים ב-$f$ ובוחרים" },
    { id: "C07-Q3", step: { type: "numeric",
        prompt: String.raw`ב-$f(x,y)=xy$ תחת $x^2+y^2=2$, בנקודה $(1,1)$ מתקיימת מערכת לגראנז' $y=2\lambda x$, ‏$x=2\lambda y$. מהו $\lambda$ ? (תשובה עשרונית)`,
        answer: 0.5, tol: 0,
        explain: String.raw`מציבים $x=y=1$ במשוואה $y=2\lambda x$ ומקבלים $1=2\lambda$, כלומר $\lambda=\frac12$. בנקודה $(1,-1)$ היה מתקבל $\lambda=-\frac12$.` },
      recap: "אחרי הצבת הנקודה, $\\lambda$ נקבע" },
    { id: "C07-Q4", step: { type: "numeric",
        prompt: String.raw`כמה נקודות $(x,y)$ פותרות את מערכת לגראנז' של $f(x,y)=xy$ תחת $x^2+y^2=2$ ?`,
        answer: 4, tol: 0,
        explain: String.raw`מ-$y=2\lambda x$ ו-$x=2\lambda y$ מקבלים (בהצבה) $y=4\lambda^2y$. כי $y\ne0$ (אחרת גם $x=0$ והאילוץ לא מתקיים), $\lambda=\pm\frac12$ ולכן $y=\pm x$. מהאילוץ $2x^2=2$: $x=\pm1$. ארבע נקודות $(\pm1,\pm1)$.` },
      recap: "$x^2=y^2$ והאילוץ נותנים ארבע נקודות" },
    { id: "C07-Q5", question: String.raw`באיור: קווי הגובה של $f=xy$, המעגל $x^2+y^2=2$, ולכל נקודה על המעגל חצים של $\nabla f$ ושל $\nabla g$.

` + "```contour\n24A-A-Q4b\n```" + String.raw`

בנקודת קיצון על המעגל החצים מקבילים. מה זה אומר גאומטרית?`,
      options: [
        { id: "a", value: "קו הגובה של $f$ משיק לעקום האילוץ" },
        { id: "b", value: "קו הגובה של $f$ ניצב לעקום האילוץ" },
        { id: "c", value: String.raw`$\nabla f=0$ בנקודה` },
        { id: "d", value: "עקום האילוץ עובר דרך הראשית" },
      ], correctId: "a",
      explanation: String.raw`$\nabla f$ ניצב לקו הגובה ו-$\nabla g$ ניצב לעקום. כשהגרדיאנטים מקבילים, הקו והעקום משיקים. אם קו הגובה היה חותך את העקום (ובמיוחד ניצב לו), אפשר היה לנוע לאורך העקום ולהגדיל או להקטין את $f$, ולכן זו לא נקודת קיצון. גם $\nabla f=0$ לא מתקיים: ב-$(1,1)$ הוא $(1,1)$. והמעגל אינו עובר דרך הראשית, שהיא מרכזו.`,
      recap: "גרדיאנטים מקבילים = קו גובה משיק לאילוץ" },
    { id: "C07-Q6", step: { type: "numeric",
        prompt: String.raw`מהו הערך המינימלי של $f(x,y)=x^2+y^2$ על הישר $x+y=2$ ?`,
        answer: 2, tol: 0,
        explain: String.raw`$\nabla f=(2x,2y)=\lambda(1,1)$ נותן $x=y$, ומהאילוץ $x=y=1$ ו-$f=2$. הישר אינו חסום: רחוק מהראשית $f$ גדל בלי גבול. לכן $2$ הוא מינימום ואין מקסימום. כשהאילוץ לא חסום, בודקים בנפרד איזה סוג קיצון קיבלנו.` },
      recap: "על עקום לא חסום ייתכן רק מינימום או רק מקסימום" },
  ],
});
