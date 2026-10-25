"""Discovery-only seam footprint audit. No all-copy compensation assertion."""
import argparse
import json
from pathlib import Path
from check_conditional_fresh_tip_closure import (load_model, base_copies, endpoints,
    partner, shift, PROTECTED, FLEX, static_certificate, neighbors)

if not __debug__: raise RuntimeError('Run without -O.')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    base,*_=load_model();old,_=static_certificate(base);records=[]
    for n in (1,2,3,4):
        cur=base_copies(base,n);P=endpoints(cur);O=P|cur[2]
        board={(r,c) for r in range(28) for c in range(24*n)}
        K={shift(v,i) for v,w in PROTECTED for i in range(n)}
        S={v for v in board if 0<v[1]<24*n-1 and v not in O and partner(v) not in O
           and not set(neighbors(partner(v)))&O and not set(neighbors(v))&cur[2]}-K
        F={v for v in board if v[1]==0 or (v not in O and set(neighbors(v))&cur[2])}
        Q={shift(t[1],i) for t in old for i in range(n)}|{shift(w,i) for v,w in FLEX+PROTECTED for i in range(n)}|{shift((3,13),i) for i in range(n)}
        transverse=lambda v:(v[0]+(-1 if v[0]%2==0 else 1),v[1])
        remaining={v for v in S if transverse(v) in board-F and partner(transverse(v)) not in F}
        horizontal=[(v,w) for v in sorted(S) for w in sorted(Q) if v[0]==w[0] and w in neighbors(v)]
        assert not horizontal
        seams=[v for v in sorted(remaining) if v[1]%24 in (0,23)]
        # A measured pattern for four finite footprints, not an arbitrary-n proof.
        assert len(S)==39*n+28*(n-1) and len(remaining)==4*n+18*(n-1)
        records.append(dict(copies=n,necessary_unprotected_candidates=len(S),
            residual_after_untouched_mixed_exclusions=len(remaining),
            new_seam_tip_candidates=seams,horizontal_possible_target_collisions=horizontal))
    out=dict(status='PASS',scope='Finite necessary-geometry discovery only, n=1,2,3,4. No assertion that these candidates can be activated, frozen, or paired simultaneously. No all-copy loss or compensation theorem.',records=records)
    args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(status='PASS',counts=[(r['copies'],r['necessary_unprotected_candidates'],r['residual_after_untouched_mixed_exclusions']) for r in records])))

if __name__=='__main__':main()
