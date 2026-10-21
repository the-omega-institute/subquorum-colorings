import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenRaisedRightBand

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def northU (origin offset breadth depth far : Int) (left : Bool) (point : Point) : Prop :=
  endpoint breadth depth far
    (point.1-origin+4+depth,if left then offset+1-point.2 else point.2-offset+1)

def parentB (origin offset oldWidth width depth far : Int) (point : Point) : Prop :=
  endpoint (oldWidth+width+26) (depth+2) far
    (point.1-origin+12,point.2-offset+width+13)

def oldP (origin offset oldWidth : Int) (point : Point) : Prop :=
  endpoint (oldWidth+12) 10 4 (point.1-origin+8,oldWidth+13+offset-point.2)

def currentP (origin offset width depth : Int) (point : Point) : Prop :=
  endpoint (width+12) 10 4 (point.1-origin-depth+14,offset+1-point.2)

theorem parent_consumes_current_t (origin offset oldWidth width depth far : Int)
    (hdepth : 24 ≤ depth) :
    parentB origin offset oldWidth width depth far (origin+depth-10,offset-width-12) := by
  unfold parentB endpoint
  dsimp
  omega

theorem parent_far_collision (origin offset oldWidth width depth far : Int)
    (hfar : 12 ≤ far) :
    parentB origin offset oldWidth width depth far (origin,offset+oldWidth+13) ∧
    endpoint 6 4 4 (4,6) := by
  unfold parentB endpoint
  dsimp
  omega

theorem allowed_far_phases (far : Int) (hlower : 4 ≤ far) (heven : far % 2 = 0)
    (havoids : ¬12 ≤ far) : far = 4 ∨ far = 6 ∨ far = 8 ∨ far = 10 := by
  omega

theorem parent_contains_blocker (origin offset oldWidth width depth far : Int)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) :
    parentB origin offset oldWidth width depth far (origin-12,offset) := by
  unfold parentB endpoint
  dsimp
  omega

theorem deep_predecessor_hits_blocker (origin offset breadth incident far : Int)
    (hbreadth : 6 ≤ breadth) (hincident : 8 ≤ incident) (left : Bool) :
    northU origin offset breadth incident far left (origin-12,offset) := by
  cases left <;> unfold northU endpoint <;> dsimp <;> omega

theorem surviving_incident_phases (incident : Int)
    (hlower : 4 ≤ incident) (heven : incident % 2 = 0) (hbound : incident < 8) :
    incident = 4 ∨ incident = 6 := by
  omega

theorem right_depth_four_collision (origin offset breadth far oldWidth : Int)
    (hbreadth : 6 ≤ breadth) (hold : 12 ≤ oldWidth) :
    northU origin offset breadth 4 far false (origin-8,offset+1) ∧
    oldP origin offset oldWidth (origin-8,offset+1) := by
  unfold northU oldP endpoint
  dsimp
  omega

theorem right_depth_six_narrow_collision (origin offset breadth far oldWidth : Int)
    (hbreadth : 6 ≤ breadth) (hupper : breadth ≤ oldWidth+12) (hfar : 4 ≤ far) :
    northU origin offset breadth 6 far false (origin-8,offset+breadth-1) ∧
    oldP origin offset oldWidth (origin-8,offset+breadth-1) := by
  unfold northU oldP endpoint
  dsimp
  omega

theorem right_depth_six_wide_collision (origin offset breadth predecessorFar oldWidth width depth far : Int)
    (hold : 12 ≤ oldWidth) (hwidth : oldWidth+14 ≤ breadth) (hfar : 4 ≤ far) :
    northU origin offset breadth 6 predecessorFar false (origin-10,offset+oldWidth+13) ∧
    parentB origin offset oldWidth width depth far (origin-10,offset+oldWidth+13) := by
  unfold northU parentB endpoint
  dsimp
  omega

theorem left_too_wide_collision (origin offset breadth incident predecessorFar oldWidth width depth far : Int)
    (hincident : incident = 4 ∨ incident = 6) (hdepth : 24 ≤ depth)
    (hwidth : 12 ≤ width) (hbreadth : width+14 ≤ breadth) :
    northU origin offset breadth incident predecessorFar true
      (origin-4-incident,offset-width-12) ∧
    parentB origin offset oldWidth width depth far (origin-4-incident,offset-width-12) := by
  unfold northU parentB endpoint
  dsimp
  omega

