import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenArbitraryConsumers

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def northU (origin offset breadth depth far : Int) (left : Bool) (point : Point) : Prop :=
  endpoint breadth depth far
    (point.1-origin+4+depth,if left then offset+1-point.2 else point.2-offset+1)

def oldP (origin offset width : Int) (point : Point) : Prop :=
  endpoint (width+12) 10 4 (point.1-origin+8,width+13+offset-point.2)

def oldRoot (origin offset width rootBreadth : Int) (point : Point) : Prop :=
  endpoint rootBreadth 6 4 (point.1-origin+6,point.2-offset-width-13)

def oldE (origin offset width : Int) (point : Point) : Prop :=
  endpoint 6 4 4 (origin+4-point.1,point.2-offset-width-7)

theorem north_terminal (origin offset breadth depth far : Int)
    (hdepth : 4 ≤ depth) (left : Bool) :
    northU origin offset breadth depth far left (origin-4,offset) := by
  cases left <;> unfold northU endpoint <;> dsimp <;> omega

theorem relative_and_absolute_parity (origin depth far : Int)
    (horigin : origin % 2 = 1) (hdepth : depth % 2 = 0) (hfar : far % 2 = 0) :
    (-4-depth) % 2 = 0 ∧ (origin-4-depth) % 2 = 1 ∧
    (-4-depth+far) % 2 = 0 ∧ (origin-4-depth+far) % 2 = 1 := by
  omega

theorem right_depth_four_collision (origin offset breadth far width : Int)
    (hbreadth : 6 ≤ breadth) (hwidth : 12 ≤ width) :
    northU origin offset breadth 4 far false (origin-8,offset+1) ∧
    oldP origin offset width (origin-8,offset+1) := by
  unfold northU oldP endpoint
  dsimp
  omega

theorem right_P_frontier_collision (origin offset breadth depth far width : Int)
    (hbreadth : 6 ≤ breadth) (hwidth : breadth ≤ width+12)
    (hdepth : 6 ≤ depth) (hfar : depth-4 ≤ far) :
    northU origin offset breadth depth far false (origin-8,offset+breadth-1) ∧
    oldP origin offset width (origin-8,offset+breadth-1) := by
  unfold northU oldP endpoint
  dsimp
  omega

theorem right_E_frontier_collision (origin offset depth far width : Int)
    (hfar : depth+4 ≤ far) (hdepth : 4 ≤ depth) :
    northU origin offset (width+14) depth far false (origin,offset+width+13) ∧
    oldE origin offset width (origin,offset+width+13) := by
  unfold northU oldE endpoint
  dsimp
  omega

theorem right_root_frontier_collision (origin offset breadth depth far width rootBreadth : Int)
    (hlower : width+16 ≤ breadth) (hupper : breadth ≤ width+rootBreadth+14)
    (hdepth : 6 ≤ depth) (hfar : depth-2 ≤ far) :
    northU origin offset breadth depth far false (origin-6,offset+breadth-1) ∧
    oldRoot origin offset width rootBreadth (origin-6,offset+breadth-1) := by
  unfold northU oldRoot endpoint
  dsimp
  omega

theorem P_frontier_even_bound (depth far : Int)
    (hdepth : depth % 2 = 0) (hfar : far % 2 = 0) :
    (¬depth-4 ≤ far) ↔ far ≤ depth-6 := by
  omega

theorem E_frontier_even_bound (depth far : Int)
    (hdepth : depth % 2 = 0) (hfar : far % 2 = 0) :
    (¬depth+4 ≤ far) ↔ far ≤ depth+2 := by
  omega

theorem root_frontier_even_bound (depth far : Int)
    (hdepth : depth % 2 = 0) (hfar : far % 2 = 0) :
    (¬depth-2 ≤ far) ↔ far ≤ depth-4 := by
  omega

theorem breadth_intervals_exhaustive (breadth width rootBreadth : Int)
    (hbreadth : breadth % 2 = 0) (hwidth : width % 2 = 0)
    (hroot : rootBreadth % 2 = 0) :
    breadth ≤ width+12 ∨ breadth = width+14 ∨
    (width+16 ≤ breadth ∧ breadth ≤ width+rootBreadth+14) ∨
    width+rootBreadth+16 ≤ breadth := by
  omega

theorem right_charge (breadthHalf nearHalf farHalf : Int) :
    (2*breadthHalf-1+nearHalf+farHalf)+(nearHalf+farHalf-2)-
      2*(2*breadthHalf+nearHalf+farHalf-2) = 1-2*breadthHalf := by
  omega

theorem left_charge (breadthHalf nearHalf farHalf : Int) :
    (2*breadthHalf-1+nearHalf+farHalf)+(nearHalf+farHalf+2)-
      2*(2*breadthHalf+nearHalf+farHalf) = 1-2*breadthHalf := by
  omega

