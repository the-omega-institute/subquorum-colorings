import SubQuorum.SourceSeparatorTransfer

set_option autoImplicit false

namespace SubQuorum.FeasibleCoreSeparator

open SourceRetentionClosure SourceSeparatorTransfer

variable {Owner Vertex : Type}

theorem a_side_of_a_feasible_core_is_feasible
    (endpoint support : Owner → Vertex → Prop)
    (adjacent : Vertex → Vertex → Prop) (anchor : Owner → Vertex → Vertex)
    (hsymmetric : ∀ first second, adjacent first second → adjacent second first)
    (hanchor : ∀ owner point, support owner point →
      endpoint owner (anchor owner point) ∧ adjacent point (anchor owner point))
    (hunique : ∀ first second point, endpoint first point → endpoint second point → first = second)
    (hfull : feasible endpoint support adjacent (fun _ => True))
    (core keep : Owner → Prop)
    (hcore : feasible endpoint support adjacent core)
    (hsubset : ∀ owner, core owner → keep owner)
    (hcross : ∀ first second point neighbor, keep first → ¬core first →
      ¬keep second → endpoint first point → endpoint second neighbor →
        adjacent point neighbor → False) :
    feasible endpoint support adjacent keep := by
  intro point hselected first second hfirstAdj hsecondAdj hfirstOcc hsecondOcc
  rcases hselected with ⟨⟨producer, hproducer, hsupport⟩, hnotEndpoint⟩
  have hneighbor : ∀ neighbor, adjacent point neighbor →
      occupied endpoint support keep neighbor → neighbor = anchor producer point := by
    intro neighbor hadjacent hoccupied
    classical
    apply Classical.byContradiction
    intro hdifferent
    rcases hoccupied with ⟨other, hother, horiginal⟩
    rcases a_second_occupied_neighbor_forces_consumption endpoint support adjacent anchor
      hanchor (fun _ => True) hfull producer other point neighbor trivial trivial
      hsupport horiginal hadjacent hdifferent with ⟨consumer, _, hconsumer⟩
    have hconsumerNot : ¬keep consumer := fun hkeep =>
      hnotEndpoint ⟨consumer, hkeep, hconsumer⟩
    have hproducerCore : core producer := by
      apply Classical.byContradiction
      intro hnot
      exact hcross producer consumer (anchor producer point) point hproducer hnot
        hconsumerNot (hanchor producer point hsupport).1 hconsumer
        (hsymmetric point (anchor producer point) (hanchor producer point hsupport).2)
    have hselectedCore : selected endpoint support core point := by
      refine ⟨⟨producer, hproducerCore, hsupport⟩, ?_⟩
      rintro ⟨owner, howner, hendpoint⟩
      exact hnotEndpoint ⟨owner, hsubset owner howner, hendpoint⟩
    have hnotCoreNeighbor : ¬occupied endpoint support core neighbor := by
      intro hcoreOccupied
      exact hdifferent (hcore point hselectedCore neighbor (anchor producer point)
        hadjacent (hanchor producer point hsupport).2 hcoreOccupied
        ⟨producer, hproducerCore, Or.inl (hanchor producer point hsupport).1⟩)
    by_cases hotherCore : core other
    · exact hnotCoreNeighbor ⟨other, hotherCore, horiginal⟩
    rcases horiginal with hotherEndpoint | hotherSupport
    · exact hcross other consumer neighbor point hother hotherCore hconsumerNot
        hotherEndpoint hconsumer (hsymmetric point neighbor hadjacent)
    · have hanchorDifferent : point ≠ anchor other neighbor := by
        intro hequal
        have howner := hunique other consumer point
          (hequal.symm ▸ (hanchor other neighbor hotherSupport).1) hconsumer
        exact hconsumerNot (howner ▸ hother)
      rcases a_second_occupied_neighbor_forces_consumption endpoint support adjacent anchor
        hanchor (fun _ => True) hfull other consumer neighbor point trivial trivial
        hotherSupport (Or.inl hconsumer) (hsymmetric point neighbor hadjacent)
        hanchorDifferent with ⟨neighborOwner, _, hneighborEndpoint⟩
      have hneighborCore : core neighborOwner := by
        apply Classical.byContradiction
        intro hnot
        by_cases hkeep : keep neighborOwner
        · exact hcross neighborOwner consumer neighbor point hkeep hnot hconsumerNot
            hneighborEndpoint hconsumer (hsymmetric point neighbor hadjacent)
        · exact hcross other neighborOwner (anchor other neighbor) neighbor hother hotherCore
            hkeep (hanchor other neighbor hotherSupport).1 hneighborEndpoint
            (hsymmetric neighbor (anchor other neighbor) (hanchor other neighbor hotherSupport).2)
      exact hnotCoreNeighbor ⟨neighborOwner, hneighborCore, Or.inl hneighborEndpoint⟩
  exact (hneighbor first hfirstAdj hfirstOcc).trans (hneighbor second hsecondAdj hsecondOcc).symm

