# Independent blind solve of 23A-A (refuter).
import sympy as sp, numpy as np
x,y,z,r,th,n,u,v=sp.symbols('x y z r th n u v',real=True)
# 1a
I1=sp.integrate(sp.integrate(th*r,(r,1,2)),(th,sp.pi/4,sp.pi/3)); print('1a',sp.simplify(I1), sp.Rational(7,192)*sp.pi**2, float(I1))
gx,gy=np.meshgrid(np.linspace(0,2,4001),np.linspace(0,2,4001)); dA=(2/4000)**2
m=(gx**2+gy**2>=1)&(gx**2+gy**2<=4)&(gy>=gx)&(gy<=np.sqrt(3)*gx)
print('1a numeric',(np.arctan2(gy,gx)*m).sum()*dA)
# 1b
f=sp.log(x**2+y**2+z**2); print('1b grad',[sp.simplify(sp.diff(f,w).subs({x:1,y:2,z:1})) for w in (x,y,z)])
# 2a numerics
print('2a1 monotone decreasing from n=2:',all(np.sin(np.pi/k)>np.sin(np.pi/(k+1)) for k in range(2,10000)),' abs terms ~ pi/n limit',sp.limit(sp.sin(sp.pi/n)*n,n,sp.oo))
print('2a2 abs limit comparison n^(4/3):',sp.limit(sp.log(1+1/(n*n**sp.Rational(1,3)))*n**sp.Rational(4,3),n,sp.oo))
# 3a
print('3a ratio',sp.limit(sp.Abs(3*(2*n+1)**2/((2*n+3)**2*sp.sqrt(5))),n,sp.oo),' R=',sp.sqrt(5)/3)
# 3b symbolic chain rule
F=sp.Function('f'); U=1/y-1/x; V=x*y*sp.exp(-z**2/2); g=F(U,V)
expr=x**2*sp.diff(g,x)+y**2*sp.diff(g,y)+(x+y)/z*sp.diff(g,z)
print('3b',sp.simplify(expr.doit()))
# 4a: jacobian in uv: u=x^2 y, v=y-x
Uf=x**2*y; Vf=y-x
J=sp.Matrix([[sp.diff(Uf,x),sp.diff(Uf,y)],[sp.diff(Vf,x),sp.diff(Vf,y)]]).det(); print('4a J',sp.factor(J), ' integrand/J', sp.simplify((x**2+2*x*y)/J))
# numeric integral over D in first quadrant
N=6000
gx,gy=np.meshgrid(np.linspace(0.0005,6,N),np.linspace(0.0005,6,N)); dA=(6/N)**2
m=(gy>=1/gx**2)&(gy<=4/gx**2)&(gy<=gx+1)&(gy>=gx-1)
print('4a numeric',((gx**2+2*gx*gy)*m).sum()*dA,' area',m.sum()*dA,' (exact 6)')
# 4b
f4=1-x**2-y**2
th_=np.linspace(0,2*np.pi,2000001); px=1+np.cos(th_); py=1+np.sin(th_); fb=1-px**2-py**2
print('4b boundary max/min',fb.max(),fb.min(),' exact',2*np.sqrt(2)-2,-2-2*np.sqrt(2))
print('4b interior crit (0,0) in disk?',(0-1)**2+(0-1)**2<=1)
gx,gy=np.meshgrid(np.linspace(-0.1,2.1,3001),np.linspace(-0.1,2.1,3001)); ins=(gx-1)**2+(gy-1)**2<=1
Fg=1-gx**2-gy**2; print('4b grid',Fg[ins].max(),Fg[ins].min())
a=th_[fb.argmax()]; print('4b argmax pt',px[fb.argmax()],py[fb.argmax()],1-1/np.sqrt(2))
# 5a
f5=(x+y)**2-4*y**2-48*y
cp=sp.solve([sp.diff(f5,x),sp.diff(f5,y)],[x,y],dict=True); H=sp.hessian(f5,(x,y)); print('5a',cp,[H.subs(c).det() for c in cp],[f5.subs(c) for c in cp])
# 5b
f6=1/(x**2+x-6); s=sp.series(f6,x,0,12).removeO()
print('5b c10',s.coeff(x,10),' f10(0)',sp.diff(f6,x,10).subs(x,0), sp.factorial(10)*sp.Rational(1,5)*(-sp.Rational(1,2**11)-sp.Rational(1,3**11)))
print('5b closed coeff general n=0..3',[sp.Rational(1,5)*(-sp.Rational(1,2**(k+1))-sp.Rational((-1)**k,3**(k+1))) for k in range(4)], [s.coeff(x,k) for k in range(4)])
