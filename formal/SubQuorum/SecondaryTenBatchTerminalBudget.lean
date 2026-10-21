import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenBatchTerminalBudget

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def terminal (breadth near far : Int) (slot : Bool) : Point :=
  if slot then (far,breadth) else (near,1)

def oppositeAnchor (breadth near far : Int) (slot : Bool) : Point :=
  ((terminal breadth near far slot).1+1,(terminal breadth near far slot).2)

theorem terminal_is_endpoint (breadth near far : Int) (slot : Bool)
    (hnear : 4 ≤ near) (hfar : 4 ≤ far) :
    endpoint breadth near far (terminal breadth near far slot) := by
  cases slot <;> unfold terminal endpoint <;> dsimp <;> omega

theorem terminal_only_inward_neighbor (breadth near far : Int) (slot : Bool)
    (hbreadth : 6 ≤ breadth) (hnear : 4 ≤ near) (hfar : 4 ≤ far) :
    let point := terminal breadth near far slot
    endpoint breadth near far (point.1-1,point.2) ∧
      ¬endpoint breadth near far (point.1+1,point.2) ∧
      ¬endpoint breadth near far (point.1,point.2-1) ∧
      ¬endpoint breadth near far (point.1,point.2+1) := by
  cases slot <;> unfold terminal endpoint <;> dsimp <;> omega

theorem different_terminal_slots (breadth near far : Int) (hbreadth : 6 ≤ breadth) :
    terminal breadth near far false ≠ terminal breadth near far true := by
  simp only [terminal, Bool.false_eq_true, ite_false, ite_true, ne_eq, Prod.mk.injEq]
  omega

theorem same_slot_same_anchor (breadth near far : Int) (first second : Bool)
    (hsame : first = second) :
    oppositeAnchor breadth near far first = oppositeAnchor breadth near far second := by
  rw [hsame]

theorem physical_anchor_forbids_duplicate
    {Owner : Type} (owner : Point → Owner) (first second : Point)
    (hpoint : first = second) (hbase : owner first ≠ owner second) : False := by
  exact hbase (congrArg owner hpoint)

theorem three_claims_repeat_slot (first second third : Bool) :
    first = second ∨ first = third ∨ second = third := by
  cases first <;> cases second <;> cases third <;> simp

theorem no_three_distinct_terminal_claims (first second third : Bool)
    (hfirstSecond : first ≠ second) (hfirstThird : first ≠ third)
    (hsecondThird : second ≠ third) : False := by
  rcases three_claims_repeat_slot first second third with hsame | hsame | hsame
  · exact hfirstSecond hsame
  · exact hfirstThird hsame
  · exact hsecondThird hsame

theorem owner_mass_pays_two_claims (breadth claims totalCost : Int)
    (hbreadth : 6 ≤ breadth) (hclaims : claims ≤ 2) (hcost : totalCost ≤ 2*claims) :
    breadth-1-2*claims ≤ breadth-1-totalCost ∧ 1 ≤ breadth-1-totalCost := by
  omega

def remainingBudget : List (Int × Int) → Int
  | [] => 0
  | entry :: rest => entry.1-1-entry.2+remainingBudget rest

theorem batch_remaining_budget (entries : List (Int × Int))
    (hpaid : ∀ entry ∈ entries, 1 ≤ entry.1-1-entry.2) :
    (entries.length : Int) ≤ remainingBudget entries := by
  induction entries with
  | nil => simp [remainingBudget]
  | cons entry rest ih =>
    have hentry : 1 ≤ entry.1-1-entry.2 := hpaid entry (by simp)
    have hrest : ∀ other ∈ rest, 1 ≤ other.1-1-other.2 := by
      intro other hmem
      exact hpaid other (by simp [hmem])
    have hbound := ih hrest
    simp only [remainingBudget, List.length_cons, Int.natCast_add, Int.natCast_one]
    omega

theorem exact_batch_ledger (actualPhi baseline mass costs extraFull extraEvents : Int)
    (hexact : actualPhi = baseline+mass-costs+2*extraFull-extraEvents) :
    actualPhi-baseline = mass-costs+2*extraFull-extraEvents := by
  omega

theorem batch_compensation_iff_exterior_paid
    (actualPhi baseline remaining extraFull extraEvents : Int)
    (hexact : actualPhi = baseline+remaining+2*extraFull-extraEvents) :
    baseline ≤ actualPhi ↔ extraEvents-2*extraFull ≤ remaining := by
  omega

