import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.LowCostExceptionalDoubles

def compensatedDimensions (width left right : Int) : Prop :=
  width = 6 ∨
  ((width = 8 ∨ width = 10) ∧ (left = 4 ∨ left = 6) ∧ (right = 4 ∨ right = 6)) ∨
  (width = 8 ∧ ((left = 4 ∧ right = 8) ∨ (left = 8 ∧ right = 4)))

theorem left_corner_or_longitudinal_hits_blank (extent : Int) (hminimum : 6 ≤ extent) :
    2 ≤ (5 : Int) ∧ 5 ≤ extent := by omega

theorem left_transverse_height (height : Int)
    (hminimum : 4 ≤ height) (heven : height % 2 = 0)
    (hcollision : height+2 < 8) : height = 4 := by omega

theorem left_bar_covers_right_corner (breadth : Int) (hminimum : 6 ≤ breadth) :
    2 ≤ (2 : Int) ∧ 2 ≤ breadth+1 ∧ (6 : Int) = 6 := by omega

theorem left_owner_cannot_own_right_gate (column : Int) (hmaximum : column ≤ 6) :
    column ≠ 7 := by omega

theorem right_longitudinal_height (height : Int)
    (hminimum : 4 ≤ height) (heven : height % 2 = 0)
    (hblank : ¬(2 ≤ (9 : Int) ∧ 9 ≤ height+2)) : height = 4 ∨ height = 6 := by omega

theorem longitudinal_bars_intersect (leftBreadth rightBreadth height : Int)
    (hleft : 6 ≤ leftBreadth) (hright : 6 ≤ rightBreadth)
    (hheight : height = 4 ∨ height = 6) :
    2 ≤ height+1 ∧ height+1 ≤ leftBreadth+1 ∧
    8-rightBreadth ≤ (6 : Int) ∧ 6 ≤ (7 : Int) := by omega

theorem low_matching_dimensions_compensated (width left right matching : Int)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hwidthEven : width % 2 = 0) (hleftEven : left % 2 = 0)
    (hrightEven : right % 2 = 0)
    (hmatching : 2*matching = 2*width+left+right-2)
    (hsmall : matching ≤ 13) : compensatedDimensions width left right := by
  unfold compensatedDimensions
  omega

theorem exceptional_matching_at_least_fourteen (width left right matching : Int)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hwidthEven : width % 2 = 0) (hleftEven : left % 2 = 0)
    (hrightEven : right % 2 = 0)
    (hmatching : 2*matching = 2*width+left+right-2)
    (hexceptional : ¬compensatedDimensions width left right) : 14 ≤ matching := by
  have hnotSmall : ¬matching ≤ 13 := by
    intro hbound
    exact hexceptional (low_matching_dimensions_compensated width left right matching
      hwidth hleft hright hwidthEven hleftEven hrightEven hmatching hbound)
  omega

theorem extended_two_slot_count (reserve activated boundary zero single twice : Int)
    (hreserve : activated+boundary ≤ 2*reserve)
    (hactivation : single+2*twice ≤ activated)
    (hboundary : 2*zero ≤ boundary) :
    2*zero+single+2*twice ≤ 2*reserve := by omega

theorem extended_compensation_margin
    (unmarked reserve zero single twice exceptional margin : Int)
    (hreserve : 2*zero+single+2*twice ≤ 2*reserve)
    (hmargin : margin = unmarked+reserve-zero-single-twice-exceptional) :
    unmarked-exceptional-single/2 ≤ margin := by omega

theorem improved_matching_budget
    (positive exceptional marked positiveMatching negativeMatching matching : Int)
    (hpositive : 9*positive+5*exceptional ≤ positiveMatching)
    (hnegative : 9*marked ≤ 4*negativeMatching)
    (hpartition : positiveMatching+negativeMatching ≤ matching) :
    36*positive+20*exceptional+9*marked ≤ 4*matching := by omega

theorem improved_scaled_margin
    (positive exceptional single marked reserve matching margin slack : Int)
    (hsingle : 0 ≤ single) (hreserve : 0 ≤ reserve)
    (hpartition : exceptional+single ≤ positive)
    (hbudget : 36*positive+20*exceptional+9*marked ≤ 4*matching)
    (hmargin : margin = positive+reserve-marked)
    (hcompensation : -exceptional-single/2 ≤ margin)
    (hslack : margin ≤ slack) : 0 ≤ 37*slack+2*matching := by omega

theorem improved_boundary_coefficient (area selected matching slack : Int)
    (harea : 2*slack = area-2*selected-2*matching)
    (hscaled : 0 ≤ 37*slack+2*matching) :
    74*selected+70*matching ≤ 37*area := by omega

theorem expanded_nonexceptional_scaled_margin
    (positive single marked reserve matching margin slack : Int)
    (hpartition : single ≤ positive)
    (hbudget : 36*positive+9*marked ≤ 4*matching)
    (hmargin : margin = positive+reserve-marked)
    (hactivation : single ≤ 2*reserve)
    (hcompensation : -(single/2) ≤ margin)
    (hslack : margin ≤ slack) : 0 ≤ 27*slack+matching := by omega

theorem abstract_budget_equality :
    (36 : Int)*2+20*2+9*4 = 4*37 ∧
    (2 : Int)+0-4 = -2 ∧ (37 : Int)*(-2)+2*37 = 0 := by omega

#print axioms compensatedDimensions
#print axioms left_corner_or_longitudinal_hits_blank
#print axioms left_transverse_height
#print axioms left_bar_covers_right_corner
#print axioms left_owner_cannot_own_right_gate
#print axioms right_longitudinal_height
#print axioms longitudinal_bars_intersect
#print axioms low_matching_dimensions_compensated
#print axioms exceptional_matching_at_least_fourteen
#print axioms extended_two_slot_count
#print axioms extended_compensation_margin
#print axioms improved_matching_budget
#print axioms improved_scaled_margin
#print axioms improved_boundary_coefficient
#print axioms expanded_nonexceptional_scaled_margin
#print axioms abstract_budget_equality

end SubQuorum.LowCostExceptionalDoubles
