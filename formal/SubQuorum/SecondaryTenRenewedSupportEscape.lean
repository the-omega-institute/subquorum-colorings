import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenRenewedSupportEscape

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

def oldV (origin width offset depth : Int) (point : Point) : Prop :=
  endpoint (width+10) 8 depth (point.1-origin+6,width+12+offset-point.2)

def westRotor (origin offset : Int) (point : Point) : Prop :=
  point = (origin-4,offset-1) ∨ point = (origin-3,offset-1) ∨
  point = (origin-3,offset) ∨ point = (origin-3,offset+1) ∨
  point = (origin-2,offset-2) ∨ point = (origin-2,offset-1) ∨
  point = (origin-2,offset) ∨ point = (origin-1,offset)

def southU (origin offset breadth depth far : Int) (left : Bool) (point : Point) : Prop :=
  endpoint breadth depth far
    (origin+depth-2-point.1,if left then offset+2-point.2 else point.2-offset)

theorem r_original_V_support (origin width offset depth : Int) (hdepth : 4 ≤ depth) :
    originalSupport (width+10) 8 depth
      ((origin-2)-origin+6,width+12+offset-(offset+1)) := by
  unfold originalSupport
  dsimp
  omega

theorem r_three_retained_blockers (origin width offset depth : Int)
    (hdepth : 4 ≤ depth) :
    westRotor origin offset (origin-3,offset+1) ∧
    westRotor origin offset (origin-2,offset) ∧
    oldV origin width offset depth (origin-2,offset+2) := by
  constructor
  · simp [westRotor]
  constructor
  · simp [westRotor]
  · unfold oldV endpoint
    dsimp
    omega

theorem r_absent_from_Z_and_V (origin width offset depth : Int)
    (hwidth : 12 ≤ width) :
    ¬westRotor origin offset (origin-2,offset+1) ∧
    ¬oldV origin width offset depth (origin-2,offset+1) := by
  unfold westRotor oldV endpoint
  simp only [Prod.mk.injEq]
  omega

theorem south_terminal_in_both_frames (origin offset breadth depth far : Int)
    (hdepth : 4 ≤ depth) (left : Bool) :
    southU origin offset breadth depth far left (origin-2,offset+1) := by
  cases left <;> unfold southU endpoint <;> dsimp <;> omega

theorem right_bar_hits_V_below_threshold (origin offset breadth depth far width oldDepth : Int)
    (hbreadth : 6 ≤ breadth) (hdepth : 4 ≤ depth) (hshort : depth < oldDepth-2) :
    southU origin offset breadth depth far false (origin+depth-3,offset+2) ∧
    oldV origin width offset oldDepth (origin+depth-3,offset+2) := by
  unfold southU oldV endpoint
  dsimp
  omega

theorem right_escape_requires_depth (origin offset breadth depth far width oldDepth : Int)
    (hbreadth : 6 ≤ breadth) (hdepth : 4 ≤ depth)
    (hdisjoint : ∀ point, southU origin offset breadth depth far false point →
      ¬oldV origin width offset oldDepth point) :
    oldDepth-2 ≤ depth := by
  by_cases hbound : oldDepth-2 ≤ depth
  · exact hbound
  · have hcollision := right_bar_hits_V_below_threshold origin offset breadth depth far
      width oldDepth hbreadth hdepth (by omega)
    exact False.elim (hdisjoint _ hcollision.1 hcollision.2)

theorem right_escape_hits_next_E (origin offset breadth depth far oldDepth nextWidth : Int)
    (hdepth : oldDepth-2 ≤ depth) (holdDepth : 24 ≤ oldDepth) :
    southU origin offset breadth depth far false (origin+oldDepth-6,offset+1) ∧
    endpoint 6 4 4
      ((origin+oldDepth-6)+4-(origin+oldDepth-6),
       (offset+1)-nextWidth-7-(offset-nextWidth-12)) := by
  unfold southU endpoint
  dsimp
  omega

theorem t_is_retained_original_support (origin width offset : Int) :
    originalSupport (width+12) 10 4
      ((origin-4)-origin+8,width+13+offset-offset) := by
  unfold originalSupport
  dsimp
  omega

theorem t_three_retained_blockers (origin width offset : Int) :
    westRotor origin offset (origin-4,offset-1) ∧
    endpoint (width+12) 10 4
      ((origin-4)-origin+8,width+13+offset-(offset+1)) ∧
    westRotor origin offset (origin-3,offset) := by
  constructor
  · simp [westRotor]
  constructor
  · unfold endpoint
    dsimp
    omega
  · simp [westRotor]

theorem t_absent_from_new_originals (origin offset : Int) :
    ¬westRotor origin offset (origin-4,offset) ∧
    ¬southU origin offset 6 4 4 true (origin-4,offset) := by
  unfold westRotor southU endpoint
  simp only [Prod.mk.injEq]
  dsimp
  omega

