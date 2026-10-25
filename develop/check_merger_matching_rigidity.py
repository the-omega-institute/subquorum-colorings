"""Check explicit closed-trap proofs; enumerate matchings only as controls.

The certificate proof uses leaf forcing and nonempty blocked endpoint sets.
It never enumerates perfect matchings. --refresh-certificate discovers a
certificate, which the independent checker then replays from the raw graph.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

from check_merger_completion_reserves import (
    STATES, complete, feasible, frozen, inspect, load, neighbors, whole_bands,
)
from check_rematching_receiver_flux import canonical, perfect_matchings
from check_exchange_terminal_nonunique import fixture as nonunique_fixture

if not __debug__:
    raise RuntimeError('Run without -O.')

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT/'develop/fixtures/merger_matching_rigidity_certificate.json'


def edges(P):
    return {tuple(sorted((v,w))) for v in P for w in neighbors(v) if w in P}


def options(E,v):
    return {w if u==v else u for u,w in E if v in (u,w)}


def force(E,e):
    return {a for a in E if a==e or not set(a)&set(e)}


def leaf_reduce(P,E):
    E=set(E);done=set();proof=[]
    while True:
        change=False
        for v in sorted(P-done):
            O=options(E,v)
            if not O:
                return E,proof,v
            if len(O)==1:
                w=next(iter(O));reduced=force(E,tuple(sorted((v,w))))
                if reduced!=E:
                    proof.append((v,w))
                E=reduced
                done|={v,w};change=True
        if not change:
            return E,proof,None


def replay_leaves(P,E,proof):
    E=set(E)
    for v,w in proof:
        assert v in P and options(E,v)=={w}
        E=force(E,tuple(sorted((v,w))))
    return E


def upper_neighbors(P,T,E,U,v):
    # ANY possible mate outside U is granted, independently for each neighbor.
    return set(neighbors(v)) & (T|{y for y in P if options(E,y)-U})


def is_trap(P,T,E,U):
    return bool(U) and U<=P and all(len(upper_neighbors(P,T,E,U,v))<=1 for v in U)


def discover_trap(P,T,E):
    F=set()
    while True:
        newly={v for v in P if len(upper_neighbors(P,T,E,P-F,v))>=2}-F
        if not newly:
            break
        F|=newly
    U=P-F
    if not U:
        return set()
    changed=True
    while changed:
        changed=False
        for v in sorted(U):
            if is_trap(P,T,E,U-{v}):
                U.remove(v);changed=True;break
    assert is_trap(P,T,E,U)
    return U


def helpers(current):
    P={v for e in current[3] for v in e}
    return {v for p in P for v in neighbors(p)
            if 0<=v[0]<current[0] and 0<=v[1]<current[1]
            and v not in P|current[2]
            and feasible((*current[:2],current[2]|{v},current[3]))}


def discover(current):
    P={v for e in current[3] for v in e};T=current[2]|helpers(current)
    E=edges(P);steps=[]
    while True:
        E,leaves,empty=leaf_reduce(P,E);assert empty is None
        if leaves:
            steps.append(dict(kind='leaves',pairs=leaves))
        removed=False
        for e in sorted(E):
            if len(options(E,e[0]))==1:
                continue
            branch,ls,empty=leaf_reduce(P,force(E,e))
            U=set() if empty else discover_trap(P,T,branch)
            if empty or U:
                step=dict(kind='exclude',edge=e,leaves=ls)
                if empty:
                    step['empty_vertex']=empty
                else:
                    step['trap']=sorted(U)
                steps.append(step);E.remove(e);removed=True;break
        if not removed:
            break
    assert E==canonical(current[3])
    return dict(helpers=sorted(helpers(current)),steps=steps)


def check_certificate(current,record):
    P={v for e in current[3] for v in e};H=helpers(current)
    assert set(map(tuple,record['helpers']))==H
    T=current[2]|H;E=edges(P);traps=[];leaf_count=0
    for step in record['steps']:
        ls=[tuple(map(tuple,pair)) for pair in step.get('pairs',step.get('leaves',[]))]
        if step['kind']=='leaves':
            E=replay_leaves(P,E,ls);leaf_count+=len(ls);continue
        assert step['kind']=='exclude'
        e=tuple(map(tuple,step['edge']));assert e in E
        branch=replay_leaves(P,force(E,e),ls)
        if 'empty_vertex' in step:
            v=tuple(step['empty_vertex']);assert v in P and not options(branch,v)
        else:
            U=set(map(tuple,step['trap']));assert is_trap(P,T,branch,U)
            traps.append(dict(edge=e,trap=sorted(U),
                possible_retained_neighbors=[dict(endpoint=v,neighbors=sorted(upper_neighbors(P,T,branch,U,v))) for v in sorted(U)]))
        E.remove(e)
    assert E==canonical(current[3])
    assert all(len(options(E,v))==1 for v in P)
    return dict(endpoint_count=len(P),helper_selections=sorted(H),
                leaf_forcings=leaf_count,excluded_edges=len(traps),traps=traps)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--refresh-certificate',action='store_true');a=ap.parse_args()
    _,base=load();good=[s for s in STATES if s[0] not in ('inner_beta','outer_beta')]
    if a.refresh_certificate:
        CERT.write_text(json.dumps({s[0]:discover(complete(base,s)) for s in good},indent=2)+'\n')
    certificates=json.loads(CERT.read_text());proofs={};counts={};totals=Counter()
    for state in good:
        cur=complete(base,state);P={v for e in cur[3] for v in e}
        proofs[state[0]]=check_certificate(cur,certificates[state[0]])
        totals['certificate_states']+=1;totals['closed_trap_exclusions']+=proofs[state[0]]['excluded_edges']
        H=helpers(cur);frozen_matchings=[];all_count=0
        # Independent exhaustive controls, NOT used by check_certificate.
        for matching in perfect_matchings(P):
            all_count+=1;optimistic=(*cur[:2],cur[2]|H,list(matching))
            if frozen(optimistic):
                assert canonical(matching)==canonical(cur[3]);frozen_matchings.append(matching)
        assert len(frozen_matchings)==1
        counts[state[0]]=dict(perfect_matchings=all_count,optimistically_frozen=1)
        totals['independent_matching_controls']+=all_count
        # Every compatible subset of helpful selections; the simultaneous
        # optimistic union need not itself be feasible.
        hs=sorted(H)
        for mask in range(1<<len(hs)):
            final=(*cur[:2],cur[2]|{v for i,v in enumerate(hs) if mask>>i&1},cur[3])
            if feasible(final):
                assert frozen(final);inspect(final,whole_bands(final),[0],totals,independent=True)
                totals['feasible_helper_subsets']+=1
    # The other two fixed endpoint shapes cannot freeze under ANY matching:
    # w has only two occupied neighbors, and one must be its mate. Verify a
    # singleton trap under each possible incident matching edge, without
    # enumerating global matchings.
    for state in STATES:
        if state[0] not in ('inner_beta','outer_beta'):
            continue
        cur=complete(base,state);P={v for e in cur[3] for v in e}
        T=cur[2]|helpers(cur);w=(5,4);E=edges(P)
        assert len(set(neighbors(w))&(P|T))==2
        for z in options(E,w):
            assert is_trap(P,T,force(E,tuple(sorted((w,z)))),{w})
            totals['bad_shape_incident_pair_traps']+=1
        totals['bad_fixed_endpoint_shapes_excluded']=1+totals['bad_fixed_endpoint_shapes_excluded']
    # Guard against accidentally claiming global frozen-matching uniqueness.
    nonunique=nonunique_fixture()
    assert len(nonunique)==4
    Q={v for e in nonunique[3] for v in e}
    controls=[M for M in perfect_matchings(Q) if frozen((*nonunique[:3],list(M)))]
    assert len(controls)==2
    totals['known_fully_frozen_nonunique_controls']=2
    a.output.write_text(json.dumps(dict(status='PASS',proof_method='explicit leaf forcing and closed-trap certificates; no perfect matching enumeration in proof checker',
        scope='Four fixed endpoint states of active merger, arbitrary feasible selected supersets and arbitrary actual perfect matching; all-q separated copies follow by locality. Arbitrary endpoint additions/rematching of a larger endpoint graph remain OPEN.',
        totals=dict(totals),independent_matching_counts=counts,certificates=proofs),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals),independent_matching_counts=counts)))


if __name__=='__main__':
    main()
