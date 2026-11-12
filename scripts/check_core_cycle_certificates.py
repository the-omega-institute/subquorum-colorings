#!/usr/bin/env python3
"""Independent physical checks of square corrections and the girth hierarchy."""
from pathlib import Path
from fractions import Fraction
from itertools import product
from collections import Counter
import hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'develop'))
from subcubic_core_cycles import full_certificate,template_certificate
from subcubic_partial_template import layers
from check_unrestricted_subcubic_gap import all_minimal,matchings,partial_model,valid_graph
from check_subcubic_intrinsic_obstruction import exact,private_optimum,literal,diss
from check_odd_cycle_compensation import profile_model,components,residual_optimum
if not __debug__:raise RuntimeError('Assertions required')
COUNTS=Counter();FEATURES=Counter();DIGEST=hashlib.sha256()


def reference(m,bits):
    R={m['owner'][x] for x in m['X'] if m['colour'][x]!=bits[m['group'][x]]}
    raw=0;squares=[]
    for comp in components(m['g'],m['C']):
        if len(comp)==4 and all(len(m['g'][v]&comp)==2 for v in comp):
            present=comp&R
            labels=sorted(present);induced=[{labels.index(u) for u in m['g'][v]&present} for v in labels]
            bb=exact(induced)[0];assert bb==min(len(present),2)
            raw+=5*bb-3*len(present);squares.append(comp)
    optimum=residual_optimum(m['g'],R)
    assert 5*optimum>=3*len(R)+raw
    for comp in components(m['g'],R):
        if len(comp)==4 and all(len(m['g'][v]&comp)==2 for v in comp):
            assert comp in squares
    return raw,R,optimum


