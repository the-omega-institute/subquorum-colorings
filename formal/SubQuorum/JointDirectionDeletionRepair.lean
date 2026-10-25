import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.JointDirectionDeletionRepair

/-- Four exact quota-cut values, after subtracting the common old baseline. -/
def Gain (r switches deletions rankH rankC : Int) : Int :=
  min r (min (switches+deletions) (min (switches+rankC) (deletions+rankH)))

def MinimumDeletes (target switches rankH : Int) : Int :=
  max 0 (max (target-switches) (target-rankH))

theorem four_cut_target_iff (r switches deletions rankH rankC target : Int) :
    target≤Gain r switches deletions rankH rankC ↔
      target≤r ∧ target≤switches+deletions ∧
      target≤switches+rankC ∧ target≤deletions+rankH := by
  unfold Gain
  omega

/-- Given the two conditions independent of the deletion budget, this is
an exact lower bound and an attainable count. -/
theorem minimum_deletions_exact (r switches rankH rankC target deletions : Int)
    (targetRank : target≤r) (candidateCoverage : target≤switches+rankC)
    (nonnegative : 0≤deletions) :
    target≤Gain r switches deletions rankH rankC ↔
      MinimumDeletes target switches rankH≤deletions := by
  unfold Gain MinimumDeletes
  omega

theorem target_feasible_iff (r switches rankH rankC target : Int) :
    (∃ deletions, 0≤deletions ∧ target≤Gain r switches deletions rankH rankC) ↔
      target≤r ∧ target≤switches+rankC := by
  constructor
  · rintro ⟨d,_,h⟩
    unfold Gain at h
    omega
  · rintro ⟨hr,hc⟩
    refine ⟨MinimumDeletes target switches rankH,?_,?_⟩
    · unfold MinimumDeletes
      omega
    · unfold Gain MinimumDeletes
      omega

/-- Rank hypotheses follow from the written common resource-network proof. -/
theorem gain_at_least_useful_switches (r switches deletions rankH rankC : Int)
    (_hNonnegative : 0≤rankH) (cNonnegative : 0≤rankC)
    (included : rankH≤r) (_sNonnegative : 0≤switches) (dNonnegative : 0≤deletions) :
    min switches rankH≤Gain r switches deletions rankH rankC := by
  unfold Gain
  omega

theorem exact_optimal_action_counts (r switches deletions rankH rankC : Int)
    (hNonnegative : 0≤rankH) (cNonnegative : 0≤rankC)
    (included : rankH≤r) (submodularBound : r≤rankH+rankC)
    (sNonnegative : 0≤switches) (dNonnegative : 0≤deletions) :
    let g := Gain r switches deletions rankH rankC
    let h := min switches rankH
    0≤g-h ∧ g-h≤deletions ∧
      Gain r h (g-h) rankH rankC=g ∧
      MinimumDeletes g switches rankH=g-h := by
  have lower := gain_at_least_useful_switches r switches deletions rankH rankC
    hNonnegative cNonnegative included sNonnegative dNonnegative
  dsimp
  unfold Gain MinimumDeletes at *
  omega

theorem zero_switch_budget (r deletions rankH rankC : Int)
    (includedC : rankC≤r) (hNonnegative : 0≤rankH) :
    Gain r 0 deletions rankH rankC=min deletions rankC := by
  unfold Gain
  omega

theorem unlimited_class_budgets (r switches deletions rankH rankC : Int)
    (submodularBound : r≤rankH+rankC)
    (allH : rankH≤switches) (allC : rankC≤deletions) :
    Gain r switches deletions rankH rankC=r := by
  unfold Gain
  omega

theorem exact_slack_deficit_identity
    (oldSlack oldDeficit newSlack newDeficit deleted gain : Int)
    (slack : newSlack=oldSlack+deleted) (deficit : newDeficit=oldDeficit-gain) :
    newSlack+newDeficit=oldSlack+oldDeficit+deleted-gain := by omega

/-- Point deletions never add further combined-budget improvement beyond
what the available direction rank and switch count already allow. -/
theorem combined_budget_lower_bound
    (oldSlack oldDeficit newSlack newDeficit deleted switched gain rankH switches : Int)
    (slack : newSlack=oldSlack+deleted) (deficit : newDeficit=oldDeficit-gain)
    (quota : switched≤switches) (unitBound : gain≤switched+deleted)
    (rankBound : gain≤rankH+deleted) :
    oldSlack+oldDeficit-min switches rankH≤newSlack+newDeficit := by omega

theorem optimal_counts_attain_budget
    (oldSlack oldDeficit newSlack newDeficit deleted gain h : Int)
    (slack : newSlack=oldSlack+deleted) (deficit : newDeficit=oldDeficit-gain)
    (optimalDeletionCount : deleted=gain-h) :
    newSlack+newDeficit=oldSlack+oldDeficit-h := by omega

/-- A deletion outside the guarded strips cannot name a private inside
switch unit. This is the explicit no-cross-class-reuse implication. -/
theorem cross_class_units_distinct {Q : Type} (inside : Q → Prop) (h c : Q)
    (switchInside : inside h) (deletionOutside : ¬inside c) : h≠c := by
  intro same
  exact deletionOutside (same ▸ switchInside)

theorem path_family_frontier (q switches deletions : Int) (dNonnegative : 0≤deletions) :
    Gain q switches deletions q (q-1)=min q (min (switches+deletions) (switches+q-1)) := by
  unfold Gain
  omega

theorem path_family_full_iff (q switches deletions : Int)
    (_positive : 1≤q) (dNonnegative : 0≤deletions) :
    Gain q switches deletions q (q-1)=q ↔ 1≤switches ∧ q≤switches+deletions := by
  unfold Gain
  omega

theorem stacked_board_slack (n q : Int) :
    6*(q*(2*n+6)-4) - (q*(9*n+5)+5*(q-1)) - q*(3*n+5)=21*q-19 := by
  simp only [Int.mul_add,Int.mul_sub,Int.mul_left_comm q]
  omega

theorem all_isolated_deleted_count (n q : Int) :
    q*(9*n+5)+5*(q-1) - (q*(7*n-14)-1)=q*(2*n+24)-4 := by
  simp only [Int.mul_add,Int.mul_sub,Int.mul_left_comm q]
  omega

#print axioms four_cut_target_iff
#print axioms minimum_deletions_exact
#print axioms target_feasible_iff
#print axioms gain_at_least_useful_switches
#print axioms exact_optimal_action_counts
#print axioms zero_switch_budget
#print axioms unlimited_class_budgets
#print axioms exact_slack_deficit_identity
#print axioms combined_budget_lower_bound
#print axioms optimal_counts_attain_budget
#print axioms cross_class_units_distinct
#print axioms path_family_frontier
#print axioms path_family_full_iff
#print axioms stacked_board_slack
#print axioms all_isolated_deleted_count

end SubQuorum.JointDirectionDeletionRepair
