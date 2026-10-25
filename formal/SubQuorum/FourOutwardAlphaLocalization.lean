import Lean.Elab.Tactic.Omega

set_option autoImplicit false

/-! The geometric injections are proved in FOUR_OUTWARD_ALPHA_LOCALIZATION.md.
This module checks their local finite geometry and aggregate arithmetic.
It does not identify abstract flags with arbitrary physical grid owners. -/
namespace SubQuorum.FourOutwardAlphaLocalization

def bit (b : Bool) : Nat := if b then 1 else 0

def verticalOnly (nw ne sw se : Bool) : Nat :=
  bit (!nw && !sw) + bit (!ne && !se)

def doubleFaces (nw ne sw se : Bool) : Nat :=
  bit (!nw && !ne) + bit (!sw && !se) + bit (nw && sw) + bit (ne && se)

/-- True flags are horizontal actual exits, after normalizing N vertically. -/
theorem sixteen_exit_cases (nw ne sw se : Bool) :
    verticalOnly nw ne sw se ≤ doubleFaces nw ne sw se := by
  cases nw <;> cases ne <;> cases sw <;> cases se <;> decide

/-- When N directions differ, exactly one endpoint is perpendicular to M. -/
theorem direction_change_one_endpoint (first second axis : Bool)
    (h : first ≠ second) :
    bit (first != axis) + bit (second != axis) = 1 := by
  cases first <;> cases second <;> cases axis <;> simp_all [bit]

theorem two_removed_neighbors (degree : Nat) (h : degree ≤ 3) :
    degree - 2 ≤ 1 := by omega

/-- The frozen-square adapter supplies the exclusion of two degree<=3 corners. -/
theorem each_color_has_defect (d e : Nat) (hd : d ≤ 4) (he : e ≤ 4)
    (blocked : ¬ (d ≤ 3 ∧ e ≤ 3)) : d = 4 ∨ e = 4 := by omega

theorem local_wire_bound (i a b c D v h : Nat)
    (split : i ≤ v + h) (vertical : v ≤ D)
    (double : 2 * D ≤ a + b) (horizontal : h ≤ a + c) :
    2 * i ≤ 3 * a + b + 2 * c := by omega

theorem local_exact_three (i c : Nat) (h : 2 * i ≤ 2 * c) : i ≤ c := by omega

structure TileLedger where
  i : Nat
  a : Nat
  b : Nat
  c : Nat

def total (f : TileLedger → Nat) (xs : List TileLedger) : Nat :=
  (xs.map f).sum

theorem sum_local (xs : List TileLedger)
    (perTile : ∀ x ∈ xs, 2*x.i ≤ 3*x.a + x.b + 2*x.c) :
    2 * total TileLedger.i xs ≤
      3 * total TileLedger.a xs + total TileLedger.b xs + 2 * total TileLedger.c xs := by
  induction xs with
  | nil => simp [total]
  | cons x xs ih =>
    have hx := perTile x (by simp)
    have ht := ih (by intro y hy; exact perTile y (by simp [hy]))
    simp only [total, List.map_cons, List.sum_cons] at *
    omega

/-- Two flags refer to a defect's own tile and its actual mate's tile in F. -/
def endpointWeight (p : Bool × Bool) : Nat := 3 * bit p.1 + bit p.2

theorem endpoint_weight_cap (p : Bool × Bool) : endpointWeight p ≤ 4 := by
  rcases p with ⟨a,b⟩
  cases a <;> cases b <;> decide

theorem all_endpoint_weights (ps : List (Bool × Bool)) :
    (ps.map endpointWeight).sum ≤ 4 * ps.length := by
  induction ps with
  | nil => simp
  | cons p ps ih =>
    have hp := endpoint_weight_cap p
    simp only [List.map_cons, List.sum_cons, List.length_cons]
    omega

/-- The geometry supplies the exact incidence identities and seam injection. -/
theorem aggregate_bound (xs : List TileLedger) (J E : Nat)
    (perTile : ∀ x ∈ xs, 2*x.i ≤ 3*x.a + x.b + 2*x.c)
    (weighted : 3 * total TileLedger.a xs + total TileLedger.b xs ≤ 4 * J)
    (seams : total TileLedger.c xs ≤ E) :
    total TileLedger.i xs ≤ 2 * J + E := by
  have h := sum_local xs perTile
  omega

theorem uniform_exact_three (I : Nat) (h : I ≤ 2 * 0 + 0) : I = 0 := by omega

#print axioms sixteen_exit_cases
#print axioms direction_change_one_endpoint
#print axioms two_removed_neighbors
#print axioms each_color_has_defect
#print axioms local_wire_bound
#print axioms local_exact_three
#print axioms sum_local
#print axioms endpoint_weight_cap
#print axioms all_endpoint_weights
#print axioms aggregate_bound
#print axioms uniform_exact_three

end SubQuorum.FourOutwardAlphaLocalization
