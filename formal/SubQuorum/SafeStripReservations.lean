import Std

set_option autoImplicit false

namespace SubQuorum.SafeStripReservations

structure ComponentTransition where
  removed : Nat
  rankBefore : Nat
  rankAfter : Nat
  weightedBefore : Nat
  weightedAfter : Nat
  mixedAfter : Nat
  oddBefore : Nat
  oddAfter : Nat
  useWeighted : Bool

def admissible (component : ComponentTransition) : Prop :=
  component.rankBefore ≤ component.removed+component.rankAfter ∧
  component.rankAfter ≤ component.mixedAfter ∧
  component.weightedAfter ≤ component.mixedAfter ∧
  2*component.weightedBefore+component.oddBefore =
    2*(component.removed+component.weightedAfter)+component.oddAfter ∧
  (if component.useWeighted then component.rankBefore ≤ component.weightedBefore
    else component.weightedBefore ≤ component.rankBefore)

def beforeCredits (component : ComponentTransition) : Nat :=
  if component.useWeighted then component.weightedBefore else component.rankBefore

def afterCredits (component : ComponentTransition) : Nat :=
  component.removed+component.mixedAfter

def countedOddBefore (component : ComponentTransition) : Nat :=
  if component.useWeighted then component.oddBefore else 0

def countedOddAfter (component : ComponentTransition) : Nat :=
  if component.useWeighted then component.oddAfter else 0

def recoverySurplus (component : ComponentTransition) : Nat :=
  if component.useWeighted then component.mixedAfter-component.weightedAfter
    else afterCredits component-component.rankBefore

def total (value : ComponentTransition → Nat) : List ComponentTransition → Nat
  | [] => 0
  | component :: rest => value component+total value rest

theorem old_branch_attains_max (component : ComponentTransition)
    (hvalid : admissible component) :
    beforeCredits component = max component.rankBefore component.weightedBefore := by
  rcases hvalid with ⟨_, _, _, _, hbranch⟩
  cases hchoice : component.useWeighted <;>
    simp [beforeCredits, hchoice] at hbranch ⊢ <;> omega

theorem component_parity_budget (component : ComponentTransition)
    (hvalid : admissible component) :
    2*beforeCredits component+countedOddBefore component ≤
      2*afterCredits component+countedOddAfter component := by
  rcases hvalid with ⟨hrank, hafterRank, hafterWeighted, hhandshake, _⟩
  cases hchoice : component.useWeighted <;>
    simp [beforeCredits, afterCredits, countedOddBefore, countedOddAfter, hchoice] <;>
    omega

theorem rank_branch_preserves_budget (component : ComponentTransition)
    (hvalid : admissible component) (hchoice : component.useWeighted = false) :
    beforeCredits component ≤ afterCredits component := by
  have hbound := component_parity_budget component hvalid
  simp [countedOddBefore, countedOddAfter, hchoice] at hbound
  omega

theorem component_parity_preserves_budget (component : ComponentTransition)
    (hvalid : admissible component)
    (hparity : countedOddAfter component ≤ countedOddBefore component) :
    beforeCredits component ≤ afterCredits component := by
  have hbound := component_parity_budget component hvalid
  omega

theorem component_exact_budget (component : ComponentTransition)
    (hvalid : admissible component) :
    2*afterCredits component+countedOddAfter component =
      2*beforeCredits component+countedOddBefore component+2*recoverySurplus component := by
  rcases hvalid with ⟨hrank, hafterRank, hafterWeighted, hhandshake, _⟩
  cases hchoice : component.useWeighted <;>
    simp [beforeCredits, afterCredits, countedOddBefore, countedOddAfter,
      recoverySurplus, hchoice] <;> omega

theorem batch_parity_budget (components : List ComponentTransition)
    (hvalid : ∀ component ∈ components, admissible component) :
    2*total beforeCredits components+total countedOddBefore components ≤
      2*total afterCredits components+total countedOddAfter components := by
  induction components with
  | nil => simp [total]
  | cons component rest inductionHypothesis =>
      have hhead := component_parity_budget component (hvalid component (by simp))
      have htail := inductionHypothesis (by
        intro other hmember
        exact hvalid other (by simp [hmember]))
      simp only [total]
      omega

theorem aggregate_parity_preserves_budget (components : List ComponentTransition)
    (hvalid : ∀ component ∈ components, admissible component)
    (hparity : total countedOddAfter components ≤ total countedOddBefore components) :
    total beforeCredits components ≤ total afterCredits components := by
  have hbound := batch_parity_budget components hvalid
  omega

theorem batch_exact_budget (components : List ComponentTransition)
    (hvalid : ∀ component ∈ components, admissible component) :
    2*total afterCredits components+total countedOddAfter components =
      2*total beforeCredits components+total countedOddBefore components+
        2*total recoverySurplus components := by
  induction components with
  | nil => simp [total]
  | cons component rest inductionHypothesis =>
      have hhead := component_exact_budget component (hvalid component (by simp))
      have htail := inductionHypothesis (by
        intro other hmember
        exact hvalid other (by simp [hmember]))
      simp only [total]
      omega

theorem exact_preservation_criterion (components : List ComponentTransition)
    (hvalid : ∀ component ∈ components, admissible component) :
    total beforeCredits components ≤ total afterCredits components ↔
      total countedOddAfter components ≤ total countedOddBefore components+
        2*total recoverySurplus components := by
  have hexact := batch_exact_budget components hvalid
  omega

theorem preserve_existing_coverage (components : List ComponentTransition)
    (reserved charge : Nat)
    (hvalid : ∀ component ∈ components, admissible component)
    (hparity : total countedOddAfter components ≤ total countedOddBefore components)
    (hcoverage : charge ≤ reserved+total beforeCredits components) :
    charge ≤ reserved+total afterCredits components := by
  have hbound := aggregate_parity_preserves_budget components hvalid hparity
  omega

end SubQuorum.SafeStripReservations
