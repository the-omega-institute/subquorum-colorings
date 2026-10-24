import SubQuorum.WidthSixBottomOwner

set_option autoImplicit false

namespace SubQuorum.CSecondCornerPhase

open WidthSixBottomOwner

def northOwn (width incident far : Int) (point : Point) : Prop :=
  endpoint width incident far (incident+1-point.1,point.2+3)

def routeCOwn (width incident far : Int) (point : Point) : Prop :=
  endpoint width far incident (incident+1-point.1,point.2+width+1)

def eastOwn (width incident far : Int) (point : Point) : Prop :=
  endpoint width incident far (point.2+incident+2,2-point.1)

def companionOwn (width height far : Int) (point : Point) : Prop :=
  endpoint width height far (point.2+height+1,point.1+1)

theorem north_terminal_must_cross_route_c
    (width incident far otherWidth otherIncident otherFar : Int)
    (hwidth : 6 ≤ width) (hincident : 4 ≤ incident)
    (hotherWidth : 6 ≤ otherWidth) (hotherIncident : 4 ≤ otherIncident) :
    (routeCOwn width incident far (incident,-2) ∧
      northOwn otherWidth otherIncident otherFar (incident,-2)) ∨
    (routeCOwn width incident far (otherIncident+1,-1) ∧
      northOwn otherWidth otherIncident otherFar (otherIncident+1,-1)) := by
  by_cases hlong : incident ≤ otherIncident+1
  · left
    simp [routeCOwn, northOwn, endpoint]
    omega
  · right
    simp [routeCOwn, northOwn, endpoint]
    omega

theorem east_terminal_must_cross_companion
    (width height far otherWidth otherIncident otherFar : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height)
    (hotherWidth : 6 ≤ otherWidth) (hotherIncident : 4 ≤ otherIncident) :
    (companionOwn width height far (1,-height) ∧
      eastOwn otherWidth otherIncident otherFar (1,-height)) ∨
    (companionOwn width height far (0,-otherIncident-2) ∧
      eastOwn otherWidth otherIncident otherFar (0,-otherIncident-2)) := by
  by_cases hlong : height ≤ otherIncident+2
  · left
    simp [companionOwn, eastOwn, endpoint]
    omega
  · right
    simp [companionOwn, eastOwn, endpoint]
    omega

theorem both_phase01_terminal_shapes_are_excluded
    (width incident far companionWidth height companionFar : Int)
    (otherWidth otherIncident otherFar : Int)
    (hwidth : 6 ≤ width) (hincident : 4 ≤ incident)
    (hcompanionWidth : 6 ≤ companionWidth) (hheight : 4 ≤ height)
    (hotherWidth : 6 ≤ otherWidth) (hotherIncident : 4 ≤ otherIncident)
    (northShape : Bool)
    (hnorth : northShape = true → ∀ point,
      routeCOwn width incident far point →
      ¬ northOwn otherWidth otherIncident otherFar point)
    (heast : northShape = false → ∀ point,
      companionOwn companionWidth height companionFar point →
      ¬ eastOwn otherWidth otherIncident otherFar point) : False := by
  cases northShape with
  | false =>
    rcases east_terminal_must_cross_companion companionWidth height companionFar
      otherWidth otherIncident otherFar hcompanionWidth hheight hotherWidth hotherIncident
      with ⟨hfirst,hsecond⟩ | ⟨hfirst,hsecond⟩
    · exact heast rfl _ hfirst hsecond
    · exact heast rfl _ hfirst hsecond
  | true =>
    rcases north_terminal_must_cross_route_c width incident far otherWidth
      otherIncident otherFar hwidth hincident hotherWidth hotherIncident
      with ⟨hfirst,hsecond⟩ | ⟨hfirst,hsecond⟩
    · exact hnorth rfl _ hfirst hsecond
    · exact hnorth rfl _ hfirst hsecond

theorem phase_typed_pools_recover_the_single_pool
    (source01 source10 cap01 cap10 old01 old10 routeC negativeC interiorD
      secondD01 secondD10 unused01 unused10 : Nat)
    (h01 : 2*source01 = cap01+old01+routeC+secondD01+unused01)
    (h10 : 2*source10 = cap10+old10+negativeC+interiorD+secondD10+unused10) :
    2*(source01+source10) = (cap01+cap10)+(old01+old10)+routeC+
      negativeC+interiorD+(secondD01+secondD10)+(unused01+unused10) := by
  omega

theorem phase10_capacity_keeps_all_competing_claims
    (source10 cap10 old10 negativeC interiorD secondD10 unused10 : Nat)
    (h10 : 2*source10 = cap10+old10+negativeC+interiorD+secondD10+unused10) :
    cap10+old10+negativeC+interiorD+secondD10 ≤ 2*source10 := by
  omega

theorem aa_typed_capacity
    (source10 cap10 old10 routeC negativeC interiorD secondD10 unused10 positiveC : Nat)
    (h10 : 2*source10 = cap10+old10+negativeC+interiorD+secondD10+unused10)
    (hsplit : negativeC+positiveC = routeC) (haa : positiveC = 0) :
    cap10+old10+routeC+interiorD+secondD10 ≤ 2*source10 := by
  omega

end SubQuorum.CSecondCornerPhase
