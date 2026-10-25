"""Construct/check the seam-completed certificate on retained base copies.
General proof: docs/SEAM_RESIDUAL_COMPENSATION.md. Finite models only check it.
"""
from check_conditional_fresh_tip_closure import *
from check_residual_fresh_domains import color, geometry
from check_terminal_cancellation_and_stranded_demand import components
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_promotion_cores import frozen_certificate
import argparse,json,random
from pathlib import Path

if not __debug__: raise RuntimeError("Run without -O.")

def construct(base,initial,cur,n):
 P=endpoints(cur);P0=endpoints(initial);T=cur[2];O=T|P
 assert feasible(cur) and initial[2]<=T and P0<=P
 assert all(len(set(neighbors(v))&O)>=3 for v in P)
 d,meta,_=whole_support_data(cur,whole_bands(cur));owners,*_=owner_data(*d[:2]);tips={v for v,k in d[0].items() if k=='TP'}
 old,_=static_certificate(base);assignment={};pool=set();details=[]
 def bp(v,w,kind):
  assert d[0][w]=='BP' and (v,w) in d[2]
  key=('bp',w);assert key not in assignment and v not in assignment.values(),(v,w,kind)
  assignment[key]=v;details.append((kind,v,w))
 def unit(v,w,kind):
  j=meta['owner'][w[0]//2,w[1]]
  assert j in d[4] and j in d[3][owners[v]],(v,w,j,kind)
  assert j not in pool and v not in assignment.values(),(v,w,j,kind,meta['intervals'][j])
  record=meta['intervals'][j]
  if kind=='seam_unit':
   i=(v[1]-23)//24
   assert 4<=record['band']<=11 and 21+24*i<=record['first']<=record['last']<=26+24*i
  if kind=='bottom_even_unit':
   i=v[1]//24
   assert record['band']==13 and record['first']-24*i in (9,11,12,13) and record['last']<=13+24*i
  assignment['interval',j,0]=v;pool.add(j);details.append((kind,v,record))
 for i in range(n):
  for target,v in old.items():bp(shift(v,i),shift(target[1],i),'old')
  for v,w in FLEX+[(v,w) for v,w in PROTECTED if shift(v,i) in tips]:
   v,w=shift(v,i),shift(w,i)
   if w in P:bp(v,w,'conditional')
   else:unit(v,w,'conditional')
  if shift((2,14),i) in T:bp(shift((3,14),i),shift((3,13),i),'promotion')
 for v in sorted(tips-P0):
  if v[1]%24 not in (0,23) or v[0]>=26:continue
  blanks=[w for w in sorted(neighbors(v)) if w[0]==v[0] and 0<=w[1]<24*n and w not in O and partner(w) not in O]
  if blanks:unit(v,blanks[0],'seam_unit')
  else:
   candidates=[w for w in sorted(neighbors(v)) if w[0]==v[0] and d[0].get(w)=='BP']
   assert candidates,('no BP',v)
   bp(v,candidates[0],'seam_BP')
 for i in range(n):
  v=shift((26,14),i)
  if v not in tips:continue
  w=shift((26,13),i)
  if w in P:bp(v,w,'bottom_even_BP')
  else:
   if w in T:
    w=shift((26,12),i)
    if partner(w) in T:w=shift((26,11),i)
   assert w not in O and partner(w) not in O
   unit(v,w,'bottom_even_unit')
 holes=tips-set(assignment.values());C=[(v,t[1]) for t,v in assignment.items() if t[0]=='bp']
 reduced,inv,recs=cancel_pairs(*d[:2],C,Counter())
 mate={v:w for e in cur[3] for v,w in (e,e[::-1])};linked={v for e in C for v in e}
 for v in holes:
  w=mate[v]
  if d[0].get(w)=='BP' and not {v,w}&linked:continue
  assert v[0]==26 and v[1]%24 in (13,15),(v,w,'unclassified relevant hole')
 physical_edges=cur[3]+[(v,partner(v)) for v in P if v<partner(v) and partner(v) in P]+C
 physical_pairs=[];physical_paths=0
 for component in components(P,physical_edges):
  if component['cycle']:continue
  assert len(component['edges'])%2==1 and len(component['ends'])==2
  x,y=component['ends'];assert color(x)!=color(y)
  physical_pairs.append(tuple(sorted((x,y))));physical_paths+=1
 assert set(physical_pairs)=={tuple(sorted(e)) for e in reduced}
 alphas=[e for e in reduced if all(d[0][v]=='TP' for v in e)]
 hole_alpha_ends={v for e in alphas for v in e if v in holes}
 assert all(color(v)==1 for v in hole_alpha_ends),(hole_alpha_ends,holes)
 assert all(not set(e)<=holes for e in alphas)
 h=sum(shift(w,i) in P for v,w in FLEX for i in range(n))
 p=sum(shift((2,14),i) in T for i in range(n))
 g=sum(shift(v,i) in tips for v,w in PROTECTED for i in range(n))
 q=sum(shift(v,i) in tips and shift(w,i) in P for v,w in PROTECTED for i in range(n))
 z=sum(kind.startswith('seam') for kind,v,w in details);zb=sum(kind=='seam_BP' for kind,v,w in details)
 b=sum(kind.startswith('bottom_even') for kind,v,w in details);bb=sum(kind=='bottom_even_BP' for kind,v,w in details)
 assert len(assignment)==len(set(assignment.values()))==23*n+p+g+z+b
 assert len(C)==18*n+h+p+q+zb+bb and len(pool)==5*n-h+g-q+z-zb+b-bb
 restricted=clipped(d,pool);lifted=lift(restricted,assignment)
 assert lifted['certified_deficit']==ordinary_flow(*restricted)['deficit']==0
 return dict(holes=len(holes),relevant_odd_holes=len(hole_alpha_ends),seam_tips=sum(kind.startswith('seam') for kind,v,w in details),bottom_even=sum(kind.startswith('bottom_even') for kind,v,w in details),details=details,physical_paths=physical_paths,assigned=len(assignment),units=len(pool),links=len(C),frozen=frozen(cur))

def audit_footprints(base):
 S,_,_,_=geometry(base);records=[]
 seam={(r,c) for r in list(range(8,14))+[22,23,26,27] for c in (23,24)}|{(r,23) for r in range(14,22)}
 assert len(seam)==28
 old,_=static_certificate(base)
 for n in range(1,7):
  initial=base_copies(base,n);P=endpoints(initial);O=P|initial[2]
  actual={(r,c) for r in range(28) for c in range(1,24*n-1)
      if (r,c) not in O and partner((r,c)) not in O and not set(neighbors(partner((r,c))))&O
      and not set(neighbors((r,c)))&initial[2]}-{shift(v,i) for v,w in PROTECTED for i in range(n)}
  expected={shift(v,i) for v in S for i in range(n)}|{shift(v,i) for v in seam for i in range(n-1)}
  assert actual==expected
  Q={shift(t[1],i) for t in old for i in range(n)}|{shift(w,i) for v,w in FLEX+PROTECTED for i in range(n)}|{shift((3,13),i) for i in range(n)}
  assert not {(v,w) for v in actual for w in Q if v[0]==w[0] and w in neighbors(v)}
  assert all(shift((r,c),i) in P for r in range(8,24) for c in (3,20) for i in range(n))
  assert all(shift((25,c),i) in initial[2] for c in (2,4,6,8,11,17,19,21) for i in range(n))
  records.append(dict(copies=n,unprotected_candidates=len(actual),local_candidates=39*n,seam_candidates=28*(n-1)))
 # Literal guard triples used in the written adapter and Lean geometry check.
 initial=base_copies(base,2);O=endpoints(initial)|initial[2]
 triples=[((25,1),(25,2),(24,2)),((26,2),(25,2),(24,2)),
  ((25,12),(25,11),(24,11)),((26,11),(25,11),(24,11)),
  ((25,16),(25,17),(24,17)),((26,17),(25,17),(24,17)),
  ((25,22),(25,21),(24,21)),((26,21),(25,21),(24,21)),
  ((24,23),(24,22),(24,21)),((25,25),(25,26),(24,26)),
  ((24,24),(24,25),(24,26)),((26,26),(25,26),(24,26))]
 for blank,t,w in triples:
  assert blank not in O and t in initial[2] and w in O and blank!=w
  assert set(neighbors(t))&O=={w} and blank in neighbors(t)
 return dict(footprints=records,seam_literal=sorted(seam),guard_triples=triples)


def seam_caps(base,n):
 initial=base_copies(base,n)
 newT={shift(v,i) for i in range(n-1) for v in [(8,23),(11,23),(9,22),(10,24)]}
 newM=[(shift((9,23),i),shift((10,23),i)) for i in range(n-1)]
 return initial,(*initial[:2],initial[2]|newT,initial[3]+newM)


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 base,*_=load_model();audit=audit_footprints(base);totals=Counter();named={}
 def inspect_model(initial,cur,n,independent=False):
  result=construct(base,initial,cur,n)
  totals['models']+=1;totals['frozen' if result['frozen'] else 'degree_three_nonfrozen']+=1
  totals['physical_odd_paths']+=result['physical_paths']
  totals['seam_assignments']+=result['seam_tips'];totals['bottom_even_assignments']+=result['bottom_even']
  totals['models_with_odd_final_alpha_holes']+=result['relevant_odd_holes']>0
  totals['max_relevant_odd_holes']=max(totals['max_relevant_odd_holes'],result['relevant_odd_holes'])
  for kind,v,w in result['details']:
   totals[kind+'_assignments']+=1
   if kind=='bottom_even_unit':totals['bottom_unit_first_residue_'+str(w['first']%24)]+=1
  # Independent primitive enumeration is confined to small explicit cap models.
  if independent:
   d,meta,_=whole_support_data(cur,whole_bands(cur));pool=set()
   for kind,v,w in result['details']:
    if isinstance(w,dict):pool.add(meta['owner'][w['band'],w['first']])
   dd=clipped(d,pool)
   for forks in (False,True):
    direct=optimize(*dd,allow_forks=forks);flow=fork_flow(*dd) if forks else ordinary_flow(*dd)
    assert (direct['value'],direct['cost'])==(flow['value'],flow['cost'])
    totals['independent_primitive_comparisons']+=1
  return {k:v for k,v in result.items() if k!='details'}
 for n in range(1,9):
  initial,cur=seam_caps(base,n)
  assert len(endpoints(cur))==314*n-6 and len(cur[2])==53*n-4
  layers=[[w['endpoint'] for w in layer] for layer in frozen_certificate(initial)[1]]
  if n>1:layers.append([v for edge in cur[3][len(initial[3]):] for v in edge])
  check_rank_certificate(cur,layers);totals['cap_independent_rank_checks']+=1
  before=inspect(base,initial,cur,n,Counter(),independent=False)
  assert before['exact_strategy_loss']==before['ordinary_deficit']==n-1
  after=inspect_model(initial,cur,n,n<=2)
  assert after['seam_tips']==2*(n-1) and after['bottom_even']==after['holes']==0
  named['caps_'+str(n)]=dict(old_conditional=before,new_certificate=after)
  totals['strict_restricted_pool_repairs']+=n>1
  # The same occupations allow arbitrary actual rematching.
  for sq,alt in list(square_switches(cur))[:5]:
   inspect_model(initial,alt,n);totals['actual_rematches']+=1
  j=json.loads(Path('develop/fixtures/residual_fresh_frozen_bottom.json').read_text())
  bottom=(*cur[:2],cur[2]|{shift(tuple(v),i) for v in j['new_selected'] for i in range(n)},cur[3]+[tuple(shift(tuple(v),i) for v in e) for e in j['new_matching'] for i in range(n)])
  named['caps_plus_bottom_'+str(n)]=inspect_model(initial,bottom,n,n==1)
  assert named['caps_plus_bottom_'+str(n)]['frozen']
  for sq,alt in list(square_switches(bottom))[:5]:
   inspect_model(initial,alt,n);totals['actual_rematches']+=1
  print(json.dumps(dict(progress_copies=n,models=totals['models'])),flush=True)
 initial=base_copies(base,2);fixture=json.loads(Path('develop/fixtures/seam_degree_three_controls.json').read_text())
 for j in fixture['cases']:
  removed={frozenset(map(tuple,e)) for e in j['removed_matching']}
  cur=(*initial[:2],initial[2]|set(map(tuple,j['added_selected'])),[e for e in initial[3] if frozenset(e) not in removed]+[tuple(map(tuple,e)) for e in j['added_matching']])
  named[j['name']]=inspect_model(initial,cur,2)
  for sq,alt in list(square_switches(cur))[:12]:
   inspect_model(initial,alt,2);totals['actual_rematches']+=1
  totals['solver_discovered_models_rechecked_without_solver']+=1
 assert totals['seam_BP_assignments'] and totals['bottom_even_BP_assignments']
 assert all(totals['bottom_unit_first_residue_'+str(c)] for c in (11,12,13))
 assert totals['models_with_odd_final_alpha_holes']>0
 report=dict(status='PASS',counts=dict(totals),audit=audit,named=named,
  scope='Written arbitrary-n theorem on SAME28x24n rectangle retaining old T/P and PP seams: every feasible extension with all final P occupied-degree>=3 has full ordinary compensation, arbitrary actual M. Completely frozen extensions included. New nonbottom seam assignments and bottom-even protection are injective in original units/BPs; only odd relevant alpha holes remain. Universal grids, larger rectangles and numerical5/6 improvement remain open.')
 args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',counts=dict(totals))))

if __name__=='__main__':main()
