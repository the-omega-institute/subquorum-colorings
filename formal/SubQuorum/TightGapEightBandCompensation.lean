import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.TightGapEightBandCompensation

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

def eastEndpoint (width height far : Int) (point : Point) : Prop :=
  uEndpoint (width-4) 4 far (height-point.2,point.1-2)

def downEndpoint (width leg far crossWidth height : Int) (point : Point) : Prop :=
  uEndpoint width leg far (point.2-height+leg,point.1-crossWidth+2)

def upEndpoint (width leg far crossWidth height : Int) (point : Point) : Prop :=
  uEndpoint width leg far (point.2-height+leg,crossWidth-point.1)

def successorUpEndpoint (width leg far crossWidth height : Int) (point : Point) : Prop :=
  uEndpoint width leg far (point.2-height+leg,crossWidth+1-point.1)

def bandEndpoint (width height far : Int) (point : Point) : Prop :=
  uEndpoint width 4 far (height-point.2,point.1-2)

def southEndpoint (width leg far bandWidth height : Int) (point : Point) : Prop :=
  uEndpoint width leg far (leg+bandWidth+3-point.1,height+1-point.2)

theorem the_tight_band_exit_has_its_original_support_and_two_fixed_neighbors
    (width height far other : Int) (hwidth : 10 ≤ width) (hfar : 4 ≤ far) :
    uSupport (width-4) 4 other (0,width-3) ∧
      eastEndpoint width height other (width-2,height) ∧
      crossEndpoint width height far (width-1,height+1) ∧
      crossEndpoint width height far (width+1,height) := by
  unfold uSupport eastEndpoint crossEndpoint uEndpoint
  dsimp
  omega

theorem neither_band_owner_owns_the_exit
    (width height far other : Int) (hwidth : 10 ≤ width) :
    ¬crossEndpoint width height far (width-1,height) ∧
      ¬eastEndpoint width height other (width-1,height) := by
  unfold crossEndpoint eastEndpoint uEndpoint
  dsimp
  omega

theorem the_axial_support_is_an_original_degree_three_bar_point
    (width height far : Int) (hwidth : 10 ≤ width) :
    crossEndpoint width height far (width-2,height+1) ∧
      crossEndpoint width height far (width,height+1) ∧
      crossEndpoint width height far (width-1,height+2) ∧
      ¬crossEndpoint width height far (width-1,height) := by
  unfold crossEndpoint uEndpoint
  dsimp
  omega

theorem the_old_near_tight_axial_role_is_a_straight_degree_two_point
    (width height far : Int) (hwidth : 6 ≤ width) (hheight : 10 ≤ height) :
    uEndpoint width height far (3,1) ∧ uEndpoint width height far (5,1) ∧
      ¬uEndpoint width height far (4,0) ∧ ¬uEndpoint width height far (4,2) := by
  unfold uEndpoint
  dsimp
  omega

theorem every_downward_terminal_bar_with_a_short_leg_hits_the_far_cross_leg
    (width leg far crossWidth height crossFar : Int)
    (hwidth : 6 ≤ width) (hleg : 4 ≤ leg) (hshort : leg < crossFar) :
    downEndpoint width leg far crossWidth height (crossWidth+1,height-leg+1) ∧
      crossEndpoint crossWidth height crossFar (crossWidth+1,height-leg+1) := by
  unfold downEndpoint crossEndpoint uEndpoint
  dsimp
  omega

theorem endpoint_disjointness_bounds_the_positive_incident_leg
    (width leg far crossWidth height crossFar : Int)
    (hwidth : 6 ≤ width) (hleg : 4 ≤ leg)
    (hdisjoint : ∀ point, downEndpoint width leg far crossWidth height point →
      ¬crossEndpoint crossWidth height crossFar point) : crossFar ≤ leg := by
  by_cases hbound : crossFar ≤ leg
  · exact hbound
  have hcollision := every_downward_terminal_bar_with_a_short_leg_hits_the_far_cross_leg
    width leg far crossWidth height crossFar hwidth hleg (by omega)
  exact False.elim (hdisjoint _ hcollision.1 hcollision.2)

