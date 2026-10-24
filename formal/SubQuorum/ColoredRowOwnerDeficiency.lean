import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.ColoredRowOwnerDeficiency

/-- On either checkerboard color, opposite-color two-tip owners cannot repeat.
The geometric hypotheses establishing the owner fibers remain written. -/
theorem owner_unique_on_color {D O C : Type} (eligible : D → Prop)
    (owner : D → O) (color : D → C) (other : D → D)
    (ownerFiber : ∀ x y, eligible x → eligible y → owner x = owner y →
      x = y ∨ y = other x)
    (opposite : ∀ x, eligible x → color (other x) ≠ color x)
    (x y : D) (hx : eligible x) (hy : eligible y)
    (sameColor : color x = color y) (sameOwner : owner x = owner y) : x = y := by
  rcases ownerFiber x y hx hy sameOwner with eq | eq
  · exact eq
  · subst y
    exact False.elim (opposite x hx sameColor.symm)

/-- An injective monochromatic terminal assignment uses different whole owners. -/
theorem monochromatic_allocation_nonreuse {A D O C : Type}
    (eligible : D → Prop) (owner : D → O) (color : D → C) (other : D → D)
    (ownerFiber : ∀ x y, eligible x → eligible y → owner x = owner y →
      x = y ∨ y = other x)
    (opposite : ∀ x, eligible x → color (other x) ≠ color x)
    (f : A → D) (injective : ∀ a b, f a = f b → a = b)
    (valid : ∀ a, eligible (f a)) (gamma : C)
    (monochromatic : ∀ a, color (f a) = gamma) :
    ∀ a b, owner (f a) = owner (f b) → a = b := by
  intro a b eq
  apply injective a b
  exact owner_unique_on_color eligible owner color other ownerFiber opposite
    (f a) (f b) (valid a) (valid b)
    ((monochromatic a).trans (monochromatic b).symm) eq

/-- A horizontal link and the following odd mixed strand flip color twice. -/
theorem two_flips_preserve_phase (first bp last : Bool)
    (horizontal : first ≠ bp) (strand : bp ≠ last) : first = last := by
  cases first <;> cases bp <;> cases last <;> simp_all

/-- A finite mixed-relay chain; only its color adapter is formalized here. -/
inductive RelayChain : Bool → Bool → Prop where
  | refl (phase : Bool) : RelayChain phase phase
  | step {first bp next last : Bool} : first ≠ bp → bp ≠ next →
      RelayChain next last → RelayChain first last

theorem relay_chain_preserves_phase {first last : Bool}
    (chain : RelayChain first last) : first = last := by
  induction chain with
  | refl _ => rfl
  | step horizontal strand _ ih =>
      exact (two_flips_preserve_phase _ _ _ horizontal strand).trans ih

/-- Exact signed consequences of the two physical color inventories. -/
theorem colored_owner_ledger (n b10 b11 b2 q0 q1 c0 c1 : Int)
    (color0 : n+c0 = b2+b10+q0) (color1 : n+c1 = b2+b11+q1) :
    n-(b2+b10+b11) = q0-c0-b11 ∧
    n-(b2+b10+b11) = q1-c1-b10 ∧
    2*(n-(b2+b10+b11)) = q0+q1-(c0+c1)-(b10+b11) := by
  omega

/-- The one-step Hall inequality after counting each beta and interval once. -/
theorem resource_cut_conversion (n b q c b1 intervals : Int)
    (ledger : 2*(n-b) = q-c-b1) :
    (n ≤ b+intervals ↔ q ≤ c+b1+2*intervals) := by
  omega

end SubQuorum.ColoredRowOwnerDeficiency

#print axioms SubQuorum.ColoredRowOwnerDeficiency.owner_unique_on_color
#print axioms SubQuorum.ColoredRowOwnerDeficiency.monochromatic_allocation_nonreuse
#print axioms SubQuorum.ColoredRowOwnerDeficiency.colored_owner_ledger
#print axioms SubQuorum.ColoredRowOwnerDeficiency.resource_cut_conversion

#print axioms SubQuorum.ColoredRowOwnerDeficiency.two_flips_preserve_phase
#print axioms SubQuorum.ColoredRowOwnerDeficiency.relay_chain_preserves_phase
