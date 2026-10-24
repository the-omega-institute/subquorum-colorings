import SubQuorum.CapacityAwareStrips

set_option autoImplicit false

namespace SubQuorum.RemoteCombRungs

open OwnedDonorCompensation LongBentTerminalStrips

theorem continuing_comb_boundary (state : Int → Int → Label)
    (hendpoint : state 1 0 = .endpoint) (hsupport : state 1 (-1) = .selected)
    (hfeasible : feasibleAt state 1 (-1)) :
    state 0 (-1) = .blank ∧
      selectedCount (state 0 (-1))+selectedCount (state 1 (-1)) = 1 := by
  have hblank : state 0 (-1) = .blank := by
    cases hlabel : state 0 (-1) <;>
      simp_all [feasibleAt, degree, occupied] <;> omega
  simp [hblank, hsupport, selectedCount]

theorem remote_strip_partition
    (tiles selected boundarySelected originalDeficit shiftedDeficit : Int)
    (horiginal : originalDeficit = 2*tiles-selected)
    (hshifted : shiftedDeficit = 2*(tiles-1)-(selected-boundarySelected))
    (hnonnegative : 0 ≤ shiftedDeficit) :
    originalDeficit = 2-boundarySelected+shiftedDeficit ∧
      2-boundarySelected ≤ originalDeficit := by
  omega

structure WeightedDonor where
  payment : Nat
  usage : Nat
  capacity : Nat

theorem weighted_rung_capacity (donors : List WeightedDonor)
    (husage : ∀ donor ∈ donors, donor.usage ≤ donor.capacity) :
    (donors.map fun donor => donor.usage*donor.payment).sum ≤
      (donors.map fun donor => donor.capacity*donor.payment).sum := by
  induction donors with
  | nil => simp
  | cons donor rest inductionHypothesis =>
      have hhead := husage donor (by simp)
      have hlocal := Nat.mul_le_mul_right donor.payment hhead
      have hrest := inductionHypothesis (by
        intro following hfollowing
        exact husage following (by simp [hfollowing]))
      simp only [List.map_cons, List.sum_cons]
      omega

theorem integral_flux_compensation
    (capacity objective flux slack exterior paid : Int)
    (hledger : 2*(capacity-objective) = flux+slack+2*exterior)
    (hslack : 0 ≤ slack) (hexterior : paid ≤ exterior)
    (hflux : -1 ≤ flux+2*paid) :
    objective ≤ capacity := by
  omega

end SubQuorum.RemoteCombRungs
