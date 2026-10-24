import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenRootCavityExclusion

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def guard (width : Int) (point : Point) : Prop :=
  (point.1 = -1 ∧ 0 ≤ point.2 ∧ point.2 ≤ width) ∨
  (point.1 = 0 ∧ point.2 = width) ∨
  (point.1 = 4 ∧ 0 ≤ point.2 ∧ point.2 < width) ∨
  (point.2 = -1 ∧ 0 ≤ point.1 ∧ point.1 ≤ 2)

def eastTerminal (breadth incident far : Int) (south : Bool) (point : Point) : Prop :=
  endpoint breadth incident far
    (incident-point.2,if south then point.1+1 else 1-point.1)

def southTerminal (breadth incident far : Int) (left : Bool) (point : Point) : Prop :=
  endpoint breadth incident far
    (incident-point.1,if left then 1-point.2 else point.2+1)

def outerCorner (breadth incident far : Int) (transpose : Bool) (point : Point) : Prop :=
  endpoint breadth incident far
    (if transpose then (point.2,point.1+1) else (point.1,point.2+1))

def parent (origin offset oldWidth width depth : Int) (point : Point) : Prop :=
  endpoint (oldWidth+width+26) (depth+4) 4
    (point.1-origin+14,point.2-offset+width+13)

def oldP (origin offset width : Int) (point : Point) : Prop :=
  endpoint (width+12) 10 4 (point.1-origin+8,offset+width+13-point.2)

def consumer (origin offset breadth far : Int) (point : Point) : Prop :=
  endpoint breadth 8 far (point.1-origin+12,offset+1-point.2)

def blockedAt (origin offset width : Int) (point : Point) : Prop :=
  guard (width+12) (point.1-origin+12,point.2-offset-1)

theorem south_terminal_collision (breadth incident far width : Int) (left : Bool)
    (hbreadth : 6 ≤ breadth) (hincident : 4 ≤ incident) (hwidth : 3 ≤ width) :
    southTerminal breadth incident far left (4,0) ∧ guard width (4,0) := by
  cases left <;> unfold southTerminal endpoint guard <;> dsimp <;> omega

theorem corner_collision (breadth incident far width : Int) (transpose : Bool)
    (hbreadth : 6 ≤ breadth) (hincident : 4 ≤ incident) (hwidth : 3 ≤ width) :
    outerCorner breadth incident far transpose (4,0) ∧ guard width (4,0) := by
  cases transpose <;> unfold outerCorner endpoint guard <;> dsimp <;> omega

theorem east_long_collision (breadth incident far width : Int) (south : Bool)
    (hbreadth : 6 ≤ breadth) (hwidth : 3 ≤ width) (hlong : width ≤ incident) :
    eastTerminal breadth incident far south (0,width) ∧ guard width (0,width) := by
  cases south <;> unfold eastTerminal endpoint guard <;> dsimp <;> omega

theorem east_short_north_collision (breadth incident far width : Int)
    (hbreadth : 6 ≤ breadth) (hincident : 4 ≤ incident) (hshort : incident < width) :
    eastTerminal breadth incident far false (-1,incident) ∧ guard width (-1,incident) := by
  unfold eastTerminal endpoint guard
  dsimp
  omega

theorem east_short_south_collision (breadth incident far width : Int)
    (hbreadth : 6 ≤ breadth) (hincident : 4 ≤ incident) (hshort : incident < width) :
    eastTerminal breadth incident far true (4,incident) ∧ guard width (4,incident) := by
  unfold eastTerminal endpoint guard
  dsimp
  omega

theorem every_east_terminal_collision (breadth incident far width : Int) (south : Bool)
    (hbreadth : 6 ≤ breadth) (hincident : 4 ≤ incident) (hwidth : 3 ≤ width) :
    ∃ point, eastTerminal breadth incident far south point ∧ guard width point := by
  by_cases hlong : width ≤ incident
  · exact ⟨(0,width), east_long_collision breadth incident far width south hbreadth hwidth hlong⟩
  · have hshort : incident < width := by omega
    cases south
    · exact ⟨(-1,incident), east_short_north_collision breadth incident far width hbreadth hincident hshort⟩
    · exact ⟨(4,incident), east_short_south_collision breadth incident far width hbreadth hincident hshort⟩

