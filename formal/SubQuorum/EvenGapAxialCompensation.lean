import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.EvenGapAxialCompensation

inductive Mode where
  | down
  | up
  | rotatedCorner
  | eastTerminal
  | upperRotor
  | lowerRotor
  deriving DecidableEq

def sourceCharge (mode : Mode) (breadthHalf : Int) : Int :=
  match mode with
  | .down | .rotatedCorner => 1-2*breadthHalf
  | .up | .eastTerminal => 1
  | .upperRotor => -2
  | .lowerRotor => 0

def sourceContribution (mode : Mode) (breadthHalf : Int) : Int :=
  max 0 (-sourceCharge mode breadthHalf) +
    if 0 < sourceCharge mode breadthHalf then 1 else 0

def fullCount (mode : Mode) (breadthHalf nearHalf farHalf : Int)
    (spanning equalDepth : Bool) : Int :=
  match mode with
  | .down => nearHalf+1 + if spanning then farHalf+1 else 0
  | .up => nearHalf+1 + if spanning then farHalf+(if equalDepth then 1 else 0) else 0
  | .rotatedCorner => breadthHalf
  | .eastTerminal | .upperRotor | .lowerRotor => 1

def eventCount (mode : Mode) (breadthHalf nearHalf farHalf : Int)
    (spanning equalDepth : Bool) : Int :=
  match mode with
  | .down => 2*nearHalf+1 + if spanning then 2*farHalf+1 else 0
  | .up => 2*nearHalf + if spanning then 2*farHalf else 0
  | .rotatedCorner => 3*breadthHalf
  | .eastTerminal => if equalDepth then 1 else 0
  | .upperRotor => 1
  | .lowerRotor => 0

def marginal (mode : Mode) (breadthHalf nearHalf farHalf : Int)
    (spanning equalDepth : Bool) : Int :=
  sourceContribution mode breadthHalf +
    2*fullCount mode breadthHalf nearHalf farHalf spanning equalDepth -
    eventCount mode breadthHalf nearHalf farHalf spanning equalDepth

def expectedGain (mode : Mode) (breadthHalf : Int) (spanning equalDepth : Bool) : Int :=
  match mode with
  | .down => 2*breadthHalf + if spanning then 1 else 0
  | .up => 3 + if spanning && equalDepth then 2 else 0
  | .rotatedCorner => breadthHalf-1
  | .eastTerminal => 3 - if equalDepth then 1 else 0
  | .upperRotor => 3
  | .lowerRotor => 2

def gainSum (gains : List Int) : Int :=
  match gains with
  | [] => 0
  | gain :: rest => gain+gainSum rest

def mixedGainSum (entries : List (Bool × Int)) : Int :=
  match entries with
  | [] => 0
  | entry :: rest => entry.2+mixedGainSum rest

def tenCount (entries : List (Bool × Int)) : Int :=
  match entries with
  | [] => 0
  | entry :: rest => (if entry.1 then 1 else 0)+tenCount rest

theorem receipt_identity (mode : Mode) (breadthHalf nearHalf farHalf : Int)
    (spanning equalDepth : Bool) (hbreadth : 3 ≤ breadthHalf) :
    marginal mode breadthHalf nearHalf farHalf spanning equalDepth =
      expectedGain mode breadthHalf spanning equalDepth := by
  cases mode <;> cases spanning <;> cases equalDepth <;>
    simp [marginal,sourceContribution,sourceCharge,fullCount,eventCount,expectedGain] <;> omega

theorem all_single_receipts_at_least_two (mode : Mode)
    (breadthHalf nearHalf farHalf : Int) (spanning equalDepth : Bool)
    (hbreadth : 3 ≤ breadthHalf) :
    2 ≤ marginal mode breadthHalf nearHalf farHalf spanning equalDepth := by
  rw [receipt_identity mode breadthHalf nearHalf farHalf spanning equalDepth hbreadth]
  cases mode <;> cases spanning <;> cases equalDepth <;> simp [expectedGain] <;> omega

theorem downward_stem_frontier (gap depthHalf : Int) (heven : gap % 2 = 0)
    (hmiss : 5+2*depthHalf < gap) :
    2*depthHalf ≤ gap-6 := by
  omega

theorem downward_bar_frontier (gap breadthHalf : Int) (heven : gap % 2 = 0)
    (hmiss : 4+2*breadthHalf < gap) :
    2*breadthHalf ≤ gap-6 := by
  omega

theorem horizontal_depth_frontier (width depthHalf : Int) (heven : width % 2 = 0)
    (hmiss : 1+2*depthHalf < width+1) :
    2*depthHalf ≤ width-2 := by
  omega

theorem upward_far_stem_frontier (nearHalf farHalf : Int)
    (hmiss : 1 < 5+2*nearHalf-2*farHalf) :
    2*farHalf ≤ 2*nearHalf+2 := by
  omega

