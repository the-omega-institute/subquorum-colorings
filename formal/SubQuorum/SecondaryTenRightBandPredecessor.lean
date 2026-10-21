import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenRightBandPredecessor

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def northU (origin offset breadth depth far : Int) (left : Bool) (point : Point) : Prop :=
  endpoint breadth depth far
    (point.1-origin+4+depth,if left then offset+1-point.2 else point.2-offset+1)

def parentFar (origin offset oldWidth width depth far : Int) (point : Point) : Prop :=
  endpoint (oldWidth+width+26) depth far (point.1-origin+10,point.2-offset+width+13)

def parentB (origin offset oldWidth width depth : Int) (point : Point) : Prop :=
  parentFar origin offset oldWidth width depth 4 point

def predecessorA (origin offset breadth far : Int) (point : Point) : Prop :=
  endpoint breadth 4 far (point.1-origin+8,offset+1-point.2)

def oldP (origin offset oldWidth : Int) (point : Point) : Prop :=
  endpoint (oldWidth+12) 10 4 (point.1-origin+8,oldWidth+13+offset-point.2)

def currentP (origin offset width depth : Int) (point : Point) : Prop :=
  endpoint (width+12) 10 4 (point.1-origin-depth+14,offset+1-point.2)

theorem parent_consumes_current_t (origin offset oldWidth width depth : Int)
    (hdepth : 24 ≤ depth) :
    parentB origin offset oldWidth width depth (origin+depth-10,offset-width-12) := by
  unfold parentB parentFar endpoint
  dsimp
  omega

theorem parent_contains_depth_blocker (origin offset oldWidth width depth : Int)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) :
    parentB origin offset oldWidth width depth (origin-10,offset) := by
  unfold parentB parentFar endpoint
  dsimp
  omega

theorem every_deep_predecessor_hits_parent (origin offset breadth incident far : Int)
    (hbreadth : 6 ≤ breadth) (hincident : 6 ≤ incident) (left : Bool) :
    northU origin offset breadth incident far left (origin-10,offset) := by
  cases left <;> unfold northU endpoint <;> dsimp <;> omega

theorem depth_four_right_hits_oldP (origin offset breadth far oldWidth : Int)
    (hbreadth : 6 ≤ breadth) (hold : 12 ≤ oldWidth) :
    northU origin offset breadth 4 far false (origin-8,offset+1) ∧
    oldP origin offset oldWidth (origin-8,offset+1) := by
  unfold northU oldP endpoint
  dsimp
  omega

theorem overly_wide_predecessor_hits_parent (origin offset oldWidth width depth breadth far : Int)
    (hwidth : 12 ≤ width) (hdepth : 24 ≤ depth) (hbreadth : width+14 ≤ breadth) :
    predecessorA origin offset breadth far (origin-8,offset-width-12) ∧
    parentB origin offset oldWidth width depth (origin-8,offset-width-12) := by
  unfold predecessorA parentB parentFar endpoint
  dsimp
  omega

theorem admissible_predecessor_avoids_parent
    (origin offset oldWidth width depth breadth far : Int) (point : Point)
    (hold : 12 ≤ oldWidth) (hbreadth : 6 ≤ breadth) (hupper : breadth ≤ width+12)
    (hpoint : predecessorA origin offset breadth far point) :
    ¬parentB origin offset oldWidth width depth point := by
  unfold predecessorA endpoint at hpoint
  unfold parentB parentFar endpoint
  dsimp at hpoint ⊢
  omega

theorem overly_long_predecessor_hits_currentP
    (origin offset width depth breadth far : Int)
    (hbreadth : 6 ≤ breadth) (hupper : breadth ≤ width+12)
    (hdepth : 24 ≤ depth) (hfar : depth-6 ≤ far) :
    predecessorA origin offset breadth far (origin+depth-14,offset+1-breadth) ∧
    currentP origin offset width depth (origin+depth-14,offset+1-breadth) := by
  unfold predecessorA currentP endpoint
  dsimp
  omega

theorem predecessor_far_bound (depth far : Int)
    (hdepth : depth % 2 = 0) (hfar : far % 2 = 0) :
    (¬depth-6 ≤ far) ↔ far ≤ depth-8 := by
  omega

theorem predecessor_endpoint_row_bound (origin offset breadth far depth : Int)
    (point : Point) (hdepth : 24 ≤ depth) (hfar : far ≤ depth-8)
    (hpoint : predecessorA origin offset breadth far point) :
    origin-8 ≤ point.1 ∧ point.1 ≤ origin+depth-16 := by
  unfold predecessorA endpoint at hpoint
  dsimp at hpoint
  omega

theorem parent_endpoint_bounds (origin offset oldWidth width depth : Int)
    (point : Point) (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) (hdepth : 24 ≤ depth)
    (hpoint : parentB origin offset oldWidth width depth point) :
    origin-10 ≤ point.1 ∧ point.1 ≤ origin+depth-10 ∧
    offset-width-12 ≤ point.2 ∧ point.2 ≤ offset+oldWidth+13 := by
  unfold parentB parentFar endpoint at hpoint
  dsimp at hpoint
  omega

theorem parent_avoids_oldP (origin offset oldWidth width depth : Int) (point : Point)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width)
    (hpoint : parentB origin offset oldWidth width depth point) :
    ¬oldP origin offset oldWidth point := by
  unfold parentB parentFar endpoint at hpoint
  unfold oldP endpoint
  dsimp at hpoint ⊢
  omega

