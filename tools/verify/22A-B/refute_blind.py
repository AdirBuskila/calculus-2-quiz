import sympy as sp, numpy as np
from scipy import integrate
x,y,z,r,th,t,u,v=sp.symbols('x y z r th t u v',real=True)
g=sp.Matrix([sp.diff(sp.log(x**2+y**2+z**2),s) for s in (x,y,z)]).subs({x:1,y:2,z:1});print('1a',g.T,sp.sqrt(g.dot(g)))
print('1b',sp.integrate(sp.integrate(sp.sin(2+r**2)*r,(r,0,3)),(th,0,sp.pi)),sp.N(sp.pi/2*(sp.cos(2)-sp.cos(11))),
 integrate.dblquad(lambda xx,yy:np.sin(2+xx*xx+yy*yy),0,3,lambda yy:-np.sqrt(9-yy*yy),lambda yy:np.sqrt(9-yy*yy))[0])
n=np.arange(2,2000000,dtype=float);print('2a abs partial',np.sum(1/(n-np.log(n))**3))
n=np.arange(1,200);print('2b',np.sum((1+np.cos(n))/2.0**(n+1)))
f=(x**3+y**3)/(x**2+y**2);print('2c diff along (t,t)',sp.limit((f.subs({x:t,y:t})-2*t)/(sp.sqrt(2)*t),t,0,'+'))
n=np.arange(1,40);a=n/(n**2+1.);print('3a decreasing',np.all(np.diff(a)<0))
nn=sp.symbols('nn',positive=True);print('3a lc 1/n',sp.limit((nn/(nn**2+1))/(1/nn),nn,sp.oo))
F=z**3-3*x*y*z-4;zz=sp.Function('zz')(x,y)
eq=zz**3-3*x*y*zz-4
zx=sp.solve(sp.diff(eq,x),sp.diff(zz,x))[0];zy=sp.solve(sp.diff(eq,y),sp.diff(zz,y))[0]
zxy=sp.diff(zx,y).subs(sp.diff(zz,y),zy).subs(sp.diff(zz,x),zx)
pt={zz:-2};print('3b',zx.subs(zz,-2).subs({x:2,y:1}),zy.subs(zz,-2).subs({x:2,y:1}),sp.simplify(zxy.subs(zz,-2).subs({x:2,y:1})))
# numeric check z_xy via solving cubic
import mpmath as mp
def Z(X,Y): return mp.findroot(lambda w:w**3-3*X*Y*w-4,-2)
mp.mp.dps=30;print('3b num',mp.diff(lambda X,Y:Z(X,Y),(2,1),(1,1)))
print('4a',sp.integrate(sp.integrate(u/v/3,(u,1,4)),(v,6,8)),sp.N(sp.Rational(5,2)*sp.log(sp.Rational(4,3))))
X_,Y_=np.meshgrid(np.linspace(-2,4,6001),np.linspace(0,14,14001))
m=((Y_-X_)>=1)&((Y_-X_)<=4)&((2*X_+Y_)>=6)&((2*X_+Y_)<=8)
print('4a num',(np.where(m,(Y_-X_)/np.where(m,2*X_+Y_,1),0)).sum()*1e-6)
th_=np.linspace(0,2*np.pi,2000001);xx=1+np.cos(th_);yy=1+np.sin(th_);F_=1-xx**2-yy**2
print('4b boundary',F_.max(),F_.min(),2*2**.5-2,-2-2*2**.5)
# interior has no crit pt (0,0 outside disc)
print('5a',sp.series(sp.atan(x),x,0,9))
f5=x**3+8*y**3-6*x*y+1
sol=sp.solve([sp.diff(f5,x),sp.diff(f5,y)],[x,y],dict=True);print([s for s in sol if all(sp.im(vv)==0 for vv in s.values())])
H=sp.hessian(f5,(x,y))
for s in sol:
    if all(sp.im(vv)==0 for vv in s.values()): h=H.subs(s);print(s,h.det(),h[0,0])
