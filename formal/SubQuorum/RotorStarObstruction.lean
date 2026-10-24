import SubQuorum.FrozenPromotion

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 16000000

namespace SubQuorum.RotorStarObstruction

open FrozenPromotion

abbrev Vertex := Fin 120

def coordinates : Array (Nat × Nat) :=
  #[(1, 9), (4, 1), (9, 12), (12, 4), (1, 11), (2, 1), (11, 12), (12, 2), (0, 1), (1, 13), (12, 0), (13, 12), (1, 2), (2, 12), (11, 1), (12, 11), (0, 3), (3, 13), (10, 0), (13, 10), (1, 4), (4, 12), (9, 1), (12, 9), (0, 5), (5, 13), (8, 0), (13, 8), (1, 6), (6, 12), (7, 1), (12, 7), (3, 6), (6, 10), (7, 3), (10, 7), (5, 6), (6, 8), (7, 5), (8, 7), (6, 6), (6, 7), (7, 6), (7, 7), (4, 6), (6, 9), (7, 4), (9, 7), (2, 6), (6, 11), (7, 2), (11, 7), (0, 6), (6, 13), (7, 0), (13, 7), (1, 5), (5, 12), (8, 1), (12, 8), (0, 4), (4, 13), (9, 0), (13, 9), (1, 3), (3, 12), (10, 1), (12, 10), (0, 2), (2, 13), (11, 0), (13, 11), (1, 1), (1, 12), (12, 1), (12, 12), (1, 10), (3, 1), (10, 12), (12, 3), (0, 0), (0, 7), (0, 9), (0, 11), (0, 13), (1, 8), (2, 0), (2, 7), (2, 10), (3, 2), (3, 5), (4, 0), (4, 7), (5, 1), (5, 5), (5, 8), (5, 10), (6, 0), (6, 2), (6, 4), (7, 9), (7, 11), (7, 13), (8, 3), (8, 5), (8, 8), (8, 12), (9, 6), (9, 13), (10, 8), (10, 11), (11, 3), (11, 6), (11, 13), (12, 5), (13, 0), (13, 2), (13, 4), (13, 6), (13, 13)]

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

def Selected (vertex : Vertex) : Prop := 80 ≤ vertex.val
def Endpoint (vertex : Vertex) : Prop := vertex.val < 80

instance (vertex : Vertex) : Decidable (Selected vertex) := by
  unfold Selected
  infer_instance

instance (vertex : Vertex) : Decidable (Endpoint vertex) := by
  unfold Endpoint
  infer_instance

def mateIndices : Array Nat :=
  #[76, 77, 78, 79, 73, 72, 75, 74, 68, 69, 70, 71, 64, 65, 66, 67, 60, 61, 62, 63, 56, 57, 58, 59, 52, 53, 54, 55, 48, 49, 50, 51, 44, 45, 46, 47, 40, 41, 42, 43, 36, 37, 38, 39, 32, 33, 34, 35, 28, 29, 30, 31, 24, 25, 26, 27, 20, 21, 22, 23, 16, 17, 18, 19, 12, 13, 14, 15, 8, 9, 10, 11, 5, 4, 7, 6, 0, 1, 2, 3, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119]

def mate (vertex : Vertex) : Vertex := Fin.ofNat 120 mateIndices[vertex.val]!

theorem coordinates_inside : ∀ vertex : Vertex,
    (coordinate vertex).1 < 14 ∧ (coordinate vertex).2 < 14 := by decide

theorem coordinates_injective : ∀ first second : Vertex,
    coordinate first = coordinate second → first = second := by decide

theorem matching_involution : ∀ vertex : Vertex, mate (mate vertex) = vertex := by decide

theorem matching_endpoint : ∀ vertex : Vertex, Endpoint vertex →
    Endpoint (mate vertex) ∧ adjacent vertex (mate vertex) := by decide

theorem selected_feasible : ∀ chosen : Vertex, Selected chosen →
    ((List.finRange 120).filter fun other => decide (adjacent chosen other)).length ≤ 1 := by decide

theorem endpoints_degree_three : ∀ vertex : Vertex, Endpoint vertex →
    ((List.finRange 120).filter fun other => decide (adjacent vertex other)).length = 3 := by decide

