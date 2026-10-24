import sympy as sp, json, re
x,y=sp.symbols('x y',real=True)
f=(x**2-2*y**2)*sp.exp(x-y)
e=sp.exp(x-y)
print(sp.simplify(sp.diff(f,x,2)/e-(x**2+4*x+2-2*y**2)), sp.simplify(sp.diff(f,y,2)/e-(x**2-2*y**2+8*y-4)), sp.simplify(sp.diff(f,x,y)/e-(2*y**2-x**2-2*x-4*y)))
print(sp.simplify(sp.diff(f,x)/e-(x**2+2*x-2*y**2)),sp.simplify(sp.diff(f,y)/e-(-x**2-4*y+2*y**2)))
num=(x**3+y**3)/(2*x**2+y**2)-x/2-y
print(sp.simplify(num+x*y*(4*x+y)/(2*(2*x**2+y**2))))
print(sp.simplify((num/sp.sqrt(x**2+y**2)).subs(y,x).subs(x,sp.Symbol('s',positive=True))), -5/(6*2**.5))
d=json.load(open('../../raw/23A-C.json',encoding='utf8'))
s=json.dumps(d,ensure_ascii=False)
print('הפתרון הרשמי' in s, re.findall(r'(אפשרות|תשובה|סעיף|חלופה)\s*(א|ב|ג|ד|[a-d])\b',s), re.findall(r'(?:אפשרות|חלופה)\s*\S+',s))
for q in d['questions']:
    print(q['num'],q['part'],sum(r['points'] for r in q['rubric']),q['points'],q['solutionSource'],q['official'])
    for st in q['steps']:
        if st['type']=='choice':
            ids=[o['id'] for o in st['options']]; print('  choice',st['correctId'] in ids,len(ids))
