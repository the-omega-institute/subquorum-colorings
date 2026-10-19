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

theorem positive_excess_matching_budget (capacity left right matching excess order : Int)
    (hcapacity : 0 < capacity) (hleft : 0 ≤ left) (hright : 0 ≤ right)
    (hexcess : 0 < excess)
    (hleftPacking : capacity * (left + excess) ≤ left * (left - 1))
    (hrightPacking : capacity * (right + excess) ≤ right * (right - 1))
    (hpartition : matching + left + right + excess = order) :
    matching + excess ≤ order - 2 * capacity - 4 := by
  have hleftBound := packing_forces_many_unused capacity left excess
    hcapacity hleft hexcess hleftPacking
  have hrightBound := packing_forces_many_unused capacity right excess
    hcapacity hright hexcess hrightPacking
  omega

theorem zero_excess_packing (capacity unused : Int) (hunused : 0 ≤ unused)
    (hpacking : capacity * unused ≤ unused * (unused - 1)) :
    unused = 0 ∨ capacity + 1 ≤ unused := by
  by_cases hzero : unused = 0
  · exact Or.inl hzero
  · apply Or.inr
    apply Classical.byContradiction
    intro hsmall
    have hfactor : unused - 1 ≤ capacity - 1 := by omega
    have hproduct := Int.mul_le_mul_of_nonneg_left hfactor hunused
    have hexpand : unused * (capacity - 1) = capacity * unused - unused := by
      simp [Int.mul_sub, Int.mul_comm]
    omega

theorem optimal_support_one_side (capacity left right matching order : Int)
    (hleft : 0 ≤ left) (hright : 0 ≤ right) (hmatching : 0 ≤ matching)
    (hleftPacking : capacity * left ≤ left * (left - 1))
    (hrightPacking : capacity * right ≤ right * (right - 1))
    (hpartition : matching + left + right = order)
    (horder : order ≤ 2 * capacity + 1) : left = 0 ∨ right = 0 := by
  rcases zero_excess_packing capacity left hleft hleftPacking with hzero | hbound
  · exact Or.inl hzero
  · rcases zero_excess_packing capacity right hright hrightPacking with hzero | hother
    · exact Or.inr hzero
    · omega

def pappusNeighbors (vertex : Fin 18) : List Nat :=
  match vertex.val with
  | 0 => [1, 5, 17]
  | 1 => [0, 2, 8]
  | 2 => [1, 3, 13]
  | 3 => [2, 4, 10]
  | 4 => [3, 5, 15]
  | 5 => [0, 4, 6]
  | 6 => [5, 7, 11]
  | 7 => [6, 8, 14]
  | 8 => [1, 7, 9]
  | 9 => [8, 10, 16]
  | 10 => [3, 9, 11]
  | 11 => [6, 10, 12]
  | 12 => [11, 13, 17]
  | 13 => [2, 12, 14]
  | 14 => [7, 13, 15]
  | 15 => [4, 14, 16]
  | 16 => [9, 15, 17]
  | 17 => [0, 12, 16]
  | _ => []

def pappusSelected : List Nat := [0, 1, 4, 6, 7, 9, 10, 12, 13, 15]

set_option maxRecDepth 8192 in
set_option maxHeartbeats 800000 in
theorem pappus_regular_bipartite_certificate :
    (∀ vertex : Fin 18, (pappusNeighbors vertex).length = 3 ∧
      (pappusNeighbors vertex).Nodup ∧
      ∀ neighbor, neighbor ∈ pappusNeighbors vertex →
        neighbor < 18 ∧ neighbor % 2 ≠ vertex.val % 2) ∧
    (∀ first second : Fin 18,
      second.val ∈ pappusNeighbors first ↔ first.val ∈ pappusNeighbors second) := by
  decide

set_option maxRecDepth 8192 in
set_option maxHeartbeats 800000 in
theorem pappus_no_four_cycle_certificate :
    ∀ first second : Fin 18, first ≠ second →
      ((pappusNeighbors first).filter (fun vertex =>
        (pappusNeighbors second).contains vertex)).length ≤ 1 := by
  decide

set_option maxRecDepth 8192 in
set_option maxHeartbeats 800000 in
theorem pappus_dissociation_certificate :
    pappusSelected.length = 10 ∧ pappusSelected.Nodup ∧
    (∀ vertex, vertex ∈ pappusSelected → vertex < 18) ∧
    (∀ vertex : Fin 18, vertex.val ∈ pappusSelected →
      ((pappusNeighbors vertex).filter (fun neighbor =>
        pappusSelected.contains neighbor)).length ≤ 1) := by
  decide

end Subquorum.C4FreeRepresentatives
