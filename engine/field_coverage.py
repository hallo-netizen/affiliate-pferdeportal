import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load():
    inv=json.loads((ROOT/'evidence/K9_RULE_FIELD_INVENTORY.json').read_text())
    pol=json.loads((ROOT/'FIELD_POLICY.json').read_text())
    return inv,pol

def classify(path,policy):
    hits=[]
    for row in policy.get('superseded',[]):
        if re.search(row['pattern'],path):
            hits.append(('SUPERSEDED',None,row['replaced_by'],row['pattern']))
    for pat in policy['descriptive_patterns']:
        if re.search(pat,path): hits.append(('DESCRIPTIVE',None,None,pat))
    for pat in policy['target_patterns']:
        if re.search(pat,path): hits.append(('TARGET','writer_guidance',None,pat))
    for row in policy['hard_bindings']:
        if re.search(row['pattern'],path): hits.append(('HARD',row['owner'],row['rule_id'],row['pattern']))
    # Priority: SUPERSEDED > TARGET > HARD > DESCRIPTIVE; ambiguity within same priority is forbidden.
    for cls in ('SUPERSEDED','TARGET','HARD','DESCRIPTIVE'):
        chosen=[h for h in hits if h[0]==cls]
        if chosen:
            uniq={(a,b,c) for a,b,c,_ in chosen}
            if len(uniq)!=1: return {'path':path,'status':'AMBIGUOUS','hits':chosen}
            a,b,c=next(iter(uniq)); return {'path':path,'status':'OK','classification':a,'owner':b,'rule_id':c}
    return {'path':path,'status':'UNCLASSIFIED','hits':[]}

def audit():
    inv,pol=load(); rows=[]
    for section,paths in inv.items():
        prefix='table_rule.' if section=='table_rule' else ''
        for p in paths: rows.append(classify(prefix+p,pol))
    bad=[r for r in rows if r['status']!='OK']
    counts={k:sum(r.get('classification')==k for r in rows) for k in ('HARD','TARGET','DESCRIPTIVE','SUPERSEDED')}
    return {'status':'PASS' if not bad else 'BLOCKED','total':len(rows),**{k.lower():v for k,v in counts.items()},'bad':bad,'rows':rows}
