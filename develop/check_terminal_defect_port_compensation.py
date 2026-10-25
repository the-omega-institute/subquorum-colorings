"""Physical port graph, exact joint withdrawals, independent allocation checks.

Standard library only. General proofs: TERMINAL_DEFECT_PORT_COMPENSATION.md.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_cooperative_promotion import neighbors, occupied_degrees
from check_four_outward_alpha_localization import fixture as root_fixture
from check_full_pool_singleton_obstruction import fixture as singleton
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_interval_connector_cycles_and_missing_ports import block, stack
from check_owned_donors import capacity_cross, straight_comb
from check_pinwheel_two_track_switches import model
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_thin_component_receivers import capped
from check_whole_support_fork_flow import fork_flow
from degree_three_fusion import four_way, corner_join
from rotor_networks import chain

if not __debug__:
    raise RuntimeError('Run with assertions, without -O.')


def matching(choices):
    """Independent bipartite augmentation, including reassignment of old units."""
    assigned = {}
    def visit(edge, seen):
        for unit in sorted(choices[edge]):
            if unit in seen:
                continue
            seen.add(unit)
            if unit not in assigned or visit(assigned[unit], seen):
                assigned[unit] = edge
                return True
        return False
    for edge in sorted(choices):
        visit(edge, set())
    result = {edge: unit for unit, edge in assigned.items()}
    assert len(result) == len(assigned)
    assert all(unit in choices[edge] for edge, unit in result.items())
    return result


def brute(choices):
    rows = list(choices.values())
    def recurse(i, used):
        if i == len(rows):
            return 0
        return max([recurse(i+1, used)] +
                   [1+recurse(i+1, used | {u}) for u in rows[i]-used])
    return recurse(0, set())


def components(capacity, edges):
    adj = defaultdict(list)
    for edge, pair in edges.items():
        for v in pair:
            adj[v].append(edge)
    assert all(len(adj[v]) <= 2 for v in capacity)
    assert all(len(adj[v]) <= 1 for v, cap in capacity.items() if not cap)
    pending = set(capacity)
    result = []
    while pending:
        todo = [min(pending)]; vertices = set(todo); seen_edges = set()
        while todo:
            v = todo.pop()
            for edge in adj[v]:
                seen_edges.add(edge)
                for u in edges[edge]:
                    if u not in vertices:
                        vertices.add(u); todo.append(u)
        pending -= vertices
        cycle = len(seen_edges) == len(vertices)
        assert cycle or len(seen_edges)+1 == len(vertices)
        zero = sum(not capacity[v] for v in vertices)
        assert zero <= 2 and (not cycle or zero == 0)
        result.append(dict(vertices=vertices, edges=seen_edges, cycle=cycle, zero=zero))
    return result


def deficit(parts, removed):
    return sum(len(p['vertices'] & removed) if p['cycle'] else
               max(0, p['zero']+len(p['vertices'] & removed)-1) for p in parts)


def port_graph(cur):
    """Extract forests from physical cells independently of the model compiler."""
    R, C, T, M = cur
    P = {v for e in M for v in e}; O = T | P
    mate = {a: b for e in M for a, b in (e, e[::-1])}
    data, closed, _, partner = model(cur)
    own, A, B, mixed = owner_data(*data[:2])
    capacity = {}; forest_at = {}; keys = {}
    for r in range(0, R, 2):
        labels = [tuple(sorted('P' if (a,c) in P else 'T' if (a,c) in T else 'B'
                               for a in (r,r+1))) for c in range(C)]
        unseen = {c for c, x in enumerate(labels) if x in (('B','B'), ('T','T'))}
        for c, x in enumerate(labels):
            if x == ('T','T'):
                assert all(labels[d] == ('B','B') for d in (c-1,c+1) if 0 <= d < C)
        while unseen:
            todo = [min(unseen)]; cols = set(todo); unseen -= cols
            while todo:
                c = todo.pop()
                for d in (c-1,c+1):
                    if d in unseen and (labels[c] == ('T','T') or labels[d] == ('T','T')):
                        unseen.remove(d); cols.add(d); todo.append(d)
            first, last = min(cols), max(cols)
            assert cols == set(range(first,last+1))
            unit = ('forest', r, first, last)
            cap = sum(1 if labels[c] == ('B','B') else -1 for c in cols)
            assert cap in (0,1)
            if not cap:
                assert (first == 0 and labels[first] == ('T','T')) or (
                    last == C-1 and labels[last] == ('T','T'))
            capacity[unit] = cap
            keys[unit] = tuple((a,c) for a,c in sorted(itertools.product((r,r+1), cols)))
            for c in cols:
                forest_at[r,c] = unit
    positive = {u for u in capacity if capacity[u]}
    assert {keys[u] for u in positive} == data[4]
    edges = {}; d4 = boundary = 0
    for a in sorted(A):
        tips = []
        for v in data[1][a]:
            r, c = v; band = r//2*2; n = partner[v]
            assert n in T and mate[v][1] == c and mate[v][0]//2 != r//2
            degree = len(set(neighbors(v)) & O)
            ports = []
            for d in (c-1,c+1):
                if 0 <= d < C and all((x,d) not in O for x in (band,band+1)):
                    ports.append(forest_at[band,d])
            assert len(ports) <= 1
            if 0 < c < C-1:
                assert degree+len(ports) == 4
            assert degree in (3,4)
            if ports:
                u = ports[0]
                if capacity[u]:
                    assert keys[u] in data[3][a]
                else:
                    boundary += 1
            else:
                u = ('missing', r, c, 0); capacity[u] = 0
                if degree == 4:
                    d4 += 1
                else:
                    assert c in (0,C-1); boundary += 1
            tips.append(u)
        edges[a] = tuple(tips)
    parts = components(capacity, edges)
    h = sum(p['zero'] for p in parts if p['edges'])
    assert h == d4+boundary
    slack = R*C//2-len(T)-len(M)
    assert slack == len(data[4])+len(B)-len(A)
    return data, capacity, keys, edges, parts, d4, boundary, slack


def check_physical(name, cur, totals, rng, pools=5):
    direct_check(*cur)
    assert min(occupied_degrees(cur).values()) >= 3
    data, caps, keys, edges, parts, d4, boundary, slack = port_graph(cur)
    own, A, B, mixed = owner_data(*data[:2])
    positive = {u for u, cap in caps.items() if cap}
    d0 = deficit(parts,set())
    assert 2*d0 <= d4+boundary
    assert slack >= len(B)-d0
    tests = [set(), positive] + [{u for u in sorted(positive) if rng.randrange(4) == 0} for _ in range(pools)]
    for removed in tests:
        choices = {a: set(pair) & (positive-removed) for a,pair in edges.items()}
        paid = matching(choices)
        D = deficit(parts,removed)
        assert len(paid) == len(A)-D
        assert D <= d0+len(removed)
        if len(A) <= 5:
            assert brute(choices) == len(paid)
            totals['physical_exhaustive_port_optima'] += 1
        # Whole support can improve this certificate; do not assert equality.
        available = {keys[u] for u in positive-removed}
        whole = (*data[:3], {a:w & available for a,w in data[3].items()}, available)
        assert len(matching({a:whole[3][a] for a in A})) >= len(paid)
        if name.startswith(('control', 'root')) or len(A) <= 2:
            assert fork_flow(*whole)['value'] >= len(paid)
            totals['whole_fork_comparisons'] += 1
        totals['physical_withdrawal_profiles'] += 1
    if not boundary and d4 <= 1:
        assert not d0 and len(matching({a:set(pair)&positive for a,pair in edges.items()})) == len(A)
        totals['automatic_full_pool_models'] += 1
        totals['nonvacuous_automatic_full_pool_models'] += bool(A)
    if d4+boundary <= 2*len(B)+1:
        assert slack >= 0
        totals['coefficient_one_criteria'] += 1
    totals['physical_models'] += 1
    totals['alpha_paths'] += len(A)
    totals['degree_four_alpha_terminals'] += d4
    totals['raw_boundary_defects'] += boundary
    totals['positive_port_deficits'] += d0 > 0
    return dict(name=name,shape=list(cur[:2]),alpha=len(A),beta=len(B),d4=d4,boundary=boundary,
                port_deficit=d0,slack=slack,cycles=sum(p['cycle'] for p in parts))


def abstract_controls(totals):
    # Every degree-at-most-two multigraph through four vertices, loops once,
    # parallel ordinary edges twice. Zero original vertices can only be leaves.
    for n in range(1,5):
        pairs=list(itertools.combinations_with_replacement(range(n),2))
        def build(i, edges, degree):
            if i == len(pairs):
                yield dict(enumerate(edges)); return
            u,v=pairs[i]
            for k in range((1 if u==v else 2)+1):
                d=degree[:];d[u]+=k;d[v]+=k
                if max(d)<=2:
                    yield from build(i+1,edges+[(u,v)]*k,d)
        for edges in build(0,[],[0]*n):
            deg=Counter(v for pair in edges.values() for v in pair)
            leaves=[v for v in range(n) if deg[v]<=1]
            for mask in range(1<<len(leaves)):
                zero={v for i,v in enumerate(leaves) if mask>>i&1}
                caps={('v',v):int(v not in zero) for v in range(n)}
                es={i:tuple(('v',v) for v in pair) for i,pair in edges.items()}
                parts=components(caps,es);positive={v for v in caps if caps[v]}
                for bits in range(1<<len(positive)):
                    removed={v for i,v in enumerate(sorted(positive)) if bits>>i&1}
                    choices={a:set(pair)&(positive-removed) for a,pair in es.items()}
                    value=len(matching(choices))
                    assert value == brute(choices) == len(es)-deficit(parts,removed)
                    assert deficit(parts,removed)<=deficit(parts,set())+len(removed)
                    totals['abstract_withdrawal_optima']+=1
                assert 2*deficit(parts,set()) <= len(zero)
                totals['abstract_port_graphs']+=1


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args();totals=Counter();records=[];rng=random.Random(20261026)
    families=[('root',root_fixture()[0]),('control-singleton',singleton(8)),
              ('control-cycle',block('cycle',6,4)),('control-missing',block('missing',6,4))]
    for q in (1,2,3,4):
        families += [(f'chain{q}',chain(q)[0]),(f'cross{q}',capacity_cross(q)[0]),
                     (f'comb{q}',straight_comb(q)),
                     (f'control-sharp-missing{q}',stack(6,4,['missing']*q))]
    for w in (8,10,12):
        families += [(f'four{w}',four_way(w)[0]),(f'corner{w}',corner_join(w)[0])]
    for w,a,b,v,h in itertools.product(range(3,10),(1,3),(1,5),range(2),range(2)):
        families.append((f'cap{w},{a},{b},{v},{h}',capped(w,a,b,v,h,set())))
    for name,cur in families:
        for sym in itertools.product((False,True),repeat=3):
            shape,T,M=transformed(*cur,*sym);c=(*shape,T,M)
            records.append(check_physical(name+str(sym),c,totals,rng,pools=2))
        if name.startswith('control-sharp'):
            data,cap,keys,edges,parts,d4,boundary,slack=port_graph(cur)
            assert boundary == 0 and 2*deficit(parts,set()) == d4 == 2*len(edges) > 0
            totals['sharp_frozen_half_tax_controls']+=1
        if name=='control-cycle':
            data,cap,keys,edges,parts,d4,boundary,slack=port_graph(cur)
            cycles=[p for p in parts if p['cycle']]
            assert len(edges)==2 and len(cycles)==1 and not d4 and not boundary
            assert len(cycles[0]['vertices'])==2
            for u in cycles[0]['vertices']:
                assert deficit(parts,{u})==1
                totals['physical_shared_cycle_withdrawals']+=1
        if name in ('root','control-cycle','control-missing','chain2'):
            P={v for e in cur[3] for v in e};frozen,layers=frozen_certificate(cur);assert frozen==P
            totals['independent_frozen_rank_events']+=len(check_rank_certificate(cur,
                [[w['endpoint'] for w in wave] for wave in layers]))
    # Optional T additions preserve original degree-three endpoint neighbourhoods.
    for name,cur in families[:26]:
        if set(occupied_degrees(cur).values())!={3}:continue
        R,C,T0,M=cur;P={v for e in M for v in e}
        candidates=[v for v in itertools.product(range(R),range(C)) if v not in T0|P
                    and not set(neighbors(v))&P]
        for repeat in range(4):
            T=set(T0);O=T|P;order=candidates[:];rng.shuffle(order)
            for v in order:
                near=set(neighbors(v))&O
                if len(near)<=1 and not any(set(neighbors(t))&O for t in near):
                    T.add(v);O.add(v)
            records.append(check_physical('extension-'+name,(R,C,T,M),totals,rng,pools=2))
            totals['degree_three_selection_extensions']+=1
    abstract_controls(totals)
    result=dict(status='PASS',counts=dict(totals),records=records,
        theorem='Written general geometric port adapter; exact port deficit equals number of double-zero-ended paths; half-tax bound 2D<=degree4 alpha terminals+explicit boundary defects; arbitrary withdrawal formula by original path/cycle components; coefficient-one criterion d4+b<=2beta+1.',
        scope='Port certificate exact; full whole-support network only a lower bound. All original positive intervals including marked boundary units available initially. General raw rectangle boundary defects retained. Finite controls do not prove the universal statements. Universal5/6 open.')
    args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(status='PASS',counts=dict(totals))))


if __name__=='__main__':main()
