import SubQuorum.SteppedPatchIsolation

set_option autoImplicit false

namespace SubQuorum.FrozenRailElbows

open FrozenPromotion

theorem anchored_frozen_chain {Vertex : Type}
    (adjacent : Vertex → Vertex → Prop) (selected : Vertex → Prop)
    (mate : Vertex → Vertex) (wave anchor : Nat → Vertex)
    (cap : Vertex) (length : Nat)
    (hinvolution : ∀ vertex, mate (mate vertex) = vertex)
    (hcap : selected cap) (hcapAdjacent : adjacent (wave 0) cap)
    (hcapDistinct : cap ≠ anchor 0)
    (hanchorAdjacent : ∀ index, index ≤ length → adjacent (wave index) (anchor index))
    (hanchorFrozen : ∀ index, index ≤ length →
      Frozen adjacent selected mate (mate (anchor index)))
    (hpreviousAdjacent : ∀ index, index < length →
      adjacent (wave (index+1)) (mate (wave index)))
    (hdistinct : ∀ index, index < length →
      anchor (index+1) ≠ mate (wave index)) :
    ∀ index, index ≤ length → Frozen adjacent selected mate (wave index) := by
  intro index
  induction index with
  | zero =>
      intro hbound
      exact Frozen.selected_frozen _ cap (anchor 0) hcapAdjacent
        (hanchorAdjacent 0 hbound) hcapDistinct hcap (hanchorFrozen 0 hbound)
  | succ index inductionHypothesis =>
      intro hbound
      apply Frozen.two_frozen _ (anchor (index+1)) (mate (wave index))
      · exact hanchorAdjacent (index+1) hbound
      · exact hpreviousAdjacent index (by omega)
      · exact hdistinct index (by omega)
      · exact hanchorFrozen (index+1) hbound
      · simpa only [hinvolution] using inductionHypothesis (by omega)

theorem rail_charge_bound (selected pairs misaligned tiles charge : Int)
    (hselected : selected ≤ pairs) (hmisaligned : 0 ≤ misaligned)
    (htiles : tiles = pairs+misaligned)
    (hcharge : charge = selected+pairs-2*tiles) :
    charge = selected-pairs-2*misaligned ∧ charge ≤ -2*misaligned ∧ charge ≤ 0 := by
  omega

theorem positive_charge_rigidity (charge loss misaligned : Int)
    (hloss : 0 ≤ loss) (hmisaligned : 0 ≤ misaligned)
    (hcharge : charge = 1-loss-2*misaligned) :
    charge ≤ 1 ∧ (0 < charge ↔ charge = 1 ∧ loss = 0 ∧ misaligned = 0) := by
  omega

theorem owned_rail_ledger (deficit donors components loss misaligned otherLoss : Int)
    (hdonors : components ≤ donors) (hloss : 0 ≤ loss)
    (hmisaligned : 0 ≤ misaligned) (hother : 0 ≤ otherLoss)
    (hledger : deficit = donors-components+loss+2*misaligned+otherLoss) :
    0 ≤ deficit ∧ (deficit = 0 ↔ donors = components ∧ loss = 0 ∧
      misaligned = 0 ∧ otherLoss = 0) := by
  omega

end SubQuorum.FrozenRailElbows
