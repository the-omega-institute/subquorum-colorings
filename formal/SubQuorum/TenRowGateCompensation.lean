import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.TenRowGateCompensation

abbrev Point := Int × Int

inductive Mode where
  | down
  | up
  | longUp
  | lowerRotor
  | upperRotor
  deriving DecidableEq

def isU (mode : Mode) : Bool :=
  match mode with
  | .down | .up | .longUp => true
  | .lowerRotor | .upperRotor => false

def isolatedGain (mode : Mode) (breadth : Int) : Int :=
  match mode with
  | .down => breadth
  | .up | .longUp | .upperRotor => 3
  | .lowerRotor => 2

def crossDebit (left right : Mode) : Bool :=
  isU left != isU right &&
    (left == .lowerRotor || right == .lowerRotor ||
      left == .longUp || right == .longUp)

def jointGain (left right : Mode) (leftBreadth rightBreadth : Int)
    (tight : Bool) : Int :=
  isolatedGain left leftBreadth + isolatedGain right rightBreadth -
    if tight && crossDebit left right then 1 else 0

def gainSum (gains : List Int) : Int :=
  match gains with
  | [] => 0
  | gain :: rest => gain + gainSum rest

def leftRotor (upper : Bool) (point : Point) : Prop :=
  point ∈ if upper then
    [(3,2),(4,2),(4,3),(4,4),(5,1),(5,2),(5,3),(6,3)]
  else [(4,3),(5,1),(5,2),(5,3),(6,2),(6,3),(6,4),(7,2)]

def rightRotor (upper : Bool) (width : Int) (point : Point) : Prop :=
  leftRotor upper (point.1,width+1-point.2)

theorem near_depth_four (depth : Int) (hmin : 4 ≤ depth)
    (hblocked : depth < 6) (heven : depth % 2 = 0) : depth = 4 := by omega

theorem far_depth_four_or_six (depth : Int) (hmin : 4 ≤ depth)
    (hblocked : depth < 8) (heven : depth % 2 = 0) : depth = 4 ∨ depth = 6 := by omega

theorem nonspanning_even_breadth (width breadth : Int)
    (hwidth : width % 2 = 0) (hbreadth : breadth % 2 = 0)
    (hinside : breadth < width) : breadth ≤ width-2 := by omega

theorem down_receipt (breadth indicator : Int)
    (hindicator : indicator = 0 ∨ indicator = 1) :
    (breadth-1)+2*(3*(1+indicator))-5*(1+indicator) = breadth+indicator := by
  rcases hindicator with hzero | hone <;> omega

theorem up_receipt (indicator : Int) :
    1+2*(3*(1+indicator))-4*(1+indicator) = 3+2*indicator := by omega

theorem isolated_gain_lower (mode : Mode) (breadth : Int)
    (hbreadth : isU mode = true → 6 ≤ breadth) :
    2 ≤ isolatedGain mode breadth := by
  cases mode <;> simp [isolatedGain, isU] at * <;> omega

theorem joint_gain_lower (left right : Mode) (leftBreadth rightBreadth : Int)
    (tight : Bool) (hleft : isU left = true → 6 ≤ leftBreadth)
    (hright : isU right = true → 6 ≤ rightBreadth) :
    4 ≤ jointGain left right leftBreadth rightBreadth tight := by
  cases left <;> cases right <;> cases tight <;>
    simp [jointGain, isolatedGain, crossDebit, isU] at * <;> omega

theorem shared_up_gain : 5 ≤ (1 : Int)+2*6-8 := by omega

theorem shared_down_gain (width : Int) (hwidth : 6 ≤ width) :
    5 ≤ (width-1)+2*6-10 := by omega

theorem two_U_overlap (left right : Point → Prop)
    (width leftBreadth rightBreadth barRow : Int)
    (hwidth : rightBreadth ≤ width) (hoverlap : width < leftBreadth+rightBreadth)
    (hrow : 5 ≤ barRow ∧ barRow ≤ 9)
    (hleft : ∀ column : Int, 1 ≤ column → column ≤ leftBreadth → left (barRow,column))
    (hright : ∀ row : Int, 5 ≤ row → row ≤ 9 → right (row,width+1-rightBreadth)) :
    ∃ point, left point ∧ right point := by
  exact ⟨(barRow,width+1-rightBreadth),
    hleft _ (by omega) (by omega), hright _ hrow.1 hrow.2⟩

