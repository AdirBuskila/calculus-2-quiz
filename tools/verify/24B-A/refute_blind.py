from sympy import *
import numpy as np
x,y,t,n,k=symbols('x y t n k',real=True)
f=y*x**2/(2*y**2+3*x**4)
print('Q1a along y=kx^2',simplify(f.subs(y,k*x**2)), limit(f.subs(y,k*x**2),x,0))
print('Q1c', diff(f,x).subs({x:1,y:1}), diff(f,y).subs({x:1,y:1}))
# 2a bound, 2b alternating & abs diverge
print('2b abs int', integrate(1/(t*log(t)),(t,2,oo)))
g=2*x**2-y**2+1
print('3 grad',[diff(g,v).subs({x:2,y:3}) for v in(x,y)])
print('3c crit',solve([diff(g,x),diff(g,y)],[x,y]), hessian(g,(x,y)))
# 3d numeric grid
th=np.linspace(0,2*np.pi,2001); r=np.linspace(0,1,1001)
R,T=np.meshgrid(r,th); X=1+R*np.cos(T);Y=R*np.sin(T)
F=2*X**2-Y**2+1; print('3d',F.min(),F.max(), Rational(2,3).evalf())
# 4a
G=2*x**2-y**2+symbols('z')**2
z=symbols('z'); G=2*x**2-y**2+z**2
gr=[diff(G,v).subs({x:1,y:-1,z:2}) for v in(x,y,z)];print('4a',gr)
# 4b ratio
a=lambda n:2**n*factorial(n)/factorial(2*n)
print('4b ratio',simplify(a(n+1)/a(n)))
# 5
F5=log(2*x**2+3*x+1); print('5 ser',series(F5,x,0,7))
print('5c', diff(F5,x,5).subs(x,0))
print('5b numerics: x=1/2 sum', N(summation(((-1)**(n+1)*(2**n+1)/n*Rational(1,2)**n),(n,1,oo))), N(F5.subs(x,Rational(1,2))))
print('x=-1/2 ratio check', [N(F5.subs(x,-Rational(1,2)+Rational(1,10**j))) for j in (3,6,9)])
