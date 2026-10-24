import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenBothFarCompensation

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

theorem coupled_column_envelope (offset breadth gap : Int) (hgap : 0 ≤ gap) :
    offset-breadth-gap ≤ (offset+1-breadth)-1 := by omega

theorem consumer_right_envelope (offset width : Int) (hwidth : 12 ≤ width) :
    offset+1 < offset+width+13 := by omega

theorem aligned_tile_column_gate (left right column : Int)
    (hleft : left % 2 = 0) (hright : right % 2 = 1)
    (hlower : left/2 ≤ column/2) (hupper : column/2 ≤ right/2) :
    left ≤ column ∧ column ≤ right := by omega

theorem aligned_bar_collision (left right column far : Int)
    (hlower : left ≤ column) (hupper : column ≤ right) :
    endpoint (right-left+1) 10 far (0,right+1-column) := by
  unfold endpoint
  dsimp
  omega

theorem continuous_stem_stops (start finish barrier : Int)
    (hstart : start ≤ barrier)
    (hdisjoint : ¬(start ≤ barrier ∧ barrier ≤ finish)) : finish < barrier := by omega

theorem stop_before_aligned_bar (finish barrier : Int)
    (hbarrier : barrier % 2 = 0) (hstop : finish < barrier) :
    finish/2 < barrier/2 := by omega

theorem earlier_short_parts_separated (first second : Int)
    (hgap : first+18 ≤ second) : (first-1)/2 < (second-11)/2 := by omega

theorem earlier_long_starts_above (first second : Int)
    (hgap : first+18 ≤ second) : first-11 < second-11 ∧ first-8 < second-11 := by omega

theorem equal_frontier_when_tight (column offset : Int) :
    (offset-4 ≤ column ↔ offset-3 ≤ column+1) := by omega

def activeFrontier (anchor bottom terminal deduction : Int) : Prop :=
  deduction = 0 ∨
  (deduction = 1 ∧ bottom = anchor-3 ∧ terminal ≤ anchor-6) ∨
  (deduction = 2 ∧ (bottom = anchor-7 ∨ bottom = anchor-5) ∧ terminal ≤ anchor-10) ∨
  (deduction = 1 ∧ bottom = anchor-9 ∧ terminal ≤ anchor-10)

theorem positive_old_deduction_stops_T (anchor bottom terminal deduction : Int)
    (hfrontier : activeFrontier anchor bottom terminal deduction)
    (hpositive : 0 < deduction) : terminal < bottom := by
  unfold activeFrontier at hfrontier
  rcases hfrontier with hzero | hZ | hfar | hbar
  · omega
  · omega
  · rcases hfar.2.1 with hfirst | hsecond <;> omega
  · omega

theorem mutual_terminal_forces_zero_old (anchor bottom terminal deduction : Int)
    (hfrontier : activeFrontier anchor bottom terminal deduction)
    (hmutual : bottom < terminal) : deduction = 0 := by
  unfold activeFrontier at hfrontier
  rcases hfrontier with hzero | hZ | hfar | hbar
  · exact hzero
  · omega
  · rcases hfar.2.1 with hfirst | hsecond <;> omega
  · omega

theorem deductions_do_not_stack (deduction epsilon : Int)
    (hdeduction : deduction ≤ 2) (hepsilon : epsilon = 0 ∨ epsilon = 1)
    (hexclusion : epsilon = 1 → deduction = 0) : deduction+2*epsilon ≤ 2 := by
  rcases hepsilon with hzero | hone
  · omega
  · have hvanish := hexclusion hone
    omega

theorem mutual_receipt (full epsilon : Int) : 2*full-(2*full+2*epsilon) = -2*epsilon := by omega

theorem triple_tile_receipt (triple : Int) : 2*triple-0 = 2*triple := by omega

theorem exceptional_width (offset frontierOffset breadth : Int)
    (hgap : frontierOffset+24 ≤ offset)
    (hcolumn : offset+1-breadth = frontierOffset-3) : 28 ≤ breadth := by omega

structure PairData where
  breadth : Int
  deduction : Int
  exceptional : Int
  epsilon : Int
  triple : Int

def gain (entry : PairData) : Int :=
  entry.breadth-entry.deduction-entry.exceptional-2*entry.epsilon+2*entry.triple

theorem exact_ledger (entry : PairData) (oldReceiverFull oldConsumerFull mutualFull : Int) :
    entry.breadth+2*(6+oldReceiverFull+oldConsumerFull+mutualFull+entry.triple)-
      (12+2*oldReceiverFull+2*oldConsumerFull+entry.deduction+entry.exceptional+
        2*mutualFull+2*entry.epsilon) = gain entry := by unfold gain; omega

def validEntry (entry : PairData) : Prop :=
  6 ≤ entry.breadth ∧ 0 ≤ entry.triple ∧
  entry.deduction+2*entry.epsilon ≤ 2 ∧
  (entry.exceptional = 0 ∨ entry.exceptional = 1) ∧
  (entry.exceptional = 1 → 28 ≤ entry.breadth)

theorem one_pair_lower (entry : PairData) (hvalid : validEntry entry) : 4 ≤ gain entry := by
  unfold gain validEntry at *
  rcases hvalid.2.2.2.1 with hzero | hone
  · omega
  · have hlarge := hvalid.2.2.2.2 hone
    omega

theorem exceptional_pair_lower (entry : PairData) (hvalid : validEntry entry)
    (hexceptional : entry.exceptional = 1) : 25 ≤ gain entry := by
  have hlarge := hvalid.2.2.2.2 hexceptional
  unfold gain validEntry at *
  omega

def totalGain : List PairData → Int
  | [] => 0
  | entry :: remaining => gain entry+totalGain remaining

def valid : List PairData → Prop
  | [] => True
  | entry :: remaining => validEntry entry ∧ valid remaining

theorem simultaneous_lower (entries : List PairData) (hvalid : valid entries) :
    4*(entries.length : Int) ≤ totalGain entries := by
  induction entries with
  | nil => simp [totalGain]
  | cons entry remaining inductionHypothesis =>
    have hentry := one_pair_lower entry hvalid.1
    have hremaining := inductionHypothesis hvalid.2
    simp only [totalGain, List.length_cons]
    omega

theorem triple_correction_witness : gain ⟨28,0,1,1,1⟩ = 27 := by decide

theorem sharp_old_loss_witness : gain ⟨6,2,0,0,0⟩ = 4 := by decide

end SubQuorum.SecondaryTenBothFarCompensation
