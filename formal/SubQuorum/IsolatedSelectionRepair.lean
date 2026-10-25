import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.IsolatedSelectionRepair

abbrev Subset {α : Type} (A B : α → Prop) : Prop := ∀ x, A x → B x

def Insert {α : Type} (e : α) (A : α → Prop) : α → Prop := fun x => x=e ∨ A x

def Extend {α : Type} (A : α → Prop) : List α → (α → Prop)
  | [] => A
  | e::xs => Insert e (Extend A xs)

theorem subset_extend {α : Type} (A : α → Prop) (xs : List α) : Subset A (Extend A xs) := by
  induction xs with
  | nil => exact fun _ h => h
  | cons e xs ih => exact fun x h => Or.inr (ih x h)

theorem list_member_in_extension {α : Type} (A : α → Prop) (xs : List α) (e : α)
    (member : e∈xs) : Extend A xs e := by
  induction xs with
  | nil => simp at member
  | cons x xs ih =>
    simp only [List.mem_cons] at member
    rcases member with same | tail
    · exact Or.inl same
    · exact Or.inr (ih tail)

theorem insert_absorbed {α : Type} (A : α → Prop) (e : α) (member : A e) :
    Insert e A=A := by
  funext x
  apply propext
  constructor
  · intro h
    rcases h with same | old
    · exact same ▸ member
    · exact old
  · exact Or.inr

/-- Zero marginal gain persists in larger pools. This is the diminishing
returns consequence of the written resource cut submodularity proof. -/
theorem zero_marginal_lifts {α : Type} (rank : (α → Prop) → Nat)
    (mono : ∀ A B, Subset A B → rank A≤rank B)
    (diminishing : ∀ A B e, Subset A B →
      rank (Insert e B)+rank A≤rank (Insert e A)+rank B)
    (A B : α → Prop) (e : α) (included : Subset A B)
    (zero : rank (Insert e A)=rank A) : rank (Insert e B)=rank B := by
  have low := mono B (Insert e B) (fun _ h => Or.inr h)
  have high := diminishing A B e included
  omega

/-- An arbitrarily long list of individually zero marginal candidates
has zero collective gain. No finite enumeration bound is assumed. -/
theorem no_gain_extension {α : Type} (rank : (α → Prop) → Nat)
    (mono : ∀ A B, Subset A B → rank A≤rank B)
    (diminishing : ∀ A B e, Subset A B →
      rank (Insert e B)+rank A≤rank (Insert e A)+rank B)
    (A : α → Prop) (xs : List α)
    (zero : ∀ e, e∈xs → rank (Insert e A)=rank A) : rank (Extend A xs)=rank A := by
  induction xs with
  | nil => rfl
  | cons e xs ih =>
    have tail := ih (fun x hx => zero x (List.mem_cons_of_mem e hx))
    have first := zero e (by simp)
    have lift := zero_marginal_lifts rank mono diminishing A (Extend A xs) e
      (subset_extend A xs) first
    exact lift.trans tail

/-- General finite augmentation: if a covered target has greater rank,
some candidate improves the current pool. This underlies free repair choice. -/
theorem improving_candidate_exists {α : Type} (rank : (α → Prop) → Nat)
    (mono : ∀ A B, Subset A B → rank A≤rank B)
    (diminishing : ∀ A B e, Subset A B →
      rank (Insert e B)+rank A≤rank (Insert e A)+rank B)
    (A B : α → Prop) (xs : List α) (cover : Subset B (Extend A xs))
    (gain : rank A<rank B) : ∃ e, e∈xs ∧ rank A<rank (Insert e A) := by
  classical
  apply Classical.byContradiction
  intro none
  have zero : ∀ e, e∈xs → rank (Insert e A)=rank A := by
    intro e member
    have low := mono A (Insert e A) (fun _ h => Or.inr h)
    have noGain : ¬rank A<rank (Insert e A) := by
      intro yes
      exact none ⟨e,member,yes⟩
    omega
  have unchanged := no_gain_extension rank mono diminishing A xs zero
  have bound := mono B (Extend A xs) cover
  omega

def IndependentOver {α : Type} (rank : (α → Prop) → Nat) (A : α → Prop) : List α → Prop
  | [] => True
  | e::xs => IndependentOver rank A xs ∧ rank (Insert e (Extend A xs))=rank (Extend A xs)+1

