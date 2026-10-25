import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.PinwheelBetaCoreSwitches

def bit (b : Bool) : Nat := if b then 1 else 0

/-- Used crossings have unit input/output capacities. Direct stub payments
use the same input gate, but do not visit any output port in the flow. -/
def admissible (a00 a01 a10 a11 d0 d1 : Bool) : Prop :=
  bit a00 + bit a01 + bit d0 ≤ 1 ∧
  bit a10 + bit a11 + bit d1 ≤ 1 ∧
  bit a00 + bit a10 ≤ 1 ∧ bit a01 + bit a11 ≤ 1

instance (a00 a01 a10 a11 d0 d1 : Bool) :
    Decidable (admissible a00 a01 a10 a11 d0 d1) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _))

def compatible (flip a00 a01 a10 a11 : Bool) : Prop :=
  if flip then a00 = false ∧ a11 = false else a01 = false ∧ a10 = false

instance (flip a00 a01 a10 a11 : Bool) :
    Decidable (compatible flip a00 a01 a10 a11) := by
  unfold compatible
  infer_instance

/-- Complete the pairing, assigning a direct-paying stub its unused port.
Both final port loads include payments absent from the relaxed core inflow. -/
theorem completed_port_capacity (flip a00 a01 a10 a11 d0 d1 : Bool) :
    admissible a00 a01 a10 a11 d0 d1 →
    compatible flip a00 a01 a10 a11 →
    bit a00 + bit a10 + (if flip then bit d1 else bit d0) ≤ 1 ∧
    bit a01 + bit a11 + (if flip then bit d0 else bit d1) ≤ 1 := by
  cases flip <;> cases a00 <;> cases a01 <;> cases a10 <;>
    cases a11 <;> cases d0 <;> cases d1 <;> decide

/-- A beta has two physical BP ends, including unchanged external entries. -/
theorem beta_total_load (ports external through direct outside : Nat)
    (ends : ports + external = 2)
    (completed : through + direct ≤ ports)
    (unchanged : outside ≤ external) : through + direct + outside ≤ 2 := by
  omega

/-- A second payment requires an original interval even if paid at a stub. -/
theorem second_payment_needs_interval (betaUsed bodyIntervals stubIntervals : Nat)
    (one_private : betaUsed ≤ 1)
    (two : betaUsed + bodyIntervals + stubIntervals = 2) :
    1 ≤ bodyIntervals + stubIntervals := by omega

/-- Replacing one interval payment by the unused private beta releases a
resource. The retained interval count never exceeds the old available count. -/
theorem normalize_beta_outputs (r betaUsed bodyIntervals stubIntervals : Nat)
    (count : r = betaUsed + bodyIntervals + stubIntervals)
    (one_private : betaUsed ≤ 1) (positive : 0 < r) (two_ends : r ≤ 2) :
    ∃ retained : Nat, r = 1 + retained ∧ retained ≤ 1 ∧
      retained ≤ bodyIntervals + stubIntervals := by
  refine ⟨r-1, ?_, ?_, ?_⟩ <;> omega

#print axioms completed_port_capacity
#print axioms beta_total_load
#print axioms second_payment_needs_interval
#print axioms normalize_beta_outputs

end SubQuorum.PinwheelBetaCoreSwitches
