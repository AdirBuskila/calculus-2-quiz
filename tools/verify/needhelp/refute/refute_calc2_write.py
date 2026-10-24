import json,re
R='tools/raw/'
A={
'limits_diff':{
'C01-Q1':1,'C01-Q2':0,'C01-Q3':'d','C01-Q4':1.2,'C01-Q5':'b','C01-Q6':'c',
'C02-Q1':'c','C02-Q2':0.5,'C02-Q3':0.4,'C02-Q4':'a','C02-Q5':1/3,'C02-Q6':0.5,
'C03-Q1':0,'C03-Q2':'c','C03-Q3':3,'C03-Q4':1,'C03-Q5':'d','C03-Q6':-1,
'C04-Q1':2,'C04-Q2':'a','C04-Q3':0.385,'C04-Q4':1,'C04-Q5':'c','C04-Q6':0,
'C05-Q1':0,'C05-Q2':1,'C05-Q3':'b','C05-Q4':'a','C05-Q5':0.5,'C05-Q6':1,
'C06-Q1':3,'C06-Q2':1,'C06-Q3':0,'C06-Q4':[3,0,1,2],'C06-Q5':'d','C06-Q6':'a',
'C07-Q1':-0.3536,'C07-Q2':'b','C07-Q3':1,'C07-Q4':[4,0,1,2,3],'C07-Q5':1,'C07-Q6':'c',
'C08-Q1':'a','C08-Q2':0.5,'C08-Q3':'c','C08-Q4':0.3536,'C08-Q5':'c','C08-Q6':'b'},
'chain_rule':{
'C01-Q1':'a','C01-Q2':'a','C01-Q3':12,'C01-Q4':'a','C01-Q5':'a',
'C02-Q1':'a','C02-Q2':24,'C02-Q3':'a','C02-Q4':3,'C02-Q5':-6,'C02-Q6':'a',
'C03-Q1':'a','C03-Q2':'a','C03-Q3':12,'C03-Q4':1,'C03-Q5':'a','C03-Q6':2.33,
'C04-Q1':[3,0,1,2],'C04-Q2':'a','C04-Q3':1,'C04-Q4':3,
'C05-Q1':'a','C05-Q2':36,'C05-Q3':'a','C05-Q4':1,'C05-Q5':'a',
'C06-Q1':'a','C06-Q2':'a','C06-Q3':7,'C06-Q4':2,'C06-Q5':'a','C06-Q6':'a',
'C07-Q1':7,'C07-Q2':-1,'C07-Q3':-4,'C07-Q4':'a','C07-Q5':1},
'series':{
'C01-Q1':'c','C01-Q2':2.5,'C01-Q3':1/6,'C01-Q4':'d','C01-Q5':'a','C01-Q6':2,
'C02-Q1':'d','C02-Q2':2,'C02-Q3':'b','C02-Q4':'c','C02-Q5':3,'C02-Q6':'c',
'C03-Q1':0.5,'C03-Q2':'a','C03-Q3':'d','C03-Q4':'d','C03-Q5':'c','C03-Q6':[3,0,1,2],
'C04-Q1':'c','C04-Q2':'c','C04-Q3':'b','C04-Q4':'c','C04-Q5':9,'C04-Q6':2,
'C05-Q1':3,'C05-Q2':'c','C05-Q3':1.25,'C05-Q4':'c','C05-Q5':'c','C05-Q6':'d',
'C06-Q1':'c','C06-Q2':'b','C06-Q3':'d','C06-Q4':'d','C06-Q5':'d','C06-Q6':3,
'C07-Q1':'d','C07-Q2':20,'C07-Q3':-120,'C07-Q4':'c','C07-Q5':744,'C07-Q6':'c'}}
for c,a in A.items():
    d=json.load(open(R+f'_blind_course_{c}.json',encoding='utf8'))
    out={}
    for L in d['levels']:
        for q in L['questions']:
            if 'bankId' in q: continue
            v=a[q['id']]
            if isinstance(v,list):
                lines=(q.get('step') or q)['lines']; v=[lines[i] for i in v]
            out[q['id']]={'answer':v}
    json.dump({'answers':out},open(R+f'_verify_course_{c}.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
