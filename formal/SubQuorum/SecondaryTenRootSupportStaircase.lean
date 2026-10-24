import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenRootSupportStaircase

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def horizontal (origin offset oldWidth index height incident far : Int) (down : Bool)
    (point : Point) : Prop :=
  endpoint height incident far
    (point.2-offset-oldWidth-12+incident,
     if down then point.1-origin+10+index else origin-8-index-point.1)

def parent (origin offset oldWidth width depth : Int) (point : Point) : Prop :=
  endpoint (oldWidth+width+26) (depth+4) 4
    (point.1-origin+14,point.2-offset+width+13)

def nextP (origin offset width depth : Int) (point : Point) : Prop :=
  endpoint (width+12) 10 4 (point.1-origin-depth+14,offset+1-point.2)

theorem north_ray_meets_ceiling (index : Int) (hindex : 1 ≤ index ∧ index ≤ 3) :
    1 ≤ 4-index ∧ 4-index ≤ 4 := by
  omega

theorem incident_crosses_parent (origin offset oldWidth width depth index height incident far : Int)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width)
    (hindex : 1 ≤ index ∧ index ≤ 3) (hdepth : 24 ≤ depth)
    (hheight : 6 ≤ height) (hlong : oldWidth+width+24 ≤ incident) (down : Bool) :
    horizontal origin offset oldWidth index height incident far down
      (origin-9-index,offset-width-12) ∧
    parent origin offset oldWidth width depth (origin-9-index,offset-width-12) := by
  cases down <;> unfold horizontal parent endpoint <;> dsimp <;> omega

theorem upward_bar_hits_parent (origin offset oldWidth width depth index height incident far : Int)
    (hindex : 1 ≤ index ∧ index ≤ 3) (hheight : 6 ≤ height)
    (hincident : 4 ≤ incident) (hshort : incident ≤ oldWidth+width+22) :
    horizontal origin offset oldWidth index height incident far false
      (origin-13,offset+oldWidth+12-incident) ∧
    parent origin offset oldWidth width depth
      (origin-13,offset+oldWidth+12-incident) := by
  unfold horizontal parent endpoint
  dsimp
  omega

theorem short_incident_hits_previous
    (origin offset oldWidth index height incident far previousHeight previousDepth previousFar : Int)
    (hheight : 6 ≤ height) (hprevious : 6 ≤ previousHeight)
    (hincident : 4 ≤ incident) (hshort : incident ≤ previousDepth) :
    horizontal origin offset oldWidth index height incident far true
      (origin-8-index,offset+oldWidth+13-incident) ∧
    horizontal origin offset oldWidth (index-1) previousHeight previousDepth previousFar true
      (origin-8-index,offset+oldWidth+13-incident) := by
  unfold horizontal endpoint
  dsimp
  omega

theorem far_ray_hits_previous_bar
    (origin offset oldWidth index height incident far previousHeight previousDepth previousFar : Int)
    (hheight : 6 ≤ height) (hshort : height ≤ previousHeight)
    (hleft : previousDepth+2 ≤ incident) (hreach : incident ≤ previousDepth+far) :
    horizontal origin offset oldWidth index height incident far true
      (origin-10-index+height,offset+oldWidth+12-previousDepth) ∧
    horizontal origin offset oldWidth (index-1) previousHeight previousDepth previousFar true
      (origin-10-index+height,offset+oldWidth+12-previousDepth) := by
  unfold horizontal endpoint
  dsimp
  omega

theorem tall_bar_hits_nextP
    (origin offset oldWidth width depth breadth index height incident far : Int)
    (hindex : 1 ≤ index ∧ index ≤ 3) (hdepth : 24 ≤ depth) (hbreadth : 6 ≤ breadth)
    (hlower : oldWidth+breadth+14 ≤ incident) (hupper : incident ≤ oldWidth+width+22)
    (htall : depth+index-4 ≤ height) :
    horizontal origin offset oldWidth index height incident far true
      (origin+depth-14,offset+oldWidth+12-incident) ∧
    nextP origin offset width depth
      (origin+depth-14,offset+oldWidth+12-incident) := by
  unfold horizontal nextP endpoint
  dsimp
  omega

