import SubQuorum.FrozenPromotion

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 16000000

namespace SubQuorum.CapacityOneStripObstruction

open FrozenPromotion

abbrev Vertex := Fin 54
abbrev Tile := Fin 4 × Fin 5

def coordinates : Array (Nat × Nat) :=
  #[(1, 1), (2, 4), (3, 8), (1, 3), (2, 2), (3, 1), (5, 8), (4, 2), (5, 1), (7, 8), (6, 2), (6, 7), (7, 1), (6, 4), (7, 3), (7, 6), (6, 5), (6, 6), (7, 5), (7, 4), (7, 7), (6, 3), (6, 8), (4, 8), (7, 2), (6, 1), (5, 2), (4, 1), (3, 2), (2, 1), (1, 2), (2, 3), (0, 1), (0, 3), (0, 5), (0, 6), (0, 8), (0, 9), (1, 0), (1, 7), (2, 5), (2, 8), (3, 0), (3, 4), (3, 6), (3, 9), (4, 3), (4, 7), (5, 0), (5, 4), (5, 6), (5, 9), (7, 0), (7, 9)]

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

def Selected (vertex : Vertex) : Prop := 32 ≤ vertex.val
def Endpoint (vertex : Vertex) : Prop := vertex.val < 32

instance (vertex : Vertex) : Decidable (Selected vertex) := by
  unfold Selected
  infer_instance

instance (vertex : Vertex) : Decidable (Endpoint vertex) := by
  unfold Endpoint
  infer_instance

def mateIndices : Array Nat :=
  #[29, 31, 23, 30, 28, 27, 22, 26, 25, 20, 21, 17, 24, 16, 19, 18, 13, 11, 15, 14, 9, 10, 6, 2, 12, 8, 7, 5, 4, 0, 3, 1, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53]

def mate (vertex : Vertex) : Vertex := Fin.ofNat 54 mateIndices[vertex.val]!

theorem coordinates_inside : ∀ vertex : Vertex,
    (coordinate vertex).1 < 8 ∧ (coordinate vertex).2 < 10 := by decide

theorem coordinates_injective : ∀ first second : Vertex,
    coordinate first = coordinate second → first = second := by decide

theorem matching_involution : ∀ vertex : Vertex, mate (mate vertex) = vertex := by decide

theorem matching_endpoint : ∀ vertex : Vertex, Endpoint vertex →
    Endpoint (mate vertex) ∧ adjacent vertex (mate vertex) := by decide

theorem selected_feasible : ∀ chosen : Vertex, Selected chosen →
    ((List.finRange 54).filter fun other => decide (adjacent chosen other)).length ≤ 1 := by decide

theorem endpoints_terminal : ∀ vertex : Vertex, Endpoint vertex →
    3 ≤ ((List.finRange 54).filter fun other => decide (adjacent vertex other)).length := by decide

theorem frozen_00 : Frozen adjacent Selected mate (0 : Vertex) := by
  exact .two_selected 0 32 38 (by decide) (by decide) (by decide) (by decide) (by decide)

theorem frozen_01 : Frozen adjacent Selected mate (1 : Vertex) := by
  exact .two_selected 1 40 43 (by decide) (by decide) (by decide) (by decide) (by decide)

theorem frozen_02 : Frozen adjacent Selected mate (2 : Vertex) := by
  exact .two_selected 2 41 45 (by decide) (by decide) (by decide) (by decide) (by decide)

theorem frozen_03 : Frozen adjacent Selected mate (3 : Vertex) := by
  exact .selected_frozen 3 33 31 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (1 : Vertex); exact frozen_01)

theorem frozen_04 : Frozen adjacent Selected mate (4 : Vertex) := by
  exact .two_frozen 4 29 31 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (0 : Vertex); exact frozen_00)
    (by change Frozen adjacent Selected mate (1 : Vertex); exact frozen_01)

theorem frozen_05 : Frozen adjacent Selected mate (5 : Vertex) := by
  exact .selected_frozen 5 42 29 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (0 : Vertex); exact frozen_00)

theorem frozen_06 : Frozen adjacent Selected mate (6 : Vertex) := by
  exact .selected_frozen 6 51 23 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (2 : Vertex); exact frozen_02)

theorem frozen_07 : Frozen adjacent Selected mate (7 : Vertex) := by
  exact .two_frozen 7 28 27 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (4 : Vertex); exact frozen_04)
    (by change Frozen adjacent Selected mate (5 : Vertex); exact frozen_05)

theorem frozen_08 : Frozen adjacent Selected mate (8 : Vertex) := by
  exact .selected_frozen 8 48 27 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (5 : Vertex); exact frozen_05)

