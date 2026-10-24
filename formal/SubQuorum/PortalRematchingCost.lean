import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.PortalRematchingCost

structure Position where
  band : Int
  column : Int

def GridStep (first second : Position) : Prop :=
  (first.band = second.band ∧
    -1 ≤ first.column - second.column ∧ first.column - second.column ≤ 1) ∨
  (first.column = second.column ∧
    -1 ≤ first.band - second.band ∧ first.band - second.band ≤ 1)

inductive Walk : Position → Position → Nat → Prop where
  | stop (position : Position) : Walk position position 0
  | auxiliary (first second finish : Position) (cost : Nat)
      (sameBand : first.band = second.band)
      (sameColumn : first.column = second.column)
      (tail : Walk second finish cost) : Walk first finish cost
  | grid (first second finish : Position) (cost : Nat)
      (step : GridStep first second)
      (tail : Walk second finish cost) : Walk first finish (cost + 1)

theorem band_column_drop {first finish : Position} {cost : Nat}
    (walk : Walk first finish cost) :
    first.band + first.column - finish.band - finish.column ≤ (cost : Int) := by
  induction walk with
  | stop position => omega
  | auxiliary first second finish cost sameBand sameColumn tail inductionHypothesis =>
    omega
  | grid first second finish cost step tail inductionHypothesis =>
    rcases step with horizontal | vertical
    · obtain ⟨sameBand, lower, upper⟩ := horizontal
      omega
    · obtain ⟨sameColumn, lower, upper⟩ := vertical
      omega

theorem column_drop {first finish : Position} {cost : Nat}
    (walk : Walk first finish cost) :
    first.column - finish.column ≤ (cost : Int) := by
  induction walk with
  | stop position => omega
  | auxiliary first second finish cost sameBand sameColumn tail inductionHypothesis =>
    omega
  | grid first second finish cost step tail inductionHypothesis =>
    rcases step with horizontal | vertical
    · obtain ⟨sameBand, lower, upper⟩ := horizontal
      omega
    · obtain ⟨sameColumn, lower, upper⟩ := vertical
      omega

theorem upper_source_cost {column : Int} {cost : Nat}
    (walk : Walk ⟨2, column⟩ ⟨2, column - 2⟩ cost) :
    3 ≤ cost + 1 := by
  have bound := column_drop walk
  change column - (column - 2) ≤ (cost : Int) at bound
  omega

theorem lower_source_upper_target_cost {column : Int} {halfWidth cost : Nat}
    (walk : Walk ⟨(halfWidth : Int) + 2, column⟩ ⟨2, column - 2⟩ cost) :
    halfWidth + 3 ≤ cost + 1 := by
  have bound := band_column_drop walk
  change (halfWidth : Int) + 2 + column - 2 - (column - 2) ≤ (cost : Int) at bound
  omega

theorem lower_source_lower_target_cost {column : Int} {halfWidth tailLength cost : Nat}
    (walk : Walk ⟨(halfWidth : Int) + 2, column⟩
      ⟨(halfWidth : Int) + 2, column - (tailLength : Int)⟩ cost) :
    tailLength + 1 ≤ cost + 1 := by
  have bound := column_drop walk
  change column - (column - (tailLength : Int)) ≤ (cost : Int) at bound
  omega

theorem prescribed_lower_source_cost {column : Int} {halfWidth tailLength cost : Nat}
    (walk : Walk ⟨(halfWidth : Int) + 2, column⟩ ⟨2, column - 2⟩ cost ∨
      Walk ⟨(halfWidth : Int) + 2, column⟩
        ⟨(halfWidth : Int) + 2, column - (tailLength : Int)⟩ cost) :
    min (tailLength + 1) (halfWidth + 3) ≤ cost + 1 := by
  rcases walk with upper | lower
  · have bound := lower_source_upper_target_cost upper
    omega
  · have bound := lower_source_lower_target_cost lower
    omega

theorem cost_growth (index : Nat) :
    min (2 * index + 1) (2 * index + 3) = 2 * index + 1 := by
  omega

#print axioms band_column_drop
#print axioms column_drop
#print axioms upper_source_cost
#print axioms lower_source_upper_target_cost
#print axioms lower_source_lower_target_cost
#print axioms prescribed_lower_source_cost
#print axioms cost_growth

end SubQuorum.PortalRematchingCost
