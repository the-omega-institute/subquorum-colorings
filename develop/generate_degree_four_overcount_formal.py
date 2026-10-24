"""Generate the actual 8-by-10 frozen counterexample to the coarse criterion."""

from degree_four_overcount import opposed_bands, opposed_band_certificate


def source():
    current, modules = opposed_bands(6, 4)
    certificate = opposed_band_certificate(6, 4)
    endpoints = [witness[0] for witness in certificate]
    selected = sorted(current[2])
    coordinates = endpoints+selected
    indices = {point: index for index, point in enumerate(coordinates)}
    mates = {point: partner for edge in current[3]
             for point, partner in (edge, edge[::-1])}
    array = lambda values: '#['+', '.join(str(value) for value in values)+']'
    owners = [next(index+1 for index, module in enumerate(modules) if point in module['endpoints'])
              for point in endpoints]+[0]*len(selected)
    old_selected = [array(sorted(indices[point] for point in module['selected'])) for module in modules]
    positive = modules[1]
    chosen, anchor, opposite, guard = positive['guard']
    protectors = sorted(({(anchor[0]+1, anchor[1]), (anchor[0]-1, anchor[1]),
                          (anchor[0], anchor[1]+1), (anchor[0], anchor[1]-1)} &
                         positive['endpoints']) | {guard})
    text = f'''import SubQuorum.FrozenPromotion

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 16000000

namespace SubQuorum.DegreeFourOvercount

open FrozenPromotion

abbrev Vertex := Fin 56

def coordinates : Array (Nat × Nat) :=
  {array(coordinates)}

def coordinate (vertex : Vertex) : Nat × Nat := coordinates[vertex.val]!

def adjacent (first second : Vertex) : Prop :=
  (coordinate first).1 = (coordinate second).1 ∧
    ((coordinate first).2+1 = (coordinate second).2 ∨
      (coordinate second).2+1 = (coordinate first).2) ∨
  (coordinate first).2 = (coordinate second).2 ∧
    ((coordinate first).1+1 = (coordinate second).1 ∨
      (coordinate second).1+1 = (coordinate first).1)

instance (first second : Vertex) : Decidable (adjacent first second) := by
  unfold adjacent
  infer_instance

def Selected (vertex : Vertex) : Prop := 44 ≤ vertex.val
def Endpoint (vertex : Vertex) : Prop := vertex.val < 44

instance (vertex : Vertex) : Decidable (Selected vertex) := by
  unfold Selected
  infer_instance

instance (vertex : Vertex) : Decidable (Endpoint vertex) := by
  unfold Endpoint
  infer_instance

def mateIndices : Array Nat :=
  {array(indices[mates.get(point, point)] for point in coordinates)}

def mate (vertex : Vertex) : Vertex := Fin.ofNat 56 mateIndices[vertex.val]!

def ownerIndices : Array Nat := {array(owners)}
def owner (vertex : Vertex) : Nat := ownerIndices[vertex.val]!

def originalSelectedIndices : Array (Array Nat) := #[{', '.join(old_selected)}]

def OldEndpoint (module : Fin 2) (vertex : Vertex) : Prop := owner vertex = module.val+1
def OldSelected (module : Fin 2) (vertex : Vertex) : Prop :=
  vertex.val ∈ (originalSelectedIndices[module.val]!).toList
def OldOccupied (module : Fin 2) (vertex : Vertex) : Prop :=
  OldEndpoint module vertex ∨ OldSelected module vertex

instance (module : Fin 2) (vertex : Vertex) : Decidable (OldEndpoint module vertex) := by
  unfold OldEndpoint
  infer_instance

instance (module : Fin 2) (vertex : Vertex) : Decidable (OldSelected module vertex) := by
  unfold OldSelected
  infer_instance

instance (module : Fin 2) (vertex : Vertex) : Decidable (OldOccupied module vertex) := by
  unfold OldOccupied
  infer_instance

def sameTile (first second : Vertex) : Prop :=
  (coordinate first).1/2 = (coordinate second).1/2 ∧
    (coordinate first).2/2 = (coordinate second).2/2

instance (first second : Vertex) : Decidable (sameTile first second) := by
  unfold sameTile
  infer_instance

def occupiedDegree (vertex : Vertex) : Nat :=
  ((List.finRange 56).filter fun other => decide (adjacent vertex other)).length

theorem coordinates_inside : ∀ vertex : Vertex,
    (coordinate vertex).1 < 8 ∧ (coordinate vertex).2 < 10 := by decide

theorem coordinates_injective : ∀ first second : Vertex,
    coordinate first = coordinate second → first = second := by decide

theorem matching_involution : ∀ vertex : Vertex, mate (mate vertex) = vertex := by decide

theorem matching_endpoint : ∀ vertex : Vertex, Endpoint vertex →
    Endpoint (mate vertex) ∧ adjacent vertex (mate vertex) := by decide

theorem selected_feasible : ∀ vertex : Vertex, Selected vertex → occupiedDegree vertex ≤ 1 := by
  decide

theorem original_degrees_three : ∀ module : Fin 2, ∀ vertex : Vertex,
    OldEndpoint module vertex →
      ((List.finRange 56).filter fun other =>
        decide (adjacent vertex other ∧ OldOccupied module other)).length = 3 := by decide

theorem original_support_feasible : ∀ module : Fin 2, ∀ vertex : Vertex,
    OldSelected module vertex →
      ((List.finRange 56).filter fun other =>
        decide (adjacent vertex other ∧ OldOccupied module other)).length = 1 := by decide

theorem final_degrees_three_or_four : ∀ vertex : Vertex, Endpoint vertex →
    occupiedDegree vertex = 3 ∨ occupiedDegree vertex = 4 := by decide

'''
    for index, (endpoint, first, second) in enumerate(certificate):
        witnesses = [first, second]
        witnesses.sort(key=lambda point: point not in current[2])
        first_index, second_index = (indices[point] for point in witnesses)
        count = sum(point in current[2] for point in witnesses)
        constructor = ('two_frozen', 'selected_frozen', 'two_selected')[count]
        checks = 3+count
        text += f'theorem frozen_{index:02d} : Frozen adjacent Selected mate ({index} : Vertex) := by\n'
        text += f'  exact .{constructor} {index} {first_index} {second_index}'+(' (by decide)'*checks)+'\n'
        for witness in witnesses[count:]:
            previous = indices[mates[witness]]
            assert previous < index
            text += f'    (by change Frozen adjacent Selected mate ({previous} : Vertex); exact frozen_{previous:02d})\n'
        text += '\n'
    text += '''theorem all_endpoints_frozen (vertex : Vertex) (hendpoint : Endpoint vertex) :
    Frozen adjacent Selected mate vertex := by
  rcases vertex with ⟨value, hvalue⟩
  match value with
'''
    text += ''.join(f'  | {index} => exact frozen_{index:02d}\n' for index in range(44))
    text += '''  | value+44 =>
      change value+44 < 44 at hendpoint
      omega

theorem no_feasible_bundle (promoted retained : Vertex → Prop)
    (hpromoted : ∀ vertex, promoted vertex → Endpoint vertex)
    (hselected : ∀ vertex, Selected vertex → retained vertex)
    (hretained : ∀ vertex, ¬promoted (mate vertex) → retained vertex)
    (hfeasible : ∀ vertex first second, promoted vertex →
      adjacent vertex first → adjacent vertex second →
      retained first → retained second → first = second) :
    ∀ vertex, ¬promoted vertex := by
  intro vertex hpromotion
  exact frozen_exclusion adjacent Selected promoted retained mate hselected hretained
    hfeasible vertex (all_endpoints_frozen vertex (hpromoted vertex hpromotion)) hpromotion

def tiles : List (Nat × Nat) := (List.range 4).flatMap fun row =>
  (List.range 5).map fun column => (row, column)

def inTile (vertex : Vertex) (tile : Nat × Nat) : Bool :=
  decide ((coordinate vertex).1/2 = tile.1 ∧ (coordinate vertex).2/2 = tile.2)

def oldReceivers (module : Fin 2) : List (Nat × Nat) :=
  tiles.filter fun tile => (List.finRange 56).any fun vertex =>
    decide (OldEndpoint module vertex) && inTile vertex tile

def oldReceiverSelections (module : Fin 2) : Nat :=
  ((List.finRange 56).filter fun vertex => decide (OldSelected module vertex) &&
    (oldReceivers module).any (inTile vertex)).length

def oldMatchingCount (module : Fin 2) : Nat :=
  ((List.finRange 56).filter fun vertex => decide (OldEndpoint module vertex)).length/2

def oldCharge (module : Fin 2) : Int :=
  (oldReceiverSelections module : Int)+(oldMatchingCount module : Int)-
    2*((oldReceivers module).length : Int)

def newMixedSquares : Nat :=
  (tiles.filter fun tile =>
    ((List.finRange 56).filter fun vertex => decide (Endpoint vertex) && inTile vertex tile).length = 4 &&
    (List.finRange 56).any (fun vertex => decide (owner vertex = 1) && inTile vertex tile) &&
    (List.finRange 56).any (fun vertex => decide (owner vertex = 2) && inTile vertex tile)).length

def originallyOccupied (vertex other : Vertex) : Prop :=
  (owner vertex = 1 ∧ OldOccupied 0 other) ∨ (owner vertex = 2 ∧ OldOccupied 1 other)

instance (vertex other : Vertex) : Decidable (originallyOccupied vertex other) := by
  unfold originallyOccupied
  infer_instance

def insideLoss : Nat :=
  ((List.finRange 56).filter fun vertex => decide (Endpoint vertex ∧
    ∃ other : Vertex, Endpoint other ∧ adjacent vertex other ∧ sameTile vertex other ∧
      ¬originallyOccupied vertex other)).length

def degreeFourCount : Nat :=
  ((List.finRange 56).filter fun vertex => decide (Endpoint vertex ∧ occupiedDegree vertex = 4)).length

def negativeMass : Int := 1-(oldCharge 0+oldCharge 1)

'''
    text += f'def protectors : List Vertex := [{", ".join(str(indices[point]) for point in protectors)}]\n'
    text += '''
def markedModules : Nat := if protectors.any (fun vertex => occupiedDegree vertex = 4) then 1 else 0

theorem exact_original_charges : oldCharge 0 = -5 ∧ oldCharge 1 = 1 := by decide

theorem exact_degree_four_count : degreeFourCount = 12 := by decide

theorem exact_mixed_square_count : newMixedSquares = 0 := by decide

theorem exact_internal_loss : insideLoss = 0 := by decide

theorem exact_marked_module_count : markedModules = 1 := by decide

theorem coarse_criterion_fails : ¬ (degreeFourCount : Int) ≤ negativeMass+2*newMixedSquares := by
  decide

theorem finer_criterion_holds : (insideLoss : Int)+markedModules ≤ negativeMass+2*newMixedSquares := by
  decide

'''
    text += f'theorem positive_canonical_donor_consumed : OldSelected 1 ({indices[chosen]} : Vertex) ∧\n'
    text += f'    OldEndpoint 0 ({indices[chosen]} : Vertex) := by decide\n\n'
    text += '''def objective : Nat :=
  ((List.finRange 56).filter fun vertex => decide (Selected vertex)).length+
    ((List.finRange 56).filter fun vertex => decide (Endpoint vertex)).length/2

theorem exact_objective : objective = 34 := by decide

theorem actual_target_holds : (objective : Int) < 8*10/2 := by decide

theorem coarse_gap_unbounded (bound : Nat) : ∃ height : Nat,
    4 ≤ height ∧ height % 2 = 0 ∧ (bound : Int) < 2*(height : Int)+4-5 := by
  refine ⟨2*(bound+2), ?_, ?_, ?_⟩ <;> omega

theorem fine_credit_constant (width : Int) : (width-1)-0-1 = width-2 := by omega

theorem doubled_slack_identity (width height : Int) :
    (height+4)*(width+4)-2*(2*width+4*height+6) = height*(width-4)+4 := by
  simp only [Int.mul_add, Int.add_mul, Int.mul_sub]
  omega

end SubQuorum.DegreeFourOvercount
'''
    return text


if __name__ == '__main__':
    print(source(), end='')