theorem independent_extension_count {α : Type} (rank : (α → Prop) → Nat)
    (A : α → Prop) (xs : List α) (independent : IndependentOver rank A xs) :
    rank (Extend A xs)=rank A+xs.length := by
  induction xs with
  | nil => simp [Extend]
  | cons e xs ih =>
    have tail := ih independent.1
    have step := independent.2
    change rank (Insert e (Extend A xs))=rank A+(xs.length+1)
    omega

theorem independent_candidates_distinct {α : Type} (rank : (α → Prop) → Nat)
    (A : α → Prop) (xs : List α) (independent : IndependentOver rank A xs) : xs.Nodup := by
  induction xs with
  | nil => exact List.nodup_nil
  | cons e xs ih =>
    apply List.nodup_cons.mpr
    constructor
    · intro member
      have inPool := list_member_in_extension A xs e member
      have absorbed := insert_absorbed (Extend A xs) e inPool
      have impossible := independent.2
      rw [absorbed] at impossible
      omega
    · exact ih independent.1

theorem extension_gain_at_most_count {α : Type} (rank : (α → Prop) → Nat)
    (unitBound : ∀ A e, rank (Insert e A)≤rank A+1)
    (A : α → Prop) (xs : List α) : rank (Extend A xs)≤rank A+xs.length := by
  induction xs with
  | nil => simp [Extend]
  | cons e xs ih =>
    have bound := unitBound (Extend A xs) e
    change rank (Insert e (Extend A xs))≤rank A+(xs.length+1)
    omega

theorem independent_spanning_is_minimum {α : Type} (rank : (α → Prop) → Nat)
    (unitBound : ∀ A e, rank (Insert e A)≤rank A+1)
    (A : α → Prop) (chosen other : List α)
    (independent : IndependentOver rank A chosen)
    (spans : rank (Extend A chosen)≤rank (Extend A other)) : chosen.length≤other.length := by
  have exactCount := independent_extension_count rank A chosen independent
  have upper := extension_gain_at_most_count rank unitBound A other
  omega

/-- The old P-neighborhood sees no deleted point, so its entire occupied
neighbor predicate remains literally the same. -/
theorem endpoint_neighbors_unchanged {V : Type} (occupied removed endpoints : V → Prop)
    (adjacent : V → V → Prop)
    (isolatedFromP : ∀ p x, endpoints p → adjacent p x → ¬removed x)
    (p x : V) (hp : endpoints p) (neighbor : adjacent p x) :
    (occupied x ∧ ¬removed x) ↔ occupied x := by
  exact ⟨And.left,fun old => ⟨old,isolatedFromP p x hp neighbor⟩⟩

/-- A TT column next to a selected candidate would make the adjacent TT
cell see its mate and the candidate, violating feasible occupied degree. -/
theorem neighboring_TT_forbidden {V : Type} (occupied : V → Prop)
    (adjacent : V → V → Prop) (cell mate candidate : V)
    (mateOccupied : occupied mate) (candidateOccupied : occupied candidate)
    (mateNeighbor : adjacent cell mate) (candidateNeighbor : adjacent cell candidate)
    (different : mate≠candidate)
    (feasible : ∀ u v, adjacent cell u → adjacent cell v → occupied u → occupied v → u=v) : False := by
  exact different (feasible mate candidate mateNeighbor candidateNeighbor mateOccupied candidateOccupied)

/-- A deletion only adds one sink; gain cannot exceed the number deleted.
Thus opening resources cannot lower this combined slack/deficit budget. -/
theorem slack_deficit_monotone (oldSlack oldDeficit newSlack newDeficit deleted gain : Int)
    (s : newSlack=oldSlack+deleted) (d : newDeficit=oldDeficit-gain)
    (unitBound : gain≤deleted) : oldSlack+oldDeficit≤newSlack+newDeficit := by omega

theorem minimum_repairs_for_full_payment (k p repairs : Nat) (baseline : p≤k)
    (gainBound : k≤p+repairs) : k-p≤repairs := by omega

#print axioms subset_extend
#print axioms list_member_in_extension
#print axioms insert_absorbed
#print axioms zero_marginal_lifts
#print axioms no_gain_extension
#print axioms improving_candidate_exists
#print axioms independent_extension_count
#print axioms independent_candidates_distinct
#print axioms extension_gain_at_most_count
#print axioms independent_spanning_is_minimum
#print axioms endpoint_neighbors_unchanged
#print axioms neighboring_TT_forbidden
#print axioms slack_deficit_monotone
#print axioms minimum_repairs_for_full_payment

end SubQuorum.IsolatedSelectionRepair
