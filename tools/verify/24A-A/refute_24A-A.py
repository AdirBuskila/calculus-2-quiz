# Independent blind solve of 24A-A (refuter).
import sympy as sp, numpy as np
x,y,z,n,r,th=sp.symbols('x y z n r th',real=True)
# 1a continuity
print('1a polar',sp.simplify((r**3*sp.cos(th)**3*r*sp.sin(th)-r*sp.cos(th)*r**3*sp.sin(th)**3)/r**2/r**2*r**2) if False else sp.simplify((r**4*sp.cos(th)*sp.sin(th)*(sp.cos(th)**2-sp.sin(th)**2))/r**2))
print('1a bound |f|<=r^2/2 ->0 continuous')
# 1b
f=2*sp.exp(-x**2)+sp.exp(-3*y**2); print('1b grad',[sp.simplify(sp.diff(f,w).subs({x:1,y:0})) for w in (x,y)])
# 2a
a1=np.array([(-1)**k*np.sin(1/np.sqrt(k)) for k in range(1,2000001)]); print('2a1 partial',np.cumsum(a1)[-2:],' abs ~',sp.limit(sp.sin(1/sp.sqrt(n))*sp.sqrt(n),n,sp.oo),' monotone',all(np.sin(1/np.sqrt(k))>np.sin(1/np.sqrt(k+1)) for k in range(1,10000)))
a2=np.array([(-1)**k*(np.sqrt(k)-np.sqrt(k-1)) for k in range(1,2000001)]); print('2a2 partial',np.cumsum(a2)[-2:],' abs ~',sp.limit((sp.sqrt(n)-sp.sqrt(n-1))*sp.sqrt(n),n,sp.oo),' monotone dec',all(np.sqrt(k)-np.sqrt(k-1)>np.sqrt(k+1)-np.sqrt(k) for k in range(1,10000)))
# 2b
h=sp.symbols('h',real=True)
fxy=lambda X,Y:X*Y*(X**2-Y**2)/(X**2+Y**2)
print('2b fx(0,0)=',sp.limit(fxy(h,0)/h,h,0),' fy=',sp.limit(fxy(0,h)/h,h,0))
print('2b differentiability limit r*cos*sin*cos2th ->',sp.limit(r*sp.cos(th)*sp.sin(th)*sp.cos(2*th),r,0), '(|.|<=r/2, differentiable)')
# 3a
print('3a ratio',sp.limit(2*(n**2+1)/((n+1)**2+1),n,sp.oo),' R=1/2: |x+1|<1/2; endpoints terms 1/(n^2+1) abs conv')
print('3a sum of endpoint check',float(sp.summation(1/(n**2+1),(n,1,sp.oo)).evalf()) if False else sum(1/(k**2+1) for k in range(1,10**6)))
# 3b Euler: use symbolic F
F=sp.Function('F'); k=sp.symbols('k'); u=x**k*F(z/x,y/x)
print('3b',sp.simplify((x*sp.diff(u,x)+y*sp.diff(u,y)+z*sp.diff(u,z)-k*u).doit()))
# 4a
print('4a',sp.summation(1/(n**2+6*n+8),(n,1,sp.oo)),sp.Rational(7,24))
# 4b
t=sp.symbols('t'); fb=sp.sqrt(2)*sp.cos(t)*sp.sqrt(2)*sp.sin(t)
tt=np.linspace(0,2*np.pi,2000001); vals=2*np.cos(tt)*np.sin(tt); print('4b max/min',vals.max(),vals.min(),'at',np.sqrt(2)*np.cos(tt[vals.argmax()]),np.sqrt(2)*np.sin(tt[vals.argmax()]),np.sqrt(2)*np.cos(tt[vals.argmin()]),np.sqrt(2)*np.sin(tt[vals.argmin()]))
lam=sp.symbols('lam'); print('4b lagrange',sp.solve([y-2*lam*x,x-2*lam*y,x**2+y**2-2],[x,y,lam],dict=True))
# 5a
f5=x**3+8*y**3-6*x*y+1; cp=sp.solve([sp.diff(f5,x),sp.diff(f5,y)],[x,y],dict=True); H=sp.hessian(f5,(x,y))
print('5a real crit',[ (c,f5.subs(c),H.subs(c).det(),H.subs(c)[0,0]) for c in cp if all(sp.im(v)==0 for v in c.values())])
# 5b
f6=1/(1-3*x**2); s=sp.series(f6,x,0,10).removeO(); print('5b',s,' f5(0)=',sp.diff(f6,x,5).subs(x,0),' R=',1/sp.sqrt(3))
