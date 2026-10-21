import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenRootDeepTriple

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def consumer (origin offset breadth incident far : Int) (left : Bool) (point : Point) : Prop :=
  endpoint breadth incident far
    (point.1-origin+4+incident,
     if left then offset+1-point.2 else point.2-offset+1)

def parent (origin offset oldWidth width depth : Int) (point : Point) : Prop :=
  endpoint (oldWidth+width+26) (depth+4) 4
    (point.1-origin+14,point.2-offset+width+13)

def receiver (origin column breadth far : Int) (point : Point) : Prop :=
  endpoint breadth 8 far (point.1-origin+9,point.2-column+1)

def oldP (origin offset width : Int) (point : Point) : Prop :=
  endpoint (width+12) 10 4 (point.1-origin+8,offset+width+13-point.2)

def nextP (origin offset width depth : Int) (point : Point) : Prop :=
  endpoint (width+12) 10 4 (point.1-origin-depth+14,offset+1-point.2)

theorem deep_incident_hits_parent (origin offset breadth incident far oldWidth width depth : Int)
    (hbreadth : 6 ≤ breadth) (hincident : 10 ≤ incident)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) (left : Bool) :
    consumer origin offset breadth incident far left (origin-13,offset) ∧
    parent origin offset oldWidth width depth (origin-13,offset) := by
  cases left <;> unfold consumer parent endpoint <;> dsimp <;> omega

theorem incident_trichotomy (incident : Int) (hlower : 4 ≤ incident)
    (heven : incident % 2 = 0) (havoids : ¬10 ≤ incident) :
    incident = 4 ∨ incident = 6 ∨ incident = 8 := by
  omega

theorem right_four_hits_oldP (origin offset breadth far width : Int)
    (hbreadth : 6 ≤ breadth) (hwidth : 12 ≤ width) :
    consumer origin offset breadth 4 far false (origin-8,offset+1) ∧
    oldP origin offset width (origin-8,offset+1) := by
  unfold consumer oldP endpoint
  dsimp
  omega

theorem right_small_hits_oldP (origin offset breadth incident far width : Int)
    (hbreadth : 6 ≤ breadth) (hupper : breadth ≤ width+12)
    (hincident : incident = 6 ∨ incident = 8) (hfar : 4 ≤ far) :
    consumer origin offset breadth incident far false (origin-8,offset+breadth-1) ∧
    oldP origin offset width (origin-8,offset+breadth-1) := by
  unfold consumer oldP endpoint
  dsimp
  omega

theorem right_six_wide_hits_receiver (origin offset breadth far oldWidth receiverBreadth receiverFar : Int)
    (hold : 12 ≤ oldWidth) (hwide : oldWidth+14 ≤ breadth) (hreceiver : 6 ≤ receiverBreadth) :
    consumer origin offset breadth 6 far false (origin-9,offset+oldWidth+13) ∧
    receiver origin (offset+oldWidth+13) receiverBreadth receiverFar
      (origin-9,offset+oldWidth+13) := by
  unfold consumer receiver endpoint
  dsimp
  omega

theorem right_eight_wide_hits_parent (origin offset breadth far oldWidth width depth : Int)
    (hold : 12 ≤ oldWidth) (hwide : oldWidth+14 ≤ breadth) :
    consumer origin offset breadth 8 far false (origin-11,offset+oldWidth+13) ∧
    parent origin offset oldWidth width depth (origin-11,offset+oldWidth+13) := by
  unfold consumer parent endpoint
  dsimp
  omega

theorem left_wide_hits_parent (origin offset breadth incident far oldWidth width depth : Int)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) (hdepth : 24 ≤ depth)
    (hwide : width+14 ≤ breadth) (hincident : 4 ≤ incident ∧ incident ≤ 8) :
    consumer origin offset breadth incident far true (origin-4-incident,offset-width-12) ∧
    parent origin offset oldWidth width depth (origin-4-incident,offset-width-12) := by
  unfold consumer parent endpoint
  dsimp
  omega

