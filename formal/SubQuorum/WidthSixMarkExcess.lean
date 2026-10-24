import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.WidthSixMarkExcess

def coreWitness (bar row column : Int) : Prop :=
  (row = bar+2 ∧ column = 2) ∨ (row = bar+4 ∧ column = 2) ∨
  (row = bar+2 ∧ column = 3) ∨ (row = bar+2 ∧ column = 5) ∨
  (row = bar+4 ∧ column = 5) ∨ (row = bar+2 ∧ column = 4)

def upwardWitness (bar row column : Int) : Prop :=
  coreWitness 0 (bar+9-row) column

def canonicalEndpoints (row column : Int) : Prop :=
  ((row = 0 ∨ row = 1) ∧ 1 ≤ column ∧ column ≤ 6) ∨
  (1 ≤ row ∧ row ≤ 4 ∧ (column = 1 ∨ column = 6))

def canonicalSupports (row column : Int) : Prop :=
  (row = 0 ∧ (column = 0 ∨ column = 7)) ∨
  (row = 5 ∧ (column = 1 ∨ column = 6)) ∨
  ((row = 2 ∨ row = 4) ∧ (column = 0 ∨ column = 7)) ∨
  (row = 3 ∧ (column = 2 ∨ column = 5))

theorem core_witness_bounds (bar row column : Int)
    (hwitness : coreWitness bar row column) :
    (row = bar+2 ∨ row = bar+4) ∧ 2 ≤ column ∧ column ≤ 5 := by
  unfold coreWitness at hwitness
  omega

theorem core_witness_originally_blank (row column : Int)
    (hwitness : coreWitness 0 row column) :
    ¬canonicalEndpoints row column ∧ ¬canonicalSupports row column := by
  unfold coreWitness at hwitness
  unfold canonicalEndpoints canonicalSupports
  omega

theorem earlier_B_witness_below_new_source (bar row column : Int)
    (hwitness : coreWitness bar row column) : ¬(bar+5 ≤ row) := by
  have hbounds := core_witness_bounds bar row column hwitness
  omega

theorem witness_not_old_wall (bar row column : Int)
    (hwitness : coreWitness bar row column) : column ≠ 0 ∧ column ≠ 7 := by
  have hbounds := core_witness_bounds bar row column hwitness
  omega

theorem earlier_B_witness_in_chamber (bar row column : Int)
    (hwitness : coreWitness bar row column) :
    bar+2 ≤ row ∧ row ≤ bar+9 ∧ 1 ≤ column ∧ column ≤ 6 := by
  have hbounds := core_witness_bounds bar row column hwitness
  omega

theorem upward_witness_bounds (bar row column : Int)
    (hwitness : upwardWitness bar row column) :
    (row = bar+5 ∨ row = bar+7) ∧ 2 ≤ column ∧ column ≤ 5 := by
  unfold upwardWitness at hwitness
  have hbounds := core_witness_bounds 0 (bar+9-row) column hwitness
  omega

theorem upward_witness_not_old_rows (bar row column : Int)
    (hwitness : upwardWitness bar row column) : ¬(row ≤ bar+4 ∨ bar+10 ≤ row) := by
  have hbounds := upward_witness_bounds bar row column hwitness
  omega

theorem upward_witness_not_old_wall (bar row column : Int)
    (hwitness : upwardWitness bar row column) : column ≠ 0 ∧ column ≠ 7 := by
  have hbounds := upward_witness_bounds bar row column hwitness
  omega

theorem exact_mark_excess_slack
    (slack potential marked gaps downward exteriorPositive lastMarks
      unmarked singleMarked doubleMarked : Int)
    (hledger : potential-marked ≤ slack)
    (hpotential : 4*gaps+2*downward+2+exteriorPositive ≤ potential)
    (hpositive : exteriorPositive = unmarked+singleMarked+doubleMarked)
    (hmarked : marked = lastMarks+singleMarked+2*doubleMarked) :
    4*gaps+2*downward+2-lastMarks+unmarked-doubleMarked ≤ slack := by
  omega

theorem sufficient_exterior_mark_excess
    (slack potential marked gaps downward exteriorPositive lastMarks
      unmarked singleMarked doubleMarked : Int)
    (hledger : potential-marked ≤ slack)
    (hpotential : 4*gaps+2*downward+2+exteriorPositive ≤ potential)
    (hpositive : exteriorPositive = unmarked+singleMarked+doubleMarked)
    (hmarked : marked = lastMarks+singleMarked+2*doubleMarked)
    (hlast : lastMarks ≤ 2)
    (hexcess : doubleMarked ≤ unmarked+4*gaps+2*downward) : 0 ≤ slack := by
  have hslack := exact_mark_excess_slack slack potential marked gaps downward exteriorPositive
    lastMarks unmarked singleMarked doubleMarked hledger hpotential hpositive hmarked
  omega

theorem previous_density_implies_mark_excess
    (gaps downward exteriorPositive unmarked singleMarked doubleMarked : Int)
    (hdownward : 0 ≤ downward ∧ downward ≤ gaps)
    (hunmarked : 0 ≤ unmarked) (hsingle : 0 ≤ singleMarked)
    (hpositive : exteriorPositive = unmarked+singleMarked+doubleMarked)
    (hprevious : exteriorPositive ≤ 4*downward) :
    doubleMarked ≤ unmarked+4*gaps+2*downward := by omega

theorem new_density_implies_mark_excess
    (gaps downward exteriorPositive unmarked singleMarked doubleMarked : Int)
    (hunmarked : 0 ≤ unmarked) (hsingle : 0 ≤ singleMarked)
    (hpositive : exteriorPositive = unmarked+singleMarked+doubleMarked)
    (hdensity : exteriorPositive ≤ 4*gaps+2*downward) :
    doubleMarked ≤ unmarked+4*gaps+2*downward := by omega

theorem no_double_marks_suffices
    (gaps downward unmarked doubleMarked : Int)
    (hgaps : 0 ≤ gaps) (hdownward : 0 ≤ downward)
    (hunmarked : 0 ≤ unmarked) (hdouble : doubleMarked = 0) :
    doubleMarked ≤ unmarked+4*gaps+2*downward := by omega

#print axioms coreWitness
#print axioms upwardWitness
#print axioms canonicalEndpoints
#print axioms canonicalSupports
#print axioms core_witness_bounds
#print axioms core_witness_originally_blank
#print axioms earlier_B_witness_below_new_source
#print axioms witness_not_old_wall
#print axioms earlier_B_witness_in_chamber
#print axioms upward_witness_bounds
#print axioms upward_witness_not_old_rows
#print axioms upward_witness_not_old_wall
#print axioms exact_mark_excess_slack
#print axioms sufficient_exterior_mark_excess
#print axioms previous_density_implies_mark_excess
#print axioms new_density_implies_mark_excess
#print axioms no_double_marks_suffices

end SubQuorum.WidthSixMarkExcess
