import Mathlib.Data.Fin.Basic
import Mathlib.Algebra.BigOperators.Group.List.Basic
import Mathlib.Data.Nat.Bits
import Mathlib.Tactic

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace SubQuorum.BandCompensation

abbrev Column := Fin 9

def upper (column : Column) : Nat := column.val / 3

def lower (column : Column) : Nat := column.val % 3

def occupied (label : Nat) : Nat := if label = 0 then 0 else 1

def vertexWeight (label : Nat) : Int :=
  if label = 0 then 1 else if label = 1 then -1 else 0

def weight (column : Column) : Int :=
  vertexWeight (upper column) + vertexWeight (lower column)

def endpoint (column : Column) : Prop :=
  upper column ≠ 1 ∧ lower column = 0

instance (column : Column) : Decidable (endpoint column) := inferInstanceAs
  (Decidable (upper column ≠ 1 ∧ lower column = 0))

def compatible (left middle right : Column) : Prop :=
  (upper middle = 1 →
    lower middle = 0 ∧ upper left = 0 ∧ upper right = 0) ∧
  (lower middle = 1 →
    occupied (upper middle) + occupied (lower left) + occupied (lower right) ≤ 1)

instance (left middle right : Column) : Decidable (compatible left middle right) :=
  inferInstanceAs (Decidable
    ((upper middle = 1 →
      lower middle = 0 ∧ upper left = 0 ∧ upper right = 0) ∧
    (lower middle = 1 →
      occupied (upper middle) + occupied (lower left) + occupied (lower right) ≤ 1)))

private def potentialTable : List Int := [
    4, 2, 3, 2, 0, 1, 3, 1, 2,
    3, 1, 2, 1, -1, 0, 2, 0, 1,
    4, 2, 3, 2, 0, 1, 3, 1, 2,
    3, 1, 2, -10000, -10000, -10000, -10000, -10000, -10000,
    -10000, -10000, -10000, -10000, -10000, -10000, -10000, -10000, -10000,
    -10000, -10000, -10000, -10000, -10000, -10000, -10000, -10000, -10000,
    3, 1, 2, 1, -1, 0, 2, 0, 1,
    3, -10000, -10000, 1, -10000, -10000, 2, -10000, -10000,
    3, 1, 2, 1, -1, 0, 2, 0, 1,
    2, 3, 4, 3, 1, 2, 1, 2, 3,
    3, 1, 2, 1, -1, 0, 2, 0, 1,
    4, 2, 3, 2, 0, 1, 3, 1, 2,
    3, 1, 2, -10000, -10000, -10000, -10000, -10000, -10000,
    -10000, -10000, -10000, -10000, -10000, -10000, -10000, -10000, -10000,
    -10000, -10000, -10000, -10000, -10000, -10000, -10000, -10000, -10000,
    4, 2, 3, 2, 0, 1, 3, 1, 2,
    2, -10000, -10000, 0, -10000, -10000, 1, -10000, -10000,
    3, 1, 2, 1, -1, 0, 2, 0, 1]

def potential (odd : Bool) (left current : Column) : Int :=
  potentialTable.getD ((if odd then 81 else 0) + 9*left.val + current.val) (-10000)

def reachable (odd : Bool) (left current : Column) : Prop :=
  potential odd left current ≠ -10000

instance (odd : Bool) (left current : Column) : Decidable (reachable odd left current) :=
  inferInstanceAs (Decidable (potential odd left current ≠ -10000))

theorem potential_start : ∀ current : Column, endpoint current →
    reachable true 0 current ∧ potential true 0 current ≤ weight current := by
  decide

theorem potential_step : ∀ (odd : Bool) (left current next : Column),
    reachable odd left current → compatible left current next →
    reachable (!odd) current next ∧
      potential (!odd) current next ≤ potential odd left current + weight next := by
  decide

theorem potential_finish : ∀ (odd : Bool) (left current : Column),
    reachable odd left current → endpoint current → compatible left current 0 →
    (if odd then (1 : Int) else 2) ≤ potential odd left current := by
  decide

def weightSum (columns : List Column) : Int :=
  (columns.map weight).sum

def blankWeight (column : Column) : Nat :=
  (if upper column = 0 then 1 else 0) + (if lower column = 0 then 1 else 0)

def selectedWeight (column : Column) : Nat :=
  (if upper column = 1 then 1 else 0) + (if lower column = 1 then 1 else 0)

