import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.AllLengthSingletonCompanions

abbrev Point := Int × Int

def uEndpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def terminalEndpoint (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (near+3-point.1,point.2-1)

def crossEndpoint (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (near+2-point.2,point.1-1)

def eastEndpoint (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (near+3-point.2,point.1-2)

def southEndpoint (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (near+3-point.1,point.2-2)

def horizontalEndpoint (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (point.1-3,point.2-2)

def verticalEndpoint (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (point.2-3,point.1-2)

theorem every_east_leg_stops_before_the_transverse_bar
    (width incident other crossWidth height crossFar halfIncident halfHeight : Int)
    (hwidth : 6 ≤ width) (hincident : 4 ≤ incident) (hcross : 6 ≤ crossWidth)
    (hheight : 4 ≤ height) (hieven : incident = 2*halfIncident)
    (hheven : height = 2*halfHeight)
    (hdisjoint : ∀ point, eastEndpoint width incident other point →
      ¬crossEndpoint crossWidth height crossFar point) : incident ≤ height-4 := by
  by_cases hbound : incident ≤ height-4
  · exact hbound
  have heast : eastEndpoint width incident other (3,height+1) := by
    unfold eastEndpoint uEndpoint
    dsimp
    omega
  have hcrosspoint : crossEndpoint crossWidth height crossFar (3,height+1) := by
    unfold crossEndpoint uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (3,height+1) heast hcrosspoint)

theorem the_east_companion_has_a_short_bar_or_a_wide_leg
    (width incident far companionWidth leg other halfIncident halfCompanion halfWidth halfLeg : Int)
    (_hwidth : 6 ≤ width) (hincident : 6 ≤ incident) (hleg : 4 ≤ leg)
    (hieven : incident = 2*halfIncident) (hceven : companionWidth = 2*halfCompanion)
    (hweven : width = 2*halfWidth) (hleven : leg = 2*halfLeg)
    (hdisjoint : ∀ point, eastEndpoint companionWidth leg other point →
      ¬terminalEndpoint width incident far point) :
    companionWidth ≤ incident-2 ∨ width ≤ leg := by
  by_cases hbound : companionWidth ≤ incident-2 ∨ width ≤ leg
  · exact hbound
  have heast : eastEndpoint companionWidth leg other (incident+2,leg+2) := by
    unfold eastEndpoint uEndpoint
    dsimp
    omega
  have hterminal : terminalEndpoint width incident far (incident+2,leg+2) := by
    unfold terminalEndpoint uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (incident+2,leg+2) heast hterminal)

theorem every_south_leg_is_shorter_than_the_singleton_leg
    (width incident far companionWidth leg other halfIncident halfLeg : Int)
    (hwidth : 6 ≤ width) (hincident : 6 ≤ incident) (hcompanion : 6 ≤ companionWidth)
    (hieven : incident = 2*halfIncident) (hleven : leg = 2*halfLeg)
    (hdisjoint : ∀ point, southEndpoint companionWidth leg other point →
      ¬terminalEndpoint width incident far point) : leg ≤ incident-2 := by
  by_cases hbound : leg ≤ incident-2
  · exact hbound
  have hsouth : southEndpoint companionWidth leg other (incident+2,3) := by
    unfold southEndpoint uEndpoint
    dsimp
    omega
  have hterminal : terminalEndpoint width incident far (incident+2,3) := by
    unfold terminalEndpoint uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (incident+2,3) hsouth hterminal)

theorem a_south_bar_stops_before_the_transverse_or_below_it
    (width leg other crossWidth height crossFar halfWidth halfHeight halfLeg halfCross : Int)
    (_hwidth : 6 ≤ width) (hleg : 4 ≤ leg) (_hcross : 6 ≤ crossWidth)
    (hheight : 4 ≤ height) (hweven : width = 2*halfWidth)
    (hheven : height = 2*halfHeight) (hleven : leg = 2*halfLeg)
    (hceven : crossWidth = 2*halfCross)
    (hdisjoint : ∀ point, southEndpoint width leg other point →
      ¬crossEndpoint crossWidth height crossFar point) :
    width ≤ height-2 ∨ crossWidth ≤ leg := by
  by_cases hbound : width ≤ height-2 ∨ crossWidth ≤ leg
  · exact hbound
  have hsouth : southEndpoint width leg other (leg+2,height+1) := by
    unfold southEndpoint uEndpoint
    dsimp
    omega
  have hcrosspoint : crossEndpoint crossWidth height crossFar (leg+2,height+1) := by
    unfold crossEndpoint uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (leg+2,height+1) hsouth hcrosspoint)

theorem a_south_far_leg_cannot_reach_the_transverse_stem
    (width leg other crossWidth height crossFar halfLeg halfOther : Int)
    (hwidth : 6 ≤ width) (hleg : 4 ≤ leg) (hgap : width ≤ height-2)
    (hleven : leg = 2*halfLeg) (hoeven : other = 2*halfOther)
    (hdisjoint : ∀ point, southEndpoint width leg other point →
      ¬crossEndpoint crossWidth height crossFar point) : other ≤ leg := by
  by_cases hbound : other ≤ leg
  · exact hbound
  have hsouth : southEndpoint width leg other (2,width+2) := by
    unfold southEndpoint uEndpoint
    dsimp
    omega
  have hcrosspoint : crossEndpoint crossWidth height crossFar (2,width+2) := by
    unfold crossEndpoint uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (2,width+2) hsouth hcrosspoint)

theorem a_south_length_four_leg_always_has_the_short_bar
    (width other crossWidth height crossFar halfWidth halfHeight halfCross : Int)
    (hwidth : 6 ≤ width) (hcross : 6 ≤ crossWidth) (hheight : 4 ≤ height)
    (hweven : width = 2*halfWidth) (hheven : height = 2*halfHeight)
    (hceven : crossWidth = 2*halfCross)
    (hdisjoint : ∀ point, southEndpoint width 4 other point →
      ¬crossEndpoint crossWidth height crossFar point) : width ≤ height-2 := by
  have halternative := a_south_bar_stops_before_the_transverse_or_below_it
    width 4 other crossWidth height crossFar halfWidth halfHeight 2 halfCross
    hwidth (by omega) hcross hheight hweven hheven (by omega) hceven hdisjoint
  omega

theorem every_horizontal_corner_leg_is_shorter_than_the_singleton_leg
    (width incident far companionWidth leg other halfIncident halfLeg : Int)
    (hwidth : 6 ≤ width) (hincident : 6 ≤ incident)
    (hieven : incident = 2*halfIncident) (hleven : leg = 2*halfLeg)
    (hdisjoint : ∀ point, horizontalEndpoint companionWidth leg other point →
      ¬terminalEndpoint width incident far point) : leg ≤ incident-2 := by
  by_cases hbound : leg ≤ incident-2
  · exact hbound
  have hcorner : horizontalEndpoint companionWidth leg other (incident+2,3) := by
    unfold horizontalEndpoint uEndpoint
    dsimp
    omega
  have hterminal : terminalEndpoint width incident far (incident+2,3) := by
    unfold terminalEndpoint uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (incident+2,3) hcorner hterminal)

