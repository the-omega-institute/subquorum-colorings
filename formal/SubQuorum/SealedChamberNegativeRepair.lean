import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SealedChamberNegativeRepair

abbrev Point := Int × Int

def adjacent (first second : Point) : Prop :=
  (first.1 = second.1 ∧ (first.2+1 = second.2 ∨ second.2+1 = first.2)) ∨
  (first.2 = second.2 ∧ (first.1+1 = second.1 ∨ second.1+1 = first.1))

def interior (lower upper right : Int) (point : Point) : Prop :=
  lower < point.1 ∧ point.1 < upper ∧ 0 < point.2 ∧ point.2 < right

def boundary (lower upper right : Int) (point : Point) : Prop :=
  ((point.1 = lower ∨ point.1 = upper) ∧ 0 ≤ point.2 ∧ point.2 ≤ right) ∨
  ((point.2 = 0 ∨ point.2 = right) ∧ lower ≤ point.1 ∧ point.1 ≤ upper)

inductive SourceWalk (vertices : Point → Prop) : Point → Point → Prop where
  | stay (point : Point) (hpoint : vertices point) : SourceWalk vertices point point
  | advance {start finish next : Point} (path : SourceWalk vertices start finish)
      (hnext : vertices next) (hstep : adjacent finish next) : SourceWalk vertices start next

def rotatedEndpoints (point : Point) : Prop :=
  (point.2 = 1 ∧ 5 ≤ point.1 ∧ point.1 ≤ 10) ∨
  (point.2 = 2 ∧ 6 ≤ point.1 ∧ point.1 ≤ 9) ∨
  ((point.1 = 5 ∨ point.1 = 10) ∧ 1 ≤ point.2 ∧ point.2 ≤ 5)

def negativeEndpoints (point : Point) : Prop :=
  (point.2 = 7 ∧ 4 ≤ point.1 ∧ point.1 ≤ 9) ∨
  (point.2 = 6 ∧ 5 ≤ point.1 ∧ point.1 ≤ 8) ∨
  ((point.1 = 4 ∨ point.1 = 9) ∧ 3 ≤ point.2 ∧ point.2 ≤ 7)

def nextBar (width : Int) (point : Point) : Prop :=
  (point.1 = 12 ∨ point.1 = 13) ∧ 1 ≤ point.2 ∧ point.2 ≤ width

def eastRotor (upper : Bool) (point : Point) : Prop :=
  point ∈ if upper then
    [(9,2),(10,2),(10,3),(10,4),(11,1),(11,2),(11,3),(12,3)]
  else [(10,3),(11,1),(11,2),(11,3),(12,2),(12,3),(12,4),(13,2)]

def gainSum (gains : List Int) : Int :=
  match gains with
  | [] => 0
  | gain :: rest => gain+gainSum rest

theorem step_stays_inside (lower upper right : Int) (first second : Point)
    (hinside : interior lower upper right first) (hstep : adjacent first second)
    (havoid : ¬ boundary lower upper right second) :
    interior lower upper right second := by
  simp only [interior] at *
  simp only [adjacent] at hstep
  simp only [boundary] at havoid
  omega

theorem source_walk_confined (vertices : Point → Prop) (lower upper right : Int)
    (havoid : ∀ point, vertices point → ¬ boundary lower upper right point)
    {start finish : Point} (path : SourceWalk vertices start finish) :
    interior lower upper right start → interior lower upper right finish := by
  induction path with
  | stay hpoint => exact fun hstart => hstart
  | @advance finish next path hnext hstep inductionHypothesis =>
    intro hstart
    exact step_stays_inside lower upper right finish next
      (inductionHypothesis hstart) hstep (havoid next hnext)

theorem connected_original_confined (vertices : Point → Prop)
    (lower upper right : Int)
    (havoid : ∀ point, vertices point → ¬ boundary lower upper right point)
    (hconnected : ∀ first second, vertices first → vertices second → SourceWalk vertices first second)
    (start : Point) (hstart : vertices start) (hinside : interior lower upper right start) :
    ∀ point, vertices point → interior lower upper right point := by
  intro point hpoint
  exact source_walk_confined vertices lower upper right havoid
    (hconnected start point hstart hpoint) hinside

theorem tile_mate_inside_or_boundary (startHalf endHalf widthHalf : Int)
    (first second : Point)
    (hinside : interior (2*startHalf+1) (2*endHalf) (2*widthHalf+1) first)
    (hrow : first.1/2 = second.1/2) (hcolumn : first.2/2 = second.2/2) :
    interior (2*startHalf+1) (2*endHalf) (2*widthHalf+1) second ∨
      boundary (2*startHalf+1) (2*endHalf) (2*widthHalf+1) second := by
  simp only [interior,boundary] at *
  omega

theorem tile_mate_of_new_endpoint_inside (startHalf endHalf widthHalf : Int)
    (first second : Point)
    (hinside : interior (2*startHalf+1) (2*endHalf) (2*widthHalf+1) first)
    (hrow : first.1/2 = second.1/2) (hcolumn : first.2/2 = second.2/2)
    (havoid : ¬ boundary (2*startHalf+1) (2*endHalf) (2*widthHalf+1) second) :
    interior (2*startHalf+1) (2*endHalf) (2*widthHalf+1) second := by
  exact (tile_mate_inside_or_boundary startHalf endHalf widthHalf first second hinside hrow hcolumn).resolve_right havoid

