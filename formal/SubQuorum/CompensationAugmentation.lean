import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.CompensationAugmentation

theorem simple_path_cannot_reenter_start {Vertex : Type}
    (vertex : Nat → Vertex) (length : Nat)
    (simple : ∀ first, first ≤ length → ∀ second, second ≤ length →
      vertex first = vertex second → first = second)
    (step : Nat) (bound : step < length) :
    vertex (step + 1) ≠ vertex 0 := by
  intro same
  have impossible := simple (step + 1) (by omega) 0 (by omega) same
  omega

theorem simple_path_cannot_leave_finish {Vertex : Type}
    (vertex : Nat → Vertex) (length : Nat)
    (simple : ∀ first, first ≤ length → ∀ second, second ≤ length →
      vertex first = vertex second → first = second)
    (step : Nat) (bound : step < length) :
    vertex step ≠ vertex length := by
  intro same
  have impossible := simple step (by omega) length (by omega) same
  omega

theorem saturated_source_arc_untouched {Vertex Edge : Type}
    (vertex : Nat → Vertex) (length : Nat)
    (simple : ∀ first, first ≤ length → ∀ second, second ≤ length →
      vertex first = vertex second → first = second)
    (edge : Nat → Edge) (forward : Nat → Bool) (tail : Edge → Vertex)
    (flow capacity : Edge → Nat) (boundary : Edge)
    (atSource : tail boundary = vertex 0)
    (saturated : flow boundary = capacity boundary)
    (forwardResidual : ∀ step, step < length → forward step = true →
      flow (edge step) < capacity (edge step))
    (reverseWalk : ∀ step, step < length → forward step = false →
      tail (edge step) = vertex (step + 1)) :
    ∀ step, step < length → edge step ≠ boundary := by
  intro step bound same
  cases orientation : forward step with
  | false =>
    have reached := reverseWalk step bound orientation
    rw [same, atSource] at reached
    exact simple_path_cannot_reenter_start vertex length simple step bound reached.symm
  | true =>
    have available := forwardResidual step bound orientation
    rw [same, saturated] at available
    omega

theorem saturated_resource_arc_untouched {Vertex Edge : Type}
    (vertex : Nat → Vertex) (length : Nat)
    (simple : ∀ first, first ≤ length → ∀ second, second ≤ length →
      vertex first = vertex second → first = second)
    (edge : Nat → Edge) (forward : Nat → Bool) (head : Edge → Vertex)
    (flow capacity : Edge → Nat) (boundary : Edge)
    (atSink : head boundary = vertex length)
    (saturated : flow boundary = capacity boundary)
    (forwardResidual : ∀ step, step < length → forward step = true →
      flow (edge step) < capacity (edge step))
    (reverseWalk : ∀ step, step < length → forward step = false →
      head (edge step) = vertex step) :
    ∀ step, step < length → edge step ≠ boundary := by
  intro step bound same
  cases orientation : forward step with
  | false =>
    have reached := reverseWalk step bound orientation
    rw [same, atSink] at reached
    exact simple_path_cannot_leave_finish vertex length simple step bound reached.symm
  | true =>
    have available := forwardResidual step bound orientation
    rw [same, saturated] at available
    omega

def applyResidualMoves {Edge : Type} [DecidableEq Edge]
    (flow : Edge → Int) : List (Edge × Bool) → Edge → Int
  | [], boundary => flow boundary
  | (edge, forward) :: rest, boundary =>
      applyResidualMoves flow rest boundary +
        if edge = boundary then (if forward then 1 else -1) else 0

theorem untouched_arc_keeps_flow {Edge : Type} [DecidableEq Edge]
    (flow : Edge → Int) (moves : List (Edge × Bool)) (boundary : Edge)
    (untouched : ∀ move ∈ moves, move.1 ≠ boundary) :
    applyResidualMoves flow moves boundary = flow boundary := by
  induction moves with
  | nil => rfl
  | cons move rest previous =>
    have headDistinct := untouched move (by simp)
    have restUntouched : ∀ other ∈ rest, other.1 ≠ boundary := by
      intro other member
      exact untouched other (by simp [member])
    rcases move with ⟨edge, forward⟩
    simp only [applyResidualMoves]
    rw [previous restUntouched]
    simp at headDistinct
    simp [headDistinct]

end SubQuorum.CompensationAugmentation

#print axioms SubQuorum.CompensationAugmentation.simple_path_cannot_reenter_start
#print axioms SubQuorum.CompensationAugmentation.simple_path_cannot_leave_finish
#print axioms SubQuorum.CompensationAugmentation.saturated_source_arc_untouched
#print axioms SubQuorum.CompensationAugmentation.saturated_resource_arc_untouched
#print axioms SubQuorum.CompensationAugmentation.untouched_arc_keeps_flow
