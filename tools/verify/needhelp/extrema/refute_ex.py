from sympy import *
import numpy as np
x,y=symbols('x y')
def crit(f): return solve([diff(f,x),diff(f,y)],[x,y],dict=True)
print(crit(x**2-x*y+y**2-3*x), len(crit(x**3-3*x+y**3-3*y)), len(crit(x*y*(4-x-y))))
f=x**3+8*y**3-6*x*y+1
for c in crit(f):
  if all(v.is_real for v in c.values()): H=hessian(f,(x,y)).subs(c); print(c,H.det())
print(crit(2*x**2-3*y**2+x*y-3*x+8*y))
f=x**2+x*y+y**2-6*x
X,Y=np.meshgrid(np.linspace(0,4,2001),np.linspace(0,4,2001));m=X+Y<=4
V=(X**2+X*Y+Y**2-6*X)[m];print(V.min(),V.max())
t=np.linspace(0,2*np.pi,200001);print((np.cos(t)**4+np.sin(t)**4).min())
r=np.linspace(0,1,1001);T=np.linspace(0,2*np.pi,2001);R,TT=np.meshgrid(r,T)
print((R**2*(np.cos(TT)**2+3*np.sin(TT)**2)).max())
