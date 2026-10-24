import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.MaximalWidthTenCornerPair

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

def baseEndpoint (leg far : Int) (point : Point) : Prop :=
  endpoint 10 leg far (leg+3-point.1,point.2-1)

def crossEndpoint (width height far : Int) (point : Point) : Prop :=
  endpoint width height far (height+2-point.2,point.1-1)

def cornerEndpoint (leg near : Int) (point : Point) : Prop :=
  endpoint (leg-2) near 4 (point.2-3,point.1-2)

def consumerEndpoint (leg width far : Int) (point : Point) : Prop :=
  endpoint width 6 far (9-point.2,leg+2-point.1)

def inside (leg width : Int) (point : Point) : Prop :=
  leg+2-width < point.1 ∧ point.1 < leg+1 ∧ 4 < point.2 ∧ point.2 < 8

def boundary (leg width : Int) (point : Point) : Prop :=
  leg+2-width ≤ point.1 ∧ point.1 ≤ leg+1 ∧ 4 ≤ point.2 ∧ point.2 ≤ 8 ∧
    (point.1 = leg+2-width ∨ point.1 = leg+1 ∨ point.2 = 4 ∨ point.2 = 8)

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

theorem a_cross_owner_of_the_forced_support_would_overlap_the_base
    (leg far width height crossFar halfHeight halfFar : Int)
    (hleg : 8 ≤ leg) (hheight : 8 ≤ height)
    (hevenheight : height = 2*halfHeight) (hevenfar : crossFar = 2*halfFar)
    (howns : crossEndpoint width height crossFar (leg+1,3)) :
    crossEndpoint width height crossFar (leg+1,2) ∧ baseEndpoint leg far (leg+1,2) := by
  unfold crossEndpoint at howns ⊢
  unfold baseEndpoint endpoint at *
  dsimp at *
  omega

theorem the_only_remaining_even_incident_length_is_six
    (incident halfIncident : Int) (heven : incident = 2*halfIncident)
    (hlower : 4 < incident) (hupper : incident ≤ 6) : incident = 6 := by
  omega

theorem an_overwide_consumer_hits_the_cross_near_stem
    (leg width far crossWidth height crossFar : Int)
    (hwidth : leg ≤ width) (hleg : 8 ≤ leg) (hheight : 8 ≤ height)
    (hcross : 1 ≤ crossWidth) :
    consumerEndpoint leg width far (2,9) ∧
      crossEndpoint crossWidth height crossFar (2,9) := by
  unfold consumerEndpoint crossEndpoint endpoint
  dsimp
  omega

theorem an_overlong_other_leg_hits_the_corner_bar
    (leg width far near : Int) (_hleg : 8 ≤ leg)
    (hwidth : 6 ≤ width) (hupper : width ≤ leg-2) (hfar : 6 ≤ far) :
    consumerEndpoint leg width far (leg+2-width,4) ∧
      cornerEndpoint leg near (leg+2-width,4) := by
  unfold consumerEndpoint cornerEndpoint endpoint
  dsimp
  omega

theorem the_rectangle_boundary_has_only_known_endpoint_owners
    (leg width near : Int) (point : Point)
    (_hleg : 8 ≤ leg) (_hwidth : 6 ≤ width) (hupper : width ≤ leg-2)
    (hboundary : boundary leg width point) :
    cornerEndpoint leg near point ∨ consumerEndpoint leg width 4 point := by
  unfold boundary at hboundary
  unfold cornerEndpoint consumerEndpoint endpoint
  dsimp at *
  omega

theorem the_corner_interior_endpoints_are_only_its_far_leg
    (leg width near : Int) (point : Point)
    (_hwidth : 6 ≤ width) (hupper : width ≤ leg-2)
    (hinside : inside leg width point) :
    (cornerEndpoint leg near point ↔ point.1 = leg ∧ point.2 ≤ 7) ∧
      ¬consumerEndpoint leg width 4 point := by
  unfold inside at hinside
  unfold cornerEndpoint consumerEndpoint endpoint
  dsimp at *
  omega

theorem an_avoiding_unit_step_stays_inside
    (leg width : Int) (point next : Point) (hinside : inside leg width point)
    (hstep : adjacent point next) (havoid : ¬boundary leg width next) :
    inside leg width next := by
  unfold inside at hinside ⊢
  unfold adjacent at hstep
  unfold boundary at havoid
  rcases hstep with hstep | hstep | hstep | hstep <;> omega

theorem an_avoiding_unit_walk_stays_inside
    (leg width : Int) (length : Nat) (path : Nat → Point)
    (hstart : inside leg width (path 0))
    (hsteps : ∀ index, index < length → adjacent (path index) (path (index+1)))
    (havoid : ∀ index, index ≤ length → ¬boundary leg width (path index)) :
    inside leg width (path length) := by
  induction length with
  | zero => exact hstart
  | succ length inductionHypothesis =>
    have hprevious := inductionHypothesis
      (fun index hindex => hsteps index (by omega))
      (fun index hindex => havoid index (by omega))
    exact an_avoiding_unit_step_stays_inside leg width
      (path length) (path (length+1)) hprevious (hsteps length (by omega))
      (havoid (length+1) (by omega))