theorem left_receipt (breadth : Int) : (breadth-1)+2*2-4 = breadth-1 := by
  omega

theorem deep_receipt (breadth : Int) : (breadth-1)+2*2-5 = breadth-2 := by
  omega

theorem deep_special_receipt (breadth overlap : Int) :
    (breadth-1)+2*(2+overlap)-(6+2*overlap) = breadth-3 := by
  omega

theorem wide_receipt (breadth widthHalf : Int) :
    (breadth-1)+2*(widthHalf+8)-(4*widthHalf+29) = breadth-2*widthHalf-14 := by
  omega

theorem tight_receipt (widthHalf extension : Int) :
    (2*widthHalf+13)+2*(widthHalf+10+extension)-
      (4*widthHalf+32+2*extension) = 1 := by
  omega

def localGain (left : Bool) (breadth depth far width : Int) : Int :=
  if left then breadth-1
  else if depth = 6 then
    if breadth = width+14 then 1 else breadth-width-14
  else breadth-2-(if breadth = width+14 ∧ depth-4 ≤ far then 1 else 0)

def admissible (left : Bool) (breadth depth far width rootBreadth : Int) : Prop :=
  left = true ∨
  (left = false ∧
    ((depth = 6 ∧ ((breadth = width+14 ∧ far ≤ 8) ∨
        width+rootBreadth+16 ≤ breadth)) ∨
     (8 ≤ depth ∧
       ((breadth ≤ width+12 ∧ far ≤ depth-6) ∨
        (breadth = width+14 ∧ far ≤ depth+2) ∨
        (width+16 ≤ breadth ∧ breadth ≤ width+rootBreadth+14 ∧ far ≤ depth-4) ∨
        width+rootBreadth+16 ≤ breadth))))

theorem all_local_gains_positive (left : Bool) (breadth depth far width rootBreadth : Int)
    (hbreadth : 6 ≤ breadth) (hroot : 6 ≤ rootBreadth)
    (hlegal : admissible left breadth depth far width rootBreadth) :
    1 ≤ localGain left breadth depth far width := by
  cases left with
  | false =>
    simp [admissible] at hlegal
    by_cases hdepth : depth = 6
    · by_cases hspecial : breadth = width+14
      · simp [localGain, hdepth, hspecial]
      · simp [localGain, hdepth, hspecial]
        omega
    · by_cases hcontact : breadth = width+14 ∧ depth-4 ≤ far <;>
        simp [localGain, hdepth, hcontact] <;> omega
  | true =>
    simp [localGain]
    omega

theorem local_gain_equality (left : Bool) (breadth depth far width rootBreadth : Int)
    (hbreadth : 6 ≤ breadth) (hroot : 6 ≤ rootBreadth)
    (hlegal : admissible left breadth depth far width rootBreadth) :
    localGain left breadth depth far width = 1 ↔
      left = false ∧ depth = 6 ∧ breadth = width+14 := by
  cases left with
  | false =>
    simp [admissible] at hlegal
    by_cases hdepth : depth = 6
    · by_cases hspecial : breadth = width+14
      · simp [localGain, hdepth, hspecial]
      · simp [localGain, hdepth, hspecial]
        omega
    · by_cases hcontact : breadth = width+14 ∧ depth-4 ≤ far <;>
        simp [localGain, hdepth, hcontact] <;> omega
  | true =>
    simp [localGain]
    omega

theorem equality_far_lengths (far : Int) (hlower : 4 ≤ far) (hupper : far ≤ 8)
    (heven : far % 2 = 0) : far = 4 ∨ far = 6 ∨ far = 8 := by
  omega

theorem overlap_range (depth far overlap : Int)
    (hlower : depth-4 ≤ far) (hupper : far ≤ depth+2)
    (hcount : 2*overlap = far-depth+4) : 0 ≤ overlap ∧ overlap ≤ 3 := by
  omega

theorem selected_local_bound (baseline rootBreadth before after gain : Int)
    (hbefore : before = baseline+rootBreadth-2)
    (hafter : after = before+gain) (hgain : 1 ≤ gain) :
    baseline+rootBreadth-1 ≤ after := by
  omega

theorem selected_tail_bound (baseline rootBreadth before after gain : Int)
    (hroot : 6 ≤ rootBreadth) (hbefore : before = baseline+rootBreadth-6)
    (hafter : after = before+gain) (hgain : 1 ≤ gain) :
    baseline+1 ≤ after := by
  omega

theorem nested_far_column_separation (offset nextOffset breadth nextBreadth nextWidth : Int)
    (hoffset : nextOffset = offset-nextWidth-12)
    (hwidth : nextBreadth+nextWidth+14 ≤ breadth) :
    offset+1-breadth ≤ nextOffset+1-nextBreadth-2 := by
  omega

