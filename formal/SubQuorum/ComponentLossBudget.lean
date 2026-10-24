import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.ComponentLossBudget

def possibleDeltas : List Int → List Int
  | [] => [0]
  | change :: changes => possibleDeltas changes ++
      (possibleDeltas changes).map (fun total => change+total)

def leastDelta : List Int → Int
  | [] => 0
  | change :: changes => min 0 change+leastDelta changes

def aggregateLoss (changes : List Int) : Int := -leastDelta changes

theorem the_least_delta_is_attained (changes : List Int) :
    leastDelta changes ∈ possibleDeltas changes := by
  induction changes with
  | nil => simp [possibleDeltas, leastDelta]
  | cons change changes inductionHypothesis =>
    by_cases hnegative : change < 0
    · have hminimum : min 0 change = change := by omega
      simp only [possibleDeltas, leastDelta, hminimum, List.mem_append]
      exact Or.inr (List.mem_map.mpr ⟨leastDelta changes, inductionHypothesis, rfl⟩)
    · have hminimum : min 0 change = 0 := by omega
      simp only [possibleDeltas, leastDelta, hminimum, Int.zero_add, List.mem_append]
      exact Or.inl inductionHypothesis

theorem every_possible_delta_is_at_least_the_least
    (changes : List Int) (total : Int) (hpossible : total ∈ possibleDeltas changes) :
    leastDelta changes ≤ total := by
  induction changes generalizing total with
  | nil =>
    have hequal : total = 0 := by simpa [possibleDeltas] using hpossible
    simp [leastDelta, hequal]
  | cons change changes inductionHypothesis =>
    simp only [possibleDeltas, List.mem_append, List.mem_map] at hpossible
    rcases hpossible with hretained | ⟨smaller, hsmaller, hequal⟩
    · have hlower := inductionHypothesis total hretained
      have hminimum : min 0 change ≤ 0 := by omega
      simp only [leastDelta]
      omega
    · have hlower := inductionHypothesis smaller hsmaller
      have hminimum : min 0 change ≤ change := by omega
      simp only [leastDelta]
      omega

theorem the_least_delta_is_nonpositive (changes : List Int) :
    leastDelta changes ≤ 0 := by
  induction changes with
  | nil => simp [leastDelta]
  | cons change changes inductionHypothesis =>
    have hminimum : min 0 change ≤ 0 := by omega
    simp only [leastDelta]
    omega

theorem aggregate_loss_is_nonnegative (changes : List Int) :
    0 ≤ aggregateLoss changes := by
  have hleast := the_least_delta_is_nonpositive changes
  unfold aggregateLoss
  omega

theorem persistent_activation_bounds_all_losses_at_once
    (changes : List Int) (reserve activated : Int)
    (hfloor : ∀ total, total ∈ possibleDeltas changes →
      activated ≤ 2*(reserve+total)) :
    2*aggregateLoss changes ≤ 2*reserve-activated := by
  have hleast := hfloor (leastDelta changes) (the_least_delta_is_attained changes)
  unfold aggregateLoss
  omega

theorem all_subextension_margins_are_nonnegative_iff
    (changes : List Int) (reserve positive marked : Int) :
    (∀ total, total ∈ possibleDeltas changes → 0 ≤ positive+reserve+total-marked) ↔
      aggregateLoss changes ≤ positive+reserve-marked := by
  constructor
  · intro hnonnegative
    have hleast := hnonnegative (leastDelta changes) (the_least_delta_is_attained changes)
    unfold aggregateLoss
    omega
  · intro hbudget total hpossible
    have hleast := every_possible_delta_is_at_least_the_least changes total hpossible
    unfold aggregateLoss at hbudget
    omega

end SubQuorum.ComponentLossBudget
