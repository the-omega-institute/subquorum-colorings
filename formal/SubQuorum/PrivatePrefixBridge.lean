set_option autoImplicit false

namespace SubQuorum.PrivatePrefixBridge

/-- Two distinct private pre/post witnesses allow a receiver to keep its
already used unit and add exactly one unused unit, on the opposite side.
Privacy says that either witness, if used already, must be the receiver's
own assigned unit. The old unit may lie on either side or equal a witness. -/
theorem retain_old_unit_add_fresh
    {Resource : Type} [DecidableEq Resource]
    (used before after : Resource → Prop) (old pre post : Resource)
    (_old_used : used old)
    (old_side : before old ∨ after old)
    (pre_side : before pre) (post_side : after post)
    (distinct : pre ≠ post)
    (private_pre : used pre → pre = old)
    (private_post : used post → post = old) :
    ∃ fresh, ¬ used fresh ∧ fresh ≠ old ∧
      ((before old ∧ after fresh) ∨ (before fresh ∧ after old)) := by
  by_cases hp : old = pre
  · refine ⟨post, ?_, ?_, Or.inl ⟨?_, post_side⟩⟩
    · intro hu
      exact distinct (hp.symm.trans (private_post hu).symm)
    · intro h
      exact distinct (hp.symm.trans h.symm)
    · exact hp.symm ▸ pre_side
  · by_cases hs : old = post
    · refine ⟨pre, ?_, ?_, Or.inr ⟨pre_side, ?_⟩⟩
      · intro hu
        exact distinct ((private_pre hu).trans hs)
      · intro h
        exact hp h.symm
      · exact hs.symm ▸ post_side
    · cases old_side with
      | inl hb =>
        refine ⟨post, ?_, ?_, Or.inl ⟨hb, post_side⟩⟩
        · intro hu
          exact hs (private_post hu).symm
        · intro h
          exact hs h.symm
      | inr ha =>
        refine ⟨pre, ?_, ?_, Or.inr ⟨pre_side, ha⟩⟩
        · intro hu
          exact hp (private_pre hu).symm
        · intro h
          exact hp h.symm

end SubQuorum.PrivatePrefixBridge

#print axioms SubQuorum.PrivatePrefixBridge.retain_old_unit_add_fresh
