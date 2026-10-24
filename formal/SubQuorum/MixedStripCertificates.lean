import Std

set_option autoImplicit false

namespace SubQuorum.MixedStripCertificates

theorem mixed_loss_identity (vertices capacity oddPairs : Nat)
    (hodd : oddPairs ≤ capacity) :
    max (min vertices capacity) (capacity-oddPairs) =
      capacity-min (capacity-vertices) oddPairs := by
  omega

theorem no_loss_iff_no_excess_or_even (vertices capacity oddPairs : Nat)
    (hodd : oddPairs ≤ capacity) :
    max (min vertices capacity) (capacity-oddPairs) = capacity ↔
      capacity ≤ vertices ∨ oddPairs = 0 := by
  omega

theorem mixed_component_budget (vertices capacity oddPairs : Nat) :
    max (min vertices capacity) (capacity-oddPairs) ≤ capacity := by
  omega

theorem even_ends_reservation_decreases_budget (rank capacity oddPairs : Nat)
    (hfit : oddPairs+2 ≤ capacity) (hweighted : rank ≤ capacity-oddPairs-2) :
    max rank (capacity-oddPairs) =
      1+(1+max rank (capacity-1-(oddPairs+1))) := by
  omega

end SubQuorum.MixedStripCertificates
