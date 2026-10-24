import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.ShortSaturatedReturnPair

abbrev Point := Int × Int

def endpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def support (width near far : Int) (point : Point) : Prop :=
  (point.1 = 0 ∧ (point.2 = 0 ∨ point.2 = width+1)) ∨
  (point.1 = near+1 ∧ point.2 = 1) ∨
  (point.1 = far+1 ∧ point.2 = width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧
    ((point.1 % 2 = 0 ∧ point.2 = 0) ∨ (point.1 % 2 = 1 ∧ point.2 = 2))) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧
    ((point.1 % 2 = 0 ∧ point.2 = width+1) ∨
      (point.1 % 2 = 1 ∧ point.2 = width-1)))

def cornerEndpoint (leg near far : Int) (point : Point) : Prop :=
  endpoint (leg-2) near far (point.2-3,point.1-2)

def consumerEndpoint (leg incident : Int) (point : Point) : Prop :=
  endpoint 6 incident (incident-2) (incident+3-point.2,leg+2-point.1)

def baseEndpoint (width leg far : Int) (point : Point) : Prop :=
  endpoint width leg far (leg+3-point.1,point.2-1)

def inside (leg incident : Int) (point : Point) : Prop :=
  leg-4 < point.1 ∧ point.1 < leg+1 ∧ 4 < point.2 ∧ point.2 < incident+2

def boundary (leg incident : Int) (point : Point) : Prop :=
  leg-4 ≤ point.1 ∧ point.1 ≤ leg+1 ∧ 4 ≤ point.2 ∧ point.2 ≤ incident+2 ∧
    (point.1 = leg-4 ∨ point.1 = leg+1 ∨ point.2 = 4 ∨ point.2 = incident+2)

def adjacent (point next : Point) : Prop :=
  (next.1 = point.1-1 ∧ next.2 = point.2) ∨
  (next.1 = point.1+1 ∧ next.2 = point.2) ∨
  (next.1 = point.1 ∧ next.2 = point.2-1) ∨
  (next.1 = point.1 ∧ next.2 = point.2+1)

def connectedEndpoints (belongs : Point → Prop) : Prop :=
  ∀ point next, belongs point → belongs next →
    ∃ length : Nat, ∃ path : Nat → Point,
      path 0 = point ∧ path length = next ∧
      (∀ index, index ≤ length → belongs (path index)) ∧
      (∀ index, index < length → adjacent (path index) (path (index+1)))

def rotorMinus (tip point : Point) : Prop :=
  point = (tip.1-2,tip.2+1) ∨ point = (tip.1-1,tip.2+1) ∨
  point = (tip.1-1,tip.2+2) ∨ point = (tip.1-1,tip.2+3) ∨
  point = tip ∨ point = (tip.1,tip.2+1) ∨
  point = (tip.1,tip.2+2) ∨ point = (tip.1+1,tip.2+2)

def rotorPlus (tip point : Point) : Prop :=
  point = (tip.1-1,tip.2+2) ∨ point = tip ∨
  point = (tip.1,tip.2+1) ∨ point = (tip.1,tip.2+2) ∨
  point = (tip.1+1,tip.2+1) ∨ point = (tip.1+1,tip.2+2) ∨
  point = (tip.1+1,tip.2+3) ∨ point = (tip.1+2,tip.2+1)

theorem the_entire_boundary_has_fixed_endpoint_owners
    (leg near far incident : Int) (point : Point)
    (hleg : 8 ≤ leg) (hincident : 6 ≤ incident)
    (hboundary : boundary leg incident point) :
    cornerEndpoint leg near far point ∨ consumerEndpoint leg incident point := by
  unfold boundary at hboundary
  unfold cornerEndpoint consumerEndpoint endpoint
  dsimp at *
  omega

theorem the_only_fixed_interior_endpoints_are_on_the_bottom_far_stem
    (leg near far incident : Int) (point : Point)
    (hleg : 8 ≤ leg) (hinside : inside leg incident point) :
    (cornerEndpoint leg near far point ↔ point.1 = leg ∧ point.2 ≤ far+3) ∧
      ¬consumerEndpoint leg incident point := by
  unfold inside at hinside
  unfold cornerEndpoint consumerEndpoint endpoint
  dsimp at *
  omega

theorem an_avoiding_unit_step_stays_inside
    (leg incident : Int) (point next : Point) (hinside : inside leg incident point)
    (hstep : adjacent point next) (havoid : ¬boundary leg incident next) :
    inside leg incident next := by
  unfold inside at hinside ⊢
  unfold adjacent at hstep
  unfold boundary at havoid
  rcases hstep with hstep | hstep | hstep | hstep <;> omega

