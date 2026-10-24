import SubQuorum.FrozenPromotion

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 16000000

namespace SubQuorum.DegreeFourOvercount

open FrozenPromotion

abbrev Vertex := Fin 56

def coordinates : Array (Nat × Nat) :=
  #[(1, 1), (3, 1), (5, 1), (4, 2), (7, 1), (6, 2), (1, 8), (3, 8), (5, 8), (4, 7), (7, 8), (6, 7), (7, 3), (6, 4), (7, 5), (6, 6), (7, 7), (7, 6), (6, 5), (7, 4), (6, 3), (7, 2), (6, 1), (5, 2), (4, 1), (3, 2), (2, 1), (1, 2), (6, 8), (5, 7), (4, 8), (3, 7), (2, 8), (1, 7), (2, 3), (1, 4), (2, 5), (1, 6), (2, 6), (1, 5), (2, 4), (1, 3), (2, 2), (2, 7), (0, 1), (0, 8), (1, 0), (1, 9), (3, 0), (3, 9), (4, 3), (4, 6), (5, 0), (5, 9), (7, 0), (7, 9)]

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

def Selected (vertex : Vertex) : Prop := 44 ≤ vertex.val
def Endpoint (vertex : Vertex) : Prop := vertex.val < 44

instance (vertex : Vertex) : Decidable (Selected vertex) := by
  unfold Selected
  infer_instance

instance (vertex : Vertex) : Decidable (Endpoint vertex) := by
  unfold Endpoint
  infer_instance

def mateIndices : Array Nat :=
  #[26, 24, 22, 23, 21, 20, 32, 30, 28, 29, 16, 15, 19, 18, 17, 11, 10, 14, 13, 12, 5, 4, 2, 3, 1, 42, 0, 41, 8, 9, 7, 43, 6, 37, 40, 39, 38, 33, 36, 35, 34, 27, 25, 31, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55]

def mate (vertex : Vertex) : Vertex := Fin.ofNat 56 mateIndices[vertex.val]!

def ownerIndices : Array Nat := #[2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def owner (vertex : Vertex) : Nat := ownerIndices[vertex.val]!

def originalSelectedIndices : Array (Array Nat) := #[#[0, 1, 2, 5, 6, 7, 8, 11, 50, 51], #[3, 9, 42, 43, 44, 45, 46, 47, 48, 49, 52, 53, 54, 55]]

def OldEndpoint (module : Fin 2) (vertex : Vertex) : Prop := owner vertex = module.val+1
def OldSelected (module : Fin 2) (vertex : Vertex) : Prop :=
  vertex.val ∈ (originalSelectedIndices[module.val]!).toList
def OldOccupied (module : Fin 2) (vertex : Vertex) : Prop :=
  OldEndpoint module vertex ∨ OldSelected module vertex

instance (module : Fin 2) (vertex : Vertex) : Decidable (OldEndpoint module vertex) := by
  unfold OldEndpoint
  infer_instance

instance (module : Fin 2) (vertex : Vertex) : Decidable (OldSelected module vertex) := by
  unfold OldSelected
  infer_instance

instance (module : Fin 2) (vertex : Vertex) : Decidable (OldOccupied module vertex) := by
  unfold OldOccupied
  infer_instance

def sameTile (first second : Vertex) : Prop :=
  (coordinate first).1/2 = (coordinate second).1/2 ∧
    (coordinate first).2/2 = (coordinate second).2/2

instance (first second : Vertex) : Decidable (sameTile first second) := by
  unfold sameTile
  infer_instance

def occupiedDegree (vertex : Vertex) : Nat :=
  ((List.finRange 56).filter fun other => decide (adjacent vertex other)).length

theorem coordinates_inside : ∀ vertex : Vertex,
    (coordinate vertex).1 < 8 ∧ (coordinate vertex).2 < 10 := by decide

theorem coordinates_injective : ∀ first second : Vertex,
    coordinate first = coordinate second → first = second := by decide

theorem matching_involution : ∀ vertex : Vertex, mate (mate vertex) = vertex := by decide

theorem matching_endpoint : ∀ vertex : Vertex, Endpoint vertex →
    Endpoint (mate vertex) ∧ adjacent vertex (mate vertex) := by decide

