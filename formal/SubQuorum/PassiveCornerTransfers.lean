import SubQuorum.WidthSixBottomOwner

set_option autoImplicit false

namespace SubQuorum.PassiveCornerTransfers

open WidthSixBottomOwner

set_option maxHeartbeats 1000000 in
theorem full_receiver_owner_roles
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hevenLeft : left%2 = 0) (hevenRight : right%2 = 0)
    (hroot : endpoint width left right anchor)
    (hnorthEndpoint : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (-1,0)))
    (hnorthSupport : support width left right
      (pull transpose flipRow flipColumn anchor (-1,0)))
    (hwestEndpoint : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,-1)))
    (hwestSupport : ¬ support width left right
      (pull transpose flipRow flipColumn anchor (0,-1))) :
    (transpose = true ∧ flipRow = false ∧
      ((flipColumn = false ∧ anchor = (0,1)) ∨
       (flipColumn = true ∧ anchor = (0,width)))) ∨
    (transpose = false ∧ flipRow = true ∧
      ((flipColumn = true ∧ anchor = (left,1)) ∨
       (flipColumn = false ∧ anchor = (right,width)))) := by
  rcases anchor with ⟨row,column⟩
  rcases hroot with hbar | ⟨rfl,hrowNear,hleftBound⟩ | ⟨rfl,hrowFar,hrightBound⟩
  · have hrow : row = 0 ∨ row = 1 := by omega
    rcases hrow with rfl | rfl
    all_goals
      cases transpose <;> cases flipRow <;> cases flipColumn <;>
        simp [endpoint, support, pull, Prod.mk.injEq] at hnorthEndpoint hnorthSupport hwestEndpoint hwestSupport ⊢ <;> omega
  all_goals
    cases transpose <;> cases flipRow <;> cases flipColumn <;>
      simp [endpoint, support, pull, Prod.mk.injEq] at hnorthEndpoint hnorthSupport hwestEndpoint hwestSupport ⊢ <;> omega

theorem receiver_roles_are_positive
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hevenWidth : width%2 = 0) (hevenLeft : left%2 = 0) (hevenRight : right%2 = 0)
    (hroles :
      (transpose = true ∧ flipRow = false ∧
        ((flipColumn = false ∧ anchor = (0,1)) ∨
         (flipColumn = true ∧ anchor = (0,width)))) ∨
      (transpose = false ∧ flipRow = true ∧
        ((flipColumn = true ∧ anchor = (left,1)) ∨
         (flipColumn = false ∧ anchor = (right,width))))) :
    positiveParity transpose flipRow flipColumn anchor := by
  rcases hroles with ⟨rfl,rfl,⟨rfl,rfl⟩ | ⟨rfl,rfl⟩⟩ |
    ⟨rfl,rfl,⟨rfl,rfl⟩ | ⟨rfl,rfl⟩⟩ <;>
    simp [positiveParity, hevenWidth, hevenLeft, hevenRight]

def rotorT : List Point :=
  [(0,2),(1,1),(2,5),(1,4),(5,3),(4,4),(3,0),(4,1)]

def candidateRotors : List (Bool × Int × Int) :=
  (([false,true].flatMap fun mirror => rotorP.map fun root =>
    (mirror,1-root.1,2-(if mirror then -root.2 else root.2))).filter fun owner =>
      let points := rotorP.map (rotorMove owner.1 owner.2.1 owner.2.2)
      let selections := rotorT.map (rotorMove owner.1 owner.2.1 owner.2.2)
      !points.contains (0,2) && selections.contains (0,2) &&
        !points.contains (1,1) && !selections.contains (1,1))

theorem unique_rotor_candidate : candidateRotors = [(true,0,4)] := by decide

theorem rotor_candidate_hits_retained_support_neighbor :
    (rotorP.map (rotorMove true 0 4)).contains (2,0) = true := by decide

theorem shared_corner_charging
    (counted direct unactivatedCorner activatedCorner terminal activation boundary : Nat)
    (hpartition : counted = direct+unactivatedCorner+activatedCorner+terminal)
    (hdefects : direct+unactivatedCorner ≤ boundary)
    (hcorner : activatedCorner ≤ activation)
    (hterminal : terminal ≤ activation) : counted ≤ 2*activation+boundary := by omega

theorem corner_reserve_budget
    (counted activation unfilled rotor boundary reserve : Nat)
    (hcount : counted ≤ 2*activation+boundary)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary) :
    counted+boundary+2*unfilled+2*rotor ≤ 4*reserve := by omega

theorem AA_corner_charging
    (counted direct unactivatedCorner activatedCorner terminal activation boundary : Nat)
    (hpartition : counted = direct+unactivatedCorner+activatedCorner+terminal)
    (hdefects : direct+unactivatedCorner ≤ boundary)
    (hcorner : activatedCorner ≤ activation)
    (hterminal : terminal = 0) (hboundary : boundary = 0) :
    counted ≤ activation := by omega

theorem charged_owner_width_bound (width incident long : Int)
    (hwidthEven : width%2 = 0) (hincidentEven : incident%2 = 0)
    (hbarsDisjoint : width-2 < incident+1)
    (hfourStems : incident+10 ≤ long) :
    width ≤ incident+2 ∧ width ≤ long-8 := by omega

theorem two_counted_corners_impossible (width firstLong secondLong : Int)
    (hsecondLong : 4 ≤ secondLong)
    (hlongLegs : firstLong+secondLong+4 ≤ width)
    (hwidth : width ≤ firstLong-8) : False := by omega

theorem opposite_corner_hits_incoming_bar (width incident far incomingWidth : Int)
    (hwidth : width = incident+2) (hincomingWidth : 6 ≤ incomingWidth) :
    endpoint incomingWidth incident far (incident+3-width,2) := by
  simp [endpoint]
  omega

theorem opposite_corner_has_retained_incoming_support (width incident incomingWidth far : Int)
    (hwidth : 6 ≤ width) (hwidthEven : width%2 = 0)
    (hincidentEven : incident%2 = 0) (hless : width ≤ incident)
    (_hincomingWidth : 6 ≤ incomingWidth) :
    support incomingWidth incident far (incident+3-width,2) ∧
    endpoint incomingWidth incident far (incident+3-width,1) := by
  have hodd : (incident+3-width)%2 = 1 := by omega
  simp [endpoint, support, hodd]
  omega

theorem retained_support_cannot_have_two_occupied_neighbors
    (originalSupport occupied selected : Point → Prop) (point first second : Point)
    (hsupport : originalSupport point) (hblank : ¬occupied point)
    (hretention : originalSupport point → ¬occupied point → selected point)
    (hdegree : selected point → ¬(occupied first ∧ occupied second))
    (hfirst : occupied first) (hsecond : occupied second) : False := by
  exact hdegree (hretention hsupport hblank) ⟨hfirst,hsecond⟩

end SubQuorum.PassiveCornerTransfers
