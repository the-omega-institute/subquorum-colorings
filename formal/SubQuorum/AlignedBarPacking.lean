import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.AlignedBarPacking

abbrev Point := Int × Int

def endpoint (top left right leftTip rightTip : Int) (point : Point) : Prop :=
  (top ≤ point.1 ∧ point.1 ≤ top+1 ∧ left ≤ point.2 ∧ point.2 ≤ right) ∨
  (point.2 = left ∧ top ≤ point.1 ∧ point.1 ≤ leftTip) ∨
  (point.2 = right ∧ top ≤ point.1 ∧ point.1 ≤ rightTip)

def sameTile (first second : Point) : Prop :=
  first.1/2 = second.1/2 ∧ first.2/2 = second.2/2

theorem endpoint_bounds (top left right leftTip rightTip : Int) (point : Point)
    (hwidth : left ≤ right) (hpoint : endpoint top left right leftTip rightTip point) :
    top ≤ point.1 ∧ left ≤ point.2 ∧ point.2 ≤ right := by
  rcases hpoint with hbar | hleft | hright <;> omega

theorem aligned_column_interval (left right column other : Int)
    (hleft : left % 2 = 0) (hright : right % 2 = 1)
    (hother : left ≤ other ∧ other ≤ right) (htile : column/2 = other/2) :
    left ≤ column ∧ column ≤ right := by omega

theorem aligned_row_lower_bound (top row other : Int)
    (htop : top % 2 = 0) (hother : top ≤ other) (htile : row/2 = other/2) :
    top ≤ row := by omega

theorem ordered_shared_tile_forces_collision
    (topFirst leftFirst rightFirst leftTipFirst rightTipFirst : Int)
    (topSecond leftSecond rightSecond leftTipSecond rightTipSecond : Int)
    (first second : Point)
    (hwidthSecond : leftSecond ≤ rightSecond)
    (htopFirst : topFirst % 2 = 0) (htopSecond : topSecond % 2 = 0)
    (hleftSecond : leftSecond % 2 = 0) (hrightSecond : rightSecond % 2 = 1)
    (horder : topFirst ≤ topSecond)
    (hfirst : endpoint topFirst leftFirst rightFirst leftTipFirst rightTipFirst first)
    (hsecond : endpoint topSecond leftSecond rightSecond leftTipSecond rightTipSecond second)
    (htile : sameTile first second) :
    endpoint topFirst leftFirst rightFirst leftTipFirst rightTipFirst (topSecond,first.2) ∧
    endpoint topSecond leftSecond rightSecond leftTipSecond rightTipSecond (topSecond,first.2) := by
  have hsecondBounds := endpoint_bounds topSecond leftSecond rightSecond
    leftTipSecond rightTipSecond second hwidthSecond hsecond
  have hrow := aligned_row_lower_bound topSecond first.1 second.1 htopSecond
    hsecondBounds.1 htile.1
  have hcolumn := aligned_column_interval leftSecond rightSecond first.2 second.2
    hleftSecond hrightSecond hsecondBounds.2 htile.2
  constructor
  · rcases hfirst with hbar | hleft | hright
    · apply Or.inl
      dsimp at hbar ⊢
      omega
    · exact Or.inr (Or.inl ⟨hleft.1,horder,by omega⟩)
    · exact Or.inr (Or.inr ⟨hright.1,horder,by omega⟩)
  · exact Or.inl ⟨by omega,by omega,hcolumn.1,hcolumn.2⟩

theorem disjoint_aligned_U_have_disjoint_tiles
    (topFirst leftFirst rightFirst leftTipFirst rightTipFirst : Int)
    (topSecond leftSecond rightSecond leftTipSecond rightTipSecond : Int)
    (hwidthFirst : leftFirst ≤ rightFirst) (hwidthSecond : leftSecond ≤ rightSecond)
    (htopFirst : topFirst % 2 = 0) (htopSecond : topSecond % 2 = 0)
    (hleftFirst : leftFirst % 2 = 0) (hrightFirst : rightFirst % 2 = 1)
    (hleftSecond : leftSecond % 2 = 0) (hrightSecond : rightSecond % 2 = 1)
    (hdisjoint : ∀ point,
      endpoint topFirst leftFirst rightFirst leftTipFirst rightTipFirst point →
      endpoint topSecond leftSecond rightSecond leftTipSecond rightTipSecond point → False)
    (first second : Point)
    (hfirst : endpoint topFirst leftFirst rightFirst leftTipFirst rightTipFirst first)
    (hsecond : endpoint topSecond leftSecond rightSecond leftTipSecond rightTipSecond second) :
    ¬sameTile first second := by
  intro htile
  by_cases horder : topFirst ≤ topSecond
  · rcases ordered_shared_tile_forces_collision
      topFirst leftFirst rightFirst leftTipFirst rightTipFirst
      topSecond leftSecond rightSecond leftTipSecond rightTipSecond first second
      hwidthSecond htopFirst htopSecond hleftSecond hrightSecond
      horder hfirst hsecond htile with ⟨hcollisionFirst,hcollisionSecond⟩
    exact hdisjoint (topSecond,first.2) hcollisionFirst hcollisionSecond
  · rcases ordered_shared_tile_forces_collision
      topSecond leftSecond rightSecond leftTipSecond rightTipSecond
      topFirst leftFirst rightFirst leftTipFirst rightTipFirst second first
      hwidthFirst htopSecond htopFirst hleftFirst hrightFirst
      (by omega) hsecond hfirst ⟨htile.1.symm,htile.2.symm⟩ with
      ⟨hcollisionSecond,hcollisionFirst⟩
    exact hdisjoint (topFirst,second.2) hcollisionFirst hcollisionSecond

