import SubQuorum.WidthSixBottomOwner
import SubQuorum.NeutralSupportInjection

set_option autoImplicit false

namespace SubQuorum.CriticalPhaseTenBackfill

open WidthSixBottomOwner NeutralSupportInjection

abbrev Point := Int × Int

def addPoint (first second : Point) : Point :=
  (first.1+second.1,first.2+second.2)

def shift (root direction : Point) (amount : Int) : Point :=
  (root.1+amount*direction.1,root.2+amount*direction.2)

def backTile : List Point := [(0,-2),(0,-1),(1,-2),(1,-1)]

def criticalSites (frame : Frame) : List Point :=
  [(0,0),(-frame.1.1,-frame.1.2),frame.2,
   (frame.2.1-frame.1.1,frame.2.2-frame.1.2)]

def ordinarySites (frame : Frame) : List Point :=
  [(0,0),frame.1,(-frame.2.1,-frame.2.2),
   (frame.1.1-frame.2.1,frame.1.2-frame.2.2)]

def backSites (frame : Frame) : List Point :=
  [(-frame.2.1,-frame.2.2),(-2*frame.2.1,-2*frame.2.2),
   (-frame.1.1-frame.2.1,-frame.1.2-frame.2.2),
   (-frame.1.1-2*frame.2.1,-frame.1.2-2*frame.2.2)]

def activeCritical (frame : Frame) : List Point :=
  [(frame.1.1-frame.2.1,frame.1.2-frame.2.2),frame.1,
   (frame.1.1+frame.2.1,frame.1.2+frame.2.2)]

def companionCritical (frame : Frame) : List Point :=
  [(-frame.2.1,-frame.2.2),(-2*frame.2.1,-2*frame.2.2)]

def activeOrdinary (frame : Frame) : List Point :=
  [(-frame.1.1-frame.2.1,-frame.1.2-frame.2.2),
   (-frame.2.1,-frame.2.2),(frame.1.1-frame.2.1,frame.1.2-frame.2.2),
   (2*frame.1.1-frame.2.1,2*frame.1.2-frame.2.2)]

def knownActive : List Point := [(-1,-1),(-1,0),(-1,1)]

def knownOther : List Point := [(0,-2),(0,-1),(0,0),(1,0),(2,0)]

set_option maxHeartbeats 2000000 in
theorem every_U_critical_owner_has_a_two_step_run
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hroot : endpoint width left right anchor)
    (hnorth : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (-1,0)))
    (hwest : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,-1))) :
    (endpoint width left right (pull transpose flipRow flipColumn anchor (1,0)) ∧
     endpoint width left right (pull transpose flipRow flipColumn anchor (2,0))) ∨
    (endpoint width left right (pull transpose flipRow flipColumn anchor (0,1)) ∧
     endpoint width left right (pull transpose flipRow flipColumn anchor (0,2))) := by
  rcases anchor with ⟨row,column⟩
  rcases hroot with hbar | hnear | hfar
  all_goals cases transpose <;> cases flipRow <;> cases flipColumn <;>
    simp [endpoint, pull] at hnorth hwest ⊢ <;> omega

theorem every_rotor_critical_owner_has_a_two_step_run :
    (rotorOwners [(-1,0),(0,-1)]).all (fun owner =>
      let sites := rotorP.map (rotorMove owner.1 owner.2.1 owner.2.2)
      (sites.contains (1,0) && sites.contains (2,0)) ||
      (sites.contains (0,1) && sites.contains (0,2))) = true := by decide

set_option maxHeartbeats 2000000 in
theorem phase_ten_south_terminal_backfill_stencil
    (width left right : Int) (anchor : Point) (flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hevenWidth : width%2 = 0) (hevenLeft : left%2 = 0)
    (hevenRight : right%2 = 0)
    (hterminal : anchor = (left,1) ∨ anchor = (right,width))
    (hphase : (anchor.2-(if flipColumn then 1 else 0))%2 = 0) :
    support width left right (pull false true flipColumn anchor (1,-1)) ∧
    endpoint width left right (pull false true flipColumn anchor (1,0)) ∧
    endpoint width left right (pull false true flipColumn anchor (2,0)) ∧
    ¬ endpoint width left right (pull false true flipColumn anchor (1,-1)) ∧
    ¬ endpoint width left right (pull false true flipColumn anchor (1,-2)) ∧
    ¬ endpoint width left right (pull false true flipColumn anchor (1,1)) ∧
    pull false true flipColumn anchor (1,0) ≠ (left,1) ∧
    pull false true flipColumn anchor (1,0) ≠ (right,width) := by
  rcases hterminal with rfl | rfl
  all_goals cases flipColumn <;>
    simp [endpoint, support, pull, Prod.mk.injEq] at hphase ⊢ <;> omega

