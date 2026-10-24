import SubQuorum.OccupiedGateActivation

set_option autoImplicit false
set_option maxHeartbeats 20000000

namespace SubQuorum.SaturatedGateGeometry

open SubQuorum.WidthEightUCapObstruction
open SubQuorum.OccupiedGateActivation

theorem corner_bar_contains_footprint (width height other column : Int)
    (hwidth : 6 ≤ width) (hlower : 2 ≤ column) (hupper : column ≤ 6) :
    cornerBarRight width height other (2,column) := by
  exact reference_bar_endpoint width height other _ _ (Or.inl (by omega))
    (by omega) (by omega)

theorem corner_leg_contains_footprint (width height other column : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height)
    (hlower : 2 ≤ column) (hupper : column ≤ 6) :
    cornerLegRight width height other (2,column) := by
  exact reference_left_column_endpoint width height other _ (by omega) (by omega) (by omega)

theorem horizontal_tip_contains_footprint (width height other column : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height)
    (hlower : 2 ≤ column) (hupper : column ≤ 6) :
    rightDown width height other (2,column) := by
  exact reference_left_column_endpoint width height other _ (by omega) (by omega) (by omega)

theorem distinct_transverse_owners_need_width
    (positiveWidth : Int) (first second : Point → Prop)
    (hwidth : 6 ≤ positiveWidth)
    (hleft : ∀ column, 2 ≤ column → column ≤ 6 → first (2,column))
    (hright : ∀ column, 2 ≤ column → column ≤ 6 → second (2,positiveWidth+1-column))
    (hdisjoint : ∀ point, first point → ¬second point) : 10 < positiveWidth := by
  by_cases hlarge : 10 < positiveWidth
  · exact hlarge
  · have hsecond := hright (positiveWidth-4) (by omega) (by omega)
    have heq : positiveWidth+1-(positiveWidth-4) = 5 := by omega
    rw [heq] at hsecond
    exact False.elim (hdisjoint (2,5) (hleft 5 (by omega) (by omega)) hsecond)

theorem down_right_outside_pair (width height other : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height) :
    downRight width height other (height+2,2) ∧
    downRight width height other (height+2,3) ∧
    ¬downRight width height other (height+3,2) ∧
    ¬downRight width height other (height+3,3) := by
  simp only [downRight, uEndpoint]
  omega

theorem down_right_outside_pair_has_no_support (width height other row column : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height) (_hother : 4 ≤ other)
    (hrow : row = height+2 ∨ row = height+3) (hcolumn : column = 2 ∨ column = 3) :
    ¬uSupport width height other (height+2-row,column-1) := by
  simp only [uSupport]
  omega

theorem saturated_vertical_clearance
    (positiveHeight width height other : Int) (occupied : Point → Prop)
    (hpositive : 4 ≤ positiveHeight) (hwidth : 6 ≤ width) (_hheight : 4 ≤ height)
    (hevenPositive : positiveHeight%2 = 0) (hevenHeight : height%2 = 0)
    (hsource : ∀ point, downRight width height other point → occupied point)
    (hfull : occupied (height+3,2)) (hblank : ¬occupied (positiveHeight+1,2)) :
    height ≤ positiveHeight-4 := by
  have hshort : height < positiveHeight := by
    by_cases hshorter : height < positiveHeight
    · exact hshorter
    · exact False.elim (hblank (hsource _ (down_right_contains_tip_neighbor width height other
        positiveHeight hwidth hpositive (by omega))))
  have hnotAdjacent : height+3 ≠ positiveHeight+1 := by
    intro heq
    rw [heq] at hfull
    exact hblank hfull
  omega

theorem upright_original_beyond_tip (width height other : Int) :
    uSupport width height other ((height+3)-2,2-1) := by
  simp only [uSupport]
  omega

theorem shorter_side_width_descent
    (positiveWidth left right width height other : Int)
    (hpositive : 6 ≤ positiveWidth) (hwidth : 6 ≤ width) (hheight : 4 ≤ height)
    (hshorter : left ≤ right) (hshort : height < left)
    (hdisjoint : ∀ point, uEndpoint positiveWidth left right point →
      ¬downRight width height other point) : width ≤ positiveWidth-2 := by
  by_cases hsmall : width ≤ positiveWidth-2
  · exact hsmall
  · have hclear := down_right_clears_opposite_leg positiveWidth left right width height other
      hpositive hwidth hheight (by omega) hdisjoint
    omega

theorem upright_strict_clearance
    (positiveHeight width height other : Int)
    (hpositive : 4 ≤ positiveHeight) (_hwidth : 6 ≤ width)
    (hevenPositive : positiveHeight%2 = 0) (hevenHeight : height%2 = 0)
    (hnoEndpoint : ¬cornerBarRight width height other (positiveHeight+1,2))
    (hnoSupport : height+3 ≠ positiveHeight+1) : height ≤ positiveHeight-4 := by
  have hshort : height < positiveHeight := by
    by_cases hshorter : height < positiveHeight
    · exact hshorter
    · apply False.elim
      apply hnoEndpoint
      exact Or.inr (Or.inl ⟨by omega,by omega,rfl⟩)
  omega

theorem common_owner_dimensions (positiveWidth left right width height other : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height) (hother : 4 ≤ other)
    (hwidthRelation : positiveWidth = width+2)
    (hleft : height ≤ left-4) (hright : other ≤ right-4) :
    8 ≤ positiveWidth ∧ 8 ≤ left ∧ 8 ≤ right := by omega

theorem single_positive_failure_needs_large_dimension
    (positiveWidth left right : Int)
    (hgeometry : (8 ≤ left ∧ 8 ≤ right) ∨
      (12 ≤ positiveWidth ∨ 8 ≤ left ∨ 8 ≤ right)) :
    12 ≤ positiveWidth ∨ 8 ≤ max left right := by
  simp only [Int.max_def]
  split <;> omega

theorem small_positive_joint_allocation
    (positiveWidth left right reserve marked : Int)
    (hwidth : positiveWidth ≤ 10) (hleft : left ≤ 6) (hright : right ≤ 6)
    (hfailureGeometry : 1+reserve-marked < 0 →
      12 ≤ positiveWidth ∨ 8 ≤ max left right) : 0 ≤ 1+reserve-marked := by
  simp only [Int.max_def] at hfailureGeometry
  split at hfailureGeometry <;> omega

end SubQuorum.SaturatedGateGeometry
