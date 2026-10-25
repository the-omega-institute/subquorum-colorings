"""Forced PP guards of short alpha--beta--alpha motifs, and closed blocks.

General proofs: FORCED_POCKET_GUARDS_AND_CYCLE_ELIMINATION.md.
No solver discovery is imported. Original strand/resource identities persist.
"""
import argparse
from collections import Counter,defaultdict
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_cooperative_promotion import neighbors,occupied_degrees
from check_frozen_beta_support_fork import fixture as fork_fixture,stacked
from check_frozen_beta_support_fork import restrict
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_frozen_tip_slot_obstruction import independent_strands
from check_guarded_pocket_fork_replacement import EDGE,extend
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_neutral_portal_strip_compensation import image_map
from check_one_sided_interval_allocation import allocate
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check,transformed
from check_shared_pocket_completion import fixture as loose_fixture
from check_tight_shared_pocket import fixture as tight_fixture
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import canonical,evaluate,optimize,ordinary_flow,whole_support_data

if not __debug__:
    raise RuntimeError('Run without -O; assertions required.')


def closed_dependency(current,vertices):
    P={v for e in current[3] for v in e};mate={v:w for e in current[3] for v,w in (e,e[::-1])}
    assert vertices<=P and vertices
    for v in vertices:
        nonmate=set(neighbors(v))&(current[2]|P)-{mate[v]}
        outside={w for w in nonmate if w in current[2] or mate[w] not in vertices}
        assert len(outside)<=1


def inspect_geometry(current,bands,totals):
    direct_check(*current);P={v for edge in current[3] for v in edge}
    frozen,layers=frozen_certificate(current);assert frozen==P
    rank={tuple(w['endpoint']):i for i,layer in enumerate(layers) for w in layer}
    mate={v:w for edge in current[3] for v,w in (edge,edge[::-1])}
    data,_,_=whole_support_data(current,bands);owner,aa,bb,_=owner_data(*data[:2])
    kinds,components=independent_strands(current,bands)
    assert kinds==data[0] and {tips for tips,body in components if tips}=={frozenset(pair) for pair in data[1]}
    body={frozenset(tips):vertices for tips,vertices in components if tips}
    location={v:(i,c,p) for i,band in enumerate(bands) for c,column in enumerate(band) for p,v in enumerate(column)}
    partner={a:b for band in bands for col in band for a,b in (col,col[::-1])}
    motifs=[]
    for beta in sorted(bb):
        if len(body[frozenset(data[1][beta])])!=2:continue
        u,v=sorted(data[1][beta],key=lambda w:location[w][1])
        band,c,pos=location[u]
        if location[v]!=(band,c+1,pos) or c==0 or c+2>=len(bands[band]):continue
        a,b=bands[band][c-1][pos],bands[band][c+2][pos]
        if a not in owner or b not in owner or owner[a] not in aa or owner[b] not in aa:continue
        assert kinds[a]==kinds[b]=='TP'
        dr,dc=u[0]-partner[u][0],u[1]-partner[u][1]
        add=lambda p,n:(p[0]+n*dr,p[1]+n*dc)
        h,k,hp,kp=add(u,1),add(v,1),add(u,2),add(v,2)
        ap,bp=add(a,1),add(b,1)
        assert mate[u]==v and mate[v]==u
        assert mate[a]==ap and mate[b]==bp
        assert partner[ap] in current[2]|P and partner[bp] in current[2]|P
        assert h in P and k in P and hp in P and kp in P
        assert partner[h]==hp and partner[k]==kp
        # These are forced retained neighbors, not merely occupied sites.
        assert rank[mate[h]]<rank[u] and rank[mate[k]]<rank[v]
        assert not data[3][beta]
        incoming=[edge for edge in data[2] if owner[edge[1]]==beta]
        assert set(incoming)=={(a,u),(b,v)}
        motifs.append(dict(beta=beta,ends=(owner[a],owner[b]),edge=(u,v),
            boundary_tips=(a,b),guards=(h,k),guard_partners=(hp,kp)))
        totals['forced_guard_motifs']+=1
    totals['frozen_physical_boards']+=1
    return data,motifs


