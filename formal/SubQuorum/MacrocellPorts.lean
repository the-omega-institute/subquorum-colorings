import Lean.Elab.Tactic.Omega

/-! Physical 4-by-2 strip port constraints, from adjacency and mate involution.
Vertices 0,...,7 are row-major: coordinate (r,c) has index 2*r+c.
No enumeration of global board sizes or hypotheses asserting the port result.
The global relaxed-flow theorem and family embeddings remain written proofs.
-/
set_option autoImplicit false
namespace SubQuorum.MacrocellPorts

def adjacent (u v : Fin 8) : Prop :=
  (u.val / 2 = v.val / 2 ∧ u.val % 2 ≠ v.val % 2) ∨
  u.val + 2 = v.val ∨ v.val + 2 = u.val

theorem top_left_neighbours (v : Fin 8) (h : adjacent 0 v) :
    v = 1 ∨ v = 2 := by
  have hv := v.isLt
  have hval : v.val = 1 ∨ v.val = 2 := by
    simp [adjacent] at h
    omega
  rcases hval with hval | hval
  · left; exact Fin.ext hval
  · right; exact Fin.ext hval

theorem top_right_neighbours (v : Fin 8) (h : adjacent 1 v) :
    v = 0 ∨ v = 3 := by
  have hv := v.isLt
  have hval : v.val = 0 ∨ v.val = 3 := by
    simp [adjacent] at h
    omega
  rcases hval with hval | hval
  · left; exact Fin.ext hval
  · right; exact Fin.ext hval

theorem side_neighbours (v : Fin 8) (h : adjacent 5 v) :
    v = 3 ∨ v = 4 ∨ v = 7 := by
  have hv := v.isLt
  have hval : v.val = 3 ∨ v.val = 4 ∨ v.val = 7 := by
    simp [adjacent] at h
    omega
  rcases hval with hval | hval | hval
  · left; exact Fin.ext hval
  · right; left; exact Fin.ext hval
  · right; right; exact Fin.ext hval

theorem forced_top_ports (mate : Fin 8 → Fin 8)
    (legal : ∀ v, adjacent v (mate v))
    (involution : ∀ v, mate (mate v) = v) :
    (mate 0 = 1 ∧ mate 1 = 0) ∨
    (mate 0 = 2 ∧ mate 1 = 3) := by
  rcases top_left_neighbours (mate 0) (legal 0) with h01 | h02
  · left
    exact ⟨h01, by simpa [h01] using involution 0⟩
  · right
    refine ⟨h02, ?_⟩
    rcases top_right_neighbours (mate 1) (legal 1) with h10 | h13
    · have h01 : mate 0 = 1 := by simpa [h10] using involution 1
      have : (1 : Fin 8) = 2 := h01.symm.trans h02
      exact False.elim (by cases this)
    · exact h13

theorem forced_selected_end (mate : Fin 8 → Fin 8)
    (legal : ∀ v, adjacent v (mate v))
    (involution : ∀ v, mate (mate v) = v) :
    mate 1 = 0 ∨ (mate 1 = 3 ∧ (mate 5 = 4 ∨ mate 5 = 7)) := by
  rcases top_right_neighbours (mate 1) (legal 1) with h10 | h13
  · exact Or.inl h10
  · right
    refine ⟨h13, ?_⟩
    have h31 : mate 3 = 1 := by simpa [h13] using involution 1
    rcases side_neighbours (mate 5) (legal 5) with h53 | h54 | h57
    · have h35 : mate 3 = 5 := by simpa [h53] using involution 5
      have : (1 : Fin 8) = 5 := h31.symm.trans h35
      exact False.elim (by cases this)
    · exact Or.inl h54
    · exact Or.inr h57

end SubQuorum.MacrocellPorts

#print axioms SubQuorum.MacrocellPorts.top_left_neighbours
#print axioms SubQuorum.MacrocellPorts.top_right_neighbours
#print axioms SubQuorum.MacrocellPorts.side_neighbours
#print axioms SubQuorum.MacrocellPorts.forced_top_ports
#print axioms SubQuorum.MacrocellPorts.forced_selected_end
