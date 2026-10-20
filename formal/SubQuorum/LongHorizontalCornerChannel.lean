import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.LongHorizontalCornerChannel

abbrev Point := Int × Int

def uEndpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def returningEndpoint (incident far : Int) (point : Point) : Prop :=
  uEndpoint 6 incident far (incident+3-point.1,point.2-1)

def cornerEndpoint (width incident far : Int) (point : Point) : Prop :=
  uEndpoint width incident far (point.1-3,point.2-2)

def inside (incident : Int) (point : Point) : Prop :=
  4 < point.1 ∧ point.1 < incident+2 ∧ 3 < point.2 ∧ point.2 < 7

def boundary (incident : Int) (point : Point) : Prop :=
  4 ≤ point.1 ∧ point.1 ≤ incident+2 ∧ 3 ≤ point.2 ∧ point.2 ≤ 7 ∧
    (point.1 = 4 ∨ point.1 = incident+2 ∨ point.2 = 3 ∨ point.2 = 7)

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

theorem disjointness_makes_the_returning_far_leg_exact
    (width incident cornerFar returningFar halfIncident halfFar : Int)
    (hwidth : 6 ≤ width) (hincident : 6 ≤ incident)
    (hfar : incident-2 ≤ returningFar)
    (hieven : incident = 2*halfIncident) (hfeven : returningFar = 2*halfFar)
    (hdisjoint : ∀ point, returningEndpoint incident returningFar point →
      ¬cornerEndpoint width (incident-2) cornerFar point) : returningFar = incident-2 := by
  by_cases hequal : returningFar = incident-2
  · exact hequal
  have hreturn : returningEndpoint incident returningFar (3,7) := by
    unfold returningEndpoint uEndpoint
    dsimp
    omega
  have hcorner : cornerEndpoint width (incident-2) cornerFar (3,7) := by
    unfold cornerEndpoint uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (3,7) hreturn hcorner)

theorem the_long_channel_has_an_endpoint_boundary
    (width incident cornerFar returningFar : Int) (point : Point)
    (hwidth : 6 ≤ width) (hincident : 6 ≤ incident)
    (hfar : incident-2 ≤ returningFar) (hboundary : boundary incident point) :
    returningEndpoint incident returningFar point ∨
      cornerEndpoint width (incident-2) cornerFar point := by
  unfold boundary at hboundary
  unfold returningEndpoint cornerEndpoint uEndpoint
  dsimp
  omega

theorem neither_boundary_owner_has_an_interior_endpoint
    (width incident cornerFar returningFar : Int) (point : Point)
    (hwidth : 6 ≤ width) (hinside : inside incident point) :
    ¬returningEndpoint incident returningFar point ∧
      ¬cornerEndpoint width (incident-2) cornerFar point := by
  unfold inside at hinside
  unfold returningEndpoint cornerEndpoint uEndpoint
  dsimp
  omega

theorem an_avoiding_unit_step_stays_in_the_channel
    (incident : Int) (point next : Point) (hinside : inside incident point)
    (hstep : adjacent point next) (havoid : ¬boundary incident next) :
    inside incident next := by
  unfold inside at hinside ⊢
  unfold adjacent at hstep
  unfold boundary at havoid
  rcases hstep with hstep | hstep | hstep | hstep <;> omega

theorem an_avoiding_unit_walk_stays_in_the_channel
    (incident : Int) (length : Nat) (path : Nat → Point)
    (hstart : inside incident (path 0))
    (hsteps : ∀ index, index < length → adjacent (path index) (path (index+1)))
    (havoid : ∀ index, index ≤ length → ¬boundary incident (path index)) :
    inside incident (path length) := by
  induction length with
  | zero => exact hstart
  | succ length inductionHypothesis =>
    have hprevious := inductionHypothesis
      (fun index hindex => hsteps index (by omega))
      (fun index hindex => havoid index (by omega))
    exact an_avoiding_unit_step_stays_in_the_channel incident
      (path length) (path (length+1)) hprevious (hsteps length (by omega))
      (havoid (length+1) (by omega))

theorem no_connected_foreign_source_fits_in_the_long_channel
    (incident : Int) (belongs : Point → Prop) (seed : Point)
    (hconnected : connectedEndpoints belongs) (hseed : belongs seed)
    (hinside : inside incident seed)
    (havoid : ∀ point, belongs point → ¬boundary incident point)
    (hextent : ∃ point next, belongs point ∧ belongs next ∧ point.2+3 ≤ next.2) : False := by
  have hall : ∀ point, belongs point → inside incident point := by
    intro point hpoint
    obtain ⟨length,path,hstart,hend,hbelongs,hsteps⟩ :=
      hconnected seed point hseed hpoint
    have hresult := an_avoiding_unit_walk_stays_in_the_channel incident
      length path (hstart ▸ hinside) hsteps
      (fun index hindex => havoid (path index) (hbelongs index hindex))
    exact hend ▸ hresult
  obtain ⟨point,next,hpoint,hnext,hseparation⟩ := hextent
  have hfirst := hall point hpoint
  have hlast := hall next hnext
  unfold inside at hfirst hlast
  omega

theorem the_first_lower_pair_has_two_corner_endpoints
    (width incident far : Int) (hwidth : 6 ≤ width) :
    cornerEndpoint width incident far (4,4) ∧
      cornerEndpoint width incident far (4,5) := by
  unfold cornerEndpoint uEndpoint
  dsimp
  omega

theorem the_first_lower_pair_bottom_is_in_the_long_channel
    (incident : Int) (hincident : 6 ≤ incident) :
    inside incident (5,4) ∧ inside incident (5,5) := by
  unfold inside
  dsimp
  omega

theorem opposite_first_lower_pairs_are_distinct
    (width : Int) (hwidth : 6 ≤ width) :
    ¬((4 : Int) = width ∨ 4 = width+1) ∧
      ¬((5 : Int) = width ∨ 5 = width+1) := by
  omega

theorem including_long_corner_receipts_implies_the_residual_bound
    (positive marked transferred caps resolved residual activation prior upper lower
      reserve unmarked : Int)
    (hmarks : marked ≤ 2*(positive-unmarked))
    (hpartition : marked = transferred+caps+resolved+residual)
    (hinjection : transferred ≤ activation)
    (hfloor : activation+prior+caps+2*upper+2*lower ≤ 2*reserve) :
    unmarked+upper+lower+(prior-resolved-residual+1)/2 ≤ positive+reserve-marked := by
  omega

end SubQuorum.LongHorizontalCornerChannel