theorem every_upward_terminal_bar_with_a_short_leg_hits_the_east_far_leg
    (width leg far crossWidth height other : Int)
    (hwidth : 6 ≤ width) (hleg : 4 ≤ leg) (hshort : leg ≤ other+1) :
    upEndpoint width leg far crossWidth height (crossWidth-2,height-leg+1) ∧
      eastEndpoint crossWidth height other (crossWidth-2,height-leg+1) := by
  unfold upEndpoint eastEndpoint uEndpoint
  dsimp
  omega

theorem endpoint_disjointness_bounds_the_negative_incident_leg
    (width leg far crossWidth height other : Int)
    (hwidth : 6 ≤ width) (hleg : 4 ≤ leg)
    (hdisjoint : ∀ point, upEndpoint width leg far crossWidth height point →
      ¬eastEndpoint crossWidth height other point) : other+2 ≤ leg := by
  by_cases hbound : other+2 ≤ leg
  · exact hbound
  have hcollision := every_upward_terminal_bar_with_a_short_leg_hits_the_east_far_leg
    width leg far crossWidth height other hwidth hleg (by omega)
  exact False.elim (hdisjoint _ hcollision.1 hcollision.2)

theorem a_terminal_has_the_two_original_supports_used_by_the_certificate
    (width leg far halfLeg : Int) (hleg : 4 ≤ leg) (heven : leg = 2*halfLeg) :
    uSupport width leg far (leg,0) ∧ uSupport width leg far (leg+1,1) := by
  unfold uSupport
  dsimp
  omega

theorem the_negative_terminal_forces_a_successor_between_three_fixed_endpoints
    (width leg far crossWidth height crossFar : Int)
    (hwidth : 6 ≤ width) (hleg : 4 ≤ leg)
    (hcross : 10 ≤ crossWidth) (hfar : 4 ≤ crossFar) :
    upEndpoint width leg far crossWidth height (crossWidth-1,height) ∧
      crossEndpoint crossWidth height crossFar (crossWidth,height+1) ∧
      crossEndpoint crossWidth height crossFar (crossWidth+1,height) ∧
      ¬upEndpoint width leg far crossWidth height (crossWidth,height) ∧
      ¬crossEndpoint crossWidth height crossFar (crossWidth,height) := by
  unfold upEndpoint crossEndpoint uEndpoint
  dsimp
  omega

theorem a_short_upward_successor_bar_hits_the_negative_near_stem
    (width leg far nextWidth nextLeg nextFar crossWidth height : Int)
    (hwidth : 6 ≤ width) (hleg : 4 ≤ leg)
    (hnext : 6 ≤ nextWidth) (hnextleg : 4 ≤ nextLeg) (hshort : nextLeg ≤ leg+1) :
    upEndpoint width leg far crossWidth height (crossWidth-1,height-nextLeg+1) ∧
      successorUpEndpoint nextWidth nextLeg nextFar crossWidth height
        (crossWidth-1,height-nextLeg+1) := by
  unfold upEndpoint successorUpEndpoint uEndpoint
  dsimp
  omega

theorem the_old_singleton_producer_collision_and_self_exclusion
    (width height far : Int) (hwidth : 10 ≤ width) :
    crossEndpoint width height far (width,height+2) ∧
      ¬crossEndpoint width height far (width,height+3) := by
  unfold crossEndpoint uEndpoint
  dsimp
  omega

theorem the_old_pair_producer_endpoint_exists
    (oldWidth near far leg : Int) (hleg : 4 ≤ leg) (hwidth : leg+4 ≤ oldWidth) :
    uEndpoint oldWidth near far (0,leg+3) := by
  unfold uEndpoint
  dsimp
  omega

theorem the_old_pair_producer_collision_and_self_exclusion
    (width height far leg : Int) (hwidth : 10 ≤ width) (hleg : 4 ≤ leg) :
    crossEndpoint width height far (width-4,height+1) ∧
      ¬crossEndpoint width height far (width-4,height-leg-1) := by
  unfold crossEndpoint uEndpoint
  dsimp
  omega

theorem the_old_east_companion_collision_and_self_exclusion
    (width height far : Int) (hwidth : 10 ≤ width) :
    crossEndpoint width height far (width-4,height+2) ∧
      ¬crossEndpoint width height far (width-4,height-3) := by
  unfold crossEndpoint uEndpoint
  dsimp
  omega

