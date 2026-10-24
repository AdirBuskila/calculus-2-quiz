/* chain_rule, level 3 - a free factor or free term next to g: product rule + the extra route */
COURSE_LEVEL("chain_rule", {
  id: "C03", order: 3, icon: "✖️", title: "גורם חופשי לפני g: כלל המכפלה",
  goal: "לגזור ביטויים כמו $y\\,g(x^2-y^2)$ או $\\frac{y}{3x}+g(xy)$ בלי לשכוח את $g(t)$ עצמה.",
  source: "ai-verified",
  lesson: { html: String.raw`
<p>בבחינות $g$ כמעט אף פעם לא עומדת לבד. לפניה יש גורם כמו $y$ או $x$, או שמחובר אליה איבר חופשי. כל אחד מהם משנה את הגזירה.</p>
<h3>גורם חופשי: כלל המכפלה</h3>
<p>עבור $z=y\,g(t)$ עם $t=x^2-y^2$ גוזרים לפי המשתנה של הגורם עם <b>כלל המכפלה</b> $(uv)'=u'v+uv'$, ולכן יש שני מחוברים:</p>
<div class="lesson-ex"><b>דוגמה:</b> $z=y\,g(t)$, $t=x^2-y^2$, $t_x=2x$, $t_y=-2y$.
<ul>
<li>לפי $x$: הגורם $y$ קבוע, ולכן אין כלל מכפלה: $z_x=y\,g'(t)\cdot2x=2xy\,g'(t)$.</li>
<li>לפי $y$: הגורם $y$ משתנה, ולכן $z_y=1\cdot g(t)+y\,g'(t)\cdot(-2y)=g(t)-2y^2g'(t)$.</li>
</ul></div>
<div class="lesson-rule">🔑 <b>כלל המכפלה נדרש רק כשמגזרים לפי משתנה שמופיע בגורם החופשי.</b> שואלים פעם אחת: "האם הגורם שלפני $g$ מכיל את המשתנה שלפיו אני גוזר?"</div>
<div class="lesson-trap">⚠️ <b>הטעות הנפוצה ביותר: לשכוח את $g(t)$.</b> ב-$z_y$ למעלה המחובר $g(t)$ בא מנגזרת הגורם $y$. מי שכותב רק $-2y^2g'(t)$ איבד אותו, וההוכחה לא תצא.</div>
<h3>איבר חופשי מחובר</h3>
<p>אם $z=\dfrac{y}{3x}+g(xy)$, כל איבר נגזר בנפרד ומחברים: $z_x=-\dfrac{y}{3x^2}+y\,g'(t)$ ו-$z_y=\dfrac1{3x}+x\,g'(t)$ עם $t=xy$. כאן $y$ מופיע בשני האיברים, ולכן שני מסלולים.</p>
<div class="lesson-ex"><b>דוגמה נוספת:</b> $z=x\,g(xy)$ עם $t=xy$, $t_x=y$, $t_y=x$.
<ul>
<li>$z_x=g(t)+x\,g'(t)\cdot y$ (כלל מכפלה, כי $x$ מופיע בגורם).</li>
<li>$z_y=x\,g'(t)\cdot x=x^2g'(t)$ (אין כלל מכפלה, כי $x$ קבוע לפי $y$).</li>
</ul>
אפשר לראות שמתקיים $x\,z_x-y\,z_y=x\,g(t)=z$: המחוברים עם $g'$ מתבטלים. זה בדיוק הסוג של התוצאה שהמבחן מבקש.</div>
` },
  questions: [
    { id: "C03-Q1",
      question: String.raw`נתון $z=y\,g(t)$ עם $t=x^2-y^2$. מהו $z_y$ ?`,
      options: [
        { id: "a", value: String.raw`$g(t)-2y^2\,g'(t)$` },
        { id: "b", value: String.raw`$-2y^2\,g'(t)$` },
        { id: "c", value: String.raw`$g(t)+2y^2\,g'(t)$` },
        { id: "d", value: String.raw`$g(t)-2y\,g'(t)$` },
      ],
      correctId: "a",
      explanation: String.raw`$y$ הוא גם הגורם החופשי וגם משתנה, ולכן כלל מכפלה: $1\cdot g(t)+y\,g'(t)\,t_y$ עם $t_y=-2y$, כלומר $g(t)-2y^2g'(t)$. בלי $g(t)$ שכחתם את נגזרת הגורם. הסימן $+2y^2$ שוכח את המינוס של $t_y$. ו-$-2y\,g'(t)$ שכח להכפיל ב-$y$ של הגורם.`,
      recap: String.raw`גורם חופשי שמכיל את המשתנה הנגזר: כלל מכפלה, והמחובר $g(t)$ לא נעלם` },
    { id: "C03-Q2",
      question: String.raw`נתון $z=y\,g(t)$ עם $t=x^2-y^2$. מהו $z_x$ ?`,
      options: [
        { id: "a", value: String.raw`$2xy\,g'(t)$` },
        { id: "b", value: String.raw`$g(t)+2xy\,g'(t)$` },
        { id: "c", value: String.raw`$2x\,g'(t)$` },
        { id: "d", value: String.raw`$2xy\,g(t)$` },
      ],
      correctId: "a",
      explanation: String.raw`לפי $x$ הגורם $y$ הוא קבוע, ולכן אין כלל מכפלה: $z_x=y\,g'(t)\,t_x=2xy\,g'(t)$. הוספת $g(t)$ היא כלל מכפלה שלא נדרש. $2x\,g'(t)$ שכח את הגורם $y$. ו-$2xy\,g(t)$ לא גזר את $g$.`,
      recap: String.raw`אם הגורם החופשי לא מכיל את המשתנה הנגזר, הוא יוצא כקבוע` },
    { id: "C03-Q3",
      step: { type: "numeric", prompt: String.raw`תהי $z=x\,g(xy)$ כאשר $g(t)=t^2$. חשבו את $z_x$ בנקודה $(1,2)$.`, answer: 12, tol: 0,
              explain: String.raw`$t=xy=2$, $g(t)=4$, $g'(t)=2t=4$ ו-$t_x=y=2$. כלל מכפלה: $z_x=g(t)+x\,g'(t)\,t_x=4+1\cdot4\cdot2=12$. בדיקה: $z=x^3y^2$ ו-$z_x=3x^2y^2=12$.` },
      recap: String.raw`$z_x=g(t)+x\,g'(t)\,t_x$` },
    { id: "C03-Q4",
      step: { type: "findbug",
              prompt: String.raw`הפתרון הבא עוסק ב-$z=x\,g(xy)$. באיזו שורה כתוב משהו שאינו נכון לגבי הפונקציה $z$ ?`,
              lines: [
                String.raw`נסמן $t=xy$. אז $z=x\,g(t)$, $t_x=y$ וגם $t_y=x$.`,
                String.raw`$z_x=x\,g'(t)\cdot y$`,
                String.raw`$z_y=x\,g'(t)\cdot x=x^2g'(t)$`,
                String.raw`$x\,z_x-y\,z_y=x\,g(t)=z$`,
              ],
              bugIndex: 1,
              explain: String.raw`ב-$z_x$ חסר המחובר $g(t)$, שבא מנגזרת הגורם החופשי $x$. הנכון: $z_x=g(t)+x\,g'(t)\,y$. השורה האחרונה נכונה, אבל היא נכונה רק עם המחובר שחסר.` },
      recap: String.raw`שוכחים את $g(t)$ כשהגורם החופשי מכיל את המשתנה הנגזר` },
    { id: "C03-Q5",
      question: String.raw`נתון $z=x\,g(xy)$. מהו $x\,z_x-y\,z_y$ ?`,
      options: [
        { id: "a", value: String.raw`$z$` },
        { id: "b", value: String.raw`$0$` },
        { id: "c", value: String.raw`$2z$` },
        { id: "d", value: String.raw`$x\,g'(xy)$` },
      ],
      correctId: "a",
      explanation: String.raw`$x\,z_x=x\,g(t)+x^2y\,g'(t)$ ו-$y\,z_y=x^2y\,g'(t)$. ההפרש הוא $x\,g(t)=z$: המחוברים עם $g'$ מתבטלים ונשאר מה שהגיע מכלל המכפלה. $0$ נכון רק אם שכחו את $g(t)$ ב-$z_x$. $2z$ ו-$x\,g'(xy)$ לא יוצאים מהחישוב.`,
      recap: String.raw`ה-$g'$ מצטמצם ונשאר מה שבא מהגורם החופשי` },
    { id: "C03-Q6",
      step: { type: "numeric", prompt: String.raw`תהי $z=\dfrac{y}{3x}+g(xy)$ כאשר $g(t)=t^2$. חשבו את $z_y$ בנקודה $(1,1)$. (תשובה עשרונית, דיוק $0.01$.)`, answer: 2.3333333, tol: 0.01,
              explain: String.raw`$z_y=\dfrac1{3x}+g'(t)\,x$ עם $t=xy=1$ ו-$g'(t)=2t=2$. לכן $z_y=\dfrac13+2=\dfrac73\approx2.33$.` },
      recap: String.raw`שני מסלולים אל $y$: האיבר החופשי ו-$g$` },
  ],
});
