"""Physical fragment controls for shared-TH star compensation.

All-word classification and all-length constructions are proved in the note.
This checker verifies finite actual boards, full matchings and resource sets.
"""
from itertools import product
import json
from pathlib import Path

from check_mixed_terminal_compensation import (
    decompose, edge, grid, neighbours, selected_feasible,
)
from check_ordered_th_relay import all_gates, relay

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]


def word_counts(word):
    extended = ['T']+list(word)+['H']
    return tuple(sum((a, b) == pair for a, b in zip(extended, extended[1:]))
                 for pair in [('T','T'), ('H','H')])+(
        sum(a != b for a, b in zip(extended, extended[1:])),)


def family(word):
    assert word and set(word) <= {'T', 'H'}
    k = len(word); h, w = 6, 6*k+2
    m = {edge((3,0),(4,0)), edge((3,w-1),(4,w-1))}
    m |= {edge((3,c),(3,c+1)) for c in range(1,w-2,2)}
    n = {edge((3,c),(3,c+1)) for c in range(0,w,2)}
    n |= {edge((4,c),(5,c)) for c in range(w)}
    t = {(5,0)}; leaves = []
    centre = [(5,0),(4,0)]+[(3,c) for c in range(w)]+[(4,w-1),(5,w-1)]
    for j, kind in enumerate(word):
        c = 2+6*j
        path = [(0,c),(1,c),(2,c),(2,c+1),(2,c+2),(2,c+3),(1,c+3),(0,c+3)]
        leaves.append(path)
        m |= {edge(path[i],path[i+1]) for i in (1,3,5)}
        n |= {edge(path[i],path[i+1]) for i in (0,2,4,6)}
        n |= {edge((r,c+1),(r,c+2)) for r in (0,1)}
        if kind == 'T':
            t |= {path[0],path[-1]}
    for j in range(k+1):
        c = 6*j
        n |= {edge((r,c),(r,c+1)) for r in range(3)}
    return dict(h=h,w=w,M=sorted(m),N=sorted(n),T=t,
                centre=centre,leaves=leaves,squares=[(2,2+6*j) for j in range(k)])


def analyse_star(board, m, n, t, centre, leaves, gates):
    before = decompose(board,m,n,t); paths = before['paths']
    index = {frozenset(p['vertices']): i for i,p in enumerate(paths)}
    ci = index[frozenset(centre)]
    assert paths[ci]['kind']=='TH'
    if centre[-1] in t:
        centre = list(reversed(centre))
    assert centre[0] in t and centre[-1] in before['H']
    li = [index[frozenset(p)] for p in leaves]
    assert len(set([ci]+li)) == len(li)+1 == len(gates)+1
    assert all(paths[i]['kind'] in {'TT','HH'} for i in li)
    positions = {edge(u,v): j for j,(u,v) in enumerate(zip(centre,centre[1:]))}
    seen = set(); ordered = []
    for leaf_id, g in zip(li,gates):
        assert g['ids']=={ci,leaf_id}
        assert not seen & g['vertices']; seen |= g['vertices']
        assert not g['old'] & set(m) and not g['new'] & set(m)
        ordered.append((positions[g['cut'][ci]],leaf_id,g))
    ordered.sort(key=lambda x:x[0])
    word = ['T' if paths[i]['kind']=='TT' else 'H' for _,i,_ in ordered]
    current = set(n)
    for _,_,g in ordered:
        assert g['old']<=current
        current = current-g['old']|g['new']
    after = decompose(board,m,sorted(current),t)
    assert before['path_M']==after['path_M']
    assert set(m)&set(n)==set(m)&current
    affected = set(centre).union(*(set(paths[i]['vertices']) for i in li))
    outputs = [p for p in after['paths'] if set(p['vertices'])&affected]
    assert len(outputs)==len(li)+1
    assert set().union(*(set(p['vertices']) for p in outputs))==affected
    assert all(set(p['vertices'])<=affected for p in outputs)
    counts = tuple(sum(p['kind']==kind for p in outputs) for kind in ['TT','HH','TH'])
    assert counts==word_counts(word)
    cuts = [p for p,_,_ in ordered]
    fragments = [centre[a:b+1] for a,b in zip([0]+[x+1 for x in cuts],cuts+[len(centre)-1])]
    assert len(fragments)==len(li)+1
    assert sum(map(len,fragments))==len(centre)
    extended = ['T']+word+['H']; output_m=[]; used=set(); fragment_owners=set()
    for j,frag in enumerate(fragments):
        matches = [p for p in outputs if set(frag)<=set(p['vertices'])]
        assert len(matches)==1
        p=matches[0]
        owner=tuple(p['vertices']);assert owner not in fragment_owners;fragment_owners.add(owner)
        kind = 'TH' if extended[j]!=extended[j+1] else extended[j]*2
        assert p['kind']==kind
        assert not used & p['M']; used |= p['M']; output_m.append(p['M'])
    original = set().union(*(paths[i]['M'] for i in [ci]+li))
    assert used==original
    paid = set().union(*(p['M'] for p in after['paths'] if p['kind']=='TH'))
    old_paid = set().union(*(p['M'] for p in paths if p['kind']=='TH'))
    if counts[:2]==(0,0):
        bad = set().union(*(paths[i]['M'] for i in li))
        assert not old_paid&bad and paid==old_paid|bad
    fully_alternating = all(a!=b for a,b in zip(extended,extended[1:]))
    assert (counts[:2]==(0,0))==fully_alternating
    return dict(word=''.join(word), star_counts=counts,
                before=before['counts'],after=after['counts'],
                fragment_costs=[len(x) for x in output_m],
                paid_M=len(paid), old_paid_M=len(old_paid),
                all_repaired=fully_alternating, auxiliary=sorted(current),
                leaf_ids=[i for _,i,_ in ordered], centre_id=ci, original=before)


