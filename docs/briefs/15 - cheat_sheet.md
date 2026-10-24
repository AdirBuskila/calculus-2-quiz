# דף נוסחאות ומשפטים לכל הקורס

הסימונים כמו בדף הנוסחאות הרשמי של הקורס. כל סעיף מפנה לפרק המלא.

## 1. נגזרות חלקיות ודיפרנציאביליות ([[partials_differentiability]])
$$\frac{\partial f}{\partial x}(x,y)=\lim_{\Delta x\to0}\frac{f(x+\Delta x,y)-f(x,y)}{\Delta x},\qquad \frac{\partial f}{\partial y}(x,y)=\lim_{\Delta y\to0}\frac{f(x,y+\Delta y)-f(x,y)}{\Delta y}.$$
- **דיפרנציאבילית** ב-$(a,b)$: $\displaystyle\lim_{(h,k)\to(0,0)}\frac{f(a+h,b+k)-f(a,b)-f_xh-f_yk}{\sqrt{h^2+k^2}}=0$.
- **דיפרנציאל שלם:** $df=f_x\,dx+f_y\,dy$. **קירוב:** $f(x+\Delta x,y+\Delta y)\approx f(x,y)+df$.
- דיפרנציאבילית $\Rightarrow$ רציפה + נגזרות חלקיות. נגזרות חלקיות רציפות בסביבה $\Rightarrow$ דיפרנציאבילית. ההפכים לא נכונים.

## 2. גבולות ורציפות ([[limits_continuity]])
- הגבול קיים רק אם הוא זהה בכל מסלול. שני מסלולים עם ערכים שונים: **לא קיים**.
- רציפות: $\lim f=f(0,0)$.
- קוטבי: $|f-L|\le g(r)\to0$ עם חסם בלתי תלוי ב-$\theta$.

## 3. כלל השרשרת ([[chain_rule_identity]])
$$\frac{dz}{dt}=f_x\frac{dx}{dt}+f_y\frac{dy}{dt},\qquad \frac{\partial z}{\partial u}=f_x\frac{\partial x}{\partial u}+f_y\frac{\partial y}{\partial u},\quad \frac{\partial z}{\partial v}=f_x\frac{\partial x}{\partial v}+f_y\frac{\partial y}{\partial v}.$$
זהות אוילר (הומוגנית מדרגה $k$): $xf_x+yf_y+zf_z=kf$.

## 4. גרדיאנט, נגזרת כיוונית ומישור משיק ([[gradient_directional]])
- $\nabla f=(f_x,f_y)$ או $(f_x,f_y,f_z)$.
- $D_{\vec u}f=\nabla f\cdot\vec u=\|\nabla f\|\cos\delta$ עבור **וקטור יחידה** $\vec u$.
- מקסימום $\|\nabla f\|$ בכיוון $\nabla f$. מינימום $-\|\nabla f\|$. אפס בכיוון אנכי לגרדיאנט.
- מישור משיק ל-$F(x,y,z)=0$: $F_x(x-x_0)+F_y(y-y_0)+F_z(z-z_0)=0$.
- מישור משיק לגרף $z=f(x,y)$: $f_x(x-x_0)+f_y(y-y_0)-(z-z_0)=0$, $z_0=f(x_0,y_0)$.

## 5. פונקציה סתומה ([[implicit_function]])
אם $F(P)=0$, $F$ בעלת נגזרות חלקיות רציפות ו-$F_z(P)\neq0$, אז קיימת $z=f(x,y)$ יחידה ליד $P$ ו-
$$z_x=-\frac{F_x}{F_z},\qquad z_y=-\frac{F_y}{F_z}.$$

## 6. אקסטרמום מקומי ([[local_extrema]])
- נקודה קריטית: $f_x=f_y=0$ (או נגזרת לא קיימת). בנקודה קריטית $A=f_{xx}$, $B=f_{xy}$, $C=f_{yy}$, $\Delta=AC-B^2$:

| תנאי | מסקנה |
|---|---|
| $\Delta>0$, $A>0$ | מינימום מקומי |
| $\Delta>0$, $A<0$ | מקסימום מקומי |
| $\Delta<0$ | אוכף |
| $\Delta=0$ | המבחן לא מכריע |

## 7. אקסטרמום מוחלט ולגראנז' ([[absolute_extrema]])
- ויירשטראס: רציפה על סגור וחסום יש מקסימום ומינימום מוחלטים.
- מועמדים: נקודות קריטיות בפנים + קיצון על השפה + קודקודים. משווים ערכים.
- **לגראנז'** עם אילוץ אחד: $\nabla f=\lambda\nabla g$ ו-$g=0$. עם שני אילוצים: $\nabla f=\lambda\nabla g+\mu\nabla h$.