theorem every_horizontal_bar_stops_before_the_transverse_bar
    (width leg other crossWidth height crossFar halfWidth halfHeight : Int)
    (_hwidth : 6 ≤ width) (hcross : 6 ≤ crossWidth) (hheight : 4 ≤ height)
    (hweven : width = 2*halfWidth) (hheven : height = 2*halfHeight)
    (hdisjoint : ∀ point, horizontalEndpoint width leg other point →
      ¬crossEndpoint crossWidth height crossFar point) : width ≤ height-2 := by
  by_cases hbound : width ≤ height-2
  · exact hbound
  have hcorner : horizontalEndpoint width leg other (3,height+1) := by
    unfold horizontalEndpoint uEndpoint
    dsimp
    omega
  have hcrosspoint : crossEndpoint crossWidth height crossFar (3,height+1) := by
    unfold crossEndpoint uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (3,height+1) hcorner hcrosspoint)

theorem every_vertical_bar_is_shorter_than_the_singleton_leg
    (width incident far companionWidth leg other halfIncident halfCompanion : Int)
    (hwidth : 6 ≤ width) (hincident : 6 ≤ incident)
    (hieven : incident = 2*halfIncident) (hceven : companionWidth = 2*halfCompanion)
    (hdisjoint : ∀ point, verticalEndpoint companionWidth leg other point →
      ¬terminalEndpoint width incident far point) : companionWidth ≤ incident-2 := by
  by_cases hbound : companionWidth ≤ incident-2
  · exact hbound
  have hcorner : verticalEndpoint companionWidth leg other (incident+2,3) := by
    unfold verticalEndpoint uEndpoint
    dsimp
    omega
  have hterminal : terminalEndpoint width incident far (incident+2,3) := by
    unfold terminalEndpoint uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (incident+2,3) hcorner hterminal)