theorem an_avoiding_unit_walk_stays_inside
    (leg incident : Int) (length : Nat) (path : Nat → Point)
    (hstart : inside leg incident (path 0))
    (hsteps : ∀ index, index < length → adjacent (path index) (path (index+1)))
    (havoid : ∀ index, index ≤ length → ¬boundary leg incident (path index)) :
    inside leg incident (path length) := by
  induction length with
  | zero => exact hstart
  | succ length inductionHypothesis =>
    have hprevious := inductionHypothesis
      (fun index hindex => hsteps index (by omega))
      (fun index hindex => havoid index (by omega))
    exact an_avoiding_unit_step_stays_inside leg incident
      (path length) (path (length+1)) hprevious (hsteps length (by omega))
      (havoid (length+1) (by omega))

theorem a_connected_foreign_source_is_confined
    (leg incident : Int) (belongs : Point → Prop) (seed : Point)
    (hconnected : connectedEndpoints belongs) (hseed : belongs seed)
    (hinside : inside leg incident seed)
    (havoid : ∀ point, belongs point → ¬boundary leg incident point) :
    ∀ point, belongs point → inside leg incident point := by
  intro point hpoint
  obtain ⟨length,path,hstart,hend,hbelongs,hsteps⟩ := hconnected seed point hseed hpoint
  have hresult := an_avoiding_unit_walk_stays_inside leg incident
    length path (hstart ▸ hinside) hsteps
    (fun index hindex => havoid (path index) (hbelongs index hindex))
  exact hend ▸ hresult

theorem a_foreign_U_of_five_row_extent_cannot_fit
    (leg incident : Int) (belongs : Point → Prop)
    (hconfined : ∀ point, belongs point → inside leg incident point)
    (hextent : ∃ point next, belongs point ∧ belongs next ∧ point.1+4 ≤ next.1) :
    False := by
  obtain ⟨point,next,hpoint,hnext,hseparation⟩ := hextent
  have hfirst := hconfined point hpoint
  have hlast := hconfined next hnext
  unfold inside at hfirst hlast
  omega

theorem a_minus_rotor_touching_the_first_column_has_tip_at_five
    (leg incident : Int) (tip point : Point)
    (hconfined : ∀ next, rotorMinus tip next → inside leg incident next)
    (hpoint : rotorMinus tip point) (hcolumn : point.2 = 5) : tip.2 = 5 := by
  have htip := hconfined tip (by unfold rotorMinus; simp)
  unfold inside at htip
  unfold rotorMinus at hpoint
  rcases hpoint with hpoint | hpoint | hpoint | hpoint | hpoint | hpoint | hpoint | hpoint
  all_goals subst point; (try dsimp at *); omega

theorem a_plus_rotor_touching_the_first_column_has_tip_at_five
    (leg incident : Int) (tip point : Point)
    (hconfined : ∀ next, rotorPlus tip next → inside leg incident next)
    (hpoint : rotorPlus tip point) (hcolumn : point.2 = 5) : tip.2 = 5 := by
  have htip := hconfined tip (by unfold rotorPlus; simp)
  unfold inside at htip
  unfold rotorPlus at hpoint
  rcases hpoint with hpoint | hpoint | hpoint | hpoint | hpoint | hpoint | hpoint | hpoint
  all_goals subst point; (try dsimp at *); omega

theorem a_confined_minus_rotor_with_tip_at_five_hits_the_corner
    (leg near far incident : Int) (tip : Point) (_hleg : 8 ≤ leg) (hfar : 4 ≤ far)
    (hcolumn : tip.2 = 5)
    (hconfined : ∀ point, rotorMinus tip point → inside leg incident point) :
    rotorMinus tip (leg,7) ∧ cornerEndpoint leg near far (leg,7) := by
  have htop := hconfined (tip.1-2,tip.2+1) (by unfold rotorMinus; simp)
  have hbottom := hconfined (tip.1+1,tip.2+2) (by unfold rotorMinus; simp)
  have hrow : tip.1 = leg-1 := by unfold inside at htop hbottom; dsimp at *; omega
  constructor
  · unfold rotorMinus
    right; right; right; right; right; right; right
    apply Prod.ext <;> dsimp <;> omega
  · unfold cornerEndpoint endpoint
    dsimp
    omega

theorem a_confined_plus_rotor_with_tip_at_five_hits_the_corner
    (leg near far incident : Int) (tip : Point) (_hleg : 8 ≤ leg) (hfar : 4 ≤ far)
    (hcolumn : tip.2 = 5)
    (hconfined : ∀ point, rotorPlus tip point → inside leg incident point) :
    rotorPlus tip (leg,6) ∧ cornerEndpoint leg near far (leg,6) := by
  have htop := hconfined (tip.1-1,tip.2+2) (by unfold rotorPlus; simp)
  have hbottom := hconfined (tip.1+2,tip.2+1) (by unfold rotorPlus; simp)
  have hrow : tip.1 = leg-2 := by unfold inside at htop hbottom; dsimp at *; omega
  constructor
  · unfold rotorPlus
    right; right; right; right; right; right; right
    apply Prod.ext <;> dsimp <;> omega
  · unfold cornerEndpoint endpoint
    dsimp
    omega

