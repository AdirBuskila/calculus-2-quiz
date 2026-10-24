# כלל השרשרת והוכחת זהויות

## מה המבחן שואל
כמעט בכל מבחן יש סעיף "הראו שהפונקציה $z=\ldots g(\ldots)$ מקיימת את המשוואה ...", כאשר $g$ היא פונקציה גזירה **כללית** (לא נתונה במפורש). זו שאלה מכנית אחרי שמכירים את התבנית.

- פונקציה של פונקציה אחת עם כפל: `22A-A-Q1b` ו-`24A-B-Q3b` ($z=\frac{y}{3x}+g(xy)$), `23A-C-Q3b` ו-`25A-A-Q3b` ($z=y\,g(x^2-y^2)$), `25A-B-Q3b` ($z=y\,g(\cos(x-y))$).
- פונקציה של שני משתנים-ביניים: `23A-A-Q3b` ($g(x,y,z)=f(\frac1y-\frac1x,\;xye^{-z^2/2})$), `24A-A-Q3b` ($u=x^kF(\frac zx,\frac yx)$, זהות אוילר).
- שינוי משתנים בנגזרות: `26A-A-Q3b` ($z=e^{x^2y}$ עם $x=\sqrt{uv}$, $y=\frac1v$).
- חישוב מספרי עם נתונים בנקודה: `24B-B-Q4a` ($z(u,v)=2uv+3v^2$) ו-`24S-A-Q4a` ($f(2t+1,e^t)=3$).

## הגדרות ומשפטים
לפי דף הנוסחאות:

- אם $z=f(x,y)$ דיפרנציאבילית ו-$x=x(t)$, $y=y(t)$ גזירות, אז $\dfrac{dz}{dt}=\dfrac{\partial f}{\partial x}\dfrac{dx}{dt}+\dfrac{\partial f}{\partial y}\dfrac{dy}{dt}$.
- אם $x=x(u,v)$, $y=y(u,v)$ אז
$$\frac{\partial z}{\partial u}=\frac{\partial f}{\partial x}\frac{\partial x}{\partial u}+\frac{\partial f}{\partial y}\frac{\partial y}{\partial u},\qquad \frac{\partial z}{\partial v}=\frac{\partial f}{\partial x}\frac{\partial x}{\partial v}+\frac{\partial f}{\partial y}\frac{\partial y}{\partial v}.$$
- כלל מעשי: מסמנים את המשתנה הפנימי באות חדשה ($t=xy$), וכותבים $z=\ldots+g(t)$. אז $\frac{\partial}{\partial x}g(t)=g'(t)\,\frac{\partial t}{\partial x}$.
- **פונקציה הומוגנית** מדרגה $k$: $f(\lambda x,\lambda y,\lambda z)=\lambda^kf(x,y,z)$. אז $xf_x+yf_y+zf_z=kf$ (זהות אוילר). הצורה $u=x^kF(\frac zx,\frac yx)$ כבר מראה זאת.

## מתכון פתרון
1. **סמנו את המשתנים הפנימיים** ($t$, או $u,v$) וכתבו את $z$ באמצעותם.
2. **רשמו את נגזרות הפנימיים:** $t_x,t_y$ (או $u_x,u_y,v_x,v_y$).
3. **כלל השרשרת:** $z_x=\ldots$, $z_y=\ldots$, תוך שמירה על כלל המכפלה כשיש גורם חופשי ($y\cdot g(t)$ נותן $g(t)+y\,g'(t)\,t_y$).
4. **הציבו באגף השמאל** של המשוואה והראו שהמונחים עם $g'$ מצטמצמים, ושמה שנשאר שווה לאגף הימין. לפעמים צריך להחליף את הביטוי החופשי בעזרת $z$.
5. בשאלות מספריות: חשבו את כל הנגזרות החלקיות **בנקודה** ורק אז הציבו.

## מלכודות
> 🪤 ב-`25A-B-Q3b` $t=\cos(x-y)$, ולכן $\frac{\partial t}{\partial x}=-\sin(x-y)$ אבל $\frac{\partial t}{\partial y}=+\sin(x-y)$. בפתרון שבקובץ נכתב $\frac{\partial t}{\partial x}$ במקום $\frac{\partial t}{\partial y}$ והוא תוקן. סימנים לפי $y$ הפוכים מסימנים לפי $x$ כשיש $x-y$.

> 🪤 כשכופלים ב-$y$: $z=y\,g(x^2-y^2)$ נגזר לפי $y$ **בכלל המכפלה**: $\frac{\partial z}{\partial y}=g(t)+y\,g'(t)(-2y)$. לשכוח את $g(t)$ הוא הטעות הנפוצה.

> 🪤 ב-`24S-A-Q4a` לא צריך לדעת מי $f$. הנתון $f(2t+1,e^t)=3$ קבוע, ולכן הנגזרת לפי $t$ היא $0$: $2f_x+e^tf_y=0$. עם $f_x=\frac{e^t}{2}$ מקבלים $f_y=-1$.

> ⚠️ אין לכתוב $g'_x$ כשהכוונה ל-$g'(t)$. בעבודה עם $g(t)$ הנגזרת היא $\frac{dg}{dt}$ (משתנה אחד), ובעבודה עם $f(u,v)$ היא $\frac{\partial f}{\partial u}$.

> 💡 ב-`26A-A-Q3b` אפשר לחסוך חישוב: $x^2y=uv\cdot\frac1v=u$, לכן $z=e^u$ ו-$z_v=0$. אז $uz_u-vz_v=ue^u$, ואגף ימין $z\frac{x^2}{v}=e^u\cdot u$. הפתרון הרשמי עובר דרך כלל השרשרת המלא, שניהם נכונים.

## דוגמה פתורה
(`25A-A-Q3b`, שווה ל-`23A-C-Q3b`) הראו ש-$z=y\,g(x^2-y^2)$ מקיימת $\dfrac1x\dfrac{\partial z}{\partial x}+\dfrac1y\dfrac{\partial z}{\partial y}=\dfrac{z}{y^2}$.

נסמן $t=x^2-y^2$, אז $t_x=2x$ ו-$t_y=-2y$.
$$\frac{\partial z}{\partial x}=y\,g'(t)\cdot2x=2xy\,g'(t),\qquad \frac{\partial z}{\partial y}=g(t)+y\,g'(t)\cdot(-2y)=g(t)-2y^2g'(t).$$
מציבים:
$$\frac1x\cdot2xy\,g'(t)+\frac1y\bigl(g(t)-2y^2g'(t)\bigr)=2y\,g'(t)+\frac{g(t)}y-2y\,g'(t)=\frac{g(t)}y.$$
ומצד שני $\dfrac{z}{y^2}=\dfrac{y\,g(t)}{y^2}=\dfrac{g(t)}y$. הצדדים שווים.

**דוגמה לזהות אוילר** (`24A-A-Q3b`): אם $z=xy\,g(\frac xy)$ אז $xz_x+yz_y=2z$, כי הפונקציה הומוגנית מדרגה $2$.
