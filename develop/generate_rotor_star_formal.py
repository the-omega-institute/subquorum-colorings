"""Emit the reproducible Lean patch for the fixed degree-three charge-two star."""

from check_promotion_cores import frozen_certificate
from rotor_networks import star, transform_module


def source():
    module = transform_module(star(6), (False, False, False), (4, 4))
    current = 14, 14, module['selected'], module['matching']
    frozen, layers = frozen_certificate(current)
    assert frozen == module['endpoints']
    witnesses = [witness for layer in layers for witness in layer]
    points = [witness['endpoint'] for witness in witnesses]+sorted(module['selected'])
    index = {point: number for number, point in enumerate(points)}
    mates = {point: partner for edge in module['matching']
             for point, partner in (edge, edge[::-1])}
    coordinates = ', '.join(f'({row}, {column})' for row, column in points)
    mate_indices = ', '.join(str(index[mates.get(point, point)]) for point in points)
    lines = [f'''import SubQuorum.FrozenPromotion

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 16000000

namespace SubQuorum.RotorStarObstruction

open FrozenPromotion

abbrev Vertex := Fin 120

def coordinates : Array (Nat × Nat) :=
  #[{coordinates}]

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

def Selected (vertex : Vertex) : Prop := 80 ≤ vertex.val
def Endpoint (vertex : Vertex) : Prop := vertex.val < 80

instance (vertex : Vertex) : Decidable (Selected vertex) := by
  unfold Selected
  infer_instance

instance (vertex : Vertex) : Decidable (Endpoint vertex) := by
  unfold Endpoint
  infer_instance

def mateIndices : Array Nat :=
  #[{mate_indices}]

def mate (vertex : Vertex) : Vertex := Fin.ofNat 120 mateIndices[vertex.val]!

theorem coordinates_inside : ∀ vertex : Vertex,
    (coordinate vertex).1 < 14 ∧ (coordinate vertex).2 < 14 := by decide

theorem coordinates_injective : ∀ first second : Vertex,
    coordinate first = coordinate second → first = second := by decide

theorem matching_involution : ∀ vertex : Vertex, mate (mate vertex) = vertex := by decide

theorem matching_endpoint : ∀ vertex : Vertex, Endpoint vertex →
    Endpoint (mate vertex) ∧ adjacent vertex (mate vertex) := by decide

theorem selected_feasible : ∀ chosen : Vertex, Selected chosen →
    ((List.finRange 120).filter fun other => decide (adjacent chosen other)).length ≤ 1 := by decide

theorem endpoints_degree_three : ∀ vertex : Vertex, Endpoint vertex →
    ((List.finRange 120).filter fun other => decide (adjacent vertex other)).length = 3 := by decide
''']
    for number, witness in enumerate(witnesses):
        neighbors = sorted(witness['kept_neighbors'], key=lambda point: point not in module['selected'])
        first, second = (index[point] for point in neighbors)
        selected_count = sum(point in module['selected'] for point in neighbors)
        constructor = ('two_frozen', 'selected_frozen', 'two_selected')[selected_count]
        line = f'theorem frozen_{number:02d} : Frozen adjacent Selected mate ({number} : Vertex) := by\n'
        line += f'  exact .{constructor} {number} {first} {second} (by decide) (by decide) (by decide)'
        for point in neighbors:
            if point in module['selected']:
                line += ' (by decide)'
            else:
                earlier = index[mates[point]]
                assert earlier < number
                line += (f'\n    (by change Frozen adjacent Selected mate ({earlier} : Vertex); '
                         f'exact frozen_{earlier:02d})')
        lines.append(line+'\n')
    lines.append('''theorem all_endpoints_frozen (vertex : Vertex) (hendpoint : Endpoint vertex) :
    Frozen adjacent Selected mate vertex := by
  rcases vertex with ⟨value, bound⟩
  match value with''')
    lines.extend(f'  | {number} => exact frozen_{number:02d}' for number in range(80))
    lines.append('''  | value+80 =>
      change value+80 < 80 at hendpoint
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

def endpointCount (row column : Nat) : Nat :=
  ((List.finRange 120).filter fun vertex => decide (Endpoint vertex ∧
    (coordinate vertex).1/2 = row ∧ (coordinate vertex).2/2 = column)).length

def selectedCount (row column : Nat) : Nat :=
  ((List.finRange 120).filter fun vertex => decide (Selected vertex ∧
    (coordinate vertex).1/2 = row ∧ (coordinate vertex).2/2 = column)).length

def tiles : List (Nat × Nat) := (List.range 7).flatMap fun row =>
  (List.range 7).map fun column => (row, column)

def receiverTiles : List (Nat × Nat) :=
  tiles.filter fun tile => 0 < endpointCount tile.1 tile.2

def receiverSelected : Nat :=
  (receiverTiles.map fun tile => selectedCount tile.1 tile.2).sum

def receiverCharge : Int := (receiverSelected : Int)+40-2*(receiverTiles.length : Int)

theorem exact_receiver_counts : receiverTiles.length = 33 ∧ receiverSelected = 28 := by decide

theorem original_receiver_charge_two : receiverCharge = 2 := by decide

theorem degree_three_frozen_ceiling_fails : ¬ receiverCharge ≤ 1 := by
  rw [original_receiver_charge_two]
  omega

end SubQuorum.RotorStarObstruction
''')
    return '\n'.join(lines)


if __name__ == '__main__':
    print('*** Begin Patch')
    print('*** Add File: formal/SubQuorum/RotorStarObstruction.lean')
    print('\n'.join('+'+line for line in source().splitlines()))
    print('*** End Patch')
