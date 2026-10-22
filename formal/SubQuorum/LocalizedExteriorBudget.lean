import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 10000
set_option maxHeartbeats 4000000

namespace SubQuorum.LocalizedExteriorBudget

def corners : List Nat := [0, 1, 2, 3]

def adjacent (first second : Nat) : Bool :=
  first != second && first+second != 3

def endpoint (state vertex : Nat) : Bool := state / 3^vertex % 3 == 1

def support (state vertex : Nat) : Bool := state / 3^vertex % 3 == 2

def occupied (state vertex : Nat) : Bool := endpoint state vertex || support state vertex

def endpointCount (state : Nat) : Nat := (corners.filter (endpoint state)).length

def supportCount (state : Nat) : Nat := (corners.filter (support state)).length

def edgeCount (state : Nat) : Nat :=
  ([(0,1), (0,2), (1,3), (2,3)].filter fun pair =>
    endpoint state pair.1 && endpoint state pair.2).length

def feasible (state : Nat) : Bool :=
  corners.any (endpoint state) && corners.all (fun vertex =>
    (!endpoint state vertex || corners.any (fun other =>
      adjacent vertex other && occupied state other)) &&
    (!support state vertex || (corners.filter (fun other =>
      adjacent vertex other && occupied state other)).length == 1))

def doubledWeight (endpoints edges supports full : Int) : Int :=
  3*endpoints-4*edges-2*supports+4*full

def localWeight (state : Nat) : Int :=
  doubledWeight (Int.ofNat (endpointCount state)) (Int.ofNat (edgeCount state))
    (Int.ofNat (supportCount state)) (if endpointCount state == 4 then 1 else 0)

def tableHolds (state : Nat) : Prop :=
  (endpointCount state = 1 ∧ supportCount state = 1 ∧ localWeight state = 1) ∨
  (endpointCount state = 1 ∧ supportCount state = 2 ∧ localWeight state = -1) ∨
  (endpointCount state = 2 ∧ supportCount state = 0 ∧ localWeight state = 2) ∨
  (endpointCount state = 2 ∧ supportCount state = 1 ∧ localWeight state = 0) ∨
  (endpointCount state = 3 ∧ supportCount state = 0 ∧ localWeight state = 1) ∨
  (endpointCount state = 4 ∧ supportCount state = 0 ∧ localWeight state = 0)

instance (state : Nat) : Decidable (tableHolds state) := by
  unfold tableHolds
  infer_instance

theorem complete_local_table (state : Fin 81) :
    feasible state.val = true → tableHolds state.val := by
  have checked : ∀ code : Fin 81, feasible code.val = true → tableHolds code.val := by
    decide
  exact checked state

theorem local_negative_iff (state : Fin 81) (hfeasible : feasible state.val = true) :
    localWeight state.val < 0 ↔ endpointCount state.val = 1 ∧ supportCount state.val = 2 := by
  have htable := complete_local_table state hfeasible
  rcases htable with hcase | hcase | hcase | hcase | hcase | hcase <;>
    rcases hcase with ⟨hendpoints, hsupports, hweight⟩ <;> omega

theorem exact_event_cancellation
    (endpoints edges owners supportIncidences retained full originalFull mixed events : Int)
    (hevents : events = 2*(edges-endpoints+owners-originalFull)-
      (supportIncidences-retained))
    (hfull : full = originalFull+mixed) :
    4*owners-endpoints-2*supportIncidences+4*mixed-2*events =
      doubledWeight endpoints edges retained full := by
  unfold doubledWeight
  omega

theorem canonical_u_charge (halfWidth depthSum charge : Int)
    (hcharge : charge = (2*halfWidth-1+depthSum)+(4+depthSum)-
      2*(halfWidth+1+depthSum)) : charge = 1 := by omega

theorem wall_u_charge (halfWidth depthSum charge : Int)
    (hcharge : charge = (2*halfWidth-1+depthSum)+depthSum-
      2*(halfWidth+depthSum)) : charge = -1 := by omega

