import SubQuorum.CriticalPhaseOneBarReturns
import SubQuorum.NeutralFullReceiverInjection

set_option autoImplicit false

namespace SubQuorum.CriticalRegularReceiverSeparation

open NeutralSupportInjection NeutralFullReceiverInjection WidthSixBottomOwner

abbrev Point := Int × Int

def criticalTile : List Point := [(0,0),(1,0),(0,1),(1,1)]

def activeCritical : List Point := [(-1,-1),(-1,0),(-1,1)]

def otherCritical : List Point := [(0,-1),(0,-2)]

set_option maxHeartbeats 2000000 in
theorem critical_regular_shared_tile_catalogue
    (tag : Point → Option Point) (frame : Frame) (point : Point)
    (hframe : frame ∈ frames) (hpoint : point ∈ criticalTile)
    (hnonzero : point ≠ (0,0))
    (htile : ∀ site ∈ tileSites frame, addPoint point site ∈ criticalTile)
    (hcriticalActive : ∀ site ∈ activeCritical, tag site = some (-1,0))
    (hcriticalOther : ∀ site ∈ otherCritical, tag site = none)
    (hregularActive : ∀ site ∈ extendedActiveSites frame,
      tag (addPoint point site) = some frame.1)
    (hregularOther : ∀ site ∈ passiveSites frame,
      tag (addPoint point site) = none ∨ tag (addPoint point site) = some frame.2) :
    (point = (1,0) ∧ frame = ((-1,0),(0,-1))) ∨
    (point = (1,1) ∧ frame = ((-1,0),(0,1))) ∨
    (point = (0,1) ∧ frame = ((0,-1),(-1,0))) := by
  simp only [frames, List.mem_cons, List.not_mem_nil, or_false] at hframe
  rcases hframe with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals
    simp only [criticalTile, List.mem_cons, List.not_mem_nil, or_false] at hpoint
    rcases hpoint with rfl | rfl | rfl | rfl
  all_goals simp [criticalTile, tileSites, addPoint, extendedActiveSites,
    passiveSites, activeCritical, otherCritical, baseFrame]
    at hnonzero htile hcriticalActive hcriticalOther hregularActive hregularOther ⊢
  all_goals simp_all

set_option maxHeartbeats 2000000 in
theorem U_owner_avoiding_three_neighbors_has_two_step_terminal_stencil
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hroot : endpoint width left right anchor)
    (hnorth : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (-1,0)))
    (hwest : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,-1)))
    (heast : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,1))) :
    endpoint width left right (pull transpose flipRow flipColumn anchor (2,0)) ∧
    ¬ endpoint width left right (pull transpose flipRow flipColumn anchor (2,-1)) := by
  rcases anchor with ⟨row,column⟩
  rcases hroot with hbar | hnear | hfar
  all_goals
    cases transpose <;> cases flipRow <;> cases flipColumn <;>
      simp [endpoint, pull] at hnorth hwest heast ⊢ <;> omega

theorem three_neighbor_rotor_owner_contains_second_south_point :
    (rotorOwners [(-1,0),(0,-1),(0,1)]).all (fun owner =>
      (rotorP.map (rotorMove owner.1 owner.2.1 owner.2.2)).contains (2,0)) = true := by decide

theorem U_terminal_stencil_conflicts_with_a_foreign_U_pair
    {Owner : Type} (owns : Owner → Point → Prop) (critical companion : Owner)
    (hstep : owns critical (2,0)) (hlateral : ¬ owns critical (2,-1))
    (hpairFirst : owns companion (2,0)) (hpairSecond : owns companion (2,-1))
    (hunique : ∀ first second site, owns first site → owns second site → first = second) :
    False := by
  have hequal := hunique critical companion (2,0) hstep hpairFirst
  exact hlateral (hequal.symm ▸ hpairSecond)

theorem rotor_step_conflicts_with_a_U_companion
    {Owner : Type} (owns : Owner → Point → Prop) (isRotor : Owner → Prop)
    (critical companion : Owner) (hrotor : isRotor critical) (hU : ¬ isRotor companion)
    (hstep : owns critical (2,0)) (hpairFirst : owns companion (2,0))
    (hunique : ∀ first second site, owns first site → owns second site → first = second) :
    False := by
  have hequal := hunique critical companion (2,0) hstep hpairFirst
  exact hU (hequal ▸ hrotor)

theorem outside_critical_joint_endpoint_count
    (contacts long nonfull additional criticalOutside outsideTotal : Nat)
    (hregular : additional+nonfull = 2*(contacts+long))
    (hdisjointCount : outsideTotal = additional+criticalOutside) :
    outsideTotal+nonfull = 2*(contacts+long)+criticalOutside := by omega

theorem outside_and_closed_bar_joint_endpoint_count
    (contacts long nonfull additional criticalOutside criticalClosed total : Nat)
    (hregular : additional+nonfull = 2*(contacts+long))
    (hdisjointCount : total = additional+criticalOutside+4*criticalClosed) :
    total+nonfull = 2*(contacts+long)+criticalOutside+4*criticalClosed := by omega

theorem joint_critical_count_uses_the_existing_H_pool
    (contacts long nonfull criticalOutside criticalClosed total passive activation boundary : Nat)
    (hcount : total+nonfull = 2*(contacts+long)+criticalOutside+4*criticalClosed)
    (hbudget : passive+nonfull ≤ 2*activation+boundary) :
    2*(contacts+long)+criticalOutside+4*criticalClosed+passive ≤
      total+2*activation+boundary := by omega

theorem AA_outside_critical_endpoint_requirement
    (curves contacts long nonfull criticalOutside total : Nat)
    (hcount : total+nonfull = 2*(contacts+long)+criticalOutside)
    (hturn : 4*curves ≤ contacts) (hstop : nonfull = 0) :
    8*curves+2*long+criticalOutside ≤ total := by omega

end SubQuorum.CriticalRegularReceiverSeparation
