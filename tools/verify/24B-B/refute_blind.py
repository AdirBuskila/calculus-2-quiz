import sympy as sp, numpy as np
x,y,n=sp.symbols('x y n',real=True)
# Q1
f=x**3*y/(x**2+y**2)
print('Q1a fx(1,0)',sp.diff(f,x).subs({x:1,y:0}),'fy(1,0)',sp.simplify(sp.diff(f,y).subs({x:1,y:0})))
# at origin: f(h,0)=0, f(0,k)=0 -> 0,0
# diff: eps = f/ r ; along y=x: x^4/(2x^2)/(sqrt2|x|) ->0 ; |f|<=|x|^3|y|/r^2 <= r^2/... 
r,t=sp.symbols('r t',positive=True)
print('Q1c |f|/r in polar:',sp.simplify((f.subs({x:r*sp.cos(t),y:r*sp.sin(t)})/r)))  # r^3 cos^3 sin /r^... 
# Q2a
print('Q2a limit', sp.limit((n**2+3*sp.log(n))/((n+1)*(n+2)),n,sp.oo))
# Q2b
print('Q2b abs sum numeric', sum((1+1/np.sqrt(k))/k**3 for k in range(1,100000)))
# Q3
F=x**2-2*x*(y+1)+3
g=[sp.diff(F,v) for v in (x,y)]
print('grad',g,'at(2,-1)',[e.subs({x:2,y:-1}) for e in g])
gr=np.array([float(e.subs({x:2,y:-1})) for e in g]);print('Du',gr@np.array([-3,4])/5)
print('crit',sp.solve(g,[x,y]),'H',sp.hessian(F,(x,y)),sp.hessian(F,(x,y)).det())
fn=sp.lambdify((x,y),F)
# grid on D: -2<=y<=x<=1
best=[]
N=2001
xs=np.linspace(-2,1,N)
mn=1e9;mx=-1e9
for xv in xs:
    ys=np.linspace(-2,xv,N) if xv>=-2 else []
    if len(ys)==0: continue
    v=fn(xv,ys)
    i=v.argmin();j=v.argmax()
    if v[i]<mn: mn=v[i];pmn=(xv,ys[i])
    if v[j]>mx: mx=v[j];pmx=(xv,ys[j])
print('Q3d grid min',mn,pmn,'max',mx,pmx)
# Q4a
X,Y=sp.symbols('X Y')
u=sp.cos(X-3*Y)
ux=sp.diff(u,X).subs({X:sp.pi,Y:-sp.pi});uy=sp.diff(u,Y).subs({X:sp.pi,Y:-sp.pi});u0=u.subs({X:sp.pi,Y:-sp.pi})
v0,vx,vy=2,5,4
zu=2*v0;zv=2*u0+6*v0
print('u0',u0,'ux',ux,'uy',uy,'zx',zu*ux+zv*vx,'zy',zu*uy+zv*vy)
# Q4b
a=sp.symbols('a')
# R=1/2 ; endpoints
print('Q4b: R=1/2, x=3/2 term 1/sqrt(n+4) diverges; x=1/2 alt converges cond')
# Q5
h=sp.log(6*x**2+5*x+1)
print(sp.factor(6*x**2+5*x+1), sp.series(h,x,0,7))
print('f5(0)',sp.diff(h,x,5).subs(x,0))
c=lambda k: sp.Rational((-1)**(k+1),k)*(2**k+3**k)*(-1)**0
# ln(1+2x)+ln(1+3x) = sum (-1)^(k+1)(2^k+3^k)x^k/k ; domain -1/3<x<=1/3
print([sp.series(sp.log(1+2*x)+sp.log(1+3*x),x,0,7).removeO().coeff(x,k) for k in range(1,7)])
print('f5 =', sp.Rational(1,5)*(2**5+3**5)*120)
