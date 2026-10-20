import Std

set_option autoImplicit false

namespace SubQuorum.CompleteSourceCoefficient

theorem source_matching_minimum (width leftHeight rightHeight matching : Nat)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ leftHeight) (hright : 4 ≤ rightHeight)
    (hsize : 2*matching+2 = 2*width+leftHeight+rightHeight) :
    9 ≤ matching := by omega

theorem exceptional_matching_minimum (width leftHeight rightHeight matching : Nat)
    (hwidth : 8 ≤ width) (hleft : 4 ≤ leftHeight) (hright : 4 ≤ rightHeight)
    (hexceptional : 12 ≤ width ∨ 8 ≤ leftHeight ∨ 8 ≤ rightHeight)
    (hsize : 2*matching+2 = 2*width+leftHeight+rightHeight) :
    13 ≤ matching := by omega

theorem matching_pays_thirteen_losses (exceptional single matching : Nat)
    (hcost : 13*exceptional+9*single ≤ matching) :
    13*(exceptional+single/2) ≤ matching := by omega

theorem universal_scaled_margin (exceptional single matching : Nat) (slack : Int)
    (hcost : 13*exceptional+9*single ≤ matching)
    (hmargin : -(exceptional : Int)-(single : Int)/2 ≤ slack) :
    0 ≤ 13*slack+matching := by omega

theorem nonexceptional_scaled_margin (single matching : Nat) (slack : Int)
    (hcost : 9*single ≤ matching)
    (hmargin : -((single : Int)/2) ≤ slack) :
    0 ≤ 18*slack+matching := by omega

theorem universal_boundary_coefficient (area selected matching : Nat) (slack : Int)
    (hledger : 2*slack = (area : Int)-2*selected-2*matching)
    (hscaled : 0 ≤ 13*slack+matching) :
    26*selected+24*matching ≤ 13*area := by omega

theorem nonexceptional_boundary_coefficient (area selected matching : Nat) (slack : Int)
    (hledger : 2*slack = (area : Int)-2*selected-2*matching)
    (hscaled : 0 ≤ 18*slack+matching) :
    36*selected+34*matching ≤ 18*area := by omega

theorem negative_U_matching_covers_charge (width leftHeight rightHeight matching charge : Nat)
    (hleft : 4 ≤ leftHeight) (hright : 4 ≤ rightHeight)
    (hsize : 2*matching+2 = 2*width+leftHeight+rightHeight)
    (hcharge : charge ≤ width-1) (hwidth : 6 ≤ width) :
    charge+4 ≤ matching := by omega

theorem combined_source_matching_budget (positive exceptional matching negativeCharge : Nat)
    (hcost : 9*positive+4*exceptional+negativeCharge ≤ matching)
    (reserve : Nat) (margin : Int)
    (hledger : margin = (positive : Int)+reserve-negativeCharge) :
    (10*positive+4*exceptional+reserve : Int)-margin ≤ matching := by omega

theorem universal_charge_scaled_margin
    (positive exceptional single reserve matching negativeCharge : Nat) (margin slack : Int)
    (hpartition : exceptional+single ≤ positive)
    (hcost : 9*positive+4*exceptional+negativeCharge ≤ matching)
    (hledger : margin = (positive : Int)+reserve-negativeCharge)
    (hcompensation : -(exceptional : Int)-(single : Int)/2 ≤ margin)
    (hslack : margin ≤ slack) :
    0 ≤ 15*slack+matching := by omega

theorem nonexceptional_charge_scaled_margin
    (positive single reserve matching negativeCharge : Nat) (margin slack : Int)
    (hpartition : single ≤ positive)
    (hcost : 9*positive+negativeCharge ≤ matching)
    (hledger : margin = (positive : Int)+reserve-negativeCharge)
    (hactivation : single ≤ 2*reserve)
    (hcompensation : -((single : Int)/2) ≤ margin)
    (hslack : margin ≤ slack) :
    0 ≤ 22*slack+matching := by omega

theorem universal_charge_boundary_coefficient (area selected matching : Nat) (slack : Int)
    (hledger : 2*slack = (area : Int)-2*selected-2*matching)
    (hscaled : 0 ≤ 15*slack+matching) :
    30*selected+28*matching ≤ 15*area := by omega

theorem nonexceptional_charge_boundary_coefficient (area selected matching : Nat) (slack : Int)
    (hledger : 2*slack = (area : Int)-2*selected-2*matching)
    (hscaled : 0 ≤ 22*slack+matching) :
    44*selected+42*matching ≤ 22*area := by omega

end SubQuorum.CompleteSourceCoefficient
