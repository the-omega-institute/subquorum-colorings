import SubQuorum.WidthSixBottomOwner

set_option autoImplicit false

namespace SubQuorum.BoundaryStopAndJointCore

open WidthSixBottomOwner

set_option maxHeartbeats 1000000 in
theorem U_endpoint_stop_roles
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hroot : endpoint width left right anchor)
    (hwest : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,-1)))
    (hsouthEndpoint : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (1,0))) :
    ((transpose = false ∧ flipRow = true ∧
      ((flipColumn = false ∧ anchor = (0,1)) ∨
       (flipColumn = true ∧ anchor = (0,width)))) ∨
     (transpose = true ∧ flipRow = false ∧
      ((flipColumn = true ∧ anchor = (0,1)) ∨
       (flipColumn = false ∧ anchor = (0,width))))) ∨
    (((transpose = false ∧ flipRow = false) ∨
      (transpose = true ∧ flipRow = true)) ∧
      (anchor = (left,1) ∨ anchor = (right,width))) := by
  rcases anchor with ⟨row,column⟩
  rcases hroot with hbar | hnear | hfar
  all_goals
    cases transpose <;> cases flipRow <;> cases flipColumn <;>
      simp [endpoint, pull, Prod.mk.injEq] at hwest hsouthEndpoint ⊢ <;>
      omega

theorem U_boundary_stop_roles
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hevenLeft : left%2 = 0) (hevenRight : right%2 = 0)
    (hroot : endpoint width left right anchor)
    (hwest : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,-1)))
    (hsouthEndpoint : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (1,0)))
    (hsouthSupport : ¬ support width left right
      (pull transpose flipRow flipColumn anchor (1,0))) :
    (transpose = false ∧ flipRow = true ∧
      ((flipColumn = false ∧ anchor = (0,1)) ∨
       (flipColumn = true ∧ anchor = (0,width)))) ∨
    (transpose = true ∧ flipRow = true ∧
      ((flipColumn = false ∧ anchor = (left,1)) ∨
       (flipColumn = true ∧ anchor = (right,width)))) := by
  rcases U_endpoint_stop_roles width left right anchor transpose flipRow flipColumn
      hwidth hleft hright hroot hwest hsouthEndpoint with hcorner | ⟨horientation,htip⟩
  · rcases hcorner with hcorner | ⟨rfl,rfl,hcorner⟩
    · exact Or.inl hcorner
    · exfalso
      apply hsouthSupport
      rcases hcorner with ⟨rfl,rfl⟩ | ⟨rfl,rfl⟩ <;> simp [pull, support]
  · rcases horientation with ⟨rfl,rfl⟩ | ⟨rfl,rfl⟩
    · exfalso
      apply hsouthSupport
      rcases htip with rfl | rfl <;> simp [pull, support]
    · exact Or.inr ⟨rfl,rfl,
        terminal_avoiding_lower_support_points_down width left right anchor flipColumn
          hwidth hleft hright hevenLeft hevenRight
          (htip.imp (fun equality => by cases equality; simp)
            (fun equality => by cases equality; simp)) hsouthSupport |>.imp
          (fun ⟨hrow,hcolumn,hflip⟩ => ⟨hflip,Prod.ext hrow hcolumn⟩)
          (fun ⟨hrow,hcolumn,hflip⟩ => ⟨hflip,Prod.ext hrow hcolumn⟩)⟩

theorem corner_even_tile_profile (width left right : Int)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right) :
    endpoint width left right (0,1) ∧ endpoint width left right (0,2) ∧
    ¬ endpoint width left right (-1,1) ∧ ¬ endpoint width left right (-1,2) ∧
    ¬ support width left right (0,1) ∧ ¬ support width left right (0,2) ∧
    ¬ support width left right (-1,1) ∧ ¬ support width left right (-1,2) := by
  simp [endpoint, support]
  omega

def coreMove (incident : Int) (point : Point) : Point :=
  (incident+2-point.1,point.2+1)

theorem both_core_tip_predecessors_point_down (incident far width : Int) :
    coreMove incident (incident-1,1) = (3,2) ∧
    coreMove incident (far-1,width) = (incident+3-far,width+1) := by
  simp [coreMove, Prod.mk.injEq]
  omega

