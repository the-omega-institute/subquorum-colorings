"""Independent physical controls for persistent private original intervals.

General proofs and exact private-source elimination are in
PROTECTED_SINGLETON_RESERVES.md. No solver is used. Random additions test
monotone feasible extensions, which need not be completely frozen.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_cooperative_promotion import neighbors
from check_compensation_flow_normal_form import owner_data
from check_frozen_beta_fork_escape import fixture
from check_frozen_tip_slot_obstruction import independent_strands
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_whole_support_fork_normal_form import whole_support_data,canonical,optimize,ordinary_flow
from check_whole_support_fork_flow import fork_flow

if not __debug__:
    raise RuntimeError('Assertions required; run without -O.')


def protected(current):
    """Scan actual T/P, matching guards, original cycle and interval identities."""
    direct_check(*current)
    P={v for e in current[3] for v in e}
    kinds,bodies=independent_strands(current,whole_bands(current))
    body_of={v:i for i,(_,body) in enumerate(bodies) for v in body}
    data,meta,_=whole_support_data(current,whole_bands(current))
    owner,alphas,_,_=owner_data(*data[:2])
    intervals={(x['band'],x['first'],x['last']):j for j,x in enumerate(meta['intervals'])}
    result=[]
    for a in sorted(kinds):
        if kinds[a]!='TP' or owner[a] not in alphas:continue
        r,ac=a;partner=r^1;out=r-1 if r%2==0 else r+1
        for s in (-1,1):
            c=ac-s;u=(r,c);v=(partner,c);x=(r,c-s);y=(partner,c-s);h=(out,c)
            if u in current[2]|P or v in current[2]|P:continue
            if not {x,y,h}<=P:continue
            cycle=bodies[body_of[x]]
            if cycle[0] or y not in cycle[1]:continue
            key=(r//2,c,c);j=intervals.get(key)
            if j not in data[4]:continue
            users={o for o,w in data[3].items() if j in w}
            assert users=={owner[a]}
            result.append(dict(alpha_tip=a,alpha_body=sorted(bodies[body_of[a]][1]),
                alpha_owner=owner[a],interval=key,blank=(u,v),
                fixed_guards=(a,x,h),selected_guard=(partner,ac),cycle_body=sorted(cycle[1])))
    return result,data


def remove_private(data,chosen):
    kinds,pairs,links,support,resources=data
    removed=set(chosen);units=set(chosen.values())
    assert len(units)==len(removed)
    for a,j in chosen.items():
        assert kinds[pairs[a][0]]==kinds[pairs[a][1]]=='TP'
        assert {o for o,w in support.items() if j in w}=={a}
    kept=[o for o in range(len(pairs)) if o not in removed]
    free={v for o in kept for v in pairs[o]}
    return ({v:kinds[v] for v in free},[pairs[o] for o in kept],
        [e for e in links if set(e)<=free],
        {i:support[o]-units for i,o in enumerate(kept)},resources-units)


def exact_elimination(data,chosen,totals,independent=False):
    residual=remove_private(data,chosen);q=len(chosen)
    for solver in (ordinary_flow,fork_flow):
        full=solver(*data);rest=solver(*residual)
        assert (full['value'],full['cost'])==(q+rest['value'],rest['cost'])
        totals['value_and_minimum_link_comparisons']+=1
    if independent:
        full=optimize(*data);rest=optimize(*residual)
        assert (full['value'],full['cost'])==(q+rest['value'],rest['cost'])
        totals['independent_primitive_pack_comparisons']+=1
    return residual


def physical_controls(totals):
    records=[]
    for q,padding,plug in itertools.product(range(1,13),(0,2,10),(False,True)):
        current,_=fixture(q,padding,plug);claims,data=protected(current)
        critical={tuple(c['alpha_tip']):c for c in claims}
        chosen={}
        meta=whole_support_data(current,whole_bands(current))[1]
        units={(x['band'],x['first'],x['last']):j for j,x in enumerate(meta['intervals'])}
        for i in range(q):
            claim=critical[8+12*i,11]
            assert claim['interval']==(4+6*i,10,10)
            chosen[claim['alpha_owner']]=units[claim['interval']]
        assert len(chosen)==q
        exact_elimination(data,chosen,totals,independent=q<=3)
        totals['frozen_copy_padding_boards']+=1
        assert len(frozen_certificate(current)[0])==2*len(current[3])
        records.append(dict(copies=q,padding=padding,plug=plug,private_units=q,
            payment=q,minimum_links=0))
    return records



def pinned_family(q):
    base,layers=fixture(q,0,True)
    current=(*base[:2],base[2]|{(4+12*i,12) for i in range(q)},base[3])
    return current,layers


def reservation_profile(totals):
    records=[]
    for q in range(1,13):
        current,_=pinned_family(q)
        claims,data=protected(current)
        direct_check(*current)
        assert len(frozen_certificate(current)[0])==52*q
        assert len(current[2])==20*q and len(data[4])==26*q
        owner,alphas,betas,mixed=owner_data(*data[:2])
        assert (len(alphas),len(betas),len(mixed))==(q,q,2*q)
        private={a:next(iter(data[3][a])) for a in alphas}
        assert all(len(data[3][a])==1 for a in alphas)
        assert len(set(private.values()))==q
        exact_elimination(data,private,totals,independent=q<=3)
        # All subsets through eight copies; representative cardinalities for
        # larger q. The arbitrary-subset formula has a separate written proof.
        subsets=range(1<<q) if q<=8 else [0]+[(1<<r)-1 for r in range(1,q+1)]
        for mask in subsets:
            chosen=[a for i,a in enumerate(sorted(alphas)) if mask>>i&1]
            reserved={private[a] for a in chosen}
            resources=data[4]-reserved
            restricted=(*data[:3],{o:w-reserved for o,w in data[3].items()},resources)
            for solver in (ordinary_flow,fork_flow):
                answer=solver(*restricted)
                assert (answer['value'],answer['cost'])==(q,len(chosen))
                totals['physical_reservation_solver_comparisons']+=1
            if q<=3:
                answer=optimize(*restricted)
                assert (answer['value'],answer['cost'])==(q,len(chosen))
                totals['independent_physical_reservation_packs']+=1
            totals['physical_reservation_subsets']+=1
        totals['pinned_unique_support_boards']+=1
        records.append(dict(copies=q,selected=20*q,endpoints=52*q,
            original_resources=26*q,private_units=q,alpha_support_size=1,
            all_reservations_checked=q<=8))
    return records


def extensions(totals):
    rng=random.Random(20261025)
    summaries=[]
    for case in range(160):
        q=1+case%3;plug=bool(case%2);base,_=fixture(q,2*(case%3),plug)
        # Larger blank collars permit additional paths and components. Keep
        # original coordinates and aligned bands fixed.
        old=(*((base[0]+4,base[1]+4)),base[2],base[3])
        claims,_=protected(old)
        chosen=[x for x in claims if tuple(x['alpha_tip']) in {(8+12*i,11) for i in range(q)}]
        assert len(chosen)==q
        cur=(old[0],old[1],set(old[2]),list(old[3]));attempts=accepted=0
        sites=list(itertools.product(range(cur[0]),range(1,cur[1]-1)));rng.shuffle(sites)
        for v in sites[:110]:
            P={v for e in cur[3] for v in e};occupied=P|cur[2]
            if v in occupied:continue
            candidates=[None]+[w for w in neighbors(v) if w in sites and w not in occupied]
            rng.shuffle(candidates)
            for w in candidates:
                attempts+=1
                nxt=(cur[0],cur[1],cur[2]|({v} if w is None else set()),
                     cur[3]+([] if w is None else [(v,w)]))
                try:direct_check(*nxt)
                except AssertionError:continue
                cur=nxt;accepted+=1;break
        newclaims,data=protected(cur)
        by_tip={tuple(x['alpha_tip']):x for x in newclaims}
        meta=whole_support_data(cur,whole_bands(cur))[1]
        units={(x['band'],x['first'],x['last']):j for j,x in enumerate(meta['intervals'])}
        private={}
        for c in chosen:
            n=by_tip[tuple(c['alpha_tip'])]
            assert c['alpha_body']==n['alpha_body']
            assert c['cycle_body']==n['cycle_body']
            assert c['interval']==n['interval']
            private[n['alpha_owner']]=units[n['interval']]
        exact_elimination(data,private,totals)
        totals['feasible_monotone_extensions']+=1
        totals['accepted_additions']+=accepted
        totals['protected_source_extension_checks']+=q
        summaries.append(dict(case=case,copies=q,accepted_additions=accepted,
            protected_sources=q,total_alphas=len(owner_data(*data[:2])[1])))
    return summaries


def abstract_controls(totals):
    # All terminal links and all one-external-resource supports on these
    # three-owner types, with an additional truly private source resource.
    for types in ('AAB','AAM','ABB','AMM'):
        kinds,pairs,possible=canonical(types)
        for mask in range(1<<len(possible)):
            links=[e for i,e in enumerate(possible) if mask>>i&1]
            for access in range(1<<len(pairs)):
                support={o:({0} if access>>o&1 else set()) for o in range(len(pairs))}
                support[0].add(1)
                data=kinds,pairs,links,support,{0,1}
                exact_elimination(data,{0:1},totals,True)
                # Reserve the external unit: the private one is not reserved.
                restricted=(*data[:3],{o:w-{0} for o,w in support.items()},{1})
                exact_elimination(restricted,{0:1},totals,True)
                totals['exhaustive_abstract_models']+=2
    rng=random.Random(20261026)
    for case in range(240):
        types='AAA'+''.join(rng.choice('BM') for _ in range(1+case%3))
        kinds,pairs,possible=canonical(types);rng.shuffle(possible)
        links=possible[:min(10,rng.randrange(len(possible)+1))]
        support={o:{j for j in range(2) if rng.randrange(2)} for o in range(len(pairs))}
        q=1+case%3;private={a:2+a for a in range(q)}
        for a,j in private.items():support[a].add(j)
        exact_elimination((kinds,pairs,links,support,{0,1}|set(private.values())),private,totals,True)
        totals['seeded_abstract_models']+=1
    # Privacy is essential: two sources with the SAME sole interval pay one.
    kinds,pairs,_=canonical('AA')
    data=kinds,pairs,[],{0:{0},1:{0}},{0}
    assert fork_flow(*data)['value']==1
    totals['shared_unit_negative_controls']+=1


def rematching_negative(totals):
    base,_=fixture(plug=True)
    # Alternating augmentation from the protected upper blank to another
    # previously blank vertex, changing three fixed old actual edges.
    path=[(8,10),(7,10),(6,10),(5,10),(5,9),(4,9),(4,8),(3,8)]
    remove={frozenset(path[i:i+2]) for i in range(1,len(path)-1,2)}
    assert remove<={frozenset(e) for e in base[3]}
    new=[e for e in base[3] if frozenset(e) not in remove]
    new += [tuple(path[i:i+2]) for i in range(0,len(path),2)]
    extended=(*base[:3],new);direct_check(*extended)
    oldP={v for e in base[3] for v in e};newP={v for e in new for v in e}
    assert oldP<newP and newP-oldP=={path[0],path[-1]}
    assert (8,10) in newP
    frozen,_=frozen_certificate(extended)
    assert len(frozen)==32 and len(newP)==54
    totals['fixed_matching_hypothesis_negative_controls']+=1
    return dict(path=path,old_matching_edges_removed=[sorted(e) for e in sorted(remove,key=lambda x:sorted(x))],
        added_endpoints=sorted(newP-oldP),frozen_endpoints=len(frozen),total_endpoints=len(newP),
        scope='Feasible extension retaining old T and P but changing old mates fills the protected gap. '
              'This extension is not completely frozen; it refutes dropping fixed old mates '
              'from the feasible-extension lemma, not its frozen-only strengthening or the grid bound.')


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    totals=Counter();physical=physical_controls(totals);profiles=reservation_profile(totals);extension=extensions(totals)
    abstract_controls(totals);negative=rematching_negative(totals)
    report=dict(status='PASS',totals=dict(totals),physical=physical,pinned_profiles=profiles,extensions=extension,
        rematching_negative=negative,
        scope='General local locking and persistent private-resource proofs; exact private-source '
              'elimination in ordinary/full whole-support flow, including minimum links. '
              'No automatic protected reserve at every fork, no arbitrary-rematching persistence, '
              'no universal compensation or 5/6 improvement.')
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__=='__main__':main()
