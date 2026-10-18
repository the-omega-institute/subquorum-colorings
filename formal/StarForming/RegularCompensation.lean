import StarForming.CubicStability

namespace StarForming.RegularCompensation

theorem unused_capacity_pays_leaf_loss
    (maximum isolates unusedOne unusedTwo defect : Nat)
    (hmaximum : 3 ≤ maximum)
    (hcapacity : isolates + (maximum - 1) * unusedOne +
      (maximum - 2) * unusedTwo ≤ defect) :
    isolates + unusedOne + unusedTwo ≤ defect := by
  have hfirst : unusedOne ≤ (maximum - 1) * unusedOne := by
    have hbound : 1 ≤ maximum - 1 := by omega
    simpa using Nat.mul_le_mul_right unusedOne hbound
  have hsecond : unusedTwo ≤ (maximum - 2) * unusedTwo := by
    have hbound : 1 ≤ maximum - 2 := by omega
    simpa using Nat.mul_le_mul_right unusedTwo hbound
  omega

theorem weighted_compensation
    (weightedBase size capacityOrder beta defect : Nat)
    (hslack : weightedBase + defect = capacityOrder)
    (hexchange : 2 * size ≤ 2 * beta + defect) :
    weightedBase + 2 * size ≤ capacityOrder + 2 * beta := by
  omega

theorem regular_compensation
    (degree order size beta : Nat) (hdegree : 1 ≤ degree)
    (hweighted : (2 * degree - 1) * size + 2 * size ≤ degree * order + 2 * beta) :
    (2 * degree + 1) * size ≤ degree * order + 2 * beta := by
  have hsplit : 2 * degree + 1 = (2 * degree - 1) + 2 := by omega
  rw [hsplit, Nat.add_mul]
  exact hweighted

theorem regular_gap_bound
    (degree order size beta : Int)
    (hdegree : 1 ≤ degree)
    (hregular : (2 * degree + 1) * size ≤ degree * order + 2 * beta)
    (hbalanced : order ≤ 2 * beta) :
    (4 * degree + 2) * (size - beta) ≤ order := by
  have hpositive : 0 ≤ 2 * degree - 1 := by omega
  have hscaled := Int.mul_le_mul_of_nonneg_left hbalanced hpositive
  simp only [Int.sub_mul, Int.add_mul, Int.mul_sub,
    Int.one_mul] at hregular hscaled ⊢
  simp only [Int.mul_assoc, Int.mul_left_comm degree 2] at hregular hscaled ⊢
  omega

end StarForming.RegularCompensation
