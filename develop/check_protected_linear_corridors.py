"""Protected line corridors: extreme resources and one min-cost fork flow.

General proof: docs/PROTECTED_LINEAR_CORRIDORS.md. Primitive packing and
all gate states independently check the optimization, not prove the theorem.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_destructive_exchange_choice import constrained_optimum
from check_frozen_coordinated_pivots import family
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_canonical_band_coarsening import forests
from check_degree_changing_bent_completions import compile_model
from check_P_free_pivot_interface import regions
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import canonical, optimize

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def subsets(items):
    items=list(items)
    return [frozenset(x for i,x in enumerate(items) if mask>>i&1)
            for mask in range(1<<len(items))]


def requirements(corridor, index, side):
    return {g for g,slot in corridor['gates'] if
            (slot<=index if side=='left' else slot>index)}


def offers(corridors, weights):
    result=[]
    for i,c in enumerate(corridors):
        units=c['units']
        if not units:continue
        for side,j in [('left',0),('right',len(units)-1)]:
            if c[side] is not None:
                G=requirements(c,j,side)
                result.append(dict(corridor=i,side=side,owner=c[side],unit=units[j],
                                   gates=G,fee=sum(weights[g] for g in G)))
    assert sum(len(o['gates']) for o in result)==len(set().union(set(),*(o['gates'] for o in result)))
    return result


def apply(base, corridors, opened, compressed=False):
    W={o:set(S) for o,S in base[3].items()}
    for c in corridors:
        for j,unit in enumerate(c['units']):
            for side in ('left','right'):
                if compressed and j!=(0 if side=='left' else len(c['units'])-1):continue
                if c[side] is not None and requirements(c,j,side)<=opened:
                    W[c[side]].add(unit)
    return (*base[:3],W,base[4])


def corridor_flow(base,corridors,weights,required=frozenset(),independent=True):
    """Costed exact full fork network, independently constructed here.

    Integral min-cost max-flow uses Bellman--Ford. New support arcs cost
    scale*once-per-prefix fee; terminal links cost one. The extreme-resource
    theorem, not generic charging per path, justifies this objective.
    """
    kinds,pairs,links,W,Q=base;own,A,B,M=owner_data(kinds,pairs)
    H=len(A)+len(M);scale=H+1;protect=scale*sum(weights.values())+H+1
    source=('s',);sink=('t',);adj=defaultdict(list);edges=[]
    def add(u,v,cap,cost=0,tag=None):
        i=len(edges)
        edges.extend([dict(u=u,v=v,cap=cap,initial=cap,cost=cost,tag=tag),
                      dict(u=v,v=u,cap=0,initial=0,cost=-cost,tag=None)])
        adj[u].append(i);adj[v].append(i+1)
    exit=lambda o:('a',o) if o in A else ('out',o) if o in M else ('b',o)
    for a in sorted(A):add(source,exit(a),1,-protect if a in required else 0,('source',a))
    for m in sorted(M):add(('in',m),exit(m),1)
    for b in sorted(B):
        for tip in pairs[b]:add(('tip',tip),exit(b),1)
        add(exit(b),sink,1)
    for j in sorted(Q):add(('resource',j),sink,1)
    for p,q in sorted(set(links)):
        if own[p]!=own[q]:
            add(exit(own[p]),('tip',q) if own[q] in B else ('in',own[q]),len(A)+1,1,('link',p,q))
    for o,S in W.items():
        for j in sorted(S):add(exit(o),('resource',j),len(A)+1)
    oo=offers(corridors,weights)
    for i,o in enumerate(oo):
        add(exit(o['owner']),('resource',o['unit']),1,scale*o['fee'],('offer',i))
    value=0;nodes=set(adj)|{source,sink}
    while True:
        dist={source:0};parent={}
        for _ in range(len(nodes)-1):
            changed=False
            for i,e in enumerate(edges):
                if e['cap'] and e['u'] in dist:
                    alt=dist[e['u']]+e['cost']
                    if e['v'] not in dist or alt<dist[e['v']]:
                        dist[e['v']]=alt;parent[e['v']]=i;changed=True
            if not changed:break
        if sink not in dist:break
        v=sink;seen=set()
        while v!=source:
            assert v not in seen;seen.add(v)
            i=parent[v];edges[i]['cap']-=1;edges[i^1]['cap']+=1;v=edges[i]['u']
        value+=1
    used=[e for e in edges[::2] if e['initial']>e['cap']]
    chosen=[oo[e['tag'][1]] for e in used if e['tag'] and e['tag'][0]=='offer']
    opened=set().union(set(),*(o['gates'] for o in chosen))
    fee=sum(weights[g] for g in opened)
    assert fee==sum(o['fee'] for o in chosen)
    nlinks=sum(e['initial']-e['cap'] for e in used if e['tag'] and e['tag'][0]=='link')
    paid={e['tag'][1] for e in used if e['tag'] and e['tag'][0]=='source'}
    assert required<=paid and nlinks<=H
    if independent:
        assert constrained_optimum(apply(base,corridors,opened),required)==(value,nlinks)
    return dict(value=value,fee=fee,links=nlinks,opened=sorted(opened),paid=sorted(paid),scale=scale)


def validate(base,corridors,weights,counts):
    resources=[j for c in corridors for j in c['units']]
    gates=[g for c in corridors for g,slot in c['gates']]
    assert len(resources)==len(set(resources)) and len(gates)==len(set(gates))
    assert set(resources)<=base[4] and all(not set(resources)&S for S in base[3].values())
    assert all(0<=slot<=len(c['units']) for c in corridors for g,slot in c['gates'])
    assert set(gates)==set(weights) and all(isinstance(w,int) and w>=0 for w in weights.values())
    candidates=[]
    for F in subsets(sorted(weights)):
        original=apply(base,corridors,F);compressed=apply(base,corridors,F,True)
        p=optimize(*original);q=optimize(*compressed);f=fork_flow(*original)
        assert (p['value'],p['cost'])==(q['value'],q['cost'])==(f['value'],f['cost'])
        candidates.append((p['value'],sum(weights[g] for g in F),p['cost'],F))
        counts['all_state_extreme_privatization_vs_primitive_and_flow']+=1
        counts['states_with_beta_forks']+=any(c['kind']=='fork' for c in f['certificates'])
    expected=max(candidates,key=lambda c:(c[0],-c[1],-c[2]))
    result=corridor_flow(base,corridors,weights)
    assert (result['value'],result['fee'],result['links'])==expected[:3]
    counts['single_flow_vs_gate_enumeration_lex_optima']+=1
    _,A,_,_=owner_data(*base[:2]);old=apply(base,corridors,set())
    for P in subsets(sorted(A)):
        if constrained_optimum(old,P) is None:continue
        constrained=[]
        for value,fee,links,F in candidates:
            pair=constrained_optimum(apply(base,corridors,F),P)
            if pair is not None:constrained.append((pair[0],fee,pair[1]))
        e=max(constrained,key=lambda x:(x[0],-x[1],-x[2]))
        protected=corridor_flow(base,corridors,weights,P)
        assert (protected['value'],protected['fee'],protected['links'])==e
        assert e[:2]==expected[:2]
        counts['protected_source_lex_optima']+=1
        counts['nonempty_protected_source_sets']+=bool(P)
    counts['models']+=1
    return result


def frozen_board(nleft,nright,single=False):
    q=max(nleft,nright,6);old,bits,ranks,oldgates=family(q)
    width=2*old[1]-2;reflect=lambda p:(p[0],width-1-p[1])
    T=old[2]|set(map(reflect,old[2]))
    if single:T=T|{(3,16+2*q)}
    cur=(16,width,T,old[3]+[tuple(map(reflect,e)) for e in old[3]])
    bb={(r,c):False for r in range(0,16,2) for c in range(0,width,2)}
    bb.update(bits);bb.update({(r,width-2-c):v for (r,c),v in bits.items()})
    for t in oldgates:bb[t]=False;bb[t[0],width-2-t[1]]=False
    left=[(2,16+2*i) for i in range(nleft)]
    right=[(2,width-2-(16+2*i)) for i in range(nright)]
    for t in left+right:bb[t]=True
    rr=[[p for x in layer for p in (x,reflect(x))] for layer in ranks]
    return cur,bb,rr,left,right,q


def physical(nleft,nright,single,counts):
    cur,bits,ranks,left,right,q=frozen_board(nleft,nright,single);gates=left+right
    P={v for e in cur[3] for v in e};direct_check(*cur)
    assert len(check_rank_certificate(cur,ranks))==140 and frozen_certificate(cur)[0]==P
    assert len(cur[2])==142+4*q+int(single) and len(cur[3])==70
    for r,c in gates:
        cells={(r+i,c+j) for i,j in itertools.product(range(2),repeat=2)}
        assert not cells&P
        assert cells&cur[2] in ({(r,c+1),(r+1,c)},{(r,c),(r+1,c+1)})
    allgates=set(range(len(gates)))
    chosen=subsets(sorted(allgates)) if len(gates)<=8 else [frozenset(),frozenset(allgates),
        frozenset(range(nleft)),frozenset(range(nleft,len(gates))),
        *[frozenset(allgates-{i}) for i in allgates],*[frozenset({i}) for i in allgates]]
    first=None;rows=[];target={frozenset({(2,c),(3,c)}) for c in (16+2*q,17+2*q) if not single or c==17+2*q}
    for F in chosen:
        changed=dict(bits)
        for i,t in enumerate(gates):changed[t]=i not in F
        regs=regions(cur,changed);data,closed,_=compile_model(cur,regs);fs=forests(cur,regs)
        cells={fs[j][1] for j in data[4]};W={o:{fs[j][1] for j in S} for o,S in data[3].items()}
        own,A,B,M=owner_data(*data[:2]);aL=own[3,12];aR=own[3,cur[1]-13]
        assert (len(A),len(B),len(M))==(4,4,10)
        if first is None:first=data,closed,cells,W
        assert data[:2]==first[0][:2] and set(data[2])==set(first[0][2])
        assert [(x['body'],x['ends']) for x in closed]==[(x['body'],x['ends']) for x in first[1]]
        assert cells==first[2] and len(cells)==60+28*q-int(single)
        l=set(range(nleft))<=F;r=set(range(nleft,len(gates)))<=F
        assert W[aL]==(target if l else set()) and W[aR]==(target if r else set())
        assert all(W[o]==first[3][o] for o in W if o not in (aL,aR))
        f=fork_flow(*data);p=optimize(*data)
        expected=2+(int(l or r) if single else int(l)+int(r))
        assert (f['value'],f['cost'])==(p['value'],p['cost'])==(expected,2)
        rows.append(dict(opened=sorted(F),value=f['value'],links=f['cost']))
        counts['frozen_physical_states']+=1
    data=first[0];fs=forests(cur,regions(cur,bits))
    units=[j for j in sorted(data[4]) if fs[j][1] in target]
    assert len(units)==(1 if single else 2)
    corridor=dict(left=aL,right=aR,units=units,
                  gates=[(i,0 if i<nleft else len(units)) for i in range(len(gates))])
    results=[]
    for fees in [dict.fromkeys(allgates,1),{g:(g%3)+1 for g in allgates},dict.fromkeys(allgates,0)]:
        result=corridor_flow(data,[corridor],fees)
        lc=sum(fees[g] for g in range(nleft));rc=sum(fees[g] for g in range(nleft,len(gates)))
        assert (result['value'],result['fee'],result['links'])==((3,min(lc,rc),2) if single else (4,lc+rc,2))
        results.append(dict(weights=[fees[g] for g in sorted(fees)],**result))
        counts['physical_costed_flow_checks']+=1
    counts['frozen_boards']+=1;counts['strict_freeze_events']+=140
    return dict(nleft=nleft,nright=nright,one_unit=single,q=q,shape=list(cur[:2]),T=len(cur[2]),
                raw=len(first[2]),frozen=140,exhaustive=len(gates)<=8,states=rows,cost_profiles=results)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();counts=Counter();controls={}
    kinds,pairs,_=canonical('AA')
    # One original unit must remain one shared token, not two private credits.
    base=(kinds,pairs,[],{0:set(),1:set()},{0})
    c=dict(left=0,right=1,units=[0],gates=[(0,0),(1,1)])
    controls['one_shared_unit']=validate(base,[c],{0:1,1:3},counts)
    assert (controls['one_shared_unit']['value'],controls['one_shared_unit']['fee'])==(1,1)
    base=(kinds,pairs,[],{0:set(),1:set()},set(range(4)))
    c=dict(left=0,right=1,units=list(range(4)),gates=[(0,0),(1,2),(2,4)])
    controls['interior_gate_unnecessary']=validate(base,[c],{0:2,1:100,2:3},counts)
    assert controls['interior_gate_unnecessary']['opened']==[0,2]
    assert controls['interior_gate_unnecessary']['fee']==5
    # A beta at one end and mixed owner at the other share the source network.
    kinds,pairs,_=canonical('AAABM')
    base=(kinds,pairs,[(0,6),(2,7),(4,8)],{o:set() for o in range(5)},set(range(3)))
    c=dict(left=3,right=4,units=[0,1,2],gates=[(0,0),(1,1),(2,3)])
    controls['beta_fork_and_mixed_compete']=validate(base,[c],{0:2,1:8,2:3},counts)
    assert (controls['beta_fork_and_mixed_compete']['value'],controls['beta_fork_and_mixed_compete']['fee'])==(3,5)
    kinds,pairs,_=canonical('AAA')
    base=(kinds,pairs,[],{0:set(),1:set(),2:{0}},set(range(3)))
    c=dict(left=0,right=1,units=[0,1,2],gates=[])
    original=optimize(*apply(base,[c],set()))
    wrong=optimize(*apply(base,[c],set(),True))
    assert (original['value'],wrong['value'])==(3,2)
    controls['unguarded_outside_owner']=dict(original_value=3,unguarded_privatized_value=2,
        reason='Outside alpha uses left extreme; endpoint must keep access to an interior unit.')
    counts['unguarded_rule_counterexamples']+=1
    rng=random.Random(2026102602)
    for index in range(90):
        types='AA'+''.join(rng.choice('ABM') for _ in range(rng.randrange(1,5)))
        kinds,pairs,possible=canonical(types);rng.shuffle(possible)
        links=possible[:rng.randrange(min(9,len(possible))+1)]
        nfree=rng.randrange(3);nextunit=nfree;corridors=[];weights={}
        for _ in range(rng.randrange(1,4)):
            m=rng.randrange(5);units=list(range(nextunit,nextunit+m));nextunit+=m
            gates=[]
            for _ in range(rng.randrange(min(3,5-len(weights))+1)):
                g=len(weights);weights[g]=rng.randrange(5);gates.append((g,rng.randrange(m+1)))
            endpoints=[rng.choice([None]+list(range(len(pairs)))) for _ in range(2)]
            corridors.append(dict(left=endpoints[0],right=endpoints[1],units=units,gates=gates))
        support={o:{j for j in range(nfree) if rng.randrange(2)} for o in range(len(pairs))}
        validate((kinds,pairs,links,support,set(range(nextunit))),corridors,weights,counts)
    boards=[physical(l,r,single,counts) for l,r in [(1,1),(1,3),(2,2),(3,3),(4,4),(7,1),(1,7),(16,17),(32,19)] for single in (False,True)]
    report=dict(status='PASS',counts=dict(counts),controls=controls,physical=boards,
        scope='Extreme resource support privatization for each tested gate state; scalar lex mincost full fork flow versus independently enumerated operations and primitive packing; source protection; all-length physical family construction checks.',
        limits='General proofs are in the note; enumeration is validation. Protected support-only corridor contract required. No arbitrary branched/shared-gate topology claim, no universal 5/6 improvement, no end-to-end Lean claim.')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(counts),indent=2));print('PASS: protected linear corridors')


if __name__=='__main__':main()
