import Lean.Elab.Tactic.Omega

/-! Arithmetic kernels only. Matching decomposition, distinct-component square
gluing, Hall coverage and the grid construction are written in the note.
-/
set_option autoImplicit false
namespace SubQuorum.MixedTerminalCompensation

theorem terminal_balance (T H a b t : Int)
    (tt : T = 2*a+t) (hh : H = 2*b+t) : H-T = 2*(b-a) := by omega

theorem batch_residuals (T H a b t s : Nat)
    (tt : T = 2*a+t) (hh : H = 2*b+t)
    (left : s ≤ a) (right : s ≤ b) :
    T = (t+2*s)+2*(a-s) ∧ H = (t+2*s)+2*(b-s) := by omega

/-- Hall coverage is an explicit hypothesis, not a grid theorem. The weighted
quantity is scaled by six to keep the exact 5/6 coefficient integral. -/
theorem full_hall_weighted (T H m area a b t : Int)
    (tt : T = 2*a+t) (hh : H = 2*b+t)
    (partition : area = T+H+2*m) (cover : a ≤ b) :
    2*(T+m) = area-2*(b-a) ∧ 2*(T+m) ≤ area ∧
    6*T+5*m = 3*area-6*(b-a)-m := by omega

/-- The matching-theoretic normalization and optimality inequalities are
inputs; this kernel only identifies the common optimum cost. -/
theorem retention_normalized (m retained cost : Nat)
    (inclusion : retained ≤ m)
    (fromPayment : m-retained ≤ cost)
    (fromNormalizedOptimum : cost ≤ m-retained) :
    cost = m-retained ∧ cost+retained=m := by omega

theorem terminal_penalty (m unrestricted constrained cost : Nat)
    (subset : constrained ≤ unrestricted) (actual : unrestricted ≤ m)
    (retention : cost = m-constrained) :
    cost = (m-unrestricted)+(unrestricted-constrained) := by omega

theorem band_counts (bands : Nat) :
    2*(6+4*bands)+2*2 = (4+2*bands)*4 ∧
    2*((6+4*bands)+2) = (4+2*bands)*4 := by omega

theorem penalty_one (cost retained unrestricted m : Nat)
    (actual : m=2) (all : unrestricted=2) (typed : retained=1)
    (retention : cost=m-retained) :
    cost=1 ∧ unrestricted-retained=1 := by omega

end SubQuorum.MixedTerminalCompensation
#print axioms SubQuorum.MixedTerminalCompensation.terminal_balance
#print axioms SubQuorum.MixedTerminalCompensation.batch_residuals
#print axioms SubQuorum.MixedTerminalCompensation.full_hall_weighted
#print axioms SubQuorum.MixedTerminalCompensation.retention_normalized
#print axioms SubQuorum.MixedTerminalCompensation.terminal_penalty
#print axioms SubQuorum.MixedTerminalCompensation.band_counts
#print axioms SubQuorum.MixedTerminalCompensation.penalty_one
