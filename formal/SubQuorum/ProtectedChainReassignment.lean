import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.ProtectedChainReassignment

theorem full_path_allocation_forced_right (edgeCount : Nat) (pay : Nat → Nat)
    (incident : ∀ edge, edge < edgeCount → pay edge = edge ∨ pay edge = edge + 1)
    (rootReserved : ∀ edge, edge < edgeCount → pay edge ≠ 0)
    (unitCapacity : ∀ first, first < edgeCount → ∀ second, second < edgeCount →
      pay first = pay second → first = second) :
    ∀ edge, edge < edgeCount → pay edge = edge + 1 := by
  intro edge
  induction edge with
  | zero =>
    intro bound
    rcases incident 0 bound with atRoot | atNext
    · exact False.elim (rootReserved 0 bound atRoot)
    · exact atNext
  | succ edge previous =>
    intro bound
    rcases incident (edge + 1) bound with atCurrent | atNext
    · have previousBound : edge < edgeCount := by omega
      have previousPay := previous previousBound
      have same : pay edge = pay (edge + 1) := previousPay.trans atCurrent.symm
      have impossible := unitCapacity edge previousBound (edge + 1) bound same
      omega
    · exact atNext

theorem every_old_assignment_changes (edgeCount : Nat) (pay : Nat → Nat)
    (incident : ∀ edge, edge < edgeCount → pay edge = edge ∨ pay edge = edge + 1)
    (rootReserved : ∀ edge, edge < edgeCount → pay edge ≠ 0)
    (unitCapacity : ∀ first, first < edgeCount → ∀ second, second < edgeCount →
      pay first = pay second → first = second) :
    ∀ edge, edge < edgeCount → pay edge ≠ edge := by
  intro edge bound
  have forced := full_path_allocation_forced_right edgeCount pay incident rootReserved
    unitCapacity edge bound
  omega

end SubQuorum.ProtectedChainReassignment

#print axioms SubQuorum.ProtectedChainReassignment.full_path_allocation_forced_right
#print axioms SubQuorum.ProtectedChainReassignment.every_old_assignment_changes
