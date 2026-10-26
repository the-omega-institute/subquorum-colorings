set_option autoImplicit false

namespace SubQuorum.PivotSupportRepair

variable {O R : Type}

/-- Keep every old witness except an affected witness without a reservation. -/
def Retained (paid : O → Prop) (affected : R → Prop) (old : O → R)
    (backed : O → Prop) (o : O) : Prop :=
  paid o ∧ (affected (old o) → backed o)

def repaired (affected : R → Prop) [DecidablePred affected]
    (old reserve : O → R) (o : O) : R :=
  if affected (old o) then reserve o else old o

/-- A simultaneous repair keeps the incidence of every retained witness. -/
theorem repair_valid (paid : O → Prop) (affected : R → Prop)
    [DecidablePred affected] (old reserve : O → R) (backed : O → Prop)
    (newSupport : O → R → Prop)
    (unchanged : ∀ o, paid o → ¬ affected (old o) → newSupport o (old o))
    (reserved : ∀ o, paid o → affected (old o) → backed o →
      newSupport o (reserve o)) :
    ∀ o, Retained paid affected old backed o →
      newSupport o (repaired affected old reserve o) := by
  intro o ho
  by_cases ha : affected (old o)
  · simp only [repaired, if_pos ha]
    exact reserved o ho.1 ha (ho.2 ha)
  · simp only [repaired, if_neg ha]
    exact unchanged o ho.1 ha

/-- Reservations lie inside the affected pool, while untouched assignments
lie outside it. Distinct backed witnesses get distinct reservations.
Thus no retained old assignment and new reservation can be spent twice. -/
theorem repair_injective (paid : O → Prop) (affected : R → Prop)
    [DecidablePred affected] (old reserve : O → R) (backed : O → Prop)
    (oldInjective : ∀ o p, paid o → paid p → old o = old p → o = p)
    (reserveAffected : ∀ o, paid o → affected (old o) → backed o →
      affected (reserve o))
    (reserveInjective : ∀ o p, backed o → backed p → reserve o = reserve p → o = p) :
    ∀ o p, Retained paid affected old backed o →
      Retained paid affected old backed p →
      repaired affected old reserve o = repaired affected old reserve p → o = p := by
  intro o p ho hp he
  by_cases ha : affected (old o)
  · by_cases hb : affected (old p)
    · simp only [repaired, if_pos ha, if_pos hb] at he
      exact reserveInjective o p (ho.2 ha) (hp.2 hb) he
    · simp only [repaired, if_pos ha, if_neg hb] at he
      exact False.elim (hb (he ▸ reserveAffected o ho.1 ha (ho.2 ha)))
  · by_cases hb : affected (old p)
    · simp only [repaired, if_neg ha, if_pos hb] at he
      exact False.elim (ha (he.symm ▸ reserveAffected p hp.1 hb (hp.2 hb)))
    · simp only [repaired, if_neg ha, if_neg hb] at he
      exact oldInjective o p ho.1 hp.1 he

/-- A dropped old witness lies both in the unbacked-owner set and, through
its injective old assignment, in the affected-resource set. -/
theorem lost_is_unbacked_and_affected (paid : O → Prop) (affected : R → Prop)
    [DecidablePred affected] (old : O → R) (backed : O → Prop)
    (o : O) (hp : paid o) (lost : ¬ Retained paid affected old backed o) :
    affected (old o) ∧ ¬ backed o := by
  by_cases ha : affected (old o)
  · refine ⟨ha, ?_⟩
    intro hb
    exact lost ⟨hp, fun _ => hb⟩
  · exact False.elim (lost ⟨hp, fun h => False.elim (ha h)⟩)

end SubQuorum.PivotSupportRepair

#print axioms SubQuorum.PivotSupportRepair.repair_valid
#print axioms SubQuorum.PivotSupportRepair.repair_injective
#print axioms SubQuorum.PivotSupportRepair.lost_is_unbacked_and_affected
