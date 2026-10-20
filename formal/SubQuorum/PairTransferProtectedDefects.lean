import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.PairTransferProtectedDefects

abbrev Point := Int × Int

def uEndpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def pairEndpoint (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (point.2-2,point.1-2)

def transverseEndpoint (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (near+2-point.2,point.1-1)

theorem disjoint_pair_and_transverse_bar_force_strict_leg_separation
    (width near far crossWidth height crossFar : Int)
    (hwidth : 6 ≤ width) (hcross : 6 ≤ crossWidth)
    (hheight : 4 ≤ height)
    (hdisjoint : ∀ point, pairEndpoint width near far point →
      ¬transverseEndpoint crossWidth height crossFar point) : near < height := by
  by_cases hseparation : near < height
  · exact hseparation
  have hpair : pairEndpoint width near far (3,height+2) := by
    unfold pairEndpoint uEndpoint
    dsimp
    omega
  have hbar : transverseEndpoint crossWidth height crossFar (3,height+2) := by
    unfold transverseEndpoint uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (3,height+2) hpair hbar)

theorem separated_even_legs_have_two_units_of_clearance
    (near height halfNear halfHeight : Int)
    (hnear : near = 2*halfNear) (hheight : height = 2*halfHeight)
    (hstrict : near < height) : near+2 ≤ height := by
  omega

theorem the_pair_terminal_outer_support_is_consumed
    (crossWidth height crossFar near : Int)
    (hwidth : 6 ≤ crossWidth) (hnear : 4 ≤ near)
    (hseparation : near+2 ≤ height) :
    transverseEndpoint crossWidth height crossFar (2,near+2) := by
  unfold transverseEndpoint uEndpoint
  dsimp
  omega

theorem the_pair_target_forbids_a_singleton_producer_guard
    (crossWidth height crossFar near : Int)
    (hwidth : 6 ≤ crossWidth) (hnear : 4 ≤ near)
    (hseparation : near+2 ≤ height) :
    transverseEndpoint crossWidth height crossFar (2,near+4) := by
  unfold transverseEndpoint uEndpoint
  dsimp
  omega

theorem pair_consumption_requires_producer_width_at_least_ten
    (producerWidth near height : Int)
    (hnear : 4 ≤ near) (hseparation : near+2 ≤ height)
    (hbound : height ≤ producerWidth-4) : 10 ≤ producerWidth := by
  omega

def inside (lower upper first last : Int) (point : Point) : Prop :=
  lower < point.1 ∧ point.1 < upper ∧ first < point.2 ∧ point.2 < last

def boundary (lower upper first last : Int) (point : Point) : Prop :=
  lower ≤ point.1 ∧ point.1 ≤ upper ∧ first ≤ point.2 ∧ point.2 ≤ last ∧
    (point.1 = lower ∨ point.1 = upper ∨ point.2 = first ∨ point.2 = last)

def adjacent (point next : Point) : Prop :=
  (next.1 = point.1-1 ∧ next.2 = point.2) ∨
  (next.1 = point.1+1 ∧ next.2 = point.2) ∨
  (next.1 = point.1 ∧ next.2 = point.2-1) ∨
  (next.1 = point.1 ∧ next.2 = point.2+1)

theorem an_avoiding_unit_step_cannot_leave_an_endpoint_rectangle
    (lower upper first last : Int) (point next : Point)
    (hinside : inside lower upper first last point)
    (hstep : adjacent point next)
    (havoid : ¬boundary lower upper first last next) :
    inside lower upper first last next := by
  unfold inside at hinside ⊢
  unfold adjacent at hstep
  unfold boundary at havoid
  rcases hstep with hstep | hstep | hstep | hstep <;> omega

theorem an_avoiding_unit_walk_stays_inside_the_rectangle
    (lower upper first last : Int) (length : Nat) (path : Nat → Point)
    (hstart : inside lower upper first last (path 0))
    (hsteps : ∀ index, index < length → adjacent (path index) (path (index+1)))
    (havoid : ∀ index, index ≤ length → ¬boundary lower upper first last (path index)) :
    inside lower upper first last (path length) := by
  induction length with
  | zero => exact hstart
  | succ length inductionHypothesis =>
    have hprevious := inductionHypothesis
      (fun index hindex => hsteps index (by omega))
      (fun index hindex => havoid index (by omega))
    exact an_avoiding_unit_step_cannot_leave_an_endpoint_rectangle
      lower upper first last (path length) (path (length+1))
      hprevious (hsteps length (by omega)) (havoid (length+1) (by omega))

def connectedEndpoints (belongs : Point → Prop) : Prop :=
  ∀ point next, belongs point → belongs next →
    ∃ length : Nat, ∃ path : Nat → Point,
      path 0 = point ∧ path length = next ∧
      (∀ index, index ≤ length → belongs (path index)) ∧
      (∀ index, index < length → adjacent (path index) (path (index+1)))

theorem a_connected_disjoint_source_cannot_fit_in_three_interior_rows
    (lower upper first last : Int) (belongs : Point → Prop) (seed : Point)
    (hheight : upper = lower+4)
    (hconnected : connectedEndpoints belongs)
    (hseed : belongs seed) (hinside : inside lower upper first last seed)
    (havoid : ∀ point, belongs point → ¬boundary lower upper first last point)
    (hextent : ∃ point next, belongs point ∧ belongs next ∧ point.1+3 ≤ next.1) : False := by
  have hall : ∀ point, belongs point → inside lower upper first last point := by
    intro point hpoint
    obtain ⟨length,path,hstart,hend,hbelongs,hsteps⟩ :=
      hconnected seed point hseed hpoint
    have hresult := an_avoiding_unit_walk_stays_inside_the_rectangle
      lower upper first last length path (hstart ▸ hinside) hsteps
      (fun index hindex => havoid (path index) (hbelongs index hindex))
    exact hend ▸ hresult
  obtain ⟨point,next,hpoint,hnext,hseparation⟩ := hextent
  have hfirst := hall point hpoint
  have hlast := hall next hnext
  unfold inside at hfirst hlast
  omega

theorem a_persistent_cap_floor_strengthens_simultaneous_loss
    (reserve loss activation protectedUnits : Int)
    (hfloor : activation+protectedUnits ≤ 2*(reserve-loss)) :
    2*loss ≤ 2*reserve-activation-protectedUnits := by
  omega

def crossCapFrame (width : Int) (point : Point) : Point :=
  (point.1-2,width+1-point.2)

theorem the_two_cap_receipt_types_cannot_share_an_original_cap
    (width : Int) (positiveOwner negativeOwner : Point → Prop)
    (hwidth : 6 ≤ width) (hpositive : positiveOwner (1,3))
    (hnegative : ∀ column, 2 ≤ column → column ≤ width-1 →
      negativeOwner (crossCapFrame width (3,column)))
    (hdisjoint : ∀ point, positiveOwner point → ¬negativeOwner point) : False := by
  have hpoint := hnegative (width-2) (by omega) (by omega)
  have hequal : crossCapFrame width (3,width-2) = (1,3) := by
    unfold crossCapFrame
    apply Prod.ext <;> dsimp <;> omega
  exact hdisjoint (1,3) hpositive (hequal ▸ hpoint)

theorem the_protected_floor_pays_the_remaining_marked_demand
    (reserve loss activation protectedUnits marked positive : Int)
    (hfloor : 2*loss ≤ 2*reserve-activation-protectedUnits)
    (hdemand : 2*(marked-positive) ≤ activation+protectedUnits) :
    loss ≤ positive+reserve-marked := by
  omega

theorem at_most_one_nonpositive_gate_consumer_implies_allocation
    (positive marked positiveConsumers activation reserve : Int)
    (hmarks : marked ≤ 2*positive)
    (hinjection : positiveConsumers ≤ activation)
    (hfloor : activation ≤ 2*reserve)
    (hother : marked-positiveConsumers ≤ 1) :
    0 ≤ positive+reserve-marked := by
  omega

end SubQuorum.PairTransferProtectedDefects
