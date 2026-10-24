/* double_int, level 7 - general (linear and non-linear) change of variables with the Jacobian */
COURSE_LEVEL("double_int", {
  id: "C07", order: 7, icon: "🔁", title: "שינוי משתנים ליניארי והיעקוביאן",
  goal: "לבחור משתנים חדשים שהופכים את התחום למלבן, לחשב את היעקוביאן דרך ההפוך, ולחשב את האינטגרל.",
  source: "ai-verified",
  lesson: { html: String.raw`
<p>כשהתחום חסום בארבעה עקומים (ישרים מקבילים, היפרבולות, פרבולות), מחפשים משתנים חדשים $u(x,y)$ ו-$v(x,y)$ שבהם כל עקום הוא <b>קבוע</b>, כלומר התחום הופך למלבן $a\le u\le b$, $c\le v\le d$.</p>
<div class="lesson-formula">$$\iint_R f(x,y)\,dA=\iint_Q f\bigl(x(u,v),y(u,v)\bigr)\,\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,du\,dv$$</div>
<div class="lesson-rule">🔑 <b>היעקוביאן דרך ההפוך.</b> בדרך כלל $u,v$ נתונים כפונקציות של $x,y$, ולכן קל לחשב את $\dfrac{\partial(u,v)}{\partial(x,y)}$. מה שמציבים באינטגרל הוא ההופכי של ערכו המוחלט:
$$\left|\frac{\partial(x,y)}{\partial(u,v)}\right|=\frac{1}{\left|\dfrac{\partial(u,v)}{\partial(x,y)}\right|}.$$</div>
<ul>
<li>ישרים מקבילים $y-x=c$ או $x+y=c$: בוחרים $u=y-x$ או $u=x+y$;</li>
<li>היפרבולות $xy=c$: בוחרים $v=xy$;</li>
<li>קרניים $y=mx$: בוחרים $u=\dfrac yx$.</li>
</ul>
<div class="lesson-ex">התחום $D$: $1\le x+y\le3$ ו-$0\le x-y\le2$. נבחר $u=x+y$ ו-$v=x-y$ (מלבן $1\le u\le3$, $0\le v\le2$). אז $\dfrac{\partial(u,v)}{\partial(x,y)}=\begin{vmatrix}1&1\\1&-1\end{vmatrix}=-2$, ולכן $|J|=\tfrac12$ ו-$dA=\tfrac12\,du\,dv$. השטח הוא $\tfrac12\cdot2\cdot2=2$, ו-
$$\iint_D(x+y)\,dA=\tfrac12\int_1^3u\,du\int_0^2dv=\tfrac12\cdot4\cdot2=4.$$</div>
<p>באיור אפשר לעבור לתצוגת רשת $u,v$ ולראות את המקבילית הופכת למלבן:</p>
<div class="region-fig" data-region='{"inequalities":["x+y>=1","3>=x+y","x-y>=0","2>=x-y"],"boundary_curves":["x+y=1","x+y=3","y=x","y=x-2"],"substitution":{"u":"x+y","v":"x-y","u_range":[1,3],"v_range":[0,2],"abs_jacobian_xy_over_uv":"1/2"},"vertices":[[0.5,0.5],[1.5,1.5],[2.5,0.5],[1.5,-0.5]],"integrand":"x+y","value":"4","area":"2"}'></div>
<h3>דוגמה לא ליניארית</h3>
<p>התחום ברביע הראשון החסום בין הקרניים $y=x$ ו-$y=2x$ ובין ההיפרבולות $xy=1$ ו-$xy=4$. נבחר $u=\dfrac yx\in[1,2]$ ו-$v=xy\in[1,4]$. אז $\dfrac{\partial(u,v)}{\partial(x,y)}=\begin{vmatrix}-\frac y{x^2}&\frac1x\\y&x\end{vmatrix}=-\dfrac yx-\dfrac yx=-2u$ ולכן $|J|=\dfrac1{2u}$ והשטח הוא $\int_1^2\int_1^4\dfrac1{2u}\,dv\,du=\tfrac32\ln2$.</p>
<div class="region-fig" data-region='{"inequalities":["y>=x","2*x>=y","x*y>=1","4>=x*y"],"boundary_curves":["y=x","y=2*x","x*y=1","x*y=4"],"substitution":{"u":"y/x","v":"x*y","u_range":[1,2],"v_range":[1,4],"abs_jacobian_xy_over_uv":"x/(2*y)"},"area":"3*ln(2)/2"}'></div>
<div class="lesson-trap">⚠️ מציבים את הערך <b>המוחלט</b> של ההופכי: אם $\dfrac{\partial(u,v)}{\partial(x,y)}=-2$ אז הגורם הוא $\tfrac12$, לא $-2$ ולא $2$. וכשהיעקוביאן תלוי ב-$x,y$, מבטאים אותו דרך $u,v$ לפני האינטגרציה.</div>
` },
  questions: [
    { id: "C07-Q1",
      step: { type: "numeric", prompt: String.raw`נבחרו $u=y-x$ ו-$v=y+2x$. מהו $\left|\dfrac{\partial(x,y)}{\partial(u,v)}\right|$ ? ענו כמספר עשרוני.`,
              answer: 0.33333, tol: 0.001,
              explain: String.raw`$\dfrac{\partial(u,v)}{\partial(x,y)}=\begin{vmatrix}-1&1\\2&1\end{vmatrix}=-1-2=-3$, ולכן $\left|\dfrac{\partial(x,y)}{\partial(u,v)}\right|=\tfrac13\approx0.333$. מי שמציב את $3$ (בלי להפוך) מקבל תוצאה גדולה פי $9$.` },
      recap: "מחשבים $\\partial(u,v)/\\partial(x,y)$, ואת ההופכי שלו מציבים." },
    { id: "C07-Q2", question: String.raw`התחום ברביע הראשון חסום על ידי $y=x$, $y=2x$, $xy=1$ ו-$xy=4$. איזו הצבה הופכת אותו למלבן?`,
      options: [
        { id: "a", value: String.raw`$u=x+y,\ v=x-y$` },
        { id: "b", value: String.raw`$u=y-x,\ v=xy$` },
        { id: "c", value: String.raw`$u=x^2+y^2,\ v=\dfrac yx$` },
        { id: "d", value: String.raw`$u=\dfrac yx,\ v=xy$` },
      ],
      correctId: "d",
      explanation: String.raw`בהצבה $u=\tfrac yx$ ו-$v=xy$ ארבעת העקומים הם $u=1$, $u=2$, $v=1$, $v=4$: קבועים, ולכן התחום הוא המלבן $1\le u\le2$, $1\le v\le4$. בהצבה $u=x+y$, $v=x-y$ ההיפרבולה $xy=1$ אינה קבועה (היא $\tfrac{u^2-v^2}4=1$). בהצבה $u=y-x$ הקרן $y=2x$ היא $u=x$, לא קבועה. ובהצבה $u=x^2+y^2$ ההיפרבולות $xy=c$ אינן קבועות.`,
      recap: "כל עקום גבול צריך להיות $u=$ קבוע או $v=$ קבוע." },
    { id: "C07-Q3",
      step: { type: "numeric", prompt: String.raw`עם $u=\dfrac yx$ ו-$v=xy$ מתקבל $\left|\dfrac{\partial(u,v)}{\partial(x,y)}\right|=2u$. מהו $\left|\dfrac{\partial(x,y)}{\partial(u,v)}\right|$ בנקודה שבה $u=2$ ? ענו כמספר עשרוני.`,
              answer: 0.25, tol: 0.001,
              explain: String.raw`ההופכי של $2u=4$ הוא $\tfrac14=0.25$. בדרך כלל כותבים $|J|=\tfrac1{2u}$ לכל $u$.` },
      recap: "היעקוביאן ההפוך תלוי ב-$u$: $|J|=\\frac1{2u}$." },
    { id: "C07-Q4",
      step: { type: "numeric", prompt: String.raw`חשבו את שטח התחום $1\le\tfrac yx\le2,\ 1\le xy\le4$ כאינטגרל $\int_1^2\int_1^4\dfrac1{2u}\,dv\,du$. ענו כמספר עשרוני.`,
              answer: 1.0397, tol: 0.005,
              explain: String.raw`הפנימי $\int_1^4\tfrac1{2u}\,dv=\tfrac3{2u}$ ואז $\int_1^2\tfrac3{2u}\,du=\tfrac32\ln2\approx1.0397$.` },
      recap: "שטח = אינטגרל על המלבן של $|J|$." },
    { id: "C07-Q5", question: String.raw`נבחרו $u=x+y$ ו-$v=x-y$, ומתקבל $\dfrac{\partial(u,v)}{\partial(x,y)}=-2$. איך נראה אלמנט השטח $dA$ באינטגרל החדש?`,
      options: [
        { id: "a", value: String.raw`$-2\,du\,dv$` },
        { id: "b", value: String.raw`$2\,du\,dv$` },
        { id: "c", value: String.raw`$-\tfrac12\,du\,dv$` },
        { id: "d", value: String.raw`$\tfrac12\,du\,dv$` },
      ],
      correctId: "d",
      explanation: String.raw`מציבים את הערך המוחלט של ההופכי: $\left|\dfrac{1}{-2}\right|=\tfrac12$. הצבת $-2$ או $2$ שוכחת להפוך (השטח בעולם $(x,y)$ קטן מהשטח בעולם $(u,v)$ פי $2$), והצבת $-\tfrac12$ שוכחת את הערך המוחלט.`,
      recap: "$dA=\\left|\\frac{1}{\\partial(u,v)/\\partial(x,y)}\\right|du\\,dv$." },
    { id: "C07-Q6",
      step: { type: "findbug", prompt: String.raw`מוצג החישוב של $\iint_D(x+y)\,dA$ על התחום $1\le x+y\le3,\ 0\le x-y\le2$. כל שורה נבחנת כאמירה בפני עצמה, ובדיוק אחת מהן שגויה. סמנו אותה.`,
              lines: [
                String.raw`$u=x+y,\ v=x-y$, והתחום החדש: $1\le u\le3,\ 0\le v\le2$`,
                String.raw`$\left|\dfrac{\partial(u,v)}{\partial(x,y)}\right|=\left|\begin{vmatrix}1&1\\1&-1\end{vmatrix}\right|=2$`,
                String.raw`לכן $dA=2\,du\,dv$`,
                String.raw`$\iint_D(x+y)\,dA=\tfrac12\int_1^3u\,du\int_0^2dv$`,
                String.raw`$=\tfrac12\cdot4\cdot2=4$`,
              ],
              bugIndex: 2,
              explain: String.raw`מה שמציבים הוא ההופכי של $2$, כלומר $dA=\tfrac12\,du\,dv$, וכך מופיע בשורה שאחריה. שאר השורות נכונות.` },
      recap: "היעקוביאן שמציבים הוא ההופכי של $\\partial(u,v)/\\partial(x,y)$." },
  ],
});
