import SubQuorum.WidthSixBottomOwner

set_option autoImplicit false

namespace SubQuorum.AABSecondCorner

open WidthSixBottomOwner

def positiveBandSecondStencil : List Point :=
  [(-1,-2),(-1,-1),(-1,0),(-1,1),(0,1),(0,2),(0,3)]

theorem unrestricted_positive_band_stencil_leaves_two_rotor_roles :
    (rotorOwners positiveBandSecondStencil).length = 2 := by decide

theorem incoming_endpoint_excludes_both_remaining_rotor_roles :
    rotorOwners ((1,0)::positiveBandSecondStencil) = [] := by decide

theorem positive_terminal_frame_transports_incoming_endpoint
    (transpose flipRow flipColumn : Bool)
    (hnorth : pull transpose flipRow flipColumn (0,0) (-1,0) = (0,1))
    (hwest : pull transpose flipRow flipColumn (0,0) (0,-1) = (1,0)) :
    pull transpose flipRow flipColumn (0,0) (1,0) = (0,-1) ∧
    pull transpose flipRow flipColumn (0,0) (0,1) = (-1,0) := by
  cases transpose <;> cases flipRow <;> cases flipColumn <;>
    simp [pull] at hnorth hwest ⊢

def lowerIncomingOwn (width height far : Int) (point : Point) : Prop :=
  endpoint width height far (height+2-point.1,point.2-4)

def upperIncomingOwn (width height far firstShort secondShort : Int)
    (point : Point) : Prop :=
  endpoint width height far (point.1-(firstShort+secondShort-height-1),point.2-4)

theorem equal_incoming_height_collides_with_companion_pair
    (width height far shortHeight : Int) (hwidth : 6 ≤ width)
    (hequal : height = shortHeight) :
    lowerIncomingOwn width height far (shortHeight+1,7) ∧
    ¬ lowerIncomingOwn width height far (shortHeight,7) := by
  simp [lowerIncomingOwn, endpoint, hequal]
  omega

theorem strict_incoming_height_supplies_foreign_west_point
    (width height far shortHeight : Int)
    (hwidth : 6 ≤ width) (hshort : 4 ≤ shortHeight)
    (hstrict : shortHeight+2 ≤ height) :
    lowerIncomingOwn width height far (shortHeight+1,5) ∧
    ¬ lowerIncomingOwn width height far (shortHeight+1,6) := by
  simp [lowerIncomingOwn, endpoint]
  omega

set_option maxHeartbeats 1000000 in
theorem three_foreign_neighbors_force_original_terminal
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hroot : endpoint width left right anchor)
    (hnorth : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (-1,0)))
    (heast : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,1)))
    (hwest : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,-1))) :
    anchor = (left,1) ∨ anchor = (right,width) := by
  rcases anchor with ⟨row,column⟩
  rcases hroot with hbar | hnear | hfar
  all_goals
    cases transpose <;> cases flipRow <;> cases flipColumn <;>
      simp [pull, endpoint, Prod.mk.injEq] at hnorth heast hwest ⊢ <;> omega

theorem opposite_incoming_owners_share_point_and_have_distinguishing_endpoint
    (lowerWidth lowerHeight lowerFar upperWidth upperHeight upperFar
      firstShort secondShort : Int)
    (hlowerWidth : 6 ≤ lowerWidth) (hupperWidth : 6 ≤ upperWidth)
    (hfirst : 4 ≤ firstShort) (hsecond : 4 ≤ secondShort)
    (hlowerHeight : firstShort+2 ≤ lowerHeight)
    (hupperHeight : secondShort ≤ upperHeight) :
    lowerIncomingOwn lowerWidth lowerHeight lowerFar (firstShort+1,5) ∧
    upperIncomingOwn upperWidth upperHeight upperFar firstShort secondShort (firstShort+1,5) ∧
    upperIncomingOwn upperWidth upperHeight upperFar firstShort secondShort
      (firstShort+secondShort-upperHeight-1,6) ∧
    ¬ lowerIncomingOwn lowerWidth lowerHeight lowerFar
      (firstShort+secondShort-upperHeight-1,6) := by
  simp [lowerIncomingOwn, upperIncomingOwn, endpoint]
  omega

theorem aa_negative_only_all_route_exact_census
    (phase01 phase10 phase11 negativeCap oldReservations cornerEvents
      negativeBand positiveBand unused routeA routeB routeD capB capD
      unselected allRoutes : Int)
    (hcap : negativeCap = 2*phase11)
    (hpool : negativeCap+oldReservations+2*cornerEvents+2*negativeBand+
      positiveBand+unused = 2*(phase01+phase10))
    (hselected : 2*phase11 = routeA+capB+capD+unselected)
    (hb : routeB = capB+positiveBand) (hd : routeD = capD+negativeBand)
    (hall : allRoutes = routeA+routeB+cornerEvents+routeD) :
    2*(phase01+phase10) = allRoutes+cornerEvents+negativeBand+
      oldReservations+unselected+unused := by omega

theorem remaining_negative_terminal_must_cross_companion
    (companionWidth height companionFar width incident far shortHeight : Int)
    (hcompanionWidth : 6 ≤ companionWidth) (hwidth : 6 ≤ width)
    (hincident : 4 ≤ incident) (hshort : 4 ≤ shortHeight)
    (hinterior : shortHeight+4 ≤ height)
    (hdisjoint : ∀ point : Point,
      endpoint companionWidth height companionFar (height-point.1,8-point.2) →
      ¬ endpoint width incident far (shortHeight+incident+1-point.1,point.2-5)) : False := by
  by_cases hreach : height-1 ≤ shortHeight+incident+1
  · have hcompanion : endpoint companionWidth height companionFar
        (height-(height-1),8-6) := by
      simp [endpoint]
      omega
    have hforbidden := hdisjoint (height-1,6) hcompanion
    simp [endpoint] at hforbidden
    omega
  · have hcompanion : endpoint companionWidth height companionFar
        (height-(shortHeight+incident+1),8-7) := by
      simp [endpoint]
      omega
    have hforbidden := hdisjoint (shortHeight+incident+1,7) hcompanion
    simp [endpoint] at hforbidden
    omega

theorem aa_negative_only_all_route_capacity
    (phase01 phase10 allRoutes cornerEvents negativeBand oldReservations
      unselected unused : Int)
    (hidentity : 2*(phase01+phase10) =
      allRoutes+cornerEvents+negativeBand+oldReservations+unselected+unused)
    (hunused : 0 ≤ unused) :
    allRoutes+cornerEvents+negativeBand+oldReservations+unselected ≤
      2*(phase01+phase10) := by omega

end SubQuorum.AABSecondCorner
