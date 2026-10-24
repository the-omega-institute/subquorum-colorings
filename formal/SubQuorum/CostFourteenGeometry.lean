import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.CostFourteenGeometry

theorem short_corner_hits_endpoint_or_support (height : Int)
    (hminimum : 4 ≤ height) (heven : height % 2 = 0) :
    (2 ≤ (7 : Int) ∧ 7 ≤ height+2) ∨ height+3 = 7 := by omega

theorem y_longitudinal_incident_height (height : Int)
    (hminimum : 4 ≤ height) (heven : height % 2 = 0)
    (hblank : ¬(2 ≤ (7 : Int) ∧ 7 ≤ height+2)) : height = 4 := by omega

theorem y_longitudinal_breadth (breadth : Int)
    (hminimum : 6 ≤ breadth) (heven : breadth % 2 = 0)
    (hcollision : ¬(2 ≤ (8 : Int) ∧ 8 ≤ breadth+1)) : breadth = 6 := by omega

theorem y_longitudinal_other_height (height : Int)
    (hminimum : 4 ≤ height) (heven : height % 2 = 0)
    (hcollision : ¬(6-height ≤ (1 : Int) ∧ 1 ≤ (6 : Int))) : height = 4 := by omega

theorem transverse_incident_height (height : Int)
    (hminimum : 4 ≤ height) (heven : height % 2 = 0)
    (hcollision : ¬(2 ≤ (8 : Int) ∧ 8 ≤ height+2)) : height = 4 := by omega

theorem y_right_longitudinal_collision (breadth height : Int)
    (hminimum : 6 ≤ breadth) (hheight : 4 ≤ height)
    (heven : height % 2 = 0)
    (hblank : ¬(2 ≤ (9 : Int) ∧ 9 ≤ height+2)) :
    (height = 4 ∨ height = 6) ∧ 2 ≤ height+1 ∧ height+1 ≤ breadth+1 := by omega

theorem x_right_longitudinal_height (height : Int)
    (hminimum : 4 ≤ height) (heven : height % 2 = 0)
    (hblank : ¬(2 ≤ (11 : Int) ∧ 11 ≤ height+2))
    (hfirstCollision : height ≠ 4) (hsecondCollision : height ≠ 6) :
    height = 8 := by omega

theorem x_left_breadth (breadth : Int)
    (hminimum : 6 ≤ breadth) (heven : breadth % 2 = 0)
    (hcollision : ¬(2 ≤ (9 : Int) ∧ 9 ≤ breadth+1)) : breadth = 6 := by omega

theorem all_right_bars_cover_column_six (breadth : Int) (hminimum : 6 ≤ breadth) :
    8-breadth ≤ (6 : Int) ∧ (6 : Int) ≤ 7 := by omega

#print axioms short_corner_hits_endpoint_or_support
#print axioms y_longitudinal_incident_height
#print axioms y_longitudinal_breadth
#print axioms y_longitudinal_other_height
#print axioms transverse_incident_height
#print axioms y_right_longitudinal_collision
#print axioms x_right_longitudinal_height
#print axioms x_left_breadth
#print axioms all_right_bars_cover_column_six

end SubQuorum.CostFourteenGeometry
