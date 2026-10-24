import sympy as sp, numpy as np
x,y,k,n,t=sp.symbols('x y k n t',real=True)
f=x**2*y**2/(x**6+y**3)
print('Q1a y=kx',sp.limit(f.subs(y,k*x),x,0,'+'),' y=x^2',sp.limit(f.subs(y,x**2),x,0,'+'), ' y=x (x->0+)',sp.limit(f.subs(y,x),x,0,'+'))
print('  y=-x^2+x^4 ',sp.limit(f.subs(y,-x**2+x**4),x,0,'+'))
# Q1b f=x+xy, direction (a,b) unit: fx=1+y=0, fy=x=1 at (1,-1) -> grad (0,1)
a,b=sp.symbols('a b')
print('Q1b',sp.solve([a*0+b*1-1/sp.sqrt(2),a**2+b**2-1],[a,b]))
# Q2a
print('Q2a1: 1/((n+1)ln(n+1)) integral diverges; alt -> conditional')
print('Q2a2: sum ((-1)^n+n)/3^n abs conv (ratio 1/3)')
print('Q2a2 sum', sp.summation(((-1)**n+n)/sp.Integer(3)**n,(n,1,sp.oo)))
# Q2b
g=(x**3+y**3)/(2*x**2+y**2)
print('Q2b fx(0,0)=lim h/(2)=',sp.limit(g.subs(y,0)/x,x,0),' fy(0,0)=',sp.limit(g.subs(x,0)/y,y,0))
# differentiability: eps=(f - x*fx - y*fy)/r, fx=1/2, fy=1
r=sp.symbols('r',positive=True);th=sp.symbols('th')
eps=sp.simplify(((g-x/2-y).subs({x:r*sp.cos(th),y:r*sp.sin(th)}))/r)
print(' eps polar',eps, ' th=0:',sp.simplify(eps.subs(th,0)),' th=pi: ',sp.simplify(eps.subs(th,sp.pi)))
# along dy=k dx, dx->0+ and dx->0-
dx=sp.symbols('dx',real=True)
e=((g-x/2-y)/sp.sqrt(x**2+y**2)).subs(y,k*x)
print(' dx->0+',sp.simplify(sp.limit(e,x,0,'+')),' dx->0-',sp.simplify(sp.limit(e,x,0,'-')))
# Q3a
nn=sp.symbols('n',positive=True)
term=1/(sp.cbrt(nn+1)*sp.sqrt(nn**2+1))
print('Q3a ratio R:',sp.limit(term.subs(nn,nn+1)/term,nn,sp.oo),' n^(4/3)*term->',sp.limit(term*nn**sp.Rational(4,3),nn,sp.oo))
print(' sum at x=-4 (x+5=1) numeric:',sum(1/((j+1)**(1/3)*(j*j+1)**0.5) for j in range(1,2000000)))
print(' sum at x=-6 abs same -> conv; domain [-6,-4]')
# Q3b
X,Y=sp.symbols('X Y',positive=True)
G=sp.Function('g')
z=Y/(3*X)+G(X*Y)
expr=X**2*sp.diff(z,X)-X*Y*sp.diff(z,Y)+2*Y/3
print('Q3b',sp.simplify(sp.expand(expr.doit())))
# Q4a
print('Q4a',sp.summation(5/sp.Integer(3)**n-4/((n+3)*(n+4)),(n,1,sp.oo)), ' split:',sp.summation(5/sp.Integer(3)**n,(n,1,sp.oo)),sp.summation(4/((n+3)*(n+4)),(n,1,sp.oo)))
# Q4b
F=2*x**4+y**4-x**2-2*y**2
fn=sp.lambdify((x,y),F)
th_=np.linspace(0,2*np.pi,2000001)
xs=np.linspace(-1.5,1.5,3001)
XX,YY=np.meshgrid(xs,xs);m=XX**2+YY**2<=2
V=np.where(m,fn(XX,YY),np.nan)
i=np.nanargmin(V);j=np.nanargmax(V)
print('Q4b grid min',np.nanmin(V),XX.flat[i],YY.flat[i],' max',np.nanmax(V),XX.flat[j],YY.flat[j])
print(' crit',sp.solve([sp.diff(F,x),sp.diff(F,y)],[x,y]))
print(' boundary: x^2=s, y^2=2-s:',sp.simplify(F.subs({x:sp.sqrt(sp.Symbol('s')),y:sp.sqrt(2-sp.Symbol('s'))})))
s=sp.Symbol('s')
Fb=sp.expand(F.subs({x**4:s**2}).subs({x:sp.sqrt(s),y:sp.sqrt(2-s)}))
print(' Fb(s)',Fb, sp.solve(sp.diff(Fb,s),s), [Fb.subs(s,v) for v in (0,2,sp.Rational(3,4)*1)])
# Q5a
h=(3-x)*(3-y)*(x+y-3)
sol=sp.solve([sp.diff(h,x),sp.diff(h,y)],[x,y],dict=True)
H=sp.hessian(h,(x,y))
for p in sol: print('Q5a',p,'f=',h.subs(p),'det',H.det().subs(p),'fxx',H[0,0].subs(p))
# Q5b
p=sp.series(x/(25+x**2),x,0,8);print(p, sp.diff(x/(25+x**2),x,5).subs(x,0))
