import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.OpposedStemSupportGap

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

def leftEndpoint (width near far : Int) (point : Point) : Prop :=
  endpoint width near far (point.2,point.1+width)

def rightEndpoint (width near far gap : Int) (point : Point) : Prop :=
  endpoint width near far (far+2-point.2,width-gap-point.1)

def inside (gap far : Int) (point : Point) : Prop :=
  -gap < point.1 ∧ point.1 < 0 ∧ 1 < point.2 ∧ point.2 < far+1

def boundary (gap far : Int) (point : Point) : Prop :=
  -gap ≤ point.1 ∧ point.1 ≤ 0 ∧ 1 ≤ point.2 ∧ point.2 ≤ far+1 ∧
    (point.1 = -gap ∨ point.1 = 0 ∨ point.2 = 1 ∨ point.2 = far+1)

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

def cornerEndpoint (leg near far : Int) (point : Point) : Prop :=
  endpoint (leg-2) near far (point.2-3,point.1-2)

def crossEndpoint (width height far : Int) (point : Point) : Prop :=
  endpoint width height far (height+2-point.2,point.1-1)

def shortReturnEndpoint (leg : Int) (point : Point) : Prop :=
  endpoint 6 8 4 (11-point.2,leg+2-point.1)

def northEscapeEndpoint (width incident far leg : Int) (point : Point) : Prop :=
  endpoint width incident far (point.1-(leg-1-incident),point.2-4)

theorem the_two_original_endpoint_sets_are_disjoint
    (width otherWidth near otherNear far gap : Int) (point : Point)
    (hwidth : 6 ≤ width) (hotherWidth : 6 ≤ otherWidth)
    (hfar : 4 ≤ far) (hgap : gap = 2 ∨ gap = 3) :
    ¬(leftEndpoint width near far point ∧ rightEndpoint otherWidth otherNear far gap point) := by
  unfold leftEndpoint rightEndpoint endpoint
  dsimp
  rcases hgap with hgap | hgap <;> omega

theorem the_chamber_boundary_has_only_fixed_owners
    (width otherWidth near otherNear far gap : Int) (point : Point)
    (hwidth : 6 ≤ width) (hotherWidth : 6 ≤ otherWidth)
    (hfar : 4 ≤ far) (hgap : gap = 2 ∨ gap = 3)
    (hboundary : boundary gap far point) :
    leftEndpoint width near far point ∨ rightEndpoint otherWidth otherNear far gap point := by
  unfold boundary at hboundary
  unfold leftEndpoint rightEndpoint endpoint
  dsimp at *
  rcases hgap with hgap | hgap <;> omega

theorem neither_fixed_owner_has_an_interior_endpoint
    (width otherWidth near otherNear far gap : Int) (point : Point)
    (hwidth : 6 ≤ width) (hotherWidth : 6 ≤ otherWidth)
    (hgap : gap = 2 ∨ gap = 3) (hinside : inside gap far point) :
    ¬leftEndpoint width near far point ∧ ¬rightEndpoint otherWidth otherNear far gap point := by
  unfold inside at hinside
  unfold leftEndpoint rightEndpoint endpoint
  dsimp at *
  rcases hgap with hgap | hgap <;> omega

theorem the_original_inner_support_has_its_fixed_anchor
    (width near far gap : Int) (_hwidth : 6 ≤ width) (hfar : 4 ≤ far)
    (hgap : gap = 2 ∨ gap = 3) :
    support width near far (3,width-1) ∧
      leftEndpoint width near far (0,3) ∧ inside gap far (-1,3) := by
  unfold support leftEndpoint endpoint inside
  dsimp
  rcases hgap with hgap | hgap <;> omega

theorem gap_two_has_a_second_fixed_endpoint_neighbor
    (width near far : Int) (_hwidth : 6 ≤ width) (hfar : 4 ≤ far) :
    rightEndpoint width near far 2 (-2,3) := by
  unfold rightEndpoint endpoint
  dsimp
  omega

theorem gap_three_has_an_adjacent_mandatory_support
    (width near far halfFar : Int) (hfar : 4 ≤ far) (heven : far = 2*halfFar) :
    support width near far (far-1,width-1) ∧ adjacent (-1,3) (-2,3) := by
  unfold support adjacent
  dsimp
  omega

theorem a_second_occupied_neighbor_forces_endpoint_consumption
    (occupied endpointAt : Point → Prop)
    (hoccupied : occupied (-2,3))
    (hselected : ¬endpointAt (-1,3) →
      ∀ point, adjacent (-1,3) point → occupied point → point = (0,3)) :
    endpointAt (-1,3) := by
  apply Classical.byContradiction
  intro hnot
  have hequal := hselected hnot (-2,3) (by unfold adjacent; simp) hoccupied
  have hrows := congrArg Prod.fst hequal
  dsimp at hrows
  omega

