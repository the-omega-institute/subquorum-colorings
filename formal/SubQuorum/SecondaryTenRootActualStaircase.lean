import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenRootActualStaircase

theorem even_interval_overlap (left right : Int)
    (hleft : left % 2 = 0) (hright : right % 2 = 0) :
    2 * ((right-left)/2) - (right-left+1) = -1 := by
  omega

theorem pair_receipt_bound (tiles events length : Int)
    (hlength : length % 2 = 1) (htiles : (length-1)/2 ≤ tiles)
    (hevents : events ≤ length) :
    -1 ≤ 2*tiles-events := by
  omega

theorem four_pair_bound (first second third fourth : Int)
    (hfirst : -1 ≤ first) (hsecond : -1 ≤ second)
    (hthird : -1 ≤ third) (hfourth : -1 ≤ fourth) :
    -4 ≤ first+second+third+fourth := by
  omega

theorem packed_two_intervals (left middle next right : Int)
    (hgap : middle+2 ≤ next) :
    (middle-left)+(right-next) ≤ right-left-2 := by
  omega

theorem shared_bottom_budget (depth oldWidth length count : Int)
    (hdepth : depth % 2 = 0) (hwidth : oldWidth % 2 = 0)
    (hlength : length % 2 = 0)
    (hpacking : length ≤ depth-oldWidth-12-2*(count-1)) :
    length/2+count ≤ (depth-oldWidth-12)/2+1 := by
  omega

theorem empty_bottom_budget (depth oldWidth : Int)
    (hdepth : oldWidth+12 ≤ depth) :
    0 ≤ (depth-oldWidth-12)/2+1 := by
  omega

theorem upper_ledger (oldWidth width breadth secondDepth fourthDepth : Int)
    (hold : oldWidth % 2 = 0) (hbreadth : breadth % 2 = 0)
    (hsecond : secondDepth % 2 = 0) (hfourth : fourthDepth % 2 = 0) :
    oldWidth+width+breadth+24+4+
      2*((oldWidth+breadth+12)/2+secondDepth/2+1+fourthDepth/2+1)-
      (3*(oldWidth+breadth+12)/2+secondDepth+2+3*fourthDepth/2+2) =
        oldWidth/2+width+breadth/2+22-fourthDepth/2 := by
  omega

theorem receipt_partition_bound (pair bottom boundary extra depth oldWidth : Int)
    (hpair : -4 ≤ pair) (hbottom : -((depth-oldWidth-12)/2)-1 ≤ bottom)
    (hboundary : -2 ≤ boundary) (hextra : 0 ≤ extra) :
    -4-((depth-oldWidth-12)/2)-1-2 ≤ pair+bottom+boundary+extra := by
  omega

theorem actual_staircase_gain (oldWidth width breadth depth eta gain : Int)
    (hold : oldWidth % 2 = 0) (hdepth : depth % 2 = 0)
    (hwall : depth ≤ oldWidth+width+22) (hbreadth : 6 ≤ breadth)
    (hreceipts : -4-(depth-oldWidth-12)/2-1-2 ≤ eta)
    (hledger : gain = oldWidth/2+width+breadth/2+22-depth/2+eta) :
    breadth/2-1 ≤ gain ∧ 2 ≤ gain := by
  omega

theorem same_phase_distinct_rows (first second : Int)
    (hphase : first % 2 = second % 2) (hdistinct : first ≠ second) :
    first/2 ≠ second/2 := by
  omega

theorem far_row_phase (origin index height : Int)
    (horigin : origin % 2 = 1) (hheight : height % 2 = 0) :
    (origin-10-index+height) % 2 = 1-index%2 := by
  omega

end SubQuorum.SecondaryTenRootActualStaircase
