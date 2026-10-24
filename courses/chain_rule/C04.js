/* chain_rule, level 4 - plugging the derivatives into the identity: g' cancels, the rest is the right-hand side */
COURSE_LEVEL("chain_rule", {
  id: "C04", order: 4, icon: "🎯", title: "הצבה בזהות: ה-g' מצטמצם",
  goal: "להציב את $z_x$ ו-$z_y$ באגף שמאל של המשוואה, לראות את $g'$ מצטמצם, ולהשוות את מה שנשאר לאגף ימין.",
  source: "ai-verified",
  lesson: { html: String.raw`
<p>שאלת הוכחת הזהות נראית תמיד אותו דבר: "הראו ש-$z=\ldots g(\ldots)$ מקיימת $\;a\,z_x+b\,z_y=c$", ו-$g$ כללית. המתכון:</p>
<ol>
<li><b>מסמנים</b> את משתנה הביניים $t$, וכותבים $t_x$ ו-$t_y$.</li>
<li><b>גוזרים</b> את $z$ לפי $x$ ולפי $y$ (כלל השרשרת, וכלל מכפלה אם יש גורם חופשי).</li>
<li><b>מציבים</b> באגף שמאל של המשוואה.</li>
<li><b>מצמצמים:</b> כל המחוברים עם $g'(t)$ חייבים להתבטל זה בזה.</li>
<li><b>משווים</b> את מה שנשאר לאגף ימין. לפעמים האגף הימני כתוב בעזרת $z$ ($z$ עצמה, או $\frac{z}{y^2}$), ואז מחליפים אותה בביטוי שלה.</li>
</ol>
<div class="lesson-ex"><b>דוגמה:</b> הראו ש-$z=x\,g(x-y)$ מקיימת $x\,(z_x+z_y)=z$. נסמן $t=x-y$, אז $t_x=1$ ו-$t_y=-1$.
$$z_x=g(t)+x\,g'(t),\qquad z_y=-x\,g'(t).$$
מציבים: $z_x+z_y=g(t)+x\,g'(t)-x\,g'(t)=g(t)$. לכן $x(z_x+z_y)=x\,g(t)=z$. הצדדים שווים.</div>
<div class="lesson-rule">🔑 <b>אם $g'$ לא התבטל, יש טעות.</b> במשוואה שנכונה לכל $g$ המחוברים עם $g'$ חייבים להתבטל. אם נשאר $g'(t)$, חזרו לבדוק את הסימנים של $t_x$ ו-$t_y$ ואת כלל המכפלה, לפני שמחפשים שגיאה אחרת.</div>
<div class="lesson-trap">⚠️ <b>מקדמי המשוואה לא עוזרים לבד.</b> המקדמים ($\frac1x$, $y$, $x^2$) נבחרו כדי שה-$g'$ יתבטל. מקדם שמוצב על הנגזרת הלא נכונה ($y$ על $z_y$ במקום על $z_x$) שובר את הצמצום.</div>
` },
  questions: [
    { id: "C04-Q1",
      step: { type: "order",
              prompt: String.raw`סדרו את הוכחת הזהות $x\,z_x+y\,z_y=2z$ עבור $z=x^2g\!\left(\dfrac yx\right)$.`,
              lines: [
                String.raw`נסמן $t=\dfrac yx$. אז $z=x^2g(t)$, $t_x=-\dfrac{y}{x^2}$ ו-$t_y=\dfrac1x$.`,
                String.raw`גוזרים: $z_x=2x\,g(t)-y\,g'(t)$ וגם $z_y=x\,g'(t)$.`,
                String.raw`מציבים באגף שמאל: $x\,z_x+y\,z_y=2x^2g(t)-xy\,g'(t)+xy\,g'(t)$.`,
                String.raw`המחוברים עם $g'$ מתבטלים ונשאר $2x^2g(t)=2z$, כנדרש.`,
              ],
              explain: String.raw`הסדר נקבע לפי התלות: קודם הנגזרות הפנימיות, אחר כך $z_x$ ו-$z_y$, אחר כך ההצבה, ורק בסוף הצמצום והשוואה לאגף הימני.` },
      recap: String.raw`סמן, גזור, הצב, צמצם, השווה` },
    { id: "C04-Q2",
      question: String.raw`נתון $z=g(x^2+y^2)$. איזו משוואה מתקיימת עבור כל $g$ גזירה?`,
      options: [
        { id: "a", value: String.raw`$y\,z_x-x\,z_y=0$` },
        { id: "b", value: String.raw`$x\,z_x+y\,z_y=0$` },
        { id: "c", value: String.raw`$x\,z_x-y\,z_y=0$` },
        { id: "d", value: String.raw`$y\,z_x+x\,z_y=0$` },
      ],
      correctId: "a",
      explanation: String.raw`$z_x=2x\,g'(t)$ ו-$z_y=2y\,g'(t)$. אז $y\,z_x-x\,z_y=2xy\,g'-2xy\,g'=0$. בשלוש האחרות ה-$g'$ לא מתבטל: $x\,z_x+y\,z_y=2(x^2+y^2)g'$, $x\,z_x-y\,z_y=2(x^2-y^2)g'$ ו-$y\,z_x+x\,z_y=4xy\,g'$, והם לא אפס בכל נקודה.`,
      recap: String.raw`מקדמים שמבטלים את $g'$: $y$ על $z_x$ ו-$-x$ על $z_y$` },
    { id: "C04-Q3",
      step: { type: "findbug",
              prompt: String.raw`ההוכחה הבאה מראה ש-$z=g(x^2+y^2)$ מקיימת $y\,z_x-x\,z_y=0$. באיזו שורה כתוב משהו שאינו נכון לגבי הפונקציה $z$ ?`,
              lines: [
                String.raw`נסמן $t=x^2+y^2$. אז $t_x=2x$ ו-$t_y=2y$.`,
                String.raw`$z_x=2x\,g'(t)$ וגם $z_y=2y\,g(t)$`,
                String.raw`$y\,z_x-x\,z_y=2xy\,g'(t)-2xy\,g'(t)$`,
                String.raw`לכן $y\,z_x-x\,z_y=0$.`,
              ],
              bugIndex: 1,
              explain: String.raw`ב-$z_y$ צריך $g'(t)$ ולא $g(t)$: גוזרים את $g$. הנכון: $z_y=2y\,g'(t)$. עם הטעות ההצבה לא הייתה מצטמצמת.` },
      recap: String.raw`בשתי הנגזרות החלקיות מופיע $g'$ עם אותו ארגומנט` },
    { id: "C04-Q4",
      step: { type: "numeric",
              prompt: String.raw`נתון $z=x^3g\!\left(\dfrac{y}{x^2}\right)$. נמצא $k$ שעבורו $x\,z_x+2y\,z_y=k\,z$ לכל $g$. מהו $k$ ?`,
              answer: 3, tol: 0,
              explain: String.raw`עם $t=\dfrac{y}{x^2}$: $z_x=3x^2g(t)-2y\,g'(t)$ ו-$z_y=x\,g'(t)$. אז $x\,z_x+2y\,z_y=3x^3g(t)-2xy\,g'+2xy\,g'=3x^3g(t)=3z$. לכן $k=3$.` },
      recap: String.raw`אחרי הצמצום משווים את השארית ל-$z$` },
    { bankId: "25A-A-Q3b", recap: String.raw`$z=y\,g(x^2-y^2)$: כלל מכפלה ב-$z_y$, ה-$g'$ מצטמצם, והשארית $\frac{g(t)}{y}$ שווה ל-$\frac{z}{y^2}$` },
  ],
});
