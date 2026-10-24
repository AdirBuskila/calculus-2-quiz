import sympy as sp, numpy as np
from scipy import integrate
x,y,u,v,t=sp.symbols('x y u v t',real=True)
R={}
# 1a
a=sp.integrate(sp.integrate(x*sp.exp(x**2),(y,0,2-x**2)),(x,0,sp.sqrt(2)));R['1a']=sp.simplify(a);print('1a',R['1a'],sp.N(a),integrate.dblquad(lambda yy,xx:xx*np.exp(xx*xx),0,2**.5,0,lambda xx:2-xx*xx)[0])
# 1b paths
g=sp.log(1+x*y)/(x**2+y**2)
print('1b y=x',sp.limit(g.subs(y,x),x,0),'y=-x',sp.limit(g.subs(y,-x),x,0),'y=0',sp.limit(g.subs(y,0),x,0))
# 2b
f=(x**3+y**3)/(2*x**2+y**2)
print('2b diff along (t,t):',sp.limit((f.subs({x:t,y:t})-(t/2+t))/(sp.sqrt(2)*t),t,0,'+'))
# 3b
U,V=sp.symbols('U V',positive=True)
X=sp.sqrt(U*V);Y=1/V;Z=sp.exp(X**2*Y)
print('3b',sp.simplify(U*sp.diff(Z,U)-V*sp.diff(Z,V)-Z*X**2/V), 'wrong official z x^2/v^2 diff:',sp.simplify(U*sp.diff(Z,U)-V*sp.diff(Z,V)-Z*X**2/V**2))
# 4a
J=sp.Matrix([[-1,1],[y,x]]).det();print('J',J)
print('4a',sp.integrate(sp.integrate(-u,(u,0,1)),(v,1,2)))
# numeric 4a: region 0<=y-x<=1, 1<=xy<=2
N=2500;xs=np.linspace(1e-3,3,N);ys=np.linspace(1e-3,4,N);X_,Y_=np.meshgrid(xs,ys)
m=((Y_-X_)>=0)&((Y_-X_)<=1)&(X_*Y_>=1)&(X_*Y_<=2)
print('4a num',((X_**2-Y_**2)*m).sum()*(xs[1]-xs[0])*(ys[1]-ys[0]))
# 4b
th=np.linspace(0,2*np.pi,200001);xx=2*np.cos(th);yy=2*np.sin(th);F=xx**3+xx**2-3*xx+yy**2
print('4b',F.max(),F.min(),xx[F.argmax()],xx[F.argmin()])
# 5a
f5=(x-y)**3-3*x-y**2+5*y
sol=sp.solve([sp.diff(f5,x),sp.diff(f5,y)],[x,y],dict=True);print(sol)
H=sp.hessian(f5,(x,y))
for s in sol:
    h=H.subs(s);print(s,h.det(),h[0,0])
# 5b
fr=(16-5*x)/(x**2-5*x+6);print(sp.apart(fr),sp.series(fr,x,0,4))
print('f20',sp.diff(fr,x,20).subs(x,0)-sp.factorial(20)*(sp.Rational(3,2**20)-sp.Rational(1,3**21)))
