import SubQuorum.FrozenPromotion

set_option autoImplicit false

namespace SubQuorum.BipartitePromotion

structure OccupiedPair (Vertex : Type) where
  adjacent : Vertex → Vertex → Prop
  selected : Vertex → Prop
  endpoint : Vertex → Prop
  mate : Vertex → Vertex
  color : Vertex → Bool
  partition : ∀ vertex, selected vertex ∨ endpoint vertex
  disjoint : ∀ vertex, selected vertex → ¬endpoint vertex
  selected_degree : ∀ vertex first second, selected vertex →
    adjacent vertex first → adjacent vertex second → first = second
  mate_selected : ∀ vertex, selected vertex → mate vertex = vertex
  mate_endpoint : ∀ vertex, endpoint vertex → endpoint (mate vertex)
  mate_involution : ∀ vertex, mate (mate vertex) = vertex
  mate_adjacent : ∀ vertex, endpoint vertex → adjacent vertex (mate vertex)
  proper : ∀ first second, adjacent first second → color first ≠ color second

def Retained {Vertex : Type} (config : OccupiedPair Vertex)
    (promoted : Vertex → Prop) (vertex : Vertex) : Prop :=
  ¬promoted (config.mate vertex)

structure Bundle {Vertex : Type} (config : OccupiedPair Vertex)
    (promoted : Vertex → Prop) : Prop where
  endpoints : ∀ vertex, promoted vertex → config.endpoint vertex
  compatible : ∀ vertex, promoted vertex → ¬promoted (config.mate vertex)
  selected_retained : ∀ vertex, config.selected vertex → Retained config promoted vertex
  feasible : ∀ vertex first second, (config.selected vertex ∨ promoted vertex) →
    config.adjacent vertex first → config.adjacent vertex second →
    Retained config promoted first → Retained config promoted second → first = second

def Available {Vertex : Type} (config : OccupiedPair Vertex)
    (chosen : Bool) (vertex : Vertex) : Prop :=
  config.endpoint vertex ∧ config.color vertex = chosen ∧
    ¬FrozenPromotion.Frozen config.adjacent config.selected config.mate vertex

theorem neighbor_mate_color {Vertex : Type} (config : OccupiedPair Vertex)
    (vertex neighbor : Vertex) (hadjacent : config.adjacent vertex neighbor)
    (hendpoint : config.endpoint neighbor) :
    config.color (config.mate neighbor) = config.color vertex := by
  have hfirst := config.proper vertex neighbor hadjacent
  have hsecond := config.proper neighbor (config.mate neighbor)
    (config.mate_adjacent neighbor hendpoint)
  cases hvertex : config.color vertex <;>
    cases hneighbor : config.color neighbor <;>
    cases hmate : config.color (config.mate neighbor) <;> simp_all

theorem fixed_neighbors_unique {Vertex : Type} (config : OccupiedPair Vertex)
    (vertex first second : Vertex)
    (hunfrozen : ¬FrozenPromotion.Frozen config.adjacent config.selected config.mate vertex)
    (hfirstAdjacent : config.adjacent vertex first)
    (hsecondAdjacent : config.adjacent vertex second)
    (hfirst : config.selected first ∨
      FrozenPromotion.Frozen config.adjacent config.selected config.mate (config.mate first))
    (hsecond : config.selected second ∨
      FrozenPromotion.Frozen config.adjacent config.selected config.mate (config.mate second)) :
    first = second := by
  classical
  by_cases hequal : first = second
  · exact hequal
  · apply False.elim
    apply hunfrozen
    rcases hfirst with hfirst | hfirst <;> rcases hsecond with hsecond | hsecond
    · exact .two_selected vertex first second hfirstAdjacent hsecondAdjacent hequal hfirst hsecond
    · exact .selected_frozen vertex first second hfirstAdjacent hsecondAdjacent hequal hfirst hsecond
    · exact .selected_frozen vertex second first hsecondAdjacent hfirstAdjacent
        (Ne.symm hequal) hsecond hfirst
    · exact .two_frozen vertex first second hfirstAdjacent hsecondAdjacent hequal hfirst hsecond

