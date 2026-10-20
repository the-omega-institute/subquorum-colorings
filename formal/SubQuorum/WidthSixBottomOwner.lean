import Std

set_option autoImplicit false

namespace SubQuorum.WidthSixBottomOwner

abbrev Point := Int × Int

def endpoint (width left right : Int) (point : Point) : Prop :=
  (0 ≤ point.1 ∧ point.1 ≤ 1 ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (point.2 = 1 ∧ 2 ≤ point.1 ∧ point.1 ≤ left) ∨
  (point.2 = width ∧ 2 ≤ point.1 ∧ point.1 ≤ right)

def pull (transpose flipRow flipColumn : Bool) (anchor point : Point) : Point :=
  (anchor.1 + (if flipRow then -1 else 1) *
    (if transpose then point.2 else point.1),
   anchor.2 + (if flipColumn then -1 else 1) *
    (if transpose then point.1 else point.2))

def blockers : List Point :=
  [(-1,0),(-1,1),(-1,2),(-1,3),(-1,4),(-1,5),
   (0,-1),(1,-1),(2,-1)]

def support (width left right : Int) (point : Point) : Prop :=
  (point.1 = 0 ∧ (point.2 = 0 ∨ point.2 = width+1)) ∨
  (point.1 = left+1 ∧ point.2 = 1) ∨
  (point.1 = right+1 ∧ point.2 = width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ left ∧
    ((point.1%2 = 0 ∧ point.2 = 0) ∨ (point.1%2 = 1 ∧ point.2 = 2))) ∨
  (2 ≤ point.1 ∧ point.1 ≤ right ∧
    ((point.1%2 = 0 ∧ point.2 = width+1) ∨
     (point.1%2 = 1 ∧ point.2 = width-1)))

set_option maxHeartbeats 1000000 in
theorem blocked_vertical_owner_is_horizontal_tip
    (width left right distance : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hdistance : distance = 1 ∨ distance = 2 ∨ distance = 4)
    (hroot : endpoint width left right anchor)
    (hup : ¬ endpoint width left right (pull transpose flipRow flipColumn anchor (-1,0)))
    (hleftward : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,-1)))
    (hblank : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (distance,0))) :
    transpose = true ∧ flipRow = true ∧
    ((anchor.1 = left ∧ anchor.2 = 1) ∨
     (anchor.1 = right ∧ anchor.2 = width)) := by
  rcases anchor with ⟨row,column⟩
  rcases hroot with hbar | hnear | hfar
  all_goals
    rcases hdistance with rfl | rfl | rfl <;>
      cases transpose <;> cases flipRow <;> cases flipColumn <;>
      simp [pull, endpoint] at hup hleftward hblank ⊢ <;> omega

theorem terminal_avoiding_lower_support_points_down
    (width left right : Int) (anchor : Point) (flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hevenLeft : left%2 = 0) (hevenRight : right%2 = 0)
    (htip : (anchor.1 = left ∧ anchor.2 = 1) ∨
      (anchor.1 = right ∧ anchor.2 = width))
    (hblank : ¬ support width left right
      (pull true true flipColumn anchor (1,0))) :
    (anchor.1 = left ∧ anchor.2 = 1 ∧ flipColumn = false) ∨
    (anchor.1 = right ∧ anchor.2 = width ∧ flipColumn = true) := by
  rcases anchor with ⟨row,column⟩
  rcases htip with ⟨rfl,rfl⟩ | ⟨rfl,rfl⟩
  · cases flipColumn
    · exact Or.inl ⟨rfl,rfl,rfl⟩
    · exfalso
      apply hblank
      simp [pull, support, hevenLeft]
      omega
  · cases flipColumn
    · exfalso
      apply hblank
      simp [pull, support, hevenRight]
      omega
    · exact Or.inr ⟨rfl,rfl,rfl⟩

theorem downward_terminal_receiver_profile (width incident far : Int)
    (hwidth : 6 ≤ width) (hincident : 4 ≤ incident)
    (heven : incident%2 = 0) :
    endpoint width incident far (incident,1) ∧
    endpoint width incident far (incident-1,1) ∧
    support width incident far (incident-1,2) ∧
    ¬ endpoint width incident far (incident,2) ∧
    ¬ support width incident far (incident,2) := by
  have hodd : (incident-1)%2 = 1 := by omega
  refine ⟨?_,?_,?_,?_,?_⟩
  · simp [endpoint]
    omega
  · simp [endpoint]
    omega
  · simp [support, hodd]
    omega
  · simp [endpoint]
    omega
  · simp [support, heven]
    omega

def rotorP : List Point :=
  [(1,2),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(4,3)]

