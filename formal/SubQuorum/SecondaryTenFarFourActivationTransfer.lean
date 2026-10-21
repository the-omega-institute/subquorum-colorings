import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenFarFourActivationTransfer

abbrev Point := Int × Int

def endpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def secondary (bottom width far : Int) (point : Point) : Prop :=
  endpoint width 10 far (point.1-bottom+11,point.2-5)

def eastDown (bottom incident : Int) (point : Point) : Point :=
  (bottom-6+point.2,incident+7-point.1)

def nextDown (bottom incident : Int) (point : Point) : Point :=
  (bottom-7+point.2,incident+7-point.1)

def nextUp (bottom incident : Int) (point : Point) : Point :=
  (bottom-5-point.2,incident+7-point.1)

theorem the_first_lateral_support_and_both_possible_terminal_charts_agree
    (bottom incident following : Int) :
    eastDown bottom incident (incident,0) = (bottom-6,7) ∧
    nextDown bottom following (following,1) = (bottom-6,7) ∧
    nextUp bottom following (following,1) = (bottom-6,7) := by
  unfold eastDown nextDown nextUp
  simp only [Prod.ext_iff]
  omega

theorem the_forced_site_is_absent_from_D_for_every_far_leg
    (bottom width far : Int) (hwidth : 6 ≤ width) :
    ¬secondary bottom width far (bottom-6,7) := by
  unfold secondary endpoint
  dsimp
  omega

theorem all_first_stage_blockers_exist_without_a_far_fence
    (bottom width far : Int) (hwidth : 6 ≤ width) :
    secondary bottom width far (bottom-6,6) ∧
    secondary bottom width far (bottom-10,7) ∧
    secondary bottom width far (bottom-8,6) := by
  unfold secondary endpoint
  dsimp
  omega

theorem far_four_does_not_supply_the_old_row_five_fence
    (width : Int) (hwidth : 6 ≤ width) :
    ¬endpoint width 10 4 (5,width) := by
  unfold endpoint
  dsimp
  omega

theorem both_east_rotor_blockers_are_original_E0_stem_endpoints
    (bottom width incident far : Int) (hincident : 6 ≤ incident) :
    endpoint width incident far (incident-2,1) ∧
    endpoint width incident far (incident-1,1) ∧
    eastDown bottom incident (incident-2,1) = (bottom-5,9) ∧
    eastDown bottom incident (incident-1,1) = (bottom-5,8) := by
  constructor
  · exact Or.inr (Or.inl ⟨by omega, by omega, rfl⟩)
  · constructor
    · exact Or.inr (Or.inl ⟨by omega, by omega, rfl⟩)
    · unfold eastDown
      simp only [Prod.ext_iff]
      omega

def adjacent (point next : Point) : Prop :=
  (next.1 = point.1-1 ∧ next.2 = point.2) ∨
  (next.1 = point.1+1 ∧ next.2 = point.2) ∨
  (next.1 = point.1 ∧ next.2 = point.2-1) ∨
  (next.1 = point.1 ∧ next.2 = point.2+1)

theorem the_first_target_axial_point_is_always_straight_degree_two
    (width far : Int) (point : Point) (hwidth : 6 ≤ width) :
    (endpoint width 10 far point ∧ adjacent (6,1) point) ↔
      point = (5,1) ∨ point = (7,1) := by
  unfold endpoint adjacent
  simp only [Prod.ext_iff]
  dsimp
  omega

theorem the_full_first_target_tile_does_not_need_a_far_leg_bound
    (bottom width far incident following : Int) :
    secondary bottom width far (bottom-6,6) ∧
    secondary bottom width far (bottom-5,6) ∧
    eastDown bottom incident (incident,1) = (bottom-5,7) ∧
    nextDown bottom following (following,1) = (bottom-6,7) ∧
    nextUp bottom following (following,1) = (bottom-6,7) := by
  unfold secondary endpoint eastDown nextDown nextUp
  simp only [Prod.ext_iff]
  omega

def oldS (incident : Int) (point : Point) : Point := (incident+3-point.1,3-point.2)
def oldP (point : Point) : Point := (point.2+2,point.1+2)
def oldEComp (incident : Int) (point : Point) : Point := (point.2+2,incident+3-point.1)
def oldSComp (incident : Int) (point : Point) : Point := (incident+3-point.1,point.2+2)
def frameS (bottom : Int) (point : Point) : Point := (bottom-3-point.2,point.1+4)
def frameP (bottom incident : Int) (point : Point) : Point :=
  (bottom-8+point.1,incident+9-point.2)
def frameEComp (bottom : Int) (point : Point) : Point := (bottom-8+point.1,point.2+4)
def frameSComp (bottom : Int) (point : Point) : Point := (bottom-8+point.2,point.1+4)

theorem all_four_old_recipient_frames_still_compose
    (bottom incident : Int) (point : Point) :
    frameS bottom (oldS incident point) = eastDown bottom incident point ∧
    frameP bottom incident (oldP point) = eastDown bottom incident point ∧
    frameEComp bottom (oldEComp incident point) = eastDown bottom incident point ∧
    frameSComp bottom (oldSComp incident point) = eastDown bottom incident point := by
  unfold frameS frameP frameEComp frameSComp oldS oldP oldEComp oldSComp eastDown
  simp only [Prod.ext_iff]
  omega

