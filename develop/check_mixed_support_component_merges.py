"""Exact reserve accounting for monotone whole-support incidence extensions.

The general proof is in MIXED_SUPPORT_COMPONENT_MERGE_ACCOUNTING.md.
Physical mixed links are replayed with stable alpha and original interval IDs.
"""
import argparse
from collections import Counter,defaultdict
import itertools
import json
from pathlib import Path
import random

from check_beta_closing_and_mixed_repair import closed
from check_frozen_first_destination_allocation import fixture as unported
from check_frozen_shared_mixed_gate import fixture as shared
from check_frozen_support_tree_reroot import fixture,model_at
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_joint_tree_beta_compensation import all_assignments
from check_one_sided_interval_allocation import allocate,independent_maximum
from check_shared_donor_collision_after_mixed_relays import collision_family
from check_promotion_cores import frozen_certificate
from check_even_bridge_support_completion import endpoints_of
from check_residual_corridors import direct_check
from check_terminal_cancellation_and_stranded_demand import (
    all_link_matchings,cancel_pairs,terminal_data,extended_ports)

if not __debug__:
    raise RuntimeError('Run without -O; assertions are required.')


def components(k,incidence):
    adjacency=defaultdict(set)
    for users in incidence.values():
        if len(users)==2:
            a,b=users;adjacency[a].add(b);adjacency[b].add(a)
    remaining=set(range(k));out=[]
    while remaining:
        root=min(remaining);seen={root};pending=[root]
        while pending:
            a=pending.pop()
            for b in adjacency[a]-seen:seen.add(b);pending.append(b)
        remaining-=seen
        units={j for j,users in incidence.items() if users & seen}
        assert len(units)>=len(seen)-1
        out.append(dict(owners=seen,units=units,slack=len(units)-len(seen)))
    return out


def augment_preserving(k,incidence,baseline):
    """Extend a maximum old matching; each augmentation retains used units."""
    assignment=dict(baseline);inverse={j:a for a,j in assignment.items()}
    def augment(a,seen):
        for j,users in incidence.items():
            if a not in users or j in seen:continue
            seen.add(j)
            if j not in inverse or augment(inverse[j],seen):
                inverse[j]=a;assignment[a]=j;return True
        return False
    for a in range(k):
        if a not in assignment:augment(a,set())
    assert len(set(assignment.values()))==len(assignment)
    assert set(baseline)<=set(assignment)
    assert set(baseline.values())<=set(assignment.values())
    assert all(a in incidence[j] for a,j in assignment.items())
    return assignment


def verify(k,old,new,totals,baseline=None):
    assert set(old)==set(new)
    assert all(old[j]<=new[j]<=set(range(k)) and len(new[j])<=2 for j in old)
    before,after=allocate(k,old),allocate(k,new)
    baseline=before['assignment'] if baseline is None else baseline
    assert len(baseline)==k-len(before['deficient'])
    assert len(set(baseline.values()))==len(baseline)
    assert all(a in old[j] for a,j in baseline.items())
    groups=components(k,old);post=components(k,new)
    rows=[];gain=0
    for cluster in post:
        old_groups=[g for g in groups if g['owners'] & cluster['owners']]
        assert all(g['owners']<=cluster['owners'] for g in old_groups)
        assert set().union(*(g['owners'] for g in old_groups))==cluster['owners']
        activated={j for j in cluster['units'] if not old[j]}
        d=sum(g['slack']==-1 for g in old_groups)
        s=sum(max(0,g['slack']) for g in old_groups)+len(activated)
        assert cluster['slack']==s-d and d<=s+1
        remaining=int(d==s+1)
        assert remaining==int(cluster['slack']==-1)
        assert d-remaining==min(d,s)
        # Count OLD UNUSED resources in the cluster, not new access arcs.
        unused=cluster['units']-set(baseline.values())
        assert len(unused)==s
        gain+=min(d,s)
        rows.append(dict(old_components=len(old_groups),old_deficient=d,old_unused=s,
                         activated_loose=len(activated),post_defect=remaining,
                         payment_gain=min(d,s),owners=sorted(cluster['owners'])))
        totals['post_component_identities']+=1
        totals['multiple_deficient_merge_controls']+=d>=2
        totals['shared_reserve_loss_controls']+=d>=2 and s<d
        totals['tight_paid_component_transfer_controls']+=d>0 and s==0 and len(old_groups)>d
    assert gain==len(after['assignment'])-len(before['assignment'])
    assert len(before['deficient'])-len(after['deficient'])==gain
    extended=augment_preserving(k,new,baseline)
    assert len(extended)==len(after['assignment'])==independent_maximum(k,new)
    assert len(set(extended.values())-set(baseline.values()))==gain
    assert len(after['spare_resources'])==len(before['spare_resources'])-gain
    totals['monotone_extension_models']+=1
    totals['positive_payment_gain_models']+=gain>0
    return dict(gain=gain,old_defect=len(before['deficient']),new_defect=len(after['deficient']),
                clusters=rows,extended=extended)


