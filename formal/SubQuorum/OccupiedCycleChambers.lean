import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.OccupiedCycleChambers

def Occupied {V : Type} (T P : V → Prop) (v : V) : Prop := T v ∨ P v

/-- A selected band partner would see two different occupied neighbours. -/
theorem shadow_excludes_selected_partner {V : Type}
    (N : V → V → Prop) (T P : V → Prop) (partner : V → V)
    (feasible : ∀ v, T v → ∀ x, N v x → Occupied T P x →
      ∀ y, N v y → Occupied T P y → x=y)
    (v w : V) (pv : P v) (pairEdge : N (partner v) v)
    (shadowEdge : N (partner v) w) (shadowOccupied : Occupied T P w)
    (different : v ≠ w) : ¬T (partner v) := by
  intro selected
  exact different (feasible (partner v) selected v pairEdge (Or.inr pv)
    w shadowEdge shadowOccupied)

/-- Neighbours outside the chamber lie on an actual-matching-closed wall,
or at a permanently blank site. No actual mate can cross this boundary. -/
theorem chamber_mate_closed {V : Type} (N : V → V → Prop)
    (P C W B : V → Prop) (mate : V → V)
    (mateEdge : ∀ v, P v → N v (mate v))
    (mateP : ∀ v, P v → P (mate v))
    (inverse : ∀ v, P v → mate (mate v)=v)
    (wallClosed : ∀ v, W v → W (mate v))
    (separate : ∀ v, C v → ¬W v) (blank : ∀ v, B v → ¬P v)
    (boundary : ∀ v, C v → P v → ∀ w, N v w → C w ∨ W w ∨ B w) :
    ∀ v, C v → P v → C (mate v) := by
  intro v cv pv
  rcases boundary v cv pv (mate v) (mateEdge v pv) with inside | wall | vacant
  · exact inside
  · have back := wallClosed (mate v) wall
    rw [inverse v pv] at back
    exact False.elim (separate v cv back)
  · exact False.elim (blank (mate v) vacant (mateP v pv))

/-- Band partners are either permanently nonselected, or shadowed by the wall. -/
theorem chamber_no_TP {V : Type} (N : V → V → Prop) (T P C : V → Prop)
    (partner : V → V)
    (feasible : ∀ v, T v → ∀ x, N v x → Occupied T P x →
      ∀ y, N v y → Occupied T P y → x=y)
    (pairEdge : ∀ v, P v → N (partner v) v)
    (shadow : ∀ v, C v → P v → ¬T (partner v) ∨
      ∃ w, w ≠ v ∧ N (partner v) w ∧ Occupied T P w) :
    ∀ v, C v → P v → ¬T (partner v) := by
  intro v cv pv
  rcases shadow v cv pv with noSelected | ⟨w, different, edge, occupied⟩
  · exact noSelected
  · exact shadow_excludes_selected_partner N T P partner feasible v w pv
      (pairEdge v pv) edge occupied (Ne.symm different)

/-- Reachability in the actual M/PP component, retaining actual identities. -/
inductive Reach {V : Type} (P : V → Prop) (mate partner : V → V) (root : V) :
    V → Prop where
  | start : P root → Reach P mate partner root root
  | matching {v : V} : Reach P mate partner root v → Reach P mate partner root (mate v)
  | band {v : V} : Reach P mate partner root v → P (partner v) →
      Reach P mate partner root (partner v)

/-- Closure holds for every path length, with no finite enumeration. -/
theorem actual_component_closed {V : Type} (P C : V → Prop)
    (mate partner : V → V) (root : V) (rootC : C root)
    (mateP : ∀ v, P v → P (mate v))
    (mateClosed : ∀ v, C v → P v → C (mate v))
    (bandClosed : ∀ v, C v → P v → P (partner v) → C (partner v)) :
    ∀ v, Reach P mate partner root v → C v ∧ P v := by
  intro v path
  induction path with
  | start pv => exact ⟨rootC, pv⟩
  | @matching v path ih => exact ⟨mateClosed v ih.1 ih.2, mateP v ih.2⟩
  | @band v path pp ih => exact ⟨bandClosed v ih.1 ih.2 pp, pp⟩

/-- A BP-rooted closed, shadowed chamber cannot produce a mixed TP exit. -/
theorem no_reachable_TP {V : Type} (T P C : V → Prop)
    (mate partner : V → V) (root : V) (rootC : C root)
    (mateP : ∀ v, P v → P (mate v))
    (mateClosed : ∀ v, C v → P v → C (mate v))
    (bandClosed : ∀ v, C v → P v → P (partner v) → C (partner v))
    (noTP : ∀ v, C v → P v → ¬T (partner v)) :
    ¬∃ v, Reach P mate partner root v ∧ T (partner v) := by
  rintro ⟨v, path, tp⟩
  have closed := actual_component_closed P C mate partner root rootC mateP mateClosed bandClosed v path
  exact noTP v closed.1 closed.2 tp

/-- Every actual terminal in the chamber is BP, so a finite rooted open
strand ends in BP rather than TP. The graph path classification is written. -/
theorem reached_terminal_is_BP {V : Type} (T P C : V → Prop)
    (mate partner : V → V) (root : V) (rootC : C root)
    (mateP : ∀ v, P v → P (mate v))
    (mateClosed : ∀ v, C v → P v → C (mate v))
    (bandClosed : ∀ v, C v → P v → P (partner v) → C (partner v))
    (noTP : ∀ v, C v → P v → ¬T (partner v))
    (v : V) (path : Reach P mate partner root v) (terminal : ¬P (partner v)) :
    P v ∧ ¬P (partner v) ∧ ¬T (partner v) := by
  have closed := actual_component_closed P C mate partner root rootC mateP mateClosed bandClosed v path
  exact ⟨closed.2, terminal, noTP v closed.1 closed.2⟩

#print axioms shadow_excludes_selected_partner
#print axioms chamber_mate_closed
#print axioms chamber_no_TP
#print axioms actual_component_closed
#print axioms no_reachable_TP
#print axioms reached_terminal_is_BP

end SubQuorum.OccupiedCycleChambers
