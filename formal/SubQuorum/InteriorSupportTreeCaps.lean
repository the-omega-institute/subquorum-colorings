import SubQuorum.BTColumnCorridorObstruction

set_option autoImplicit false

namespace SubQuorum.InteriorSupportTreeCaps
open SubQuorum.BTColumnCorridorObstruction (Point adjacent Frozen)

def capP (c : Nat) (v : Point) : Prop :=
  v ∈ [(6,c), (7,c), (8,c), (9,c)]

def capT (c : Nat) (v : Point) : Prop :=
  v ∈ [(5,c), (6,c+1), (8,c+1), (10,c), (7,c-1), (9,c-1)]

def capMate (c : Nat) (v : Point) : Point :=
  if v = (6,c) then (7,c) else if v = (7,c) then (6,c)
  else if v = (8,c) then (9,c) else if v = (9,c) then (8,c) else v

def capAdj (c : Nat) (v w : Point) : Prop := adjacent v w ∧ w ≠ capMate c v

/-- The four new cap endpoints freeze with actual vertical mates, for every
positive cap column. The rest of the geometric adapter remains a written proof. -/
theorem cap_frozen (c : Nat) (hc : 1 ≤ c) :
    ∀ v, capP c v → Frozen (capP c) (capT c) (capMate c) (capAdj c) v := by
  have f6 : Frozen (capP c) (capT c) (capMate c) (capAdj c) (6,c) := by
    apply Frozen.ss (a := (5,c)) (b := (6,c+1))
    all_goals simp [capP, capT, capAdj, adjacent, capMate]
  have f9 : Frozen (capP c) (capT c) (capMate c) (capAdj c) (9,c) := by
    apply Frozen.ss (a := (9,c-1)) (b := (10,c))
    all_goals simp [capP, capT, capAdj, adjacent, capMate] <;> omega
  have f7 : Frozen (capP c) (capT c) (capMate c) (capAdj c) (7,c) := by
    apply Frozen.sp (a := (7,c-1)) (b := (8,c))
    · simp [capP]
    · simp
    · simp [capAdj, adjacent, capMate]; omega
    · simp [capAdj, adjacent, capMate]
    · simp [capT]
    · simp [capP]
    · simpa [capMate] using f9
  have f8 : Frozen (capP c) (capT c) (capMate c) (capAdj c) (8,c) := by
    apply Frozen.sp (a := (8,c+1)) (b := (7,c))
    · simp [capP]
    · simp
    · simp [capAdj, adjacent, capMate]
    · simp [capAdj, adjacent, capMate]
    · simp [capT]
    · simp [capP]
    · simpa [capMate] using f6
  intro v hv
  simp [capP] at hv
  rcases hv with h | h | h | h
  · exact h ▸ f6
  · exact h ▸ f7
  · exact h ▸ f8
  · exact h ▸ f9

theorem cap_mate_closed (c : Nat) : ∀ v, capP c v → capP c (capMate c v) := by
  intro v hv
  simp [capP] at hv
  rcases hv with h | h | h | h <;> subst v <;> simp [capMate, capP]

def tailRow (r col : Nat) : Nat := if col % 2 = 1 then r else r+1

theorem tail_row_alternates (r col : Nat) :
    tailRow r col ≠ tailRow r (col+1) := by
  simp only [tailRow]
  split <;> split <;> omega

theorem tail_not_horizontal_neighbors (r col : Nat) :
    ¬ adjacent (tailRow r col,col) (tailRow r (col+1),col+1) := by
  have different := tail_row_alternates r col
  simp only [adjacent]
  omega

/-- Exact scalar ledger for the written all-length family and empty padding. -/
theorem capped_ledger (d r : Nat) :
    12*(20+2*d+2*r) = 2*((33+4*d)+25+12+(50+8*d+12*r)) ∧
    (51+8*d+12*r)-1 = 50+8*d+12*r := by omega

/-- All tokens not assigned internally are external; a tree has n-1 units. -/
theorem two_external_witnesses (n internal external : Nat) (hn : 1 ≤ n)
    (partition : internal+external = 2*n)
    (capacity : internal ≤ 2*(n-1)) : 2 ≤ external := by omega

/-- The geometric fiber capacities and Hall witness supply these hypotheses.
The theorem checks their arithmetic consequence, not those adapters. -/
theorem hall_defect_bound (trees neighbors betaTokens zeroTokens : Nat)
    (lower : 2*trees ≤ betaTokens+zeroTokens)
    (upper : betaTokens ≤ 2*neighbors)
    (hall : neighbors ≤ trees) : 2*(trees-neighbors) ≤ zeroTokens := by omega

theorem at_most_one_zero_token_forces_saturation
    (trees matched zeroTokens : Nat)
    (bounded : 2*(trees-matched) ≤ zeroTokens)
    (small : zeroTokens ≤ 1) (matching : matched ≤ trees) : matched = trees := by omega

#print axioms cap_frozen
#print axioms cap_mate_closed
#print axioms tail_row_alternates
#print axioms tail_not_horizontal_neighbors
#print axioms capped_ledger
#print axioms two_external_witnesses
#print axioms hall_defect_bound
#print axioms at_most_one_zero_token_forces_saturation

end SubQuorum.InteriorSupportTreeCaps
