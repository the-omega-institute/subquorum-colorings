#!/usr/bin/env python3
"""Physical checks of zero-budget replacements, path events and strict bound."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from itertools import product
import hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'develop'),str(ROOT/'scripts')]
from subcubic_zero_budget_repair import zero_budget_certificate,components
from subcubic_phase_pairing import pairing_data,expectation
from subcubic_phase_slack import owner_slack,full_certificate
from subcubic_partial_template import layers
from check_unrestricted_subcubic_gap import all_minimal,matchings,partial_model,valid_graph
from check_subcubic_intrinsic_obstruction import diss,exact,private_optimum
from check_odd_cycle_compensation import profile_model,residual_optimum
if not __debug__:raise RuntimeError('Assertions required')
COUNTS=Counter();FEATURES=Counter();DIGEST=hashlib.sha256()


def check_selection(g,colour,S,beta):
    D,data=full_certificate(g,S,colour,beta);w=data['baseline']['witnesses'];m=data['baseline']['template']
    assert diss(g,D) and len(D)<=beta
    if len(g):assert 81*(len(S)-beta)<8*len(g) and len(S)-beta<=(8*len(g)-1)//81
    else:assert not S and beta==0
    if data['slack']['sigma']==0:
        inner,repair=zero_budget_certificate(m)
        retained=(w['R']-w['I0'])|{ell for c,ell,x in w['triples']}
        candidate=inner|retained
        assert diss(g,candidate) and len(candidate)<=beta
        counts=data['baseline']['counts']
        if not (counts['e'] or counts['q'] or counts['b3'] or repair['ordinary_helpers'] or repair['core_paths']):
            H=m['I']|m['C']|m['X'];outside=set(range(len(g)))-H
            assert all(g[v]<=H for v in H)
            independent=max(({v for v in outside if colour[v]==bit} for bit in (0,1)),key=len)
            assert len(independent)*2>=len(outside) and diss(g,inner|independent)
            COUNTS['closed_extraction_controls']+=1
        COUNTS['zero_budget_selections']+=1
    COUNTS['minimal_selections']+=1
    FEATURES['positive_gap']+=len(S)>beta
    DIGEST.update(json.dumps([len(g),sorted(S),beta,str(data['slack']['sigma'])],sort_keys=True).encode()+b'\n')


def check_graph(g,colour):
    valid_graph(g,colour);beta,selections=all_minimal(g);assert beta==exact(g)[0]
    for S in selections:check_selection(g,colour,S,beta)
    COUNTS['graphs']+=1;COUNTS['literal_subsets']+=1<<len(g)


def check_template(m,optimize=False):
    valid_graph(m['g'],m['graph_colour'])
    sigma=owner_slack(m,pairing_data(m))['sigma'];COUNTS['templates']+=1
    if sigma==0:
        D,data=zero_budget_certificate(m);assert diss(m['g'],D)
        assert all(diss(m['g'],a) for a in data['alternatives'])
        bo,t=data['ordinary_helpers'],data['core_paths'];b=len(m['I'])
        assert 20*len(D)>=52*b+3*bo+t
        FEATURES['ordinary_replacement']+=bo>0;FEATURES['path_credit']+=t>0
        FEATURES['both_resources']+=bo>0 and t>0
        FEATURES['zero_without_either_resource']+=b>0 and bo==t==0
        rem=data['remainder'];total=Fraction(0)
        for bits in product((0,1),repeat=len(rem['components'])):
            A={rem['owner'][x] for x in rem['X'] if rem['colour'][x]!=bits[rem['group'][x]]}
            beta=residual_optimum(m['g'],A)
            assert Fraction(beta)-Fraction(2*len(A),3)>=expectation(data['terms'],dict(enumerate(bits)))
            total+=Fraction(beta)-Fraction(2*len(A),3)
            for row in data['events']:
                if all(bits[j]==bit for j,bit in row['requirements'].items()):
                    K=set(row['prefix']);assert K<=A
                    assert all((m['g'][v]&A)<=K for v in K)
                    COUNTS['endpoint_event_witnesses']+=1
            COUNTS['phase_assignments']+=1
        assert total/2**len(rem['components'])>=data['initial']
        for k,value in enumerate(data['steps']):
            values=[expectation(data['terms'],dict(enumerate(bits)))
                    for bits in product((0,1),repeat=len(rem['components']))
                    if all(bits[j]==data['phases'][j] for j in range(k))]
            assert sum(values)/len(values)==value
            COUNTS['conditional_expectation_controls']+=1
        if bo==t==0:
            assert all(len(m['g'][v]&m['C'])==2 for v in m['C'])
            assert all(v in m['q'] for v in m['X'])
            COUNTS['saturated_template_controls']+=1
        COUNTS['zero_budget_templates']+=1
    if optimize:
        beta=exact(m['g'])[0]
        # independent private-neighbour formula uses an actual original colour side
        assert beta==private_optimum(m['g'],[v for v in range(len(m['g'])) if not m['graph_colour'][v]])
        check_selection(m['g'],m['graph_colour'],m['I']|m['C'],beta)
        COUNTS['exact_templates']+=1


def zero_model(cycles,paths,mode,seed):
    m=profile_model(cycles,paths,'empty');g=m['g'];rng=random.Random(seed);remaining=set()
    def edge(v,u):
        assert v!=u and m['graph_colour'][v]!=m['graph_colour'][u]
        g[v].add(u);g[u].add(v)
    for j,order in enumerate(m['components']):
        distinguished=m['cyclic'][j] and len(order)%8==4
        for bit in (0,1):
            U={m['owner'][x] for x in order if m['colour'][x]==bit}
            aa=sorted(v for v in U if not m['graph_colour'][v]);bb=sorted(U-set(aa))
            rng.shuffle(aa);rng.shuffle(bb)
            while len(aa)>(1 if distinguished else 0):
                a,c=aa.pop(),aa.pop();b,d=bb.pop(),bb.pop()
                for v,u in ((a,b),(b,c),(c,d),(d,a)):edge(v,u)
            assert len(aa)==len(bb)==int(distinguished)
            remaining.update(aa+bb)
    aa=sorted(v for v in remaining if not m['graph_colour'][v]);bb=sorted(remaining-set(aa));rng.shuffle(aa);rng.shuffle(bb)
    if mode=='matching':
        for v,u in zip(aa,bb):edge(v,u)
    elif mode=='cycle' and aa:
        for j,v in enumerate(aa):edge(v,bb[j]);edge(v,bb[(j+1)%len(bb)])
    elif mode=='random':
        es=list(product(aa,bb));rng.shuffle(es)
        for v,u in es:
            if len(g[v]&m['C'])<2 and len(g[u]&m['C'])<2 and rng.random()<.6:edge(v,u)
    else:assert mode in ('empty','cycle')
    return layers(g,m['C'],m['I'],m['X'],m['owner'],m['centre'],m['graph_colour'])


def main():
    for n in range(8):
        for a in range(n//2+1):
            es=list(product(range(a),range(a,n)))
            for mask in range(1<<len(es)):
                g=[set() for _ in range(n)]
                for j,(v,u) in enumerate(es):
                    if mask>>j&1:g[v].add(u);g[u].add(v)
                if max(map(len,g),default=0)<=3:check_graph(g,{v:int(v>=a) for v in range(n)})
    exhaustive=COUNTS['graphs']
    for b in range(1,4):
        for a in range(b+1):
            s=partial_model(b,a,[],[]);aa=sorted(v for v in s['C'] if not s['graph_colour'][v]);bb=sorted(s['C']-set(aa))
            xa=sorted(v for v in s['X'] if not s['graph_colour'][v]);xb=sorted(s['X']-set(xa));es=list(product(aa,bb))
            for mask in range(1<<len(es)):
                core=[e for j,e in enumerate(es) if mask>>j&1]
                if any(sum(v in e for e in core)>2 for v in s['C']):continue
                for interface in matchings(xa,xb):check_template(partial_model(b,a,core,interface),True)
    rng=random.Random(81162)
    for _ in range(90):
        n=rng.randrange(8,13);a=rng.randrange(1,n);g=[set() for _ in range(n)];es=list(product(range(a),range(a,n)));rng.shuffle(es)
        for v,u in es:
            if len(g[v])<3 and len(g[u])<3 and rng.random()<.6:g[v].add(u);g[u].add(v)
        check_graph(g,{v:int(v>=a) for v in range(n)})
    g=[set() for _ in range(14)]
    for j in range(7):
        for v in (j,(j-1)%7,(j-3)%7):g[v].add(7+j);g[7+j].add(v)
    beta,ss=all_minimal(g);assert beta==exact(g)[0]==7
    for S in ss:check_selection(g,{v:int(v>=7) for v in range(14)},S,beta)
    profiles=[([1],[]),([3],[]),([5],[]),([2],[]),([4],[]),([],[4]),([],[8]),
      ([1,1],[]),([1,3],[]),([3,3,1],[]),([1],[4]),([3,2],[4]),([1,3,2],[4,8])]
    for cycles,paths in profiles:
        for mode in ('empty','matching','cycle','random'):
            for seed in range(4):
                model=zero_model(cycles,paths,mode,seed);assert owner_slack(model,pairing_data(model))['sigma']==0
                check_template(model);COUNTS['targeted_zero_models']+=1
    for name in ('three-cycle-phase-ceiling','three-construction-ceiling'):
        f=json.loads((ROOT/('develop/fixtures/'+name+'.json')).read_text());g=[set() for _ in range(f['n'])]
        for v,u in f['edges']:g[v].add(u);g[u].add(v)
        m=layers(g,set(f['C']),set(f['I']),set(f['X']),{int(k):v for k,v in f['owner'].items()},
            {int(k):v for k,v in f['centre'].items()},{int(k):v for k,v in f['graph_colour'].items()})
        check_template(m);COUNTS['accepted_fixture_controls']+=1
    assert all(FEATURES[k] for k in ['ordinary_replacement','path_credit','both_resources','zero_without_either_resource','positive_gap'])
    report={'status':'PASS','counts':dict(sorted(COUNTS.items())),'features':dict(sorted(FEATURES.items())),
      'exhaustive_graph_models':exhaustive,'exact_control_digest':DIGEST.hexdigest(),
      'scope':'General written strict8n/81 proof and conditional zero-budget20beta>=52b+3bO+t. Finite original graphs check all minimal sets; exact small templates check their distinguished minimal selection. Targeted larger zero-budget models enumerate phases and check actual certificates, without computing unrestricted optima. The original equality obstruction follows from saturation and the external bipartite independent set, not finite-order enumeration. Imported older main suites are not executed. No Lean, template13/5 impossibility or smaller asymptotic graph coefficient.'}
    out=ROOT/'output/zero-budget-repair-check.json';out.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'PASS','bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
if __name__=='__main__':main()
