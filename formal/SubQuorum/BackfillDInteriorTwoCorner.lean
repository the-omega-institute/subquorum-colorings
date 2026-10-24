import SubQuorum.BackfillBandOutputs

set_option autoImplicit false

namespace SubQuorum.BackfillDInteriorTwoCorner

open WidthSixBottomOwner BackfillBandOutputs

def secondCornerBlockers : List Point :=
  [(-1,-2),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(2,1)]

theorem companion_supplies_four_second_corner_blockers
    (width height far incident : Int)
    (hwidth : 6 ≤ width) (hincident : 4 ≤ incident)
    (hinterior : incident ≤ height-4) :
    companionOwn width height far (0,-incident-4) ∧
    companionOwn width height far (0,-incident-3) ∧
    companionOwn width height far (0,-incident-2) ∧
    companionOwn width height far (0,-incident-1) := by
  simp [companionOwn, endpoint]
  omega

theorem negative_bar_supplies_three_second_corner_blockers
    (width incident far : Int) (hwidth : 6 ≤ width) :
    negativeOwn width incident far (1,-incident-1) ∧
    negativeOwn width incident far (2,-incident-1) ∧
    negativeOwn width incident far (3,-incident-1) := by
  simp [negativeOwn, endpoint]
  omega

theorem second_corner_has_no_rotor_owner :
    rotorOwners secondCornerBlockers = [] := by decide

theorem second_corner_keeps_original_tile_parity
    (incident : Int) (heven : incident%2 = 0) :
    (1 : Int)%2 = 1 ∧ (-incident-2)%2 = 0 := by omega

theorem aa_terminal_support_frame_forces_two_westward_endpoints
    (transpose flipRow flipColumn : Bool)
    (hframe :
      (pull transpose flipRow flipColumn (0,0) (-1,0) = (1,0) ∧
       pull transpose flipRow flipColumn (0,0) (0,1) = (0,1)) ∨
      (pull transpose flipRow flipColumn (0,0) (-1,0) = (0,1) ∧
       pull transpose flipRow flipColumn (0,0) (0,1) = (1,0))) :
    (pull transpose flipRow flipColumn (0,0) (-1,-1) = (1,-1) ∧
     pull transpose flipRow flipColumn (0,0) (-1,-2) = (1,-2)) ∨
    (pull transpose flipRow flipColumn (0,0) (1,1) = (1,-1) ∧
     pull transpose flipRow flipColumn (0,0) (2,1) = (1,-2)) := by
  cases transpose <;> cases flipRow <;> cases flipColumn <;>
    simp [pull] at hframe ⊢

theorem aa_incoming_owner_contains_collision_but_not_west_extension
    (width height far shortHeight : Int)
    (hwidth : 6 ≤ width) (hshort : 4 ≤ shortHeight)
    (hheight : shortHeight ≤ height) :
    endpoint width height far (height+2-(shortHeight+1),5-4) ∧
    ¬ endpoint width height far (height+2-(shortHeight+1),4-4) := by
  simp [endpoint]
  omega

theorem aa_collision_cannot_be_hidden_by_recurring_owner
    (ownerOf : Point → Nat) (incoming other : Nat) (collision extension : Point)
    (hincoming : ownerOf collision = incoming)
    (hcollision : ownerOf collision = other)
    (hextension : ownerOf extension = other)
    (habsent : ownerOf extension ≠ incoming) : False := by
  have hequal : other = incoming := hcollision.symm.trans hincoming
  exact habsent (hextension.trans hequal)

theorem enlarged_pool_exposes_one_unit_per_interior_event
    (activation positiveCap positiveSecond positiveBand positiveD
      negativeD negativeBand oldUnused newUnused : Int)
    (hpartition : negativeD+positiveD = negativeBand)
    (hcomplement : oldUnused = negativeD+newUnused) :
    (activation-positiveCap-positiveSecond-positiveBand)+oldUnused =
      (activation-positiveCap-positiveSecond-positiveBand-positiveD)+
        newUnused+negativeBand := by omega

theorem d_two_corner_exact_single_pool_identity
    (phase01 phase10 phase11 negativeCap positiveCap unfilled oldReservations
      cornerEvents negativeSecond positiveSecond positiveBand negativeBand
      negativeD positiveD activation unused rotor boundary reserve : Int)
    (hsecond : negativeSecond+positiveSecond = cornerEvents)
    (hdsecond : negativeD+positiveD = negativeBand)
    (hpool : negativeCap+oldReservations+cornerEvents+negativeSecond+
      negativeBand+negativeD+unused = 2*phase01+2*phase10)
    (hcap : negativeCap+positiveCap+unfilled = 2*phase11)
    (hreserve : 2*reserve = activation+unfilled+rotor+boundary) :
    2*reserve = 2*(phase11-phase01-phase10)+oldReservations+2*cornerEvents+
      2*negativeBand+positiveBand+
      (activation-positiveCap-positiveSecond-positiveBand-positiveD)+
      rotor+boundary+unused := by omega

theorem d_two_corner_cap_activation_capacity
    (phase01 phase10 phase11 negativeCap positiveCap unfilled oldReservations
      cornerEvents negativeSecond positiveSecond positiveBand negativeBand
      negativeD positiveD activation unused : Int)
    (hsecond : negativeSecond+positiveSecond = cornerEvents)
    (hdsecond : negativeD+positiveD = negativeBand)
    (hpool : negativeCap+oldReservations+cornerEvents+negativeSecond+
      negativeBand+negativeD+unused = 2*phase01+2*phase10)
    (hcap : negativeCap+positiveCap+unfilled = 2*phase11)
    (hactivation : positiveCap+positiveSecond+positiveBand+positiveD ≤ activation)
    (hunused : 0 ≤ unused) :
    2*phase11+oldReservations+2*cornerEvents+2*negativeBand+positiveBand ≤
      2*(phase01+phase10)+activation+unfilled := by omega

