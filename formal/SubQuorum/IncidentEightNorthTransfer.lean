import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.IncidentEightNorthTransfer

abbrev Point := Int × Int

def endpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def support (width near far : Int) (point : Point) : Prop :=
  (point.1 = 0 ∧ (point.2 = 0 ∨ point.2 = width+1)) ∨
  (point.1 = near+1 ∧ point.2 = 1) ∨
  (point.1 = far+1 ∧ point.2 = width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧
    ((point.1 % 2 = 0 ∧ point.2 = 0) ∨ (point.1 % 2 = 1 ∧ point.2 = 2))) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧
    ((point.1 % 2 = 0 ∧ point.2 = width+1) ∨
      (point.1 % 2 = 1 ∧ point.2 = width-1)))

def corner (bottom near : Int) (point : Point) : Prop :=
  endpoint (bottom-2) near 6 (point.2-3,point.1-2)

def returning (bottom : Int) (point : Point) : Prop :=
  endpoint 6 8 4 (11-point.2,bottom+2-point.1)

def parent (bottom width incident other : Int) (point : Point) : Prop :=
  endpoint width incident other (point.1-(bottom-1-incident),point.2-4)

def secondary (bottom width incident other : Int) (point : Point) : Prop :=
  endpoint width incident other (point.1-(bottom-1-incident),point.2-5)

def positive (bottom width incident other : Int) (point : Point) : Prop :=
  endpoint width incident other (incident+7-point.2,point.1-(bottom-6))

def adjacent (point next : Point) : Prop :=
  (next.1 = point.1-1 ∧ next.2 = point.2) ∨
  (next.1 = point.1+1 ∧ next.2 = point.2) ∨
  (next.1 = point.1 ∧ next.2 = point.2-1) ∨
  (next.1 = point.1 ∧ next.2 = point.2+1)

theorem the_secondary_site_is_a_corner_support (bottom near : Int)
    (_hbottom : 14 ≤ bottom) : support (bottom-2) near 6 (3,bottom-3) := by
  unfold support
  omega

theorem both_secondary_forcing_neighbors_exist
    (bottom near width incident other : Int) (_hbottom : 14 ≤ bottom)
    (hincident : 8 ≤ incident) :
    corner bottom near (bottom,6) ∧ parent bottom width incident other (bottom-1,5) := by
  unfold corner parent endpoint
  dsimp
  omega

theorem no_fixed_source_owns_the_secondary_site
    (bottom near width incident other : Int) (hbottom : 14 ≤ bottom)
    (hincident : 8 ≤ incident) (hwidth : 6 ≤ width) :
    ¬corner bottom near (bottom-1,6) ∧ ¬returning bottom (bottom-1,6) ∧
      ¬parent bottom width incident other (bottom-1,6) := by
  unfold corner returning parent endpoint
  dsimp
  omega

theorem a_too_long_secondary_hits_the_parent_bar
    (bottom parentWidth incident parentOther width length other : Int)
    (hincident : 8 ≤ incident) (hwidth : 6 ≤ width)
    (hparent : 6 ≤ parentWidth) (hlength : incident ≤ length) :
    secondary bottom width length other (bottom-incident,6) ∧
      parent bottom parentWidth incident parentOther (bottom-incident,6) := by
  unfold secondary parent endpoint
  dsimp
  omega

theorem a_left_bar_hits_the_parent_leg
    (bottom parentWidth incident parentOther width length other : Int)
    (_hincident : 8 ≤ incident) (hwidth : 6 ≤ width)
    (hlength : 4 ≤ length) (hupper : length ≤ incident-2) :
    endpoint width length other (0,2) ∧
      parent bottom parentWidth incident parentOther (bottom-1-length,5) := by
  unfold parent endpoint
  dsimp
  omega

theorem secondary_length_four_hits_the_return (bottom width other : Int)
    (hwidth : 6 ≤ width) :
    secondary bottom width 4 other (bottom-4,7) ∧ returning bottom (bottom-4,7) := by
  unfold secondary returning endpoint
  dsimp
  omega

