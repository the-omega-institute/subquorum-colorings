#!/usr/bin/env python3
"""Independent residual formulas, all-phase scores and unrestricted ledgers."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'develop'))
from subcubic_phase_pairing import template_certificates,full_certificate
from subcubic_partial_template import layers
from check_unrestricted_subcubic_gap import all_minimal,matchings,partial_model,valid_graph
from check_subcubic_intrinsic_obstruction import exact,private_optimum,literal,diss
from check_odd_cycle_compensation import profile_model,components,residual_optimum
if not __debug__:raise RuntimeError('Assertions required')
COUNTS=Counter();FEATURES=Counter();DIGEST=hashlib.sha256()


def check_selection(g,colour,S,beta):
    D,data=full_certificate(g,S,colour,beta)
    assert diss(g,D) and len(D)<=beta
    assert not data['inner']&data['retained']
    assert all(not g[v]&data['inner'] for v in data['retained'])
    assert diss(g,data['retained'])
    assert 81*(len(S)-beta)<=8*len(g)
    for key in ('a','p','b3','e','r','q'):
        FEATURES[key+'_positive']+=data['counts'][key]>0
    FEATURES['positive_gap']+=len(S)>beta
    FEATURES['retained_leaves']+=bool(data['witnesses']['triples'])
    COUNTS['minimal_selections']+=1
    DIGEST.update(json.dumps([len(g),sorted(S),beta,sorted(D),data['counts']],sort_keys=True).encode()+b'\n')


def check_graph(g,colour):
    valid_graph(g,colour);beta,ss=all_minimal(g);assert exact(g)[0]==beta
    for S in ss:check_selection(g,colour,S,beta)
    COUNTS['graphs']+=1;COUNTS['literal_subsets']+=1<<len(g)


def check_template(m,optimize=False,phases=True):
    b=len(m['I']);g=m['g'];D,data=template_certificates(m);p=data['pairing']
    valid_graph(g,m['graph_colour']);assert diss(g,D)
    assert all(diss(g,Z) for Z in data['alternatives']) and 5*len(D)>=13*b
    FEATURES['partial_interface']+=not all(m['cyclic'])
    FEATURES['unbalanced']+=sum(1-2*m['graph_colour'][v] for v in m['I'])!=0
    FEATURES['positive_rho']+=p['rho']>0
    charge_total=Fraction(0)
    for key,c in p['classes'].items():
        supports=[s for s,_ in c['mixed']];used=set(c['monochromatic'])
        for s in supports:assert not s&used;used|=s
        assert used<=c['U']
        assert c['loss']<=c['budget'];charge_total+=c['loss']
        FEATURES['distinguished_with_two_remainders']+=c['distinguished'] and len(c['remaining'])==2
    assert charge_total==p['rho']
    for row in p['rows']:
        FEATURES['cycle_'+str(len(row['K']))]+=1
        if len(row['full'])==1:FEATURES['monochromatic_cycle']+=1
        if row['loss'] and len(row['full'])>1:FEATURES['exceptional_mixed_cycle']+=1
        if row['gamma']==row['delta'] and row['delta']:FEATURES['full_cancellation']+=1
    if phases:
        scores={};sum_surplus=Fraction(0)
        for bits in product((0,1),repeat=len(m['components'])):
            A={m['owner'][x] for x in m['X'] if m['colour'][x]!=bits[m['group'][x]]}
            bb=residual_optimum(g,A);score=Fraction(0)
            for coeff,req in p['terms']:
                if all(bits[j]==bit for j,bit in req.items()):score+=coeff
            assert Fraction(bb)-Fraction(2*len(A),3)>=score
            for row in p['rows']:
                K=row['K'];v=residual_optimum(g,A&K)-Fraction(2*len(A&K),3)
                s=-row['delta']*all(bits[j]==bit for j,bit in row['full'].items())
                if row['gamma']:s+=row['gamma']*all(bits[j]==bit for j,bit in row['compensation'].items())
                assert v>=s;COUNTS['cycle_pointwise_comparisons']+=1
            sum_surplus+=Fraction(bb)-Fraction(b,2);scores[bits]=score
            if b<=6:
                vs=sorted(A);remap={v:j for j,v in enumerate(vs)}
                induced=[{remap[u] for u in g[v]&A} for v in vs]
                assert exact(induced)[0]==bb;COUNTS['independent_residual_optima']+=1
            COUNTS['phase_assignments']+=1
        assert sum(scores.values())/len(scores)==-p['rho']
        assert sum_surplus/len(scores)>=Fraction(p['odd'],3)
        for k,want in enumerate(data['steps']):
            options=[s for bits,s in scores.items() if all(bits[j]==data['phases'][j] for j in range(k))]
            assert sum(options)/len(options)==want;COUNTS['conditional_steps']+=1
        FEATURES['sharp_phase_expectation']+=sum_surplus/len(scores)==Fraction(p['odd'],3) and p['odd']>0
    S=m['I']|m['C'];inverse={c:x for x,c in m['owner'].items()}
    assert all(literal(g,S,x) for x in m['X'])
    assert all(not literal(g,S-{v},v if v in m['I'] else inverse[v]) for v in S)
    if optimize:
        beta=exact(g)[0];assert beta==private_optimum(g,[v for v in range(len(g)) if not m['graph_colour'][v]])
        assert beta>=len(D);check_selection(g,m['graph_colour'],S,beta);COUNTS['exact_templates']+=1
    COUNTS['templates']+=1


def partitions(n,k=1,minimum=1):
    if n==0:yield []
    if k>5:return
    for first in range(minimum,n+1):
        for rest in partitions(n-first,k+1,first):yield [first]+rest


def physical_cycle(labels,ell=11):
    k=max(j for j,bit in labels)+1
    m=profile_model([ell]*k,[],'empty');chosen=[]
    for pos,(j,bit) in enumerate(labels):
        candidates=[v for x,v in m['owner'].items() if m['group'][x]==j and m['colour'][x]==bit
                    and m['graph_colour'][v]==pos%2 and v not in chosen]
        chosen.append(min(candidates))
    for v,u in zip(chosen,chosen[1:]+chosen[:1]):m['g'][v].add(u);m['g'][u].add(v)
    return m


def main():
    for n in range(8):
        for a in range(n//2+1):
            es=list(product(range(a),range(a,n)))
            for mask in range(1<<len(es)):
                g=[set() for _ in range(n)]
                for j,(v,u) in enumerate(es):
                    if mask>>j&1:g[v].add(u);g[u].add(v)
                if max(map(len,g),default=0)<=3:check_graph(g,{v:int(v>=a) for v in range(n)})
    exhaustive_graphs=COUNTS['graphs']
    for b in range(1,4):
        for a in range(b+1):
            seed=partial_model(b,a,[],[]);aa=sorted(v for v in seed['C'] if not seed['graph_colour'][v]);bb=sorted(seed['C']-set(aa));es=list(product(aa,bb))
            xa=sorted(v for v in seed['X'] if not seed['graph_colour'][v]);xb=sorted(seed['X']-set(xa))
            for mask in range(1<<len(es)):
                core=[e for j,e in enumerate(es) if mask>>j&1]
                if any(sum(v in e for e in core)>2 for v in seed['C']):continue
                for interface in matchings(xa,xb):check_template(partial_model(b,a,core,interface),True)
    exhaustive_templates=COUNTS['exact_templates']
    rng=random.Random(811131)
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
    # All unordered positive class-size patterns through20, with at most5 bits.
    for n in range(4,21,2):
        for sizes in partitions(n):
            labels=[(j,0) for j,size in enumerate(sizes) for _ in range(size)]
            check_template(physical_cycle(labels));COUNTS['physical_residue_patterns']+=1
    # All signed4-tuples on2bits, including contradictory full-retention events.
    for labels in product(range(4),repeat=4):
        check_template(physical_cycle([divmod(x,2) for x in labels],3));COUNTS['signed_square_patterns']+=1
    for cy,pa in [([1,2,3,5],[1,2,3]),([],[1,2,3,4,5]),([1]*16,[])]:
        for j,mode in enumerate(('empty','intact','broken','random')):
            check_template(profile_model(cy,pa,mode,811+j),phases=len(cy)+len(pa)<=8)
    fixture=json.loads((ROOT/'develop/fixtures/three-cycle-phase-ceiling.json').read_text())
    g=[set() for _ in range(fixture['n'])]
    for v,u in fixture['edges']:g[v].add(u);g[u].add(v)
    m=layers(g,set(fixture['C']),set(fixture['I']),set(fixture['X']),
             {int(x):v for x,v in fixture['owner'].items()},
             {int(x):v for x,v in fixture['centre'].items()},
             {int(x):v for x,v in fixture['graph_colour'].items()})
    check_template(m)
    inverse={c:x for x,c in m['owner'].items()};seen=set()
    for bits in product((0,1),repeat=3):
        A={m['owner'][x] for x in m['X'] if m['colour'][x]!=bits[m['group'][x]]}
        cs=components(g,A);assert sorted(map(len,cs))==[3,3] and residual_optimum(g,A)==4
        COUNTS['sharp_ceiling_phases']+=1
    for pairs in [[(18,19),(20,21)],[(26,27),(28,29)],[(18,26),(19,27),(20,28),(21,29),(22,23),(24,25)]]:
        perm={v:v for v in m['C']}
        for a,b in pairs:perm[a]=b;perm[b]=a
        assert all({perm[u] for u in g[v]&m['C']}==g[perm[v]]&m['C'] for v in m['C'])
        for bits in product((0,1),repeat=3):
            A={m['owner'][x] for x in m['X'] if m['colour'][x]!=bits[m['group'][x]]}
            B={perm[v] for v in A};image=tuple(1-m['colour'][inverse[next(v for v in B if m['group'][inverse[v]]==j)]] for j in range(3))
            assert B=={m['owner'][x] for x in m['X'] if m['colour'][x]!=image[m['group'][x]]}
            seen.add((bits,image))
    witness={0,1,3,4,5,6,8,10,11,14,16,19,22,23,24,25,27}
    assert len(witness)==17 and diss(g,witness)
    # Transitive closure of independently checked phase actions.
    orbit={(0,0,0)}
    while True:
        more={v for u,v in seen if u in orbit}
        if more<=orbit:break
        orbit|=more
    assert len(orbit)==8
    assert FEATURES['exceptional_mixed_cycle'] and FEATURES['full_cancellation']
    assert FEATURES['distinguished_with_two_remainders'] and FEATURES['sharp_phase_expectation']
    report=dict(status='PASS',scope='New checker only; imported older checker mains are not run. General proofs are in the note.',
                exhaustive_graph_models=exhaustive_graphs,exhaustive_template_models=exhaustive_templates,
                counts=dict(sorted(COUNTS.items())),features=dict(sorted(FEATURES.items())),
                phase_ceiling=dict(vertices=30,b=6,o=3,phase_set_size=16,explicit_unrestricted_witness=17,phase_orbit=8),
                digest=DIGEST.hexdigest())
    path=ROOT/'output/sharp-phase-compensation-check.json';path.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status='PASS',report=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest())))
if __name__=='__main__':main()