theorem U_rotor_overlap (original rotor : Point → Prop) (width breadth : Int)
    (hwidth : width % 2 = 0) (hbreadth : breadth % 2 = 0)
    (hinside : breadth ≤ width) (hoverlap : width < breadth+4)
    (horiginal : original (5,breadth))
    (hrotor : rotor (5,width) ∧ rotor (5,width-2)) :
    ∃ point, original point ∧ rotor point := by
  have halternatives : breadth = width ∨ breadth = width-2 := by omega
  rcases halternatives with hfull | hnear
  · exact ⟨(5,breadth),horiginal,by simpa [hfull] using hrotor.1⟩
  · exact ⟨(5,breadth),horiginal,by simpa [hnear] using hrotor.2⟩

theorem width_six_rotors_collide (leftUpper rightUpper : Bool) :
    ∃ point, leftRotor leftUpper point ∧ rightRotor rightUpper 6 point := by
  cases leftUpper <;> cases rightUpper
  · exact ⟨(6,3),by simp [leftRotor],by simp [rightRotor,leftRotor]⟩
  · exact ⟨(4,3),by simp [leftRotor],by simp [rightRotor,leftRotor]⟩
  · exact ⟨(4,4),by simp [leftRotor],by simp [rightRotor,leftRotor]⟩
  · exact ⟨(4,3),by simp [leftRotor],by simp [rightRotor,leftRotor]⟩

theorem different_gap_rows (origin spacing firstRow secondRow : Int)
    (hspacing : 10 ≤ spacing)
    (hfirst : origin+3 ≤ firstRow ∧ firstRow ≤ origin+9)
    (hsecond : origin+spacing+3 ≤ secondRow ∧ secondRow ≤ origin+spacing+9) :
    firstRow / 2 < secondRow / 2 := by omega

theorem different_gap_owners (origin spacing row : Int) (hspacing : 10 ≤ spacing)
    (hfirst : origin+3 ≤ row ∧ row ≤ origin+9) :
    ¬ (origin+spacing+3 ≤ row ∧ row ≤ origin+spacing+9) := by omega

theorem boundary_bands_distinct (width : Int) (hwidth : 6 ≤ width) : width / 2 ≠ 0 := by omega

theorem width_six_requires_shared_owner (leftRadius rightRadius : Int)
    (hleft : 4 ≤ leftRadius) (hright : 4 ≤ rightRadius) :
    ¬ leftRadius+rightRadius ≤ 6 := by omega

theorem gain_sum_lower (gains : List Int) (floor : Int)
    (hgains : ∀ gain ∈ gains, floor ≤ gain) :
    floor*(gains.length : Int) ≤ gainSum gains := by
  induction gains with
  | nil => simp [gainSum]
  | cons gain rest inductionHypothesis =>
    have hgain : floor ≤ gain := hgains gain (by simp)
    have hrest : floor*(rest.length : Int) ≤ gainSum rest :=
      inductionHypothesis (by intro value hvalue; exact hgains value (by simp [hvalue]))
    simp only [List.length_cons, Int.natCast_add, Int.natCast_one, Int.mul_add, Int.mul_one, gainSum]
    omega

theorem simultaneous_selected_bound (amount : Int) (gains : List Int)
    (hcount : (gains.length : Int) = amount-1)
    (hgains : ∀ gain ∈ gains, 4 ≤ gain) :
    3*(amount-1) ≤ 1-amount+gainSum gains := by
  have hsum := gain_sum_lower gains 4 hgains
  omega

theorem width_six_selected_bound (amount : Int) (gains : List Int)
    (hcount : (gains.length : Int) = amount-1)
    (hgains : ∀ gain ∈ gains, 5 ≤ gain) :
    4*(amount-1) ≤ 1-amount+gainSum gains := by
  have hsum := gain_sum_lower gains 5 hgains
  omega

end SubQuorum.TenRowGateCompensation
