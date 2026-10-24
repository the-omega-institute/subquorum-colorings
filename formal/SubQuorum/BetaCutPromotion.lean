import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.BetaCutPromotion

/-- Beta i supports adjacent original intervals i,i+1. Avoid any chosen hole
without assigning the same interval twice, for every finite chain length. -/
def avoidHole (q : Nat) (hole : Fin (q+1)) (i : Fin q) : Fin (q+1) :=
  ⟨if i.val<hole.val then i.val else i.val+1, by split <;> omega⟩

theorem avoidHole_injective (q : Nat) (hole : Fin (q+1)) :
    Function.Injective (avoidHole q hole) := by
  intro i j same
  have values := congrArg Fin.val same
  simp only [avoidHole] at values
  apply Fin.ext
  split at values <;> split at values <;> omega

theorem avoidHole_not_deleted (q : Nat) (hole : Fin (q+1)) (i : Fin q) :
    avoidHole q hole i≠hole := by
  intro same
  have values := congrArg Fin.val same
  simp only [avoidHole] at values
  split at values <;> omega

theorem avoidHole_is_supported (q : Nat) (hole : Fin (q+1)) (i : Fin q) :
    (avoidHole q hole i).val=i.val ∨ (avoidHole q hole i).val=i.val+1 := by
  simp only [avoidHole]
  split <;> simp

def oldAllocation (q : Nat) (i : Fin q) : Fin (q+1) := ⟨i.val, by omega⟩

theorem oldAllocation_range (q : Nat) (j : Fin (q+1)) :
    (∃ i, oldAllocation q i=j) ↔ j.val<q := by
  constructor
  · rintro ⟨i, same⟩
    have values := congrArg Fin.val same
    simp only [oldAllocation] at values
    omega
  · intro below
    refine ⟨⟨j.val,below⟩, ?_⟩
    apply Fin.ext
    rfl

/-- Even with q separate double-entry beta receivers and deletion-robust
Hall witnesses, exactly one original interval is globally unused. -/
theorem only_one_unused_interval (q : Nat) (j : Fin (q+1)) :
    (¬∃ i, oldAllocation q i=j) ↔ j.val=q := by
  rw [oldAllocation_range]
  omega

/-- Promoting s single-entry and d double-entry beta bodies changes the
cut by newIntervals-d. Strict maximal-source-side optimality gives surplus. -/
theorem strict_joint_promotion_ledger (oldCut single double newIntervals : Int)
    (strict : oldCut < oldCut-(single+2*double)+(single+double)+newIntervals) :
    double+1≤newIntervals := by omega

#print axioms avoidHole_injective
#print axioms avoidHole_not_deleted
#print axioms avoidHole_is_supported
#print axioms oldAllocation_range
#print axioms only_one_unused_interval
#print axioms strict_joint_promotion_ledger

end SubQuorum.BetaCutPromotion
