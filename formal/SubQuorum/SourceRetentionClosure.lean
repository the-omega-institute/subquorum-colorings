import Std

set_option autoImplicit false

namespace SubQuorum.SourceRetentionClosure

variable {Owner Vertex : Type}

def originalOccupied (endpoint support : Owner → Vertex → Prop)
    (owner : Owner) (point : Vertex) : Prop :=
  endpoint owner point ∨ support owner point

def retainedEndpoint (endpoint : Owner → Vertex → Prop)
    (keep : Owner → Prop) (point : Vertex) : Prop :=
  ∃ owner, keep owner ∧ endpoint owner point

def occupied (endpoint support : Owner → Vertex → Prop)
    (keep : Owner → Prop) (point : Vertex) : Prop :=
  ∃ owner, keep owner ∧ originalOccupied endpoint support owner point

def selected (endpoint support : Owner → Vertex → Prop)
    (keep : Owner → Prop) (point : Vertex) : Prop :=
  (∃ owner, keep owner ∧ support owner point) ∧ ¬retainedEndpoint endpoint keep point

def feasible (endpoint support : Owner → Vertex → Prop)
    (adjacent : Vertex → Vertex → Prop) (keep : Owner → Prop) : Prop :=
  ∀ point, selected endpoint support keep point →
    ∀ first second, adjacent point first → adjacent point second →
      occupied endpoint support keep first → occupied endpoint support keep second →
        first = second

def conflict (endpoint support : Owner → Vertex → Prop)
    (adjacent : Vertex → Vertex → Prop) (anchor : Owner → Vertex → Vertex)
    (first second consumer : Owner) : Prop :=
  ∃ point neighbor, support first point ∧
    originalOccupied endpoint support second neighbor ∧ adjacent point neighbor ∧
    neighbor ≠ anchor first point ∧ endpoint consumer point

def hornClosed (endpoint support : Owner → Vertex → Prop)
    (adjacent : Vertex → Vertex → Prop) (anchor : Owner → Vertex → Vertex)
    (keep : Owner → Prop) : Prop :=
  ∀ first second consumer, conflict endpoint support adjacent anchor first second consumer →
    keep first → keep second → keep consumer

theorem occupied_iff_endpoint_or_selected
    (endpoint support : Owner → Vertex → Prop) (keep : Owner → Prop) (point : Vertex) :
    occupied endpoint support keep point ↔
      retainedEndpoint endpoint keep point ∨ selected endpoint support keep point := by
  constructor
  · intro hoccupied
    rcases hoccupied with ⟨owner, hkeep, hendpoint | hsupport⟩
    · exact Or.inl ⟨owner, hkeep, hendpoint⟩
    · rcases Classical.em (retainedEndpoint endpoint keep point) with hretained | hnot
      · exact Or.inl hretained
      · exact Or.inr ⟨⟨owner, hkeep, hsupport⟩, hnot⟩
  · intro hretained
    rcases hretained with ⟨owner, hkeep, hendpoint⟩ | ⟨⟨owner, hkeep, hsupport⟩, _⟩
    · exact ⟨owner, hkeep, Or.inl hendpoint⟩
    · exact ⟨owner, hkeep, Or.inr hsupport⟩

theorem a_second_occupied_neighbor_forces_consumption
    (endpoint support : Owner → Vertex → Prop) (adjacent : Vertex → Vertex → Prop)
    (anchor : Owner → Vertex → Vertex)
    (hanchor : ∀ owner point, support owner point →
      endpoint owner (anchor owner point) ∧ adjacent point (anchor owner point))
    (keep : Owner → Prop) (hfeasible : feasible endpoint support adjacent keep)
    (first second : Owner) (point neighbor : Vertex)
    (hfirst : keep first) (hsecond : keep second) (hsupport : support first point)
    (hoccupied : originalOccupied endpoint support second neighbor)
    (hadjacent : adjacent point neighbor) (hdifferent : neighbor ≠ anchor first point) :
    retainedEndpoint endpoint keep point := by
  classical
  apply Classical.byContradiction
  intro hnot
  have hselected : selected endpoint support keep point := ⟨⟨first, hfirst, hsupport⟩, hnot⟩
  have hroot := hanchor first point hsupport
  exact hdifferent (hfeasible point hselected neighbor (anchor first point)
    hadjacent hroot.2 ⟨second, hsecond, hoccupied⟩ ⟨first, hfirst, Or.inl hroot.1⟩)

