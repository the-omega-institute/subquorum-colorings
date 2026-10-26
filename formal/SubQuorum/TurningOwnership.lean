import Lean.Elab.Tactic.Omega

/-!
Scalar actual-edge resource accounting and arbitrary-length forced ownership.
The Hall/grid adapter and the coordinate family are written arguments; these
theorems keep their local capacity and path hypotheses explicit.
-/
namespace SubQuorum.TurningOwnership

theorem local_charge_from_owner (t p m : Int) (cover : t + p - 2 ≤ m) :
    2 * t + p - 4 ≤ 2 * m - p := by omega

theorem endpoint_capacity (su sv : Int) (capacity : su + sv ≤ 0) :
    (su + 1) + (sv + 1) ≤ 2 := by omega

theorem exact_resource_margin (t m b d r u : Int)
    (occupancy : t + 2 * m - 2 * b = d - r)
    (resources : m = d + u) : t + m = 2 * b - u - r := by omega

theorem half_area_from_resources (t m b d r u : Int)
    (occupancy : t + 2 * m - 2 * b = d - r)
    (resources : m = d + u) (unused : 0 ≤ u) (sparse : 0 ≤ r) :
    t + m ≤ 2 * b := by
  have h := exact_resource_margin t m b d r u occupancy resources
  omega

theorem node_forces_next (a prev next : Nat)
    (prev_bit : prev ≤ 1)
    (cover : a + (1 - prev) + next ≥ a + 1) : prev ≤ next := by omega

theorem forced_path (n : Nat) (x : Nat → Nat)
    (source : x 0 = 1)
    (bits : ∀ i, i < n → x i ≤ 1)
    (relay : ∀ i, i + 1 < n → x i ≤ x (i + 1)) :
    ∀ i, i < n → x i = 1 := by
  intro i
  induction i with
  | zero => intro _; exact source
  | succ i ih =>
    intro hi
    have hp := ih (by omega)
    have hr := relay i hi
    have hb := bits (i + 1) hi
    omega

theorem every_old_path_owner_changes (n : Nat) (x : Nat → Nat)
    (source : x 0 = 1)
    (bits : ∀ i, i < n → x i ≤ 1)
    (relay : ∀ i, i + 1 < n → x i ≤ x (i + 1)) :
    ∀ i, i < n → x i ≠ 0 := by
  intro i hi
  have hf := forced_path n x source bits relay i hi
  omega

end SubQuorum.TurningOwnership
#print axioms SubQuorum.TurningOwnership.local_charge_from_owner
#print axioms SubQuorum.TurningOwnership.endpoint_capacity
#print axioms SubQuorum.TurningOwnership.exact_resource_margin
#print axioms SubQuorum.TurningOwnership.half_area_from_resources
#print axioms SubQuorum.TurningOwnership.node_forces_next
#print axioms SubQuorum.TurningOwnership.forced_path
#print axioms SubQuorum.TurningOwnership.every_old_path_owner_changes
