import SubQuorum.ElbowSources

set_option autoImplicit false

namespace SubQuorum.ElbowOwnedDonors

open OwnedDonorCompensation LongBentTerminalStrips

theorem capped_corner_unit_deficit (state : Int → Int → Label)
    (hnorthLeft : state (-1) 0 = .endpoint)
    (hnorthRight : state (-1) 1 = .endpoint)
    (hwestUpper : state 0 (-1) = .endpoint)
    (hwestLower : state 1 (-1) = .selected)
    (hupperLeftNotEndpoint : state 0 0 ≠ .endpoint)
    (hupperRightNotEndpoint : state 0 1 ≠ .endpoint)
    (hupperLeftFeasible : feasibleAt state 0 0)
    (hupperRightFeasible : feasibleAt state 0 1)
    (hwestLowerFeasible : feasibleAt state 1 (-1))
    (hlowerRightTerminal : state 1 1 = .endpoint → 3 ≤ degree state 1 1) :
    state 0 0 = .blank ∧ state 1 0 = .blank ∧
      state 0 1 ≠ .endpoint ∧ state 1 1 ≠ .endpoint ∧
      selectedCount (state 0 0)+selectedCount (state 0 1)+
        selectedCount (state 1 0)+selectedCount (state 1 1) ≤ 1 := by
  have heastBound : occupied (state 1 2) ≤ 1 := by
    cases state 1 2 <;> decide
  have hsouthBound : occupied (state 2 1) ≤ 1 := by
    cases state 2 1 <;> decide
  cases hnorthwest : state 0 0 <;> cases hnortheast : state 0 1 <;>
    cases hsouthwest : state 1 0 <;> cases hsoutheast : state 1 1 <;>
    simp_all [feasibleAt, degree, occupied, selectedCount] <;> omega

theorem opposite_run_incompatible (state : Int → Int → Label)
    (hupper : state 0 (-1) = .endpoint)
    (hlower : state 2 (-1) = .endpoint)
    (hsupport : state 1 (-1) = .selected)
    (hfeasible : feasibleAt state 1 (-1)) : False := by
  simp_all [feasibleAt, degree, occupied]
  omega

end SubQuorum.ElbowOwnedDonors
