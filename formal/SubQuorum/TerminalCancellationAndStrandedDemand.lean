import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.TerminalCancellationAndStrandedDemand

inductive Kind where
  | tp
  | bp
  deriving DecidableEq

structure Strand where
  left : Kind
  right : Kind

def weight : Kind → Int
  | .tp => -1
  | .bp => 1

def charge : Strand → Int
  | ⟨.tp, .tp⟩ => -1
  | ⟨.bp, .bp⟩ => 1
  | _ => 0

def alpha : Strand → Int
  | ⟨.tp, .tp⟩ => 1
  | _ => 0

def beta : Strand → Int
  | ⟨.bp, .bp⟩ => 1
  | _ => 0

def total (measure : Strand → Int) : List Strand → Int
  | [] => 0
  | strand :: rest => measure strand + total measure rest

theorem charge_equals_terminal_weights (strand : Strand) :
    2 * charge strand = weight strand.left + weight strand.right := by
  rcases strand with ⟨left, right⟩
  cases left <;> cases right <;> decide

theorem strand_charge_inventory (strands : List Strand) :
    total charge strands = total beta strands - total alpha strands := by
  induction strands with
  | nil => rfl
  | cons strand rest inductionHypothesis =>
    rcases strand with ⟨left, right⟩
    cases left <;> cases right <;> simp_all [total, charge, alpha, beta] <;> omega

theorem joining_opposite_terminals (left first second right : Kind)
    (opposite : first ≠ second) :
    charge ⟨left, first⟩ + charge ⟨second, right⟩ = charge ⟨left, right⟩ := by
  cases left <;> cases first <;> cases second <;> cases right <;>
    simp_all [charge]

theorem closing_opposite_terminals (left right : Kind) (opposite : left ≠ right) :
    charge ⟨left, right⟩ = 0 := by
  cases left <;> cases right <;> simp_all [charge]

theorem reversing_strand (left right : Kind) :
    charge ⟨left, right⟩ = charge ⟨right, left⟩ := by
  cases left <;> cases right <;> decide

inductive Surgery : List Strand → List Strand → Prop where
  | refl (strands : List Strand) : Surgery strands strands
  | join (left first second right : Kind) (rest : List Strand)
      (opposite : first ≠ second) :
      Surgery (⟨left, first⟩ :: ⟨second, right⟩ :: rest) (⟨left, right⟩ :: rest)
  | close (left right : Kind) (rest : List Strand) (opposite : left ≠ right) :
      Surgery (⟨left, right⟩ :: rest) rest
  | reverse (left right : Kind) (rest : List Strand) :
      Surgery (⟨left, right⟩ :: rest) (⟨right, left⟩ :: rest)
  | swap (first second : Strand) (rest : List Strand) :
      Surgery (first :: second :: rest) (second :: first :: rest)
  | lift (strand : Strand) {before after : List Strand}
      (step : Surgery before after) : Surgery (strand :: before) (strand :: after)
  | trans {before middle after : List Strand}
      (first : Surgery before middle) (second : Surgery middle after) : Surgery before after

theorem finite_surgery_preserves_credit {before after : List Strand}
    (surgery : Surgery before after) : total charge before = total charge after := by
  induction surgery with
  | refl => rfl
  | join left first second right rest opposite =>
    have localIdentity := joining_opposite_terminals left first second right opposite
    simp only [total]
    omega
  | close left right rest opposite =>
    simp [total, closing_opposite_terminals left right opposite]
  | reverse left right rest =>
    simp only [total]
    rw [reversing_strand left right]
  | swap first second rest => simp only [total]; omega
  | lift strand step inductionHypothesis => simp only [total]; omega
  | trans first second firstHypothesis secondHypothesis => omega

theorem finite_surgery_preserves_path_inventory {before after : List Strand}
    (surgery : Surgery before after) :
    total beta after - total alpha after = total beta before - total alpha before := by
  have conservation := finite_surgery_preserves_credit surgery
  rw [strand_charge_inventory, strand_charge_inventory] at conservation
  omega

theorem beta_inventory_nonnegative (strands : List Strand) : 0 ≤ total beta strands := by
  induction strands with
  | nil => decide
  | cons strand rest inductionHypothesis =>
    rcases strand with ⟨left, right⟩
    cases left <;> cases right <;> simp_all [total, beta] <;> omega

theorem alpha_inventory_nonnegative (strands : List Strand) : 0 ≤ total alpha strands := by
  induction strands with
  | nil => decide
  | cons strand rest inductionHypothesis =>
    rcases strand with ⟨left, right⟩
    cases left <;> cases right <;> simp_all [total, alpha] <;> omega

theorem joining_does_not_create_beta (left first second right : Kind)
    (opposite : first ≠ second) :
    beta ⟨left, right⟩ ≤ beta ⟨left, first⟩ + beta ⟨second, right⟩ := by
  cases left <;> cases first <;> cases second <;> cases right <;>
    simp_all [beta]

