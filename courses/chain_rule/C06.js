/* chain_rule, level 6 - two intermediate variables: g = f(u,v) */
COURSE_LEVEL("chain_rule", {
  id: "C06", order: 6, icon: "🧬", title: "שני משתני ביניים",
  goal: "לגזור $f(u,v)$ כאשר $u$ ו-$v$ תלויים ב-$x,y,z$, ולצמצם את הנגזרות החלקיות של $f$.",
  source: "ai-verified",
  lesson: { html: String.raw`
<p>לפעמים בתוך $f$ יש שני ביטויים: $g(x,y,z)=f(u,v)$ עם $u=u(x,y,z)$ ו-$v=v(x,y,z)$, ו-$f$ כללית. עכשיו $f$ היא פונקציה של שני משתנים, ולכן יש לה שתי נגזרות חלקיות, $f_u=\dfrac{\partial f}{\partial u}$ ו-$f_v=\dfrac{\partial f}{\partial v}$.</p>
<h3>העץ והנוסחה</h3>
<p>מכל משתנה (נניח $x$) יש <b>שני</b> מסלולים אל $g$: דרך $u$ ודרך $v$. לפי הכלל "כופלים לאורך מסלול, מחברים בין מסלולים":</p>
<div class="lesson-formula">$g_x=f_u\,u_x+f_v\,v_x,\qquad g_y=f_u\,u_y+f_v\,v_y,\qquad g_z=f_u\,u_z+f_v\,v_z$</div>
<div class="lesson-ex"><b>דוגמה:</b> $g=f(x^2-y,\;xy)$. נסמן $u=x^2-y$ ו-$v=xy$. אז $u_x=2x$, $u_y=-1$, $v_x=y$, $v_y=x$, ולכן
$$g_x=2x\,f_u+y\,f_v,\qquad g_y=-f_u+x\,f_v.$$
ה-$f_u$ וה-$f_v$ נשארים כסימנים; אין צורך לדעת מי $f$.</div>
<div class="lesson-trap">⚠️ <b>כל נגזרת פנימית יושבת ליד הנגזרת החלקית של ה-$f$ שלה.</b> $u_x$ מתחבר ל-$f_u$ ו-$v_x$ מתחבר ל-$f_v$. החלפה ($y\,f_u$ במקום $y\,f_v$) היא טעות נפוצה.</div>
<div class="lesson-trap">⚠️ <b>משתנה שאינו מופיע.</b> אם $u$ לא תלוי ב-$z$ אז $u_z=0$ והמסלול נעלם. $f_u$ ו-$f_v$ לא מוכפלים זה בזה.</div>
<h3>אותו כלל עם אותיות אחרות</h3>
<p>גם $z=f(x,y)$ כש-$x=x(u,v)$ ו-$y=y(u,v)$ הוא אותו מבנה: $z_u=f_x\,x_u+f_y\,y_u$ ו-$z_v=f_x\,x_v+f_y\,y_v$. הפעם $u,v$ הם המשתנים העצמאיים.</p>
<div class="lesson-rule">🔑 <b>קיצור דרך.</b> לפני שגוזרים, בדקו אם הביטוי מתפשט: כש-$z=e^{xy}$ ו-$x=uv$, $y=\dfrac1u$ מתקבל $xy=v$, כלומר $z=e^{v}$ ולכן $z_u=0$ בלי כלל שרשרת. אבל כלל השרשרת המלא נותן את אותה תשובה.</div>
` },
  questions: [
    { id: "C06-Q1",
      question: String.raw`נתון $g=f(u,v)$ עם $u=x+y$ ו-$v=xy$. מהו $g_x$ ?`,
      options: [
        { id: "a", value: String.raw`$f_u+y\,f_v$` },
        { id: "b", value: String.raw`$f_u+x\,f_v$` },
        { id: "c", value: String.raw`$f_u+f_v$` },
        { id: "d", value: String.raw`$y\,f_u+f_v$` },
      ],
      correctId: "a",
      explanation: String.raw`$u_x=1$ ו-$v_x=y$, ולכן $g_x=f_u\cdot1+f_v\cdot y$. הערך עם $x\,f_v$ הוא $v_y$ (הנגזרת לפי המשתנה השני). $f_u+f_v$ שוכח את $v_x=y$. ו-$y\,f_u+f_v$ מחליף את הנגזרות החלקיות בין המסלולים.`,
      recap: String.raw`$g_x=f_u\,u_x+f_v\,v_x$` },
    { id: "C06-Q2",
      question: String.raw`נתון $g=f(u,v)$ עם $u=x^2-y$ ו-$v=xy$. מהו $g_y$ ?`,
      options: [
        { id: "a", value: String.raw`$-f_u+x\,f_v$` },
        { id: "b", value: String.raw`$f_u+x\,f_v$` },
        { id: "c", value: String.raw`$-2y\,f_u+x\,f_v$` },
        { id: "d", value: String.raw`$-f_u+y\,f_v$` },
      ],
      correctId: "a",
      explanation: String.raw`$u_y=-1$ ו-$v_y=x$, ולכן $g_y=-f_u+x\,f_v$. $+f_u$ מאבד את המינוס של $u_y$. $-2y\,f_u$ גוזר את $x^2-y$ כאילו $y$ היה בריבוע. ו-$y\,f_v$ הוא $v_x$ ולא $v_y$.`,
      recap: String.raw`מחשבים בנפרד $u_y$ ו-$v_y$, ורק אז מחברים` },
    { id: "C06-Q3",
      step: { type: "numeric", prompt: String.raw`תהי $f(u,v)=u\,v^2$ ו-$g(x,y)=f(x+y,\,x-y)$. חשבו את $g_x$ בנקודה $(2,1)$ בעזרת כלל השרשרת.`, answer: 7, tol: 0,
              explain: String.raw`$u=x+y=3$ ו-$v=x-y=1$ בנקודה. $f_u=v^2=1$ ו-$f_v=2uv=6$. $u_x=1$ ו-$v_x=1$. לכן $g_x=1\cdot1+6\cdot1=7$. בדיקה: $g=(x+y)(x-y)^2$ ו-$g_x=(x-y)^2+2(x+y)(x-y)=1+6=7$.` },
      recap: String.raw`מחשבים $f_u,f_v$ ב-$(u,v)$ שמתאים לנקודה` },
    { id: "C06-Q4",
      step: { type: "findbug",
              prompt: String.raw`נתון $g(x,y,z)=f(xy,\;z^2-x)$ ו-$f$ כללית. באיזו שורה כתוב משהו שאינו נכון לגבי הפונקציה $g$ ?`,
              lines: [
                String.raw`נסמן $u=xy$ ו-$v=z^2-x$.`,
                String.raw`$g_x=y\,f_u-f_v$`,
                String.raw`$g_z=2z\,f_u$`,
                String.raw`$g_y=x\,f_u$`,
              ],
              bugIndex: 2,
              explain: String.raw`$z$ מופיע רק ב-$v$, ולכן $g_z=f_v\,v_z=2z\,f_v$. השורה השגויה מחליפה את $f_v$ ב-$f_u$. שאר השורות נכונות: $g_x=f_u\cdot y+f_v\cdot(-1)$ ו-$g_y=f_u\cdot x$ (כי $v$ לא תלוי ב-$y$).` },
      recap: String.raw`הנגזרת הפנימית של $v$ מחוברת ל-$f_v$` },
    { id: "C06-Q5",
      question: String.raw`נתון $z=f(u,v)$ עם $u=xy$ ו-$v=\dfrac xy$. מהו $x\,z_x+y\,z_y$ ?`,
      options: [
        { id: "a", value: String.raw`$2u\,f_u$` },
        { id: "b", value: String.raw`$2v\,f_v$` },
        { id: "c", value: String.raw`$u\,f_u+v\,f_v$` },
        { id: "d", value: String.raw`$0$` },
      ],
      correctId: "a",
      explanation: String.raw`$z_x=y\,f_u+\dfrac1y\,f_v$ ו-$z_y=x\,f_u-\dfrac{x}{y^2}\,f_v$. לכן $x\,z_x=xy\,f_u+\dfrac xy\,f_v$ ו-$y\,z_y=xy\,f_u-\dfrac xy\,f_v$. המחוברים עם $f_v$ מתבטלים ונשאר $2xy\,f_u=2u\,f_u$. הערך $2v\,f_v$ הוא תוצאת ההפרש $x\,z_x-y\,z_y$, ו-$u\,f_u+v\,f_v$ ו-$0$ לא יוצאים משום חישוב.`,
      recap: String.raw`מכפילים במקדמים הנכונים, ורק אז רואים מה מתבטל` },
    { id: "C06-Q6",
      question: String.raw`נתון $z=e^{xy}$ עם $x=uv$ ו-$y=\dfrac1u$. מהו $z_u$ ?`,
      options: [
        { id: "a", value: String.raw`$0$` },
        { id: "b", value: String.raw`$\dfrac{v}{u}\,e^{v}$` },
        { id: "c", value: String.raw`$-\dfrac{v}{u}\,e^{v}$` },
        { id: "d", value: String.raw`$e^{v}$` },
      ],
      correctId: "a",
      explanation: String.raw`בכלל השרשרת: $z_u=z_x\,x_u+z_y\,y_u=y\,e^{xy}\cdot v+x\,e^{xy}\cdot\left(-\dfrac1{u^2}\right)=\dfrac vu e^{v}-\dfrac vu e^{v}=0$. בקיצור: $xy=v$, ולכן $z=e^{v}$ לא תלוי ב-$u$. הערכים $\pm\dfrac vue^v$ הם כל אחד מסלול אחד בלבד, ו-$e^v$ הוא הערך של $z$ ולא נגזרת.`,
      recap: String.raw`לפני כלל השרשרת בודקים אם הביטוי מתפשט` },
  ],
});
