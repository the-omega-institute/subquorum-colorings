import Std

namespace StarForming.Regular

def TwoAt {Vertex : Type} (adjacency : Vertex → Vertex → Prop)
    (selection : Vertex → Prop) (outside : Vertex) : Prop :=
  (∃ first second, selection first ∧ selection second ∧ first ≠ second ∧
    adjacency outside first ∧ adjacency outside second) ∨
  (∃ center leaf, selection center ∧ selection leaf ∧
    adjacency outside center ∧ adjacency center leaf)

def Forms {Vertex : Type} (adjacency : Vertex → Vertex → Prop)
    (selection : Vertex → Prop) : Prop :=
  ∀ outside, ¬ selection outside → TwoAt adjacency selection outside

def Minimal {Vertex : Type} (adjacency : Vertex → Vertex → Prop)
    (selection : Vertex → Prop) : Prop :=
  Forms adjacency selection ∧ ∀ smaller : Vertex → Prop,
    (∀ vertex, smaller vertex → selection vertex) →
    (∃ vertex, selection vertex ∧ ¬ smaller vertex) → ¬ Forms adjacency smaller

def High {Vertex : Type} (adjacency : Vertex → Vertex → Prop)
    (selection : Vertex → Prop) (vertex : Vertex) : Prop :=
  selection vertex ∧ ∃ first second, selection first ∧ selection second ∧
    first ≠ second ∧ adjacency vertex first ∧ adjacency vertex second

def Failure {Vertex : Type} (adjacency : Vertex → Vertex → Prop)
    (selection : Vertex → Prop) (deleted outside : Vertex) : Prop :=
  ¬ selection outside ∧
    ¬ TwoAt adjacency (fun vertex => selection vertex ∧ vertex ≠ deleted) outside

theorem high_has_failure {Vertex : Type}
    (adjacency : Vertex → Vertex → Prop) (selection : Vertex → Prop)
    (hirreflexive : ∀ vertex, ¬ adjacency vertex vertex)
    (hminimal : Minimal adjacency selection) (deleted : Vertex)
    (hhigh : High adjacency selection deleted) :
    ∃ outside, Failure adjacency selection deleted outside := by
  classical
  apply Classical.byContradiction
  intro hnone
  have hforms : Forms adjacency (fun vertex => selection vertex ∧ vertex ≠ deleted) := by
    intro outside houtside
    by_cases hequal : outside = deleted
    · subst outside
      obtain ⟨first, second, hf, hs, hne, ha, hb⟩ := hhigh.2
      have hfirst : first ≠ deleted := by
        intro hsame
        subst first
        exact hirreflexive deleted ha
      have hsecond : second ≠ deleted := by
        intro hsame
        subst second
        exact hirreflexive deleted hb
      exact Or.inl ⟨first, second, ⟨hf, hfirst⟩, ⟨hs, hsecond⟩, hne, ha, hb⟩
    · have hold : ¬ selection outside := fun hs => houtside ⟨hs, hequal⟩
      apply Classical.byContradiction
      intro hfailure
      exact hnone ⟨outside, hold, hfailure⟩
  exact hminimal.2 _ (fun _ hvertex => hvertex.1)
    ⟨deleted, hhigh.1, fun hvertex => hvertex.2 rfl⟩ hforms

theorem adjacent_high_survives {Vertex : Type}
    (adjacency : Vertex → Vertex → Prop) (selection : Vertex → Prop)
    (center deleted outside : Vertex) (hhigh : High adjacency selection center)
    (hdifferent : center ≠ deleted) (hedge : adjacency outside center) :
    TwoAt adjacency (fun vertex => selection vertex ∧ vertex ≠ deleted) outside := by
  classical
  obtain ⟨first, second, hf, hs, hne, ha, hb⟩ := hhigh.2
  by_cases hfirst : first = deleted
  · have hsecond : second ≠ deleted := fun heq => hne (hfirst.trans heq.symm)
    exact Or.inr ⟨center, second, ⟨hhigh.1, hdifferent⟩, ⟨hs, hsecond⟩, hedge, hb⟩
  · exact Or.inr ⟨center, first, ⟨hhigh.1, hdifferent⟩, ⟨hf, hfirst⟩, hedge, ha⟩

theorem failure_witnesses_disjoint {Vertex : Type}
    (adjacency : Vertex → Vertex → Prop) (selection : Vertex → Prop)
    (hforms : Forms adjacency selection) (first second outside : Vertex)
    (hfirst : High adjacency selection first) (hsecond : High adjacency selection second)
    (hfailureFirst : Failure adjacency selection first outside)
    (hfailureSecond : Failure adjacency selection second outside) : first = second := by
  classical
  apply Classical.byContradiction
  intro hdifferent
  have hnotFirst : ¬ adjacency outside first := by
    intro hedge
    exact hfailureSecond.2
      (adjacent_high_survives adjacency selection first second outside hfirst hdifferent hedge)
  have hnotSecond : ¬ adjacency outside second := by
    intro hedge
    exact hfailureFirst.2
      (adjacent_high_survives adjacency selection second first outside hsecond
        (fun heq => hdifferent heq.symm) hedge)
  rcases hforms outside hfailureFirst.1 with ⟨left, right, hl, hr, hne, ha, hb⟩ |
    ⟨center, leaf, hc, hl, ha, hb⟩
  · have hleft : left ≠ first := fun heq => hnotFirst (heq ▸ ha)
    have hright : right ≠ first := fun heq => hnotFirst (heq ▸ hb)
    exact hfailureFirst.2 (Or.inl ⟨left, right, ⟨hl, hleft⟩, ⟨hr, hright⟩, hne, ha, hb⟩)
  · have hcenter : center ≠ first := fun heq => hnotFirst (heq ▸ ha)
    by_cases hleaf : leaf = first
    · have hcenterSecond : center ≠ second := fun heq => hnotSecond (heq ▸ ha)
      have hleafSecond : leaf ≠ second := fun heq => hdifferent (hleaf.symm.trans heq)
      exact hfailureSecond.2
        (Or.inr ⟨center, leaf, ⟨hc, hcenterSecond⟩, ⟨hl, hleafSecond⟩, ha, hb⟩)
    · exact hfailureFirst.2 (Or.inr ⟨center, leaf, ⟨hc, hcenter⟩, ⟨hl, hleaf⟩, ha, hb⟩)

