import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.PPCycleNormalization

def normalizedMate {Vertex : Type} (inside : Vertex → Prop) [DecidablePred inside]
    (actual auxiliary : Vertex → Vertex) (point : Vertex) : Vertex :=
  if inside point then auxiliary point else actual point

theorem unchanged_outside {Vertex : Type} (inside : Vertex → Prop) [DecidablePred inside]
    (actual auxiliary : Vertex → Vertex) (point : Vertex) (outside : ¬inside point) :
    normalizedMate inside actual auxiliary point = actual point := by
  simp [normalizedMate, outside]

theorem auxiliary_inside {Vertex : Type} (inside : Vertex → Prop) [DecidablePred inside]
    (actual auxiliary : Vertex → Vertex) (point : Vertex) (member : inside point) :
    normalizedMate inside actual auxiliary point = auxiliary point := by
  simp [normalizedMate, member]

theorem normalized_involution {Vertex : Type} (inside : Vertex → Prop) [DecidablePred inside]
    (actual auxiliary : Vertex → Vertex)
    (actualInvolution : ∀ point, actual (actual point) = point)
    (auxiliaryInvolution : ∀ point, inside point → auxiliary (auxiliary point) = point)
    (actualClosed : ∀ point, inside point → inside (actual point))
    (auxiliaryClosed : ∀ point, inside point → inside (auxiliary point)) :
    ∀ point, normalizedMate inside actual auxiliary
      (normalizedMate inside actual auxiliary point) = point := by
  intro point
  by_cases member : inside point
  · have following := auxiliaryClosed point member
    simp only [normalizedMate, if_pos member, if_pos following]
    exact auxiliaryInvolution point member
  · have following : ¬inside (actual point) := by
      intro contrary
      have returned := actualClosed (actual point) contrary
      rw [actualInvolution point] at returned
      exact member returned
    simp only [normalizedMate, if_neg member, if_neg following]
    exact actualInvolution point

theorem normalized_no_fixed_points {Vertex : Type} (inside : Vertex → Prop)
    [DecidablePred inside] (actual auxiliary : Vertex → Vertex)
    (actualDistinct : ∀ point, actual point ≠ point)
    (auxiliaryDistinct : ∀ point, inside point → auxiliary point ≠ point) :
    ∀ point, normalizedMate inside actual auxiliary point ≠ point := by
  intro point
  by_cases member : inside point
  · simpa only [normalizedMate, if_pos member] using auxiliaryDistinct point member
  · simpa only [normalizedMate, if_neg member] using actualDistinct point

theorem normalized_edges_permitted {Vertex : Type} (inside : Vertex → Prop)
    [DecidablePred inside] (actual auxiliary : Vertex → Vertex)
    (permitted : Vertex → Vertex → Prop)
    (actualPermitted : ∀ point, permitted point (actual point))
    (auxiliaryPermitted : ∀ point, inside point → permitted point (auxiliary point)) :
    ∀ point, permitted point (normalizedMate inside actual auxiliary point) := by
  intro point
  by_cases member : inside point
  · simpa only [normalizedMate, if_pos member] using auxiliaryPermitted point member
  · simpa only [normalizedMate, if_neg member] using actualPermitted point

end SubQuorum.PPCycleNormalization

#print axioms SubQuorum.PPCycleNormalization.unchanged_outside
#print axioms SubQuorum.PPCycleNormalization.auxiliary_inside
#print axioms SubQuorum.PPCycleNormalization.normalized_involution
#print axioms SubQuorum.PPCycleNormalization.normalized_no_fixed_points
#print axioms SubQuorum.PPCycleNormalization.normalized_edges_permitted
