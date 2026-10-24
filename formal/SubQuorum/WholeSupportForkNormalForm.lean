import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.WholeSupportForkNormalForm

/-- Remaining alpha-to-beta assignment on an odd alternating path after
reserving an alpha root, or a beta root with its two adjacent alphas. -/
def residualBeta (p a : Nat) : Nat := if a<p then a else a-1

/-- Reserve alpha p in a path with n+1 alpha and n beta owners. -/
theorem alpha_root_bounds (n p a : Nat) (hp : p≤n) (ha : a≤n) (hne : a≠p) :
    residualBeta p a<n := by
  unfold residualBeta
  split <;> omega

theorem residual_adjacent (p a : Nat) :
    residualBeta p a=a ∨ residualBeta p a+1=a := by
  unfold residualBeta
  split <;> omega

theorem alpha_root_injective (p a b : Nat) (ha : a≠p) (hb : b≠p)
    (same : residualBeta p a=residualBeta p b) : a=b := by
  unfold residualBeta at same
  split at same <;> split at same <;> omega

theorem alpha_root_coverage (n p b : Nat) (_hp : p≤n) (hb : b<n) :
    ∃ a, a≤n ∧ a≠p ∧ residualBeta p a=b := by
  by_cases h : b<p
  · exact ⟨b, by omega, by omega, by simp [residualBeta,h]⟩
  · refine ⟨b+1, by omega, by omega, ?_⟩
    simp [residualBeta,show ¬b+1<p by omega]

/-- Reserve beta p and both adjacent alphas p,p+1. All other beta
owners are still covered exactly once by the same adjacent map. -/
theorem fork_root_excludes_beta (p a : Nat) (ha : a≠p) (ha' : a≠p+1) :
    residualBeta p a≠p := by
  unfold residualBeta
  split <;> omega

theorem fork_root_coverage (n p b : Nat) (_hp : p<n) (hb : b<n) (hne : b≠p) :
    ∃ a, a≤n ∧ a≠p ∧ a≠p+1 ∧ residualBeta p a=b := by
  by_cases h : b<p
  · exact ⟨b, by omega, by omega, by omega, by simp [residualBeta,h]⟩
  · refine ⟨b+1, by omega, by omega, by omega, ?_⟩
    simp [residualBeta,show ¬b+1<p by omega]

/-- s interval stems, t beta stems and f beta forks consume t+f whole
betas and s+f distinct original intervals, paying s+t+2*f alphas. -/
theorem normal_form_ledger (k b i s t f : Nat)
    (alphas : s+t+2*f≤k) (betas : t+f≤b) (intervals : s+f≤i) :
    ((i-(s+f) : Nat) : Int)+((b-(t+f) : Nat) : Int)-
      ((k-(s+t+2*f) : Nat) : Int) = (i : Int)+b-k := by omega

#print axioms alpha_root_bounds
#print axioms residual_adjacent
#print axioms alpha_root_injective
#print axioms alpha_root_coverage
#print axioms fork_root_excludes_beta
#print axioms fork_root_coverage
#print axioms normal_form_ledger

end SubQuorum.WholeSupportForkNormalForm
