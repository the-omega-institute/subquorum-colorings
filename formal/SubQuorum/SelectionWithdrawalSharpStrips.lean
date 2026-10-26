import Lean.Elab.Tactic.Omega
set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 1600000
namespace SubQuorum.SelectionWithdrawalSharpStrips

/-- A strict witness cannot be the endpoint's own mate. -/
theorem strict_witness_not_mate {V : Type} (P T : V → Prop) (mate : V → V)
    (rank : V → Nat) (v w : V) (inv : mate (mate v) = v)
    (pm : P (mate v)) (disjoint : ∀ u, P u → ¬T u)
    (witness : T w ∨ (P w ∧ rank (mate w) < rank v)) : w ≠ mate v := by
  intro eq
  subst w
  rcases witness with selected | ⟨_, lower⟩
  · exact disjoint (mate v) pm selected
  · rw [inv] at lower
    omega

/-- Mate plus at most one other occupied neighbour cannot supply strict witnesses. -/
theorem mate_plus_one_exclusion {V : Type} (P T : V → Prop) (mate : V → V)
    (rank : V → Nat) (adj : V → V → Prop) (v p : V)
    (inv : mate (mate v) = v) (pm : P (mate v))
    (disjoint : ∀ u, P u → ¬T u)
    (only : ∀ u, adj v u → (P u ∨ T u) → u = mate v ∨ u = p) :
    ¬ ∃ a b, a ≠ b ∧ adj v a ∧ adj v b ∧
      (T a ∨ (P a ∧ rank (mate a) < rank v)) ∧
      (T b ∨ (P b ∧ rank (mate b) < rank v)) := by
  rintro ⟨a,b,distinct,ha,hb,wa,wb⟩
  have na := strict_witness_not_mate P T mate rank v a inv pm disjoint wa
  have nb := strict_witness_not_mate P T mate rank v b inv pm disjoint wb
  have oa : P a ∨ T a := by
    rcases wa with ht | ⟨hp,_⟩
    · exact Or.inr ht
    · exact Or.inl hp
  have ob : P b ∨ T b := by
    rcases wb with ht | ⟨hp,_⟩
    · exact Or.inr ht
    · exact Or.inl hp
  have ap : a = p := (only a ha oa).resolve_left na
  have bp : b = p := (only b hb ob).resolve_left nb
  exact distinct (ap.trans bp.symm)

/-- Indicators of new occupation, expressed using actual NEW edges in the
    free tree; old matching edges are retained in this theorem's grid adapter. -/
def occ (t m : Nat → Nat) : Nat → Nat
  | 0 => t 0 + m 0
  | 1 => t 1 + m 0 + m 1
  | 2 => t 2 + m 1 + m 2 + m 3
  | 3 => t 3 + m 4
  | 4 => t 4 + m 2 + m 4
  | 5 => t 5 + m 3 + m 5
  | 6 => t 6 + m 5 + m 6 + m 7
  | 7 => t 7 + m 6
  | 8 => t 8 + m 7
  | _ => 0

def sumT (t : Nat → Nat) : Nat := t 0+t 1+t 2+t 3+t 4+t 5+t 6+t 7+t 8
def sumM (m : Nat → Nat) : Nat := m 0+m 1+m 2+m 3+m 4+m 5+m 6+m 7
def weightedLHS (t m : Nat → Nat) : Nat :=
  (t 1+occ t m 0) +
  (t 2+occ t m 1+occ t m 4) +
  (t 2+occ t m 4+occ t m 5) +
  (t 5+occ t m 2+occ t m 6) +
  (t 6+occ t m 7+occ t m 8) +
  t 0+t 7+t 8+2*t 3

theorem weighted_identity (t m : Nat → Nat) :
    weightedLHS t m=2*(sumT t+sumM m)+t 2+m 2 := by
  simp only [weightedLHS,occ,sumT,sumM]
  omega

theorem tree_bound (t m : Nat → Nat) (td : t 0 ≤ 1) (tl : t 7 ≤ 1)
    (tr : t 8 ≤ 1) (tu : t 3=0) (anchor : t 1+occ t m 0 ≤ 1)
    (h0 : t 2+occ t m 1+occ t m 4 ≤ 2)
    (h1 : t 2+occ t m 4+occ t m 5 ≤ 2)
    (h2 : t 5+occ t m 2+occ t m 6 ≤ 2)
    (h3 : t 6+occ t m 7+occ t m 8 ≤ 2)
    : sumT t+sumM m ≤ 6 := by
  have hb : weightedLHS t m ≤ 12 := by
    unfold weightedLHS
    omega
  have hi := weighted_identity t m
  omega