theorem secondary_lengths_from_disjointness
    (bottom parentWidth incident parentOther width length other : Int)
    (hincident : 8 ≤ incident) (hparent : 6 ≤ parentWidth)
    (hwidth : 6 ≤ width) (hlength : 4 ≤ length)
    (heven : length % 2 = 0) (hparentEven : incident % 2 = 0)
    (havoidParent : ∀ point, secondary bottom width length other point →
      ¬parent bottom parentWidth incident parentOther point)
    (havoidReturn : ∀ point, secondary bottom width length other point →
      ¬returning bottom point) : 6 ≤ length ∧ length ≤ incident-2 := by
  have hnotFour : length ≠ 4 := by
    intro hequal
    subst length
    have hhit := secondary_length_four_hits_the_return bottom width other hwidth
    exact havoidReturn (bottom-4,7) hhit.1 hhit.2
  have hless : length < incident := by
    by_cases hless : length < incident
    · exact hless
    · have hhit := a_too_long_secondary_hits_the_parent_bar
        bottom parentWidth incident parentOther width length other hincident hwidth hparent (by omega)
      exact False.elim (havoidParent (bottom-incident,6) hhit.1 hhit.2)
  omega

theorem incident_eight_forces_secondary_six (length : Int)
    (hlower : 6 ≤ length) (hupper : length ≤ 8-2) : length = 6 := by omega

theorem secondary_width_six_hits_the_return (bottom other : Int)
    (hother : 4 ≤ other) :
    secondary bottom 6 6 other (bottom-4,11) ∧ returning bottom (bottom-4,11) := by
  unfold secondary returning endpoint
  dsimp
  omega

theorem a_wide_secondary_hits_the_parent_far_leg
    (bottom parentWidth parentOther width other : Int)
    (hparent : 6 ≤ parentWidth) (hother : 4 ≤ parentOther)
    (hwidth : parentWidth ≤ width) :
    secondary bottom width 6 other (bottom-7,parentWidth+4) ∧
      parent bottom parentWidth 8 parentOther (bottom-7,parentWidth+4) := by
  unfold secondary parent endpoint
  dsimp
  omega

theorem the_positive_site_and_three_neighbors
    (bottom width other : Int) (hwidth : 8 ≤ width) :
    support 6 8 4 (4,7) ∧
      secondary bottom width 6 other (bottom-6,7) ∧
      secondary bottom width 6 other (bottom-5,6) ∧
      returning bottom (bottom-4,7) := by
  unfold support secondary returning endpoint
  dsimp
  omega

theorem none_of_the_four_sources_owns_the_positive_site
    (bottom near parentWidth parentIncident parentOther width other : Int)
    (hbottom : 14 ≤ bottom) (hparent : 6 ≤ parentWidth) (hincident : 8 ≤ parentIncident)
    (hwidth : 8 ≤ width) :
    ¬corner bottom near (bottom-5,7) ∧ ¬returning bottom (bottom-5,7) ∧
      ¬parent bottom parentWidth parentIncident parentOther (bottom-5,7) ∧
      ¬secondary bottom width 6 other (bottom-5,7) := by
  unfold corner returning parent secondary endpoint
  dsimp
  omega

theorem two_fixed_neighbors_force_an_original_support
    (point anchor foreign : Point) (isEndpoint : Point → Prop)
    (hforeign : adjacent point foreign) (hoccupied : isEndpoint foreign)
    (hdistinct : foreign ≠ anchor)
    (hretained : ¬isEndpoint point →
      ∀ next, adjacent point next → isEndpoint next → next = anchor) : isEndpoint point := by
  by_cases hpoint : isEndpoint point
  · exact hpoint
  · exact False.elim (hdistinct (hretained hpoint foreign hforeign hoccupied))

theorem a_too_long_east_terminal_hits_the_secondary_far_leg
    (bottom width other positiveWidth incident far : Int)
    (hwidth : 8 ≤ width) (hother : 4 ≤ other) (hpositive : 6 ≤ positiveWidth)
    (hlength : width-2 ≤ incident) :
    positive bottom positiveWidth incident far (bottom-5,width+5) ∧
      secondary bottom width 6 other (bottom-5,width+5) := by
  unfold positive secondary endpoint
  dsimp
  omega

