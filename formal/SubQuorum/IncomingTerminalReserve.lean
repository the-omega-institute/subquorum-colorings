import SubQuorum.WidthSixBottomOwner

set_option autoImplicit false

namespace SubQuorum.IncomingTerminalReserve

open WidthSixBottomOwner

def incomingOwn (width height far positiveWidth : Int) (point : Point) : Prop :=
  endpoint width height far (height+2-point.1,point.2-positiveWidth+2)

def bandCompanionOwn (width height far positiveWidth : Int) (point : Point) : Prop :=
  endpoint width height far (height-point.1,positiveWidth+2-point.2)

def capOwn (width height far positiveWidth shortHeight : Int)
    (transposed : Bool) (point : Point) : Prop :=
  endpoint width height far
    (if transposed then positiveWidth+2-point.2 else shortHeight+2-point.1,
     if transposed then shortHeight+2-point.1 else positiveWidth+2-point.2)

theorem incoming_has_endpoint_and_missing_neighbor
    (width height far positiveWidth shortHeight : Int)
    (hwidth : 6 ≤ width) (hshort : 4 ≤ shortHeight)
    (hheight : shortHeight ≤ height) :
    incomingOwn width height far positiveWidth (shortHeight+1,positiveWidth-1) ∧
    ¬ incomingOwn width height far positiveWidth (shortHeight+1,positiveWidth-2) := by
  simp [incomingOwn, endpoint]
  omega

theorem band_companion_must_cross_incoming
    (width height far otherWidth otherHeight otherFar positiveWidth : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height)
    (hotherWidth : 6 ≤ otherWidth) (hotherHeight : 4 ≤ otherHeight) :
    (bandCompanionOwn width height far positiveWidth (otherHeight+1,positiveWidth+1) ∧
      incomingOwn otherWidth otherHeight otherFar positiveWidth
        (otherHeight+1,positiveWidth+1)) ∨
    (bandCompanionOwn width height far positiveWidth (height,positiveWidth-1) ∧
      incomingOwn otherWidth otherHeight otherFar positiveWidth (height,positiveWidth-1)) := by
  by_cases horder : otherHeight+1 ≤ height
  · left
    simp [bandCompanionOwn, incomingOwn, endpoint]
    omega
  · right
    simp [bandCompanionOwn, incomingOwn, endpoint]
    omega

theorem incoming_excludes_band_companion
    (width height far otherWidth otherHeight otherFar positiveWidth : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height)
    (hotherWidth : 6 ≤ otherWidth) (hotherHeight : 4 ≤ otherHeight)
    (hdisjoint : ∀ point, bandCompanionOwn width height far positiveWidth point →
      ¬ incomingOwn otherWidth otherHeight otherFar positiveWidth point) : False := by
  rcases band_companion_must_cross_incoming width height far otherWidth otherHeight
    otherFar positiveWidth hwidth hheight hotherWidth hotherHeight
    with ⟨hfirst,hsecond⟩ | ⟨hfirst,hsecond⟩
  · exact hdisjoint _ hfirst hsecond
  · exact hdisjoint _ hfirst hsecond

theorem both_cap_orientations_own_distinguishing_pair
    (width height far positiveWidth shortHeight : Int) (transposed : Bool)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height) :
    capOwn width height far positiveWidth shortHeight transposed
      (shortHeight+1,positiveWidth-1) ∧
    capOwn width height far positiveWidth shortHeight transposed
      (shortHeight+1,positiveWidth-2) := by
  cases transposed <;> simp [capOwn, endpoint] <;> omega

theorem reserved_activation_improves_all_route_bound
    (reserve negativeSources allRoutes routeC interiorD old capComplement
      activationSlack rotor boundary unused protectedTerminals : Nat)
    (hidentity : 2*reserve+2*negativeSources = allRoutes+routeC+interiorD+old+
      capComplement+activationSlack+rotor+boundary+unused)
    (hprotected : protectedTerminals ≤ activationSlack) :
    allRoutes+routeC+interiorD+old+capComplement+rotor+boundary+protectedTerminals
      ≤ 2*reserve+2*negativeSources := by
  omega

theorem competing_activation_bounds_use_maximum
    (activationSlack protectedTerminals terminalClaims : Nat)
    (hprotected : protectedTerminals ≤ activationSlack)
    (hterminal : terminalClaims ≤ activationSlack) :
    max protectedTerminals terminalClaims ≤ activationSlack := by
  omega

end SubQuorum.IncomingTerminalReserve
