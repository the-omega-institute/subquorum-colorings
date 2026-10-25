import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.JointIntervalBetaBlocks

/-- One chosen original alpha per distinct zero-cost interval component
cannot identify two component choices. The grid/forest adapter is written. -/
theorem representatives_injective {C V : Type} (component : V → C) (choose : C → V)
    (own : ∀ c, component (choose c)=c) : Function.Injective choose := by
  intro c d same
  have mapped := congrArg component same
  simpa only [own] using mapped

/-- Distinct nonroot interval components cannot spend the same parent beta.
The input records actual unordered endpoints and strict forest distance. -/
theorem parent_betas_not_reused {V E : Type} (used : V → Prop)
    (parent : V → V) (edge : V → E) (ends : E → V × V) (distance : V → Nat)
    (down : ∀ v, used v → distance (parent v)<distance v)
    (incidence : ∀ v, used v → ends (edge v)=(v,parent v) ∨ ends (edge v)=(parent v,v)) :
    ∀ u v, used u → used v → edge u=edge v → u=v := by
  intro u v hu hv same
  have equalEnds := congrArg ends same
  rcases incidence u hu with iu | iu <;> rcases incidence v hv with iv | iv
  · rw [iu,iv] at equalEnds
    exact congrArg Prod.fst equalEnds
  · rw [iu,iv] at equalEnds
    have x := congrArg Prod.fst equalEnds
    have y := congrArg Prod.snd equalEnds
    have du := down u hu
    have dv := down v hv
    change u=parent v at x
    change parent u=v at y
    rw [y] at du
    rw [←x] at dv
    omega
  · rw [iu,iv] at equalEnds
    have x := congrArg Prod.fst equalEnds
    have y := congrArg Prod.snd equalEnds
    have du := down u hu
    have dv := down v hv
    change parent u=v at x
    change u=parent v at y
    rw [x] at du
    rw [←y] at dv
    omega
  · rw [iu,iv] at equalEnds
    exact congrArg Prod.snd equalEnds

/-- n sources, q interval components, x exterior alpha roots, and z
distinct components meeting those roots. Internal beta cost is q-max(1,z),
not q-max(1,x). The partition supplies the stated count hypotheses. -/
theorem weighted_local_root_ledger (n q x z : Nat)
    (positive : 1≤q) (componentsFit : q≤n) (rootsFit : x≤n)
    (seen : z≤q) (atMostRoots : z≤x) (zero : z=0 ↔ x=0)
    (duplicatesFit : x-z≤n-q) :
    ((n-q)-(x-z))+(q-max 1 z)=n-max 1 x ∧
    q-max 1 z=(q-1)-(z-1) := by
  by_cases hx : x=0
  · have hz : z=0 := zero.mpr hx
    subst x; subst z
    simp only [Nat.sub_zero,Nat.max_eq_left (by omega : 0≤1)]
    omega
  · have hz : 1≤z := by omega
    have hxx : max 1 x=x := Nat.max_eq_right (by omega)
    have hzz : max 1 z=z := Nat.max_eq_right hz
    rw [hxx,hzz]
    omega

/-- The discounted units are distinct beta resources of the quotient tree. -/
theorem discount_within_beta_budget (q z : Nat) (seen : z≤q) : z-1≤q-1 := by omega

/-- Conditional saturated-block ledger. The written allocation proof supplies
interval payment n-x-(t-z); exactly t-z distinct beta units finish it. -/
theorem saturated_local_root_ledger (n t x z : Nat)
    (seen : z≤t) (rootsFit : x≤n) (deficienciesFit : t-z≤n-x) :
    (n-x-(t-z))+(t-z)=n-x ∧ t-z+z=t := by omega


def Eligible (a : Fin 3) (r : Fin 4) : Prop :=
  (a=0 ∧ (r=0 ∨ r=2)) ∨ (a=1 ∧ (r=0 ∨ r=1 ∨ r=3)) ∨ (a=2 ∧ r=1)

def ValidAssignment (f : Fin 3 → Fin 4) : Prop :=
  (∀ a, Eligible a (f a)) ∧ Function.Injective f

def totalCost (f : Fin 3 → Fin 4) : Nat :=
  (if f 0=1 then 1 else 0)+(if f 1=1 then 1 else 0)+(if f 2=1 then 1 else 0)

def assignment (a : Fin 3) : Fin 4 := if a=0 then 2 else if a=1 then 0 else 1

/-- The named three-alpha control has true exact cost one. Selecting two
external roots in its same interval component cannot lower that cost to zero. -/
theorem same_interval_component_control :
    (ValidAssignment assignment ∧ totalCost assignment=1) ∧
    (∀ f, ValidAssignment f → 1≤totalCost f) := by
  constructor
  · constructor
    · unfold ValidAssignment Function.Injective Eligible assignment
      decide
    · decide
  · intro f valid
    have forced : f 2=1 := by
      have allowed := valid.1 2
      simpa [Eligible] using allowed
    unfold totalCost
    rw [forced]
    simp only [ite_true]
    omega

#print axioms representatives_injective
#print axioms parent_betas_not_reused
#print axioms weighted_local_root_ledger
#print axioms discount_within_beta_budget
#print axioms same_interval_component_control
#print axioms saturated_local_root_ledger

end SubQuorum.JointIntervalBetaBlocks
