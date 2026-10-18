import StarForming.CoverPullback

namespace StarForming.DissociationCover

open StarForming.CoverPullback

def Dissociates {Vertex : Type} (adjacency : Vertex → Vertex → Prop)
    (selection : Vertex → Prop) : Prop :=
  ∀ center first second, selection center → selection first → selection second →
    adjacency center first → adjacency center second → first = second

theorem dissociates_pullback {Base Lift : Type}
    {baseAdjacency : Base → Base → Prop} {liftAdjacency : Lift → Lift → Prop}
    {projection : Lift → Base} (cover : NeighborhoodCover baseAdjacency liftAdjacency projection)
    {selection : Base → Prop} (hdissociates : Dissociates baseAdjacency selection) :
    Dissociates liftAdjacency (fun vertex => selection (projection vertex)) := by
  intro center first second hc hf hs ha hb
  apply cover.neighbor_injective center first second ha hb
  exact hdissociates _ _ _ hc hf hs (cover.map_edge _ _ ha) (cover.map_edge _ _ hb)

theorem dissociates_of_pullback {Base Lift : Type}
    {baseAdjacency : Base → Base → Prop} {liftAdjacency : Lift → Lift → Prop}
    {projection : Lift → Base} (cover : NeighborhoodCover baseAdjacency liftAdjacency projection)
    (hsurjective : ∀ vertex, ∃ lifted, projection lifted = vertex)
    {selection : Base → Prop}
    (hdissociates : Dissociates liftAdjacency (fun vertex => selection (projection vertex))) :
    Dissociates baseAdjacency selection := by
  intro center first second hc hf hs ha hb
  obtain ⟨centerLift, hcenterImage⟩ := hsurjective center
  obtain ⟨firstLift, hfirstEdge, hfirstImage⟩ :=
    cover.neighbor_surjective centerLift first (hcenterImage.symm ▸ ha)
  obtain ⟨secondLift, hsecondEdge, hsecondImage⟩ :=
    cover.neighbor_surjective centerLift second (hcenterImage.symm ▸ hb)
  have hcenter : selection (projection centerLift) := hcenterImage.symm ▸ hc
  have hfirst : selection (projection firstLift) := hfirstImage.symm ▸ hf
  have hsecond : selection (projection secondLift) := hsecondImage.symm ▸ hs
  have hequal := hdissociates centerLift firstLift secondLift hcenter hfirst hsecond
    hfirstEdge hsecondEdge
  exact hfirstImage.symm.trans ((congrArg projection hequal).trans hsecondImage)

theorem dissociates_pullback_iff {Base Lift : Type}
    {baseAdjacency : Base → Base → Prop} {liftAdjacency : Lift → Lift → Prop}
    {projection : Lift → Base} (cover : NeighborhoodCover baseAdjacency liftAdjacency projection)
    (hsurjective : ∀ vertex, ∃ lifted, projection lifted = vertex)
    {selection : Base → Prop} :
    Dissociates liftAdjacency (fun vertex => selection (projection vertex)) ↔
      Dissociates baseAdjacency selection := by
  exact ⟨dissociates_of_pullback cover hsurjective, dissociates_pullback cover⟩

theorem four_cycle_excludes_triples {Vertex : Type}
    {adjacency : Vertex → Vertex → Prop} {selection : Vertex → Prop}
    (hsymmetric : ∀ first second, adjacency first second → adjacency second first)
    (hdissociates : Dissociates adjacency selection)
    (first second third fourth : Vertex) (hfirstThird : first ≠ third)
    (hsecondFourth : second ≠ fourth)
    (hfirstSecond : adjacency first second) (hsecondThird : adjacency second third)
    (hthirdFourth : adjacency third fourth) (hfourthFirst : adjacency fourth first) :
    ¬ (selection first ∧ selection second ∧ selection third) ∧
    ¬ (selection second ∧ selection third ∧ selection fourth) ∧
    ¬ (selection third ∧ selection fourth ∧ selection first) ∧
    ¬ (selection fourth ∧ selection first ∧ selection second) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · rintro ⟨hf, hs, ht⟩
    exact hfirstThird (hdissociates second first third hs hf ht
      (hsymmetric _ _ hfirstSecond) hsecondThird)
  · rintro ⟨hs, ht, hfourth⟩
    exact hsecondFourth (hdissociates third second fourth ht hs hfourth
      (hsymmetric _ _ hsecondThird) hthirdFourth)
  · rintro ⟨ht, hfourth, hf⟩
    exact hfirstThird (hdissociates fourth third first hfourth ht hf
      (hsymmetric _ _ hthirdFourth) hfourthFirst).symm
  · rintro ⟨hfourth, hf, hs⟩
    exact hsecondFourth (hdissociates first fourth second hf hfourth hs
      (hsymmetric _ _ hfourthFirst) hfirstSecond).symm

theorem four_cycle_capacity {Vertex : Type}
    {adjacency : Vertex → Vertex → Prop} {selection : Vertex → Prop}
    [DecidablePred selection]
    (hsymmetric : ∀ first second, adjacency first second → adjacency second first)
    (hdissociates : Dissociates adjacency selection)
    (first second third fourth : Vertex) (hfirstThird : first ≠ third)
    (hsecondFourth : second ≠ fourth)
    (hfirstSecond : adjacency first second) (hsecondThird : adjacency second third)
    (hthirdFourth : adjacency third fourth) (hfourthFirst : adjacency fourth first) :
    (if selection first then 1 else 0) + (if selection second then 1 else 0) +
      (if selection third then 1 else 0) + (if selection fourth then 1 else 0) ≤ (2 : Nat) := by
  have hexclusions := four_cycle_excludes_triples hsymmetric hdissociates first second third fourth
    hfirstThird hsecondFourth hfirstSecond hsecondThird hthirdFourth hfourthFirst
  by_cases hf : selection first <;> by_cases hs : selection second <;>
    by_cases ht : selection third <;> by_cases hfourth : selection fourth <;> simp_all

end StarForming.DissociationCover
