import SubQuorum.WidthSixBottomOwner

set_option autoImplicit false

namespace SubQuorum.CriticalOwnerProfiles

open WidthSixBottomOwner

def square : List Point := [(0,0),(1,0),(0,1),(1,1)]

def terminalStep (transpose : Bool) : Point :=
  if transpose then (0,1) else (1,0)

set_option maxHeartbeats 2000000 in
theorem critical_U_owner_is_outer_corner_or_terminal
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hroot : endpoint width left right anchor)
    (hnorth : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (-1,0)))
    (hwest : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,-1))) :
    (flipRow = false ∧
      ((flipColumn = false ∧ anchor = (0,1)) ∨
       (flipColumn = true ∧ anchor = (0,width)))) ∨
    (flipRow = true ∧ (anchor = (left,1) ∨ anchor = (right,width))) := by
  rcases anchor with ⟨row,column⟩
  rcases hroot with hbar | hnear | hfar
  all_goals
    cases transpose <;> cases flipRow <;> cases flipColumn <;>
      simp [endpoint, pull, Prod.mk.injEq] at hnorth hwest ⊢ <;> omega

set_option maxHeartbeats 2000000 in
theorem positive_U_cannot_own_a_critical_point
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hevenWidth : width%2 = 0) (hevenLeft : left%2 = 0)
    (hevenRight : right%2 = 0)
    (hroot : endpoint width left right anchor)
    (hnorth : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (-1,0)))
    (hwest : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,-1)))
    (hrow : (anchor.1-(if flipRow then 1 else 0))%2 = 0)
    (hcolumn : (anchor.2-(if flipColumn then 1 else 0))%2 = 0) : False := by
  have hrole := critical_U_owner_is_outer_corner_or_terminal width left right anchor
    transpose flipRow flipColumn hwidth hleft hright hroot hnorth hwest
  rcases anchor with ⟨row,column⟩
  cases flipRow <;> cases flipColumn <;>
    simp [Prod.mk.injEq] at hrole hrow hcolumn <;> omega

set_option maxHeartbeats 2000000 in
theorem critical_terminal_has_exact_original_pair
    (width left right : Int) (anchor : Point)
    (transpose flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hterminal : anchor = (left,1) ∨ anchor = (right,width)) :
    ∀ point ∈ square,
      endpoint width left right (pull transpose true flipColumn anchor point) ↔
        point = (0,0) ∨ point = terminalStep transpose := by
  rcases hterminal with rfl | rfl
  all_goals
    intro point hpoint
    simp only [square, List.mem_cons, List.not_mem_nil, or_false] at hpoint
    rcases hpoint with rfl | rfl | rfl | rfl
    all_goals cases transpose <;> cases flipColumn <;>
      simp [endpoint, pull, terminalStep] <;> omega

set_option maxHeartbeats 2000000 in
theorem critical_terminal_has_exact_original_support
    (width left right phaseColumn : Int) (anchor : Point)
    (transpose flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hevenLeft : left%2 = 0) (hevenRight : right%2 = 0)
    (hevenWidth : width%2 = 0)
    (hterminal : anchor = (left,1) ∨ anchor = (right,width))
    (hphase : phaseColumn = 0 ∨ phaseColumn = 1)
    (hcolumn : (anchor.2-(if flipColumn then 1 else 0))%2 = phaseColumn) :
    ∀ point ∈ square,
      support width left right (pull transpose true flipColumn anchor point) ↔
        point = (if phaseColumn = 0 then
          (if transpose then (1,0) else (0,1)) else (1,1)) := by
  rcases hterminal with rfl | rfl
  all_goals rcases hphase with rfl | rfl
  all_goals
    intro point hpoint
    simp only [square, List.mem_cons, List.not_mem_nil, or_false] at hpoint
    rcases hpoint with rfl | rfl | rfl | rfl
    all_goals cases transpose <;> cases flipColumn <;>
      simp [support, pull, hevenWidth, hevenLeft, hevenRight] at hcolumn ⊢ <;> omega