theorem no_foreign_catalogue_source_meets_the_first_interior_column
    (leg near far incident : Int) (belongs : Point → Prop) (seed : Point)
    (hleg : 8 ≤ leg) (hfar : 4 ≤ far)
    (hconnected : connectedEndpoints belongs) (hseed : belongs seed)
    (hinside : inside leg incident seed) (hcolumn : seed.2 = 5)
    (havoid : ∀ point, belongs point → ¬boundary leg incident point)
    (hdisjoint : ∀ point, belongs point → ¬cornerEndpoint leg near far point)
    (hshape : (∃ point next, belongs point ∧ belongs next ∧ point.1+4 ≤ next.1) ∨
      (∃ tip, ∀ point, belongs point ↔ rotorMinus tip point) ∨
      (∃ tip, ∀ point, belongs point ↔ rotorPlus tip point)) : False := by
  have hall := a_connected_foreign_source_is_confined leg incident belongs seed
    hconnected hseed hinside havoid
  rcases hshape with hextent | ⟨tip,hminus⟩ | ⟨tip,hplus⟩
  · exact a_foreign_U_of_five_row_extent_cannot_fit leg incident belongs hall hextent
  · have hconfined : ∀ point, rotorMinus tip point → inside leg incident point :=
      fun point hpoint => hall point ((hminus point).mpr hpoint)
    have htip := a_minus_rotor_touching_the_first_column_has_tip_at_five
      leg incident tip seed hconfined ((hminus seed).mp hseed) hcolumn
    obtain ⟨hrotor,hcorner⟩ := a_confined_minus_rotor_with_tip_at_five_hits_the_corner
      leg near far incident tip hleg hfar htip hconfined
    exact hdisjoint (leg,7) ((hminus (leg,7)).mpr hrotor) hcorner
  · have hconfined : ∀ point, rotorPlus tip point → inside leg incident point :=
      fun point hpoint => hall point ((hplus point).mpr hpoint)
    have htip := a_plus_rotor_touching_the_first_column_has_tip_at_five
      leg incident tip seed hconfined ((hplus seed).mp hseed) hcolumn
    obtain ⟨hrotor,hcorner⟩ := a_confined_plus_rotor_with_tip_at_five_hits_the_corner
      leg near far incident tip hleg hfar htip hconfined
    exact hdisjoint (leg,6) ((hplus (leg,6)).mpr hrotor) hcorner

theorem the_pair_has_only_its_two_fixed_endpoints
    (leg near far incident : Int) (hleg : 8 ≤ leg) (hincident : 6 ≤ incident) :
    cornerEndpoint leg near far (leg-2,4) ∧ cornerEndpoint leg near far (leg-1,4) ∧
      inside leg incident (leg-2,5) ∧ inside leg incident (leg-1,5) ∧
      ¬cornerEndpoint leg near far (leg-2,5) ∧
      ¬cornerEndpoint leg near far (leg-1,5) ∧
      ¬consumerEndpoint leg incident (leg-2,5) ∧
      ¬consumerEndpoint leg incident (leg-1,5) := by
  unfold cornerEndpoint consumerEndpoint endpoint inside
  dsimp
  omega

theorem the_missing_vertices_are_not_original_corner_supports
    (leg near far : Int) (hleg : 8 ≤ leg) :
    ¬support (leg-2) near far (2,leg-4) ∧ ¬support (leg-2) near far (2,leg-3) := by
  unfold support
  dsimp
  omega

theorem the_hypothetical_old_H_transverse_bar_cannot_belong_to_B
    (width leg far oldHeight : Int) (hwidth : 6 ≤ width) (hheight : 4 ≤ oldHeight) :
    ¬baseEndpoint width leg far (leg+1-oldHeight,3) := by
  unfold baseEndpoint endpoint
  dsimp
  omega

theorem the_single_use_integer_ledger
    (positive reserve marked activation q c paid residual nzero upper pairs mEight rho : Int)
    (hpartition : marked = q+c+paid+residual)
    (hmarks : marked ≤ 2*(positive-nzero))
    (hactivation : q+rho ≤ activation)
    (hreserve : activation+mEight+c+2*pairs+2*upper ≤ 2*reserve) :
    nzero+upper+pairs+(mEight-paid-residual+rho+1)/2 ≤ positive+reserve-marked := by
  omega

theorem the_exhausted_residual_coverage_corollary
    (positive reserve marked activation q c paid nzero upper pairs mEight rho : Int)
    (hpartition : marked = q+c+paid)
    (hmarks : marked ≤ 2*(positive-nzero))
    (hactivation : q+rho ≤ activation)
    (hreserve : activation+mEight+c+2*pairs+2*upper ≤ 2*reserve)
    (hinjection : paid ≤ pairs) (hpaid : 0 ≤ paid)
    (hnzero : 0 ≤ nzero) (hupper : 0 ≤ upper)
    (hmEight : 0 ≤ mEight) (hrho : 0 ≤ rho) : 0 ≤ positive+reserve-marked := by
  omega

end SubQuorum.ShortSaturatedReturnPair
