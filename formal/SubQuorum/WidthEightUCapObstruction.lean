import Std

set_option autoImplicit false
set_option maxRecDepth 1000000
set_option maxHeartbeats 10000000

namespace SubQuorum.WidthEightUCapObstruction

abbrev Point := Int × Int
abbrev Owner := Bool × Int × Int

def uEndpoint (width leftHeight rightHeight : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ leftHeight ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ rightHeight ∧ point.2 = width)

def uSupport (width leftHeight rightHeight : Int) (point : Point) : Prop :=
  (point.1 = 0 ∧ (point.2 = 0 ∨ point.2 = width+1)) ∨
  (2 ≤ point.1 ∧ point.1 ≤ leftHeight ∧ point.1 % 2 = 0 ∧ point.2 = 0) ∨
  (2 ≤ point.1 ∧ point.1 ≤ rightHeight ∧ point.1 % 2 = 0 ∧ point.2 = width+1) ∨
  (3 ≤ point.1 ∧ point.1 < leftHeight ∧ point.1 % 2 = 1 ∧ point.2 = 2) ∨
  (3 ≤ point.1 ∧ point.1 < rightHeight ∧ point.1 % 2 = 1 ∧ point.2 = width-1) ∨
  (point.1 = leftHeight+1 ∧ point.2 = 1) ∨
  (point.1 = rightHeight+1 ∧ point.2 = width)

def rootOffset (row column : Int) (transpose flipRow flipColumn : Bool) (offset : Point) : Point :=
  let first := if transpose then offset.2 else offset.1
  let second := if transpose then offset.1 else offset.2
  (row+(if flipRow then -first else first),
   column+(if flipColumn then -second else second))

theorem three_blockers_force_terminal
    (width leftHeight rightHeight row column : Int)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ leftHeight) (hright : 4 ≤ rightHeight)
    (hendpoint : uEndpoint width leftHeight rightHeight (row,column))
    (hblockedRight : ¬uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (0,1)))
    (hblockedDown : ¬uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (1,0)))
    (hblockedUp : ¬uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (-2,0))) :
    transpose = true ∧ flipRow = false ∧
      ((row = leftHeight ∧ column = 1) ∨ (row = rightHeight ∧ column = width)) := by
  unfold uEndpoint at hendpoint
  rcases hendpoint with ⟨hrow | hrow, hcolumn⟩ | ⟨hrow, hcolumn⟩ | ⟨hrow, hcolumn⟩ <;>
    cases transpose <;> cases flipRow <;> cases flipColumn <;>
    simp_all [uEndpoint, rootOffset] <;> omega

theorem three_blockers_force_left_ray
    (width leftHeight rightHeight row column distance : Int)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ leftHeight) (hright : 4 ≤ rightHeight)
    (hendpoint : uEndpoint width leftHeight rightHeight (row,column))
    (hblockedRight : ¬uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (0,1)))
    (hblockedDown : ¬uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (1,0)))
    (hblockedUp : ¬uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (-2,0)))
    (hlower : 1 ≤ distance) (hupper : distance ≤ 4) :
    uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (0,-distance)) := by
  obtain ⟨rfl, rfl, hterminal⟩ := three_blockers_force_terminal
    width leftHeight rightHeight row column transpose flipRow flipColumn
    hwidth hleft hright hendpoint hblockedRight hblockedDown hblockedUp
  rcases hterminal with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;>
    cases flipColumn <;> simp_all [uEndpoint, rootOffset] <;> omega

theorem five_blockers_force_upper_support
    (width leftHeight rightHeight row column : Int)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ leftHeight) (hright : 4 ≤ rightHeight)
    (hleftEven : leftHeight % 2 = 0) (hrightEven : rightHeight % 2 = 0)
    (hendpoint : uEndpoint width leftHeight rightHeight (row,column))
    (hblockedRight : ¬uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (0,1)))
    (hblockedDown : ¬uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (1,0)))
    (hblockedUp : ¬uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (-2,0)))
    (hblockedLeft : ¬uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (0,-6)))
    (hblockedCorner : ¬uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (-2,-4))) :
    uSupport width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (-1,0)) := by
  obtain ⟨rfl, rfl, hterminal⟩ := three_blockers_force_terminal
    width leftHeight rightHeight row column transpose flipRow flipColumn
    hwidth hleft hright hendpoint hblockedRight hblockedDown hblockedUp
  rcases hterminal with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;> cases flipColumn <;>
    simp_all [uEndpoint, uSupport, rootOffset] <;> omega

def corridorHit (width leftHeight rightHeight row column : Int)
    (transpose flipRow flipColumn : Bool) : Prop :=
  uEndpoint width leftHeight rightHeight (rootOffset row column transpose flipRow flipColumn (0,1)) ∨
  uEndpoint width leftHeight rightHeight (rootOffset row column transpose flipRow flipColumn (-1,0)) ∨
  uEndpoint width leftHeight rightHeight (rootOffset row column transpose flipRow flipColumn (1,0)) ∨
  uEndpoint width leftHeight rightHeight (rootOffset row column transpose flipRow flipColumn (0,-6)) ∨
  uEndpoint width leftHeight rightHeight (rootOffset row column transpose flipRow flipColumn (-1,-4)) ∨
  uEndpoint width leftHeight rightHeight (rootOffset row column transpose flipRow flipColumn (1,-4))

