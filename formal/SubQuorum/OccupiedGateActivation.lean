import SubQuorum.WidthEightUCapObstruction

set_option autoImplicit false
set_option maxHeartbeats 20000000

namespace SubQuorum.OccupiedGateActivation

open SubQuorum.WidthEightUCapObstruction

def downLeft (width height other : Int) (point : Point) : Prop :=
  uEndpoint width height other (height+2-point.1,3-point.2)

def downRight (width height other : Int) (point : Point) : Prop :=
  uEndpoint width height other (height+2-point.1,point.2-1)

def rightUp (width height other : Int) (point : Point) : Prop :=
  uEndpoint width height other (height+2-point.2,3-point.1)

def rightDown (width height other : Int) (point : Point) : Prop :=
  uEndpoint width height other (height+2-point.2,point.1-1)

def cornerBarRight (width height other : Int) (point : Point) : Prop :=
  uEndpoint width height other (point.1-2,point.2-1)

def cornerLegRight (width height other : Int) (point : Point) : Prop :=
  uEndpoint width height other (point.2-2,point.1-1)

theorem reference_bar_endpoint (width height other row column : Int)
    (hrow : row = 0 ∨ row = 1) (hlower : 1 ≤ column) (hupper : column ≤ width) :
    uEndpoint width height other (row,column) := Or.inl ⟨hrow,hlower,hupper⟩

theorem reference_left_column_endpoint (width height other row : Int)
    (hwidth : 1 ≤ width) (hlower : 0 ≤ row) (hupper : row ≤ height) :
    uEndpoint width height other (row,1) := by
  by_cases hzero : row = 0
  · exact reference_bar_endpoint width height other row 1 (Or.inl hzero) (by omega) hwidth
  by_cases hone : row = 1
  · exact reference_bar_endpoint width height other row 1 (Or.inr hone) (by omega) hwidth
  exact Or.inr (Or.inl ⟨by omega,hupper,rfl⟩)

theorem down_left_clears_same_leg
    (positiveWidth left right width height other : Int)
    (_hpositive : 6 ≤ positiveWidth) (hwidth : 6 ≤ width) (hheight : 4 ≤ height)
    (hdisjoint : ∀ point, uEndpoint positiveWidth left right point →
      ¬downLeft width height other point) : left ≤ height := by
  by_cases hclear : left ≤ height
  · exact hclear
  · have hown : uEndpoint positiveWidth left right (height+1,1) :=
      Or.inr (Or.inl ⟨by omega,by omega,rfl⟩)
    have hforeign : downLeft width height other (height+1,1) :=
      reference_bar_endpoint width height other _ _ (Or.inr (by omega)) (by omega) (by omega)
    exact False.elim (hdisjoint _ hown hforeign)

theorem down_right_clears_opposite_leg
    (positiveWidth left right width height other : Int)
    (hpositive : 6 ≤ positiveWidth) (_hwidth : 6 ≤ width) (hheight : 4 ≤ height)
    (hreach : positiveWidth ≤ width+1)
    (hdisjoint : ∀ point, uEndpoint positiveWidth left right point →
      ¬downRight width height other point) : right ≤ height := by
  by_cases hclear : right ≤ height
  · exact hclear
  · have hown : uEndpoint positiveWidth left right (height+1,positiveWidth) :=
      Or.inr (Or.inr ⟨by omega,by omega,rfl⟩)
    have hforeign : downRight width height other (height+1,positiveWidth) :=
      reference_bar_endpoint width height other _ _ (Or.inr (by omega)) (by omega) (by omega)
    exact False.elim (hdisjoint _ hown hforeign)

theorem down_left_contains_tip_neighbor
    (width height other positiveHeight : Int)
    (hwidth : 6 ≤ width) (hpositive : 4 ≤ positiveHeight) (hclear : positiveHeight ≤ height) :
    downLeft width height other (positiveHeight+1,2) := by
  simp only [downLeft, uEndpoint]
  omega

