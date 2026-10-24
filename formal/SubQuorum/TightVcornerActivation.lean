import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.TightVcornerActivation

abbrev Point := Int × Int

def uEndpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def uSupport (width near far : Int) (point : Point) : Prop :=
  (point.1 = 0 ∧ (point.2 = 0 ∨ point.2 = width+1)) ∨
  (point.1 = near+1 ∧ point.2 = 1) ∨
  (point.1 = far+1 ∧ point.2 = width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧
    ((point.1 % 2 = 0 ∧ point.2 = 0) ∨ (point.1 % 2 = 1 ∧ point.2 = 2))) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧
    ((point.1 % 2 = 0 ∧ point.2 = width+1) ∨
      (point.1 % 2 = 1 ∧ point.2 = width-1)))

def crossEndpoint (width height far : Int) (point : Point) : Prop :=
  uEndpoint width height far (height+2-point.2,point.1-1)

def cornerEndpoint (width height far : Int) (point : Point) : Prop :=
  uEndpoint width (height-4) far (point.2-3,point.1-2)

def companionEndpoint (width leg far height : Int) (point : Point) : Prop :=
  uEndpoint width leg far (leg+3-point.1,height+1-point.2)

def rightCompanionEndpoint (width leg far height : Int) (point : Point) : Prop :=
  uEndpoint width leg far (leg+3-point.1,point.2-height+1)

def rotorEndpoint (point : Point) : Prop :=
  point = (1,2) ∨ point = (2,2) ∨ point = (2,3) ∨ point = (2,4) ∨
  point = (3,1) ∨ point = (3,2) ∨ point = (3,3) ∨ point = (4,3)

theorem the_tight_target_is_an_original_corner_endcap
    (width height far : Int) : uSupport width (height-4) far (height-3,1) := by
  unfold uSupport
  dsimp
  omega

theorem the_tight_endcap_has_three_distinct_fixed_endpoint_neighbors
    (width height far cornerWidth cornerFar : Int)
    (hwidth : 6 ≤ width) (hheight : 8 ≤ height)
    (hcorner : 6 ≤ cornerWidth) :
    crossEndpoint width height far (2,height) ∧
      crossEndpoint width height far (3,height+1) ∧
      cornerEndpoint cornerWidth height cornerFar (3,height-1) ∧
      ¬crossEndpoint width height far (3,height) ∧
      ¬cornerEndpoint cornerWidth height cornerFar (3,height) := by
  unfold crossEndpoint cornerEndpoint uEndpoint
  dsimp
  omega

theorem the_first_south_rotor_hits_the_transverse_bar
    (width height far : Int) (hwidth : 6 ≤ width) :
    rotorEndpoint (4-2,(height+1)-height+2) ∧
      crossEndpoint width height far (4,height+1) := by
  constructor
  · have hcoordinates : (4-2,(height+1)-height+2) = ((2 : Int),(3 : Int)) := by
      apply Prod.ext <;> dsimp <;> omega
    rw [hcoordinates]
    simp [rotorEndpoint]
  · unfold crossEndpoint uEndpoint
    dsimp
    omega

theorem the_second_south_rotor_hits_the_transverse_bar
    (width height far : Int) (hwidth : 6 ≤ width) :
    rotorEndpoint (5-2,height+2-(height+1)) ∧
      crossEndpoint width height far (5,height+1) := by
  constructor
  · have hcoordinates : (5-2,height+2-(height+1)) = ((3 : Int),(1 : Int)) := by
      apply Prod.ext <;> dsimp <;> omega
    rw [hcoordinates]
    simp [rotorEndpoint]
  · unfold crossEndpoint uEndpoint
    dsimp
    omega

theorem the_new_incident_leg_stops_before_the_transverse_far_leg
    (width leg far crossWidth height crossFar halfLeg halfCross : Int)
    (hwidth : 6 ≤ width) (hleg : 4 ≤ leg) (hcross : 6 ≤ crossWidth)
    (hcrossfar : 4 ≤ crossFar) (hlegen : leg = 2*halfLeg)
    (hcrosseven : crossWidth = 2*halfCross)
    (hdisjoint : ∀ point, companionEndpoint width leg far height point →
      ¬crossEndpoint crossWidth height crossFar point) : leg ≤ crossWidth-4 := by
  by_cases hbound : leg ≤ crossWidth-4
  · exact hbound
  have hcompanion : companionEndpoint width leg far height (crossWidth+1,height) := by
    unfold companionEndpoint uEndpoint
    dsimp
    omega
  have htransverse : crossEndpoint crossWidth height crossFar (crossWidth+1,height) := by
    unfold crossEndpoint uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (crossWidth+1,height) hcompanion htransverse)

