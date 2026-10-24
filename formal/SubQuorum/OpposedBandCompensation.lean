import SubQuorum.BandCompensation

set_option autoImplicit false

namespace SubQuorum.OpposedBandCompensation

open SubQuorum.BandCompensation

def verticalValid (column : Column) : Prop :=
  (upper column = 1 → lower column = 0) ∧
    (lower column = 1 → upper column = 0)

instance (column : Column) : Decidable (verticalValid column) :=
  inferInstanceAs (Decidable
    ((upper column = 1 → lower column = 0) ∧
      (lower column = 1 → upper column = 0)))

theorem column_nonnegative : ∀ column : Column,
    verticalValid column → (0 : Int) ≤ weight column := by
  decide

theorem interior_nonnegative (middle : List Column)
    (hvalid : ∀ column ∈ middle, verticalValid column) :
    (0 : Int) ≤ weightSum middle := by
  induction middle with
  | nil => simp [weightSum]
  | cons column rest inductionHypothesis =>
      have hcolumn := column_nonnegative column (hvalid column (by simp))
      have hrest := inductionHypothesis (by
        intro following hfollowing
        exact hvalid following (by simp [hfollowing]))
      simp only [weightSum, List.map_cons, List.sum_cons] at *
      omega

theorem opposed_band_blank_surplus (middle : List Column)
    (hvalid : ∀ column ∈ middle, verticalValid column) :
    (4 : Int) ≤ weightSum (0 :: middle ++ [0]) := by
  have hmiddle := interior_nonnegative middle hvalid
  have hblank : weight (0 : Column) = 2 := by decide
  simp only [weightSum, List.map_cons, List.map_append, List.map_nil,
    List.sum_cons, List.sum_append, List.sum_nil, hblank] at *
  omega

theorem opposed_matching_compensation (middle : List Column)
    (hvalid : ∀ column ∈ middle, verticalValid column)
    (internal crossing : Nat)
    (hvertices : (2 * (0 :: middle ++ [0]).length : Nat) =
      selectedCount (0 :: middle ++ [0]) + blankCount (0 :: middle ++ [0]) +
        2*internal + crossing) :
    (2*selectedCount (0 :: middle ++ [0]) + 2*internal + crossing : Nat) +
      4 + crossing % 2 ≤ 2 * (0 :: middle ++ [0]).length := by
  have hband := opposed_band_blank_surplus middle hvalid
  have hcounts := weightSum_eq_counts (0 :: middle ++ [0])
  omega

theorem opposed_charge_compensation (middle : List Column)
    (hvalid : ∀ column ∈ middle, verticalValid column)
    (internal crossing saturatedExports : Nat) (chargeTwice : Int)
    (hvertices : (2 * (0 :: middle ++ [0]).length : Nat) =
      selectedCount (0 :: middle ++ [0]) + blankCount (0 :: middle ++ [0]) +
        2*internal + crossing)
    (hcharge : chargeTwice = 2*(selectedCount (0 :: middle ++ [0]) : Int) +
      2*internal + crossing - 2*(0 :: middle ++ [0]).length + saturatedExports) :
    chargeTwice + 4 + crossing % 2 ≤ saturatedExports := by
  have hband := opposed_matching_compensation middle hvalid internal crossing hvertices
  omega

theorem two_source_compensation (middle : List Column)
    (hvalid : ∀ column ∈ middle, verticalValid column)
    (internal crossing saturatedExports : Nat)
    (bandChargeTwice upperChargeTwice lowerChargeTwice : Int)
    (hvertices : (2 * (0 :: middle ++ [0]).length : Nat) =
      selectedCount (0 :: middle ++ [0]) + blankCount (0 :: middle ++ [0]) +
        2*internal + crossing)
    (hcharge : bandChargeTwice = 2*(selectedCount (0 :: middle ++ [0]) : Int) +
      2*internal + crossing - 2*(0 :: middle ++ [0]).length + saturatedExports)
    (hupper : upperChargeTwice ≤ 2) (hlower : lowerChargeTwice ≤ 2)
    (hbudget : saturatedExports ≤ crossing % 2) :
    upperChargeTwice + bandChargeTwice + lowerChargeTwice ≤ 0 := by
  have hband := opposed_charge_compensation middle hvalid internal crossing
    saturatedExports bandChargeTwice hvertices hcharge
  omega

end SubQuorum.OpposedBandCompensation
