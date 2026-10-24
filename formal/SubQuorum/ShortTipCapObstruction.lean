import SubQuorum.WidthEightUCapObstruction

set_option autoImplicit false
set_option maxRecDepth 1000000
set_option maxHeartbeats 10000000

namespace SubQuorum.ShortTipCapObstruction

open SubQuorum.WidthEightUCapObstruction

theorem flexible_four_site_stencil
    (width leftHeight rightHeight row column distance : Int)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ leftHeight) (hright : 4 ≤ rightHeight)
    (hendpoint : uEndpoint width leftHeight rightHeight (row,column))
    (hlower : 1 ≤ distance) (hupper : distance ≤ 4) :
    uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (0,1)) ∨
    uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (1,0)) ∨
    uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (-2,0)) ∨
    uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (0,-distance)) := by
  classical
  by_cases hrightSite : uEndpoint width leftHeight rightHeight
    (rootOffset row column transpose flipRow flipColumn (0,1))
  · exact Or.inl hrightSite
  by_cases hdownSite : uEndpoint width leftHeight rightHeight
    (rootOffset row column transpose flipRow flipColumn (1,0))
  · exact Or.inr (Or.inl hdownSite)
  by_cases hupSite : uEndpoint width leftHeight rightHeight
    (rootOffset row column transpose flipRow flipColumn (-2,0))
  · exact Or.inr (Or.inr (Or.inl hupSite))
  exact Or.inr (Or.inr (Or.inr (three_blockers_force_left_ray
    width leftHeight rightHeight row column distance transpose flipRow flipColumn
    hwidth hleft hright hendpoint hrightSite hdownSite hupSite hlower hupper)))

theorem short_tip_forces_inner_support_and_bar
    (width leftHeight rightHeight row column : Int)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ leftHeight) (hright : 4 ≤ rightHeight)
    (hleftEven : leftHeight % 2 = 0) (hrightEven : rightHeight % 2 = 0)
    (hshort : row ≤ 6)
    (hendpoint : uEndpoint width leftHeight rightHeight (row,column))
    (hblockedRight : ¬uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (0,1)))
    (hblockedDown : ¬uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (1,0)))
    (hblockedUp : ¬uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (-2,0)))
    (hblockedCornerFour : ¬uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (-2,-4)))
    (hblockedCornerSix : ¬uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (-2,-6))) :
    uSupport width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (1,-1)) ∧
    (uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (1,-3)) ∨
     uEndpoint width leftHeight rightHeight
      (rootOffset row column transpose flipRow flipColumn (1,-5))) := by
  obtain ⟨rfl, rfl, hterminal⟩ := three_blockers_force_terminal
    width leftHeight rightHeight row column transpose flipRow flipColumn
    hwidth hleft hright hendpoint hblockedRight hblockedDown hblockedUp
  rcases hterminal with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;> cases flipColumn <;>
    simp_all [uEndpoint, uSupport, rootOffset] <;> omega

def capCore : List Point :=
  seedOwners.flatMap (fun owner => rotorP.map (move owner)) ++
  [(-4,-7),(-4,-6),(-4,-5),(-4,-4),(-4,-3),(-4,-2),(-4,-1),(-4,0),
   (-3,-7),(-3,-6),(-3,-5),(-3,-4),(-3,-3),(-3,-2),(-3,-1),(-3,0),
   (-2,0),(-1,0),(0,0)]

def rotorSupports : List Point := seedOwners.flatMap (fun owner => rotorT.map (move owner))

theorem core_endpoint_disjointness : capCore.length = 43 ∧ capCore.Nodup := by decide

theorem first_support_forcing :
    rotorSupports.contains (-1,-1) = true ∧ capCore.contains (-1,-1) = false ∧
    2 ≤ ((neighbors (-1,-1)).filter capCore.contains).length := by decide

theorem short_tip_blockers_present :
    [(-1,0),(0,-1),(-3,-1),(-3,-5),(-3,-7)].all capCore.contains = true := by decide

theorem first_rotor_owner : ownersAt (-1,-1) capCore = [(false,-3,-5)] := by decide

def rotorBranch : List Point := capCore ++ rotorP.map (move (false,-3,-5))

theorem rotor_branch_endpoint_disjointness :
    rotorBranch.length = 51 ∧ rotorBranch.Nodup := by decide

theorem rotor_branch_forced_support :
    (rotorT.map (move (false,-3,-5))).contains (-2,-1) = true ∧
    rotorBranch.contains (-2,-1) = false ∧
    2 ≤ ((neighbors (-2,-1)).filter rotorBranch.contains).length := by decide

theorem rotor_branch_no_rotor_owner : ownersAt (-2,-1) rotorBranch = [] := by decide

theorem rotor_branch_barrier_present :
    [(-3,-1),(-2,0),(-2,-3),(2,-1)].all rotorBranch.contains = true := by decide

def uRayMask : List Point :=
  capCore ++ [(-1,-1),(-1,-2),(-1,-3),(-1,-4),(-1,-5)]

theorem inner_support_has_two_neighbors :
    uRayMask.contains (0,-2) = false ∧
    2 ≤ ((neighbors (0,-2)).filter uRayMask.contains).length := by decide

theorem inner_support_no_rotor_owner : ownersAt (0,-2) uRayMask = [] := by decide

theorem reflected_three_blockers_present :
    [(0,-1),(-1,-2),(2,-2)].all uRayMask.contains = true := by decide

theorem bounded_even_cap_tip (capWidth tipHeight : Int)
    (hwidthEven : capWidth % 2 = 0) (htipEven : tipHeight % 2 = 0)
    (hwall : tipHeight < capWidth-2) :
    tipHeight ≤ capWidth-4 := by omega

theorem long_tip_requires_wide_cap (capWidth tipHeight : Int)
    (hlong : 8 ≤ tipHeight) (hbound : tipHeight ≤ capWidth-4) :
    12 ≤ capWidth := by omega

theorem arbitrary_cap_covers_bar (capWidth capLeftHeight row column : Int)
    (hwidth : 8 ≤ capWidth) (hleft : 4 ≤ capLeftHeight)
    (hrow : row = -4 ∨ row = -3) (hlower : -7 ≤ column) (hupper : column ≤ 0) :
    uEndpoint capWidth capLeftHeight 4 (row+4,column+capWidth) := by
  simp only [uEndpoint]
  omega

theorem arbitrary_cap_covers_right_stem (capWidth capLeftHeight row : Int)
    (hlower : -2 ≤ row) (hupper : row ≤ 0) :
    uEndpoint capWidth capLeftHeight 4 (row+4,capWidth) := by
  apply Or.inr
  apply Or.inr
  exact ⟨by omega, by omega, rfl⟩

end SubQuorum.ShortTipCapObstruction
