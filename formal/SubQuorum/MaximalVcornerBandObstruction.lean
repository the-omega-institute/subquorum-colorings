import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.MaximalVcornerBandObstruction

abbrev Point := Int × Int

def endpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def negativeEndpoint (width leg far : Int) (point : Point) : Prop :=
  endpoint width leg far (leg+3-point.1,point.2-1)

def cornerEndpoint (leg near far : Int) (point : Point) : Prop :=
  endpoint (leg-2) near far (point.2-3,point.1-2)

def eastUpEndpoint (width incident far leg : Int) (point : Point) : Prop :=
  endpoint width incident far (incident+3-point.2,leg+2-point.1)

def eastDownEndpoint (width incident far leg : Int) (point : Point) : Prop :=
  endpoint width incident far (incident+3-point.2,point.1-leg)

theorem the_outer_support_has_three_fixed_foreign_endpoint_neighbors
    (width leg far near other : Int)
    (hwidth : 6 ≤ width) (hleg : 8 ≤ leg) :
    cornerEndpoint leg near other (leg,3) ∧
      negativeEndpoint width leg far (leg+1,2) ∧
      negativeEndpoint width leg far (leg+2,3) ∧
      ¬cornerEndpoint leg near other (leg+1,3) ∧
      ¬negativeEndpoint width leg far (leg+1,3) := by
  unfold cornerEndpoint negativeEndpoint endpoint
  dsimp
  omega

theorem the_far_stem_blocker_exists_independently_of_the_far_length
    (width leg far : Int)
    (hfar : 4 ≤ far) : negativeEndpoint width leg far (leg+1,width+1) := by
  unfold negativeEndpoint endpoint
  dsimp
  omega

theorem either_long_terminal_stem_hits_the_fixed_far_stem
    (width leg far newWidth incident newFar : Int)
    (hwidth : 6 ≤ width) (hfar : 4 ≤ far)
    (hnew : 6 ≤ newWidth) (hreaches : width-2 ≤ incident) :
    eastUpEndpoint newWidth incident newFar leg (leg+1,width+1) ∧
      eastDownEndpoint newWidth incident newFar leg (leg+1,width+1) ∧
      negativeEndpoint width leg far (leg+1,width+1) := by
  unfold eastUpEndpoint eastDownEndpoint negativeEndpoint endpoint
  dsimp
  omega

theorem an_upward_bar_in_the_only_remaining_range_hits_the_corner
    (width leg near other newWidth incident newFar : Int)
    (hnew : 6 ≤ newWidth)
    (hincident : 4 ≤ incident) (hupper : incident ≤ width-4)
    (hlong : width-4 ≤ other) :
    eastUpEndpoint newWidth incident newFar leg (leg,incident+3) ∧
      cornerEndpoint leg near other (leg,incident+3) := by
  unfold eastUpEndpoint cornerEndpoint endpoint
  dsimp
  omega

theorem a_downward_bar_in_the_only_remaining_range_hits_the_negative_bar
    (width leg far newWidth incident newFar : Int)
    (hnew : 6 ≤ newWidth)
    (hincident : 4 ≤ incident) (hupper : incident ≤ width-4) :
    eastDownEndpoint newWidth incident newFar leg (leg+2,incident+3) ∧
      negativeEndpoint width leg far (leg+2,incident+3) := by
  unfold eastDownEndpoint negativeEndpoint endpoint
  dsimp
  omega

theorem both_rotor_collision_coordinates_are_fixed_endpoints
    (width leg far near other : Int)
    (hwidth : 6 ≤ width) (hleg : 8 ≤ leg) :
    cornerEndpoint leg near other (leg,4) ∧
      negativeEndpoint width leg far (leg+2,4) := by
  unfold cornerEndpoint negativeEndpoint endpoint
  dsimp
  omega

theorem evenness_bounds_the_only_remaining_incident_length
    (width incident halfWidth halfIncident : Int)
    (hwidth : width = 2*halfWidth) (hincident : incident = 2*halfIncident)
    (hshort : ¬width-2 ≤ incident) : incident ≤ width-4 := by
  omega

theorem complete_maximal_occurrences_require_a_short_far_leg_and_wide_return
    (width far halfWidth halfFar : Int)
    (hwidth : width = 2*halfWidth) (hfar : far = 2*halfFar)
    (hminimum : 4 ≤ far) (hnotlong : ¬width-4 ≤ far) :
    far ≤ width-6 ∧ 10 ≤ width := by
  omega

end SubQuorum.MaximalVcornerBandObstruction
