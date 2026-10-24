/* double_int, level 6 - polar coordinates and the Jacobian r */
COURSE_LEVEL("double_int", {
  id: "C06", order: 6, icon: "🎯", title: "קואורדינטות קוטביות והיעקוביאן r",
  goal: "לעבור לקואורדינטות קוטביות בתחום מעגלי, לכתוב את הגבולות, לא לשכוח את הגורם r, ולחשב.",
  source: "ai-verified",
  lesson: { html: String.raw`
<p>כשהתחום מורכב ממעגלים סביב הראשית, מקטעי מעגל או ישרים דרך הראשית, כדאי לעבור לקואורדינטות קוטביות:</p>
<div class="lesson-formula">$$x=r\cos\theta,\qquad y=r\sin\theta,\qquad x^2+y^2=r^2,\qquad dx\,dy=r\,dr\,d\theta$$</div>
<div class="lesson-rule">🔑 <b>היעקוביאן הוא $r$.</b> האלמנט הקטן בקואורדינטות קוטביות הוא מלבן "קשת" ברוחב $dr$ ובאורך $r\,d\theta$, ולכן השטח שלו $r\,dr\,d\theta$. שוכחים את $r$ ומקבלים תשובה שגויה.</div>
<table><thead><tr><th>התחום</th><th>גבולות</th></tr></thead><tbody>
<tr><td>דיסק $x^2+y^2\le a^2$</td><td>$0\le r\le a,\ 0\le\theta\le2\pi$</td></tr>
<tr><td>חצי דיסק עליון ($y\ge0$)</td><td>$0\le r\le a,\ 0\le\theta\le\pi$</td></tr>
<tr><td>רבע ראשון</td><td>$0\le\theta\le\tfrac\pi2$</td></tr>
<tr><td>טבעת $a^2\le x^2+y^2\le b^2$</td><td>$a\le r\le b$</td></tr>
<tr><td>הישר $y=mx$ ($x>0$)</td><td>$\theta=\arctan m$</td></tr>
</tbody></table>
<div class="lesson-ex">דוגמה: $\iint_{x^2+y^2\le4}\left(x^2+y^2\right)dA=\int_0^{2\pi}\!\int_0^2 r^2\cdot r\,dr\,d\theta=2\pi\cdot\tfrac{2^4}{4}=8\pi$.</div>
<div class="region-fig" data-region='{"inequalities":["x>=0","y>=0","x^2+y^2>=1","4>=x^2+y^2"],"boundary_curves":["x^2+y^2=1","x^2+y^2=4"],"polar":{"r":[1,2],"theta":[0,"pi/2"]},"area":"3*pi/4"}'></div>
<h3>מעגל שעובר דרך הראשית</h3>
<p>המעגל $x^2+y^2=2x$ הוא $(x-1)^2+y^2=1$. מציבים: $r^2=2r\cos\theta$ ולכן $r=2\cos\theta$, והתחום הפנימי הוא $0\le r\le2\cos\theta$ עבור $-\tfrac\pi2\le\theta\le\tfrac\pi2$. הגבולות של $r$ כאן תלויים ב-$\theta$.</p>
<div class="region-fig" data-region='{"inequalities":["2*x>=x^2+y^2"],"boundary_curves":["x^2+y^2=2*x"],"orderXY":{"x":[0,2],"y":["-sqrt(2*x-x^2)","sqrt(2*x-x^2)"]},"polar":{"r":[0,"2*cos(theta)"],"theta":["-pi/2","pi/2"]},"area":"pi"}'></div>
<div class="lesson-trap">⚠️ $x^2+y^2=a^2$ נותן $r=a$ ולא $r=a^2$. ו-$\arctan\frac yx=\theta$ רק כש-$x>0$.</div>
` },
  questions: [
    { id: "C06-Q1", question: String.raw`מהם הגבולות בקואורדינטות קוטביות של חצי הדיסק $x^2+y^2\le9,\ y\ge0$ ?`,
      options: [
        { id: "a", value: String.raw`$0\le r\le9,\ 0\le\theta\le\pi$` },
        { id: "b", value: String.raw`$0\le r\le3,\ 0\le\theta\le2\pi$` },
        { id: "c", value: String.raw`$0\le r\le3,\ -\tfrac\pi2\le\theta\le\tfrac\pi2$` },
        { id: "d", value: String.raw`$0\le r\le3,\ 0\le\theta\le\pi$` },
      ],
      correctId: "d",
      explanation: String.raw`$r^2\le9$ נותן $0\le r\le3$, ו-$y=r\sin\theta\ge0$ נותן $0\le\theta\le\pi$. הטווח $r\le9$ נובע משכחת השורש. $0\le\theta\le2\pi$ מתאר את כל הדיסק, ו-$-\tfrac\pi2\le\theta\le\tfrac\pi2$ מתאר את החצי הימני ($x\ge0$).`,
      recap: "רדיוס $a$: $r\\le a$. $y\\ge0$: $\\theta\\in[0,\\pi]$." },
    { id: "C06-Q2",
      step: { type: "numeric", prompt: String.raw`חשבו את $\iint_{x^2+y^2\le1}\left(x^2+y^2\right)dA$ בקואורדינטות קוטביות. ענו כמספר עשרוני.`,
              answer: 1.5708, tol: 0.001,
              explain: String.raw`$\int_0^{2\pi}\int_0^1 r^2\cdot r\,dr\,d\theta=2\pi\cdot\tfrac14=\tfrac\pi2\approx1.5708$. מי ששוכח את הגורם $r$ מקבל $2\pi\cdot\tfrac13\approx2.094$.` },
      recap: "מציבים $x^2+y^2=r^2$ ולא שוכחים את $r$ של היעקוביאן." },
    { id: "C06-Q3", question: String.raw`בהחלפה לקואורדינטות קוטביות, $dx\,dy$ הופך ל:`,
      options: [
        { id: "a", value: String.raw`$r^2\,dr\,d\theta$` },
        { id: "b", value: String.raw`$r\,dr\,d\theta$` },
        { id: "c", value: String.raw`$dr\,d\theta$` },
        { id: "d", value: String.raw`$\tfrac1r\,dr\,d\theta$` },
      ],
      correctId: "b",
      explanation: String.raw`היעקוביאן $\begin{vmatrix}\cos\theta&-r\sin\theta\\\sin\theta&r\cos\theta\end{vmatrix}=r\cos^2\theta+r\sin^2\theta=r$. לכן $dx\,dy=r\,dr\,d\theta$. בלי $r$ מתעלמים מכך שאלמנט השטח גדל ככל שמתרחקים מהראשית.`,
      recap: "$dx\\,dy=r\\,dr\\,d\\theta$." },
    { id: "C06-Q4",
      step: { type: "numeric", prompt: String.raw`חשבו את שטח הטבעת ברביע הראשון $1\le x^2+y^2\le4,\ x\ge0,\ y\ge0$. ענו כמספר עשרוני.`,
              answer: 2.3562, tol: 0.002,
              explain: String.raw`$\int_0^{\pi/2}\int_1^2 r\,dr\,d\theta=\tfrac\pi2\cdot\left(\tfrac{4-1}{2}\right)=\tfrac{3\pi}4\approx2.356$. בדיקה: רבע מהפרש שטחי המעגלים, $\tfrac14(4\pi-\pi)=\tfrac{3\pi}4$.` },
      recap: "שטח בקוטביות: $\\iint r\\,dr\\,d\\theta$." },
    { id: "C06-Q5", question: String.raw`מהי המשוואה בקואורדינטות קוטביות של המעגל $x^2+y^2=4x$ ?`,
      options: [
        { id: "a", value: "$r=4$" },
        { id: "b", value: String.raw`$r=2\cos\theta$` },
        { id: "c", value: String.raw`$r=4\sin\theta$` },
        { id: "d", value: String.raw`$r=4\cos\theta$` },
      ],
      correctId: "d",
      explanation: String.raw`מציבים $r^2=4r\cos\theta$ ומצמצמים ב-$r\neq0$: $r=4\cos\theta$. המעגל הוא $(x-2)^2+y^2=4$ שעובר דרך הראשית. $r=4$ הוא מעגל סביב הראשית. $r=2\cos\theta$ הוא המעגל $x^2+y^2=2x$ (רדיוס $1$), ו-$r=4\sin\theta$ הוא מעגל שמרכזו על ציר $y$.`,
      recap: "מעגל דרך הראשית עם מרכז על ציר $x$: $r=2a\\cos\\theta$." },
    { id: "C06-Q6",
      step: { type: "order", prompt: String.raw`סדרו את שלבי החישוב של $\iint_D xy\,dA$ כאשר $D$ הוא הרבע של הדיסק $x^2+y^2\le4$ ברביע הראשון.`,
              lines: [
                String.raw`מציבים $x=r\cos\theta,\ y=r\sin\theta$ ו-$dA=r\,dr\,d\theta$; התחום: $0\le r\le2,\ 0\le\theta\le\tfrac\pi2$`,
                String.raw`$\iint_D xy\,dA=\int_0^{\pi/2}\int_0^2 r^2\cos\theta\sin\theta\cdot r\,dr\,d\theta$`,
                String.raw`האינטגרל מתפצל: $\int_0^2r^3\,dr\cdot\int_0^{\pi/2}\sin\theta\cos\theta\,d\theta$`,
                String.raw`$=4\cdot\tfrac12$`,
                String.raw`$=2$`,
              ],
              explain: String.raw`קודם ההצבה והגבולות, אחר כך האינטגרל עם $r$ של היעקוביאן, אחר כך ההפרדה (התחום מלבן ב-$(r,\theta)$), ובסוף הערכים: $\int_0^2r^3dr=4$ ו-$\int_0^{\pi/2}\sin\theta\cos\theta\,d\theta=\tfrac12$.` },
      recap: "בקוטביות תחום מעגלי הופך למלבן ומפרידים." },
  ],
});
