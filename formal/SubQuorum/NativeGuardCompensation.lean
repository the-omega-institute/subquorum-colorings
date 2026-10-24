import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.NativeGuardCompensation

def occupied (label : Fin 3) : Nat := if label = 0 then 0 else 1
def selected (label : Fin 3) : Nat := if label = 1 then 1 else 0

theorem foreign_upper_corner_excluded (middle exterior : Fin 3)
    (hcycle : middle = 2 → exterior ≠ 2)
    (hselected : exterior = 1 → occupied middle + 1 ≤ 1)
    (hdegree : middle = 2 → 3 ≤ 2 + occupied exterior) : middle ≠ 2 := by
  have checked : ∀ middle exterior : Fin 3,
      (middle = 2 → exterior ≠ 2) →
      (exterior = 1 → occupied middle + 1 ≤ 1) →
      (middle = 2 → 3 ≤ 2 + occupied exterior) → middle ≠ 2 := by decide
  exact checked middle exterior hcycle hselected hdegree

theorem native_guard_donor (upperRight lowerLeft lowerRight : Fin 3)
    (hupper : upperRight ≠ 2)
    (hguard : occupied lowerLeft + 1 ≤ 1)
    (hselected : upperRight = 1 → occupied lowerRight + 1 ≤ 1)
    (hdegree : lowerRight = 2 → 3 ≤ occupied upperRight + occupied lowerLeft + 2) :
    lowerLeft = 0 ∧ lowerRight ≠ 2 ∧ selected upperRight + selected lowerRight ≤ 1 := by
  have checked : ∀ upperRight lowerLeft lowerRight : Fin 3,
      upperRight ≠ 2 → occupied lowerLeft + 1 ≤ 1 →
      (upperRight = 1 → occupied lowerRight + 1 ≤ 1) →
      (lowerRight = 2 → 3 ≤ occupied upperRight + occupied lowerLeft + 2) →
      lowerLeft = 0 ∧ lowerRight ≠ 2 ∧ selected upperRight + selected lowerRight ≤ 1 := by decide
  exact checked upperRight lowerLeft lowerRight hupper hguard hselected hdegree

theorem opposite_native_runs_impossible (occupiedNeighbors : Nat)
    (hruns : 2 ≤ occupiedNeighbors) (hfeasible : occupiedNeighbors ≤ 1) : False := by omega

theorem original_tile_payment
    (areaHalf objective originalDeficit signedCharge positiveCharge
      positivePieces assignedCapacity : Int)
    (hledger : areaHalf - objective = originalDeficit - signedCharge)
    (hsigned : signedCharge ≤ positiveCharge)
    (hunit : positiveCharge ≤ positivePieces)
    (hassignment : positivePieces ≤ assignedCapacity)
    (hphysical : assignedCapacity ≤ originalDeficit) : objective ≤ areaHalf := by omega

def elbowEndpoint (width height row column : Int) : Prop :=
  ((row = 0 ∨ row = 1) ∧ 0 ≤ column ∧ column < width) ∨
  (2 ≤ row ∧ row < height ∧ (column = width - 2 ∨ column = width - 1)) ∨
  (row = 2 ∧ column = 0) ∨ (row = height ∧ column = width - 1)

def elbowSelected (width height row column : Int) : Prop :=
  (row = 0 ∧ (column = -1 ∨ column = width)) ∨
  (row = 2 ∧ column = -1) ∨ (row = 3 ∧ column = 0) ∨
  (row = height + 1 ∧ column = width - 1) ∨
  (2 ≤ row ∧ row ≤ height ∧ row % 2 = 0 ∧ column = width) ∨
  (3 ≤ row ∧ row < height ∧ row % 2 = 1 ∧ column = width - 3)

theorem completed_outer_donor_no_endpoints (width height : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height) :
    ¬ elbowEndpoint width height 2 1 ∧ ¬ elbowEndpoint width height 2 2 ∧
    ¬ elbowEndpoint width height 3 1 ∧ ¬ elbowEndpoint width height 3 2 := by
  unfold elbowEndpoint
  omega

theorem completed_outer_donor_no_selections (width height : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height) :
    ¬ elbowSelected width height 2 1 ∧ ¬ elbowSelected width height 2 2 ∧
    ¬ elbowSelected width height 3 1 ∧ ¬ elbowSelected width height 3 2 := by
  unfold elbowSelected
  omega

theorem original_donor_has_foreign_endpoints (width height : Int)
    (hwidth : 6 ≤ width) :
    ¬ elbowEndpoint width height (-1) 1 ∧ ¬ elbowEndpoint width height (-1) 2 ∧
    elbowEndpoint width height 0 1 ∧ elbowEndpoint width height 0 2 := by
  unfold elbowEndpoint
  omega

theorem inner_receiver_charge (width height : Int) :
    (width + height - 1) + (height + 2) - 2 * (width + height) = 1 - width := by omega

theorem original_union_objective (outerWidth outerHeight innerWidth innerHeight : Int) :
    (outerWidth + outerHeight + innerWidth + innerHeight - 2) + (outerHeight + innerHeight + 6) =
      outerWidth + innerWidth + 2 * outerHeight + 2 * innerHeight + 4 := by omega

theorem obstruction_signed_charge (width outerCharge innerCharge wholeCharge : Int)
    (houter : outerCharge = 1) (hinner : innerCharge = 1 - width)
    (hadd : wholeCharge = outerCharge + innerCharge) : wholeCharge = 2 - width := by omega

theorem obstruction_preserves_target (width originalDeficit margin : Int)
    (hwidth : 6 ≤ width) (hdeficit : 0 ≤ originalDeficit)
    (hledger : margin = originalDeficit - (2 - width)) :
    margin = originalDeficit + width - 2 ∧ 4 ≤ margin := by omega

end SubQuorum.NativeGuardCompensation

#print axioms SubQuorum.NativeGuardCompensation.foreign_upper_corner_excluded
#print axioms SubQuorum.NativeGuardCompensation.native_guard_donor
#print axioms SubQuorum.NativeGuardCompensation.opposite_native_runs_impossible
#print axioms SubQuorum.NativeGuardCompensation.original_tile_payment
#print axioms SubQuorum.NativeGuardCompensation.completed_outer_donor_no_endpoints
#print axioms SubQuorum.NativeGuardCompensation.completed_outer_donor_no_selections
#print axioms SubQuorum.NativeGuardCompensation.original_donor_has_foreign_endpoints
#print axioms SubQuorum.NativeGuardCompensation.inner_receiver_charge
#print axioms SubQuorum.NativeGuardCompensation.original_union_objective
#print axioms SubQuorum.NativeGuardCompensation.obstruction_signed_charge
#print axioms SubQuorum.NativeGuardCompensation.obstruction_preserves_target
