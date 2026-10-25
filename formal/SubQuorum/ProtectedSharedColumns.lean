import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.ProtectedSharedColumns

/-- A nearest-neighbour involution on an even finite path has the forced
consecutive matching. The physical collar-to-path adapter is written in
the note, not assumed to have been formalized by this theorem. -/
theorem even_path_pairing (L : Nat) (mate : Nat → Nat)
    (involutive : ∀ x, x < 2*L → mate (mate x) = x)
    (step : ∀ x, x < 2*L → mate x + 1 = x ∨ x + 1 = mate x)
    (i : Nat) (hi : i < L) :
    mate (2*i) = 2*i+1 ∧ mate (2*i+1) = 2*i := by
  induction i with
  | zero =>
    have h := step 0 (by omega)
    have first : mate 0 = 1 := by omega
    have second := involutive 0 (by omega)
    simp only [first] at second
    exact ⟨first, second⟩
  | succ i ih =>
    have previous := ih (by omega)
    have h := step (2*(i+1)) (by omega)
    have first : mate (2*(i+1)) = 2*(i+1)+1 := by
      rcases h with lower | upper
      · have eq : mate (2*(i+1)) = 2*i+1 := by omega
        have twice := involutive (2*(i+1)) (by omega)
        rw [eq, previous.2] at twice
        omega
      · omega
    have second := involutive (2*(i+1)) (by omega)
    rw [first] at second
    exact ⟨first, second⟩

/-- The opposite-side blank has a retained selected guard one row away.
This checks the index is inside the column, including both ends. -/
theorem side_guard_indices (L j : Nat) (hj : j < 2*L) :
    (j%2=0 → j+1<2*L) ∧ (j%2=1 → 0<j ∧ j-1<2*L) := by
  omega

/-- Strict rank dependencies for even and odd endpoint chains. -/
theorem strict_rank_dependencies (L i : Nat) :
    (0<i → i-1<i) ∧
    (i+1<L → L-(i+1)-1<L-i-1) := by omega

/-- Slot=(bottom?, gap index); two geometrically different singleton units
per gap. Source 0 uses top gap 0; source 1 uses bottom gap 0; later sources
use the top unit of the gap immediately to their left. -/
def assignedSlot : Nat → Bool × Nat
  | 0 => (false,0)
  | 1 => (true,0)
  | i+2 => (false,i+1)

theorem assigned_slot_injective (i j : Nat)
    (h : assignedSlot i = assignedSlot j) : i=j := by
  match i,j with
  | 0,0 => rfl
  | 0,1 => simp [assignedSlot] at h
  | 0,j+2 => simp [assignedSlot] at h
  | 1,0 => simp [assignedSlot] at h
  | 1,1 => rfl
  | 1,j+2 => simp [assignedSlot] at h
  | i+2,0 => simp [assignedSlot] at h
  | i+2,1 => simp [assignedSlot] at h
  | i+2,j+2 =>
    simp only [assignedSlot, Prod.mk.injEq, true_and] at h
    omega

theorem assigned_slot_eligible (m i : Nat) (hm : 2≤m) (hi : i<m) :
    (assignedSlot i).2 < m-1 ∧
    ((assignedSlot i).2=i ∨ (assignedSlot i).2+1=i) := by
  match i with
  | 0 => simp [assignedSlot] <;> omega
  | 1 => simp [assignedSlot] <;> omega
  | i+2 => simp [assignedSlot] <;> omega

def physicalSlot (b L c : Nat) (s : Bool × Nat) : Nat × Nat :=
  (if s.1 then b+L else b, c+3*s.2+(if s.1 then 2 else 1))

theorem physical_slot_injective (b L c : Nat) (hL : 0<L)
    (s t : Bool × Nat) (same : physicalSlot b L c s = physicalSlot b L c t) : s=t := by
  rcases s with ⟨sb,si⟩
  rcases t with ⟨tb,ti⟩
  cases sb <;> cases tb <;> simp_all [physicalSlot]
  all_goals omega

/-- Deleting only the m chosen units preserves the compensation ledger.
Deleting all 2m-2 internal units exposes the nonnegative surplus m-2.
The count of available identities is a hypothesis, not a Lean geometry claim. -/
theorem shared_block_ledger (m a b intervals : Nat) (hm : 2≤m)
    (ha : m≤a) (hI : 2*m-2≤intervals) :
    ((intervals : Int) + (b : Int) - (a : Int) =
      ((intervals-m : Nat) : Int) + (b : Int) - ((a-m : Nat) : Int)) ∧
    ((intervals : Int) + (b : Int) - (a : Int) =
      ((intervals-(2*m-2) : Nat) : Int) + (b : Int) - ((a-m : Nat) : Int) +
        ((m-2 : Nat) : Int)) := by omega

#print axioms even_path_pairing
#print axioms side_guard_indices
#print axioms strict_rank_dependencies
#print axioms assigned_slot_injective
#print axioms assigned_slot_eligible
#print axioms physical_slot_injective
#print axioms shared_block_ledger

end SubQuorum.ProtectedSharedColumns