def physical(current,bands,fixed,totals):
    data,meta,before,old,_,_=model_at(current,bands)
    kinds=data[0]
    after_data,after_meta,after,new,_,_=model_at(current,bands,fixed)
    assert before['alpha']==after['alpha'] and before['beta']==after['beta']
    assert meta['intervals']==after_meta['intervals'] and meta['boundary']==after_meta['boundary']
    old_owner={v:a for a,pair in enumerate(old['alphas']) for v in pair}
    stable={}
    for record in new['records']:
        if record['cycle']:continue
        pair=set(record['ends'])
        final=next((i for i,p in enumerate(new['alphas']) if set(p)==pair),None)
        if final is not None:
            sources={old_owner[v] for v in record['vertices'] if v in old_owner}
            assert len(sources)==1
            stable[final]=next(iter(sources))
    assert set(stable.values())==set(range(before['alpha']))
    incidence={j:{stable[a] for a in users} for j,users in new['incidence'].items()}
    result=verify(before['alpha'],old['incidence'],incidence,totals)
    totals['physical_whole_support_nonsingleton_merge_clusters']+=sum(
        r['old_components']>1 for r in result['clusters'])
    assert result['gain']==after['paid']-before['paid']
    assert before['margin']==after['margin']
    totals['physical_mixed_batch_controls']+=1
    return dict(shape=current[:2],links=fixed,**{k:v for k,v in result.items() if k!='extended'})


def terminal_collision(width,totals):
    """Reuse the archived physical donor collision, with explicit access scope.

    The whole-support graph of this example already pays both alphas. These
    nontrivial merges belong to its monotone TERMINAL/CAP incidence model.
    """
    current,bands=collision_family(width)
    direct_check(*current)
    assert frozen_certificate(current)[0]==endpoints_of(current)
    original,labels,intervals,owner,kinds,pairs,ports=terminal_data(current,bands)
    access=extended_ports(current,bands,labels,intervals,owner,kinds,ports,Counter())
    marked={owner[b,c] for b in range(len(bands)) for c in (0,len(bands[b])-1)}
    resources=set(range(len(intervals)))-marked
    stable={(width+4,5):0,(width+4,15):1}
    first=[((5,5),(5,6))]
    left=((5,7),(5,8));right=((5,15),(5,14))
    states={}
    for name,extra in [('initial',[]),('left',[left]),('right',[right]),('both',[left,right])]:
        reduced,_,_=cancel_pairs(kinds,pairs,first+extra,Counter())
        incidence={j:set() for j in resources}
        for pair in reduced:
            if all(kinds[v]=='TP' for v in pair):
                source={stable[v] for v in pair if v in stable}
                assert len(source)==1;a=next(iter(source))
                for v in pair:
                    for port in access[v]:
                        j=owner[port]
                        if j in incidence:incidence[j].add(a)
        states[name]=incidence
    examples=[]
    for before,after in [('initial','left'),('initial','right'),('initial','both'),
                         ('left','both'),('right','both')]:
        record=verify(2,states[before],states[after],totals)
        if before=='initial' and after=='both':
            assert record['gain']==1 and record['new_defect']==1
            assert any(r['old_deficient']==2 and r['old_unused']==1 for r in record['clusters'])
        if before in ('left','right'):
            assert record['gain']==0
            assert any(r['old_components']==2 and r['old_deficient']==1 and r['old_unused']==0
                       for r in record['clusters'])
        totals['physical_terminal_cap_merge_transitions']+=1
        if width==8:examples.append(dict(kind='archived-physical-terminal-cap',width=width,
            before=before,after=after,**record))
    return examples