theorem d_two_corner_all_route_exact_identity
    (phase01 phase10 phase11 oldReservations cornerEvents positiveBand negativeBand
      activation positiveCap positiveSecond positiveD rotor boundary unused reserve
      routeA routeB routeC routeD capB capD unselected allRoutes : Int)
    (hidentity : 2*reserve =
      2*(phase11-phase01-phase10)+oldReservations+2*cornerEvents+2*negativeBand+
      positiveBand+(activation-positiveCap-positiveSecond-positiveBand-positiveD)+
      rotor+boundary+unused)
    (hselected : 2*phase11 = routeA+capB+capD+unselected)
    (hb : routeB = capB+positiveBand) (hc : routeC = cornerEvents)
    (hd : routeD = capD+negativeBand)
    (hall : allRoutes = routeA+routeB+routeC+routeD) :
    2*reserve = allRoutes+cornerEvents+negativeBand-2*(phase01+phase10)+
      oldReservations+unselected+
      (activation-positiveCap-positiveSecond-positiveBand-positiveD)+
      rotor+boundary+unused := by omega

theorem d_two_corner_all_route_retained_compensation
    (allRoutes cornerEvents negativeBand phase01 phase10 oldReservations unselected
      activation positiveCap positiveSecond positiveBand positiveD
      rotor boundary unused reserve : Int)
    (hidentity : 2*reserve =
      allRoutes+cornerEvents+negativeBand-2*(phase01+phase10)+oldReservations+
      unselected+(activation-positiveCap-positiveSecond-positiveBand-positiveD)+
      rotor+boundary+unused)
    (hactivation : positiveCap+positiveSecond+positiveBand+positiveD ≤ activation)
    (hunused : 0 ≤ unused) :
    allRoutes+cornerEvents+negativeBand-2*(phase01+phase10)+oldReservations+
      unselected+rotor+boundary ≤ 2*reserve := by omega

theorem d_two_corner_all_route_cap_activation_capacity
    (phase01 phase10 phase11 oldReservations cornerEvents positiveBand negativeBand
      activation unfilled routeA routeB routeD capB capD unselected allRoutes : Int)
    (hcapacity : 2*phase11+oldReservations+2*cornerEvents+2*negativeBand+positiveBand ≤
      2*(phase01+phase10)+activation+unfilled)
    (hselected : 2*phase11 = routeA+capB+capD+unselected)
    (hb : routeB = capB+positiveBand) (hd : routeD = capD+negativeBand)
    (hall : allRoutes = routeA+routeB+cornerEvents+routeD) :
    allRoutes+cornerEvents+negativeBand+oldReservations+unselected ≤
      2*(phase01+phase10)+activation+unfilled := by omega

theorem aa_new_negative_complement_and_activation_restriction
    (negativeD positiveD negativeBand oldUnused newUnused terminal
      positiveCap positiveSecond positiveBand activation : Int)
    (hpartition : negativeD+positiveD = negativeBand)
    (hcomplement : oldUnused = negativeD+newUnused)
    (hdpositive : positiveD = 0) (hcpositive : positiveSecond = 0)
    (hcap : positiveCap = 0) (hactivation : activation = 2)
    (hterminal : terminal+positiveCap+positiveSecond+positiveBand+positiveD ≤ activation) :
    negativeD = negativeBand ∧ oldUnused = negativeBand+newUnused ∧
      terminal+positiveBand ≤ 2 := by omega

theorem d_two_corner_shared_stops
    (counted direct unactivatedCorner activatedCorner terminal oldStops rotorStops
      positiveCap positiveSecond positiveBand positiveD activation boundary
      rotor unfilled reserve : Int)
    (hpartition : counted = direct+unactivatedCorner+activatedCorner+terminal)
    (hstops : direct+unactivatedCorner+oldStops ≤ boundary)
    (hcorner : activatedCorner ≤ activation)
    (hterminal : terminal+positiveCap+positiveSecond+positiveBand+positiveD ≤ activation)
    (hrotor : rotorStops ≤ rotor)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary) :
    counted+oldStops+rotorStops+positiveCap+positiveSecond+positiveBand+positiveD+
      unfilled ≤ 2*reserve+activation := by omega

theorem d_two_corner_all_route_shared_stops
    (counted oldStops rotorStops phase01 phase10 phase11 negativeCap positiveCap
      unfilled oldReservations cornerEvents negativeSecond positiveSecond
      positiveBand negativeBand negativeD positiveD unused reserve activation
      routeA routeB routeD capB capD unselected allRoutes : Int)
    (hjoint : counted+oldStops+rotorStops+positiveCap+positiveSecond+positiveBand+
      positiveD+unfilled ≤ 2*reserve+activation)
    (hsecond : negativeSecond+positiveSecond = cornerEvents)
    (hdsecond : negativeD+positiveD = negativeBand)
    (hpool : negativeCap+oldReservations+cornerEvents+negativeSecond+
      negativeBand+negativeD+unused = 2*phase01+2*phase10)
    (hcap : negativeCap+positiveCap+unfilled = 2*phase11)
    (hselected : 2*phase11 = routeA+capB+capD+unselected)
    (hb : routeB = capB+positiveBand) (hd : routeD = capD+negativeBand)
    (hall : allRoutes = routeA+routeB+cornerEvents+routeD) :
    counted+oldStops+rotorStops+allRoutes+cornerEvents+negativeBand-
      2*(phase01+phase10)+oldReservations+unselected+unused ≤
        2*reserve+activation := by omega

end SubQuorum.BackfillDInteriorTwoCorner
