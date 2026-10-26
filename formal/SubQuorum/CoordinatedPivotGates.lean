set_option autoImplicit false

namespace SubQuorum.CoordinatedPivotGates

variable {I : Type}

/-- All members of a finite serial corridor must be open. -/
def allOn : List I → (I → Bool) → Bool
  | [], _ => true
  | i :: rest, opened => opened i && allOn rest opened

theorem allOn_iff (gates : List I) (opened : I → Bool) :
    allOn gates opened = true ↔ ∀ i, i ∈ gates → opened i = true := by
  induction gates with
  | nil => simp [allOn]
  | cons i rest ih => simp [allOn, ih]

/-- One old source is paid; the corridor supplies one further payment. -/
def value (gates : List I) (opened : I → Bool) : Nat :=
  if allOn gates opened then 2 else 1

theorem value_two_iff (gates : List I) (opened : I → Bool) :
    value gates opened = 2 ↔ ∀ i, i ∈ gates → opened i = true := by
  rw [← allOn_iff]
  cases h : allOn gates opened <;> simp [value, h]

theorem missing_gate_value_one (gates : List I) (opened : I → Bool)
    (i : I) (hi : i ∈ gates) (closed : opened i = false) :
    value gates opened = 1 := by
  have no : allOn gates opened ≠ true := by
    intro h
    have yes := (allOn_iff gates opened).mp h i hi
    rw [closed] at yes
    exact Bool.false_ne_true yes
  cases h : allOn gates opened with
  | false => simp [value, h]
  | true => exact False.elim (no h)

theorem value_monotone (gates : List I) (opened later : I → Bool)
    (extension : ∀ i, i ∈ gates → opened i = true → later i = true) :
    value gates opened ≤ value gates later := by
  cases ho : allOn gates opened with
  | false =>
    cases hl : allOn gates later <;> simp [value, ho, hl]
  | true =>
    have hl : allOn gates later = true :=
      (allOn_iff gates later).mpr (fun i hi => extension i hi ((allOn_iff gates opened).mp ho i hi))
    simp [value, ho, hl]

/-- Two different missing gates give a strict submodularity violation.
This is an arbitrary finite-list theorem, not a check at a fixed n. -/
theorem strict_submodularity_violation [DecidableEq I]
    (gates : List I) (left right : I) (hl : left ∈ gates) (hr : right ∈ gates)
    (different : left ≠ right) :
    let s := fun i => decide (i ≠ left)
    let t := fun i => decide (i ≠ right)
    value gates (fun i => s i || t i) + value gates (fun i => s i && t i) >
      value gates s + value gates t := by
  dsimp only
  have hs : value gates (fun i => decide (i ≠ left)) = 1 :=
    missing_gate_value_one gates _ left hl (by simp)
  have ht : value gates (fun i => decide (i ≠ right)) = 1 :=
    missing_gate_value_one gates _ right hr (by simp)
  have hu : value gates (fun i => decide (i ≠ left) || decide (i ≠ right)) = 2 := by
    apply (value_two_iff gates _).mpr
    intro i _
    by_cases h : i = left
    · subst i
      simp [different]
    · simp [h]
  have hm : value gates (fun i => decide (i ≠ left) && decide (i ≠ right)) = 1 :=
    missing_gate_value_one gates _ left hl (by simp)
  rw [hs, ht, hu, hm]
  decide

end SubQuorum.CoordinatedPivotGates

#print axioms SubQuorum.CoordinatedPivotGates.allOn_iff
#print axioms SubQuorum.CoordinatedPivotGates.value_two_iff
#print axioms SubQuorum.CoordinatedPivotGates.missing_gate_value_one
#print axioms SubQuorum.CoordinatedPivotGates.value_monotone
#print axioms SubQuorum.CoordinatedPivotGates.strict_submodularity_violation
