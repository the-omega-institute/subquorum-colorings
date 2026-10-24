import Std

set_option autoImplicit false

namespace SubQuorum.LowChargeRankBarrier

structure ComponentCounts where
  rank : Nat
  slots : Nat

def admissible (component : ComponentCounts) : Prop :=
  component.slots ≤ component.rank ∨
    (2 ≤ component.rank ∧ 2*component.slots ≤ component.rank*component.rank)

def rankSum : List ComponentCounts → Nat
  | [] => 0
  | component :: rest => component.rank + rankSum rest

def slotSum : List ComponentCounts → Nat
  | [] => 0
  | component :: rest => component.slots + slotSum rest

def smallBudget (rank : Nat) : Nat := rank + if rank = 3 then 1 else 0

theorem component_small_bound (component : ComponentCounts)
    (hvalid : admissible component) (hsmall : component.rank ≤ 3) :
    component.slots ≤ smallBudget component.rank := by
  rcases component with ⟨rank, slots⟩
  change slots ≤ rank ∨ (2 ≤ rank ∧ 2*slots ≤ rank*rank) at hvalid
  change rank ≤ 3 at hsmall
  have hcases : rank = 0 ∨ rank = 1 ∨ rank = 2 ∨ rank = 3 := by omega
  rcases hcases with hzero | hone | htwo | hthree
  all_goals subst rank
  all_goals simp [smallBudget]
  all_goals omega

theorem small_budget_add (first second : Nat) (hsmall : first+second ≤ 3) :
    smallBudget first + smallBudget second ≤ smallBudget (first+second) := by
  by_cases hfirst : first = 3
  · subst first
    have hzero : second = 0 := by omega
    subst second
    decide
  by_cases hsecond : second = 3
  · subst second
    have hzero : first = 0 := by omega
    subst first
    decide
  simp only [smallBudget, if_neg hfirst, if_neg hsecond, Nat.add_zero]
  omega

theorem small_total_bound (components : List ComponentCounts) :
    (∀ component ∈ components, admissible component) → rankSum components ≤ 3 →
    slotSum components ≤ smallBudget (rankSum components) := by
  induction components with
  | nil => simp [rankSum, slotSum, smallBudget]
  | cons component rest inductionHypothesis =>
      intro hvalid hsmall
      have hhead : component.rank ≤ 3 := by
        change component.rank + rankSum rest ≤ 3 at hsmall
        omega
      have hrest : rankSum rest ≤ 3 := by
        change component.rank + rankSum rest ≤ 3 at hsmall
        omega
      have hlocal := component_small_bound component (hvalid component (by simp)) hhead
      have htail := inductionHypothesis (by
        intro other hmember
        exact hvalid other (by simp [hmember])) hrest
      have hsum := small_budget_add component.rank (rankSum rest) hsmall
      change component.slots + slotSum rest ≤ smallBudget (component.rank+rankSum rest)
      exact Nat.le_trans (Nat.add_le_add hlocal htail) hsum

theorem rank_at_most_two_uses_all_slots (components : List ComponentCounts)
    (hvalid : ∀ component ∈ components, admissible component)
    (hsmall : rankSum components ≤ 2) : slotSum components ≤ rankSum components := by
  have hbound := small_total_bound components hvalid (by omega)
  have hnot : rankSum components ≠ 3 := by omega
  simpa [smallBudget, hnot] using hbound

theorem separating_failure_needs_rank_three (components : List ComponentCounts)
    (hvalid : ∀ component ∈ components, admissible component)
    (hfailure : rankSum components < slotSum components) : 3 ≤ rankSum components := by
  by_cases hsmall : rankSum components ≤ 2
  · have hbound := rank_at_most_two_uses_all_slots components hvalid hsmall
    omega
  · omega

theorem separating_failure_needs_charge_four (components : List ComponentCounts) (charge : Nat)
    (hvalid : ∀ component ∈ components, admissible component)
    (hcertificateFails : rankSum components < charge)
    (htargetSurvives : charge ≤ slotSum components) : 4 ≤ charge := by
  have hrank := separating_failure_needs_rank_three components hvalid (by omega)
  omega

theorem charge_four_numeric_shape (components : List ComponentCounts)
    (hvalid : ∀ component ∈ components, admissible component)
    (hcertificateFails : rankSum components < 4)
    (htargetSurvives : 4 ≤ slotSum components) :
    rankSum components = 3 ∧ slotSum components = 4 := by
  have hrank := separating_failure_needs_rank_three components hvalid (by omega)
  have hbound := small_total_bound components hvalid (by omega)
  have hexact : rankSum components = 3 := by omega
  rw [hexact] at hbound
  simp [smallBudget] at hbound
  omega

end SubQuorum.LowChargeRankBarrier
