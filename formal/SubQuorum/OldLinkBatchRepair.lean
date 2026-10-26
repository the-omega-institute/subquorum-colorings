set_option autoImplicit false

namespace SubQuorum.OldLinkBatchRepair

/-- Aggregating support along disjoint old primitives cannot turn a physical
two-owner resource into three distinct request credits. -/
theorem disjoint_aggregation_preserves_two_users
    {Owner Request Resource : Type}
    (member : Owner → Request → Prop) (support : Resource → Owner → Prop)
    (disjoint : ∀ o d e, member o d → member o e → d = e)
    (capacity : ∀ j x y z, support j x → support j y → support j z →
      x = y ∨ x = z ∨ y = z)
    (j : Resource) (d e f : Request)
    (hd : ∃ o, member o d ∧ support j o)
    (he : ∃ o, member o e ∧ support j o)
    (hf : ∃ o, member o f ∧ support j o) :
    d = e ∨ d = f ∨ e = f := by
  obtain ⟨x, hxd, hx⟩ := hd
  obtain ⟨y, hye, hy⟩ := he
  obtain ⟨z, hzf, hz⟩ := hf
  rcases capacity j x y z hx hy hz with h | h | h
  · subst y
    exact Or.inl (disjoint x d e hxd hye)
  · subst z
    exact Or.inr (Or.inl (disjoint x d f hxd hzf))
  · subst z
    exact Or.inr (Or.inr (disjoint y e f hye hzf))

/-- The two fork arms meet only at beta. A proper prefix of either arm
which excludes beta can coexist with the other full beta arm. -/
theorem proper_prefix_disjoint_from_other_arm
    {Owner : Type} (left right initialPart : Owner → Prop) (beta : Owner)
    (shared : ∀ o, left o → right o → o = beta)
    (subset : ∀ o, initialPart o → left o)
    (excludes : ¬ initialPart beta) :
    ∀ o, initialPart o → ¬ right o := by
  intro o hp hr
  have equal := shared o (subset o hp) hr
  subst o
  exact excludes hp

end SubQuorum.OldLinkBatchRepair

#print axioms SubQuorum.OldLinkBatchRepair.disjoint_aggregation_preserves_two_users
#print axioms SubQuorum.OldLinkBatchRepair.proper_prefix_disjoint_from_other_arm