theorem feasible_iff_horn_closed
    (endpoint support : Owner → Vertex → Prop) (adjacent : Vertex → Vertex → Prop)
    (anchor : Owner → Vertex → Vertex)
    (hanchor : ∀ owner point, support owner point →
      endpoint owner (anchor owner point) ∧ adjacent point (anchor owner point))
    (hunique : ∀ first second point, endpoint first point → endpoint second point → first = second)
    (hfull : feasible endpoint support adjacent (fun _ => True)) (keep : Owner → Prop) :
    feasible endpoint support adjacent keep ↔ hornClosed endpoint support adjacent anchor keep := by
  constructor
  · intro hfeasible first second consumer hconflict hfirst hsecond
    rcases hconflict with ⟨point, neighbor, hsupport, hoccupied, hadjacent, hdifferent, hconsumer⟩
    rcases a_second_occupied_neighbor_forces_consumption endpoint support adjacent anchor
      hanchor keep hfeasible first second point neighbor hfirst hsecond hsupport
      hoccupied hadjacent hdifferent with ⟨actual, hactual, hendpoint⟩
    have hequal := hunique actual consumer point hendpoint hconsumer
    simpa [hequal] using hactual
  · intro hclosed point hselected firstNeighbor secondNeighbor hfirstAdj hsecondAdj hfirstOcc hsecondOcc
    rcases hselected with ⟨⟨producer, hproducer, hsupport⟩, hnotEndpoint⟩
    have hneighbor : ∀ neighbor, adjacent point neighbor →
        occupied endpoint support keep neighbor → neighbor = anchor producer point := by
      intro neighbor hadjacent hoccupied
      classical
      apply Classical.byContradiction
      intro hdifferent
      rcases hoccupied with ⟨other, hother, horiginal⟩
      rcases a_second_occupied_neighbor_forces_consumption endpoint support adjacent anchor
        hanchor (fun _ => True) hfull producer other point neighbor trivial trivial hsupport
        horiginal hadjacent hdifferent with ⟨consumer, _, hconsumer⟩
      have hconflict : conflict endpoint support adjacent anchor producer other consumer :=
        ⟨point, neighbor, hsupport, horiginal, hadjacent, hdifferent, hconsumer⟩
      exact hnotEndpoint ⟨consumer, hclosed producer other consumer hconflict hproducer hother, hconsumer⟩
    exact (hneighbor firstNeighbor hfirstAdj hfirstOcc).trans
      (hneighbor secondNeighbor hsecondAdj hsecondOcc).symm

theorem arbitrary_intersections_are_closed
    (endpoint support : Owner → Vertex → Prop) (adjacent : Vertex → Vertex → Prop)
    (anchor : Owner → Vertex → Vertex) {Index : Type} (families : Index → Owner → Prop)
    (hclosed : ∀ index, hornClosed endpoint support adjacent anchor (families index)) :
    hornClosed endpoint support adjacent anchor (fun owner => ∀ index, families index owner) := by
  intro first second consumer hconflict hfirst hsecond index
  exact hclosed index first second consumer hconflict (hfirst index) (hsecond index)

theorem arbitrary_intersections_are_feasible
    (endpoint support : Owner → Vertex → Prop) (adjacent : Vertex → Vertex → Prop)
    (anchor : Owner → Vertex → Vertex)
    (hanchor : ∀ owner point, support owner point →
      endpoint owner (anchor owner point) ∧ adjacent point (anchor owner point))
    (hunique : ∀ first second point, endpoint first point → endpoint second point → first = second)
    (hfull : feasible endpoint support adjacent (fun _ => True))
    {Index : Type} (families : Index → Owner → Prop)
    (hfeasible : ∀ index, feasible endpoint support adjacent (families index)) :
    feasible endpoint support adjacent (fun owner => ∀ index, families index owner) := by
  apply (feasible_iff_horn_closed endpoint support adjacent anchor hanchor hunique hfull _).mpr
  exact arbitrary_intersections_are_closed endpoint support adjacent anchor families
    (fun index => (feasible_iff_horn_closed endpoint support adjacent anchor hanchor hunique hfull
      (families index)).mp (hfeasible index))

