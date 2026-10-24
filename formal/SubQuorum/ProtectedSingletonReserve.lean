import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.ProtectedSingletonReserve

abbrev Point := Int × Int

def Adjacent (p q : Point) : Prop :=
  q=(p.1+1,p.2) ∨ q=(p.1-1,p.2) ∨ q=(p.1,p.2+1) ∨ q=(p.1,p.2-1)

def Occupied (T P : Point → Prop) (p : Point) : Prop := T p ∨ P p

def Feasible (T P : Point → Prop) : Prop :=
  ∀ t, T t → ∀ x, Adjacent t x → Occupied T P x →
    ∀ y, Adjacent t y → Occupied T P y → x=y

/-- Retaining an old mate cannot attach an old endpoint to a previously blank
vertex. This derives the exclusion from the actual matching-extension rule. -/
theorem retained_mate_excludes_blank {V : Type} (oldP : V → Prop)
    (oldMate newMate : V → V) (guard blank : V)
    (guardOld : oldP guard) (blankOld : ¬oldP blank)
    (oldRange : ∀ p, oldP p → oldP (oldMate p))
    (retained : newMate guard=oldMate guard) : newMate guard≠blank := by
  intro eq
  have h := oldRange guard guardOld
  rw [←retained,eq] at h
  exact blankOld h

/-- Full grid-coordinate locking lemma. All hypotheses concern the actual
final occupied set and actual mates, with the three mate exclusions derived
from fixed old matching edges by retained_mate_excludes_blank. Reflections
transport the statement. No freezing hypothesis is needed. -/
theorem protected_singleton (r c : Int) (T P : Point → Prop) (mate : Point → Point)
    (feasible : Feasible T P)
    (selectedGuard : T (r+1,c+1))
    (rightP : P (r,c+1)) (leftP : P (r,c-1))
    (mateRange : ∀ p, P p → P (mate p))
    (mateInverse : ∀ p, P p → mate (mate p)=p)
    (mateEdge : ∀ p, P p → Adjacent p (mate p))
    (rightFixed : mate (r,c+1)≠(r,c))
    (leftFixed : mate (r,c-1)≠(r,c))
    (aboveFixed : mate (r-1,c)≠(r,c)) :
    ¬Occupied T P (r,c) ∧ ¬Occupied T P (r+1,c) := by
  have lowerBlank : ¬Occupied T P (r+1,c) := by
    intro lower
    have eq := feasible (r+1,c+1) selectedGuard (r,c+1)
      (by simp [Adjacent]) (Or.inr rightP) (r+1,c)
      (by simp [Adjacent]) lower
    have bad := congrArg Prod.snd eq
    omega
  have notSelected : ¬T (r,c) := by
    intro selected
    have eq := feasible (r,c) selected (r,c+1)
      (by simp [Adjacent]) (Or.inr rightP) (r,c-1)
      (by simp [Adjacent]) (Or.inr leftP)
    have bad := congrArg Prod.snd eq
    omega
  have notEndpoint : ¬P (r,c) := by
    intro endpoint
    have inv := mateInverse (r,c) endpoint
    have edge := mateEdge (r,c) endpoint
    dsimp only [Adjacent] at edge
    rcases edge with eq | eq | eq | eq
    · have occupied := mateRange (r,c) endpoint
      rw [eq] at occupied
      exact lowerBlank (Or.inr occupied)
    · rw [eq] at inv
      exact aboveFixed inv
    · rw [eq] at inv
      exact rightFixed inv
    · rw [eq] at inv
      exact leftFixed inv
  exact ⟨fun h => h.elim notSelected notEndpoint,lowerBlank⟩

/-- An original interval having a unique eligible alpha cannot be selected
as a private reserve by two different owners. The interval identities stay
in the type R, rather than being renumbered independently by components. -/
theorem private_choice_injective {A R : Type} (choice : A → R) (owner : R → A)
    (correct : ∀ a, owner (choice a)=a) :
    ∀ a b, choice a=choice b → a=b := by
  intro a b eq
  have h := congrArg owner eq
  simpa only [correct] using h

#print axioms retained_mate_excludes_blank
#print axioms protected_singleton
#print axioms private_choice_injective

end SubQuorum.ProtectedSingletonReserve
