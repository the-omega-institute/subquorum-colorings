import Std

namespace Subquorum.C4FreeRepresentatives

def NoFourCycle {Vertex : Type} (adjacency : Vertex → Vertex → Prop) : Prop :=
  ∀ first second left right, first ≠ second → left ≠ right →
    first ≠ left → first ≠ right → second ≠ left → second ≠ right →
    adjacency first left → adjacency first right →
    adjacency second left → adjacency second right → False

theorem neighbor_pair_unique_owner {Vertex : Type}
    {adjacency : Vertex → Vertex → Prop} (hfree : NoFourCycle adjacency)
    (first second left right : Vertex) (hpair : left ≠ right)
    (hfirstLeft : first ≠ left) (hfirstRight : first ≠ right)
    (hsecondLeft : second ≠ left) (hsecondRight : second ≠ right)
    (hfirstEdge : adjacency first left) (hfirstOther : adjacency first right)
    (hsecondEdge : adjacency second left) (hsecondOther : adjacency second right) :
    first = second := by
  apply Classical.byContradiction
  intro hdifferent
  exact hfree first second left right hdifferent hpair hfirstLeft hfirstRight
    hsecondLeft hsecondRight hfirstEdge hfirstOther hsecondEdge hsecondOther

theorem packing_forces_many_unused (capacity unused excess : Int)
    (hcapacity : 0 < capacity) (hunused : 0 ≤ unused) (hexcess : 0 < excess)
    (hpacking : capacity * (unused + excess) ≤ unused * (unused - 1)) :
    capacity + 2 ≤ unused := by
  apply Classical.byContradiction
  intro hsmall
  have hfactor : unused - 1 ≤ capacity := by omega
  have hproduct := Int.mul_le_mul_of_nonneg_left hfactor hunused
  have hpositive : 0 < capacity * excess := Int.mul_pos hcapacity hexcess
  have hexpand : capacity * (unused + excess) =
      unused * capacity + capacity * excess := by
    simp [Int.mul_add, Int.mul_comm]
  omega

theorem positive_excess_size_threshold (capacity left right matching excess order : Int)
    (hcapacity : 0 < capacity) (hleft : 0 ≤ left) (hright : 0 ≤ right)
    (hmatching : 0 ≤ matching) (hexcess : 0 < excess)
    (hleftPacking : capacity * (left + excess) ≤ left * (left - 1))
    (hrightPacking : capacity * (right + excess) ≤ right * (right - 1))
    (hpartition : matching + left + right + excess = order) :
    2 * capacity + 5 ≤ order := by
  have hleftBound := packing_forces_many_unused capacity left excess
    hcapacity hleft hexcess hleftPacking
  have hrightBound := packing_forces_many_unused capacity right excess
    hcapacity hright hexcess hrightPacking
  omega

theorem no_positive_excess_below_threshold (capacity left right matching excess order : Int)
    (hcapacity : 0 < capacity) (hleft : 0 ≤ left) (hright : 0 ≤ right)
    (hmatching : 0 ≤ matching) (hexcess : 0 < excess)
    (hleftPacking : capacity * (left + excess) ≤ left * (left - 1))
    (hrightPacking : capacity * (right + excess) ≤ right * (right - 1))
    (hpartition : matching + left + right + excess = order)
    (horder : order ≤ 2 * capacity + 4) : False := by
  have hthreshold := positive_excess_size_threshold capacity left right matching excess order
    hcapacity hleft hright hmatching hexcess hleftPacking hrightPacking hpartition
  omega

end Subquorum.C4FreeRepresentatives
