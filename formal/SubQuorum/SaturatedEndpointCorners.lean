import SubQuorum.OwnedDonorCompensation

set_option autoImplicit false

namespace SubQuorum.SaturatedEndpointCorners

open OwnedDonorCompensation

theorem saturated_endpoint_corner_exact (state : Int → Int → Label)
    (hanchor : state 0 0 = .selected)
    (howner : state 0 (-1) = .endpoint)
    (hguardNorth : state 0 2 = .endpoint)
    (hguardEast : state 1 3 = .endpoint)
    (hguardSouth : state 2 2 = .endpoint)
    (hguardDegree : degree state 1 2 ≤ 3)
    (hanchorFeasible : feasibleAt state 0 0) :
    state 0 1 = .blank ∧ state 1 0 = .blank ∧ state 1 1 = .blank := by
  cases hnorth : state (-1) 0 <;> cases heast : state 0 1 <;>
    cases hsouth : state 1 0 <;> cases hopposite : state 1 1 <;>
    simp_all [feasibleAt, degree, occupied] <;> omega

theorem two_leg_receiver_charge (width halfHeightSum tiles selections matching : Int)
    (htiles : tiles = width+1+halfHeightSum)
    (hselections : selections = halfHeightSum+4)
    (hmatching : matching = 2*width+halfHeightSum-1) :
    selections+matching-2*tiles = 1 := by
  omega

end SubQuorum.SaturatedEndpointCorners
