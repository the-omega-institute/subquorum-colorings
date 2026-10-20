import SubQuorum.SourceRetentionClosure

set_option autoImplicit false

namespace SubQuorum.SourceSeparatorTransfer

open SourceRetentionClosure

variable {Owner Vertex : Type}

theorem separator_side_is_feasible
    (endpoint support : Owner → Vertex → Prop)
    (adjacent : Vertex → Vertex → Prop) (anchor : Owner → Vertex → Vertex)
    (hsymmetric : ∀ first second, adjacent first second → adjacent second first)
    (hanchor : ∀ owner point, support owner point →
      endpoint owner (anchor owner point) ∧ adjacent point (anchor owner point))
    (hunique : ∀ first second point, endpoint first point → endpoint second point → first = second)
    (hintrinsic : ∀ owner point neighbor, support owner point →
      originalOccupied endpoint support owner neighbor → adjacent point neighbor →
        neighbor = anchor owner point)
    (hfull : feasible endpoint support adjacent (fun _ => True))
    (separator : Owner) (keep : Owner → Prop)
    (hcross : ∀ first second point neighbor, keep first → first ≠ separator →
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
    have hproducerRoot : producer = separator := by
      apply Classical.byContradiction
      intro hnot
      exact hcross producer consumer (anchor producer point) point hproducer hnot
        hconsumerNot (hanchor producer point hsupport).1 hconsumer
        (hsymmetric point (anchor producer point) (hanchor producer point hsupport).2)
    have hotherNotRoot : other ≠ separator := by
      intro hequal
      have hsame : other = producer := hequal.trans hproducerRoot.symm
      have horiginalProducer : originalOccupied endpoint support producer neighbor := hsame ▸ horiginal
      exact hdifferent (hintrinsic producer point neighbor hsupport horiginalProducer hadjacent)
    rcases horiginal with hotherEndpoint | hotherSupport
    · exact hcross other consumer neighbor point hother hotherNotRoot hconsumerNot
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
      have hneighborRoot : neighborOwner = separator := by
        apply Classical.byContradiction
        intro hnot
        by_cases hkeep : keep neighborOwner
        · exact hcross neighborOwner consumer neighbor point hkeep hnot hconsumerNot
            hneighborEndpoint hconsumer (hsymmetric point neighbor hadjacent)
        · exact hcross other neighborOwner (anchor other neighbor) neighbor hother hotherNotRoot
            hkeep (hanchor other neighbor hotherSupport).1 hneighborEndpoint
            (hsymmetric neighbor (anchor other neighbor) (hanchor other neighbor hotherSupport).2)
      have hsame : neighborOwner = producer := hneighborRoot.trans hproducerRoot.symm
      have hownEndpoint : endpoint producer neighbor := hsame ▸ hneighborEndpoint
      exact hdifferent (hintrinsic producer point neighbor hsupport (Or.inl hownEndpoint) hadjacent)
  exact (hneighbor first hfirstAdj hfirstOcc).trans (hneighbor second hsecondAdj hsecondOcc).symm

def directedEvent (endpoint support : Owner → Vertex → Prop)
    (adjacent sameTile : Vertex → Vertex → Prop) (keep : Owner → Prop)
    (owner : Owner) (point target : Vertex) : Prop :=
  keep owner ∧ endpoint owner point ∧ retainedEndpoint endpoint keep target ∧
    ¬originalOccupied endpoint support owner target ∧ adjacent point target ∧ sameTile point target

theorem directed_event_lies_on_a_separator_side
    (endpoint support : Owner → Vertex → Prop)
    (adjacent sameTile : Vertex → Vertex → Prop)
    (separator : Owner) (left right : Owner → Prop)
    (hcover : ∀ owner, left owner ∨ right owner)
    (hleftRoot : left separator) (hrightRoot : right separator)
    (hcross : ∀ first second point target, left first → first ≠ separator →
      right second → second ≠ separator → endpoint first point → endpoint second target →
        adjacent point target → False)
    (hsymmetric : ∀ first second, adjacent first second → adjacent second first)
    (owner : Owner) (point target : Vertex)
    (hevent : directedEvent endpoint support adjacent sameTile (fun _ => True) owner point target) :
    directedEvent endpoint support adjacent sameTile left owner point target ∨
      directedEvent endpoint support adjacent sameTile right owner point target := by
  rcases hevent with ⟨_, hpoint, ⟨consumer, _, htarget⟩, houtside, hadjacent, htile⟩
  have hconstruct : ∀ keep : Owner → Prop, keep owner → keep consumer →
      directedEvent endpoint support adjacent sameTile keep owner point target := by
    intro keep howner hconsumer
    exact ⟨howner, hpoint, ⟨consumer, hconsumer, htarget⟩, houtside, hadjacent, htile⟩
  by_cases hownerRoot : owner = separator
  · rcases hcover consumer with hleft | hright
    · exact Or.inl (hconstruct left (hownerRoot ▸ hleftRoot) hleft)
    · exact Or.inr (hconstruct right (hownerRoot ▸ hrightRoot) hright)
  by_cases hconsumerRoot : consumer = separator
  · rcases hcover owner with hleft | hright
    · exact Or.inl (hconstruct left hleft (hconsumerRoot ▸ hleftRoot))
    · exact Or.inr (hconstruct right hright (hconsumerRoot ▸ hrightRoot))
  rcases hcover owner with hleft | hright
  · rcases hcover consumer with hconsumer | hconsumer
    · exact Or.inl (hconstruct left hleft hconsumer)
    · exact False.elim (hcross owner consumer point target hleft hownerRoot hconsumer
        hconsumerRoot hpoint htarget hadjacent)
  · rcases hcover consumer with hconsumer | hconsumer
    · exact False.elim (hcross consumer owner target point hconsumer hconsumerRoot hright
        hownerRoot htarget hpoint (hsymmetric point target hadjacent))
    · exact Or.inr (hconstruct right hright hconsumer)

theorem separator_sides_have_disjoint_directed_events
    (endpoint support : Owner → Vertex → Prop)
    (adjacent sameTile : Vertex → Vertex → Prop)
    (hunique : ∀ first second point, endpoint first point → endpoint second point → first = second)
    (separator : Owner) (left right : Owner → Prop)
    (hoverlap : ∀ owner, left owner → right owner → owner = separator)
    (owner : Owner) (point target : Vertex)
    (hleft : directedEvent endpoint support adjacent sameTile left owner point target)
    (hright : directedEvent endpoint support adjacent sameTile right owner point target) : False := by
  rcases hleft with ⟨hownerLeft, _, ⟨first, hfirst, hfirstEndpoint⟩, houtside, _, _⟩
  rcases hright with ⟨hownerRight, _, ⟨second, hsecond, hsecondEndpoint⟩, _, _, _⟩
  have hconsumer := hunique first second target hfirstEndpoint hsecondEndpoint
  have hfirstRight : right first := hconsumer.symm ▸ hsecond
  have hfirstRoot := hoverlap first hfirst hfirstRight
  have hownerRoot := hoverlap owner hownerLeft hownerRight
  have hsame : first = owner := hfirstRoot.trans hownerRoot.symm
  exact houtside (Or.inl (hsame ▸ hfirstEndpoint))

end SubQuorum.SourceSeparatorTransfer
