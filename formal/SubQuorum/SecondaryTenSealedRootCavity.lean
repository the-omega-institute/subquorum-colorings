import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenSealedRootCavity

abbrev Point := Int × Int

def adjacent (first second : Point) : Prop :=
  (first.1 = second.1 ∧ (first.2+1 = second.2 ∨ second.2+1 = first.2)) ∨
  (first.2 = second.2 ∧ (first.1+1 = second.1 ∨ second.1+1 = first.1))

def inside (top bottom left right : Int) (point : Point) : Prop :=
  top ≤ point.1 ∧ point.1 ≤ bottom ∧ left ≤ point.2 ∧ point.2 ≤ right

def boundary (top bottom left right : Int) (point : Point) : Prop :=
  ((point.1 = top-1 ∨ point.1 = bottom+1) ∧ left ≤ point.2 ∧ point.2 ≤ right) ∨
  ((point.2 = left-1 ∨ point.2 = right+1) ∧ top ≤ point.1 ∧ point.1 ≤ bottom)

inductive Walk (allowed : Point → Prop) (start : Point) : Point → Prop where
  | refl (hallowed : allowed start) : Walk allowed start start
  | step {current next : Point} (path : Walk allowed start current)
      (hadjacent : adjacent current next) (hallowed : allowed next) : Walk allowed start next

theorem step_confined (top bottom left right : Int) (first second : Point)
    (hfirst : inside top bottom left right first) (hadjacent : adjacent first second)
    (hboundary : ¬boundary top bottom left right second) :
    inside top bottom left right second := by
  unfold inside adjacent boundary at *
  omega

theorem walk_confined (top bottom left right : Int) (allowed : Point → Prop)
    (start finish : Point) (hstart : inside top bottom left right start)
    (hwalls : ∀ point, boundary top bottom left right point → ¬allowed point)
    (path : Walk allowed start finish) : inside top bottom left right finish := by
  induction path with
  | refl hallowed => exact hstart
  | @step current next path hadjacent hallowed inductionHypothesis =>
    apply step_confined top bottom left right current next inductionHypothesis hadjacent
    intro hboundary
    exact hwalls next hboundary hallowed

theorem no_narrow_connected_owner (top bottom left right : Int) (owner : Point → Prop)
    (start first second : Point) (hstart : inside top bottom left right start)
    (hwalls : ∀ point, boundary top bottom left right point → ¬owner point)
    (hconnected : ∀ point, owner point → Walk owner start point)
    (hfirst : owner first) (hsecond : owner second)
    (hspan : 3 ≤ second.2-first.2) (hnarrow : right-left ≤ 2) : False := by
  have hfirstInside := walk_confined top bottom left right owner start first hstart hwalls
    (hconnected first hfirst)
  have hsecondInside := walk_confined top bottom left right owner start second hstart hwalls
    (hconnected second hsecond)
  unfold inside at hfirstInside hsecondInside
  omega

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def transformedColumn (offset : Int) (transpose reflectColumn : Bool) (point : Point) : Int :=
  offset + if reflectColumn then -(if transpose then point.1 else point.2)
    else (if transpose then point.1 else point.2)

theorem full_U_projection (breadth near far offset : Int) (transpose reflectColumn : Bool)
    (hbreadth : 6 ≤ breadth) (hnear : 4 ≤ near) :
    ∃ first second : Point, endpoint breadth near far first ∧ endpoint breadth near far second ∧
      4 ≤ transformedColumn offset transpose reflectColumn second-
        transformedColumn offset transpose reflectColumn first := by
  cases transpose <;> cases reflectColumn
  · refine ⟨(0,1),(0,breadth),?_,?_,?_⟩
    all_goals dsimp [endpoint, transformedColumn]; omega
  · refine ⟨(0,breadth),(0,1),?_,?_,?_⟩
    all_goals dsimp [endpoint, transformedColumn]; omega
  · refine ⟨(0,1),(near,1),?_,?_,?_⟩
    all_goals dsimp [endpoint, transformedColumn]; omega
  · refine ⟨(near,1),(0,1),?_,?_,?_⟩
    all_goals dsimp [endpoint, transformedColumn]; omega

def rotorEndpoint (point : Point) : Prop :=
  point = (1,2) ∨ point = (2,2) ∨ point = (2,3) ∨ point = (2,4) ∨
  point = (3,1) ∨ point = (3,2) ∨ point = (3,3) ∨ point = (4,3)

theorem rotor_projection (offset : Int) (transpose reflectColumn : Bool) :
    ∃ first second : Point, rotorEndpoint first ∧ rotorEndpoint second ∧
      3 ≤ transformedColumn offset transpose reflectColumn second-
        transformedColumn offset transpose reflectColumn first := by
  cases transpose <;> cases reflectColumn
  · refine ⟨(3,1),(2,4),by simp [rotorEndpoint],by simp [rotorEndpoint],?_⟩
    unfold transformedColumn
    dsimp
    omega
  · refine ⟨(2,4),(3,1),by simp [rotorEndpoint],by simp [rotorEndpoint],?_⟩
    unfold transformedColumn
    dsimp
    omega
  · refine ⟨(1,2),(4,3),by simp [rotorEndpoint],by simp [rotorEndpoint],?_⟩
    unfold transformedColumn
    dsimp
    omega
  · refine ⟨(4,3),(1,2),by simp [rotorEndpoint],by simp [rotorEndpoint],?_⟩
    unfold transformedColumn
    dsimp
    omega

