import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.BentGapPrivateReserves

def blankCount : List Bool → Nat
  | [] => 0
  | x :: xs => (if x then 0 else 1) + blankCount xs

-- Only disjoint triples are needed for the density bound. Physical feasibility
-- excludes every consecutive selected triple, which is a stronger hypothesis.
def blockSafe : List Bool → Prop
  | a :: b :: c :: xs => ¬ (a = true ∧ b = true ∧ c = true) ∧ blockSafe xs
  | _ => True

theorem selected_triple_impossible (a b c : Bool)
    (feasible : b = true → (if a then 1 else 0) + (if c then 1 else 0) ≤ (1 : Nat)) :
    ¬ (a = true ∧ b = true ∧ c = true) := by
  cases a <;> cases b <;> cases c <;> simp_all

theorem triple_has_blank (a b c : Bool) (safe : ¬ (a = true ∧ b = true ∧ c = true)) :
    1 ≤ (if a then 0 else 1) + (if b then 0 else 1) + (if c then 0 else 1) := by
  cases a <;> cases b <;> cases c <;> simp_all

theorem triple_block_density (xs : List Bool) (safe : blockSafe xs) :
    xs.length / 3 ≤ blankCount xs := by
  cases xs with
  | nil => simp [blankCount]
  | cons a tail =>
    cases tail with
    | nil => simp [blankCount]
    | cons b tail =>
      cases tail with
      | nil => simp [blankCount]
      | cons c rest =>
        have h := triple_has_blank a b c safe.1
        have ih := triple_block_density rest safe.2
        simp only [List.length_cons, blankCount]
        omega
termination_by xs.length

theorem blankCount_append (xs ys : List Bool) :
    blankCount (xs ++ ys) = blankCount xs + blankCount ys := by
  induction xs with
  | nil => simp [blankCount]
  | cons x xs ih => simp [blankCount, ih, Nat.add_assoc]

theorem anchored_end_forces_blank (next : Bool)
    (feasible : 1 + (if next then 1 else 0) ≤ (1 : Nat)) : next = false := by
  cases next <;> simp_all

theorem anchored_pressure_density (middle : List Bool) (safe : blockSafe middle) :
    2 + middle.length / 3 ≤ blankCount ([true, false] ++ middle ++ [false, true]) := by
  have ih := triple_block_density middle safe
  simp only [blankCount_append, blankCount]
  simp
  omega

theorem even_BB_ends_need_distinct_forests (half tt : Nat) :
    2 * half ≠ 2 * tt + 1 := by omega

theorem occupied_family_private_bound (w upper lower : Nat)
    (width : 6 ≤ w) (pressure : 2 + (w - 6) / 3 ≤ upper)
    (endForests : 2 ≤ lower) : w / 3 + 2 ≤ upper + lower := by omega

theorem different_bands_give_different_units (Resource : Type) (band : Resource → Nat)
    (u v : Resource) (different : band u ≠ band v) : u ≠ v := by
  intro same
  exact different (congrArg band same)

theorem private_completion_ledger (units thirds alpha beta margin : Int)
    (privateUnits : (thirds + 2) * alpha ≤ units)
    (ledger : margin = units + beta - alpha) : beta + (thirds + 1) * alpha ≤ margin := by
  simp only [Int.add_mul] at *
  omega

end SubQuorum.BentGapPrivateReserves

#print axioms SubQuorum.BentGapPrivateReserves.selected_triple_impossible
#print axioms SubQuorum.BentGapPrivateReserves.triple_has_blank
#print axioms SubQuorum.BentGapPrivateReserves.triple_block_density
#print axioms SubQuorum.BentGapPrivateReserves.blankCount_append
#print axioms SubQuorum.BentGapPrivateReserves.anchored_end_forces_blank
#print axioms SubQuorum.BentGapPrivateReserves.anchored_pressure_density
#print axioms SubQuorum.BentGapPrivateReserves.even_BB_ends_need_distinct_forests
#print axioms SubQuorum.BentGapPrivateReserves.occupied_family_private_bound
#print axioms SubQuorum.BentGapPrivateReserves.different_bands_give_different_units
#print axioms SubQuorum.BentGapPrivateReserves.private_completion_ledger
