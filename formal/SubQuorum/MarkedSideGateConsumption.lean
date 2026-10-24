import SubQuorum.SourceRetentionClosure
import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.MarkedSideGateConsumption

open SourceRetentionClosure

abbrev Point := Int × Int

def neighbors (point : Point) : List Point :=
  [(point.1-1,point.2),(point.1+1,point.2),
   (point.1,point.2-1),(point.1,point.2+1)]

def occupiedDegree (occupied : Point → Bool) (point : Point) : Nat :=
  ((neighbors point).filter occupied).length

theorem canonical_mark_iff_gate_endpoint
    (occupied endpoint : Point → Bool)
    (hanchor : occupied (3,1) = true)
    (hselected : endpoint (3,2) = false → ∀ neighbor,
      neighbor ∈ neighbors (3,2) → occupied neighbor = true → neighbor = (3,1))
    (htriggers : ∀ point, point ∈ ([(2,2),(4,2),(2,3)] : List Point) →
      occupied point = true → endpoint point = true)
    (hdegree : ∀ point, endpoint point = true → 3 ≤ occupiedDegree occupied point) :
    (occupied (2,2) = true ∨ occupied (4,2) = true ∨ occupied (2,3) = true) ↔
      endpoint (3,2) = true := by
  constructor
  · intro hmark
    by_cases hconsumed : endpoint (3,2) = true
    · exact hconsumed
    have hfalse : endpoint (3,2) = false := by
      cases hvalue : endpoint (3,2) <;> simp_all
    have hblank : ∀ neighbor, neighbor ∈ neighbors (3,2) →
        neighbor ≠ (3,1) → occupied neighbor = false := by
      intro neighbor hneighbor hdifferent
      cases hvalue : occupied neighbor
      · rfl
      · exact False.elim (hdifferent (hselected hfalse neighbor hneighbor hvalue))
    have hfirst := hblank (2,2) (by decide) (by decide)
    have hsecond := hblank (4,2) (by decide) (by decide)
    have hother := hblank (3,3) (by decide) (by decide)
    rcases hmark with hmark | hmark | hmark
    · simp_all
    · simp_all
    · have hendpoint := htriggers (2,3) (by decide) hmark
      have hlarge := hdegree (2,3) hendpoint
      have hsmall : occupiedDegree occupied (2,3) ≤ 2 := by
        cases hupper : occupied (1,3) <;> cases hright : occupied (2,4) <;>
          simp [occupiedDegree, neighbors, hfirst, hother, hupper, hright]
      omega
  · intro hconsumed
    by_cases hfirst : occupied (2,2) = true
    · exact Or.inl hfirst
    by_cases hsecond : occupied (4,2) = true
    · exact Or.inr (Or.inl hsecond)
    have hfirstFalse : occupied (2,2) = false := by
      cases hvalue : occupied (2,2) <;> simp_all
    have hsecondFalse : occupied (4,2) = false := by
      cases hvalue : occupied (4,2) <;> simp_all
    have hlarge := hdegree (3,2) hconsumed
    have hsmall : occupiedDegree occupied (3,2) ≤ 2 := by
      cases hother : occupied (3,3) <;>
        simp [occupiedDegree, neighbors, hfirstFalse, hsecondFalse, hanchor, hother]
    omega

theorem a_foreign_occupied_blank_at_a_protector_is_endpoint
    {Owner Vertex : Type}
    (endpoint support : Owner → Vertex → Prop)
    (adjacent : Vertex → Vertex → Prop) (anchor : Owner → Vertex → Vertex)
    (hanchor : ∀ owner point, support owner point →
      endpoint owner (anchor owner point) ∧ adjacent point (anchor owner point))
    (hunique : ∀ first second point, endpoint first point → endpoint second point → first = second)
    (keep : Owner → Prop) (hfeasible : feasible endpoint support adjacent keep)
    (positive : Owner) (hpositive : keep positive)
    (point protector : Vertex)
    (hprotector : endpoint positive protector)
    (hblank : ¬originalOccupied endpoint support positive point)
    (hadjacent : adjacent point protector)
    (hoccupied : occupied endpoint support keep point) :
    retainedEndpoint endpoint keep point := by
  rcases hoccupied with ⟨owner, howner, hendpoint | hsupport⟩
  · exact ⟨owner, howner, hendpoint⟩
  · have hdifferent : protector ≠ anchor owner point := by
      intro hequal
      have hsame := hunique positive owner protector hprotector
        (hequal.symm ▸ (hanchor owner point hsupport).1)
      exact hblank (Or.inr (hsame.symm ▸ hsupport))
    exact a_second_occupied_neighbor_forces_consumption endpoint support adjacent anchor
      hanchor keep hfeasible owner positive point protector howner hpositive hsupport
      (Or.inl hprotector) hadjacent hdifferent

theorem retained_gate_iff_original_consumer_retained
    {Owner Vertex : Type} (endpoint : Owner → Vertex → Prop)
    (hunique : ∀ first second point, endpoint first point → endpoint second point → first = second)
    (consumer : Owner) (gate : Vertex) (hconsumer : endpoint consumer gate)
    (keep : Owner → Prop) :
    retainedEndpoint endpoint keep gate ↔ keep consumer := by
  constructor
  · rintro ⟨owner, howner, hendpoint⟩
    have hequal := hunique owner consumer gate hendpoint hconsumer
    exact hequal ▸ howner
  · intro hkeep
    exact ⟨consumer, hkeep, hconsumer⟩

end SubQuorum.MarkedSideGateConsumption