theorem every_vertical_corner_leg_stops_before_the_transverse_bar
    (width leg other crossWidth height crossFar halfLeg halfHeight : Int)
    (hwidth : 6 ≤ width) (_hleg : 4 ≤ leg) (hcross : 6 ≤ crossWidth)
    (hheight : 4 ≤ height) (hleven : leg = 2*halfLeg) (hheven : height = 2*halfHeight)
    (hdisjoint : ∀ point, verticalEndpoint width leg other point →
      ¬crossEndpoint crossWidth height crossFar point) : leg ≤ height-4 := by
  by_cases hbound : leg ≤ height-4
  · exact hbound
  have hcorner : verticalEndpoint width leg other (3,height+1) := by
    unfold verticalEndpoint uEndpoint
    dsimp
    omega
  have hcrosspoint : crossEndpoint crossWidth height crossFar (3,height+1) := by
    unfold crossEndpoint uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (3,height+1) hcorner hcrosspoint)

theorem the_general_south_pair_predecessor_hits_the_producer_anchor
    (oldWidth oldNear oldFar leg : Int) (hleg : 4 ≤ leg) (hwidth : leg+4 ≤ oldWidth) :
    uEndpoint oldWidth oldNear oldFar (1,leg+2) ∧
      ((leg+5-(leg+2),1) : Point) = (3,1) := by
  constructor
  · unfold uEndpoint
    dsimp
    omega
  · apply Prod.ext <;> dsimp <;> omega

def crossInnerSupport (height : Int) (point : Point) : Prop :=
  ∃ position index : Int, 3 ≤ position ∧ position ≤ height-1 ∧
    position = 2*index+1 ∧ point = (3,height+2-position)

def southFourInterior (width : Int) (point : Point) : Prop :=
  2 < point.1 ∧ point.1 < 6 ∧ 3 < point.2 ∧ point.2 < width+2

theorem the_south_four_forced_point_is_an_original_inner_support
    (width height halfWidth halfHeight : Int)
    (hwidth : 6 ≤ width) (hgap : width ≤ height-2)
    (hweven : width = 2*halfWidth) (hheven : height = 2*halfHeight) :
    crossInnerSupport height (3,width+1) := by
  unfold crossInnerSupport
  refine ⟨height-width+1,halfHeight-halfWidth,?_,?_,?_,?_⟩
  · omega
  · omega
  · omega
  · apply Prod.ext <;> dsimp <;> omega

theorem the_south_four_forced_point_is_strictly_inside
    (width : Int) (hwidth : 6 ≤ width) : southFourInterior width (3,width+1) := by
  unfold southFourInterior
  dsimp
  omega

theorem the_south_four_forced_point_has_two_fixed_endpoint_neighbors
    (width crossWidth height crossFar : Int)
    (hwidth : 6 ≤ width) (hgap : width ≤ height-2) :
    crossEndpoint crossWidth height crossFar (2,width+1) ∧
      southEndpoint width 4 4 (3,width+2) := by
  unfold crossEndpoint southEndpoint uEndpoint
  dsimp
  omega

theorem the_south_four_enclosure_has_an_endpoint_boundary
    (width crossWidth height crossFar : Int) (point : Point)
    (_hwidth : 6 ≤ width) (hgap : width ≤ height-2)
    (hboundary : 2 ≤ point.1 ∧ point.1 ≤ 6 ∧ 3 ≤ point.2 ∧ point.2 ≤ width+2 ∧
      (point.1 = 2 ∨ point.1 = 6 ∨ point.2 = 3 ∨ point.2 = width+2)) :
    crossEndpoint crossWidth height crossFar point ∨ southEndpoint width 4 4 point := by
  unfold crossEndpoint southEndpoint uEndpoint
  dsimp
  omega

theorem the_south_four_enclosure_has_no_boundary_owner_interior_endpoint
    (width crossWidth height crossFar : Int) (point : Point)
    (hcross : 6 ≤ crossWidth) (hgap : width ≤ height-2)
    (hinside : southFourInterior width point) :
    ¬crossEndpoint crossWidth height crossFar point ∧ ¬southEndpoint width 4 4 point := by
  unfold southFourInterior at hinside
  unfold crossEndpoint southEndpoint uEndpoint
  dsimp
  omega