theorem parent_avoids_currentP (origin offset oldWidth width depth : Int) (point : Point)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) (hdepth : 24 ≤ depth)
    (hpoint : parentB origin offset oldWidth width depth point) :
    ¬currentP origin offset width depth point := by
  unfold parentB parentFar endpoint at hpoint
  unfold currentP endpoint
  dsimp at hpoint ⊢
  omega

theorem three_owner_corner_cells (origin offset oldWidth width depth breadth far : Int)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) (hbreadth : 6 ≤ breadth) :
    parentB origin offset oldWidth width depth (origin-9,offset) ∧
    parentB origin offset oldWidth width depth (origin-9,offset+1) ∧
    predecessorA origin offset breadth far (origin-8,offset) ∧
    oldP origin offset oldWidth (origin-8,offset+1) := by
  unfold parentB parentFar predecessorA oldP endpoint
  dsimp
  omega

theorem corner_missing_from_parent_and_predecessor
    (origin offset oldWidth width depth breadth far : Int)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) :
    ¬parentB origin offset oldWidth width depth (origin-8,offset+1) ∧
    ¬predecessorA origin offset breadth far (origin-8,offset+1) := by
  unfold parentB parentFar predecessorA endpoint
  dsimp
  omega

theorem corner_top_missing_from_oldP_and_predecessor
    (origin offset oldWidth breadth far : Int) :
    ¬oldP origin offset oldWidth (origin-9,offset) ∧
    ¬predecessorA origin offset breadth far (origin-9,offset) := by
  unfold oldP predecessorA endpoint
  dsimp
  omega

theorem boundary_column (offset breadth width : Int) (hboundary : breadth = width+12) :
    offset+1-breadth = (offset-width-12)+1 := by
  omega

theorem strict_column_gap (offset breadth width : Int) (hstrict : breadth ≤ width+10) :
    (offset-width-12)+3 ≤ offset+1-breadth := by
  omega

theorem preceding_band_debit (oldHalf : Int) :
    2*(oldHalf+7)-(4*oldHalf+27) = -(2*oldHalf+13) := by
  omega

theorem parent_gain (oldHalf width : Int) :
    (2*oldHalf+width+25)+2*(oldHalf+9)-(4*oldHalf+32) = width+11 := by
  omega

theorem strict_joint_gain (oldHalf predecessorHalf width : Int) :
    (2*oldHalf+width+2*predecessorHalf+24)+
      2*(oldHalf+predecessorHalf+11)-(4*oldHalf+4*predecessorHalf+36) = width+10 := by
  omega

theorem boundary_signed_bonus (farHalf : Int) : 2*(1+farHalf)-(2*farHalf+1) = 1 := by
  omega

theorem predecessor_marginal (width extra : Int) :
    (width+10+extra)-(width+11) = -1+extra := by
  omega

theorem mixed_pair_lower_bound (width extra : Int) (hwidth : 12 ≤ width) (hextra : 0 ≤ extra) :
    22 ≤ width+10+extra := by
  omega

theorem pair_row_separation (currentOrigin nextOrigin : Int)
    (hgap : currentOrigin+18 ≤ nextOrigin) :
    currentOrigin-4+12 ≤ nextOrigin-10 := by
  omega

def pairedGain : List (Int × Bool) → Int
  | [] => 0
  | entry :: remaining => entry.1+10+(if entry.2 then 1 else 0)+pairedGain remaining

def pairWidthsValid : List (Int × Bool) → Prop
  | [] => True
  | entry :: remaining => 12 ≤ entry.1 ∧ pairWidthsValid remaining

theorem paired_gain_lower_bound (entries : List (Int × Bool))
    (hvalid : pairWidthsValid entries) :
    22*(entries.length : Int) ≤ pairedGain entries := by
  induction entries with
  | nil => simp [pairedGain]
  | cons entry remaining inductionHypothesis =>
    simp only [pairWidthsValid] at hvalid
    have hremaining := inductionHypothesis hvalid.2
    simp only [pairedGain, List.length_cons]
    split <;> omega

theorem paired_chain_selected_bound (baseline rootBreadth before after : Int)
    (entries : List (Int × Bool)) (hvalid : pairWidthsValid entries)
    (hbefore : before = baseline+rootBreadth-1-2*(entries.length : Int))
    (hafter : after = before+pairedGain entries) :
    baseline+rootBreadth-1+20*(entries.length : Int) ≤ after := by
  have hcompensation := paired_gain_lower_bound entries hvalid
  omega

theorem extended_far_hits_oldE (origin offset oldWidth width depth far : Int)
    (hfar : 10 ≤ far) :
    parentFar origin offset oldWidth width depth far (origin,offset+oldWidth+13) ∧
    endpoint 6 4 4 (4,6) := by
  unfold parentFar endpoint
  dsimp
  omega

theorem far_even_phase (far : Int) (hlower : 4 ≤ far) (heven : far % 2 = 0)
    (havoids : ¬10 ≤ far) : far = 4 ∨ far = 6 ∨ far = 8 := by
  omega

theorem extended_far_stays_above_current (origin depth far : Int)
    (hdepth : 24 ≤ depth) (hfar : far ≤ 8) :
    origin-10+far+12 ≤ origin+depth-14 := by
  omega

theorem extended_parent_gain (oldHalf width extension : Int) :
    (2*oldHalf+width+25)+2*(oldHalf+9+extension)-
      (4*oldHalf+32+2*extension) = width+11 := by
  omega

theorem extended_joint_gain (oldHalf predecessorHalf width extension : Int) :
    (2*oldHalf+width+2*predecessorHalf+24)+
      2*(oldHalf+predecessorHalf+11+extension)-
      (4*oldHalf+4*predecessorHalf+36+2*extension) = width+10 := by
  omega

end SubQuorum.SecondaryTenRightBandPredecessor
