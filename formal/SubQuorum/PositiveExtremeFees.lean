import Std.Tactic

set_option autoImplicit false

namespace SubQuorum.PositiveExtremeFees

/-- A singleton handoff from a local legacy incidence forbids every earlier
left prerequisite. This is the ordered part of the legacy reassignment. -/
theorem legacy_singleton_has_no_earlier_gate (gate : Nat → Prop)
    (first own : Nat) (earlier : first < own)
    (handoff : ∀ g, gate g → g ≤ own → g = own) :
    ∀ g, gate g → g ≤ first → False := by
  intro g hg before
  have eq := handoff g hg (Nat.le_trans before (Nat.le_of_lt earlier))
  have ownBefore : own ≤ first := eq ▸ before
  exact Nat.not_le_of_gt earlier ownBefore

/-- Either a used legacy incidence already backs the extreme or no gate
precedes that extreme. Ordinary H access transfers by prefix inclusion. -/
theorem left_extreme_with_legacy (gate opened : Nat → Prop)
    (first used : Nat) (oldFirst oldUsed : Bool) (order : first ≤ used)
    (legacy : oldUsed = true → oldFirst = true ∨
      (∀ g, gate g → g ≤ first → False)) :
    (oldUsed = true ∨ (∀ g, gate g → g ≤ used → opened g)) →
    (oldFirst = true ∨ (∀ g, gate g → g ≤ first → opened g)) := by
  intro accessible
  cases accessible with
  | inl old =>
    cases legacy old with
    | inl backed => exact Or.inl backed
    | inr empty =>
      exact Or.inr (fun g hg before => False.elim (empty g hg before))
  | inr route =>
    exact Or.inr (fun g hg before => route g hg (Nat.le_trans before order))

/-- Inclusive prefixes can overlap suffixes only in their common endpoint
containing tile. Unlike capacity-zero gates, a positive pivot may be there. -/
theorem common_prerequisite_is_common_tile (first last g : Nat)
    (order : first ≤ last) (left : g ≤ first) (right : last ≤ g) :
    first = g ∧ last = g := by
  exact ⟨Nat.le_antisymm (Nat.le_trans order right) left,
    Nat.le_antisymm right (Nat.le_trans left order)⟩

/-- If the two extrema are in that gate tile, every intervening original
unit is in the same tile; a physical capacity-two bound then limits the gap. -/
theorem intervening_unit_in_common_tile (first last g p : Nat)
    (_order : first ≤ last) (left : g ≤ first) (right : last ≤ g)
    (insideLeft : first ≤ p) (insideRight : p ≤ last) : p = g := by
  exact Nat.le_antisymm (Nat.le_trans insideRight right) (Nat.le_trans left insideLeft)

/-- The entire discrepancy of per-end charging is exactly one duplicated
pivot fee when both ends are used. Outer prefix fees are paid separately. -/
theorem local_shared_fee_identity (leftUsed rightUsed : Bool) (pivot left right : Nat) :
    (if leftUsed then pivot + left else 0) +
      (if rightUsed then pivot + right else 0) =
    (if leftUsed || rightUsed then pivot else 0) +
      (if leftUsed then left else 0) + (if rightUsed then right else 0) +
      (if leftUsed && rightUsed then pivot else 0) := by
  cases leftUsed with
  | false =>
    cases rightUsed with
    | false => rfl
    | true =>
      change 0 + (pivot + right) = (pivot + 0) + 0 + right + 0
      exact Nat.zero_add (pivot + right)
  | true =>
    cases rightUsed with
    | false =>
      change (pivot + left) + 0 = (pivot + left) + 0 + 0
      rfl
    | true =>
      change (pivot + left) + (pivot + right) = ((pivot + left) + right) + pivot
      exact (Nat.add_assoc (pivot + left) pivot right).symm.trans
        (Nat.add_right_comm (pivot + left) pivot right)

/-- Shared output capacity or a single normalized witness forbids two uses;
then ordinary per-offer charges equal the actual union fee. -/
theorem exclusive_ends_have_no_fee_duplication
    (leftUsed rightUsed : Bool) (pivot left right : Nat)
    (exclusive : (leftUsed && rightUsed) = false) :
    (if leftUsed then pivot + left else 0) +
      (if rightUsed then pivot + right else 0) =
    (if leftUsed || rightUsed then pivot else 0) +
      (if leftUsed then left else 0) + (if rightUsed then right else 0) := by
  cases leftUsed with
  | false =>
    cases rightUsed with
    | false => rfl
    | true =>
      change 0 + (pivot + right) = (pivot + 0) + 0 + right
      exact Nat.zero_add (pivot + right)
  | true =>
    cases rightUsed with
    | false =>
      change (pivot + left) + 0 = (pivot + left) + 0
      rfl
    | true => exact Bool.noConfusion exclusive

end SubQuorum.PositiveExtremeFees

#print axioms SubQuorum.PositiveExtremeFees.legacy_singleton_has_no_earlier_gate
#print axioms SubQuorum.PositiveExtremeFees.left_extreme_with_legacy
#print axioms SubQuorum.PositiveExtremeFees.common_prerequisite_is_common_tile
#print axioms SubQuorum.PositiveExtremeFees.intervening_unit_in_common_tile
#print axioms SubQuorum.PositiveExtremeFees.local_shared_fee_identity
#print axioms SubQuorum.PositiveExtremeFees.exclusive_ends_have_no_fee_duplication
