import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.ShortReturnRotorCavity

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

def cornerEndpoint (leg near : Int) (point : Point) : Prop :=
  endpoint (leg-2) near 4 (point.2-3,point.1-2)

def returnEndpoint (leg : Int) (point : Point) : Prop :=
  endpoint 6 8 4 (11-point.2,leg+2-point.1)

def rotorEndpoint (leg : Int) (point : Point) : Prop :=
  (point.1 = leg-3 ∧ point.2 = 7) ∨
  (point.1 = leg-2 ∧ 7 ≤ point.2 ∧ point.2 ≤ 9) ∨
  (point.1 = leg-1 ∧ 6 ≤ point.2 ∧ point.2 ≤ 8) ∨
  (point.1 = leg ∧ point.2 = 8)

def rotorSupport (leg : Int) (point : Point) : Prop :=
  point = (leg-4,7) ∨ point = (leg-3,6) ∨ point = (leg-3,9) ∨
  point = (leg-2,10) ∨ point = (leg-1,5) ∨ point = (leg,6) ∨
  point = (leg,9) ∨ point = (leg+1,8)

def adjacent (point next : Point) : Prop :=
  (next.1 = point.1-1 ∧ next.2 = point.2) ∨
  (next.1 = point.1+1 ∧ next.2 = point.2) ∨
  (next.1 = point.1 ∧ next.2 = point.2-1) ∨
  (next.1 = point.1 ∧ next.2 = point.2+1)

def inside (leg : Int) (point : Point) : Prop :=
  leg-4 < point.1 ∧ point.1 < leg-2 ∧ 7 < point.2 ∧ point.2 < 10

def boundary (leg : Int) (point : Point) : Prop :=
  leg-4 ≤ point.1 ∧ point.1 ≤ leg-2 ∧ 7 ≤ point.2 ∧ point.2 ≤ 10 ∧
    (point.1 = leg-4 ∨ point.1 = leg-2 ∨ point.2 = 7 ∨ point.2 = 10)

def connectedEndpoints (belongs : Point → Prop) : Prop :=
  ∀ point next, belongs point → belongs next →
    ∃ length : Nat, ∃ path : Nat → Point,
      path 0 = point ∧ path length = next ∧
      (∀ index, index ≤ length → belongs (path index)) ∧
      (∀ index, index < length → adjacent (path index) (path (index+1)))

theorem the_prescribed_corner_and_return_are_disjoint
    (leg near : Int) (point : Point) (hleg : 8 ≤ leg) :
    ¬(cornerEndpoint leg near point ∧ returnEndpoint leg point) := by
  unfold cornerEndpoint returnEndpoint endpoint
  dsimp
  omega

theorem the_forced_point_is_an_original_return_support (leg : Int) :
    support 6 8 4 (11-8,leg+2-leg) := by
  unfold support
  omega

theorem the_two_forcing_neighbors_are_fixed_endpoints (leg near : Int) :
    cornerEndpoint leg near (leg,7) ∧ returnEndpoint leg (leg+1,8) := by
  unfold cornerEndpoint returnEndpoint endpoint
  dsimp
  omega

theorem neither_fixed_owner_has_the_forced_point
    (leg near : Int) (hleg : 8 ≤ leg) :
    ¬cornerEndpoint leg near (leg,8) ∧ ¬returnEndpoint leg (leg,8) := by
  unfold cornerEndpoint returnEndpoint endpoint
  dsimp
  omega

theorem a_north_terminal_hits_the_return_far_stem
    (width incident far : Int) (hwidth : 6 ≤ width) (hincident : 4 ≤ incident) :
    endpoint width incident far (incident-4,1) := by
  unfold endpoint
  dsimp
  omega

theorem an_east_terminal_hits_the_return_bar
    (width incident far : Int) (hwidth : 6 ≤ width) (hincident : 4 ≤ incident) :
    endpoint width incident far (incident-2,1) := by
  unfold endpoint
  dsimp
  omega

theorem a_north_outer_bar_hits_the_return_far_stem
    (width near far : Int) (hwidth : 6 ≤ width) : endpoint width near far (0,5) := by
  unfold endpoint
  dsimp
  omega

