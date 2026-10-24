import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.MixedSupportComponentMerges

def OldPair {V R : Type} (owner : Nat → V) (unit : Nat → R) (n : Nat)
    (v : V) (r : R) : Prop :=
  ∃ i, i<n ∧ v=owner (i+1) ∧ r=unit i

def NewPair {V R : Type} (owner : Nat → V) (unit : Nat → R) (n : Nat)
    (v : V) (r : R) : Prop :=
  ∃ i, i≤n ∧ v=owner i ∧ r=unit i

/-- On an alternating augmenting path, every previously paid owner stays paid. -/
theorem augment_keeps_old_paid {V R : Type} (owner : Nat → V) (unit : Nat → R)
    (n : Nat) (v : V) (r : R) (old : OldPair owner unit n v r) :
    ∃ r', NewPair owner unit n v r' := by
  obtain ⟨i,hi,hv,_⟩ := old
  exact ⟨unit (i+1),i+1,by omega,hv,rfl⟩

/-- The same old resource is reassigned along the path, never discarded. -/
theorem augment_keeps_old_units {V R : Type} (owner : Nat → V) (unit : Nat → R)
    (n : Nat) (v : V) (r : R) (old : OldPair owner unit n v r) :
    ∃ v', NewPair owner unit n v' r := by
  obtain ⟨i,hi,_,hr⟩ := old
  exact ⟨owner i,i,by omega,rfl,hr⟩

theorem augment_new_pair_functional {V R : Type} (owner : Nat → V) (unit : Nat → R)
    (n : Nat) (ownerInj : ∀ i j, i≤n → j≤n → owner i=owner j → i=j)
    (v : V) (r s : R) (first : NewPair owner unit n v r)
    (second : NewPair owner unit n v s) : r=s := by
  obtain ⟨i,hi,hv,hr⟩ := first
  obtain ⟨j,hj,hw,hs⟩ := second
  have ij := ownerInj i j hi hj (hv.symm.trans hw)
  subst j
  exact hr.trans hs.symm

theorem augment_units_not_reused {V R : Type} (owner : Nat → V) (unit : Nat → R)
    (n : Nat) (unitInj : ∀ i j, i≤n → j≤n → unit i=unit j → i=j)
    (v w : V) (r : R) (first : NewPair owner unit n v r)
    (second : NewPair owner unit n w r) : v=w := by
  obtain ⟨i,hi,hv,hr⟩ := first
  obtain ⟨j,hj,hw,hs⟩ := second
  have ij := unitInj i j hi hj (hr.symm.trans hs)
  subst j
  exact hv.trans hw.symm

theorem augment_uses_one_new_unit {V R : Type} (owner : Nat → V) (unit : Nat → R)
    (n : Nat) (unitInj : ∀ i j, i≤n → j≤n → unit i=unit j → i=j) :
    NewPair owner unit n (owner n) (unit n) ∧
    ¬ ∃ v, OldPair owner unit n v (unit n) := by
  constructor
  · exact ⟨n,Nat.le_refl n,rfl,rfl⟩
  · rintro ⟨v,i,hi,_,hr⟩
    have same := unitInj n i (by omega) (by omega) hr
    omega

theorem new_root_was_unpaid {V R : Type} (owner : Nat → V) (unit : Nat → R)
    (n : Nat) (ownerInj : ∀ i j, i≤n → j≤n → owner i=owner j → i=j) :
    ¬ ∃ r, OldPair owner unit n (owner 0) r := by
  rintro ⟨r,i,hi,hv,_⟩
  have same := ownerInj 0 (i+1) (by omega) (by omega) hv
  omega

/-- Connectivity of a resource graph with at most two owners supplies this
signed count. The finite geometric partition is a written adapter. -/
theorem cluster_deficiency_iff (d s : Nat) :
    (s : Int)-d = -1 ↔ d=s+1 := by omega

theorem cluster_gain (d s : Nat) (connected : d≤s+1) :
    d-(if s<d then 1 else 0) = min d s := by
  by_cases h : s<d
  · simp only [h,ite_true]
    have sd : s≤d := by omega
    rw [Nat.min_eq_right sd]
    omega
  · simp only [h,ite_false,Nat.sub_zero]
    exact (Nat.min_eq_left (by omega)).symm

theorem cluster_unpaid_at_most_one (d s : Nat) (connected : d≤s+1) :
    d-min d s ≤ 1 := by
  by_cases h : d≤s
  · rw [Nat.min_eq_left h]; omega
  · rw [Nat.min_eq_right (by omega)]; omega

theorem cluster_consumes_distinct_reserves (d s : Nat) : min d s ≤ s := Nat.min_le_right d s

theorem constant_ledger (unused beta oldDefect gain newUnused newDefect : Nat)
    (units : newUnused+gain=unused) (defects : newDefect+gain=oldDefect) :
    (unused : Int)+beta-oldDefect = (newUnused : Int)+beta-newDefect := by omega

#print axioms augment_keeps_old_paid
#print axioms augment_keeps_old_units
#print axioms augment_new_pair_functional
#print axioms augment_units_not_reused
#print axioms augment_uses_one_new_unit
#print axioms new_root_was_unpaid
#print axioms cluster_deficiency_iff
#print axioms cluster_gain
#print axioms cluster_unpaid_at_most_one
#print axioms cluster_consumes_distinct_reserves
#print axioms constant_ledger

end SubQuorum.MixedSupportComponentMerges
