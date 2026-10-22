import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 10000
set_option maxHeartbeats 4000000

namespace SubQuorum.BoundedHeightSharpChains

def time (index remaining endpoint : Nat) : Nat :=
  match endpoint with
  | 0 => 3*index+1
  | 1 => 3*remaining+6
  | 2 => 3*index+2
  | 3 => 3*remaining+5
  | 4 => 3*index+3
  | 5 => if remaining = 0 then 1 else 3*remaining+4
  | 6 => 3*index+4
  | 7 => 4
  | 8 => 3*index+3
  | 9 => 3*remaining+5
  | 10 => 3
  | 11 => 3*index+5
  | 12 => 1
  | 13 => 1
  | 14 => 3*index+6
  | 15 => 2
  | _ => 0

def median (first second third : Nat) : Nat :=
  max (min first second) (min (max first second) third)

def rightSupportTime (remaining : Nat) : Nat :=
  if remaining = 0 then 0 else 3*remaining+3

theorem all_local_recurrences (index remaining : Nat) :
    time index remaining 0 = 1+3*index ∧
    time index remaining 1 = 1+max (time index remaining 3) (time index remaining 10) ∧
    time index remaining 2 = 1+min (time index remaining 0) (time index remaining 8) ∧
    time index remaining 3 = 1+max (time index remaining 5) (time index remaining 7) ∧
    time index remaining 4 = 1+max (time index remaining 2) (time index remaining 12) ∧
    time index remaining 5 = 1+rightSupportTime remaining ∧
    time index remaining 6 = 1+max (time index remaining 0) (time index remaining 8) ∧
    time index remaining 7 = 1+median (time index remaining 10) (time index remaining 3) (time index remaining 15) ∧
    time index remaining 8 = 1+max (time index remaining 2) (time index remaining 12) ∧
    time index remaining 9 = 1+max (time index remaining 5) (time index remaining 7) ∧
    time index remaining 10 = 1+max (time index remaining 15) (time index remaining 13) ∧
    time index remaining 11 = 1+max (time index remaining 8) (time index remaining 6) ∧
    time index remaining 12 = 1 ∧ time index remaining 13 = 1 ∧
    time index remaining 14 = 1+max (time index remaining 6) (time index remaining 11) ∧
    time index remaining 15 = 1+time index remaining 13 := by
  by_cases boundary : remaining = 0
  · simp [time, rightSupportTime, median, boundary]
    omega
  · simp [time, rightSupportTime, median, boundary]
    omega

theorem left_relay (index remaining : Nat) (hinterior : 0 < index) :
    time (index-1) (remaining+1) 4 = 3*index := by
  simp only [time]
  omega

theorem right_relay (index remaining : Nat) (hinterior : 0 < remaining) :
    time (index+1) (remaining-1) 1 = rightSupportTime remaining := by
  have nonzero : remaining ≠ 0 := by omega
  simp only [time, rightSupportTime, if_neg nonzero]
  omega

theorem all_times_positive_and_bounded (copies index remaining : Nat)
    (hposition : copies = index+remaining+1) (endpoint : Fin 16) :
    0 < time index remaining endpoint.val ∧ time index remaining endpoint.val ≤ 3*copies+3 := by
  have cases : endpoint.val = 0 ∨ endpoint.val = 1 ∨ endpoint.val = 2 ∨ endpoint.val = 3 ∨
      endpoint.val = 4 ∨ endpoint.val = 5 ∨ endpoint.val = 6 ∨ endpoint.val = 7 ∨
      endpoint.val = 8 ∨ endpoint.val = 9 ∨ endpoint.val = 10 ∨ endpoint.val = 11 ∨
      endpoint.val = 12 ∨ endpoint.val = 13 ∨ endpoint.val = 14 ∨ endpoint.val = 15 := by
    omega
  rcases cases with equation | equation | equation | equation | equation | equation | equation | equation |
    equation | equation | equation | equation | equation | equation | equation | equation
  all_goals simp only [equation, time]
  all_goals first | omega | (split <;> omega)

theorem last_endpoint_attains (copies : Nat) (hpositive : 0 < copies) :
    time (copies-1) 0 14 = 3*copies+3 := by
  simp only [time]
  omega

theorem first_endpoint_attains (copies : Nat) (hpositive : 0 < copies) :
    time 0 (copies-1) 1 = 3*copies+3 := by
  simp only [time]
  omega

theorem unbounded_displayed_depth (bound : Nat) :
    bound < time bound 0 14 := by
  simp only [time]
  omega

theorem fixed_height_board_margin (copies : Nat) :
    5*(6*copies+2) = (16*copies+2)+(14*copies+8) := by omega

#print axioms all_local_recurrences
#print axioms left_relay
#print axioms right_relay
#print axioms all_times_positive_and_bounded
#print axioms last_endpoint_attains
#print axioms first_endpoint_attains
#print axioms unbounded_displayed_depth
#print axioms fixed_height_board_margin

end SubQuorum.BoundedHeightSharpChains