theorem available_neighbor_fixed {Vertex : Type} (config : OccupiedPair Vertex)
    (chosen : Bool) (vertex neighbor : Vertex)
    (hvertex : Available config chosen vertex)
    (hadjacent : config.adjacent vertex neighbor)
    (hretained : Retained config (Available config chosen) neighbor) :
    config.selected neighbor ∨
      FrozenPromotion.Frozen config.adjacent config.selected config.mate (config.mate neighbor) := by
  classical
  rcases config.partition neighbor with hselected | hendpoint
  · exact Or.inl hselected
  · apply Or.inr
    by_cases hfrozen : FrozenPromotion.Frozen config.adjacent config.selected config.mate
        (config.mate neighbor)
    · exact hfrozen
    · exact False.elim (hretained ⟨config.mate_endpoint neighbor hendpoint,
        (neighbor_mate_color config vertex neighbor hadjacent hendpoint).trans hvertex.2.1,
        hfrozen⟩)

theorem available_bundle {Vertex : Type} (config : OccupiedPair Vertex) (chosen : Bool) :
    Bundle config (Available config chosen) := by
  classical
  constructor
  · intro vertex hvertex
    exact hvertex.1
  · intro vertex hvertex hmate
    exact config.proper vertex (config.mate vertex)
      (config.mate_adjacent vertex hvertex.1) (hvertex.2.1.trans hmate.2.1.symm)
  · intro vertex hselected hpromoted
    have hsame := config.mate_selected vertex hselected
    have hendpoint : config.endpoint vertex := by simpa [hsame] using hpromoted.1
    exact config.disjoint vertex hselected hendpoint
  · intro vertex first second hvertex hfirstAdjacent hsecondAdjacent hfirstKept hsecondKept
    rcases hvertex with hselected | hpromoted
    · exact config.selected_degree vertex first second hselected hfirstAdjacent hsecondAdjacent
    · exact fixed_neighbors_unique config vertex first second hpromoted.2.2
        hfirstAdjacent hsecondAdjacent
        (available_neighbor_fixed config chosen vertex first hpromoted hfirstAdjacent hfirstKept)
        (available_neighbor_fixed config chosen vertex second hpromoted hsecondAdjacent hsecondKept)

theorem frozen_excludes_bundle {Vertex : Type} (config : OccupiedPair Vertex)
    (promoted : Vertex → Prop) (hbundle : Bundle config promoted) (vertex : Vertex)
    (hfrozen : FrozenPromotion.Frozen config.adjacent config.selected config.mate vertex) :
    ¬promoted vertex := by
  exact FrozenPromotion.frozen_exclusion config.adjacent config.selected promoted
    (Retained config promoted) config.mate hbundle.selected_retained
    (fun _ hnot => hnot)
    (fun current first second hpromoted =>
      hbundle.feasible current first second (Or.inr hpromoted)) vertex hfrozen

theorem frozen_iff_unpromotable {Vertex : Type} (config : OccupiedPair Vertex)
    (vertex : Vertex) (hendpoint : config.endpoint vertex) :
    FrozenPromotion.Frozen config.adjacent config.selected config.mate vertex ↔
      ∀ promoted : Vertex → Prop, Bundle config promoted → ¬promoted vertex := by
  classical
  constructor
  · intro hfrozen promoted hbundle
    exact frozen_excludes_bundle config promoted hbundle vertex hfrozen
  · intro hunpromotable
    by_cases hfrozen : FrozenPromotion.Frozen config.adjacent config.selected config.mate vertex
    · exact hfrozen
    · exact False.elim (hunpromotable (Available config (config.color vertex))
        (available_bundle config (config.color vertex)) ⟨hendpoint, rfl, hfrozen⟩)

theorem available_greatest {Vertex : Type} (config : OccupiedPair Vertex)
    (chosen : Bool) (promoted : Vertex → Prop) (hbundle : Bundle config promoted)
    (hcolor : ∀ vertex, promoted vertex → config.color vertex = chosen) :
    ∀ vertex, promoted vertex → Available config chosen vertex := by
  intro vertex hpromoted
  refine ⟨hbundle.endpoints vertex hpromoted, hcolor vertex hpromoted, ?_⟩
  intro hfrozen
  exact frozen_excludes_bundle config promoted hbundle vertex hfrozen hpromoted