theorem a_rightward_bar_hits_the_transverse_bar
    (width leg far crossWidth height crossFar : Int)
    (hwidth : 6 ≤ width) (hleg : 4 ≤ leg) (hupper : leg ≤ crossWidth-4) :
    rightCompanionEndpoint width leg far height (leg+2,height+1) ∧
      crossEndpoint crossWidth height crossFar (leg+2,height+1) := by
  unfold rightCompanionEndpoint crossEndpoint uEndpoint
  dsimp
  omega

theorem a_short_bar_with_a_long_far_leg_hits_the_vertical_corner
    (width leg far height cornerWidth cornerFar : Int)
    (hwidth : 6 ≤ width) (hleg : 4 ≤ leg) (hfar : leg ≤ far)
    (hshort : width ≤ height-4) :
    companionEndpoint width leg far height (3,height+1-width) ∧
      cornerEndpoint cornerWidth height cornerFar (3,height+1-width) := by
  unfold companionEndpoint cornerEndpoint uEndpoint
  dsimp
  omega

theorem a_short_bar_forces_a_strictly_shorter_far_leg
    (width leg far height cornerWidth cornerFar halfLeg halfFar : Int)
    (hwidth : 6 ≤ width) (hleg : 4 ≤ leg) (hshort : width ≤ height-4)
    (hlegeven : leg = 2*halfLeg) (hfareven : far = 2*halfFar)
    (hdisjoint : ∀ point, companionEndpoint width leg far height point →
      ¬cornerEndpoint cornerWidth height cornerFar point) : far ≤ leg-2 := by
  by_cases hbound : far ≤ leg-2
  · exact hbound
  have hfar : leg ≤ far := by omega
  have hcollision := a_short_bar_with_a_long_far_leg_hits_the_vertical_corner
    width leg far height cornerWidth cornerFar hwidth hleg hfar hshort
  exact False.elim (hdisjoint (3,height+1-width) hcollision.1 hcollision.2)

theorem a_wide_bar_with_a_short_leg_hits_the_vertical_bar
    (width leg far height cornerWidth cornerFar : Int)
    (hheight : 8 ≤ height) (hleg : 4 ≤ leg)
    (hwide : height-2 ≤ width) (hshort : leg ≤ cornerWidth) :
    companionEndpoint width leg far height (leg+2,4) ∧
      cornerEndpoint cornerWidth height cornerFar (leg+2,4) := by
  unfold companionEndpoint cornerEndpoint uEndpoint
  dsimp
  omega

theorem a_wide_bar_forces_a_leg_below_the_vertical_bar
    (width leg far height cornerWidth cornerFar halfLeg halfCorner : Int)
    (hheight : 8 ≤ height) (hleg : 4 ≤ leg) (hwide : height-2 ≤ width)
    (hlegeven : leg = 2*halfLeg) (hcornereven : cornerWidth = 2*halfCorner)
    (hdisjoint : ∀ point, companionEndpoint width leg far height point →
      ¬cornerEndpoint cornerWidth height cornerFar point) : cornerWidth+2 ≤ leg := by
  by_cases hbound : cornerWidth+2 ≤ leg
  · exact hbound
  have hshort : leg ≤ cornerWidth := by omega
  have hcollision := a_wide_bar_with_a_short_leg_hits_the_vertical_bar
    width leg far height cornerWidth cornerFar hheight hleg hwide hshort
  exact False.elim (hdisjoint (leg+2,4) hcollision.1 hcollision.2)

theorem the_two_width_branches_force_incident_length_at_least_six
    (width leg far height cornerWidth halfWidth halfHeight : Int)
    (_hwidth : 6 ≤ width) (hfar : 4 ≤ far) (hcorner : 6 ≤ cornerWidth)
    (hweven : width = 2*halfWidth) (hheven : height = 2*halfHeight)
    (hshort : width ≤ height-4 → far ≤ leg-2)
    (hwide : height-2 ≤ width → cornerWidth+2 ≤ leg) : 6 ≤ leg := by
  by_cases hbranch : width ≤ height-4
  · have hbound := hshort hbranch
    omega
  · have hbound := hwide (by omega)
    omega

