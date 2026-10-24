from sympy import *
import numpy as np
x,y,t,n,k,u,v=symbols('x y t n k u v',real=True)
f=4*x**3*y/(3*x**6+2*y**2)
print('1a',limit(f.subs(y,k*x**3),x,0),'polar-ish k=1:',simplify(f.subs(y,x**3)))
# 1b grid
th=np.linspace(0,2*np.pi,4001); r=np.linspace(0,3,1501)
R,T=np.meshgrid(r,th);X=R*np.cos(T);Y=R*np.sin(T);F=Y**4-X**4;print('1b',F.min(),F.max())
# 2a numeric partial sums
N_=200000
ns=np.arange(2,N_);print('2a-i abs',np.sum(1/(ns*np.log(ns)**2)),'integral tail',1/np.log(N_))
ns=np.arange(1,10**6);s=np.cumsum((-1.0)**ns*(np.sqrt(ns)-np.sqrt(ns-1)));print('2a-ii partial',s[-1],s[-2],'abs',np.sum(np.sqrt(ns)-np.sqrt(ns-1)))
# 2b
val=Rational(1,2)*integrate(integrate(v*exp(u*v),(v,-1,1)),(u,1,3));print('2b',val, N(val))
# direct numeric: region via x,y grid
from scipy import integrate as si
def integrand(yy,xx): return (xx-yy)*np.exp(xx**2-yy**2)
# region: 1<=x+y<=3, -1<=x-y<=1
val2=si.dblquad(lambda b,a:(b)*np.exp(a*b)/2,1,3,-1,1)[0];print('2b num',val2)
# 3a
an=lambda m:2**m/sqrt(5*m**2+1)
print('3a ratio',limit(an(n+1)/an(n),n,oo))
print('3a endpoint + terms*n',limit((Rational(1,2))**n*an(n)*n,n,oo))
# 3b
g=Function('g');z=y*g(x**2-y**2)
print('3b',simplify(diff(z,x)/x+diff(z,y)/y-z/y**2))
# 4a
print('4a',integrate(integrate(sin(pi*x**2/2),(x,y,1)),(y,0,1)), integrate(x*sin(pi*x**2/2),(x,0,1)))
# 4b
F4=(x**2-2*y**2)*exp(x-y)
sol=solve([diff(F4,x),diff(F4,y)],[x,y],dict=True);print('4b crit',sol)
H=hessian(F4,(x,y))
for s in sol: 
    Hs=H.subs(s);print(s,simplify(F4.subs(s)),simplify(Hs.det()),simplify(Hs[0,0]))
# 5a
f5=sqrt(x**2+2*y);gr=[diff(f5,w).subs({x:4,y:10}) for w in(x,y)];print('5a',f5.subs({x:4,y:10}),gr,sqrt(gr[0]**2+gr[1]**2))
print('5b',diff(log(1+x**2)-exp(2*x),x,6).subs(x,0))