theorem frozen_00 : Frozen adjacent Selected mate (0 : Vertex) := by
  exact .two_selected 0 82 85 (by decide) (by decide) (by decide) (by decide) (by decide)

theorem frozen_01 : Frozen adjacent Selected mate (1 : Vertex) := by
  exact .two_selected 1 91 93 (by decide) (by decide) (by decide) (by decide) (by decide)

theorem frozen_02 : Frozen adjacent Selected mate (2 : Vertex) := by
  exact .two_selected 2 106 108 (by decide) (by decide) (by decide) (by decide) (by decide)

theorem frozen_03 : Frozen adjacent Selected mate (3 : Vertex) := by
  exact .two_selected 3 114 117 (by decide) (by decide) (by decide) (by decide) (by decide)

theorem frozen_04 : Frozen adjacent Selected mate (4 : Vertex) := by
  exact .selected_frozen 4 83 76 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (0 : Vertex); exact frozen_00)

theorem frozen_05 : Frozen adjacent Selected mate (5 : Vertex) := by
  exact .selected_frozen 5 86 77 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (1 : Vertex); exact frozen_01)

theorem frozen_06 : Frozen adjacent Selected mate (6 : Vertex) := by
  exact .selected_frozen 6 113 78 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (2 : Vertex); exact frozen_02)

theorem frozen_07 : Frozen adjacent Selected mate (7 : Vertex) := by
  exact .selected_frozen 7 116 79 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (3 : Vertex); exact frozen_03)

theorem frozen_08 : Frozen adjacent Selected mate (8 : Vertex) := by
  exact .selected_frozen 8 80 72 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (5 : Vertex); exact frozen_05)

theorem frozen_09 : Frozen adjacent Selected mate (9 : Vertex) := by
  exact .selected_frozen 9 84 73 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (4 : Vertex); exact frozen_04)

theorem frozen_10 : Frozen adjacent Selected mate (10 : Vertex) := by
  exact .selected_frozen 10 115 74 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (7 : Vertex); exact frozen_07)

theorem frozen_11 : Frozen adjacent Selected mate (11 : Vertex) := by
  exact .selected_frozen 11 119 75 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (6 : Vertex); exact frozen_06)

theorem frozen_12 : Frozen adjacent Selected mate (12 : Vertex) := by
  exact .two_frozen 12 68 72 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (8 : Vertex); exact frozen_08)
    (by change Frozen adjacent Selected mate (5 : Vertex); exact frozen_05)

theorem frozen_13 : Frozen adjacent Selected mate (13 : Vertex) := by
  exact .two_frozen 13 73 69 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (4 : Vertex); exact frozen_04)
    (by change Frozen adjacent Selected mate (9 : Vertex); exact frozen_09)

theorem frozen_14 : Frozen adjacent Selected mate (14 : Vertex) := by
  exact .two_frozen 14 70 74 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (10 : Vertex); exact frozen_10)
    (by change Frozen adjacent Selected mate (7 : Vertex); exact frozen_07)

theorem frozen_15 : Frozen adjacent Selected mate (15 : Vertex) := by
  exact .two_frozen 15 75 71 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (6 : Vertex); exact frozen_06)
    (by change Frozen adjacent Selected mate (11 : Vertex); exact frozen_11)

theorem frozen_16 : Frozen adjacent Selected mate (16 : Vertex) := by
  exact .two_frozen 16 68 64 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (8 : Vertex); exact frozen_08)
    (by change Frozen adjacent Selected mate (12 : Vertex); exact frozen_12)

theorem frozen_17 : Frozen adjacent Selected mate (17 : Vertex) := by
  exact .two_frozen 17 69 65 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (9 : Vertex); exact frozen_09)
    (by change Frozen adjacent Selected mate (13 : Vertex); exact frozen_13)

theorem frozen_18 : Frozen adjacent Selected mate (18 : Vertex) := by
  exact .two_frozen 18 66 70 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (14 : Vertex); exact frozen_14)
    (by change Frozen adjacent Selected mate (10 : Vertex); exact frozen_10)

