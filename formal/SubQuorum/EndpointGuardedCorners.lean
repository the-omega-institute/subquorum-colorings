import SubQuorum.OwnedDonorCompensation

set_option autoImplicit false

namespace SubQuorum.EndpointGuardedCorners

open OwnedDonorCompensation

theorem endpoint_guarded_corner_exact (state : Int → Int → Label)
    (hanchor : state 0 0 = .selected)
    (howner : state 0 (-1) = .endpoint)
    (heastGuard : state 1 2 = .endpoint)
    (hsouthGuard : state 2 1 = .endpoint)
    (hanchorFeasible : feasibleAt state 0 0)
    (hoppositeFeasible : feasibleAt state 1 1)
    (hoppositeTerminal : state 1 1 = .endpoint → 3 ≤ degree state 1 1) :
    state 0 1 = .blank ∧ state 1 0 = .blank ∧ state 1 1 = .blank := by
  cases hnorth : state (-1) 0 <;> cases heast : state 0 1 <;>
    cases hsouth : state 1 0 <;> cases hopposite : state 1 1 <;>
    simp_all [feasibleAt, degree, occupied] <;> omega

end SubQuorum.EndpointGuardedCorners
