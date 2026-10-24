import SubQuorum.FrozenPromotion

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

namespace SubQuorum.CornerFreeFrozenReceiver

open FrozenPromotion

abbrev Vertex := Fin 32
abbrev Tile := Fin 4 × Fin 4

def coordinates : Array (Nat × Nat) :=
  #[(1, 6), (6, 4), (1, 4), (6, 2), (1, 2), (6, 0), (2, 3), (5, 1), (3, 2), (4, 0), (3, 0), (3, 1), (3, 3), (4, 1), (2, 2), (5, 0), (1, 3), (6, 1), (1, 5), (6, 3), (0, 2), (0, 4), (0, 6), (1, 7), (2, 0), (2, 5), (3, 4), (5, 3), (6, 5), (7, 0), (7, 2), (7, 4)]

def coordinate (vertex : Vertex) : Nat × Nat :=
  coordinates[vertex.val]!

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

def Selected (vertex : Vertex) : Prop := 20 ≤ vertex.val
def Endpoint (vertex : Vertex) : Prop := vertex.val < 20

instance (vertex : Vertex) : Decidable (Selected vertex) := by
  unfold Selected
  infer_instance

instance (vertex : Vertex) : Decidable (Endpoint vertex) := by
  unfold Endpoint
  infer_instance

def mateIndices : Array Nat := #[18, 19, 16, 17, 14, 15, 12, 13, 11, 10, 9, 8, 6, 7, 4, 5, 2, 3, 0, 1, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

def mate (vertex : Vertex) : Vertex :=
  Fin.ofNat 32 mateIndices[vertex.val]!

def neighborIndices : Array Nat := #[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2, 0, 0, 10, 18, 12, 19, 1, 5, 3, 1]

def selectedNeighbor (vertex : Vertex) : Vertex :=
  Fin.ofNat 32 neighborIndices[vertex.val]!

theorem coordinates_inside : ∀ vertex : Vertex,
    (coordinate vertex).1 < 8 ∧ (coordinate vertex).2 < 8 := by decide

theorem coordinates_injective : ∀ first second : Vertex,
    coordinate first = coordinate second → first = second := by decide

theorem matching_involution : ∀ vertex : Vertex, mate (mate vertex) = vertex := by decide

theorem matching_endpoint : ∀ vertex : Vertex, Endpoint vertex →
    Endpoint (mate vertex) ∧ adjacent vertex (mate vertex) := by decide

theorem selected_has_neighbor : ∀ chosen : Vertex, Selected chosen →
    adjacent chosen (selectedNeighbor chosen) := by decide

theorem selected_neighbor_unique : ∀ chosen other : Vertex, Selected chosen →
    adjacent chosen other → other = selectedNeighbor chosen := by decide

theorem occupied_degree_three : ∀ vertex : Vertex, Endpoint vertex →
    ((List.finRange 32).filter fun other => decide (adjacent vertex other)).length = 3 := by decide

theorem frozen_00 : Frozen adjacent Selected mate (0 : Vertex) := by
  exact .two_selected 0 22 23 (by decide) (by decide) (by decide)
    (by decide)
    (by decide)

theorem frozen_01 : Frozen adjacent Selected mate (1 : Vertex) := by
  exact .two_selected 1 28 31 (by decide) (by decide) (by decide)
    (by decide)
    (by decide)

theorem frozen_02 : Frozen adjacent Selected mate (2 : Vertex) := by
  exact .selected_frozen 2 21 18 (by decide) (by decide) (by decide)
    (by decide)
    (by change Frozen adjacent Selected mate (0 : Vertex); exact frozen_00)

theorem frozen_03 : Frozen adjacent Selected mate (3 : Vertex) := by
  exact .selected_frozen 3 30 19 (by decide) (by decide) (by decide)
    (by decide)
    (by change Frozen adjacent Selected mate (1 : Vertex); exact frozen_01)

