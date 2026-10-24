import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.NearTightVcornerDoubleActivation

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
  uEndpoint width (height-6) far (point.2-3,point.1-2)

def leftTerminal (width leg far column : Int) (point : Point) : Prop :=
  uEndpoint width leg far (leg+3-point.1,column+1-point.2)

def rightTerminal (width leg far column : Int) (point : Point) : Prop :=
  uEndpoint width leg far (leg+3-point.1,point.2-column+1)

def southRotor (mirrored : Bool) (point : Point) : Prop :=
  let column := if mirrored then -point.2 else point.2
  (point.1,column) = (0,0) ∨ (point.1,column) = (1,0) ∨
  (point.1,column) = (1,1) ∨ (point.1,column) = (1,2) ∨
  (point.1,column) = (2,-1) ∨ (point.1,column) = (2,0) ∨
  (point.1,column) = (2,1) ∨ (point.1,column) = (3,1)

theorem the_first_two_forced_points_have_original_support_producers
    (width height far cornerWidth cornerFar : Int) (hheight : 10 ≤ height) :
    uSupport cornerWidth (height-6) cornerFar (height-5,1) ∧
      uSupport width height far (3,2) ∧
      crossEndpoint width height far (2,height-2) ∧
      crossEndpoint width height far (2,height-1) := by
  unfold uSupport crossEndpoint uEndpoint
  dsimp
  omega

theorem neither_fixed_owner_owns_the_first_two_forced_points
    (width height far cornerWidth cornerFar : Int)
    (hheight : 10 ≤ height) (hwidth : 6 ≤ width) (hcorner : 6 ≤ cornerWidth) :
    ¬crossEndpoint width height far (3,height-2) ∧
      ¬crossEndpoint width height far (3,height-1) ∧
      ¬cornerEndpoint cornerWidth height cornerFar (3,height-2) ∧
      ¬cornerEndpoint cornerWidth height cornerFar (3,height-1) := by
  unfold crossEndpoint cornerEndpoint uEndpoint
  dsimp
  omega

theorem every_eastward_u_role_hits_the_transverse_bar
    (width leg far crossWidth height crossFar column : Int)
    (hwidth : 6 ≤ width) (hleg : 4 ≤ leg) (hcross : 6 ≤ crossWidth)
    (hcolumn : height-2 ≤ column) (hcolumnupper : column ≤ height-1) :
    uEndpoint width leg far (column+leg-(height+1),1) ∧
      uEndpoint width leg far (0,height+2-column) ∧
      uEndpoint width leg far (height+1-column,1) ∧
      crossEndpoint crossWidth height crossFar (3,height+1) := by
  unfold crossEndpoint uEndpoint
  dsimp
  omega

theorem the_far_transverse_leg_crosses_both_candidate_stem_columns
    (width height far column : Int)
    (_hwidth : 6 ≤ width) (hfar : 4 ≤ far)
    (hcolumn : height-2 ≤ column) (hcolumnupper : column ≤ height) :
    crossEndpoint width height far (width+1,column) := by
  unfold crossEndpoint uEndpoint
  dsimp
  omega

theorem endpoint_disjointness_bounds_a_leftward_south_terminal
    (width leg far column crossWidth height crossFar halfLeg halfWidth : Int)
    (hwidth : 6 ≤ width) (_hleg : 4 ≤ leg) (hcross : 6 ≤ crossWidth)
    (hfar : 4 ≤ crossFar) (hcolumn : height-2 ≤ column)
    (hcolumnupper : column ≤ height) (hevenleg : leg = 2*halfLeg)
    (hevenwidth : crossWidth = 2*halfWidth)
    (hdisjoint : ∀ point, leftTerminal width leg far column point →
      ¬crossEndpoint crossWidth height crossFar point) : leg ≤ crossWidth-4 := by
  by_cases hbound : leg ≤ crossWidth-4
  · exact hbound
  have hterminal : leftTerminal width leg far column (crossWidth+1,column) := by
    unfold leftTerminal uEndpoint
    dsimp
    omega
  have htransverse := the_far_transverse_leg_crosses_both_candidate_stem_columns
    crossWidth height crossFar column hcross hfar hcolumn hcolumnupper
  exact False.elim (hdisjoint (crossWidth+1,column) hterminal htransverse)

