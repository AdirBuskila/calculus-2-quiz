# Independent blind solve of 22A-A (refuter). Does not reuse author harness.
import sympy as sp, numpy as np
from scipy import integrate
x,y,t,n=sp.symbols('x y t n',real=True)
R={}
# 1a
f=2*sp.sin(2*x+2*y); g=[sp.diff(f,v).subs({x:sp.pi/2,y:sp.pi/2}) for v in (x,y)]
print('1a grad',g,'max',sp.sqrt(g[0]**2+g[1]**2))
# 1b
g_=sp.Function('g'); s=y/(3*x)+g_(x*y)
print('1b',sp.simplify(x**2*sp.diff(s,x)-x*y*sp.diff(s,y)+2*y/3))
# 2a numerics: partial sums behave (abs conv by integral test sum 1/(n ln^2 n))
print('2a int', sp.integrate(1/(t*sp.log(t)**2),(t,2,sp.oo)))
print('2a2 sum', sp.summation(((-1)**n+n)/3**n,(n,1,sp.oo)))
# 2b
h=sp.symbols('h',real=True)
print('2b fx',sp.limit(h**2*sp.sin(1/sp.Abs(h))/h,h,0))
# 3a: terms sin(pi/sqrt n), decreasing from?
vals=[np.sin(np.pi/np.sqrt(k)) for k in range(1,12)]
print('3a terms',[round(v,3) for v in vals])
print('3a first n s.t. decreasing after', [k for k in range(1,200) if all(np.sin(np.pi/np.sqrt(j+1))<=np.sin(np.pi/np.sqrt(j))+1e-15 for j in range(k,400))][:1])
print('3a ratio limit', sp.limit(sp.sin(sp.pi/sp.sqrt(n+1))/sp.sin(sp.pi/sp.sqrt(n)),n,sp.oo))
# alt series at x+1=-1 numeric partial sums behave
S=np.cumsum([(-1)**k*np.sin(np.pi/np.sqrt(k)) for k in range(1,400001)]); print('3a alt partial',S[-3:])
S=np.cumsum([np.sin(np.pi/np.sqrt(k)) for k in range(1,400001)]); print('3a +end partial grows',S[[999,9999,99999,399999]])
# 3b
z=sp.symbols('z'); F=y**3+x*z+y**2+sp.exp(z)-3
pt={x:1,y:1,z:0}
print('3b F',F.subs(pt),[sp.diff(F,v).subs(pt) for v in (x,y,z)])
zx=-sp.diff(F,x).subs(pt)/sp.diff(F,z).subs(pt); zy=-sp.diff(F,y).subs(pt)/sp.diff(F,z).subs(pt); print('3b zx zy',zx,zy)
# 4a
u,v=x-0,0
Y=sp.symbols('Y')
# region: 1<=y-x<=2? statement: y-x=1, y=x+2 ; y^2=-4x, y^2=-4x+9
# numeric: Monte-Carlo-free exact grid integral over D (both pieces)
def inD(X,Yv):
    uu=Yv-X; vv=Yv**2+4*X
    return (uu>=1)&(uu<=2)&(vv>=0)&(vv<=9)
X,Yg=np.meshgrid(np.linspace(-12,5,6001),np.linspace(-14,8,6601)); dA=(17/6000)*(22/6600)
m=inD(X,Yg); w=np.exp(Yg-X)*(2*Yg+4)
print('4a pieces: y>0:',(w*(m&(Yg>0))).sum()*dA,' y<-4:',(w*(m&(Yg<-4))).sum()*dA,' ymin in D',Yg[m].min(),' ymax',Yg[m].max())
print('4a 9(e^2-e)=',float(9*(sp.E**2-sp.E)))
print('4a pieces area/signs: any point with -4.8<y<0 in D?',bool((m&(Yg>-4.5)&(Yg<0.5)).any()))
# 4b
f4=2*x**4+y**4-x**2-2*y**2
cps=sp.solve([sp.diff(f4,x),sp.diff(f4,y)],[x,y],dict=True)
print('4b crit',[(c[x],c[y],f4.subs(c)) for c in cps if c[x]**2+c[y]**2<=2])
b=sp.simplify(f4.subs(x**2,2-t)) ; tt=sp.symbols('tt'); bd=sp.expand(2*(2-tt)**2+tt**2-(2-tt)-2*tt); print('4b boundary in t=y^2',bd, sp.solve(sp.diff(bd,tt),tt))
th=np.linspace(0,2*np.pi,2000001); fb=2*(np.sqrt(2)*np.cos(th))**4+(np.sqrt(2)*np.sin(th))**4-2*np.cos(th)**2-4*np.sin(th)**2
print('4b boundary numeric max/min',fb.max(),fb.min())
gx,gy=np.meshgrid(np.linspace(-1.5,1.5,3001),np.linspace(-1.5,1.5,3001)); ins=gx**2+gy**2<=2
Fg=2*gx**4+gy**4-gx**2-2*gy**2; print('4b grid max/min',Fg[ins].max(),Fg[ins].min(), -9/8)
# 5a
k=sp.symbols('k',integer=True,nonnegative=True)
ser=sp.series(1/(x**2+x-2),x,0,8).removeO(); print('5a series',ser)
cf=lambda m: -sp.Rational(1,3)*(1+sp.Rational((-1)**m,2**(m+1)))
print('5a check',[cf(m) for m in range(8)])
# 5b
f5=x*y**2-y**2-x**2/2-2*x+3
cps=sp.solve([sp.diff(f5,x),sp.diff(f5,y)],[x,y],dict=True)
H=sp.hessian(f5,(x,y))
for c in cps: print('5b',c,f5.subs(c),H.subs(c).det(),H.subs(c)[0,0])
