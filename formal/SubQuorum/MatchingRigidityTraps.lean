import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.MatchingRigidityTraps

/-- The actual inductive freezing rule, with two distinct retained neighbors. -/
inductive Frozen {V : Type} (P T : V → Prop) (mate : V → V)
    (adj : V → V → Prop) : V → Prop where
  | ss {v a b} : P v → a ≠ b → adj v a → adj v b →
      T a → T b → Frozen P T mate adj v
  | sp {v a b} : P v → a ≠ b → adj v a → adj v b →
      T a → P b → Frozen P T mate adj (mate b) → Frozen P T mate adj v
  | ps {v a b} : P v → a ≠ b → adj v a → adj v b →
      P a → Frozen P T mate adj (mate a) → T b → Frozen P T mate adj v
  | pp {v a b} : P v → a ≠ b → adj v a → adj v b →
      P a → Frozen P T mate adj (mate a) →
      P b → Frozen P T mate adj (mate b) → Frozen P T mate adj v

/-- Grant every candidate mate outside the trap, even mutually incompatible ones. -/
def Upper {V : Type} (P S U : V → Prop) (E : V → V → Prop) (y : V) : Prop :=
  S y ∨ (P y ∧ ∃ z, E y z ∧ ¬ U z)

/-- A nonempty trap cannot start freezing. No finite size or rank bound is used. -/
theorem frozen_avoids_trap {V : Type} {P T S U : V → Prop}
    {mate : V → V} {adj E : V → V → Prop}
    (selections : ∀ y, T y → S y)
    (compatible : ∀ y, P y → E y (mate y))
    (blocked : ∀ v, U v → ∀ a b, adj v a → adj v b →
      Upper P S U E a → Upper P S U E b → a = b)
    {v : V} (h : Frozen P T mate adj v) : ¬ U v := by
  induction h with
  | ss _ distinct va vb ta tb =>
      intro uv
      exact distinct (blocked _ uv _ _ va vb (Or.inl (selections _ ta))
        (Or.inl (selections _ tb)))
  | sp _ distinct va vb ta pb _ ih =>
      intro uv
      exact distinct (blocked _ uv _ _ va vb (Or.inl (selections _ ta))
        (Or.inr ⟨pb, _, compatible _ pb, ih⟩))
  | ps _ distinct va vb pa _ tb ih =>
      intro uv
      exact distinct (blocked _ uv _ _ va vb
        (Or.inr ⟨pa, _, compatible _ pa, ih⟩) (Or.inl (selections _ tb)))
  | pp _ distinct va vb pa _ pb _ iha ihb =>
      intro uv
      exact distinct (blocked _ uv _ _ va vb
        (Or.inr ⟨pa, _, compatible _ pa, iha⟩)
        (Or.inr ⟨pb, _, compatible _ pb, ihb⟩))

theorem nonempty_trap_excludes_complete {V : Type} {P T S U : V → Prop}
    {mate : V → V} {adj E : V → V → Prop}
    (selections : ∀ y, T y → S y)
    (compatible : ∀ y, P y → E y (mate y))
    (blocked : ∀ v, U v → ∀ a b, adj v a → adj v b →
      Upper P S U E a → Upper P S U E b → a = b)
    (nonempty : ∃ v, P v ∧ U v) : ¬ (∀ v, P v → Frozen P T mate adj v) := by
  intro complete
  obtain ⟨v, pv, uv⟩ := nonempty
  exact frozen_avoids_trap selections compatible blocked (complete v pv) uv

