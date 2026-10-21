import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenInternalLongPair

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

theorem continuous_far_column (breadth near far row : Int)
    (hbreadth : 6 ≤ breadth) (hlower : 0 ≤ row) (hupper : row ≤ far) :
    endpoint breadth near far (row,breadth) := by unfold endpoint; dsimp; omega

theorem R_column_gate (farColumn column longColumn : Int)
    (hfar : farColumn % 2 = 0) (hcolumn : column % 2 = 1)
    (hlong : longColumn % 2 = 1)
    (hlower : farColumn/2 ≤ longColumn/2) (hupper : longColumn/2 ≤ column/2) :
    farColumn+1 ≤ longColumn ∧ longColumn ≤ column := by omega

theorem T_column_gate (farColumn column longColumn : Int)
    (hfar : farColumn % 2 = 1) (hcolumn : column % 2 = 0)
    (hlong : longColumn % 2 = 1)
    (hlower : farColumn/2 ≤ longColumn/2) (hupper : longColumn/2 ≤ column/2) :
    farColumn ≤ longColumn ∧ longColumn ≤ column+1 := by omega

theorem R_bar_collision (farColumn column longColumn : Int)
    (hlower : farColumn ≤ longColumn) (hupper : longColumn ≤ column) :
    endpoint (column-farColumn+1) 10 4 (0,column+1-longColumn) := by
  unfold endpoint
  dsimp
  omega

theorem T_bar_collision (column breadth longColumn far : Int)
    (hlower : column-breadth+1 ≤ longColumn) (hupper : longColumn ≤ column) :
    endpoint breadth 4 far (0,column+1-longColumn) := by unfold endpoint; dsimp; omega

theorem retained_P_guard (width : Int) (hwidth : 12 ≤ width) :
    endpoint (width+12) 10 4 (0,width+12) := by unfold endpoint; dsimp; omega

theorem continuous_interval_stops (start finish barrier : Int)
    (hstart : start ≤ barrier)
    (havoids : ¬(start ≤ barrier ∧ barrier ≤ finish)) : finish < barrier := by omega

theorem R_stop_before_first_tile (origin finish : Int)
    (horigin : origin % 2 = 1) (hstop : finish < origin-11) :
    finish/2 < (origin-11)/2 := by omega

theorem T_stop_before_first_tile (origin finish : Int)
    (horigin : origin % 2 = 1) (hfinish : finish % 2 = 1)
    (hstop : finish < origin-8) : finish/2 < (origin-8)/2 := by omega

theorem long_far_starts_above_later_bars (first second : Int)
    (hgap : first+18 ≤ second) : first-8 < second-11 ∧ first-8 < second-8 := by omega

theorem short_parts_before_later_pairs (first second : Int)
    (hgap : first+18 ≤ second) : (first-1)/2 < (second-11)/2 := by omega

theorem far_terminals_odd (origin far : Int)
    (horigin : origin % 2 = 1) (hfar : far % 2 = 0) : (origin-8+far) % 2 = 1 := by omega

theorem exceptional_width (firstOffset frontierOffset breadth : Int)
    (hgap : frontierOffset+24 ≤ firstOffset)
    (hcolumn : firstOffset+1-breadth = frontierOffset-3) : 28 ≤ breadth := by omega

def gain (breadth tight deduction : Int) : Int := breadth-2*tight-deduction

theorem long_pair_receipt_identity (breadth tight extraFull deduction : Int) :
    breadth+2*(6+extraFull)-(12+2*tight+2*extraFull+deduction) =
      gain breadth tight deduction := by unfold gain; omega

theorem long_pair_lower (breadth tight deduction : Int)
    (hbreadth : 6 ≤ breadth) (htight : tight = 0 ∨ tight = 1)
    (hdeduction : deduction = 0 ∨ deduction = 1)
    (hexception : deduction = 1 → 28 ≤ breadth) : 4 ≤ gain breadth tight deduction := by
  unfold gain
  cases hdeduction with
  | inl hzero => omega
  | inr hone =>
    have hlarge := hexception hone
    omega

theorem exceptional_pair_lower (breadth tight : Int)
    (hbreadth : 28 ≤ breadth) (htight : tight = 0 ∨ tight = 1) :
    25 ≤ gain breadth tight 1 := by unfold gain; omega

def totalGain : List (Int × Int × Int) → Int
  | [] => 0
  | entry :: remaining => gain entry.1 entry.2.1 entry.2.2+totalGain remaining

def valid : List (Int × Int × Int) → Prop
  | [] => True
  | entry :: remaining =>
    6 ≤ entry.1 ∧ (entry.2.1 = 0 ∨ entry.2.1 = 1) ∧
    (entry.2.2 = 0 ∨ entry.2.2 = 1) ∧
    (entry.2.2 = 1 → 28 ≤ entry.1) ∧ valid remaining

theorem simultaneous_lower (entries : List (Int × Int × Int)) (hvalid : valid entries) :
    4*(entries.length : Int) ≤ totalGain entries := by
  induction entries with
  | nil => simp [totalGain]
  | cons entry remaining inductionHypothesis =>
    simp only [valid] at hvalid
    have hentry := long_pair_lower entry.1 entry.2.1 entry.2.2
      hvalid.1 hvalid.2.1 hvalid.2.2.1 hvalid.2.2.2.1
    have hremaining := inductionHypothesis hvalid.2.2.2.2
    simp only [totalGain, List.length_cons]
    omega

end SubQuorum.SecondaryTenInternalLongPair
