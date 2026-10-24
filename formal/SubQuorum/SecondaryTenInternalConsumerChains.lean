import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenInternalConsumerChains

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def originalSupport (breadth near far : Int) (point : Point) : Prop :=
  point = (0,0) ∨ point = (0,breadth+1) ∨
  point = (near+1,1) ∨ point = (far+1,breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧
    ((point.1 % 2 = 0 ∧ point.2 = 0) ∨
     (point.1 % 2 = 1 ∧ point.2 = 2))) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧
    ((point.1 % 2 = 0 ∧ point.2 = breadth+1) ∨
     (point.1 % 2 = 1 ∧ point.2 = breadth-1)))

def terminal (breadth near far : Int) (slot : Bool) : Point :=
  if slot then (far,breadth) else (near,1)

def move (transpose flipRow flipColumn : Bool) (offset : Point) (point : Point) : Point :=
  let row := if flipRow then -point.1 else point.1
  let column := if flipColumn then -point.2 else point.2
  if transpose then (column+offset.1,row+offset.2)
  else (row+offset.1,column+offset.2)

def color (point : Point) : Int := (point.1+point.2) % 2

theorem endpoint_leg_exchange (breadth near far : Int) (point : Point) :
    endpoint breadth near far point ↔
      endpoint breadth far near (point.1,breadth+1-point.2) := by
  unfold endpoint
  dsimp
  omega

theorem support_leg_exchange (breadth near far : Int) (point : Point) :
    originalSupport breadth near far point ↔
      originalSupport breadth far near (point.1,breadth+1-point.2) := by
  rcases point with ⟨row, column⟩
  simp only [originalSupport, Prod.mk.injEq]
  constructor
  · intro hsupport
    rcases hsupport with hsupport | hsupport | hsupport | hsupport | hsupport | hsupport
    · right; left; omega
    · left; omega
    · right; right; right; left; omega
    · right; right; left; omega
    · right; right; right; right; right; omega
    · right; right; right; right; left; omega
  · intro hsupport
    rcases hsupport with hsupport | hsupport | hsupport | hsupport | hsupport | hsupport
    · right; left; omega
    · left; omega
    · right; right; right; left; omega
    · right; right; left; omega
    · right; right; right; right; right; omega
    · right; right; right; right; left; omega

theorem canonical_terminal_colors (breadthHalf nearHalf farHalf : Int) :
    color (terminal (2*breadthHalf) (2*nearHalf) (2*farHalf) false) ≠
      color (terminal (2*breadthHalf) (2*nearHalf) (2*farHalf) true) := by
  unfold color terminal
  dsimp
  omega

theorem transformed_terminal_colors (breadthHalf nearHalf farHalf : Int)
    (transpose flipRow flipColumn : Bool) (offset : Point) :
    color (move transpose flipRow flipColumn offset
      (terminal (2*breadthHalf) (2*nearHalf) (2*farHalf) false)) ≠
    color (move transpose flipRow flipColumn offset
      (terminal (2*breadthHalf) (2*nearHalf) (2*farHalf) true)) := by
  cases transpose <;> cases flipRow <;> cases flipColumn <;>
    unfold color move terminal <;> dsimp <;> omega

theorem same_color_terminal_slots_equal
    (breadthHalf nearHalf farHalf : Int)
    (transpose flipRow flipColumn first second : Bool) (offset : Point)
    (hsame : color (move transpose flipRow flipColumn offset
      (terminal (2*breadthHalf) (2*nearHalf) (2*farHalf) first)) =
      color (move transpose flipRow flipColumn offset
      (terminal (2*breadthHalf) (2*nearHalf) (2*farHalf) second))) :
    first = second := by
  have hdifferent := transformed_terminal_colors breadthHalf nearHalf farHalf
    transpose flipRow flipColumn offset
  cases first <;> cases second <;> simp_all

def oldV (origin width offset depth : Int) (point : Point) : Prop :=
  endpoint (width+10) 8 depth (point.1-origin+6,width+12+offset-point.2)

def eastE (origin width offset : Int) (point : Point) : Prop :=
  endpoint 6 4 4 (origin+4-point.1,point.2-width-7-offset)

def zeroRepair (origin width offset : Int) (point : Point) : Prop :=
  endpoint (width+12) 10 4 (point.1-origin+8,width+13+offset-point.2)

theorem forced_p_original_support (origin width offset depth : Int) :
    originalSupport (width+10) 8 depth
      ((origin+2)-origin+6,width+12+offset-(width+12+offset)) := by
  unfold originalSupport
  dsimp
  omega

theorem p_absent_from_V_and_E (origin width offset depth : Int)
    (hwidth : 12 ≤ width) :
    ¬oldV origin width offset depth (origin+2,width+12+offset) ∧
      ¬eastE origin width offset (origin+2,width+12+offset) := by
  unfold oldV eastE endpoint
  dsimp
  omega

theorem p_three_foreign_blockers (origin width offset depth : Int) :
    oldV origin width offset depth (origin+2,width+11+offset) ∧
      eastE origin width offset (origin+2,width+13+offset) ∧
      eastE origin width offset (origin+3,width+12+offset) := by
  unfold oldV eastE endpoint
  dsimp
  omega

theorem zero_repair_consumes_p (origin width offset : Int) :
    zeroRepair origin width offset (origin+2,width+12+offset) := by
  unfold zeroRepair endpoint
  dsimp
  omega

