import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.FrozenForkSurplus

/-- Actual two-witness freezing, truncated at a finite number of rounds.
`adj` is the nonmate-neighbor relation. Each retained endpoint witness
requires its actual mate to have frozen in an earlier round. -/
def frozenBy {V : Type} (P T : V → Prop) (mate : V → V)
    (adj : V → V → Prop) : Nat → V → Prop
  | 0, _ => False
  | n + 1, v => P v ∧ ∃ a b, a ≠ b ∧ adj v a ∧ adj v b ∧
      (T a ∨ (P a ∧ frozenBy P T mate adj n (mate a))) ∧
      (T b ∨ (P b ∧ frozenBy P T mate adj n (mate b)))

/-- A closed dependency set has no first freezing round. The hypothesis
says any two potential witnesses include an endpoint whose mate is blocked. -/
theorem closed_set_never_freezes {V : Type} (P T U : V → Prop)
    (mate : V → V) (adj : V → V → Prop)
    (closed : ∀ v a b, U v → a ≠ b → adj v a → adj v b →
      (T a ∨ P a) → (T b ∨ P b) →
      (¬ T a ∧ U (mate a)) ∨ (¬ T b ∧ U (mate b))) :
    ∀ n v, U v → ¬ frozenBy P T mate adj n v := by
  intro n
  induction n with
  | zero => intro v uv frozen; exact frozen
  | succ n ih =>
    intro v uv frozen
    obtain ⟨_, a, b, distinct, va, vb, ha, hb⟩ := frozen
    have oa : T a ∨ P a := ha.elim Or.inl (fun h => Or.inr h.1)
    have ob : T b ∨ P b := hb.elim Or.inl (fun h => Or.inr h.1)
    rcases closed v a b uv distinct va vb oa ob with ⟨nta, ua⟩ | ⟨ntb, ub⟩
    · rcases ha with ta | ⟨_, fa⟩
      · exact nta ta
      · exact ih (mate a) ua fa
    · rcases hb with tb | ⟨_, fb⟩
      · exact ntb tb
      · exact ih (mate b) ub fb

/-- Specialization to the two vertices {central BP, mate of fork TP}.
The geometric proof supplies the two local witness restrictions. -/
theorem fork_pair_never_freezes {V : Type} (P T : V → Prop)
    (mate : V → V) (adj : V → V → Prop) (v a : V)
    (centralNeedsMate : ∀ x y, x ≠ y → adj v x → adj v y →
      (T x ∨ P x) → (T y ∨ P y) →
      (¬ T x ∧ mate x = a) ∨ (¬ T y ∧ mate y = a))
    (mateNeedsCentral : ∀ x y, x ≠ y → adj a x → adj a y →
      (T x ∨ P x) → (T y ∨ P y) →
      (¬ T x ∧ mate x = v) ∨ (¬ T y ∧ mate y = v)) :
    ∀ n, ¬ frozenBy P T mate adj n v ∧ ¬ frozenBy P T mate adj n a := by
  have h := closed_set_never_freezes P T (fun z => z = v ∨ z = a) mate adj
    (by
      intro z x y member distinct zx zy ox oy
      rcases member with rfl | rfl
      · rcases centralNeedsMate x y distinct zx zy ox oy with ⟨nt, eq⟩ | ⟨nt, eq⟩
        · exact Or.inl ⟨nt, Or.inr eq⟩
        · exact Or.inr ⟨nt, Or.inr eq⟩
      · rcases mateNeedsCentral x y distinct zx zy ox oy with ⟨nt, eq⟩ | ⟨nt, eq⟩
        · exact Or.inl ⟨nt, Or.inl eq⟩
        · exact Or.inr ⟨nt, Or.inl eq⟩)
  intro n
  exact ⟨h n v (Or.inl rfl), h n a (Or.inr rfl)⟩

/-- Signed scalar consequence; no route-existence claim is encoded. -/
theorem weighted_budget (k b q c intervals : Int)
    (weighted : 2*k+c ≤ 2*b+q) :
    2*intervals+c-q ≤ 2*(intervals+b-k) := by omega

theorem conditional_nonnegative_budget (k b q c intervals : Int)
    (weighted : 2*k+c ≤ 2*b+q) (enough : q ≤ 2*intervals+c) :
    0 ≤ intervals+b-k := by omega

end SubQuorum.FrozenForkSurplus

#print axioms SubQuorum.FrozenForkSurplus.closed_set_never_freezes
#print axioms SubQuorum.FrozenForkSurplus.fork_pair_never_freezes
#print axioms SubQuorum.FrozenForkSurplus.weighted_budget
#print axioms SubQuorum.FrozenForkSurplus.conditional_nonnegative_budget