## 8. אינטגרל כפול ([[double_integrals]])
$$\iint_Rf\,dS=\int_a^b\!\!\int_{g_1(x)}^{g_2(x)}f\,dy\,dx$$
או בסדר ההפוך
$$\iint_Rf\,dS=\int_c^d\!\!\int_{h_1(y)}^{h_2(y)}f\,dx\,dy.$$
גבולות חיצוניים קבועים. שרטטו תחום לפני חילוף סדר. שטח: $\iint1\,dS$.

## 9. שינוי משתנים ([[change_of_variables]])
$$\iint_Rf(x,y)\,dS=\iint_Qf\bigl(x(u,v),y(u,v)\bigr)\left|\frac{\partial(x,y)}{\partial(u,v)}\right|du\,dv,\qquad\frac{\partial(x,y)}{\partial(u,v)}=\begin{vmatrix}x_u&x_v\\y_u&y_v\end{vmatrix}.$$
- קוטבי: $x=r\cos\varphi$, $y=r\sin\varphi$, יעקוביאן $r$.
- הפוך: $\left|\frac{\partial(x,y)}{\partial(u,v)}\right|=\left|\frac{\partial(u,v)}{\partial(x,y)}\right|^{-1}$.

## 10. אינטגרל לא אמיתי ([[improper_integrals]])
$\int_1^\infty\frac{dx}{x^p}$ מתכנס אם ורק אם $p>1$. $\int_0^1\frac{dx}{x^p}$ מתכנס אם ורק אם $p<1$. $\int_2^\infty\frac{dx}{x(\ln x)^2}=\frac1{\ln2}$ מתכנס; $\int_2^\infty\frac{dx}{x\ln x}$ מתבדר.

## 11. טורים מספריים ([[numeric_series]])
- **תנאי הכרחי:** $\sum a_n$ מתכנס $\Rightarrow a_n\to0$. אם $a_n\not\to0$: מתבדר.
- **הנדסי** $\sum q^n$: מתכנס אם $|q|<1$. **$p$:** $\sum\frac1{n^p}$ מתכנס אם $p>1$.
- **טורים חיוביים:** השוואה ($a_n\le b_n$), השוואה גבולית ($\frac{a_n}{b_n}\to l\in(0,\infty)$), אינטגרל, **קושי** ($\sqrt[n]{a_n}\to c$) ו-**דלאמבר** ($\frac{a_{n+1}}{a_n}\to D$): מתכנס אם $c,D<1$, מתבדר אם $>1$, לא מכריע אם $=1$.
- **לייבניץ:** $a_n\downarrow0\Rightarrow\sum(-1)^{n+1}a_n$ מתכנס, $0<S<a_1$.
- **בהחלט / בתנאי:** $\sum|a_n|$ מתכנס: בהחלט. רק $\sum a_n$ מתכנס: בתנאי.
- **סכום:** הנדסי $\frac{a_1}{1-q}$; טלסקופי: סכום חלקי ואז גבול.

## 12. טורי חזקות ([[power_series]])
- $R=\frac1c$ כאשר $c=\lim\sqrt[n]{|a_n|}$ (קושי-הדמר), או $R=\lim\left|\frac{a_n}{a_{n+1}}\right|$ (דלאמבר).
- מתכנס בהחלט ל-$|x|<R$ ומתבדר ל-$|x|>R$. **קצוות נבדקים בנפרד.** סביב $x_0$: $|x-x_0|<R$.
- גזירה ואינטגרציה איבר-איבר בתוך הקטע, הרדיוס נשמר.

## 13. טיילור ומקלורן ([[taylor_maclaurin]])
$$f(x)=\sum_{n=0}^\infty\frac{f^{(n)}(x_0)}{n!}(x-x_0)^n,\qquad f^{(n)}(0)=n!\,c_n.$$
$$e^x=\sum\frac{x^n}{n!},\quad\sin x=\sum\frac{(-1)^nx^{2n+1}}{(2n+1)!},\quad\cos x=\sum\frac{(-1)^nx^{2n}}{(2n)!},$$
$$\ln(1+x)=\sum_{n\ge1}\frac{(-1)^{n+1}x^n}{n}\ (-1<x\le1),\qquad\frac1{1-x}=\sum_{n\ge0}x^n\ (|x|<1).$$

## 14. אינטגרלים מיידיים שחוזרים בקורס
$$\int\frac{dx}{1+x^2}=\arctan x+c,\quad\int\frac{dx}{x}=\ln|x|+c,\quad\int\tan x\,dx=-\ln|\cos x|+c,\quad\int\frac{dx}{a^2+x^2}=\frac1a\arctan\frac xa+c.$$
זהויות: $\sin^2\alpha+\cos^2\alpha=1$, $\cos2\alpha=2\cos^2\alpha-1$ (לחישוב $\int\cos^2$ בקוטביות).