theorem frozen_09 : Frozen adjacent Selected mate (9 : Vertex) := by
  exact .selected_frozen 9 53 22 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (6 : Vertex); exact frozen_06)

theorem frozen_10 : Frozen adjacent Selected mate (10 : Vertex) := by
  exact .two_frozen 10 26 25 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (7 : Vertex); exact frozen_07)
    (by change Frozen adjacent Selected mate (8 : Vertex); exact frozen_08)

theorem frozen_11 : Frozen adjacent Selected mate (11 : Vertex) := by
  exact .two_frozen 11 22 20 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (6 : Vertex); exact frozen_06)
    (by change Frozen adjacent Selected mate (9 : Vertex); exact frozen_09)

theorem frozen_12 : Frozen adjacent Selected mate (12 : Vertex) := by
  exact .selected_frozen 12 52 25 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (8 : Vertex); exact frozen_08)

theorem frozen_13 : Frozen adjacent Selected mate (13 : Vertex) := by
  exact .selected_frozen 13 49 21 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (10 : Vertex); exact frozen_10)

theorem frozen_14 : Frozen adjacent Selected mate (14 : Vertex) := by
  exact .two_frozen 14 21 24 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (10 : Vertex); exact frozen_10)
    (by change Frozen adjacent Selected mate (12 : Vertex); exact frozen_12)

theorem frozen_15 : Frozen adjacent Selected mate (15 : Vertex) := by
  exact .two_frozen 15 17 20 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (11 : Vertex); exact frozen_11)
    (by change Frozen adjacent Selected mate (9 : Vertex); exact frozen_09)

theorem frozen_16 : Frozen adjacent Selected mate (16 : Vertex) := by
  exact .two_frozen 16 17 18 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (11 : Vertex); exact frozen_11)
    (by change Frozen adjacent Selected mate (15 : Vertex); exact frozen_15)

theorem frozen_17 : Frozen adjacent Selected mate (17 : Vertex) := by
  exact .selected_frozen 17 50 16 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (13 : Vertex); exact frozen_13)

theorem frozen_18 : Frozen adjacent Selected mate (18 : Vertex) := by
  exact .two_frozen 18 16 19 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (13 : Vertex); exact frozen_13)
    (by change Frozen adjacent Selected mate (14 : Vertex); exact frozen_14)

theorem frozen_19 : Frozen adjacent Selected mate (19 : Vertex) := by
  exact .two_frozen 19 13 18 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (16 : Vertex); exact frozen_16)
    (by change Frozen adjacent Selected mate (15 : Vertex); exact frozen_15)

theorem frozen_20 : Frozen adjacent Selected mate (20 : Vertex) := by
  exact .two_frozen 20 11 15 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (17 : Vertex); exact frozen_17)
    (by change Frozen adjacent Selected mate (18 : Vertex); exact frozen_18)

theorem frozen_21 : Frozen adjacent Selected mate (21 : Vertex) := by
  exact .two_frozen 21 13 14 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (16 : Vertex); exact frozen_16)
    (by change Frozen adjacent Selected mate (19 : Vertex); exact frozen_19)

theorem frozen_22 : Frozen adjacent Selected mate (22 : Vertex) := by
  exact .two_frozen 22 11 9 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (17 : Vertex); exact frozen_17)
    (by change Frozen adjacent Selected mate (20 : Vertex); exact frozen_20)

theorem frozen_23 : Frozen adjacent Selected mate (23 : Vertex) := by
  exact .selected_frozen 23 47 6 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (22 : Vertex); exact frozen_22)

theorem frozen_24 : Frozen adjacent Selected mate (24 : Vertex) := by
  exact .two_frozen 24 10 14 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (21 : Vertex); exact frozen_21)
    (by change Frozen adjacent Selected mate (19 : Vertex); exact frozen_19)

theorem frozen_25 : Frozen adjacent Selected mate (25 : Vertex) := by
  exact .two_frozen 25 10 12 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (21 : Vertex); exact frozen_21)
    (by change Frozen adjacent Selected mate (24 : Vertex); exact frozen_24)

theorem frozen_26 : Frozen adjacent Selected mate (26 : Vertex) := by
  exact .two_frozen 26 8 10 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (25 : Vertex); exact frozen_25)
    (by change Frozen adjacent Selected mate (21 : Vertex); exact frozen_21)

theorem frozen_27 : Frozen adjacent Selected mate (27 : Vertex) := by
  exact .two_frozen 27 7 8 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (26 : Vertex); exact frozen_26)
    (by change Frozen adjacent Selected mate (25 : Vertex); exact frozen_25)

theorem frozen_28 : Frozen adjacent Selected mate (28 : Vertex) := by
  exact .two_frozen 28 5 7 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (27 : Vertex); exact frozen_27)
    (by change Frozen adjacent Selected mate (26 : Vertex); exact frozen_26)