theorem an_east_terminal_four_hits_the_return (bottom width other : Int)
    (hwidth : 6 ≤ width) :
    positive bottom width 4 other (bottom-4,10) ∧ returning bottom (bottom-4,10) := by
  unfold positive returning endpoint
  dsimp
  omega

theorem an_upward_east_bar_hits_the_secondary
    (bottom width other incident positiveWidth : Int)
    (_hwidth : 8 ≤ width) (hlength : 4 ≤ incident) (hupper : incident ≤ width-4)
    (hpositive : 6 ≤ positiveWidth) :
    endpoint positiveWidth incident 4 (0,2) ∧
      secondary bottom width 6 other (bottom-6,incident+7) := by
  unfold secondary endpoint
  dsimp
  omega

theorem positive_incident_bounds_from_disjointness
    (bottom width other positiveWidth incident far : Int)
    (hwidth : 8 ≤ width) (hother : 4 ≤ other) (hpositive : 6 ≤ positiveWidth)
    (hlength : 4 ≤ incident) (heven : incident % 2 = 0) (hwidthEven : width % 2 = 0)
    (havoidSecondary : ∀ point, positive bottom positiveWidth incident far point →
      ¬secondary bottom width 6 other point)
    (havoidReturn : ∀ point, positive bottom positiveWidth incident far point →
      ¬returning bottom point) : 6 ≤ incident ∧ incident ≤ width-4 := by
  have hnotFour : incident ≠ 4 := by
    intro hequal
    subst incident
    have hhit := an_east_terminal_four_hits_the_return bottom positiveWidth far hpositive
    exact havoidReturn (bottom-4,10) hhit.1 hhit.2
  have hless : incident < width-2 := by
    by_cases hless : incident < width-2
    · exact hless
    · have hhit := a_too_long_east_terminal_hits_the_secondary_far_leg
        bottom width other positiveWidth incident far hwidth hother hpositive (by omega)
      exact False.elim (havoidSecondary (bottom-5,width+5) hhit.1 hhit.2)
  omega

theorem width_ten_and_twelve_are_necessary (parentWidth width incident : Int)
    (hincident : 6 ≤ incident) (hupper : incident ≤ width-4)
    (hparent : width ≤ parentWidth-2) : 10 ≤ width ∧ 12 ≤ parentWidth := by omega

def gateB (bottom width other : Int) (point : Point) : Prop :=
  endpoint width bottom other (bottom+3-point.1,point.2-1)

theorem a_thin_E_with_long_far_leg_hits_Q
    (bottom incident far : Int) (hincident : 6 ≤ incident) (hfar : incident-4 ≤ far) :
    positive bottom 6 incident far (bottom,11) ∧ returning bottom (bottom,11) := by
  unfold positive returning endpoint
  dsimp
  omega

theorem a_tall_E_bar_inside_the_actual_gate_hits_B
    (bottom gateWidth gateOther width incident far : Int)
    (_hgate : 12 ≤ gateWidth) (hwidth : 8 ≤ width) (hincident : 6 ≤ incident)
    (hinside : incident+7 ≤ gateWidth+1) :
    positive bottom width incident far (bottom+2,incident+7) ∧
      gateB bottom gateWidth gateOther (bottom+2,incident+7) := by
  unfold positive gateB endpoint
  dsimp
  omega

