import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxHeartbeats 4000000

namespace SubQuorum.TenRowCompleteChambers

abbrev Point := Int × Int

def adjacent (first second : Point) : Prop :=
  (first.1 = second.1 ∧ (first.2+1 = second.2 ∨ second.2+1 = first.2)) ∨
  (first.2 = second.2 ∧ (first.1+1 = second.1 ∨ second.1+1 = first.1))

inductive SourceWalk (vertices : Point → Prop) : Point → Point → Prop where
  | stay (point : Point) (hpoint : vertices point) : SourceWalk vertices point point
  | advance {start finish next : Point} (path : SourceWalk vertices start finish)
      (hnext : vertices next) (hstep : adjacent finish next) : SourceWalk vertices start next

def pocketRows (point : Point) : Prop :=
  (2 ≤ point.1 ∧ point.1 ≤ 4) ∨ (7 ≤ point.1 ∧ point.1 ≤ 9)

def uEndpoints (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def framed (transpose reverseRow reverseColumn : Bool) (offset point : Point) : Point :=
  let row := if reverseRow then -point.1 else point.1
  let column := if reverseColumn then -point.2 else point.2
  if transpose then (offset.1+column, offset.2+row)
  else (offset.1+row, offset.2+column)

def rotorEndpoints : List Point :=
  [(1,2),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(4,3)]

def pocketFirst : List Point :=
  [(0,1),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(3,2)]

def pocketFirstSupports : List Point :=
  [(-1,1),(0,0),(0,3),(1,4),(2,-1),(3,0),(3,3),(4,2)]

def pocketPoint (index : Fin 6) (point : Point) : Point :=
  (point.1+(index.val/2 : Nat), if index.val%2 = 0 then point.2 else 3-point.2)

def pocketRotor (index : Fin 6) : List Point :=
  pocketFirst.map (pocketPoint index)

def pocketSupports (index : Fin 6) : List Point :=
  pocketFirstSupports.map (pocketPoint index)

def pocketWitness (index : Fin 6) : Point :=
  [(0,0),(0,0),(0,1),(0,2),(2,0),(2,0)][index.val]

def witnessAnchor (index : Fin 6) : Point :=
  [(0,1),(1,0),(1,1),(1,2),(2,1),(3,0)][index.val]

def witnessBlocker (index : Fin 6) : Point :=
  [(-1,0),(-1,0),(-1,1),(-1,2),(2,-1),(2,-1)][index.val]

def boundary (point : Point) : Prop :=
  ((point.1 = -1 ∨ point.1 = 6) ∧ -1 ≤ point.2 ∧ point.2 ≤ 4) ∨
  ((point.2 = -1 ∨ point.2 = 4) ∧ -1 ≤ point.1 ∧ point.1 ≤ 6)

def overlap (first second : Fin 6) : Bool :=
  (pocketRotor first).any fun point => (pocketRotor second).contains point

def firstUpperRotor : List Point :=
  [(3,2),(4,2),(4,3),(4,4),(5,1),(5,2),(5,3),(6,3)]

def reflectedUpperRotor : List Point :=
  firstUpperRotor.map fun point => (point.1,7-point.2)

theorem adjacent_cannot_cross_pockets (first second : Point)
    (hfirst : 2 ≤ first.1 ∧ first.1 ≤ 4) (hsecond : pocketRows second)
    (hstep : adjacent first second) : 2 ≤ second.1 ∧ second.1 ≤ 4 := by
  simp only [pocketRows,adjacent] at *
  omega

theorem upper_walk_stays_upper (vertices : Point → Prop)
    (hrows : ∀ point, vertices point → pocketRows point)
    {start finish : Point} (path : SourceWalk vertices start finish) :
    (2 ≤ start.1 ∧ start.1 ≤ 4) → (2 ≤ finish.1 ∧ finish.1 ≤ 4) := by
  induction path with
  | stay hpoint => exact fun hstart => hstart
  | @advance finish next path hnext hstep inductionHypothesis =>
    intro hstart
    exact adjacent_cannot_cross_pockets finish next
      (inductionHypothesis hstart) (hrows next hnext) hstep

theorem connected_source_has_one_short_band (vertices : Point → Prop)
    (hrows : ∀ point, vertices point → pocketRows point)
    (hconnected : ∀ first second, vertices first → vertices second → SourceWalk vertices first second) :
    (∀ point, vertices point → 2 ≤ point.1 ∧ point.1 ≤ 4) ∨
      (∀ point, vertices point → 7 ≤ point.1 ∧ point.1 ≤ 9) := by
  by_cases hupper : ∃ point, vertices point ∧ 2 ≤ point.1 ∧ point.1 ≤ 4
  · obtain ⟨anchor,hanchor,hanchorRows⟩ := hupper
    left
    intro point hpoint
    exact upper_walk_stays_upper vertices hrows (hconnected anchor point hanchor hpoint) hanchorRows
  · right
    intro point hpoint
    have hpointRows := hrows point hpoint
    have hnot : ¬ (2 ≤ point.1 ∧ point.1 ≤ 4) := by
      intro hbad
      exact hupper ⟨point,hpoint,hbad⟩
    exact hpointRows.resolve_left hnot

theorem full_u_cannot_fit_three_rows (breadth near far lower : Int)
    (hbreadth : 6 ≤ breadth) (hnear : 4 ≤ near) (_hfar : 4 ≤ far)
    (transpose reverseRow reverseColumn : Bool) (offset : Point)
    (hfit : ∀ point, uEndpoints breadth near far point →
      lower ≤ (framed transpose reverseRow reverseColumn offset point).1 ∧
        (framed transpose reverseRow reverseColumn offset point).1 ≤ lower+2) : False := by
  have hbarFirst : uEndpoints breadth near far (0,1) := by simp [uEndpoints]; omega
  have hbarLast : uEndpoints breadth near far (0,breadth) := by simp [uEndpoints]; omega
  have hstemLast : uEndpoints breadth near far (near,1) := by simp [uEndpoints]; omega
  have hfirst := hfit (0,1) hbarFirst
  have hlast := hfit (0,breadth) hbarLast
  have hstem := hfit (near,1) hstemLast
  cases transpose <;> cases reverseRow <;> cases reverseColumn <;>
    simp only [framed,Bool.false_eq_true,if_false,if_true] at * <;> omega

theorem full_u_cannot_fit_four_columns (breadth near far lower : Int)
    (hbreadth : 6 ≤ breadth) (hnear : 4 ≤ near) (_hfar : 4 ≤ far)
    (transpose reverseRow reverseColumn : Bool) (offset : Point)
    (hfit : ∀ point, uEndpoints breadth near far point →
      lower ≤ (framed transpose reverseRow reverseColumn offset point).2 ∧
        (framed transpose reverseRow reverseColumn offset point).2 ≤ lower+3) : False := by
  have hbarFirst : uEndpoints breadth near far (0,1) := by simp [uEndpoints]; omega
  have hbarLast : uEndpoints breadth near far (0,breadth) := by simp [uEndpoints]; omega
  have hstemLast : uEndpoints breadth near far (near,1) := by simp [uEndpoints]; omega
  have hfirst := hfit (0,1) hbarFirst
  have hlast := hfit (0,breadth) hbarLast
  have hstem := hfit (near,1) hstemLast
  cases transpose <;> cases reverseRow <;> cases reverseColumn <;>
    simp only [framed,Bool.false_eq_true,if_false,if_true] at * <;> omega

theorem rotor_cannot_fit_three_rows (lower : Int)
    (transpose reverseRow reverseColumn : Bool) (offset : Point)
    (hfit : ∀ point ∈ rotorEndpoints,
      lower ≤ (framed transpose reverseRow reverseColumn offset point).1 ∧
        (framed transpose reverseRow reverseColumn offset point).1 ≤ lower+2) : False := by
  have htop := hfit (1,2) (by simp [rotorEndpoints])
  have hbottom := hfit (4,3) (by simp [rotorEndpoints])
  have hleft := hfit (3,1) (by simp [rotorEndpoints])
  have hright := hfit (2,4) (by simp [rotorEndpoints])
  cases transpose <;> cases reverseRow <;> cases reverseColumn <;>
    simp only [framed,Bool.false_eq_true,if_false,if_true] at * <;> omega

theorem six_rotors_always_overlap : ∀ first second : Fin 6, overlap first second = true := by decide

theorem pocket_witness_original_support : ∀ index : Fin 6,
    (pocketSupports index).contains (pocketWitness index) = true := by decide

theorem pocket_witness_not_own_endpoint : ∀ index : Fin 6,
    (pocketRotor index).contains (pocketWitness index) = false := by decide

theorem witness_has_own_anchor : ∀ index : Fin 6,
    (pocketRotor index).contains (witnessAnchor index) = true := by decide

theorem witness_has_two_distinct_neighbours : ∀ index : Fin 6,
    adjacent (pocketWitness index) (witnessAnchor index) ∧
      adjacent (pocketWitness index) (witnessBlocker index) ∧
      witnessAnchor index ≠ witnessBlocker index := by
  unfold adjacent
  decide

theorem witness_blocker_on_boundary : ∀ index : Fin 6, boundary (witnessBlocker index) := by
  unfold boundary
  decide

theorem no_complete_rotor_choice (chosen : Fin 6 → Prop)
    (hdisjoint : ∀ first second, chosen first → chosen second →
      first ≠ second → overlap first second = false)
    (hconsume : ∀ index, chosen index → ∃ other, chosen other ∧
      (pocketRotor other).contains (pocketWitness index) = true) :
    ∀ index, ¬ chosen index := by
  intro index hindex
  obtain ⟨other,hother,hcontains⟩ := hconsume index hindex
  by_cases hequal : index = other
  · subst other
    have hnot := pocket_witness_not_own_endpoint index
    rw [hnot] at hcontains
    cases hcontains
  · have hfalse := hdisjoint index other hindex hother hequal
    have htrue := six_rotors_always_overlap index other
    rw [hfalse] at htrue
    cases htrue

theorem upper_gate_rotors_collide :
    (firstUpperRotor.contains (4,3) && reflectedUpperRotor.contains (4,3) &&
      firstUpperRotor.contains (4,4) && reflectedUpperRotor.contains (4,4)) = true := by decide

theorem canonical_u_north_terminal_continues (breadth near far row column : Int)
    (hbreadth : 6 ≤ breadth) (hnear : 4 ≤ near) (hfar : 4 ≤ far)
    (hpoint : uEndpoints breadth near far (row,column))
    (heast : ¬ uEndpoints breadth near far (row,column+1))
    (hwest : ¬ uEndpoints breadth near far (row,column-1))
    (hsouth : ¬ uEndpoints breadth near far (row+1,column)) :
    uEndpoints breadth near far (row-2,column) := by
  rcases hpoint with hbar | hleft | hright
  · rcases hbar with ⟨hrow,hcolumnLower,hcolumnUpper⟩
    by_cases hcolumn : column < breadth
    · exact False.elim (heast (Or.inl ⟨hrow,by omega,by omega⟩))
    · exact False.elim (hwest (Or.inl ⟨hrow,by omega,by omega⟩))
  · rcases hleft with ⟨hrowLower,hrowUpper,hcolumn⟩
    have hterminal : row = near := by
      by_cases hequal : row = near
      · exact hequal
      · exact False.elim (hsouth (Or.inr (Or.inl ⟨by omega,by omega,hcolumn⟩)))
    exact Or.inr (Or.inl ⟨by omega,by omega,hcolumn⟩)
  · rcases hright with ⟨hrowLower,hrowUpper,hcolumn⟩
    have hterminal : row = far := by
      by_cases hequal : row = far
      · exact hequal
      · exact False.elim (hsouth (Or.inr (Or.inr ⟨by omega,by omega,hcolumn⟩)))
    exact Or.inr (Or.inr ⟨by omega,by omega,hcolumn⟩)

theorem canonical_u_no_other_single_direction (breadth near far row column : Int)
    (hbreadth : 6 ≤ breadth) (_hnear : 4 ≤ near) (_hfar : 4 ≤ far)
    (hpoint : uEndpoints breadth near far (row,column))
    (hnorth : ¬ uEndpoints breadth near far (row-1,column)) :
    (uEndpoints breadth near far (row,column-1) ∧ uEndpoints breadth near far (row+1,column)) ∨
      (uEndpoints breadth near far (row,column+1) ∧ uEndpoints breadth near far (row+1,column)) ∨
      (uEndpoints breadth near far (row,column-1) ∧ uEndpoints breadth near far (row,column+1)) := by
  rcases hpoint with hbar | hleft | hright
  · rcases hbar with ⟨hrow,hcolumnLower,hcolumnUpper⟩
    have hzero : row = 0 := by
      rcases hrow with hzero | hone
      · exact hzero
      · exact False.elim (hnorth (Or.inl ⟨Or.inl (by omega),hcolumnLower,hcolumnUpper⟩))
    have hsouth : uEndpoints breadth near far (row+1,column) :=
      Or.inl ⟨Or.inr (by omega),hcolumnLower,hcolumnUpper⟩
    by_cases hfirst : column = 1
    · exact Or.inr (Or.inl ⟨Or.inl ⟨Or.inl hzero,by omega,by omega⟩,hsouth⟩)
    · by_cases hlast : column = breadth
      · exact Or.inl ⟨Or.inl ⟨Or.inl hzero,by omega,by omega⟩,hsouth⟩
      · exact Or.inr (Or.inr ⟨Or.inl ⟨Or.inl hzero,by omega,by omega⟩,
          Or.inl ⟨Or.inl hzero,by omega,by omega⟩⟩)
  · rcases hleft with ⟨hrowLower,hrowUpper,hcolumn⟩
    by_cases htwo : row = 2
    · exact False.elim (hnorth (Or.inl ⟨Or.inr (by omega),by omega,by omega⟩))
    · exact False.elim (hnorth (Or.inr (Or.inl ⟨by omega,by omega,hcolumn⟩)))
  · rcases hright with ⟨hrowLower,hrowUpper,hcolumn⟩
    by_cases htwo : row = 2
    · exact False.elim (hnorth (Or.inl ⟨Or.inr (by omega),by omega,by omega⟩))
    · exact False.elim (hnorth (Or.inr (Or.inr ⟨by omega,by omega,hcolumn⟩)))

theorem rotor_single_direction_continues : ∀ role near : Fin 8,
    adjacent rotorEndpoints[role.val] rotorEndpoints[near.val] →
    (∀ other : Fin 8, adjacent rotorEndpoints[role.val] rotorEndpoints[other.val] →
      rotorEndpoints[other.val] = rotorEndpoints[near.val]) →
    (2*rotorEndpoints[near.val].1-rotorEndpoints[role.val].1,
      2*rotorEndpoints[near.val].2-rotorEndpoints[role.val].2) ∈ rotorEndpoints := by
  unfold adjacent
  decide

theorem complete_width_six_budget (gaps downward : Int) :
    -gaps+7*downward+5*(gaps-downward) = 4*gaps+2*downward := by omega

theorem spanning_downward_gain (width : Int) :
    width-1+2*6-10 = width+1 := by omega

theorem excluded_rotor_chain_value (amount : Int) : 4-(amount-1) = 5-amount := by omega

theorem general_rotor_chain_value (gaps amount : Int) :
    -gaps+5-(amount-1) = 6-gaps-amount := by omega

theorem rotor_chain_chamber_marginal (amount : Int) : 5-(amount-1) = 6-amount := by omega

end SubQuorum.TenRowCompleteChambers

#print axioms SubQuorum.TenRowCompleteChambers.Point
#print axioms SubQuorum.TenRowCompleteChambers.adjacent
#print axioms SubQuorum.TenRowCompleteChambers.SourceWalk
#print axioms SubQuorum.TenRowCompleteChambers.pocketRows
#print axioms SubQuorum.TenRowCompleteChambers.uEndpoints
#print axioms SubQuorum.TenRowCompleteChambers.framed
#print axioms SubQuorum.TenRowCompleteChambers.rotorEndpoints
#print axioms SubQuorum.TenRowCompleteChambers.pocketFirst
#print axioms SubQuorum.TenRowCompleteChambers.pocketFirstSupports
#print axioms SubQuorum.TenRowCompleteChambers.pocketPoint
#print axioms SubQuorum.TenRowCompleteChambers.pocketRotor
#print axioms SubQuorum.TenRowCompleteChambers.pocketSupports
#print axioms SubQuorum.TenRowCompleteChambers.pocketWitness
#print axioms SubQuorum.TenRowCompleteChambers.witnessAnchor
#print axioms SubQuorum.TenRowCompleteChambers.witnessBlocker
#print axioms SubQuorum.TenRowCompleteChambers.boundary
#print axioms SubQuorum.TenRowCompleteChambers.overlap
#print axioms SubQuorum.TenRowCompleteChambers.firstUpperRotor
#print axioms SubQuorum.TenRowCompleteChambers.reflectedUpperRotor
#print axioms SubQuorum.TenRowCompleteChambers.adjacent_cannot_cross_pockets
#print axioms SubQuorum.TenRowCompleteChambers.upper_walk_stays_upper
#print axioms SubQuorum.TenRowCompleteChambers.connected_source_has_one_short_band
#print axioms SubQuorum.TenRowCompleteChambers.full_u_cannot_fit_three_rows
#print axioms SubQuorum.TenRowCompleteChambers.full_u_cannot_fit_four_columns
#print axioms SubQuorum.TenRowCompleteChambers.rotor_cannot_fit_three_rows
#print axioms SubQuorum.TenRowCompleteChambers.six_rotors_always_overlap
#print axioms SubQuorum.TenRowCompleteChambers.pocket_witness_original_support
#print axioms SubQuorum.TenRowCompleteChambers.pocket_witness_not_own_endpoint
#print axioms SubQuorum.TenRowCompleteChambers.witness_has_own_anchor
#print axioms SubQuorum.TenRowCompleteChambers.witness_has_two_distinct_neighbours
#print axioms SubQuorum.TenRowCompleteChambers.witness_blocker_on_boundary
#print axioms SubQuorum.TenRowCompleteChambers.no_complete_rotor_choice
#print axioms SubQuorum.TenRowCompleteChambers.upper_gate_rotors_collide
#print axioms SubQuorum.TenRowCompleteChambers.canonical_u_north_terminal_continues
#print axioms SubQuorum.TenRowCompleteChambers.canonical_u_no_other_single_direction
#print axioms SubQuorum.TenRowCompleteChambers.rotor_single_direction_continues
#print axioms SubQuorum.TenRowCompleteChambers.complete_width_six_budget
#print axioms SubQuorum.TenRowCompleteChambers.spanning_downward_gain
#print axioms SubQuorum.TenRowCompleteChambers.excluded_rotor_chain_value
#print axioms SubQuorum.TenRowCompleteChambers.general_rotor_chain_value
#print axioms SubQuorum.TenRowCompleteChambers.rotor_chain_chamber_marginal
