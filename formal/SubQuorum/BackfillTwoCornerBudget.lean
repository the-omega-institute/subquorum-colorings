import SubQuorum.BackfillCornerRouting

set_option autoImplicit false

namespace SubQuorum.BackfillTwoCornerBudget

open WidthSixBottomOwner

def secondCornerBlockers : List Point :=
  [(-1,-2),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(2,1)]

theorem singleton_route_second_corner_has_no_rotor_owner :
    rotorOwners secondCornerBlockers = [] := by decide

theorem two_corner_cap_and_activation_budget
    (phase01 phase10 phase11 negativeCap positiveCap unfilled irregular oldRegular
      cornerEvents negativeSecond positiveSecond activation unused : Int)
    (hsecond : negativeSecond+positiveSecond = cornerEvents)
    (hpool : negativeCap+irregular+oldRegular+cornerEvents+negativeSecond+unused =
      2*phase01+2*phase10)
    (hcap : negativeCap+positiveCap+unfilled = 2*phase11)
    (hactivation : positiveCap+positiveSecond ≤ activation) (hunused : 0 ≤ unused) :
    2*phase11+irregular+oldRegular+2*cornerEvents ≤
      2*phase01+2*phase10+activation+unfilled := by omega

theorem two_corner_exact_single_pool_identity
    (phase01 phase10 phase11 negativeCap positiveCap unfilled irregular oldRegular
      cornerEvents negativeSecond positiveSecond activation unused rotor boundary reserve : Int)
    (hsecond : negativeSecond+positiveSecond = cornerEvents)
    (hpool : negativeCap+irregular+oldRegular+cornerEvents+negativeSecond+unused =
      2*phase01+2*phase10)
    (hcap : negativeCap+positiveCap+unfilled = 2*phase11)
    (hreserve : 2*reserve = activation+unfilled+rotor+boundary) :
    2*reserve = 2*(phase11-phase01-phase10)+irregular+oldRegular+2*cornerEvents+
      (activation-positiveCap-positiveSecond)+rotor+boundary+unused := by omega

theorem two_corner_retained_compensation
    (phase01 phase10 phase11 irregular oldRegular cornerEvents activation positiveCap
      positiveSecond rotor boundary unused reserve : Int)
    (hidentity : 2*reserve =
      2*(phase11-phase01-phase10)+irregular+oldRegular+2*cornerEvents+
      (activation-positiveCap-positiveSecond)+rotor+boundary+unused)
    (hactivation : positiveCap+positiveSecond ≤ activation) (hunused : 0 ≤ unused) :
    2*(phase11-phase01-phase10)+irregular+oldRegular+2*cornerEvents+rotor+boundary
      ≤ 2*reserve := by omega

theorem shared_stops_with_cap_and_backfill_activations
    (counted direct unactivatedCorner activatedCorner terminal oldStops rotorStops
      positiveCap positiveSecond activation boundary rotor unfilled reserve : Int)
    (hpartition : counted = direct+unactivatedCorner+activatedCorner+terminal)
    (hstops : direct+unactivatedCorner+oldStops ≤ boundary)
    (hcorner : activatedCorner ≤ activation)
    (hterminal : terminal+positiveCap+positiveSecond ≤ activation)
    (hrotor : rotorStops ≤ rotor)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary) :
    counted+oldStops+rotorStops+positiveCap+positiveSecond+unfilled
      ≤ 2*reserve+activation := by omega

theorem two_corner_shared_stops_compensation
    (counted oldStops rotorStops phase01 phase10 phase11 negativeCap positiveCap
      unfilled irregular oldRegular cornerEvents negativeSecond positiveSecond
      unused reserve activation : Int)
    (hjoint : counted+oldStops+rotorStops+positiveCap+positiveSecond+unfilled
      ≤ 2*reserve+activation)
    (hsecond : negativeSecond+positiveSecond = cornerEvents)
    (hpool : negativeCap+irregular+oldRegular+cornerEvents+negativeSecond+unused =
      2*phase01+2*phase10)
    (hcap : negativeCap+positiveCap+unfilled = 2*phase11) :
    counted+oldStops+rotorStops+2*(phase11-phase01-phase10)+irregular+oldRegular+
      2*cornerEvents+unused ≤ 2*reserve+activation := by omega

end SubQuorum.BackfillTwoCornerBudget
