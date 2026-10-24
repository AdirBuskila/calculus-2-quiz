/* extrema course · level 2 - the Hessian test: classify a critical point */
COURSE_LEVEL("extrema", {
  id: "C02", order: 2, icon: "🧮", title: "סיווג בעזרת ההסיאן",
  goal: "לחשב $A,B,C,\\Delta$ בנקודה קריטית ולקבוע: מינימום, מקסימום או אוכף.",
  source: "ai-verified",
  lesson: { html: String.raw`
<p>נקודה קריטית היא רק מועמדת. כדי לדעת מה היא, בודקים את הנגזרות השנייה בה. מסמנים</p>
<div class="lesson-formula">$A=f_{xx},\quad B=f_{xy},\quad C=f_{yy},\quad \Delta=AC-B^2$</div>
<p>ומחשבים אותם <b>בנקודה הקריטית עצמה</b>. הכלל:</p>
<table>
<thead><tr><th>התנאי</th><th>המסקנה</th></tr></thead>
<tbody>
<tr><td>$\Delta>0$ ו-$A>0$</td><td>מינימום מקומי</td></tr>
<tr><td>$\Delta>0$ ו-$A<0$</td><td>מקסימום מקומי</td></tr>
<tr><td>$\Delta<0$</td><td>נקודת אוכף (לא קיצון)</td></tr>
<tr><td>$\Delta=0$</td><td>המבחן אינו מכריע</td></tr>
</tbody></table>
<div class="lesson-rule">🔑 <b>קודם $\Delta$, אחר כך הסימן של $A$.</b> רק כש-$\Delta>0$ הסימן של $A$ קובע בין מינימום למקסימום. כש-$\Delta<0$ אין חשיבות לסימן של $A$: זה אוכף.</div>
<div class="lesson-ex"><b>דוגמה.</b> $f(x,y)=xy(6-x-y)=6xy-x^2y-xy^2$ ובנקודה הקריטית $(2,2)$ מקבלים
$A=-2y=-4$, $B=6-2x-2y=-2$, $C=-2x=-4$. לכן $\Delta=(-4)(-4)-(-2)^2=12>0$ ו-$A<0$: <b>מקסימום מקומי</b>, והערך שלו $f(2,2)=8$.</div>
<div class="contour-fig" data-contour="24S-A-Q5b"></div>
<p>באיור: בנקודה $(2,2)$ קווי הגובה הם טבעות סביב המקסימום, ובשלוש הנקודות האחרות קווי הגובה נחתכים, כמו באוכף.</p>
<div class="lesson-trap">⚠️ <b>$A>0$ לא מספיק.</b> ל-$f=(x+y)^2-4y^2-48y$ יש נקודה קריטית $(6,-6)$ עם $A=2>0$, אבל $C=-6$ ו-$B=2$, ולכן $\Delta=-12-4=-16<0$. זה אוכף, לא מינימום.</div>
<div class="lesson-trap">⚠️ חשבו $\Delta=AC-B^2$ ולא רק $AC$. את $B$ מעלים בריבוע, ולכן הוא תמיד מוריד מ-$\Delta$.</div>
` },
  questions: [
    { id: "C02-Q1", question: String.raw`ל-$f(x,y)=x^2+3y^2$ יש נקודה קריטית $(0,0)$. מה היא?`,
      options: [
        { id: "a", value: "מינימום מקומי" },
        { id: "b", value: "מקסימום מקומי" },
        { id: "c", value: "נקודת אוכף" },
        { id: "d", value: "המבחן אינו מכריע" },
      ], correctId: "a",
      explanation: String.raw`$A=2$, $B=0$, $C=6$ ולכן $\Delta=12>0$ ו-$A>0$: מינימום מקומי. הערך $\Delta>0$ שולל אוכף ושולל מצב לא מכריע, והסימן החיובי של $A$ שולל מקסימום.`,
      recap: "$\\Delta>0$ ו-$A>0$ זה מינימום" },
    { id: "C02-Q2", step: { type: "numeric",
        prompt: String.raw`נתונה $f(x,y)=x^3+8y^3-6xy+1$. מהו $\Delta$ בנקודה הקריטית $(0,0)$?`,
        answer: -36, tol: 0,
        explain: String.raw`$f_{xx}=6x$, $f_{yy}=48y$ ו-$f_{xy}=-6$. בראשית $A=0$ ו-$C=0$, ולכן $\Delta=0\cdot0-(-6)^2=-36$.` },
      recap: "$B^2$ מוריד מ-$\\Delta$ גם כש-$A=C=0$" },
    { id: "C02-Q3", question: String.raw`ל-$f(x,y)=xy(6-x-y)$ יש נקודה קריטית $(2,2)$ שבה $A=-4$, ‏$B=-2$, ‏$C=-4$. מה היא?`,
      options: [
        { id: "a", value: "מקסימום מקומי" },
        { id: "b", value: "מינימום מקומי" },
        { id: "c", value: "נקודת אוכף" },
        { id: "d", value: "המבחן אינו מכריע" },
      ], correctId: "a",
      explanation: String.raw`$\Delta=(-4)(-4)-(-2)^2=12>0$ ו-$A=-4<0$: מקסימום מקומי. אוכף היה מתקבל רק אם $\Delta$ היה שלילי, ומינימום רק אם $A$ היה חיובי.`,
      recap: "$\\Delta>0$ ו-$A<0$ זה מקסימום" },
    { id: "C02-Q4", question: String.raw`ל-$f(x,y)=(x+y)^2-4y^2-48y$ יש נקודה קריטית $(6,-6)$ שבה $A=2$, ‏$B=2$, ‏$C=-6$. מה היא?`,
      options: [
        { id: "a", value: "נקודת אוכף" },
        { id: "b", value: "מינימום מקומי" },
        { id: "c", value: "מקסימום מקומי" },
        { id: "d", value: "המבחן אינו מכריע" },
      ], correctId: "a",
      explanation: String.raw`$\Delta=AC-B^2=2\cdot(-6)-2^2=-16<0$: אוכף. הסימן החיובי של $A$ מטעה ומוביל למינימום, אבל הוא רלוונטי רק כש-$\Delta>0$. מקסימום לא יכול להיות כי $\Delta<0$, והמבחן כן מכריע כי $\Delta\neq0$.`,
      recap: "$\\Delta<0$ זה אוכף, בלי קשר ל-$A$" },
    { id: "C02-Q5", step: { type: "numeric",
        prompt: String.raw`ל-$f(x,y)=x^3+y^3-3xy$ יש שתי נקודות קריטיות: $(0,0)$ ו-$(1,1)$. אחת מהן מינימום מקומי. מהו הערך של $f$ בו?`,
        answer: -1, tol: 0,
        explain: String.raw`$A=6x$, $B=-3$, $C=6y$. בראשית $\Delta=0-9=-9<0$: אוכף. ב-$(1,1)$ מתקבל $\Delta=36-9=27>0$ ו-$A=6>0$: מינימום מקומי, וערכו $f(1,1)=1+1-3=-1$.` },
      recap: "מסווגים כל נקודה, ואז מציבים בנקודה הנכונה" },
    { id: "C02-Q6", question: String.raw`בנקודה קריטית של $f$ התקבל $\Delta=5$ ו-$A=-3$. מה הנקודה?`,
      options: [
        { id: "a", value: "מקסימום מקומי" },
        { id: "b", value: "מינימום מקומי" },
        { id: "c", value: "נקודת אוכף" },
        { id: "d", value: "המבחן אינו מכריע" },
      ], correctId: "a",
      explanation: String.raw`$\Delta>0$ ולכן יש קיצון, והסימן של $A$ בוחר איזה: $A<0$ הוא מקסימום מקומי. אוכף דורש $\Delta<0$, ומצב לא מכריע דורש $\Delta=0$.`,
      recap: "קודם $\\Delta$, אחר כך הסימן של $A$" },
  ],
});
