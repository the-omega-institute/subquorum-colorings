import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.NeutralPairDonorSaturation

def pairAdjacent (first second : Fin 6) : Bool :=
  (first == 0 && (second == 1 || second == 2 || second == 3)) ||
  (first == 1 && (second == 0 || second == 4 || second == 5)) ||
  ((first == 2 || first == 3) && second == 0) ||
  ((first == 4 || first == 5) && second == 1)

def pairSelected (promoteFirst promoteSecond : Bool) (vertex : Fin 6) : Bool :=
  if vertex = 0 then promoteFirst else if vertex = 1 then promoteSecond else true

def pairOccupied (promoteFirst promoteSecond : Bool) (vertex : Fin 6) : Bool :=
  if vertex = 0 then !promoteSecond else if vertex = 1 then !promoteFirst else true

def pairFeasible (promoteFirst promoteSecond : Bool) : Prop :=
  ∀ vertex : Fin 6, pairSelected promoteFirst promoteSecond vertex = true →
    ([0, 1, 2, 3, 4, 5] : List (Fin 6)).countP
      (fun other => pairAdjacent vertex other &&
        pairOccupied promoteFirst promoteSecond other) ≤ 1

instance (promoteFirst promoteSecond : Bool) : Decidable (pairFeasible promoteFirst promoteSecond) :=
  inferInstanceAs (Decidable (∀ vertex : Fin 6,
    pairSelected promoteFirst promoteSecond vertex = true →
      ([0, 1, 2, 3, 4, 5] : List (Fin 6)).countP
        (fun other => pairAdjacent vertex other &&
          pairOccupied promoteFirst promoteSecond other) ≤ 1))

theorem pair_all_exchanges_excluded (promoteFirst promoteSecond : Bool) :
    pairFeasible promoteFirst promoteSecond ↔
      promoteFirst = false ∧ promoteSecond = false := by
  cases promoteFirst <;> cases promoteSecond <;> decide

def outerEndpoint (width height row column : Int) : Prop :=
  ((row = 0 ∨ row = 1) ∧ 0 ≤ column ∧ column < width) ∨
  (2 ≤ row ∧ row < height ∧ (column = width - 2 ∨ column = width - 1)) ∨
  (row = 2 ∧ column = 0) ∨ (row = height ∧ column = width - 1)

theorem lost_tile_has_no_outer_endpoints (width height : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height) :
    ¬ outerEndpoint width height 2 1 ∧ ¬ outerEndpoint width height 2 2 ∧
    ¬ outerEndpoint width height 3 1 ∧ ¬ outerEndpoint width height 3 2 := by
  unfold outerEndpoint
  omega

theorem relocated_tile_has_no_outer_endpoints (width height : Int)
    (hwidth : 6 ≤ width) :
    ¬ outerEndpoint width height 4 1 ∧ ¬ outerEndpoint width height 4 2 ∧
    ¬ outerEndpoint width height 5 1 ∧ ¬ outerEndpoint width height 5 2 := by
  unfold outerEndpoint
  omega

theorem pair_charge_zero : (1 : Int) + 3 - 2 * 2 = 0 := by omega

theorem saturation_removes_unit :
    (2 : Int) - 1 = 1 ∧ (2 : Int) - 2 = 0 ∧ ¬ (1 : Int) ≤ -(0 : Int) := by omega

theorem outer_charge_one (halfWidth height : Int) :
    (2 * halfWidth + height - 1) + (height + 4) -
      2 * (halfWidth + height + 1) = 1 := by omega

theorem original_counts (width height : Int) :
    (width + height) + (height + 7) = width + 2 * height + 7 := by omega

theorem original_margin (areaHalf width height deficit margin : Int)
    (hdeficit : deficit = areaHalf - width - 2 * height - 6)
    (hmargin : margin = areaHalf - (width + 2 * height + 7)) :
    margin = deficit - 1 := by omega

theorem relocated_original_payment (areaHalf objective deficit : Int)
    (hledger : areaHalf - objective = deficit - 1)
    (hphysical : 2 ≤ deficit) : objective + 1 ≤ areaHalf := by omega

end SubQuorum.NeutralPairDonorSaturation

#print axioms SubQuorum.NeutralPairDonorSaturation.pair_all_exchanges_excluded
#print axioms SubQuorum.NeutralPairDonorSaturation.lost_tile_has_no_outer_endpoints
#print axioms SubQuorum.NeutralPairDonorSaturation.relocated_tile_has_no_outer_endpoints
#print axioms SubQuorum.NeutralPairDonorSaturation.pair_charge_zero
#print axioms SubQuorum.NeutralPairDonorSaturation.saturation_removes_unit
#print axioms SubQuorum.NeutralPairDonorSaturation.outer_charge_one
#print axioms SubQuorum.NeutralPairDonorSaturation.original_counts
#print axioms SubQuorum.NeutralPairDonorSaturation.original_margin
#print axioms SubQuorum.NeutralPairDonorSaturation.relocated_original_payment
