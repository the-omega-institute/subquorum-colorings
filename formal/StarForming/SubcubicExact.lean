import StarForming.SubcubicCertificate

namespace StarForming.Subcubic

theorem supported_deletion {Vertex : Type}
    (adjacency : Vertex → Vertex → Prop) (selection : Vertex → Prop) (deleted : Vertex)
    (hforms : Forms adjacency selection)
    (hnew : TwoAt adjacency (fun vertex => selection vertex ∧ vertex ≠ deleted) deleted)
    (hadjacent : ∀ outside, ¬ selection outside → adjacency outside deleted →
      TwoAt adjacency (fun vertex => selection vertex ∧ vertex ≠ deleted) outside)
    (hreplacement : ∀ center, selection center → adjacency center deleted →
      ∃ leaf, (selection leaf ∧ leaf ≠ deleted) ∧ adjacency center leaf) :
    Forms adjacency (fun vertex => selection vertex ∧ vertex ≠ deleted) := by
  classical
  intro outside houtside
  by_cases hequal : outside = deleted
  · exact hequal ▸ hnew
  have hold : ¬ selection outside := fun hselected => houtside ⟨hselected, hequal⟩
  by_cases hadj : adjacency outside deleted
  · exact hadjacent outside hold hadj
  rcases hforms outside hold with ⟨first, second, hf, hs, hne, ha, hb⟩ |
    ⟨center, leaf, hc, hl, ha, hb⟩
  · have hfirst : first ≠ deleted := fun heq => hadj (heq ▸ ha)
    have hsecond : second ≠ deleted := fun heq => hadj (heq ▸ hb)
    exact Or.inl ⟨first, second, ⟨hf, hfirst⟩, ⟨hs, hsecond⟩, hne, ha, hb⟩
  · have hcenter : center ≠ deleted := fun heq => hadj (heq ▸ ha)
    by_cases hleaf : leaf = deleted
    · obtain ⟨replacement, hr, hedge⟩ := hreplacement center hc (hleaf ▸ hb)
      exact Or.inr ⟨center, replacement, ⟨hc, hcenter⟩, hr, ha, hedge⟩
    · exact Or.inr ⟨center, leaf, ⟨hc, hcenter⟩, ⟨hl, hleaf⟩, ha, hb⟩

def coreLabel (vertex : Fin 10) : Fin 12 :=
  ⟨if vertex.val < 5 then vertex.val + 1 else vertex.val + 2, by split <;> omega⟩

def CoreAdj (first second : Fin 10) : Prop := Adj (coreLabel first) (coreLabel second)

def attachment (vertex : Fin 10) : Prop := coreLabel vertex = 3 ∨ coreLabel vertex = 11

def coreSelected (mask : Fin 1024) (vertex : Fin 10) : Prop := mask.val.testBit vertex.val = true

def coreCard (mask : Fin 1024) : Nat :=
  ((List.finRange 10).filter (fun vertex => mask.val.testBit vertex.val)).length

def SafeCore (mask : Fin 1024) (deleted : Fin 10) : Prop :=
  coreSelected mask deleted ∧ ¬ attachment deleted ∧
  TwoAt CoreAdj (fun vertex => coreSelected mask vertex ∧ vertex ≠ deleted) deleted ∧
  (∀ center, coreSelected mask center → CoreAdj center deleted →
    ∃ leaf, (coreSelected mask leaf ∧ leaf ≠ deleted) ∧ CoreAdj center leaf) ∧
  (∀ outside, ¬ coreSelected mask outside → CoreAdj outside deleted →
    TwoAt CoreAdj (fun vertex => coreSelected mask vertex ∧ vertex ≠ deleted) outside)

set_option maxRecDepth 200000 in
set_option maxHeartbeats 0 in
set_option synthInstance.maxSize 4096 in
set_option maxSynthPendingDepth 128 in
theorem dense_core_certificate : ∀ mask : Fin 1024, 7 ≤ coreCard mask →
    ∃ deleted, SafeCore mask deleted := by
  unfold SafeCore TwoAt CoreAdj Adj neighbors attachment coreLabel coreSelected coreCard
  decide +kernel

