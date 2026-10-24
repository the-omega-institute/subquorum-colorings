import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenNextSupportEastTerminal

abbrev Point := Int × Int

def adjacent (point other : Point) : Prop :=
  other = (point.1-1,point.2) ∨ other = (point.1+1,point.2) ∨
  other = (point.1,point.2-1) ∨ other = (point.1,point.2+1)

theorem four_blocked_neighbors (fresh : Point → Prop) (point : Point)
    (hnorth : ¬fresh (point.1-1,point.2))
    (hsouth : ¬fresh (point.1+1,point.2))
    (hwest : ¬fresh (point.1,point.2-1))
    (heast : ¬fresh (point.1,point.2+1))
    (hmatched : ∃ other, adjacent point other ∧ fresh other) : False := by
  rcases hmatched with ⟨other, hadjacent, hfresh⟩
  unfold adjacent at hadjacent
  rcases hadjacent with hfirst | hsecond | hthird | hfourth
  · exact hnorth (hfirst ▸ hfresh)
  · exact hsouth (hsecond ▸ hfresh)
  · exact hwest (hthird ▸ hfresh)
  · exact heast (hfourth ▸ hfresh)

theorem three_blocked_neighbors_force_south (fresh : Point → Prop) (point : Point)
    (hnorth : ¬fresh (point.1-1,point.2))
    (hwest : ¬fresh (point.1,point.2-1))
    (heast : ¬fresh (point.1,point.2+1))
    (hmatched : ∃ other, adjacent point other ∧ fresh other) :
    fresh (point.1+1,point.2) := by
  rcases hmatched with ⟨other, hadjacent, hfresh⟩
  unfold adjacent at hadjacent
  rcases hadjacent with hfirst | hsecond | hthird | hfourth
  · exact False.elim (hnorth (hfirst ▸ hfresh))
  · exact hsecond ▸ hfresh
  · exact False.elim (hwest (hthird ▸ hfresh))
  · exact False.elim (heast (hfourth ▸ hfresh))

theorem sealed_continuous_U_stem (fresh : Int → Prop) (start depth : Int)
    (hdepth : 4 ≤ depth)
    (hcontinuous : ∀ row, start ≤ row → row ≤ start+depth → fresh row)
    (hblocked : ¬fresh (start+3)) : False := by
  exact hblocked (hcontinuous (start+3) (by omega) (by omega))

theorem sealed_rotor_fork (fresh : Point → Prop) (point : Point)
    (hleft : ¬fresh (point.1+2,point.2-1))
    (hright : ¬fresh (point.1+2,point.2+1))
    (hroles : fresh (point.1+2,point.2-1) ∨ fresh (point.1+2,point.2+1)) : False := by
  exact hroles.elim hleft hright

theorem south_terminal_bar_rows (depth : Int) (hdepth : depth = 4 ∨ depth = 6) :
    25 ≤ 23+depth-1 ∧ 23+depth-1 ≤ 31 := by omega

theorem corner_near_classification (depth : Int)
    (hdepth : 4 ≤ depth) (hparity : depth % 2 = 0) (hstop : depth < 8) :
    depth = 4 ∨ depth = 6 := by omega

theorem corner_width_classification (breadth : Int)
    (hwidth : 6 ≤ breadth) (hparity : breadth % 2 = 0) (hblocked : breadth ≠ 6) :
    8 ≤ breadth := by omega

theorem corner_six_all_neighbors (depth : Int) (hdepth : depth = 6) :
    24+depth = 30 ∧ 24+depth+1 = 31 := by omega

theorem corner_four_stem_block (depth : Int) (hdepth : depth = 4) :
    24+depth = 28 ∧ 24+depth+3 = 31 := by omega

theorem corner_partial_gain (breadth depth : Int) :
    (breadth-1)+2*(7+(depth-4)/2)-(20+depth-4) =
      breadth-7+(2*((depth-4)/2)-(depth-4)) := by omega

theorem corner_partial_gain_even (breadth depth : Int) (heven : depth % 2 = 0) :
    (breadth-1)+2*(7+(depth-4)/2)-(20+depth-4) = breadth-7 := by omega

theorem upward_source_charge (halfBreadth halfNear halfFar : Int) :
    (2*halfBreadth-1+halfNear+halfFar)+(halfNear+halfFar)-
      2*(halfBreadth+halfNear+halfFar) = -1 := by omega

theorem upward_near_receipt : (1 : Int)+2*2-3 = 2 := by omega

theorem upward_exact_ledger (farFull exceptional : Int) :
    1+2*(2+farFull)-(3+2*farFull+exceptional) = 2-exceptional := by omega

theorem upward_positive (exceptional : Int)
    (hflag : exceptional = 0 ∨ exceptional = 1) : 1 ≤ 2-exceptional := by omega

theorem six_bar_collision_gate (width near far : Int) :
    width+17 ≤ width+13+near-far ↔ 4 ≤ near-far := by omega

theorem eight_far_activation (width near far : Int) :
    width+13+near-far ≤ width+15 ↔ near-far ≤ 2 := by omega

theorem high_far_physical_row (breadth : Int) (hwidth : 10 ≤ breadth) :
    (24-breadth)/2 < 16/2 := by omega

theorem upward_far_before_near : (16 : Int)/2 < 22/2 := by omega

theorem downward_source_charge (halfBreadth halfNear halfFar : Int) :
    (2*halfBreadth-1+halfNear+halfFar)+(4+halfNear+halfFar)-
      2*(halfBreadth+1+halfNear+halfFar) = 1 := by omega

theorem downward_exact_ledger (farEvents : Int) :
    1+2*2-(2+farEvents) = 3-farEvents := by omega

theorem downward_positive (farEvents : Int)
    (hflag : farEvents = 0 ∨ farEvents = 1) : 2 ≤ 3-farEvents := by omega

theorem even_frontier_terminal (frontier terminal : Int)
    (hfrontier : frontier % 2 = 0) (hterminal : terminal % 2 = 1)
    (hafter : frontier < terminal) :
    terminal = frontier+1 ∨ frontier+3 ≤ terminal := by omega

theorem odd_frontier_terminal (frontier terminal : Int)
    (hfrontier : frontier % 2 = 1) (hterminal : terminal % 2 = 1)
    (hafter : frontier < terminal) :
    terminal = frontier+2 ∨ frontier+4 ≤ terminal := by omega

theorem even_partner_excluded (frontier partner terminal : Int)
    (hpartner : partner ≤ frontier) (hafter : frontier < terminal) : partner < terminal := by
  omega

theorem odd_partner_excluded (frontier partner terminal : Int)
    (hpartner : partner ≤ frontier+2) (hafter : frontier+4 ≤ terminal) :
    partner < terminal-1 := by omega

theorem actual_owner_compensation (ownerGain exceptional : Int)
    (hflag : exceptional = 0 ∨ exceptional = 1)
    (hframe : ownerGain = 2-exceptional ∨ ownerGain = 3-exceptional) :
    1 ≤ ownerGain := by omega

theorem downward_bar_right_separation (width depth : Int) (hdepth : 8 ≤ depth) :
    width+19 < width+13+depth-1 := by omega

theorem downward_far_after_near (row : Int) (hrow : 28 ≤ row) :
    (22 : Int)/2 < row/2 := by omega

end SubQuorum.SecondaryTenNextSupportEastTerminal