theorem small_left_column_and_row_bounds (origin offset : Int) (point : Point)
    (hpoint : southU origin offset 6 4 4 true point) :
    offset-4 ≤ point.2 ∧ point.2 ≤ offset+1 ∧
    origin-2 ≤ point.1 ∧ point.1 ≤ origin+2 := by
  unfold southU endpoint at hpoint
  dsimp at hpoint
  omega

theorem new_original_row_separation (origin nextOrigin oldDepth : Int)
    (hnext : nextOrigin = origin+oldDepth-6) (hdepth : 24 ≤ oldDepth) :
    origin+2+12 ≤ nextOrigin-4 := by
  omega

theorem tail_far_terminal_row (origin offset width depth : Int)
    (hdepth : 22 ≤ depth) :
    southU origin offset width depth (depth-6) false (origin+4,offset+width) := by
  unfold southU endpoint
  dsimp
  omega

theorem tail_column_bound (origin offset width depth : Int) (point : Point)
    (hwidth : 12 ≤ width)
    (hpoint : southU origin offset width depth (depth-6) false point) :
    offset+1 ≤ point.2 ∧ point.2 ≤ offset+width := by
  unfold southU endpoint at hpoint
  dsimp at hpoint
  omega

theorem tail_avoids_V (origin offset width depth oldDepth : Int) (point : Point)
    (hwidth : 12 ≤ width) (holdDepth : 24 ≤ oldDepth)
    (hdepth : oldDepth-2 ≤ depth)
    (hpoint : southU origin offset width depth (depth-6) false point) :
    ¬oldV origin width offset oldDepth point := by
  unfold southU endpoint at hpoint
  unfold oldV endpoint
  dsimp at hpoint ⊢
  omega

theorem tail_t_still_absent (origin offset width depth : Int) :
    ¬southU origin offset width depth (depth-6) false (origin-4,offset) := by
  unfold southU endpoint
  dsimp
  omega

theorem earlier_L_column_gap (offset width earlierOffset : Int)
    (hearlier : offset+width+12 ≤ earlierOffset) :
    offset+width+2 ≤ earlierOffset-4 := by
  omega

theorem right_charge_count (breadthHalf nearHalf farHalf : Int) :
    (2*breadthHalf-1+nearHalf+farHalf)+(nearHalf+farHalf+4)-
      2*(breadthHalf+1+nearHalf+farHalf) = 1 := by
  omega

theorem left_charge_count (breadthHalf nearHalf farHalf : Int) :
    (2*breadthHalf-1+nearHalf+farHalf)+(nearHalf+farHalf)-
      2*(breadthHalf+nearHalf+farHalf) = -1 := by
  omega

theorem equal_r_colors (origin offset nextOrigin nextOffset : Int)
    (horigin : origin % 2 = 1) (hoffset : offset % 2 = 0)
    (hnextOrigin : nextOrigin % 2 = 1) (hnextOffset : nextOffset % 2 = 0) :
    ((origin-2)+(offset+1)) % 2 = ((nextOrigin-2)+(nextOffset+1)) % 2 := by
  omega

theorem closure_zero_increment (count : Int) : count+2*count-3*count = 0 := by
  omega

theorem tail_negative_increment : (1 : Int)+2*2-9 = -4 := by
  omega

theorem tail_joint_ledger (baseline rootBreadth count : Int) :
    baseline+rootBreadth-1-count+1+2*2-9 =
      baseline+rootBreadth-1-count-4 := by
  omega

theorem specified_Y_consumes_t (origin offset width : Int) :
    endpoint (width+14) 6 4
      ((origin-4)-(origin-10),offset-(offset-1)) := by
  unfold endpoint
  dsimp
  omega

theorem specified_Y_bounds (origin offset width : Int) (point : Point)
    (hwidth : 12 ≤ width)
    (hpoint : endpoint (width+14) 6 4 (point.1-origin+10,point.2-offset+1)) :
    origin-10 ≤ point.1 ∧ point.1 ≤ origin-4 ∧
    offset ≤ point.2 ∧ point.2 ≤ offset+width+13 := by
  unfold endpoint at hpoint
  dsimp at hpoint
  omega

theorem specified_Y_tile_boundary (offsetHalf widthHalf : Int) :
    (2*offsetHalf+2*widthHalf+13)/2+1 = (2*offsetHalf+2*widthHalf+14)/2 := by
  omega

theorem specified_Y_unit_gain (widthHalf : Int) :
    (2*widthHalf+13)+2*(widthHalf+10)-(4*widthHalf+32) = 1 := by
  omega

theorem specified_compensation_joint_ledger (baseline rootBreadth count : Int) :
    baseline+rootBreadth-1-count+count = baseline+rootBreadth-1 := by
  omega

theorem specified_compensation_tail_ledger (baseline rootBreadth count : Int)
    (hroot : 6 ≤ rootBreadth) :
    baseline+1 ≤ baseline+rootBreadth-1-count-4+count := by
  omega

theorem still_missing_E_original_support : originalSupport 6 4 4 (5,6) := by
  simp [originalSupport]

end SubQuorum.SecondaryTenRenewedSupportEscape
