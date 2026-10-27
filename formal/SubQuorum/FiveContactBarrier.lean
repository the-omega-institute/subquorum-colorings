import Lean.Elab.Tactic.Omega

/-! Exact symbolic ledger and quantified unbounded cost ratio.
Actual domino geometry, feasibility, contact routing and the completeness
of the six reverse pairs remain written, not assumed verified by this file. -/
set_option autoImplicit false
namespace SubQuorum.FiveContactBarrier

theorem symbolic_ledger (L d w : Nat) :
    2*w+2*L+5*d+80 = (2*L+3*d+78)+2*(w+d+1) := by omega

theorem quadratic_cost (L w : Nat) (positive : 1 ≤ L)
    (hw : w=(L-1)*L+2*L+1) :
    w+13=L*L+L+14 := by
  have h := Nat.mul_le_mul_left L positive
  simp only [Nat.mul_one] at h
  rw [Nat.sub_mul, Nat.one_mul] at hw
  omega

theorem positive_gap (L : Nat) (lower : 12 ≤ L) :
    5*L+78 < L*L+L+14 := by
  have h := Nat.mul_le_mul_right L lower
  omega

theorem linear_bound (L : Nat) (lower : 12 ≤ L) :
    5*L+78 ≤ 12*L := by omega

theorem ratio_bound (L K : Nat) (lower : 12 ≤ L) (large : 12*K < L) :
    K*(5*L+78) < L*L+L+14 := by
  have h := linear_bound L lower
  have hL : 0 < L := by omega
  calc
    K*(5*L+78) ≤ K*(12*L) := Nat.mul_le_mul_left K h
    _ = (12*K)*L := by rw [← Nat.mul_assoc, Nat.mul_comm K 12]
    _ < L*L := Nat.mul_lt_mul_of_pos_right large hL
    _ ≤ L*L+L+14 := by omega

/-- For every prescribed integer factor, an explicit even admissible
parameter violates that factor. The written adapter supplies actual costs. -/
theorem unbounded_ratio (K : Nat) :
    ∃ L : Nat, 12 ≤ L ∧ (∃ n : Nat, L=2*n) ∧
      K*(5*L+78) < L*L+L+14 := by
  refine ⟨20*(K+1), by omega, ⟨10*(K+1), by omega⟩, ?_⟩
  exact ratio_bound _ K (by omega) (by omega)

end SubQuorum.FiveContactBarrier
#print axioms SubQuorum.FiveContactBarrier.symbolic_ledger
#print axioms SubQuorum.FiveContactBarrier.quadratic_cost
#print axioms SubQuorum.FiveContactBarrier.positive_gap
#print axioms SubQuorum.FiveContactBarrier.linear_bound
#print axioms SubQuorum.FiveContactBarrier.ratio_bound
#print axioms SubQuorum.FiveContactBarrier.unbounded_ratio