theorem band_endpoint_pair (origin width offset depth column : Int)
    (hmin : offset+2 ≤ column) (hmax : column ≤ offset+width+11) :
    zeroRepair origin width offset (origin-7,column) ∧
      oldV origin width offset depth (origin-6,column) := by
  unfold zeroRepair oldV endpoint
  dsimp
  omega

theorem band_directions_survive (origin width offset depth column : Int)
    (hdepth : 24 ≤ depth)
    (hmin : offset+2 ≤ column) (hmax : column ≤ offset+width+11) :
    ¬originalSupport (width+10) 8 depth
      ((origin-7)-origin+6,width+12+offset-column) ∧
    ¬originalSupport (width+12) 10 4
      ((origin-6)-origin+8,width+13+offset-column) := by
  unfold originalSupport
  simp only [Prod.mk.injEq]
  dsimp
  omega

theorem renewed_q_is_original_support (origin width offset : Int) :
    originalSupport (width+12) 10 4
      ((origin-3)-origin+8,width+13+offset-(offset+1)) := by
  unfold originalSupport
  simp only [Prod.mk.injEq]
  dsimp
  omega

theorem renewed_q_absent_locally (origin width offset depth : Int)
    (hwidth : 12 ≤ width) :
    ¬zeroRepair origin width offset (origin-3,offset+1) ∧
      ¬oldV origin width offset depth (origin-3,offset+1) := by
  unfold zeroRepair oldV endpoint
  dsimp
  omega

theorem renewed_q_two_endpoint_neighbors (origin width offset depth : Int)
    (hdepth : 24 ≤ depth) :
    zeroRepair origin width offset (origin-4,offset+1) ∧
      oldV origin width offset depth (origin-3,offset+2) := by
  unfold zeroRepair oldV endpoint
  dsimp
  omega

theorem chain_body_row_gap (origin nextOrigin depth : Int)
    (hdepth : 24 ≤ depth) (hnext : nextOrigin = origin+depth-6) :
    origin+10+2 ≤ nextOrigin-6 := by
  omega

theorem successive_repair_row_gap (origin nextOrigin depth : Int)
    (hdepth : 24 ≤ depth) (hnext : nextOrigin = origin+depth-6) :
    origin+2+8 ≤ nextOrigin-8 := by
  omega

theorem nonadjacent_column_gap (offset nextOffset width laterMaximum : Int)
    (hwidth : 12 ≤ width) (hnext : nextOffset = offset-width-12)
    (hlater : laterMaximum ≤ nextOffset+5) :
    laterMaximum+21 ≤ offset+2 := by
  omega

theorem internal_consumer_chart (origin nextOrigin width nextWidth offset nextOffset
    depth row column : Int)
    (hrow : nextOrigin = origin+depth-6)
    (hcolumn : nextOffset = offset-nextWidth-12) :
    (origin-6+row,width+12+offset-((width+10)+1-column)) =
      (nextOrigin-depth+row,nextWidth+13+nextOffset+column) := by
  apply Prod.ext <;> dsimp <;> omega

theorem chain_deficit (actualPhi baseline widthSum amount rootBreadth : Int)
    (hactual : actualPhi = widthSum+8*amount+rootBreadth-1)
    (hbaseline : baseline = widthSum+9*amount) :
    actualPhi-baseline = rootBreadth-1-amount := by
  omega

theorem arbitrary_chain_relative_loss (actualPhi baseline amount rootBreadth : Int)
    (hexact : actualPhi = baseline+rootBreadth-1-amount)
    (hlong : rootBreadth-1 < amount) : actualPhi < baseline := by
  omega

theorem chain_absolute_positive (widthSum amount rootBreadth : Int)
    (hamount : 1 ≤ amount) (hwidths : 12*amount ≤ widthSum)
    (hroot : 6 ≤ rootBreadth) : 0 < widthSum+8*amount+rootBreadth-1 := by
  omega

def freshMass : List Int → Int
  | [] => 0
  | breadth :: rest => breadth-1+freshMass rest

theorem distinct_fresh_owner_mass (breadths : List Int)
    (hlegal : ∀ breadth ∈ breadths, 6 ≤ breadth) :
    5*(breadths.length : Int) ≤ freshMass breadths := by
  induction breadths with
  | nil => simp [freshMass]
  | cons breadth rest ih =>
    have hhead : 6 ≤ breadth := hlegal breadth (by simp)
    have hrest : ∀ other ∈ rest, 6 ≤ other := by
      intro other hmem
      exact hlegal other (by simp [hmem])
    have hbound := ih hrest
    simp only [freshMass, List.length_cons, Int.natCast_add, Int.natCast_one]
    omega

theorem fresh_mass_exterior_reduction
    (actualPhi baseline rootBreadth amount mass full events : Int)
    (hexact : actualPhi = baseline+rootBreadth-1-amount+mass+2*full-events)
    (hmass : 5*amount ≤ mass) :
    baseline+rootBreadth-1+4*amount+2*full-events ≤ actualPhi := by
  omega

theorem zero_gain_repair_receipt (width breadth mass full events : Int)
    (hbreadth : breadth = width+10) (hmass : mass = width+11)
    (hfull : 2*full = breadth+2) (hevents : events = 2*breadth+3) :
    mass+2*full-events = 0 := by
  omega

end SubQuorum.SecondaryTenInternalConsumerChains
