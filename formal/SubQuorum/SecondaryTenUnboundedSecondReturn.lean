import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenUnboundedSecondReturn

theorem positive_charge (halfWidth : Int) :
    (halfWidth+11)+(halfWidth+10)-2*(halfWidth+10) = 1 := by omega

theorem exact_second_marginal (halfWidth : Int) :
    1+2*(halfWidth+3)-(3*halfWidth+9) = -halfWidth-2 := by omega

theorem exact_group_increment (halfWidth : Int) :
    4+(-3)+(1+2*(halfWidth+3)-(3*halfWidth+9)) = -halfWidth-1 := by omega

theorem second_marginal_negative (halfWidth : Int) (hwidth : 6 ≤ halfWidth) :
    -halfWidth-2 ≤ -8 := by omega

theorem selected_increment_negative (halfWidth : Int) (hwidth : 6 ≤ halfWidth) :
    -halfWidth-1 ≤ -7 := by omega

theorem unbounded_selected_debit (bound : Int) (hbound : 0 ≤ bound) :
    ∃ halfWidth : Int, 6 ≤ halfWidth ∧ -halfWidth-1 < -bound := by
  refine ⟨bound+6, ?_, ?_⟩ <;> omega

theorem initial_band_tile (halfWidth : Int) :
    1+(halfWidth+2) = halfWidth+3 ∧
    2*halfWidth+6+(halfWidth+3) = 3*halfWidth+9 := by omega

theorem second_owner_bar_above_old (row : Int) (hrow : row ≤ 22) : row < 23 := by omega

end SubQuorum.SecondaryTenUnboundedSecondReturn
