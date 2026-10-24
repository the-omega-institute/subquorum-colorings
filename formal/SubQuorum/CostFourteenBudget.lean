import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.CostFourteenBudget

theorem negative_long_leg_size (width left right matching leftLong rightLong : Int)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hleftFlag : leftLong = 0 ∨ leftLong = 1)
    (hrightFlag : rightLong = 0 ∨ rightLong = 1)
    (hleftLong : leftLong = 1 → 8 ≤ left)
    (hrightLong : rightLong = 1 → 8 ≤ right)
    (hmatching : 2*matching = 2*width+left+right-2) :
    9+2*(leftLong+rightLong) ≤ matching := by omega

theorem negative_mark_and_long_leg_budget
    (sources marked longLegs matching : Int)
    (hmarks : marked ≤ 4*sources)
    (hmatching : 9*sources+2*longLegs ≤ matching) :
    9*marked+8*longLegs ≤ 4*matching := by omega

theorem conditional_shared_reserve_margin
    (unmarked reserve zero single twice middle remaining credit margin : Int)
    (hunmarked : 0 ≤ unmarked)
    (hreserve : 2*zero+single+2*twice+middle-credit ≤ 2*reserve)
    (hmargin : margin = unmarked+reserve-zero-single-twice-middle-remaining) :
    2*(-margin) ≤ 2*remaining+single+middle+credit := by omega

theorem conditional_matching_budget
    (positive middle remaining marked credit positiveMatching negativeMatching matching : Int)
    (hpositive : 9*positive+5*middle+6*remaining ≤ positiveMatching)
    (hnegative : 9*marked+8*credit ≤ 4*negativeMatching)
    (hpartition : positiveMatching+negativeMatching ≤ matching) :
    36*positive+20*middle+24*remaining+9*marked+8*credit ≤ 4*matching := by omega

theorem conditional_scaled_margin
    (positive middle remaining single credit marked reserve matching margin slack : Int)
    (hsingle : 0 ≤ single) (hreserve : 0 ≤ reserve)
    (hcredit : 0 ≤ credit) (hcreditBound : credit ≤ middle)
    (hpartition : single+middle+remaining ≤ positive)
    (hbudget : 36*positive+20*middle+24*remaining+9*marked+8*credit ≤ 4*matching)
    (hmargin : margin = positive+reserve-marked)
    (hcompensation : 2*(-margin) ≤ 2*remaining+single+middle+credit)
    (hslack : margin ≤ slack) : 0 ≤ 39*slack+2*matching := by omega

theorem conditional_coefficient (area selected matching slack : Int)
    (harea : 2*slack = area-2*selected-2*matching)
    (hscaled : 0 ≤ 39*slack+2*matching) :
    78*selected+74*matching ≤ 39*area := by omega

#print axioms negative_long_leg_size
#print axioms negative_mark_and_long_leg_budget
#print axioms conditional_shared_reserve_margin
#print axioms conditional_matching_budget
#print axioms conditional_scaled_margin
#print axioms conditional_coefficient

end SubQuorum.CostFourteenBudget
