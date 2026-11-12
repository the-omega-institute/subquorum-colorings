#!/usr/bin/env python3
"""Physical checks of exact class budgets and a construction-family ceiling."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from itertools import product,combinations
import hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from subcubic_phase_slack import template_certificate,full_certificate
from subcubic_partial_template import layers
from check_unrestricted_subcubic_gap import all_minimal,matchings,partial_model,valid_graph
from check_subcubic_intrinsic_obstruction import diss,exact,literal,private_optimum
from check_odd_cycle_compensation import components,residual_optimum,profile_model
from check_sharp_phase_compensation import partitions,physical_cycle
if not __debug__:raise RuntimeError('Assertions required')
COUNTS=Counter();FEATURES=Counter();DIGEST=hashlib.sha256()


def structural_reference(m):
    core_components=components(m['g'],m['C']);O=D=0
    for j,order in enumerate(m['components']):
        distinguished=m['cyclic'][j] and len(order)%8==4
        for bit in (0,1):
            U={m['owner'][x] for x in order if m['colour'][x]==bit};covered=set()
            for K in core_components:
                if K<=U and len(K)==4 and all(len(m['g'][v]&K)==2 for v in K):covered|=K
            good=len(U-covered)==(2 if distinguished else 0)
            if not good:
                if distinguished:D+=1
                else:O+=1
    return O,D


def check_template(m,optimize=False,all_phases=True):
    g=m['g'];b=len(m['I']);D,data=template_certificate(m);p=data['baseline']['pairing'];slack=data['slack'];sigma=slack['sigma']
    assert diss(g,D);valid_graph(g,m['graph_colour']);O,B=structural_reference(m)
    assert (O,B)==(slack['ordinary_violations'],slack['distinguished_violations'])
    assert (sigma==0)==(O+B==0) and 12*sigma>=O+2*B
    FEATURES['zero_sigma']+=sigma==0;FEATURES['positive_sigma']+=sigma>0
    FEATURES['ordinary_violations']+=O>0;FEATURES['distinguished_violations']+=B>0
    FEATURES['partial_interface']+=not all(m['cyclic']);FEATURES['fractional_sigma']+=sigma.denominator>1
    if all_phases:
        total=Fraction(0)
        for bits in product((0,1),repeat=len(m['components'])):
            A={m['owner'][x] for x in m['X'] if m['colour'][x]!=bits[m['group'][x]]}
            optimum=residual_optimum(g,A);total+=Fraction(optimum)-Fraction(b,2)
            COUNTS['phase_assignments']+=1
        assert total/2**len(m['components'])>=Fraction(p['odd'],3)+sigma
    if optimize:
        beta=exact(g)[0];assert beta==private_optimum(g,[v for v in range(len(g)) if not m['graph_colour'][v]])
        assert 5*beta>=13*b+3*sigma
        check_selection(g,m['graph_colour'],m['I']|m['C'],beta);COUNTS['exact_templates']+=1
    COUNTS['templates']+=1


def check_selection(g,colour,S,beta):
    D,data=full_certificate(g,S,colour,beta);sigma=data['slack']['sigma'];d=len(S)-beta;n=len(g)
    assert diss(g,D) and len(D)<=beta
    assert 81*d<=8*n-3*sigma
    assert 81*d<=8*n-Fraction(data['slack']['ordinary_violations']+2*data['slack']['distinguished_violations'],4)
    assert d<=(8*n)//81-int(n%162==81)
    if sigma>0:assert d<=(8*n+80)//81-1
    FEATURES['positive_selected_gap']+=d>0;FEATURES['nonempty_extraction']+=bool(data['baseline']['template']['I'])
    COUNTS['minimal_selections']+=1
    DIGEST.update(json.dumps([n,sorted(S),beta,sorted(D),str(sigma)],sort_keys=True).encode()+b'\n')


def check_graph(g,colour):
    valid_graph(g,colour);beta,ss=all_minimal(g);assert beta==exact(g)[0]
    for S in ss:check_selection(g,colour,S,beta)
    COUNTS['graphs']+=1;COUNTS['literal_subsets']+=1<<len(g)


def load_fixture():
    f=json.loads((ROOT/'develop/fixtures/three-construction-ceiling.json').read_text());g=[set() for _ in range(f['n'])]
    for v,u in f['edges']:g[v].add(u);g[u].add(v)
    m=layers(g,set(f['C']),set(f['I']),set(f['X']),{int(k):v for k,v in f['owner'].items()},
             {int(k):v for k,v in f['centre'].items()},{int(k):v for k,v in f['graph_colour'].items()})
    return f,m


def quotient_set(m,side,J):
    T={x for x in m['X'] if m['centre'][x] in J};forbidden={m['q'][x] for x in T if x in m['q']}
    D={v for v in m['C'] if m['graph_colour'][v]==side}|T
    D|={v for v in m['I'] if m['graph_colour'][v]==side and v not in J}
    for v in m['I']:
        if m['graph_colour'][v]==side:continue
        D.add(v);options=(m['g'][v]&m['X'])-forbidden
        if options:D.add(min(options))
    return D


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
    rng=random.Random(162081)
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
    for n in range(4,21,2):
        for sizes in partitions(n):
            check_template(physical_cycle([(j,0) for j,size in enumerate(sizes) for _ in range(size)]));COUNTS['physical_class_patterns']+=1
    for labels in product(range(4),repeat=4):
        check_template(physical_cycle([divmod(x,2) for x in labels],3));COUNTS['signed_square_patterns']+=1
    for cy,pa in [([1,2,3,5],[1,2,3]),([],[1,2,3,4,5])]:
        for j,mode in enumerate(('empty','intact','broken','random')):check_template(profile_model(cy,pa,mode,162+j))
    f,m=load_fixture();g=m['g'];assert len(components(g,set(range(50))))==1
    assert len(g)==50 and sum(map(len,g))//2==70 and sorted(map(len,m['components']))==[4,4,12]
    assert sum(1 for v in range(50) if m['graph_colour'][v])==25
    assert all(len(g[v])==(2 if v in m['I'] else 3) for v in range(50))
    S=m['I']|m['C'];inverse={v:x for x,v in m['owner'].items()}
    assert all(literal(g,S,x) for x in m['X'])
    assert all(not literal(g,S-{v},v if v in m['I'] else inverse[v]) for v in S)
    phase_sizes=[]
    for bits in product((0,1),repeat=3):
        A={m['owner'][x] for x in m['X'] if m['colour'][x]!=bits[m['group'][x]]}
        cs=components(g,A);assert sorted(map(len,cs))==[3,3,4]
        vs=sorted(A);remap={v:j for j,v in enumerate(vs)};induced=[{remap[u] for u in g[v]&A} for v in vs]
        assert exact(induced)[0]==residual_optimum(g,A)==6
        phase_sizes.append(20+6);COUNTS['ceiling_residual_optima']+=1
    quotient_max=[]
    for side in (0,1):
        helpers=sorted(v for v in m['I'] if m['graph_colour'][v]==side);sizes=[]
        for mask in range(1<<len(helpers)):
            J={v for j,v in enumerate(helpers) if mask>>j&1};D=quotient_set(m,side,J);assert diss(g,D);sizes.append(len(D));COUNTS['quotient_subsets']+=1
        quotient_max.append(max(sizes))
    assert phase_sizes==[26]*8 and quotient_max==[26,26]
    witness=set(f['attaining_witness']);assert len(witness)==27 and diss(g,witness)
    check_template(m);D,data=template_certificate(m);assert len(D)==26 and data['slack']['sigma']==0
    # Actual large unions, without enumerating2^(3t) global phases or exact beta.
    for t in (2,3,8,32):
        gg=[set() for _ in range(50*t)];colour={};owner={};centre={};I=set();C=set();X=set();W=set()
        for j in range(t):
            shift=50*j
            for v in range(50):gg[shift+v]={shift+u for u in g[v]};colour[shift+v]=m['graph_colour'][v]
            I|={shift+v for v in m['I']};C|={shift+v for v in m['C']};X|={shift+v for v in m['X']};W|={shift+v for v in witness}
            owner.update({shift+x:shift+v for x,v in m['owner'].items()});centre.update({shift+x:shift+v for x,v in m['centre'].items()})
        big=layers(gg,C,I,X,owner,centre,colour);D,data=template_certificate(big)
        assert len(D)==26*t and data['slack']['sigma']==0 and len(W)==27*t and diss(gg,W)
        COUNTS['large_union_certificates']+=1
    assert all(FEATURES[k] for k in ('zero_sigma','positive_sigma','ordinary_violations','distinguished_violations','partial_interface','fractional_sigma','positive_selected_gap'))
    report=dict(status='PASS',counts=dict(sorted(COUNTS.items())),features=dict(sorted(FEATURES.items())),exhaustive_graph_models=exhaustive_graphs,exact_control_digest=DIGEST.hexdigest(),ceiling=dict(n=50,b=10,o=3,connected=True,quotient_maxima=quotient_max,phase_maximum=26,explicit_witness=27,unrestricted_optimum='not computed or claimed'),scope='General written proofs, exact finite implementation controls. Imported older checker mains are not run. Large unions check actual certificates, not exact unrestricted optima or all global phases. Optional exploratory full50vertex recurrence was terminated for memory after an explicit27set sufficed; no optimum was obtained or used. The unconditional n=81mod162 refinement follows from the parity proof, not finite-order extrapolation.')
    out=ROOT/'output/phase-budget-equality-check.json';out.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest())))
if __name__=='__main__':main()
