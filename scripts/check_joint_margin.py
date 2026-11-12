#!/usr/bin/env python3
"""Exact physical checks of the shared-margin31/314 construction."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from itertools import product
import hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'develop'),str(ROOT/'scripts')]
from subcubic_joint_margin import resources,template_certificate,full_certificate
from subcubic_phase_pairing import expectation
from subcubic_partial_template import layers
from check_unrestricted_subcubic_gap import all_minimal,matchings,partial_model,valid_graph
from check_subcubic_intrinsic_obstruction import diss,exact,private_optimum
from check_odd_cycle_compensation import profile_model,residual_optimum
from check_zero_budget_repair import zero_model
if not __debug__:raise RuntimeError('Assertions required')
COUNTS=Counter();FEATURES=Counter();DIGEST=hashlib.sha256()


def check_selection(g,colour,S,beta):
    D,data=full_certificate(g,S,colour,beta)
    assert diss(g,D) and len(D)<=beta
    assert all(diss(g,A) and len(A)<=beta for A in data['alternatives'])
    assert 314*(len(S)-beta)<=31*len(g)
    c=data['counts'];res=data['template_data']['resources']
    assert sum(data['nonnegative_terms'])==62*len(g)-628*(len(S)-beta)
    assert diss(g,data['retained']) and not data['inner']&data['retained']
    assert all(not (g[v]&data['inner']) for v in data['retained'])
    for key in ('p','e','b3','r','q','Z','W'):FEATURES['full_'+key+'_positive']+=c[key]>0
    for key,value in data['boundary_by_layer'].items():FEATURES['external_'+key+'_edge']+=value>0
    FEATURES['positive_gap']+=len(S)>beta
    FEATURES['positive_sigma_extraction']+=res['sigma']>0
    FEATURES['nonempty_extraction']+=bool(data['template']['I'])
    COUNTS['minimal_selections']+=1
    DIGEST.update(json.dumps([len(g),sorted(S),beta,sorted(D),c],sort_keys=True).encode()+b'\n')


def check_graph(g,colour):
    valid_graph(g,colour);beta,ss=all_minimal(g);assert beta==exact(g)[0]
    for S in ss:check_selection(g,colour,S,beta)
    COUNTS['graphs']+=1;COUNTS['literal_subsets']+=1<<len(g)


def check_template(m,optimize=False,phases=True):
    valid_graph(m['g'],m['graph_colour']);D,data=template_certificate(m)
    assert diss(m['g'],D) and all(diss(m['g'],A) for A in data['alternatives'])
    r=data['resources'];b=len(m['I'])
    assert 20*len(D)>=52*b+12*r['sigma']+3*r['bG']+r['tg']
    assert 2*r['tb']+2*r['sb']<=24*r['sigma']
    FEATURES['positive_sigma_template']+=r['sigma']>0
    FEATURES['zero_sigma_template']+=r['sigma']==0
    for k in ('tg','tb','sg','sb','bG'):FEATURES[k+'_positive']+=r[k]>0
    for row in r['classes']:
        FEATURES['shared_bad_path_and_flag']+=row['p']>0 and row['f']>0
        FEATURES['distinguished_bad_path']+=row['distinguished'] and row['p']>0
    FEATURES['non_square_monochromatic']+=any(c.get('non_square_mono',False) for c in r['pairing']['classes'].values())
    FEATURES['mixed_cycle_loss']+=any(c['mixed'] for c in r['pairing']['classes'].values())
    FEATURES['combined_good_and_bad']+=r['bG']>0 and r['tb']>0
    if phases:
        rem=data['remainder'];scores={}
        for bits in product((0,1),repeat=len(rem['components'])):
            fixed=dict(enumerate(bits));A={rem['owner'][x] for x in rem['X'] if rem['colour'][x]!=bits[rem['group'][x]]}
            score=expectation(data['terms'],fixed)
            optimum=residual_optimum(m['g'],A)
            assert Fraction(optimum)-Fraction(2*len(A),3)>=score
            scores[bits]=score
            for row in data['remainder_resources']['events']:
                if all(bits[j]==bit for j,bit in row['requirements'].items()):
                    K=row['prefix'];assert K<=A and all(m['g'][v]&A<=K for v in K)
                    COUNTS['endpoint_event_witnesses']+=1
            COUNTS['phase_assignments']+=1
        assert sum(scores.values())/len(scores)==data['initial']
        for k,value in enumerate(data['steps']):
            selected=[s for bits,s in scores.items() if all(bits[j]==data['phases'][j] for j in range(k))]
            assert sum(selected)/len(selected)==value
            COUNTS['conditional_expectation_controls']+=1
    if optimize:
        beta=exact(m['g'])[0]
        assert beta==private_optimum(m['g'],[v for v in range(len(m['g'])) if not m['graph_colour'][v]])
        check_selection(m['g'],m['graph_colour'],m['I']|m['C'],beta)
        COUNTS['exact_templates']+=1
    COUNTS['templates']+=1


def long_class_paths(cycles,paths,with_good=False):
    m=zero_model(cycles,paths,'empty',0) if with_good else profile_model(cycles,paths,'empty')
    g=m['g']
    for j,order in enumerate(m['components']):
        if with_good and not m['cyclic'][j]:continue
        for bit in (0,1):
            U={m['owner'][x] for x in order if m['colour'][x]==bit}
            aa=sorted(v for v in U if not m['graph_colour'][v]);bb=sorted(U-set(aa))
            # Replace all old core edges in this class before making one path.
            for v in U:
                for u in list(g[v]&m['C']):g[v].remove(u);g[u].remove(v)
            order2=[v for pair in zip(aa,bb) for v in pair]
            for v,u in zip(order2,order2[1:]):g[v].add(u);g[u].add(v)
    return layers(g,m['C'],m['I'],m['X'],m['owner'],m['centre'],m['graph_colour'])



def mixed_loss_model(cyclic):
    m=profile_model([3,5] if cyclic else [],[] if cyclic else [6,10],'empty')
    groups=[]
    for j in (0,1):
        U={m['owner'][x] for x in m['components'][j] if m['colour'][x]==0}
        groups.append(([v for v in sorted(U) if not m['graph_colour'][v]],
                       [v for v in sorted(U) if m['graph_colour'][v]]))
    a0,b0=groups[0];a1,b1=groups[1]
    aa=a0[:2]+a1[:3];bb=b0[:1]+b1[:4]
    order=[v for pair in zip(aa,bb) for v in pair]
    g=m['g']
    def edge(v,u):
        assert m['graph_colour'][v]!=m['graph_colour'][u]
        g[v].add(u);g[u].add(v)
    for v,u in zip(order,order[1:]+order[:1]):edge(v,u)
    # The same owner class supports a mixed loss and a disjoint bad-prefix
    # triple; in the auxiliary-path variant it also receives a bad-path flag.
    rest=[b0[1],a0[2],b0[2]]
    for v,u in zip(rest,rest[1:]):edge(v,u)
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
                check_template(zero_model(cycles,paths,mode,seed));COUNTS['targeted_zero_models']+=1
        for mode in ('empty','intact','random','broken'):
            for seed in range(6):
                check_template(profile_model(cycles,paths,mode,seed));COUNTS['targeted_general_models']+=1
    for cycles,paths,good in [([],[4],False),([3],[],False),([5],[],False),([3],[4],True),([2,3],[4],True)]:
        check_template(long_class_paths(cycles,paths,good));COUNTS['targeted_long_prefix_models']+=1
    for cyclic in (False,True):
        check_template(mixed_loss_model(cyclic));COUNTS['targeted_mixed_support_models']+=1
    for name in ('three-cycle-phase-ceiling','three-construction-ceiling'):
        f=json.loads((ROOT/('develop/fixtures/'+name+'.json')).read_text());g=[set() for _ in range(f['n'])]
        for v,u in f['edges']:g[v].add(u);g[u].add(v)
        m=layers(g,set(f['C']),set(f['I']),set(f['X']),{int(k):v for k,v in f['owner'].items()},
          {int(k):v for k,v in f['centre'].items()},{int(k):v for k,v in f['graph_colour'].items()})
        check_template(m);COUNTS['accepted_fixture_controls']+=1
    required=['positive_gap','positive_sigma_extraction','nonempty_extraction','positive_sigma_template','zero_sigma_template',
      'tg_positive','tb_positive','sg_positive','sb_positive','bG_positive','shared_bad_path_and_flag',
      'distinguished_bad_path','non_square_monochromatic','mixed_cycle_loss','combined_good_and_bad',
      'external_I_edge','external_C_edge','external_X_edge']
    assert all(FEATURES[k]>0 for k in required),{k:FEATURES[k] for k in required}
    report={'status':'PASS','counts':dict(sorted(COUNTS.items())),'features':dict(sorted(FEATURES.items())),
      'exhaustive_graph_models':exhaustive,'exact_control_digest':DIGEST.hexdigest(),
      'scope':'Written universal314d<=31n proof; shared class-margin allocation, disjoint physical supports, conditional phase scores, three actual full-graph alternatives, layer boundary bounds and exact nonnegative62n-628d ledger. All minimal sets in finite graph controls and independent exact small-template optima; larger prescribed templates check actual certificates and all phases without unrestricted large exact optimization. Imported older main suites are not executed. No Lean or sharpness claim.'}
    out=ROOT/'output/joint-margin-check.json';out.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'PASS','bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
if __name__=='__main__':main()
