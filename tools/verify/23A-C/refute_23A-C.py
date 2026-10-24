import sympy as sp, numpy as np
x,y,z,t,r,th,n=sp.symbols('x y z t r theta n',real=True)
# 1a
A=sp.integrate(sp.integrate(r,(r,2*sp.cos(th),4*sp.cos(th))),(th,-sp.pi/2,sp.pi/2)); print('1a',sp.simplify(A))
# 1b
f=x**2*y*sp.sqrt(z); g=sp.Matrix([sp.diff(f,v) for v in (x,y,z)]).subs({x:2,y:1,z:1}); u=sp.Matrix([1,2,2])/3
D=g.dot(u); print('1b',g.T,D,g.norm(),sp.nsimplify(g.norm()/D),D/g.norm())
# 2a
print('2a ratios',float(2/3),float(sp.atan(1)))
print(' arctan((n+2)/(n+3)) n=1e6:',np.arctan((1e6+2)/(1e6+3)))
# 2b
f2=lambda a,b:(a**3+b**3)/(2*a**2+b**2)
for s in (1e-3,1e-5):
    print('2b',(f2(s,s)-2*s)/(s*2**.5), (f2(s,0)-s)/s,(f2(0,s)-s)/s)
a,b=sp.symbols('a b'); print(sp.limit(((a**3+a**3)/(3*a**2)-2*a)/(sp.sqrt(2)*a),a,0,'+'))
# 3a
for xv in (3,-3,2.9):
    print('3a',xv,[xv**k/(2**k+3**k) for k in (50,51,200)])
# 3b
g_=sp.Function('g'); zz=y*g_(x**2-y**2)
print('3b',sp.simplify(sp.diff(zz,x)/x+sp.diff(zz,y)/y-zz/y**2))
# 4a: numeric area equality, test f=1 and f=x*y^2
import scipy.integrate as si
for fn in (lambda X,Y:1.0, lambda X,Y:X*Y**2+Y):
    I1=si.dblquad(lambda Y,X:fn(X,Y),-4,0,0,lambda X:np.sqrt(X+4))[0]+si.dblquad(lambda Y,X:fn(X,Y),0,2,0,lambda X:2-X)[0]
    I2=si.dblquad(lambda X,Y:fn(X,Y),0,2,lambda Y:Y**2-4,lambda Y:2-Y)[0]
    print('4a',I1,I2)
# 4b
F=lambda X,Y:X**2+Y**2+4*X*Y
best=[]
for R in np.linspace(0,1,801):
    for T in np.linspace(0,np.pi/3,801):
        best.append((F(R*np.cos(T),R*np.sin(T)),R,T))
print('4b max',max(best),'min',min(best), 'xy max pt',np.cos(np.pi/4))
print('4b crit',sp.solve([2*x+4*y,2*y+4*x],[x,y]))
# 5a
f5=(x**2-2*y**2)*sp.exp(x-y)
sol=sp.solve([sp.diff(f5,x),sp.diff(f5,y)],[x,y],dict=True); print('5a',sol)
H=sp.hessian(f5,(x,y))
for s in sol:
    h=H.subs(s); print(s,sp.simplify(h),sp.simplify(h.det()),sp.simplify(h[0,0]),sp.N(f5.subs(s)))
# 5b
f6=1/(x**2+x-2)
print('5b',sp.series(f6,x,0,6)); c=-sp.Rational(1,3)-sp.Rational(1,6)*(-sp.Rational(1,2))**n
print([c.subs(n,k) for k in range(5)])
print('f10',sp.factorial(10)*c.subs(n,10), sp.diff(f6,x,10).subs(x,0))
print(sp.apart(f6))