theorem selected_feasible : ∀ vertex : Vertex, Selected vertex → occupiedDegree vertex ≤ 1 := by
  decide

theorem original_degrees_three : ∀ module : Fin 2, ∀ vertex : Vertex,
    OldEndpoint module vertex →
      ((List.finRange 56).filter fun other =>
        decide (adjacent vertex other ∧ OldOccupied module other)).length = 3 := by decide

theorem original_support_feasible : ∀ module : Fin 2, ∀ vertex : Vertex,
    OldSelected module vertex →
      ((List.finRange 56).filter fun other =>
        decide (adjacent vertex other ∧ OldOccupied module other)).length = 1 := by decide

theorem final_degrees_three_or_four : ∀ vertex : Vertex, Endpoint vertex →
    occupiedDegree vertex = 3 ∨ occupiedDegree vertex = 4 := by decide

theorem frozen_00 : Frozen adjacent Selected mate (0 : Vertex) := by
  exact .two_selected 0 44 46 (by decide) (by decide) (by decide) (by decide) (by decide)

theorem frozen_01 : Frozen adjacent Selected mate (1 : Vertex) := by
  exact .selected_frozen 1 48 26 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (0 : Vertex); exact frozen_00)

theorem frozen_02 : Frozen adjacent Selected mate (2 : Vertex) := by
  exact .selected_frozen 2 52 24 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (1 : Vertex); exact frozen_01)

theorem frozen_03 : Frozen adjacent Selected mate (3 : Vertex) := by
  exact .selected_frozen 3 50 24 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (1 : Vertex); exact frozen_01)

theorem frozen_04 : Frozen adjacent Selected mate (4 : Vertex) := by
  exact .selected_frozen 4 54 22 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (2 : Vertex); exact frozen_02)

theorem frozen_05 : Frozen adjacent Selected mate (5 : Vertex) := by
  exact .two_frozen 5 23 22 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (3 : Vertex); exact frozen_03)
    (by change Frozen adjacent Selected mate (2 : Vertex); exact frozen_02)

theorem frozen_06 : Frozen adjacent Selected mate (6 : Vertex) := by
  exact .two_selected 6 45 47 (by decide) (by decide) (by decide) (by decide) (by decide)

theorem frozen_07 : Frozen adjacent Selected mate (7 : Vertex) := by
  exact .selected_frozen 7 49 32 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (6 : Vertex); exact frozen_06)

theorem frozen_08 : Frozen adjacent Selected mate (8 : Vertex) := by
  exact .selected_frozen 8 53 30 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (7 : Vertex); exact frozen_07)

theorem frozen_09 : Frozen adjacent Selected mate (9 : Vertex) := by
  exact .selected_frozen 9 51 30 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (7 : Vertex); exact frozen_07)

theorem frozen_10 : Frozen adjacent Selected mate (10 : Vertex) := by
  exact .selected_frozen 10 55 28 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (8 : Vertex); exact frozen_08)

theorem frozen_11 : Frozen adjacent Selected mate (11 : Vertex) := by
  exact .two_frozen 11 29 28 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (9 : Vertex); exact frozen_09)
    (by change Frozen adjacent Selected mate (8 : Vertex); exact frozen_08)

theorem frozen_12 : Frozen adjacent Selected mate (12 : Vertex) := by
  exact .two_frozen 12 20 21 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (5 : Vertex); exact frozen_05)
    (by change Frozen adjacent Selected mate (4 : Vertex); exact frozen_04)

theorem frozen_13 : Frozen adjacent Selected mate (13 : Vertex) := by
  exact .two_frozen 13 19 20 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (12 : Vertex); exact frozen_12)
    (by change Frozen adjacent Selected mate (5 : Vertex); exact frozen_05)

theorem frozen_14 : Frozen adjacent Selected mate (14 : Vertex) := by
  exact .two_frozen 14 18 19 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (13 : Vertex); exact frozen_13)
    (by change Frozen adjacent Selected mate (12 : Vertex); exact frozen_12)

theorem frozen_15 : Frozen adjacent Selected mate (15 : Vertex) := by
  exact .two_frozen 15 17 18 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (14 : Vertex); exact frozen_14)
    (by change Frozen adjacent Selected mate (13 : Vertex); exact frozen_13)

