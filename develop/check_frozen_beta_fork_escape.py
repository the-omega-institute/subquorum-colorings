"""Solver-free geometric escape lemma controls and a pure-cycle witness.

General geometric and ownership proofs are in FROZEN_BETA_FORK_ESCAPE.md.
Discovery output is not used as a proof. Every fixture is rebuilt and checked.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path

from check_compensation_flow_normal_form import owner_data
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_frozen_tip_slot_obstruction import independent_strands
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_whole_support_fork_normal_form import whole_support_data, ordinary_flow

FIXTURE = Path(__file__).parent/'fixtures/frozen_beta_fork_escape.json'
if not __debug__:
    raise RuntimeError('Run without -O; assertions are required.')


def fixture(copies=1,padding=0,plug=False):
    assert copies >= 1 and padding >= 0 and padding%2 == 0
    j = json.loads(FIXTURE.read_text())
    maps = [lambda v,i=i:(v[0]+12*i,v[1]) for i in range(copies)]
    current = (12*copies,14+padding,
        {f(tuple(v)) for f in maps for v in j['selected']},
        [tuple(f(tuple(v)) for v in edge) for f in maps for edge in j['matching']])
    layers = [[f(tuple(w['endpoint'])) for f in maps for w in layer] for layer in j['freezing_layers']]
    if plug:
        current = (*current[:3],current[3]+[(f((6,7)),f((7,7))) for f in maps])
        layers.append([f(v) for f in maps for v in ((6,7),(7,7))])
    return current,layers


def scan(current,bands,totals):
    """Horizontal aligned-band instance of the coordinate-invariant lemma."""
    direct_check(*current)
    frozen,layers = frozen_certificate(current)
    mate = {v:w for edge in current[3] for v,w in (edge,edge[::-1])}
    assert frozen == set(mate)
    rank = {tuple(w['endpoint']):i for i,layer in enumerate(layers) for w in layer}
    data,meta,_ = whole_support_data(current,bands)
    owner,aa,bb,mm = owner_data(*data[:2])
    kinds,bodies = independent_strands(current,bands)
    assert kinds == data[0]
    body_of = {v:i for i,(tips,body) in enumerate(bodies) for v in body}
    motifs = []
    for a in sorted(kinds):
        if kinds[a] != 'TP' or owner[a] not in aa:
            continue
        r,c = a
        eps = 1 if r%2 else -1
        for s in (-1,1):
            b,m,n = (r,c-s),(r,c-2*s),(r,c+s)
            if kinds.get(b) != 'BP' or owner[b] not in bb or kinds.get(m) != 'TP':
                continue
            # The stronger outer-T exclusion is checked before the BP case.
            assert n not in current[2]
            if kinds.get(n) != 'BP':
                continue
            am,bm,z,h = (r+eps,c),(r+eps,c-s),(r+eps,c+s),(r+2*eps,c)
            assert mate[a] == am and mate[b] == bm
            assert z in mate and h in set(mate)|current[2]
            assert rank[mate[z]] < rank[am] < rank[b]
            assert mate[n] == (r,c+2*s)
            assert rank[am] < rank[n]
            assert (r+2*eps,c+s) not in current[2]
            assert kinds.get(z) != 'TP'
            if len(bodies[body_of[a]][1]) == 2:
                assert kinds[z] == 'BP'
                totals['short_alpha_opposite_tip_bp_bypasses'] += 1
            tips,body = bodies[body_of[z]]
            kind = 'cycle' if not tips else ('alpha' if owner[next(iter(tips))] in aa
                else 'beta' if owner[next(iter(tips))] in bb else 'mixed')
            motifs.append(dict(alpha=a,beta=b,other_tp=m,outer_bp=n,escape=z,
                alpha_owner=owner[a],escape_body=body_of[z],escape_kind=kind,
                escape_body_size=len(body),rank_escape_mate=rank[mate[z]],
                rank_alpha_mate=rank[am],rank_beta=rank[b]))
    assert len({m['escape'] for m in motifs}) == len(motifs)
    by_cycle = defaultdict(set)
    for m in motifs:
        if m['escape_kind'] == 'cycle' and m['escape_body_size'] == 2:
            by_cycle[m['escape_body']].add(m['alpha_owner'])
    assert all(len(owners) <= 1 for owners in by_cycle.values())
    totals['frozen_systems'] += 1
    totals['fork_motifs'] += len(motifs)
    totals['pure_two_point_cycle_escapes'] += sum(m['escape_kind']=='cycle' and m['escape_body_size']==2 for m in motifs)
    return motifs,data,meta


def physical_family(totals):
    records = []
    for q,padding,plug in itertools.product(range(1,13),(0,2,10),(False,True)):
        current,layers = fixture(q,padding,plug)
        check_rank_certificate(current,layers)
        motifs,data,_ = scan(current,whole_bands(current),totals)
        critical = [m for m in motifs if m['alpha'] in {(5+12*i,5) for i in range(q)}]
        assert len(critical) == q
        for i in range(q):
            m = next(m for m in critical if m['alpha']==(5+12*i,5))
            assert m['escape']==(6+12*i,6)
            assert m['escape_kind']=='cycle' and m['escape_body_size']==2
            if plug:
                endpoints = {v for e in current[3] for v in e}
                assert {(r+12*i,c) for r in (6,7) for c in (5,7)} <= endpoints
        owner,aa,bb,mm = owner_data(*data[:2])
        assert (len(aa),len(bb),len(mm)) == (q,q,2*q)
        flow = ordinary_flow(*data)
        assert (flow['value'],flow['cost']) == (q,0)
        metadata = whole_support_data(current,whole_bands(current))[1]
        for a_owner in aa:
            source = next(v for v in data[1][a_owner] if v[1] == 5)
            i = (source[0]-5)//12
            support_keys = {(metadata['intervals'][j]['band'],metadata['intervals'][j]['first'],
                metadata['intervals'][j]['last']) for j in data[3][a_owner]}
            expected = {(2+6*i,12,12),(4+6*i,10,10)}
            if not plug:
                expected.add((3+6*i,7,7))
            assert expected <= support_keys
            if padding == 0:
                assert support_keys == expected
        if plug:
            original,_ = fixture(q,padding)
            old,oldmeta,_ = whole_support_data(original,whole_bands(original))
            newmeta = whole_support_data(current,whole_bands(current))[1]
            keys = lambda model,metadata:{(metadata['intervals'][j]['band'],metadata['intervals'][j]['first'],
                metadata['intervals'][j]['last']) for j in model[4]}
            removed = {(3+6*i,7,7) for i in range(q)}
            assert keys(old,oldmeta)-removed == keys(data,newmeta)
            assert len(old[4])-len(data[4]) == q
            assert {frozenset(p) for p in old[1]} == {frozenset(p) for p in data[1]}
            totals['exact_interval_deletion_comparisons'] += 1
        totals['explicit_copy_padding_boards'] += 1
        records.append(dict(copies=q,padding=padding,plug=plug,forced_cycle_sites=q,
            adjacent_gap_units_per_forced_cycle=0 if plug else 1,
            new_open_owner_resources_from_these_cycles=0,payment=q,minimum_links=0))
    # All eight square images, with bands, ranks and critical points carried
    # together. Inspect the expected motif directly in the original frame.
    for plug,transpose,fr,fc in itertools.product((False,True),repeat=4):
        base,layers = fixture(plug=plug)
        def move(v):
            r,c = v
            r = base[0]-1-r if fr else r
            c = base[1]-1-c if fc else c
            return (c,r) if transpose else (r,c)
        shape = base[:2][::-1] if transpose else base[:2]
        current = (*shape,{move(v) for v in base[2]},[tuple(map(move,e)) for e in base[3]])
        bands = [[tuple(map(move,col)) for col in band] for band in whole_bands(base)]
        direct_check(*current)
        check_rank_certificate(current,[[move(v) for v in layer] for layer in layers])
        assert len(frozen_certificate(current)[0]) == (52 if plug else 50)
        data,_,_ = whole_support_data(current,bands)
        _,bodies = independent_strands(current,bands)
        cycle = {move((6,6)),move((7,6))}
        assert any(not tips and body == cycle for tips,body in bodies)
        assert ordinary_flow(*data)['value'] == 1
        totals['carried_band_isometries'] += 1
    return records


def survey(totals):
    from check_compensation_flow_geometry_frontier import pad_image
    from check_elbow_sources import elbow
    from check_exchange_terminal_nonunique import fixture as bent, matching_orders, graft
    from check_frozen_beta_support_fork import fixture as fork
    from check_frozen_first_destination_allocation import fixture as unported
    from check_frozen_shared_mixed_gate import fixture as shared
    from check_frozen_tip_slot_obstruction import fixture as tip
    from check_interval_connector_cycles_and_missing_ports import stack
    from degree_three_fusion import occupied_bands
    from rotor_networks import rotor,combine,star_modules,transform_module
    base = bent()
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
    sources += [('new_cycle_escape',fixture()[0]),('plugged_cycle_escape',fixture(plug=True)[0])]
    counts = Counter()
    for (name,raw),sym,offset in itertools.product(sources,itertools.product((False,True),repeat=3),itertools.product((2,3),repeat=2)):
        current = pad_image(raw,sym,offset)
        if len(frozen_certificate(current)[0]) != 2*len(current[3]):
            totals['nonfrozen_survey_alignments_excluded'] += 1
            continue
        motifs,_,_ = scan(current,whole_bands(current),totals)
        counts[name,len(motifs)] += 1
        totals['survey_boards'] += 1
    return [dict(family=k[0],motifs=k[1],boards=v) for k,v in sorted(counts.items())]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    totals = Counter()
    family_records = physical_family(totals)
    survey_records = survey(totals)
    report = dict(status='PASS',totals=dict(totals),physical_family=family_records,survey=survey_records,
        scope='Written geometric rank/outward-mate and injective-site lemmas; pure two-point cycle escapes '
        'belong to at most one distinct alpha owner. Explicit actual frozen cycle witness, all-copy proof, '
        'no inference that P sites or cycles are new beta/interval resources. No frozen live-gate realization '
        'or universal compensation/5/6 improvement.')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__ == '__main__':
    main()