theorem chamber_tile_row_frontier (startHalf endHalf widthHalf : Int) (point : Point)
    (hinside : interior (2*startHalf+1) (2*endHalf) (2*widthHalf+1) point) :
    startHalf+1 ≤ point.1/2 ∧ point.1/2 ≤ endHalf-1 := by
  simp only [interior] at hinside
  omega

theorem different_chamber_tiles_disjoint (firstStart firstEnd secondStart secondEnd widthHalf : Int)
    (first second : Point) (hordered : firstEnd ≤ secondStart)
    (hfirst : interior (2*firstStart+1) (2*firstEnd) (2*widthHalf+1) first)
    (hsecond : interior (2*secondStart+1) (2*secondEnd) (2*widthHalf+1) second) :
    first.1/2 ≠ second.1/2 := by
  have hleft := chamber_tile_row_frontier firstStart firstEnd widthHalf first hfirst
  have hright := chamber_tile_row_frontier secondStart secondEnd widthHalf second hsecond
  omega

theorem gate_not_consumed_by_R_Z :
    ¬ rotatedEndpoints (11,1) ∧ ¬ negativeEndpoints (11,1) := by
  simp [rotatedEndpoints,negativeEndpoints]

theorem gate_has_R_and_next_bar_neighbours (width : Int) (hwidth : 8 ≤ width) :
    rotatedEndpoints (10,1) ∧ nextBar width (12,1) := by
  simp [rotatedEndpoints,nextBar]
  omega

theorem both_east_rotors_hit_next_bar (width : Int) (upper : Bool) (hwidth : 8 ≤ width) :
    ∃ point, eastRotor upper point ∧ nextBar width point := by
  cases upper
  · refine ⟨(12,2),?_,?_⟩ <;> simp [eastRotor,nextBar] <;> omega
  · refine ⟨(12,3),?_,?_⟩ <;> simp [eastRotor,nextBar] <;> omega

theorem actual_breadth_frontier (breadthHalf : Int) (hminimum : 3 ≤ breadthHalf)
    (hmiss : 1 < 12-2*breadthHalf) :
    breadthHalf = 3 ∨ breadthHalf = 4 ∨ breadthHalf = 5 := by
  omega

theorem actual_near_frontier (nearHalf : Int) (hmiss : 7 < 1+2*nearHalf) :
    4 ≤ nearHalf := by
  omega

theorem actual_right_wall_frontier (nearHalf widthHalf : Int)
    (hmiss : 1+2*nearHalf < 2*widthHalf+1) :
    nearHalf ≤ widthHalf-1 := by
  omega

theorem breadth_ten_far_frontier (nearHalf farHalf : Int)
    (hmiss : 1 < 1+2*nearHalf-2*farHalf) :
    farHalf ≤ nearHalf-1 := by
  omega

theorem breadth_six_eight_far_frontier (nearHalf farHalf : Int)
    (hmiss : 7 < 1+2*nearHalf-2*farHalf) :
    farHalf ≤ nearHalf-4 := by
  omega

theorem short_breadth_requires_near_twelve (nearHalf farHalf : Int)
    (hminimum : 2 ≤ farHalf) (hfar : farHalf ≤ nearHalf-4) :
    6 ≤ nearHalf := by
  omega

theorem width_eight_has_no_actual_owner (nearHalf : Int)
    (hnear : 4 ≤ nearHalf) (hwall : nearHalf ≤ 4-1) : False := by
  omega

theorem width_ten_twelve_force_breadth_ten (breadthHalf nearHalf farHalf widthHalf : Int)
    (hwidth : widthHalf ≤ 6) (hfar : 2 ≤ farHalf) (hwall : nearHalf ≤ widthHalf-1)
    (hshort : breadthHalf ≠ 5 → farHalf ≤ nearHalf-4) :
    breadthHalf = 5 := by
  omega

theorem negative_marginal_exact : (1 : Int)+2*1-4 = -1 := by omega

theorem actual_repair_marginal_exact : (1 : Int)+2*3-5 = 2 := by omega

theorem negative_and_actual_repair_joint : (-1 : Int)+(1+2*3-5) = 1 := by omega

theorem constant_repair_sum (gains : List Int) (hgains : ∀ gain ∈ gains, gain = 2) :
    gainSum gains = 2*(gains.length : Int) := by
  induction gains with
  | nil => simp [gainSum]
  | cons gain rest inductionHypothesis =>
    have hgain : gain = 2 := hgains gain (by simp)
    have hrest := inductionHypothesis (by intro value hvalue; exact hgains value (by simp [hvalue]))
    simp only [gainSum,List.length_cons,Int.natCast_add,Int.natCast_one]
    omega

theorem simultaneous_branch_repair (gaps : Int) (gains : List Int)
    (hcount : (gains.length : Int) = gaps) (hgains : ∀ gain ∈ gains, gain = 2) :
    gaps-gaps+gainSum gains = 2*gaps := by
  have hsum := constant_repair_sum gains hgains
  omega

end SubQuorum.SealedChamberNegativeRepair