def parent (origin offset oldWidth width depth : Int) (point : Point) : Prop :=
  endpoint (oldWidth+width+26) (depth+4) 4
    (point.1-origin+14,point.2-offset+width+13)

def horizontal (origin offset oldWidth index height incident far : Int) (point : Point) : Prop :=
  endpoint height incident far
    (point.2-offset-oldWidth-12+incident,point.1-origin+10+index)

def nextP (origin offset width depth : Int) (point : Point) : Prop :=
  endpoint (width+12) 10 4 (point.1-origin-depth+14,offset+1-point.2)

theorem parent_top_wall (origin offset oldWidth width depth incident column : Int)
    (hincident : 4 ≤ incident)
    (hcolumn : offset-width-11 ≤ column ∧ column ≤ offset+oldWidth+11-incident) :
    parent origin offset oldWidth width depth (origin-13,column) := by
  unfold parent endpoint
  dsimp
  omega

theorem parent_left_wall (origin offset oldWidth width depth row : Int)
    (hrow : origin-12 ≤ row ∧ row ≤ origin+depth-15) :
    parent origin offset oldWidth width depth (row,offset-width-12) := by
  unfold parent endpoint
  dsimp
  omega

theorem third_right_wall (origin offset oldWidth depth incident far row : Int)
    (hrow : origin-12 ≤ row ∧ row ≤ origin+depth-15) :
    horizontal origin offset oldWidth 3 (depth-2) incident far
      (row,offset+oldWidth+12-incident) := by
  unfold horizontal endpoint
  dsimp
  omega

theorem nextP_bottom_wall (origin offset width depth column : Int)
    (hcolumn : offset-width-11 ≤ column ∧ column ≤ offset) :
    nextP origin offset width depth (origin+depth-14,column) := by
  unfold nextP endpoint
  dsimp
  omega

theorem mandatory_support_phase (depth : Int) (hdepth : 24 ≤ depth) (heven : depth % 2 = 0) :
    2 ≤ depth-1 ∧ depth-1 ≤ depth+4 ∧ (depth-1)%2 = 1 := by
  omega

theorem cavity_width (oldWidth width incident : Int) :
    (oldWidth+12-incident)-(-width-12)-1 = oldWidth+width+23-incident := by
  omega

theorem narrow_depth_frontier (oldWidth width incident : Int)
    (heven : incident%2 = 0) (hold : oldWidth%2 = 0) (hwidth : width%2 = 0)
    (hroom : 4 ≤ oldWidth+width+23-incident) :
    incident ≤ oldWidth+width+18 := by
  omega

theorem third_bottom_gain (oldWidth width breadth incident gain : Int)
    (hfrontier : incident ≤ oldWidth+width+18)
    (hledger : oldWidth+width+breadth/2+25-incident ≤ gain) :
    breadth/2+7 ≤ gain := by
  omega

theorem first_bottom_gain (oldWidth width breadth firstDepth lastDepth far eta gain : Int)
    (hold : oldWidth%2 = 0) (hdepth : lastDepth%2 = 0)
    (hwall : lastDepth ≤ oldWidth+width+22) (hgap : firstDepth+4 ≤ lastDepth)
    (hfar : far ≤ firstDepth-oldWidth-12) (hreceipts : -(far/2)-1 ≤ eta)
    (hledger : gain = oldWidth/2+width+breadth/2+22-lastDepth/2+eta) :
    breadth/2+7 ≤ gain := by
  omega

theorem first_bottom_stronger_gain (oldWidth width breadth firstDepth lastDepth far eta gain : Int)
    (hold : oldWidth%2 = 0) (hdepth : lastDepth%2 = 0)
    (hwall : lastDepth ≤ oldWidth+width+22) (hgap : firstDepth+8 ≤ lastDepth)
    (hfar : far ≤ firstDepth-oldWidth-12) (hreceipts : -(far/2)-1 ≤ eta)
    (hledger : gain = oldWidth/2+width+breadth/2+22-lastDepth/2+eta) :
    breadth/2+9 ≤ gain := by
  omega

theorem no_bottom_gain (oldWidth width breadth lastDepth eta gain : Int)
    (hold : oldWidth%2 = 0) (hdepth : lastDepth%2 = 0)
    (hwall : lastDepth ≤ oldWidth+width+22) (hwidth : 12 ≤ width) (hreceipts : -3 ≤ eta)
    (hledger : gain = oldWidth/2+width+breadth/2+22-lastDepth/2+eta) :
    breadth/2+14 ≤ gain := by
  omega

theorem complete_prefix_ge_ten (breadth gain : Int)
    (hbreadth : 6 ≤ breadth) (hbound : breadth/2+7 ≤ gain) : 10 ≤ gain := by
  omega

end SubQuorum.SecondaryTenSealedRootCavity
