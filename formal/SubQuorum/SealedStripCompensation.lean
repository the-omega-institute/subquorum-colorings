import Std

set_option autoImplicit false

namespace SubQuorum.SealedStripCompensation

def pairSum (column : Nat → Nat) : Nat → Nat
  | 0 => 0
  | count+1 => pairSum column count + column (2*count) + column (2*count+1)

theorem unit_square_selection_bound (topLeft topRight bottomLeft bottomRight : Nat)
    (htopLeft : topLeft ≤ 1) (htopRight : topRight ≤ 1)
    (hbottomLeft : bottomLeft ≤ 1) (hbottomRight : bottomRight ≤ 1)
    (hfirst : topLeft = 1 → topRight+bottomLeft ≤ 1)
    (hsecond : topRight = 1 → topLeft+bottomRight ≤ 1)
    (hthird : bottomLeft = 1 → topLeft+bottomRight ≤ 1)
    (hfourth : bottomRight = 1 → topRight+bottomLeft ≤ 1) :
    topLeft+topRight+bottomLeft+bottomRight ≤ 2 := by
  omega

theorem shifted_pair_identity (column : Nat → Nat) (count : Nat) :
    pairSum column (count+1) =
      column 0 + pairSum (fun index => column (index+1)) count + column (2*count+1) := by
  induction count with
  | zero => simp [pairSum]
  | succ count inductionHypothesis =>
      change pairSum column (count+1) + column (2*(count+1)) + column (2*(count+1)+1) =
        column 0 + (pairSum (fun index => column (index+1)) count +
          column (2*count+1) + column (2*count+1+1)) + column (2*(count+1)+1)
      rw [inductionHypothesis]
      have hindex : 2*count+1+1 = 2*(count+1) := by omega
      rw [hindex]
      omega

theorem pair_sum_bound (column : Nat → Nat) (count : Nat) :
    (∀ index, index < count → column (2*index)+column (2*index+1) ≤ 2) →
    pairSum column count ≤ 2*count := by
  induction count with
  | zero => simp [pairSum]
  | succ count inductionHypothesis =>
      intro hfaces
      have hprevious := inductionHypothesis (by
        intro index hindex
        exact hfaces index (Nat.lt_trans hindex (Nat.lt_succ_self count)))
      have hlast := hfaces count (Nat.lt_succ_self count)
      simp only [pairSum]
      omega

theorem sealed_strip_capacity (column : Nat → Nat) (count : Nat)
    (hleft : column 0 = 0) (hright : column (2*count+1) = 0)
    (hfaces : ∀ index, index < count → column (2*index+1)+column (2*index+2) ≤ 2) :
    2 ≤ 2*(count+1)-pairSum column (count+1) := by
  have hshifted := pair_sum_bound (fun index => column (index+1)) count (by
    intro index hindex
    simpa [Nat.add_assoc] using hfaces index hindex)
  have hidentity := shifted_pair_identity column count
  omega

theorem congestion_two_nonreuse (claims incidence remaining : Nat)
    (hcapacity : 2*claims ≤ incidence) (hcongestion : incidence ≤ 2*remaining) :
    claims ≤ remaining := by
  omega

theorem reserved_strip_budget (reserved claims incidence remaining total : Nat)
    (hcapacity : 2*claims ≤ incidence) (hcongestion : incidence ≤ 2*remaining)
    (hpartition : reserved+remaining = total) : reserved+claims ≤ total := by
  omega

end SubQuorum.SealedStripCompensation