theorem batch_spare_bound (actualPhi baseline extraFull extraEvents : Int)
    (entries : List (Int × Int))
    (hexact : actualPhi = baseline+remainingBudget entries+2*extraFull-extraEvents)
    (hpaid : ∀ entry ∈ entries, 1 ≤ entry.1-1-entry.2) :
    baseline+(entries.length : Int)+2*extraFull-extraEvents ≤ actualPhi := by
  have hbudget := batch_remaining_budget entries hpaid
  omega

def reflectedResidual (origin width breadth far : Int) (point : Point) : Prop :=
  endpoint breadth 8 far (origin-7-point.1,width+12-point.2)

def lowerResidual (origin width breadth far : Int) (point : Point) : Prop :=
  endpoint breadth 8 far (point.1-origin+6,width+12-point.2)

theorem opposing_bar_collision_free_rows (origin width breadth far : Int)
    (column : Int) (hmin : width+12-breadth ≤ column) (hmax : column ≤ width+11) :
    lowerResidual origin width breadth far (origin-6,column) ∧
      reflectedResidual origin width breadth far (origin-7,column) := by
  unfold lowerResidual reflectedResidual endpoint
  dsimp
  omega

theorem opposing_bars_exterior_debit (breadth full events : Int)
    (hfull : 2*full = breadth) (hevents : events = 2*breadth) :
    2*full-events = -breadth := by
  omega

theorem shared_consumer_baseline_loss (width mass cost debit : Int)
    (hmass : mass = 15) (hcost : cost = 2) (hdebit : debit = -(width+8)) :
    mass-cost+debit = 5-width := by
  omega

theorem shared_consumer_loss_negative (width : Int) (hwidth : 12 ≤ width) :
    5-width < 0 ∧ 0 < width+23 := by
  omega

def sharedConsumer (origin width : Int) (point : Point) : Prop :=
  endpoint 16 4 4 (width+18-point.2,origin+2-point.1)

def upperU (right : Bool) (origin width breadth depth far : Int) (point : Point) : Prop :=
  endpoint breadth depth far (point.1-origin+depth,
    if right then point.2-width-13 else width+15-point.2)

def reflectedC (origin width : Int) (point : Point) : Prop :=
  endpoint 8 6 4 (point.1-origin+19,point.2-width-6)

theorem fixed_consumer_blocks_east_U (origin width : Int) :
    sharedConsumer origin width (origin,width+17) := by
  unfold sharedConsumer endpoint
  dsimp
  omega

theorem fixed_consumer_blocks_east_rotor (origin width : Int) :
    sharedConsumer origin width (origin+1,width+16) := by
  unfold sharedConsumer endpoint
  dsimp
  omega

theorem short_right_upper_hits_shared
    (origin width breadth depth far : Int)
    (hbreadth : 6 ≤ breadth) (hmin : 4 ≤ depth) (hmax : depth ≤ 14) :
    upperU true origin width breadth depth far (origin+1-depth,width+17) ∧
      sharedConsumer origin width (origin+1-depth,width+17) := by
  unfold upperU sharedConsumer endpoint
  dsimp
  omega

theorem long_upper_hits_reflected_C
    (right : Bool) (origin width breadth depth far : Int)
    (hbreadth : 6 ≤ breadth) (hdepth : 16 ≤ depth) :
    upperU right origin width breadth depth far (origin-15,width+14) ∧
      reflectedC origin width (origin-15,width+14) := by
  cases right <;> unfold upperU reflectedC endpoint <;> dsimp <;> omega

theorem short_left_upper_hits_lower_V
    (origin width oldBreadth oldFar breadth depth far : Int)
    (hold : 6 ≤ oldBreadth) (hbreadth : 6 ≤ breadth)
    (hmin : 4 ≤ depth) (hmax : depth ≤ 6) :
    upperU false origin width breadth depth far (origin+1-depth,width+11) ∧
      lowerResidual origin width oldBreadth oldFar (origin+1-depth,width+11) := by
  unfold upperU lowerResidual endpoint
  dsimp
  omega

