set_option autoImplicit false

namespace SubQuorum.MixedZeroCorridors

/-- Saturate the opposite-target cuts. Geometry supplies completeness in
this saturated state and soundness of final-corridor prerequisites at every
state. If those prerequisites avoid all saturated cuts, monotonicity makes
the final corridors complete already in the original state. -/
theorem final_corridor_projection
    {Gate Route : Type}
    (support : (Gate → Prop) → Prop) (cut : Gate → Prop)
    (needed : Route → Gate → Prop)
    (monotone : ∀ x y, (∀ i, x i → y i) → support x → support y)
    (avoids : ∀ r i, needed r i → cut i → False)
    (sound : ∀ x : Gate → Prop, (∃ r, ∀ i, needed r i → x i) → support x)
    (complete_after_cuts : ∀ x : Gate → Prop, support (fun i => x i ∨ cut i) →
      ∃ r, ∀ i, needed r i → x i ∨ cut i)
    (state : Gate → Prop) :
    support state ↔ ∃ r, ∀ i, needed r i → state i := by
  constructor
  · intro accessible
    have saturated := monotone state (fun i => state i ∨ cut i)
      (fun _ hi => Or.inl hi) accessible
    obtain ⟨r, hr⟩ := complete_after_cuts state saturated
    refine ⟨r, ?_⟩
    intro i hi
    cases hr i hi with
    | inl hs => exact hs
    | inr hc => exact False.elim (avoids r i hi hc)
  · exact sound state

/-- Fixing all positive-capacity gates leaves monotonicity on the remaining
zero-capacity coordinates. The embedding need only preserve state inclusion;
no incidence from two different branch resource pools is ever combined. -/
theorem monotonicity_on_fixed_branch
    {Global Local : Type}
    (support : (Global → Prop) → Prop)
    (embed : (Local → Prop) → Global → Prop)
    (monotone : ∀ x y, (∀ i, x i → y i) → support x → support y)
    (embed_monotone : ∀ x y, (∀ i, x i → y i) →
      ∀ j, embed x j → embed y j) :
    ∀ x y, (∀ i, x i → y i) → support (embed x) → support (embed y) := by
  intro x y h old
  exact monotone (embed x) (embed y) (embed_monotone x y h) old

end SubQuorum.MixedZeroCorridors

#print axioms SubQuorum.MixedZeroCorridors.final_corridor_projection
#print axioms SubQuorum.MixedZeroCorridors.monotonicity_on_fixed_branch