theorem frozen_19 : Frozen adjacent Selected mate (19 : Vertex) := by
  exact .two_frozen 19 67 71 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (15 : Vertex); exact frozen_15)
    (by change Frozen adjacent Selected mate (11 : Vertex); exact frozen_11)

theorem frozen_20 : Frozen adjacent Selected mate (20 : Vertex) := by
  exact .two_frozen 20 60 64 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (16 : Vertex); exact frozen_16)
    (by change Frozen adjacent Selected mate (12 : Vertex); exact frozen_12)

theorem frozen_21 : Frozen adjacent Selected mate (21 : Vertex) := by
  exact .two_frozen 21 65 61 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (13 : Vertex); exact frozen_13)
    (by change Frozen adjacent Selected mate (17 : Vertex); exact frozen_17)

theorem frozen_22 : Frozen adjacent Selected mate (22 : Vertex) := by
  exact .two_frozen 22 62 66 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (18 : Vertex); exact frozen_18)
    (by change Frozen adjacent Selected mate (14 : Vertex); exact frozen_14)

theorem frozen_23 : Frozen adjacent Selected mate (23 : Vertex) := by
  exact .two_frozen 23 67 63 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (15 : Vertex); exact frozen_15)
    (by change Frozen adjacent Selected mate (19 : Vertex); exact frozen_19)

theorem frozen_24 : Frozen adjacent Selected mate (24 : Vertex) := by
  exact .two_frozen 24 60 56 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (16 : Vertex); exact frozen_16)
    (by change Frozen adjacent Selected mate (20 : Vertex); exact frozen_20)

theorem frozen_25 : Frozen adjacent Selected mate (25 : Vertex) := by
  exact .two_frozen 25 61 57 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (17 : Vertex); exact frozen_17)
    (by change Frozen adjacent Selected mate (21 : Vertex); exact frozen_21)

theorem frozen_26 : Frozen adjacent Selected mate (26 : Vertex) := by
  exact .two_frozen 26 58 62 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (22 : Vertex); exact frozen_22)
    (by change Frozen adjacent Selected mate (18 : Vertex); exact frozen_18)

theorem frozen_27 : Frozen adjacent Selected mate (27 : Vertex) := by
  exact .two_frozen 27 59 63 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (23 : Vertex); exact frozen_23)
    (by change Frozen adjacent Selected mate (19 : Vertex); exact frozen_19)

theorem frozen_28 : Frozen adjacent Selected mate (28 : Vertex) := by
  exact .two_frozen 28 52 56 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (24 : Vertex); exact frozen_24)
    (by change Frozen adjacent Selected mate (20 : Vertex); exact frozen_20)

theorem frozen_29 : Frozen adjacent Selected mate (29 : Vertex) := by
  exact .two_frozen 29 57 53 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (21 : Vertex); exact frozen_21)
    (by change Frozen adjacent Selected mate (25 : Vertex); exact frozen_25)

theorem frozen_30 : Frozen adjacent Selected mate (30 : Vertex) := by
  exact .two_frozen 30 54 58 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (26 : Vertex); exact frozen_26)
    (by change Frozen adjacent Selected mate (22 : Vertex); exact frozen_22)

theorem frozen_31 : Frozen adjacent Selected mate (31 : Vertex) := by
  exact .two_frozen 31 59 55 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (23 : Vertex); exact frozen_23)
    (by change Frozen adjacent Selected mate (27 : Vertex); exact frozen_27)

theorem frozen_32 : Frozen adjacent Selected mate (32 : Vertex) := by
  exact .selected_frozen 32 90 48 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (28 : Vertex); exact frozen_28)

theorem frozen_33 : Frozen adjacent Selected mate (33 : Vertex) := by
  exact .selected_frozen 33 96 49 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (29 : Vertex); exact frozen_29)

theorem frozen_34 : Frozen adjacent Selected mate (34 : Vertex) := by
  exact .selected_frozen 34 103 50 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (30 : Vertex); exact frozen_30)

theorem frozen_35 : Frozen adjacent Selected mate (35 : Vertex) := by
  exact .selected_frozen 35 109 51 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (31 : Vertex); exact frozen_31)

theorem frozen_36 : Frozen adjacent Selected mate (36 : Vertex) := by
  exact .selected_frozen 36 94 44 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (32 : Vertex); exact frozen_32)

