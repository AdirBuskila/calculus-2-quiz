from sympy import *
x,y,h,k,t,u,v,n=symbols('x y h k t u v n',real=True)
print(limit((x**2-y**2)/(x**2+y**2),x,0) if False else '')
# limits_diff checks
print(Rational(6,5), (2*x**2*(-x**2))/(x**4+x**4))
r,th=symbols('r th')
print(maximum(cos(th)**2*sin(th),th,Interval(0,pi/2)).evalf(4))
f=(x**3)/(x**2+y**2); Q=(f.subs({x:h,y:h})-h)/(sqrt(2)*h); print(simplify(Q), N(Q.subs(h,1)))
print(N(((h**3)/(2*h**2))/(h*sqrt(2)),4).subs(h,1))
# chain
g=Function('g'); 
f=u*v**2; G=f.subs({u:x+y,v:x-y}); print(diff(G,x).subs({x:2,y:1}))
z=(u**2+3*u*v).subs({u:x**2*y,v:x-y}); print(diff(z,x).subs({x:1,y:1}),diff(z,y).subs({x:1,y:1}))
print(diff((x*y)**3,x,y).subs({x:1,y:2}), diff(x*(x*y)**2,x).subs({x:1,y:2}), diff(y/(3*x)+(x*y)**2,y).subs({x:1,y:1}), diff((x**2-3*y)**2,y).subs({x:2,y:1}))
# series
print(diff(x**2*exp(x),x,5).subs(x,0), diff(sin(x**2),x,6).subs(x,0), diff(1/((1-x)*(1-2*x)),x,4).subs(x,0))
print(summation(1/3**n,(n,2,oo)), 1/(3*sqrt(3)/2*3))
N_=symbols('N'); print([i for i in range(1,30) if 1/(i+1)**2<=0.01][0])
print(limit(((n+1)**2/2**(n+1))/(n**2/2**n),n,oo), limit((n/(n+1))**n,n,oo))
