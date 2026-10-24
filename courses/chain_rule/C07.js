/* chain_rule, level 7 - values at a point, a constant composite, homogeneous functions (Euler) */
COURSE_LEVEL("chain_rule", {
  id: "C07", order: 7, icon: "📍", title: "חישוב בנקודה, הרכבה קבועה והומוגניות",
  goal: "לחשב נגזרות חלקיות של הרכבה בנקודה מתוך נתונים, לגזור הרכבה קבועה, ולהוכיח את זהות אוילר.",
  source: "ai-verified",
  lesson: { html: String.raw`
<p>עד עכשיו הוכחנו זהויות. בשלושה סוגי שאלות אחרים משתמשים באותו כלל שרשרת.</p>
<h3>1. חישוב מספרי בנקודה</h3>
<p>נתון $z=z(u,v)$ מפורשת ו-$u,v$ תלויים ב-$x,y$, ושואלים על $z_x$ בנקודה. בונים טבלה: קודם <b>מחשבים את $u$ ו-$v$ בנקודה</b>, אחר כך את $z_u,z_v$ בערכים האלה, אחר כך את $u_x,v_x$ בנקודה, ואז כופלים ומחברים. גוזרים לפני שמציבים.</p>
<div class="lesson-ex"><b>דוגמה:</b> $z=u^2+3uv$, $u=x^2y$, $v=x-y$, בנקודה $(1,1)$.
<ul>
<li>בנקודה: $u=1$ ו-$v=0$.</li>
<li>$z_u=2u+3v=2$ ו-$z_v=3u=3$.</li>
<li>$u_x=2xy=2$, $u_y=x^2=1$, $v_x=1$, $v_y=-1$.</li>
</ul>
$z_x=z_u\,u_x+z_v\,v_x=2\cdot2+3\cdot1=7$, וגם $z_y=2\cdot1+3\cdot(-1)=-1$.</div>
<div class="lesson-trap">⚠️ <b>הנגזרת של ביטוי פנימי יכולה להתאפס בנקודה.</b> אם $u_x=u_y=0$ בנקודה, כל המחוברים שמכילים את $u_x$ ו-$u_y$ נעלמים, ונשארים רק המחוברים של $v$. תבדקו זאת לפני שמתחילים לחשב הכול.</div>
<h3>2. הרכבה קבועה</h3>
<p>אם ידוע ש-$f(x(t),y(t))$ שווה לקבוע לכל $t$, אז הנגזרת שלה לפי $t$ היא $0$, ובכלל השרשרת זה נותן משוואה על $f_x$ ו-$f_y$:</p>
<div class="lesson-formula">$f(x(t),y(t))=c\;\Longrightarrow\;f_x\,x'(t)+f_y\,y'(t)=0$</div>
<div class="lesson-ex"><b>דוגמה:</b> $f(t^2,3t)=5$ לכל $t$. אז $2t\,f_x+3\,f_y=0$ בנקודה $(t^2,3t)$. עבור $t=2$ זו הנקודה $(4,6)$, ו-$4\,f_x(4,6)+3\,f_y(4,6)=0$. אין צורך לדעת מי $f$.</div>
<h3>3. פונקציה הומוגנית וזהות אוילר</h3>
<p>הפונקציה $w=x^k\,F\!\left(\dfrac zx,\dfrac yx\right)$ היא הומוגנית מדרגה $k$. עבורה מתקיים:</p>
<div class="lesson-formula">$x\,w_x+y\,w_y+z\,w_z=k\,w$</div>
<p>ההוכחה: נסמן $s=\dfrac zx$ ו-$t=\dfrac yx$. אז $s_x=-\dfrac z{x^2}$, $s_z=\dfrac1x$, $t_x=-\dfrac y{x^2}$, $t_y=\dfrac1x$, והאחרות אפס. $w_x$ כולל כלל מכפלה (גורם $x^k$ וגם $F$), ובהצבה המחוברים עם $F_s$ ו-$F_t$ מתבטלים ונשאר $k\,w$.</p>
<div class="lesson-rule">🔑 <b>איך מזהים שאפשר להשתמש בזהות אוילר:</b> הפונקציה היא חזקה של $x$ כפול פונקציה של היחסים $\frac zx$ ו-$\frac yx$. החזקה היא $k$ בזהות.</div>
` },
  questions: [
    { id: "C07-Q1",
      step: { type: "numeric", prompt: String.raw`נתון $z=u^2+3uv$ עם $u=x^2y$ ו-$v=x-y$. חשבו את $z_x$ בנקודה $(1,1)$.`, answer: 7, tol: 0,
              explain: String.raw`בנקודה $u=1$, $v=0$. $z_u=2u+3v=2$, $z_v=3u=3$, $u_x=2xy=2$, $v_x=1$. לכן $z_x=2\cdot2+3\cdot1=7$.` },
      recap: String.raw`קודם הערכים של $u,v$ בנקודה, אחר כך הנגזרות` },
    { id: "C07-Q2",
      step: { type: "numeric", prompt: String.raw`באותה פונקציה ($z=u^2+3uv$, $u=x^2y$, $v=x-y$) חשבו את $z_y$ בנקודה $(1,1)$.`, answer: -1, tol: 0,
              explain: String.raw`$z_u=2$ ו-$z_v=3$ כמקודם. $u_y=x^2=1$ ו-$v_y=-1$. לכן $z_y=2\cdot1+3\cdot(-1)=-1$.` },
      recap: String.raw`$v_y=-1$: לא לשכוח את המינוס` },
    { id: "C07-Q3",
      step: { type: "numeric", prompt: String.raw`נתון ש-$f(x,y)$ דיפרנציאבילית, $f(t^2,3t)=5$ לכל $t$, ו-$f_x(4,6)=3$. חשבו את $f_y(4,6)$.`, answer: -4, tol: 0,
              explain: String.raw`גוזרים לפי $t$: $2t\,f_x+3\,f_y=0$. ב-$t=2$ (הנקודה $(4,6)$): $4\cdot3+3\,f_y=0$, ולכן $f_y(4,6)=-4$.` },
      recap: String.raw`הרכבה קבועה: הנגזרת לפי $t$ היא אפס` },
    { id: "C07-Q4",
      question: String.raw`נתון $w=x^3F\!\left(\dfrac zx,\dfrac yx\right)$ עם $F$ גזירה. מהו $x\,w_x+y\,w_y+z\,w_z$ ?`,
      options: [
        { id: "a", value: String.raw`$3w$` },
        { id: "b", value: String.raw`$w$` },
        { id: "c", value: String.raw`$x^3$` },
        { id: "d", value: String.raw`$0$` },
      ],
      correctId: "a",
      explanation: String.raw`$w$ הומוגנית מדרגה $3$, ולכן לפי זהות אוילר הסכום שווה ל-$3w$. הערך $w$ יוצא למי ששכח את החזקה. $x^3$ הוא הגורם שלפני $F$ ולא קשור לסכום. ו-$0$ נכון רק אם $w$ קבועה על הקרניים.`,
      recap: String.raw`$x\,w_x+y\,w_y+z\,w_z=k\,w$ עבור הומוגנית מדרגה $k$` },
    { id: "C07-Q5",
      step: { type: "findbug",
              prompt: String.raw`ההוכחה הבאה עוסקת ב-$w=x^kF(s,t)$ עם $s=\dfrac zx$ ו-$t=\dfrac yx$. באיזו שורה כתוב משהו שאינו נכון לגבי הפונקציה $w$ ?`,
              lines: [
                String.raw`$s_x=-\dfrac{z}{x^2}$ וגם $t_x=-\dfrac{y}{x^2}$.`,
                String.raw`$w_x=x^k\left(F_s\,s_x+F_t\,t_x\right)$`,
                String.raw`$w_y=x^{k-1}F_t$ וגם $w_z=x^{k-1}F_s$.`,
                String.raw`$x\,w_x+y\,w_y+z\,w_z=k\,x^kF-x^{k-1}\left(zF_s+yF_t\right)+x^{k-1}\left(yF_t+zF_s\right)$`,
              ],
              bugIndex: 1,
              explain: String.raw`ב-$w_x$ חסר המחובר $k\,x^{k-1}F$ שבא מגזירת $x^k$ (כלל מכפלה). הנכון: $w_x=k\,x^{k-1}F+x^k\left(F_s s_x+F_t t_x\right)$. השורה האחרונה נכונה רק עם המחובר הזה.` },
      recap: String.raw`גם $x^k$ נגזר: כלל מכפלה ב-$w_x$` },
    { bankId: "24A-A-Q3b", recap: String.raw`$u=x^kF(\frac zx,\frac yx)$: כלל מכפלה ב-$u_x$, ואז $x\,u_x+y\,u_y+z\,u_z=k\,u$` },
  ],
});
