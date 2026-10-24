import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenLeftChainExterior

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def northLeft (origin offset breadth depth far : Int) (point : Point) : Prop :=
  endpoint breadth depth far (point.1-origin+4+depth,offset+1-point.2)

def oldX (origin offset : Int) (point : Point) : Prop :=
  endpoint 6 4 4 (origin+2-point.1,offset+2-point.2)

def oldP (origin offset width : Int) (point : Point) : Prop :=
  endpoint (width+12) 10 4 (point.1-origin+8,width+13+offset-point.2)

def oldZ (origin offset : Int) (point : Point) : Prop :=
  point = (origin-4,offset-1) ∨ point = (origin-3,offset-1) ∨
  point = (origin-3,offset) ∨ point = (origin-3,offset+1) ∨
  point = (origin-2,offset-2) ∨ point = (origin-2,offset-1) ∨
  point = (origin-2,offset) ∨ point = (origin-1,offset)

theorem first_column_strip (column previousOffset offset width : Int)
    (hcolumn : column % 2 = 1) (hprevious : previousOffset % 2 = 0)
    (hbefore : column < previousOffset-3)
    (hrecurrence : previousOffset = offset+width+12) :
    column ≤ previousOffset-5 ∧ column ≤ offset+width+7 := by
  omega

theorem strip_three_cases (column offset : Int)
    (hcolumn : column % 2 = 1) (hoffset : offset % 2 = 0)
    (hlower : offset-3 ≤ column) :
    column = offset-3 ∨ column = offset-1 ∨ offset+1 ≤ column := by
  omega

theorem far_stem_contains (origin offset breadth depth far row : Int)
    (hlower : origin-2-depth ≤ row) (hupper : row ≤ origin-4-depth+far) :
    northLeft origin offset breadth depth far (row,offset+1-breadth) := by
  unfold northLeft endpoint
  dsimp
  omega

theorem X_frontier_endpoint (origin offset : Int) :
    oldX origin offset (origin+1,offset-3) := by
  unfold oldX endpoint
  dsimp
  omega

theorem X_frontier_collision (origin offset breadth depth far nextOrigin nextOffset : Int)
    (hcolumn : offset+1-breadth = nextOffset-3)
    (hstart : origin-2-depth ≤ nextOrigin+1)
    (hend : nextOrigin+1 ≤ origin-4-depth+far) :
    northLeft origin offset breadth depth far (nextOrigin+1,nextOffset-3) ∧
    oldX nextOrigin nextOffset (nextOrigin+1,nextOffset-3) := by
  constructor
  · have hpoint := far_stem_contains origin offset breadth depth far (nextOrigin+1) hstart hend
    simpa only [hcolumn] using hpoint
  · exact X_frontier_endpoint nextOrigin nextOffset

theorem Z_frontier_endpoint (origin offset : Int) :
    oldZ origin offset (origin-4,offset-1) := by
  simp [oldZ]

theorem P_frontier_endpoint (origin offset width column : Int)
    (hlower : offset+1 ≤ column) (hupper : column ≤ offset+width+7) :
    oldP origin offset width (origin-8,column) := by
  unfold oldP endpoint
  dsimp
  omega

theorem X_frontier_bound (origin terminal : Int) :
    (¬origin+1 ≤ terminal) ↔ terminal ≤ origin := by
  omega

theorem Z_frontier_bound (origin terminal : Int)
    (horigin : origin % 2 = 1) (hterminal : terminal % 2 = 1) :
    (¬origin-4 ≤ terminal) ↔ terminal ≤ origin-6 := by
  omega

theorem P_frontier_bound (origin terminal : Int)
    (horigin : origin % 2 = 1) (hterminal : terminal % 2 = 1) :
    (¬origin-8 ≤ terminal) ↔ terminal ≤ origin-10 := by
  omega

theorem activated_terminal_lengths (origin terminal : Int)
    (horigin : origin % 2 = 1) (hterminal : terminal % 2 = 1)
    (hlower : origin-2 ≤ terminal) (hupper : terminal ≤ origin) :
    terminal = origin-2 ∨ terminal = origin := by
  omega

theorem old_X_contact_stem_endpoints (origin offset overlap : Int)
    (hlower : 0 ≤ overlap) (hupper : overlap ≤ 1) :
    oldX origin offset (origin-2+2*overlap,offset-4) := by
  unfold oldX endpoint
  dsimp
  omega

theorem extra_signed_debit (overlap : Int) :
    2*overlap-(2*overlap+1) = -1 := by
  omega

theorem exceptional_breadth (offset nextOffset breadth : Int)
    (hcolumn : offset+1-breadth = nextOffset-3)
    (hgap : nextOffset+24 ≤ offset) :
    breadth = offset-nextOffset+4 ∧ 28 ≤ breadth := by
  omega

theorem full_chain_left_gain (breadth loss : Int)
    (hbreadth : 6 ≤ breadth) (hlower : 0 ≤ loss) (hupper : loss ≤ 1)
    (hwide : loss = 1 → 28 ≤ breadth) :
    5 ≤ breadth-1-loss ∧ (breadth-1-loss = 5 ↔ breadth = 6) := by
  omega

theorem exceptional_gain (breadth : Int) (hwide : 28 ≤ breadth) :
    26 ≤ breadth-2 := by
  omega

theorem receipt_row_separation (origin nextOrigin : Int) (hgap : origin+18 ≤ nextOrigin) :
    origin-4+20 ≤ nextOrigin-2 := by
  omega

theorem later_blocks_after_terminal (origin nextOrigin terminal : Int)
    (hgap : origin+18 ≤ nextOrigin) (hterminal : terminal ≤ origin) :
    terminal+10 ≤ nextOrigin-8 := by
  omega

end SubQuorum.SecondaryTenLeftChainExterior
