#!/usr/bin/env python3
"""Non-vacuous symmetry/translation checks for the forced-companion moves.
Run from develop; the adjacent main checker supplies the exact definitions.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, random
from pathlib import Path
import verify_grid_short_path_compensation as core

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path('results/grid-short-path-symmetries-verification.json'))
    args=parser.parse_args();rng=random.Random(2026092706)
    T=sum(1<<v for v in (0,5,12,17,19,22))
    M=((1,2),(3,4),(7,13),(10,16),(8,9))
    count=promotions=flips=0
    for extra in ((),((14,15),)):
        for transpose in (False,True):
            height,width=(6,4) if transpose else (4,6)
            for flip_i,flip_j in itertools.product((False,True),repeat=2):
                for offset_i,offset_j in itertools.product((0,2,4),repeat=2):
                    def remap(v):
                        i,j=divmod(v,6)
                        if transpose:i,j=j,i
                        if flip_i:i=height-1-i
                        if flip_j:j=width-1-j
                        return (i+offset_i)*12+j+offset_j
                    tt=sum(1<<remap(v) for v in core.bits(T))
                    mm=tuple((remap(v),remap(w)) for v,w in M+extra)
                    assert core.feasible(core.graph(12,12)[0],tt,mm)
                    out=core.check(12,12,tt,mm,rng,normal=True)
                    assert out['sources']==1 and out['steps']==1
                    promotions+=out['promotions'];flips+=out['flips'];count+=1
    assert (count,promotions,flips)==(144,72,72)
    report={
        'scope':'Finite planted tests under all eight square symmetries and nine even translations; not a universal proof.',
        'seed':2026092706,'board':[12,12],'cases':count,
        'promotions':promotions,'flips':flips,
        'parent_sha256':hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'result':'ALL_LISTED_CHECKS_PASSED'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)
if __name__=='__main__':main()
