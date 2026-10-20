import SubQuorum.ActivatedSingletonBudget

set_option autoImplicit false
set_option maxRecDepth 1000000
set_option maxHeartbeats 500000000

namespace SubQuorum.ExactEventReserve

open SubQuorum.SingletonNegativeDefects
open SubQuorum.ActivatedSingletonBudget

def loneIrregular (profiles : List Profile) : Bool :=
  (endpoints profiles).length == 1 && profiles.all singletonProfile

def soleIrregularPair (profiles : List Profile) : Bool :=
  (endpoints profiles).length == 2 && profiles.length == 1 &&
    profiles.all barProfile

def mutualIrregularPair (profiles : List Profile) : Bool :=
  (endpoints profiles).length == 2 && profiles.length == 2 &&
    profiles.all singletonProfile && (charge profiles).irregular == 0

def mixedThree (profiles : List Profile) : Bool :=
  (endpoints profiles).length == 3 && decide (1 < profiles.length)

def weight (flag : Bool) : Int := if flag then 1 else 0

def boundaryCost (profiles : List Profile) : Int :=
  weight (loneIrregular profiles)+2*weight (soleIrregularPair profiles)+
    2*weight (mutualIrregularPair profiles)+weight (mixedThree profiles)

def exactLocalCheck (profiles : List Profile) : Bool :=
  if feasible profiles then
    let current := charge profiles
    decide (current.slots+current.exceptionalThree-
      2*(current.irregular-current.credit)+forwarding profiles-
      Int.ofNat (activatedSingletons profiles) = boundaryCost profiles)
  else true

theorem complete_exact_local_table : allPackings.all exactLocalCheck = true := by decide

theorem boundary_cost_nonnegative (profiles : List Profile) : 0 ≤ boundaryCost profiles := by
  unfold boundaryCost weight
  split <;> split <;> split <;> split <;> omega

theorem exact_reserve_identity
    (reserve diagonal exceptionalU exceptionalR forwardingU forwardingR
      activatedPositive activatedRotor unusedU unpairedRotor remainder boundary : Int)
    (hreserve : 2*reserve = 2*diagonal-exceptionalU-exceptionalR+remainder)
    (hunused : unusedU = 2*diagonal-exceptionalU-forwardingU)
    (hunpaired : unpairedRotor = activatedRotor-exceptionalR-forwardingR)
    (hlocal : boundary = remainder+forwardingU+forwardingR-
      activatedPositive-activatedRotor) :
    2*reserve = activatedPositive+unusedU+unpairedRotor+boundary := by omega

theorem zero_reserve_iff
    (reserve activated unused unpaired lone bar mutualPairs mixed : Int)
    (hactivated : 0 ≤ activated) (hunused : 0 ≤ unused)
    (hunpaired : 0 ≤ unpaired) (hlone : 0 ≤ lone) (hbar : 0 ≤ bar)
    (hmutual : 0 ≤ mutualPairs) (hmixed : 0 ≤ mixed)
    (hidentity : 2*reserve = activated+unused+unpaired+lone+2*bar+2*mutualPairs+mixed) :
    reserve = 0 ↔ activated = 0 ∧ unused = 0 ∧ unpaired = 0 ∧
      lone = 0 ∧ bar = 0 ∧ mutualPairs = 0 ∧ mixed = 0 := by omega

theorem residual_parity
    (reserve activated unused unpaired lone bar mutualPairs mixed : Int)
    (hidentity : 2*reserve = activated+unused+unpaired+lone+2*bar+2*mutualPairs+mixed) :
    (activated+unused+unpaired+lone+mixed)%2 = 0 := by omega

theorem exact_defect_slack
    (slack positive marked reserve activated unused unpaired lone bar mutualPairs mixed : Int)
    (hledger : positive+reserve-marked ≤ slack)
    (hidentity : 2*reserve = activated+unused+unpaired+lone+2*bar+2*mutualPairs+mixed) :
    positive-marked+bar+mutualPairs+(activated+unused+unpaired+lone+mixed)/2 ≤ slack := by
  omega

theorem joint_allocation_iff
    (positive marked reserve defect : Int)
    (hidentity : 2*reserve = defect) :
    0 ≤ positive+reserve-marked ↔ 2*marked ≤ 2*positive+defect := by omega

theorem joint_failure_iff
    (positive marked reserve defect : Int)
    (hidentity : 2*reserve = defect) :
    positive+reserve-marked < 0 ↔ defect ≤ 2*marked-2*positive-2 := by omega

theorem blank_gate_refinement
    (reserve activated unused unpaired boundary blank : Int)
    (hidentity : 2*reserve = activated+unused+unpaired+boundary)
    (hblank : blank ≤ boundary) :
    activated+blank+unused+unpaired ≤ 2*reserve := by omega

theorem single_positive_failure_saturates
    (marked reserve defect : Int)
    (hmarked : marked ≤ 2) (hdefect : 0 ≤ defect)
    (hidentity : 2*reserve = defect) (hfailure : 1+reserve-marked < 0) :
    marked = 2 ∧ reserve = 0 ∧ defect = 0 := by omega

theorem single_positive_nonzero_defect_pays
    (marked reserve defect : Int)
    (hmarked : marked ≤ 2) (hdefect : 0 < defect)
    (hidentity : 2*reserve = defect) : 0 ≤ 1+reserve-marked := by omega

end SubQuorum.ExactEventReserve