def abstract(totals):
    # Exhaust all old<=new owner sets on three original units for k<=3.
    for k in range(1,4):
        users=[set(x) for n in range(min(k,2)+1) for x in itertools.combinations(range(k),n)]
        choices=[(a,b) for a in users for b in users if a<=b]
        for record in itertools.product(choices,repeat=3):
            old={i:a for i,(a,b) in enumerate(record)}
            new={i:b for i,(a,b) in enumerate(record)}
            verify(k,old,new,totals)
            if k<=2:
                canonical=allocate(k,old)['assignment']
                for baseline in all_assignments(k,old):
                    if len(baseline)==len(canonical) and baseline!=canonical:
                        verify(k,old,new,totals,baseline)
                        totals['noncanonical_maximum_baseline_controls']+=1
    rng=random.Random(20261025)
    for _ in range(1200):
        k=rng.randint(2,16);old={};new={}
        for j in range(rng.randint(0,2*k)):
            target=set(rng.sample(range(k),rng.randint(0,2)))
            new[j]=target;old[j]={a for a in target if rng.randrange(2)}
        verify(k,old,new,totals)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();totals=Counter();examples=[]
    # Explicit independent accounting controls: one loose unit cannot pay two
    # old deficits; a tight paid component has NO spare merely because reached.
    controls=[(2,{0:set()},{0:{0,1}}),
              (2,{0:{1}},{0:{0,1}}),
              (2,{0:{1},1:{1}},{0:{0,1},1:{1}})]
    for k,old,new in controls:examples.append(dict(kind='abstract',old={j:sorted(u) for j,u in old.items()},
        new={j:sorted(u) for j,u in new.items()},**verify(k,old,new,totals)))
    abstract(totals)
    models=[fixture()[0],closed(1)[0],unported()[0],shared()]
    for current in models:
        direct_check(*current)
        assert frozen_certificate(current)[0]==endpoints_of(current)
        bands=whole_bands(current)
        data,_,before,model,_,_=model_at(current,bands)
        kinds,pairs,links,_,_=data
        beta_tips={v for p in pairs if all(kinds[v]=='BP' for v in p) for v in p}
        allowed=[link for link in links if link[1] not in beta_tips]
        for fixed in all_link_matchings(allowed):
            record=physical(current,bands,fixed,totals)
            if any(r['old_deficient']>=2 or (r['old_deficient'] and r['old_components']>r['old_deficient'])
                   for r in record['clusters']):
                if len(examples)<12:examples.append(dict(kind='physical',**record))
    for width in range(8,41,2):examples.extend(terminal_collision(width,totals))
    receipt=dict(status='PASS',totals=dict(totals),examples=examples,
        scope='All finite monotone incidence extensions with <=2 owners per original unit: '
              'post-component gain=min(oldDeficientTrees,oldUnusedOriginalUnitsInCluster); '
              'maximum old paid-owner set and used-unit set can be preserved by augmentation. '
              'Physical legal mixed-only batches checked with stable alpha IDs; '
              'archived terminal-cap collision supplies nontrivial merge controls, '
              'while these whole-support batches have no cross-component merges. '
              'Written general proof, not enumeration, establishes the theorem; counting '
              'whole-support access is not asserted to equal terminal route access.')
    args.output.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__=='__main__':main()