set_option maxHeartbeats 2000000 in
theorem companion_terminal_back_tile_profile
    (width left right : Int) (anchor : Point) (flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hevenLeft : left%2 = 0) (hevenRight : right%2 = 0)
    (hrole : (anchor = (left+1,1) ∧ flipColumn = false) ∨
      (anchor = (right+1,width) ∧ flipColumn = true)) :
    endpoint width left right (pull true false flipColumn anchor (0,-1)) ∧
    endpoint width left right (pull true false flipColumn anchor (0,-2)) ∧
    endpoint width left right (pull true false flipColumn anchor (0,-3)) ∧
    support width left right (pull true false flipColumn anchor (1,-2)) ∧
    ¬ endpoint width left right (pull true false flipColumn anchor (1,-2)) ∧
    ¬ endpoint width left right (pull true false flipColumn anchor (1,-1)) := by
  rcases hrole with ⟨rfl,rfl⟩ | ⟨rfl,rfl⟩
  all_goals simp [endpoint, support, pull] <;> omega

def adjacent (first second : Point) : Prop :=
  Int.natAbs (first.1-second.1)+Int.natAbs (first.2-second.2) = 1

theorem two_support_consumptions_fill_the_back_tile
    (originalSupport occupied selected : Point → Prop)
    (hfirstSupport : originalSupport (1,-1))
    (hsecondSupport : originalSupport (1,-2))
    (hfirstAnchor : occupied (1,0)) (hsecondAnchor : occupied (0,-1))
    (hthirdAnchor : occupied (0,-2))
    (hretention : ∀ point, originalSupport point → ¬ occupied point → selected point)
    (hdegree : ∀ point first second, selected point → occupied first → occupied second →
      adjacent point first → adjacent point second → first = second) :
    ∀ point ∈ backTile, occupied point := by
  have hfirst := two_distinct_anchors_force_consumption originalSupport occupied selected
    (1,-1) (1,0) (0,-1) hfirstSupport hfirstAnchor hsecondAnchor (by decide)
    (hretention (1,-1)) (fun hselected hanchor hother =>
      hdegree (1,-1) (1,0) (0,-1) hselected hanchor hother
        (by simp [adjacent]) (by simp [adjacent]))
  have hsecond := two_distinct_anchors_force_consumption originalSupport occupied selected
    (1,-2) (1,-1) (0,-2) hsecondSupport hfirst hthirdAnchor (by decide)
    (hretention (1,-2)) (fun hselected hanchor hother =>
      hdegree (1,-2) (1,-1) (0,-2) hselected hanchor hother
        (by simp [adjacent]) (by simp [adjacent]))
  intro point hpoint
  simp only [backTile, List.mem_cons, List.not_mem_nil, or_false] at hpoint
  rcases hpoint with rfl | rfl | rfl | rfl
  · exact hthirdAnchor
  · exact hsecondAnchor
  · exact hsecond
  · exact hfirst

set_option maxHeartbeats 2000000 in
theorem back_tile_has_no_ordinary_receiver
    (tag : Point → Option Point) (frame : Frame) (point : Point)
    (hframe : frame ∈ frames) (hpoint : point ∈ backTile)
    (htile : ∀ site ∈ ordinarySites frame, addPoint point site ∈ backTile)
    (hactive : ∀ site ∈ knownActive, tag site = some (-1,0))
    (hother : ∀ site ∈ knownOther, tag site = none)
    (hordinary : ∀ site ∈ activeOrdinary frame,
      tag (addPoint point site) = some frame.1) : False := by
  simp only [frames, List.mem_cons, List.not_mem_nil, or_false] at hframe
  rcases hframe with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals simp only [backTile, List.mem_cons, List.not_mem_nil, or_false] at hpoint
  all_goals rcases hpoint with rfl | rfl | rfl | rfl
  all_goals simp [backTile, ordinarySites, activeOrdinary, addPoint, knownActive,
    knownOther, baseFrame] at htile hactive hother hordinary
  all_goals simp_all

