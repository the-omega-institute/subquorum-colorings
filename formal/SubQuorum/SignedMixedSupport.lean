set_option autoImplicit false

namespace SubQuorum.SignedMixedSupport

def termTrue {Gate : Type} (positive negative state : Gate → Prop) : Prop :=
  (∀ i, positive i → state i) ∧ (∀ i, negative i → ¬ state i)

def dnfTrue {Gate Term : Type} (positive negative : Term → Gate → Prop)
    (state : Gate → Prop) : Prop :=
  ∃ t, termTrue (positive t) (negative t) state

/-- Once a consistent signed DNF is known to be increasing in the changed
gate set, dropping all negative literals is exact, at every state. -/
theorem monotone_dnf_positive_retraction
    {Gate Term : Type} (positive negative : Term → Gate → Prop)
    (consistent : ∀ t i, positive t i → negative t i → False)
    (monotone : ∀ x y : Gate → Prop, (∀ i, x i → y i) →
      dnfTrue positive negative x → dnfTrue positive negative y)
    (state : Gate → Prop) :
    dnfTrue positive negative state ↔ ∃ t, ∀ i, positive t i → state i := by
  constructor
  · intro h
    obtain ⟨t, hp, _⟩ := h
    exact ⟨t, hp⟩
  · intro h
    obtain ⟨t, hp⟩ := h
    have smallest : dnfTrue positive negative (positive t) := by
      refine ⟨t, ?_, ?_⟩
      · intro i hi
        exact hi
      · intro i hn hi
        exact consistent t i hi hn
    exact monotone (positive t) state hp smallest

/-- A term true before a single 0-to-1 gate change can disappear only if it
contains the negative literal of that same gate. -/
theorem losing_term_contains_switched_negative
    {Gate : Type} [DecidableEq Gate]
    (positive negative before after : Gate → Prop)
    [DecidablePred negative] (gate : Gate)
    (growing : ∀ i, before i → after i)
    (other_unchanged : ∀ i, i ≠ gate → after i → before i)
    (old_true : termTrue positive negative before)
    (new_false : ¬ termTrue positive negative after) :
    negative gate := by
  by_cases hn : negative gate
  · exact hn
  · apply False.elim
    apply new_false
    constructor
    · intro i hp
      exact growing i (old_true.1 i hp)
    · intro i hi ha
      by_cases he : i = gate
      · subst i
        exact hn hi
      · exact old_true.2 i hi (other_unchanged i he ha)

end SubQuorum.SignedMixedSupport

#print axioms SubQuorum.SignedMixedSupport.monotone_dnf_positive_retraction
#print axioms SubQuorum.SignedMixedSupport.losing_term_contains_switched_negative