theorem an_east_outer_bar_hits_the_return_bar
    (width near far : Int) (hwidth : 6 ≤ width) : endpoint width near far (0,3) := by
  unfold endpoint
  dsimp
  omega

theorem all_three_catalogue_blockers_are_return_endpoints (leg : Int) :
    returnEndpoint leg (leg-4,8) ∧ returnEndpoint leg (leg,10) ∧
      returnEndpoint leg (leg-1,10) := by
  unfold returnEndpoint endpoint
  dsimp
  omega

theorem the_return_and_surviving_rotor_are_disjoint (leg : Int) (point : Point) :
    ¬(returnEndpoint leg point ∧ rotorEndpoint leg point) := by
  unfold returnEndpoint rotorEndpoint endpoint
  dsimp
  omega

theorem the_cavity_boundary_is_owned (leg : Int) (point : Point)
    (hboundary : boundary leg point) :
    returnEndpoint leg point ∨ rotorEndpoint leg point := by
  unfold boundary at hboundary
  unfold returnEndpoint rotorEndpoint endpoint
  dsimp at *
  omega

theorem neither_fixed_source_has_an_interior_endpoint (leg : Int) (point : Point)
    (hinside : inside leg point) :
    ¬returnEndpoint leg point ∧ ¬rotorEndpoint leg point := by
  unfold inside at hinside
  unfold returnEndpoint rotorEndpoint endpoint
  dsimp at *
  omega

theorem the_rotor_support_and_both_anchors_are_exact (leg : Int) :
    rotorSupport leg (leg-3,9) ∧ rotorEndpoint leg (leg-2,9) ∧
      returnEndpoint leg (leg-4,9) := by
  refine ⟨?_, ?_, ?_⟩
  · simp [rotorSupport]
  · unfold rotorEndpoint
    dsimp
    omega
  · unfold returnEndpoint endpoint
    dsimp
    omega

theorem the_other_cavity_point_is_a_return_support (leg : Int) :
    support 6 8 4 (11-8,leg+2-(leg-3)) ∧ rotorEndpoint leg (leg-3,7) := by
  unfold support rotorEndpoint
  dsimp
  omega

theorem an_avoiding_unit_step_stays_inside
    (leg : Int) (point next : Point) (hinside : inside leg point)
    (hstep : adjacent point next) (havoid : ¬boundary leg next) : inside leg next := by
  unfold inside at hinside ⊢
  unfold adjacent at hstep
  unfold boundary at havoid
  rcases hstep with hstep | hstep | hstep | hstep <;> omega

theorem an_avoiding_unit_walk_stays_inside
    (leg : Int) (length : Nat) (path : Nat → Point)
    (hstart : inside leg (path 0))
    (hsteps : ∀ index, index < length → adjacent (path index) (path (index+1)))
    (havoid : ∀ index, index ≤ length → ¬boundary leg (path index)) :
    inside leg (path length) := by
  induction length with
  | zero => exact hstart
  | succ length inductionHypothesis =>
    have hprevious := inductionHypothesis
      (fun index hindex => hsteps index (by omega))
      (fun index hindex => havoid index (by omega))
    exact an_avoiding_unit_step_stays_inside leg (path length) (path (length+1))
      hprevious (hsteps length (by omega)) (havoid (length+1) (by omega))

theorem no_foreign_source_can_consume_the_cavity_support
    (leg : Int) (belongs : Point → Prop)
    (hconnected : connectedEndpoints belongs) (hseed : belongs (leg-3,9))
    (havoid : ∀ point, belongs point → ¬boundary leg point)
    (hextent : ∃ point next, belongs point ∧ belongs next ∧ point.1+3 ≤ next.1) : False := by
  have hinside : inside leg (leg-3,9) := by unfold inside; dsimp; omega
  have hall : ∀ point, belongs point → inside leg point := by
    intro point hpoint
    obtain ⟨length,path,hstart,hend,hbelongs,hsteps⟩ :=
      hconnected (leg-3,9) point hseed hpoint
    have hresult := an_avoiding_unit_walk_stays_inside leg length path
      (hstart ▸ hinside) hsteps
      (fun index hindex => havoid (path index) (hbelongs index hindex))
    exact hend ▸ hresult
  obtain ⟨point,next,hpoint,hnext,hseparation⟩ := hextent
  have hfirst := hall point hpoint
  have hlast := hall next hnext
  unfold inside at hfirst hlast
  omega

