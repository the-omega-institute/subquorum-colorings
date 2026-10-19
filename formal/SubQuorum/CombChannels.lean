import SubQuorum.OpenSourceCavities

set_option autoImplicit false

namespace SubQuorum.CombChannels

theorem whole_channel_partition
    (physicalTiles shiftedSquares selected endpoints boundarySelected rows unequal
      originalExcessTwice shiftedExcessTwice physicalDeficit shiftedDeficit
      sourcePhase flux : Int)
    (hphysical : 2*physicalDeficit =
      4*physicalTiles-2*selected-endpoints+originalExcessTwice)
    (hshifted : 2*shiftedDeficit =
      4*shiftedSquares-2*(selected-boundarySelected)-endpoints+shiftedExcessTwice)
    (htiles : 2*(physicalTiles-shiftedSquares) = rows)
    (hboundary : boundarySelected = rows-2+unequal)
    (hphase : originalExcessTwice-shiftedExcessTwice = 2*sourcePhase+2*flux)
    (hsource : 0 ≤ sourcePhase) (hdeficit : 0 ≤ shiftedDeficit) :
    physicalDeficit = 2-unequal+sourcePhase+flux+shiftedDeficit ∧
      2-unequal+flux ≤ physicalDeficit := by
  omega

theorem aligned_unequal_weighted_payment (unequal payment : Int)
    (hunequal : unequal = 0 ∨ unequal = 1)
    (hpayment : 2-unequal ≤ payment) :
    2 ≤ (1+unequal)*payment := by
  rcases hunequal with haligned | hdifferent
  · subst unequal
    omega
  · subst unequal
    omega

theorem residual_channel_compensation
    (capacity objective flux phase shifted single exterior weightedPayment
      lowerPayment : Int)
    (hledger : 2*(capacity-objective) = flux+phase+shifted+single+2*exterior)
    (hphase : 0 ≤ phase) (hshifted : 0 ≤ shifted)
    (hlower : lowerPayment ≤ weightedPayment)
    (hbudget : weightedPayment ≤ single+2*exterior)
    (hcertificate : -1 ≤ flux+lowerPayment) :
    objective ≤ capacity := by
  omega

end SubQuorum.CombChannels
