import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenEFarFrontier

theorem far_column_bound (offset width breadth : Int)
    (hwidth : width+20 ≤ breadth) : offset+width+14-breadth ≤ offset-6 := by omega

theorem first_contact_upper (column previousOffset : Int)
    (hcolumn : column % 2 = 0) (hoffset : previousOffset % 2 = 0)
    (hfirst : column < previousOffset-4) : column ≤ previousOffset-6 := by omega

theorem terminal_even (anchor far : Int)
    (hanchor : anchor % 2 = 1) (hfar : far % 2 = 0) :
    (anchor-11+far) % 2 = 0 := by omega

theorem frontier_exhaustive (column offset : Int)
    (hcolumn : column % 2 = 0) (hoffset : offset % 2 = 0)
    (hlower : offset-4 ≤ column) :
    column = offset-4 ∨ column = offset-2 ∨ column = offset ∨ offset+2 ≤ column := by omega

theorem X_or_Z_collision_bound (anchor terminal : Int)
    (hanchor : anchor % 2 = 1) (hterminal : terminal % 2 = 0) :
    (terminal < anchor-2 ↔ terminal ≤ anchor-3) := by omega

theorem P_far_collision_bound (anchor terminal : Int)
    (hanchor : anchor % 2 = 1) (hterminal : terminal % 2 = 0) :
    (terminal < anchor-3 ↔ terminal ≤ anchor-5) := by omega

theorem P_bar_collision_bound (anchor terminal : Int)
    (hanchor : anchor % 2 = 1) (hterminal : terminal % 2 = 0) :
    (terminal < anchor-8 ↔ terminal ≤ anchor-9) := by omega

theorem P_far_activation_exhaustive (anchor terminal : Int)
    (hanchor : anchor % 2 = 1) (hterminal : terminal % 2 = 0)
    (hlower : anchor-7 ≤ terminal) (hupper : terminal ≤ anchor-5) :
    terminal = anchor-7 ∨ terminal = anchor-5 := by omega

theorem later_block_tile_separation (anchor nextAnchor terminal : Int)
    (hgap : anchor+18 ≤ nextAnchor) (hstop : terminal ≤ anchor-3) :
    terminal/2 < (nextAnchor-8)/2 := by omega

theorem entry_tile_zero : 2*(0 : Int)-0 = 0 := by omega

theorem Z_terminal_receipt : 2*(1 : Int)-3 = -1 := by omega

theorem P_far_receipt (overlap : Int) : 2*overlap-(2*overlap+2) = -2 := by omega

theorem P_bar_terminal_receipt : 2*(0 : Int)-1 = -1 := by omega

def gain (deduction : Int) : Int := 1-deduction

theorem old_frontier_identity (extraFull deduction : Int) :
    1+2*(4+extraFull)-(8+2*extraFull+deduction) = gain deduction := by
  unfold gain
  omega

theorem old_frontier_lower (deduction : Int) (hlower : 0 ≤ deduction)
    (hupper : deduction ≤ 2) : -1 ≤ gain deduction := by unfold gain; omega

theorem sharp_iff (deduction : Int) : gain deduction = -1 ↔ deduction = 2 := by
  unfold gain
  omega

theorem witness_coordinates :
    (31 : Int)+18 = 49 ∧ 49+18 = 67 ∧ 49-11+22 = 60 ∧ 67-7 = 60 ∧
    1+1-50 = -48 := by omega

end SubQuorum.SecondaryTenEFarFrontier