theorem root_anchor_unique (occupied : Point → Prop) (first second : Point)
    (hfirstLeft : ∀ point, occupied point → first.2 ≤ point.2)
    (hsecondLeft : ∀ point, occupied point → second.2 ≤ point.2)
    (hfirstTip : occupied (first.1+5,first.2))
    (hsecondTip : occupied (second.1+5,second.2))
    (hfirstMax : ∀ row, occupied (row,first.2) → row ≤ first.1+5)
    (hsecondMax : ∀ row, occupied (row,second.2) → row ≤ second.1+5) : first = second := by
  have hcolumn : first.2 = second.2 := by
    have hleft := hfirstLeft (second.1+5,second.2) hsecondTip
    have hright := hsecondLeft (first.1+5,first.2) hfirstTip
    dsimp at hleft hright
    omega
  have hrowFirst := hfirstMax (second.1+5) (by simpa only [hcolumn] using hsecondTip)
  have hrowSecond := hsecondMax (first.1+5) (by simpa only [hcolumn] using hfirstTip)
  apply Prod.ext
  · omega
  · exact hcolumn

theorem contact_bar_precedes_root (rootBar rootTip bar tip : Int)
    (hcontact : ∃ row, rootBar ≤ row ∧ row ≤ rootTip ∧ bar ≤ row ∧ row ≤ tip)
    (hbarCollision : rootBar ≤ bar → bar ≤ rootTip → False) :
    bar < rootBar ∧ rootBar ≤ tip := by
  rcases hcontact with ⟨row,hrootLower,hrootUpper,hbarLower,htip⟩
  constructor
  · by_cases hbefore : bar < rootBar
    · exact hbefore
    · exact False.elim (hbarCollision (by omega) (by omega))
  · omega

theorem near_column_is_full (occupied : Point → Prop) (rootBar bar row : Int)
    (hbar : bar ≤ rootBar) (hrow : rootBar ≤ row ∧ row ≤ 30)
    (heven : row % 2 = 0)
    (hleftUpper : ∀ height, bar ≤ height → height ≤ 22 → occupied (height,0))
    (hleftLower : ∀ height, 23 ≤ height → height ≤ 33 → occupied (height,0))
    (hright : ∀ height, rootBar ≤ height → height ≤ 30 → occupied (height,1))
    (hcap : occupied (31,1)) :
    occupied (row,0) ∧ occupied (row+1,0) ∧
      occupied (row,1) ∧ occupied (row+1,1) := by
  have hleftFirst : occupied (row,0) := by
    by_cases hupper : row ≤ 22
    · exact hleftUpper row (by omega) hupper
    · exact hleftLower row (by omega) (by omega)
  have hleftSecond : occupied (row+1,0) := by
    by_cases hupper : row+1 ≤ 22
    · exact hleftUpper (row+1) (by omega) hupper
    · exact hleftLower (row+1) (by omega) (by omega)
  refine ⟨hleftFirst,hleftSecond,hright row hrow.1 hrow.2,?_⟩
  by_cases hbottom : row = 30
  · simpa [hbottom] using hcap
  · exact hright (row+1) (by omega) (by omega)

theorem foreign_root_credit (delta eta cap triple : Int)
    (hdelta : delta = 0 ∨ delta = 1) (heta : eta = 0 ∨ eta = 1)
    (hcap : cap = 0 ∨ cap = 1) (hcapEta : cap = 1 → eta = 1)
    (htriple : triple = cap*delta) :
    (if eta = 0 then 1 else 0) ≤ 2-delta-eta-cap+2*triple := by
  rcases hdelta with hdelta | hdelta <;>
    rcases heta with heta | heta <;>
    rcases hcap with hcap | hcap <;>
    simp_all <;> omega

theorem batch_remainder_reduction (localGain external contacts total eligible : Int)
    (hledger : total = localGain+external+contacts)
    (hcontacts : -eligible ≤ contacts) (hlocal : eligible ≤ localGain) :
    external ≤ total := by omega

theorem unbounded_one_consumer_family (amount : Int) :
    (2*amount-1)-(amount-1) = amount := by omega

end SubQuorum.AlignedBarPacking