theorem down_right_contains_tip_neighbor
    (width height other positiveHeight : Int)
    (hwidth : 6 ≤ width) (hpositive : 4 ≤ positiveHeight) (hclear : positiveHeight ≤ height) :
    downRight width height other (positiveHeight+1,2) := by
  simp only [downRight, uEndpoint]
  omega

theorem positive_beyond_tip_is_original_support
    (width left right : Int) : uSupport width left right (left+1,1) := by
  simp [uSupport]

theorem right_up_always_collides
    (positiveWidth left right width height other : Int)
    (hpositive : 6 ≤ positiveWidth) (hright : 4 ≤ right)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height) :
    ∃ point, uEndpoint positiveWidth left right point ∧ rightUp width height other point := by
  by_cases hbar : height+1 ≤ positiveWidth
  · exact ⟨(1,height+1),
      reference_bar_endpoint positiveWidth left right _ _ (Or.inr rfl) (by omega) hbar,
      reference_bar_endpoint width height other _ _ (Or.inr (by omega)) (by omega) (by omega)⟩
  · exact ⟨(2,positiveWidth), Or.inr (Or.inr ⟨by omega,by omega,rfl⟩),
      reference_left_column_endpoint width height other _ (by omega) (by omega) (by omega)⟩

theorem right_down_collides_when_stem_reaches
    (positiveWidth left right width height other : Int)
    (hpositive : 6 ≤ positiveWidth) (hright : 4 ≤ right)
    (hwidth : 6 ≤ width) (hreach : positiveWidth ≤ height+2) :
    uEndpoint positiveWidth left right (2,positiveWidth) ∧
      rightDown width height other (2,positiveWidth) := by
  exact ⟨Or.inr (Or.inr ⟨by omega,by omega,rfl⟩),
    reference_left_column_endpoint width height other _ (by omega) (by omega) (by omega)⟩

theorem corner_bar_collides_when_bar_reaches
    (positiveWidth left right width height other : Int)
    (hpositive : 6 ≤ positiveWidth) (hright : 4 ≤ right)
    (hreach : positiveWidth ≤ width+1) :
    uEndpoint positiveWidth left right (2,positiveWidth) ∧
      cornerBarRight width height other (2,positiveWidth) := by
  exact ⟨Or.inr (Or.inr ⟨by omega,by omega,rfl⟩),
    reference_bar_endpoint width height other _ _ (Or.inl (by omega)) (by omega) (by omega)⟩

theorem corner_leg_collides_when_leg_reaches
    (positiveWidth left right width height other : Int)
    (hpositive : 6 ≤ positiveWidth) (hright : 4 ≤ right)
    (hreach : positiveWidth ≤ height+2) :
    uEndpoint positiveWidth left right (2,positiveWidth) ∧
      cornerLegRight width height other (2,positiveWidth) := by
  exact ⟨Or.inr (Or.inr ⟨by omega,by omega,rfl⟩),
    Or.inr (Or.inl ⟨by omega,by omega,rfl⟩)⟩

theorem width_six_reach_is_automatic (width height : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height) :
    6 ≤ width+1 ∧ 6 ≤ height+2 := by omega

theorem shorter_leg_activation_height (left right height : Int)
    (hshorter : left ≤ right) (hclear : right ≤ height) : left ≤ height := by omega

theorem width_six_slack
    (slack positive reserve marked unequal activated blank : Int)
    (hledger : positive+reserve-marked ≤ slack)
    (hreserve : activated+blank ≤ 2*reserve)
    (hactivation : marked-unequal ≤ activated+blank) :
    positive-(marked+unequal)/2 ≤ slack := by omega

theorem width_six_joint_allocation
    (positive reserve marked unequal : Int)
    (hmarked : marked ≤ 2*positive) (hunequal : unequal ≤ 1)
    (hactivation : marked-unequal ≤ 2*reserve) :
    0 ≤ positive+reserve-marked := by omega

theorem partially_marked_joint_allocation
    (positive reserve marked unequal : Int)
    (hmarks : marked+unequal ≤ 2*positive+1)
    (hactivation : marked-unequal ≤ 2*reserve) :
    0 ≤ positive+reserve-marked := by omega

end SubQuorum.OccupiedGateActivation
