import Std

set_option autoImplicit false

namespace SubQuorum.WidthSixGateInterleaving

abbrev Point := Int × Int

def uEndpoint (width nearHeight farHeight : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ nearHeight ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ farHeight ∧ point.2 = width)

def incomingEndpoint (width incident farHeight : Int) (point : Point) : Prop :=
  uEndpoint width incident farHeight (incident+2-point.1, point.2-1)

theorem forced_pair_profile (width incident farHeight : Int)
    (hwidth : 6 ≤ width) (hincident : 4 ≤ incident) (hfar : 4 ≤ farHeight) :
    incomingEndpoint width incident farHeight (incident+2,2) ∧
    incomingEndpoint width incident farHeight (incident+2,3) ∧
    ¬incomingEndpoint width incident farHeight (incident+3,2) ∧
    ¬incomingEndpoint width incident farHeight (incident+3,3) := by
  dsimp [incomingEndpoint, uEndpoint]
  omega

theorem original_corner_neighbor_mask (width nearHeight farHeight : Int)
    (hwidth : 6 ≤ width) (hnear : 4 ≤ nearHeight) (hfar : 4 ≤ farHeight) :
    uEndpoint width nearHeight farHeight (1,1) ∧
    uEndpoint width nearHeight farHeight (0,2) ∧
    ¬uEndpoint width nearHeight farHeight (-1,1) ∧
    ¬uEndpoint width nearHeight farHeight (0,0) ∧
    uEndpoint width nearHeight farHeight (0,1) ∧
    uEndpoint width nearHeight farHeight (0,3) ∧
    uEndpoint width nearHeight farHeight (1,2) ∧
    ¬uEndpoint width nearHeight farHeight (-1,2) := by
  dsimp [uEndpoint]
  omega

theorem horizontal_blank_corner_overlap (width nearHeight farHeight : Int)
    (hwidth : 6 ≤ width) :
    uEndpoint width nearHeight farHeight (3-3,6-1) := by
  dsimp [uEndpoint]
  omega

theorem vertical_blank_corner_overlap (width nearHeight farHeight : Int)
    (hnear : 4 ≤ nearHeight) :
    uEndpoint width nearHeight farHeight (6-3,2-1) := by
  dsimp [uEndpoint]
  omega

theorem width_six_distinct_tip_owner (width incident otherIncident : Int)
    (hwidth : 6 ≤ width) :
    ¬((otherIncident-incident = 0 ∧ width-1 = 3) ∨
      (width-1 = 0 ∧ otherIncident-incident = 3) ∨
      (otherIncident-incident = 0 ∧ width-1 = -3) ∨
      (width-1 = 0 ∧ otherIncident-incident = -3)) := by omega

theorem two_gate_stem_bar_separation (incident oppositeIncident : Int)
    (hincident : 4 ≤ incident)
    (hdisjoint : ¬(2 ≤ incident+1 ∧ incident+1 ≤ oppositeIncident+2)) :
    oppositeIncident ≤ incident-2 := by omega

theorem opposite_phase11_hits_long_leg (longHeight incident oppositeIncident : Int)
    (hopposite : 4 ≤ oppositeIncident)
    (hclearance : incident ≤ longHeight-2)
    (hseparation : oppositeIncident ≤ incident-2) :
    2 ≤ oppositeIncident+1 ∧ oppositeIncident+1 ≤ longHeight := by omega

theorem two_gate_interleaving_gap (longHeight shortHeight incident oppositeIncident : Int)
    (hclearance : incident ≤ longHeight-2)
    (hseparation : oppositeIncident ≤ incident-2)
    (hopposite : shortHeight ≤ oppositeIncident) :
    shortHeight+4 ≤ longHeight := by omega

theorem height_gap_four_is_tight (longHeight shortHeight incident oppositeIncident : Int)
    (hclearance : incident ≤ longHeight-2)
    (hseparation : oppositeIncident ≤ incident-2)
    (hopposite : shortHeight ≤ oppositeIncident)
    (hgap : longHeight ≤ shortHeight+4) :
    longHeight = shortHeight+4 ∧ incident = longHeight-2 ∧
      oppositeIncident = shortHeight := by omega

