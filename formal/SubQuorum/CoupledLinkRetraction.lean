import Lean.Elab.Tactic.Omega
import Init.Data.List.Perm
import Init.Data.List.Range

set_option autoImplicit false
namespace SubQuorum.CoupledLinkRetraction

/-- Source 0 has only resource 0. Every later source can reach its own
resource or its predecessor. Injectivity forces every full payment to shift.
The network-to-assignment adapter is proved in the accompanying note. -/
theorem serial_full_assignment_forced (n : Nat) (f : Nat → Nat)
    (first : f 0 = 0)
    (allowed : ∀ i, i < n → f i = i ∨ (0 < i ∧ f i = i-1))
    (distinct : ∀ i j, i < n → j < n → f i = f j → i = j) :
    ∀ i, i < n → f i = i := by
  intro i
  induction i with
  | zero => intro _; exact first
  | succ i ih =>
    intro bound
    rcases allowed (i+1) bound with h | h
    · exact h
    · have prev := ih (by omega)
      have eq : f (i+1) = f i := by omega
      have bad := distinct (i+1) i bound (by omega) eq
      omega

/-- Every old link with label 1,...,n-1 must be released. This counts old
link identities, rather than separately charging entry and source conflicts. -/
theorem serial_tail_links_must_release (n : Nat) (f : Nat → Nat)
    (released : Nat → Prop)
    (forced : ∀ i, i < n → f i = i)
    (kept : ∀ i, 0 < i → i < n → ¬ released i → f i = i-1) :
    ∀ i, 0 < i → i < n → released i := by
  intro i positive bound
  by_cases h : released i
  · exact h
  · have a := forced i bound
    have b := kept i positive bound h
    omega

/-- A list of actual released-link labels must contain at least n-1 entries. -/
theorem serial_release_count_lower_bound (n : Nat) (positive : 0 < n)
    (released : List Nat)
    (covers : ∀ i, 0 < i → i < n → i ∈ released) :
    n-1 ≤ released.length := by
  have sub : List.range' 1 (n-1) ⊆ released := by
    intro i hi
    obtain ⟨j,hj,eq⟩ := List.mem_range'.mp hi
    apply covers i <;> omega
  have h := (List.nodup_range' (s:=1) (n:=n-1)).length_le_of_subset sub
  simpa using h

/-- At any budget below n-1 the one-unit deficit persists. -/
theorem serial_plateau (n budget paid : Nat) (two : 2 ≤ n)
    (base : n-1 ≤ paid) (upper : paid ≤ n)
    (fullRequires : paid = n → n-1 ≤ budget)
    (small : budget < n-1) : paid = n-1 := by omega

/-- The full construction retains old link 0 and replaces the other n-1;
there are n-1 two-link routes and one final direct beta route. -/
theorem serial_full_link_count (n : Nat) (positive : 0 < n) :
    2*(n-1)+1 = 2*n-1 := by omega

/-- The reward objective converts retained-link count to retraction count. -/
theorem reward_retraction_identity (old retained : Nat) (bound : retained ≤ old) :
    (old-retained : Nat) + retained = old := by omega

/-- Rewarding retained old links by a scale above the entire possible link
count gives the exact lexicographic objective. -/
theorem reward_strict_priority (bound scale linksA linksB keepA keepB : Int)
    (aLower : 0 ≤ linksA) (_aUpper : linksA ≤ bound)
    (_bLower : 0 ≤ linksB) (bUpper : linksB ≤ bound)
    (dominates : bound < scale) (more : keepB = keepA+1) :
    linksB-scale*keepB < linksA-scale*keepA := by
  simp only [more, Int.mul_add, Int.mul_one]
  omega

theorem reward_equal_priority (scale linksA linksB keep : Int) :
    linksA-scale*keep ≤ linksB-scale*keep ↔ linksA ≤ linksB := by omega

/-- If all one-unit defect bundles have the same positive length, the
whole-budget frontier advances only after another complete bundle. -/
theorem equal_bundle_budget (q length budget repaired : Nat)
    (positive : 0 < length) (count : repaired ≤ q)
    (cost : repaired*length ≤ budget) :
    repaired ≤ min q (budget/length) := by
  apply Nat.le_min.mpr
  exact ⟨count, (Nat.le_div_iff_mul_le positive).mpr cost⟩

#print axioms serial_full_assignment_forced
#print axioms serial_tail_links_must_release
#print axioms serial_release_count_lower_bound
#print axioms serial_plateau
#print axioms serial_full_link_count
#print axioms reward_retraction_identity
#print axioms reward_strict_priority
#print axioms reward_equal_priority
#print axioms equal_bundle_budget
end SubQuorum.CoupledLinkRetraction