set_option maxHeartbeats 2000000 in
theorem back_tile_critical_catalogue
    (tag : Point → Option Point) (frame : Frame) (point : Point)
    (hframe : frame ∈ frames) (hpoint : point ∈ backTile)
    (htile : ∀ site ∈ criticalSites frame, addPoint point site ∈ backTile)
    (hactive : ∀ site ∈ knownActive, tag site = some (-1,0))
    (hother : ∀ site ∈ knownOther, tag site = none)
    (hcriticalActive : ∀ site ∈ activeCritical frame,
      tag (addPoint point site) = some frame.1)
    (hcriticalCompanion : ∀ site ∈ companionCritical frame,
      tag (addPoint point site) = none) :
    (point = (0,-2) ∧ frame = ((-1,0),(0,1))) ∨
    (point = (0,-2) ∧ frame = ((0,-1),(1,0))) ∨
    (point = (0,-1) ∧ frame = ((-1,0),(0,-1))) ∨
    (point = (1,-2) ∧ frame = ((1,0),(0,1))) ∨
    (point = (1,-2) ∧ frame = ((0,-1),(-1,0))) := by
  simp only [frames, List.mem_cons, List.not_mem_nil, or_false] at hframe
  rcases hframe with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals simp only [backTile, List.mem_cons, List.not_mem_nil, or_false] at hpoint
  all_goals rcases hpoint with rfl | rfl | rfl | rfl
  all_goals simp [backTile, criticalSites, activeCritical, companionCritical,
    addPoint, knownActive, knownOther, baseFrame]
    at htile hactive hother hcriticalActive hcriticalCompanion ⊢
  all_goals simp_all

theorem five_critical_candidates_conflict_with_original_owners
    {Owner : Type} (owns : Owner → Point → Prop) (phaseEleven : Owner → Prop)
    (firstCompanion firstRoot secondRoot secondCompanion : Owner)
    (point : Point) (frame : Frame)
    (hcases : (point = (0,-2) ∧ frame = ((-1,0),(0,1))) ∨
      (point = (0,-2) ∧ frame = ((0,-1),(1,0))) ∨
      (point = (0,-1) ∧ frame = ((-1,0),(0,-1))) ∨
      (point = (1,-2) ∧ frame = ((1,0),(0,1))) ∨
      (point = (1,-2) ∧ frame = ((0,-1),(-1,0))))
    (hunique : ∀ first second site, owns first site → owns second site → first = second)
    (hFphase : phaseEleven firstCompanion) (hGphase : ¬ phaseEleven firstRoot)
    (hDphase : phaseEleven secondCompanion)
    (hFtopLeft : owns firstCompanion (0,-2))
    (hFnotBottomLeft : ¬ owns firstCompanion (1,-2))
    (hGroot : owns firstRoot (0,0)) (hGnext : owns firstRoot (1,0))
    (hGnotBottomLeft : ¬ owns firstRoot (1,-2))
    (hroot : owns secondRoot point)
    (hcompanion : owns secondCompanion (shift point frame.2 (-1)))
    (hrun : (owns secondRoot (shift point frame.1 (-1)) ∧
      owns secondRoot (shift point frame.1 (-2))) ∨
      (owns secondRoot (shift point frame.2 1) ∧
      owns secondRoot (shift point frame.2 2))) : False := by
  have hFnotGroot : ¬ owns firstCompanion (0,0) := by
    intro hown
    have hequal := hunique firstCompanion firstRoot (0,0) hown hGroot
    exact hGphase (hequal ▸ hFphase)
  rcases hcases with ⟨rfl,rfl⟩ | ⟨rfl,rfl⟩ | ⟨rfl,rfl⟩ | ⟨rfl,rfl⟩ | ⟨rfl,rfl⟩
  · have hequal := hunique secondRoot firstCompanion (0,-2) hroot hFtopLeft
    simp [shift, hequal] at hrun
    rcases hrun with hdown | heast
    · exact hFnotBottomLeft hdown.1
    · exact hFnotGroot heast.2
  · have hequal := hunique secondRoot firstCompanion (0,-2) hroot hFtopLeft
    simp [shift, hequal] at hrun
    rcases hrun with heast | hdown
    · exact hFnotGroot heast.2
    · exact hFnotBottomLeft hdown.1
  · have hown : owns secondCompanion (0,0) := by simpa [shift] using hcompanion
    have hequal := hunique secondCompanion firstRoot (0,0) hown hGroot
    exact hGphase (hequal ▸ hDphase)
  all_goals
    have hnotF : secondRoot ≠ firstCompanion := by
      intro hequal
      exact hFnotBottomLeft (hequal ▸ hroot)
    have hnotG : secondRoot ≠ firstRoot := by
      intro hequal
      exact hGnotBottomLeft (hequal ▸ hroot)
    have hnorth : ¬ owns secondRoot (0,-2) := by
      intro hown
      exact hnotF (hunique secondRoot firstCompanion (0,-2) hown hFtopLeft)
    have heast : ¬ owns secondRoot (1,0) := by
      intro hown
      exact hnotG (hunique secondRoot firstRoot (1,0) hown hGnext)
    simp [shift] at hrun
    rcases hrun with hfirst | hsecond
    all_goals first | exact hnorth hfirst.1 | exact heast hfirst.2 |
      exact hnorth hsecond.1 | exact heast hsecond.2