theorem left_too_long_collision (origin offset breadth incident far width depth : Int)
    (hincident : incident = 4 ∨ incident = 6) (hdepth : 24 ≤ depth)
    (hbreadth : 6 ≤ breadth) (hupper : breadth ≤ width+12)
    (hfar : depth+incident-10 ≤ far) :
    northU origin offset breadth incident far true (origin+depth-14,offset+1-breadth) ∧
    currentP origin offset width depth (origin+depth-14,offset+1-breadth) := by
  unfold northU currentP endpoint
  dsimp
  omega

theorem legal_far_bound (depth incident far : Int)
    (hdepth : depth % 2 = 0) (hincident : incident % 2 = 0) (hfar : far % 2 = 0) :
    (¬depth+incident-10 ≤ far) ↔ far ≤ depth+incident-12 := by
  omega

theorem unraised_three_owner_cell_absent (origin offset oldWidth width depth far breadth predecessorFar : Int)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) :
    ¬parentB origin offset oldWidth width depth far (origin-10,offset+1) ∧
    ¬northU origin offset breadth 6 predecessorFar true (origin-10,offset+1) ∧
    ¬oldP origin offset oldWidth (origin-10,offset+1) := by
  unfold parentB northU oldP endpoint
  dsimp
  omega

theorem parent_receipt (oldWidth width overlap : Int) :
    (oldWidth+width+25)+2*(2+overlap)-(6+2*overlap) = oldWidth+width+23 := by
  omega

theorem depth_four_receipt (oldWidth width breadth overlap : Int) :
    (oldWidth+width+breadth+24)+2*(4+overlap)-(10+2*overlap) =
      oldWidth+width+breadth+22 := by
  omega

theorem depth_six_receipt (oldWidth width breadthHalf overlap : Int) :
    (oldWidth+width+2*breadthHalf+24)+2*(breadthHalf+3+overlap)-
      (4*breadthHalf+10+2*overlap) = oldWidth+width+20 := by
  omega

theorem depth_four_boundary_signed (farHalf : Int) :
    2*farHalf-(2*farHalf+1) = -1 := by
  omega

theorem depth_six_boundary_signed (farHalf : Int) :
    2*(1+farHalf)-(2*farHalf+1) = 1 := by
  omega

def jointGain (oldWidth width breadth : Int) (depthSix boundary : Bool) : Int :=
  if depthSix then oldWidth+width+20+(if boundary then 1 else 0)
  else oldWidth+width+breadth+22-(if boundary then 1 else 0)

theorem all_joint_gains (oldWidth width breadth : Int) (depthSix boundary : Bool)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) (hbreadth : 6 ≤ breadth) :
    oldWidth+width+20 ≤ jointGain oldWidth width breadth depthSix boundary ∧
    44 ≤ jointGain oldWidth width breadth depthSix boundary := by
  cases depthSix <;> cases boundary <;> simp only [jointGain] <;> omega

theorem pair_row_separation (currentOrigin nextOrigin : Int)
    (hgap : currentOrigin+18 ≤ nextOrigin) :
    currentOrigin-4+10 ≤ nextOrigin-12 := by
  omega

def batchGain : List Int → Int
  | [] => 0
  | gain :: remaining => gain+batchGain remaining

def batchValid : List Int → Prop
  | [] => True
  | gain :: remaining => 44 ≤ gain ∧ batchValid remaining

theorem arbitrary_batch_lower_bound (gains : List Int) (hvalid : batchValid gains) :
    44*(gains.length : Int) ≤ batchGain gains := by
  induction gains with
  | nil => simp [batchGain]
  | cons gain remaining inductionHypothesis =>
    simp only [batchValid] at hvalid
    have hremaining := inductionHypothesis hvalid.2
    simp only [batchGain, List.length_cons]
    omega

theorem arbitrary_paired_chain_bound (baseline rootBreadth before after : Int)
    (gains : List Int) (hvalid : batchValid gains)
    (hbefore : before = baseline+rootBreadth-1-2*(gains.length : Int))
    (hafter : after = before+batchGain gains) :
    baseline+rootBreadth-1+42*(gains.length : Int) ≤ after := by
  have hbudget := arbitrary_batch_lower_bound gains hvalid
  omega

end SubQuorum.SecondaryTenRaisedRightBand
