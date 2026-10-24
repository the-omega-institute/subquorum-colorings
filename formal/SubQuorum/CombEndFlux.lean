import SubQuorum.TransverseCombMouths

set_option autoImplicit false

namespace SubQuorum.CombEndFlux

open OwnedDonorCompensation LongBentTerminalStrips

theorem saturated_end_shifted_count (state : Int → Int → Label)
    (hprevious : state (-1) 0 = .endpoint)
    (hpreviousSupport : state (-1) (-1) = .selected)
    (hendpoint : state 0 0 = .endpoint) (haxial : state 1 0 = .selected)
    (hpreviousFeasible : feasibleAt state (-1) (-1))
    (haxialFeasible : feasibleAt state 1 0) :
    state 0 (-1) = .blank ∧ state 1 (-1) = .blank ∧
      selectedCount (state 0 (-1))+selectedCount (state 1 (-1))+
        selectedCount (state 0 0)+selectedCount (state 1 0) = 1 := by
  have hfirst : state 0 (-1) = .blank := by
    cases hlabel : state 0 (-1) <;>
      simp_all [feasibleAt, degree, occupied] <;> omega
  have hsecond : state 1 (-1) = .blank := by
    cases hlabel : state 1 (-1) <;>
      simp_all [feasibleAt, degree, occupied] <;> omega
  simp [hfirst, hsecond, hendpoint, haxial, selectedCount]

theorem two_tiling_flux
    (physicalTiles physicalEndpointTiles shiftedEndpointTiles sparse saturated
      selectedPhysicalEmpty selectedShiftedEmpty : Nat)
    (weightTwice physicalDeficit shiftedDeficit : Int)
    (hphysicalWeight : weightTwice = 4*(physicalEndpointTiles : Int)+
      saturated-sparse+2*selectedPhysicalEmpty)
    (hshiftedWeight : weightTwice = 4*(shiftedEndpointTiles : Int)+
      sparse-saturated+2*selectedShiftedEmpty)
    (hphysicalDeficit : physicalDeficit = 2*(physicalTiles : Int)-
      2*physicalEndpointTiles-selectedPhysicalEmpty)
    (hshiftedDeficit : shiftedDeficit = 2*((physicalTiles : Int)-1)-
      2*shiftedEndpointTiles-selectedShiftedEmpty) :
    physicalDeficit+sparse = 2+saturated+shiftedDeficit := by
  omega

def flag (present : Bool) : Int := if present then 1 else 0

theorem end_contact_conservation (contacts : List (Bool × Bool)) :
    (contacts.map (fun contact => flag contact.1)).sum+
      (contacts.map (fun contact => flag (!contact.1 && contact.2))).sum =
    (contacts.map (fun contact => flag contact.2)).sum+
      (contacts.map (fun contact => flag (contact.1 && !contact.2))).sum := by
  induction contacts with
  | nil => simp
  | cons contact rest inductionHypothesis =>
      rcases contact with ⟨sparse, saturated⟩
      cases sparse <;> cases saturated <;> simp_all [flag] <;> omega

theorem boundary_flux_bound
    (capacity objective sources unmatchedSparse unmatchedSaturated
      shiftedDeficit remainder : Int)
    (hledger : capacity-objective = sources+unmatchedSaturated-unmatchedSparse+
      shiftedDeficit+remainder)
    (hshifted : 0 ≤ shiftedDeficit) (hremainder : 0 ≤ remainder) :
    objective+sources+unmatchedSaturated ≤ capacity+unmatchedSparse := by
  omega

end SubQuorum.CombEndFlux