theorem an_event_on_both_sides_is_exactly_a_core_event
    (endpoint support : Owner → Vertex → Prop)
    (adjacent sameTile : Vertex → Vertex → Prop)
    (hunique : ∀ first second point, endpoint first point → endpoint second point → first = second)
    (left right : Owner → Prop) (owner : Owner) (point target : Vertex) :
    directedEvent endpoint support adjacent sameTile (fun source => left source ∧ right source)
        owner point target ↔
      directedEvent endpoint support adjacent sameTile left owner point target ∧
        directedEvent endpoint support adjacent sameTile right owner point target := by
  constructor
  · rintro ⟨⟨hleft, hright⟩, hpoint, ⟨consumer, ⟨hconsumerLeft, hconsumerRight⟩, htarget⟩,
      houtside, hadjacent, htile⟩
    exact ⟨⟨hleft, hpoint, ⟨consumer, hconsumerLeft, htarget⟩, houtside, hadjacent, htile⟩,
      ⟨hright, hpoint, ⟨consumer, hconsumerRight, htarget⟩, houtside, hadjacent, htile⟩⟩
  · rintro ⟨⟨hleft, hpoint, ⟨first, hfirst, hfirstEndpoint⟩, houtside, hadjacent, htile⟩,
      ⟨hright, _, ⟨second, hsecond, hsecondEndpoint⟩, _, _, _⟩⟩
    have hequal := hunique first second target hfirstEndpoint hsecondEndpoint
    exact ⟨⟨hleft, hright⟩, hpoint,
      ⟨first, ⟨hfirst, hequal.symm ▸ hsecond⟩, hfirstEndpoint⟩, houtside, hadjacent, htile⟩

theorem every_event_belongs_to_a_side
    (endpoint support : Owner → Vertex → Prop)
    (adjacent sameTile : Vertex → Vertex → Prop)
    (hsymmetric : ∀ first second, adjacent first second → adjacent second first)
    (left right : Owner → Prop) (hcover : ∀ owner, left owner ∨ right owner)
    (hcross : ∀ first second point target, left first → ¬right first →
      right second → ¬left second → endpoint first point → endpoint second target →
        adjacent point target → False)
    (owner : Owner) (point target : Vertex)
    (hevent : directedEvent endpoint support adjacent sameTile (fun _ => True) owner point target) :
    directedEvent endpoint support adjacent sameTile left owner point target ∨
      directedEvent endpoint support adjacent sameTile right owner point target := by
  classical
  rcases hevent with ⟨_, hpoint, ⟨consumer, _, htarget⟩, houtside, hadjacent, htile⟩
  have hconstruct : ∀ keep : Owner → Prop, keep owner → keep consumer →
      directedEvent endpoint support adjacent sameTile keep owner point target := by
    intro keep howner hconsumer
    exact ⟨howner, hpoint, ⟨consumer, hconsumer, htarget⟩, houtside, hadjacent, htile⟩
  by_cases hownerLeft : left owner
  · by_cases hconsumerLeft : left consumer
    · exact Or.inl (hconstruct left hownerLeft hconsumerLeft)
    have hconsumerRight := (hcover consumer).resolve_left hconsumerLeft
    by_cases hownerRight : right owner
    · exact Or.inr (hconstruct right hownerRight hconsumerRight)
    exact False.elim (hcross owner consumer point target hownerLeft hownerRight
      hconsumerRight hconsumerLeft hpoint htarget hadjacent)
  · have hownerRight := (hcover owner).resolve_left hownerLeft
    by_cases hconsumerRight : right consumer
    · exact Or.inr (hconstruct right hownerRight hconsumerRight)
    have hconsumerLeft := (hcover consumer).resolve_right hconsumerRight
    exact False.elim (hcross consumer owner target point hconsumerLeft hconsumerRight
      hownerRight hownerLeft htarget hpoint (hsymmetric point target hadjacent))

end SubQuorum.FeasibleCoreSeparator