theorem the_actual_B_fence_width_alternative
    (bottom gateWidth gateOther width incident far : Int)
    (hgate : 12 ≤ gateWidth) (hwidth : 6 ≤ width) (hwidthEven : width % 2 = 0)
    (hincident : 6 ≤ incident) (hincidentEven : incident % 2 = 0)
    (hgateEven : gateWidth % 2 = 0) (hfar : 4 ≤ far) (hfarEven : far % 2 = 0)
    (havoidQ : ∀ point, positive bottom width incident far point → ¬returning bottom point)
    (havoidB : ∀ point, positive bottom width incident far point →
      ¬gateB bottom gateWidth gateOther point) :
    (width = 6 ∧ far ≤ incident-6 ∧ 10 ≤ incident) ∨
      (8 ≤ width ∧ gateWidth-4 ≤ incident) := by
  by_cases hthin : width = 6
  · subst width
    have hshort : far < incident-4 := by
      by_cases hshort : far < incident-4
      · exact hshort
      · have hhit := a_thin_E_with_long_far_leg_hits_Q bottom incident far hincident (by omega)
        exact False.elim (havoidQ (bottom,11) hhit.1 hhit.2)
    exact Or.inl ⟨rfl, by omega, by omega⟩
  · have htall : 8 ≤ width := by omega
    have houtside : gateWidth+1 < incident+7 := by
      by_cases houtside : gateWidth+1 < incident+7
      · exact houtside
      · have hhit := a_tall_E_bar_inside_the_actual_gate_hits_B
          bottom gateWidth gateOther width incident far hgate htall hincident (by omega)
        exact False.elim (havoidB (bottom+2,incident+7) hhit.1 hhit.2)
    exact Or.inr ⟨htall, by omega⟩

theorem actual_incident_eight_width_lower_bounds
    (gateWidth parentWidth width incident : Int) (hgate : 12 ≤ gateWidth)
    (halternative : 10 ≤ incident ∨ gateWidth-4 ≤ incident)
    (hupper : incident ≤ width-4) (hparent : width ≤ parentWidth-2) :
    8 ≤ incident ∧ 12 ≤ width ∧ 14 ≤ parentWidth ∧
      (14 ≤ gateWidth → 10 ≤ incident ∧ 14 ≤ width ∧ 16 ≤ parentWidth) := by omega

theorem both_terminal_supports_are_consumed_by_the_secondary
    (bottom width other positiveWidth incident far : Int)
    (hwidth : 8 ≤ width) (hincident : 6 ≤ incident) (heven : incident % 2 = 0) :
    support positiveWidth incident far (incident+1,1) ∧
      support positiveWidth incident far (incident,0) ∧
      secondary bottom width 6 other (bottom-5,6) ∧
      secondary bottom width 6 other (bottom-6,7) := by
  unfold support secondary endpoint
  dsimp
  omega

theorem the_full_terminal_tile_has_three_secondary_endpoints
    (bottom width other : Int) (hwidth : 8 ≤ width) :
    secondary bottom width 6 other (bottom-6,6) ∧
      secondary bottom width 6 other (bottom-6,7) ∧
      secondary bottom width 6 other (bottom-5,6) := by
  unfold secondary endpoint
  dsimp
  omega

theorem the_original_axial_support_has_two_straight_neighbors
    (width other : Int) (point : Point) (hwidth : 8 ≤ width) :
    (endpoint width 6 other point ∧ adjacent (2,1) point) ↔
      point = (1,1) ∨ point = (3,1) := by
  unfold endpoint adjacent
  simp only [Prod.ext_iff]
  dsimp
  omega

theorem the_original_lateral_support_has_three_neighbors
    (width other : Int) (point : Point) (hwidth : 8 ≤ width) :
    (endpoint width 6 other point ∧ adjacent (1,2) point) ↔
      point = (0,2) ∨ point = (1,1) ∨ point = (1,3) := by
  unfold endpoint adjacent
  simp only [Prod.ext_iff]
  dsimp
  omega

def targetFrame (bottom incident : Int) (point : Point) : Point :=
  (bottom-6+point.2,incident+7-point.1)

def oldS (incident : Int) (point : Point) : Point :=
  (incident+3-point.1,3-point.2)

def oldP (point : Point) : Point := (point.2+2,point.1+2)

def producerS (bottom : Int) (point : Point) : Point :=
  (bottom-3-point.2,point.1+4)

def producerP (bottom incident : Int) (point : Point) : Point :=
  (bottom-8+point.1,incident+9-point.2)

theorem old_S_frame_composition (bottom incident : Int) (point : Point) :
    producerS bottom (oldS incident point) = targetFrame bottom incident point := by
  apply Prod.ext <;> dsimp [producerS, oldS, targetFrame] <;> omega

theorem old_P_frame_composition (bottom incident : Int) (point : Point) :
    producerP bottom incident (oldP point) = targetFrame bottom incident point := by
  apply Prod.ext <;> dsimp [producerP, oldP, targetFrame] <;> omega