theorem the_return_and_rotor_have_no_complete_endpoint_family
    (Owner : Type) (returnOwner rotorOwner : Owner)
    (belongs : Owner → Point → Prop) (occupied : Point → Prop) (leg : Int)
    (hreturn : ∀ point, belongs returnOwner point ↔ returnEndpoint leg point)
    (hrotor : ∀ point, belongs rotorOwner point ↔ rotorEndpoint leg point)
    (hunique : ∀ first second point, belongs first point → belongs second point → first = second)
    (hconnected : ∀ owner, connectedEndpoints (belongs owner))
    (hextent : ∀ owner, ∃ point next,
      belongs owner point ∧ belongs owner next ∧ point.1+3 ≤ next.1)
    (hoccupied : ∀ owner point, belongs owner point → occupied point)
    (hretain : (¬∃ owner, belongs owner (leg-3,9)) →
      ∀ point, adjacent (leg-3,9) point → occupied point → point = (leg-2,9)) : False := by
  have hconsumer : ∃ owner, belongs owner (leg-3,9) := by
    apply Classical.byContradiction
    intro hnot
    have hfixed := (the_rotor_support_and_both_anchors_are_exact leg).2.2
    have hequal := hretain hnot (leg-4,9)
      (by unfold adjacent; dsimp; omega)
      (hoccupied returnOwner (leg-4,9) ((hreturn (leg-4,9)).mpr hfixed))
    have hrows := congrArg Prod.fst hequal
    dsimp at hrows
    omega
  obtain ⟨consumer,hconsumer⟩ := hconsumer
  have hinside : inside leg (leg-3,9) := by unfold inside; dsimp; omega
  have hfixed := neither_fixed_source_has_an_interior_endpoint leg (leg-3,9) hinside
  have hnotReturn : consumer ≠ returnOwner := by
    intro hequal
    exact hfixed.1 ((hreturn (leg-3,9)).mp (hequal ▸ hconsumer))
  have hnotRotor : consumer ≠ rotorOwner := by
    intro hequal
    exact hfixed.2 ((hrotor (leg-3,9)).mp (hequal ▸ hconsumer))
  apply no_foreign_source_can_consume_the_cavity_support leg (belongs consumer)
    (hconnected consumer) hconsumer ?_ (hextent consumer)
  intro point hpoint hboundary
  rcases the_cavity_boundary_is_owned leg point hboundary with hreturnPoint | hrotorPoint
  · exact hnotReturn (hunique consumer returnOwner point hpoint ((hreturn point).mpr hreturnPoint))
  · exact hnotRotor (hunique consumer rotorOwner point hpoint ((hrotor point).mpr hrotorPoint))

theorem the_forced_consumer_is_the_surviving_rotor
    (Owner : Type) (returnOwner consumer : Owner) (belongs : Owner → Point → Prop)
    (leg : Int) (hnot : consumer ≠ returnOwner)
    (hreturn : ∀ point, belongs returnOwner point ↔ returnEndpoint leg point)
    (hunique : ∀ first second point, belongs first point → belongs second point → first = second)
    (hcatalogue : belongs consumer (leg-4,8) ∨ belongs consumer (leg,10) ∨
      belongs consumer (leg-1,10) ∨ (∀ point, belongs consumer point ↔ rotorEndpoint leg point)) :
    ∀ point, belongs consumer point ↔ rotorEndpoint leg point := by
  have hfixed := all_three_catalogue_blockers_are_return_endpoints leg
  rcases hcatalogue with hfirst | hsecond | hthird | hrotor
  · exact False.elim (hnot (hunique consumer returnOwner (leg-4,8) hfirst
      ((hreturn (leg-4,8)).mpr hfixed.1)))
  · exact False.elim (hnot (hunique consumer returnOwner (leg,10) hsecond
      ((hreturn (leg,10)).mpr hfixed.2.1)))
  · exact False.elim (hnot (hunique consumer returnOwner (leg-1,10) hthird
      ((hreturn (leg-1,10)).mpr hfixed.2.2)))
  · exact hrotor

