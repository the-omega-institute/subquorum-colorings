"""Exact reserve ledger on the explicit all-n frozen seam-cap family."""
import argparse,itertools,json
from collections import Counter
from pathlib import Path
from check_seam_residual_compensation import *

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 base,*_=load_model();spec=json.loads(Path('develop/fixtures/seam_frozen_caps.json').read_text());counts=Counter();records=[]
 for n in range(1,9):
  initial,cur=seam_caps(base,n)
  assert cur[2]==initial[2]|{shift(tuple(v),i) for v in spec['new_selected_per_seam'] for i in range(n-1)}
  assert cur[3]==initial[3]+[tuple(shift(tuple(v),i) for v in e) for e in spec['new_matching_per_seam'] for i in range(n-1)]
  d,meta,_=whole_support_data(cur,whole_bands(cur));owners,aa,bb,mm=owner_data(*d[:2])
  old_pool={meta['owner'][v[0]//2,v[1]] for x,w in FLEX for i in range(n) for v in [shift(w,i)]}
  new_units=[meta['owner'][4,24+24*i] for i in range(n-1)]
  assert len(set(new_units))==n-1 and old_pool.isdisjoint(new_units) and len(aa)==5*n-1
  for i,unit in enumerate(new_units):
   v=shift((9,23),i);w=shift((10,23),i);o=owners[v]
   assert owners[w]==o and d[0][v]==d[0][w]=='TP'
   assert not any(v in e or w in e for e in d[2])
   assert d[3][o]&(old_pool|set(new_units))=={unit}
   assert meta['intervals'][unit]==dict(band=4,first=24+24*i,last=24+24*i)
  choices=list(itertools.product((False,True),repeat=n-1)) if n<=5 else [tuple(False for i in range(n-1)),tuple(i==0 for i in range(n-1)),tuple(True for i in range(n-1))]
  for flags in choices:
   J={unit for unit,keep in zip(new_units,flags) if keep};dd=clipped(d,old_pool|J)
   ordinary=ordinary_flow(*dd);full=fork_flow(*dd)
   assert ordinary['deficit']==full['deficit']==n-1-len(J)
   assert ordinary['value']==full['value']==4*n+len(J)
   counts['reserve_profiles']+=1
   if n<=2:
    for forks in (False,True):
     exact=optimize(*dd,allow_forks=forks);flow=full if forks else ordinary
     assert (exact['value'],exact['cost'])==(flow['value'],flow['cost'])
     counts['independent_primitive_comparisons']+=1
  records.append(dict(copies=n,P=len(endpoints(cur)),T=len(cur[2]),alpha=len(aa),old_pool_deficit=n-1,one_distinct_unit_per_seam_suffices=True))
 out=dict(status='PASS',counts=dict(counts),records=records,scope='Written all-n proof: new isolated alpha per seam has no terminal link and supports exactly its own selected new unit in old_pool union new_units. Hence exact deficit n-1-card(J), and n-1 additional distinct units necessary and sufficient in this specified reserve model. Full resources always compensate.')
 args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(status='PASS',counts=dict(counts))))

if __name__=='__main__':main()