def rotorSouthOne : List Point :=
  [(0,0),(1,0),(1,1),(1,2),(2,-1),(2,0),(2,1),(3,1)]

def rotorEastOne : List Point :=
  [(-2,1),(-1,1),(-1,2),(-1,3),(0,0),(0,1),(0,2),(1,2)]

def rotorSouthTwo : List Point :=
  [(0,0),(1,-2),(1,-1),(1,0),(2,-1),(2,0),(2,1),(3,-1)]

def rotorEastTwo : List Point :=
  [(-1,2),(0,0),(0,1),(0,2),(1,1),(1,2),(1,3),(2,1)]

theorem rotor_south_one_collision (width : Int) :
    (2,-1) ∈ rotorSouthOne ∧ guard width (2,-1) := by
  constructor
  · decide
  · unfold guard
    dsimp
    omega

theorem rotor_east_one_collision (width : Int) (hwidth : 3 ≤ width) :
    (-1,1) ∈ rotorEastOne ∧ guard width (-1,1) := by
  constructor
  · decide
  · unfold guard
    dsimp
    omega

theorem rotor_south_two_collision (width : Int) :
    (1,-1) ∈ rotorSouthTwo ∧ guard width (1,-1) := by
  constructor
  · decide
  · unfold guard
    dsimp
    omega

theorem rotor_east_two_collision (width : Int) (hwidth : 3 ≤ width) :
    (-1,2) ∈ rotorEastTwo ∧ guard width (-1,2) := by
  constructor
  · decide
  · unfold guard
    dsimp
    omega

theorem all_guards_are_retained (origin offset oldWidth width depth breadth far : Int)
    (point : Point) (hwidth : 12 ≤ width) (hbreadth : 6 ≤ breadth)
    (hguard : blockedAt origin offset oldWidth point) :
    parent origin offset oldWidth width depth point ∨
    oldP origin offset oldWidth point ∨ consumer origin offset breadth far point := by
  unfold blockedAt guard at hguard
  dsimp at hguard
  rcases hguard with hnorth | heast | hsouth | hwest
  · left
    unfold parent endpoint
    dsimp
    omega
  · left
    unfold parent endpoint
    dsimp
    omega
  · right
    left
    unfold oldP endpoint
    dsimp
    omega
  · right
    right
    unfold consumer endpoint
    dsimp
    omega

theorem missing_point_avoids_parent (origin offset oldWidth width depth : Int)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) :
    ¬parent origin offset oldWidth width depth (origin-12,offset+1) := by
  unfold parent endpoint
  dsimp
  omega

theorem missing_point_avoids_oldP (origin offset oldWidth : Int) :
    ¬oldP origin offset oldWidth (origin-12,offset+1) := by
  unfold oldP endpoint
  dsimp
  omega

theorem missing_point_avoids_consumer (origin offset breadth far : Int) :
    ¬consumer origin offset breadth far (origin-12,offset+1) := by
  unfold consumer endpoint
  dsimp
  omega

theorem two_foreign_neighbors (origin offset oldWidth width depth breadth far : Int)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) (hbreadth : 6 ≤ breadth) :
    parent origin offset oldWidth width depth (origin-13,offset+1) ∧
    consumer origin offset breadth far (origin-12,offset) := by
  unfold parent consumer endpoint
  dsimp
  omega

theorem surviving_marginal_lower_bound (breadth width tight : Int)
    (hbreadth : 6 ≤ breadth) (hwidth : 12 ≤ width)
    (htight : tight = 0 ∨ (tight = 1 ∧ breadth = width+12)) :
    5 ≤ breadth-1-tight := by
  omega

theorem stronger_joint_lower_bound (oldWidth width breadth tight : Int)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) (hbreadth : 6 ≤ breadth)
    (htight : tight = 0 ∨ (tight = 1 ∧ breadth = width+12)) :
    54 ≤ oldWidth+width+breadth+24-tight := by
  omega

theorem conditional_improvement : (54 : Int)-46 = 8 := by decide

def shallowConsumer (origin offset breadth incident far : Int) (point : Point) : Prop :=
  endpoint breadth incident far
    (point.1-origin+4+incident,offset+1-point.2)

def receiver (origin offset oldWidth breadth far : Int) (point : Point) : Prop :=
  endpoint breadth 8 far (point.1-origin+9,point.2-offset-oldWidth-12)