theorem a_connected_foreign_source_of_span_three_cannot_fit
    (leg width : Int) (belongs : Point → Prop) (seed : Point)
    (hconnected : connectedEndpoints belongs) (hseed : belongs seed)
    (hinside : inside leg width seed)
    (havoid : ∀ point, belongs point → ¬boundary leg width point)
    (hextent : ∃ point next, belongs point ∧ belongs next ∧ point.2+3 ≤ next.2) : False := by
  have hall : ∀ point, belongs point → inside leg width point := by
    intro point hpoint
    obtain ⟨length,path,hstart,hend,hbelongs,hsteps⟩ :=
      hconnected seed point hseed hpoint
    have hresult := an_avoiding_unit_walk_stays_inside leg width
      length path (hstart ▸ hinside) hsteps
      (fun index hindex => havoid (path index) (hbelongs index hindex))
    exact hend ▸ hresult
  obtain ⟨point,next,hpoint,hnext,hseparation⟩ := hextent
  have hfirst := hall point hpoint
  have hlast := hall next hnext
  unfold inside at hfirst hlast
  omega

theorem the_receipt_has_two_original_endpoints_and_two_unowned_inside_corners
    (leg width near : Int) (hleg : 8 ≤ leg)
    (hwidth : 6 ≤ width) (_hupper : width ≤ leg-2) :
    cornerEndpoint leg near (leg-2,4) ∧ cornerEndpoint leg near (leg-1,4) ∧
      inside leg width (leg-2,5) ∧ inside leg width (leg-1,5) ∧
      ¬cornerEndpoint leg near (leg-2,5) ∧ ¬cornerEndpoint leg near (leg-1,5) ∧
      ¬consumerEndpoint leg width 4 (leg-2,5) ∧
      ¬consumerEndpoint leg width 4 (leg-1,5) := by
  unfold cornerEndpoint consumerEndpoint endpoint inside
  dsimp
  omega

theorem neither_missing_corner_is_an_original_corner_support
    (leg near : Int) (hleg : 8 ≤ leg) :
    ¬support (leg-2) near 4 (2,leg-4) ∧ ¬support (leg-2) near 4 (2,leg-3) := by
  unfold support
  dsimp
  omega

theorem the_hypothetical_old_cross_bar_cannot_belong_to_the_base
    (leg far oldHeight : Int) (hheight : 4 ≤ oldHeight) :
    ¬baseEndpoint leg far (leg+1-oldHeight,3) := by
  unfold baseEndpoint endpoint
  dsimp
  omega

theorem the_opposite_first_lower_pairs_are_distinct
    (leg : Int) (hleg : 8 ≤ leg) :
    ¬((leg-2 : Int) = 4 ∨ leg-2 = 5 ∨ leg-1 = 4 ∨ leg-1 = 5) := by
  omega

theorem the_enlarged_pair_union_gives_the_existing_integer_certificate
    (positive marked transferred caps resolved residual activation prior upper lower
      reserve unmarked extra : Int)
    (hmarks : marked ≤ 2*(positive-unmarked))
    (hpartition : marked = transferred+caps+resolved+residual)
    (hinjection : transferred+extra ≤ activation)
    (hfloor : activation+prior+caps+2*upper+2*lower ≤ 2*reserve) :
    unmarked+upper+lower+(prior-resolved-residual+extra+1)/2 ≤
      positive+reserve-marked := by
  omega

theorem joint_H_and_critical_corner_coverage_implies_nonnegative_margin
    (positive marked transferred caps resolved activation prior upper lower
      reserve unmarked extra : Int)
    (hmarks : marked ≤ 2*(positive-unmarked))
    (hpartition : marked = transferred+caps+resolved)
    (hinjection : transferred+extra ≤ activation)
    (hfloor : activation+prior+caps+2*upper+2*lower ≤ 2*reserve)
    (hpairinjection : resolved ≤ lower)
    (hnonnegative : 0 ≤ unmarked ∧ 0 ≤ upper ∧ 0 ≤ prior ∧
      0 ≤ resolved ∧ 0 ≤ extra) :
    unmarked+upper+(lower-resolved)+(prior+resolved+extra+1)/2 ≤
      positive+reserve-marked ∧ 0 ≤ positive+reserve-marked := by
  omega

theorem the_entire_forced_lower_strip_has_at_least_one_pair
    (width : Int) (hwidth : 6 ≤ width) : 1 ≤ width/2-2 := by
  omega

end SubQuorum.MaximalWidthTenCornerPair
