import SubQuorum.OwnedDonorCompensation

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace SubQuorum.SingleSquareObstacle

abbrev Vertex := Nat × Nat

def selected : List Vertex :=
  [(0,0),(0,2),(0,4),(0,5),(0,7),(1,1),(1,3),(1,6),
   (2,0),(2,2),(2,5),(2,7),(3,0),(3,6),(4,1),(4,7),
   (5,0),(5,2),(5,5),(5,7),(6,1),(6,4),(6,6),
   (7,0),(7,2),(7,3),(7,5),(7,7)]

def matching : List (Vertex × Vertex) :=
  [((3,3),(2,3)),((3,4),(3,5)),((4,4),(5,4)),((4,3),(4,2))]

def endpoints : List Vertex :=
  [(3,3),(2,3),(3,4),(3,5),(4,4),(5,4),(4,3),(4,2)]

def vertices : List Vertex :=
  (List.range 8).flatMap fun row => (List.range 8).map fun column => (row,column)

def adjacent (first second : Vertex) : Prop :=
  (first.1 = second.1 ∧ (first.2+1 = second.2 ∨ second.2+1 = first.2)) ∨
  (first.2 = second.2 ∧ (first.1+1 = second.1 ∨ second.1+1 = first.1))

instance (first second : Vertex) : Decidable (adjacent first second) :=
  inferInstanceAs (Decidable ((_ ∧ _) ∨ (_ ∧ _)))

def occupiedDegree (vertex : Vertex) : Nat :=
  (vertices.filter fun other => decide (adjacent vertex other) &&
    (selected.contains other || endpoints.contains other)).length

def tile (vertex : Vertex) : Vertex := (vertex.1/2,vertex.2/2)

def selectedIn (row column : Nat) : Nat :=
  (selected.filter fun vertex => tile vertex == (row,column)).length

def endpointsIn (row column : Nat) : Nat :=
  (endpoints.filter fun vertex => tile vertex == (row,column)).length

def internalIn (row column : Nat) : Nat :=
  (matching.filter fun edge => tile edge.1 == (row,column) &&
    tile edge.2 == (row,column)).length

def mate (vertex : Vertex) : Vertex :=
  if vertex = (3,3) then (2,3) else if vertex = (2,3) then (3,3) else
  if vertex = (3,4) then (3,5) else if vertex = (3,5) then (3,4) else
  if vertex = (4,4) then (5,4) else if vertex = (5,4) then (4,4) else
  if vertex = (4,3) then (4,2) else if vertex = (4,2) then (4,3) else vertex

theorem valid_matching : endpoints.Nodup ∧
    matching.flatMap (fun edge => [edge.1,edge.2]) = endpoints ∧
    (∀ edge ∈ matching, adjacent edge.1 edge.2 ∧ mate edge.1 = edge.2 ∧
      mate edge.2 = edge.1) ∧
    (∀ vertex ∈ endpoints, vertex ∈ vertices ∧ vertex ∉ selected) ∧
    (∀ vertex ∈ selected, vertex ∈ vertices) := by
  decide

theorem feasible_selected : ∀ vertex ∈ selected, occupiedDegree vertex ≤ 1 := by
  decide

theorem endpoint_terminal : ∀ vertex ∈ endpoints, occupiedDegree vertex = 3 := by
  decide

theorem unique_square : ∀ row column : Fin 7,
    ((row.val,column.val) ∈ endpoints ∧ (row.val+1,column.val) ∈ endpoints ∧
     (row.val,column.val+1) ∈ endpoints ∧ (row.val+1,column.val+1) ∈ endpoints) ↔
      row.val = 3 ∧ column.val = 3 := by
  decide

theorem neutral_tiles :
    (∀ edge ∈ matching, tile edge.1 = tile edge.2) ∧
    (∀ row column : Fin 4,
      (selectedIn row.val column.val = 2 ∧ endpointsIn row.val column.val = 0 ∧
       internalIn row.val column.val = 0) ∨
      (selectedIn row.val column.val = 1 ∧ endpointsIn row.val column.val = 2 ∧
       internalIn row.val column.val = 1)) := by
  decide

theorem exact_objective : selected.length = 28 ∧ endpoints.length = 8 ∧
    matching.length = 4 ∧ selected.length+matching.length = 32 := by
  decide

theorem all_frozen : ∀ vertex ∈ endpoints,
    FrozenPromotion.Frozen adjacent (fun vertex => vertex ∈ selected) mate vertex := by
  have hnorth : FrozenPromotion.Frozen adjacent (fun vertex => vertex ∈ selected) mate (2,3) :=
    .two_selected (2,3) (1,3) (2,2) (by decide) (by decide) (by decide) (by decide) (by decide)
  have heast : FrozenPromotion.Frozen adjacent (fun vertex => vertex ∈ selected) mate (3,5) :=
    .two_selected (3,5) (2,5) (3,6) (by decide) (by decide) (by decide) (by decide) (by decide)
  have hsouth : FrozenPromotion.Frozen adjacent (fun vertex => vertex ∈ selected) mate (5,4) :=
    .two_selected (5,4) (5,5) (6,4) (by decide) (by decide) (by decide) (by decide) (by decide)
  have hwest : FrozenPromotion.Frozen adjacent (fun vertex => vertex ∈ selected) mate (4,2) :=
    .two_selected (4,2) (4,1) (5,2) (by decide) (by decide) (by decide) (by decide) (by decide)
  have htopLeft : FrozenPromotion.Frozen adjacent (fun vertex => vertex ∈ selected) mate (3,3) :=
    .two_frozen (3,3) (3,4) (4,3) (by decide) (by decide) (by decide)
      (by simpa [mate] using heast) (by simpa [mate] using hwest)
  have htopRight : FrozenPromotion.Frozen adjacent (fun vertex => vertex ∈ selected) mate (3,4) :=
    .two_frozen (3,4) (3,3) (4,4) (by decide) (by decide) (by decide)
      (by simpa [mate] using hnorth) (by simpa [mate] using hsouth)
  have hbottomRight : FrozenPromotion.Frozen adjacent (fun vertex => vertex ∈ selected) mate (4,4) :=
    .two_frozen (4,4) (3,4) (4,3) (by decide) (by decide) (by decide)
      (by simpa [mate] using heast) (by simpa [mate] using hwest)
  have hbottomLeft : FrozenPromotion.Frozen adjacent (fun vertex => vertex ∈ selected) mate (4,3) :=
    .two_frozen (4,3) (3,3) (4,4) (by decide) (by decide) (by decide)
      (by simpa [mate] using hnorth) (by simpa [mate] using hsouth)
  intro vertex hvertex
  simp only [endpoints, List.mem_cons, List.not_mem_nil, or_false] at hvertex
  rcases hvertex with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact htopLeft
  · exact hnorth
  · exact htopRight
  · exact heast
  · exact hbottomRight
  · exact hsouth
  · exact hbottomLeft
  · exact hwest

end SubQuorum.SingleSquareObstacle