def possibleBackRoots : List Point :=
  [(0,0),(1,0),(0,-3),(1,-3),(-1,-2),(-1,-1),(2,-2),(2,-1)]

set_option maxHeartbeats 2000000 in
theorem distinct_companion_pairs_sharing_a_back_tile_catalogue
    (point : Point) (frame : Frame) (hframe : frame ∈ frames)
    (hpoint : point ∈ possibleBackRoots)
    (htile : ∀ site ∈ backSites frame, addPoint point site ∈ backTile)
    (hforeign : ∀ site ∈ companionCritical frame,
      addPoint point site ≠ (0,-2) ∧ addPoint point site ≠ (0,-1)) :
    (point = (1,0) ∧ frame = ((1,0),(0,1))) ∨
    (point = (1,-3) ∧ frame = ((1,0),(0,-1))) := by
  simp only [frames, List.mem_cons, List.not_mem_nil, or_false] at hframe
  rcases hframe with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals simp only [possibleBackRoots, List.mem_cons, List.not_mem_nil, or_false] at hpoint
  all_goals rcases hpoint with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals simp [backTile, backSites, companionCritical, addPoint, baseFrame]
    at htile hforeign ⊢

theorem joint_profile_and_backfill_endpoint_count
    (contacts long ordinaryStops criticalOutside triplesOutside fullOutside
      criticalClosed phaseTenCritical ordinary criticalMass backfillMass total : Nat)
    (hregular : ordinary+ordinaryStops = 2*(contacts+long))
    (hcritical : criticalMass = 2*criticalOutside+triplesOutside+2*fullOutside+4*criticalClosed)
    (hbackfill : backfillMass = 4*phaseTenCritical)
    (hdisjoint : total = ordinary+criticalMass+backfillMass) :
    total+ordinaryStops = 2*(contacts+long)+2*criticalOutside+
      triplesOutside+2*fullOutside+4*criticalClosed+4*phaseTenCritical := by omega

theorem AA_outside_backfill_endpoint_requirement
    (curves contacts long criticalOutside triplesOutside fullOutside phaseTenCritical
      outside : Nat)
    (hturn : 4*curves ≤ contacts)
    (hcount : 2*(contacts+long)+2*criticalOutside+triplesOutside+
      2*fullOutside+2*phaseTenCritical ≤ outside) :
    8*curves+2*long+2*criticalOutside+triplesOutside+2*fullOutside+
      2*phaseTenCritical ≤ outside := by omega

end SubQuorum.CriticalPhaseTenBackfill
