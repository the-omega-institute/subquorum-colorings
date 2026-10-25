import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.FrozenCertificateReplay

variable {V : Type}

/-- A neighbor retained when p freezes: selected, or its actual mate was
scheduled at a strictly smaller rank. K is the old partial frozen set. -/
def Kept (T P K : V → Prop) (mate : V → V) (rank : V → Nat)
    (p x : V) : Prop :=
  T x ∨ (P x ∧ K (mate x) ∧ rank (mate x) < rank p)

def Certificate (E : V → V → Prop) (T P K : V → Prop)
    (mate : V → V) (rank : V → Nat) : Prop :=
  ∀ p, K p → ∃ x y, x ≠ y ∧ E p x ∧ E p y ∧
    Kept T P K mate rank p x ∧ Kept T P K mate rank p y

/-- Removing all endpoints outside a mate-closed partial frozen set and
adding selections preserves each exact old rank witness. -/
theorem kept_replay (T T' P K : V → Prop) (mate : V → V)
    (rank : V → Nat) (p x : V)
    (involution : ∀ v, mate (mate v) = v)
    (mateClosed : ∀ v, K v → K (mate v))
    (retainT : ∀ v, T v → T' v)
    (old : Kept T P K mate rank p x) :
    Kept T' K K mate rank p x := by
  rcases old with selected | ⟨_, scheduled, earlier⟩
  · exact Or.inl (retainT x selected)
  · have kx : K x := by
      simpa only [involution x] using mateClosed (mate x) scheduled
    exact Or.inr ⟨kx, scheduled, earlier⟩

theorem certificate_replay (E : V → V → Prop) (T T' P K : V → Prop)
    (mate : V → V) (rank : V → Nat)
    (involution : ∀ v, mate (mate v) = v)
    (mateClosed : ∀ v, K v → K (mate v))
    (retainT : ∀ v, T v → T' v)
    (old : Certificate E T P K mate rank) :
    Certificate E T' K K mate rank := by
  intro p hp
  obtain ⟨x,y,distinct,ex,ey,hx,hy⟩ := old p hp
  exact ⟨x,y,distinct,ex,ey,
    kept_replay T T' P K mate rank p x involution mateClosed retainT hx,
    kept_replay T T' P K mate rank p y involution mateClosed retainT hy⟩

/-- Any predicate closed under the physical two-kept-neighbor freezing
rule contains all scheduled vertices. No finite enumeration is used. -/
theorem certificate_sound (E : V → V → Prop) (T P K F : V → Prop)
    (mate : V → V) (rank : V → Nat)
    (certificate : Certificate E T P K mate rank)
    (freeze : ∀ p, K p → (∃ x y, x ≠ y ∧ E p x ∧ E p y ∧
      (T x ∨ F (mate x)) ∧ (T y ∨ F (mate y))) → F p) :
    ∀ p, K p → F p := by
  have inductionStep : ∀ n p, rank p = n → K p → F p := by
    intro n
    induction n using Nat.strongRecOn with
    | ind n ih =>
      intro p hp hk
      obtain ⟨x,y,distinct,ex,ey,hx,hy⟩ := certificate p hk
      have witness : ∀ z, Kept T P K mate rank p z → T z ∨ F (mate z) := by
        intro z hz
        rcases hz with selected | ⟨_,scheduled,earlier⟩
        · exact Or.inl selected
        · have smaller : rank (mate z) < n := by
            simpa only [hp] using earlier
          exact Or.inr (ih (rank (mate z)) smaller (mate z) rfl scheduled)
      exact freeze p hk ⟨x,y,distinct,ex,ey,witness x hx,witness y hy⟩
  intro p hp
  exact inductionStep (rank p) p rfl hp

end SubQuorum.FrozenCertificateReplay

#print axioms SubQuorum.FrozenCertificateReplay.kept_replay
#print axioms SubQuorum.FrozenCertificateReplay.certificate_replay
#print axioms SubQuorum.FrozenCertificateReplay.certificate_sound
