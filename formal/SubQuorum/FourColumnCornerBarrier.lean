import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.FourColumnCornerBarrier

abbrev Point := Int × Int

def inside (lower upper first : Int) (point : Point) : Prop :=
  lower < point.1 ∧ point.1 < upper ∧ first < point.2 ∧ point.2 < first+5

def barrier (lower upper first : Int) (point : Point) : Prop :=
  lower ≤ point.1 ∧ point.1 ≤ upper ∧ first ≤ point.2 ∧ point.2 ≤ first+5 ∧
    (point.1 = lower ∨ point.1 = upper ∨ point.2 = first ∨ point.2 = first+5) ∧
    ¬(point.1 = upper ∧ point.2 = first+5)

def adjacent (point next : Point) : Prop :=
  (next.1 = point.1-1 ∧ next.2 = point.2) ∨
  (next.1 = point.1+1 ∧ next.2 = point.2) ∨
  (next.1 = point.1 ∧ next.2 = point.2-1) ∨
  (next.1 = point.1 ∧ next.2 = point.2+1)

theorem a_unit_step_cannot_escape_through_the_missing_corner
    (lower upper first : Int) (point next : Point)
    (hinside : inside lower upper first point) (hstep : adjacent point next)
    (havoid : ¬barrier lower upper first next) : inside lower upper first next := by
  unfold inside at hinside ⊢
  unfold adjacent at hstep
  unfold barrier at havoid
  rcases hstep with hstep | hstep | hstep | hstep <;> omega

theorem an_avoiding_walk_stays_inside_the_punctured_barrier
    (lower upper first : Int) (length : Nat) (path : Nat → Point)
    (hstart : inside lower upper first (path 0))
    (hsteps : ∀ index, index < length → adjacent (path index) (path (index+1)))
    (havoid : ∀ index, index ≤ length → ¬barrier lower upper first (path index)) :
    inside lower upper first (path length) := by
  induction length with
  | zero => exact hstart
  | succ length inductionHypothesis =>
    have hprevious := inductionHypothesis
      (fun index hindex => hsteps index (by omega))
      (fun index hindex => havoid index (by omega))
    exact a_unit_step_cannot_escape_through_the_missing_corner
      lower upper first (path length) (path (length+1)) hprevious
      (hsteps length (by omega)) (havoid (length+1) (by omega))

theorem a_five_column_extent_cannot_fit_the_four_column_interior
    (lower upper first : Int) (belongs : Point → Prop)
    (hconfined : ∀ point, belongs point → inside lower upper first point)
    (hextent : ∃ point next, belongs point ∧ belongs next ∧ point.2+4 ≤ next.2) : False := by
  obtain ⟨point,next,hpoint,hnext,hseparation⟩ := hextent
  have hfirst := hconfined point hpoint
  have hlast := hconfined next hnext
  unfold inside at hfirst hlast
  omega

def leftRotorEndpoint (tip : Point) (up : Bool) (point : Point) : Prop :=
  point = tip ∨ point = (tip.1,tip.2+1) ∨
  ((tip.1-1 ≤ point.1 ∧ point.1 ≤ tip.1+1) ∧ point.2 = tip.2+2) ∨
  (if up then
    point = (tip.1+2,tip.2+1) ∨ point = (tip.1+1,tip.2+1) ∨
      point = (tip.1+1,tip.2+3)
  else
    point = (tip.1-2,tip.2+1) ∨ point = (tip.1-1,tip.2+1) ∨
      point = (tip.1-1,tip.2+3))

def perpendicularSupport (tip : Point) (up : Bool) : Point :=
  if up then (tip.1-1,tip.2) else (tip.1+1,tip.2)

theorem the_left_column_contains_only_the_rotor_tip
    (tip point : Point) (up : Bool) (hcolumn : point.2 = tip.2)
    (hpoint : leftRotorEndpoint tip up point) : point = tip := by
  rcases tip with ⟨tipRow,tipColumn⟩
  rcases point with ⟨row,column⟩
  cases up <;> simp_all [leftRotorEndpoint, Prod.mk.injEq] <;> omega

theorem the_perpendicular_support_is_not_an_own_endpoint
    (tip : Point) (up : Bool) :
    ¬leftRotorEndpoint tip up (perpendicularSupport tip up) := by
  rcases tip with ⟨tipRow,tipColumn⟩
  cases up <;> simp [leftRotorEndpoint, perpendicularSupport, Prod.mk.injEq] <;> omega

theorem every_left_rotor_has_the_same_three_point_spine
    (tip : Point) (up : Bool) (row : Int)
    (hrow : tip.1-1 ≤ row ∧ row ≤ tip.1+1) :
    leftRotorEndpoint tip up (row,tip.2+2) := by
  unfold leftRotorEndpoint
  exact Or.inr (Or.inr (Or.inl ⟨hrow,rfl⟩))

theorem a_confined_rotors_perpendicular_support_is_inside
    (lower upper first : Int) (tip : Point) (up : Bool)
    (hcolumn : tip.2 = first+1)
    (hconfined : ∀ point, leftRotorEndpoint tip up point →
      inside lower upper first point) :
    inside lower upper first (perpendicularSupport tip up) := by
  have hnorth := hconfined (tip.1-1,tip.2+2)
    (every_left_rotor_has_the_same_three_point_spine tip up (tip.1-1) (by omega))
  have hsouth := hconfined (tip.1+1,tip.2+2)
    (every_left_rotor_has_the_same_three_point_spine tip up (tip.1+1) (by omega))
  unfold inside at hnorth hsouth ⊢
  unfold perpendicularSupport
  cases up <;> dsimp <;> omega

