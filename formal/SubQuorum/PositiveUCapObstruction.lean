import Std

set_option autoImplicit false
set_option maxRecDepth 1000000
set_option maxHeartbeats 10000000

namespace SubQuorum.PositiveUCapObstruction

abbrev Point := Int × Int
abbrev Owner := Bool × Int × Int

def rotorP : List Point :=
  [(1,2),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(4,3)]

def rotorT : List Point :=
  [(0,2),(1,1),(2,5),(1,4),(5,3),(4,4),(3,0),(4,1)]

def uP : List Point :=
  [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
   (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),
   (2,1),(3,1),(4,1),(2,6),(3,6),(4,6)]

def uT : List Point :=
  [(0,0),(2,0),(4,0),(0,7),(2,7),(4,7),(3,2),(3,5),(5,1),(5,6)]

def move (owner : Owner) (point : Point) : Point :=
  (point.1+owner.2.1,(if owner.1 then -point.2 else point.2)+owner.2.2)

def seedOwners : List Owner := [(false,0,0),(false,-3,0),(false,-1,-3)]

def seedP : List Point :=
  seedOwners.flatMap (fun owner => rotorP.map (move owner)) ++ uP.map (move (false,-4,-6))

def seedT : List Point :=
  seedOwners.flatMap (fun owner => rotorT.map (move owner)) ++ uT.map (move (false,-4,-6))

def neighbors (point : Point) : List Point :=
  [(point.1-1,point.2),(point.1+1,point.2),(point.1,point.2-1),(point.1,point.2+1)]

def blocking : List Point := [(-1,0),(0,-1),(-3,-1),(-1,-5)]

def firstForced : Point := (-1,-1)

def forced (point : Point) (originalP originalT : List Point) : Bool :=
  originalT.contains point && !originalP.contains point &&
  decide (2 ≤ ((neighbors point).filter originalP.contains).length)

theorem seed_endpoint_disjointness : seedP.length = 42 ∧ seedP.Nodup := by decide

theorem first_support_forcing : forced firstForced seedP seedT = true := by decide

theorem u_barrier_is_present : blocking.all seedP.contains = true := by decide

theorem every_three_neighbors_hit_barrier :
    [[(-2,-1),(-1,0),(0,-1)],[(-2,-1),(-1,0),(-1,-2)],
     [(-2,-1),(0,-1),(-1,-2)],[(-1,0),(0,-1),(-1,-2)]].all
      (fun triple => triple.any blocking.contains) = true := by decide

theorem opposite_neighbors_hit_barrier :
    [[(-2,-1),(0,-1)],[(-1,-2),(-1,0)]].all
      (fun pair => pair.any blocking.contains) = true := by decide

theorem four_step_rays_hit_barrier :
    [(-1,0),(0,1),(1,0),(0,-1)].all (fun direction =>
      [1,2,3,4].any fun distance =>
        blocking.contains (firstForced.1+distance*direction.1,
                           firstForced.2+distance*direction.2)) = true := by decide

def rotorOwners : List Owner :=
  (([false,true].flatMap fun mirror => rotorP.map fun endpoint =>
    (mirror,firstForced.1-endpoint.1,
      firstForced.2-(if mirror then -endpoint.2 else endpoint.2))).filter fun owner =>
        (rotorP.map (move owner)).all fun point => !seedP.contains point)

theorem unique_rotor_owner : rotorOwners = [(false,-3,-5)] := by decide

def extendedP : List Point := seedP ++ rotorP.map (move (false,-3,-5))

def extendedT : List Point := seedT ++ rotorT.map (move (false,-3,-5))

def cavity : List Point := [(-2,-4),(-1,-4)]

theorem forced_rotor_disjointness : extendedP.length = 50 ∧ extendedP.Nodup := by decide

theorem second_support_forcing : forced (-2,-4) extendedP extendedT = true := by decide

theorem cavity_is_free_and_closed :
    cavity.length = 2 ∧ cavity.Nodup ∧
    cavity.all (fun point => !extendedP.contains point) = true ∧
    cavity.all (fun point => (neighbors point).all fun other =>
      extendedP.contains other || cavity.contains other) = true := by decide

inductive FreeReach (blocked : List Point) (start : Point) : Point → Prop where
  | base : FreeReach blocked start start
  | advance {current next : Point} :
      FreeReach blocked start current →
      next ∈ neighbors current →
      next ∉ blocked →
      FreeReach blocked start next

theorem closed_region_traps_paths (blocked region : List Point) (start finish : Point)
    (hstart : start ∈ region)
    (hclosed : ∀ point ∈ region, ∀ other ∈ neighbors point,
      other ∉ blocked → other ∈ region)
    (hpath : FreeReach blocked start finish) :
    finish ∈ region := by
  induction hpath with
  | base => exact hstart
  | advance previous adjacent free inductionHypothesis =>
    exact hclosed _ inductionHypothesis _ adjacent free

theorem u_source_size (width leftHeight rightHeight : Int)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ leftHeight) (hright : 4 ≤ rightHeight) :
    18 ≤ 2*width+leftHeight+rightHeight-2 := by omega

def uEndpoint (width leftHeight rightHeight : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ leftHeight ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ rightHeight ∧ point.2 = width)

def rootOffset (row column : Int) (transpose flipRow flipColumn : Bool) (offset : Point) : Point :=
  let first := if transpose then offset.2 else offset.1
  let second := if transpose then offset.1 else offset.2
  (row+(if flipRow then -first else first),
   column+(if flipColumn then -second else second))

def uStencilHit (width leftHeight rightHeight row column : Int)
    (transpose flipRow flipColumn : Bool) : Prop :=
  uEndpoint width leftHeight rightHeight (rootOffset row column transpose flipRow flipColumn (0,1)) ∨
  uEndpoint width leftHeight rightHeight (rootOffset row column transpose flipRow flipColumn (1,0)) ∨
  uEndpoint width leftHeight rightHeight (rootOffset row column transpose flipRow flipColumn (-2,0)) ∨
  uEndpoint width leftHeight rightHeight (rootOffset row column transpose flipRow flipColumn (0,-4))

theorem every_u_endpoint_hits_stencil (width leftHeight rightHeight row column : Int)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ leftHeight) (hright : 4 ≤ rightHeight)
    (hendpoint : uEndpoint width leftHeight rightHeight (row,column)) :
    uStencilHit width leftHeight rightHeight row column transpose flipRow flipColumn := by
  unfold uEndpoint at hendpoint
  rcases hendpoint with ⟨hrow | hrow, hcolumn⟩ | ⟨hrow, hcolumn⟩ | ⟨hrow, hcolumn⟩ <;>
    cases transpose <;> cases flipRow <;> cases flipColumn <;>
    simp [uStencilHit, rootOffset, uEndpoint] at * <;> omega

end SubQuorum.PositiveUCapObstruction