theorem a_rightward_bar_hits_the_transverse_bar
    (width leg far column crossWidth height crossFar : Int)
    (hwidth : 6 ≤ width) (hleg : 4 ≤ leg) (hupper : leg ≤ crossWidth-4)
    (hcolumn : height-2 ≤ column) (hcolumnupper : column ≤ height) :
    rightTerminal width leg far column (leg+2,height+1) ∧
      crossEndpoint crossWidth height crossFar (leg+2,height+1) := by
  unfold rightTerminal crossEndpoint uEndpoint
  dsimp
  omega

theorem adjacent_south_rotor_tips_always_share_an_endpoint
    (firstMirrored secondMirrored : Bool) :
    ∃ point : Point, southRotor firstMirrored point ∧
      southRotor secondMirrored (point.1,point.2-1) := by
  cases firstMirrored with
  | false =>
    cases secondMirrored with
    | false => exact ⟨(1,1), by simp [southRotor]⟩
    | true => exact ⟨(1,0), by simp [southRotor]⟩
  | true =>
    cases secondMirrored with
    | false => exact ⟨(2,1), by simp [southRotor]⟩
    | true => exact ⟨(1,-1), by simp [southRotor]⟩

theorem a_rotor_at_the_first_point_blocks_a_terminal_at_the_second
    (mirrored : Bool) :
    southRotor mirrored (1,1) ∨ southRotor mirrored (2,1) := by
  cases mirrored <;> simp [southRotor]

theorem a_terminal_at_the_first_point_blocks_a_rotor_at_the_second
    (mirrored : Bool) :
    southRotor mirrored (1,-1) ∨ southRotor mirrored (2,-1) := by
  cases mirrored <;> simp [southRotor]

theorem a_south_terminal_stem_contains_both_rotor_blockers
    (width leg far column : Int) (hwidth : 6 ≤ width) (hleg : 4 ≤ leg) :
    leftTerminal width leg far column (4,column) ∧
      leftTerminal width leg far column (5,column) := by
  unfold leftTerminal uEndpoint
  dsimp
  omega

theorem the_middle_terminal_has_an_original_support_at_the_last_point
    (width leg far height halfLeg : Int) (hleg : 4 ≤ leg)
    (heven : leg = 2*halfLeg) :
    uSupport width leg far (leg+3-3,height-height) := by
  unfold uSupport
  dsimp
  omega

theorem the_last_forced_point_has_the_two_transverse_support_owners
    (width height far : Int) (hwidth : 6 ≤ width) (hheight : 10 ≤ height) :
    crossEndpoint width height far (2,height) ∧
      crossEndpoint width height far (3,height+1) ∧
      ¬crossEndpoint width height far (3,height) := by
  unfold crossEndpoint uEndpoint
  dsimp
  omega

theorem adjacent_leftward_terminals_force_strict_leg_growth
    (firstWidth firstLeg firstFar secondWidth secondLeg secondFar column
      halfFirst halfSecond : Int)
    (hfirst : 6 ≤ firstWidth) (hsecond : 6 ≤ secondWidth)
    (hfirstleg : 4 ≤ firstLeg) (hsecondleg : 4 ≤ secondLeg)
    (hevenfirst : firstLeg = 2*halfFirst) (hevensecond : secondLeg = 2*halfSecond)
    (hdisjoint : ∀ point, leftTerminal firstWidth firstLeg firstFar column point →
      ¬leftTerminal secondWidth secondLeg secondFar (column+1) point) :
    firstLeg+2 ≤ secondLeg := by
  by_cases hbound : firstLeg+2 ≤ secondLeg
  · exact hbound
  have hfirstpoint : leftTerminal firstWidth firstLeg firstFar column
      (secondLeg+2,column) := by
    unfold leftTerminal uEndpoint
    dsimp
    omega
  have hsecondpoint : leftTerminal secondWidth secondLeg secondFar (column+1)
      (secondLeg+2,column) := by
    unfold leftTerminal uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (secondLeg+2,column) hfirstpoint hsecondpoint)