theorem far_leg_six_is_not_the_forced_point_argument (leg near : Int) :
    endpoint (leg-2) near 6 (8-3,leg-2) ∧ returnEndpoint leg (leg,10) := by
  unfold returnEndpoint endpoint
  dsimp
  omega

theorem the_return_support_must_be_consumed
    (occupied endpointAt : Point → Prop) (leg : Int)
    (hwest : occupied (leg,7))
    (hretain : ¬endpointAt (leg,8) →
      ∀ point, adjacent (leg,8) point → occupied point → point = (leg+1,8)) :
    endpointAt (leg,8) := by
  apply Classical.byContradiction
  intro hnot
  have hequal := hretain hnot (leg,7) (by unfold adjacent; dsimp; omega) hwest
  have hcolumns := congrArg Prod.snd hequal
  dsimp at hcolumns
  omega

theorem the_corner_and_return_have_no_complete_endpoint_family
    (Owner : Type) (cornerOwner returnOwner : Owner)
    (belongs : Owner → Point → Prop) (occupied : Point → Prop)
    (leg near : Int) (hleg : 8 ≤ leg)
    (hcorner : ∀ point, belongs cornerOwner point ↔ cornerEndpoint leg near point)
    (hreturn : ∀ point, belongs returnOwner point ↔ returnEndpoint leg point)
    (hunique : ∀ first second point, belongs first point → belongs second point → first = second)
    (hconnected : ∀ owner, connectedEndpoints (belongs owner))
    (hextent : ∀ owner, ∃ point next,
      belongs owner point ∧ belongs owner next ∧ point.1+3 ≤ next.1)
    (hoccupied : ∀ owner point, belongs owner point → occupied point)
    (hretainReturn : (¬∃ owner, belongs owner (leg,8)) →
      ∀ point, adjacent (leg,8) point → occupied point → point = (leg+1,8))
    (hretainRotor : ∀ rotorOwner,
      (∀ point, belongs rotorOwner point ↔ rotorEndpoint leg point) →
      (¬∃ owner, belongs owner (leg-3,9)) →
      ∀ point, adjacent (leg-3,9) point → occupied point → point = (leg-2,9))
    (hcatalogue : ∀ consumer, belongs consumer (leg,8) →
      ¬belongs consumer (leg,7) → ¬belongs consumer (leg+1,8) →
      belongs consumer (leg-4,8) ∨ belongs consumer (leg,10) ∨
      belongs consumer (leg-1,10) ∨
      (∀ point, belongs consumer point ↔ rotorEndpoint leg point)) : False := by
  have hneighbors := the_two_forcing_neighbors_are_fixed_endpoints leg near
  have hwest := hoccupied cornerOwner (leg,7) ((hcorner (leg,7)).mpr hneighbors.1)
  obtain ⟨consumer,hconsumer⟩ := the_return_support_must_be_consumed occupied
    (fun point => ∃ owner, belongs owner point) leg hwest hretainReturn
  have hfixed := neither_fixed_owner_has_the_forced_point leg near hleg
  have hnotCorner : consumer ≠ cornerOwner := by
    intro hequal
    exact hfixed.1 ((hcorner (leg,8)).mp (hequal ▸ hconsumer))
  have hnotReturn : consumer ≠ returnOwner := by
    intro hequal
    exact hfixed.2 ((hreturn (leg,8)).mp (hequal ▸ hconsumer))
  have hnotWest : ¬belongs consumer (leg,7) := by
    intro hpoint
    exact hnotCorner (hunique consumer cornerOwner (leg,7) hpoint
      ((hcorner (leg,7)).mpr hneighbors.1))
  have hnotSouth : ¬belongs consumer (leg+1,8) := by
    intro hpoint
    exact hnotReturn (hunique consumer returnOwner (leg+1,8) hpoint
      ((hreturn (leg+1,8)).mpr hneighbors.2))
  have hrotor := the_forced_consumer_is_the_surviving_rotor Owner returnOwner consumer
    belongs leg hnotReturn hreturn hunique (hcatalogue consumer hconsumer hnotWest hnotSouth)
  exact the_return_and_rotor_have_no_complete_endpoint_family Owner returnOwner consumer
    belongs occupied leg hreturn hrotor hunique hconnected hextent hoccupied
    (hretainRotor consumer hrotor)

end SubQuorum.ShortReturnRotorCavity
