import SubQuorum.OrthogonalMouthFlux

set_option autoImplicit false

namespace SubQuorum.AdaptiveStripCompensation

structure DonorClaim where
  payment : Nat
  horizontal : Bool
  vertical : Bool

def claimedPayment (donor : DonorClaim) : Nat :=
  (if donor.horizontal then donor.payment else 0)+
    (if donor.vertical then donor.payment else 0)

theorem exclusive_donor_budget (donors : List DonorClaim)
    (hexclusive : ∀ donor ∈ donors, donor.horizontal = false ∨ donor.vertical = false) :
    (donors.map claimedPayment).sum ≤ (donors.map DonorClaim.payment).sum := by
  induction donors with
  | nil => simp
  | cons donor rest inductionHypothesis =>
      have hhead := hexclusive donor (by simp)
      have hrest := inductionHypothesis (by
        intro following hfollowing
        exact hexclusive following (by simp [hfollowing]))
      have hlocal : claimedPayment donor ≤ donor.payment := by
        rcases donor with ⟨payment, horizontal, vertical⟩
        cases horizontal <;> cases vertical <;> simp_all [claimedPayment]
      simp only [List.map_cons, List.sum_cons]
      omega

theorem independent_strip_compensation
    (capacity objective sources unionPayment remainder certificate : Int)
    (hledger : capacity-objective = -sources+unionPayment+remainder)
    (hcertificate : certificate ≤ unionPayment) (hremainder : 0 ≤ remainder) :
    objective+certificate+remainder ≤ capacity+sources ∧
      (sources ≤ certificate → objective ≤ capacity) := by
  omega

theorem negative_star_budget (count : Nat) (hcount : 2 ≤ count) :
    max (2*count-1) 2 = 2*count-1 ∧
      count+1 ≤ max (2*count-1) 2 := by
  have hmajority : 2 ≤ 2*count-1 := by omega
  rw [Nat.max_eq_left hmajority]
  omega

end SubQuorum.AdaptiveStripCompensation