def rotorMove (mirror : Bool) (row column : Int) (point : Point) : Point :=
  (point.1+row,(if mirror then -point.2 else point.2)+column)

def rotorOwners (blocked : List Point) : List (Bool × Int × Int) :=
  (([false,true].flatMap fun mirror => rotorP.map fun tip =>
    (mirror,-tip.1,-(if mirror then -tip.2 else tip.2))).filter fun owner =>
      (rotorP.map (rotorMove owner.1 owner.2.1 owner.2.2)).all fun point =>
        !blocked.contains point)

theorem bottom_point_has_no_rotor_owner : rotorOwners blockers = [] := by decide

theorem second_point_has_no_rotor_owner :
    rotorOwners [(-1,0),(-1,1),(-1,2),(-1,3),(0,-1),(1,0)] = [] := by decide

theorem clearance_four_last_receiver_hits_forbidden_point (long outer : Int)
    (hclearance : long = outer+4) :
    (outer+5,2) = (long+1,2) := by
  congr 1
  omega

def positiveParity (transpose flipRow flipColumn : Bool) (anchor : Point) : Prop :=
  anchor.1%2 = (if transpose then (if flipRow then 1 else 0)
    else (if flipRow then 0 else 1)) ∧
  anchor.2%2 = (if transpose then (if flipColumn then 0 else 1)
    else (if flipColumn then 1 else 0))

set_option maxHeartbeats 1000000 in
theorem positive_bottom_role_catalogue
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hevenWidth : width%2 = 0) (hevenLeft : left%2 = 0) (hevenRight : right%2 = 0)
    (hroot : endpoint width left right anchor)
    (hup : ¬ endpoint width left right (pull transpose flipRow flipColumn anchor (-1,0)))
    (hwest : ¬ endpoint width left right (pull transpose flipRow flipColumn anchor (0,-1)))
    (hphase : positiveParity transpose flipRow flipColumn anchor) :
    (transpose = true ∧ flipRow = false ∧
      ((flipColumn = false ∧ anchor = (0,1)) ∨
       (flipColumn = true ∧ anchor = (0,width)))) ∨
    (transpose = false ∧ flipRow = true ∧
      ((flipColumn = true ∧ anchor = (left,1)) ∨
       (flipColumn = false ∧ anchor = (right,width)))) := by
  rcases anchor with ⟨row,column⟩
  rcases hroot with hbar | hnear | hfar
  all_goals
    cases transpose <;> cases flipRow <;> cases flipColumn <;>
      simp [pull, endpoint, positiveParity, Prod.mk.injEq] at hup hwest hphase ⊢ <;> omega

theorem westward_terminal_cannot_fit
    (width incident far clearance : Int)
    (hwidth : 6 ≤ width) (hincident : 4 ≤ incident) (hclearance : 4 ≤ clearance)
    (hevenIncident : incident%2 = 0) (hevenClearance : clearance%2 = 0)
    (hblank : ¬ endpoint width incident far (incident-(clearance-2),1))
    (hwall : ∀ row, 0 ≤ row → row ≤ clearance-3 →
      ¬ endpoint width incident far (incident-row,2)) : False := by
  have hfit : incident ≤ clearance-4 := by
    simp [endpoint] at hblank
    omega
  have hcollision := hwall (incident-1) (by omega) (by omega)
  apply hcollision
  simp [endpoint]
  omega

theorem positive_vertical_bar_fits_clearance
    (width left right clearance : Int)
    (hwidth : 6 ≤ width) (hclearance : 4 ≤ clearance)
    (hevenWidth : width%2 = 0) (hevenClearance : clearance%2 = 0)
    (hblankEndpoint : ¬ endpoint width left right (0,clearance-1))
    (hblankSupport : ¬ support width left right (0,clearance-1)) :
    width ≤ clearance-4 := by
  simp [endpoint] at hblankEndpoint
  simp [support] at hblankSupport
  omega

theorem two_positive_legs_pay_distinct_occurrences
    (nearActivated farActivated : Bool) (activation exterior : Nat)
    (hactivation : (if nearActivated then 1 else 0)+(if farActivated then 1 else 0)+1 ≤ activation)
    (hexterior : (if nearActivated then 0 else 1)+(if farActivated then 0 else 1) ≤ exterior) :
    3 ≤ activation+exterior := by
  cases nearActivated <;> cases farActivated <;> simp_all <;> omega

theorem positive_bottom_owner_needs_two_reserves
    (activation exterior unfilled boundary rotor reserve : Nat)
    (hoccurrences : 3 ≤ activation+exterior)
    (hpool : exterior ≤ unfilled+boundary)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary) :
    2 ≤ reserve := by omega

end SubQuorum.WidthSixBottomOwner
