import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.PPCutDebt

inductive Kind where
  | tp
  | bp
  deriving DecidableEq

structure Strand where
  left : Kind
  right : Kind

def charge : Strand → Int
  | ⟨.tp, .tp⟩ => -1
  | ⟨.bp, .bp⟩ => 1
  | _ => 0

def total : List Strand → Int
  | [] => 0
  | strand :: rest => charge strand + total rest

theorem opposite_join (left first second right : Kind) (opposite : first ≠ second) :
    charge ⟨left, first⟩ + charge ⟨second, right⟩ = charge ⟨left, right⟩ := by
  cases left <;> cases first <;> cases second <;> cases right <;>
    simp_all [charge]

theorem opposite_close (left right : Kind) (opposite : left ≠ right) :
    charge ⟨left, right⟩ = 0 := by
  cases left <;> cases right <;> simp_all [charge]

theorem internal_cut (left right : Kind) :
    charge ⟨left, .bp⟩ + charge ⟨.bp, right⟩ = charge ⟨left, right⟩ + 1 := by
  cases left <;> cases right <;> decide

inductive Trace : List Strand → Nat → List Strand → Nat → Nat → Prop where
  | refl (strands : List Strand) (cycles : Nat) : Trace strands cycles strands cycles 0
  | join (left first second right : Kind) (rest : List Strand) (cycles : Nat)
      (opposite : first ≠ second) :
      Trace (⟨left, first⟩ :: ⟨second, right⟩ :: rest) cycles
        (⟨left, right⟩ :: rest) cycles 0
  | close (left right : Kind) (rest : List Strand) (cycles : Nat)
      (opposite : left ≠ right) :
      Trace (⟨left, right⟩ :: rest) cycles rest (cycles + 1) 0
  | reverse (left right : Kind) (rest : List Strand) (cycles : Nat) :
      Trace (⟨left, right⟩ :: rest) cycles (⟨right, left⟩ :: rest) cycles 0
  | swap (first second : Strand) (rest : List Strand) (cycles : Nat) :
      Trace (first :: second :: rest) cycles (second :: first :: rest) cycles 0
  | cutPath (left right : Kind) (rest : List Strand) (cycles : Nat) :
      Trace (⟨left, right⟩ :: rest) cycles
        (⟨left, .bp⟩ :: ⟨.bp, right⟩ :: rest) cycles 1
  | openCycle (rest : List Strand) (cycles : Nat) :
      Trace rest (cycles + 1) (⟨.bp, .bp⟩ :: rest) cycles 1
  | lift (strand : Strand) {before after : List Strand}
      {beforeCycles afterCycles cuts : Nat}
      (step : Trace before beforeCycles after afterCycles cuts) :
      Trace (strand :: before) beforeCycles (strand :: after) afterCycles cuts
  | trans {before middle after : List Strand} {beforeCycles middleCycles afterCycles : Nat}
      {firstCuts secondCuts : Nat}
      (first : Trace before beforeCycles middle middleCycles firstCuts)
      (second : Trace middle middleCycles after afterCycles secondCuts) :
      Trace before beforeCycles after afterCycles (firstCuts + secondCuts)

theorem finite_trace_has_exact_cut_debt {before after : List Strand}
    {beforeCycles afterCycles cuts : Nat}
    (trace : Trace before beforeCycles after afterCycles cuts) :
    total after = total before + (cuts : Int) := by
  induction trace with
  | refl => simp
  | join left first second right rest cycles opposite =>
    have identity := opposite_join left first second right opposite
    simp only [total]
    omega
  | close left right rest cycles opposite =>
    simp [total, opposite_close left right opposite]
  | reverse left right rest cycles =>
    cases left <;> cases right <;> simp [total, charge]
  | swap first second rest cycles => simp only [total]; omega
  | cutPath left right rest cycles =>
    have identity := internal_cut left right
    simp only [total]
    omega
  | openCycle rest cycles => simp only [total, charge]; omega
  | lift strand step inductionHypothesis => simp only [total]; omega
  | trans first second firstHypothesis secondHypothesis =>
    omega

theorem corrected_charge_is_invariant {before after : List Strand}
    {beforeCycles afterCycles cuts : Nat}
    (trace : Trace before beforeCycles after afterCycles cuts) :
    total after - (cuts : Int) = total before := by
  have identity := finite_trace_has_exact_cut_debt trace
  omega

theorem packet_ledger_after_trace {before after : List Strand}
    {beforeCycles afterCycles cuts : Nat}
    (trace : Trace before beforeCycles after afterCycles cuts)
    (surplus intervals boundary : Int)
    (originalLedger : surplus - boundary = intervals + total before) :
    surplus - boundary = intervals + total after - (cuts : Int) := by
  have identity := corrected_charge_is_invariant trace
  omega

theorem omitting_cut_debt_overstates_margin {before after : List Strand}
    {beforeCycles afterCycles cuts : Nat}
    (trace : Trace before beforeCycles after afterCycles cuts)
    (surplus intervals boundary : Int)
    (originalLedger : surplus - boundary = intervals + total before) :
    intervals + total after - (surplus - boundary) = (cuts : Int) := by
  have identity := packet_ledger_after_trace trace surplus intervals boundary originalLedger
  omega

theorem opening_cycle_then_pairing :
    Trace [⟨.tp, .tp⟩] 1 [⟨.bp, .tp⟩] 0 1 := by
  exact Trace.trans (Trace.openCycle [⟨.tp, .tp⟩] 0)
    (Trace.join .bp .bp .tp .tp [] 0 (by decide))

