import Std

namespace StarForming.Subcubic

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

theorem minimal_of_deletion_failures {Vertex : Type}
    (adjacency : Vertex → Vertex → Prop) (selection : Vertex → Prop)
    (hforms : Forms adjacency selection)
    (hfail : ∀ deleted, selection deleted → ∃ outside,
      ¬ (selection outside ∧ outside ≠ deleted) ∧
      ¬ TwoAt adjacency (fun vertex => selection vertex ∧ vertex ≠ deleted) outside) :
    Minimal adjacency selection := by
  refine ⟨hforms, ?_⟩
  intro smaller hsubset hexists hsmaller
  obtain ⟨deleted, hselected, hmissing⟩ := hexists
  obtain ⟨outside, houtside, hfailure⟩ := hfail deleted hselected
  have hkeep : ∀ vertex, smaller vertex → selection vertex ∧ vertex ≠ deleted := by
    intro vertex hvertex
    refine ⟨hsubset vertex hvertex, ?_⟩
    intro heq
    exact hmissing (heq ▸ hvertex)
  have hnot : ¬ smaller outside := fun hvertex => houtside (hkeep outside hvertex)
  apply hfailure
  rcases hsmaller outside hnot with ⟨first, second, hf, hs, hne, ha, hb⟩ |
    ⟨center, leaf, hc, hl, ha, hb⟩
  · exact Or.inl ⟨first, second, hkeep first hf, hkeep second hs, hne, ha, hb⟩
  · exact Or.inr ⟨center, leaf, hkeep center hc, hkeep leaf hl, ha, hb⟩

def neighbors (vertex : Fin 12) : List (Fin 12) :=
  match vertex.val with
  | 0 => [11]
  | 1 => [7,8,9]
  | 2 => [9,10,11]
  | 3 => [6,8,10]
  | 4 => [7,10]
  | 5 => [7,11]
  | 6 => [3]
  | 7 => [1,4,5]
  | 8 => [1,3]
  | 9 => [1,2]
  | 10 => [2,3,4]
  | _ => [0,2,5]

def Adj (first second : Fin 12) : Prop := second ∈ neighbors first

def selected (vertex : Fin 12) : Prop := vertex ∈ ([0,1,4,5,6,7,8,9] : List (Fin 12))

instance (vertex : Fin 12) : Decidable (selected vertex) :=
  inferInstanceAs (Decidable (vertex ∈ ([0,1,4,5,6,7,8,9] : List (Fin 12))))

def failure (vertex : Fin 12) : Fin 12 :=
  match vertex.val with
  | 1 => 2
  | 4 => 10
  | 5 => 11
  | 7 => 10
  | 8 => 3
  | 9 => 2
  | _ => vertex

theorem adjacency_simple :
    (∀ vertex : Fin 12, ¬ Adj vertex vertex) ∧
    (∀ first second : Fin 12, Adj first second ↔ Adj second first) := by
  unfold Adj neighbors
  decide +kernel

theorem base_forms : Forms Adj selected := by
  unfold Forms TwoAt Adj selected neighbors
  decide +kernel

theorem base_deletion_failures : ∀ deleted : Fin 12, selected deleted →
    ¬ (selected (failure deleted) ∧ failure deleted ≠ deleted) ∧
    ¬ TwoAt Adj (fun vertex => selected vertex ∧ vertex ≠ deleted) (failure deleted) := by
  unfold TwoAt Adj selected failure neighbors
  decide +kernel

theorem base_minimal : Minimal Adj selected := by
  apply minimal_of_deletion_failures Adj selected base_forms
  intro deleted hselected
  exact ⟨failure deleted, base_deletion_failures deleted hselected⟩

theorem selected_card :
    ((List.finRange 12).filter (fun vertex => decide (selected vertex))).length = 8 := by
  decide +kernel

def membership (mask : Fin 4096) (vertex : Fin 12) : Bool :=
  mask.val.testBit vertex.val

def card (mask : Fin 4096) : Nat :=
  ((List.finRange 12).filter (membership mask)).length

def Dissociation (mask : Fin 4096) : Prop :=
  ∀ vertex : Fin 12, membership mask vertex = true →
    ((neighbors vertex).filter (membership mask)).length ≤ 1

set_option maxRecDepth 200000 in
set_option maxHeartbeats 0 in
theorem dissociation_port_cap : ∀ mask : Fin 4096, Dissociation mask →
    card mask ≤ 6 + if membership mask 0 || membership mask 6 then 1 else 0 := by
  unfold Dissociation card membership neighbors
  decide +kernel

def portWitness (first second : Bool) : Fin 4096 :=
  match first, second with
  | false, false => 828
  | false, true => 3442
  | true, false => 829
  | true, true => 375

theorem port_attainment (first second : Bool) :
    membership (portWitness first second) 0 = first ∧
    membership (portWitness first second) 6 = second ∧
    Dissociation (portWitness first second) ∧
    card (portWitness first second) = 6 + (if first || second then 1 else 0) ∧
    (∀ port ∈ ([0,6] : List (Fin 12)),
      membership (portWitness first second) port = true →
      ((neighbors port).filter (membership (portWitness first second))).length = 0) := by
  cases first <;> cases second <;>
    unfold portWitness Dissociation card membership neighbors <;> decide +kernel

theorem no_double_counting_bound (blocks shared touched total : Nat)
    (hlocal : total + shared ≤ 6 * blocks + touched)
    (htouched : touched ≤ 2 * shared) (hblocks : touched ≤ blocks) :
    2 * total ≤ 13 * blocks := by
  omega

end StarForming.Subcubic
