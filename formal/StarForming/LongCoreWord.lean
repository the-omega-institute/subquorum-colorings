import StarForming.DissociationCover

namespace StarForming.LongCoreWord

open StarForming.DissociationCover

def insideRows : List (List Nat) := [
  [1, 6],
  [0, 2, 7],
  [1, 3, 8],
  [2, 4, 9],
  [3, 5, 10],
  [4, 11],
  [0, 12, 18],
  [1, 13, 19],
  [2, 14, 18],
  [3, 15, 19],
  [4, 16, 18],
  [5, 17, 19],
  [6],
  [7, 14],
  [8, 13],
  [9, 16],
  [10, 15],
  [11],
  [6, 8, 10],
  [7, 9, 11]]

def insideAdj (first second : Fin 20) : Prop :=
  (insideRows.getD first.val []).contains second.val = true

instance : DecidableRel insideAdj :=
  fun first second => inferInstanceAs (Decidable
    ((insideRows.getD first.val []).contains second.val = true))

def pattern (kind : Bool) : List Nat :=
  if kind then [0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 18, 19]
  else [1, 4, 6, 7, 8, 9, 10, 11, 14, 15]

def selected (kind : Bool) (vertex : Fin 20) : Prop :=
  (pattern kind).contains vertex.val = true

instance (kind : Bool) : DecidablePred (selected kind) :=
  fun vertex => inferInstanceAs (Decidable ((pattern kind).contains vertex.val = true))

def forward (first second : Fin 20) : Prop :=
  (first.val = 5 ∧ second.val = 0) ∨ (first.val = 17 ∧ second.val = 12)

instance : DecidableRel forward :=
  fun first second => inferInstanceAs (Decidable
    ((first.val = 5 ∧ second.val = 0) ∨ (first.val = 17 ∧ second.val = 12)))

def wordAdj {Block : Type} (successor : Block → Block)
    (first second : Block × Fin 20) : Prop :=
  (first.1 = second.1 ∧ insideAdj first.2 second.2) ∨
  (successor first.1 = second.1 ∧ forward first.2 second.2) ∨
  (successor second.1 = first.1 ∧ forward second.2 first.2)

set_option maxRecDepth 8192
set_option maxHeartbeats 2000000

theorem inside_dissociates (kind : Bool) : Dissociates insideAdj (selected kind) := by
  cases kind <;> unfold Dissociates <;> decide

theorem pattern_counts : ∀ kind : Bool,
    ((List.finRange 20).filter (fun vertex => decide (selected kind vertex))).length =
      (if kind then 12 else 10) ∧
    (([(12, 13), (14, 15), (16, 17)] : List (Nat × Nat)).filter
      (fun pair => !(pattern kind).contains pair.1 && !(pattern kind).contains pair.2)).length =
      (if kind then 1 else 2) := by
  decide

theorem forward_selected_forces_A :
    ∀ firstKind secondKind : Bool, ∀ first second : Fin 20,
      selected firstKind first → selected secondKind second → forward first second →
        firstKind = true ∧ secondKind = true := by
  decide

theorem selected_edge_internal {Block : Type} (successor : Block → Block)
    (word : Block → Bool)
    (hseparation : ∀ block, ¬ (word block = true ∧ word (successor block) = true))
    (first second : Block × Fin 20)
    (hfirst : selected (word first.1) first.2)
    (hsecond : selected (word second.1) second.2)
    (hedge : wordAdj successor first second) :
    first.1 = second.1 ∧ insideAdj first.2 second.2 := by
  rcases hedge with hinternal | hforward | hbackward
  · exact hinternal
  · obtain ⟨hnext, hboundary⟩ := hforward
    have hkind := forward_selected_forces_A _ _ _ _ hfirst hsecond hboundary
    have hnextKind : word (successor first.1) = true := by
      rw [hnext]
      exact hkind.2
    exact (hseparation first.1 ⟨hkind.1, hnextKind⟩).elim
  · obtain ⟨hnext, hboundary⟩ := hbackward
    have hkind := forward_selected_forces_A _ _ _ _ hsecond hfirst hboundary
    have hnextKind : word (successor second.1) = true := by
      rw [hnext]
      exact hkind.2
    exact (hseparation second.1 ⟨hkind.1, hnextKind⟩).elim

theorem word_dissociates {Block : Type} (successor : Block → Block)
    (word : Block → Bool)
    (hseparation : ∀ block, ¬ (word block = true ∧ word (successor block) = true)) :
    Dissociates (wordAdj successor)
      (fun vertex => selected (word vertex.1) vertex.2) := by
  intro center first second hcenter hfirst hsecond hfirstEdge hsecondEdge
  have hfirstInside := selected_edge_internal successor word hseparation
    center first hcenter hfirst hfirstEdge
  have hsecondInside := selected_edge_internal successor word hseparation
    center second hcenter hsecond hsecondEdge
  have hfirstSelected : selected (word center.1) first.2 := by
    rw [hfirstInside.1]
    exact hfirst
  have hsecondSelected : selected (word center.1) second.2 := by
    rw [hsecondInside.1]
    exact hsecond
  have hlocal := inside_dissociates (word center.1) center.2 first.2 second.2
    hcenter hfirstSelected hsecondSelected hfirstInside.2 hsecondInside.2
  exact Prod.ext (hfirstInside.1.symm.trans hsecondInside.1) hlocal

theorem word_accounting (firstKind secondKind periods : Nat)
    (hcount : firstKind + secondKind = periods) :
    12 * firstKind + 10 * secondKind + (firstKind + 2 * secondKind) =
        12 * periods + firstKind ∧
    12 * firstKind + 10 * secondKind + 7 * (3 * periods) +
        (firstKind + 2 * secondKind) = 33 * periods + firstKind := by
  omega

theorem phase_slack (periods firstKind beta : Nat)
    (hgain : 33 * periods + firstKind ≤ beta) :
    2 * firstKind ≤ 186 * periods + 2 * beta - 7 * (36 * periods) := by
  omega

theorem cubic_gap (periods firstKind beta star : Nat)
    (hgain : 33 * periods + firstKind ≤ beta)
    (hcomparison : beta ≤ star)
    (hcompensation : 7 * star ≤ 186 * periods + 2 * beta) :
    7 * (star - beta) + 5 * firstKind ≤ 21 * periods := by
  omega

theorem even_phase_excludes_target (copies gap : Nat)
    (hpositive : 0 < copies) (hgap : 7 * gap ≤ 37 * copies) :
    gap < 6 * copies := by
  omega

end StarForming.LongCoreWord
