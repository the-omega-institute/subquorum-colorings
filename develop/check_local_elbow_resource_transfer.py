"""Two-tile elbow resource transport; general proof in LOCAL_ELBOW_RESOURCE_TRANSFER.md."""
import argparse
from collections import Counter
from functools import cache
import itertools,json,random
from pathlib import Path
from check_canonical_band_coarsening import canonical_bands,tile_directions,forests
from check_crossing_matching_ports import rectangle
from check_degree_changing_bent_completions import compile_model
from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_flow import fork_flow

def omit(data,excluded,Q=None):
 own,A,B,X=owner_data(*data[:2]);kept=[i for i in range(len(data[1])) if i not in excluded];Q=data[4] if Q is None else Q
 return ({p:k for p,k in data[0].items() if own[p] not in excluded},[data[1][i] for i in kept],
 [e for e in data[2] if all(own[p] not in excluded for p in e)],{j:data[3][i]&Q for j,i in enumerate(kept)},Q)

def adapter(cur,regs,r,c,independent=False):
 R,C,T,M=cur;P={v for e in M for v in e};v=(r+1,c+1);patch=set(itertools.product(range(r,r+4),range(c,c+2)))
 assert P&patch=={v} and {(r,c+1),(r+1,c)}<=T and {(r+2,c+2),(r+3,c+2)}<=P
 regs=canonical_bands(R,C,regs);bits=tile_directions(R,C,regs)
 assert not bits[r,c] and not bits[r+2,c] and bits[r,c+2] and bits[r+2,c+2]
 assert all(not bits[x,c] for x in (r-2,r+4) if 0<=x<R)
 newbits=dict(bits);newbits[r,c]=newbits[r+2,c]=True
 after=canonical_bands(R,C,[rectangle(x,x+2,y,y+2,b) for (x,y),b in newbits.items()])
 d0,cl,N=compile_model(cur,regs);d1,cl1,N1=compile_model(cur,after);own,A,B,X=owner_data(*d0[:2]);a=own[v]
 assert a in A and d0[:2]==d1[:2] and [x['body'] for x in cl]==[x['body'] for x in cl1] and set(d0[2])==set(d1[2])
 f0,f1=forests(cur,regs),forests(cur,after)
 cells0={j:f0[j][1] for j in d0[4]};cells1={j:f1[j][1] for j in d1[4]};rev1={z:j for j,z in cells1.items()}
 lost={j for j,z in cells0.items() if z not in rev1};new={j for j,z in cells1.items() if z not in set(cells0.values())}
 delta=2-sum((r+3,y) in T for y in (c,c+1));assert len(lost)==len(new)==delta and delta in (1,2)
 users={o for o,W in d0[3].items() if W&lost};assert len(users)<=1
 assert all({o for o,W in d1[3].items() if j in W}=={a} for j in new)
 for o in d0[3]:
  if o!=a:assert {cells0[j] for j in d0[3][o]-lost}=={cells1[j] for j in d1[3][o]}
 rest=omit(d0,{a},d0[4]-lost);minus=omit(d0,{a});z,p,f=fork_flow(*rest),fork_flow(*minus),fork_flow(*d1)
 assert p['value']-z['value'] in (0,1)
 assert (f['value'],f['cost'])==(1+z['value'],z['cost'])
 old=fork_flow(*d0)
 assert old['value']-p['value'] in (0,1)
 if old['value']==p['value']:assert f['value']>=old['value']
 if independent:
  from check_whole_support_fork_normal_form import optimize
  for model,answer in ((d0,old),(d1,f),(rest,z),(minus,p)):
   alt=optimize(*model);assert (alt['value'],alt['cost'])==(answer['value'],answer['cost'])
 return dict(target=a,lost=lost,new=new,old_data=d0,new_data=d1,rest=rest,
   old_value=old['value'],new_value=f['value'],new_cost=f['cost'],minus_value=p['value'],rest_value=z['value'],rank_loss=p['value']-z['value'],
   old_essential_source=old['value']-p['value'],delta=delta,lost_users=users)