def control(word, individual_pairs=False):
    d=family(word); h,w,m,n,t=[d[x] for x in ['h','w','M','N','T']]
    board=grid(h,w);p={u for e in m for u in e}
    assert selected_feasible(p,t)
    initial=decompose(board,m,n,t)
    by_square={g['square']:g for g in all_gates(h,w,n,initial)}
    gates=[by_square[x] for x in d['squares']]
    result=analyse_star(board,m,n,t,d['centre'],d['leaves'],gates)
    k=len(word);tt=word.count('T');hh=word.count('H')
    assert len(m)==6*k+2 and len(t)==2*tt+1 and len(initial['H'])==24*k+7-2*tt
    assert initial['counts']==(tt,11*k+hh+3,1)
    assert result['fragment_costs']==[3]+[6]*(k-1)+[5]
    expected=sum(cost for cost,a,b in zip(result['fragment_costs'],['T']+list(word),list(word)+['H']) if a!=b)
    assert result['paid_M']==expected and result['old_paid_M']==3*k+2
    # Complete disjoint adjacent payments, independent of N and its chosen switches.
    payments=[((5,0),(5,1))]
    for j,letter in enumerate(word):
        if letter=='T':
            c=2+6*j;payments += [((0,c),(0,c+1)),((0,c+3),(0,c+2))]
    assert {u for u,v in payments}==t and len({v for u,v in payments})==len(t)
    assert all(v in initial['H'] and v in neighbours(u) for u,v in payments)
    pair_controls=0 if individual_pairs else None
    if individual_pairs:
        for out,j in enumerate(word):
            if j!='H':continue
            for incoming in range(out+1,k):
                if word[incoming]!='T':continue
                ids=result['leaf_ids']
                outp=relay(h,w,m,n,t,[ids[incoming],result['centre_id'],ids[out]],
                           [gates[incoming],gates[out]])
                assert outp['after']==(tt-1,11*k+hh+2,3)
                pair_controls+=1
    return dict(contacts=k,word=word,T=len(t),H=len(initial['H']),M=len(m),
                J=len(t)+len(m),area=len(board),before=initial['counts'],
                after=result['after'],star_counts=result['star_counts'],
                fragment_costs=result['fragment_costs'],paid_M=result['paid_M'],
                old_paid_M=result['old_paid_M'],individual_ordered_pairs=pair_controls,
                complete_unrestricted_payment_cost=0)


def main():
    rows=[control(''.join(word)) for k in range(1,9) for word in product('HT',repeat=k)]
    positive=[];obstruction=[];pair_controls=0
    for s in range(1,41):
        good=control('HT'*s);bad=control('H'*s+'T'*s,individual_pairs=s<=8)
        assert good['after']==(0,22*s+3,2*s+1) and good['paid_M']==12*s+2
        assert bad['after']==(s-1,23*s+2,3) and bad['paid_M']==14
        assert bad['star_counts']==(s-1,s-1,3)
        if s<=8:
            assert bad['individual_ordered_pairs']==s*s
        positive.append(good);obstruction.append(bad);pair_controls+=bad['individual_ordered_pairs'] or 0
    result=dict(status='PASS',all_short_actual_words=len(rows),
                all_short_words_selected_degree_feasible=True,
                all_short_fragment_and_resource_ledgers_pass=True,
                positive_family_parameters=len(positive),obstruction_parameters=len(obstruction),
                individual_ordered_relay_controls=pair_controls,
                smallest_obstruction=obstruction[1],largest_obstruction=obstruction[-1],
                largest_positive=positive[-1],
                trust_boundary='General shared-star word classification and resource-fragment theorem, arbitrary-s actual construction and Hall overestimate proof are written. Enumeration validates finite actual instances only. The obstruction concerns the specified simultaneous contacts; every constructed board has a zero-M unrestricted payment. No universal5/6 improvement or full geometric Lean is claimed.')
    (ROOT/'output/shared-th-star.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',words=len(rows),positive=len(positive),
                          obstruction=len(obstruction),individual_pairs=pair_controls,
                          largest_bad_counts=obstruction[-1]['after'],
                          largest_good_counts=positive[-1]['after'],
                          largest_bad_paid_M=obstruction[-1]['paid_M'],
                          largest_good_paid_M=positive[-1]['paid_M'])))


if __name__=='__main__':
    main()
