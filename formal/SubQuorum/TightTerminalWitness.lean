import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.TightTerminalWitness

theorem tight_clearance_rows (positiveHeight incomingHeight : Int)
    (hpositive : 6 ≤ positiveHeight)
    (htight : incomingHeight = positiveHeight-2) :
    incomingHeight+1 = positiveHeight-1 ∧
    incomingHeight+2 = positiveHeight ∧
    incomingHeight+3 = positiveHeight+1 ∧ 4 ≤ incomingHeight := by omega

theorem stronger_shared_margin
    (unmarked reserve zero single twice middle remaining margin : Int)
    (hreserve : 2*zero+single+2*twice+middle ≤ 2*reserve)
    (hmargin : margin = unmarked+reserve-zero-single-twice-middle-remaining) :
    unmarked-remaining-(single+middle)/2 ≤ margin := by omega

theorem expanded_low_cost_coefficient
    (positive single middle marked reserve matching margin slack : Int)
    (hpartition : single+middle ≤ positive)
    (hbudget : 36*positive+9*marked ≤ 4*matching)
    (hmargin : margin = positive+reserve-marked)
    (hactivationAndWitness : single+middle ≤ 2*reserve)
    (hcompensation : -((single+middle)/2) ≤ margin)
    (hslack : margin ≤ slack) : 0 ≤ 27*slack+matching := by omega

#print axioms tight_clearance_rows
#print axioms stronger_shared_margin
#print axioms expanded_low_cost_coefficient

end SubQuorum.TightTerminalWitness