theorem frozen_16 : Frozen adjacent Selected mate (16 : Vertex) := by
  exact .two_frozen 16 11 17 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (15 : Vertex); exact frozen_15)
    (by change Frozen adjacent Selected mate (14 : Vertex); exact frozen_14)

theorem frozen_17 : Frozen adjacent Selected mate (17 : Vertex) := by
  exact .two_frozen 17 15 16 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (11 : Vertex); exact frozen_11)
    (by change Frozen adjacent Selected mate (10 : Vertex); exact frozen_10)

theorem frozen_18 : Frozen adjacent Selected mate (18 : Vertex) := by
  exact .two_frozen 18 14 15 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (17 : Vertex); exact frozen_17)
    (by change Frozen adjacent Selected mate (11 : Vertex); exact frozen_11)

theorem frozen_19 : Frozen adjacent Selected mate (19 : Vertex) := by
  exact .two_frozen 19 13 14 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (18 : Vertex); exact frozen_18)
    (by change Frozen adjacent Selected mate (17 : Vertex); exact frozen_17)

theorem frozen_20 : Frozen adjacent Selected mate (20 : Vertex) := by
  exact .two_frozen 20 12 13 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (19 : Vertex); exact frozen_19)
    (by change Frozen adjacent Selected mate (18 : Vertex); exact frozen_18)

theorem frozen_21 : Frozen adjacent Selected mate (21 : Vertex) := by
  exact .two_frozen 21 5 12 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (20 : Vertex); exact frozen_20)
    (by change Frozen adjacent Selected mate (19 : Vertex); exact frozen_19)

theorem frozen_22 : Frozen adjacent Selected mate (22 : Vertex) := by
  exact .two_frozen 22 4 5 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (21 : Vertex); exact frozen_21)
    (by change Frozen adjacent Selected mate (20 : Vertex); exact frozen_20)

theorem frozen_23 : Frozen adjacent Selected mate (23 : Vertex) := by
  exact .two_frozen 23 2 5 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (22 : Vertex); exact frozen_22)
    (by change Frozen adjacent Selected mate (20 : Vertex); exact frozen_20)

theorem frozen_24 : Frozen adjacent Selected mate (24 : Vertex) := by
  exact .two_frozen 24 3 2 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (23 : Vertex); exact frozen_23)
    (by change Frozen adjacent Selected mate (22 : Vertex); exact frozen_22)

theorem frozen_25 : Frozen adjacent Selected mate (25 : Vertex) := by
  exact .two_frozen 25 1 3 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (24 : Vertex); exact frozen_24)
    (by change Frozen adjacent Selected mate (23 : Vertex); exact frozen_23)

theorem frozen_26 : Frozen adjacent Selected mate (26 : Vertex) := by
  exact .two_frozen 26 42 1 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (25 : Vertex); exact frozen_25)
    (by change Frozen adjacent Selected mate (24 : Vertex); exact frozen_24)

theorem frozen_27 : Frozen adjacent Selected mate (27 : Vertex) := by
  exact .two_frozen 27 0 42 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (26 : Vertex); exact frozen_26)
    (by change Frozen adjacent Selected mate (25 : Vertex); exact frozen_25)

theorem frozen_28 : Frozen adjacent Selected mate (28 : Vertex) := by
  exact .two_frozen 28 10 11 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (16 : Vertex); exact frozen_16)
    (by change Frozen adjacent Selected mate (15 : Vertex); exact frozen_15)

theorem frozen_29 : Frozen adjacent Selected mate (29 : Vertex) := by
  exact .two_frozen 29 8 11 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (28 : Vertex); exact frozen_28)
    (by change Frozen adjacent Selected mate (15 : Vertex); exact frozen_15)

theorem frozen_30 : Frozen adjacent Selected mate (30 : Vertex) := by
  exact .two_frozen 30 9 8 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (29 : Vertex); exact frozen_29)
    (by change Frozen adjacent Selected mate (28 : Vertex); exact frozen_28)

theorem frozen_31 : Frozen adjacent Selected mate (31 : Vertex) := by
  exact .two_frozen 31 7 9 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (30 : Vertex); exact frozen_30)
    (by change Frozen adjacent Selected mate (29 : Vertex); exact frozen_29)

