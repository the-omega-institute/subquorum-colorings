"""Compare the new single-relay formula with independent complete min-cost flow."""
from pathlib import Path
import json
import random
from corner_relay_shortest_path import solve_shortest_relay
from zero_defect_long_relay import long_extension_obstacle
from monochromatic_completion_flow import solve_completion_flow
from check_mixed_terminal_compensation import edge
from check_general_square_ports import physical_state

if not __debug__: raise RuntimeError('Assertions required')
ROOT=Path(__file__).resolve().parents[1]


def flip_rematching(m,p,rng,attempts):
    m=set(m);side=1+max(r for r,c in p)
    for _ in range(attempts):
        r=rng.randrange(side-1);c=rng.randrange(side-1)
        a,b,z,d=(r,c),(r,c+1),(r+1,c+1),(r+1,c)
        if not {a,b,z,d}<=p:continue
        horizontal={edge(a,b),edge(d,z)};vertical={edge(a,d),edge(b,z)}
        if horizontal<=m:m=(m-horizontal)|vertical
        elif vertical<=m:m=(m-vertical)|horizontal
    return m


def main():
    rng=random.Random(2026102744);rows=[];changed=positive=zero=0
    for k in range(1,9):
        f=long_extension_obstacle(k)
        for i in range(8):
            m=flip_rematching(f['M'],f['P'],rng,50*(i+1))
            if i%2:m={edge((a[1],a[0]),(b[1],b[0])) for a,b in m}
            weights={e:rng.randrange(19) for e in sorted(m)}
            if i==0:weights={e:1 for e in m}
            elif i==1:weights={e:0 for e in m}
            elif i==2:weights={e:10**400+7*j for j,e in enumerate(sorted(m))}
            s=solve_shortest_relay(k,m,weights)
            full=solve_completion_flow(f['side'],f['side'],m,f['T'],weights)
            assert full['TH_exactness_certified']
            assert s['minimum_TH_fee']==full['TH_fee']==full['all_terminal_cost']
            old=physical_state(f['board'],m,s['auxiliary'],f['T'])
            assert old['paid']==s['paid'] and old['data']['counts'][0]==0
            assert len(s['paid'])>=k
            changed+=m!=f['M'];positive+=s['minimum_TH_fee']>0;zero+=s['minimum_TH_fee']==0
            rows.append(dict(k=k,variant=i,changes_old_M=m!=f['M'],minimum_fee=s['minimum_TH_fee'],
                             paid_edges=len(s['paid']),path_length=len(s['path'])-1,
                             complete_flow_fee=full['TH_fee'],reached_vertices=s['reached_vertices']))
    # Larger construction controls use the general shortest-path proof rather
    # than pretending that exhaustive full-matching enumeration is feasible.
    large=[]
    for k in [16,32,64]:
        s=solve_shortest_relay(k)
        assert s['minimum_TH_fee']==len(s['paid'])==k
        large.append(dict(k=k,side=4*k+4,minimum_fee=k,path_length=len(s['path'])-1))
    out=dict(status='PASS',weighted_rematching_models=len(rows),changed_actual_matchings=changed,
             positive_optima=positive,zero_optima=zero,independent_complete_flow_comparisons=len(rows),
             controls=rows,large_families=large,
             scope='Exact weighted shortest relay versus existing complete min-cost flow on 64 physical rematchings/reweightings, including transpositions, domino flips, zero and 401-digit weights; older independent component extraction; canonical family to k=64.',
             proof_scope='All-k arbitrary-rematching and arbitrary nonnegative-weight equality follows from the written path lower bound and parity-completion construction. Neither finite checks nor the standard Dijkstra adapter are a new general shortest-path theorem. No Lean claim.')
    (ROOT/'output/corner-relay-shortest-path.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({key:out[key] for key in ['status','weighted_rematching_models','changed_actual_matchings','independent_complete_flow_comparisons']}))


if __name__=='__main__':main()
