import StarForming.DissociationCover

namespace StarForming.HeawoodCertificates

open StarForming.DissociationCover

def label (vertex : Fin 28) : Nat := vertex.val % 14 / 2 + 1

def sheet (vertex : Fin 28) : Nat := vertex.val % 2

def dot (first second : Nat) : Nat :=
  ((first % 2) * (second % 2) + (first / 2 % 2) * (second / 2 % 2) +
    (first / 4) * (second / 4)) % 2

def adjacency (twists : List (Nat × Nat)) (first second : Fin 28) : Prop :=
  (first.val < 14) ≠ (second.val < 14) ∧ dot (label first) (label second) = 0 ∧
    (sheet first + sheet second) % 2 =
      if twists.contains (if first.val < 14 then (label first, label second)
        else (label second, label first)) then 1 else 0

instance (twists : List (Nat × Nat)) : DecidableRel (adjacency twists) :=
  fun first second => inferInstanceAs (Decidable
    ((first.val < 14) ≠ (second.val < 14) ∧ dot (label first) (label second) = 0 ∧
      (sheet first + sheet second) % 2 =
        if twists.contains (if first.val < 14 then (label first, label second)
          else (label second, label first)) then 1 else 0))

def selected (points lines : List Nat) (vertex : Fin 28) : Prop :=
  (if vertex.val < 14 then points else lines).contains
    (10 * label vertex + sheet vertex) = true

instance (points lines : List Nat) : DecidablePred (selected points lines) :=
  fun vertex => inferInstanceAs (Decidable
    ((if vertex.val < 14 then points else lines).contains
      (10 * label vertex + sheet vertex) = true))

def scalarTwists : List (Nat × Nat) := [(3, 3), (1, 2), (2, 1)]

def jordanTwists : List (Nat × Nat) := [(3, 3), (2, 1)]

def scalarPoints : List Nat := [10, 20, 30, 50, 60, 70]

def scalarLines : List Nat := [10, 11, 20, 21, 30, 31, 41, 51, 61, 71]

def jordanPoints : List Nat := [20, 31, 40, 41, 50, 51, 61, 70]

def jordanLines : List Nat := [10, 31, 40, 41, 51, 60, 61, 70]

set_option maxRecDepth 8192 in
set_option maxHeartbeats 800000 in
theorem scalar_dissociates :
    Dissociates (adjacency scalarTwists) (selected scalarPoints scalarLines) := by
  unfold Dissociates
  decide

set_option maxRecDepth 8192 in
set_option maxHeartbeats 800000 in
theorem jordan_dissociates :
    Dissociates (adjacency jordanTwists) (selected jordanPoints jordanLines) := by
  unfold Dissociates
  decide

theorem scalar_card :
    ((List.finRange 28).filter (fun vertex =>
      decide (selected scalarPoints scalarLines vertex))).length = 16 := by
  decide

theorem jordan_card :
    ((List.finRange 28).filter (fun vertex =>
      decide (selected jordanPoints jordanLines vertex))).length = 16 := by
  decide

theorem double_quotient_gap (order size beta : Nat)
    (hcompensation : 7 * size ≤ 3 * order + 2 * beta)
    (hdensity : 15 * order ≤ 28 * beta) :
    196 * (size - beta) ≤ 9 * order := by
  omega

theorem strong_double_quotient_gap (order size beta : Nat)
    (hcompensation : 7 * size ≤ 3 * order + 2 * beta)
    (hdensity : 4 * order ≤ 7 * beta) :
    49 * (size - beta) ≤ order := by
  omega

end StarForming.HeawoodCertificates
