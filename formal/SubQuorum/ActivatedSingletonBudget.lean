import SubQuorum.SingletonNegativeDefects

set_option autoImplicit false
set_option maxRecDepth 1000000
set_option maxHeartbeats 500000000

namespace SubQuorum.ActivatedSingletonBudget

open SubQuorum.SingletonNegativeDefects

def activatedSingletons (profiles : List Profile) : Nat :=
  (profiles.filter fun profile => profile.endpoints.length == 1 &&
    profile.selected.length == 2 &&
    profile.selected.any (endpoints profiles).contains).length

def forwarding (profiles : List Profile) : Int :=
  if (endpoints profiles).length == 4 && activatedSingletons profiles == 1 &&
    profiles.any (fun profile => profile.endpoints.length == 3) then 1 else 0

def activationPaymentCheck (profiles : List Profile) : Bool :=
  if feasible profiles then
    let current := charge profiles
    decide (Int.ofNat (activatedSingletons profiles) ≤ current.slots+
      current.exceptionalThree-2*(current.irregular-current.credit)+forwarding profiles)
  else true

theorem complete_local_activation_payment :
    allPackings.all activationPaymentCheck = true := by decide

def blankGateCandidate (profiles : List Profile) : Bool :=
  !(endpoints profiles ++ retained profiles).contains 0 &&
    profiles.any (fun profile => profile.negative && profile.endpoints.length == 2 &&
      profile.endpoints.contains 3 &&
      (profile.endpoints.contains 1 || profile.endpoints.contains 2) &&
      decide (profile.selected.length ≤ 1) &&
      profile.selected.all (endpoints profiles).contains)

def blankGateCheck (profiles : List Profile) : Bool :=
  if feasible profiles && blankGateCandidate profiles then
    let current := charge profiles
    activatedSingletons profiles == 0 && forwarding profiles == 0 &&
      decide (1 ≤ current.slots+current.exceptionalThree-
        2*(current.irregular-current.credit))
  else true

theorem complete_blank_gate_payment : allPackings.all blankGateCheck = true := by decide

def zeroRotorEndpoints : List Point :=
  rotorEndpoints.map fun point => (point.1-3, point.2)

def zeroRotorSelected : List Point :=
  rotorSelected.map fun point => (point.1-3, point.2)

def neighboring (first second : Point) : Bool :=
  decide ((first.1 = second.1 ∧ (first.2 = second.2+1 ∨ second.2 = first.2+1)) ∨
    (first.2 = second.2 ∧ (first.1 = second.1+1 ∨ second.1 = first.1+1)))

def bridgeCheck (missing support anchor : Point) : Bool :=
  !(zeroRotorEndpoints ++ zeroRotorSelected).contains missing &&
    zeroRotorSelected.contains support && zeroRotorEndpoints.contains anchor &&
    neighboring missing support && neighboring anchor support && decide (missing ≠ anchor)

theorem first_original_support_bridge :
    bridgeCheck (1,2) (1,1) (0,1) = true := by decide

theorem second_original_support_bridge :
    bridgeCheck (-2,3) (-2,4) (-1,4) = true := by decide

theorem distinct_bridge_targets :
    tile ((0,1) : Point) ≠ tile ((-1,4) : Point) := by decide

theorem forwarding_cancels
    (exceptionalU exceptionalR forwardingU forwardingR activated positiveActivated
      blankMarks diagonal remainder : Int)
    (hbridge : exceptionalR+forwardingR+positiveActivated ≤ activated)
    (hlocal : activated+blankMarks ≤ remainder+forwardingU+forwardingR)
    (hsource : exceptionalU+forwardingU ≤ 2*diagonal) :
    exceptionalU+exceptionalR+positiveActivated+blankMarks ≤ 2*diagonal+remainder := by
  omega

theorem activation_reserve
    (mass credit irregular exceptionalU exceptionalR diagonal remainder
      positiveActivated blankMarks : Int)
    (hidentity : 2*(mass+credit-irregular) =
      2*diagonal-exceptionalU-exceptionalR+remainder)
    (hbudget : exceptionalU+exceptionalR+positiveActivated+blankMarks ≤
      2*diagonal+remainder) :
    positiveActivated+blankMarks ≤ 2*(mass+credit-irregular) := by omega

theorem universal_event_reserve
    (mass credit irregular positiveActivated blankMarks : Int)
    (hpositive : 0 ≤ positiveActivated) (hblank : 0 ≤ blankMarks)
    (hbudget : positiveActivated+blankMarks ≤ 2*(mass+credit-irregular)) :
    irregular ≤ mass+credit := by omega

theorem activated_slack
    (slack positive mass credit irregular marked positiveActivated blankMarks : Int)
    (hledger : positive+mass+credit-irregular-marked ≤ slack)
    (hbudget : positiveActivated+blankMarks ≤ 2*(mass+credit-irregular)) :
    positive-marked+(positiveActivated+blankMarks+1)/2 ≤ slack := by omega

theorem unmarked_coefficient_one
    (slack positive mass credit irregular : Int)
    (hpositive : 0 ≤ positive) (hledger : positive+mass+credit-irregular ≤ slack)
    (hreserve : irregular ≤ mass+credit) : 0 ≤ slack := by omega

end SubQuorum.ActivatedSingletonBudget
