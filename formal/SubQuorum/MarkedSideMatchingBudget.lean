import Std

set_option autoImplicit false

namespace SubQuorum.MarkedSideMatchingBudget

theorem phase_mark_capacity (phase01 phase10 phase11 marked : Nat)
    (hslots : marked ≤ 2*phase01+2*phase10+4*phase11) :
    marked ≤ 4*(phase01+phase10+phase11) := by omega

theorem negative_matching_pays_marked_sides (negativeSources marked negativeMatching : Nat)
    (hslots : marked ≤ 4*negativeSources)
    (hsize : 9*negativeSources ≤ negativeMatching) :
    9*marked ≤ 4*negativeMatching := by omega

theorem negative_matching_covers_marks (marked negativeMatching : Nat)
    (hbudget : 9*marked ≤ 4*negativeMatching) :
    marked ≤ negativeMatching := by omega

theorem combined_marked_matching_budget
    (positive exceptional marked positiveMatching negativeMatching matching : Nat)
    (hpositive : 9*positive+4*exceptional ≤ positiveMatching)
    (hnegative : 9*marked ≤ 4*negativeMatching)
    (hpartition : positiveMatching+negativeMatching ≤ matching) :
    36*positive+16*exceptional+9*marked ≤ 4*matching := by omega

theorem earlier_combined_budget
    (positive exceptional marked matching : Nat)
    (hbudget : 36*positive+16*exceptional+9*marked ≤ 4*matching) :
    9*positive+4*exceptional+marked ≤ matching := by omega

theorem expanded_marked_matching_budget
    (positive exceptional marked reserve matching : Nat) (margin : Int)
    (hbudget : 36*positive+16*exceptional+9*marked ≤ 4*matching)
    (hledger : margin = (positive : Int)+reserve-marked) :
    (45*positive+16*exceptional+9*reserve : Int)-9*margin ≤ 4*matching := by omega

theorem universal_marked_scaled_margin
    (positive exceptional single marked reserve matching : Nat) (margin slack : Int)
    (hpartition : exceptional+single ≤ positive)
    (hbudget : 36*positive+16*exceptional+9*marked ≤ 4*matching)
    (hledger : margin = (positive : Int)+reserve-marked)
    (hcompensation : -(exceptional : Int)-(single : Int)/2 ≤ margin)
    (hslack : margin ≤ slack) :
    0 ≤ 35*slack+2*matching := by omega

theorem nonexceptional_marked_scaled_margin
    (positive single marked reserve matching : Nat) (margin slack : Int)
    (hpartition : single ≤ positive)
    (hbudget : 36*positive+9*marked ≤ 4*matching)
    (hledger : margin = (positive : Int)+reserve-marked)
    (hactivation : single ≤ 2*reserve)
    (hcompensation : -((single : Int)/2) ≤ margin)
    (hslack : margin ≤ slack) :
    0 ≤ 27*slack+matching := by omega

theorem universal_marked_boundary_coefficient (area selected matching : Nat) (slack : Int)
    (hledger : 2*slack = (area : Int)-2*selected-2*matching)
    (hscaled : 0 ≤ 35*slack+2*matching) :
    70*selected+66*matching ≤ 35*area := by omega

theorem nonexceptional_marked_boundary_coefficient (area selected matching : Nat) (slack : Int)
    (hledger : 2*slack = (area : Int)-2*selected-2*matching)
    (hscaled : 0 ≤ 27*slack+matching) :
    54*selected+52*matching ≤ 27*area := by omega

end SubQuorum.MarkedSideMatchingBudget
