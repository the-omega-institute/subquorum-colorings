import StarForming.DissociationCover

namespace StarForming.HeawoodMultiport

open StarForming.DissociationCover

def rows : List (List Nat) := [
  [1, 5, 6],
  [0, 2, 7],
  [1, 3, 8],
  [2, 4, 9],
  [3, 5, 10],
  [0, 4, 11],
  [0, 12, 18],
  [1, 13, 19],
  [2, 14, 18],
  [3, 15, 19],
  [4, 16, 18],
  [5, 17, 19],
  [6, 17, 28],
  [7, 14, 20],
  [8, 13],
  [9, 16],
  [10, 15],
  [11, 12],
  [6, 8, 10],
  [7, 9, 11],
  [13, 27, 30],
  [28, 29, 31],
  [29, 30, 32],
  [30, 31, 33],
  [27, 31],
  [28, 32, 33],
  [27, 29, 33],
  [20, 24, 26],
  [12, 21, 25],
  [21, 22, 26],
  [20, 22, 23],
  [21, 23, 24],
  [22, 25],
  [23, 25, 26]]

def adjacency (first second : Fin 34) : Prop :=
  ((rows.getD first.val []).contains second.val) = true

instance : DecidableRel adjacency :=
  fun first second => inferInstanceAs (Decidable
    (((rows.getD first.val []).contains second.val) = true))

def chosen : List Nat := [0, 1, 3, 4, 8, 11, 12, 13, 15, 16, 18, 19, 20, 22, 24, 26, 28, 31, 32, 33]

def selected (vertex : Fin 34) : Prop := chosen.contains vertex.val = true

instance : DecidablePred selected :=
  fun vertex => inferInstanceAs (Decidable (chosen.contains vertex.val = true))

def selectedDegree (vertex : Fin 34) : Nat :=
  ((List.finRange 34).filter (fun neighbor =>
    decide (adjacency vertex neighbor ∧ selected neighbor))).length

def unjoined (first second : Fin 34) : Prop :=
  adjacency first second ∧
    ¬ (first.val = 12 ∧ second.val = 28 ∨ first.val = 28 ∧ second.val = 12 ∨
       first.val = 13 ∧ second.val = 20 ∨ first.val = 20 ∧ second.val = 13)

instance : DecidableRel unjoined :=
  fun first second => inferInstanceAs (Decidable
    (adjacency first second ∧
      ¬ (first.val = 12 ∧ second.val = 28 ∨ first.val = 28 ∧ second.val = 12 ∨
         first.val = 13 ∧ second.val = 20 ∨ first.val = 20 ∧ second.val = 13)))

def color (vertex : Fin 34) : Nat :=
  if vertex.val < 20 then
    if 6 ≤ vertex.val ∧ vertex.val < 12 then (vertex.val + 1) % 2
    else vertex.val % 2
  else if vertex.val < 27 then 0 else 1

set_option maxRecDepth 8192
set_option maxHeartbeats 2000000

theorem witness_dissociates : Dissociates adjacency selected := by
  unfold Dissociates
  decide

theorem witness_cardinality :
    ((List.finRange 34).filter (fun vertex => decide (selected vertex))).length = 20 := by
  decide

theorem simple_subcubic :
    (∀ vertex, ¬ adjacency vertex vertex) ∧
    (∀ first second, adjacency first second ↔ adjacency second first) ∧
    (∀ vertex, ((List.finRange 34).filter (fun neighbor =>
      decide (adjacency vertex neighbor))).length ≤ 3) := by
  decide

theorem bipartite : ∀ first second, adjacency first second → color first ≠ color second := by
  decide

theorem attachment_isolates :
    ∀ vertex : Fin 34, [12, 13, 20, 28].contains vertex.val = true →
      selected vertex ∧ ∀ neighbor, unjoined vertex neighbor → ¬ selected neighbor := by
  decide

theorem external_port_profile :
    (∀ vertex : Fin 34, [15, 16, 24, 32].contains vertex.val = true →
      selected vertex ∧ selectedDegree vertex = 1) ∧
    (∀ vertex : Fin 34, [14, 17].contains vertex.val = true → ¬ selected vertex) ∧
    (∀ vertex : Fin 34, ((List.finRange 34).filter (fun neighbor =>
      decide (adjacency vertex neighbor))).length = 2 ↔
        [14, 15, 16, 17, 24, 32].contains vertex.val = true) := by
  decide

theorem two_cut_deficiency_equality (ports isolated complementEdges : Nat)
    (hidentity : 7 + isolated + 2 * complementEdges = 2 * ports)
    (hports : ports ≤ 4) :
    ports = 4 ∧ isolated = 1 ∧ complementEdges = 0 := by
  omega

theorem arbitrary_interface_parameters (cores blocks beta star : Nat)
    (hlocal : beta ≤ 12 * cores + 7 * blocks)
    (hisolate : 2 * (12 * cores + 8 * blocks) ≤ 2 * beta + 2 * blocks)
    (hselection : 12 * cores + 8 * blocks ≤ star)
    (hcompensation : 7 * star ≤ 3 * (20 * cores + 14 * blocks) + 2 * beta) :
    beta = 12 * cores + 7 * blocks ∧ star = 12 * cores + 8 * blocks ∧
      star - beta = blocks := by
  omega

theorem architecture_density (cores blocks : Nat) (hcapacity : blocks ≤ 2 * cores) :
    24 * blocks ≤ 20 * cores + 14 * blocks := by
  omega

end StarForming.HeawoodMultiport