theorem lift_core_star {Vertex : Type}
    (adjacency : Vertex → Vertex → Prop) (selection : Vertex → Prop)
    (embedding : Fin 10 → Vertex) (mask : Fin 1024)
    (hinjective : ∀ first second, embedding first = embedding second → first = second)
    (hedges : ∀ first second, adjacency (embedding first) (embedding second) ↔ CoreAdj first second)
    (hselection : ∀ vertex, selection (embedding vertex) ↔ coreSelected mask vertex)
    (deleted outside : Fin 10)
    (hstar : TwoAt CoreAdj (fun vertex => coreSelected mask vertex ∧ vertex ≠ deleted) outside) :
    TwoAt adjacency (fun vertex => selection vertex ∧ vertex ≠ embedding deleted) (embedding outside) := by
  have hkeep : ∀ vertex, coreSelected mask vertex ∧ vertex ≠ deleted →
      selection (embedding vertex) ∧ embedding vertex ≠ embedding deleted := by
    intro vertex hvertex
    exact ⟨(hselection vertex).mpr hvertex.1, fun heq => hvertex.2 (hinjective _ _ heq)⟩
  rcases hstar with ⟨first, second, hf, hs, hne, ha, hb⟩ | ⟨center, leaf, hc, hl, ha, hb⟩
  · exact Or.inl ⟨embedding first, embedding second, hkeep first hf, hkeep second hs,
      fun heq => hne (hinjective _ _ heq), (hedges _ _).mpr ha, (hedges _ _).mpr hb⟩
  · exact Or.inr ⟨embedding center, embedding leaf, hkeep center hc, hkeep leaf hl,
      (hedges _ _).mpr ha, (hedges _ _).mpr hb⟩

theorem ambient_core_cap {Vertex : Type}
    (adjacency : Vertex → Vertex → Prop) (selection : Vertex → Prop)
    (embedding : Fin 10 → Vertex) (mask : Fin 1024)
    (hsymmetric : ∀ first second, adjacency first second → adjacency second first)
    (hinjective : ∀ first second, embedding first = embedding second → first = second)
    (hedges : ∀ first second, adjacency (embedding first) (embedding second) ↔ CoreAdj first second)
    (hselection : ∀ vertex, selection (embedding vertex) ↔ coreSelected mask vertex)
    (hclosed : ∀ vertex, ¬ attachment vertex → ∀ outside, adjacency (embedding vertex) outside →
      ∃ other, outside = embedding other)
    (hminimal : Minimal adjacency selection) : coreCard mask ≤ 6 := by
  classical
  by_cases hcap : coreCard mask ≤ 6
  · exact hcap
  apply False.elim
  obtain ⟨deleted, hselected, hnonport, hnew, hreplace, hadjacent⟩ :=
    dense_core_certificate mask (by omega)
  have hglobal : Forms adjacency (fun vertex => selection vertex ∧ vertex ≠ embedding deleted) := by
    apply supported_deletion adjacency selection (embedding deleted) hminimal.1
    · exact lift_core_star adjacency selection embedding mask hinjective hedges hselection deleted deleted hnew
    · intro outside houtside hedge
      obtain ⟨localOutside, rfl⟩ := hclosed deleted hnonport outside (hsymmetric _ _ hedge)
      apply lift_core_star adjacency selection embedding mask hinjective hedges hselection deleted localOutside
      apply hadjacent localOutside
      · exact fun hlocal => houtside ((hselection _).mpr hlocal)
      · exact (hedges _ _).mp hedge
    · intro center hc hedge
      obtain ⟨localCenter, rfl⟩ := hclosed deleted hnonport center (hsymmetric _ _ hedge)
      obtain ⟨leaf, hl, hedgeLeaf⟩ := hreplace localCenter ((hselection _).mp hc) ((hedges _ _).mp hedge)
      exact ⟨embedding leaf, ⟨(hselection _).mpr hl.1,
        fun heq => hl.2 (hinjective _ _ heq)⟩, (hedges _ _).mpr hedgeLeaf⟩
  exact hminimal.2 _ (fun _ hvertex => hvertex.1)
    ⟨embedding deleted, (hselection _).mpr hselected, fun hvertex => hvertex.2 rfl⟩ hglobal

theorem exact_core_accounting (contributions : List Nat) (shared total : Nat)
    (hlocal : ∀ contribution ∈ contributions, contribution ≤ 6)
    (hshared : shared ≤ contributions.length)
    (htotal : total = contributions.sum + shared) : total ≤ 7 * contributions.length := by
  have hsum : ∀ values : List Nat, (∀ contribution ∈ values, contribution ≤ 6) →
      values.sum ≤ 6 * values.length := by
    intro values
    induction values with
    | nil => simp
    | cons contribution rest hinduction =>
      intro hbound
      have hhead : contribution ≤ 6 := hbound contribution (by simp)
      have htail := hinduction (fun vertex hvertex => hbound vertex (by simp [hvertex]))
      simp only [List.sum_cons, List.length_cons]
      omega
  have hbound := hsum contributions hlocal
  omega

end StarForming.Subcubic