theorem long_far_hits_nextP (origin offset breadth incident far width depth : Int)
    (hbreadth : 6 ≤ breadth) (hupper : breadth ≤ width+12)
    (hincident : 4 ≤ incident ∧ incident ≤ 8) (hdepth : 24 ≤ depth)
    (hlong : depth+incident-10 ≤ far) :
    consumer origin offset breadth incident far true (origin+depth-14,offset+1-breadth) ∧
    nextP origin offset width depth (origin+depth-14,offset+1-breadth) := by
  unfold consumer nextP endpoint
  dsimp
  omega

theorem far_upper_bound (far depth incident : Int)
    (hfar : far % 2 = 0) (hdepth : depth % 2 = 0) (hincident : incident % 2 = 0)
    (havoids : ¬depth+incident-10 ≤ far) : far ≤ depth+incident-12 := by
  omega

theorem allowed_left_avoids_parent (origin offset breadth incident far oldWidth width depth : Int)
    (point : Point) (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width)
    (hbreadth : 6 ≤ breadth) (hupper : breadth ≤ width+12)
    (hincident : 4 ≤ incident ∧ incident ≤ 8)
    (hpoint : consumer origin offset breadth incident far true point) :
    ¬parent origin offset oldWidth width depth point := by
  unfold consumer endpoint at hpoint
  unfold parent endpoint
  dsimp at hpoint ⊢
  omega

theorem allowed_left_avoids_receiver (origin offset breadth incident far oldWidth receiverBreadth receiverFar : Int)
    (point : Point) (hold : 12 ≤ oldWidth) (hbreadth : 6 ≤ breadth) (hreceiver : 6 ≤ receiverBreadth)
    (hpoint : consumer origin offset breadth incident far true point) :
    ¬receiver origin (offset+oldWidth+13) receiverBreadth receiverFar point := by
  unfold consumer endpoint at hpoint
  unfold receiver endpoint
  dsimp at hpoint ⊢
  omega

theorem allowed_left_avoids_nextP (origin offset breadth incident far width depth : Int)
    (point : Point) (hdepth : 24 ≤ depth) (hincident : 4 ≤ incident)
    (hfar : far ≤ depth+incident-12)
    (hpoint : consumer origin offset breadth incident far true point) :
    ¬nextP origin offset width depth point := by
  unfold consumer endpoint at hpoint
  unfold nextP endpoint
  dsimp at hpoint ⊢
  omega

theorem terminal_tile_row_gap (origin incident far depth : Int)
    (hfar : far ≤ depth+incident-12) :
    origin-4-incident+far ≤ origin+depth-16 := by
  omega

theorem shallow_marginal (breadth tight : Int) :
    (breadth-1)+2*(2+tight*0)-4-tight = breadth-1-tight := by
  omega

theorem bar_band_debit (breadthHalf : Int) :
    2*(breadthHalf-1)-4*breadthHalf = -2*breadthHalf-2 := by
  omega

theorem tight_far_correction (farHalf deepest : Int) :
    2*(farHalf+deepest)-(2*farHalf+1) = 2*deepest-1 := by
  omega

theorem deep_marginal (breadthHalf tight : Int) :
    (2*breadthHalf-1)+2*(breadthHalf+1)-(4+4*breadthHalf)+tight = -3+tight := by
  omega

theorem shallow_total (oldWidth width breadth tight : Int) :
    (oldWidth+width+25)+(breadth-1-tight) = oldWidth+width+breadth+24-tight := by
  omega

theorem deep_total (oldWidth width tight : Int) :
    (oldWidth+width+25)+(-3+tight) = oldWidth+width+22+tight := by
  omega

theorem shallow_lower_bound (oldWidth width breadth tight : Int)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) (hbreadth : 6 ≤ breadth)
    (htight : tight ≤ 1) : 53 ≤ oldWidth+width+breadth+24-tight := by
  omega

theorem deep_lower_bound (oldWidth width tight : Int)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) (htight : 0 ≤ tight) :
    46 ≤ oldWidth+width+22+tight := by
  omega

theorem negative_marginal_witness : (49 : Int)+(-3) = 46 := by decide

end SubQuorum.SecondaryTenRootDeepTriple