theorem an_avoiding_unit_step_stays_inside
    (gap far : Int) (point next : Point) (hinside : inside gap far point)
    (hstep : adjacent point next) (havoid : ¬boundary gap far next) :
    inside gap far next := by
  unfold inside at hinside ⊢
  unfold adjacent at hstep
  unfold boundary at havoid
  rcases hstep with hstep | hstep | hstep | hstep <;> omega

theorem an_avoiding_unit_walk_stays_inside
    (gap far : Int) (length : Nat) (path : Nat → Point)
    (hstart : inside gap far (path 0))
    (hsteps : ∀ index, index < length → adjacent (path index) (path (index+1)))
    (havoid : ∀ index, index ≤ length → ¬boundary gap far (path index)) :
    inside gap far (path length) := by
  induction length with
  | zero => exact hstart
  | succ length inductionHypothesis =>
    have hprevious := inductionHypothesis
      (fun index hindex => hsteps index (by omega))
      (fun index hindex => havoid index (by omega))
    exact an_avoiding_unit_step_stays_inside gap far
      (path length) (path (length+1)) hprevious (hsteps length (by omega))
      (havoid (length+1) (by omega))

theorem a_foreign_source_cannot_consume_the_inner_support
    (gap far : Int) (belongs : Point → Prop) (hfar : 4 ≤ far)
    (hgap : gap = 2 ∨ gap = 3)
    (hconnected : connectedEndpoints belongs) (hseed : belongs (-1,3))
    (havoid : ∀ point, belongs point → ¬boundary gap far point)
    (hextent : ∃ point next, belongs point ∧ belongs next ∧ point.1+3 ≤ next.1) : False := by
  have hinside : inside gap far (-1,3) := by
    unfold inside
    dsimp
    rcases hgap with hgap | hgap <;> omega
  have hall : ∀ point, belongs point → inside gap far point := by
    intro point hpoint
    obtain ⟨length,path,hstart,hend,hbelongs,hsteps⟩ := hconnected (-1,3) point hseed hpoint
    have hresult := an_avoiding_unit_walk_stays_inside gap far length path
      (hstart ▸ hinside) hsteps
      (fun index hindex => havoid (path index) (hbelongs index hindex))
    exact hend ▸ hresult
  obtain ⟨point,next,hpoint,hnext,hseparation⟩ := hextent
  have hfirst := hall point hpoint
  have hlast := hall next hnext
  unfold inside at hfirst hlast
  rcases hgap with hgap | hgap <;> omega

theorem the_opposed_sources_have_no_complete_endpoint_family
    (Owner : Type) (leftOwner rightOwner : Owner)
    (originalEndpoints : Owner → Point → Prop) (occupied : Point → Prop)
    (width otherWidth near otherNear far gap halfFar : Int)
    (hwidth : 6 ≤ width) (hotherWidth : 6 ≤ otherWidth)
    (hfar : 4 ≤ far) (hevenFar : far = 2*halfFar) (hgap : gap = 2 ∨ gap = 3)
    (hleft : ∀ point, originalEndpoints leftOwner point ↔ leftEndpoint width near far point)
    (hright : ∀ point,
      originalEndpoints rightOwner point ↔ rightEndpoint otherWidth otherNear far gap point)
    (hunique : ∀ first second point,
      originalEndpoints first point → originalEndpoints second point → first = second)
    (hconnected : ∀ owner, connectedEndpoints (originalEndpoints owner))
    (hextent : ∀ owner, ∃ point next,
      originalEndpoints owner point ∧ originalEndpoints owner next ∧ point.1+3 ≤ next.1)
    (hendpointOccupied : ∀ owner point, originalEndpoints owner point → occupied point)
    (hrightSupportOccupied : ∀ point,
      support otherWidth otherNear far (far+2-point.2,otherWidth-gap-point.1) → occupied point)
    (hselected : support width near far (3,width-1) →
      ¬(∃ owner, originalEndpoints owner (-1,3)) →
      ∀ point, adjacent (-1,3) point → occupied point → point = (0,3)) : False := by
  have hmandatory :=
    (the_original_inner_support_has_its_fixed_anchor width near far gap hwidth hfar hgap).1
  have hsecond : occupied (-2,3) := by
    rcases hgap with hgap | hgap
    · have hpoint : rightEndpoint otherWidth otherNear far gap (-2,3) := by
        rw [hgap]
        exact gap_two_has_a_second_fixed_endpoint_neighbor otherWidth otherNear far hotherWidth hfar
      exact hendpointOccupied rightOwner (-2,3) ((hright (-2,3)).mpr hpoint)
    · apply hrightSupportOccupied (-2,3)
      dsimp
      rw [hgap]
      have hsupport := (gap_three_has_an_adjacent_mandatory_support
        otherWidth otherNear far halfFar hfar hevenFar).1
      have hcoordinates :
          (far+2-3,otherWidth-3-(-2)) = (far-1,otherWidth-1) := by
        apply Prod.ext <;> dsimp <;> omega
      rw [hcoordinates]
      exact hsupport
  obtain ⟨consumer,hconsumer⟩ := a_second_occupied_neighbor_forces_endpoint_consumption
    occupied (fun point => ∃ owner, originalEndpoints owner point) hsecond (hselected hmandatory)
  have hinside : inside gap far (-1,3) := by
    unfold inside
    dsimp
    rcases hgap with hgap | hgap <;> omega
  have hfixed := neither_fixed_owner_has_an_interior_endpoint
    width otherWidth near otherNear far gap (-1,3) hwidth hotherWidth hgap hinside
  have hnotLeft : consumer ≠ leftOwner := by
    intro hequal
    exact hfixed.1 ((hleft (-1,3)).mp (hequal ▸ hconsumer))
  have hnotRight : consumer ≠ rightOwner := by
    intro hequal
    exact hfixed.2 ((hright (-1,3)).mp (hequal ▸ hconsumer))
  apply a_foreign_source_cannot_consume_the_inner_support
    gap far (originalEndpoints consumer) hfar hgap (hconnected consumer) hconsumer
    ?_ (hextent consumer)
  intro point hpoint hboundary
  rcases the_chamber_boundary_has_only_fixed_owners
      width otherWidth near otherNear far gap point hwidth hotherWidth hfar hgap hboundary
      with hleftPoint | hrightPoint
  · exact hnotLeft (hunique consumer leftOwner point hpoint ((hleft point).mpr hleftPoint))
  · exact hnotRight (hunique consumer rightOwner point hpoint ((hright point).mpr hrightPoint))

