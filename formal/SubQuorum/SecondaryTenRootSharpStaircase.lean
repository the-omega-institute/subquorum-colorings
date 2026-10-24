import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenRootSharpStaircase

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def horizontal (origin offset oldWidth index height incident far : Int) (point : Point) : Prop :=
  endpoint height incident far
    (point.2-offset-oldWidth-12+incident,point.1-origin+10+index)

theorem far_overlap_hits_lower_bar
    (origin offset oldWidth upperIndex lowerIndex upperHeight lowerHeight
     upperDepth lowerDepth upperFar lowerFar : Int)
    (hupper : 6 ≤ upperHeight) (hlower : 6 ≤ lowerHeight)
    (hrows : origin-10-lowerIndex+lowerHeight = origin-10-upperIndex+upperHeight+1)
    (hstarts : upperDepth ≥ lowerDepth)
    (hreach : upperDepth-lowerDepth ≤ upperFar) :
    horizontal origin offset oldWidth upperIndex upperHeight upperDepth upperFar
      (origin-10-upperIndex+upperHeight,offset+oldWidth+12-lowerDepth) ∧
    horizontal origin offset oldWidth lowerIndex lowerHeight lowerDepth lowerFar
      (origin-10-upperIndex+upperHeight,offset+oldWidth+12-lowerDepth) := by
  unfold horizontal endpoint
  dsimp
  omega

theorem only_odd_before_even_pair (upperIndex lowerIndex : Int)
    (hupper : 0 ≤ upperIndex ∧ upperIndex ≤ 3) (hlower : 0 ≤ lowerIndex ∧ lowerIndex ≤ 3)
    (hupperPhase : upperIndex % 2 = 1) (hlowerPhase : lowerIndex % 2 = 0)
    (hordered : upperIndex < lowerIndex) :
    upperIndex = 1 ∧ lowerIndex = 2 := by
  omega

theorem old_boundary_before_bottom (origin depth consumerFar farRow : Int)
    (hfar : consumerFar ≤ depth-8) (hboundary : farRow ≤ origin-8+consumerFar) :
    farRow < origin+depth-15 := by
  omega

theorem exclusive_owner_debits (firstA thirdA firstBottom thirdBottom : Int)
    (hfirst : firstA+firstBottom ≤ 1) (hthird : thirdA+thirdBottom ≤ 1) :
    firstA+thirdA+firstBottom+thirdBottom ≤ 2 := by
  omega

theorem refined_receipt_bound (pair length count boundary eta : Int)
    (hpair : -1 ≤ pair) (hexclusive : count+boundary ≤ 2)
    (hledger : pair-length/2-count-boundary ≤ eta) :
    -(length/2)-3 ≤ eta := by
  omega

theorem shared_width_refinement (depth oldWidth length eta : Int)
    (hpacking : length ≤ depth-oldWidth-12)
    (hreceipts : -(length/2)-3 ≤ eta) :
    -((depth-oldWidth-12)/2)-3 ≤ eta := by
  omega

theorem sharp_staircase_gain (oldWidth width breadth depth eta gain : Int)
    (hold : oldWidth % 2 = 0) (hdepth : depth % 2 = 0)
    (hwall : depth ≤ oldWidth+width+22) (hbreadth : 6 ≤ breadth)
    (hreceipts : -((depth-oldWidth-12)/2)-3 ≤ eta)
    (hledger : gain = oldWidth/2+width+breadth/2+22-depth/2+eta) :
    breadth/2+3 ≤ gain ∧ 6 ≤ gain := by
  omega

theorem equality_ledger (oldWidth width breadth : Int)
    (hold : oldWidth % 2 = 0) (hwidth : width % 2 = 0) :
    oldWidth/2+width+breadth/2+22-(oldWidth+width+22)/2-1-1-(width+10)/2-1 =
      breadth/2+3 := by
  omega

theorem equality_bar_separation (width breadth : Int) (hwidth : breadth ≤ width) :
    -width-12+2 ≤ -width-10 ∧ -width-10+2 ≤ -breadth-8 ∧
    -breadth-8+2 = -breadth-6 ∧ -breadth-6+2 = -breadth-4 := by
  omega

theorem equality_far_rows (origin depth : Int) (hdepth : 24 ≤ depth) :
    origin-10+6 = origin-4 ∧ origin-11+8 = origin-3 ∧
    origin-12+10 = origin-2 ∧ origin-13+(depth-2) = origin+depth-15 ∧
    origin+2 < origin+depth-15 := by
  omega

end SubQuorum.SecondaryTenRootSharpStaircase
