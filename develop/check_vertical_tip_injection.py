"""Geometric certificates: all missing vertically mated TP tips, not just alpha.

Written proof: VERTICAL_TP_INJECTION_AND_SHORT_MIXED_HOLES.md.
Original interval identities and full exterior capacities are retained.
"""
import argparse
from collections import Counter,defaultdict
import itertools
import json
from pathlib import Path

from check_compensation_flow_normal_form import owner_data
from check_cooperative_promotion import occupied_degrees
from check_frozen_missing_port_bp_injection import nonfrozen_obstruction
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_frozen_tip_slot_obstruction import fixture as slot_fixture,matching
from check_frozen_beta_support_fork import fixture as fork_fixture
from check_interval_connector_cycles_and_missing_ports import stack,whole_bands
from check_neutral_portal_strip_compensation import image_map
from check_paired_hole_certificates import exact_check,paired_fixture
from check_partial_tip_compensation import interaction_components
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check,transformed
from check_shared_pocket_completion import fixture as loose_fixture
from check_tight_shared_pocket import fixture as tight_fixture
from check_whole_support_fork_normal_form import ordinary_flow,whole_support_data,optimize
from check_whole_support_fork_flow import fork_flow

if not __debug__:raise RuntimeError('Assertions required; run without -O.')


def row_components(demand,adj):
    remaining=set(demand)|{w for v in demand for w in adj[v]};parts=[]
    while remaining:
        start=min(remaining);seen={start};todo=[start]
        while todo:
            for w in adj[todo.pop()]-seen:seen.add(w);todo.append(w)
        remaining-=seen;parts.append(seen)
    return parts


