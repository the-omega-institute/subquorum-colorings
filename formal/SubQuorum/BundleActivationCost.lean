import Std.Tactic

set_option autoImplicit false

namespace SubQuorum.BundleActivationCost

/-- Each bundle contributes its fee once, regardless of the number of
matched real slots, when its used flag is true. -/
def spent : List (Nat × Bool) → Nat
  | [] => 0
  | (fee, used) :: rest => (if used then fee else 0) + spent rest

def saved : List (Nat × Bool) → Nat
  | [] => 0
  | (fee, used) :: rest => (if used then 0 else fee) + saved rest

def total : List (Nat × Bool) → Nat
  | [] => 0
  | (fee, _) :: rest => fee + total rest

theorem fee_complement (bundles : List (Nat × Bool)) :
    saved bundles + spent bundles = total bundles := by
  induction bundles with
  | nil => rfl
  | cons entry rest ih =>
    obtain ⟨fee, used⟩ := entry
    cases used <;> simp [saved, spent, total, Nat.add_assoc, Nat.add_left_comm, ih]

/-- In a completed matching, unused internal edges contribute saved fees. -/
theorem weight_cost_identity (bundles : List (Nat × Bool)) (scale paid : Nat) :
    (scale * paid + saved bundles) + spent bundles = scale * paid + total bundles := by
  rw [Nat.add_assoc, fee_complement]

/-- The scale totalFee+1 makes one extra paid source dominate every
possible activation-fee difference. -/
theorem cardinality_priority (totalFee p q feeP feeQ : Nat)
    (hp : feeP ≤ totalFee) (hq : feeQ ≤ totalFee) (more : q < p) :
    (totalFee + 1) * q + (totalFee - feeQ) <
      (totalFee + 1) * p + (totalFee - feeP) := by
  have step : (totalFee + 1) * (q + 1) ≤ (totalFee + 1) * p :=
    Nat.mul_le_mul_left _ (Nat.succ_le_of_lt more)
  rw [Nat.mul_add, Nat.mul_one] at step
  omega

theorem lower_fee_priority (totalFee paid feeP feeQ : Nat)
    (hp : feeP ≤ totalFee) (hq : feeQ ≤ totalFee) (cheaper : feeP < feeQ) :
    (totalFee + 1) * paid + (totalFee - feeQ) <
      (totalFee + 1) * paid + (totalFee - feeP) := by
  omega

end SubQuorum.BundleActivationCost

#print axioms SubQuorum.BundleActivationCost.fee_complement
#print axioms SubQuorum.BundleActivationCost.weight_cost_identity
#print axioms SubQuorum.BundleActivationCost.cardinality_priority
#print axioms SubQuorum.BundleActivationCost.lower_fee_priority
