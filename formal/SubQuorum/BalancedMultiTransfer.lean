import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.BalancedMultiTransfer

abbrev Span := Nat × Nat

def Valid (n : Nat) (spans : List Span) : Prop :=
  ∀ p, p ∈ spans → p.1 ≤ p.2 ∧ p.2 < n

def Separated (spans : List Span) : Prop :=
  ∀ p, p ∈ spans → ∀ q, q ∈ spans →
    p = q ∨ p.2 < q.1 ∨ q.2 < p.1

def Active (spans : List Span) (a : Nat) : Prop :=
  ∃ p, p ∈ spans ∧ p.1 < a ∧ a ≤ p.2

def Interior (spans : List Span) (b : Nat) : Prop :=
  ∃ p, p ∈ spans ∧ p.1 ≤ b ∧ b < p.2

/-- Original alpha indices at left endpoints are deleted. Shift the
remaining alphas left by one inside each disjoint transfer interval. -/
noncomputable def exchange (spans : List Span) (a : Nat) : Nat := by
  classical
  exact if Active spans a then a - 1 else a

theorem legal {n : Nat} {spans : List Span}
    (valid : Valid n spans) (separated : Separated spans)
    {a : Nat} (ha : a < n) (free : ∀ p, p ∈ spans → a ≠ p.1) :
    exchange spans a < n ∧
    (exchange spans a = a ∨ exchange spans a + 1 = a) ∧
    (∀ q, q ∈ spans → exchange spans a ≠ q.2) := by
  classical
  unfold exchange
  split
  · rename_i active
    obtain ⟨p, hp, left, right⟩ := active
    refine ⟨by omega, Or.inr (by omega), ?_⟩
    intro q hq
    have vp := valid p hp
    have vq := valid q hq
    rcases separated p hp q hq with eq | before | after
    · cases eq
      omega
    · omega
    · omega
  · rename_i inactive
    refine ⟨ha, Or.inl rfl, ?_⟩
    intro q hq eq
    have vq := valid q hq
    have not_left := free q hq
    exact inactive ⟨q, hq, by omega, by omega⟩

theorem injective {spans : List Span} {a b : Nat}
    (fa : ∀ p, p ∈ spans → a ≠ p.1)
    (fb : ∀ p, p ∈ spans → b ≠ p.1)
    (eq : exchange spans a = exchange spans b) : a = b := by
  classical
  by_cases aa : Active spans a
  · by_cases ab : Active spans b
    · simp only [exchange, if_pos aa, if_pos ab] at eq
      obtain ⟨p, hp, left, right⟩ := aa
      obtain ⟨q, hq, leftb, rightb⟩ := ab
      omega
    · simp only [exchange, if_pos aa, if_neg ab] at eq
      obtain ⟨p, hp, left, right⟩ := aa
      have not_left := fb p hp
      have active_b : Active spans b := ⟨p, hp, by omega, by omega⟩
      exact False.elim (ab active_b)
  · by_cases ab : Active spans b
    · simp only [exchange, if_neg aa, if_pos ab] at eq
      obtain ⟨p, hp, left, right⟩ := ab
      have not_left := fa p hp
      have active_a : Active spans a := ⟨p, hp, by omega, by omega⟩
      exact False.elim (aa active_a)
    · simpa only [exchange, if_neg aa, if_neg ab] using eq

theorem covers {n : Nat} {spans : List Span}
    (valid : Valid n spans) (separated : Separated spans)
    {b : Nat} (hb : b < n) (free : ∀ p, p ∈ spans → b ≠ p.2) :
    ∃ a, a < n ∧ (∀ p, p ∈ spans → a ≠ p.1) ∧ exchange spans a = b := by
  classical
  by_cases inside : Interior spans b
  · obtain ⟨p, hp, left, right⟩ := inside
    have vp := valid p hp
    refine ⟨b + 1, by omega, ?_, ?_⟩
    · intro q hq
      have vq := valid q hq
      rcases separated p hp q hq with eq | before | after
      · cases eq
        omega
      · omega
      · omega
    · have active : Active spans (b+1) := ⟨p, hp, by omega, by omega⟩
      simp [exchange, active]
  · refine ⟨b, hb, ?_, ?_⟩
    · intro p hp eq
      have vp := valid p hp
      have not_right := free p hp
      have interior : Interior spans b := ⟨p, hp, by omega, by omega⟩
      exact inside interior
    · have inactive : ¬ Active spans b := by
        intro active
        obtain ⟨p, hp, left, right⟩ := active
        have not_right := free p hp
        exact inside ⟨p, hp, by omega, by omega⟩
      simp [exchange, inactive]

/-- A bijection by adjacent F-edges between all surviving alpha/beta
indices. This sufficiency theorem is valid for any finite separated family. -/
theorem matching {n : Nat} {spans : List Span}
    (valid : Valid n spans) (separated : Separated spans) :
    (∀ a, a < n → (∀ p, p ∈ spans → a ≠ p.1) →
      exchange spans a < n ∧
      (exchange spans a = a ∨ exchange spans a + 1 = a) ∧
      (∀ p, p ∈ spans → exchange spans a ≠ p.2)) ∧
    (∀ a b, (∀ p, p ∈ spans → a ≠ p.1) →
      (∀ p, p ∈ spans → b ≠ p.1) → exchange spans a = exchange spans b → a = b) ∧
    (∀ b, b < n → (∀ p, p ∈ spans → b ≠ p.2) →
      ∃ a, a < n ∧ (∀ p, p ∈ spans → a ≠ p.1) ∧ exchange spans a = b) := by
  exact ⟨fun _ ha fa => legal valid separated ha fa,
    fun _ _ fa fb eq => injective fa fb eq,
    fun _ hb fb => covers valid separated hb fb⟩

#print axioms legal
#print axioms injective
#print axioms covers
#print axioms matching

end SubQuorum.BalancedMultiTransfer
