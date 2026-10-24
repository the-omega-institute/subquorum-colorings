import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenRootDeepPair

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def northAt (row column breadth incident far : Int) (left : Bool) (point : Point) : Prop :=
  endpoint breadth incident far
    (point.1-row+incident, if left then column+1-point.2 else point.2-column+1)

def parentB (origin column oldWidth width depth : Int) (point : Point) : Prop :=
  northAt (origin+depth-10) (column-oldWidth-width-25)
    (oldWidth+width+26) (depth+4) 4 false point

def receiver (origin column breadth far : Int) (point : Point) : Prop :=
  northAt (origin-1) column breadth 8 far false point

def root (origin column breadth : Int) (point : Point) : Prop :=
  endpoint breadth 6 4 (point.1-origin+6,point.2-column)

def oldP (origin column oldWidth : Int) (point : Point) : Prop :=
  endpoint (oldWidth+12) 10 4 (point.1-origin+8,column-point.2)

def oldE (origin column : Int) (point : Point) : Prop :=
  endpoint 6 4 4 (origin+4-point.1,point.2-column+6)

theorem parent_contains_upper_blocker (origin column oldWidth width depth : Int) :
    parentB origin column oldWidth width depth (origin-10,column) := by
  unfold parentB northAt endpoint
  dsimp
  omega

theorem every_deep_receiver_hits_parent (origin column breadth incident far : Int)
    (hbreadth : 6 ≤ breadth) (hincident : 10 ≤ incident) (left : Bool) :
    northAt (origin-1) column breadth incident far left (origin-10,column) := by
  cases left <;> unfold northAt endpoint <;> dsimp <;> omega

theorem forced_incident_eight (incident : Int)
    (hlower : 8 ≤ incident) (heven : incident % 2 = 0)
    (havoids : ¬10 ≤ incident) : incident = 8 := by
  omega

theorem narrow_receiver_hits_root (origin column breadth far rootBreadth : Int)
    (hbreadth : 6 ≤ breadth) (hupper : breadth ≤ rootBreadth) (hfar : 4 ≤ far) :
    receiver origin column breadth far (origin-6,column+breadth-1) ∧
    root origin column rootBreadth (origin-6,column+breadth-1) := by
  unfold receiver northAt root endpoint
  dsimp
  omega

theorem allowed_breadth (breadth rootBreadth : Int)
    (hbreadth : breadth % 2 = 0) (hroot : rootBreadth % 2 = 0)
    (havoids : ¬breadth ≤ rootBreadth) : rootBreadth+2 ≤ breadth := by
  omega

theorem receiver_avoids_root (origin column breadth far rootBreadth : Int) (point : Point)
    (hroot : 6 ≤ rootBreadth) (hbreadth : rootBreadth+2 ≤ breadth)
    (hpoint : receiver origin column breadth far point) :
    ¬root origin column rootBreadth point := by
  unfold receiver northAt endpoint at hpoint
  unfold root endpoint
  dsimp at hpoint ⊢
  omega

theorem receiver_avoids_parent (origin column breadth far oldWidth width depth : Int)
    (point : Point) (hbreadth : 6 ≤ breadth)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width)
    (hpoint : receiver origin column breadth far point) :
    ¬parentB origin column oldWidth width depth point := by
  unfold receiver northAt endpoint at hpoint
  unfold parentB northAt endpoint
  dsimp at hpoint ⊢
  omega

theorem bottom_three_owner_cells (origin column oldWidth breadth far : Int)
    (hold : 12 ≤ oldWidth) (hbreadth : 6 ≤ breadth) :
    oldP origin column oldWidth (origin-1,column-1) ∧
    oldP origin column oldWidth (origin,column-1) ∧
    receiver origin column breadth far (origin-1,column) ∧
    oldE origin column (origin,column) := by
  unfold oldP receiver northAt oldE endpoint
  dsimp
  omega

theorem original_receiver_charge (breadthHalf legHalf : Int) :
    (2*breadthHalf+legHalf-1)+(legHalf+4)-2*(breadthHalf+1+legHalf) = 1 := by
  omega

theorem parent_gain (oldWidth width : Int) :
    oldWidth+width+25+2*2-5 = oldWidth+width+24 := by
  omega

theorem receiver_marginal : (1 : Int)+2*4-8 = 1 := by decide

theorem omitting_bottom_tile_changes_sign : (1 : Int)+2*3-8 = -1 := by decide

theorem exact_joint_gain (oldWidth width : Int) :
    (oldWidth+width+25)+1+2*6-13 = oldWidth+width+25 := by
  omega

theorem joint_lower_bound (oldWidth width : Int)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) :
    49 ≤ oldWidth+width+25 := by
  omega

end SubQuorum.SecondaryTenRootDeepPair
