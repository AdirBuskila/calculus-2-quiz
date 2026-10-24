/* chain_rule, level 5 - second derivatives through the chain rule */
COURSE_LEVEL("chain_rule", {
  id: "C05", order: 5, icon: "²", title: "נגזרות שניות דרך כלל השרשרת",
  goal: "לחשב $z_{xx}$, $z_{xy}$ ו-$z_{yy}$ של $z=g(t)$ ולזהות משוואות מסדר שני (כמו משוואת גלים).",
  source: "ai-verified",
  lesson: { html: String.raw`
<p>חלק מהשאלות (וגם סעיפים בנושאים אחרים) מבקשים נגזרת שנייה של $z=g(t)$. הרעיון: הנגזרת הראשונה $z_x=g'(t)\,t_x$ היא <b>מכפלה</b> של שני גורמים, ושניהם יכולים להשתנות. הגורם $g'(t)$ הוא בעצמו פונקציה של $t$, ולכן גוזרים גם אותו בכלל השרשרת.</p>
<div class="lesson-formula">$z_{xx}=g''(t)\,t_x^{\,2}+g'(t)\,t_{xx}$</div>
<div class="lesson-formula">$z_{xy}=g''(t)\,t_x\,t_y+g'(t)\,t_{xy}$</div>
<p>הגורם הראשון בא מגזירת $g'(t)$ (שנהפך ל-$g''(t)\,t_y$ או $g''(t)\,t_x$). הגורם השני בא מגזירת $t_x$ עצמו, ולכן הוא מכיל את הנגזרת השנייה של הביטוי הפנימי. הנוסחה של $z_{yy}$ דומה, עם $t_y$.</p>
<div class="lesson-ex"><b>דוגמה:</b> $z=g(xy)$, $t=xy$, $t_x=y$, $t_y=x$, $t_{xx}=0$, $t_{xy}=1$.
$$z_{xx}=y^2\,g''(t),\qquad z_{xy}=g'(t)+xy\,g''(t).$$
אפשר גם לראות את זה בלי הנוסחה: $z_x=y\,g'(t)$, וגזירה לפי $y$ היא כלל מכפלה: $g'(t)+y\,g''(t)\,x$.</div>
<div class="lesson-trap">⚠️ <b>שני הגורמים.</b> כותבים $g''(t)\,t_x^{\,2}$ ו-<b>גם</b> $g'(t)\,t_{xx}$. מי ששוכח את השני טועה כשהביטוי הפנימי לא ליניארי (כמו $x^2+y^2$ שבו $t_{xx}=2$).</div>
<div class="lesson-trap">⚠️ <b>$t_x^{\,2}$ ולא $t_{xx}$.</b> הגורם עם $g''$ מכיל את הנגזרת הראשונה בריבוע, לא את הנגזרת השנייה.</div>
<div class="lesson-rule">🔑 כשהביטוי הפנימי ליניארי ($t=ax+by$) אז $t_{xx}=t_{xy}=0$ ונשאר רק הגורם עם $g''$. כך מגיעים למשוואות כמו $z_{xx}=z_{yy}$.</div>
` },
  questions: [
    { id: "C05-Q1",
      question: String.raw`נתון $z=g(t)$ עם $t=x^2+y^2$. מהו $z_{xx}$ ?`,
      options: [
        { id: "a", value: String.raw`$4x^2\,g''(t)+2\,g'(t)$` },
        { id: "b", value: String.raw`$4x^2\,g''(t)$` },
        { id: "c", value: String.raw`$2x\,g''(t)+2\,g'(t)$` },
        { id: "d", value: String.raw`$2\,g''(t)$` },
      ],
      correctId: "a",
      explanation: String.raw`$t_x=2x$ ו-$t_{xx}=2$, ולכן $z_{xx}=g''(t)\,(2x)^2+g'(t)\cdot2$. הערך $4x^2g''(t)$ שוכח את הגורם עם $t_{xx}$. הערך $2x\,g''(t)+2g'(t)$ לא העלה את $t_x$ בריבוע. והערך $2g''(t)$ משתמש ב-$t_{xx}$ במקום ב-$t_x^2$ ושוכח את $g'$.`,
      recap: String.raw`$z_{xx}=g''\,t_x^2+g'\,t_{xx}$` },
    { id: "C05-Q2",
      step: { type: "numeric", prompt: String.raw`תהי $z=g(xy)$ כאשר $g(t)=t^3$. חשבו את $z_{xy}$ בנקודה $(1,2)$.`, answer: 36, tol: 0,
              explain: String.raw`$t=xy=2$, $g'(t)=3t^2=12$, $g''(t)=6t=12$. לפי הנוסחה $z_{xy}=g'(t)+xy\,g''(t)=12+2\cdot12=36$. בדיקה: $z=x^3y^3$ ו-$z_{xy}=9x^2y^2=36$.` },
      recap: String.raw`$z_{xy}=g'(t)+xy\,g''(t)$ עבור $t=xy$` },
    { id: "C05-Q3",
      question: String.raw`נתון $z=g(x-y)$. מהו $z_{xx}+2z_{xy}+z_{yy}$ ?`,
      options: [
        { id: "a", value: String.raw`$0$` },
        { id: "b", value: String.raw`$4\,g''(t)$` },
        { id: "c", value: String.raw`$2\,g''(t)$` },
        { id: "d", value: String.raw`$g'(t)$` },
      ],
      correctId: "a",
      explanation: String.raw`הביטוי הפנימי $t=x-y$ ליניארי: $t_x=1$, $t_y=-1$, והנגזרות השניות שלו אפס. לכן $z_{xx}=g''$, $z_{xy}=-g''$ ו-$z_{yy}=g''$, והסכום $g''-2g''+g''=0$. $4g''$ יוצא למי ששכח את המינוס ב-$t_y$, $2g''$ למי שמתעלם מ-$z_{xy}$ לגמרי, ו-$g'$ לא מופיע כלל כי $t_{xx}=0$.`,
      recap: String.raw`ביטוי פנימי ליניארי: רק $g''$ נשאר, ושימו לב לסימנים` },
    { id: "C05-Q4",
      step: { type: "findbug",
              prompt: String.raw`החישוב הבא מחשב את $z_{xx}$ עבור $z=g(x^2+y^2)$. באיזו שורה כתוב משהו שאינו נכון לגבי הפונקציה $z$ ?`,
              lines: [
                String.raw`נסמן $t=x^2+y^2$. אז $z_x=2x\,g'(t)$.`,
                String.raw`$z_{xx}=2x\,g''(t)$`,
                String.raw`$z_{xx}=2\,g'(t)+4x^2\,g''(t)$`,
              ],
              bugIndex: 1,
              explain: String.raw`הנגזרת של $2x\,g'(t)$ לפי $x$ היא כלל מכפלה: $2\,g'(t)+2x\,g''(t)\cdot t_x=2g'(t)+4x^2g''(t)$. השורה השגויה שוכחת גם את $2g'(t)$ וגם את הגורם $t_x$. השורה האחרונה נכונה.` },
      recap: String.raw`$z_x$ הוא מכפלה: גוזרים כל גורם, וגוזרים את $g'$ בכלל השרשרת` },
    { id: "C05-Q5",
      question: String.raw`נתון $z=g(2x+3y)$. איזו משוואה מתקיימת לכל $g$ גזירה פעמיים?`,
      options: [
        { id: "a", value: String.raw`$9\,z_{xx}-4\,z_{yy}=0$` },
        { id: "b", value: String.raw`$3\,z_{xx}-2\,z_{yy}=0$` },
        { id: "c", value: String.raw`$z_{xx}-z_{yy}=0$` },
        { id: "d", value: String.raw`$2\,z_{xx}-3\,z_{yy}=0$` },
      ],
      correctId: "a",
      explanation: String.raw`$t=2x+3y$ ליניארי: $z_{xx}=4g''$ ו-$z_{yy}=9g''$. לכן $9z_{xx}-4z_{yy}=36g''-36g''=0$. השאר נותנים $3\cdot4-2\cdot9=-6$, $4-9=-5$ ו-$2\cdot4-3\cdot9=-19$ כפולות של $g''$, שאינן אפס בכל נקודה.`,
      recap: String.raw`$z_{xx}=a^2g''$ ו-$z_{yy}=b^2g''$ עבור $t=ax+by$` },
  ],
});
