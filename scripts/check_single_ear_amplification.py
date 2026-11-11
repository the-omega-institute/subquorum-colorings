"""Named-vertex lower certificates for the fixed-one-ear amplification."""
from pathlib import Path
import json


def make(s):
    g={};selected={'d','alpha'};left={'e','alpha'}
    def edge(a,b):
        g.setdefault(a,set()).add(b);g.setdefault(b,set()).add(a)
    for j in range(s):
        y=f'{j}:y';edge('d',y);left.add(y)
        for c in range(2):
            groups={a:[f'{j}:{c}:{a}{i}' for i in range(2)] for a in 'AVWZ'}
            p=f'{j}:{c}:p';u=f'{j}:{c}:u'
            for a in groups['A']:
                for v in groups['V']:edge(a,v)
            for w in groups['W']:
                for z in groups['Z']:edge(w,z)
            for i in range(2):
                edge(groups['A'][i],groups['Z'][i]);edge(groups['V'][i],groups['W'][i])
                edge(p,groups['Z'][i]);edge(u,groups['W'][i]);edge(y,groups['Z'][i])
            selected.update(groups['A']+groups['V']+[p,u])
            left.update(groups['A']+groups['W']+[p])
    for a,b in (('d','e'),('d','alpha'),('alpha','beta'),('beta','e')):edge(a,b)
    assert all((a in left)!=(b in left) for a,row in g.items() for b in row)
    return g,selected


def unformed(g,selected):
    active={v for v in selected if g[v]&selected}
    return {v for v in g if v not in selected and len(g[v]&selected)<2
            and not(g[v]&active)}


def main():
    report=dict(status='PASS',sizes=[1,2,3,8,16,64],models=0,
                deletion_witnesses=0,exact_optimum_source='written local-cap proof',new_Lean=False)
    for s in report['sizes']:
        g,selected=make(s)
        assert len(g)==21*s+4 and len(selected)==12*s+2
        assert not unformed(g,selected)
        for v in selected:
            assert unformed(g,selected-{v});report['deletion_witnesses']+=1
        assert 'e' in unformed(g,selected-{'d'})
        assert 'beta' in unformed(g,selected-{'alpha'})
        seen={'d'};queue=['d']
        for v in queue:
            for u in g[v]-seen:seen.add(u);queue.append(u)
        assert len(seen)==len(g)
        report['models']+=1
    out=Path(__file__).resolve().parents[1]/'output';out.mkdir(exist_ok=True)
    (out/'single-ear-amplification-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
