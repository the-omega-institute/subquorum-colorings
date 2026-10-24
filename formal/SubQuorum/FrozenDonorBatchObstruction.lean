import SubQuorum.FrozenPromotion

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 16000000

namespace SubQuorum.FrozenDonorBatchObstruction

open FrozenPromotion

abbrev Vertex := Fin 40
abbrev Tile := Fin 4 × Fin 5

def coordinates : Array (Nat × Nat) :=
  #[(6, 1), (4, 1), (2, 1), (6, 8), (4, 8), (2, 8), (0, 1), (1, 2), (0, 3), (1, 4), (0, 5), (1, 6), (0, 7), (0, 8), (1, 7), (0, 6), (1, 5), (0, 4), (1, 3), (0, 2), (1, 1), (3, 1), (5, 1), (1, 8), (3, 8), (5, 8), (0, 0), (0, 9), (2, 0), (2, 9), (3, 2), (3, 7), (4, 0), (4, 9), (5, 2), (5, 7), (6, 0), (6, 9), (7, 1), (7, 8)]

def coordinate (vertex : Vertex) : Nat × Nat := coordinates[vertex.val]!

def adjacent (first second : Vertex) : Prop :=
  (coordinate first).1 = (coordinate second).1 ∧
    ((coordinate first).2+1 = (coordinate second).2 ∨
      (coordinate second).2+1 = (coordinate first).2) ∨
  (coordinate first).2 = (coordinate second).2 ∧
    ((coordinate first).1+1 = (coordinate second).1 ∨
      (coordinate second).1+1 = (coordinate first).1)

instance (first second : Vertex) : Decidable (adjacent first second) := by
  unfold adjacent
  infer_instance

def Selected (vertex : Vertex) : Prop := 26 ≤ vertex.val
def Endpoint (vertex : Vertex) : Prop := vertex.val < 26

instance (vertex : Vertex) : Decidable (Selected vertex) := by
  unfold Selected
  infer_instance

instance (vertex : Vertex) : Decidable (Endpoint vertex) := by
  unfold Endpoint
  infer_instance

def mateIndices : Array Nat :=
  #[22, 21, 20, 25, 24, 23, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 2, 1, 0, 5, 4, 3, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]

def mate (vertex : Vertex) : Vertex := Fin.ofNat 40 mateIndices[vertex.val]!

theorem coordinates_inside : ∀ vertex : Vertex,
    (coordinate vertex).1 < 8 ∧ (coordinate vertex).2 < 10 := by decide

theorem coordinates_injective : ∀ first second : Vertex,
    coordinate first = coordinate second → first = second := by decide

theorem matching_involution : ∀ vertex : Vertex, mate (mate vertex) = vertex := by decide

theorem matching_endpoint : ∀ vertex : Vertex, Endpoint vertex →
    Endpoint (mate vertex) ∧ adjacent vertex (mate vertex) := by decide

theorem selected_feasible : ∀ chosen : Vertex, Selected chosen →
    ((List.finRange 40).filter fun other => decide (adjacent chosen other)).length ≤ 1 := by decide

theorem endpoints_terminal : ∀ vertex : Vertex, Endpoint vertex →
    3 ≤ ((List.finRange 40).filter fun other => decide (adjacent vertex other)).length := by decide

theorem frozen_00 : Frozen adjacent Selected mate (0 : Vertex) := by
  exact .two_selected 0 36 38 (by decide) (by decide) (by decide) (by decide) (by decide)

theorem frozen_01 : Frozen adjacent Selected mate (1 : Vertex) := by
  exact .selected_frozen 1 32 22 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (0 : Vertex); exact frozen_00)

theorem frozen_02 : Frozen adjacent Selected mate (2 : Vertex) := by
  exact .selected_frozen 2 28 21 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (1 : Vertex); exact frozen_01)

theorem frozen_03 : Frozen adjacent Selected mate (3 : Vertex) := by
  exact .two_selected 3 37 39 (by decide) (by decide) (by decide) (by decide) (by decide)

theorem frozen_04 : Frozen adjacent Selected mate (4 : Vertex) := by
  exact .selected_frozen 4 33 25 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (3 : Vertex); exact frozen_03)

theorem frozen_05 : Frozen adjacent Selected mate (5 : Vertex) := by
  exact .selected_frozen 5 29 24 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (4 : Vertex); exact frozen_04)

theorem frozen_06 : Frozen adjacent Selected mate (6 : Vertex) := by
  exact .selected_frozen 6 26 20 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (2 : Vertex); exact frozen_02)

