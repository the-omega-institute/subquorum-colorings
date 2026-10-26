import SubQuorum.TwoPortUnboundedRematching

set_option autoImplicit false
set_option maxRecDepth 16384
set_option maxHeartbeats 0

namespace SubQuorum.TwoPortMatchingClassification
open SubQuorum.TwoPortUnboundedRematching
universe u

/-- A kept witness after granting every endpoint outside S frozen. -/
def External {V : Type u} (K P S : V → Prop) (mate : V → V) (a : V) : Prop :=
  K a ∨ P a ∧ ¬ S (mate a)

/-- The geometric boundary tables reduce to two fronts. At a bottom vertex
    every possible support is its single seed; at an upper vertex a support
    can enter only through one of the two adjacent cut columns. A separation
    of four prevents the fronts from supporting the same endpoint together.
    The coordinate adapter that supplies hlocal is a written proof. -/
theorem separated_fronts_exclude_freezing {V : Type u}
    (Adj : V → V → Prop) (K P S : V → Prop) (mate : V → V)
    (col : V → Nat) (left right : V → V) (x z : Nat)
    (hgap : x+4≤z)
    (hlocal : ∀ v, S v →
      (∃ seed, ∀ a, Adj v a → External K P S mate a → a=seed) ∨
      (∀ a, Adj v a → External K P S mate a →
        (col v=x+1 ∧ a=left v) ∨ (col v+1=z ∧ a=right v))) :
    ∀ v, S v → ¬ Frozen Adj K P mate v := by
  intro v hv hf
  have hc : Closed Adj K P mate (fun w => ¬S w) := by
    intro w _hp hs hw
    obtain ⟨a,b,hab,hwa,hwb,ha,hb⟩ := hs
    have hae : External K P S mate a := ha
    have hbe : External K P S mate b := hb
    have heq : a=b := by
      rcases hlocal w hw with ⟨seed,hseed⟩ | hfront
      · exact (hseed a hwa hae).trans (hseed b hwb hbe).symm
      · rcases hfront a hwa hae with ⟨hal,hae⟩ | ⟨har,hae⟩
        · rcases hfront b hwb hbe with ⟨hbl,hbe⟩ | ⟨hbr,_hbe⟩
          · exact hae.trans hbe.symm
          · omega
        · rcases hfront b hwb hbe with ⟨hbl,_hbe⟩ | ⟨hbr,hbe⟩
          · omega
          · exact hae.trans hbe.symm
    exact hab heq
  exact hf (fun w => ¬S w) hc hv

/-- A nonempty subset of the natural numbers has a least member. This helper
    is consumed by the root normal form, without any finiteness assumption. -/
theorem least_root (R : Nat → Prop) (hne : ∃ a, R a) :
    ∃ a, R a ∧ ∀ b, R b → a≤b := by
  classical
  have aux : ∀ n, R n → ∃ a, R a ∧ ∀ b, R b → a≤b := by
    intro n
    induction n using Nat.strongRecOn with
    | ind n ih =>
      intro hn
      by_cases hl : ∃ b, b<n ∧ R b
      · obtain ⟨b,hbn,hb⟩ := hl
        exact ih b hbn hb
      · refine ⟨n,hn,?_⟩
        intro b hb
        by_cases hnb : n≤b
        · exact hnb
        · exact False.elim (hl ⟨b,by omega,hb⟩)
  obtain ⟨n,hn⟩ := hne
  exact aux n hn

/-- A root index set with no pair separated by two indices is exactly a
    singleton or a pair of consecutive indices. No enumeration is used. -/
theorem root_normal_form (R : Nat → Prop) (hne : ∃ a, R a)
    (hnarrow : ∀ a b, R a → R b → a<b → b≤a+1) :
    (∃ a, ∀ i, R i ↔ i=a) ∨ (∃ a, ∀ i, R i ↔ i=a ∨ i=a+1) := by
  classical
  obtain ⟨a,ha,hmin⟩ := least_root R hne
  have hbound : ∀ i, R i → i=a ∨ i=a+1 := by
    intro i hi
    have hlo := hmin i hi
    by_cases he : i=a
    · exact Or.inl he
    · have hlt : a<i := by omega
      have hhi := hnarrow a i ha hi hlt
      exact Or.inr (by omega)
  by_cases hnext : R (a+1)
  · apply Or.inr
    refine ⟨a,?_⟩
    intro i
    constructor
    · exact hbound i
    · intro hi
      rcases hi with he | he
      · simpa [he] using ha
      · simpa [he] using hnext
  · apply Or.inl
    refine ⟨a,?_⟩
    intro i
    constructor
    · intro hi
      rcases hbound i hi with he | he
      · exact he
      · exact False.elim (hnext (he ▸ hi))
    · intro he
      simpa [he] using ha

/-- Convert the actual odd-column gap restriction to the index normal form.
    The geometric interval barrier supplies hgap. -/
theorem odd_column_normal_form (R : Nat → Prop) (hne : ∃ a, R a)
    (hgap : ∀ a b, R a → R b → a<b → ¬(5+2*a+4≤5+2*b)) :
    (∃ a, ∀ i, R i ↔ i=a) ∨ (∃ a, ∀ i, R i ↔ i=a ∨ i=a+1) := by
  apply root_normal_form R hne
  intro a b ha hb hab
  have h := hgap a b ha hb hab
  omega

/-- All listed noncanonical interfaces have two independent nonempty traps.
    Combined with the written classification, absence of either input rules
    out every noncanonical member. -/
theorem absent_port_excludes_noncanonical {V : Type u}
    (P B W F : V → Prop) (p q : Prop)
    (hb : ∃ v, P v ∧ B v) (hw : ∃ v, P v ∧ W v)
    (hblockB : ¬p → ∀ v, B v → ¬F v)
    (hblockW : ¬q → ∀ v, W v → ¬F v)
    (hmissing : ¬p ∨ ¬q) : ¬(∀ v, P v → F v) := by
  intro hall
  rcases hmissing with hp | hq
  · obtain ⟨v,hpv,hbv⟩ := hb
    exact hblockB hp v hbv (hall v hpv)
  · obtain ⟨v,hpv,hwv⟩ := hw
    exact hblockW hq v hwv (hall v hpv)

end SubQuorum.TwoPortMatchingClassification
#print axioms SubQuorum.TwoPortMatchingClassification.separated_fronts_exclude_freezing
#print axioms SubQuorum.TwoPortMatchingClassification.least_root
#print axioms SubQuorum.TwoPortMatchingClassification.root_normal_form
#print axioms SubQuorum.TwoPortMatchingClassification.odd_column_normal_form
#print axioms SubQuorum.TwoPortMatchingClassification.absent_port_excludes_noncanonical
