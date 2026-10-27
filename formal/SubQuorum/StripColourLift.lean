import Lean.Elab.Tactic.Omega

/-! Word-level normalization for same-colour domino tilings of a two-column
ladder. The geometric extraction of the rung / paired-vertical tiling grammar
from a full grid matching is written in STRIP_TREE_PHYSICAL_COMPENSATION.md.
No global forest algorithm or grid embedding is asserted here. -/
set_option autoImplicit false
namespace SubQuorum.StripColourLift

variable {α : Type}

inductive Physical : List (α × α) → Prop where
  | nil : Physical []
  | rung (a : α) {tail : List (α × α)} : Physical tail → Physical ((a,a)::tail)
  | vertical (a b : α) {tail : List (α × α)} :
      Physical tail → Physical ((a,b)::(a,b)::tail)

inductive Canonical : List (α × α) → Prop where
  | nil : Canonical []
  | mono (a : α) {tail : List (α × α)} : Canonical tail → Canonical ((a,a)::tail)
  | mixed (a b : α) {tail : List (α × α)} :
      a ≠ b → Canonical tail → Canonical ((a,b)::(a,b)::tail)

theorem physical_to_canonical [DecidableEq α] {word : List (α × α)}
    (h : Physical word) : Canonical word := by
  induction h with
  | nil => exact Canonical.nil
  | rung a _ ih => exact Canonical.mono a ih
  | vertical a b _ ih =>
      by_cases hab : a = b
      · subst b; exact Canonical.mono a (Canonical.mono a ih)
      · exact Canonical.mixed a b hab ih

theorem canonical_to_physical {word : List (α × α)}
    (h : Canonical word) : Physical word := by
  induction h with
  | nil => exact Physical.nil
  | mono a _ ih => exact Physical.rung a ih
  | mixed a b _ _ ih => exact Physical.vertical a b ih

def accepts [DecidableEq α] : List (α × α) → Prop
  | [] => True
  | (a,b)::tail => if a=b then accepts tail else
      match tail with
      | [] => False
      | (c,d)::rest => a=c ∧ b=d ∧ accepts rest

private theorem accepts_cons [DecidableEq α] (a b : α) (tail : List (α × α)) :
    accepts ((a,b)::tail) = (if a=b then accepts tail else
      match tail with
      | [] => False
      | (c,d)::rest => a=c ∧ b=d ∧ accepts rest) := by
  cases tail with
  | nil => rfl
  | cons row rest => cases row; rfl

theorem canonical_accepts [DecidableEq α] {word : List (α × α)}
    (h : Canonical word) : accepts word := by
  induction h with
  | nil => trivial
  | mono a _ ih => simpa [accepts_cons] using ih
  | mixed a b hab _ ih => simp [accepts_cons, hab, ih]

theorem accepts_canonical [DecidableEq α] (word : List (α × α)) :
    accepts word → Canonical word := by
  match word with
  | [] => exact fun _ => Canonical.nil
  | (a,b)::tail =>
    intro h
    by_cases hab : a=b
    · subst b
      have ht : accepts tail := by simpa [accepts_cons] using h
      exact Canonical.mono a (accepts_canonical tail ht)
    · cases tail with
      | nil => simp [accepts_cons, hab] at h
      | cons row rest =>
        obtain ⟨c,d⟩ := row
        have hr : a=c ∧ b=d ∧ accepts rest := by simpa [accepts_cons, hab] using h
        obtain ⟨hac,hbd,ht⟩ := hr
        subst c; subst d
        exact Canonical.mixed a b hab (accepts_canonical rest ht)
termination_by word.length

theorem accepts_iff_physical [DecidableEq α] (word : List (α × α)) :
    accepts word ↔ Physical word := by
  constructor
  · intro h; exact canonical_to_physical (accepts_canonical word h)
  · intro h; exact canonical_accepts (physical_to_canonical h)

end SubQuorum.StripColourLift

#print axioms SubQuorum.StripColourLift.physical_to_canonical
#print axioms SubQuorum.StripColourLift.canonical_to_physical
#print axioms SubQuorum.StripColourLift.canonical_accepts
#print axioms SubQuorum.StripColourLift.accepts_canonical
#print axioms SubQuorum.StripColourLift.accepts_iff_physical