def southInnerSupport (leg : Int) (point : Point) : Prop :=
  ∃ position index : Int, 3 ≤ position ∧ position ≤ leg-1 ∧
    position = 2*index+1 ∧ point = (leg+3-position,4)

def narrowSouthInterior (crossWidth : Int) (point : Point) : Prop :=
  2 < point.1 ∧ point.1 < crossWidth+1 ∧ 3 < point.2 ∧ point.2 < 7

theorem the_narrow_south_forced_point_is_an_original_inner_support
    (crossWidth leg halfCross halfLeg : Int)
    (hcross : 6 ≤ crossWidth) (hleg : crossWidth ≤ leg)
    (hceven : crossWidth = 2*halfCross) (hleven : leg = 2*halfLeg) :
    southInnerSupport leg (crossWidth,4) := by
  unfold southInnerSupport
  refine ⟨leg+3-crossWidth,halfLeg-halfCross+1,?_,?_,?_,?_⟩
  · omega
  · omega
  · omega
  · apply Prod.ext <;> dsimp <;> omega

theorem the_narrow_south_forced_point_is_strictly_inside
    (crossWidth : Int) (hcross : 6 ≤ crossWidth) :
    narrowSouthInterior crossWidth (crossWidth,4) := by
  unfold narrowSouthInterior
  dsimp
  omega

theorem the_narrow_south_forced_point_has_two_fixed_endpoint_neighbors
    (width crossWidth leg other : Int)
    (hcross : 6 ≤ crossWidth) (hleg : crossWidth ≤ leg) :
    crossEndpoint crossWidth 6 4 (crossWidth+1,4) ∧
      southEndpoint width leg other (crossWidth,3) := by
  unfold crossEndpoint southEndpoint uEndpoint
  dsimp
  omega

theorem the_narrow_south_enclosure_has_an_endpoint_boundary
    (width crossWidth leg other : Int) (point : Point)
    (_hcross : 6 ≤ crossWidth) (hleg : crossWidth ≤ leg)
    (hboundary : 2 ≤ point.1 ∧ point.1 ≤ crossWidth+1 ∧ 3 ≤ point.2 ∧ point.2 ≤ 7 ∧
      (point.1 = 2 ∨ point.1 = crossWidth+1 ∨ point.2 = 3 ∨ point.2 = 7)) :
    crossEndpoint crossWidth 6 4 point ∨ southEndpoint width leg other point := by
  unfold crossEndpoint southEndpoint uEndpoint
  dsimp
  omega

theorem the_narrow_south_enclosure_has_no_boundary_owner_interior_endpoint
    (width crossWidth leg other : Int) (point : Point)
    (hwidth : 6 ≤ width) (hleg : crossWidth ≤ leg)
    (hinside : narrowSouthInterior crossWidth point) :
    ¬crossEndpoint crossWidth 6 4 point ∧ ¬southEndpoint width leg other point := by
  unfold narrowSouthInterior at hinside
  unfold crossEndpoint southEndpoint uEndpoint
  dsimp
  omega

theorem retaining_the_resolved_count_preserves_all_unused_lower_capacity
    (positive marked transferred caps resolved residual activation prior upper lower
      reserve unmarked : Int)
    (hmarks : marked ≤ 2*(positive-unmarked))
    (hpartition : marked = transferred+caps+resolved+residual)
    (hinjection : transferred ≤ activation)
    (hfloor : activation+prior+caps+2*upper+2*lower ≤ 2*reserve) :
    unmarked+upper+lower+(prior-resolved-residual+1)/2 ≤ positive+reserve-marked := by
  omega

theorem the_retained_count_threshold_implies_allocation
    (positive marked transferred caps resolved residual activation prior upper lower
      reserve unmarked : Int)
    (hmarks : marked ≤ 2*(positive-unmarked))
    (hpartition : marked = transferred+caps+resolved+residual)
    (hinjection : transferred ≤ activation)
    (hfloor : activation+prior+caps+2*upper+2*lower ≤ 2*reserve)
    (hcoverage : resolved+residual ≤ 2*unmarked+2*upper+2*lower+prior+1) :
    0 ≤ positive+reserve-marked := by
  omega

end SubQuorum.AllLengthSingletonCompanions
