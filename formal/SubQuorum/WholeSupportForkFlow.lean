import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.WholeSupportForkFlow

/-- Distinct integral paths entering one beta must use its two different
physical BP tips. Their number is at most two, without any graph-size bound. -/
theorem two_BP_entries_bound (n : Nat) (entry : Fin n → Fin 2)
    (distinct : Function.Injective entry) : n≤2 := by
  by_cases small : n≤2
  · exact small
  ·
    have big : 3≤n := by omega
    let a : Fin n := ⟨0, by omega⟩
    let b : Fin n := ⟨1, by omega⟩
    let c : Fin n := ⟨2, by omega⟩
    have ha := (entry a).isLt
    have hb := (entry b).isLt
    have hc := (entry c).isLt
    have collide : (entry a).val=(entry b).val ∨
        (entry a).val=(entry c).val ∨ (entry b).val=(entry c).val := by omega
    rcases collide with h | h | h
    · have same := congrArg Fin.val (distinct (Fin.ext h))
      change 0=1 at same
      omega
    · have same := congrArg Fin.val (distinct (Fin.ext h))
      change 0=2 at same
      omega
    · have same := congrArg Fin.val (distinct (Fin.ext h))
      change 1=2 at same
      omega

/-- A private whole-beta sink unused by the incoming paths is a fresh
resource. Reassigning one path to it preserves global resource injectivity. -/
theorem replace_by_unused_resource_injective {Source Resource : Type}
    [DecidableEq Source] (allocation : Source → Resource)
    (distinct : Function.Injective allocation) (chosen : Source) (fresh : Resource)
    (unused : ∀ x, allocation x≠fresh) :
    Function.Injective (fun x => if x=chosen then fresh else allocation x) := by
  intro x y same
  by_cases hx : x=chosen <;> by_cases hy : y=chosen
  · exact hx.trans hy.symm
  · simp only [hx, if_true, hy, if_false] at same
    exact False.elim (unused y same.symm)
  · simp only [hx, if_false, hy, if_true] at same
    exact False.elim (unused x same)
  · simp only [hx, if_false, hy, if_false] at same
    exact distinct same

/-- The normalization introduces no interval or other resource besides the
fresh beta identity. It may release an interval; it need not retain it. -/
theorem replacement_creates_no_other_resource {Source Resource : Type}
    [DecidableEq Source] (allocation : Source → Resource) (chosen x : Source)
    (fresh other : Resource) (different : other≠fresh)
    (used : (if x=chosen then fresh else allocation x)=other) :
    allocation x=other := by
  by_cases same : x=chosen
  · simp only [same, if_true] at used
    exact False.elim (different used.symm)
  · simpa only [same, if_false] using used

/-- Every nonempty beta receiver with at most two entering paths can be
normalized to one whole-beta payment and at most one interval payment. -/
theorem positive_beta_normalization (paths whole intervals : Nat)
    (positive : 1≤paths) (ports : paths≤2) (oneWhole : whole≤1)
    (inventory : whole+intervals=paths) :
    ∃ newWhole newIntervals : Nat,
      newWhole=1 ∧ newIntervals≤1 ∧ newIntervals≤intervals ∧
      newWhole+newIntervals=paths := by
  refine ⟨1, paths-1, rfl, ?_, ?_, ?_⟩ <;> omega

/-- A whole beta and an original interval remain different resource types,
even if an implementation happens to give them the same numeric index. -/
theorem beta_interval_identities_distinct {Beta Interval : Type}
    (b : Beta) (j : Interval) :
    (Sum.inl b : Sum Beta Interval)≠Sum.inr j := by
  intro same
  cases same

#print axioms two_BP_entries_bound
#print axioms replace_by_unused_resource_injective
#print axioms replacement_creates_no_other_resource
#print axioms positive_beta_normalization
#print axioms beta_interval_identities_distinct

end SubQuorum.WholeSupportForkFlow