def blocks(data,motifs):
    _,aa,_,_=owner_data(*data[:2]);adj=defaultdict(list)
    for m in motifs:
        a,b=m['ends'];adj[a].append((b,m['beta']));adj[b].append((a,m['beta']))
    remaining=set(aa);answer=[]
    while remaining:
        vertices={min(remaining)};todo=list(vertices)
        while todo:
            for v,beta in adj[todo.pop()]:
                if v not in vertices:vertices.add(v);todo.append(v)
        remaining-=vertices;units={beta for a in vertices for b,beta in adj[a]}
        answer.append((vertices,units))
    return answer


def eliminate(data,motifs,totals,independent=False,cost_exact=True):
    owner,aa,_,_=owner_data(*data[:2]);chosen=[]
    for sources,units in blocks(data,motifs):
        if len(units)>=len(sources) and (not cost_exact or all(not data[3][a] for a in sources)):
            chosen.append((sources,units))
    removed=set().union(*(s for s,b in chosen)) if chosen else set()
    beta_removed=set().union(*(b for s,b in chosen)) if chosen else set()
    local_index={a:i for i,a in enumerate(sorted(removed))}
    incidence={m['beta']:{local_index[a] for a in m['ends']} for m in motifs if m['beta'] in beta_removed}
    local=allocate(len(removed),incidence)['assignment']
    assert set(local)==set(range(len(removed)))
    chosen_links=[next(e for e in data[2] if owner[e[0]]==a and owner[e[1]]==local[local_index[a]])
                  for a in sorted(removed)]
    assert len({owner[v] for u,v in chosen_links})==len(removed)
    residual=restrict(data,set(range(len(data[1])))-removed-beta_removed,data[4])
    for solver in (ordinary_flow,fork_flow):
        old=solver(*data);after=solver(*residual)
        assert old['value']==len(removed)+after['value']
        assert after['cost']<=old['cost']<=len(removed)+after['cost']
        if cost_exact:assert old['cost']==len(removed)+after['cost']
        links=chosen_links+after['links']
        assert len({u for u,v in links})==len(links)==len({v for u,v in links})
        assert evaluate(*data[:2],links,*data[3:])['value']==old['value']
        assert len(links)==len(removed)+after['cost']
        totals['full_residual_value_cost_comparisons']+=1
        totals['actual_link_lifts']+=1
    if independent:
        old,after=optimize(*data),optimize(*residual)
        assert old['value']==len(removed)+after['value']
        assert after['cost']<=old['cost']<=len(removed)+after['cost']
        if cost_exact:assert old['cost']==len(removed)+after['cost']
        totals['independent_primitive_pack_comparisons']+=1
    totals['systems']+=1;totals['nonempty_eliminations']+=bool(removed)
    totals['cardinality_only_systems']+=not cost_exact
    totals['eliminated_sources']+=len(removed);totals['eliminated_internal_betas']+=len(beta_removed)
    return dict(sources_removed=len(removed),internal_betas_removed=len(beta_removed),
        scalar_excess=len(beta_removed)-len(removed),value=old['value'],cost=old['cost'])


