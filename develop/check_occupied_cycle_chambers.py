"""Occupied-shadow chambers: general proof adapters and actual controls.

No SAT dependency. The optional discovery script is separate.
"""
import argparse,itertools,json
from collections import Counter
from pathlib import Path
from check_merger_completion_reserves import feasible,frozen,neighbors,owner_data,whole_bands,whole_support_data
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize

def scaffold(bottom=12,left=5,right=10):
    assert bottom%2==0 and bottom>=12 and (right-left)%2==1 and right-left>=5
    M=[]
    for row,step in ((5,1),(bottom,-1)):
        first,last=left+1,right-1
        M.extend([((row,first),(row+step,first)),((row,last),(row+step,last))])
        for c in range(first,last):
            r=row+2*step if (c-first)%2==0 else row+step
            M.append(((r,c),(r,c+1)))
    for c in (left-1,right+1):
        M.extend([((r,c),(r+1,c)) for r in range(5,bottom,2)])
    roots=[(5,left),(5,right),(bottom,right),(bottom,left)]
    M.extend((v,(v[0]+(1 if v[0]==5 else -1),v[1])) for v in roots)
    T={(r,c) for r in (4,bottom+1) for c in (left-1,left+1,right-1,right+1)}
    blank={(4,left),(4,right),(bottom+1,left),(bottom+1,right)}
    return T,M,roots,blank


def chamber(left,right):
    return {(r,c) for r in range(5,13) for c in (left,right)} | {
        (r,c) for r in (8,9) for c in range(left,right+1)}


def frame_proof(right,totals):
    left=5;T,M,roots,blank=scaffold(12,left,right)
    # The source matching alone is fixed; central gate edges are NOT needed.
    sourceM=M[:-4];F={v for e in sourceM for v in e};C=chamber(left,right)
    assert not F&C
    mate={v:w for e in sourceM for v,w in (e,e[::-1])}
    assert all(mate[v] in F for v in F)
    # These are coordinate proof obligations for ANY feasible extension.
    # Not a check of finitely many matchings/selected extensions.
    for v in C:
        assert set(neighbors(v)) <= C|F|blank
        q=(v[0]^1,v[1])
        if v in roots:
            assert q in blank
        else:
            assert q in C
            witnesses=(set(neighbors(q))&F)-{v}
            assert witnesses, 'Any selected band partner would see P(v) and this old wall P.'
    totals['coordinate_chamber_certificates']+=1
    totals['arbitrary_extension_boundary_checks']+=len(C)
    return dict(width=right-left,chamber_points=len(C),fixed_source_endpoints=len(F),gate_count=4)


def actual(record):
    return (*record['shape'],set(map(tuple,record['selected'])),[tuple(map(tuple,e)) for e in record['matching']])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    totals=Counter();families=[frame_proof(right,totals) for right in range(10,51,2)]
    records={}
    fixture=Path(__file__).parent/'fixtures/frozen_wider_cycle_chamber.json'
    if fixture.exists():
        record=json.loads(fixture.read_text());cur=actual(record)
        assert feasible(cur) and frozen(cur)
        layers=[[tuple(v) for v in layer] for layer in record['freezing_layers']]
        check_rank_certificate(cur,layers)
        d,meta,_=whole_support_data(cur,whole_bands(cur));o,aa,bb,mm=owner_data(*d[:2])
        T,M,roots,blank=scaffold(record['bottom'],5,record['right'])
        canonical=lambda es:{tuple(sorted(e)) for e in es}
        assert T<=cur[2] and canonical(M)<=canonical(cur[3])
        assert not blank & (cur[2]|{v for e in cur[3] for v in e})
        gates=[o[v] for v in roots]
        assert len(aa)==4
        assert gates[0]==gates[3] and gates[0] in bb and gates[1] in mm and gates[2] in bb
        full=fork_flow(*d);brute=optimize(*d)
        assert (full['value'],full['cost'])==(brute['value'],brute['cost'])
        records['wider_frozen']=dict(endpoints=2*len(cur[3]),selected=len(cur[2]),alpha=len(aa),beta=len(bb),
            gate_kinds=['beta','mixed','beta','beta'],first_last_gate_same_beta=True,value=full['value'],cost=full['cost'])
        totals['actual_strict_freezing_certificates']+=1;totals['independent_physical_packs']+=1
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),families=families,actual=records,
      scope='General shadow-exclusion and matching/PP closure theorem written; arbitrary-width thin frame has no TP in chamber in ANY feasible source-matching-retaining extension, so its gate paths are beta, not mixed. Wider frozen control shows chamber shadow hypothesis is essential. General mixed cycle realization and5/6 remain open.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals),actual=records)))

if __name__=='__main__':main()