def blankCount (columns : List Column) : Nat :=
  (columns.map blankWeight).sum

def selectedCount (columns : List Column) : Nat :=
  (columns.map selectedWeight).sum

theorem weight_eq_counts : ∀ column : Column,
    weight column = (blankWeight column : Int) - selectedWeight column := by
  decide

theorem weightSum_eq_counts (columns : List Column) :
    weightSum columns = (blankCount columns : Int) - selectedCount columns := by
  induction columns with
  | nil => simp [weightSum, blankCount, selectedCount]
  | cons current rest inductionHypothesis =>
      simp only [weightSum, blankCount, selectedCount, List.map_cons, List.sum_cons,
        Nat.cast_add] at *
      rw [weight_eq_counts]
      omega

def remainingValid (left current : Column) : List Column → Prop
  | [] => endpoint current ∧ compatible left current 0
  | next :: rest => compatible left current next ∧ remainingValid current next rest

def finalParity (odd : Bool) : List Column → Bool
  | [] => odd
  | _ :: rest => finalParity (!odd) rest

theorem finalParity_bodd (start : Nat) (rest : List Column) :
    finalParity (Nat.bodd start) rest = Nat.bodd (start + rest.length) := by
  induction rest generalizing start with
  | nil => simp [finalParity]
  | cons current rest inductionHypothesis =>
      simp only [finalParity, List.length_cons]
      rw [← Nat.bodd_succ, inductionHypothesis]
      congr 1
      omega

theorem finalParity_length (first : Column) (rest : List Column) :
    finalParity true rest = Nat.bodd (first :: rest).length := by
  simpa [Nat.add_comm] using finalParity_bodd 1 rest

theorem potential_telescope (odd : Bool) (left current : Column)
    (rest : List Column) (hreach : reachable odd left current)
    (hvalid : remainingValid left current rest) :
    (if finalParity odd rest then (1 : Int) else 2) ≤
      potential odd left current + weightSum rest := by
  induction rest generalizing odd left current with
  | nil =>
      simpa [finalParity, weightSum] using
        potential_finish odd left current hreach hvalid.1 hvalid.2
  | cons next rest inductionHypothesis =>
      obtain ⟨hnext, hstep⟩ := potential_step odd left current next hreach hvalid.1
      have hrest := inductionHypothesis (!odd) current next hnext hvalid.2
      simp only [finalParity, weightSum, List.map_cons, List.sum_cons] at *
      omega

theorem band_blank_surplus (first : Column) (rest : List Column)
    (hfirst : endpoint first) (hvalid : remainingValid 0 first rest) :
    (if finalParity true rest then (1 : Int) else 2) ≤
      weightSum (first :: rest) := by
  obtain ⟨hreach, hstart⟩ := potential_start first hfirst
  have htelescope := potential_telescope true 0 first rest hreach hvalid
  simp only [weightSum, List.map_cons, List.sum_cons] at *
  omega

theorem even_band_blank_surplus (first : Column) (rest : List Column)
    (hfirst : endpoint first) (hvalid : remainingValid 0 first rest)
    (heven : finalParity true rest = false) :
    (2 : Int) ≤ weightSum (first :: rest) := by
  simpa [heven] using band_blank_surplus first rest hfirst hvalid

theorem odd_band_blank_surplus (first : Column) (rest : List Column)
    (hfirst : endpoint first) (hvalid : remainingValid 0 first rest) :
    (1 : Int) ≤ weightSum (first :: rest) := by
  have hsurplus := band_blank_surplus first rest hfirst hvalid
  split at hsurplus <;> omega

theorem matching_band_compensation
    (first : Column) (rest : List Column)
    (hfirst : endpoint first) (hvalid : remainingValid 0 first rest)
    (heven : finalParity true rest = false)
    (internal crossing : Nat)
    (hvertices : (2 * (first :: rest).length : Nat) =
      selectedCount (first :: rest) + blankCount (first :: rest) + 2*internal + crossing) :
    (2*selectedCount (first :: rest) + 2*internal + crossing : Nat) + 2 ≤
      2 * (first :: rest).length := by
  have hband := even_band_blank_surplus first rest hfirst hvalid heven
  have hsurplus := weightSum_eq_counts (first :: rest)
  omega

#print axioms band_blank_surplus
#print axioms matching_band_compensation

end SubQuorum.BandCompensation