theorem the_forced_leg_excludes_transverse_width_six_and_eight
    (leg crossWidth : Int) (hlower : 6 ≤ leg) (hupper : leg ≤ crossWidth-4) :
    10 ≤ crossWidth := by omega

theorem height_eight_forces_the_stronger_transverse_width_bound
    (width leg cornerWidth crossWidth : Int) (hwidth : 6 ≤ width)
    (hwide : 6 ≤ width → cornerWidth+2 ≤ leg)
    (hupper : leg ≤ crossWidth-4) : cornerWidth+6 ≤ crossWidth := by
  have hbound := hwide hwidth
  omega

theorem the_terminal_support_coordinates_have_the_same_transverse_owner
    (width height far : Int) (hwidth : 6 ≤ width) (hheight : 8 ≤ height) :
    crossEndpoint width height far (2,height) ∧
      crossEndpoint width height far (3,height+1) ∧
      crossEndpoint width height far (2,height+1) := by
  unfold crossEndpoint uEndpoint
  dsimp
  omega

theorem the_new_positive_terminal_has_two_consumed_original_supports
    (width leg far height crossWidth crossFar halfLeg : Int)
    (hleg : 4 ≤ leg) (hlegeven : leg = 2*halfLeg)
    (hcross : 6 ≤ crossWidth) (hheight : 8 ≤ height) :
    uSupport width leg far (leg+3-2,height+1-height) ∧
      uSupport width leg far (leg+3-3,height+1-(height+1)) ∧
      crossEndpoint crossWidth height crossFar (2,height) ∧
      crossEndpoint crossWidth height crossFar (3,height+1) := by
  unfold uSupport crossEndpoint uEndpoint
  dsimp
  omega

theorem the_old_singleton_producer_hits_the_original_top_bar
    (width near far height oldWidth oldNear oldFar : Int)
    (hheight : 8 ≤ height) (hheightupper : height ≤ width-4)
    (holdwidth : 6 ≤ oldWidth) :
    uEndpoint width near far (0,height-1) ∧
      uEndpoint oldWidth oldNear oldFar (0,(height-1)-height+2) ∧
      ¬uEndpoint oldWidth oldNear oldFar (0,1-height+2) ∧
      uEndpoint width near far (0,1) := by
  unfold uEndpoint
  dsimp
  omega

theorem the_old_pair_producer_hits_the_transverse_top_bar
    (oldWidth oldNear oldFar leg crossWidth height crossFar : Int)
    (hleg : 4 ≤ leg) (holdwidth : leg+4 ≤ oldWidth) (hcross : 6 ≤ crossWidth) :
    uEndpoint oldWidth oldNear oldFar
      (height+3-(height+2),leg+5-3) ∧
      crossEndpoint crossWidth height crossFar (3,height+2) ∧
      uEndpoint oldWidth oldNear oldFar (0,1) ∧
      ¬crossEndpoint crossWidth height crossFar (leg+4,height+3) := by
  unfold crossEndpoint uEndpoint
  dsimp
  omega

theorem transferring_kappa_improves_the_unrounded_margin_bound
    (margin baseline oldResidual transferred : Int)
    (hmargin : baseline-(oldResidual-transferred) ≤ 2*margin) :
    baseline-oldResidual+transferred ≤ 2*margin := by omega

theorem the_joint_activation_ledger_preserves_count_once
    (positive reserve marked unmarkedOwners activation oldClaims terminalClaims
      transferred capClaims resolved residual lowerPairs upperPairs triples margin : Int)
    (hmargin : margin = positive+reserve-marked)
    (hpartition : marked = oldClaims+terminalClaims+transferred+capClaims+resolved+residual)
    (hmarks : marked ≤ 2*(positive-unmarkedOwners))
    (hinjection : oldClaims+terminalClaims+transferred ≤ activation)
    (hreserve : activation+triples+capClaims+2*lowerPairs+2*upperPairs ≤ 2*reserve) :
    2*unmarkedOwners+2*upperPairs+2*lowerPairs+triples-resolved-residual ≤ 2*margin := by
  omega

theorem the_enlarged_residual_threshold_implies_allocation
    (margin baseline oldResidual transferred : Int)
    (hmargin : baseline-oldResidual+transferred ≤ 2*margin)
    (hthreshold : oldResidual ≤ baseline+1+transferred) : 0 ≤ margin := by omega

end SubQuorum.TightVcornerActivation
