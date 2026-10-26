import Std.Tactic

set_option autoImplicit false

namespace SubQuorum.UniformOpeningGuard

/-- An antitone incidence family which loses nothing between its extremes
is constant at every intermediate state. -/
theorem antitone_two_state_constant {State Item : Type}
    (le : State → State → Prop) (lo hi : State) (W : State → Item → Prop)
    (lower : ∀ s, le lo s) (upper : ∀ s, le s hi)
    (antitone : ∀ a b, le a b → ∀ x, W b x → W a x)
    (guard : ∀ x, W lo x → W hi x) :
    ∀ s x, W s x ↔ W lo x := by
  intro s x
  constructor
  · exact antitone lo s (lower s) x
  · intro old
    exact antitone s hi (upper s) x (guard x old)

/-- Horizontal incidences increase and vertical incidences decrease.
A single full endpoint inclusion then certifies all ordered state pairs. -/
theorem axis_two_state_monotone {State Item : Type}
    (le : State → State → Prop) (lo hi : State) (W : State → Item → Prop)
    (horizontal : Item → Bool) (lower : ∀ s, le lo s) (upper : ∀ s, le s hi)
    (hinc : ∀ a b, le a b → ∀ x, horizontal x = true → W a x → W b x)
    (vdec : ∀ a b, le a b → ∀ x, horizontal x = false → W b x → W a x)
    (guard : ∀ x, W lo x → W hi x) :
    ∀ a b, le a b → ∀ x, W a x → W b x := by
  intro a b hab x hx
  cases axis : horizontal x with
  | true => exact hinc a b hab x axis hx
  | false =>
    have old := vdec lo a (lower a) x axis hx
    exact vdec b hi (upper b) x axis (guard x old)

theorem guard_iff_all_state_monotonicity {State Item : Type}
    (le : State → State → Prop) (lo hi : State) (W : State → Item → Prop)
    (horizontal : Item → Bool) (lower : ∀ s, le lo s) (upper : ∀ s, le s hi)
    (hinc : ∀ a b, le a b → ∀ x, horizontal x = true → W a x → W b x)
    (vdec : ∀ a b, le a b → ∀ x, horizontal x = false → W b x → W a x) :
    (∀ x, W lo x → W hi x) ↔
      (∀ a b, le a b → ∀ x, W a x → W b x) := by
  constructor
  · exact axis_two_state_monotone le lo hi W horizontal lower upper hinc vdec
  · intro monotone x old
    exact monotone lo hi (lower hi) x old

/-- Rejection supplies a witness on the losing axis, not an invented
deficit in the full numerical grid inequality. -/
theorem endpoint_loss_is_vertical {State Item : Type}
    (le : State → State → Prop) (lo hi : State) (W : State → Item → Prop)
    (horizontal : Item → Bool) (ordered : le lo hi)
    (hinc : ∀ a b, le a b → ∀ x, horizontal x = true → W a x → W b x)
    (x : Item) (old : W lo x) (missing : ¬ W hi x) : horizontal x = false := by
  cases axis : horizontal x with
  | false => rfl
  | true => exact False.elim (missing (hinc lo hi ordered x axis old))

end SubQuorum.UniformOpeningGuard

#print axioms SubQuorum.UniformOpeningGuard.antitone_two_state_constant
#print axioms SubQuorum.UniformOpeningGuard.axis_two_state_monotone
#print axioms SubQuorum.UniformOpeningGuard.guard_iff_all_state_monotonicity
#print axioms SubQuorum.UniformOpeningGuard.endpoint_loss_is_vertical