def reflectedBlockedAt (origin offset oldWidth width : Int) (point : Point) : Prop :=
  guard width (origin-9-point.1,offset+oldWidth+12-point.2)

theorem reflected_six_guards_retained (origin offset oldWidth width depth breadth far receiverBreadth receiverFar : Int)
    (point : Point) (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width)
    (hbreadth : 6 ≤ breadth) (hreceiver : 6 ≤ receiverBreadth)
    (hguard : reflectedBlockedAt origin offset oldWidth (oldWidth+12) point) :
    parent origin offset oldWidth width depth point ∨ oldP origin offset oldWidth point ∨
    shallowConsumer origin offset breadth 6 far point ∨
    receiver origin offset oldWidth receiverBreadth receiverFar point := by
  unfold reflectedBlockedAt guard at hguard
  dsimp at hguard
  rcases hguard with hnorth | heast | hsouth | hwest
  · by_cases hcolumn : point.2 = offset
    · right
      right
      left
      unfold shallowConsumer endpoint
      dsimp
      omega
    · right
      left
      unfold oldP endpoint
      dsimp
      omega
  · right
    right
    left
    unfold shallowConsumer endpoint
    dsimp
    omega
  · left
    unfold parent endpoint
    dsimp
    omega
  · by_cases hrow : point.1 = origin-9
    · right
      right
      right
      unfold receiver endpoint
      dsimp
      omega
    · left
      unfold parent endpoint
      dsimp
      omega

theorem reflected_tight_four_guards_retained (origin offset oldWidth width depth far receiverBreadth receiverFar : Int)
    (point : Point) (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) (hdepth : 24 ≤ depth)
    (hreceiver : 6 ≤ receiverBreadth)
    (hguard : reflectedBlockedAt origin offset oldWidth (oldWidth+width+24) point) :
    parent origin offset oldWidth width depth point ∨ oldP origin offset oldWidth point ∨
    shallowConsumer origin offset (width+12) 4 far point ∨
    receiver origin offset oldWidth receiverBreadth receiverFar point := by
  unfold reflectedBlockedAt guard at hguard
  dsimp at hguard
  rcases hguard with hnorth | heast | hsouth | hwest
  · by_cases hcolumn : point.2 = offset-width-12
    · left
      unfold parent endpoint
      dsimp
      omega
    · by_cases hleft : point.2 ≤ offset
      · right
        right
        left
        unfold shallowConsumer endpoint
        dsimp
        omega
      · right
        left
        unfold oldP endpoint
        dsimp
        omega
  · left
    unfold parent endpoint
    dsimp
    omega
  · left
    unfold parent endpoint
    dsimp
    omega
  · by_cases hrow : point.1 = origin-9
    · right
      right
      right
      unfold receiver endpoint
      dsimp
      omega
    · left
      unfold parent endpoint
      dsimp
      omega

theorem receiver_support_two_foreign_neighbors (origin offset oldWidth breadth far : Int)
    (hold : 12 ≤ oldWidth) (hbreadth : 6 ≤ breadth) :
    receiver origin offset oldWidth breadth far (origin-9,offset+oldWidth+13) ∧
    oldP origin offset oldWidth (origin-8,offset+oldWidth+12) := by
  unfold receiver oldP endpoint
  dsimp
  omega

theorem receiver_support_avoids_new_owners (origin offset oldWidth width depth breadth incident far receiverBreadth receiverFar : Int)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) (hbreadth : 6 ≤ breadth) :
    ¬parent origin offset oldWidth width depth (origin-9,offset+oldWidth+12) ∧
    ¬shallowConsumer origin offset breadth incident far (origin-9,offset+oldWidth+12) ∧
    ¬receiver origin offset oldWidth receiverBreadth receiverFar (origin-9,offset+oldWidth+12) := by
  unfold parent shallowConsumer receiver endpoint
  dsimp
  omega

theorem remaining_width_bound (breadth width : Int)
    (hbreadth : breadth % 2 = 0) (hwidth : width % 2 = 0)
    (hupper : breadth ≤ width+12) (hnontight : breadth ≠ width+12) :
    breadth ≤ width+10 := by
  omega

end SubQuorum.SecondaryTenRootCavityExclusion
