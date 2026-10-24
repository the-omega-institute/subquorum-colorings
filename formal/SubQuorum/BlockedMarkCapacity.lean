import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.BlockedMarkCapacity

theorem width_ten_transverse_height (height : Int)
    (hminimum : 4 ≤ height) (heven : height % 2 = 0)
    (hcollision : height+2 < 10) : height = 4 ∨ height = 6 := by omega

theorem width_ten_bar_collision (breadth otherBreadth height otherHeight : Int)
    (hwidth : 6 ≤ breadth) (hotherWidth : 6 ≤ otherBreadth)
    (hheight : height = 4 ∨ height = 6)
    (hotherHeight : otherHeight = 4 ∨ otherHeight = 6) :
    2 ≤ otherHeight+1 ∧ otherHeight+1 ≤ breadth+1 ∧
    10-otherBreadth ≤ height+2 ∧ height+2 ≤ 9 := by omega

theorem y_longer_transverse_collision (breadth height : Int)
    (hwidth : 8 ≤ breadth) (hminimum : 4 ≤ height)
    (heven : height % 2 = 0) (hblank : height+2 < 11) :
    (height = 4 ∨ height = 6 ∨ height = 8) ∧
    2 ≤ height+1 ∧ height+1 ≤ breadth+1 := by omega

theorem x_longer_right_height (height : Int)
    (hminimum : 4 ≤ height) (heven : height % 2 = 0)
    (hblank : height+2 < 13) (hfirst : height ≠ 4) (hsecond : height ≠ 6) :
    height = 8 ∨ height = 10 := by omega

theorem adjacent_band_heights (left right : Int)
    (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hdisjoint : left+2 < 11-right) : left = 4 ∧ right = 4 := by omega

theorem blocked_global_capacity
    (marked phase01 phase10 phase11 blocked bad : Int)
    (hphase01 : 0 ≤ phase01) (hphase10 : 0 ≤ phase10)
    (hcapacity : marked+blocked ≤ 2*phase01+2*phase10+4*phase11)
    (hinjection : bad ≤ phase01+blocked) :
    marked+bad ≤ 4*(phase01+phase10+phase11) := by omega

theorem blocked_matching_budget (sources marked bad matching : Int)
    (hcapacity : marked+bad ≤ 4*sources)
    (hmatching : 9*sources ≤ matching) :
    9*marked+9*bad ≤ 4*matching := by omega

theorem new_reserve_margin
    (unmarked reserve zero single twice fourteen fifteen remaining bad margin : Int)
    (hunmarked : 0 ≤ unmarked)
    (hreserve : 2*zero+single+2*twice+fourteen+fifteen-bad ≤ 2*reserve)
    (hmargin : margin = unmarked+reserve-zero-single-twice-fourteen-fifteen-remaining) :
    2*(-margin) ≤ single+fourteen+fifteen+bad+2*remaining := by omega

theorem coefficient_scaled_margin
    (positive fourteen fifteen remaining single bad marked reserve matching margin slack : Int)
    (hsingle : 0 ≤ single) (hfourteen : 0 ≤ fourteen) (hfifteen : 0 ≤ fifteen)
    (hbadBound : bad ≤ fifteen) (hreserve : 0 ≤ reserve)
    (hpartition : single+fourteen+fifteen+remaining ≤ positive)
    (hbudget : 36*positive+20*fourteen+24*fifteen+28*remaining+9*marked+9*bad ≤ 4*matching)
    (hmargin : margin = positive+reserve-marked)
    (hcompensation : 2*(-margin) ≤ single+fourteen+fifteen+bad+2*remaining)
    (hslack : margin ≤ slack) : 0 ≤ 41*slack+2*matching := by omega

theorem coefficient (area selected matching slack : Int)
    (harea : 2*slack = area-2*selected-2*matching)
    (hscaled : 0 ≤ 41*slack+2*matching) :
    82*selected+78*matching ≤ 41*area := by omega

def twoSlotDimensions (width left right : Int) : Prop :=
  width = 6 ∨
  ((width = 8 ∨ width = 10) ∧ (left = 4 ∨ left = 6) ∧ (right = 4 ∨ right = 6)) ∨
  ((width = 8 ∨ width = 10) ∧ ((left = 4 ∧ right = 8) ∨ (left = 8 ∧ right = 4)))

def fourteenDimensions (width left right : Int) : Prop :=
  width = 8 ∧ ((left = 4 ∧ right = 10) ∨ (left = 10 ∧ right = 4) ∨
    (left = 6 ∧ right = 8) ∨ (left = 8 ∧ right = 6))

def fifteenDimensions (width left right : Int) : Prop :=
  (width = 8 ∧ ((left = 4 ∧ right = 12) ∨ (left = 12 ∧ right = 4) ∨
    (left = 6 ∧ right = 10) ∨ (left = 10 ∧ right = 6) ∨ (left = 8 ∧ right = 8))) ∨
  (width = 12 ∧ left = 4 ∧ right = 4)

set_option maxHeartbeats 2000000 in
theorem low_matching_dimensions (width left right matching : Int)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hwidthEven : width % 2 = 0) (hleftEven : left % 2 = 0)
    (hrightEven : right % 2 = 0)
    (hmatching : 2*matching = 2*width+left+right-2) (hsmall : matching ≤ 15) :
    twoSlotDimensions width left right ∨ fourteenDimensions width left right ∨
    fifteenDimensions width left right := by
  have hwidthCases : width = 6 ∨ width = 8 ∨ width = 10 ∨ width = 12 := by omega
  rcases hwidthCases with hwidthSix | hwidthEight | hwidthTen | hwidthTwelve
  · subst width
    exact Or.inl (Or.inl rfl)
  · subst width
    simp [twoSlotDimensions, fourteenDimensions, fifteenDimensions] <;> omega
  · subst width
    simp [twoSlotDimensions, fourteenDimensions, fifteenDimensions] <;> omega
  · subst width
    simp [twoSlotDimensions, fourteenDimensions, fifteenDimensions] <;> omega

theorem remaining_matching_at_least_sixteen (width left right matching : Int)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hwidthEven : width % 2 = 0) (hleftEven : left % 2 = 0)
    (hrightEven : right % 2 = 0)
    (hmatching : 2*matching = 2*width+left+right-2)
    (hnotTwo : ¬twoSlotDimensions width left right)
    (hnotFourteen : ¬fourteenDimensions width left right)
    (hnotFifteen : ¬fifteenDimensions width left right) : 16 ≤ matching := by
  have hnotSmall : ¬matching ≤ 15 := by
    intro hsmall
    rcases low_matching_dimensions width left right matching hwidth hleft hright
      hwidthEven hleftEven hrightEven hmatching hsmall with htwo | hfourteen | hfifteen
    · exact hnotTwo htwo
    · exact hnotFourteen hfourteen
    · exact hnotFifteen hfifteen
  omega

#print axioms width_ten_transverse_height
#print axioms width_ten_bar_collision
#print axioms y_longer_transverse_collision
#print axioms x_longer_right_height
#print axioms adjacent_band_heights
#print axioms blocked_global_capacity
#print axioms blocked_matching_budget
#print axioms new_reserve_margin
#print axioms coefficient_scaled_margin
#print axioms coefficient
#print axioms twoSlotDimensions
#print axioms fourteenDimensions
#print axioms fifteenDimensions
#print axioms low_matching_dimensions
#print axioms remaining_matching_at_least_sixteen

end SubQuorum.BlockedMarkCapacity