theorem frozen_29 : Frozen adjacent Selected mate (29 : Vertex) := by
  exact .two_frozen 29 4 5 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (28 : Vertex); exact frozen_28)
    (by change Frozen adjacent Selected mate (27 : Vertex); exact frozen_27)

theorem frozen_30 : Frozen adjacent Selected mate (30 : Vertex) := by
  exact .two_frozen 30 0 4 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (29 : Vertex); exact frozen_29)
    (by change Frozen adjacent Selected mate (28 : Vertex); exact frozen_28)

theorem frozen_31 : Frozen adjacent Selected mate (31 : Vertex) := by
  exact .two_frozen 31 3 4 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (30 : Vertex); exact frozen_30)
    (by change Frozen adjacent Selected mate (28 : Vertex); exact frozen_28)

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
  | 26 => exact frozen_26
  | 27 => exact frozen_27
  | 28 => exact frozen_28
  | 29 => exact frozen_29
  | 30 => exact frozen_30
  | 31 => exact frozen_31
  | value+32 =>
      change value+32 < 32 at hendpoint
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
  ((List.finRange 54).filter fun vertex => decide (Endpoint vertex ∧
    (coordinate vertex).1/2 = row ∧ (coordinate vertex).2/2 = column)).length

def selectedCount (row column : Nat) : Nat :=
  ((List.finRange 54).filter fun vertex => decide (Selected vertex ∧
    (coordinate vertex).1/2 = row ∧ (coordinate vertex).2/2 = column)).length

def tiles : List Tile := (List.finRange 4).flatMap fun row =>
  (List.finRange 5).map fun column => (row, column)

def receiverTiles : List Tile := tiles.filter fun tile => 0 < endpointCount tile.1.val tile.2.val

def rawChargeTwice (tile : Tile) : Int :=
  2*(selectedCount tile.1.val tile.2.val : Int)+(endpointCount tile.1.val tile.2.val : Int)-4

def transferCount (tile : Tile) : Nat :=
  ((List.finRange 54).filter fun vertex => decide (Endpoint vertex ∧
    selectedCount (tileOf vertex).1.val (tileOf vertex).2.val = 2 ∧ tileOf (mate vertex) = tile)).length

def correctedChargeTwice (tile : Tile) : Int :=
  if selectedCount tile.1.val tile.2.val < 2 then rawChargeTwice tile+(transferCount tile : Int) else 0

def deficit (row column : Nat) : Nat := 2-selectedCount row column

def maximalHorizontal (row start stop : Nat) : Bool :=
  start < stop && stop ≤ 5 &&
    ((List.range (stop-start)).all fun offset => endpointCount row (start+offset) == 0) &&
    (start == 0 || 0 < endpointCount row (start-1)) &&
    (stop == 5 || 0 < endpointCount row stop)

def maximalVertical (column start stop : Nat) : Bool :=
  start < stop && stop ≤ 4 &&
    ((List.range (stop-start)).all fun offset => endpointCount (start+offset) column == 0) &&
    (start == 0 || 0 < endpointCount (start-1) column) &&
    (stop == 4 || 0 < endpointCount stop column)

def horizontalCapacity (row start stop : Nat) : Nat :=
  ((List.range (stop-start)).map fun offset => deficit row (start+offset)).sum

def verticalCapacity (column start stop : Nat) : Nat :=
  ((List.range (stop-start)).map fun offset => deficit (start+offset) column).sum

theorem original_corrected_receiver_charge :
    (receiverTiles.map correctedChargeTwice).sum = 2 := by decide

theorem receiver_inventory : receiverTiles.length = 14 ∧
    (receiverTiles.map fun tile => selectedCount tile.1.val tile.2.val).sum = 13 := by decide

theorem all_horizontal_capacities_small : ∀ row : Fin 4, ∀ start : Fin 5, ∀ stop : Fin 6,
    maximalHorizontal row.val start.val stop.val = true →
      horizontalCapacity row.val start.val stop.val ≤ 1 := by decide

theorem all_vertical_capacities_small : ∀ column : Fin 5, ∀ start : Fin 4, ∀ stop : Fin 5,
    maximalVertical column.val start.val stop.val = true →
      verticalCapacity column.val start.val stop.val ≤ 1 := by decide

theorem outside_capacity :
    ((tiles.filter fun tile => endpointCount tile.1.val tile.2.val == 0).map
      fun tile => deficit tile.1.val tile.2.val).sum = 3 := by decide

theorem original_objective : 22+16 < 8*10/2 := by decide

end SubQuorum.CapacityOneStripObstruction