theorem frozen_37 : Frozen adjacent Selected mate (37 : Vertex) := by
  exact .selected_frozen 37 95 45 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (33 : Vertex); exact frozen_33)

theorem frozen_38 : Frozen adjacent Selected mate (38 : Vertex) := by
  exact .selected_frozen 38 104 46 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (34 : Vertex); exact frozen_34)

theorem frozen_39 : Frozen adjacent Selected mate (39 : Vertex) := by
  exact .selected_frozen 39 105 47 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (35 : Vertex); exact frozen_35)

theorem frozen_40 : Frozen adjacent Selected mate (40 : Vertex) := by
  exact .two_frozen 40 41 42 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (37 : Vertex); exact frozen_37)
    (by change Frozen adjacent Selected mate (38 : Vertex); exact frozen_38)

theorem frozen_41 : Frozen adjacent Selected mate (41 : Vertex) := by
  exact .two_frozen 41 40 43 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (36 : Vertex); exact frozen_36)
    (by change Frozen adjacent Selected mate (39 : Vertex); exact frozen_39)

theorem frozen_42 : Frozen adjacent Selected mate (42 : Vertex) := by
  exact .two_frozen 42 40 43 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (36 : Vertex); exact frozen_36)
    (by change Frozen adjacent Selected mate (39 : Vertex); exact frozen_39)

theorem frozen_43 : Frozen adjacent Selected mate (43 : Vertex) := by
  exact .two_frozen 43 41 42 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (37 : Vertex); exact frozen_37)
    (by change Frozen adjacent Selected mate (38 : Vertex); exact frozen_38)

theorem frozen_44 : Frozen adjacent Selected mate (44 : Vertex) := by
  exact .selected_frozen 44 92 36 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (40 : Vertex); exact frozen_40)

theorem frozen_45 : Frozen adjacent Selected mate (45 : Vertex) := by
  exact .selected_frozen 45 100 37 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (41 : Vertex); exact frozen_41)

theorem frozen_46 : Frozen adjacent Selected mate (46 : Vertex) := by
  exact .selected_frozen 46 99 38 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (42 : Vertex); exact frozen_42)

theorem frozen_47 : Frozen adjacent Selected mate (47 : Vertex) := by
  exact .selected_frozen 47 107 39 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (43 : Vertex); exact frozen_43)

theorem frozen_48 : Frozen adjacent Selected mate (48 : Vertex) := by
  exact .selected_frozen 48 87 32 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (44 : Vertex); exact frozen_44)

theorem frozen_49 : Frozen adjacent Selected mate (49 : Vertex) := by
  exact .selected_frozen 49 101 33 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (45 : Vertex); exact frozen_45)

theorem frozen_50 : Frozen adjacent Selected mate (50 : Vertex) := by
  exact .selected_frozen 50 98 34 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (46 : Vertex); exact frozen_46)

theorem frozen_51 : Frozen adjacent Selected mate (51 : Vertex) := by
  exact .selected_frozen 51 112 35 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (47 : Vertex); exact frozen_47)

theorem frozen_52 : Frozen adjacent Selected mate (52 : Vertex) := by
  exact .selected_frozen 52 81 28 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (48 : Vertex); exact frozen_48)

theorem frozen_53 : Frozen adjacent Selected mate (53 : Vertex) := by
  exact .selected_frozen 53 102 29 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (49 : Vertex); exact frozen_49)

theorem frozen_54 : Frozen adjacent Selected mate (54 : Vertex) := by
  exact .selected_frozen 54 97 30 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (50 : Vertex); exact frozen_50)

theorem frozen_55 : Frozen adjacent Selected mate (55 : Vertex) := by
  exact .selected_frozen 55 118 31 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (51 : Vertex); exact frozen_51)

theorem frozen_56 : Frozen adjacent Selected mate (56 : Vertex) := by
  exact .two_frozen 56 24 28 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (52 : Vertex); exact frozen_52)
    (by change Frozen adjacent Selected mate (48 : Vertex); exact frozen_48)

theorem frozen_57 : Frozen adjacent Selected mate (57 : Vertex) := by
  exact .two_frozen 57 25 29 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (53 : Vertex); exact frozen_53)
    (by change Frozen adjacent Selected mate (49 : Vertex); exact frozen_49)