theorem frozen_04 : Frozen adjacent Selected mate (4 : Vertex) := by
  exact .selected_frozen 4 20 16 (by decide) (by decide) (by decide)
    (by decide)
    (by change Frozen adjacent Selected mate (2 : Vertex); exact frozen_02)

theorem frozen_05 : Frozen adjacent Selected mate (5 : Vertex) := by
  exact .selected_frozen 5 29 17 (by decide) (by decide) (by decide)
    (by decide)
    (by change Frozen adjacent Selected mate (3 : Vertex); exact frozen_03)

theorem frozen_06 : Frozen adjacent Selected mate (6 : Vertex) := by
  exact .two_frozen 6 16 14 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (2 : Vertex); exact frozen_02)
    (by change Frozen adjacent Selected mate (4 : Vertex); exact frozen_04)

theorem frozen_07 : Frozen adjacent Selected mate (7 : Vertex) := by
  exact .two_frozen 7 15 17 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (5 : Vertex); exact frozen_05)
    (by change Frozen adjacent Selected mate (3 : Vertex); exact frozen_03)

theorem frozen_08 : Frozen adjacent Selected mate (8 : Vertex) := by
  exact .two_frozen 8 14 12 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (4 : Vertex); exact frozen_04)
    (by change Frozen adjacent Selected mate (6 : Vertex); exact frozen_06)

theorem frozen_09 : Frozen adjacent Selected mate (9 : Vertex) := by
  exact .two_frozen 9 13 15 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (7 : Vertex); exact frozen_07)
    (by change Frozen adjacent Selected mate (5 : Vertex); exact frozen_05)

theorem frozen_10 : Frozen adjacent Selected mate (10 : Vertex) := by
  exact .selected_frozen 10 24 11 (by decide) (by decide) (by decide)
    (by decide)
    (by change Frozen adjacent Selected mate (8 : Vertex); exact frozen_08)

theorem frozen_11 : Frozen adjacent Selected mate (11 : Vertex) := by
  exact .two_frozen 11 10 13 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (9 : Vertex); exact frozen_09)
    (by change Frozen adjacent Selected mate (7 : Vertex); exact frozen_07)

theorem frozen_12 : Frozen adjacent Selected mate (12 : Vertex) := by
  exact .selected_frozen 12 26 8 (by decide) (by decide) (by decide)
    (by decide)
    (by change Frozen adjacent Selected mate (11 : Vertex); exact frozen_11)

theorem frozen_13 : Frozen adjacent Selected mate (13 : Vertex) := by
  exact .two_frozen 13 11 9 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (8 : Vertex); exact frozen_08)
    (by change Frozen adjacent Selected mate (10 : Vertex); exact frozen_10)

theorem frozen_14 : Frozen adjacent Selected mate (14 : Vertex) := by
  exact .two_frozen 14 6 8 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (12 : Vertex); exact frozen_12)
    (by change Frozen adjacent Selected mate (11 : Vertex); exact frozen_11)

theorem frozen_15 : Frozen adjacent Selected mate (15 : Vertex) := by
  exact .two_frozen 15 9 7 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (10 : Vertex); exact frozen_10)
    (by change Frozen adjacent Selected mate (13 : Vertex); exact frozen_13)

theorem frozen_16 : Frozen adjacent Selected mate (16 : Vertex) := by
  exact .two_frozen 16 4 6 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (14 : Vertex); exact frozen_14)
    (by change Frozen adjacent Selected mate (12 : Vertex); exact frozen_12)

theorem frozen_17 : Frozen adjacent Selected mate (17 : Vertex) := by
  exact .two_frozen 17 7 5 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (13 : Vertex); exact frozen_13)
    (by change Frozen adjacent Selected mate (15 : Vertex); exact frozen_15)

theorem frozen_18 : Frozen adjacent Selected mate (18 : Vertex) := by
  exact .selected_frozen 18 25 2 (by decide) (by decide) (by decide)
    (by decide)
    (by change Frozen adjacent Selected mate (16 : Vertex); exact frozen_16)

