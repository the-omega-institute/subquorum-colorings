import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.DegreeChangingBentCompletions

-- The selected candidate already sees its own P anchor. An occupied N-mate
-- across the square would be a second, different occupied neighbour.
theorem square_conversion_requires_blank (candidate otherOccupied : Bool)
    (feasible : candidate = true → 1 + (if otherOccupied then 1 else 0) ≤ (1 : Nat))
    (converted : candidate = true) : otherOccupied = false := by
  cases candidate <;> cases otherOccupied <;> simp_all

theorem square_beta_not_both_converted (left right : Bool)
    (feasible : left = true → 1 + (if right then 1 else 0) ≤ (1 : Nat)) :
    ¬ (left = true ∧ right = true) := by
  cases left <;> cases right <;> simp_all

theorem fixed_body_transition_ledger
    (alpha beta nextAlpha nextBeta oneBeta twoBeta mixedBirth converted : Int)
    (alphas : nextAlpha = alpha + twoBeta + mixedBirth)
    (betas : nextBeta + oneBeta + twoBeta = beta)
    (ends : converted = oneBeta + 2 * twoBeta + mixedBirth) :
    nextBeta - nextAlpha = beta - alpha - converted := by omega

theorem exact_resource_transition
    (oldUnits nextUnits added converted oldSlack nextSlack : Int)
    (physical : nextSlack = oldSlack - added)
    (inventory : nextSlack - oldSlack = nextUnits - oldUnits - converted) :
    nextUnits = oldUnits - added + converted := by omega

theorem endpoint_birth_budget (mixedBirth betaBirth badEnds : Nat)
    (witnesses : mixedBirth + 2 * betaBirth ≤ badEnds) :
    mixedBirth + betaBirth ≤ badEnds := by omega

theorem no_bad_ends_no_new_alpha (alpha nextAlpha mixedBirth betaBirth : Nat)
    (inventory : nextAlpha = alpha + mixedBirth + betaBirth)
    (protectedEnds : mixedBirth + 2 * betaBirth ≤ 0) : nextAlpha = alpha := by omega

-- A graph adapter assigns a physical edge to its unique fixed M/PP body.
-- This section checks the witness injection without finiteness assumptions.
theorem owned_edge_witness_injective (Source Edge : Type)
    (body : Edge → Source) (choose : Source → Edge)
    (belongs : ∀ a, body (choose a) = a) :
    ∀ a b, choose a = choose b → a = b := by
  intro a b same
  have h := congrArg body same
  rw [belongs a, belongs b] at h
  exact h

theorem two_old_neighbours_forbid_new_selection (candidate : Bool)
    (feasible : candidate = true → 2 ≤ (1 : Nat)) : candidate = false := by
  cases candidate <;> simp_all

theorem width_six_upper_gap_positive (units : Nat) (a b : Bool)
    (zeroWouldFill : units = 0 → a = true ∧ b = true)
    (anchored : a = true → 1 + (if b then 1 else 0) ≤ (1 : Nat)) : 1 ≤ units := by
  have h := square_beta_not_both_converted a b anchored
  by_cases z : units = 0
  · exact False.elim (h (zeroWouldFill z))
  · omega

theorem private_withdrawal_floor (g unpaid removed : Nat)
    (familyCapacity : g = 2 ∨ g = 3) (disjointTax : g * unpaid ≤ removed) :
    unpaid ≤ removed / g := by
  rcases familyCapacity with h | h <;> subst g <;> omega

theorem two_private_unit_ledger (units alpha beta slack : Int)
    (privateUnits : 2 * alpha ≤ units)
    (ledger : slack = units + beta - alpha) : beta + alpha ≤ slack := by omega

theorem three_private_unit_ledger (units alpha beta slack : Int)
    (privateUnits : 3 * alpha ≤ units)
    (ledger : slack = units + beta - alpha) : beta + 2 * alpha ≤ slack := by omega

end SubQuorum.DegreeChangingBentCompletions

#print axioms SubQuorum.DegreeChangingBentCompletions.square_conversion_requires_blank
#print axioms SubQuorum.DegreeChangingBentCompletions.square_beta_not_both_converted
#print axioms SubQuorum.DegreeChangingBentCompletions.fixed_body_transition_ledger
#print axioms SubQuorum.DegreeChangingBentCompletions.exact_resource_transition
#print axioms SubQuorum.DegreeChangingBentCompletions.endpoint_birth_budget
#print axioms SubQuorum.DegreeChangingBentCompletions.no_bad_ends_no_new_alpha
#print axioms SubQuorum.DegreeChangingBentCompletions.owned_edge_witness_injective
#print axioms SubQuorum.DegreeChangingBentCompletions.two_old_neighbours_forbid_new_selection
#print axioms SubQuorum.DegreeChangingBentCompletions.width_six_upper_gap_positive
#print axioms SubQuorum.DegreeChangingBentCompletions.private_withdrawal_floor
#print axioms SubQuorum.DegreeChangingBentCompletions.two_private_unit_ledger
#print axioms SubQuorum.DegreeChangingBentCompletions.three_private_unit_ledger
