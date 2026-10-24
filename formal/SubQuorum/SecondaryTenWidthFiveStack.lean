import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenWidthFiveStack

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def leftEndpoint (top bottom left : Int) (point : Point) : Prop :=
  top ≤ point.1 ∧ point.1 ≤ bottom ∧ left ≤ point.2 ∧ point.2 ≤ left+4 ∧
    (point.2 ≤ left+1 ∨ point.1 = top ∨ point.1 = bottom)

def rightEndpoint (top bottom left : Int) (point : Point) : Prop :=
  top ≤ point.1 ∧ point.1 ≤ bottom ∧ left ≤ point.2 ∧ point.2 ≤ left+4 ∧
    (left+3 ≤ point.2 ∨ point.1 = top ∨ point.1 = bottom)

theorem width_five_locks_legs (near far : Int)
    (hnear : 4 ≤ near) (hfar : 4 ≤ far)
    (hnearWidth : near+1 ≤ 5) (hfarWidth : far+1 ≤ 5) :
    near = 4 ∧ far = 4 := by omega

theorem canonical_left_form (height top left : Int) (point : Point) (hheight : 6 ≤ height) :
    endpoint height 4 4 (point.2-left,point.1-top+1) ↔
      leftEndpoint top (top+height-1) left point := by
  unfold endpoint leftEndpoint
  dsimp
  omega

theorem canonical_right_form (height top left : Int) (point : Point) (hheight : 6 ≤ height) :
    endpoint height 4 4 (left+4-point.2,point.1-top+1) ↔
      rightEndpoint top (top+height-1) left point := by
  unfold endpoint rightEndpoint
  dsimp
  omega

def rotorEndpoint (point : Point) : Prop :=
  point = (1,2) ∨ point = (2,2) ∨ point = (2,3) ∨ point = (2,4) ∨
  point = (3,1) ∨ point = (3,2) ∨ point = (3,3) ∨ point = (4,3)

theorem rotor_has_no_bounding_corner (point : Point) (hpoint : rotorEndpoint point) :
    ¬ ((point.1 = 1 ∨ point.1 = 4) ∧ (point.2 = 1 ∨ point.2 = 4)) := by
  unfold rotorEndpoint at hpoint
  rcases hpoint with hpoint | hpoint | hpoint | hpoint | hpoint | hpoint | hpoint | hpoint
  all_goals subst point; decide

theorem right_notch_forced_site_absent (top bottom left : Int) (hheight : top+5 ≤ bottom) :
    ¬ rightEndpoint top bottom left (top+1,left) := by
  unfold rightEndpoint
  dsimp
  omega

theorem right_notch_top_wall (top bottom left column : Int)
    (hheight : top ≤ bottom) (hcolumn : left ≤ column ∧ column ≤ left+2) :
    rightEndpoint top bottom left (top,column) := by
  unfold rightEndpoint
  dsimp
  omega

theorem right_notch_bottom_wall (top bottom left column : Int)
    (hheight : top ≤ bottom) (hcolumn : left ≤ column ∧ column ≤ left+2) :
    rightEndpoint top bottom left (bottom,column) := by
  unfold rightEndpoint
  dsimp
  omega

theorem right_notch_right_wall (top bottom left row : Int)
    (hrow : top+1 ≤ row ∧ row ≤ bottom-1) :
    rightEndpoint top bottom left (row,left+3) := by
  unfold rightEndpoint
  dsimp
  omega

theorem left_notch_absent (top bottom left : Int) (point : Point)
    (hpoint : top+1 ≤ point.1 ∧ point.1 ≤ bottom-1 ∧
      left+2 ≤ point.2 ∧ point.2 ≤ left+4) :
    ¬ leftEndpoint top bottom left point := by
  unfold leftEndpoint
  omega

theorem left_notch_left_wall (top bottom left row : Int)
    (hrow : top+1 ≤ row ∧ row ≤ bottom-1) :
    leftEndpoint top bottom left (row,left+1) := by
  unfold leftEndpoint
  dsimp
  omega

theorem support_and_remainder_phase (topHalf bottomHalf heightHalf : Int) :
    (2*topHalf+1)+1 = 2*(topHalf+1) ∧
    (2*bottomHalf-(2*heightHalf)+1)-1 = 2*(bottomHalf-heightHalf) := by omega

