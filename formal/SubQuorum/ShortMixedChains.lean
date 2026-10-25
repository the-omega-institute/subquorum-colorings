import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.ShortMixedChains

/-- Columns of the internal link from short owner i to owner i+1,
    normalized to a chain pointing right. Physical reflection handles left. -/
def sourceColumn (i : Nat) : Nat := 2*i+1
def targetColumn (i : Nat) : Nat := 2*i+2

theorem internal_links_disjoint (i j : Nat) :
    (sourceColumn i = sourceColumn j → i = j) ∧
    (targetColumn i = targetColumn j → i = j) ∧
    sourceColumn i ≠ targetColumn j := by
  unfold sourceColumn targetColumn
  omega

theorem internal_link_adjacent (i : Nat) :
    sourceColumn i + 1 = targetColumn i := by
  unfold sourceColumn targetColumn
  omega

/-- A strictly progressing physical column cannot return to its start. -/
theorem strict_progress_no_cycle {V : Type} (column : V → Int)
    (edge : V → V → Prop)
    (progress : ∀ a b, edge a b → column a < column b)
    (a b : V) (ab : edge a b) (back : column b ≤ column a) : False := by
  have h := progress a b ab
  omega

theorem chain_toll_exact (m : Nat) (nonempty : 1 ≤ m) :
    1 + (m-1) = m := by omega

theorem hole_budget_monotone (oldHoles newHoles : Nat)
    (fewer : newHoles ≤ oldHoles) : newHoles / 2 ≤ oldHoles / 2 := by omega

theorem one_tail_zero_budget (holes : Nat) (one : holes ≤ 1) :
    holes / 2 = 0 := by omega

/-- Arbitrary-length owner walks; no enumeration cutoff is assumed. -/
inductive Walk {V : Type} (edge : V → V → Prop) : Nat → V → V → Prop where
  | nil (a : V) : Walk edge 0 a a
  | cons {n : Nat} {a b c : V} : edge a b → Walk edge n b c →
      Walk edge (n+1) a c

theorem walk_potential_bound {V : Type} (edge : V → V → Prop)
    (potential : V → Nat)
    (step : ∀ a b, edge a b → potential b ≤ potential a + 1)
    {n : Nat} {a b : V} (walk : Walk edge n a b) :
    potential b ≤ potential a + n := by
  induction walk with
  | nil a => omega
  | @cons n a b c ab rest ih =>
    have h := step a b ab
    omega

/-- The restricted actual-board owner graph exported by the Python checker:
    alpha 0, long mixed 1, unused mixed 2/3, short chain 4 -> 5.
    The only available original interval is supported by owner 5. -/
def edge (a b : Nat) : Prop :=
    (a = 0 ∧ b = 1) ∨ (a = 1 ∧ b = 4) ∨ (a = 4 ∧ b = 5)

def potential (a : Nat) : Nat :=
    if a = 0 then 0 else if a = 1 then 1 else if a = 4 then 2 else 3

theorem concrete_edge_potential (a b : Nat) (ab : edge a b) :
    potential b ≤ potential a + 1 := by
  rcases ab with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;> decide

theorem every_paying_walk_cost_at_least_three (n : Nat)
    (walk : Walk edge n 0 5) : 3 ≤ n := by
  have h := walk_potential_bound edge potential concrete_edge_potential walk
  have h0 : potential 0 = 0 := by decide
  have h5 : potential 5 = 3 := by decide
  omega

theorem three_link_paying_walk : Walk edge 3 0 5 := by
  have e01 : edge 0 1 := Or.inl ⟨rfl, rfl⟩
  have e14 : edge 1 4 := Or.inr (Or.inl ⟨rfl, rfl⟩)
  have e45 : edge 4 5 := Or.inr (Or.inr ⟨rfl, rfl⟩)
  exact Walk.cons e01 (Walk.cons e14 (Walk.cons e45 (Walk.nil 5)))

theorem separated_toll_ledger (q : Nat) :
    q * 3 = q * 2 + q ∧ (0 < q → q * 2 < q * 3) := by omega

#print axioms internal_links_disjoint
#print axioms internal_link_adjacent
#print axioms strict_progress_no_cycle
#print axioms chain_toll_exact
#print axioms hole_budget_monotone
#print axioms one_tail_zero_budget
#print axioms walk_potential_bound
#print axioms concrete_edge_potential
#print axioms every_paying_walk_cost_at_least_three
#print axioms three_link_paying_walk
#print axioms separated_toll_ledger

end SubQuorum.ShortMixedChains
