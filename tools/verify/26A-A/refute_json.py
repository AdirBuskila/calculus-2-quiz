import json,sympy as sp,numpy as np
x,y=sp.symbols('x y');t=sp.symbols('t',real=True)
# 2b with correct linearisation fx=1/2, fy=1
f=(x**3+y**3)/(2*x**2+y**2)
fx=sp.limit(f.subs(y,0)/x,x,0);fy=sp.limit(f.subs(x,0)/y,y,0);print('fx,fy',fx,fy)
print('2b diff quotient along y=x',sp.simplify(((f-(fx*x+fy*y))/sp.sqrt(x**2+y**2)).subs(y,x).subs(x,t)),sp.N(-5/(6*sp.sqrt(2))))
# 5b f20
X=sp.symbols('X');fr=(16-5*X)/(X**2-5*X+6)
c=sp.series(fr,X,0,22).removeO().coeff(X,20);print('a20 diff',sp.simplify(c-(sp.Rational(3,2**20)-sp.Rational(1,3**21))),'a1',sp.series(fr,X,0,3).removeO().coeff(X,1))
print('numeric 5b series radius: coeff ratio a21/a20',float((sp.Rational(3,2**21)-sp.Rational(1,3**22))/(sp.Rational(3,2**20)-sp.Rational(1,3**21))))
R=json.load(open('26A-A/regions.json'));C=json.load(open('26A-A/contours.json'))
for r in R:
    for vx,vy in r['vertices']:
        vx=float(sp.sympify(vx));vy=float(sp.sympify(vy))
        ok=[]
        for ineq in r['boundary_curves']:
            l,rh=ineq.split('=');ok.append(abs(float(sp.sympify(l.replace('^','**')).subs({x:vx,y:vy}))-float(sp.sympify(rh.replace('^','**')).subs({x:vx,y:vy})))<1e-9 if 'x' in l or 'y' in l else None)
        print(r['id'],(round(vx,4),round(vy,4)),'on >=2 boundary curves:',sum(1 for o in ok if o)>=2)
for c in C:
    F=sp.sympify(c['f'].replace('^','**'))
    for p in c['critical_points']:
        px=float(sp.sympify(str(p['x']))); py=float(sp.sympify(str(p['y'])))
        print(c['id'],(round(px,4),round(py,4)),'f=',float(F.subs({x:px,y:py})),'claimed',p['f'],p['role'])