theorem a_cross_owner_of_the_lower_missing_corner_would_overlap_X
    (leg near far width height crossFar halfHeight halfFar : Int)
    (hleg : 8 ≤ leg) (hheight : 8 ≤ height)
    (hevenHeight : height = 2*halfHeight) (hevenFar : crossFar = 2*halfFar)
    (howns : crossEndpoint width height crossFar (leg-1,5)) :
    crossEndpoint width height crossFar (leg-1,4) ∧
      cornerEndpoint leg near far (leg-1,4) := by
  unfold crossEndpoint at howns ⊢
  unfold cornerEndpoint endpoint at *
  dsimp at *
  omega

theorem the_cross_cannot_own_the_upper_missing_corner
    (leg width height crossFar halfLeg halfWidth : Int)
    (hleg : 8 ≤ leg) (hheight : 8 ≤ height)
    (hevenLeg : leg = 2*halfLeg) (hevenWidth : width = 2*halfWidth) :
    ¬crossEndpoint width height crossFar (leg-2,5) := by
  unfold crossEndpoint endpoint
  dsimp
  omega

theorem incident_four_hits_the_short_return
    (width far leg : Int) (hwidth : 6 ≤ width) :
    northEscapeEndpoint width 4 far leg (leg-4,10) ∧
      shortReturnEndpoint leg (leg-4,10) := by
  unfold northEscapeEndpoint shortReturnEndpoint endpoint
  dsimp
  omega

theorem a_north_escape_starting_above_row_three_hits_C
    (width incident far leg crossWidth height crossFar : Int)
    (hwidth : 6 ≤ width) (hleg : 8 ≤ leg) (hheight : 8 ≤ height)
    (hstart : leg-1-incident ≤ 2) :
    northEscapeEndpoint width incident far leg (2,5) ∧
      crossEndpoint crossWidth height crossFar (2,5) := by
  unfold northEscapeEndpoint crossEndpoint endpoint
  dsimp
  omega

theorem a_north_escape_starting_on_row_three_hits_X
    (width incident far leg near cornerFar : Int)
    (hwidth : 6 ≤ width) (hnear : 4 ≤ near) (hleg : 8 ≤ leg)
    (hstart : leg-1-incident = 3) :
    northEscapeEndpoint width incident far leg (3,5) ∧
      cornerEndpoint leg near cornerFar (3,5) := by
  unfold northEscapeEndpoint cornerEndpoint endpoint
  dsimp
  omega

theorem the_remaining_even_escape_range
    (leg incident halfLeg halfIncident : Int)
    (hevenLeg : leg = 2*halfLeg) (hevenIncident : incident = 2*halfIncident)
    (hminimum : 4 ≤ incident) (hnotFour : incident ≠ 4)
    (hstart : 4 ≤ leg-1-incident) :
    6 ≤ incident ∧ incident ≤ leg-6 ∧ 12 ≤ leg := by
  omega

theorem small_incident_legs_have_no_escape
    (leg incident : Int) (hsmall : leg = 8 ∨ leg = 10)
    (hlower : 6 ≤ incident) (hupper : incident ≤ leg-6) : False := by
  rcases hsmall with hsmall | hsmall <;> omega

theorem neither_missing_corner_is_an_original_X_support
    (leg near far : Int) (hleg : 8 ≤ leg) :
    ¬support (leg-2) near far (2,leg-4) ∧ ¬support (leg-2) near far (2,leg-3) := by
  unfold support
  dsimp
  omega

end SubQuorum.OpposedStemSupportGap
