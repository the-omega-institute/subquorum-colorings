import SubQuorum.ClosedSourceCavities

set_option autoImplicit false

namespace SubQuorum.MixedCavitySources

open OwnedDonorCompensation LongBentTerminalStrips

theorem adjacent_flank_capacity (state : Int → Int → Label)
    (hupperEndpoint : state 0 1 = .endpoint)
    (hlowerEndpoint : state 1 1 = .endpoint)
    (hupperFeasible : feasibleAt state 0 0)
    (hlowerFeasible : feasibleAt state 1 0) :
    selectedCount (state 0 0)+selectedCount (state 1 0) ≤ 1 := by
  cases hupper : state 0 0 <;> cases hlower : state 1 0 <;>
    simp_all [selectedCount, feasibleAt, degree, occupied] <;> omega

theorem flank_pair_sum_bound (pairs : List Nat)
    (hlocal : ∀ count ∈ pairs, count ≤ 1) :
    pairs.sum ≤ pairs.length := by
  induction pairs with
  | nil => simp
  | cons count rest inductionHypothesis =>
      have hhead := hlocal count (by simp)
      have hrest := inductionHypothesis (by
        intro following hfollowing
        exact hlocal following (by simp [hfollowing]))
      simp only [List.sum_cons, List.length_cons]
      omega

theorem perpendicular_source_phase_bound
    (width outerSelected innerSelected originalRaw shiftedRaw gain : Int)
    (horiginal : originalRaw = 1)
    (hshifted : shiftedRaw = 1-width+outerSelected+innerSelected)
    (hgain : gain = originalRaw-shiftedRaw)
    (houter : 2*outerSelected ≤ width)
    (hinner : 2*innerSelected ≤ width-4) :
    gain = width-outerSelected-innerSelected ∧ 2 ≤ gain ∧ shiftedRaw ≤ -1 := by
  omega

theorem mixed_cavity_partition
    (physicalTiles shiftedSquares selected endpoints boundarySelected depth
      originalExcessTwice shiftedExcessTwice physicalDeficit shiftedDeficit
      enclosedSources flux extra : Int)
    (hphysical : 2*physicalDeficit =
      4*physicalTiles-2*selected-endpoints+originalExcessTwice)
    (hshifted : 2*shiftedDeficit =
      4*shiftedSquares-2*(selected-boundarySelected)-endpoints+shiftedExcessTwice)
    (htiles : physicalTiles-shiftedSquares = depth+1)
    (hboundary : boundarySelected = 2*depth)
    (hphase : originalExcessTwice-shiftedExcessTwice =
      4*enclosedSources+2*flux+2*extra)
    (hextra : 0 ≤ extra) (hdeficit : 0 ≤ shiftedDeficit) :
    physicalDeficit = 2*(enclosedSources+1)+flux+extra+shiftedDeficit ∧
      2*(enclosedSources+1)+flux ≤ physicalDeficit := by
  omega

end SubQuorum.MixedCavitySources
