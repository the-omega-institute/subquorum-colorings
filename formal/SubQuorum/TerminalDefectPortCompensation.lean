import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.TerminalDefectPortCompensation

/-- On a path with vertices 0,...,m, choose the edge toward a fixed root.
    Edge i has endpoints i and i+1. The root itself is excluded. -/
def parentEdge (root vertex : Nat) : Nat :=
  if vertex < root then vertex else vertex - 1

theorem parent_edge_incident (root vertex : Nat) :
    parentEdge root vertex = vertex ∨ parentEdge root vertex + 1 = vertex := by
  unfold parentEdge
  split <;> omega

theorem parent_edge_in_range (m root vertex : Nat) (rootBound : root ≤ m)
    (vertexBound : vertex ≤ m) (different : vertex ≠ root) :
    parentEdge root vertex < m := by
  unfold parentEdge
  split <;> omega

theorem parent_edges_injective (root u v : Nat) (uNotRoot : u ≠ root)
    (vNotRoot : v ≠ root) (same : parentEdge root u = parentEdge root v) : u = v := by
  unfold parentEdge at same
  split at same <;> split at same <;> omega

theorem full_path_assignment (m edge : Nat) (edgeBound : edge < m) :
    edge + 1 ≤ m ∧ edge + 1 ≠ 0 ∧ (edge + 1) - 1 = edge := by omega

theorem full_path_assignment_injective (u v : Nat) (same : u + 1 = v + 1) :
    u = v := by omega

/-- Original zeros are only path ends; arbitrary removals may be internal. -/
inductive Profile where
  | path (originalZeros : Fin 3) (removed : Nat)
  | cycle (removed : Nat)

def initialDeficit : Profile → Nat
  | .path z _ => z.val - 1
  | .cycle _ => 0

def finalDeficit : Profile → Nat
  | .path z r => z.val + r - 1
  | .cycle r => r

def zeros : Profile → Nat
  | .path z _ => z.val
  | .cycle _ => 0

def removed : Profile → Nat
  | .path _ r => r
  | .cycle r => r

def total (measure : Profile → Nat) : List Profile → Nat
  | [] => 0
  | p :: rest => measure p + total measure rest

theorem initial_half_tax (profiles : List Profile) :
    2 * total initialDeficit profiles ≤ total zeros profiles := by
  induction profiles with
  | nil => decide
  | cons p rest ih =>
    cases p with
    | cycle r => simpa [total, initialDeficit, zeros] using ih
    | path z r =>
      have bound := z.isLt
      simp only [total, initialDeficit, zeros]
      omega

theorem simultaneous_withdrawal_bound (profiles : List Profile) :
    total finalDeficit profiles ≤ total initialDeficit profiles + total removed profiles := by
  induction profiles with
  | nil => decide
  | cons p rest ih =>
    cases p with
    | cycle r => simp only [total, finalDeficit, initialDeficit, removed]; omega
    | path z r => simp only [total, finalDeficit, initialDeficit, removed]; omega

theorem joint_half_tax_with_withdrawals (profiles : List Profile) :
    2 * total finalDeficit profiles ≤ total zeros profiles + 2 * total removed profiles := by
  have tax := initial_half_tax profiles
  have loss := simultaneous_withdrawal_bound profiles
  omega

theorem defect_free_profiles_pay_all (profiles : List Profile)
    (noZeros : total zeros profiles = 0) : total initialDeficit profiles = 0 := by
  have bound := initial_half_tax profiles
  omega

theorem one_terminal_defect_still_pays_all (profiles : List Profile)
    (atMostOne : total zeros profiles ≤ 1) : total initialDeficit profiles = 0 := by
  have bound := initial_half_tax profiles
  omega

theorem path_first_withdrawal_is_free : finalDeficit (.path ⟨0, by decide⟩ 1) = 0 := by
  decide

theorem cycle_withdrawal_loses_one_per_unit (r : Nat) : finalDeficit (.cycle r) = r := rfl

theorem two_missing_ends_are_one_debit :
    initialDeficit (.path ⟨2, by decide⟩ 0) = 1 := by decide

theorem ledger_from_distinct_interval_payments (L beta alpha deficit margin : Int)
    (originalLedger : margin = L + beta - alpha)
    (distinctPayments : alpha - deficit ≤ L) : beta - deficit ≤ margin := by omega

theorem coefficient_one_criterion (L beta alpha deficit degreeFour boundary margin : Int)
    (originalLedger : margin = L + beta - alpha)
    (distinctPayments : alpha - deficit ≤ L)
    (ownedHalfTax : 2 * deficit ≤ degreeFour + boundary)
    (criterion : degreeFour + boundary ≤ 2 * beta + 1) : 0 ≤ margin := by omega

theorem full_pool_zero_link_upper_bound (k value links : Nat)
    (portPayment : k ≤ value) (sourceBound : value ≤ k) (noLinks : links = 0) :
    value = k ∧ links = 0 := by omega

end SubQuorum.TerminalDefectPortCompensation

#print axioms SubQuorum.TerminalDefectPortCompensation.parent_edge_incident
#print axioms SubQuorum.TerminalDefectPortCompensation.parent_edge_in_range
#print axioms SubQuorum.TerminalDefectPortCompensation.parent_edges_injective
#print axioms SubQuorum.TerminalDefectPortCompensation.full_path_assignment
#print axioms SubQuorum.TerminalDefectPortCompensation.full_path_assignment_injective
#print axioms SubQuorum.TerminalDefectPortCompensation.initial_half_tax
#print axioms SubQuorum.TerminalDefectPortCompensation.simultaneous_withdrawal_bound
#print axioms SubQuorum.TerminalDefectPortCompensation.joint_half_tax_with_withdrawals
#print axioms SubQuorum.TerminalDefectPortCompensation.defect_free_profiles_pay_all
#print axioms SubQuorum.TerminalDefectPortCompensation.one_terminal_defect_still_pays_all
#print axioms SubQuorum.TerminalDefectPortCompensation.path_first_withdrawal_is_free
#print axioms SubQuorum.TerminalDefectPortCompensation.cycle_withdrawal_loses_one_per_unit
#print axioms SubQuorum.TerminalDefectPortCompensation.two_missing_ends_are_one_debit
#print axioms SubQuorum.TerminalDefectPortCompensation.ledger_from_distinct_interval_payments
#print axioms SubQuorum.TerminalDefectPortCompensation.coefficient_one_criterion
#print axioms SubQuorum.TerminalDefectPortCompensation.full_pool_zero_link_upper_bound
