import json,sympy as sp
x,y=sp.symbols('x y')
R=json.load(open('22A-B/regions.json'));C=json.load(open('22A-B/contours.json'))
for r in R:
    for vx,vy in r.get('vertices',[]):
        print(r['id'],(round(vx,4),round(vy,4)),'y-x',round(vy-vx,6),'y+2x',round(vy+2*vx,6))
for c in C:
    F=sp.sympify(c['f'].replace('^','**'))
    for p in c['critical_points']:
        px=float(sp.sympify(str(p['x']).replace('^','**'))); py=float(sp.sympify(str(p['y'])))
        g=[float(sp.diff(F,s).subs({x:px,y:py})) for s in (x,y)]
        print(c['id'],(round(px,4),round(py,4)),'f=',float(F.subs({x:px,y:py})),'claimed',p['f'],p['role'],'grad',[round(v,6) for v in g],'on constraint' if c['constraint'] and abs(float(sp.sympify(c['constraint'].split('=')[0].replace('^','**')).subs({x:px,y:py}))-1)<1e-9 else '')