theorem color_restriction_bundle {Vertex : Type} (config : OccupiedPair Vertex)
    (chosen : Bool) (promoted : Vertex → Prop) (hbundle : Bundle config promoted) :
    Bundle config (fun vertex => promoted vertex ∧ config.color vertex = chosen) := by
  constructor
  · intro vertex hpromoted
    exact hbundle.endpoints vertex hpromoted.1
  · intro vertex hpromoted hmate
    exact hbundle.compatible vertex hpromoted.1 hmate.1
  · intro vertex hselected hpromoted
    exact hbundle.selected_retained vertex hselected hpromoted.1
  · intro vertex first second hvertex hfirstAdjacent hsecondAdjacent hfirstKept hsecondKept
    rcases hvertex with hselected | hpromoted
    · exact config.selected_degree vertex first second hselected hfirstAdjacent hsecondAdjacent
    · apply hbundle.feasible vertex first second (Or.inr hpromoted.1)
        hfirstAdjacent hsecondAdjacent
      · intro hfirstRemoved
        have hfirstEndpoint : config.endpoint first := by
          have hmateEndpoint := config.mate_endpoint (config.mate first)
            (hbundle.endpoints (config.mate first) hfirstRemoved)
          simpa [config.mate_involution first] using hmateEndpoint
        exact hfirstKept ⟨hfirstRemoved,
          (neighbor_mate_color config vertex first hfirstAdjacent hfirstEndpoint).trans hpromoted.2⟩
      · intro hsecondRemoved
        have hsecondEndpoint : config.endpoint second := by
          have hmateEndpoint := config.mate_endpoint (config.mate second)
            (hbundle.endpoints (config.mate second) hsecondRemoved)
          simpa [config.mate_involution second] using hmateEndpoint
        exact hsecondKept ⟨hsecondRemoved,
          (neighbor_mate_color config vertex second hsecondAdjacent hsecondEndpoint).trans hpromoted.2⟩

theorem terminal_iff_all_frozen {Vertex : Type} (config : OccupiedPair Vertex) :
    (∀ promoted : Vertex → Prop, Bundle config promoted → ∀ vertex, ¬promoted vertex) ↔
      ∀ vertex, config.endpoint vertex →
        FrozenPromotion.Frozen config.adjacent config.selected config.mate vertex := by
  constructor
  · intro hterminal vertex hendpoint
    apply (frozen_iff_unpromotable config vertex hendpoint).mpr
    intro promoted hbundle
    exact hterminal promoted hbundle vertex
  · intro hall promoted hbundle vertex hpromoted
    exact frozen_excludes_bundle config promoted hbundle vertex
      (hall vertex (hbundle.endpoints vertex hpromoted)) hpromoted

theorem two_step_frozen_chain {Vertex : Type}
    (adjacent : Vertex → Vertex → Prop) (selected : Vertex → Prop)
    (mate : Vertex → Vertex) (wave : Nat → Vertex) (length : Nat)
    (hzero : FrozenPromotion.Frozen adjacent selected mate (wave 0))
    (hone : FrozenPromotion.Frozen adjacent selected mate (wave 1))
    (hfirst : ∀ index, index+2 < length →
      adjacent (wave (index+2)) (mate (wave index)))
    (hsecond : ∀ index, index+2 < length →
      adjacent (wave (index+2)) (mate (wave (index+1))))
    (hdistinct : ∀ index, index+2 < length →
      mate (wave index) ≠ mate (wave (index+1)))
    (hinvolution : ∀ vertex, mate (mate vertex) = vertex) :
    ∀ index, index < length →
      FrozenPromotion.Frozen adjacent selected mate (wave index) := by
  have hpairs : ∀ index, index+1 < length →
      FrozenPromotion.Frozen adjacent selected mate (wave index) ∧
      FrozenPromotion.Frozen adjacent selected mate (wave (index+1)) := by
    intro index
    induction index with
    | zero => intro _; exact ⟨hzero, hone⟩
    | succ index inductionHypothesis =>
      intro hbound
      have hprevious := inductionHypothesis (by omega)
      refine ⟨hprevious.2, ?_⟩
      apply FrozenPromotion.Frozen.two_frozen (wave (index+2))
        (mate (wave index)) (mate (wave (index+1)))
        (hfirst index (by omega)) (hsecond index (by omega)) (hdistinct index (by omega))
      · simpa [hinvolution] using hprevious.1
      · simpa [hinvolution] using hprevious.2
  intro index hbound
  by_cases hsame : index = 0
  · simpa [hsame] using hzero
  · have hprevious : index-1+1 = index := by omega
    have hpair := hpairs (index-1) (by omega)
    simpa [hprevious] using hpair.2

end SubQuorum.BipartitePromotion
