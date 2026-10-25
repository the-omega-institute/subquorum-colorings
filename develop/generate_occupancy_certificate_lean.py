"""Generate matching-independent point geometry; previous freezing files stay intact."""
from collections import Counter
import json
from pathlib import Path
import sys
sys.path.insert(0,'develop')
from check_frozen_mixed_gate_cycle import load_model
from check_occupancy_certificate_all_rematchings import certificate
base,*_=load_model();assigned,reserve,data,meta,groups,neighborhoods=certificate(base)
P=sorted({v for e in base[3] for v in e});T=sorted(base[2])
pt=lambda v:'('+str(v[0])+','+str(v[1])+')'
lst=lambda vs:'['+','.join(pt(v) for v in vs)+']'
coord=lambda j:(meta['intervals'][j]['band'],meta['intervals'][j]['first'])
text='''import Lean.Elab.Tactic.Omega
set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 16000000
namespace SubQuorum.OccupancyCertificate

/-- A surviving free tip cannot have a BP target: that would have been a
selected cancellation link. This statement does not mention a matching. -/
theorem free_tip_has_interval {Tip BP I : Type} (cert : Tip → Sum BP I)
    (v : Tip) (free : ∀ b, cert v ≠ Sum.inl b) :
    ∃ j, cert v = Sum.inr j := by
  cases h : cert v with
  | inl b => exact False.elim (free b h)
  | inr j => exact ⟨j,rfl⟩

/-- Distinct final alpha paths choose distinct free tips. An injective
original target certificate therefore gives different original intervals. -/
theorem surviving_interval_injection {A Tip BP I : Type}
    (cert : Tip → Sum BP I) (tip : A → Tip) (unit : A → I)
    (certInjective : ∀ x y, cert x = cert y → x=y)
    (tipInjective : ∀ a b, tip a=tip b → a=b)
    (witness : ∀ a, cert (tip a)=Sum.inr (unit a)) :
    ∀ a b, unit a=unit b → a=b := by
  intro a b hab
  apply tipInjective a b
  apply certInjective (tip a) (tip b)
  rw [witness a,witness b,hab]

/-- Signed endpoint conservation plus one distinct interval per final alpha
settles every original demand, with whole betas counted once. -/
theorem full_payment_ledger (a b aFinal bFinal : Nat)
    (balance : a+bFinal=b+aFinal) (betaMonotone : bFinal≤b) :
    b-bFinal+aFinal=a := by omega

abbrev Point := Nat × Nat
'''
text+='def selected : List Point := '+lst(T)+'\n'
text+='def endpoints : List Point := '+lst(P)+'\n'
text+='def tips : List Point := '+lst(sorted(v for v,k in data[0].items() if k=='TP'))+'\n'
text+='def blanks : List Point := '+lst(sorted((r,c) for r in range(28) for c in range(24) if (r,c) not in set(P)|set(T)))+'\n'
text+='def originalUnits : List Point := '+lst([coord(j) for j in sorted(data[4])])+'\n'
text+='def reservedPacket : List Point := '+lst(sorted(coord(j) for j in reserve))+'\n'
text+='def assignments : List (Point × Sum Point Point) := ['+','.join('('+pt(v)+','+('Sum.inl '+pt(t[1]) if t[0]=='bp' else 'Sum.inr '+pt(coord(t[1])))+')' for t,v in assigned.items())+']\n'
text+='''def partner (v : Point) : Point := (v.1 ^^^ 1,v.2)
def TP (v : Point) : Prop := v∈endpoints ∧ partner v∈selected
def BP (v : Point) : Prop := v∈endpoints ∧ partner v∈blanks
instance (v : Point) : Decidable (TP v) := inferInstanceAs (Decidable (_ ∧ _))
instance (v : Point) : Decidable (BP v) := inferInstanceAs (Decidable (_ ∧ _))
def adjacent (v w : Point) : Prop :=
  (v.1=w.1 ∧ (v.2+1=w.2 ∨ w.2+1=v.2)) ∨
  (v.2=w.2 ∧ (v.1+1=w.1 ∨ w.1+1=v.1))
instance (v w : Point) : Decidable (adjacent v w) :=
  inferInstanceAs (Decidable ((_ ∧ (_ ∨ _)) ∨ (_ ∧ (_ ∨ _))))
def gapAccess (v j : Point) : Prop :=
  j∈originalUnits ∧ v.1/2=j.1 ∧
  (2*j.1,j.2)∈blanks ∧ (2*j.1+1,j.2)∈blanks ∧
  ∀ c∈List.range 24, min v.2 j.2<c ∧ c<max v.2 j.2 →
    (2*j.1,c)∉endpoints ∧ (2*j.1+1,c)∉endpoints
instance (v j : Point) : Decidable (gapAccess v j) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _ ∧ _))
def validEntry (e : Point × Sum Point Point) : Prop :=
  TP e.1 ∧ match e.2 with
    | Sum.inl w => BP w ∧ adjacent e.1 w
    | Sum.inr j => j∈reservedPacket ∧ gapAccess e.1 j
instance (e : Point × Sum Point Point) : Decidable (validEntry e) := by
  unfold validEntry
  cases e.2 <;> infer_instance

theorem actual_tip_inventory : tips.length=23 ∧
    endpoints.filter (fun v => decide (TP v))=tips := by decide

theorem actual_occupation_certificate :
    assignments.length=23 ∧ (assignments.map Prod.fst).Nodup ∧
    (assignments.map Prod.snd).Nodup ∧
    (∀ v∈tips, v∈assignments.map Prod.fst) ∧
    (∀ e∈assignments, validEntry e) := by decide

theorem actual_five_units_eighteen_links : reservedPacket.length=5 ∧
    reservedPacket.Nodup ∧
    (assignments.filter fun e => match e.2 with | Sum.inl _ => true | _ => false).length=18 ∧
    (assignments.filter fun e => match e.2 with | Sum.inr _ => true | _ => false).length=5 := by decide
'''
text+='def obstructionGroups : List (List Point) := ['+','.join(lst(sorted(g)) for g in groups)+']\n'
text+='def intervalNeighborhoods : List (List Point) := ['+','.join(lst(sorted(coord(j) for j in E)) for E in neighborhoods)+']\n'
text+='''theorem actual_five_disjoint_obstructions : obstructionGroups.length=5 ∧
    intervalNeighborhoods.length=5 ∧ intervalNeighborhoods.flatten.Nodup ∧
    (∀ H∈obstructionGroups,
      ((endpoints.filter fun w => decide (BP w ∧ ∃ v∈H, adjacent v w)).length+1=H.length)) ∧
    (∀ p∈obstructionGroups.zip intervalNeighborhoods,
      ∀ j∈originalUnits, (∃ v∈p.1, gapAccess v j) ↔ j∈p.2) := by decide

#print axioms free_tip_has_interval
#print axioms surviving_interval_injection
#print axioms full_payment_ledger
#print axioms actual_tip_inventory
#print axioms actual_occupation_certificate
#print axioms actual_five_units_eighteen_links
#print axioms actual_five_disjoint_obstructions
end SubQuorum.OccupancyCertificate
'''
Path('formal/SubQuorum/OccupancyCertificate.lean').write_text(text)
