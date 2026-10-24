import SubQuorum.FeasibleCoreSeparator

set_option autoImplicit false

namespace SubQuorum.ContactHullLocalization

open SourceRetentionClosure

variable {Owner Vertex : Type}

def touching (endpoint : Owner → Vertex → Prop) (adjacent : Vertex → Vertex → Prop)
    (inside added : Owner → Prop) (owner : Owner) : Prop :=
  inside owner ∧ ∃ source point neighbor, added source ∧ endpoint owner point ∧
    endpoint source neighbor ∧ adjacent point neighbor

def contactCore (endpoint support : Owner → Vertex → Prop)
    (adjacent : Vertex → Vertex → Prop) (anchor : Owner → Vertex → Vertex)
    (inside added : Owner → Prop) : Owner → Prop :=
  hull endpoint support adjacent anchor (touching endpoint adjacent inside added)

theorem the_contact_core_stays_inside_the_feasible_old_family
    (endpoint support : Owner → Vertex → Prop) (adjacent : Vertex → Vertex → Prop)
    (anchor : Owner → Vertex → Vertex)
    (hanchor : ∀ owner point, support owner point →
      endpoint owner (anchor owner point) ∧ adjacent point (anchor owner point))
    (hunique : ∀ first second point, endpoint first point → endpoint second point → first = second)
    (hfull : feasible endpoint support adjacent (fun _ => True))
    (inside added : Owner → Prop) (hinside : feasible endpoint support adjacent inside) :
    ∀ owner, contactCore endpoint support adjacent anchor inside added owner → inside owner := by
  exact hull_is_least_closed_completion endpoint support adjacent anchor _ inside
    ((feasible_iff_horn_closed endpoint support adjacent anchor hanchor hunique hfull inside).mp
      hinside) (fun _ htouching => htouching.1)

theorem the_contact_core_separates_added_endpoints_from_the_old_remainder
    (endpoint support : Owner → Vertex → Prop) (adjacent : Vertex → Vertex → Prop)
    (anchor : Owner → Vertex → Vertex) (inside added : Owner → Prop)
    (oldOwner newOwner : Owner) (point neighbor : Vertex)
    (hold : inside oldOwner) (hnew : added newOwner)
    (hpoint : endpoint oldOwner point) (hneighbor : endpoint newOwner neighbor)
    (hadjacent : adjacent point neighbor) :
    contactCore endpoint support adjacent anchor inside added oldOwner := by
  exact hull_contains_seed endpoint support adjacent anchor _ oldOwner
    ⟨hold, newOwner, point, neighbor, hnew, hpoint, hneighbor, hadjacent⟩

theorem the_contact_core_with_added_owners_is_complete_feasible
    (endpoint support : Owner → Vertex → Prop) (adjacent : Vertex → Vertex → Prop)
    (anchor : Owner → Vertex → Vertex)
    (hsymmetric : ∀ first second, adjacent first second → adjacent second first)
    (hanchor : ∀ owner point, support owner point →
      endpoint owner (anchor owner point) ∧ adjacent point (anchor owner point))
    (hunique : ∀ first second point, endpoint first point → endpoint second point → first = second)
    (hfull : feasible endpoint support adjacent (fun _ => True))
    (inside added : Owner → Prop) (hcover : ∀ owner, inside owner ∨ added owner)
    (hinside : feasible endpoint support adjacent inside) :
    (∀ owner, contactCore endpoint support adjacent anchor inside added owner → inside owner) ∧
      feasible endpoint support adjacent
        (fun owner => contactCore endpoint support adjacent anchor inside added owner ∨ added owner) := by
  refine ⟨the_contact_core_stays_inside_the_feasible_old_family endpoint support adjacent anchor
    hanchor hunique hfull inside added hinside, ?_⟩
  apply FeasibleCoreSeparator.a_side_of_a_feasible_core_is_feasible endpoint support adjacent
    anchor hsymmetric hanchor hunique hfull
    (contactCore endpoint support adjacent anchor inside added)
    (fun owner => contactCore endpoint support adjacent anchor inside added owner ∨ added owner)
    (hull_is_feasible endpoint support adjacent anchor hanchor hunique hfull _)
    (fun _ hcore => Or.inl hcore)
  intro first second point neighbor hfirst hnotCore hsecond hpoint hneighbor hadjacent
  have hadded := hfirst.resolve_left hnotCore
  have hsecondInside := (hcover second).resolve_right (fun hadded => hsecond (Or.inr hadded))
  exact hsecond (Or.inl (the_contact_core_separates_added_endpoints_from_the_old_remainder
    endpoint support adjacent anchor inside added second first neighbor point
    hsecondInside hadded hneighbor hpoint (hsymmetric point neighbor hadjacent)))

theorem the_contact_core_is_the_least_feasible_contact_carrier
    (endpoint support : Owner → Vertex → Prop) (adjacent : Vertex → Vertex → Prop)
    (anchor : Owner → Vertex → Vertex)
    (hanchor : ∀ owner point, support owner point →
      endpoint owner (anchor owner point) ∧ adjacent point (anchor owner point))
    (hunique : ∀ first second point, endpoint first point → endpoint second point → first = second)
    (hfull : feasible endpoint support adjacent (fun _ => True))
    (inside added keep : Owner → Prop) (hkeep : feasible endpoint support adjacent keep)
    (hcontains : ∀ owner, touching endpoint adjacent inside added owner → keep owner) :
    ∀ owner, contactCore endpoint support adjacent anchor inside added owner → keep owner := by
  exact hull_is_least_closed_completion endpoint support adjacent anchor _ keep
    ((feasible_iff_horn_closed endpoint support adjacent anchor hanchor hunique hfull keep).mp hkeep)
    hcontains

end SubQuorum.ContactHullLocalization
