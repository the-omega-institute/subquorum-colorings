"""Named-vertex certificates for the partial-ear obstruction; no project imports."""
from pathlib import Path
import json


def model(q,ear):
    g={};left={'y'};blocks=[]
    def add(v):g.setdefault(v,set())
    def edge(a,b):add(a);add(b);g[a].add(b);g[b].add(a)
    add('y')
    for c in range(q):
        group={s:[f'{c}:{s}{i}' for i in range(2)] for s in 'AVWZ'}
        p=f'{c}:p';u=f'{c}:u';group.update(p=p,u=u)
        for a in group['A']:
            for v in group['V']:edge(a,v)
        for w in group['W']:
            for z in group['Z']:edge(w,z)
        for i in range(2):
            edge(group['A'][i],group['Z'][i]);edge(group['V'][i],group['W'][i])
            edge(p,group['Z'][i]);edge(u,group['W'][i]);edge('y',group['Z'][i])
        left.update(group['A']+group['W']+[p]);blocks.append(group)
    if ear:
        for a,b in (('d','e'),('d','y'),('d','alpha'),('alpha','beta'),('beta','e')):edge(a,b)
        left.update(('e','alpha'))
    assert all((a in left)!=(b in left) for a,row in g.items() for b in row)
    return g,left,blocks


def unformed(g,s):
    active={v for v in s if g[v]&s}
    return {v for v in g if v not in s and len(g[v]&s)<2 and not(g[v]&active)}


def verify(g,s,report):
    assert not unformed(g,s)
    for v in s:
        assert unformed(g,s-{v})
        report['single_deletions']+=1


def main():
    report=dict(status='PASS',sizes=[1,2,3,4,8,16,32,128],models=0,
                single_deletions=0,explicit_witnesses=0,new_Lean=False)
    for q in report['sizes']:
        f,left,blocks=model(q,False)
        assert len(f)==10*q+1 and len(left)==5*q+1
        verify(f,left,report)
        s=set(blocks[0]['V']+blocks[0]['Z']+[blocks[0]['u']])
        for b in blocks[1:]:s.update(b['A']+b['V']+[b['p'],b['u']])
        assert len(s)==6*q-1;verify(f,s,report)
        g,_,blocks=model(q,True)
        s={'d','alpha'}
        for b in blocks:s.update(b['A']+b['V']+[b['p'],b['u']])
        assert len(g)==10*q+5 and len(s)==6*q+2
        verify(g,s,report)
        for b in blocks:
            for i in range(2):
                assert b['Z'][i] in unformed(g,s-{b['A'][i]})
                assert b['W'][i] in unformed(g,s-{b['V'][i]})
                report['explicit_witnesses']+=2
            for v in (b['p'],b['u']):
                assert v in unformed(g,s-{v});report['explicit_witnesses']+=1
        assert 'e' in unformed(g,s-{'d'}) and 'beta' in unformed(g,s-{'alpha'})
        report['explicit_witnesses']+=2
        report['models']+=2
    out=Path(__file__).resolve().parents[1]/'output';out.mkdir(exist_ok=True)
    (out/'bipartite-ear-certificate-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
