import Std.Tactic

set_option autoImplicit false

namespace SubQuorum.FullRoutingMatching

/-- One lost priority digit cannot be offset by any lower score whose
complete range is strictly smaller than the priority coefficient. -/
theorem dominant_digit (coefficient low high rest : Nat)
    (fewer : low < high) (bounded : rest < coefficient) :
    low * coefficient + rest < high * coefficient := by
  have first : low * coefficient + rest < low * coefficient + coefficient :=
    Nat.add_lt_add_left bounded (low * coefficient)
  have step : low * coefficient + coefficient ≤ high * coefficient := by
    have mul := Nat.mul_le_mul_right coefficient (Nat.succ_le_of_lt fewer)
    exact (Nat.succ_mul low coefficient) ▸ mul
  exact Nat.lt_of_lt_of_le first step

/-- A matching with maximal score covers every required internal port,
since the all-internal matching already covers the whole port set. -/
theorem maximal_score_saturates_ports (coefficient covered total rest : Nat)
    (coverBound : covered ≤ total) (restBound : rest < coefficient)
    (optimal : total * coefficient ≤ covered * coefficient + rest) :
    covered = total := by
  cases Nat.eq_or_lt_of_le coverBound with
  | inl equal => exact equal
  | inr fewer =>
    exact False.elim (Nat.not_le_of_gt (dominant_digit coefficient covered total rest fewer restBound) optimal)

/-- The same range bound orders paid sources once internal coverage and
prescribed-source counts are fixed. -/
theorem paid_source_priority (coefficient low high lowRest highRest : Nat)
    (fewer : low < high) (bounded : lowRest < coefficient) :
    low * coefficient + lowRest < high * coefficient + highRest := by
  exact Nat.lt_of_lt_of_le (dominant_digit coefficient low high lowRest fewer bounded)
    (Nat.le_add_right (high * coefficient) highRest)

/-- Every unused bundle has exactly the complementary saved activation fee.
This is one fee for using either or both of its two original slots. -/
theorem saved_fee_complement (left right : Bool) (fee : Nat) :
    (if left || right then fee else 0) +
      (if !(left || right) then fee else 0) = fee := by
  cases left with
  | false =>
    cases right with
    | false => exact Nat.zero_add fee
    | true => rfl
  | true =>
    cases right <;> rfl

/-- Replacing an interval by a beta's unused private output can only remove
access cost and possibly used groups; no new positive charge is introduced. -/
theorem beta_private_cost_nonincrease
    (oldAccess newAccess oldGroups newGroups : Nat)
    (access : newAccess ≤ oldAccess) (groups : newGroups ≤ oldGroups) :
    newAccess + newGroups ≤ oldAccess + oldGroups := by
  exact Nat.add_le_add access groups

/-- Once payment is fixed, coefficient H+1 puts an integer fee change
strictly ahead of all possible physical link-count changes. -/
theorem fee_precedes_links (H lowFee highFee lowLinks highLinks : Nat)
    (fees : lowFee < highFee) (links : lowLinks ≤ H) :
    lowFee * (H+1) + lowLinks < highFee * (H+1) + highLinks := by
  exact paid_source_priority (H+1) lowFee highFee lowLinks highLinks fees
    (Nat.lt_succ_of_le links)

end SubQuorum.FullRoutingMatching

#print axioms SubQuorum.FullRoutingMatching.dominant_digit
#print axioms SubQuorum.FullRoutingMatching.maximal_score_saturates_ports
#print axioms SubQuorum.FullRoutingMatching.paid_source_priority
#print axioms SubQuorum.FullRoutingMatching.saved_fee_complement
#print axioms SubQuorum.FullRoutingMatching.beta_private_cost_nonincrease
#print axioms SubQuorum.FullRoutingMatching.fee_precedes_links
