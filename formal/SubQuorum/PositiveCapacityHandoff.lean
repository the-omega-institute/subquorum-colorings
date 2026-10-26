import Std.Tactic

set_option autoImplicit false

namespace SubQuorum.PositiveCapacityHandoff

/-- The closed phase is antitone. Preserving the bottom incidence at the
largest closed state forces constancy throughout that phase. -/
theorem closed_phase_constant {State : Type}
    (le : State → State → Prop) (opened : State → Bool) (W : State → Prop) (lo shut : State)
    (loClosed : opened lo = false) (shutClosed : opened shut = false)
    (lower : ∀ s, opened s = false → le lo s)
    (upper : ∀ s, opened s = false → le s shut)
    (dec : ∀ a b, le a b → opened a = false → opened b = false → W b → W a)
    (guard : W lo → W shut) :
    ∀ s, opened s = false → (W s ↔ W lo) := by
  intro s hs
  constructor
  · exact dec lo s (lower s hs) loClosed hs
  · intro old
    exact dec s shut (upper s hs) hs shutClosed (guard old)

/-- A constant closed phase hands its incidence to the smallest open state.
The open phase is monotone, so every ordered pair preserves the incidence. -/
theorem phase_guard_monotone {State : Type}
    (le : State → State → Prop) (opened : State → Bool) (W : State → Prop) (lo shut turn : State)
    (loClosed : opened lo = false) (shutClosed : opened shut = false) (turnOpen : opened turn = true)
    (lower : ∀ s, opened s = false → le lo s)
    (upper : ∀ s, opened s = false → le s shut)
    (openLower : ∀ s, opened s = true → le turn s)
    (opening : ∀ a b, le a b → opened a = true → opened b)
    (dec : ∀ a b, le a b → opened a = false → opened b = false → W b → W a)
    (inc : ∀ a b, le a b → opened a = true → opened b = true → W a → W b)
    (closedGuard : W lo → W shut) (handoff : W lo → W turn) :
    ∀ a b, le a b → W a → W b := by
  have constant := closed_phase_constant le opened W lo shut loClosed shutClosed lower upper dec closedGuard
  intro a b hab ha
  cases oa : opened a with
  | true => exact inc a b hab oa (opening a b hab oa) ha
  | false =>
    have old := (constant a oa).mp ha
    cases ob : opened b with
    | true => exact inc turn b (openLower b ob) turnOpen ob (handoff old)
    | false => exact (constant b ob).mpr old

/-- The two critical guards are necessary and sufficient; all-state
monotonicity supplies both tests from the globally least state. -/
theorem critical_guards_iff_all_states {State : Type}
    (le : State → State → Prop) (opened : State → Bool) (W : State → Prop) (lo shut turn : State)
    (loClosed : opened lo = false) (shutClosed : opened shut = false) (turnOpen : opened turn = true)
    (bottom : ∀ s, le lo s)
    (upper : ∀ s, opened s = false → le s shut)
    (openLower : ∀ s, opened s = true → le turn s)
    (opening : ∀ a b, le a b → opened a = true → opened b)
    (dec : ∀ a b, le a b → opened a = false → opened b = false → W b → W a)
    (inc : ∀ a b, le a b → opened a = true → opened b = true → W a → W b) :
    ((W lo → W shut) ∧ (W lo → W turn)) ↔
      (∀ a b, le a b → W a → W b) := by
  constructor
  · intro guards
    exact phase_guard_monotone le opened W lo shut turn loClosed shutClosed turnOpen
      (fun s _ => bottom s) upper openLower opening dec inc guards.1 guards.2
  · intro monotone
    exact ⟨monotone lo shut (bottom shut), monotone lo turn (bottom turn)⟩

end SubQuorum.PositiveCapacityHandoff

#print axioms SubQuorum.PositiveCapacityHandoff.closed_phase_constant
#print axioms SubQuorum.PositiveCapacityHandoff.phase_guard_monotone
#print axioms SubQuorum.PositiveCapacityHandoff.critical_guards_iff_all_states
