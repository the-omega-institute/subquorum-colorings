import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.GeneralBridgeRetention

/-- Retaining the already used private whole-beta output, with at most two
physical BP entries, leaves capacity for at most one original interval.
Hence this beta needs no identity-changing normalization. -/
theorem saturated_beta_already_normal
    (paths whole intervals : Nat) (private_used : whole = 1)
    (ports : paths ≤ 2) (balance : whole + intervals = paths) :
    1 ≤ paths ∧ intervals ≤ 1 ∧ intervals + 1 = paths := by
  omega

/-- A fully paid closed deficient request tree, retaining all n-1 original
units and its private beta credits, has one more outgoing than incoming
physical route. Two outgoing bridges and one incoming bridge are consistent
with one repaired tree: bounding the outgoing count alone is incorrect. -/
theorem closed_repaired_tree_flux
    (n beta paid units incoming outgoing : Nat)
    (positive : 1 ≤ n) (original_units : units = n - 1)
    (all_paid : paid = n + beta)
    (conservation : paid + incoming = units + beta + outgoing) :
    outgoing = incoming + 1 := by
  omega

/-- With at most m new links, scaling integer fees by m+1 makes fee the
primary minimization criterion, while a unit charge counts actual new links. -/
theorem fee_dominates_new_link_count
    (m cheapFee dearFee cheapCount dearCount : Nat)
    (count_bound : cheapCount ≤ m) (fee_order : cheapFee < dearFee) :
    cheapFee * (m + 1) + cheapCount < dearFee * (m + 1) + dearCount := by
  have step : cheapFee + 1 ≤ dearFee := by omega
  have scaled := Nat.mul_le_mul_right (m + 1) step
  simp only [Nat.add_mul, Nat.one_mul] at scaled
  omega

end SubQuorum.GeneralBridgeRetention

#print axioms SubQuorum.GeneralBridgeRetention.saturated_beta_already_normal
#print axioms SubQuorum.GeneralBridgeRetention.closed_repaired_tree_flux
#print axioms SubQuorum.GeneralBridgeRetention.fee_dominates_new_link_count