theorem tree_equality_data (t m : Nat → Nat) (td : t 0 ≤ 1) (tl : t 7 ≤ 1)
    (tr : t 8 ≤ 1) (tu : t 3=0) (anchor : t 1+occ t m 0 ≤ 1)
    (h0 : t 2+occ t m 1+occ t m 4 ≤ 2)
    (h1 : t 2+occ t m 4+occ t m 5 ≤ 2)
    (h2 : t 5+occ t m 2+occ t m 6 ≤ 2)
    (h3 : t 6+occ t m 7+occ t m 8 ≤ 2)
    (maximum : sumT t+sumM m=6) :
    t 0=1 ∧ t 7=1 ∧ t 8=1 ∧ t 2=0 ∧ m 2=0 := by
  have hi := weighted_identity t m
  have hb : weightedLHS t m ≤ 9+t 0+t 7+t 8 := by
    unfold weightedLHS
    omega
  omega

/-- All distinct free components are counted once, including q merged trees. -/
theorem global_extra_bound (k q extra : Nat) (valid : q+1 ≤ k)
    (partitionBound : extra ≤ 9+6*q+4*(k-1-q)+(k+1)) :
    extra ≤ 5*k+6+2*q := by omega

theorem total_objective_bound (k q extra total : Nat)
    (extraBound : extra ≤ 5*k+6+2*q)
    (oldCount : total+q=12*k+6+extra) :
    total ≤ 17*k+12+q := by omega

theorem whole_margin_bound (k q total : Nat) (valid : q ≤ k)
    (bound : total ≤ 17*k+12+q) : total+(k-q) ≤ 18*k+12 := by omega

/-- Original tile-column identity of the ONE half-unit donor for demand i.
    Activated guard i uses the successor reserve; otherwise its old rebate. -/
def donorColumn (active : Nat → Bool) (i : Nat) : Nat :=
  if active i then 5+3*i else 4+3*i

theorem successor_payment_injective (active : Nat → Bool) (i j : Nat)
    (same : donorColumn active i=donorColumn active j) : i=j := by
  cases hi : active i <;> cases hj : active j <;>
    simp [donorColumn,hi,hj] at same <;> omega

/-- A full-unit reserve is unspent only if no activated predecessor uses it. -/
theorem remaining_reserve_not_spent (active : Nat → Bool) (j : Nat)
    (remaining : ∀ i, active i=true → j ≠ i+1) :
    ∀ i, donorColumn active i ≠ 2+3*j := by
  intro i same
  cases hi : active i
  · simp [donorColumn,hi] at same
    omega
  · have avoid := remaining i hi
    simp [donorColumn,hi] at same
    omega

theorem exact_physical_ledger (k q : Int) :
    (1-k)+(k-1)+2*(k-q)=2*(k-q) := by omega

/-- If all old matching edges are retained, new endpoints must match among
    themselves. This is a general obstruction to occupation-preserving repair. -/
theorem remainder_closed {V : Type} (old extra : V → Prop)
    (actual prescribed : V → V)
    (involution : ∀ v, actual (actual v)=v)
    (oldClosed : ∀ v, old v → old (prescribed v))
    (retained : ∀ v, old v → actual v=prescribed v)
    (closed : ∀ v, extra v → old (actual v) ∨ extra (actual v))
    (disjoint : ∀ v, old v → ¬extra v) :
    ∀ v, extra v → extra (actual v) := by
  intro v hv
  rcases closed v hv with ho | he
  · have back := oldClosed (actual v) ho
    rw [←retained (actual v) ho,involution v] at back
    exact False.elim (disjoint v back hv)
  · exact he

theorem isolated_remainder_obstruction {V : Type} (extra : V → Prop)
    (actual : V → V) (adj : V → V → Prop) (v : V)
    (member : extra v) (closed : ∀ u, extra u → extra (actual u))
    (legal : adj v (actual v))
    (isolated : ∀ u, extra u → ¬adj v u) : False :=
  isolated (actual v) (closed v member) legal

abbrev Point := Nat × Nat

def adjacent (a b : Point) : Prop :=
  (a.1=b.1 ∧ (a.2+1=b.2 ∨ b.2+1=a.2)) ∨
  (a.2=b.2 ∧ (a.1+1=b.1 ∨ b.1+1=a.1))
instance (a b : Point) : Decidable (adjacent a b) :=
  inferInstanceAs (Decidable ((_ ∧ (_ ∨ _)) ∨ (_ ∧ (_ ∨ _))))

theorem isolated_new_endpoint_geometry :
    ([(2,5),(3,4),(3,5),(3,9)] : List Point).all
      (fun u => decide (¬adjacent (3,9) u)) = true := by decide

#print axioms strict_witness_not_mate
#print axioms mate_plus_one_exclusion
#print axioms weighted_identity
#print axioms tree_bound
#print axioms tree_equality_data
#print axioms global_extra_bound
#print axioms total_objective_bound
#print axioms whole_margin_bound
#print axioms successor_payment_injective
#print axioms remaining_reserve_not_spent
#print axioms exact_physical_ledger
#print axioms remainder_closed
#print axioms isolated_remainder_obstruction
#print axioms isolated_new_endpoint_geometry

end SubQuorum.SelectionWithdrawalSharpStrips
