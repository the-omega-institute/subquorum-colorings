import SubQuorum.WidthSixBottomOwner

set_option autoImplicit false

namespace SubQuorum.BackfillFourRouteBudget

open WidthSixBottomOwner

theorem route_A_companion_candidate_meets_original_root_wall
    (width rootHeight far incident : Int)
    (hincident : 4 ≤ incident)
    (hdrop : incident ≤ rootHeight-4) :
    endpoint width far rootHeight (rootHeight-(incident+2),width) := by
  simp [endpoint]
  omega

theorem south_companion_at_even_odd_corner_has_east_active_direction
    (row column : Int) (hcorner : (-row+1,-column) = ((1 : Int),(-1 : Int))) :
    (row,column) = ((0 : Int),(1 : Int)) := by
  simp only [Prod.mk.injEq] at hcorner ⊢
  omega

theorem route_A_terminal_reuse_contradicts_original_phase_tag
    (tag : Point → Option Point) (incident activeRow activeColumn : Int)
    (hcorner : (-activeRow+1,-activeColumn) = ((1 : Int),(-1 : Int)))
    (hwall : tag (incident+2,0) = none)
    (hactive : tag (incident+2+activeRow,-1+activeColumn) =
      some (activeRow,activeColumn)) : False := by
  have hframe := south_companion_at_even_odd_corner_has_east_active_direction
    activeRow activeColumn hcorner
  have hrow : activeRow = 0 := congrArg Prod.fst hframe
  have hcolumn : activeColumn = 1 := congrArg Prod.snd hframe
  subst activeRow
  subst activeColumn
  simp at hactive
  rw [hwall] at hactive
  contradiction

theorem disjoint_selected_caps_joint_capacity
    (routeA routeBCap routeDCap unfilledA negativeA positiveA
      negativeCap positiveCap unfilled phase11 : Int)
    (hpartition : routeA = unfilledA+negativeA+positiveA)
    (hunfilled : unfilledA ≤ unfilled)
    (hnegative : negativeA+routeDCap ≤ negativeCap)
    (hpositive : positiveA+routeBCap ≤ positiveCap)
    (hcap : negativeCap+positiveCap+unfilled = 2*phase11) :
    routeA+routeBCap+routeDCap ≤ 2*phase11 := by omega

theorem all_routes_exact_single_pool_identity
    (routeA routeB routeC routeD routeBCap routeDCap interiorB interiorD
      phase01 phase10 phase11 irregular oldRegular activation positiveCap positiveSecond
      rotor boundary unused unselectedCaps reserve : Int)
    (hrouteB : routeB = routeBCap+interiorB)
    (hrouteD : routeD = routeDCap+interiorD)
    (hcap : 2*phase11 = routeA+routeBCap+routeDCap+unselectedCaps)
    (hidentity : 2*reserve = 2*(phase11-phase01-phase10)+irregular+oldRegular+
      2*routeC+interiorD+interiorB+(activation-positiveCap-positiveSecond-interiorB)+
      rotor+boundary+unused) :
    2*reserve = routeA+routeB+routeC+routeD+routeC-2*(phase01+phase10)+
      irregular+oldRegular+unselectedCaps+(activation-positiveCap-positiveSecond-interiorB)+
      rotor+boundary+unused := by omega

theorem all_routes_cap_activation_inequality
    (routeA routeB routeC routeD routeBCap routeDCap interiorB interiorD phase01
      phase10 phase11 irregular oldRegular activation unfilled unselectedCaps : Int)
    (hrouteB : routeB = routeBCap+interiorB)
    (hrouteD : routeD = routeDCap+interiorD)
    (hcap : 2*phase11 = routeA+routeBCap+routeDCap+unselectedCaps)
    (hjoint : 2*phase11+irregular+oldRegular+2*routeC+interiorD+interiorB ≤
      2*phase01+2*phase10+activation+unfilled) :
    routeA+routeB+routeC+routeD+routeC+irregular+oldRegular+unselectedCaps ≤
      2*(phase01+phase10)+activation+unfilled := by omega

theorem all_routes_retained_compensation
    (routeA routeB routeC routeD phase01 phase10 irregular oldRegular unselectedCaps
      activation positiveCap positiveSecond interiorB rotor boundary unused reserve : Int)
    (hidentity : 2*reserve = routeA+routeB+routeC+routeD+routeC-2*(phase01+phase10)+
      irregular+oldRegular+unselectedCaps+(activation-positiveCap-positiveSecond-interiorB)+
      rotor+boundary+unused)
    (hactivation : positiveCap+positiveSecond+interiorB ≤ activation)
    (hunused : 0 ≤ unused) :
    routeA+routeB+routeC+routeD+routeC-2*(phase01+phase10)+irregular+oldRegular+
      unselectedCaps+rotor+boundary ≤ 2*reserve := by omega

theorem all_routes_shared_stop_compensation
    (passive oldStops rotorStops routeA routeB routeC routeD routeBCap routeDCap
      interiorB interiorD phase01 phase10 phase11 irregular oldRegular unselectedCaps
      unused reserve activation : Int)
    (hrouteB : routeB = routeBCap+interiorB)
    (hrouteD : routeD = routeDCap+interiorD)
    (hcap : 2*phase11 = routeA+routeBCap+routeDCap+unselectedCaps)
    (hjoint : passive+oldStops+rotorStops+2*(phase11-phase01-phase10)+irregular+
      oldRegular+2*routeC+interiorD+interiorB+unused ≤ 2*reserve+activation) :
    passive+oldStops+rotorStops+routeA+routeB+routeC+routeD+routeC-2*(phase01+phase10)+
      irregular+oldRegular+unselectedCaps+unused ≤ 2*reserve+activation := by omega

end SubQuorum.BackfillFourRouteBudget