theorem witness_has_no_three_neighbors {Vertex : Type}
    (adjacency : Vertex → Vertex → Prop) (selection : Vertex → Prop)
    (deleted outside first second third : Vertex)
    (hfailure : Failure adjacency selection deleted outside)
    (hf : selection first) (hs : selection second) (ht : selection third)
    (hfs : first ≠ second) (hft : first ≠ third) (hst : second ≠ third)
    (ha : adjacency outside first) (hb : adjacency outside second)
    (hc : adjacency outside third) : False := by
  classical
  apply hfailure.2
  by_cases hfirst : first = deleted
  · have hsecond : second ≠ deleted := fun heq => hfs (hfirst.trans heq.symm)
    have hthird : third ≠ deleted := fun heq => hft (hfirst.trans heq.symm)
    exact Or.inl ⟨second, third, ⟨hs, hsecond⟩, ⟨ht, hthird⟩, hst, hb, hc⟩
  · by_cases hsecond : second = deleted
    · have hthird : third ≠ deleted := fun heq => hst (hsecond.trans heq.symm)
      exact Or.inl ⟨first, third, ⟨hf, hfirst⟩, ⟨ht, hthird⟩, hft, ha, hc⟩
    · exact Or.inl ⟨first, second, ⟨hf, hfirst⟩, ⟨hs, hsecond⟩, hfs, ha, hb⟩

theorem nonadjacent_witness_unique_neighbor {Vertex : Type}
    (adjacency : Vertex → Vertex → Prop) (selection : Vertex → Prop)
    (deleted outside first second : Vertex)
    (hfailure : Failure adjacency selection deleted outside)
    (hnonadjacent : ¬ adjacency outside deleted)
    (hf : selection first) (hs : selection second)
    (ha : adjacency outside first) (hb : adjacency outside second) : first = second := by
  apply Classical.byContradiction
  intro hne
  have hfirst : first ≠ deleted := fun heq => hnonadjacent (heq ▸ ha)
  have hsecond : second ≠ deleted := fun heq => hnonadjacent (heq ▸ hb)
  exact hfailure.2 (Or.inl ⟨first, second, ⟨hf, hfirst⟩, ⟨hs, hsecond⟩, hne, ha, hb⟩)

theorem witness_capacity (maximum selectedDegree outsideDegree : Nat) (adjacent : Prop)
    (hselected : selectedDegree ≤ maximum)
    (houtside : outsideDegree ≤ 2)
    (hadjacent : adjacent → selectedDegree + 1 ≤ maximum)
    (hnonadjacent : ¬ adjacent → outsideDegree ≤ 1) :
    selectedDegree + outsideDegree ≤ maximum + 1 := by
  classical
  by_cases hedge : adjacent
  · have hbound := hadjacent hedge
    omega
  · have hbound := hnonadjacent hedge
    omega

theorem degree_capacity_accounting
    (selected outside isolated degreeSum internalIncidences cut weight capacity maximum : Nat)
    (hcut : degreeSum = internalIncidences + cut)
    (hselected : internalIncidences + isolated = selected + weight)
    (houtside : maximum * outside = cut + capacity)
    (hcapacity : weight ≤ capacity) :
    degreeSum + isolated ≤ selected + maximum * outside := by
  omega

theorem regular_bound (degree selected outside isolated : Nat)
    (hdegree : 1 ≤ degree)
    (hcapacity : degree * selected + isolated ≤ selected + degree * outside) :
    (2 * degree - 1) * selected + isolated ≤ degree * (selected + outside) := by
  have hsplit : (2 * degree - 1) * selected + selected = 2 * (degree * selected) := by
    calc
      _ = ((2 * degree - 1) + 1) * selected := by rw [Nat.add_mul, Nat.one_mul]
      _ = (2 * degree) * selected := by congr 1; omega
      _ = 2 * (degree * selected) := Nat.mul_assoc _ _ _
  rw [Nat.mul_add]
  omega

theorem cubic_bound (selected outside isolated : Nat)
    (hcapacity : 3 * selected + isolated ≤ selected + 3 * outside) :
    5 * selected + isolated ≤ 3 * (selected + outside) := by omega

theorem grid_boundary_accounting (selected outside isolated boundary : Nat)
    (hcapacity : 4 * selected + isolated ≤ selected + 4 * outside + boundary) :
    7 * selected + isolated ≤ 4 * (selected + outside) + boundary := by omega

end StarForming.Regular
