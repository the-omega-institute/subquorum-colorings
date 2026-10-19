import SubQuorum.RemoteCombRungs

set_option autoImplicit false

namespace SubQuorum.ClosedSourceCavities

structure ComponentPhase where
  positiveSource : Bool
  original : Int
  shifted : Int

def sourceCount (components : List ComponentPhase) : Nat :=
  (components.filter fun component => component.positiveSource).length

theorem complete_component_phase_sum (components : List ComponentPhase)
    (hphase : ∀ component ∈ components,
      component.original = (if component.positiveSource then 1 else 0) ∧
      component.shifted = (if component.positiveSource then -1 else 0)) :
    (components.map fun component => component.original-component.shifted).sum =
      2*(sourceCount components : Int) := by
  induction components with
  | nil => simp [sourceCount]
  | cons component rest inductionHypothesis =>
      have hhead := hphase component (by simp)
      have hrest := inductionHypothesis (by
        intro following hfollowing
        exact hphase following (by simp [hfollowing]))
      cases hsource : component.positiveSource <;>
        simp_all [sourceCount]
      omega

theorem closed_cavity_partition
    (physicalTiles shiftedSquares selected endpoints boundarySelected depth
      physicalExcess shiftedExcess physicalDeficit shiftedDeficit sources : Int)
    (hphysical : physicalDeficit = 2*physicalTiles-selected-endpoints+physicalExcess)
    (hshifted : shiftedDeficit =
      2*shiftedSquares-(selected-boundarySelected)-endpoints+shiftedExcess)
    (htiles : physicalTiles-shiftedSquares = depth+1)
    (hboundary : boundarySelected = 2*depth)
    (hphase : physicalExcess-shiftedExcess = 2*sources)
    (hnonnegative : 0 ≤ shiftedDeficit) :
    physicalDeficit = 2*(sources+1)+shiftedDeficit ∧
      2*(sources+1) ≤ physicalDeficit := by
  omega

structure CavityDonor where
  payment : Nat
  multiplicity : Nat

theorem donor_multiplicity_budget (donors : List CavityDonor) (capacity : Nat)
    (husage : ∀ donor ∈ donors, donor.multiplicity ≤ capacity) :
    (donors.map fun donor => donor.multiplicity*donor.payment).sum ≤
      capacity*(donors.map fun donor => donor.payment).sum := by
  induction donors with
  | nil => simp
  | cons donor rest inductionHypothesis =>
      have hhead := husage donor (by simp)
      have hlocal := Nat.mul_le_mul_right donor.payment hhead
      have hrest := inductionHypothesis (by
        intro following hfollowing
        exact husage following (by simp [hfollowing]))
      simp only [List.map_cons, List.sum_cons, Nat.mul_add]
      omega

theorem twofold_cavity_cover_compensation
    (capacity objective sources covered donorPayment totalCavityPayment slack : Int)
    (hledger : capacity-objective = -sources+donorPayment+slack)
    (hslack : 0 ≤ slack)
    (hcoverage : sources ≤ covered)
    (hlocal : 2*covered ≤ totalCavityPayment)
    (husage : totalCavityPayment ≤ 2*donorPayment) :
    objective ≤ capacity := by
  omega

theorem cavity_boundary_flux_partition
    (physicalTiles shiftedSquares selected endpoints boundarySelected depth
      originalExcessTwice shiftedExcessTwice physicalDeficit shiftedDeficit
      enclosedSources flux : Int)
    (hphysical : 2*physicalDeficit =
      4*physicalTiles-2*selected-endpoints+originalExcessTwice)
    (hshifted : 2*shiftedDeficit =
      4*shiftedSquares-2*(selected-boundarySelected)-endpoints+shiftedExcessTwice)
    (htiles : physicalTiles-shiftedSquares = depth+1)
    (hboundary : boundarySelected = 2*depth)
    (hphase : originalExcessTwice-shiftedExcessTwice = 4*enclosedSources+2*flux) :
    physicalDeficit = 2*(enclosedSources+1)+flux+shiftedDeficit := by
  omega

theorem disjoint_cavity_boundary_compensation
    (capacity objective sources covered donorPayment totalCavityPayment flux slack : Int)
    (hledger : capacity-objective = -sources+donorPayment+slack)
    (hslack : 0 ≤ slack) (hcoverage : sources ≤ covered)
    (hlocal : 2*covered+flux ≤ totalCavityPayment)
    (husage : totalCavityPayment ≤ donorPayment)
    (hflux : -sources ≤ flux) :
    objective ≤ capacity := by
  omega

theorem twofold_cavity_boundary_compensation
    (capacity objective sources covered donorPayment totalCavityPayment flux slack : Int)
    (hledger : capacity-objective = -sources+donorPayment+slack)
    (hslack : 0 ≤ slack) (hcoverage : sources ≤ covered)
    (hlocal : 2*covered+flux ≤ totalCavityPayment)
    (husage : totalCavityPayment ≤ 2*donorPayment)
    (hflux : -1 ≤ flux) :
    objective ≤ capacity := by
  omega

end SubQuorum.ClosedSourceCavities