def check_template(m,optimize=False,phases=True):
    b=len(m['I']);D,data=template_certificate(m);valid_graph(m['g'],m['graph_colour'])
    assert diss(m['g'],D) and 5*len(D)>=13*b+data['eta']
    FEATURES['negative_eta']+=data['eta']<0;FEATURES['positive_eta']+=data['eta']>0
    FEATURES['fractional_eta']+=data['eta'].denominator>1
    FEATURES['core_square']+=bool(data['terms'])
    FEATURES['partial_interface']+=not all(m['cyclic'])
    FEATURES['unbalanced']+=sum(1-2*m['graph_colour'][v] for v in m['I'])!=0
    S=m['I']|m['C'];inverse={c:x for x,c in m['owner'].items()}
    assert all(literal(m['g'],S,x) for x in m['X'])
    assert all(not literal(m['g'],S-{v},v if v in m['I'] else inverse[v]) for v in S)
    if phases:
        scores={}
        for bits in product((0,1),repeat=len(m['components'])):
            raw,R,bb=reference(m,bits);scores[bits]=Fraction(raw)
            lengths=[len(c) for c in components(m['g'],R)
                     if all(len(m['g'][v]&c)==2 for v in c)]
            for h in range(1,min([len(c) for c in data['cycles']],default=0)//6+1):
                assert (3*h+2)*bb>=(2*h+1)*b
            if not data['cycles']:assert 3*bb>=2*b
            if b<=6:
                labels=sorted(R);g=[{labels.index(u) for u in m['g'][v]&R} for v in labels]
                assert exact(g)[0]==bb;COUNTS['independent_residual_optima']+=1
            COUNTS['phase_assignments']+=1
        assert sum(scores.values())/len(scores)==data['eta']
        for k,want in enumerate(data['steps']):
            matches=[v for bits,v in scores.items()
                     if all(bits[j]==data['phases'][j] for j in range(k))]
            assert sum(matches)/len(matches)==want;COUNTS['conditional_steps']+=1
    if optimize:
        beta=exact(m['g'])[0]
        assert beta==private_optimum(m['g'],[v for v in range(len(m['g'])) if not m['graph_colour'][v]])
        assert beta>=len(D);check_selection(m['g'],m['graph_colour'],S,beta)
        COUNTS['exact_templates']+=1
    COUNTS['templates']+=1


def check_selection(g,colour,S,beta):
    D,data=full_certificate(g,S,colour,beta);assert diss(g,D) and len(D)<=beta
    assert not data['inner']&data['retained']
    assert all(not g[v]&data['inner'] for v in data['retained'])
    assert 648*(len(S)-beta)<=64*len(g)-data['phase']['E8']
    FEATURES['retained_leaves']+=bool(data['witnesses']['triples'])
    FEATURES['positive_gap']+=len(S)>beta
    FEATURES['b3_positive']+=data['counts']['b3']>0
    FEATURES['nonempty_extracted_core']+=bool(data['template']['C'])
    COUNTS['hierarchy_certificates']+=len(data['hierarchy'])
    COUNTS['minimal_selections']+=1
    DIGEST.update(json.dumps([len(g),sorted(S),beta,sorted(D),data['phase']['E8'],data['counts']],sort_keys=True).encode()+b'\n')


def check_graph(g,colour):
    valid_graph(g,colour);beta,selections=all_minimal(g);assert exact(g)[0]==beta
    for S in selections:check_selection(g,colour,S,beta)
    COUNTS['graphs']+=1;COUNTS['literal_subsets']+=1<<len(g)


def main():
    for n in range(8):
        for a in range(n//2+1):
            edges=list(product(range(a),range(a,n)))
            for bits in range(1<<len(edges)):
                g=[set() for _ in range(n)]
                for j,(v,u) in enumerate(edges):
                    if bits>>j&1:g[v].add(u);g[u].add(v)
                if max(map(len,g),default=0)<=3:check_graph(g,{v:int(v>=a) for v in range(n)})
    exhaustive_graphs=COUNTS['graphs']
    for b in range(1,4):
        for a in range(b+1):
            seed=partial_model(b,a,[],[]);ca=sorted(v for v in seed['C'] if not seed['graph_colour'][v]);cb=sorted(seed['C']-set(ca))
            xa=sorted(v for v in seed['X'] if not seed['graph_colour'][v]);xb=sorted(seed['X']-set(xa));edges=list(product(ca,cb))
            for mask in range(1<<len(edges)):
                core=[e for j,e in enumerate(edges) if mask>>j&1]
                if any(sum(v in e for e in core)>2 for v in seed['C']):continue
                for interface in matchings(xa,xb):check_template(partial_model(b,a,core,interface),True)
    exhaustive_templates=COUNTS['exact_templates']
    rng=random.Random(111181)
    for _ in range(90):
        n=rng.randrange(8,13);a=rng.randrange(1,n);g=[set() for _ in range(n)];edges=list(product(range(a),range(a,n)));rng.shuffle(edges)
        for v,u in edges:
            if len(g[v])<3 and len(g[u])<3 and rng.random()<.6:g[v].add(u);g[u].add(v)
        check_graph(g,{v:int(v>=a) for v in range(n)})
    g=[set() for _ in range(14)]
    for j in range(7):
        for v in (j,(j-1)%7,(j-3)%7):g[v].add(7+j);g[7+j].add(v)
    beta,ss=all_minimal(g);assert beta==exact(g)[0]==7
    for S in ss:check_selection(g,{v:int(v>=7) for v in range(14)},S,beta)
    # Every4-tuple of signed literals on4bits realized on a physical core C4.
    literal_values=set()
    for labels in product(range(8),repeat=4):
        m=profile_model([3]*4,[],'empty');chosen=[]
        for i,label in enumerate(labels):
            group,bit=divmod(label,2)
            options=[v for x,v in m['owner'].items() if m['group'][x]==group
                     and m['colour'][x]==bit and m['graph_colour'][v]==i%2 and v not in chosen]
            chosen.append(min(options))
        for v,u in zip(chosen,chosen[1:]+chosen[:1]):m['g'][v].add(u);m['g'][u].add(v)
        D,data=template_certificate(m);assert diss(m['g'],D)
        values=[reference(m,bits)[0] for bits in product((0,1),repeat=4)]
        eta=Fraction(sum(values),16);assert eta==data['eta'];literal_values.add(str(eta))
        assert eta==-1 if len(set(labels))==1 else eta>=Fraction(1,4)
        COUNTS['physical_literal_patterns']+=1
    # Exact density controls and physical tight cycles for every hierarchy level.
    for h in range(1,33):
        for length in range(6*h,6*h+132,2):
            assert Fraction((2*length)//3,length)>=Fraction(2*h+1,3*h+2)
            COUNTS['cycle_density_controls']+=1
        ell=3*h+2;m=profile_model([ell],[],'empty')
        for bit in (0,1):
            U={m['owner'][x] for x in m['X'] if m['colour'][x]==bit}
            aa=sorted(v for v in U if not m['graph_colour'][v]);bb=sorted(U-set(aa))
            order=[v for pair in zip(aa,bb) for v in pair]
            for v,u in zip(order,order[1:]+order[:1]):m['g'][v].add(u);m['g'][u].add(v)
        D,data=template_certificate(m)
        for bits in product((0,1),repeat=1):
            raw,R,bb=reference(m,bits)
            assert (3*h+2)*bb==(2*h+1)*len(R)
        assert diss(m['g'],D)
        # |D| is a certified lower bound here, not an asserted unrestricted optimum.
        _,full=full_certificate(m['g'],m['I']|m['C'],m['graph_colour'],len(D))
        assert len(full['hierarchy'])==h
        COUNTS['large_hierarchy_lower_bound_controls']+=1
    for cycles,paths in [([1]*16,[]),([1,2,3,5],[1,2,3]),([],[1,2,3,4,5])]:
        for j,mode in enumerate(('empty','intact','broken','random')):
            check_template(profile_model(cycles,paths,mode,810+j),False,False)
    fixture=json.loads((ROOT/'develop/fixtures/three-cycle-phase-ceiling.json').read_text())
    g=[set() for _ in range(30)]
    for v,u in fixture['edges']:g[v].add(u);g[u].add(v)
    m=layers(g,set(fixture['C']),set(fixture['I']),set(fixture['X']),{int(k):v for k,v in fixture['owner'].items()},
             {int(k):v for k,v in fixture['centre'].items()},{int(k):v for k,v in fixture['graph_colour'].items()})
    check_template(m,True,True)
    for row in fixture['all_phases']:
        raw,R,bb=reference(m,row['phase']);assert bb==4 and R==set(row['residual'])
        cc=components(g,R);assert sorted(map(len,cc))==[3,3]
        assert all(sorted(len(g[v]&c) for v in c)==[1,1,2] for c in cc)
        COUNTS['ceiling_phase_controls']+=1
    assert exact(g)[0]==private_optimum(g,[v for v in range(30) if not m['graph_colour'][v]])==17
    assert diss(g,set(fixture['attaining_dissociation_set']))
    assert all(FEATURES[k] for k in ('negative_eta','positive_eta','fractional_eta','core_square','retained_leaves','b3_positive','positive_gap','partial_interface','unbalanced'))
    report=dict(counts=dict(COUNTS),features=dict(FEATURES),exhaustive_graph_models=exhaustive_graphs,
                exhaustive_partial_templates=exhaustive_templates,heawood_minimal_sets=len(ss),literal_eta_values=sorted(literal_values),
                exact_control_digest=DIGEST.hexdigest(),scope='General written square-correction and core-girth proofs. General graph controls check all minimal selections; exact template controls check one distinguished minimal selection each. Large hierarchy tests use a certified physical lower bound, not an exact unrestricted beta. The phase ceiling has8 explicit base decompositions and an additive all-scale proof. Imported older main suites are not executed. No Lean or graph-sharpness.')
    out=ROOT/'output/core-cycle-certificates-check.json';out.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'PASS',**report,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
if __name__=='__main__':main()