theorem a_short_first_bar_with_a_long_far_leg_hits_the_corner
    (width leg far height cornerWidth cornerFar : Int)
    (hwidth : 6 ≤ width) (hleg : 4 ≤ leg) (hfar : leg ≤ far)
    (hshort : width ≤ height-6) :
    leftTerminal width leg far (height-2) (3,height-1-width) ∧
      cornerEndpoint cornerWidth height cornerFar (3,height-1-width) := by
  unfold leftTerminal cornerEndpoint uEndpoint
  dsimp
  omega

theorem a_wide_short_first_leg_hits_the_corner_bar
    (width leg far height cornerWidth cornerFar : Int)
    (_hwidth : 6 ≤ width) (hheight : 10 ≤ height) (hleg : 4 ≤ leg)
    (hwide : height-4 ≤ width) (hshort : leg ≤ cornerWidth) :
    leftTerminal width leg far (height-2) (leg+2,4) ∧
      cornerEndpoint cornerWidth height cornerFar (leg+2,4) := by
  unfold leftTerminal cornerEndpoint uEndpoint
  dsimp
  omega

theorem endpoint_disjointness_forces_the_first_leg_to_be_at_least_six
    (width leg far height cornerWidth cornerFar halfWidth halfHeight halfLeg halfFar : Int)
    (hwidth : 6 ≤ width) (hheight : 10 ≤ height) (hleg : 4 ≤ leg)
    (hfar : 4 ≤ far) (hcorner : 6 ≤ cornerWidth)
    (hevenwidth : width = 2*halfWidth) (hevenheight : height = 2*halfHeight)
    (hevenleg : leg = 2*halfLeg) (hevenfar : far = 2*halfFar)
    (hdisjoint : ∀ point, leftTerminal width leg far (height-2) point →
      ¬cornerEndpoint cornerWidth height cornerFar point) : 6 ≤ leg := by
  by_cases hshort : width ≤ height-6
  · by_cases hfarbelow : far < leg
    · omega
    have hcollision := a_short_first_bar_with_a_long_far_leg_hits_the_corner
      width leg far height cornerWidth cornerFar hwidth hleg (by omega) hshort
    exact False.elim (hdisjoint (3,height-1-width) hcollision.1 hcollision.2)
  · have hwide : height-4 ≤ width := by omega
    by_cases hlegabove : cornerWidth < leg
    · omega
    have hcollision := a_wide_short_first_leg_hits_the_corner_bar
      width leg far height cornerWidth cornerFar hwidth hheight hleg hwide (by omega)
    exact False.elim (hdisjoint (leg+2,4) hcollision.1 hcollision.2)

theorem strict_growth_excludes_all_transverse_widths_below_fourteen
    (firstLeg middleLeg lastLeg crossWidth : Int)
    (hfirst : 6 ≤ firstLeg) (hsecond : firstLeg+2 ≤ middleLeg)
    (hlast : middleLeg+2 ≤ lastLeg) (hupper : lastLeg ≤ crossWidth-4) :
    14 ≤ crossWidth ∧ firstLeg ≤ crossWidth-8 ∧ middleLeg ≤ crossWidth-6 := by
  omega