theorem next_support_absent_from_owner
    (origin offset oldWidth index height incident far : Int) (hheight : 6 ≤ height) :
    ¬horizontal origin offset oldWidth index height incident far true
      (origin-10-index,offset+oldWidth+12) := by
  unfold horizontal endpoint
  dsimp
  omega

theorem final_support_in_parent (origin offset oldWidth width depth : Int)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) :
    parent origin offset oldWidth width depth (origin-13,offset+oldWidth+12) := by
  unfold parent endpoint
  dsimp
  omega

theorem tradeoff_from_avoidance (height previousHeight incident previousDepth far : Int)
    (hheight : height % 2 = 0) (hprevious : previousHeight % 2 = 0)
    (hincident : incident % 2 = 0) (hdepth : previousDepth % 2 = 0)
    (hfar : far % 2 = 0)
    (havoids : ¬(height ≤ previousHeight ∧ incident ≤ previousDepth+far)) :
    previousHeight+2 ≤ height ∨ previousDepth+far+2 ≤ incident := by
  omega

theorem staircase_depth_budget (oldWidth width first second third fourth : Int)
    (hfirst : first+2 ≤ second) (hsecond : second+2 ≤ third)
    (hthird : third+2 ≤ fourth) (hwall : fourth ≤ oldWidth+width+22) :
    first ≤ oldWidth+width+16 := by
  omega

theorem necessary_frontier
    (oldWidth width depth breadth consumerFar first second third fourth
     firstHeight secondHeight thirdHeight fourthHeight firstFar secondFar thirdFar fourthFar : Int)
    (hlower : oldWidth+breadth+14 ≤ first) (hwall : fourth ≤ oldWidth+width+22)
    (hsteps : first+2 ≤ second ∧ second+2 ≤ third ∧ third+2 ≤ fourth)
    (hfirstFar : 4 ≤ firstFar) (hotherFar : 4 ≤ secondFar ∧ 4 ≤ thirdFar ∧ 4 ≤ fourthFar)
    (hfirstCap : firstHeight ≤ consumerFar+2 → firstFar ≤ first-oldWidth-breadth-12)
    (htrade : firstHeight+2 ≤ secondHeight ∨ first+secondFar+2 ≤ second)
    (htradeTwo : secondHeight+2 ≤ thirdHeight ∨ second+thirdFar+2 ≤ third)
    (htradeThree : thirdHeight+2 ≤ fourthHeight ∨ third+fourthFar+2 ≤ fourth)
    (hheight : fourthHeight ≤ depth-2)
    (hwidthEven : width % 2 = 0) (hbreadthEven : breadth % 2 = 0)
    (hfirstEven : firstHeight % 2 = 0) (hconsumerEven : consumerFar % 2 = 0) :
    breadth ≤ width ∨ (breadth = width+2 ∧ consumerFar ≤ depth-12) := by
  omega

theorem short_witness_geometry (width breadth index : Int)
    (hwidth : 12 ≤ width) (hbreadth : breadth ≤ width) (hindex : 0 ≤ index ∧ index ≤ 3) :
    -width-12+2 ≤ -width-4-2*index ∧ -width-4-2*index+4 ≤ -breadth ∧
    -width-4-2*index+4 < -4 := by
  omega

theorem tall_witness_last_row (depth consumerFar : Int) (hfar : consumerFar ≤ depth-12) :
    consumerFar-3 < depth-14 := by
  omega

theorem joint_ledger (oldWidth width breadth epsilon : Int)
    (hold : oldWidth % 2 = 0) (hwidth : width % 2 = 0) (hbreadth : breadth % 2 = 0) :
    (oldWidth+width+breadth+26)+3+
      2*(11+((oldWidth+breadth+12)+(oldWidth+width+18)+(oldWidth+width+22))/2+2*epsilon)-
      (24+3*(oldWidth+breadth+12)/2+(oldWidth+width+18)+
        3*(oldWidth+width+22)/2+7*epsilon) = width/2+breadth/2+10-3*epsilon := by
  omega

theorem joint_ge_nineteen (width breadth epsilon : Int)
    (hwidth : 12 ≤ width) (hbreadth : 6 ≤ breadth)
    (hepsilon : epsilon = 0 ∨ (epsilon = 1 ∧ breadth = width+2)) :
    19 ≤ width/2+breadth/2+10-3*epsilon := by
  omega

end SubQuorum.SecondaryTenRootSupportStaircase
