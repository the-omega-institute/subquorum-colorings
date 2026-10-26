import Std.Tactic

set_option autoImplicit false

namespace SubQuorum.ResourceDualParity

/-- Applying the usual dual-rank formula converts independence of a deleted
output set to retention of full primal rank. The formula is an assumption;
the flow matroid and its dual construction are proved in the research note. -/
theorem dual_independent_iff_full_rank
    (card fullRank complementRank dualRank : Int)
    (dualFormula : dualRank = card - fullRank + complementRank) :
    dualRank = card ↔ complementRank = fullRank := by
  omega

/-- A feasible state's activation and saved fees partition the total.
This transfers the entire optimality quantifier, over arbitrary state types. -/
theorem min_spent_iff_max_saved {State : Type}
    (feasible : State → Prop) (spent saved : State → Nat) (total : Nat)
    (complement : ∀ s, feasible s → spent s + saved s = total)
    (opt : State) (optFeasible : feasible opt) :
    (∀ s, feasible s → spent opt ≤ spent s) ↔
      (∀ s, feasible s → saved s ≤ saved opt) := by
  have optSum := complement opt optFeasible
  constructor
  · intro minimal s hs
    have otherSum := complement s hs
    have bound := minimal s hs
    omega
  · intro maximal s hs
    have otherSum := complement s hs
    have bound := maximal s hs
    omega

theorem exact_fee_from_saved (spent saved total : Nat)
    (complement : spent + saved = total) : spent = total - saved := by
  omega

theorem budget_iff_saving (spent saved total budget : Nat)
    (complement : spent + saved = total) :
    spent ≤ budget ↔ total ≤ saved + budget := by
  omega

end SubQuorum.ResourceDualParity

#print axioms SubQuorum.ResourceDualParity.dual_independent_iff_full_rank
#print axioms SubQuorum.ResourceDualParity.min_spent_iff_max_saved
#print axioms SubQuorum.ResourceDualParity.exact_fee_from_saved
#print axioms SubQuorum.ResourceDualParity.budget_iff_saving