theorem height_gap_two_forces_both_activated (leftHeight rightHeight : Int)
    (leftActivated rightActivated : Prop)
    (hleft : ¬leftActivated → rightHeight+4 ≤ leftHeight)
    (hright : ¬rightActivated → leftHeight+4 ≤ rightHeight)
    (hgapLeft : leftHeight ≤ rightHeight+2)
    (hgapRight : rightHeight ≤ leftHeight+2) :
    leftActivated ∧ rightActivated := by
  constructor
  · apply Classical.byContradiction
    intro hnot
    have hgap := hleft hnot
    omega
  · apply Classical.byContradiction
    intro hnot
    have hgap := hright hnot
    omega

theorem tight_gate_reconstruction (positiveHeight incident : Int)
    (htight : incident = positiveHeight-2) : positiveHeight-incident = 2 := by omega

theorem common_slot_count {Slot : Type} (selected pool : List Slot)
    (zeroCount paid : Nat) (hnodup : selected.Nodup) (hsubset : selected ⊆ pool)
    (hlength : selected.length = 2*zeroCount+paid) :
    2*zeroCount+paid ≤ pool.length := by
  have hcount := hnodup.length_le_of_subset hsubset
  omega

theorem reserve_after_paid_singles (zeroCount single twice paid activation unused rotor
    boundary reserve : Nat)
    (hpaid : paid ≤ single) (hactivation : single+2*twice ≤ activation)
    (hboundary : 2*zeroCount+paid ≤ boundary)
    (hidentity : 2*reserve = activation+unused+rotor+boundary) :
    zeroCount+single+twice ≤ reserve+(single-paid)/2 := by omega

theorem joint_when_remaining_single_budget (zeroCount single twice paid exceptional unmarked
    activation unused rotor boundary reserve : Nat)
    (hpaid : paid ≤ single) (hactivation : single+2*twice ≤ activation)
    (hboundary : 2*zeroCount+paid ≤ boundary)
    (hidentity : 2*reserve = activation+unused+rotor+boundary)
    (hbudget : exceptional+(single-paid)/2 ≤ unmarked) :
    zeroCount+single+twice+exceptional ≤ unmarked+reserve := by
  have hreserve := reserve_after_paid_singles zeroCount single twice paid activation unused rotor
    boundary reserve hpaid hactivation hboundary hidentity
  omega

theorem all_single_doubles_paid (zeroCount single twice activation unused rotor boundary
    reserve : Nat)
    (hactivation : single+2*twice ≤ activation)
    (hboundary : 2*zeroCount+single ≤ boundary)
    (hidentity : 2*reserve = activation+unused+rotor+boundary) :
    zeroCount+single+twice ≤ reserve := by omega

theorem first_reserve_failure_has_no_paid_single (zeroCount single twice paid unmarked activation
    unused rotor boundary reserve : Nat)
    (hactivation : single+2*twice ≤ activation)
    (hboundary : 2*zeroCount+paid ≤ boundary)
    (hidentity : 2*reserve = activation+unused+rotor+boundary)
    (hreserve : reserve = 1) (hfailure : unmarked+reserve < zeroCount+single+twice) :
    unmarked = 0 ∧ zeroCount = 0 ∧ single = 2 ∧ twice = 0 ∧ paid = 0 ∧
      activation = 2 ∧ boundary = 0 ∧ unused = 0 ∧ rotor = 0 := by omega

theorem unpayable_even_height_gap (longHeight shortHeight : Int)
    (hlongEven : longHeight % 2 = 0) (hshortEven : shortHeight % 2 = 0)
    (hgap : shortHeight+4 ≤ longHeight) (hnotTight : longHeight ≠ shortHeight+4) :
    shortHeight+6 ≤ longHeight := by omega

end SubQuorum.WidthSixGateInterleaving
