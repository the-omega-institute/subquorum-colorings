import SubQuorum.ElbowOwnedDonors

set_option autoImplicit false

namespace SubQuorum.GuardedSteppedArms

open OwnedDonorCompensation

theorem guarded_corner_exact (state : Int → Int → Label)
    (hanchor : state 0 0 = .selected)
    (howner : state 0 (-1) = .endpoint)
    (hguard : state 1 2 = .selected)
    (hguardNeighbor : state 0 2 = .endpoint)
    (hanchorFeasible : feasibleAt state 0 0)
    (hguardFeasible : feasibleAt state 1 2) :
    state 0 1 = .blank ∧ state 1 0 = .blank ∧ state 1 1 = .blank := by
  cases hnorth : state (-1) 0 <;> cases heast : state 0 1 <;>
    cases hsouth : state 1 0 <;> cases hopposite : state 1 1 <;>
    simp_all [feasibleAt, degree, occupied] <;> omega

theorem distinct_anchor_neighbors_impossible (state : Int → Int → Label)
    (hanchor : state 0 0 = .selected)
    (hwest : state 0 (-1) = .endpoint)
    (hnorth : state (-1) 0 = .endpoint)
    (hfeasible : feasibleAt state 0 0) : False := by
  simp_all [feasibleAt, degree, occupied]
  omega

theorem old_lower_corner_guard_impossible (state : Int → Int → Label)
    (hnorth : state (-1) 0 = .endpoint)
    (hwest : state 0 (-1) = .endpoint)
    (hguard : state (-1) 0 = .selected ∨ state 0 (-1) = .selected) : False := by
  rcases hguard with hguard | hguard <;> simp_all

theorem stepped_receiver_charge (length : Nat) :
    (2*(length : Int)+9)+(4*length+12)-2*(3*length+10) = 1 := by
  omega

end SubQuorum.GuardedSteppedArms
