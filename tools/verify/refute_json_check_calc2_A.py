# Refuter: check regions.json / contours.json of 22A-A, 23A-A, 24A-A against independent math.
import json, re, sympy as sp, numpy as np, os
x,y=sp.symbols('x y')
here=os.path.dirname(os.path.abspath(__file__))
P=lambda s: sp.sympify(s.replace('^','**'),locals={'sqrt':sp.sqrt,'x':x,'y':y,'e':sp.E})
def npify(s):
    s=s.replace('^','**').replace('atan','np.arctan').replace('exp','np.exp').replace('sqrt','np.sqrt')
    s=re.sub(r'(?<![A-Za-z.])x(?![A-Za-z])','gx',s); s=re.sub(r'(?<![A-Za-z.])y(?![A-Za-z])','gy',s)
    return s
for c in ['22A-A','23A-A','24A-A']:
    for it in json.load(open(f'{here}/{c}/contours.json',encoding='utf8')):
        f=P(it['f']); H=sp.hessian(f,(x,y))
        print(c,it['id'],it['kind'])
        for cp in it['critical_points']:
            X,Y=P(str(cp['x'])),P(str(cp['y'])); val=float(f.subs({x:X,y:Y}))
            ok=abs(val-float(cp['f']))<1e-9
            g=[float(sp.diff(f,v).subs({x:X,y:Y})) for v in (x,y)]
            D=float(H.det().subs({x:X,y:Y})); fxx=float(H[0,0].subs({x:X,y:Y}))
            cls='saddle' if D<0 else (('local min' if fxx>0 else 'local max') if D>0 else 'degenerate')
            print('  ',(X,Y),'f ok' if ok else f'F MISMATCH {val} vs {cp["f"]}','grad',[round(t,6) for t in g],'hess-class',cls,'| claimed:',cp['role'])
for c in ['22A-A','23A-A']:
    for it in json.load(open(f'{here}/{c}/regions.json',encoding='utf8')):
        print(c,it['id'],it['description'])
        N=6000
        if c=='22A-A': gx,gy=np.meshgrid(np.linspace(-12,5,N),np.linspace(0.0,8,N)); dA=17/N*8/N
        else: gx,gy=np.meshgrid(np.linspace(0.0005,6,N),np.linspace(0.0005,6,N)); dA=(6/N)**2
        m=np.ones_like(gx,bool)
        for ineq in it['inequalities']: m&=eval(npify(ineq))
        w=eval(npify(it['integrand']))
        val=(w*m).sum()*dA
        exact=float(sp.N(P(it['value'])))
        print('   numeric',val,'claimed',it['value'],exact,'  rel err',abs(val-exact)/abs(exact))
