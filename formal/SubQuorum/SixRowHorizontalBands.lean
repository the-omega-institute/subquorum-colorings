import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SixRowHorizontalBands

def rotorEndpoint (reflected : Bool) (top left row column : Int) : Prop :=
  (reflected = false ∧
    ((row = top ∧ column = left+1) ∨
     (row = top+1 ∧ left+1 ≤ column ∧ column ≤ left+3) ∨
     (row = top+2 ∧ left ≤ column ∧ column ≤ left+2) ∨
     (row = top+3 ∧ column = left+2))) ∨
  (reflected = true ∧
    ((row = top ∧ column = left+2) ∨
     (row = top+1 ∧ left ≤ column ∧ column ≤ left+2) ∨
     (row = top+2 ∧ left+1 ≤ column ∧ column ≤ left+3) ∨
     (row = top+3 ∧ column = left+1)))

def tipRow (reflected : Bool) (top : Int) : Int :=
  top + if reflected then 2 else 1

def sideSupportRow (upward : Bool) (row : Int) : Prop :=
  if upward then row = 0 ∨ row = 2 ∨ row = 4
  else row = 1 ∨ row = 3 ∨ row = 5

def forcedRow (reflected upward : Bool) (top : Int) : Int :=
  let tip := tipRow reflected top
  let targetParity : Int := if upward then 0 else 1
  let distance : Int := if tip % 2 = targetParity then 2 else 1
  if reflected then tip-distance else tip+distance

theorem right_tip_has_west_neighbor (reflected : Bool) (top left row : Int)
    (hpoint : rotorEndpoint reflected top left row (left+3)) :
    rotorEndpoint reflected top left row (left+2) := by
  cases reflected <;> simp [rotorEndpoint] at * <;> omega

theorem rightmost_column_has_only_tip (reflected : Bool) (top left row : Int)
    (hpoint : rotorEndpoint reflected top left row (left+3)) :
    row = tipRow reflected top := by
  cases reflected <;> simp [rotorEndpoint,tipRow] at * <;> omega

theorem tip_row_is_interior (reflected : Bool) (top : Int)
    (htop : 0 ≤ top) (hbottom : top+3 ≤ 5) :
    1 ≤ tipRow reflected top ∧ tipRow reflected top ≤ 4 := by
  cases reflected <;> simp [tipRow] <;> omega

theorem forced_row_is_unconsumed_H_support (reflected upward : Bool) (top left : Int)
    (htop : 0 ≤ top) (hbottom : top+3 ≤ 5) :
    sideSupportRow upward (forcedRow reflected upward top) ∧
    forcedRow reflected upward top ≠ tipRow reflected top ∧
    rotorEndpoint reflected top left (forcedRow reflected upward top) (left+2) ∧
    ¬ rotorEndpoint reflected top left (forcedRow reflected upward top) (left+3) := by
  cases reflected <;> cases upward <;>
    simp only [forcedRow,tipRow,Bool.false_eq_true,if_false,if_true] <;>
    split <;> simp_all [sideSupportRow,rotorEndpoint] <;> omega

theorem support_row_has_H_side_endpoint (upward : Bool) (row : Int)
    (hrow : sideSupportRow upward row) :
    (upward = true ∧ 0 ≤ row ∧ row ≤ 4) ∨
    (upward = false ∧ 1 ≤ row ∧ row ≤ 5) := by
  cases upward <;> simp [sideSupportRow] at * <;> omega

theorem west_neighbor_blocks_second_rotor (firstReflection secondReflection : Bool)
    (firstTop secondTop firstLeft row : Int)
    (hbulk : rotorEndpoint firstReflection firstTop firstLeft row (firstLeft+2))
    (hdisjoint : ∀ currentRow column,
      rotorEndpoint firstReflection firstTop firstLeft currentRow column →
      ¬ rotorEndpoint secondReflection secondTop firstLeft currentRow column) :
    ¬ rotorEndpoint secondReflection secondTop firstLeft row (firstLeft+3) := by
  intro hsecond
  exact hdisjoint row (firstLeft+2) hbulk
    (right_tip_has_west_neighbor secondReflection secondTop firstLeft row hsecond)

theorem simultaneous_budget_with_unused_odd_bars
    (aligned odd pairs contacts events horizontalMass potential : Int)
    (_hused : 2*pairs+contacts ≤ odd)
    (hevents : events ≤ 2*(odd-2*pairs-contacts))
    (hpotential : potential = aligned+5*odd-6*pairs-events+horizontalMass-3*contacts) :
    potential ≥ aligned+2*odd+horizontalMass+(odd-2*pairs-contacts) := by
  omega

theorem simultaneous_budget (aligned odd pairs contacts events horizontalMass potential : Int)
    (hused : 2*pairs+contacts ≤ odd)
    (hevents : events ≤ 2*(odd-2*pairs-contacts))
    (hpotential : potential = aligned+5*odd-6*pairs-events+horizontalMass-3*contacts) :
    potential ≥ aligned+2*odd+horizontalMass := by
  have hstrong := simultaneous_budget_with_unused_odd_bars aligned odd pairs contacts events
    horizontalMass potential hused hevents hpotential
  omega

theorem complete_sharp_block (width : Int) :
    16+(width-1)-3*2 = width+9 := by omega

theorem negative_batch_marginal (amount : Int) :
    amount*(6-1)-3*(2*amount) = -amount := by omega

end SubQuorum.SixRowHorizontalBands

#print axioms SubQuorum.SixRowHorizontalBands.rotorEndpoint
#print axioms SubQuorum.SixRowHorizontalBands.tipRow
#print axioms SubQuorum.SixRowHorizontalBands.sideSupportRow
#print axioms SubQuorum.SixRowHorizontalBands.forcedRow
#print axioms SubQuorum.SixRowHorizontalBands.right_tip_has_west_neighbor
#print axioms SubQuorum.SixRowHorizontalBands.rightmost_column_has_only_tip
#print axioms SubQuorum.SixRowHorizontalBands.tip_row_is_interior
#print axioms SubQuorum.SixRowHorizontalBands.forced_row_is_unconsumed_H_support
#print axioms SubQuorum.SixRowHorizontalBands.support_row_has_H_side_endpoint
#print axioms SubQuorum.SixRowHorizontalBands.west_neighbor_blocks_second_rotor
#print axioms SubQuorum.SixRowHorizontalBands.simultaneous_budget_with_unused_odd_bars
#print axioms SubQuorum.SixRowHorizontalBands.simultaneous_budget
#print axioms SubQuorum.SixRowHorizontalBands.complete_sharp_block
#print axioms SubQuorum.SixRowHorizontalBands.negative_batch_marginal