theorem frozen_07 : Frozen adjacent Selected mate (7 : Vertex) := by
  exact .two_frozen 7 19 20 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (6 : Vertex); exact frozen_06)
    (by change Frozen adjacent Selected mate (2 : Vertex); exact frozen_02)

theorem frozen_08 : Frozen adjacent Selected mate (8 : Vertex) := by
  exact .two_frozen 8 18 19 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (7 : Vertex); exact frozen_07)
    (by change Frozen adjacent Selected mate (6 : Vertex); exact frozen_06)

theorem frozen_09 : Frozen adjacent Selected mate (9 : Vertex) := by
  exact .two_frozen 9 17 18 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (8 : Vertex); exact frozen_08)
    (by change Frozen adjacent Selected mate (7 : Vertex); exact frozen_07)

theorem frozen_10 : Frozen adjacent Selected mate (10 : Vertex) := by
  exact .two_frozen 10 16 17 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (9 : Vertex); exact frozen_09)
    (by change Frozen adjacent Selected mate (8 : Vertex); exact frozen_08)

theorem frozen_11 : Frozen adjacent Selected mate (11 : Vertex) := by
  exact .two_frozen 11 15 16 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (10 : Vertex); exact frozen_10)
    (by change Frozen adjacent Selected mate (9 : Vertex); exact frozen_09)

theorem frozen_12 : Frozen adjacent Selected mate (12 : Vertex) := by
  exact .two_frozen 12 14 15 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (11 : Vertex); exact frozen_11)
    (by change Frozen adjacent Selected mate (10 : Vertex); exact frozen_10)

theorem frozen_13 : Frozen adjacent Selected mate (13 : Vertex) := by
  exact .selected_frozen 13 27 23 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (5 : Vertex); exact frozen_05)

theorem frozen_14 : Frozen adjacent Selected mate (14 : Vertex) := by
  exact .two_frozen 14 12 23 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (13 : Vertex); exact frozen_13)
    (by change Frozen adjacent Selected mate (5 : Vertex); exact frozen_05)

theorem frozen_15 : Frozen adjacent Selected mate (15 : Vertex) := by
  exact .two_frozen 15 11 12 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (14 : Vertex); exact frozen_14)
    (by change Frozen adjacent Selected mate (13 : Vertex); exact frozen_13)

theorem frozen_16 : Frozen adjacent Selected mate (16 : Vertex) := by
  exact .two_frozen 16 10 11 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (15 : Vertex); exact frozen_15)
    (by change Frozen adjacent Selected mate (14 : Vertex); exact frozen_14)

theorem frozen_17 : Frozen adjacent Selected mate (17 : Vertex) := by
  exact .two_frozen 17 9 10 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (16 : Vertex); exact frozen_16)
    (by change Frozen adjacent Selected mate (15 : Vertex); exact frozen_15)

theorem frozen_18 : Frozen adjacent Selected mate (18 : Vertex) := by
  exact .two_frozen 18 8 9 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (17 : Vertex); exact frozen_17)
    (by change Frozen adjacent Selected mate (16 : Vertex); exact frozen_16)

theorem frozen_19 : Frozen adjacent Selected mate (19 : Vertex) := by
  exact .two_frozen 19 7 8 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (18 : Vertex); exact frozen_18)
    (by change Frozen adjacent Selected mate (17 : Vertex); exact frozen_17)

theorem frozen_20 : Frozen adjacent Selected mate (20 : Vertex) := by
  exact .two_frozen 20 6 7 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (19 : Vertex); exact frozen_19)
    (by change Frozen adjacent Selected mate (18 : Vertex); exact frozen_18)

theorem frozen_21 : Frozen adjacent Selected mate (21 : Vertex) := by
  exact .selected_frozen 21 30 2 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (20 : Vertex); exact frozen_20)

theorem frozen_22 : Frozen adjacent Selected mate (22 : Vertex) := by
  exact .selected_frozen 22 34 1 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (21 : Vertex); exact frozen_21)

theorem frozen_23 : Frozen adjacent Selected mate (23 : Vertex) := by
  exact .two_frozen 23 13 14 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (12 : Vertex); exact frozen_12)
    (by change Frozen adjacent Selected mate (11 : Vertex); exact frozen_11)

theorem frozen_24 : Frozen adjacent Selected mate (24 : Vertex) := by
  exact .selected_frozen 24 31 5 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (23 : Vertex); exact frozen_23)

theorem frozen_25 : Frozen adjacent Selected mate (25 : Vertex) := by
  exact .selected_frozen 25 35 4 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (24 : Vertex); exact frozen_24)

