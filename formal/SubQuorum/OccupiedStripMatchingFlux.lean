import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.OccupiedStripMatchingFlux

inductive ColumnKind where
  | blank
  | double
  | other
  deriving DecidableEq

open ColumnKind

def allowed (previous next : ColumnKind) : Prop :=
  (previous = double → next = blank) ∧ (next = double → previous = blank)

def weight : ColumnKind → Int
  | blank => 1
  | double => -1
  | other => 0

inductive Trace : Nat → Int → ColumnKind → Prop where
  | first : Trace 1 1 blank
  | step {length : Nat} {balance : Int} {previous : ColumnKind}
      (prior : Trace length balance previous) (next : ColumnKind)
      (legal : allowed previous next) : Trace (length + 1) (balance + weight next) next

def invariant (length : Nat) (balance : Int) : ColumnKind → Prop
  | blank => 1 ≤ balance ∧ (balance = 1 → length % 2 = 1)
  | double => 0 ≤ balance ∧ (balance = 0 → length % 2 = 0)
  | other => 1 ≤ balance

theorem arbitrary_length_balance {length : Nat} {balance : Int} {last : ColumnKind}
    (trace : Trace length balance last) : invariant length balance last := by
  induction trace with
  | first => simp [invariant]
  | @step length balance previous prior next legal inductionHypothesis =>
    cases previous <;> cases next <;>
      simp_all [allowed, weight, invariant] <;> omega

theorem blank_entry_non_double_exit {length : Nat} {balance : Int} {last : ColumnKind}
    (trace : Trace length balance last) (exit : last ≠ double) : 1 ≤ balance := by
  have checked := arbitrary_length_balance trace
  cases last <;> simp_all [invariant]

theorem sealed_even_balance {length : Nat} {balance : Int}
    (trace : Trace length balance blank) (evenLength : length % 2 = 0) : 2 ≤ balance := by
  have checked := arbitrary_length_balance trace
  simp only [invariant] at checked
  omega

def top (column : Fin 9) : Nat := column.val % 3

def bottom (column : Fin 9) : Nat := column.val / 3

def localSelectedFeasible (source neighbor : Fin 9) : Prop :=
  (top source = 1 → (if bottom source = 0 then 0 else 1) +
    (if top neighbor = 0 then 0 else 1) ≤ 1) ∧
  (bottom source = 1 → (if top source = 0 then 0 else 1) +
    (if bottom neighbor = 0 then 0 else 1) ≤ 1)

instance (source neighbor : Fin 9) : Decidable (localSelectedFeasible source neighbor) :=
  inferInstanceAs (Decidable ((top source = 1 → (if bottom source = 0 then 0 else 1) +
    (if top neighbor = 0 then 0 else 1) ≤ 1) ∧
    (bottom source = 1 → (if top source = 0 then 0 else 1) +
    (if bottom neighbor = 0 then 0 else 1) ≤ 1)))

theorem mixed_horizontal_mate_forces_blank (source neighbor : Fin 9)
    (feasible : localSelectedFeasible source neighbor) :
    (top source = 1 → bottom source = 2 → bottom neighbor = 2 → top neighbor = 0) ∧
    (bottom source = 1 → top source = 2 → top neighbor = 2 → bottom neighbor = 0) := by
  have checked : ∀ source neighbor : Fin 9, localSelectedFeasible source neighbor →
      (top source = 1 → bottom source = 2 → bottom neighbor = 2 → top neighbor = 0) ∧
      (bottom source = 1 → top source = 2 → top neighbor = 2 → bottom neighbor = 0) := by decide
  exact checked source neighbor feasible

theorem exact_column_flux (doubleCount blankCount mixedCount singleEndpoint singleSelected
    doubleEndpoint length selected endpoints surplusTwice exports unused : Int)
    (columnCount : length = doubleCount + blankCount + mixedCount + singleEndpoint +
      singleSelected + doubleEndpoint)
    (selectedCount : selected = 2 * doubleCount + mixedCount + singleSelected)
    (endpointCount : endpoints = mixedCount + singleEndpoint + 2 * doubleEndpoint)
    (surplus : surplusTwice = 2 * length - 2 * selected - endpoints)
    (unusedCount : unused = singleEndpoint - mixedCount + exports) :
    surplusTwice + exports = 2 * (blankCount - doubleCount) + unused := by omega