theorem frozen_32 : Frozen adjacent Selected mate (32 : Vertex) := by
  exact .two_frozen 32 43 7 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (31 : Vertex); exact frozen_31)
    (by change Frozen adjacent Selected mate (30 : Vertex); exact frozen_30)

theorem frozen_33 : Frozen adjacent Selected mate (33 : Vertex) := by
  exact .two_frozen 33 6 43 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (32 : Vertex); exact frozen_32)
    (by change Frozen adjacent Selected mate (31 : Vertex); exact frozen_31)

theorem frozen_34 : Frozen adjacent Selected mate (34 : Vertex) := by
  exact .two_frozen 34 41 42 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (27 : Vertex); exact frozen_27)
    (by change Frozen adjacent Selected mate (25 : Vertex); exact frozen_25)

theorem frozen_35 : Frozen adjacent Selected mate (35 : Vertex) := by
  exact .two_frozen 35 40 41 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (34 : Vertex); exact frozen_34)
    (by change Frozen adjacent Selected mate (27 : Vertex); exact frozen_27)

theorem frozen_36 : Frozen adjacent Selected mate (36 : Vertex) := by
  exact .two_frozen 36 39 40 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (35 : Vertex); exact frozen_35)
    (by change Frozen adjacent Selected mate (34 : Vertex); exact frozen_34)

theorem frozen_37 : Frozen adjacent Selected mate (37 : Vertex) := by
  exact .two_frozen 37 38 39 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (36 : Vertex); exact frozen_36)
    (by change Frozen adjacent Selected mate (35 : Vertex); exact frozen_35)

theorem frozen_38 : Frozen adjacent Selected mate (38 : Vertex) := by
  exact .two_frozen 38 37 43 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (33 : Vertex); exact frozen_33)
    (by change Frozen adjacent Selected mate (31 : Vertex); exact frozen_31)

theorem frozen_39 : Frozen adjacent Selected mate (39 : Vertex) := by
  exact .two_frozen 39 36 37 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (38 : Vertex); exact frozen_38)
    (by change Frozen adjacent Selected mate (33 : Vertex); exact frozen_33)

theorem frozen_40 : Frozen adjacent Selected mate (40 : Vertex) := by
  exact .two_frozen 40 35 36 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (39 : Vertex); exact frozen_39)
    (by change Frozen adjacent Selected mate (38 : Vertex); exact frozen_38)

theorem frozen_41 : Frozen adjacent Selected mate (41 : Vertex) := by
  exact .two_frozen 41 34 35 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (40 : Vertex); exact frozen_40)
    (by change Frozen adjacent Selected mate (39 : Vertex); exact frozen_39)

theorem frozen_42 : Frozen adjacent Selected mate (42 : Vertex) := by
  exact .two_frozen 42 27 34 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (41 : Vertex); exact frozen_41)
    (by change Frozen adjacent Selected mate (40 : Vertex); exact frozen_40)

theorem frozen_43 : Frozen adjacent Selected mate (43 : Vertex) := by
  exact .two_frozen 43 33 38 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (37 : Vertex); exact frozen_37)
    (by change Frozen adjacent Selected mate (36 : Vertex); exact frozen_36)

theorem all_endpoints_frozen (vertex : Vertex) (hendpoint : Endpoint vertex) :
    Frozen adjacent Selected mate vertex := by
  rcases vertex with ⟨value, hvalue⟩
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
  | 32 => exact frozen_32
  | 33 => exact frozen_33
  | 34 => exact frozen_34
  | 35 => exact frozen_35
  | 36 => exact frozen_36
  | 37 => exact frozen_37
  | 38 => exact frozen_38
  | 39 => exact frozen_39
  | 40 => exact frozen_40
  | 41 => exact frozen_41
  | 42 => exact frozen_42
  | 43 => exact frozen_43
  | value+44 =>
      change value+44 < 44 at hendpoint
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

def tiles : List (Nat × Nat) := (List.range 4).flatMap fun row =>
  (List.range 5).map fun column => (row, column)

