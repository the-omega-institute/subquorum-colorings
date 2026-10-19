import SubQuorum.ParallelCombFlux

set_option autoImplicit false

namespace SubQuorum.OrthogonalMouthFlux

open OwnedDonorCompensation LongBentTerminalStrips

theorem chamber_flank_capacity (state : Int → Int → Label)
    (hupper : state 0 0 = .endpoint) (hlower : state 1 0 = .endpoint)
    (hfirst : feasibleAt state 0 (-1)) (hsecond : feasibleAt state 1 (-1)) :
    selectedCount (state 0 (-1))+selectedCount (state 1 (-1)) ≤ 1 := by
  cases hfirstLabel : state 0 (-1) <;> cases hsecondLabel : state 1 (-1) <;>
    simp_all [selectedCount, feasibleAt, degree, occupied] <;> omega

theorem arm_cap_selected_count (state : Int → Int → Label)
    (hendpoint : state 0 0 = .endpoint) (hsupport : state 1 0 = .selected)
    (hfeasible : feasibleAt state 1 0) :
    state 1 (-1) = .blank ∧
      selectedCount (state 0 (-1))+selectedCount (state 1 (-1))+
        selectedCount (state 0 0)+selectedCount (state 1 0) =
          1+selectedCount (state 0 (-1)) ∧
      selectedCount (state 0 (-1)) ≤ 1 := by
  have hblank : state 1 (-1) = .blank := by
    cases hlabel : state 1 (-1) <;>
      simp_all [feasibleAt, degree, occupied] <;> omega
  cases hoptional : state 0 (-1) <;>
    simp [hblank, hendpoint, hsupport, selectedCount]

inductive CrossingTile where
  | noEndpoint (selected : Fin 3)
  | sparseComb
  | saturatedComb
  | otherEndpoint

def crossingLoss : CrossingTile → Int
  | .noEndpoint selected => 2-(selected.val : Int)
  | .sparseComb => 1
  | .saturatedComb => -1
  | .otherEndpoint => 0

theorem crossing_tile_loss_bounds (tile : CrossingTile) :
    -1 ≤ crossingLoss tile ∧ crossingLoss tile ≤ 2 := by
  cases tile with
  | noEndpoint selected =>
      have hbound := selected.isLt
      simp only [crossingLoss]
      omega
  | sparseComb => decide
  | saturatedComb => decide
  | otherEndpoint => decide

theorem crossing_loss_sum_bounds (tiles : List CrossingTile) :
    -(tiles.length : Int) ≤ (tiles.map crossingLoss).sum ∧
      (tiles.map crossingLoss).sum ≤ 2*(tiles.length : Int) := by
  induction tiles with
  | nil => simp
  | cons tile rest inductionHypothesis =>
      have htile := crossing_tile_loss_bounds tile
      simp only [List.map_cons, List.sum_cons, List.length_cons]
      omega

theorem crossing_boundary_bound
    (capacity objective sources outward inward phaseGain shiftedDeficit remainder : Int)
    (tiles : List CrossingTile)
    (hledger : capacity-objective = sources+inward-outward-
      (tiles.map crossingLoss).sum+phaseGain+shiftedDeficit+remainder)
    (hphase : 0 ≤ phaseGain) (hshifted : 0 ≤ shiftedDeficit) (hremainder : 0 ≤ remainder) :
    objective+sources+inward ≤ capacity+outward+(tiles.map crossingLoss).sum ∧
      objective+sources+inward ≤ capacity+outward+2*(tiles.length : Int) := by
  have hcrossings := crossing_loss_sum_bounds tiles
  omega

end SubQuorum.OrthogonalMouthFlux
