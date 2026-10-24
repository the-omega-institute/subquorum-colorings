import SubQuorum.WidthSixBottomOwner

set_option autoImplicit false

namespace SubQuorum.BackfillBandOutputs

open WidthSixBottomOwner

def companionOwn (width incident far : Int) (point : Point) : Prop :=
  endpoint width incident far (point.2+incident+1,point.1+1)

def companionSupport (width incident far : Int) (point : Point) : Prop :=
  support width incident far (point.2+incident+1,point.1+1)

def positiveOwn (width incident far : Int) (point : Point) : Prop :=
  endpoint width incident far (-point.2-1,point.1)

def positiveSupport (width incident far : Int) (point : Point) : Prop :=
  support width incident far (-point.2-1,point.1)

def negativeOwn (width incident far : Int) (point : Point) : Prop :=
  endpoint width incident far (point.2+incident+1,point.1)

def negativeSupport (width incident far : Int) (point : Point) : Prop :=
  support width incident far (point.2+incident+1,point.1)

theorem positive_band_incident_drop
    (companionWidth companionHeight companionFar width incident far : Int)
    (hcompanionWidth : 6 ≤ companionWidth) (hcompanionHeight : 4 ≤ companionHeight)
    (hwidth : 6 ≤ width)
    (hdisjoint : ∀ point, companionOwn companionWidth companionHeight companionFar point →
      ¬ positiveOwn width incident far point) : incident ≤ companionHeight-2 := by
  have hbar : companionOwn companionWidth companionHeight companionFar (1,-companionHeight) := by
    simp [companionOwn, endpoint]
    omega
  have hcollision := hdisjoint (1,-companionHeight) hbar
  simp [positiveOwn, endpoint] at hcollision
  omega

theorem negative_band_incident_drop
    (companionWidth companionHeight companionFar width incident far : Int)
    (hcompanionWidth : 6 ≤ companionWidth) (hcompanionHeight : 4 ≤ companionHeight)
    (hwidth : 6 ≤ width)
    (hdisjoint : ∀ point, companionOwn companionWidth companionHeight companionFar point →
      ¬ negativeOwn width incident far point) : incident ≤ companionHeight-2 := by
  have hbar : companionOwn companionWidth companionHeight companionFar (1,-companionHeight) := by
    simp [companionOwn, endpoint]
    omega
  have hcollision := hdisjoint (1,-companionHeight) hbar
  simp [negativeOwn, endpoint] at hcollision
  omega

theorem occupied_band_output_alternatives
    (incident companionHeight : Int)
    (hevenIncident : incident%2 = 0) (hevenCompanion : companionHeight%2 = 0)
    (hdrop : incident ≤ companionHeight-2) :
    incident = companionHeight-2 ∨ incident ≤ companionHeight-4 := by omega

theorem positive_output_exact_singleton_and_two_supports
    (width incident far : Int)
    (hwidth : 6 ≤ width) (hincident : 4 ≤ incident)
    (hevenIncident : incident%2 = 0) :
    positiveOwn width incident far (1,-incident-1) ∧
    ¬ positiveOwn width incident far (0,-incident-2) ∧
    ¬ positiveOwn width incident far (0,-incident-1) ∧
    ¬ positiveOwn width incident far (1,-incident-2) ∧
    positiveSupport width incident far (0,-incident-1) ∧
    positiveSupport width incident far (1,-incident-2) ∧
    ¬ positiveSupport width incident far (0,-incident-2) ∧
    ¬ positiveSupport width incident far (1,-incident-1) := by
  simp [positiveOwn, positiveSupport, endpoint, support]
  omega

theorem negative_output_exact_singleton_and_one_support
    (width incident far : Int) (hwidth : 6 ≤ width) (hincident : 4 ≤ incident) :
    negativeOwn width incident far (1,-incident-1) ∧
    ¬ negativeOwn width incident far (0,-incident-2) ∧
    ¬ negativeOwn width incident far (0,-incident-1) ∧
    ¬ negativeOwn width incident far (1,-incident-2) ∧
    negativeSupport width incident far (0,-incident-1) ∧
    ¬ negativeSupport width incident far (1,-incident-2) ∧
    ¬ negativeSupport width incident far (0,-incident-2) ∧
    ¬ negativeSupport width incident far (1,-incident-1) := by
  simp [negativeOwn, negativeSupport, endpoint, support]
  omega

theorem companion_cap_output_exact_triple
    (width companionHeight far incident : Int)
    (hwidth : 6 ≤ width) (hincident : 4 ≤ incident)
    (hcap : incident = companionHeight-2) :
    companionOwn width companionHeight far (0,-incident-2) ∧
    companionOwn width companionHeight far (0,-incident-1) ∧
    companionOwn width companionHeight far (1,-incident-2) ∧
    ¬ companionOwn width companionHeight far (1,-incident-1) ∧
    ¬ companionSupport width companionHeight far (0,-incident-2) ∧
    ¬ companionSupport width companionHeight far (0,-incident-1) ∧
    ¬ companionSupport width companionHeight far (1,-incident-2) ∧
    ¬ companionSupport width companionHeight far (1,-incident-1) := by
  simp [companionOwn, companionSupport, endpoint, support]
  omega