theorem middle_left_upper_hits_reflected_V
    (origin width oldBreadth oldFar breadth depth far : Int)
    (hold : 6 ≤ oldBreadth) (hbreadth : 6 ≤ breadth)
    (hmin : 8 ≤ depth) (hmax : depth ≤ 14) :
    upperU false origin width breadth depth far (origin+1-depth,width+11) ∧
      reflectedResidual origin width oldBreadth oldFar (origin+1-depth,width+11) := by
  unfold upperU reflectedResidual endpoint
  dsimp
  omega

theorem every_upper_U_hits_opposing_prefix
    (right : Bool) (origin width oldBreadth oldFar breadth depth far : Int)
    (hold : 6 ≤ oldBreadth) (hbreadth : 6 ≤ breadth)
    (hmin : 4 ≤ depth) (heven : depth % 2 = 0) :
    ∃ point, upperU right origin width breadth depth far point ∧
      (sharedConsumer origin width point ∨
        lowerResidual origin width oldBreadth oldFar point ∨
        reflectedResidual origin width oldBreadth oldFar point ∨
        reflectedC origin width point) := by
  by_cases hlong : 16 ≤ depth
  · have hhit := long_upper_hits_reflected_C right origin width breadth depth far hbreadth hlong
    exact ⟨(origin-15,width+14), hhit.1, Or.inr (Or.inr (Or.inr hhit.2))⟩
  · have hmax : depth ≤ 14 := by omega
    cases right with
    | true =>
      have hhit := short_right_upper_hits_shared origin width breadth depth far hbreadth hmin hmax
      exact ⟨(origin+1-depth,width+17), hhit.1, Or.inl hhit.2⟩
    | false =>
      by_cases hshort : depth ≤ 6
      · have hhit := short_left_upper_hits_lower_V origin width oldBreadth oldFar
          breadth depth far hold hbreadth hmin hshort
        exact ⟨(origin+1-depth,width+11), hhit.1, Or.inr (Or.inl hhit.2)⟩
      · have hmiddle : 8 ≤ depth := by omega
        have hhit := middle_left_upper_hits_reflected_V origin width oldBreadth oldFar
          breadth depth far hold hbreadth hmiddle hmax
        exact ⟨(origin+1-depth,width+11), hhit.1, Or.inr (Or.inr (Or.inl hhit.2))⟩

theorem no_disjoint_upper_U_consumer
    (right : Bool) (origin width oldBreadth oldFar breadth depth far : Int)
    (hold : 6 ≤ oldBreadth) (hbreadth : 6 ≤ breadth)
    (hmin : 4 ≤ depth) (heven : depth % 2 = 0)
    (hdisjoint : ∀ point, upperU right origin width breadth depth far point →
      ¬(sharedConsumer origin width point ∨
        lowerResidual origin width oldBreadth oldFar point ∨
        reflectedResidual origin width oldBreadth oldFar point ∨
        reflectedC origin width point)) : False := by
  obtain ⟨point,hconsumer,hblocker⟩ := every_upper_U_hits_opposing_prefix right origin width
    oldBreadth oldFar breadth depth far hold hbreadth hmin heven
  exact hdisjoint point hconsumer hblocker

def variableReflectedResidual
    (origin width consumerBreadth breadth far : Int) (point : Point) : Prop :=
  endpoint breadth 8 far (origin+9-consumerBreadth-point.1,width+12-point.2)

theorem short_reflected_bases_overlap
    (origin width consumerBreadth oldBreadth oldFar : Int)
    (hold : 6 ≤ oldBreadth) (hmin : 6 ≤ consumerBreadth) (hmax : consumerBreadth ≤ 14) :
    lowerResidual origin width oldBreadth oldFar (origin+8-consumerBreadth,width+11) ∧
      variableReflectedResidual origin width consumerBreadth oldBreadth oldFar
        (origin+8-consumerBreadth,width+11) := by
  unfold lowerResidual variableReflectedResidual endpoint
  dsimp
  omega

theorem separated_reflected_bases_row_gap (origin breadth lowerRow upperRow : Int)
    (hbreadth : 18 ≤ breadth) (hlower : origin-6 ≤ lowerRow)
    (hupper : upperRow ≤ origin+9-breadth) :
    3 ≤ lowerRow-upperRow := by
  omega

theorem reflected_pair_compensation (actualPhi baseline breadth : Int)
    (hbreadth : 18 ≤ breadth) (hexact : actualPhi = 2*baseline+breadth-3) :
    2*baseline+15 ≤ actualPhi := by
  omega

end SubQuorum.SecondaryTenBatchTerminalBudget
