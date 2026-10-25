"""Cut actual matching edges without forgetting their ports or budgets.

All-size proofs: CROSSING_MATCHING_PORT_LEDGER.md. No solver dependency.
"""
import argparse
from collections import Counter,defaultdict
import itertools
import json
from pathlib import Path

from check_forced_mates_and_adjacent_maxima import configuration
from check_opposed_direction_interfaces import family,fast_rank_certificate,freezing_schedule
from check_residual_corridors import direct_check
from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize,evaluate
from check_selection_maximum_singleton import compile_even_width
from check_promotion_cores import frozen_certificate

if not __debug__:raise RuntimeError('Run without -O.')


def rectangle(r0,r1,c0,c1,vertical=False):
    assert (r1-r0)%2==(c1-c0)%2==0 and r0<r1 and c0<c1
    cells={(r,c) for r in range(r0,r1) for c in range(c0,c1)}
    bands=([[((r,c),(r,c+1)) for r in range(r0,r1)] for c in range(c0,c1,2)] if vertical else
           [[((r,c),(r+1,c)) for c in range(c0,c1)] for r in range(r0,r1,2)])
    return dict(cells=cells,bands=bands,bounds=(r0,r1,c0,c1),vertical=vertical)


def strand_parts(P,T,matching,bands):
    partner={a:b for cols in bands for pair in cols for a,b in (pair,pair[::-1])}
    vertices=P&set(partner);mate={a:b for e in matching for a,b in (e,e[::-1])}
    edges=[e for e in matching if set(e)<=vertices]
    edges += [pair for cols in bands for pair in cols if set(pair)<=vertices]
    graph={v:[] for v in vertices}
    for k,(a,b) in enumerate(edges):graph[a].append((b,k));graph[b].append((a,k))
    components=[];unseen=set(vertices)
    while unseen:
        start=min(unseen);body={start};todo=[start]
        while todo:
            v=todo.pop()
            assert len(graph[v])<=2
            for u,k in graph[v]:
                if u not in body:body.add(u);todo.append(u)
        unseen-=body;ends=[]
        for v in sorted(body):
            if mate[v] not in vertices:ends.append(('C',v))
            if partner[v] not in P:ends.append(('T' if partner[v] in T else 'B',v))
        assert len(ends) in (0,2)
        assert sum(len(graph[v]) for v in body)==2*len(body)-len(ends)
        components.append(dict(body=body,ends=ends,kind=''.join(sorted(k for k,v in ends)) or 'cycle'))
    return components,partner


def band_resources(P,T,bands):
    labels=[];Q=set();forests=[];gaps=[]
    for b,cols in enumerate(bands):
        row=[tuple(sorted('P' if v in P else 'T' if v in T else 'B' for v in pair)) for pair in cols]
        labels.append(row)
        for c,x in enumerate(row):
            if x==('T','T'):assert all(row[k]==('B','B') for k in (c-1,c+1) if 0<=k<len(row))
        unseen={c for c,x in enumerate(row) if x in (('B','B'),('T','T'))}
        while unseen:
            first=min(unseen);body={first};todo=[first];unseen.remove(first)
            while todo:
                c=todo.pop()
                for u in (c-1,c+1):
                    if u in unseen and (row[c]==('T','T') or row[u]==('T','T')):
                        unseen.remove(u);body.add(u);todo.append(u)
            first,last=min(body),max(body);assert body==set(range(first,last+1))
            bb=sum(row[c]==('B','B') for c in body);tt=len(body)-bb;assert bb-tt in (0,1)
            if bb-tt==1:
                j=(b,first,last);Q.add(j);forests.append((j,body))
            else:assert (first==0 and row[first]==('T','T')) or (last==len(row)-1 and row[last]==('T','T'))
        c=0
        while c<len(row):
            if 'P' in row[c]:c+=1;continue
            first=c
            while c<len(row) and 'P' not in row[c]:c+=1
            units={j for j,body in forests if j[0]==b and first<=j[1]<=j[2]<c}
            capacity=c-first-sum(v in T for pair in cols[first:c] for v in pair)
            assert len(units)==capacity
            gaps.append((b,first,c,units))
    BB=sum(x==('B','B') for row in labels for x in row);TT=sum(x==('T','T') for row in labels for x in row)
    assert len(Q)==BB-TT
    return Q,gaps,labels


