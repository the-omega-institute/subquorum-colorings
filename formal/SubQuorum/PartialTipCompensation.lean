import Lean.Elab.Tactic.Omega
import Init.Data.List.Perm

set_option autoImplicit false

namespace SubQuorum.PartialTipCompensation

def slotUniverse {R : Type} (resources : List R) : List (R × Bool) :=
  resources.flatMap fun j => [(j,false),(j,true)]

theorem slot_universe_length {R : Type} (resources : List R) :
    (slotUniverse resources).length=2*resources.length := by
  induction resources with
  | nil => simp [slotUniverse]
  | cons j rest ih =>
    simp only [slotUniverse,List.flatMap_cons,List.length_append,
      List.length_cons,List.length_nil] at *
    omega

/-- Actual distinct slot identities, rather than two credits per support
incidence, supply the factor two. Resource lists need not be duplicated-free
for this upper bound; using different original identities is a separate
requirement of the application. -/
theorem distinct_slots_bound {R : Type} (slots : List (R × Bool)) (resources : List R)
    (distinct : slots.Nodup)
    (eligible : ∀ p ∈ slots, p.1 ∈ resources) :
    slots.length ≤ 2*resources.length := by
  have included : ∀ p ∈ slots, p ∈ slotUniverse resources := by
    intro p hp
    apply List.mem_flatMap.mpr
    refine ⟨p.1,eligible p hp,?_⟩
    cases p with
    | mk j bit => cases bit <;> simp
  have h := distinct.length_le_of_subset included
  rw [slot_universe_length] at h
  exact h

/-- This applies to every subset of final alpha paths: exactly two free
ends per path, partitioned into genuinely assigned distinct slots and holes. -/
theorem subset_hole_bound {R : Type}
    (paths holes : Nat) (slots : List (R × Bool)) (resources : List R)
    (distinct : slots.Nodup) (eligible : ∀ p ∈ slots, p.1 ∈ resources)
    (partition : slots.length+holes=2*paths) :
    paths ≤ resources.length+holes/2 := by
  have cap := distinct_slots_bound slots resources distinct eligible
  omega

def componentBudget (holes : List Nat) : Nat := (holes.map fun h => h/2).sum
def oddCount (holes : List Nat) : Nat := (holes.map fun h => h%2).sum

/-- Rounding must be done within the genuine disjoint resource components. -/
theorem component_parity_identity (holes : List Nat) :
    2*componentBudget holes+oddCount holes=holes.sum := by
  induction holes with
  | nil => simp [componentBudget,oddCount]
  | cons h rest ih =>
    simp only [componentBudget,oddCount,List.map_cons,List.sum_cons] at *
    omega

theorem component_bound_le_global (holes : List Nat) :
    componentBudget holes≤holes.sum/2 := by
  have h := component_parity_identity holes
  omega

theorem one_hole_per_component (holes : List Nat)
    (small : ∀ h ∈ holes, h≤1) : componentBudget holes=0 := by
  induction holes with
  | nil => simp [componentBudget]
  | cons h rest ih =>
    have hh : h≤1 := small h (by simp)
    have hr : componentBudget rest=0 := ih (by
      intro k hk
      exact small k (by simp [hk]))
    simp only [componentBudget,List.map_cons,List.sum_cons] at *
    omega

/-- If two nominal pieces share an original interval, they must first be
merged. Merging two odd hole counts loses precisely one parity credit. -/
theorem merging_two_odd_counts (a b : Nat) (ha : a%2=1) (hb : b%2=1) :
    (a+b)/2=a/2+b/2+1 := by omega

/-- The model must supply actual cancellation counts and an injective
interval allocation. This theorem formalizes their exact payment ledger,
not the graph normalization or Hall existence theorem. -/
theorem cancellation_payment_bound (a b afterA afterB paidIntervals budget : Nat)
    (conservation : afterA+b=a+afterB)
    (betas : afterB≤b) (allocation : paidIntervals≤afterA)
    (deficiencyBound : afterA≤paidIntervals+budget) :
    a-(b-afterB+paidIntervals)=afterA-paidIntervals ∧
    a≤(b-afterB+paidIntervals)+budget := by omega

#print axioms distinct_slots_bound
#print axioms subset_hole_bound
#print axioms component_parity_identity
#print axioms component_bound_le_global
#print axioms one_hole_per_component
#print axioms merging_two_odd_counts
#print axioms cancellation_payment_bound

end SubQuorum.PartialTipCompensation