set_option maxHeartbeats 2000000 in
theorem phase_ten_critical_terminal_cannot_point_east
    (width left right clearance : Int) (anchor : Point) (flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hevenWidth : width%2 = 0) (hclearance : 1 ≤ clearance)
    (hterminal : anchor = (left,1) ∨ anchor = (right,width))
    (hcolumn : (anchor.2-(if flipColumn then 1 else 0))%2 = 0)
    (hbar : ∀ column, 0 ≤ column → column ≤ clearance →
      ¬ endpoint width left right (pull true true flipColumn anchor (-1,column)))
    (hwall : ¬ endpoint width left right
      (pull true true flipColumn anchor (0,clearance))) : False := by
  rcases hterminal with rfl | rfl
  · cases flipColumn
    · simp at hcolumn
    · by_cases hlong : clearance ≤ left
      · apply hwall
        simp [endpoint, pull]
        omega
      · have hcollision := hbar left (by omega) (by omega)
        apply hcollision
        simp [endpoint, pull]
        omega
  · cases flipColumn
    · by_cases hlong : clearance ≤ right
      · apply hwall
        simp [endpoint, pull]
        omega
      · have hcollision := hbar right (by omega) (by omega)
        apply hcollision
        simp [endpoint, pull]
        omega
    · simp at hcolumn
      omega

theorem terminal_points_of_one_U_cannot_share_a_tile
    (width left right : Int) (first second : Point)
    (hwidth : 6 ≤ width)
    (hfirst : first = (left,1) ∨ first = (right,width))
    (hsecond : second = (left,1) ∨ second = (right,width))
    (hlower : first.2-1 ≤ second.2) (hupper : second.2 ≤ first.2+1) :
    first = second := by
  rcases hfirst with rfl | rfl <;> rcases hsecond with rfl | rfl <;>
    simp at hlower hupper ⊢ <;> omega

def rotorT : List Point :=
  [(0,2),(1,1),(2,5),(1,4),(5,3),(4,4),(3,0),(4,1)]

def rotorEndpoints (owner : Bool × Int × Int) : List Point :=
  rotorP.map (rotorMove owner.1 owner.2.1 owner.2.2)

def rotorSupports (owner : Bool × Int × Int) : List Point :=
  rotorT.map (rotorMove owner.1 owner.2.1 owner.2.2)

def rotorReceivers (owner : Bool × Int × Int) : List Point :=
  ((rotorEndpoints owner).map fun point => (point.1/2,point.2/2)).eraseDups

def rotorCharge (owner : Bool × Int × Int) : Int :=
  Int.ofNat ((rotorSupports owner).filter fun point =>
    (rotorReceivers owner).contains (point.1/2,point.2/2)).length+
      4-2*Int.ofNat (rotorReceivers owner).length

theorem every_critical_rotor_has_zero_original_charge :
    (rotorOwners [(-1,0),(0,-1)]).all (fun owner =>
      decide (rotorCharge owner = 0)) = true := by decide

theorem complete_critical_rotor_local_profiles :
    (rotorOwners [(-1,0),(0,-1)]).all (fun owner =>
      let own := square.filter (rotorEndpoints owner).contains
      let selected := square.filter (rotorSupports owner).contains
      (own.length == 2 && selected.length == 1) ||
      (own.length == 3 && selected.isEmpty)) = true := by decide

theorem full_active_bar_reduces_critical_rotor_roles :
    (rotorOwners [(-1,0),(0,-1),(-1,1),(-1,2)]).all (fun owner =>
      ((square.filter (rotorEndpoints owner).contains == [(0,0),(1,0)]) &&
       (square.filter (rotorSupports owner).contains == [(0,1)])) ||
      ((square.filter (rotorEndpoints owner).contains == [(0,0),(1,0),(1,1)]) &&
       (rotorSupports owner).contains (0,2) &&
       (rotorEndpoints owner).contains (1,2))) = true := by decide

theorem minimum_clearance_has_no_critical_rotor :
    rotorOwners [(-1,0),(0,-1),(-1,1),(0,1),(1,1),(2,1)] = [] := by decide