def hull (endpoint support : Owner → Vertex → Prop) (adjacent : Vertex → Vertex → Prop)
    (anchor : Owner → Vertex → Vertex) (seed : Owner → Prop) (owner : Owner) : Prop :=
  ∀ keep : Owner → Prop, hornClosed endpoint support adjacent anchor keep →
    (∀ source, seed source → keep source) → keep owner

theorem hull_contains_seed
    (endpoint support : Owner → Vertex → Prop) (adjacent : Vertex → Vertex → Prop)
    (anchor : Owner → Vertex → Vertex) (seed : Owner → Prop) (owner : Owner) (hseed : seed owner) :
    hull endpoint support adjacent anchor seed owner := by
  intro keep _ hcontains
  exact hcontains owner hseed

theorem hull_is_closed
    (endpoint support : Owner → Vertex → Prop) (adjacent : Vertex → Vertex → Prop)
    (anchor : Owner → Vertex → Vertex) (seed : Owner → Prop) :
    hornClosed endpoint support adjacent anchor (hull endpoint support adjacent anchor seed) := by
  intro first second consumer hconflict hfirst hsecond keep hclosed hcontains
  exact hclosed first second consumer hconflict
    (hfirst keep hclosed hcontains) (hsecond keep hclosed hcontains)

theorem hull_is_least_closed_completion
    (endpoint support : Owner → Vertex → Prop) (adjacent : Vertex → Vertex → Prop)
    (anchor : Owner → Vertex → Vertex) (seed keep : Owner → Prop)
    (hclosed : hornClosed endpoint support adjacent anchor keep)
    (hcontains : ∀ owner, seed owner → keep owner) :
    ∀ owner, hull endpoint support adjacent anchor seed owner → keep owner := by
  intro owner howner
  exact howner keep hclosed hcontains

theorem hull_is_feasible
    (endpoint support : Owner → Vertex → Prop) (adjacent : Vertex → Vertex → Prop)
    (anchor : Owner → Vertex → Vertex)
    (hanchor : ∀ owner point, support owner point →
      endpoint owner (anchor owner point) ∧ adjacent point (anchor owner point))
    (hunique : ∀ first second point, endpoint first point → endpoint second point → first = second)
    (hfull : feasible endpoint support adjacent (fun _ => True)) (seed : Owner → Prop) :
    feasible endpoint support adjacent (hull endpoint support adjacent anchor seed) := by
  exact (feasible_iff_horn_closed endpoint support adjacent anchor hanchor hunique hfull
    (hull endpoint support adjacent anchor seed)).mpr (hull_is_closed endpoint support adjacent anchor seed)

theorem hull_is_monotone
    (endpoint support : Owner → Vertex → Prop) (adjacent : Vertex → Vertex → Prop)
    (anchor : Owner → Vertex → Vertex) (first second : Owner → Prop)
    (hsubset : ∀ owner, first owner → second owner) :
    ∀ owner, hull endpoint support adjacent anchor first owner →
      hull endpoint support adjacent anchor second owner := by
  intro owner howner keep hclosed hcontains
  exact howner keep hclosed (fun source hsource => hcontains source (hsubset source hsource))

theorem hull_is_idempotent
    (endpoint support : Owner → Vertex → Prop) (adjacent : Vertex → Vertex → Prop)
    (anchor : Owner → Vertex → Vertex) (seed : Owner → Prop) (owner : Owner) :
    hull endpoint support adjacent anchor (hull endpoint support adjacent anchor seed) owner ↔
      hull endpoint support adjacent anchor seed owner := by
  constructor
  · intro howner
    exact howner (hull endpoint support adjacent anchor seed)
      (hull_is_closed endpoint support adjacent anchor seed) (fun _ hsource => hsource)
  · exact hull_contains_seed endpoint support adjacent anchor
      (hull endpoint support adjacent anchor seed) owner

end SubQuorum.SourceRetentionClosure
