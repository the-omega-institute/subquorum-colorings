import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.MonotoneCompletionDeficit

/-- An existing band link protects its BP partner. The geometric adapter gives
adjacency of the two physical N partners; feasibility supplies uniqueness of
an occupied neighbour of any selected site. No finite graph is assumed. -/
theorem old_link_protects_BP (Site : Type) (P T₀ T₁ : Site → Prop)
    (N : Site → Site) (Adj : Site → Site → Prop) (p q : Site)
    (retained : ∀ v, T₀ v → T₁ v)
    (disjoint : ∀ v, P v → ¬ T₁ v)
    (feasible : ∀ v, T₁ v → ∀ a b,
      (P a ∨ T₁ a) → (P b ∨ T₁ b) → Adj v a → Adj v b → a = b)
    (anchor : P p) (oldTP : T₀ (N q))
    (ownAnchor : Adj (N p) p) (parallel : Adj (N p) (N q)) :
    ¬ T₁ (N p) := by
  intro converted
  have oldSelected := retained (N q) oldTP
  have same := feasible (N p) converted p (N q)
    (Or.inl anchor) (Or.inr oldSelected) ownAnchor parallel
  have occupied : P (N q) := same ▸ anchor
  exact disjoint (N q) occupied oldSelected

/-- A physically converting beta tip cannot be one of two used fork entries. -/
theorem converting_beta_has_no_old_fork (Entry : Prop) (Fork : Prop)
    (protectedTip : ¬ Entry) (twoEntries : Fork → Entry) : ¬ Fork := by
  intro fork
  exact protectedTip (twoEntries fork)

/-- If both old beta tips convert, every old source-to-beta route is absent. -/
theorem double_conversion_beta_unused (EntryLeft EntryRight Used : Prop)
    (leftProtected : ¬ EntryLeft) (rightProtected : ¬ EntryRight)
    (routeNeedsEntry : Used → EntryLeft ∨ EntryRight) : ¬ Used := by
  intro used
  rcases routeNeedsEntry used with left | right
  · exact leftProtected left
  · exact rightProtected right

/-- Resource loss, beta loss and births use ONE physical addition budget.
The lower/upper payment adapters are supplied by the packing transformations. -/
theorem joint_budget (a₀ a₁ v₀ v₁ h t r s added : Int)
    (births : a₁ = a₀ + r + s)
    (singleBudget : added = h + t + r + 2*s)
    (retainedPayments : v₀ - h - t ≤ v₁)
    (reversePayments : v₁ ≤ v₀ + r + s) :
    0 ≤ (a₁-v₁)-(a₀-v₀) ∧ (a₁-v₁)-(a₀-v₀) ≤ added-s := by
  omega

/-- A newly born mixed-body source does not consume an old incoming route. -/
theorem mixed_birth_step (a₀ a₁ v₀ v₁ : Int)
    (birth : a₁ = a₀+1) (keepOld : v₀ ≤ v₁) (discardNew : v₁ ≤ v₀+1) :
    (a₁-v₁)-(a₀-v₀) = 0 ∨ (a₁-v₁)-(a₀-v₀) = 1 := by omega

/-- A beta credit may be lost once even if it has two physical ends. -/
theorem beta_loss_step (a₀ a₁ v₀ v₁ : Int)
    (sameSources : a₁ = a₀) (loseAtMostOne : v₀-1 ≤ v₁) (truncate : v₁ ≤ v₀) :
    (a₁-v₁)-(a₀-v₀) = 0 ∨ (a₁-v₁)-(a₀-v₀) = 1 := by omega

/-- Arbitrarily many additions, without a bound on sequence length. -/
theorem chain_budget (D : Nat → Int) (steps : ∀ i, 0 ≤ D (i+1)-D i ∧ D (i+1)-D i ≤ 1) :
    ∀ n, 0 ≤ D n-D 0 ∧ D n-D 0 ≤ (n : Int) := by
  intro n
  induction n with
  | zero => simp
  | succ n ih =>
      have h := steps n
      omega

theorem corrected_potential (S₀ S₁ D₀ D₁ added betaBirth : Int)
    (slack : S₁=S₀-added) (budget : 0 ≤ D₁-D₀ ∧ D₁-D₀ ≤ added-betaBirth) :
    -added ≤ (S₁+D₁)-(S₀+D₀) ∧ (S₁+D₁)-(S₀+D₀) ≤ -betaBirth := by omega

/-- Fixed-partition completion cannot repair an existing positive deficit. -/
theorem positive_deficit_persists (D₀ D₁ : Int) (positive : 0 < D₀)
    (monotone : D₀ ≤ D₁) : 0 < D₁ := by omega

/-- A finite vertex list is wholly endangered exactly when no entry is safe.
This is the local component predicate in the path-resource deficit formula. -/
def whollyEndangered : List Bool → Bool
  | [] => true
  | x::xs => x && whollyEndangered xs

theorem whollyEndangered_iff (xs : List Bool) :
    whollyEndangered xs = true ↔ ∀ x ∈ xs, x = true := by
  induction xs with
  | nil => simp [whollyEndangered]
  | cons x xs ih => simp [whollyEndangered, ih]

/-- In an all-birth circuit a single absent birth forces the component tax to
zero, independent of the length of the source list. -/
theorem absent_birth_breaks_circuit (xs : List Bool) (absent : false ∈ xs) :
    whollyEndangered xs = false := by
  cases h : whollyEndangered xs
  · rfl
  · have all := (whollyEndangered_iff xs).mp h
    have bad := all false absent
    contradiction

/-- Two individually harmless events may jointly activate one source tax. -/
theorem source_beta_AND :
    whollyEndangered [false,false] = false ∧
    whollyEndangered [true,false] = false ∧
    whollyEndangered [false,true] = false ∧
    whollyEndangered [true,true] = true := by decide

end SubQuorum.MonotoneCompletionDeficit

#print axioms SubQuorum.MonotoneCompletionDeficit.old_link_protects_BP
#print axioms SubQuorum.MonotoneCompletionDeficit.converting_beta_has_no_old_fork
#print axioms SubQuorum.MonotoneCompletionDeficit.double_conversion_beta_unused
#print axioms SubQuorum.MonotoneCompletionDeficit.joint_budget
#print axioms SubQuorum.MonotoneCompletionDeficit.mixed_birth_step
#print axioms SubQuorum.MonotoneCompletionDeficit.beta_loss_step
#print axioms SubQuorum.MonotoneCompletionDeficit.chain_budget
#print axioms SubQuorum.MonotoneCompletionDeficit.corrected_potential
#print axioms SubQuorum.MonotoneCompletionDeficit.positive_deficit_persists
#print axioms SubQuorum.MonotoneCompletionDeficit.whollyEndangered_iff
#print axioms SubQuorum.MonotoneCompletionDeficit.absent_birth_breaks_circuit
#print axioms SubQuorum.MonotoneCompletionDeficit.source_beta_AND
