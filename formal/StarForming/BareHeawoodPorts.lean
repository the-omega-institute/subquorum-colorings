import StarForming.RegularBound

namespace StarForming.BarePorts

open StarForming.Regular

theorem only_failure_forces_bare_boundary {Vertex : Type}
    (adjacency : Vertex → Vertex → Prop) (selection : Vertex → Prop)
    (deleted port support : Vertex)
    (hminimal : Minimal adjacency selection) (hdeleted : selection deleted)
    (hnew : TwoAt adjacency (fun vertex => selection vertex ∧ vertex ≠ deleted) deleted)
    (hother : ∀ outside, ¬ selection outside → outside ≠ port →
      TwoAt adjacency (fun vertex => selection vertex ∧ vertex ≠ deleted) outside)
    (hsupport : selection support) (hkeep : support ≠ deleted)
    (hedge : adjacency port support) (hnotdeleted : ¬ adjacency port deleted) :
    ¬ selection port ∧
      ∀ neighbor, adjacency port neighbor → selection neighbor → neighbor = support := by
  classical
  obtain ⟨outside, houtside, hfailure⟩ :=
    covered_deletion_has_failure adjacency selection hminimal deleted hdeleted hnew
  have hequal : outside = port := by
    apply Classical.byContradiction
    intro hdifferent
    exact hfailure (hother outside houtside hdifferent)
  subst outside
  refine ⟨houtside, ?_⟩
  intro neighbor hadjacent hselected
  apply Classical.byContradiction
  intro hdifferent
  have hneighbor : neighbor ≠ deleted := by
    intro hequal
    exact hnotdeleted (hequal ▸ hadjacent)
  apply hfailure
  exact Or.inl ⟨neighbor, support, ⟨hselected, hneighbor⟩,
    ⟨hsupport, hkeep⟩, hdifferent, hadjacent, hedge⟩

theorem internal_neighbors_omitted {Vertex : Type}
    (adjacency : Vertex → Vertex → Prop) (selection internal : Vertex → Prop)
    (port support : Vertex)
    (hboundary : ¬ selection port ∧
      ∀ neighbor, adjacency port neighbor → selection neighbor → neighbor = support)
    (hexternal : ¬ internal support) :
    ¬ selection port ∧
      ∀ neighbor, internal neighbor → adjacency port neighbor → ¬ selection neighbor := by
  refine ⟨hboundary.1, ?_⟩
  intro neighbor hinternal hadjacent hselected
  have hequal := hboundary.2 neighbor hadjacent hselected
  exact hexternal (hequal ▸ hinternal)

theorem additive_block_losses (blocks : List (Nat × Nat))
    (hlocal : ∀ block ∈ blocks, block.1 + block.2 ≤ 8) :
    (blocks.map Prod.fst).sum + (blocks.map Prod.snd).sum ≤ 8 * blocks.length := by
  induction blocks with
  | nil => simp
  | cons block rest hinduction =>
    have hhead := hlocal block (by simp)
    have htail := hinduction (fun entry hentry => hlocal entry (by simp [hentry]))
    simp only [List.map_cons, List.sum_cons, List.length_cons]
    omega

theorem periodic_phase_bound (repeats total : Nat) (blocks : List (Nat × Nat))
    (hlocal : ∀ block ∈ blocks, block.1 + block.2 ≤ 8)
    (hblocks : blocks.length = 6 * repeats)
    (hdemand : repeats ≤ (blocks.map Prod.snd).sum)
    (htotal : total = 25 * repeats + (blocks.map Prod.fst).sum) :
    total ≤ 72 * repeats := by
  have hsum := additive_block_losses blocks hlocal
  omega

end StarForming.BarePorts
