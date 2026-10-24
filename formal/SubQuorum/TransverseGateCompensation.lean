import Std

set_option autoImplicit false

namespace SubQuorum.TransverseGateCompensation

abbrev Point := Int × Int
abbrev Owner := Bool × Int × Int

def rotorP : List Point :=
  [(1,2),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(4,3)]

def move (owner : Owner) (point : Point) : Point :=
  (point.1+owner.2.1,(if owner.1 then -point.2 else point.2)+owner.2.2)

def rotorOwners (target : Point) (blocked : List Point) : List Owner :=
  (([false,true].flatMap fun mirror => rotorP.map fun endpoint =>
    (mirror,target.1-endpoint.1,
      target.2-(if mirror then -endpoint.2 else endpoint.2))).filter fun owner =>
        (rotorP.map (move owner)).all fun point => !blocked.contains point)

def gateBlockers (incident : Int) : List Point :=
  [(1,1),(2,1),(3,1),(4,1),(5,1)] ++
    ([2,3,4,5,6].map fun column => (2,column)) ++
    ([2,3,4,5,6].flatMap fun row => [(row,incident+1),(row,incident+2)])

def secondBlockers : List Point :=
  [(3,2),(3,3),(3,4),(3,5),(3,6),
   (4,5),(4,6),(5,5),(5,6),(6,5),(6,6),(4,1),(5,1)]

theorem height_four_gate_has_no_rotor_owner : rotorOwners (3,2) (gateBlockers 4) = [] := by decide

theorem height_six_gate_has_no_rotor_owner : rotorOwners (3,2) (gateBlockers 6) = [] := by decide

theorem second_support_has_no_rotor_owner : rotorOwners (4,3) secondBlockers = [] := by decide

def uEndpoint (width leftHeight rightHeight row column : Int) : Prop :=
  ((row = 0 ∨ row = 1) ∧ 1 ≤ column ∧ column ≤ width) ∨
    (2 ≤ row ∧ row ≤ leftHeight ∧ column = 1) ∨
    (2 ≤ row ∧ row ≤ rightHeight ∧ column = width)

def uSupport (width leftHeight rightHeight row column : Int) : Prop :=
  (row = 0 ∧ (column = 0 ∨ column = width+1)) ∨
    (row = leftHeight+1 ∧ column = 1) ∨
    (row = rightHeight+1 ∧ column = width) ∨
    (2 ≤ row ∧ row ≤ leftHeight ∧
      ((row%2 = 0 ∧ column = 0) ∨ (row%2 = 1 ∧ column = 2))) ∨
    (2 ≤ row ∧ row ≤ rightHeight ∧
      ((row%2 = 0 ∧ column = width+1) ∨ (row%2 = 1 ∧ column = width-1)))

theorem forced_pair_profile (width farHeight : Int)
    (hwidth : 6 ≤ width) (hfar : 4 ≤ farHeight) :
    uEndpoint width 4 farHeight 1 2 ∧ uEndpoint width 4 farHeight 1 3 ∧
      ¬uEndpoint width 4 farHeight 2 2 ∧ ¬uEndpoint width 4 farHeight 2 3 ∧
      ¬uSupport width 4 farHeight 1 2 ∧ ¬uSupport width 4 farHeight 1 3 ∧
      ¬uSupport width 4 farHeight 2 2 ∧ ¬uSupport width 4 farHeight 2 3 := by
  simp [uEndpoint, uSupport]
  omega

theorem forbidden_a4_support (width incident farHeight : Int)
    (hwidth : 6 ≤ width) (hincident : 4 ≤ incident) (heven : incident%2 = 0) :
    uSupport width incident farHeight (incident-1) 2 := by
  simp [uSupport]
  omega

theorem forbidden_a6_short_endpoint (width farHeight : Int) (hwidth : 6 ≤ width) :
    uEndpoint width 4 farHeight 1 2 := by
  simp [uEndpoint]
  omega

theorem forbidden_a6_long_support (width incident farHeight : Int)
    (hwidth : 6 ≤ width) (hincident : 6 ≤ incident) (heven : incident%2 = 0) :
    uSupport width incident farHeight (incident-3) 2 := by
  simp [uSupport]
  omega

theorem separate_tip_witnesses (width : Int) (hwidth : 6 ≤ width) :
    (4 : Int) ≠ width ∧ (5 : Int) < width := by omega

theorem combine_with_maximum (zeroCount paid chain exterior fresh unfilled boundary : Nat)
    (hold : 2*zeroCount+paid+chain+exterior ≤ unfilled+boundary)
    (hfresh : fresh+chain+exterior ≤ unfilled+boundary) :
    max (2*zeroCount+paid) fresh+chain+exterior ≤ unfilled+boundary := by omega

theorem effective_payment_identity (zeroCount paid fresh : Nat) :
    max (2*zeroCount+paid) fresh = 2*zeroCount+max paid (fresh-2*zeroCount) := by omega

theorem signed_maximum_margin (zeroCount single twice paid chain exterior fresh exceptional
    unmarked activation unfilled rotor boundary reserve : Nat) (margin : Int)
    (hactivation : single+2*twice ≤ activation)
    (hpool : max (2*zeroCount+paid) fresh+chain+exterior ≤ unfilled+boundary)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary)
    (hledger : (unmarked : Int)+reserve-(zeroCount+single+twice+exceptional) ≤ margin) :
    (unmarked : Int)-exceptional-
      ((single : Int)-chain-exterior-(max paid (fresh-2*zeroCount) : Nat))/2 ≤ margin := by
  have heffective := effective_payment_identity zeroCount paid fresh
  omega

theorem residual_excludes_transverse_payments (activation unfilled rotor boundary reserve chain fresh : Nat)
    (hactivation : activation = 2) (hreserve : reserve = 1)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary)
    (hpool : chain+fresh ≤ unfilled+boundary) : chain = 0 ∧ fresh = 0 := by omega

end SubQuorum.TransverseGateCompensation
