import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.IsolatedCoverageObstruction

inductive Reach {V : Type} (edge : V → V → Prop) (root : V) : V → Prop
  | refl : Reach edge root root
  | step {u v : V} : Reach edge root u → edge u v → Reach edge root v

/-- No bound on route length is imposed. -/
theorem root_closure {V : Type} (edge : V → V → Prop) (root : V)
    (noOutgoing : ∀ v, ¬edge root v) (v : V) (path : Reach edge root v) : v=root := by
  induction path with
  | refl => rfl
  | step path link ih => exact False.elim (noOutgoing _ (ih ▸ link))

/-- A terminal payment may use a supported original unit or a beta gate.
Both are impossible in a singleton closure having neither at its root. -/
theorem no_terminal_payment {V Q : Type} (edge : V → V → Prop)
    (support : V → Q → Prop) (beta : V → Prop) (root : V)
    (noOutgoing : ∀ v, ¬edge root v)
    (noSupport : ∀ q, ¬support root q) (notBeta : ¬beta root) :
    ¬∃ v, Reach edge root v ∧ ((∃ q, support v q) ∨ beta v) := by
  rintro ⟨v,path,terminal⟩
  have same := root_closure edge root noOutgoing v path
  subst v
  rcases terminal with ⟨q,paid⟩ | gate
  · exact noSupport q paid
  · exact notBeta gate

/-- The selected barrier has an occupied endpoint neighbor, so it is not
an occupied-isolated candidate. -/
theorem seal_not_isolated {V : Type} (occupied : V → Prop)
    (adjacent : V → V → Prop) (barrier endpoint : V)
    (endpointOccupied : occupied endpoint) (neighbor : adjacent barrier endpoint) :
    ¬(∀ v, adjacent barrier v → ¬occupied v) := by
  intro isolated
  exact isolated endpoint neighbor endpointOccupied

theorem seal_survives_deletion {V : Type} (selected removed : V → Prop)
    (occupied : V → Prop) (adjacent : V → V → Prop) (barrier endpoint : V)
    (selectedSeal : selected barrier) (endpointOccupied : occupied endpoint)
    (neighbor : adjacent barrier endpoint)
    (onlyIsolated : ∀ x, removed x → ∀ v, adjacent x v → ¬occupied v) :
    selected barrier ∧ ¬removed barrier := by
  refine ⟨selectedSeal,?_⟩
  intro deleted
  exact onlyIsolated barrier deleted endpoint neighbor endpointOccupied

/-- Removing isolated points preserves every occupied neighbor of a remaining
selected point. The point used as a neighbor cannot have been removed. -/
theorem occupied_neighbors_preserved {V : Type} (occupied selected removed : V → Prop)
    (adjacent : V → V → Prop) (s v : V)
    (selectedOccupied : ∀ x, selected x → occupied x) (hs : selected s)
    (symmetric : ∀ x y, adjacent x y → adjacent y x)
    (onlyIsolated : ∀ x, removed x → ∀ y, adjacent x y → ¬occupied y)
    (neighbor : adjacent s v) : (occupied v ∧ ¬removed v) ↔ occupied v := by
  constructor
  · exact And.left
  · intro hv
    refine ⟨hv,?_⟩
    intro deleted
    exact onlyIsolated v deleted s (symmetric s v neighbor) (selectedOccupied s hs)

/-- Changes to auxiliary pairs outside P x P preserve the full PP graph. -/
theorem pp_graph_preserved {V : Type} (P : V → Prop) (N N' : V → V → Prop)
    (changeOutside : ∀ u v, P u → P v → (N u v ↔ N' u v)) :
    (fun u v => P u ∧ P v ∧ N u v)=(fun u v => P u ∧ P v ∧ N' u v) := by
  funext u v
  apply propext
  constructor
  · rintro ⟨hu,hv,h⟩
    exact ⟨hu,hv,(changeOutside u v hu hv).mp h⟩
  · rintro ⟨hu,hv,h⟩
    exact ⟨hu,hv,(changeOutside u v hu hv).mpr h⟩

theorem private_guard_assignment_injective (band : Nat → Nat)
    (differentBands : ∀ a b, band a=band b → a=b) (a b : Nat)
    (same : (band a,2,2)=(band b,2,2)) : a=b := by
  exact differentBands a b (congrArg Prod.fst same)

theorem two_guards_distinct (band w : Nat) (width : 8≤w) :
    (band,2,2)≠(band,w-1,w-1) := by
  intro same
  have h := congrArg (fun x : Nat × Nat × Nat => x.2.1) same
  change 2=w-1 at h
  omega

/-- Integer form avoids hiding natural-subtraction side conditions;
W=2n, n>=4, k>=1 in the coordinate specialization. -/
theorem isolated_count_identity (n k : Int) :
    ((7*k+2)*n+3*k+2) - (k*(2*n+12)+8) = k*(5*n-9)+2*n-6 := by
  simp only [Int.add_mul,Int.mul_add,Int.mul_sub,Int.mul_assoc,Int.mul_left_comm k]
  omega

theorem all_deleted_slack_identity (n k : Int) :
    2*k+(k*(5*n-9)+2*n-6)=k*(5*n-7)+2*n-6 := by
  simp only [Int.mul_sub]
  omega

theorem exact_partial_flip (k flips value : Nat) (within : flips≤k)
    (blockedUpper : value≤flips) (privateLower : flips≤value) :
    value=flips ∧ k-value=k-flips := by omega

theorem full_payment_iff_all_strips (k flips : Nat) (within : flips≤k) :
    k-flips=0 ↔ flips=k := by omega

theorem deletion_adds_slack_without_payment (oldSlack deleted oldValue newValue : Nat)
    (noGain : newValue=oldValue) :
    oldSlack+deleted+oldValue-newValue=oldSlack+deleted := by omega

#print axioms root_closure
#print axioms no_terminal_payment
#print axioms seal_not_isolated
#print axioms seal_survives_deletion
#print axioms occupied_neighbors_preserved
#print axioms pp_graph_preserved
#print axioms private_guard_assignment_injective
#print axioms two_guards_distinct
#print axioms isolated_count_identity
#print axioms all_deleted_slack_identity
#print axioms exact_partial_flip
#print axioms full_payment_iff_all_strips
#print axioms deletion_adds_slack_without_payment

end SubQuorum.IsolatedCoverageObstruction