theorem the_old_south_companion_collision_and_self_exclusion
    (width height far : Int) (hwidth : 10 ≤ width) :
    crossEndpoint width height far (width-3,height+2) ∧
      ¬crossEndpoint width height far (width-3,height+3) := by
  unfold crossEndpoint uEndpoint
  dsimp
  omega

theorem adjacent_mandatory_supports_must_both_be_consumed
    (endpoint occupied : Point → Prop) (adjacent : Point → Point → Prop)
    (first second firstAnchor secondAnchor : Point)
    (hfirst : occupied first) (hsecond : occupied second)
    (hforward : adjacent first second) (hbackward : adjacent second first)
    (hfirstother : second ≠ firstAnchor) (hsecondother : first ≠ secondAnchor)
    (hfirstunique : ¬endpoint first → ∀ point, adjacent first point →
      occupied point → point = firstAnchor)
    (hsecondunique : ¬endpoint second → ∀ point, adjacent second point →
      occupied point → point = secondAnchor) : endpoint first ∧ endpoint second := by
  constructor
  · by_cases hendpoint : endpoint first
    · exact hendpoint
    · exact False.elim (hfirstother (hfirstunique hendpoint second hforward hsecond))
  · by_cases hendpoint : endpoint second
    · exact hendpoint
    · exact False.elim (hsecondother (hsecondunique hendpoint first hbackward hfirst))

theorem the_enlarged_joint_injection_preserves_the_old_surplus
    (oldClaims newClaims surplus activations : Int)
    (hinjection : oldClaims+surplus+newClaims ≤ activations) :
    (oldClaims+newClaims)+surplus ≤ activations := by omega

theorem the_same_physical_ledger_gives_the_new_doubled_floor
    (positive reserve demand unmarked oldClaims newClaims surplus capClaims pairClaims
      oldRemainder lowerPairs upperPairs receipts activations : Int)
    (hpartition : demand = oldClaims+capClaims+pairClaims+oldRemainder)
    (hmarked : demand ≤ 2*(positive-unmarked))
    (hinjection : oldClaims+newClaims+surplus ≤ activations)
    (hinventory : activations+receipts+capClaims+2*lowerPairs+2*upperPairs ≤ 2*reserve) :
    2*unmarked+2*upperPairs+2*lowerPairs+receipts-pairClaims-oldRemainder+
      newClaims+surplus ≤ 2*(positive+reserve-demand) := by omega

theorem the_improved_threshold_suffices_for_allocation
    (margin unmarked upperPairs lowerPairs receipts pairClaims oldRemainder
      newClaims surplus : Int)
    (hfloor : 2*unmarked+2*upperPairs+2*lowerPairs+receipts-pairClaims-oldRemainder+
      newClaims+surplus ≤ 2*margin)
    (hthreshold : pairClaims+oldRemainder ≤
      2*unmarked+2*upperPairs+2*lowerPairs+receipts+surplus+newClaims+1) : 0 ≤ margin := by
  omega

theorem every_unsaturated_band_has_the_same_support_and_two_fixed_neighbors
    (bandWidth crossWidth height far other : Int)
    (hband : 6 ≤ bandWidth) (hgap : bandWidth+4 ≤ crossWidth) :
    uSupport bandWidth 4 other (0,bandWidth+1) ∧
      bandEndpoint bandWidth height other (bandWidth+2,height) ∧
      crossEndpoint crossWidth height far (bandWidth+3,height+1) ∧
      ¬bandEndpoint bandWidth height other (bandWidth+3,height) ∧
      ¬crossEndpoint crossWidth height far (bandWidth+3,height) := by
  unfold uSupport bandEndpoint crossEndpoint uEndpoint
  dsimp
  omega

theorem every_unsaturated_axial_cross_role_has_three_own_neighbors
    (bandWidth crossWidth height far : Int)
    (hband : 6 ≤ bandWidth) (hgap : bandWidth+4 ≤ crossWidth) :
    crossEndpoint crossWidth height far (bandWidth+2,height+1) ∧
      crossEndpoint crossWidth height far (bandWidth+4,height+1) ∧
      crossEndpoint crossWidth height far (bandWidth+3,height+2) ∧
      ¬crossEndpoint crossWidth height far (bandWidth+3,height) := by
  unfold crossEndpoint uEndpoint
  dsimp
  omega

