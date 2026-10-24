import SubQuorum.MixedCavitySources

set_option autoImplicit false

namespace SubQuorum.OpenSourceCavities

theorem partial_band_sum_nonnegative (gains : List Int)
    (hbands : ∀ gain ∈ gains, 0 ≤ gain) :
    0 ≤ gains.sum := by
  induction gains with
  | nil => simp
  | cons gain rest inductionHypothesis =>
      have hhead := hbands gain (by simp)
      have hrest := inductionHypothesis (by
        intro following hfollowing
        exact hbands following (by simp [hfollowing]))
      simp only [List.sum_cons]
      omega

theorem open_source_cavity_partition
    (physicalTiles shiftedSquares selected endpoints boundarySelected depth
      originalExcessTwice shiftedExcessTwice physicalDeficit shiftedDeficit
      sourcePhase flux : Int)
    (hphysical : 2*physicalDeficit =
      4*physicalTiles-2*selected-endpoints+originalExcessTwice)
    (hshifted : 2*shiftedDeficit =
      4*shiftedSquares-2*(selected-boundarySelected)-endpoints+shiftedExcessTwice)
    (htiles : physicalTiles-shiftedSquares = depth+1)
    (hboundary : boundarySelected = 2*depth)
    (hphase : originalExcessTwice-shiftedExcessTwice = 2*sourcePhase+2*flux)
    (hsource : 0 ≤ sourcePhase) (hdeficit : 0 ≤ shiftedDeficit) :
    physicalDeficit = 2+sourcePhase+flux+shiftedDeficit ∧
      2+flux ≤ physicalDeficit := by
  omega

theorem twofold_open_source_compensation
    (capacity objective sources roots sourcePhase flux donorPayment
      totalCavityPayment remainder : Int)
    (hledger : capacity-objective = -sources+donorPayment+remainder)
    (hremainder : 0 ≤ remainder)
    (hlocal : 2*roots+sourcePhase+flux ≤ totalCavityPayment)
    (husage : totalCavityPayment ≤ 2*donorPayment)
    (hcertificate : 2*sources-1 ≤ 2*roots+sourcePhase+flux) :
    objective ≤ capacity := by
  omega

end SubQuorum.OpenSourceCavities
