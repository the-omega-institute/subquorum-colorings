import SubQuorum.AdaptiveStripCompensation

set_option autoImplicit false

namespace SubQuorum.CapacityAwareStrips

structure DonorClaim where
  payment : Nat
  capacity : Nat
  horizontal : Bool
  vertical : Bool

def netClaim (donor : DonorClaim) : Int :=
  (if donor.horizontal then (donor.payment : Int) else 0)+
    (if donor.vertical then (donor.payment : Int) else 0)-
    (if donor.horizontal && donor.vertical then (donor.capacity : Int) else 0)

theorem capped_donor_budget (donors : List DonorClaim)
    (hcapacity : ∀ donor ∈ donors, donor.payment ≤ donor.capacity) :
    (donors.map netClaim).sum ≤ (donors.map fun donor => (donor.payment : Int)).sum := by
  induction donors with
  | nil => simp
  | cons donor rest inductionHypothesis =>
      have hhead := hcapacity donor (by simp)
      have hrest := inductionHypothesis (by
        intro following hfollowing
        exact hcapacity following (by simp [hfollowing]))
      have hlocal : netClaim donor ≤ (donor.payment : Int) := by
        rcases donor with ⟨payment, capacity, horizontal, vertical⟩
        cases horizontal <;> cases vertical <;> simp_all [netClaim] <;> omega
      simp only [List.map_cons, List.sum_cons]
      omega

theorem capacity_two_pair_compensation
    (capacity objective sources firstPayment secondPayment sharedPayment
      unionPayment remainder firstBudget secondBudget : Int)
    (hledger : capacity-objective = -sources+unionPayment+remainder)
    (hunion : firstPayment+secondPayment-sharedPayment ≤ unionPayment)
    (hfirst : firstBudget ≤ firstPayment) (hsecond : secondBudget ≤ secondPayment)
    (hshared : sharedPayment ≤ 2) (hremainder : 0 ≤ remainder)
    (hbudget : sources+2 ≤ firstBudget+secondBudget) :
    objective ≤ capacity := by
  omega

end SubQuorum.CapacityAwareStrips