def inspect(current,bands,totals,subsets=False,independent=False):
    direct_check(*current);P={v for e in current[3] for v in e}
    frozen,_=frozen_certificate(current);assert frozen==P
    data,meta,_=whole_support_data(current,bands)
    kinds,pairs,links,support,resources=data;owner,aa,bb,mm=owner_data(kinds,pairs)
    loc={v:(b,c,p) for b,cols in enumerate(bands) for c,col in enumerate(cols) for p,v in enumerate(col)}
    mate={v:w for e in current[3] for v,w in (e,e[::-1])}
    vertical=set();short=set();boundary=set();ports={};assigned={};users=defaultdict(list)
    for v,k in kinds.items():
        if k!='TP':continue
        b,c,p=loc[v];assert 0<c<len(bands[b])-1
        choices={meta['owner'][b,j] for j in (c-1,c+1) if meta['labels'][b][j]==('B','B')}
        ports[v]=choices
        if choices&resources:
            j=min(choices&resources);assert j in support[owner[v]]
            slot=len(users[j]);assert slot<2;users[j].append(v);assigned['interval',j,slot]=v
        elif choices:
            assert choices<=meta['boundary'];boundary.add(v)
        elif loc[mate[v]][0]!=b:
            assert loc[mate[v]][1]==c;vertical.add(v)
        else:
            assert owner[v] in mm and set(pairs[owner[v]])=={v,mate[v]}
            assert kinds[mate[v]]=='BP';short.add(v)
    # A marked extreme interval has at most one adjacent TP port in the packet.
    mark_users=defaultdict(set)
    for v in boundary:
        for j in ports[v]:mark_users[j].add(v)
    assert all(len(u)<=1 for u in mark_users.values())
    assert len(boundary)<=len(meta['boundary'])
    adj=defaultdict(set)
    for v in vertical:
        for u,w in links:
            if u==v:adj[v].add(w);adj[w].add(v)
        assert 1<=len(adj[v])<=2
    for w in {w for v in vertical for w in adj[v]}:assert len(adj[w])<=2
    for part in row_components(vertical,adj):
        left=part&vertical;right=part-vertical
        assert len({loc[v][0] for v in part})==1
        assert len({loc[v][2] for v in part})==1
        assert len({loc[v][1] for v in part})==len(part)
        assert max(loc[v][1] for v in part)-min(loc[v][1] for v in part)==len(part)-1
        assert len(right)==len(left)+(len(part)>2)
        assert (len(part)==2 and all(len(adj[v])==1 for v in part)) or (
            all(len(adj[v])==2 for v in left) and len(right)==len(left)+1)
        assert len({owner[w] for w in right})==len(right)
        totals['vertical_row_components']+=1
    injection=matching({v:{('bp',w) for w in adj[v]} for v in vertical})
    assert len(injection)==len(vertical);assigned.update(injection)
    if subsets:
        if len(vertical)<=10:
            for mask in range(1<<len(vertical)):
                X={v for i,v in enumerate(sorted(vertical)) if mask>>i&1}
                sub=defaultdict(set)
                for v in X:
                    for w in adj[v]:sub[v].add(w);sub[w].add(v)
                parts=row_components(X,sub);extra=sum(len(p)>2 for p in parts)
                N={w for v in X for w in sub[v]}
                assert len(N)==len(X)+extra
                totals['arbitrary_vertical_tip_subsets']+=1
    result=exact_check(data,assigned,Counter())
    holes={v for v,k in kinds.items() if k=='TP'}-set(assigned.values())
    assert holes==short|boundary and not short&boundary
    grouped=[]
    for part in interaction_components(data):
        oo={i for tag,i in part if tag=='o'}
        H={v for v in holes if owner[v] in oo}
        if oo and (H or oo&aa):grouped.append(dict(alpha=len(oo&aa),short=sum(v in short for v in H),boundary=sum(v in boundary for v in H)))
    bound=sum(min(g['alpha'],(g['short']+g['boundary'])//2) for g in grouped)
    assert result['interaction_budget']==bound
    old,full=ordinary_flow(*data),fork_flow(*data)
    assert full['value']>=old['value']>=result['certified_payment']>=len(aa)-bound
    if independent:
        exact=optimize(*data);assert (exact['value'],exact['cost'])==(full['value'],full['cost'])
        totals['independent_primitive_pack_comparisons']+=1
    totals['frozen_boards']+=1
    totals['vertical_missing_tips']+=len(vertical)
    totals['mixed_vertical_missing_tips']+=sum(owner[v] in mm for v in vertical)
    totals['short_mixed_holes']+=len(short);totals['boundary_holes']+=len(boundary)
    totals['geometric_certificates']+=1
    totals['zero_budget_nonempty_alpha_boards']+=bool(aa) and bound==0
    totals['positive_budget_boards']+=bound>0
    totals['certificate_deficit_boards']+=result['certified_deficit']>0
    return dict(alpha=len(aa),mixed=len(mm),vertical_missing=sorted(vertical),
        mixed_vertical_missing=sorted(v for v in vertical if owner[v] in mm),short_holes=sorted(short),
        boundary_holes=sorted(boundary),interaction_bound=bound,certificate_deficit=result['certified_deficit'],
        ordinary_value=old['value'],full_value=full['value'],minimum_full_links=full['cost'],
        assignment=[dict(target=t,tip=v) for t,v in sorted(assigned.items(),key=repr)],groups=grouped)


def nonfrozen_control(totals):
    current=nonfrozen_obstruction();assert min(occupied_degrees(current).values())==3
    data,meta,_=whole_support_data(current,whole_bands(current))
    kinds,pairs,links,_,_=data;mate={v:w for e in current[3] for v,w in (e,e[::-1])}
    X={v for v,k in kinds.items() if k=='TP' and v[0]==1 and v[1] in (2,4,6)}
    assert all(mate[v]==(2,v[1]) for v in X)
    graph={v:{('bp',w) for u,w in links if u==v} for v in X}
    assert len(X)==3 and len(matching(graph))==2
    assert len(frozen_certificate(current)[0])==2
    totals['nonfrozen_degree3_controls']+=1


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    totals=Counter();named={}
    named['sealed_slot']=inspect(slot_fixture(),whole_bands(slot_fixture()),totals,True,True)
    paired,_=paired_fixture();named['paired_sealed']=inspect(paired,whole_bands(paired),totals,True,True)
    assert named['paired_sealed']['certificate_deficit']==1 and named['paired_sealed']['ordinary_value']==2
    for width,height,kind in itertools.product(range(6,19,2),range(4,13,2),('missing','cycle','collision')):
        current=stack(width,height,[kind]);inspect(current,whole_bands(current),totals,width==6 and height==4)
    for q in range(1,7):
        for family,fixture in [('tight',tight_fixture),('loose',loose_fixture)]:
            for filled in (set(),set(range(q))):
                current,_=fixture(q,filled);inspect(current,whole_bands(current),totals,q==1,q==1)
        for pad in (0,2,10):
            current=slot_fixture(q,pad);inspect(current,whole_bands(current),totals,q==1,q==1)
    fixtures=[slot_fixture(),paired,fork_fixture()[0],stack(6,4,['missing','collision'])]
    for path in ('unported_shared_mixed_gate.json','frozen_short_beta_deletion.json','frozen_vertical_mixed_missing_tip.json'):
        raw=json.loads((Path(__file__).parent/'fixtures'/path).read_text())
        assert all(k in raw for k in ('shape','selected','matching'))
        current=(*raw['shape'],{tuple(v) for v in raw['selected']},[tuple(map(tuple,e)) for e in raw['matching']])
        if path=='frozen_vertical_mixed_missing_tip.json':
            check_rank_certificate(current,[[tuple(v) for v in layer] for layer in raw['layers']]);totals['new_fixture_saved_strict_rank_checks']+=1
        fixtures.append(current)
    for idx,current in enumerate(fixtures):
        bands=whole_bands(current)
        for symmetry in itertools.product((False,True),repeat=3):
            shape,selected,edges=transformed(*current,*symmetry);move=image_map(*current[:2],symmetry)
            carried=[[tuple(move(v) for v in col) for col in cols] for cols in bands]
            result=inspect((*shape,selected,edges),carried,totals,True,idx<2)
            if symmetry==(False,False,False):named['fixture_'+str(idx)]=result
            totals['carried_isometries']+=1
    nonfrozen_control(totals)
    # Independent separated copies retain the new original mixed endpoint.
    raw=json.loads((Path(__file__).parent/'fixtures/frozen_vertical_mixed_missing_tip.json').read_text())
    for q in range(1,9):
        move=lambda v,i:(v[0]+14*i,v[1])
        current=(14*q,16,{move(tuple(v),i) for i in range(q) for v in raw['selected']},
                 [tuple(move(tuple(v),i) for v in e) for i in range(q) for e in raw['matching']])
        result=inspect(current,whole_bands(current),totals,q==1,q==1)
        assert len(result['mixed_vertical_missing'])==q
        assert len(result['short_holes'])==2*q and not result['boundary_holes']
        assert result['full_value']==2*q and result['minimum_full_links']==0
        assert result['certificate_deficit']==0 and result['interaction_bound']==q
        totals['new_mixed_fixture_copy_models']+=1
    assert totals['mixed_vertical_missing_tips']>0
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),named=named,
        scope='General geometric injection for every original vertically mated missing TP tip, including mixed owners; explicit partial certificate leaves only short horizontal mixed tips or marked-boundary port exceptions. Component half-hole bound is sufficient; universal compensation and5/6 remain open.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))

if __name__=='__main__':main()