theorem corrected_flux_bound (surplusTwice exports balance unused delta : Int)
    (identity : surplusTwice + exports = 2 * balance + unused)
    (injection : 0 ≤ unused) (boundary : delta ≤ balance) :
    2 * delta - exports ≤ surplusTwice := by omega

theorem no_mixed_export_bound (surplusTwice exports balance unused delta : Int)
    (identity : surplusTwice + exports = 2 * balance + unused)
    (injection : 0 ≤ unused) (boundary : delta ≤ balance) (noExport : exports = 0) :
    2 * delta ≤ surplusTwice := by omega

theorem internal_matching_bound (length selected internal cut exports delta : Int)
    (endpointBound : 2 * delta - exports ≤ 2 * length - 2 * selected - 2 * internal - cut)
    (exportSubset : exports ≤ cut) :
    selected + internal ≤ length - delta ∧
    2 * selected + 2 * internal + cut - exports ≤ 2 * (length - delta) := by omega

theorem regional_physical_ledger (surplusTwice deficit rawChargeTwice length
    selected endpoints : Int)
    (surplus : surplusTwice = 2 * length - 2 * selected - endpoints)
    (tileLedger : 2 * deficit - rawChargeTwice = 2 * length - 2 * selected - endpoints) :
    surplusTwice = 2 * deficit - rawChargeTwice := by omega

theorem disjoint_region_ownership_bound (marginTwice regionalSurplusTwice
    outsideDeficit outsidePositive outsideNegative boundaryBudget : Int)
    (ledger : marginTwice = regionalSurplusTwice + 2 * outsideDeficit -
      2 * outsidePositive + 2 * outsideNegative)
    (regionalBound : 2 * boundaryBudget ≤ regionalSurplusTwice) :
    2 * (boundaryBudget + outsideDeficit - outsidePositive + outsideNegative) ≤ marginTwice := by omega

theorem receiver_closed_compensation (marginTwice regionalSurplusTwice
    outsideDeficit outsidePositive outsideNegative boundaryBudget : Int)
    (ledger : marginTwice = regionalSurplusTwice + 2 * outsideDeficit -
      2 * outsidePositive + 2 * outsideNegative)
    (regionalBound : 2 * boundaryBudget ≤ regionalSurplusTwice)
    (covered : outsidePositive ≤ boundaryBudget)
    (deficitNonnegative : 0 ≤ outsideDeficit) (negativeNonnegative : 0 ≤ outsideNegative) :
    0 ≤ marginTwice := by omega

theorem half_unit_obstructs_debit_free_bound :
    (1 : Int) + 1 = 2 * 1 + 0 ∧ (1 : Int) < 2 * 1 ∧
    (3 : Int) + 1 = 2 * 2 + 0 ∧ (3 : Int) < 2 * 2 := by decide

end SubQuorum.OccupiedStripMatchingFlux

#print axioms SubQuorum.OccupiedStripMatchingFlux.arbitrary_length_balance
#print axioms SubQuorum.OccupiedStripMatchingFlux.blank_entry_non_double_exit
#print axioms SubQuorum.OccupiedStripMatchingFlux.sealed_even_balance
#print axioms SubQuorum.OccupiedStripMatchingFlux.mixed_horizontal_mate_forces_blank
#print axioms SubQuorum.OccupiedStripMatchingFlux.exact_column_flux
#print axioms SubQuorum.OccupiedStripMatchingFlux.corrected_flux_bound
#print axioms SubQuorum.OccupiedStripMatchingFlux.no_mixed_export_bound
#print axioms SubQuorum.OccupiedStripMatchingFlux.internal_matching_bound
#print axioms SubQuorum.OccupiedStripMatchingFlux.regional_physical_ledger
#print axioms SubQuorum.OccupiedStripMatchingFlux.disjoint_region_ownership_bound
#print axioms SubQuorum.OccupiedStripMatchingFlux.receiver_closed_compensation
#print axioms SubQuorum.OccupiedStripMatchingFlux.half_unit_obstructs_debit_free_bound