theorem every_band_outer_corner_has_two_perpendicular_own_neighbors
    (bandWidth height other : Int) (hband : 6 ≤ bandWidth) :
    bandEndpoint bandWidth height other (bandWidth+1,height) ∧
      bandEndpoint bandWidth height other (bandWidth+2,height-1) ∧
      ¬bandEndpoint bandWidth height other (bandWidth+3,height) ∧
      ¬bandEndpoint bandWidth height other (bandWidth+2,height+1) := by
  unfold bandEndpoint uEndpoint
  dsimp
  omega

theorem all_eight_general_old_target_collisions_lie_on_the_cross_bar
    (bandWidth crossWidth height far row : Int)
    (hband : 6 ≤ bandWidth) (hgap : bandWidth+4 ≤ crossWidth)
    (hlower : bandWidth ≤ row) (hupper : row ≤ bandWidth+4) :
    crossEndpoint crossWidth height far (row,height+1) ∧
      crossEndpoint crossWidth height far (row,height+2) ∧
      ¬crossEndpoint crossWidth height far (row,height+3) := by
  unfold crossEndpoint uEndpoint
  dsimp
  omega

theorem the_other_general_self_exclusion_points_are_outside_the_cross
    (bandWidth crossWidth height far row column : Int)
    (hband : 6 ≤ bandWidth) (hgap : bandWidth+4 ≤ crossWidth)
    (hlower : bandWidth ≤ row) (hupper : row ≤ bandWidth+4)
    (hcolumn : column ≤ height) :
    ¬crossEndpoint crossWidth height far (row,column) := by
  unfold crossEndpoint uEndpoint
  dsimp
  omega

theorem a_south_terminal_stem_reaching_the_cross_far_leg_collides
    (width leg far bandWidth crossWidth height crossFar : Int)
    (hwidth : 6 ≤ width) (_hleg : 4 ≤ leg)
    (hgap : bandWidth+4 ≤ crossWidth) (hfar : 4 ≤ crossFar)
    (hreaches : crossWidth-bandWidth-2 ≤ leg) :
    southEndpoint width leg far bandWidth height (crossWidth+1,height) ∧
      crossEndpoint crossWidth height crossFar (crossWidth+1,height) := by
  unfold southEndpoint crossEndpoint uEndpoint
  dsimp
  omega

theorem endpoint_disjointness_bounds_a_south_terminal_at_any_band_width
    (width leg far bandWidth crossWidth height crossFar halfLeg halfCross halfBand : Int)
    (hwidth : 6 ≤ width) (hleg : 4 ≤ leg)
    (hgap : bandWidth+4 ≤ crossWidth) (hfar : 4 ≤ crossFar)
    (hevenleg : leg = 2*halfLeg) (hevencross : crossWidth = 2*halfCross)
    (hevenband : bandWidth = 2*halfBand)
    (hdisjoint : ∀ point, southEndpoint width leg far bandWidth height point →
      ¬crossEndpoint crossWidth height crossFar point) :
    leg ≤ crossWidth-bandWidth-4 ∧ 8 ≤ crossWidth-bandWidth := by
  by_cases hreaches : crossWidth-bandWidth-2 ≤ leg
  · have hcollision := a_south_terminal_stem_reaching_the_cross_far_leg_collides
      width leg far bandWidth crossWidth height crossFar hwidth hleg hgap hfar hreaches
    exact False.elim (hdisjoint _ hcollision.1 hcollision.2)
  · omega

theorem a_rightward_bar_in_the_south_terminal_range_hits_the_cross_bar
    (width leg far bandWidth crossWidth height crossFar : Int)
    (hwidth : 6 ≤ width) (hleg : 4 ≤ leg) (hband : 6 ≤ bandWidth)
    (hupper : leg ≤ crossWidth-bandWidth-4) :
    uEndpoint width leg far (1,2) ∧
      crossEndpoint crossWidth height crossFar (bandWidth+leg+2,height+1) := by
  unfold crossEndpoint uEndpoint
  dsimp
  omega

end SubQuorum.TightGapEightBandCompensation
