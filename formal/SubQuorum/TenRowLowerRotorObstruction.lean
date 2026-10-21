import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.TenRowLowerRotorObstruction

abbrev Point := Int × Int

def lowerEndpoints (point : Point) : Prop :=
  point ∈ [(4,3),(5,1),(5,2),(5,3),(6,2),(6,3),(6,4),(7,2)]

def lowerSupports (point : Point) : Prop :=
  point ∈ [(3,3),(4,1),(4,4),(5,0),(6,5),(7,1),(7,4),(8,2)]

def retainedBarrier (width : Int) (point : Point) : Prop :=
  (point.2 = 0 ∧ 5 ≤ point.1 ∧ point.1 ≤ 10) ∨
  lowerEndpoints point ∨
  (point.1 = 10 ∧ 1 ≤ point.2 ∧ point.2 ≤ width)

def verticalRotor (south mirrored : Bool) (point : Point) : Prop :=
  (if south then point.1-7 else 7-point.1,
   if mirrored then 1-point.2 else point.2-1) ∈
    [(0,0),(1,0),(1,1),(1,2),(2,-1),(2,0),(2,1),(3,1)]

inductive ActualMode where
  | down
  | up
  | longUp
  | upperRotor
  deriving DecidableEq

def isolatedGain (mode : ActualMode) (breadth : Int) : Int :=
  match mode with
  | .down => breadth
  | .up | .longUp | .upperRotor => 3

def jointGain (left right : ActualMode) (leftBreadth rightBreadth : Int)
    (tight : Bool) : Int :=
  isolatedGain left leftBreadth + isolatedGain right rightBreadth -
    if tight && ((left == .longUp && right == .upperRotor) ||
      (right == .longUp && left == .upperRotor)) then 1 else 0

def gainSum (gains : List Int) : Int :=
  match gains with
  | [] => 0
  | gain :: rest => gain + gainSum rest

theorem gate_is_original_support :
    lowerSupports (7,1) ∧ ¬ lowerEndpoints (7,1) := by
  simp [lowerSupports,lowerEndpoints]

theorem gate_has_two_retained_neighbours (width : Int) :
    retainedBarrier width (7,0) ∧ lowerEndpoints (7,2) := by
  simp [retainedBarrier,lowerEndpoints]

theorem five_point_stem_hits_barrier (occupied : Int → Prop)
    (gate lower upper : Int)
    (hgate : lower ≤ gate ∧ gate ≤ upper) (hdepth : 4 ≤ upper-lower)
    (hstem : ∀ row : Int, lower ≤ row → row ≤ upper → occupied row) :
    occupied (gate-2) ∨ occupied (gate+3) := by
  by_cases hlow : lower ≤ gate-2
  · exact Or.inl (hstem _ hlow (by omega))
  · exact Or.inr (hstem _ (by omega) (by omega))

theorem arbitrary_vertical_stem_collision (occupied : Point → Prop)
    (width lower upper : Int) (hwidth : 6 ≤ width)
    (hgate : lower ≤ 7 ∧ 7 ≤ upper) (hdepth : 4 ≤ upper-lower)
    (hstem : ∀ row : Int, lower ≤ row → row ≤ upper → occupied (row,1)) :
    ∃ point, occupied point ∧ retainedBarrier width point := by
  have hhits := five_point_stem_hits_barrier (fun row => occupied (row,1))
    7 lower upper hgate hdepth hstem
  rcases hhits with hlow | hhigh
  · exact ⟨(5,1),hlow,by simp [retainedBarrier,lowerEndpoints]⟩
  · refine ⟨(10,1),hhigh,?_⟩
    simp [retainedBarrier,lowerEndpoints]
    omega

theorem vertical_rotor_hits_wall (south mirrored : Bool) :
    verticalRotor south mirrored (if south then 9 else 5,0) := by
  cases south <;> cases mirrored <;> simp [verticalRotor]

theorem all_vertical_rotors_collide (width : Int) (south mirrored : Bool) :
    ∃ point, verticalRotor south mirrored point ∧ retainedBarrier width point := by
  refine ⟨(if south then 9 else 5,0),vertical_rotor_hits_wall south mirrored,?_⟩
  cases south <;> simp [retainedBarrier,lowerEndpoints]

theorem shared_owner_gain (width : Int) (down : Bool) (hwidth : 6 ≤ width) :
    5 ≤ if down then width+1 else 5 := by
  cases down <;> omega

theorem actual_distinct_joint_gain (left right : ActualMode)
    (leftBreadth rightBreadth : Int) (tight : Bool)
    (hleft : left = .down → 6 ≤ leftBreadth)
    (hright : right = .down → 6 ≤ rightBreadth) :
    5 ≤ jointGain left right leftBreadth rightBreadth tight := by
  cases left <;> cases right <;> cases tight <;>
    simp [jointGain,isolatedGain] at * <;> omega

theorem gain_sum_five (gains : List Int) (hgains : ∀ gain ∈ gains, 5 ≤ gain) :
    5*(gains.length : Int) ≤ gainSum gains := by
  induction gains with
  | nil => simp [gainSum]
  | cons gain rest inductionHypothesis =>
    have hgain : 5 ≤ gain := hgains gain (by simp)
    have hrest : 5*(rest.length : Int) ≤ gainSum rest :=
      inductionHypothesis (by intro value hvalue; exact hgains value (by simp [hvalue]))
    simp only [List.length_cons,Int.natCast_add,Int.natCast_one,gainSum]
    omega

theorem all_width_selected_bound (amount : Int) (gains : List Int)
    (hcount : (gains.length : Int) = amount-1)
    (hgains : ∀ gain ∈ gains, 5 ≤ gain) :
    4*(amount-1) ≤ 1-amount+gainSum gains := by
  have hsum := gain_sum_five gains hgains
  omega

theorem mixed_spacing_selected_bound (amount selectedGaps : Int) (gains : List Int)
    (hcount : (gains.length : Int) = selectedGaps)
    (hgains : ∀ gain ∈ gains, 5 ≤ gain) :
    5*selectedGaps-(amount-1) ≤ 1-amount+gainSum gains := by
  have hsum := gain_sum_five gains hgains
  omega

theorem mixed_spacing_density_criterion (amount selectedGaps : Int) (gains : List Int)
    (hcount : (gains.length : Int) = selectedGaps)
    (hgains : ∀ gain ∈ gains, 5 ≤ gain) (hdensity : amount-1 ≤ 5*selectedGaps) :
    0 ≤ 1-amount+gainSum gains := by
  have hbound := mixed_spacing_selected_bound amount selectedGaps gains hcount hgains
  omega

end SubQuorum.TenRowLowerRotorObstruction