def inTile (vertex : Vertex) (tile : Nat × Nat) : Bool :=
  decide ((coordinate vertex).1/2 = tile.1 ∧ (coordinate vertex).2/2 = tile.2)

def oldReceivers (module : Fin 2) : List (Nat × Nat) :=
  tiles.filter fun tile => (List.finRange 56).any fun vertex =>
    decide (OldEndpoint module vertex) && inTile vertex tile

def oldReceiverSelections (module : Fin 2) : Nat :=
  ((List.finRange 56).filter fun vertex => decide (OldSelected module vertex) &&
    (oldReceivers module).any (inTile vertex)).length

def oldMatchingCount (module : Fin 2) : Nat :=
  ((List.finRange 56).filter fun vertex => decide (OldEndpoint module vertex)).length/2

def oldCharge (module : Fin 2) : Int :=
  (oldReceiverSelections module : Int)+(oldMatchingCount module : Int)-
    2*((oldReceivers module).length : Int)

def newMixedSquares : Nat :=
  (tiles.filter fun tile =>
    ((List.finRange 56).filter fun vertex => decide (Endpoint vertex) && inTile vertex tile).length = 4 &&
    (List.finRange 56).any (fun vertex => decide (owner vertex = 1) && inTile vertex tile) &&
    (List.finRange 56).any (fun vertex => decide (owner vertex = 2) && inTile vertex tile)).length

def originallyOccupied (vertex other : Vertex) : Prop :=
  (owner vertex = 1 ∧ OldOccupied 0 other) ∨ (owner vertex = 2 ∧ OldOccupied 1 other)

instance (vertex other : Vertex) : Decidable (originallyOccupied vertex other) := by
  unfold originallyOccupied
  infer_instance

def insideLoss : Nat :=
  ((List.finRange 56).filter fun vertex => decide (Endpoint vertex ∧
    ∃ other : Vertex, Endpoint other ∧ adjacent vertex other ∧ sameTile vertex other ∧
      ¬originallyOccupied vertex other)).length

def degreeFourCount : Nat :=
  ((List.finRange 56).filter fun vertex => decide (Endpoint vertex ∧ occupiedDegree vertex = 4)).length

def negativeMass : Int := 1-(oldCharge 0+oldCharge 1)

def protectors : List Vertex := [1, 2, 20]

def markedModules : Nat := if protectors.any (fun vertex => occupiedDegree vertex = 4) then 1 else 0

theorem exact_original_charges : oldCharge 0 = -5 ∧ oldCharge 1 = 1 := by decide

theorem exact_degree_four_count : degreeFourCount = 12 := by decide

theorem exact_mixed_square_count : newMixedSquares = 0 := by decide

theorem exact_internal_loss : insideLoss = 0 := by decide

theorem exact_marked_module_count : markedModules = 1 := by decide

theorem coarse_criterion_fails : ¬ (degreeFourCount : Int) ≤ negativeMass+2*newMixedSquares := by
  decide

theorem finer_criterion_holds : (insideLoss : Int)+markedModules ≤ negativeMass+2*newMixedSquares := by
  decide

theorem positive_canonical_donor_consumed : OldSelected 1 (3 : Vertex) ∧
    OldEndpoint 0 (3 : Vertex) := by decide

def objective : Nat :=
  ((List.finRange 56).filter fun vertex => decide (Selected vertex)).length+
    ((List.finRange 56).filter fun vertex => decide (Endpoint vertex)).length/2

theorem exact_objective : objective = 34 := by decide

theorem actual_target_holds : (objective : Int) < 8*10/2 := by decide

theorem coarse_gap_unbounded (bound : Nat) : ∃ height : Nat,
    4 ≤ height ∧ height % 2 = 0 ∧ (bound : Int) < 2*(height : Int)+4-5 := by
  refine ⟨2*(bound+2), ?_, ?_, ?_⟩ <;> omega

theorem fine_credit_constant (width : Int) : (width-1)-0-1 = width-2 := by omega

theorem doubled_slack_identity (width height : Int) :
    (height+4)*(width+4)-2*(2*width+4*height+6) = height*(width-4)+4 := by
  simp only [Int.mul_add, Int.add_mul, Int.mul_sub]
  omega

end SubQuorum.DegreeFourOvercount
