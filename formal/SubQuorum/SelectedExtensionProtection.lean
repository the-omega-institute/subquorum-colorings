set_option autoImplicit false

namespace SubQuorum.SelectedExtensionProtection

variable {V : Type}

/-- A selected vertex has at most one occupied neighbor, and selections
are disjoint from fixed actual-matching endpoints. -/
def Feasible (E : V → V → Prop) (P T : V → Prop) : Prop :=
  (∀ v, T v → ¬ P v) ∧
  ∀ v, T v → ∀ x y, E v x → E v y → (P x ∨ T x) →
    (P y ∨ T y) → x = y

def Add (T : V → Prop) (v : V) : V → Prop := fun x => T x ∨ x = v

def Candidate (E : V → V → Prop) (P T : V → Prop) (v : V) : Prop :=
  ¬ T v ∧ Feasible E P (Add T v)

/-- Deleting selected vertices cannot violate the selected degree bound. -/
theorem feasible_downward (E : V → V → Prop) (P T U : V → Prop)
    (subset : ∀ v, T v → U v) (h : Feasible E P U) : Feasible E P T := by
  constructor
  · intro v hv
    exact h.1 v (subset v hv)
  · intro v hv x y ex ey ox oy
    exact h.2 v (subset v hv) x y ex ey
      (ox.elim Or.inl (fun hx => Or.inr (subset x hx)))
      (oy.elim Or.inl (fun hy => Or.inr (subset y hy)))

/-- Every new selection in any feasible extension was individually
selectable at the baseline. No finiteness or optimizer hypothesis. -/
theorem new_selection_in_hull (E : V → V → Prop) (P T U : V → Prop)
    (retain : ∀ v, T v → U v) (h : Feasible E P U)
    (v : V) (new : ¬ T v) (selected : U v) : Candidate E P T v := by
  refine ⟨new, feasible_downward E P (Add T v) U ?_ h⟩
  intro x hx
  rcases hx with old | equal
  · exact retain x old
  · exact equal ▸ selected

/-- A region disjoint from the baseline candidate hull retains its entire
selected/blank pattern under every feasible selected extension. -/
theorem protected_region_unchanged (E : V → V → Prop) (P T U G : V → Prop)
    [DecidablePred T]
    (retain : ∀ v, T v → U v) (h : Feasible E P U)
    (noCandidate : ∀ v, G v → ¬ Candidate E P T v) :
    ∀ v, G v → (U v ↔ T v) := by
  intro v hv
  constructor
  · intro selected
    by_cases old : T v
    · exact old
    · exact False.elim (noCandidate v hv (new_selection_in_hull E P T U retain h v old selected))
  · exact retain v

/-- Two distinct baseline occupied neighbors forbid selection forever. -/
theorem two_occupied_neighbors_forbid (E : V → V → Prop) (P T U : V → Prop)
    (retain : ∀ v, T v → U v) (h : Feasible E P U)
    (v x y : V) (different : x ≠ y) (ex : E v x) (ey : E v y)
    (ox : P x ∨ T x) (oy : P y ∨ T y) : ¬ U v := by
  intro selected
  apply different
  exact h.2 v selected x y ex ey
    (ox.elim Or.inl (fun hx => Or.inr (retain x hx)))
    (oy.elim Or.inl (fun hy => Or.inr (retain y hy)))

end SubQuorum.SelectedExtensionProtection

#print axioms SubQuorum.SelectedExtensionProtection.feasible_downward
#print axioms SubQuorum.SelectedExtensionProtection.new_selection_in_hull
#print axioms SubQuorum.SelectedExtensionProtection.protected_region_unchanged
#print axioms SubQuorum.SelectedExtensionProtection.two_occupied_neighbors_forbid