theorem apparent_payment_keeps_negative_unit :
    total [⟨.bp, .tp⟩] - (1 : Int) = total [⟨.tp, .tp⟩] := by
  exact corrected_charge_is_invariant opening_cycle_then_pairing

theorem positive_join_repays_unit (left right : Kind) :
    charge ⟨left, right⟩ = charge ⟨left, .bp⟩ + charge ⟨.bp, right⟩ - 1 := by
  cases left <;> cases right <;> decide

inductive DebtTrace : List Strand → Nat → List Strand → Nat → Int → Prop where
  | fromCuts {before after : List Strand} {beforeCycles afterCycles cuts : Nat}
      (trace : Trace before beforeCycles after afterCycles cuts) :
      DebtTrace before beforeCycles after afterCycles (cuts : Int)
  | positiveJoin (left right : Kind) (rest : List Strand) (cycles : Nat) :
      DebtTrace (⟨left, .bp⟩ :: ⟨.bp, right⟩ :: rest) cycles
        (⟨left, right⟩ :: rest) cycles (-1)
  | positiveClose (rest : List Strand) (cycles : Nat) :
      DebtTrace (⟨.bp, .bp⟩ :: rest) cycles rest (cycles + 1) (-1)
  | lift (strand : Strand) {before after : List Strand} {beforeCycles afterCycles : Nat}
      {debt : Int} (trace : DebtTrace before beforeCycles after afterCycles debt) :
      DebtTrace (strand :: before) beforeCycles (strand :: after) afterCycles debt
  | trans {before middle after : List Strand} {beforeCycles middleCycles afterCycles : Nat}
      {firstDebt secondDebt : Int}
      (first : DebtTrace before beforeCycles middle middleCycles firstDebt)
      (second : DebtTrace middle middleCycles after afterCycles secondDebt) :
      DebtTrace before beforeCycles after afterCycles (firstDebt + secondDebt)

theorem finite_reconnection_has_exact_debt {before after : List Strand}
    {beforeCycles afterCycles : Nat} {debt : Int}
    (trace : DebtTrace before beforeCycles after afterCycles debt) :
    total after = total before + debt := by
  induction trace with
  | fromCuts trace => exact finite_trace_has_exact_cut_debt trace
  | positiveJoin left right rest cycles =>
    have identity := positive_join_repays_unit left right
    simp only [total]
    omega
  | positiveClose rest cycles => simp only [total, charge]; omega
  | lift strand trace inductionHypothesis => simp only [total]; omega
  | trans first second firstHypothesis secondHypothesis => omega

theorem zero_debt_reconnection_preserves_ledger {before after : List Strand}
    {beforeCycles afterCycles : Nat}
    (trace : DebtTrace before beforeCycles after afterCycles 0)
    (surplus intervals boundary : Int)
    (originalLedger : surplus - boundary = intervals + total before) :
    surplus - boundary = intervals + total after := by
  have identity := finite_reconnection_has_exact_debt trace
  omega

theorem balanced_two_cut_repair :
    DebtTrace [⟨.tp, .tp⟩, ⟨.bp, .bp⟩] 1 [⟨.tp, .bp⟩] 1 0 := by
  have cuts : Trace [⟨.tp, .tp⟩, ⟨.bp, .bp⟩] 1
      [⟨.bp, .bp⟩, ⟨.tp, .tp⟩, ⟨.bp, .bp⟩, ⟨.bp, .bp⟩] 0 2 :=
    Trace.trans (Trace.openCycle [⟨.tp, .tp⟩, ⟨.bp, .bp⟩] 0)
      (Trace.lift ⟨.bp, .bp⟩ (Trace.lift ⟨.tp, .tp⟩ (Trace.cutPath .bp .bp [] 0)))
  have paired : Trace [⟨.bp, .bp⟩, ⟨.tp, .tp⟩, ⟨.bp, .bp⟩, ⟨.bp, .bp⟩] 0
      [⟨.tp, .bp⟩, ⟨.bp, .bp⟩, ⟨.bp, .bp⟩] 0 0 :=
    Trace.trans (Trace.join .bp .bp .tp .tp [⟨.bp, .bp⟩, ⟨.bp, .bp⟩] 0 (by decide))
      (Trace.reverse .bp .tp [⟨.bp, .bp⟩, ⟨.bp, .bp⟩] 0)
  have repaid : DebtTrace [⟨.tp, .bp⟩, ⟨.bp, .bp⟩, ⟨.bp, .bp⟩] 0
      [⟨.tp, .bp⟩] 1 (-2) :=
    DebtTrace.trans (DebtTrace.positiveJoin .tp .bp [⟨.bp, .bp⟩] 0)
      (DebtTrace.lift ⟨.tp, .bp⟩ (DebtTrace.positiveClose [] 0))
  exact DebtTrace.trans (DebtTrace.trans (DebtTrace.fromCuts cuts) (DebtTrace.fromCuts paired)) repaid

end SubQuorum.PPCutDebt

#print axioms SubQuorum.PPCutDebt.finite_trace_has_exact_cut_debt
#print axioms SubQuorum.PPCutDebt.corrected_charge_is_invariant
#print axioms SubQuorum.PPCutDebt.packet_ledger_after_trace
#print axioms SubQuorum.PPCutDebt.omitting_cut_debt_overstates_margin
#print axioms SubQuorum.PPCutDebt.opening_cycle_then_pairing
#print axioms SubQuorum.PPCutDebt.apparent_payment_keeps_negative_unit
#print axioms SubQuorum.PPCutDebt.finite_reconnection_has_exact_debt
#print axioms SubQuorum.PPCutDebt.zero_debt_reconnection_preserves_ledger
#print axioms SubQuorum.PPCutDebt.balanced_two_cut_repair
