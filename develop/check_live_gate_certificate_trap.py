"""All-live, degree-two terminal traps and their exact payment frontier.

Abstract all-size proofs are in LIVE_GATE_CERTIFICATE_TRADEOFF.md. The physical
survey constructs positive certificates on existing boards; it does not claim
a frozen realization of the abstract obstruction.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_compensation_flow_normal_form import owner_data
from check_frozen_tip_slot_obstruction import matching, slot_graph
from check_paired_hole_certificates import all_assignments
from check_partial_tip_compensation import components, interaction_components, lift, live_prune
from check_terminal_cancellation_and_stranded_demand import cancel_pairs
from check_whole_support_fork_normal_form import canonical, ordinary_flow, whole_support_data

if not __debug__:
    raise RuntimeError('Run without -O; assertions are required.')


def family(q):
    assert q >= 2
    kinds,pairs,_ = canonical(('A',)*q+('B',)*q+('M',)*(4*q-3))
    a = [pairs[i][0] for i in range(q)]
    b = [pairs[q+i][0] for i in range(q)]
    n = [pairs[2*q+i] for i in range(q)]
    m = [pairs[3*q+i] for i in range(q)]
    u = {j:pairs[4*q+j-1] for j in range(1,q)}
    v = {j:pairs[5*q-2+j] for j in range(1,q-1)}
    # Every group is a DISJOINT terminal bipartite component. Owner pairing
    # connects these groups into the all-live directed relay system.
    local = [[(m[i][1],b[i]),(a[i],b[i]),(a[i],n[i][0])] for i in range(q)]
    merges = [[(n[0][1],u[1][0]),(n[1][1],u[1][0])]]
    merges += [[(u[j-1][1],u[j][0]),(n[j][1],u[j][0])] for j in range(2,q)]
    split = [[(u[q-1][1],m[q-1][0]),
              (u[q-1][1],v[q-2][0] if q > 2 else m[0][0])]]
    split += [[(v[j][1],m[j][0]),(v[j][1],v[j-1][0])] for j in range(q-2,1,-1)]
    if q > 2:
        split += [[(v[1][1],m[1][0]),(v[1][1],m[0][0])]]
    links = [edge for group in local+merges+split for edge in group]
    data = kinds,pairs,links,{o:set() for o in range(len(pairs))},set()
    assert len(links) == 7*q-4 and len(merges) == len(split) == q-1
    return data,dict(a=a,b=b,n=n,m=m,u=u,v=v,local=local,merges=merges,split=split)


def certificate(q,required):
    """Attain maximal assignment size subject to at least required payments."""
    assert 1 <= required <= q
    data,nodes = family(q)
    d = required-1
    a,b,n,m,u,v = (nodes[k] for k in ('a','b','n','m','u','v'))
    edges = [(a[i],b[i]) for i in range(d)]
    edges += [edge for i in range(d,q) for edge in ((a[i],n[i][0]),(m[i][1],b[i]))]
    # Select one incoming edge at every merger, forcing root ancestry to N_d.
    edges += [(n[1 if d == 1 else 0][1],u[1][0])]
    edges += [(n[j][1] if j == d else u[j-1][1],u[j][0]) for j in range(2,q)]
    # Select one outgoing edge at every splitter, forcing root descent to M_d.
    if q == 2:
        edges += [(u[1][1],m[d][0])]
    else:
        edges += [(u[q-1][1],m[q-1][0] if d == q-1 else v[q-2][0])]
        edges += [(v[j][1],m[j][0] if d == j else v[j-1][0]) for j in range(q-2,1,-1)]
        edges += [(v[1][1],m[1 if d == 1 else 0][0])]
    return {('bp',w):t for t,w in edges}


def check_certificate(data,assigned,q,nodes,totals,flow=False):
    graph = slot_graph(data)
    assert len(set(assigned.values())) == len(assigned)
    assert all(t in graph[v] for t,v in assigned.items())
    links = [(v,t[1]) for t,v in assigned.items()]
    _,inventory,_ = cancel_pairs(data[0],data[1],links,Counter())
    paid = q-inventory['TP','TP']
    direct = sum(assigned.get(('bp',nodes['b'][i])) == nodes['a'][i] for i in range(q))
    assert paid <= direct+1
    assert len(assigned) <= 4*q-2-direct
    # Independent owner-component signed ledger; no interval or beta is split.
    owner,aa,bb,_ = owner_data(*data[:2])
    parts = components(set(range(len(data[1]))),[(owner[x],owner[y]) for x,y in links])
    assert sum(min(len(part&aa),len(part&bb)) for part in parts) == paid
    if flow:
        restricted = data[:2]+(links,)+data[3:]
        assert ordinary_flow(*restricted)['value'] == paid
        assert lift(data,assigned)['certified_payment'] == paid
        totals['independent_flow_lifts'] += 1
    totals['certificates'] += 1
    return paid


def abstract(totals):
    records = []
    for q in range(2,21):
        data,nodes = family(q)
        pruned,meta = live_prune(data)
        assert pruned == data and not meta['removed_mixed']
        assert len(meta['live_mixed']) == 4*q-3
        assert len(interaction_components(data)) == 1
        degree = Counter(v for edge in data[2] for v in edge)
        assert max(degree.values()) == 2
        terminal_parts = components(set(data[0]),data[2])
        assert Counter(map(len,terminal_parts)) == {4:q,3:2*q-2,1:2*q}
        # Necessary checkerboard condition: paired original ends have opposite
        # phase, and every candidate TP->BP joins opposite phases.
        color = {}
        for o,pair in enumerate(data[1]):
            colors = (0,1) if o < q else (1,0)
            color.update(zip(pair,colors))
        assert all(color[x] != color[y] for x,y in data[2])
        maximum = matching(slot_graph(data))
        assert len(maximum) == 4*q-2
        assert check_certificate(data,maximum,q,nodes,totals,True) == 1
        lifted = lift(data,maximum)
        assert lifted['holes'] == 2*q-1
        assert lifted['interaction_budget'] == lifted['final_component_budget'] == q-1
        full = ordinary_flow(*data)
        assert (full['value'],full['cost']) == (q,q)
        for paid in range(1,q+1):
            assigned = certificate(q,paid)
            assert len(assigned) == 4*q-1-paid
            assert check_certificate(data,assigned,q,nodes,totals,True) == paid
            totals['frontier_points'] += 1
        if q <= 3:
            frontier = {p:-1 for p in range(1,q+1)}
            count = 0
            for assigned in all_assignments(slot_graph(data)):
                paid = check_certificate(data,assigned,q,nodes,totals,q == 2)
                for p in frontier:
                    if paid >= p:
                        frontier[p] = max(frontier[p],len(assigned))
                count += 1
            assert count == 5**q*3**(2*q-2)
            assert frontier == {p:4*q-1-p for p in range(1,q+1)}
            totals['exhaustive_partial_certificates'] += count
        if q <= 7:
            fixed = [edge for group in nodes['local'] for edge in (group[0],group[2])]
            groups = nodes['merges']+nodes['split']
            count = 0
            for chosen in itertools.product(*groups):
                assigned = {('bp',w):v for v,w in fixed+list(chosen)}
                assert len(assigned) == 4*q-2
                assert check_certificate(data,assigned,q,nodes,totals,q <= 3) == 1
                count += 1
            assert count == 4**(q-1)
            totals['exhaustive_maximum_certificates'] += count
        records.append(dict(q=q,owners=6*q-3,live_mixed=4*q-3,removed_mixed=0,
            maximum_terminal_degree=2,maximum_assignments=4*q-2,
            number_of_maximum_certificates=4**(q-1),payment_of_every_maximum=1,
            actual_ordinary_payment=q,actual_minimum_links=q,
            largest_full_payment_certificate=3*q-1,
            assignments_sacrificed_for_full_payment=q-1))
    return records


def physical(totals):
    """Construct max-size payment-optimal certificates on existing frozen boards."""
    from check_compensation_flow_geometry_frontier import pad_image
    from check_elbow_sources import elbow
    from check_exchange_terminal_nonunique import fixture, matching_orders, graft
    from check_frozen_beta_support_fork import fixture as fork
    from check_frozen_first_destination_allocation import fixture as unported
    from check_frozen_shared_mixed_gate import fixture as shared
    from check_frozen_tip_slot_obstruction import fixture as tip
    from check_interval_connector_cycles_and_missing_ports import stack, whole_bands
    from check_promotion_cores import frozen_certificate
    from check_residual_corridors import direct_check
    from degree_three_fusion import occupied_bands
    from rotor_networks import rotor, combine, star_modules, transform_module
    base = fixture()
    sources = [('tip',tip()),('shared',shared()),('unported',unported()[0]),('fork',fork()[0])]
    sources += [('bent'+str(i),(*base[:3],list(x['matching']))) for i,x in enumerate(matching_orders())]
    sources += [('graft',graft(6,4)),('elbow',elbow(6,4))]
    sources += [(x,stack(6,4,[x])) for x in ('missing','collision','cycle')]
    sources += [('occupied'+str(w),occupied_bands(w)[0]) for w in (6,8,12)]
    module = rotor()
    sources += [('rotor',(6,6,module['selected'],module['matching']))]
    for w in (6,10,20):
        net = combine([transform_module(m,(False,False,False),(w-2,w-2)) for m in star_modules(w)])
        sources += [('star'+str(w),(2*w+2,2*w+2,net['selected'],net['matching']))]
    outcomes = Counter()
    for (name,raw),sym,offset in itertools.product(sources,itertools.product((False,True),repeat=3),itertools.product((2,3),repeat=2)):
        current = pad_image(raw,sym,offset)
        direct_check(*current)
        if len(frozen_certificate(current)[0]) != 2*len(current[3]):
            totals['nonfrozen_physical_alignments_excluded'] += 1
            continue
        data,_,_ = whole_support_data(current,whole_bands(current))
        data,_ = live_prune(data)
        flow = ordinary_flow(*data)
        assigned = {('bp',w):v for v,w in flow['links']}
        for v,j in flow['payments']:
            assigned['interval',j,0] = v
        graph = slot_graph(data)
        remaining = {v:targets-assigned.keys() for v,targets in graph.items() if v not in assigned.values()}
        extended = assigned|matching(remaining)
        maximum_size = len(matching(graph))
        assert len(extended) == maximum_size
        result = lift(data,extended)
        assert result['final_component_budget'] == flow['deficit']
        totals['physical_maximum_optimum_certificates'] += 1
        totals['physical_certificates_with_nonempty_alpha'] += result['alpha'] > 0
        totals['physical_certificates_with_positive_payment'] += flow['value'] > 0
        outcomes[name,result['alpha'],flow['value'],flow['cost'],result['holes']] += 1
    return [dict(family=k[0],alpha=k[1],payment=k[2],minimum_links=k[3],holes=k[4],count=v)
            for k,v in sorted(outcomes.items())]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    totals = Counter()
    records = abstract(totals)
    physical_records = physical(totals)
    result = dict(status='PASS',totals=dict(totals),abstract=records,physical=physical_records,
        scope='All-q written counterexample and exact frontier; every abstract mixed owner is live, '
        'every terminal has at most two candidate links, checkerboard phases consistent. '
        'NOT a frozen realization. Existing physical boards have explicitly constructed '
        'maximum certificates attaining ordinary optimum; no universal existence or 5/6 claim.')
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__ == '__main__':
    main()