theorem every_u_endpoint_hits_corridor
    (width leftHeight rightHeight row column : Int)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ leftHeight) (hright : 4 ≤ rightHeight)
    (hendpoint : uEndpoint width leftHeight rightHeight (row,column)) :
    corridorHit width leftHeight rightHeight row column transpose flipRow flipColumn := by
  unfold uEndpoint at hendpoint
  rcases hendpoint with ⟨hrow | hrow, hcolumn⟩ | ⟨hrow, hcolumn⟩ | ⟨hrow, hcolumn⟩ <;>
    cases transpose <;> cases flipRow <;> cases flipColumn <;>
    simp_all [corridorHit, uEndpoint, rootOffset] <;> omega

theorem u_support_is_not_endpoint (width leftHeight rightHeight : Int) (point : Point)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ leftHeight) (hright : 4 ≤ rightHeight)
    (hsupport : uSupport width leftHeight rightHeight point) :
    ¬uEndpoint width leftHeight rightHeight point := by
  simp only [uSupport, uEndpoint] at *
  omega

def rotorP : List Point :=
  [(1,2),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(4,3)]

def rotorT : List Point :=
  [(0,2),(1,1),(2,5),(1,4),(5,3),(4,4),(3,0),(4,1)]

def uP : List Point :=
  [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),
   (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),
   (2,1),(3,1),(4,1),(2,8),(3,8),(4,8)]

def uT : List Point :=
  [(0,0),(2,0),(4,0),(0,9),(2,9),(4,9),(3,2),(3,7),(5,1),(5,8)]

def move (owner : Owner) (point : Point) : Point :=
  (point.1+owner.2.1,(if owner.1 then -point.2 else point.2)+owner.2.2)

def seedOwners : List Owner := [(false,0,0),(false,-3,0),(false,-1,-3)]

def seedP : List Point :=
  seedOwners.flatMap (fun owner => rotorP.map (move owner)) ++ uP.map (move (false,-4,-8))

def seedT : List Point :=
  seedOwners.flatMap (fun owner => rotorT.map (move owner)) ++ uT.map (move (false,-4,-8))

def neighbors (point : Point) : List Point :=
  [(point.1-1,point.2),(point.1+1,point.2),(point.1,point.2-1),(point.1,point.2+1)]

def ownersAt (target : Point) (blocked : List Point) : List Owner :=
  (([false,true].flatMap fun mirror => rotorP.map fun endpoint =>
    (mirror,target.1-endpoint.1,
      target.2-(if mirror then -endpoint.2 else endpoint.2))).filter fun owner =>
        (rotorP.map (move owner)).all fun point => !blocked.contains point)

theorem seed_endpoint_disjointness : seedP.length = 46 ∧ seedP.Nodup := by decide

theorem first_support_forcing :
    seedT.contains (-1,-1) = true ∧ seedP.contains (-1,-1) = false ∧
    2 ≤ ((neighbors (-1,-1)).filter seedP.contains).length := by decide

theorem five_root_blockers_present :
    [(-1,0),(0,-1),(-3,-1),(-1,-7),(-3,-5)].all seedP.contains = true := by decide

theorem first_rotor_owner : ownersAt (-1,-1) seedP = [(false,-3,-5)] := by decide

def rotorBranchP : List Point := seedP ++ rotorP.map (move (false,-3,-5))

theorem rotor_branch_endpoint_disjointness :
    rotorBranchP.length = 54 ∧ rotorBranchP.Nodup := by decide

theorem rotor_branch_second_support :
    (rotorT.map (move (false,-3,-5))).contains (-2,-1) = true ∧
    rotorBranchP.contains (-2,-1) = false ∧
    2 ≤ ((neighbors (-2,-1)).filter rotorBranchP.contains).length := by decide

theorem rotor_branch_no_rotor_owner : ownersAt (-2,-1) rotorBranchP = [] := by decide

theorem rotor_branch_four_site_barrier :
    [(-3,-1),(-2,0),(-2,-3),(2,-1)].all rotorBranchP.contains = true := by decide

def guaranteedUBranchP : List Point :=
  seedP ++ [(-1,-1),(-1,-2),(-1,-3),(-1,-4),(-1,-5)]

theorem u_branch_second_neighbors :
    guaranteedUBranchP.contains (-2,-1) = false ∧
    2 ≤ ((neighbors (-2,-1)).filter guaranteedUBranchP.contains).length := by decide

theorem u_branch_no_rotor_owner : ownersAt (-2,-1) guaranteedUBranchP = [] := by decide

theorem u_branch_corridor_barrier :
    [(-2,0),(-3,-1),(-1,-1),(-2,-7),(-3,-5),(-1,-5)].all
      guaranteedUBranchP.contains = true := by decide

end SubQuorum.WidthEightUCapObstruction
