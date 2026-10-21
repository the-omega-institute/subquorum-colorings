import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenMandatoryEFootprint

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def northAt (row column breadth incident far : Int) (left : Bool) (point : Point) : Prop :=
  endpoint breadth incident far
    (point.1-row+incident, if left then column+1-point.2 else point.2-column+1)

def oldP (origin column oldWidth : Int) (point : Point) : Prop :=
  endpoint (oldWidth+12) 10 4 (point.1-origin+8,column-point.2)

def rootEast (origin column breadth : Int) (point : Point) : Prop :=
  endpoint breadth 6 4 (point.1-origin+6,point.2-column)

def earlierEast (origin column breadth depth : Int) (point : Point) : Prop :=
  endpoint breadth 8 depth (point.1-origin+depth,breadth+column+1-point.2)

theorem left_shallow_collision (origin column breadth incident far oldWidth : Int)
    (hbreadth : 6 ≤ breadth) (hold : 12 ≤ oldWidth)
    (hincident : incident = 4 ∨ incident = 6 ∨ incident = 8) :
    northAt (origin-1) column breadth incident far true (origin-incident,column-1) ∧
    oldP origin column oldWidth (origin-incident,column-1) := by
  unfold northAt oldP endpoint
  dsimp
  omega

theorem root_right_shallow_collision (origin column breadth incident far rootBreadth : Int)
    (hbreadth : 6 ≤ breadth) (hroot : 6 ≤ rootBreadth)
    (hincident : incident = 4 ∨ incident = 6) :
    northAt (origin-1) column breadth incident far false (origin-incident,column+1) ∧
    rootEast origin column rootBreadth (origin-incident,column+1) := by
  unfold northAt rootEast endpoint
  dsimp
  omega

theorem earlier_right_collision (origin column breadth incident far oldBreadth depth : Int)
    (hbreadth : 6 ≤ breadth) (hold : 6 ≤ oldBreadth)
    (hlower : 4 ≤ incident) (hupper : incident ≤ depth) :
    northAt (origin-1) column breadth incident far false (origin-incident,column+1) ∧
    earlierEast origin column oldBreadth depth (origin-incident,column+1) := by
  unfold northAt earlierEast endpoint
  dsimp
  omega

theorem incident_lower_bound (incident : Int)
    (hlower : 4 ≤ incident) (heven : incident % 2 = 0)
    (hfour : incident ≠ 4) (hsix : incident ≠ 6) : 8 ≤ incident := by
  omega

theorem left_incident_lower_bound (incident : Int)
    (hlower : 4 ≤ incident) (heven : incident % 2 = 0)
    (hfour : incident ≠ 4) (hsix : incident ≠ 6) (height : incident ≠ 8) :
    10 ≤ incident := by
  omega

theorem earlier_incident_lower_bound (incident depth : Int)
    (hincident : incident % 2 = 0) (hdepth : depth % 2 = 0)
    (havoids : ¬incident ≤ depth) : depth+2 ≤ incident := by
  omega

theorem nine_endpoint_footprint (origin column breadth incident far row : Int)
    (hbreadth : 6 ≤ breadth) (hincident : 8 ≤ incident)
    (hlower : origin-9 ≤ row) (hupper : row ≤ origin-1) (left : Bool) :
    northAt (origin-1) column breadth incident far left (row,column) := by
  cases left <;> unfold northAt endpoint <;> dsimp <;> omega

theorem rotor_left_collision (origin column : Int) :
    ((origin-1)+(-1),column+(-1)) = (origin-2,column-1) := by
  apply Prod.ext <;> dsimp <;> omega

theorem rotor_right_collision (origin column : Int) :
    ((origin-1)+(-1),column+1) = (origin-2,column+1) := by
  apply Prod.ext <;> dsimp <;> omega

theorem old_west_blocker (origin column oldWidth : Int) (hold : 12 ≤ oldWidth) :
    oldP origin column oldWidth (origin-2,column-1) ∧
    oldP origin column oldWidth (origin-1,column-1) := by
  unfold oldP endpoint
  dsimp
  omega

theorem root_east_blocker (origin column breadth : Int) (hbreadth : 6 ≤ breadth) :
    rootEast origin column breadth (origin-2,column+1) ∧
    rootEast origin column breadth (origin-1,column+1) := by
  unfold rootEast endpoint
  dsimp
  omega