theorem nested_near_column_separation (offset nextOffset nextWidth : Int)
    (hoffset : nextOffset = offset-nextWidth-12) (hwidth : 12 ≤ nextWidth) :
    nextOffset+24 ≤ offset := by
  omega

theorem nested_depth_difference (origin nextOrigin depth nextDepth barRow nextBarRow oldDepth : Int)
    (horigin : nextOrigin = origin+oldDepth-6)
    (hbar : nextBarRow = barRow+2)
    (hdepth : depth = origin-4-barRow)
    (hnextDepth : nextDepth = nextOrigin-4-nextBarRow) (hold : 24 ≤ oldDepth) :
    nextDepth-depth = oldDepth-8 ∧ depth+16 ≤ nextDepth := by
  omega

theorem nested_row_bound (origin firstBarRow count index : Int)
    (hbar : firstBarRow ≤ origin-2*count-12) (hindex : index ≤ count-1) :
    firstBarRow+2*index+4 ≤ origin-10 := by
  omega

theorem adjacent_rows_same_tile (barRow : Int) (hodd : barRow % 2 = 1) :
    (barRow+1)/2 = (barRow+2)/2 := by
  omega

theorem cross_band_debit (breadthHalf : Int) :
    2*(breadthHalf-1)-2*(2*breadthHalf) = -(2*breadthHalf+2) := by
  omega

theorem later_marginal (breadth : Int) : (breadth-1)-(breadth+2) = -3 := by
  omega

def jointGain (firstBreadth : Int) : List Int → Int
  | [] => firstBreadth-1
  | child :: remaining => jointGain firstBreadth remaining+(child-1)-(child+2)

def sourceMass : List Int → Int
  | [] => 0
  | breadth :: remaining => breadth-1+sourceMass remaining

def contactDebit : List Int → Int
  | [] => 0
  | breadth :: remaining => breadth+2+contactDebit remaining

def nestingFloor (firstBreadth : Int) : List Int → Prop
  | [] => 6 ≤ firstBreadth
  | child :: remaining => child+26 ≤ firstBreadth ∧ nestingFloor child remaining

theorem joint_source_ledger (firstBreadth : Int) (remaining : List Int) :
    firstBreadth-1+sourceMass remaining-contactDebit remaining =
      jointGain firstBreadth remaining := by
  induction remaining with
  | nil => simp [sourceMass, contactDebit, jointGain]
  | cons child remaining inductionHypothesis =>
    simp only [sourceMass, contactDebit, jointGain]
    omega

theorem joint_gain_closed_form (firstBreadth : Int) (remaining : List Int) :
    jointGain firstBreadth remaining = firstBreadth-1-3*(remaining.length : Int) := by
  induction remaining with
  | nil => simp [jointGain]
  | cons child remaining inductionHypothesis =>
    simp only [jointGain, List.length_cons]
    omega

theorem nested_width_budget (firstBreadth : Int) (remaining : List Int)
    (hnesting : nestingFloor firstBreadth remaining) :
    6+26*(remaining.length : Int) ≤ firstBreadth := by
  induction remaining generalizing firstBreadth with
  | nil => simpa [nestingFloor] using hnesting
  | cons child remaining inductionHypothesis =>
    simp only [nestingFloor] at hnesting
    have hchild := inductionHypothesis child hnesting.2
    simp only [List.length_cons]
    omega

theorem nested_compensation (firstBreadth : Int) (remaining : List Int)
    (hnesting : nestingFloor firstBreadth remaining) :
    (remaining.length : Int)+1 ≤ jointGain firstBreadth remaining := by
  have hwidth := nested_width_budget firstBreadth remaining hnesting
  rw [joint_gain_closed_form]
  omega

theorem nested_chain_final_bound (baseline rootBreadth firstBreadth before after : Int)
    (remaining : List Int) (hnesting : nestingFloor firstBreadth remaining)
    (hbefore : before = baseline+rootBreadth-1-((remaining.length : Int)+1))
    (hafter : after = before+jointGain firstBreadth remaining) :
    baseline+rootBreadth-1 ≤ after := by
  have hcomp := nested_compensation firstBreadth remaining hnesting
  omega

theorem nested_tail_final_bound (baseline rootBreadth firstBreadth before after : Int)
    (remaining : List Int) (hnesting : nestingFloor firstBreadth remaining)
    (hroot : 6 ≤ rootBreadth)
    (hbefore : before = baseline+rootBreadth-5-((remaining.length : Int)+1))
    (hafter : after = before+jointGain firstBreadth remaining) :
    baseline+1 ≤ after := by
  have hcomp := nested_compensation firstBreadth remaining hnesting
  omega

end SubQuorum.SecondaryTenArbitraryConsumers
