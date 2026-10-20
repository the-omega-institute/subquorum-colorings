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

end SubQuorum.CompleteSourceCoefficient
