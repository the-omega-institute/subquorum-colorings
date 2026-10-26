set_option autoImplicit false

namespace SubQuorum.DestructiveExchangeAllocation

variable {S R : Type}

/-- A token represents one disjoint group of withdrawn old units. -/
def Proxy (old : S → R → Prop) (enabled : R → Prop) (target : R → S)
    (s : S) (r : R) : Prop := old s r ∨ (enabled r ∧ target r = s)

/-- An activated token supports its new target; an inactive token retains
its old incidence. This implication form needs no excluded middle. -/
def Physical (old : S → R → Prop) (selected : R → Prop) (target : R → S)
    (s : S) (r : R) : Prop :=
  (selected r → target r = s) ∧ (¬ selected r → old s r)

/-- Activate just those tokens allocated directly to their enabled target. -/
def Chosen (enabled : R → Prop) (target : R → S)
    (paid : S → Prop) (assignment : S → R) (r : R) : Prop :=
  ∃ s, paid s ∧ assignment s = r ∧ enabled r ∧ target r = s

theorem chosen_enabled (enabled : R → Prop) (target : R → S)
    (paid : S → Prop) (assignment : S → R) :
    ∀ r, Chosen enabled target paid assignment r → enabled r := by
  intro r h
  obtain ⟨s,_,_,he,_⟩ := h
  exact he

/-- One source's one assigned token activates at most one action for it,
even when several enabled actions have that same target. -/
theorem chosen_targets_distinct (enabled : R → Prop) (target : R → S)
    (paid : S → Prop) (assignment : S → R) (r q : R)
    (hr : Chosen enabled target paid assignment r)
    (hq : Chosen enabled target paid assignment q)
    (same : target r = target q) : r = q := by
  obtain ⟨s,_,hs,_,ts⟩ := hr
  obtain ⟨t,_,ht,_,tt⟩ := hq
  have st : s = t := ts.symm.trans (same.trans tt)
  exact hs.symm.trans ((congrArg assignment st).trans ht)

/-- An injective proxy allocation reconstructs a simultaneous physical
choice with exactly the SAME paid source identities and assigned tokens.
Injectivity forbids another source from spending an activated old token. -/
theorem proxy_to_physical (old : S → R → Prop) (enabled : R → Prop)
    (target : R → S) (paid : S → Prop) (assignment : S → R)
    (injective : ∀ s t, paid s → paid t → assignment s = assignment t → s = t)
    (valid : ∀ s, paid s → Proxy old enabled target s (assignment s)) :
    ∀ s, paid s → Physical old (Chosen enabled target paid assignment)
      target s (assignment s) := by
  intro s hs
  constructor
  · intro selected
    obtain ⟨t,ht,equal,_,targeted⟩ := selected
    have ts : t = s := injective t s ht hs equal
    exact targeted.trans ts
  · intro inactive
    rcases valid s hs with previous | activated
    · exact previous
    · exact False.elim (inactive ⟨s,hs,rfl,activated.1,activated.2⟩)

/-- A physical allocation projects to the enabled proxy without changing
the assignment or source identities. Finite selected sets provide cases. -/
theorem physical_to_proxy (old : S → R → Prop) (enabled selected : R → Prop)
    (target : R → S) (paid : S → Prop) (assignment : S → R)
    (subset : ∀ r, selected r → enabled r)
    (cases : ∀ r, selected r ∨ ¬ selected r)
    (valid : ∀ s, paid s → Physical old selected target s (assignment s)) :
    ∀ s, paid s → Proxy old enabled target s (assignment s) := by
  intro s hs
  rcases cases (assignment s) with active | inactive
  · exact Or.inr ⟨subset (assignment s) active,(valid s hs).1 active⟩
  · exact Or.inl ((valid s hs).2 inactive)

end SubQuorum.DestructiveExchangeAllocation

#print axioms SubQuorum.DestructiveExchangeAllocation.chosen_enabled
#print axioms SubQuorum.DestructiveExchangeAllocation.chosen_targets_distinct
#print axioms SubQuorum.DestructiveExchangeAllocation.proxy_to_physical
#print axioms SubQuorum.DestructiveExchangeAllocation.physical_to_proxy
