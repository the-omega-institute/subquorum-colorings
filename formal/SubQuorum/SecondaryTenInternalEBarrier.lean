import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenInternalEBarrier

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def northAt (row column breadth incident far : Int) (left : Bool) (point : Point) : Prop :=
  endpoint breadth incident far
    (point.1-row+incident, if left then column+1-point.2 else point.2-column+1)

def earlierX (origin offset : Int) (point : Point) : Prop :=
  endpoint 6 4 4 (origin+2-point.1,offset+2-point.2)

def earlierV (origin column breadth depth : Int) (point : Point) : Prop :=
  endpoint breadth 8 depth (point.1-origin+depth,breadth+column+1-point.2)

theorem predecessor_column (offset currentOffset width : Int)
    (hrecurrence : currentOffset = offset-width-12) :
    currentOffset+width+13 = offset+1 := by omega

theorem predecessor_guard (origin offset row : Int)
    (hlower : origin-2 ≤ row) (hupper : row ≤ origin+2) :
    earlierX origin offset (row,offset+1) := by
  unfold earlierX endpoint
  dsimp
  omega

theorem predecessor_guard_recurrence (origin current depth row : Int)
    (hrecurrence : current = origin+depth-6) :
    (origin-2 ≤ row ∧ row ≤ origin+2) ↔
      (current-depth+4 ≤ row ∧ row ≤ current-depth+8) := by omega

theorem predecessor_collision (origin offset current depth breadth incident far : Int)
    (hrecurrence : current = origin+depth-6) (hdepth : 24 ≤ depth)
    (hbreadth : 6 ≤ breadth) (hincident : depth-9 ≤ incident) (left : Bool) :
    northAt (current-1) (offset+1) breadth incident far left (origin+2,offset+1) ∧
    earlierX origin offset (origin+2,offset+1) := by
  cases left <;> unfold northAt earlierX endpoint <;> dsimp <;> omega

theorem incident_upper_bound (origin offset current depth breadth incident far : Int)
    (hrecurrence : current = origin+depth-6) (hdepth : 24 ≤ depth)
    (hbreadth : 6 ≤ breadth) (hincident : incident % 2 = 0)
    (hdepthEven : depth % 2 = 0) (left : Bool)
    (hdisjoint : ∀ point, northAt (current-1) (offset+1) breadth incident far left point →
      earlierX origin offset point → False) : incident ≤ depth-10 := by
  apply Classical.byContradiction
  intro hfailure
  have hlower : depth-9 ≤ incident := by omega
  have hcollision := predecessor_collision origin offset current depth breadth incident far
    hrecurrence hdepth hbreadth hlower left
  exact hdisjoint (origin+2,offset+1) hcollision.1 hcollision.2

theorem right_bar_collision (origin column breadth incident far oldBreadth depth : Int)
    (hbreadth : 6 ≤ breadth) (hold : 6 ≤ oldBreadth)
    (hlower : 4 ≤ incident) (hupper : incident ≤ depth) :
    northAt (origin-1) column breadth incident far false (origin-incident,column+1) ∧
    earlierV origin column oldBreadth depth (origin-incident,column+1) := by
  unfold northAt earlierV endpoint
  dsimp
  omega

theorem internal_orientation (origin column breadth incident far oldBreadth depth : Int)
    (hbreadth : 6 ≤ breadth) (hold : 6 ≤ oldBreadth)
    (hlower : 4 ≤ incident) (hupper : incident ≤ depth-10) (left : Bool)
    (hdisjoint : ∀ point, northAt (origin-1) column breadth incident far left point →
      earlierV origin column oldBreadth depth point → False) : left = true := by
  cases left with
  | true => rfl
  | false =>
    have hcollision := right_bar_collision origin column breadth incident far oldBreadth depth
      hbreadth hold hlower (by omega)
    exact False.elim (hdisjoint (origin-incident,column+1) hcollision.1 hcollision.2)

theorem eleven_endpoint_footprint (origin column breadth incident far row : Int)
    (hbreadth : 6 ≤ breadth) (hincident : 10 ≤ incident)
    (hlower : origin-11 ≤ row) (hupper : row ≤ origin-1) (left : Bool) :
    northAt (origin-1) column breadth incident far left (row,column) := by
  cases left <;> unfold northAt endpoint <;> dsimp <;> omega

theorem refined_interval_gap (origin depth incident far : Int)
    (hdepth : depth % 2 = 0) (hincident : incident % 2 = 0) (hfar : 4 ≤ far)
    (havoids : ∀ row : Int,
      origin+depth-10-incident ≤ row → row ≤ origin+depth-10-incident+far →
      origin-11 ≤ row → row ≤ origin → False) :
    incident ≤ depth-12 ∨ depth+far+2 ≤ incident := by
  apply Classical.byContradiction
  intro hfailure
  have hstart : origin+depth-10-incident ≤ origin := by omega
  have hend : origin-11 ≤ origin+depth-10-incident+far := by omega
  by_cases hbefore : origin+depth-10-incident ≤ origin-11
  · exact havoids (origin-11) hbefore hend (by omega) (by omega)
  · exact havoids (origin+depth-10-incident) (by omega) (by omega) (by omega) hstart

theorem internal_first_deep_excluded (depth far : Int) (hfar : 4 ≤ far) :
    ¬ (depth+4 ≤ depth-12 ∨ depth+far+2 ≤ depth+4) := by omega

theorem internal_next_deep (depth incident far : Int)
    (hfar : 4 ≤ far) (hdeep : depth+far+2 ≤ incident) : depth+6 ≤ incident := by omega

theorem internal_next_far (depth far : Int)
    (hfar : 4 ≤ far) (hdeep : depth+far+2 ≤ depth+6) : far = 4 := by omega

theorem first_deep_shared_endpoint (origin depth far : Int) (hfar : 4 ≤ far) :
    origin+depth-10-(depth+4) ≤ origin-10 ∧
    origin-10 ≤ origin+depth-10-(depth+4)+far ∧
    origin-11 ≤ origin-10 ∧ origin-10 ≤ origin-1 := by omega

theorem internal_left_charge (breadthHalf legHalf : Int) :
    (2*breadthHalf+legHalf-1)+legHalf-2*(breadthHalf+legHalf) = -1 := by omega

def positiveCount : List Bool → Nat
  | [] => 0
  | left :: remaining => (if left then 0 else 1)+positiveCount remaining

theorem all_left_zero_positive (phases : List Bool)
    (hleft : ∀ phase ∈ phases, phase = true) : positiveCount phases = 0 := by
  induction phases with
  | nil => rfl
  | cons phase remaining inductionHypothesis =>
    have hphase : phase = true := hleft phase (by simp)
    have hremaining : ∀ candidate ∈ remaining, candidate = true := by
      intro candidate hmember
      exact hleft candidate (by simp [hmember])
    simp [positiveCount, hphase, inductionHypothesis hremaining]

theorem at_most_root_positive (root : Bool) (internal : List Bool)
    (hleft : ∀ phase ∈ internal, phase = true) : positiveCount (root :: internal) ≤ 1 := by
  have hzero := all_left_zero_positive internal hleft
  cases root <;> simp [positiveCount, hzero]

end SubQuorum.SecondaryTenInternalEBarrier