theorem spanning_upward_far_stem_frontier (nearHalf farHalf : Int)
    (hmiss : 3 < 5+2*nearHalf-2*farHalf) :
    2*farHalf ≤ 2*nearHalf := by
  omega

theorem east_terminal_far_frontier (nearHalf farHalf : Int)
    (hmiss : 0 < 1+2*nearHalf-2*farHalf) :
    farHalf ≤ nearHalf := by
  omega

theorem rotated_modes_absent_at_ten (breadthHalf : Int)
    (hbreadth : 3 ≤ breadthHalf) (hfrontier : 2*breadthHalf ≤ 10-6) : False := by
  omega

theorem rotated_breadth_at_twelve (breadthHalf : Int)
    (hbreadth : 3 ≤ breadthHalf) (hfrontier : 2*breadthHalf ≤ 12-6) :
    breadthHalf = 3 := by
  omega

theorem endpoint_window_tile_frontier (startHalf endHalf row : Int)
    (hlower : 2*startHalf+3 ≤ row) (hupper : row ≤ 2*endHalf-1) :
    startHalf+1 ≤ row/2 ∧ row/2 ≤ endHalf-1 := by
  omega

theorem different_gap_tiles_disjoint (firstStart firstEnd secondStart secondEnd
    firstRow secondRow : Int)
    (hordered : firstEnd ≤ secondStart)
    (hfirst : 2*firstStart+3 ≤ firstRow ∧ firstRow ≤ 2*firstEnd-1)
    (hsecond : 2*secondStart+3 ≤ secondRow ∧ secondRow ≤ 2*secondEnd-1) :
    firstRow/2 ≠ secondRow/2 := by
  have hleft := endpoint_window_tile_frontier firstStart firstEnd firstRow hfirst.1 hfirst.2
  have hright := endpoint_window_tile_frontier secondStart secondEnd secondRow hsecond.1 hsecond.2
  omega

theorem different_gap_owners_distinct (firstEnd secondStart : Int)
    (firstEndpoints secondEndpoints : Int → Prop) (hordered : firstEnd ≤ secondStart)
    (hfirst : ∀ row, firstEndpoints row → row ≤ firstEnd-1)
    (hsecond : ∀ row, secondEndpoints row → secondStart+3 ≤ row)
    (hnonempty : ∃ row, firstEndpoints row) :
    firstEndpoints ≠ secondEndpoints := by
  intro hequal
  obtain ⟨row,hrow⟩ := hnonempty
  have hleft := hfirst row hrow
  have hright := hsecond row (hequal ▸ hrow)
  omega

theorem gain_sum_two (gains : List Int) (hgains : ∀ gain ∈ gains, 2 ≤ gain) :
    2*(gains.length : Int) ≤ gainSum gains := by
  induction gains with
  | nil => simp [gainSum]
  | cons gain rest inductionHypothesis =>
    have hgain : 2 ≤ gain := hgains gain (by simp)
    have hrest := inductionHypothesis (by intro value hvalue; exact hgains value (by simp [hvalue]))
    simp only [gainSum,List.length_cons,Int.natCast_add,Int.natCast_one]
    omega

theorem one_owner_selected_bound (gaps : Int) (gains : List Int)
    (hcount : (gains.length : Int) = gaps) (hgains : ∀ gain ∈ gains, 2 ≤ gain) :
    gaps ≤ -gaps+gainSum gains := by
  have hsum := gain_sum_two gains hgains
  omega

theorem mixed_gain_lower_bound (entries : List (Bool × Int))
    (hgains : ∀ entry ∈ entries, (if entry.1 then 5 else 2) ≤ entry.2) :
    2*(entries.length : Int)+3*tenCount entries ≤ mixedGainSum entries := by
  induction entries with
  | nil => simp [mixedGainSum,tenCount]
  | cons entry rest inductionHypothesis =>
    have hgain : (if entry.1 then 5 else 2) ≤ entry.2 := hgains entry (by simp)
    have hrest := inductionHypothesis (by intro value hvalue; exact hgains value (by simp [hvalue]))
    rcases entry with ⟨isTen,gain⟩
    cases isTen <;>
      simp [mixedGainSum,tenCount,List.length_cons,Int.natCast_add] at * <;> omega

theorem mixed_selected_bound (gaps tenGaps : Int) (entries : List (Bool × Int))
    (hcount : (entries.length : Int) = gaps) (hten : tenCount entries = tenGaps)
    (hgains : ∀ entry ∈ entries, (if entry.1 then 5 else 2) ≤ entry.2) :
    gaps+3*tenGaps ≤ -gaps+mixedGainSum entries := by
  have hsum := mixed_gain_lower_bound entries hgains
  omega

theorem residual_selected_repair (amount : Int) (gains : List Int)
    (hcount : (gains.length : Int) = amount) (hgains : ∀ gain ∈ gains, 2 ≤ gain) :
    4+amount ≤ 4-amount+gainSum gains := by
  have hsum := gain_sum_two gains hgains
  omega

end SubQuorum.EvenGapAxialCompensation