theorem critical_rotor_triple_has_the_stated_paired_singleton :
    (rotorOwners [(-1,0),(0,-1),(-1,1),(-1,2)]).all (fun owner =>
      if (square.filter (rotorEndpoints owner).contains).length == 3 then
        ([(0,2),(1,2),(0,3),(1,3)].filter (rotorEndpoints owner).contains == [(1,2)]) &&
        ([(0,2),(1,2),(0,3),(1,3)].filter (rotorSupports owner).contains == [(0,2),(1,3)])
      else true) = true := by decide

theorem distinct_rotor_tips_cannot_share_a_tile :
    rotorP.all (fun first => rotorP.all (fun second =>
      let firstNeighbors := rotorP.filter fun point =>
        decide (Int.natAbs (point.1-first.1)+Int.natAbs (point.2-first.2) = 1)
      let secondNeighbors := rotorP.filter fun point =>
        decide (Int.natAbs (point.1-second.1)+Int.natAbs (point.2-second.2) = 1)
      if firstNeighbors.length == 1 && secondNeighbors.length == 1 &&
          decide (Int.natAbs (first.1-second.1) ≤ 1 ∧
            Int.natAbs (first.2-second.2) ≤ 1) then first == second else true)) = true := by decide

theorem two_point_profiles_bound_events_per_tile
    {Event Site : Type} (events : List Event) (profile : Event → List Site)
    (tile : List Site)
    (hsize : ∀ event ∈ events, 2 ≤ (profile event).length)
    (hnodup : (events.flatMap profile).Nodup)
    (hsubset : events.flatMap profile ⊆ tile) (htile : tile.length = 4) :
    events.length ≤ 2 := by
  have hmass : 2*events.length ≤ (events.flatMap profile).length := by
    induction events with
    | nil => simp
    | cons event rest inductionHypothesis =>
      have hhead := hsize event (by simp)
      have htail := inductionHypothesis (by
        intro current hcurrent
        exact hsize current (by simp [hcurrent]))
        (List.nodup_append.mp hnodup).2.1
        (by
          intro site hsite
          apply hsubset
          simp only [List.flatMap_cons, List.mem_append]
          exact Or.inr hsite)
      simp only [List.length_cons, List.flatMap_cons, List.length_append]
      omega
  have hbound := hnodup.length_le_of_subset hsubset
  omega

theorem exact_critical_profile_mass
    (pairs triples full total events : Nat)
    (hpartition : events = pairs+triples+full)
    (hprofile : total = 2*pairs+3*triples+4*full) :
    total = 2*events+triples+2*full := by omega

theorem joint_outside_critical_profile_count
    (contacts long ordinaryStops criticalOutside triplesOutside fullOutside
      additional total : Nat)
    (hregular : additional+ordinaryStops = 2*(contacts+long))
    (hcount : total = additional+2*criticalOutside+triplesOutside+2*fullOutside) :
    total+ordinaryStops =
      2*(contacts+long)+2*criticalOutside+triplesOutside+2*fullOutside := by omega

theorem critical_stops_use_the_existing_reserve
    (passive ordinaryStops criticalStops rotorStops activation unused rotor boundary reserve : Nat)
    (hbudget : passive+ordinaryStops+criticalStops ≤ 2*activation+boundary)
    (hrotor : rotorStops ≤ rotor)
    (hidentity : 2*reserve = activation+unused+rotor+boundary) :
    passive+ordinaryStops+criticalStops+rotorStops+unused ≤ 2*reserve+activation := by omega

theorem AA_critical_stops_vanish
    (criticalStops rotorStops boundary rotor : Nat)
    (hboundary : criticalStops ≤ boundary) (hrotor : rotorStops ≤ rotor)
    (hzeroBoundary : boundary = 0) (hzeroRotor : rotor = 0) :
    criticalStops = 0 ∧ rotorStops = 0 := by omega

end SubQuorum.CriticalOwnerProfiles