theorem companion_interior_output_exact_pair
    (width companionHeight far incident : Int)
    (hwidth : 6 ≤ width) (hincident : 4 ≤ incident)
    (hevenIncident : incident%2 = 0) (hevenCompanion : companionHeight%2 = 0)
    (hinterior : incident ≤ companionHeight-4) :
    companionOwn width companionHeight far (0,-incident-2) ∧
    companionOwn width companionHeight far (0,-incident-1) ∧
    ¬ companionOwn width companionHeight far (1,-incident-2) ∧
    ¬ companionOwn width companionHeight far (1,-incident-1) ∧
    companionSupport width companionHeight far (1,-incident-2) ∧
    ¬ companionSupport width companionHeight far (1,-incident-1) ∧
    ¬ companionSupport width companionHeight far (0,-incident-2) ∧
    ¬ companionSupport width companionHeight far (0,-incident-1) := by
  simp [companionOwn, companionSupport, endpoint, support]
  omega

theorem interior_pair_excludes_original_terminal
    (companionHeight incident : Int)
    (hincident : 4 ≤ incident) (hinterior : incident ≤ companionHeight-4) :
    3 ≤ companionHeight-incident-1 ∧ companionHeight-incident < companionHeight := by omega

theorem band_outputs_exact_single_pool_reserve
    (phase01 phase10 phase11 negativeCap positiveCap unfilled irregular oldRegular
      cornerEvents negativeSecond positiveSecond positiveBand negativeBand
      activation unused rotor boundary reserve : Int)
    (hsecond : negativeSecond+positiveSecond = cornerEvents)
    (hpool : negativeCap+irregular+oldRegular+cornerEvents+negativeSecond+negativeBand+unused =
      2*phase01+2*phase10)
    (hcap : negativeCap+positiveCap+unfilled = 2*phase11)
    (hreserve : 2*reserve = activation+unfilled+rotor+boundary) :
    2*reserve = 2*(phase11-phase01-phase10)+irregular+oldRegular+2*cornerEvents+
      negativeBand+positiveBand+(activation-positiveCap-positiveSecond-positiveBand)+
      rotor+boundary+unused := by omega

theorem band_outputs_retained_compensation
    (phase01 phase10 phase11 irregular oldRegular cornerEvents negativeBand positiveBand
      activation positiveCap positiveSecond rotor boundary unused reserve : Int)
    (hidentity : 2*reserve =
      2*(phase11-phase01-phase10)+irregular+oldRegular+2*cornerEvents+negativeBand+
      positiveBand+(activation-positiveCap-positiveSecond-positiveBand)+rotor+boundary+unused)
    (hactivation : positiveCap+positiveSecond+positiveBand ≤ activation)
    (hunused : 0 ≤ unused) :
    2*(phase11-phase01-phase10)+irregular+oldRegular+2*cornerEvents+
      negativeBand+positiveBand+rotor+boundary ≤ 2*reserve := by omega

theorem band_outputs_shared_stops
    (counted direct unactivatedCorner activatedCorner terminal oldStops rotorStops
      positiveCap positiveSecond positiveBand activation boundary rotor unfilled reserve : Int)
    (hpartition : counted = direct+unactivatedCorner+activatedCorner+terminal)
    (hstops : direct+unactivatedCorner+oldStops ≤ boundary)
    (hcorner : activatedCorner ≤ activation)
    (hterminal : terminal+positiveCap+positiveSecond+positiveBand ≤ activation)
    (hrotor : rotorStops ≤ rotor)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary) :
    counted+oldStops+rotorStops+positiveCap+positiveSecond+positiveBand+unfilled
      ≤ 2*reserve+activation := by omega

theorem band_outputs_shared_source_census
    (counted oldStops rotorStops phase01 phase10 phase11 negativeCap positiveCap
      unfilled irregular oldRegular cornerEvents negativeSecond positiveSecond
      positiveBand negativeBand unused reserve activation : Int)
    (hjoint : counted+oldStops+rotorStops+positiveCap+positiveSecond+positiveBand+unfilled
      ≤ 2*reserve+activation)
    (hsecond : negativeSecond+positiveSecond = cornerEvents)
    (hpool : negativeCap+irregular+oldRegular+cornerEvents+negativeSecond+negativeBand+unused =
      2*phase01+2*phase10)
    (hcap : negativeCap+positiveCap+unfilled = 2*phase11) :
    counted+oldStops+rotorStops+2*(phase11-phase01-phase10)+irregular+oldRegular+
      2*cornerEvents+negativeBand+positiveBand+unused ≤ 2*reserve+activation := by omega

theorem all_positive_routes_activation_capacity
    (positiveRoutes capRoutes positiveBand terminal positiveCap positiveSecond activation : Int)
    (hpartition : positiveRoutes = capRoutes+positiveBand)
    (hcap : capRoutes ≤ positiveCap)
    (hactivation : terminal+positiveCap+positiveSecond+positiveBand ≤ activation) :
    terminal+positiveSecond+positiveRoutes ≤ activation := by omega

theorem all_positive_routes_enter_shared_bound
    (counted oldStops rotorStops positiveCap positiveSecond positiveBand unfilled
      positiveRoutes capRoutes reserve activation : Int)
    (hjoint : counted+oldStops+rotorStops+positiveCap+positiveSecond+positiveBand+unfilled
      ≤ 2*reserve+activation)
    (hpartition : positiveRoutes = capRoutes+positiveBand)
    (hcap : capRoutes ≤ positiveCap) :
    counted+oldStops+rotorStops+positiveRoutes+positiveSecond+unfilled
      ≤ 2*reserve+activation := by omega

end SubQuorum.BackfillBandOutputs