/-- Upper supports may be infeasible; only inclusion of actual T is needed. -/
theorem upper_monotone {V : Type} {P S S' U : V → Prop}
    {E E' : V → V → Prop}
    (hs : ∀ y, S y → S' y) (he : ∀ y z, E y z → E' y z)
    {y : V} : Upper P S U E y → Upper P S' U E' y := by
  intro h
  rcases h with sy | ⟨py, z, eyz, uz⟩
  · exact Or.inl (hs y sy)
  · exact Or.inr ⟨py, z, he y z eyz, uz⟩

def Pin {V : Type} (E : V → V → Prop) (a b x y : V) : Prop :=
  E x y ∧ (x = a → y = b) ∧ (x = b → y = a) ∧
    (y = a → x = b) ∧ (y = b → x = a)

/-- A singleton candidate neighborhood forces its actual matching edge. -/
theorem leaf_forces {V : Type} {P : V → Prop} {mate : V → V}
    {E : V → V → Prop} {a b : V}
    (compatible : ∀ x, P x → E x (mate x)) (pa : P a)
    (singleton : ∀ y, E a y → y = b) : mate a = b :=
  singleton _ (compatible a pa)

/-- Removing every edge conflicting with a forced pair is sound. -/
theorem pin_preserves_compatibility {V : Type} {P : V → Prop}
    {mate : V → V} {E : V → V → Prop} {a b : V}
    (involution : ∀ x, mate (mate x) = x)
    (compatible : ∀ x, P x → E x (mate x)) (hab : mate a = b) :
    ∀ x, P x → Pin E a b x (mate x) := by
  have hba : mate b = a := by rw [← hab]; exact involution a
  intro x px
  refine ⟨compatible x px, ?_, ?_, ?_, ?_⟩
  · intro h; simpa [h] using hab
  · intro h; simpa [h] using hba
  · intro h
    calc x = mate (mate x) := (involution x).symm
         _ = b := by rw [h, hab]
  · intro h
    calc x = mate (mate x) := (involution x).symm
         _ = a := by rw [h, hba]

def DeleteEdge {V : Type} (E : V → V → Prop) (a b x y : V) : Prop :=
  E x y ∧ ¬ ((x = a ∧ y = b) ∨ (x = b ∧ y = a))

/-- A trap under an assumed pair excludes that pair in either orientation. -/
theorem delete_preserves_compatibility {V : Type} {P : V → Prop}
    {mate : V → V} {E : V → V → Prop} {a b : V}
    (involution : ∀ x, mate (mate x) = x)
    (compatible : ∀ x, P x → E x (mate x)) (impossible : mate a ≠ b) :
    ∀ x, P x → DeleteEdge E a b x (mate x) := by
  intro x px
  refine ⟨compatible x px, ?_⟩
  intro h
  rcases h with ⟨xa, mb⟩ | ⟨xb, ma⟩
  · exact impossible (xa ▸ mb)
  · have mba : mate b = a := xb ▸ ma
    have hab : mate a = b := by rw [← mba]; exact involution b
    exact impossible hab

/-- Replaying any finite sound reduction proves uniqueness at singleton leaves. -/
theorem singleton_candidates_unique {V : Type} {P : V → Prop}
    {mate target : V → V} {E : V → V → Prop}
    (compatible : ∀ x, P x → E x (mate x))
    (singleton : ∀ x, P x → ∀ y, E x y → y = target x) :
    ∀ x, P x → mate x = target x := by
  intro x px
  exact singleton x px (mate x) (compatible x px)

/-- Independent components add neither payments nor unused resource credit. -/
theorem elimination_ledger (q f I b k V Vres c cres : Int)
    (hv : V = 2*q+Vres) (hc : c = f+cres) :
    ((I-(2*q-f))+(b-f)-(k-2*q) = I+b-k) ∧
    (k-V = (k-2*q)-Vres) ∧ (c-f = cres) := by omega

#print axioms frozen_avoids_trap
#print axioms nonempty_trap_excludes_complete
#print axioms upper_monotone
#print axioms leaf_forces
#print axioms pin_preserves_compatibility
#print axioms delete_preserves_compatibility
#print axioms singleton_candidates_unique
#print axioms elimination_ledger

end SubQuorum.MatchingRigidityTraps