def abstract_checks(totals):
    rng=random.Random(2026102503)
    for i in range(400):
        n=rng.randrange(1,7);p=rng.randrange(3);edges=[]
        for v in range(1,n):edges.append((v,rng.randrange(v)))
        edges += [(rng.randrange(n),rng.randrange(n)) for _ in range(rng.randrange(1,4))]
        nb=len(edges);ne=rng.randrange(3);nm=rng.randrange(3)
        kinds,pairs,_=canonical('A'*(n+p)+'B'*(nb+ne)+'M'*nm)
        owner,aa,bb,mm=owner_data(kinds,pairs);local=set(range(n+p,n+p+nb));links=[];motifs=[]
        for e,(a,b) in enumerate(edges):
            beta=n+p+e;links += [(2*a,2*beta),(2*b+1,2*beta+1)]
            motifs.append(dict(beta=beta,ends=(a,b)))
        for u in kinds:
            if kinds[u]!='TP':continue
            for v in kinds:
                if kinds[v]=='BP' and owner[v] not in local and rng.random()<.14:links.append((u,v))
        resources=set(range(rng.randrange(5)));support={o:set() for o in range(len(pairs))}
        for o in support:
            if o not in local and o>=n:support[o]={j for j in resources if rng.random()<.4}
        data=kinds,pairs,links,support,resources
        result=eliminate(data,motifs,totals,independent=len(pairs)<=10)
        assert result['sources_removed']==n and result['internal_betas_removed']==nb
        if i%4==0 and resources:
            changed={o:set(w) for o,w in support.items()};changed[rng.randrange(n)]=set(resources)
            eliminate((*data[:3],changed,resources),motifs,totals,
                independent=len(pairs)<=10,cost_exact=False)
    # The unsupported-source condition is necessary for the cost equality.
    k,p,_=canonical('AB');data=(k,p,[(0,2),(1,3)],{0:{0},1:set()},{0})
    original=fork_flow(*data)
    assert (original['value'],original['cost'])==(1,0)
    assert original['cost']!=1
    eliminate(data,[dict(beta=1,ends=(0,0))],totals,True,cost_exact=False)
    return dict(supported_loop=dict(value=1,cost=0,invalid_unconditional_cost=1))


def nonfrozen_control(totals):
    T={(0,1),(0,4),(3,1),(3,4)}
    M=[((1,1),(2,1)),((1,4),(2,4)),((1,2),(1,3)),((2,2),(2,3))]
    current=4,6,T,M;direct_check(*current)
    assert min(occupied_degrees(current).values())==3
    assert not frozen_certificate(current)[0]
    closed_dependency(current,{(2,3),(1,2)})
    closed_dependency(current,{(2,2),(1,3)})
    totals['nonfrozen_degree_three_controls']+=1
    return dict(shape=current[:2],selected=sorted(T),matching=M,
        closed_pairs=[[(2,3),(1,2)],[(2,2),(1,3)]],frozen_endpoints=0)


def physical_checks(totals):
    records=[]
    for q in range(1,13):
        masks=range(1<<q) if q<=4 else [0]+[(1<<s)-1 for s in range(1,q+1)]
        for mask in masks:
            filled={i for i in range(q) if mask>>i&1}
            for name in ('parallel_cycle','loop'):
                if name=='parallel_cycle':current,layers=tight_fixture(q,filled);check_rank_certificate(current,layers)
                else:
                    current=stacked(q)
                    current=(*current[:3],current[3]+[tuple((r+16*i,c) for r,c in EDGE) for i in sorted(filled)])
                data,motifs=inspect_geometry(current,whole_bands(current),totals)
                result=eliminate(data,motifs,totals,independent=q<=2)
                assert result['sources_removed']==len(filled)*(2 if name=='parallel_cycle' else 1)
                records.append(dict(family=name,copies=q,filled=sorted(filled),**result))
    for i in range(40):
        current,_=extend(2026102503+i,True)
        data,motifs=inspect_geometry(current,whole_bands(current),totals)
        result=eliminate(data,motifs,totals,True)
        assert result['sources_removed']>=1
        totals['monotone_frozen_extension_controls']+=1
    for fixture in (tight_fixture,loose_fixture):
        current,_=fixture(1,{0})
        for sym in itertools.product((False,True),repeat=3):
            move=image_map(*current[:2],sym);shape,T,M=transformed(*current,*sym)
            carried=[[tuple(map(move,col)) for col in band] for band in whole_bands(current)]
            data,motifs=inspect_geometry((*shape,T,M),carried,totals)
            eliminate(data,motifs,totals,True);totals['carried_band_isometries']+=1
    return records


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    totals=Counter();hypotheses=abstract_checks(totals);negative=nonfrozen_control(totals)
    physical=physical_checks(totals)
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),physical=physical,
        hypothesis_controls=hypotheses,nonfrozen_geometry_control=negative,
        scope='General forced PP guards for horizontal two-endpoint beta between alpha TP tips; '
        'exact full-network unsupported cyclic-component elimination, source and beta identities once. '
        'Pure-cycle PP/M components are not beta resources. Universal compensation and5/6 remain open.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__=='__main__':main()
