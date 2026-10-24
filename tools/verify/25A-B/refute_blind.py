from sympy import *
import numpy as np
x,y,t,n,k,u,v=symbols('x y t n k u v',real=True)
f=sqrt(41-4*x**2-y**2)
f0=f.subs({x:2,y:3});fx=diff(f,x).subs({x:2,y:3});fy=diff(f,y).subs({x:2,y:3})
lin=f0+fx*Rational(1,10)+fy*(-Rational(1,10));print('1a',f0,fx,fy,lin,N(lin),N(f.subs({x:2.1,y:2.9})))
th=np.linspace(0,2*np.pi,100001);print('1b',(np.sqrt(2)*np.cos(th)*np.sqrt(2)*np.sin(th)).min(),(2*np.cos(th)*np.sin(th)).max())
print('2a',summation(1/(n*(n-1)),(n,2,oo)))
print('2b',integrate(integrate(u/v,(u,1,4)),(v,6,8))/3, N(Rational(5,2)*log(Rational(4,3))))
# check Jacobian & numeric over region directly
from scipy import integrate as si
# region in x,y: u=y-x in[1,4], v=2x+y in[6,8]; x=(v-u)/3, y=(v+2u)/3
J=Matrix([(v-u)/3,(v+2*u)/3]).jacobian([u,v]);print('J',J.det())
val=si.dblquad(lambda vv,uu:uu/vv/3,1,4,6,8)[0];print('2b num',val)
# 3a
print('3a coeff',limit(sin(1/n)**2*n**2,n,oo))
g=Function('g');z=y*g(cos(x-y));print('3b',simplify(diff(z,x)+diff(z,y)-z/y), simplify(diff(z,x)), simplify(diff(z,y)))
print('3b dt/dy (t=cos(x-y))',diff(cos(x-y),y))
# 4a numeric check with f=1 and f=x+y^2
for ff in (lambda X,Y:1+0*X, lambda X,Y:X*Y+X**2+Y):
    a=si.dblquad(lambda Y,X:ff(X,Y),-4,0,lambda X:0,lambda X:np.sqrt(X+4))[0]+si.dblquad(lambda Y,X:ff(X,Y),0,2,lambda X:0,lambda X:2-X)[0]
    b=si.dblquad(lambda X,Y:ff(X,Y),0,2,lambda Y:Y**2-4,lambda Y:2-Y)[0];print('4a',a,b)
# 4b
F=x**3+8*y**3-6*x*y+1
sol=solve([diff(F,x),diff(F,y)],[x,y],dict=True);print(sol)
H=hessian(F,(x,y))
for s in sol:
    if all(im(val)==0 for val in s.values()): print(s,F.subs(s),H.subs(s).det(),H.subs(s)[0,0])
# 5a
f5=y*cos(x*y);print('5a grad',[diff(f5,w).subs({x:1,y:0}) for w in(x,y)])
# 5b
F5=1/(x**2-5*x+6);print('5b',diff(F5,x,5).subs(x,0), Rational(3325,1944), series(F5,x,0,6))
