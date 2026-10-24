import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.MaximalHReturnRigidity

abbrev Point := Int × Int

def uEndpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def returningEndpoint (incident : Int) (point : Point) : Prop :=
  uEndpoint 6 incident (incident-2) (incident+3-point.1,point.2-1)

def cornerEndpoint (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (point.1-3,point.2-2)

def inside (incident : Int) (point : Point) : Prop :=
  4 < point.1 ∧ point.1 < incident+2 ∧ 2 < point.2 ∧ point.2 < 7

def boundary (incident : Int) (point : Point) : Prop :=
  4 ≤ point.1 ∧ point.1 ≤ incident+2 ∧ 2 ≤ point.2 ∧ point.2 ≤ 7 ∧
  (point.1 = 4 ∨ point.1 = incident+2 ∨ point.2 = 2 ∨ point.2 = 7)

theorem the_maximal_return_and_corner_fill_the_entire_boundary
    (incident width near far : Int) (point : Point)
    (hincident : 6 ≤ incident) (hwidth : 6 ≤ width)
    (hboundary : boundary incident point) :
    returningEndpoint incident point ∨ cornerEndpoint width near far point := by
  unfold boundary at hboundary
  unfold returningEndpoint cornerEndpoint uEndpoint
  dsimp
  omega

theorem neither_fixed_owner_occupies_the_last_interior_column
    (incident width near far : Int) (point : Point)
    (hwidth : 6 ≤ width) (hinside : inside incident point) (hcolumn : point.2 = 6) :
    ¬returningEndpoint incident point ∧ ¬cornerEndpoint width near far point := by
  unfold inside at hinside
  unfold returningEndpoint cornerEndpoint uEndpoint
  dsimp
  omega

theorem reflection_preserves_the_interior_and_exchanges_the_extreme_columns
    (incident : Int) (point : Point) (hinside : inside incident point) :
    inside incident (point.1,9-point.2) ∧ (point.2 = 6 ↔ 9-point.2 = 3) := by
  unfold inside at hinside ⊢
  dsimp
  omega

theorem a_short_near_leg_forces_an_unowned_interior_support_and_two_neighbors
    (incident width near far : Int)
    (hwidth : 6 ≤ width) (hnear : 4 ≤ near) (hshort : near < incident-2) :
    inside incident (near+4,3) ∧
      ¬returningEndpoint incident (near+4,3) ∧
      ¬cornerEndpoint width near far (near+4,3) ∧
      cornerEndpoint width near far (near+3,3) ∧
      returningEndpoint incident (near+4,2) := by
  unfold inside returningEndpoint cornerEndpoint uEndpoint
  dsimp
  omega

theorem completeness_and_the_reflected_barrier_force_the_near_leg
    (incident width near far : Int) (endpoint : Point → Prop)
    (hwidth : 6 ≤ width) (hnear : 4 ≤ near) (hupper : near ≤ incident-2)
    (hforced : near < incident-2 → endpoint (near+4,3))
    (hnoforeign : ∀ point, inside incident point → endpoint point →
      returningEndpoint incident point ∨ cornerEndpoint width near far point) :
    near = incident-2 := by
  by_cases hequal : near = incident-2
  · exact hequal
  have hshort : near < incident-2 := by omega
  have hgeometry := a_short_near_leg_forces_an_unowned_interior_support_and_two_neighbors
    incident width near far hwidth hnear hshort
  rcases hnoforeign (near+4,3) hgeometry.1 (hforced hshort) with hreturn | hcorner
  · exact False.elim (hgeometry.2.1 hreturn)
  · exact False.elim (hgeometry.2.2.1 hcorner)

end SubQuorum.MaximalHReturnRigidity