theorem old_P_width_supplies_the_new_pair_of_same_bar_witnesses
    (width incident near far : Int) (hincident : 6 ≤ incident)
    (hwidth : incident+4 ≤ width) :
    endpoint width near far (0,incident+3) ∧
    endpoint width near far (0,incident+4) := by
  unfold endpoint
  dsimp
  omega

theorem both_new_P_bar_witnesses_have_the_stated_coordinates
    (bottom incident : Int) :
    frameP bottom incident (0,incident+3) = (bottom-8,6) ∧
    frameP bottom incident (0,incident+4) = (bottom-8,5) := by
  unfold frameP
  simp only [Prod.ext_iff]
  omega

def parentH (bottom width incident far : Int) (point : Point) : Prop :=
  endpoint width incident far (point.1-bottom+1+incident,point.2-4)

theorem new_P_witnesses_are_D_and_H_endpoints_without_E2
    (bottom width far parentWidth parentIncident parentFar : Int)
    (hparent : 12 ≤ parentIncident) :
    secondary bottom width far (bottom-8,6) ∧
    parentH bottom parentWidth parentIncident parentFar (bottom-8,5) := by
  unfold secondary parentH endpoint
  dsimp
  omega

theorem the_actual_D_terminal_is_present_and_absent_from_H
    (bottom width far parentWidth parentIncident parentFar : Int)
    (hparentWidth : 6 ≤ parentWidth) (hparent : 12 ≤ parentIncident) :
    secondary bottom width far (bottom-1,6) ∧
    ¬parentH bottom parentWidth parentIncident parentFar (bottom-1,6) := by
  unfold secondary parentH endpoint
  dsimp
  omega

theorem one_old_producer_cannot_contain_the_two_distinct_owner_witnesses
    (Owner : Type) (owns : Owner → Point → Prop) (first second producer : Owner)
    (firstPoint secondPoint : Point)
    (hunique : ∀ left right point, owns left point → owns right point → left = right)
    (hdifferent : first ≠ second) (hfirst : owns first firstPoint)
    (hsecond : owns second secondPoint) :
    ¬(owns producer firstPoint ∧ owns producer secondPoint) := by
  intro hproducer
  apply hdifferent
  exact (hunique first producer firstPoint hfirst hproducer.1).trans
    (hunique producer second secondPoint hproducer.2 hsecond)

def ceilHalf (value : Int) : Int := (value+1)/2

theorem the_same_inventory_far_four_single_activation_bound
    (positiveCount reserve total unmarked upper pairs m8 resolved residual oldClaims added extra caps : Int)
    (hgate : total ≤ 2*(positiveCount-unmarked))
    (hcount : total = oldClaims+caps+resolved+residual)
    (hreserve : oldClaims+added+extra+m8+caps+2*pairs+2*upper ≤ 2*reserve) :
    unmarked+upper+pairs+ceilHalf (m8-resolved-residual+extra+added) ≤
      positiveCount+reserve-total := by
  unfold ceilHalf
  omega

theorem every_two_far_four_activations_gain_one (baseline added : Int) :
    ceilHalf (baseline+added+2)-ceilHalf (baseline+added) = 1 := by
  unfold ceilHalf
  omega

theorem one_far_four_activation_gains_zero_or_one (baseline : Int) :
    ceilHalf (baseline+1)-ceilHalf baseline = 0 ∨
    ceilHalf (baseline+1)-ceilHalf baseline = 1 := by
  unfold ceilHalf
  omega

theorem the_far_four_coefficient_one_threshold
    (positiveCount reserve total unmarked upper pairs m8 resolved residual oldClaims added extra caps : Int)
    (hgate : total ≤ 2*(positiveCount-unmarked))
    (hcount : total = oldClaims+caps+resolved+residual)
    (hreserve : oldClaims+added+extra+m8+caps+2*pairs+2*upper ≤ 2*reserve)
    (hthreshold : resolved+residual ≤ 2*unmarked+2*upper+2*pairs+m8+extra+added+1) :
    0 ≤ positiveCount+reserve-total := by omega

theorem all_secondary_ten_single_and_double_classes_share_one_certificate
    (positiveCount reserve total unmarked upper pairs m8 resolved residual oldClaims
      singleClaims doubleClaims extra caps : Int)
    (hgate : total ≤ 2*(positiveCount-unmarked))
    (hcount : total = oldClaims+caps+resolved+residual)
    (hreserve : oldClaims+singleClaims+2*doubleClaims+extra+m8+caps+2*pairs+2*upper ≤
      2*reserve) :
    unmarked+upper+pairs+doubleClaims+ceilHalf (m8-resolved-residual+extra+singleClaims) ≤
      positiveCount+reserve-total := by
  unfold ceilHalf
  omega

theorem the_unified_single_and_double_coefficient_one_threshold
    (positiveCount reserve total unmarked upper pairs m8 resolved residual oldClaims
      singleClaims doubleClaims extra caps : Int)
    (hgate : total ≤ 2*(positiveCount-unmarked))
    (hcount : total = oldClaims+caps+resolved+residual)
    (hreserve : oldClaims+singleClaims+2*doubleClaims+extra+m8+caps+2*pairs+2*upper ≤
      2*reserve)
    (hthreshold : resolved+residual ≤
      2*unmarked+2*upper+2*pairs+m8+extra+singleClaims+2*doubleClaims+1) :
    0 ≤ positiveCount+reserve-total := by omega

end SubQuorum.SecondaryTenFarFourActivationTransfer
