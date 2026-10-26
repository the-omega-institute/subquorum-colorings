import Std.Tactic

set_option autoImplicit false

namespace SubQuorum.ProtectedCorridorExtremes

/-- Reaching a later resource opens every gate needed for the first. -/
theorem left_extreme_reachable (isGate opened : Nat → Prop) (first used : Nat)
    (order : first ≤ used)
    (route : ∀ g, isGate g → g < used → opened g) :
    ∀ g, isGate g → g < first → opened g := by
  intro g hg before
  exact route g hg (Nat.lt_of_lt_of_le before order)

/-- Reaching an earlier resource from the right opens every gate after last. -/
theorem right_extreme_reachable (isGate opened : Nat → Prop) (used last : Nat)
    (order : used ≤ last)
    (route : ∀ g, isGate g → used < g → opened g) :
    ∀ g, isGate g → last < g → opened g := by
  intro g hg after
  exact route g hg (Nat.lt_of_le_of_lt order after)

/-- The two retained payment offers never charge the same actual gate. -/
theorem extreme_prerequisites_disjoint (first last : Nat)
    (order : first ≤ last) :
    ∀ g : Nat, ¬ (g < first ∧ last < g) := by
  intro g both
  omega

/-- Two original units give genuinely different valid extreme IDs.
The one-unit corridor cannot use this lemma to duplicate its resource. -/
theorem distinct_valid_extreme_indices (units : Nat) (two : 2 ≤ units) :
    0 < units ∧ units - 1 < units ∧ (0 : Nat) ≠ units - 1 := by
  omega

end SubQuorum.ProtectedCorridorExtremes

#print axioms SubQuorum.ProtectedCorridorExtremes.left_extreme_reachable
#print axioms SubQuorum.ProtectedCorridorExtremes.right_extreme_reachable
#print axioms SubQuorum.ProtectedCorridorExtremes.extreme_prerequisites_disjoint
#print axioms SubQuorum.ProtectedCorridorExtremes.distinct_valid_extreme_indices