theorem old_S_witnesses_have_two_distinct_fixed_owners
    (bottom near parentWidth parentOther : Int) (hbottom : 14 ≤ bottom) :
    corner bottom near (producerS bottom (0,1)) ∧
      parent bottom parentWidth 8 parentOther (producerS bottom (1,1)) := by
  unfold corner parent producerS endpoint
  dsimp
  omega

theorem old_P_witnesses_have_two_distinct_fixed_owners
    (bottom incident parentWidth parentOther width other : Int)
    (hparent : 6 ≤ parentWidth) (hwidth : 8 ≤ width) :
    parent bottom parentWidth 8 parentOther (producerP bottom incident (0,incident+3)) ∧
      secondary bottom width 6 other (producerP bottom incident (1,incident+3)) := by
  unfold parent secondary producerP endpoint
  dsimp
  omega

theorem old_S_witnesses_at_every_parent_incident_length
    (bottom near parentWidth parentIncident parentOther : Int)
    (hbottom : 14 ≤ bottom) (hincident : 8 ≤ parentIncident) :
    corner bottom near (producerS bottom (0,1)) ∧
      parent bottom parentWidth parentIncident parentOther (producerS bottom (1,1)) := by
  unfold corner parent producerS endpoint
  dsimp
  omega

theorem old_P_is_excluded_by_the_same_secondary_owner
    (bottom incident width other : Int) (hwidth : 1 ≤ width) :
    ¬secondary bottom width 6 other (producerP bottom incident (0,incident+3)) ∧
      secondary bottom width 6 other (producerP bottom incident (1,incident+3)) := by
  unfold secondary producerP endpoint
  dsimp
  omega

theorem the_old_P_witnesses_exist_at_arbitrary_old_width
    (width incident near far : Int) (hincident : 6 ≤ incident) (hwidth : incident+4 ≤ width) :
    endpoint width near far (0,incident+3) ∧ endpoint width near far (1,incident+3) := by
  unfold endpoint
  dsimp
  omega

theorem the_physical_secondary_leg_cannot_be_an_old_tight_leg
    (oldLength : Int) (hlength : 8 ≤ oldLength) (hequal : oldLength = 6) : False := by omega

theorem same_source_and_ordered_axial_role_exclude_degree_three
    (degree : Nat) (hnew : degree = 2) (hold : degree = 3) : False := by omega

def ceilHalf (value : Int) : Int := (value+1)/2

theorem same_inventory_integer_bound
    (positiveCount reserve total unmarked upper pairs m8 resolved residual oldTargets added extra caps : Int)
    (hgate : total ≤ 2*(positiveCount-unmarked))
    (hcount : total = oldTargets+caps+resolved+residual)
    (hreserve : oldTargets+added+extra+m8+caps+2*pairs+2*upper ≤ 2*reserve) :
    unmarked+upper+pairs+ceilHalf (m8-resolved-residual+added+extra) ≤
      positiveCount+reserve-total := by
  unfold ceilHalf
  omega

theorem every_two_new_claims_gain_one (baseline added : Int) :
    ceilHalf (baseline+added+2)-ceilHalf baseline =
      ceilHalf (baseline+added)-ceilHalf baseline+1 := by
  unfold ceilHalf
  omega

theorem exact_gain_is_between_the_two_parities (baseline added : Int) :
    added/2 ≤ ceilHalf (baseline+added)-ceilHalf baseline ∧
      ceilHalf (baseline+added)-ceilHalf baseline ≤ (added+1)/2 := by
  unfold ceilHalf
  omega

theorem the_same_coefficient_one_threshold
    (positiveCount reserve total unmarked upper pairs m8 resolved residual oldTargets added extra caps : Int)
    (hgate : total ≤ 2*(positiveCount-unmarked))
    (hcount : total = oldTargets+caps+resolved+residual)
    (hreserve : oldTargets+added+extra+m8+caps+2*pairs+2*upper ≤ 2*reserve)
    (hthreshold : resolved+residual ≤ 2*unmarked+2*upper+2*pairs+m8+extra+added+1) :
    0 ≤ positiveCount+reserve-total := by omega

end SubQuorum.IncidentEightNorthTransfer
