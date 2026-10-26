import Lean.Elab.Tactic.Omega

/-!
The unrestricted-length part of the six-row boundary invariant. These theorems
take local potential inequalities as hypotheses; they do not assert that the
published lookup table or the coordinate adapter has been formalized.
-/
namespace SubQuorum.BoundaryPotentialInduction

theorem prefix_bound (score phi : Nat → Int)
    (seed : score 1 - 6 ≤ phi 1)
    (step : ∀ n, 1 ≤ n →
      score (n + 1) - score n - 6 + phi n ≤ phi (n + 1)) :
    ∀ n, 1 ≤ n → score n - 6 * (n : Int) ≤ phi n := by
  intro n
  induction n with
  | zero => omega
  | succ n ih =>
    intro hn
    by_cases h : n = 0
    · subst n
      simpa using seed
    · have hn' : 1 ≤ n := by omega
      have hp := ih hn'
      have hs := step n hn'
      omega

theorem closed_trace_bound (score phi : Nat → Int)
    (seed : score 1 - 6 ≤ phi 1)
    (step : ∀ n, 1 ≤ n →
      score (n + 1) - score n - 6 + phi n ≤ phi (n + 1))
    (w : Nat) (positive : 1 ≤ w)
    (terminal : phi w ≤ 2 * ((w % 2 : Nat) : Int)) :
    score w ≤ 6 * (w : Int) + 2 * ((w % 2 : Nat) : Int) := by
  have hp := prefix_bound score phi seed step w positive
  omega

theorem objective_bound (j : Int) (w : Nat)
    (bound : 2 * j ≤ 6 * (w : Int) + 2 * ((w % 2 : Nat) : Int)) :
    j ≤ 3 * (w : Int) + ((w % 2 : Nat) : Int) := by
  omega

theorem even_width_half_area (j : Int) (w : Nat)
    (bound : 2 * j ≤ 6 * (w : Int) + 2 * ((w % 2 : Nat) : Int))
    (even : w % 2 = 0) : j ≤ 3 * (w : Int) := by
  have hb := objective_bound j w bound
  simp only [even, Int.natCast_zero, Int.add_zero] at hb
  exact hb

end SubQuorum.BoundaryPotentialInduction
#print axioms SubQuorum.BoundaryPotentialInduction.prefix_bound
#print axioms SubQuorum.BoundaryPotentialInduction.closed_trace_bound
#print axioms SubQuorum.BoundaryPotentialInduction.objective_bound
#print axioms SubQuorum.BoundaryPotentialInduction.even_width_half_area