theorem near_far_core_bar_directions (incident width : Int) :
    coreMove incident (0,2) = (incident+2,3) ∧
    coreMove incident (0,width-1) = (incident+2,width) := by
  simp [coreMove]

def rotorT : List Point :=
  [(0,2),(1,1),(2,5),(1,4),(5,3),(4,4),(3,0),(4,1)]

def rotorStopOwners : List (Bool × Int × Int) :=
  (([false,true].flatMap fun mirror => rotorP.map fun tip =>
    (mirror,-tip.1,-(if mirror then -tip.2 else tip.2))).filter fun owner =>
      let points := rotorP.map (rotorMove owner.1 owner.2.1 owner.2.2)
      let selections := rotorT.map (rotorMove owner.1 owner.2.1 owner.2.2)
      !points.contains (0,-1) && !points.contains (1,0) &&
      !selections.contains (1,0))

theorem unique_rotor_stop : rotorStopOwners = [(true,-2,4)] := by decide

theorem rotor_stop_has_consumable_lower_support :
    (rotorT.map (rotorMove true (-2) 4)).contains (2,0) = true ∧
    (rotorP.map (rotorMove true (-2) 4)).contains (2,1) = true := by decide

theorem rotor_stop_original_triple :
    [(0,0),(0,1),(1,0),(1,1)].filter
      ((rotorP.map (rotorMove true (-2) 4)).contains) = [(0,0),(0,1),(1,1)] := by decide

theorem last_point_south_is_not_original_support
    (occupied selected originalSupport : Point → Prop) (row : Int)
    (hnotEndpoint : ¬ occupied (row+1,2))
    (hretention : ∀ point, originalSupport point → ¬occupied point → selected point)
    (hdegree : selected (row+1,2) →
      ¬(occupied (row,2) ∧ occupied (row+1,1)))
    (hprevious : occupied (row,2)) (hwall : occupied (row+1,1)) :
    ¬ originalSupport (row+1,2) := by
  intro hsupport
  exact hdegree (hretention _ hsupport hnotEndpoint) ⟨hprevious,hwall⟩

theorem rotor_stop_must_reach_terminal (lastRow terminal : Int)
    (hlast : lastRow ≤ terminal)
    (hnotBefore : ¬lastRow+2 ≤ terminal)
    (hnotPenultimate : lastRow+1 ≠ terminal) :
    lastRow = terminal := by omega

theorem even_stop_is_rotor (row : Int) (isCorner isTerminal isRotor : Prop)
    (hroles : isCorner ∨ isTerminal ∨ isRotor)
    (heven : row%2 = 0)
    (hcorner : isCorner → row%2 ≠ 0)
    (hterminal : isTerminal → row%2 ≠ 0) : isRotor := by
  rcases hroles with hrole | hrole | hrole
  · exact False.elim (hcorner hrole heven)
  · exact False.elim (hterminal hrole heven)
  · exact hrole

theorem odd_corner_incident_clearance (lastRow outer incident long : Int)
    (hlast : lastRow ≤ long-1)
    (hdisjoint : outer+3 ≤ lastRow-incident) :
    incident ≤ long-outer-4 := by omega

theorem mutual_near_tip_identification
    (firstStop secondStop firstPort secondPort secondAnchorRow secondAnchorColumn : Int)
    (hfirstRow : firstStop = secondAnchorRow+secondPort)
    (hfirstColumn : 1 = secondAnchorColumn+2)
    (hsecondRow : secondAnchorRow+1 = 2)
    (hsecondColumn : secondAnchorColumn+secondStop = firstPort) :
    firstStop = secondPort+1 ∧ secondStop = firstPort+1 := by omega

theorem two_cores_cannot_supply_both_stops
    (firstStop secondStop firstPort secondPort secondAnchorRow secondAnchorColumn : Int)
    (hfirstLong : 13 ≤ firstStop) (_hfirstPort : firstPort ≤ 4)
    (hsecondPort : secondPort ≤ 4)
    (hfirstRow : firstStop = secondAnchorRow+secondPort)
    (_hfirstColumn : 1 = secondAnchorColumn+2)
    (hsecondRow : secondAnchorRow+1 = 2)
    (_hsecondColumn : secondAnchorColumn+secondStop = firstPort) : False := by omega

end SubQuorum.BoundaryStopAndJointCore