theorem upper_rectangle_size (top bottom height : Int) :
    (bottom-height+1)-top = (bottom-top+1)-height := by omega

theorem positive_small_remainder (remaining height : Int)
    (hremaining : 0 < remaining) (hsmall : remaining < 6) (hheight : 6 ≤ height) :
    ¬ height ≤ remaining := by omega

inductive Stack : Int → Int → Prop where
  | empty : Stack 0 0
  | push (half rest count : Int) (hhalf : 3 ≤ half) (previous : Stack rest count) :
      Stack (2*half+rest) (count+1)

theorem stack_size_even (size count : Int) (hstack : Stack size count) :
    ∃ half : Int, size = 2*half := by
  induction hstack with
  | empty => exact ⟨0, by omega⟩
  | push half rest count hhalf previous ih =>
      obtain ⟨restHalf,hrest⟩ := ih
      exact ⟨half+restHalf,by omega⟩

theorem stack_count_nonnegative (size count : Int) (hstack : Stack size count) :
    0 ≤ count := by
  induction hstack with
  | empty => omega
  | push half rest count hhalf previous ih => omega

theorem stack_resource_bound (size count : Int) (hstack : Stack size count) :
    6*count ≤ size := by
  induction hstack with
  | empty => omega
  | push half rest count hhalf previous ih => omega

theorem immutable_source_charge (height : Int) :
    (height+3)+6-2*(height+4) = 1-height := by omega

theorem full_tile_partition (size count : Int) :
    (size/2+1)+2*(count+1) = size/2+2*count+3 := by omega

theorem directed_event_partition (size count : Int) :
    size+size/2+7+7+4*(count-1) = size+size/2+4*count+10 := by omega

theorem joint_ledger (size count : Int) (heven : ∃ half : Int, size = 2*half) :
    (size-count)+2*(size/2+2*count+3)-(3*(size/2)+4*count+10) =
      size/2-count-4 := by
  obtain ⟨half,hhalf⟩ := heven
  omega

theorem complete_stack_gain_ge_four (size count : Int)
    (hsize : 22 ≤ size) (hstack : Stack size count) :
    4 ≤ size/2-count-4 := by
  have heven := stack_size_even size count hstack
  have hresource := stack_resource_bound size count hstack
  obtain ⟨half,hhalf⟩ := heven
  omega

theorem width_five_enlarged_gain (breadth prefixGain stackGain : Int)
    (hprefix : breadth/2+7 ≤ prefixGain) (hstack : 4 ≤ stackGain) :
    breadth/2+11 ≤ prefixGain+stackGain := by omega

theorem wider_bottom_gain (oldWidth width breadth incident gain : Int)
    (hincident : incident ≤ oldWidth+width+16)
    (hgain : oldWidth+width+breadth/2+25-incident ≤ gain) :
    breadth/2+9 ≤ gain := by omega

theorem selectable_group_ge_twelve (breadth gain : Int)
    (hwidth : 6 ≤ breadth) (hgain : breadth/2+9 ≤ gain) :
    12 ≤ gain := by omega

theorem root_column_separation (left nextLeft width : Int)
    (hwidth : 12 ≤ width) (hnext : nextLeft = left-width-12) :
    nextLeft+3 < left-1 := by omega

theorem no_shared_tile_column (left nextLeft tile : Int)
    (hseparated : nextLeft+3 < left-1)
    (hnextTile : 2*tile ≤ nextLeft+3) (hthisTile : left-1 ≤ 2*tile) :
    False := by omega

inductive Batch : Int → Int → Prop where
  | empty : Batch 0 0
  | push (size stackCount previousGain previousCount : Int)
      (hsize : 22 ≤ size) (hstack : Stack size stackCount)
      (previous : Batch previousGain previousCount) :
      Batch (previousGain+(size/2-stackCount-4)) (previousCount+1)

theorem simultaneous_stack_gain (gain count : Int) (hbatch : Batch gain count) :
    4*count ≤ gain := by
  induction hbatch with
  | empty => omega
  | push size stackCount previousGain previousCount hsize hstack previous ih =>
      have hgain := complete_stack_gain_ge_four size stackCount hsize hstack
      omega

end SubQuorum.SecondaryTenWidthFiveStack