theorem height_ten_gives_the_stronger_transverse_width_bound
    (cornerWidth firstLeg middleLeg lastLeg crossWidth : Int)
    (hfirst : cornerWidth+2 ≤ firstLeg) (hsecond : firstLeg+2 ≤ middleLeg)
    (hlast : middleLeg+2 ≤ lastLeg) (hupper : lastLeg ≤ crossWidth-4) :
    cornerWidth+10 ≤ crossWidth := by omega

theorem the_first_positive_terminal_has_its_two_original_supports_consumed
    (width leg far height crossWidth crossFar middleWidth middleLeg middleFar
      halfLeg : Int)
    (hleg : 4 ≤ leg) (hheight : 10 ≤ height) (hcross : 6 ≤ crossWidth)
    (hmiddle : 4 ≤ middleLeg) (heven : leg = 2*halfLeg) :
    uSupport width leg far (leg+1,1) ∧ uSupport width leg far (leg,0) ∧
      crossEndpoint crossWidth height crossFar (2,height-2) ∧
      leftTerminal middleWidth middleLeg middleFar (height-1) (3,height-1) := by
  unfold uSupport crossEndpoint leftTerminal uEndpoint
  dsimp
  omega

theorem the_first_pair_target_producer_hits_the_transverse_near_stem
    (oldWidth oldNear oldFar leg crossWidth height crossFar : Int)
    (hleg : 4 ≤ leg) (holdwidth : leg+4 ≤ oldWidth)
    (hcross : 6 ≤ crossWidth) (hheight : 10 ≤ height) :
    uEndpoint oldWidth oldNear oldFar (1,leg+3) ∧
      crossEndpoint crossWidth height crossFar (2,height) ∧
      crossEndpoint crossWidth height crossFar (2,height+2) ∧
      ¬uEndpoint oldWidth oldNear oldFar (-1,leg+3) := by
  unfold crossEndpoint uEndpoint
  dsimp
  omega

theorem both_old_companion_producers_hit_the_original_bar
    (width near far height oldWidth oldNear oldFar : Int)
    (hwidth : height+4 ≤ width) (hheight : 10 ≤ height) (hold : 6 ≤ oldWidth) :
    uEndpoint width near far (0,height) ∧ uEndpoint width near far (1,height) ∧
      uEndpoint oldWidth oldNear oldFar (0,1) ∧
      uEndpoint oldWidth oldNear oldFar (1,1) ∧
      ¬uEndpoint oldWidth oldNear oldFar (height+1-width,1) ∧
      ¬uEndpoint oldWidth oldNear oldFar (0,height+1-width) := by
  unfold uEndpoint
  dsimp
  omega

theorem the_joint_two_target_ledger_counts_each_activation_once
    (positive reserve marked unmarkedOwners activation oldClaims transferred
      capClaims resolved oldResidual lowerPairs upperPairs triples margin : Int)
    (hmargin : margin = positive+reserve-marked)
    (hpartition : marked = oldClaims+transferred+capClaims+resolved+(oldResidual-transferred))
    (hmarks : marked ≤ 2*(positive-unmarkedOwners))
    (hinjection : oldClaims+2*transferred ≤ activation)
    (hreserve : activation+triples+capClaims+2*lowerPairs+2*upperPairs ≤ 2*reserve) :
    2*unmarkedOwners+2*upperPairs+2*lowerPairs+triples-resolved-oldResidual+
      2*transferred ≤ 2*margin := by omega

theorem every_near_tight_claim_improves_the_integer_certificate_by_one
    (margin baseline difference transferred : Int)
    (hbound : 2*baseline+difference+2*transferred ≤ 2*margin) :
    baseline+transferred+(difference+1)/2 ≤ margin := by omega

theorem the_double_improved_threshold_implies_allocation
    (margin baseline oldResidual transferred : Int)
    (hbound : baseline-oldResidual+2*transferred ≤ 2*margin)
    (hthreshold : oldResidual ≤ baseline+1+2*transferred) : 0 ≤ margin := by omega

end SubQuorum.NearTightVcornerDoubleActivation
