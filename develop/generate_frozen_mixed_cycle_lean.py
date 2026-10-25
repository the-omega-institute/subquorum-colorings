import json,sys
from pathlib import Path
sys.path.insert(0,'develop')
from check_occupied_cycle_chambers import actual
from check_promotion_cores import frozen_certificate
from check_merger_completion_reserves import neighbors
r=json.loads(Path('develop/fixtures/frozen_all_mixed_gate_cycle.json').read_text());cur=actual(r);T=cur[2];M=cur[3]
mate={v:w for e in M for v,w in (e,e[::-1])};P=set(mate)
_,layers=frozen_certificate(cur);rank={tuple(w['endpoint']):i for i,layer in enumerate(layers) for w in layer}
records=[]
for v in sorted(P,key=lambda x:(rank[x],x)):
 kept=sorted(w for w in neighbors(v) if w in T or w in P and rank[mate[w]]<rank[v]);assert len(kept)>=2
 records.append((v,rank[v],kept[0],kept[1]))
roots=[(5,6),(5,19),(24,6),(5,4),(5,5),(5,18),(24,18),(24,5)]
paths=[]
for root in roots:
 path=[];v=root
 while True:
  path.extend([v,mate[v]]);q=(mate[v][0]^1,mate[v][1])
  if q not in P:break
  v=q
 assert len(set(path))==len(path);paths.append(path)
point=lambda v:'('+str(v[0])+','+str(v[1])+')'
plist=lambda vs:'['+','.join(map(point,vs))+']'
s=Path('formal/SubQuorum/ReserveBoundarySplit.lean').read_text();core=s[s.index('/-- Endpoint freezing'):s.index('abbrev Point')]
adj=s[s.index('abbrev Point'):s.index('def baseSelected')]
text='''import Lean.Elab.Tactic.Omega
set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 16000000
namespace SubQuorum.FrozenMixedGateCycle
'''+core+adj
text+='def selected : List Point := '+plist(sorted(T))+'\n'
text+='def matching : List (Point × Point) := ['+','.join('('+point(v)+','+point(w)+')' for v,w in M)+']\n'
text+='''structure Witness where
  point : Point
  rank : Nat
  left : Point
  right : Point
  deriving Inhabited
'''
text+='def witnesses : List Witness := ['+',\n'.join('⟨'+point(v)+','+str(k)+','+point(a)+','+point(b)+'⟩' for v,k,a,b in records)+']\n'
text+='''def endpoints : List Point := matching.flatMap fun e => [e.1,e.2]
def lookupMate (v : Point) : List (Point × Point) → Point
  | [] => v
  | (a,b)::rest => if v=a then b else if v=b then a else lookupMate v rest
def mate (v : Point) : Point := lookupMate v matching
def record (v : Point) : Witness := (witnesses.find? fun w => w.point==v).getD default
def rank (v : Point) : Nat := (record v).rank
def validAt (v : Point) : Prop :=
  let a := (record v).left
  let b := (record v).right
  a≠b ∧ adjacent v a ∧ adjacent v b ∧
    (a∈selected ∨ (a∈endpoints ∧ rank (mate a)<rank v)) ∧
    (b∈selected ∨ (b∈endpoints ∧ rank (mate b)<rank v))
instance (v : Point) : Decidable (validAt v) :=
  inferInstanceAs (Decidable (_≠_ ∧ _ ∧ _ ∧ (_ ∨ (_ ∧ _)) ∧ (_ ∨ (_ ∧ _))))

theorem actual_geometry : endpoints.Nodup ∧ selected.Nodup ∧
    (∀ e∈matching, adjacent e.1 e.2) ∧
    (∀ v∈endpoints, v∉selected) ∧
    (∀ v∈selected ++ endpoints, v.1<28 ∧ v.2<24) ∧
    (∀ v∈selected, ((selected ++ endpoints).filter fun w => decide (adjacent v w)).length≤1) := by decide

theorem mate_closed : ∀ v∈endpoints, mate v∈endpoints := by decide
theorem certificate_valid : ∀ v∈endpoints, validAt v := by decide

theorem actual_board_completely_frozen : ∀ v∈endpoints,
    Frozen (fun x => x∈endpoints) (fun x => x∈selected) mate adjacent v := by
  apply strict_rank_complete (fun x => x∈endpoints) (fun x => x∈selected)
    mate adjacent rank mate_closed
  intro v pv
  exact ⟨(record v).left,(record v).right,certificate_valid v pv⟩

def partner (v : Point) : Point :=
  if v.1%2=0 then (v.1+1,v.2) else (v.1-1,v.2)
def alternating : List Point → Bool
  | [] => true
  | [_] => false
  | u::v::rest => (mate u==v) && (match rest with
      | [] => true
      | w::tail => (partner v==w) && alternating (w::tail))
def TP (v : Point) : Prop := v∈endpoints ∧ partner v∈selected
def BP (v : Point) : Prop := v∈endpoints ∧ partner v∉selected ∧ partner v∉endpoints
instance (v : Point) : Decidable (TP v) := inferInstanceAs (Decidable (_ ∧ _))
instance (v : Point) : Decidable (BP v) := inferInstanceAs (Decidable (_ ∧ _ ∧ _))
'''
text+='def paths : List (List Point) := ['+',\n'.join(plist(vs) for vs in paths)+']\n'
text+='''theorem eight_original_strands_disjoint : paths.length=8 ∧ paths.flatten.Nodup ∧
    (∀ path∈paths, alternating path=true ∧ ∀ v∈path, v∈endpoints) := by decide
'''
text+='theorem four_alpha_four_mixed_terminals : '+ ' ∧ '.join(('TP '+point(path[0]) if i<4 else 'BP '+point(path[0]))+' ∧ TP '+point(path[-1]) for i,path in enumerate(paths))+' := by decide\n'
links=[((5,6),(5,5)),((5,4),(5,5)),((5,17),(5,18)),((5,19),(5,18)),((24,17),(24,18)),((24,19),(24,18)),((24,6),(24,5)),((24,4),(24,5))]
text+='def cycleLinks : List (Point × Point) := ['+','.join('('+point(v)+','+point(w)+')' for v,w in links)+']\n'
text+='''theorem eight_actual_cycle_contacts : ∀ e∈cycleLinks, TP e.1 ∧ BP e.2 ∧ adjacent e.1 e.2 := by decide
#print axioms actual_geometry
#print axioms actual_board_completely_frozen
#print axioms eight_original_strands_disjoint
#print axioms four_alpha_four_mixed_terminals
#print axioms eight_actual_cycle_contacts
end SubQuorum.FrozenMixedGateCycle
'''
Path('formal/SubQuorum/FrozenMixedGateCycle.lean').write_text(text)
print('Generated',len(P),'endpoint witnesses, strand lengths',list(map(len,paths)))
