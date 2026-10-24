import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.ForkAllocationExchange

/-- q=n+1. Interval-paid sources are A_i for i<n, K_i for i<n,
and the final K_n. J and H are distinct original interval families. -/
def chainInterval (n : Nat) : Sum (Fin n) (Option (Fin n)) →
    Sum (Fin (n+1)) (Fin (n+1))
  | .inl i => .inr ⟨i.val, by omega⟩
  | .inr (.some i) => .inl ⟨i.val+1, by omega⟩
  | .inr .none => .inr ⟨n, by omega⟩

theorem chain_intervals_injective (n : Nat) :
    Function.Injective (chainInterval n) := by
  intro a b same
  rcases a with i | (_ | i) <;> rcases b with j | (_ | j) <;>
    simp_all [chainInterval,Fin.ext_iff] <;> omega

abbrev ChainSource (n : Nat) :=
  Sum (Fin (n+1)) (Sum (Fin (n+1)) (Fin (n+1)))

/-- The source constructors distinguish A, C and K identities. -/
def chainIntervalSource (n : Nat) : Sum (Fin n) (Option (Fin n)) → ChainSource n
  | .inl i => .inl ⟨i.val, by omega⟩
  | .inr (.some i) => .inr (.inr ⟨i.val, by omega⟩)
  | .inr .none => .inr (.inr ⟨n, by omega⟩)

def chainBetaSource (n : Nat) (i : Fin (n+1)) : ChainSource n := .inr (.inl i)

theorem chain_interval_sources_injective (n : Nat) :
    Function.Injective (chainIntervalSource n) := by
  intro a b same
  rcases a with i | (_ | i) <;> rcases b with j | (_ | j) <;>
    simp_all [chainIntervalSource,Fin.ext_iff] <;> omega

theorem chain_beta_sources_injective (n : Nat) :
    Function.Injective (chainBetaSource n) := by
  intro a b same
  simpa [chainBetaSource] using same

theorem chain_payment_sources_disjoint (n : Nat)
    (a : Sum (Fin n) (Option (Fin n))) (b : Fin (n+1)) :
    chainIntervalSource n a ≠ chainBetaSource n b := by
  rcases a with i | (_ | i) <;> simp [chainIntervalSource,chainBetaSource]

/-- Every original ordinary source K_i remains paid after the chain exchange. -/
theorem every_old_ordinary_source_paid (n : Nat) (k : Fin (n+1)) :
    ∃ a, chainIntervalSource n a = (.inr (.inr k) : ChainSource n) := by
  by_cases below : k.val<n
  · refine ⟨.inr (.some ⟨k.val,below⟩), ?_⟩
    simp [chainIntervalSource]
  · refine ⟨.inr .none, ?_⟩
    simp only [chainIntervalSource,Sum.inr.injEq]
    apply Fin.ext
    simp only
    omega

/-- All old H_i interval identities remain used, although their owners
change from K_i to A_i except at the last vertex. -/
theorem every_old_interval_identity_retained (n : Nat) (j : Fin (n+1)) :
    ∃ a, chainInterval n a = (.inr j : Sum (Fin (n+1)) (Fin (n+1))) := by
  by_cases below : j.val<n
  · refine ⟨.inl ⟨j.val,below⟩, ?_⟩
    simp [chainInterval]
  · refine ⟨.inr .none, ?_⟩
    simp only [chainInterval,Sum.inr.injEq]
    apply Fin.ext
    simp only
    omega

/-- With an already covered ordinary left set of size m, a maximum joint
matching has m+g edges; the remaining h-g forks lose one payment each. -/
theorem exchange_value_ledger (h m t mu g delta : Int)
    (extra : mu=m+g) (defect : delta=h+m-mu) :
    t+h+mu = t+m+2*h-delta ∧ delta=h-g := by omega

theorem joint_defect_improves_fixed (h m mu fixedMu : Int)
    (baselineAndFixed : m+fixedMu≤mu) : h+m-mu≤h-fixedMu := by omega

/-- The two-owner condition with a fixed inside witness leaves a unique
possible outside witness. -/
theorem unique_external_witness {Owner : Type} (witness : Owner → Prop)
    (inside x y : Owner)
    (twoOwners : ∀ a b c, witness a → witness b → witness c →
      a=b ∨ a=c ∨ b=c)
    (wi : witness inside) (wx : witness x) (wy : witness y)
    (outsideX : inside≠x) (outsideY : inside≠y) : x=y := by
  rcases twoOwners inside x y wi wx wy with same | same | same
  · exact False.elim (outsideX same)
  · exact False.elim (outsideY same)
  · exact same

/-- A closed connected component with as many units as owners and one
external-entry unit must be a tree with exactly one private anchor.
Connectedness supplies the spanning-tree lower bound on internal edges. -/
theorem closed_component_single_anchor (vertices edges privateUnits : Int)
    (inventory : edges+privateUnits=vertices)
    (connected : vertices-1≤edges) (entry : 1≤privateUnits) :
    edges=vertices-1 ∧ privateUnits=1 := by omega

/-- Pairwise-neighbor formulation of feasibility for a selected vertex. -/
def SelectedFeasible {V : Type} (selected occupied : V → Prop)
    (adj : V → V → Prop) : Prop :=
  ∀ t, selected t → ∀ a b, adj t a → adj t b → occupied a → occupied b → a=b

theorem saturated_selected_guard_excludes_neighbor {V : Type}
    (selected occupied : V → Prop) (adj : V → V → Prop)
    (feasible : SelectedFeasible selected occupied adj) (t a b : V)
    (st : selected t) (ta : adj t a) (tb : adj t b)
    (oa : occupied a) (different : a≠b) : ¬occupied b := by
  intro ob
  exact different (feasible t st a b ta tb oa ob)

theorem two_old_neighbors_forbid_new_selection {V : Type}
    (selected occupied : V → Prop) (adj : V → V → Prop)
    (feasible : SelectedFeasible selected occupied adj) (v a b : V)
    (va : adj v a) (vb : adj v b) (oa : occupied a) (ob : occupied b)
    (different : a≠b) : ¬selected v := by
  intro sv
  exact different (feasible v sv a b va vb oa ob)

theorem alternating_chain_ledgers (q : Nat) (positive : 1≤q) :
    q+(2*q-1)=3*q-1 ∧
    (3*q : Int)-(3*q-1)=1 ∧
    (2*q : Int)+q-3*q=0 := by omega

#print axioms chain_intervals_injective
#print axioms chain_interval_sources_injective
#print axioms chain_beta_sources_injective
#print axioms chain_payment_sources_disjoint
#print axioms every_old_ordinary_source_paid
#print axioms every_old_interval_identity_retained
#print axioms exchange_value_ledger
#print axioms joint_defect_improves_fixed
#print axioms unique_external_witness
#print axioms closed_component_single_anchor
#print axioms saturated_selected_guard_excludes_neighbor
#print axioms two_old_neighbors_forbid_new_selection
#print axioms alternating_chain_ledgers

end SubQuorum.ForkAllocationExchange