theorem all_endpoints_frozen (vertex : Vertex) (hendpoint : Endpoint vertex) :
    Frozen adjacent Selected mate vertex := by
  rcases vertex with ⟨value, bound⟩
  match value with
  | 0 => exact frozen_00
  | 1 => exact frozen_01
  | 2 => exact frozen_02
  | 3 => exact frozen_03
  | 4 => exact frozen_04
  | 5 => exact frozen_05
  | 6 => exact frozen_06
  | 7 => exact frozen_07
  | 8 => exact frozen_08
  | 9 => exact frozen_09
  | 10 => exact frozen_10
  | 11 => exact frozen_11
  | 12 => exact frozen_12
  | 13 => exact frozen_13
  | 14 => exact frozen_14
  | 15 => exact frozen_15
  | 16 => exact frozen_16
  | 17 => exact frozen_17
  | 18 => exact frozen_18
  | 19 => exact frozen_19
  | 20 => exact frozen_20
  | 21 => exact frozen_21
  | 22 => exact frozen_22
  | 23 => exact frozen_23
  | 24 => exact frozen_24
  | 25 => exact frozen_25
  | value+26 =>
      change value+26 < 26 at hendpoint
      omega

theorem no_feasible_bundle (promoted retained : Vertex → Prop)
    (hpromoted : ∀ vertex, promoted vertex → Endpoint vertex)
    (hselected : ∀ vertex, Selected vertex → retained vertex)
    (hretained : ∀ vertex, ¬promoted (mate vertex) → retained vertex)
    (hfeasible : ∀ vertex first second, promoted vertex →
      adjacent vertex first → adjacent vertex second →
      retained first → retained second → first = second) :
    ∀ vertex, ¬promoted vertex := by
  intro vertex hpromotion
  exact frozen_exclusion adjacent Selected promoted retained mate hselected hretained
    hfeasible vertex (all_endpoints_frozen vertex (hpromoted vertex hpromotion)) hpromotion

def tileOf (vertex : Vertex) : Tile :=
  (Fin.ofNat 4 ((coordinate vertex).1/2), Fin.ofNat 5 ((coordinate vertex).2/2))

def endpointCount (row column : Nat) : Nat :=
  ((List.finRange 40).filter fun vertex => decide (Endpoint vertex ∧
    (coordinate vertex).1/2 = row ∧ (coordinate vertex).2/2 = column)).length

def selectedCount (row column : Nat) : Nat :=
  ((List.finRange 40).filter fun vertex => decide (Selected vertex ∧
    (coordinate vertex).1/2 = row ∧ (coordinate vertex).2/2 = column)).length

def tiles : List Tile := (List.finRange 4).flatMap fun row =>
  (List.finRange 5).map fun column => (row, column)

def receiverTiles : List Tile := tiles.filter fun tile => 0 < endpointCount tile.1.val tile.2.val

def rawChargeTwice (tile : Tile) : Int :=
  2*(selectedCount tile.1.val tile.2.val : Int)+(endpointCount tile.1.val tile.2.val : Int)-4

def transferCount (tile : Tile) : Nat :=
  ((List.finRange 40).filter fun vertex => decide (Endpoint vertex ∧
    selectedCount (tileOf vertex).1.val (tileOf vertex).2.val = 2 ∧ tileOf (mate vertex) = tile)).length

def correctedChargeTwice (tile : Tile) : Int :=
  if selectedCount tile.1.val tile.2.val < 2 then rawChargeTwice tile+(transferCount tile : Int) else 0

def deficit (row column : Nat) : Nat := 2-selectedCount row column

theorem receiver_inventory : receiverTiles.length = 11 ∧
    (receiverTiles.map fun tile => selectedCount tile.1.val tile.2.val).sum = 10 := by decide

theorem original_corrected_receiver_charge :
    (receiverTiles.map correctedChargeTwice).sum = 2 := by decide

theorem selected_matching_inventory :
    ((List.finRange 40).filter fun vertex => decide (Selected vertex)).length = 14 ∧
    ((List.finRange 40).filter fun vertex => decide (Endpoint vertex)).length = 26 := by decide

theorem original_objective : 14+13 < 8*10/2 := by decide

theorem endpoint_degree_exact : ∀ vertex : Vertex, Endpoint vertex →
    ((List.finRange 40).filter fun other => decide (adjacent vertex other)).length = 3 := by decide

def pointAdjacent (first second : Nat × Nat) : Bool :=
  (first.1 == second.1 && (first.2+1 == second.2 || second.2+1 == first.2)) ||
    (first.2 == second.2 && (first.1+1 == second.1 || second.1+1 == first.1))