theorem frozen_58 : Frozen adjacent Selected mate (58 : Vertex) := by
  exact .two_frozen 58 30 26 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (50 : Vertex); exact frozen_50)
    (by change Frozen adjacent Selected mate (54 : Vertex); exact frozen_54)

theorem frozen_59 : Frozen adjacent Selected mate (59 : Vertex) := by
  exact .two_frozen 59 31 27 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (51 : Vertex); exact frozen_51)
    (by change Frozen adjacent Selected mate (55 : Vertex); exact frozen_55)

theorem frozen_60 : Frozen adjacent Selected mate (60 : Vertex) := by
  exact .two_frozen 60 24 20 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (52 : Vertex); exact frozen_52)
    (by change Frozen adjacent Selected mate (56 : Vertex); exact frozen_56)

theorem frozen_61 : Frozen adjacent Selected mate (61 : Vertex) := by
  exact .two_frozen 61 21 25 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (57 : Vertex); exact frozen_57)
    (by change Frozen adjacent Selected mate (53 : Vertex); exact frozen_53)

theorem frozen_62 : Frozen adjacent Selected mate (62 : Vertex) := by
  exact .two_frozen 62 26 22 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (54 : Vertex); exact frozen_54)
    (by change Frozen adjacent Selected mate (58 : Vertex); exact frozen_58)

theorem frozen_63 : Frozen adjacent Selected mate (63 : Vertex) := by
  exact .two_frozen 63 23 27 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (59 : Vertex); exact frozen_59)
    (by change Frozen adjacent Selected mate (55 : Vertex); exact frozen_55)

theorem frozen_64 : Frozen adjacent Selected mate (64 : Vertex) := by
  exact .two_frozen 64 16 20 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (60 : Vertex); exact frozen_60)
    (by change Frozen adjacent Selected mate (56 : Vertex); exact frozen_56)

theorem frozen_65 : Frozen adjacent Selected mate (65 : Vertex) := by
  exact .two_frozen 65 17 21 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (61 : Vertex); exact frozen_61)
    (by change Frozen adjacent Selected mate (57 : Vertex); exact frozen_57)

theorem frozen_66 : Frozen adjacent Selected mate (66 : Vertex) := by
  exact .two_frozen 66 22 18 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (58 : Vertex); exact frozen_58)
    (by change Frozen adjacent Selected mate (62 : Vertex); exact frozen_62)

theorem frozen_67 : Frozen adjacent Selected mate (67 : Vertex) := by
  exact .two_frozen 67 23 19 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (59 : Vertex); exact frozen_59)
    (by change Frozen adjacent Selected mate (63 : Vertex); exact frozen_63)

theorem frozen_68 : Frozen adjacent Selected mate (68 : Vertex) := by
  exact .two_frozen 68 16 12 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (60 : Vertex); exact frozen_60)
    (by change Frozen adjacent Selected mate (64 : Vertex); exact frozen_64)

theorem frozen_69 : Frozen adjacent Selected mate (69 : Vertex) := by
  exact .two_frozen 69 13 17 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (65 : Vertex); exact frozen_65)
    (by change Frozen adjacent Selected mate (61 : Vertex); exact frozen_61)

theorem frozen_70 : Frozen adjacent Selected mate (70 : Vertex) := by
  exact .two_frozen 70 18 14 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (62 : Vertex); exact frozen_62)
    (by change Frozen adjacent Selected mate (66 : Vertex); exact frozen_66)

theorem frozen_71 : Frozen adjacent Selected mate (71 : Vertex) := by
  exact .two_frozen 71 15 19 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (67 : Vertex); exact frozen_67)
    (by change Frozen adjacent Selected mate (63 : Vertex); exact frozen_63)

theorem frozen_72 : Frozen adjacent Selected mate (72 : Vertex) := by
  exact .two_frozen 72 8 12 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (68 : Vertex); exact frozen_68)
    (by change Frozen adjacent Selected mate (64 : Vertex); exact frozen_64)

