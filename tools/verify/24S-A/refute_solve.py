from sympy import *
import numpy as np
x,y,z,t=symbols('x y z t',real=True)
R={}
f=y*cos(x*y); g=[diff(f,v).subs({x:1,y:0}) for v in(x,y)]; R['1a']=g  # unit u with u.g=-1
zz=exp(x-y)*sin(x+y); R['1b']=simplify(diff(zz,x,2)+diff(zz,y,2))
# 2a numerics
fn=lambda a,b:a*b**3/(a*a+b*b)
r=np.linspace(1e-6,1e-2,5);th=np.linspace(0,6.28,400)
R['2a_cont_max']=max(abs(fn(rr*np.cos(q),rr*np.sin(q))) for rr in r for q in th)
R['2a_diff_ratio_max']=max(abs(fn(rr*np.cos(q),rr*np.sin(q)))/rr for rr in [1e-3] for q in th)
R['2a_fx,fy']=(fn(1e-9,0)/1e-9,fn(0,1e-9)/1e-9)
# 2b numerics
n=symbols('n',positive=True)
R['2b1_ratio']=limit((1/(n**5+2)**Rational(1,4))/n**Rational(-5,4),n,oo)
R['2b2_ratio']=limit((1/sqrt(n*(n+1)))/(1/n),n,oo)
R['3a_R']=limit(abs((1/(n*4**n))/(1/((n+1)*4**(n+1)))),n,oo)
# 3b
F=2*x**2-3*y**2+x*y-3*x+8*y
print('interior crit',solve([diff(F,x),diff(F,y)],[x,y]))
c=[(0,0),(0,1),(1,1)]
for nm,e,sub,lo,hi in [('x=0',F.subs(x,0),y,0,1),('y=1',F.subs(y,1),x,0,1),('y=x',F.subs(y,x),x,0,1)]:
    cp=solve(diff(e,sub),sub); print(nm,e,cp)
    c+= [(0,p) for p in cp if lo<=p<=hi] if nm=='x=0' else [(p,1) for p in cp if lo<=p<=hi] if nm=='y=1' else [(p,p) for p in cp if lo<=p<=hi]
print({p:F.subs({x:p[0],y:p[1]}) for p in c})
G=np.linspace(0,1,1001);X,Y=np.meshgrid(G,G);m=Y>=X
V=2*X**2-3*Y**2+X*Y-3*X+8*Y;V=np.where(m,V,np.nan);print('grid',np.nanmax(V),np.nanmin(V))
# 4a
R['4a']=solve(2*symbols('a')+exp(t)*symbols('b'),symbols('b'))[0].subs(symbols('a'),exp(t)/2)
# 4b
fl=log(x+1/y);print(solve([diff(fl,x)-1,diff(fl,y)+Rational(16,9)],[x,y],dict=True))
# 5a
Fz=5*z**3+3*x*y*z-x**2*y**2+1
pt={x:1,y:-1,z:0};print('F',Fz.subs(pt),'Fz',diff(Fz,z).subs(pt),'zx',(-diff(Fz,x)/diff(Fz,z)).subs(pt),'zy',(-diff(Fz,y)/diff(Fz,z)).subs(pt))
# 5b
h=x*y*(6-x-y);H=hessian(h,(x,y))
for s in solve([diff(h,x),diff(h,y)],[x,y],dict=True):
    Hs=H.subs(s);print(s,h.subs(s),Hs.det(),Hs[0,0])
print(R)
