"""Unreserved fully frozen singleton collision; independent no-TT compiler.

Written all-height and all-copy proofs: FULL_POOL_SINGLETON_OBSTRUCTION.md.
The no-TT compiler allows BT boundary columns; published packet adapters remain
unchanged. Exhaustive terminal checks are controls, not general proofs.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_compensation_flow_normal_form import owner_data
from check_endpoint_component_resource_gluing import physical_groups, local, restrict
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_frozen_tip_slot_obstruction import independent_strands
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_whole_support_donor_collision import sealed
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import whole_support_data

if not __debug__:
    raise RuntimeError('Assertions required; run without -O.')


def fixture(width, raw=True, upper_closed=True):
    base, _ = sealed(width); r = width+4
    added = {(4,1),(r+1,1)}
    if upper_closed:
        added.add((4,11))
    if raw:
        added |= {(5,0),(r,0),(4,21),(r+1,21)}
    assert not added & (base[2] | {v for e in base[3] for v in e})
    return base[0], 22, base[2] | added, base[3]


def compile_no_tt(cur, bands, marked=False):
    """Independent physical strand/gap extraction, all cells, no TT columns.

    A raw resource identity is (original band, original BB column). The two
    boundary BB columns are excluded only when explicitly requested. Pure
    PP/M cycles are not credited or silently converted into path owners.
    """
    P = {v for e in cur[3] for v in e}
    assert {v for cols in bands for col in cols for v in col} == {
        (r,c) for r in range(cur[0]) for c in range(cur[1])}
    assert sum(2*len(cols) for cols in bands) == cur[0]*cur[1]
    kinds, comps = independent_strands(cur, bands)
    pairs = [tuple(sorted(tips)) for tips, _ in comps if tips]
    owner, A, B, M = owner_data(kinds, pairs)
    nodes = {}
    endpoint_owner = {v: owner[next(iter(tips))] for tips, body in comps if tips for v in body}
    for b, cols in enumerate(bands):
        for c, col in enumerate(cols):
            users = {endpoint_owner[v] for v in col if v in endpoint_owner}
            assert len(users) <= 1
            if users:
                nodes[b,c] = next(iter(users))
    labels = [[tuple(sorted('T' if v in cur[2] else 'P' if v in P else 'B' for v in col))
               for col in cols] for cols in bands]
    assert all(label != ('T','T') for row in labels for label in row)
    raw = {(b,c) for b,row in enumerate(labels) for c,label in enumerate(row) if label == ('B','B')}
    boundary = {(b,c) for b,row in enumerate(labels) for c in (0,len(row)-1) if (b,c) in raw}
    Q = raw-boundary if marked else raw
    support = {o:set() for o in range(len(pairs))}; gaps = []
    for b,row in enumerate(labels):
        c = 0
        while c < len(row):
            if 'P' in row[c]:
                c += 1; continue
            first = c
            while c < len(row) and 'P' not in row[c]:
                c += 1
            units = {(b,j) for j in range(first,c)} & raw
            for boundary_column in (first-1,c):
                if (b,boundary_column) in nodes:
                    support[nodes[b,boundary_column]] |= units & Q
            gaps.append(dict(band=b,first=first,last=c-1,raw_units=sorted(units)))
    links = []
    for cols in bands:
        for left,right in zip(cols,cols[1:]):
            for a,b in zip(left,right):
                if kinds.get(a) == 'TP' and kinds.get(b) == 'BP': links.append((a,b))
                if kinds.get(b) == 'TP' and kinds.get(a) == 'BP': links.append((b,a))
    assert all(sum(j in js for js in support.values()) <= 2 for j in Q)
    slack = cur[0]*cur[1]//2-len(cur[2])-len(cur[3])
    assert slack == len(raw)+len(B)-len(A)
    return (kinds,pairs,links,support,Q), dict(raw=raw,boundary=boundary,slack=slack,
        labels=labels,gaps=gaps,cycles=sum(not tips for tips,_ in comps))


def reachable(data, source):
    owner,A,B,M = owner_data(*data[:2]); assert not B
    seen = {source}; todo = [source]
    while todo:
        u = todo.pop()
        for a,b in data[2]:
            v = owner[b]
            if owner[a] == u and v not in seen:
                assert v in M
                seen.add(v); todo.append(v)
    return seen, set().union(set(), *(data[3][o] for o in seen))


def independent_terminal_optimum(data):
    """All legal terminal matchings, independent union/find and resource DFS.

    This does not call cancel_pairs, evaluate, brute, optimize, or a flow
    implementation. No-beta components each have one original alpha or none.
    """
    kinds,pairs,links,support,Q = data
    owner,A,B,_ = owner_data(kinds,pairs); assert not B
    best = (0,0); count = 0; histogram = Counter()
    def evaluate(chosen):
        nonlocal best,count
        parent = list(range(len(pairs)))
        def root(v):
            while parent[v] != v:
                v = parent[v]
            return v
        for a,b in chosen:
            ra,rb = root(owner[a]),root(owner[b]); parent[ra] = rb
        groups = {}
        for o in range(len(pairs)):
            groups.setdefault(root(o),set()).add(o)
        demands = []
        for g in groups.values():
            assert len(g & A) <= 1
            if g & A:
                demands.append(set().union(set(), *(support[o] for o in g)))
        assert len(demands) == len(A)
        def assign(i,used):
            if i == len(demands):return 0
            return max([assign(i+1,used)] + [1+assign(i+1,used|{j}) for j in demands[i]-used])
        value = assign(0,set()); candidate = (value,len(chosen))
        if (candidate[0],-candidate[1]) > (best[0],-best[1]):best = candidate
        histogram[value] += 1; count += 1
    def visit(i,used,chosen):
        if i == len(links):
            evaluate(chosen);return
        visit(i+1,used,chosen)
        edge = links[i]
        if not set(edge) & used:
            visit(i+1,used|set(edge),chosen+[edge])
    visit(0,set(),[])
    return best,count,dict(histogram)


def compare_old(cur,bands,totals):
    old,meta,_ = whole_support_data(cur,bands)
    new,_, = compile_no_tt(cur,bands,marked=True)
    owner,_,_,_ = owner_data(*new[:2])
    renumber = {o:owner[pair[0]] for o,pair in enumerate(old[1])}
    resource = {j:(x['band'],x['first']) for j,x in enumerate(meta['intervals'])}
    assert all(x['first'] == x['last'] for x in meta['intervals'])
    assert old[0] == new[0] and set(old[2]) == set(new[2])
    assert {resource[j] for j in old[4]} == new[4]
    assert all({resource[j] for j in js} == new[3][renumber[o]] for o,js in old[3].items())
    totals['legacy_adapter_exact_comparisons'] += 1


def inspect(cur,bands,units,expected_cost,totals,exhaust=False):
    direct_check(*cur)
    frozen,certificate = frozen_certificate(cur)
    layers = [[w['endpoint'] for w in layer] for layer in certificate]
    assert frozen == {v for e in cur[3] for v in e}
    rank = check_rank_certificate(cur,[list(layer) for layer in layers])
    data,meta = compile_no_tt(cur,bands)
    _,A,B,M = owner_data(*data[:2]); assert not B
    assert len(A) == 2*len(units) and len(M) == 14*len(units)
    seen = []; available = []
    for a in sorted(A):
        owners,resources = reachable(data,a)
        assert len(resources) == 1 and resources <= units
        seen.append(owners); available.append(resources)
        assert not data[3][a]
    assert Counter(next(iter(x)) for x in available) == Counter({j:2 for j in units})
    answer = fork_flow(*data)
    assert (answer['value'],answer['cost'],answer['deficit']) == (len(units),expected_cost,len(units))
    assert {tuple(x) for kind,x in answer['cut']} == units
    assert all(kind == 'interval' for kind,_ in answer['cut'])
    groups,_ = physical_groups(cur,data); active = [g for g in groups if g&A]
    assert len(active) == 2*len(units)
    local_values = []
    for g in active:
        v = fork_flow(*local(data,g,data[4])); no = fork_flow(*local(data,g,data[4]-units))
        assert v['value'] == 1 and no['value'] == 0
        local_values.append([v['value'],v['cost']])
    assert sorted(v[1] for v in local_values) == [1]*len(units)+[2]*len(units)
    if exhaust:
        optimum,count,hist = independent_terminal_optimum(data)
        assert optimum == (answer['value'],answer['cost'])
        totals['independent_terminal_matchings'] += count
    else:
        count = 0;hist = {}
    totals['frozen_raw_boards'] += 1
    return data,meta,dict(shape=cur[:2],selected=len(cur[2]),matching=len(cur[3]),
        raw_intervals=len(meta['raw']),boundary_BB=len(meta['boundary']),slack=meta['slack'],
        value=answer['value'],cost=answer['cost'],deficit=answer['deficit'],
        shared_units=sorted(units),local_value_cost=local_values,
        independent_terminal_matchings=count,terminal_value_histogram=hist),rank,layers


def main():
    p = argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    args = p.parse_args();totals = Counter();records = [];base_fixture = None
    for w in list(range(8,42,2))+[64,128]:
        cur = fixture(w);bands = whole_bands(cur);j = (w//2+2,11)
        data,meta,row,rank,layers = inspect(cur,bands,{j},1,totals,exhaust=w == 8)
        assert (row['selected'],row['matching'],row['raw_intervals'],row['slack'],row['boundary_BB']) == (41,3*w+10,8*w+83,8*w+81,w+8)
        # Check the exhaustive all-height support table used in the proof.
        r = w+4
        positive = {frozenset(data[1][o]):js for o,js in data[3].items() if js}
        assert positive == {
            frozenset(((r-1,7),(r-1,8))):{(r//2-1,c) for c in (9,10,11,12)},
            frozenset(((r-1,17),(r-1,18))):{(r//2-1,c) for c in (19,20,21)},
            frozenset(((r,8),(r,9))):{j},
            frozenset(((r,13),(r,14))):{j}}
        own,alphas,_,_ = owner_data(*data[:2])
        assert {frozenset(data[1][a]) for a in alphas} == {
            frozenset(((5,5),(r,5))),frozenset(((5,15),(r,15)))}
        assert len(data[2]) == 26
        assert sum(own[a] != own[b] for a,b in data[2]) == 12
        row['width_parameter'] = w;records.append(row)
        # Deleting just upper singleton's selection restores two independent
        # resources and full payment, with no change in endpoint geometry.
        control = fixture(w,upper_closed=False)
        dd,mm = compile_no_tt(control,whole_bands(control));flow = fork_flow(*dd)
        assert (flow['value'],flow['cost']) == (2,3)
        assert {j for a in owner_data(*dd[:2])[1] for j in reachable(dd,a)[1]} == {(2,11),(w//2+2,11)}
        totals['two_unit_repairs'] += 1
        # Original first-BB adapter, with only standard marks removed. No extra
        # reservations and no fixed old C. This is already an obstruction.
        marked = fixture(w,raw=False);compare_old(marked,whole_bands(marked),totals)
        md,mt = compile_no_tt(marked,whole_bands(marked),marked=True)
        ff = fork_flow(*md)
        assert (ff['value'],ff['cost'],len(md[4]),mt['slack']-len(mt['boundary'])) == (1,1,7*w+75,7*w+73)
        totals['original_boundary_convention_obstructions'] += 1
        if w == 8:
            base_fixture = dict(shape=cur[:2],selected=sorted(cur[2]),matching=cur[3],
                freezing_layers=[sorted(layer) for layer in layers],strict_rank_witnesses=rank,
                inventory=row,all_strands=[dict(ends=p,support=sorted(data[3][o])) for o,p in enumerate(data[1])],
                links=data[2])
    base = fixture(8);bands0 = whole_bands(base)
    for transpose,fr,fc in itertools.product((False,True),repeat=3):
        def move(v):
            r,c = v
            r = base[0]-1-r if fr else r
            c = base[1]-1-c if fc else c
            return (c,r) if transpose else (r,c)
        shape = base[:2][::-1] if transpose else base[:2]
        cur = (*shape,{move(v) for v in base[2]},[tuple(map(move,e)) for e in base[3]])
        bands = [[tuple(map(move,col)) for col in cols] for cols in bands0]
        inspect(cur,bands,{(6,11)},1,totals)
        totals['carried_band_isometries'] += 1
    for w,q in itertools.product((8,12,20),(2,3,5,8)):
        base = fixture(w);stride = base[0]
        move = lambda v,i:(v[0]+i*stride,v[1])
        cur = (stride*q,22,{move(v,i) for i in range(q) for v in base[2]},
               [tuple(move(v,i) for v in e) for i in range(q) for e in base[3]])
        units = {(w//2+2+i*stride//2,11) for i in range(q)}
        _,meta,row,_,_ = inspect(cur,whole_bands(cur),units,q,totals)
        assert row['raw_intervals'] == q*(8*w+83) and row['slack'] == q*(8*w+81)
        records.append(dict(width_parameter=w,copies=q,**row));totals['stacked_boards'] += 1
    # Independent compiler agrees exactly on old unmodified sealed fixtures.
    for w in (8,12,20):
        cur,_ = sealed(w);compare_old(cur,whole_bands(cur),totals)
    target = Path(__file__).parent/'fixtures'/'full_pool_singleton_obstruction.json'
    target.write_text(json.dumps(base_fixture,indent=2)+'\n')
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),records=records,
        scope='Independent no-TT physical compiler; complete raw pool and original marked pool; '
              'all-terminal matching base check. General proofs are written, not inferred from enumeration.',
        limits=['No claim of maximal selected set, globally optimal extremizer, or all mate surgeries.',
                'No universal target counterexample or 5/6 improvement.',
                'New raw adapter does not assert original BB-boundary packet hypotheses.']),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals)),indent=2))

if __name__ == '__main__':main()