theorem frozen_73 : Frozen adjacent Selected mate (73 : Vertex) := by
  exact .two_frozen 73 9 13 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (69 : Vertex); exact frozen_69)
    (by change Frozen adjacent Selected mate (65 : Vertex); exact frozen_65)

theorem frozen_74 : Frozen adjacent Selected mate (74 : Vertex) := by
  exact .two_frozen 74 14 10 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (66 : Vertex); exact frozen_66)
    (by change Frozen adjacent Selected mate (70 : Vertex); exact frozen_70)

theorem frozen_75 : Frozen adjacent Selected mate (75 : Vertex) := by
  exact .two_frozen 75 15 11 (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (67 : Vertex); exact frozen_67)
    (by change Frozen adjacent Selected mate (71 : Vertex); exact frozen_71)

theorem frozen_76 : Frozen adjacent Selected mate (76 : Vertex) := by
  exact .selected_frozen 76 88 4 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (73 : Vertex); exact frozen_73)

theorem frozen_77 : Frozen adjacent Selected mate (77 : Vertex) := by
  exact .selected_frozen 77 89 5 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (72 : Vertex); exact frozen_72)

theorem frozen_78 : Frozen adjacent Selected mate (78 : Vertex) := by
  exact .selected_frozen 78 110 6 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (75 : Vertex); exact frozen_75)

theorem frozen_79 : Frozen adjacent Selected mate (79 : Vertex) := by
  exact .selected_frozen 79 111 7 (by decide) (by decide) (by decide) (by decide)
    (by change Frozen adjacent Selected mate (74 : Vertex); exact frozen_74)

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
  | 44 => exact frozen_44
  | 45 => exact frozen_45
  | 46 => exact frozen_46
  | 47 => exact frozen_47
  | 48 => exact frozen_48
  | 49 => exact frozen_49
  | 50 => exact frozen_50
  | 51 => exact frozen_51
  | 52 => exact frozen_52
  | 53 => exact frozen_53
  | 54 => exact frozen_54
  | 55 => exact frozen_55
  | 56 => exact frozen_56
  | 57 => exact frozen_57
  | 58 => exact frozen_58
  | 59 => exact frozen_59
  | 60 => exact frozen_60
  | 61 => exact frozen_61
  | 62 => exact frozen_62
  | 63 => exact frozen_63
  | 64 => exact frozen_64
  | 65 => exact frozen_65
  | 66 => exact frozen_66
  | 67 => exact frozen_67
  | 68 => exact frozen_68
  | 69 => exact frozen_69
  | 70 => exact frozen_70
  | 71 => exact frozen_71
  | 72 => exact frozen_72
  | 73 => exact frozen_73
  | 74 => exact frozen_74
  | 75 => exact frozen_75
  | 76 => exact frozen_76
  | 77 => exact frozen_77
  | 78 => exact frozen_78
  | 79 => exact frozen_79
  | value+80 =>
      change value+80 < 80 at hendpoint
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

def endpointCount (row column : Nat) : Nat :=
  ((List.finRange 120).filter fun vertex => decide (Endpoint vertex ∧
    (coordinate vertex).1/2 = row ∧ (coordinate vertex).2/2 = column)).length

def selectedCount (row column : Nat) : Nat :=
  ((List.finRange 120).filter fun vertex => decide (Selected vertex ∧
    (coordinate vertex).1/2 = row ∧ (coordinate vertex).2/2 = column)).length

def tiles : List (Nat × Nat) := (List.range 7).flatMap fun row =>
  (List.range 7).map fun column => (row, column)

def receiverTiles : List (Nat × Nat) :=
  tiles.filter fun tile => 0 < endpointCount tile.1 tile.2

def receiverSelected : Nat :=
  (receiverTiles.map fun tile => selectedCount tile.1 tile.2).sum

def receiverCharge : Int := (receiverSelected : Int)+40-2*(receiverTiles.length : Int)

theorem exact_receiver_counts : receiverTiles.length = 33 ∧ receiverSelected = 28 := by decide

theorem original_receiver_charge_two : receiverCharge = 2 := by decide

theorem degree_three_frozen_ceiling_fails : ¬ receiverCharge ≤ 1 := by
  rw [original_receiver_charge_two]
  omega

end SubQuorum.RotorStarObstruction