theorem finite_surgery_does_not_create_beta {before after : List Strand}
    (surgery : Surgery before after) : total beta after ≤ total beta before := by
  induction surgery with
  | refl => omega
  | join left first second right rest opposite =>
    have localBound := joining_does_not_create_beta left first second right opposite
    simp only [total]
    omega
  | close left right rest opposite =>
    cases left <;> cases right <;> simp_all [total, beta]
  | reverse left right rest =>
    cases left <;> cases right <;> simp [total, beta]
  | swap first second rest => simp only [total]; omega
  | lift strand step inductionHypothesis => simp only [total]; omega
  | trans first second firstHypothesis secondHypothesis => omega

theorem finite_surgery_has_common_nonnegative_drop {before after : List Strand}
    (surgery : Surgery before after) :
    ∃ consumed : Int, 0 ≤ consumed ∧ consumed ≤ total beta before ∧
      consumed ≤ total alpha before ∧
      total beta after = total beta before - consumed ∧
      total alpha after = total alpha before - consumed := by
  have monotone := finite_surgery_does_not_create_beta surgery
  have conservation := finite_surgery_preserves_path_inventory surgery
  have nonnegativeBeta := beta_inventory_nonnegative after
  have nonnegativeAlpha := alpha_inventory_nonnegative after
  refine ⟨total beta before - total beta after, ?_⟩
  omega

theorem no_beta_prevents_demand_reduction {before after : List Strand}
    (surgery : Surgery before after) (noBeta : total beta before = 0) :
    total beta after = 0 ∧ total alpha after = total alpha before := by
  obtain ⟨consumed, conditions⟩ := finite_surgery_has_common_nonnegative_drop surgery
  omega

theorem packet_ledger_after_surgery {before after : List Strand}
    (surgery : Surgery before after) (surplus balance : Int)
    (original : surplus = balance + total beta before - total alpha before) :
    surplus = balance + total beta after - total alpha after := by
  have conservation := finite_surgery_preserves_path_inventory surgery
  omega

theorem virtual_connector_ledger {before after : List Strand}
    (surgery : Surgery before after)
    (surplus balance boundary edges omitted interior oneMark twoMarks : Int)
    (original : surplus = balance + total beta before - total alpha before)
    (coverage : total alpha after = edges + omitted)
    (euler : balance - edges = interior + oneMark + twoMarks)
    (boundaryInventory : boundary = oneMark + 2 * twoMarks) :
    surplus - boundary = interior + total beta after - twoMarks - omitted := by
  have ledger := packet_ledger_after_surgery surgery surplus balance original
  omega

theorem virtual_compensation_iff (surplus boundary interior betaCount twoMarks omitted : Int)
    (ledger : surplus - boundary = interior + betaCount - twoMarks - omitted) :
    boundary ≤ surplus ↔ twoMarks + omitted ≤ interior + betaCount := by omega

theorem beta_target_no_collision_suffices (surplus boundary interior betaCount : Int)
    (ledger : surplus - boundary = interior + betaCount)
    (interiorNonnegative : 0 ≤ interior) (betaNonnegative : 0 ≤ betaCount) :
    boundary ≤ surplus := by omega

theorem mixed_tail_has_zero_credit (count : Nat) :
    total charge (List.replicate count (⟨.bp, .tp⟩ : Strand)) = 0 := by
  induction count with
  | zero => rfl
  | succ count inductionHypothesis =>
    simp [List.replicate_succ, total, charge, inductionHypothesis]

theorem alpha_with_mixed_tail_is_full_demand (count : Nat) :
    total charge ((⟨.tp, .tp⟩ : Strand) :: List.replicate count ⟨.bp, .tp⟩) = -1 := by
  simp [total, charge, mixed_tail_has_zero_credit]

theorem two_alpha_one_beta_do_not_pay_two_demands :
    total charge [⟨.tp, .tp⟩, ⟨.bp, .bp⟩, ⟨.tp, .tp⟩] = -1 := by decide

theorem opposite_mixed_cycle_has_zero_credit : charge ⟨.tp, .bp⟩ = 0 := by decide

theorem stranded_family_margin (surplus area width height : Int)
    (inventory : surplus = area + 5 * width + 10 * height + 63) :
    surplus - (width + 12) = area + 4 * width + 10 * height + 51 := by omega

end SubQuorum.TerminalCancellationAndStrandedDemand

#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.charge_equals_terminal_weights
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.strand_charge_inventory
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.joining_opposite_terminals
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.closing_opposite_terminals
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.reversing_strand
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.finite_surgery_preserves_credit
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.finite_surgery_preserves_path_inventory
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.beta_inventory_nonnegative
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.alpha_inventory_nonnegative
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.joining_does_not_create_beta
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.finite_surgery_does_not_create_beta
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.finite_surgery_has_common_nonnegative_drop
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.no_beta_prevents_demand_reduction
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.packet_ledger_after_surgery
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.virtual_connector_ledger
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.virtual_compensation_iff
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.beta_target_no_collision_suffices
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.mixed_tail_has_zero_credit
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.alpha_with_mixed_tail_is_full_demand
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.two_alpha_one_beta_do_not_pay_two_demands
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.opposite_mixed_cycle_has_zero_credit
#print axioms SubQuorum.TerminalCancellationAndStrandedDemand.stranded_family_margin