def oppositeCorner (vertex : Vertex) : Nat × Nat :=
  (4*((coordinate vertex).1/2)+1-(coordinate vertex).1,
    4*((coordinate vertex).2/2)+1-(coordinate vertex).2)

def donorWitness (chosen anchor guard : Vertex) : Prop :=
  Selected chosen ∧ Endpoint anchor ∧ Endpoint guard ∧
    endpointCount (tileOf chosen).1.val (tileOf chosen).2.val = 0 ∧
    selectedCount (tileOf chosen).1.val (tileOf chosen).2.val = 1 ∧
    tileOf anchor ≠ tileOf chosen ∧ tileOf guard ≠ tileOf chosen ∧
    adjacent chosen anchor ∧ pointAdjacent (coordinate guard) (oppositeCorner chosen) = true ∧
    ((List.finRange 40).filter fun other => decide (Endpoint other ∧ adjacent guard other)).length = 3

instance (chosen anchor guard : Vertex) : Decidable (donorWitness chosen anchor guard) := by
  unfold donorWitness
  infer_instance

theorem left_donor_witness : donorWitness 30 21 18 ∧ tileOf 30 = (1,1) := by decide

theorem right_donor_witness : donorWitness 31 24 11 ∧ tileOf 31 = (1,3) := by decide

theorem endpoint_free_tiles_exact : ∀ row : Fin 4, ∀ column : Fin 5,
    endpointCount row.val column.val = 0 ↔ 1 ≤ row.val ∧ 1 ≤ column.val ∧ column.val ≤ 3 := by
  decide

def residualCapacity (mask : Fin 4) (row column : Nat) : Nat :=
  if endpointCount row column = 0 then
    deficit row column -
      (if mask.val%2 = 1 ∧ row = 1 ∧ column = 1 then 1 else 0) -
      (if mask.val/2 = 1 ∧ row = 1 ∧ column = 3 then 1 else 0)
  else 0

def horizontalCapacity (mask : Fin 4) (row : Nat) : Nat :=
  ((List.range 5).map fun column => residualCapacity mask row column).sum

def verticalCapacity (mask : Fin 4) (column : Nat) : Nat :=
  ((List.range 4).map fun row => residualCapacity mask row column).sum

def halfQuota (mask : Fin 4) : Nat :=
  ((List.range 4).map fun row => horizontalCapacity mask row/2).sum+
    ((List.range 5).map fun column => verticalCapacity mask column/2).sum

def localQuota (degree : Nat) : Nat := if degree = 0 then 0 else max 1 (degree/2)

def localQuotaTotal (mask : Fin 4) : Nat :=
  ((List.range 4).map fun row => localQuota (horizontalCapacity mask row)).sum+
    ((List.range 5).map fun column => localQuota (verticalCapacity mask column)).sum

def reservedCount (mask : Fin 4) : Nat := mask.val%2+mask.val/2

theorem base_capacity_matrix :
    ((List.range 4).map fun row => (List.range 5).map fun column =>
      residualCapacity 0 row column) =
      [[0,0,0,0,0], [0,1,2,1,0], [0,1,2,1,0], [0,2,2,2,0]] := by decide

theorem quota_totals :
    halfQuota 0 = 14 ∧ halfQuota 1 = 12 ∧ halfQuota 2 = 12 ∧ halfQuota 3 = 11 := by decide

theorem local_quota_gives_no_extra : ∀ mask : Fin 4,
    localQuotaTotal mask = halfQuota mask := by decide

theorem no_nonempty_batch_preserves_quota : ∀ mask : Fin 4, 0 < mask.val →
    reservedCount mask+localQuotaTotal mask = 13 ∧
      reservedCount mask+localQuotaTotal mask < localQuotaTotal 0 := by decide

theorem no_nonempty_batch_preserves_mixed_score : ∀ mask : Fin 4, 0 < mask.val →
    reservedCount mask+max 6 (halfQuota mask) = 13 ∧
      reservedCount mask+max 6 (halfQuota mask) < max 6 (halfQuota 0) := by decide

theorem all_width_budget_loss (halfWidth : Nat) (hwidth : 4 ≤ halfWidth) :
    max (halfWidth+2) (6*halfWidth-10) = 6*halfWidth-10 ∧
    1+max (halfWidth+2) (6*halfWidth-12) = 6*halfWidth-11 ∧
    2+max (halfWidth+2) (6*halfWidth-13) = 6*halfWidth-11 := by
  omega

end SubQuorum.FrozenDonorBatchObstruction