theorem earlier_east_blocker (origin column breadth depth : Int)
    (hdepth : 24 ≤ depth) :
    earlierEast origin column breadth depth (origin-2,column+1) ∧
    earlierEast origin column breadth depth (origin-1,column+1) := by
  unfold earlierEast endpoint
  dsimp
  omega

theorem recent_bands_hit_footprint (origin offset oldWidth width depth far raised : Int)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) (hfar : 4 ≤ far)
    (hraised : raised = 0 ∨ raised = 2) :
    northAt (origin+depth-10) (offset-width-12) (oldWidth+width+26)
      (depth+raised) far false (origin-8,offset+oldWidth+13) := by
  unfold northAt endpoint
  dsimp
  omega

theorem arbitrary_interval_necessary_condition (origin depth incident far : Int)
    (hdepth : depth % 2 = 0) (hincident : incident % 2 = 0)
    (hfar : 4 ≤ far)
    (havoids : ∀ row : Int,
      origin+depth-10-incident ≤ row → row ≤ origin+depth-10-incident+far →
      origin-9 ≤ row → row ≤ origin → False) :
    incident ≤ depth-12 ∨ depth+far ≤ incident := by
  apply Classical.byContradiction
  intro hfailure
  have hstart : origin+depth-10-incident ≤ origin := by omega
  have hend : origin-9 ≤ origin+depth-10-incident+far := by omega
  by_cases hbefore : origin+depth-10-incident ≤ origin-9
  · exact havoids (origin-9) hbefore hend (by omega) (by omega)
  · exact havoids (origin+depth-10-incident) (by omega) (by omega) (by omega) hstart

theorem first_deep_phase (depth incident far : Int)
    (hfar : 4 ≤ far) (hdeep : depth+far ≤ incident) : depth+4 ≤ incident := by
  omega

theorem first_deep_far (depth far : Int)
    (hfar : 4 ≤ far) (hdeep : depth+far ≤ depth+4) : far = 4 := by
  omega

theorem current_support_color (origin offset : Int)
    (horigin : origin % 2 = 1) (hoffset : offset % 2 = 0) :
    (origin-4+offset) % 2 = 1 := by
  omega

theorem E_support_color (origin offset width : Int)
    (horigin : origin % 2 = 1) (hoffset : offset % 2 = 0) (hwidth : width % 2 = 0) :
    (origin-1+(offset+width+13)) % 2 = 1 := by
  omega

theorem canonical_terminals_opposite (breadth incident far : Int)
    (hbreadth : breadth % 2 = 0) (hincident : incident % 2 = 0)
    (hfar : far % 2 = 0) : (incident+1) % 2 ≠ (far+breadth) % 2 := by
  omega

theorem left_original_charge (breadthHalf legHalf : Int) :
    (2*breadthHalf+legHalf-1)+legHalf-2*(breadthHalf+legHalf) = -1 := by
  omega

theorem right_original_charge (breadthHalf legHalf : Int) :
    (2*breadthHalf+legHalf-1)+(legHalf+4)-2*(breadthHalf+1+legHalf) = 1 := by
  omega

def originalValue (charge : Int) : Int :=
  (if 0 < charge then 1 else 0)+max 0 (-charge)

theorem each_E_owner_value (left : Bool) :
    originalValue (if left then -1 else 1) = 1 := by
  cases left <;> decide

def terminalMass : List Int → Int
  | [] => 0
  | breadth :: remaining => breadth-1+terminalMass remaining

def ownerValue : List Int → Int
  | [] => 0
  | breadth :: remaining => breadth+ownerValue remaining

def breadthsValid : List Int → Prop
  | [] => True
  | breadth :: remaining => 6 ≤ breadth ∧ breadthsValid remaining

theorem immutable_owner_inventory (breadths : List Int) :
    ownerValue breadths = terminalMass breadths+(breadths.length : Int) := by
  induction breadths with
  | nil => simp [ownerValue, terminalMass]
  | cons breadth remaining inductionHypothesis =>
    simp only [ownerValue, terminalMass, List.length_cons]
    omega

theorem immutable_owner_lower_bound (breadths : List Int) (hvalid : breadthsValid breadths) :
    6*(breadths.length : Int) ≤ ownerValue breadths := by
  induction breadths with
  | nil => simp [ownerValue]
  | cons breadth remaining inductionHypothesis =>
    simp only [breadthsValid] at hvalid
    have hremaining := inductionHypothesis hvalid.2
    simp only [ownerValue, List.length_cons]
    omega

end SubQuorum.SecondaryTenMandatoryEFootprint