def local_family_regions(w,k,actions,leaf_only=False):
 from check_mixed_terminal_defect import mixed_regions
 R,C=w+2,10*k+2;bits=tile_directions(R,C,mixed_regions(w,k))
 for i,side in actions:
  start=0 if side=='upper' else w-2
  rows=(0,) if side=='upper' and leaf_only else ((w,) if leaf_only else (start,start+2))
  for r in rows:bits[r,10*i+2]=True
 return canonical_bands(R,C,[rectangle(r,r+2,c,c+2,b) for (r,c),b in bits.items()])


@cache
def cover_members(w,k):
 from check_frozen_selection_frontier import cover
 from check_forced_mates_and_adjacent_maxima import configuration
 base=configuration(w,k)
 caps=cover(w,k,(*base[:2],set(),base[3]))
 members={}
 for key,cap in caps.items():
  if len(key)==3:_,r,c=key;height=4
  else:r,c=key;height=2
  members[key]=(cap,{(r+x,c+y) for x in range(height) for y in (0,1)})
 seen=set()
 for cap,cells in members.values():assert not seen&cells;seen|=cells
 assert seen==set(itertools.product(range(w+2),range(10*k+2)))
 assert sum(cap for cap,cells in members.values())==(7*k+2)*(w//2)+3*k+2
 return members


def family_profile(w,k,cur,actions,totals,independent=False):
 from check_frozen_selection_frontier import seals
 from check_mixed_terminal_defect import mixed_regions
 from check_residual_corridors import direct_check
 direct_check(*cur)
 assert seals(w,k)<=cur[2]
 olddata,oldclosed,_=compile_model(cur,mixed_regions(w,k))
 loss={key:cap-len(cur[2]&cells) for key,(cap,cells) in cover_members(w,k).items()}
 assert all(x>=0 for x in loss.values())
 ell=sum(loss.values());assert ell==(7*k+2)*(w//2)+3*k+2-len(cur[2])
 h=[sum(loss[r,10*i+c] for r in (0,w) for c in (0,4)) for i in range(k)]
 assert ell>=sum(h)
 oldown,oldA,oldB,oldX=owner_data(*olddata[:2])
 assert oldA=={oldown[1,10*i+3] for i in range(k)}
 for i in range(k):
  a=oldown[1,10*i+3]
  assert len(olddata[3][a])==h[i]
  assert all({o for o,W in olddata[3].items() if j in W}=={a} for j in olddata[3][a])
  assert not any(oldown[p]==a and oldown[q]!=a for p,q in olddata[2])
 oldflow=fork_flow(*olddata)
 assert (oldflow['value'],oldflow['deficit'],oldflow['cost'])==(sum(x>0 for x in h),sum(x==0 for x in h),0)
 data,closed,N=compile_model(cur,local_family_regions(w,k,actions));own,A,B,X=owner_data(*data[:2])
 assert data[:2]==olddata[:2]
 assert [x['body'] for x in closed]==[x['body'] for x in oldclosed]
 hit={i for i,side in actions}
 expected=sum(i in hit or x>0 for i,x in enumerate(h))
 for i in range(k):
  a=own[1,10*i+3]
  assert bool(data[3][a])==(i in hit or h[i]>0)
  assert all({o for o,W in data[3].items() if j in W}=={a} for j in data[3][a])
  assert not any(own[p]==a and own[q]!=a for p,q in data[2])
 f=fork_flow(*data);assert (f['value'],f['deficit'],f['cost'])==(expected,k-expected,0)
 assert ell+f['deficit']+len(hit)>=k
 if independent:
  from check_whole_support_fork_normal_form import optimize
  z=optimize(*data);assert (z['value'],z['cost'])==(f['value'],f['cost']);totals['family_independent_primitive_optima']+=1
 totals['arbitrary_T_and_elbow_profiles']+=1
 return dict(w=w,k=k,size=len(cur[2]),ell=ell,actions=[list(x) for x in sorted(actions)],hit_modules=len(hit),
             old_private_support_sizes=h,value=f['value'],deficit=f['deficit'],links=f['cost'])


def main():
 from check_forced_mates_and_adjacent_maxima import configuration
 from check_residual_corridors import transformed,direct_check
 from check_frozen_selection_frontier import seals
 from check_frozen_inventory_frontier import inventory_schedule
 from check_opposed_direction_interfaces import fast_rank_certificate
 from check_degree_changing_bent_completions import add_selections
 from check_mixed_terminal_defect import port_graph,mixed_regions
 p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);args=p.parse_args()
 totals=Counter();rng=random.Random(2026102624);records=[];fixture=None
 # Exhaust family action sets (upper/lower redundant alternatives included).
 for w,k in itertools.product((8,10,14),(1,2,3)):
  base=configuration(w,k);R,C=base[:2]
  actions=[(i,side) for i in range(k) for side in ('upper','lower')]
  for mask in range(1<<len(actions)):
   F={action for j,action in enumerate(actions) if mask>>j&1}
   z=family_profile(w,k,base,F,totals,independent=w==8 and k<=2)
   assert z['value']==len({i for i,side in F})
   totals['maximum_T_all_upper_lower_action_sets']+=1
  # A single leaf-tile flip exchanges one seam defect for one boundary
  # defect; it cannot by itself create a reserve on this maximum.
  for i in range(k):
   leaf,_=port_graph(base,local_family_regions(w,k,{(i,'upper')},True))
   pair,_=port_graph(base,local_family_regions(w,k,{(i,'upper')}))
   assert (leaf['boundary'],leaf['seam'],leaf['value'],leaf['deficit'])==(1,2*k-1,0,k)
   assert (pair['boundary'],pair['seam'],pair['value'],pair['deficit'])==(0,2*k-1,1,k-1)
   totals['single_tile_moves_seam_to_boundary_controls']+=1
  # Rebuild feasible T from seals only; no retention of previous T.
  for repeat in range(8):
   cur=add_selections((R,C,seals(w,k),base[3]),rng)
   if repeat%2:cur=(R,C,{v for v in sorted(cur[2]) if v in seals(w,k) or rng.randrange(2)},base[3])
   F={action for action in actions if rng.randrange(2)}
   family_profile(w,k,cur,F,totals,independent=k==1 and repeat<2)
   totals['T_rebuilt_from_only_leaf_seals']+=1
 # Constant two-tile repairs at large heights; all joint quota attainments.
 for w,k in ((8,3),(14,3),(32,5),(64,7)):
  base=configuration(w,k)
  for j,d in itertools.product(range(k+1),repeat=2):
   q=min(j,k-d);F={(i,'upper') for i in range(q)}
   cur=(*base[:2],base[2]-{(0,10*i+5) for i in range(q,k-d)},base[3])
   z=family_profile(w,k,cur,F,totals)
   assert z['ell']==max(0,k-d-j) and z['deficit']==d
   ranks=fast_rank_certificate(cur,inventory_schedule(w,k));totals['strict_freezing_events']+=len(ranks)
   totals['sharp_frozen_joint_quota_attainers']+=1
   if w==8:records.append(dict(patch_budget=j,deficit_threshold=d,**z))
   if (w,k,j,d)==(8,3,1,1):
    fixture=dict(shape=cur[:2],selected=sorted(cur[2]),matching=cur[3],actions=sorted(F),freezing_layers=inventory_schedule(w,k),expected=z)
 # General geometric adapter with genuine supported old resource losses.
 for w,k in ((8,1),(8,2),(10,3),(14,3)):
  base=configuration(w,k);R,C=base[:2]
  for i in range(k):
   for cutT in (set(),{(3,10*i+3)}):
    cur=(*base[:2],base[2]-cutT,base[3])
    regs=canonical_bands(R,C,[rectangle(0,R,0,10*i+4),rectangle(0,R,10*i+4,C,True)])
    z=adapter(cur,regs,0,10*i+2,True)
    totals['general_adapter_models']+=1
    totals['adapter_delta_two_cases']+=z['delta']==2
    totals['adapter_old_resources_supported_by_other_owner']+=bool(z['lost_users']-{z['target']})
    totals['adapter_independent_primitive_optima']+=4
 # Diverse existing physical fixtures and deterministic mixed mosaics.
 seen=set()
 for path in sorted((Path(__file__).parent/'fixtures').glob('*.json')):
  try:
   raw=json.loads(path.read_text())
   if not {'shape','selected','matching'}<=raw.keys():continue
   base=(*raw['shape'],set(map(tuple,raw['selected'])),[tuple(map(tuple,e)) for e in raw['matching']])
   if base[0]%2 or base[1]%2 or base[0]*base[1]>2000:continue
   direct_check(*base)
  except (ValueError,TypeError,AssertionError):continue
  for sym in ((False,False,False),(False,True,False),(True,False,False)):
   shape,T,M=transformed(*base,*sym);cur=(*shape,T,M);R,C=shape;P={v for e in M for v in e}
   for r in range(0,R-3,2):
    for c in range(0,C-3,2):
     patch=set(itertools.product(range(r,r+4),range(c,c+2)));v=(r+1,c+1)
     if P&patch!={v} or not {(r,c+1),(r+1,c)}<=T or not {(r+2,c+2),(r+3,c+2)}<=P:continue
     key=(R,C,frozenset(T),frozenset(map(frozenset,M)),r,c)
     if key in seen:continue
     seen.add(key)
     for sample in range(4):
      bits={(x,y):bool(rng.randrange(2)) for x in range(0,R,2) for y in range(0,C,2)}
      for x in (r,r+2):
       for y in range(0,c+2,2):bits[x,y]=False
       bits[x,c+2]=True
      for x in (r-2,r+4):
       if 0<=x<R:bits[x,c]=False
      regs=canonical_bands(R,C,[rectangle(x,x+2,y,y+2,b) for (x,y),b in bits.items()])
      data,_,_=compile_model(cur,regs);own,A,B,X=owner_data(*data[:2])
      if own.get(v) not in A:continue
      z=adapter(cur,regs,r,c)
      totals['general_adapter_models']+=1;totals['mixed_mosaic_adapter_models']+=1
      totals['adapter_delta_two_cases']+=z['delta']==2
      totals['adapter_old_resources_supported_by_other_owner']+=bool(z['lost_users']-{z['target']})
      totals['positive_rank_loss_models']+=z['rank_loss']>0
 fp=Path(__file__).parent/'fixtures/local_elbow_repair_w8_k3.json';fp.write_text(json.dumps(fixture,indent=2)+'\n')
 saved=json.loads(fp.read_text());cur=(*saved['shape'],set(map(tuple,saved['selected'])),[tuple(map(tuple,e)) for e in saved['matching']])
 assert family_profile(8,3,cur,set(map(tuple,saved['actions'])),totals,True)==saved['expected']
 fast_rank_certificate(cur,[[tuple(v) for v in layer] for layer in saved['freezing_layers']])
 assert totals['adapter_delta_two_cases']>0 and totals['adapter_old_resources_supported_by_other_owner']>0
 args.output.write_text(json.dumps(dict(status='PASS',counts=dict(totals),quota_records=records,
  theorem='Local4x2HToVElbow: only one P at upper right, two selected seals, outside right P guards in lower rows, canonical H runs end at right boundary, adjacent upper/lower tiles H or board boundary; target global alpha. All M/PP owners and TPBP links unchanged. Exactly delta=1or2 old positive units disappear, supported by at most one old owner; exactly delta new private target units appear; all other resources/supports for non-target owners unchanged. Vnew=1+VoldWithoutTargetAndLostUnits, cost equal. With pminus=VoldWithoutTarget, rankloss=pminus-Vrest in0or1. If an old maximum excludes target then gain=1-rankloss, never negative; no automatic strict-gain claim.',
  family='All even W>=8,k>=1; ANY sealed final T in existing mixedH4V6 family. Upper/lower two-tile elbow actions give exact V=count(i oldh_i>0 or at least one action hits i), cost0. All action supports private. Frozen optimum under at most j patch actions and D<=d is tau-max(0,k-d-j), attained with two direction-bit flips per patch independent of W. On T*, leaf-tile flip alone moves one seam to b and pays0; the adjacent second flip opens the guard and pays1.',
  limits=['No full-pool physical rankloss1 example is claimed. Computed zero losses do not prove that freezing or geometry forces rankloss0 in general.',
          'Raw old and new local pools replace one another, never add; action counts are patch counts, not a proof of globally minimum tile-flip count.',
          'No universal5/6 improvement; general geometry written/executable, formal scope separately stated.']),indent=2)+'\n')
 print(json.dumps(dict(status='PASS',counts=dict(totals)),indent=2))

if __name__=='__main__':main()
