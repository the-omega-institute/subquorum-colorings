import SubQuorum.LongBentTerminalStrips

set_option autoImplicit false

namespace SubQuorum.TransverseCombMouths

open OwnedDonorCompensation LongBentTerminalStrips

def gridAdjacent (first second : Int × Int) : Prop :=
  (first.1 = second.1 ∧ (first.2+1 = second.2 ∨ second.2+1 = first.2)) ∨
  (first.2 = second.2 ∧ (first.1+1 = second.1 ∨ second.1+1 = first.1))

theorem even_arm_frozen (selected : (Int × Int) → Prop)
    (mate : (Int × Int) → (Int × Int)) (column offset : Int) (length : Nat)
    (hoffset : offset = 1 ∨ offset = -1)
    (hbase : FrozenPromotion.Frozen gridAdjacent selected mate (1, column))
    (hsupport : ∀ index : Nat, index < length →
      selected (2*(index : Int)+3, column+offset))
    (hmate : ∀ index : Nat, index < length →
      mate (2*(index : Int)+2, column) = (2*(index : Int)+1, column)) :
    ∀ index : Nat, index ≤ length →
      FrozenPromotion.Frozen gridAdjacent selected mate (2*(index : Int)+1, column) := by
  intro index
  induction index with
  | zero =>
      intro hbound
      simpa using hbase
  | succ index inductionHypothesis =>
      intro hbound
      have hstep : index < length := by omega
      apply FrozenPromotion.Frozen.selected_frozen _
        (2*(index : Int)+3, column+offset) (2*(index : Int)+2, column)
      · simp only [gridAdjacent, Int.natCast_succ]
        omega
      · simp only [gridAdjacent, Int.natCast_succ]
        right
        constructor
        · trivial
        · right
          omega
      · intro hsame
        have hcolumn := congrArg Prod.snd hsame
        omega
      · exact hsupport index hstep
      · rw [hmate index hstep]
        exact inductionHypothesis (by omega)

theorem transverse_square_capacity (state : Int → Int → Label)
    (hupper : state 0 0 = .endpoint) (_hlower : state 1 0 = .endpoint)
    (hfirstNotEndpoint : state 0 1 ≠ .endpoint)
    (hsecondNotEndpoint : state 1 1 ≠ .endpoint)
    (hfirstFeasible : feasibleAt state 0 1)
    (_hsecondFeasible : feasibleAt state 1 1) :
    selectedCount (state 0 1)+selectedCount (state 1 1) ≤ 1 := by
  cases hfirst : state 0 1 <;> cases hsecond : state 1 1 <;>
    simp_all [selectedCount, feasibleAt, degree, occupied] <;> omega

theorem neutral_crossing_removal (physicalTiles crossingTiles emptyTiles selectedEmpty : Nat)
    (hpartition : emptyTiles+crossingTiles = physicalTiles)
    (hweighted : selectedEmpty+2*crossingTiles+2 ≤ 2*physicalTiles) :
    2 ≤ 2*emptyTiles-selectedEmpty := by
  omega

end SubQuorum.TransverseCombMouths
