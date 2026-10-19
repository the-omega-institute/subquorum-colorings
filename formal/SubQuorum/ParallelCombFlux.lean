import SubQuorum.CombEndFlux

set_option autoImplicit false

namespace SubQuorum.ParallelCombFlux

open OwnedDonorCompensation LongBentTerminalStrips

def horizontalComb (length : Nat) (row column : Int) : Label :=
  if row = 0 then
    if 0 ≤ column ∧ column < 2*(length : Int) then .endpoint
    else if column = -1 ∨ column = 2*(length : Int) then .selected else .blank
  else if (row = 1 ∧ 0 ≤ column ∧ column < 2*(length : Int) ∧ column % 2 = 1) ∨
      (row = -1 ∧ 0 ≤ column ∧ column < 2*(length : Int) ∧ column % 2 = 0)
    then .selected else .blank

def endpointCount : Label → Nat
  | .endpoint => 1
  | _ => 0

def tileCounts (length : Nat) (column : Int) : Nat × Nat :=
  let labels := [horizontalComb length 0 column, horizontalComb length 0 (column+1),
    horizontalComb length 1 column, horizontalComb length 1 (column+1)]
  ((labels.map endpointCount).sum, (labels.map selectedCount).sum)

def rawExcessTwice (length : Nat) (column : Int) : Int :=
  let counts := tileCounts length column
  (counts.1 : Int)+2*(counts.2 : Int)-4

theorem aligned_tile_counts (length : Nat) (index : Int)
    (hlower : 0 ≤ index) (hupper : index < length) :
    tileCounts length (2*index) = (2, 1) := by
  have hfirst : 0 ≤ 2*index ∧ 2*index < 2*(length : Int) := by omega
  have hsecond : 0 ≤ 2*index+1 ∧ 2*index+1 < 2*(length : Int) := by omega
  have heven : (2*index) % 2 = 0 := by omega
  have hodd : (2*index+1) % 2 = 1 := by omega
  simp [tileCounts, horizontalComb, hfirst, hsecond, heven, hodd, hupper,
    endpointCount, selectedCount]

theorem first_shifted_tile_counts (length : Nat) (hpositive : 1 ≤ length) :
    tileCounts length (-1) = (1, 1) := by
  have hzero : (0 : Int) < 2*(length : Int) := by omega
  simp [tileCounts, horizontalComb, hzero, endpointCount, selectedCount]

theorem last_shifted_tile_counts (length : Nat) (hpositive : 1 ≤ length) :
    tileCounts length (2*(length : Int)-1) = (1, 2) := by
  have hinside : 0 ≤ 2*(length : Int)-1 ∧ 2*(length : Int)-1 < 2*(length : Int) := by omega
  have hbound : 1 ≤ 2*(length : Int) := by omega
  have hlast : 2*(length : Int)-1+1 = 2*(length : Int) := by omega
  have hodd : (2*(length : Int)-1) % 2 = 1 := by omega
  simp [tileCounts, horizontalComb, hinside, hbound, hlast, hodd,
    endpointCount, selectedCount]

theorem middle_shifted_tile_counts (length : Nat) (index : Int)
    (hlower : 1 ≤ index) (hupper : index < length) :
    tileCounts length (2*index-1) = (2, 1) := by
  have hfirst : 0 ≤ 2*index-1 ∧ 2*index-1 < 2*(length : Int) := by omega
  have hsecond : 0 ≤ 2*index ∧ 2*index < 2*(length : Int) := by omega
  have hnext : 2*index-1+1 = 2*index := by omega
  have hodd : (2*index-1) % 2 = 1 := by omega
  have heven : (2*index) % 2 = 0 := by omega
  have hbound : 1 ≤ 2*index := by omega
  simp [tileCounts, horizontalComb, hfirst, hsecond, hnext, hodd, heven, hbound, hupper,
    endpointCount, selectedCount]

private theorem range_sum_zero (size : Nat) (function : Nat → Int)
    (hzero : ∀ index, index < size → function index = 0) :
    ((List.range size).map function).sum = 0 := by
  induction size with
  | zero => simp
  | succ size inductionHypothesis =>
      have hprevious := inductionHypothesis (fun index hindex => hzero index (by omega))
      simp [List.range_succ, hprevious, hzero size (by omega)]

theorem whole_parallel_comb_balance (length : Nat) (hpositive : 1 ≤ length) :
    ((List.range length).map (fun (index : Nat) => rawExcessTwice length (2*(index : Int)))).sum = 0 ∧
    rawExcessTwice length (-1)+
      ((List.range (length-1)).map
        (fun (index : Nat) => rawExcessTwice length (2*((index : Int)+1)-1))).sum+
      rawExcessTwice length (2*(length : Int)-1) = 0 := by
  have haligned := range_sum_zero length
    (fun index => rawExcessTwice length (2*(index : Int))) (by
      intro index hindex
      simp [rawExcessTwice, aligned_tile_counts length index (by omega) (by omega)])
  have hmiddle := range_sum_zero (length-1)
    (fun index => rawExcessTwice length (2*((index : Int)+1)-1)) (by
      intro index hindex
      simp [rawExcessTwice, middle_shifted_tile_counts length ((index : Int)+1)
        (by omega) (by omega)])
  constructor
  · exact haligned
  · rw [hmiddle]
    simp [rawExcessTwice, first_shifted_tile_counts length hpositive,
      last_shifted_tile_counts length hpositive]

end SubQuorum.ParallelCombFlux
