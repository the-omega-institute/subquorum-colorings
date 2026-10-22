import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.TerminalExteriorClosure

def capEndpoint (width depth last row column : Int) : Prop :=
  (row = last+depth+5 ∧ 1 ≤ column ∧ column ≤ width) ∨
  (row = last+depth+4 ∧ 2 ≤ column ∧ column ≤ width-1) ∨
  ((column = 1 ∨ column = width) ∧ last+5 ≤ row ∧ row ≤ last+depth+5)

theorem cap_support_has_unique_endpoint (width depth last row column : Int)
    (hwidth : 6 ≤ width) (_hdepth : 4 ≤ depth)
    (hlower : last+6 ≤ row) (hupper : row ≤ last+depth+2)
    (hcolumn : column = 2 ∨ column = width-1) :
    ¬ capEndpoint width depth last (row-1) column ∧
    ¬ capEndpoint width depth last (row+1) column ∧
    ((column = 2 ∧ capEndpoint width depth last row (column-1) ∧
       ¬ capEndpoint width depth last row (column+1)) ∨
     (column = width-1 ∧ capEndpoint width depth last row (column+1) ∧
       ¬ capEndpoint width depth last row (column-1))) := by
  rcases hcolumn with hcolumn | hcolumn <;> subst column <;>
    simp [capEndpoint] <;> omega

theorem downward_tip_orders (wall tip : Int)
    (hwall : wall % 2 = 0) (htip : tip % 2 = 1) :
    wall+1 ≤ tip ∨ tip+1 ≤ wall := by
  omega

theorem early_wall_support_within_stem (last depth wall : Int)
    (hlower : last+6 ≤ wall) (hearly : wall < last+depth+5) :
    last+5 ≤ wall+1 ∧ wall+1 ≤ last+depth+5 := by
  omega

theorem late_wall_covers_tip_support (last depth wall : Int)
    (hlate : last+depth+5 < wall) :
    last+depth+6 ≤ wall := by
  omega

theorem far_depth_is_equal (near far : Int)
    (hnear : near % 2 = 0) (hfar : far % 2 = 0)
    (hreach : near ≤ far) (hblocked : far < near+2) : far = near := by
  omega

theorem cap_depth_exists_iff (last leftWall rightWall : Int) :
    (∃ depth : Int, 4 ≤ depth ∧ depth % 2 = 0 ∧
      last+depth+6 ≤ leftWall ∧ last+depth+6 ≤ rightWall) ↔
    last+10 ≤ leftWall ∧ last+10 ≤ rightWall := by
  constructor
  · rintro ⟨depth, hlower, _hparity, hleft, hright⟩
    omega
  · rintro ⟨hleft, hright⟩
    exact ⟨4, by omega, by omega, by omega, by omega⟩

theorem cap_receipt_is_five (depth potential : Int)
    (hreceipt : potential = 1+2*(depth+2)-2*depth) : potential = 5 := by
  omega

theorem six_copies_force_nonnegative (value : Int)
    (hsix : 0 ≤ 5+6*value) : 0 ≤ value := by
  omega

theorem anchored_width_six_marginal (amount before after : Int)
    (hbefore : before = 5+16*amount) (hafter : after = 5+15*amount) :
    after-before = -amount := by
  omega

theorem anchored_totals_stay_positive (amount before after : Int)
    (hamount : 1 ≤ amount)
    (hbefore : before = 5+16*amount) (hafter : after = 5+15*amount) :
    0 < after ∧ after < before := by
  omega

#print axioms capEndpoint
#print axioms cap_support_has_unique_endpoint
#print axioms downward_tip_orders
#print axioms early_wall_support_within_stem
#print axioms late_wall_covers_tip_support
#print axioms far_depth_is_equal
#print axioms cap_depth_exists_iff
#print axioms cap_receipt_is_five
#print axioms six_copies_force_nonnegative
#print axioms anchored_width_six_marginal
#print axioms anchored_totals_stay_positive

end SubQuorum.TerminalExteriorClosure