theorem frozen_19 : Frozen adjacent Selected mate (19 : Vertex) := by
  exact .selected_frozen 19 27 3 (by decide) (by decide) (by decide)
    (by decide)
    (by change Frozen adjacent Selected mate (17 : Vertex); exact frozen_17)

theorem all_endpoints_frozen (vertex : Vertex) (hendpoint : Endpoint vertex) :
    Frozen adjacent Selected mate vertex := by
  have hcases : ∀ candidate : Vertex, Endpoint candidate →
      candidate = 0 ∨ candidate = 1 ∨ candidate = 2 ∨ candidate = 3 ∨ candidate = 4 ∨ candidate = 5 ∨ candidate = 6 ∨ candidate = 7 ∨ candidate = 8 ∨ candidate = 9 ∨ candidate = 10 ∨ candidate = 11 ∨ candidate = 12 ∨ candidate = 13 ∨ candidate = 14 ∨ candidate = 15 ∨ candidate = 16 ∨ candidate = 17 ∨ candidate = 18 ∨ candidate = 19 := by decide
  rcases hcases vertex hendpoint with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals first
    | exact frozen_00
    | exact frozen_01
    | exact frozen_02
    | exact frozen_03
    | exact frozen_04
    | exact frozen_05
    | exact frozen_06
    | exact frozen_07
    | exact frozen_08
    | exact frozen_09
    | exact frozen_10
    | exact frozen_11
    | exact frozen_12
    | exact frozen_13
    | exact frozen_14
    | exact frozen_15
    | exact frozen_16
    | exact frozen_17
    | exact frozen_18
    | exact frozen_19

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
  (Fin.ofNat 4 ((coordinate vertex).1/2), Fin.ofNat 4 ((coordinate vertex).2/2))

def receiverTiles : List Tile := [(0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (2, 0), (3, 0), (3, 1), (3, 2)]

def endpointCount (tile : Tile) : Nat :=
  ((List.finRange 32).filter fun vertex => decide (Endpoint vertex ∧ tileOf vertex = tile)).length

def selectedCount (tile : Tile) : Nat :=
  ((List.finRange 32).filter fun vertex => decide (Selected vertex ∧ tileOf vertex = tile)).length

def transferCount (tile : Tile) : Nat :=
  ((List.finRange 32).filter fun vertex =>
    decide (Endpoint vertex ∧ selectedCount (tileOf vertex) = 2 ∧ tileOf (mate vertex) = tile)).length

def rawChargeTwice (tile : Tile) : Int :=
  2*(selectedCount tile : Int)+(endpointCount tile : Int)-4

def correctedChargeTwice (tile : Tile) : Int :=
  if selectedCount tile < 2 then rawChargeTwice tile+(transferCount tile : Int) else 0

theorem receiver_complete : ∀ tile : Tile,
    tile ∈ receiverTiles ↔ ∃ vertex : Vertex, Endpoint vertex ∧ tileOf vertex = tile := by
  have hfinite : ∀ row column : Fin 4,
      (row, column) ∈ receiverTiles ↔
        ∃ vertex : Vertex, Endpoint vertex ∧ tileOf vertex = (row, column) := by decide
  intro tile
  exact hfinite tile.1 tile.2

theorem receiver_counts :
    receiverTiles.length = 9 ∧
    (receiverTiles.map endpointCount).sum = 20 ∧
    (receiverTiles.map selectedCount).sum = 9 := by decide

theorem raw_receiver_charge_twice :
    (receiverTiles.map rawChargeTwice).sum = 2 := by decide

theorem original_corrected_receiver_charge_twice :
    (receiverTiles.map correctedChargeTwice).sum = 2 := by decide

theorem positive_receiver_charge :
    0 < (receiverTiles.map correctedChargeTwice).sum := by
  rw [original_corrected_receiver_charge_twice]
  decide

end SubQuorum.CornerFreeFrozenReceiver