theorem row_shift_u_charge (width depthSum charge : Int)
    (hcharge : charge = (width-1+depthSum)+(2+depthSum)-
      2*(width+depthSum)) : charge = 1-width := by omega

theorem double_shift_u_charge (width depthSum charge : Int)
    (hcharge : charge = (width-1+depthSum)+(depthSum-2)-
      2*(width-2+depthSum)) : charge = 1-width := by omega

theorem long_wall_baseline :
    doubledWeight 3 2 2 0+doubledWeight 1 0 1 0 = -2 := by decide

theorem coincident_wall_baseline : doubledWeight 2 1 2 0 = -2 := by decide

theorem chamber_gate_baseline : 2*doubledWeight 3 2 2 0 = -6 := by decide

theorem regional_exact_identity
    (delta positive finalWeight oldWeight negativeU residual : Int)
    (hidentity : 2*delta = 4*positive+finalWeight-oldWeight)
    (hpartition : finalWeight = -negativeU+residual) :
    2*delta = 4*positive-negativeU+residual-oldWeight := by omega

theorem complete_exterior_bound
    (delta positive negativeU residual : Int)
    (hcount : negativeU ≤ 2*positive) (hresidual : 0 ≤ residual)
    (hidentity : 2*delta = 4+4*positive-negativeU+residual) :
    2+positive ≤ delta := by omega

theorem complete_cut_bound
    (delta positive oldTerminals oldWeight negativeU residual : Int)
    (hcount : negativeU ≤ 2*positive+oldTerminals) (hresidual : 0 ≤ residual)
    (hidentity : 2*delta = 4*positive-negativeU+residual-oldWeight) :
    2*positive-oldTerminals-oldWeight ≤ 2*delta := by omega

theorem complete_chamber_bound
    (delta positive negativeU residual : Int)
    (hcount : negativeU ≤ 2*positive) (hresidual : 0 ≤ residual)
    (hidentity : 2*delta = 6+4*positive-negativeU+residual) :
    3+positive ≤ delta := by omega

theorem complete_global_bound
    (potential gaps chamberPositive exteriorPositive chamberDelta exteriorDelta : Int)
    (hwhole : potential = -gaps+chamberDelta+exteriorDelta)
    (hchamber : 3*gaps+chamberPositive ≤ chamberDelta)
    (hexterior : 2+exteriorPositive ≤ exteriorDelta) :
    2*gaps+2+chamberPositive+exteriorPositive ≤ potential := by omega

theorem width_six_complete_bound
    (potential gaps downward positive exterior : Int)
    (hwhole : potential = 4*gaps+2*downward+exterior)
    (hexterior : 2+positive ≤ exterior) :
    4*gaps+2*downward+2+positive ≤ potential := by omega

theorem subfive_two_positive_saturation
    (delta negativeU residual : Int)
    (hcount : negativeU ≤ 4) (hresidual : 0 ≤ residual)
    (hidentity : 2*delta = 12-negativeU+residual) (hbelow : delta < 5) :
    delta = 4 ∧ negativeU = 4 ∧ residual = 0 := by omega

#print axioms corners
#print axioms adjacent
#print axioms endpoint
#print axioms support
#print axioms occupied
#print axioms endpointCount
#print axioms supportCount
#print axioms edgeCount
#print axioms feasible
#print axioms doubledWeight
#print axioms localWeight
#print axioms tableHolds
#print axioms instDecidableTableHolds
#print axioms complete_local_table
#print axioms local_negative_iff
#print axioms exact_event_cancellation
#print axioms canonical_u_charge
#print axioms wall_u_charge
#print axioms row_shift_u_charge
#print axioms double_shift_u_charge
#print axioms long_wall_baseline
#print axioms coincident_wall_baseline
#print axioms chamber_gate_baseline
#print axioms regional_exact_identity
#print axioms complete_exterior_bound
#print axioms complete_cut_bound
#print axioms complete_chamber_bound
#print axioms complete_global_bound
#print axioms width_six_complete_bound
#print axioms subfive_two_positive_saturation

end SubQuorum.LocalizedExteriorBudget