def model_for_components(P,T,bands,components,Q,gaps):
    closed=[x for x in components if x['kind'] in ('TT','BB','BT')]
    pairs=[tuple(v for k,v in x['ends']) for x in closed]
    kinds={v:'TP' if k=='T' else 'BP' for x in closed for k,v in x['ends']}
    body_owner={v:i for i,x in enumerate(closed) for v in x['body']};nodes={}
    for b,cols in enumerate(bands):
        for c,pair in enumerate(cols):
            users={body_owner[v] for v in pair if v in body_owner};assert len(users)<=1
            if users:nodes[b,c]=next(iter(users))
    W={o:set() for o in range(len(pairs))}
    for b,first,after,units in gaps:
        for boundary in (first-1,after):
            if (b,boundary) in nodes:W[nodes[b,boundary]]|=units
    links=[]
    for cols in bands:
        for left,right in zip(cols,cols[1:]):
            for a,b in zip(left,right):
                if kinds.get(a)=='TP' and kinds.get(b)=='BP':links.append((a,b))
                if kinds.get(b)=='TP' and kinds.get(a)=='BP':links.append((b,a))
    return (kinds,pairs,links,W,Q),closed


def compile_partition(cur,regions,independent=False):
    R,C,T,M=cur;P={v for e in M for v in e};seen=set();all_bands=[];owner_region={};results=[]
    for i,region in enumerate(regions):
        assert not seen&region['cells'];seen|=region['cells']
        owner_region.update({v:i for v in region['cells']})
        all_bands+=region['bands']
    assert seen=={(r,c) for r in range(R) for c in range(C)}
    crossings=[e for e in M if owner_region[e[0]]!=owner_region[e[1]]]
    global_parts,_=strand_parts(P,T,M,all_bands);Q,gaps,labels=band_resources(P,T,all_bands)
    data,global_closed=model_for_components(P,T,all_bands,global_parts,Q,gaps)
    assert len(global_closed)==sum(x['kind']!='cycle' for x in global_parts)
    global_flow=fork_flow(*data);_,GA,GB,_=owner_data(*data[:2]);closed_bodies=set();inventory=Counter();local_value=0;local_deficit=0
    port_parts=[];global_band_offset=0;retained_global_owners=set()
    global_by_body={frozenset(x['body']):i for i,x in enumerate(global_closed)}
    used_resources=set();lifted_paid=[];retained_links=[];local_cost=0
    for i,region in enumerate(regions):
        localP=P&region['cells'];parts,_=strand_parts(P,T,M,region['bands'])
        lQ,lgaps,llabels=band_resources(P,T,region['bands']);ld,lc=model_for_components(P,T,region['bands'],parts,lQ,lgaps)
        f=fork_flow(*ld);_,A,B,_=owner_data(*ld[:2]);counts=Counter(x['kind'] for x in parts);inventory+=counts
        internal=sum(set(e)<=region['cells'] for e in M);ports=sum(owner_region[v]==i for e in crossings for v in e)
        cut_slack=len(region['cells'])//2-len(T&region['cells'])-internal
        assert cut_slack==len(lQ)+counts['BB']-counts['TT']+counts['BC']+counts['CC']
        assert ports==counts['CT']+counts['BC']+2*counts['CC']
        assert sum(k=='T' for x in parts for k,v in x['ends'])==2*counts['TT']+counts['BT']+counts['CT']
        assert sum(k=='B' for x in parts for k,v in x['ends'])==2*counts['BB']+counts['BT']+counts['BC']
        for x in lc:
            key=frozenset(x['body']);assert key not in closed_bodies;closed_bodies.add(key)
            assert key in global_by_body;retained_global_owners.add(global_by_body[key])
        for x in parts:
            if 'C' in x['kind']:port_parts.append((i,x))
        # Verify each local primitive really embeds in the SAME global source,
        # owner and resource identities; never just add independent values.
        for cert in f['certificates']:
            mapped=[global_by_body[frozenset(lc[o]['body'])] for o in cert['owners']]
            assert not set(mapped)&set(lifted_paid);lifted_paid+=mapped
            for link in cert['links']:
                assert link in data[2];retained_links.append(link)
            if cert['kind']!='beta':
                j=cert.get('interval')
                if j is not None:
                    gj=(j[0]+global_band_offset,j[1],j[2]);assert gj in Q and gj not in used_resources
                    used_resources.add(gj)
                    witness=global_by_body[frozenset(lc[cert['witness']]['body'])]
                    assert gj in data[3][witness]
        local_value+=f['value'];local_deficit+=f['deficit'];local_cost+=f['cost']
        results.append(dict(region=i,bounds=region['bounds'],vertical=region['vertical'],ports=ports,
            internal_matching=internal,raw=len(lQ),counts=dict(counts),cut_slack=cut_slack,
            closed_alpha=len(A),closed_beta=len(B),closed_value=f['value'],closed_deficit=f['deficit'],closed_cost=f['cost']))
        global_band_offset+=len(region['bands'])
    # Restore the removed M edges on the port-only skeleton, independently
    # of computing the full endpoint components.
    graph=defaultdict(list);end_label={}
    for i,x in port_parts:
        ports=[v for k,v in x['ends'] if k=='C'];ordinary=[k for k,v in x['ends'] if k!='C']
        if len(ports)==2:
            a,b=ports;graph[a].append(b);graph[b].append(a)
        else:
            assert len(ports)==len(ordinary)==1;end_label[ports[0]]=ordinary[0]
    for a,b in crossings:graph[a].append(b);graph[b].append(a)
    remaining=set(graph);interface=Counter();skeleton=[]
    while remaining:
        root=min(remaining);body={root};todo=[root]
        while todo:
            v=todo.pop()
            for u in graph[v]:
                if u not in body:body.add(u);todo.append(u)
        remaining-=body;ends=[end_label[v] for v in sorted(body) if v in end_label]
        assert len(ends) in (0,2)
        kind=''.join(sorted(ends)) or 'cycle';interface[kind]+=1
        gp=next(x for x in global_parts if root in x['body']);assert gp['kind']==kind
        skeleton.append(dict(ports=sorted(body),kind=kind))
    assert len(GA)==inventory['TT']+interface['TT'] and len(GB)==inventory['BB']+interface['BB']
    assert inventory['CT']==2*interface['TT']+interface['BT']
    assert inventory['BC']==2*interface['BB']+interface['BT']
    assert inventory['BC']+inventory['CC']-len(crossings)==interface['BB']-interface['TT']
    assert interface['TT']+interface['BB']+interface['BT']==len(crossings)-inventory['CC']
    slack=R*C//2-len(T)-len(M)
    assert slack==len(Q)+len(GB)-len(GA)
    assert slack==sum(x['cut_slack'] for x in results)-len(crossings)
    assert slack==len(Q)+inventory['BB']-inventory['TT']+interface['BB']-interface['TT']
    assert global_flow['value']>=local_value
    assert len(retained_links)==local_cost and len({v for e in retained_links for v in e})==2*len(retained_links)
    assert evaluate(*data[:2],retained_links,*data[3:])['value']>=local_value
    assert global_flow['deficit']<=local_deficit+interface['TT']<=local_deficit+len(crossings)
    boundary_alphas=GA-retained_global_owners
    assert len(boundary_alphas)==interface['TT']
    # Reserve only ORIGINAL units not already spent by the retained packs.
    assignment={}
    def reserve(a,seen):
        for j in sorted(data[3][a]-used_resources-seen):
            seen.add(j)
            if j not in assignment or reserve(assignment[j],seen):assignment[j]=a;return True
        return False
    nu=sum(reserve(a,set()) for a in sorted(boundary_alphas))
    assert len(assignment)==nu and len(set(assignment.values()))==nu
    assert all(a in boundary_alphas and j not in used_resources and j in data[3][a] for j,a in assignment.items())
    assert global_flow['value']>=local_value+nu
    assert global_flow['deficit']<=local_deficit+interface['TT']-nu
    if independent:
        pack=optimize(*data);assert (pack['value'],pack['cost'])==(global_flow['value'],global_flow['cost'])
    return dict(crossing_edges=crossings,regions=results,local_inventory=dict(inventory),interface=dict(interface),
        interface_components=skeleton,alpha=len(GA),beta=len(GB),raw=len(Q),slack=slack,
        value=global_flow['value'],cost=global_flow['cost'],deficit=global_flow['deficit'],
        local_closed_value=local_value,local_closed_deficit=local_deficit,local_closed_cost=local_cost,
        available_crossing_deficit_bound=local_deficit+interface['TT'],reserved_interface_payments=nu,
        retained_pack_reserve_bound=local_deficit+interface['TT']-nu,
        reserved_original_units=sorted((a,j) for j,a in assignment.items())),data


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);args=p.parse_args()
    records=[];totals=Counter();fixture=None
    for w,q in itertools.product((8,10,20,40),(1,2,3,7)):
        cur=configuration(w,q);direct_check(*cur);R,C=cur[:2]
        assert frozen_certificate(cur)[0]=={v for e in cur[3] for v in e}
        for cut in sorted({2,4,R//2//2*2,R-2}):
            for topv,bottomv in itertools.product((False,True),repeat=2):
                regions=[rectangle(0,cut,0,C,topv),rectangle(cut,R,0,C,bottomv)]
                rec,data=compile_partition(cur,regions,independent=(w,q)==(8,1));rec.update(w=w,q=q,cut_row=cut,top_vertical=topv,bottom_vertical=bottomv)
                records.append(rec);totals['physical_partitions']+=1
                totals['crossing_matching_edges']+=len(rec['crossing_edges']);totals['interface_cycles']+=rec['interface'].get('cycle',0)
                totals['mixed_region_direction_partitions']+=topv!=bottomv
                totals['independent_primitive_optimum_controls']+=(w,q)==(8,1)
                if cut==2 and not bottomv:
                    assert len(rec['crossing_edges'])==q and rec['interface']['TT']==q
                    assert rec['local_closed_deficit']==rec['local_closed_value']==0
                    assert (rec['alpha'],rec['beta'],rec['raw'],rec['value'],rec['deficit'],rec['slack'])==(q,0,3*q,0,q,2*q)
                    assert [x['cut_slack'] for x in rec['regions']]==[0,3*q]
                    totals['sharp_frozen_interfaces']+=1
                    if not topv:
                        old,meta=compile_even_width(cur)
                        assert (fork_flow(*old)['value'],fork_flow(*old)['cost'])==(rec['value'],rec['cost'])
                    if (w,q,topv)==(8,1,True):
                        fixture=dict(record=rec,selected_points=sorted(cur[2]),matching_edges=cur[3],
                            kinds=sorted(data[0].items()),pairs=data[1],links=data[2],support=sorted((o,sorted(js)) for o,js in data[3].items()),resources=sorted(data[4]))
    # A four-region control exercises CC relays and independent choices of
    # direction on both axes rather than only a single horizontal cut.
    for q in (1,2,3):
        cur=family(q)[0];R,C=cur[:2];L=C//2
        for choices in itertools.product((False,True),repeat=4):
            regions=[rectangle(r0,r1,c0,c1,v) for (r0,r1,c0,c1),v in zip(
                [(0,2,0,L),(2,R,0,L),(0,2,L,C),(2,R,L,C)],choices)]
            rec,data=compile_partition(cur,regions);rec.update(q=q,opposed_four_regions=True,directions=choices)
            records.append(rec);totals['physical_partitions']+=1;totals['four_region_partitions']+=1
            totals['crossing_matching_edges']+=len(rec['crossing_edges']);totals['interface_cycles']+=rec['interface'].get('cycle',0)
    for q in (1,2,3):
        cur=family(q)[0];R,C=cur[:2];L=C//2
        rec,_=compile_partition(cur,[rectangle(0,R,0,L,True),rectangle(0,R,L,C,False)])
        assert not rec['crossing_edges'] and rec['alpha']==rec['value']==2*q and rec['cost']==0
        rec['no_crossing_recovery_control']=q;records.append(rec);totals['no_crossing_recovery_controls']+=1
    # A physically embedded port-only cycle has zero interface credit.
    cycle=(2,4,set(),[((0,1),(0,2)),((1,1),(1,2))]);direct_check(*cycle)
    rec,_=compile_partition(cycle,[rectangle(0,2,0,2),rectangle(0,2,2,4)],independent=True)
    assert (len(rec['crossing_edges']),rec['local_inventory']['CC'],rec['interface']['cycle'])==(2,2,1)
    assert rec['alpha']==rec['beta']==0 and rec['raw']==rec['slack']==2
    rec['nonfrozen_cycle_control']=True;records.append(rec);totals['physical_port_cycle_controls']+=1
    # Arbitrarily many CC relay components still yield ONE interface path.
    for m in (*range(9),16,32):
        C=2*(m+2);T={(0,0),(0,C-1)}
        M=[((0,2*i+1),(0,2*i+2)) for i in range(m+1)]
        M += [((1,2*i),(1,2*i+1)) for i in range(1,m+1)]
        cur=(2,C,T,M);direct_check(*cur)
        regions=[rectangle(0,2,2*i,2*i+2,i in (0,m+1)) for i in range(m+2)]
        rec,_=compile_partition(cur,regions,independent=m<=4)
        assert (len(rec['crossing_edges']),rec['local_inventory'].get('CC',0),rec['interface']['TT'])==(m+1,m,1)
        assert (rec['alpha'],rec['beta'],rec['raw'],rec['value'],rec['deficit'],rec['slack'])==(1,0,2,1,0,1)
        rec['nonfrozen_relay_control']=m;records.append(rec);totals['physical_port_relay_controls']+=1
    totals['all_physical_partition_controls']=len(records)
    totals['strict_reserve_bound_improvements']=sum(r['reserved_interface_payments']>0 for r in records)
    totals['reserved_original_units']=sum(r['reserved_interface_payments'] for r in records)
    assert fixture is not None
    (Path(__file__).parent/'fixtures/crossing_matching_port_obstruction.json').write_text(json.dumps(fixture,indent=2)+'\n')
    # Keep the permanent receipt concise; the smallest full physical model
    # stays in the fixture and every other detail is reproducible above.
    keys=('w','q','cut_row','top_vertical','bottom_vertical','opposed_four_regions','directions',
          'no_crossing_recovery_control','nonfrozen_cycle_control','nonfrozen_relay_control',
          'local_inventory','interface','alpha','beta','raw','slack','value','cost','deficit',
          'local_closed_value','local_closed_deficit','local_closed_cost',
          'reserved_interface_payments','retained_pack_reserve_bound')
    summaries=[dict(**{k:r[k] for k in keys if k in r},crossing_matching_edges=len(r['crossing_edges'])) for r in records]
    report=dict(status='PASS',totals=dict(totals),records=summaries,
        scope='Written arbitrary-even-rectangle-partition port ledger and boundary stitching; retained closed local primitive packs inject into one global resource pool; deficit at most sum local deficits plus interface alphas minus a matching into original units unused by retained packs; interface alphas bounded by crossing M edges; physical fully frozen sharp family.',
        limits=['Local pack hypothesis excludes open port components; their budgets are not independent closed-strand payments.',
                'Declared links are valid within local chosen bands; arbitrary extra interface links are not assumed.',
                'No universal5over6 improvement or guarantee of full compensation.'])
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',totals=dict(totals)),indent=2))

if __name__=='__main__':main()
