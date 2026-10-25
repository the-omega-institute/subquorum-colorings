"""Check the sharp central-inventory refinement of the all-T frontier.
Written general proof: FROZEN_SELECTION_REPAIR_FRONTIER.md, Section4.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_frozen_selection_frontier import configuration, schedule, inspect, check_rank_certificate

if not __debug__:raise RuntimeError('Assertions required; no -O.')


def inventory_schedule(w,k):
    order=[v for layer in schedule(w,k) for v in layer]
    for i in range(k):
        v=(w,10*i+7);order.remove(v);order.insert(order.index((w,10*i+5)),v)
    return [[v] for v in order]


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);args=p.parse_args()
    totals=Counter();records=[]
    for w,k in ((8,1),(8,2),(8,3),(10,3),(14,3),(32,5),(64,7)):
        base=configuration(w,k);layers=inventory_schedule(w,k)
        # Exhaust inventories and thresholds on small modules; include endpoints
        # and interior inventory points for larger footprints.
        inventories=list(itertools.product(range(k+1),repeat=2)) if k<=3 else [(k,0),(0,k),(0,0),(k//2,k//2),(1,1),(k-1,1)]
        for a,b in inventories:
            if a+b>k:continue
            for d in range(a+2):
                paid=max(0,a-d)
                removed={(0,10*i+5) for i in range(a,k)}
                removed|={(w+1,10*i+5) for i in range(a,a+b)}
                removed|={(w+1,10*i+7) for i in range(paid)}
                cur=(*base[:2],base[2]-removed,base[3])
                ranks=check_rank_certificate(cur,layers);totals['refined_strict_freezing_events']+=len(ranks)
                z=inspect(w,k,cur,totals,k<=2)
                assert (z['alpha'],z['central_beta'],z['value'],z['deficit'],z['links'])==(a,b,paid,min(a,d),paid)
                assert z['ell']==k-a+b+max(0,a-d)==k+b-min(a,d)
                totals['sharp_inventory_attainers']+=1
                totals['positive_central_beta_sharp_attainers']+=b>0
                totals['central_mixed_sharp_attainers']+=a+b<k
                if w==8 and k==3:records.append(dict(requested_deficit_threshold=d,**z))
    args.output.write_text(json.dumps(dict(status='PASS',counts=dict(totals),records=records,
        theorem='All even W>=8,k>=1; fixed central alpha count a and beta count b, a+b<=k; integer threshold d>=0; fully frozen optimum |T|=tau-k-b+min(a,d). All cases attained by deleting central tip partners and distinct lower private-beta partners; common strict schedule works without any central N partners.',
        scope='General proof written; finite cases verify geometric adapters and sharpness, not universal quantifiers.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(totals)),indent=2))

if __name__=='__main__':main()