theorem adjacent_left_tips_force_a_shared_original_endpoint
    (tip nextTip : Point) (up nextUp : Bool)
    (hcolumn : nextTip.2 = tip.2)
    (hrow : nextTip.1 = tip.1-1 ∨ nextTip.1 = tip.1+1) :
    leftRotorEndpoint tip up (tip.1,tip.2+2) ∧
      leftRotorEndpoint nextTip nextUp (tip.1,tip.2+2) := by
  constructor
  · exact every_left_rotor_has_the_same_three_point_spine tip up tip.1 (by omega)
  · have hequal : (tip.1,tip.2+2) = (tip.1,nextTip.2+2) := by
      apply Prod.ext <;> dsimp <;> omega
    rw [hequal]
    exact every_left_rotor_has_the_same_three_point_spine nextTip nextUp tip.1 (by omega)

theorem no_disjoint_rotor_cluster_can_consume_all_perpendicular_supports
    {Owner : Type} (tip : Owner → Point) (up : Owner → Bool) (column : Int)
    (hcolumn : ∀ owner, (tip owner).2 = column)
    (hdisjoint : ∀ owner other point,
      leftRotorEndpoint (tip owner) (up owner) point →
      leftRotorEndpoint (tip other) (up other) point → owner = other)
    (hforced : ∀ owner, ∃ other,
      leftRotorEndpoint (tip other) (up other) (perpendicularSupport (tip owner) (up owner)))
    (owner : Owner) : False := by
  obtain ⟨other,hconsumer⟩ := hforced owner
  have htip := the_left_column_contains_only_the_rotor_tip
    (tip other) (perpendicularSupport (tip owner) (up owner)) (up other)
    (by cases up owner <;> simp [perpendicularSupport,hcolumn]) hconsumer
  have htiprow : (tip other).1 = (tip owner).1-1 ∨
      (tip other).1 = (tip owner).1+1 := by
    have hcoordinates := congrArg Prod.fst htip
    have hsupportrow : (perpendicularSupport (tip owner) (up owner)).1 = (tip owner).1-1 ∨
        (perpendicularSupport (tip owner) (up owner)).1 = (tip owner).1+1 := by
      cases hcase : up owner <;> simp [perpendicularSupport,hcase]
    rcases hsupportrow with hrow | hrow
    · exact Or.inl (hcoordinates.symm.trans hrow)
    · exact Or.inr (hcoordinates.symm.trans hrow)
  have hshared := adjacent_left_tips_force_a_shared_original_endpoint
    (tip owner) (tip other) (up owner) (up other)
    (by rw [hcolumn owner,hcolumn other]) htiprow
  have hsame := hdisjoint owner other ((tip owner).1,(tip owner).2+2)
    hshared.1 hshared.2
  subst other
  exact the_perpendicular_support_is_not_an_own_endpoint (tip owner) (up owner) hconsumer

def uEndpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def returningEndpoint (incident far : Int) (point : Point) : Prop :=
  uEndpoint 6 incident far (incident+3-point.1,point.2-1)

def cornerEndpoint (incident far : Int) (point : Point) : Prop :=
  uEndpoint 6 (incident-2) far (point.1-3,point.2-2)

theorem the_H_return_has_a_corner_punctured_endpoint_boundary
    (incident returningFar cornerFar : Int) (point : Point)
    (_hincident : 6 ≤ incident) (hfar : incident-2 ≤ cornerFar)
    (hbarrier : barrier 4 (incident+2) 3 point) :
    returningEndpoint incident returningFar point ∨ cornerEndpoint incident cornerFar point := by
  unfold barrier at hbarrier
  unfold returningEndpoint cornerEndpoint uEndpoint
  dsimp
  omega

theorem neither_fixed_owner_consumes_a_first_interior_column_point
    (incident returningFar cornerFar : Int) (point : Point)
    (hinside : inside 4 (incident+2) 3 point) (hcolumn : point.2 = 4) :
    ¬returningEndpoint incident returningFar point ∧
      ¬cornerEndpoint incident cornerFar point := by
  unfold inside at hinside
  unfold returningEndpoint cornerEndpoint uEndpoint
  dsimp
  omega

theorem every_shorter_return_forces_an_interior_cap_with_two_endpoint_neighbors
    (incident returningFar cornerFar : Int)
    (_hincident : 6 ≤ incident) (hreturn : 4 ≤ returningFar)
    (hshort : returningFar ≤ incident-4) (hfar : incident-2 ≤ cornerFar) :
    inside 4 (incident+2) 3 (incident+2-returningFar,7) ∧
      returningEndpoint incident returningFar (incident+3-returningFar,7) ∧
      cornerEndpoint incident cornerFar (incident+2-returningFar,8) := by
  unfold inside returningEndpoint cornerEndpoint uEndpoint
  dsimp
  omega

end SubQuorum.FourColumnCornerBarrier
