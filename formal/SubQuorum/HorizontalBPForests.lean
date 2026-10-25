import Lean.Elab.Tactic.Omega

set_option autoImplicit false
namespace SubQuorum.HorizontalBPForests

/-- An arbitrary finite directed path, with its initial root retained. -/
inductive RootPath {V : Type} (E : V → V → Prop) (root : V) : V → Prop where
  | refl : RootPath E root root
  | tail {u v : V} : RootPath E root u → E u v → RootPath E root v

/-- Unique incoming H edges imply unique roots, without a path-length bound. -/
theorem roots_unique {V : Type} {E : V → V → Prop}
    (oneParent : ∀ a b v, E a v → E b v → a=b)
    {r s v : V}
    (rRoot : ∀ x, ¬ E x r) (sRoot : ∀ x, ¬ E x s)
    (p : RootPath E r v) (q : RootPath E s v) : r=s := by
  induction p with
  | refl =>
    cases q with
    | refl => rfl
    | tail _ last => exact False.elim (rRoot _ last)
  | @tail u v priorPath last ih =>
    cases q with
    | refl => exact False.elim (sRoot _ last)
    | @tail w _ other lastOther =>
      have same : u=w := oneParent u w v last lastOther
      subst w
      exact ih other

/-- Descendants of different roots cannot be the same physical mixed owner. -/
theorem different_root_descendants_disjoint {V : Type} {E : V → V → Prop}
    (oneParent : ∀ a b v, E a v → E b v → a=b)
    {r s v : V} (different : r≠s)
    (rRoot : ∀ x, ¬ E x r) (sRoot : ∀ x, ¬ E x s)
    (p : RootPath E r v) : ¬ RootPath E s v := by
  intro q
  exact different (roots_unique oneParent rRoot sRoot p q)

/-- A path into a closed region would need a first entry edge. -/
theorem no_path_into_closed_region {V : Type} {E : V → V → Prop}
    (inside : V → Prop)
    (closed : ∀ a b, E a b → inside b → inside a)
    {r v : V} (outside : ¬ inside r) (p : RootPath E r v) : ¬ inside v := by
  induction p with
  | refl => exact outside
  | tail _ last ih =>
    intro hv
    exact ih (closed _ _ last hv)

/-- The finite cycle proof supplies each cycle vertex's cyclic predecessor. -/
theorem cycle_region_incoming_closed {V : Type} {E : V → V → Prop}
    (oneParent : ∀ a b v, E a v → E b v → a=b)
    (inside : V → Prop)
    (cyclicPredecessor : ∀ v, inside v → ∃ u, inside u ∧ E u v) :
    ∀ a b, E a b → inside b → inside a := by
  intro a b edge hb
  obtain ⟨u,hu,previous⟩ := cyclicPredecessor b hb
  have same : a=u := oneParent a u b edge previous
  exact same.symm ▸ hu

/-- In one physical row the actual horizontal mate consumes one BP side. -/
theorem horizontal_bp_other_neighbour (c u : Int)
    (adjacent : u+1=c ∨ u=c+1) (notActualMate : u≠c+1) : u=c-1 := by omega

/-- A unique-parent depth certificate is monotone on arbitrary-length paths. -/
theorem path_depth_monotone {V : Type} {E : V → V → Prop}
    (depth : V → Nat) (edgeDepth : ∀ a b, E a b → depth b=depth a+1)
    {r v : V} (p : RootPath E r v) : depth r ≤ depth v := by
  induction p with
  | refl => exact Nat.le_refl _
  | tail _ last ih =>
    have step := edgeDepth _ _ last
    omega

/-- Union-of-sink matching adds to the already disjoint serial baseline. -/
theorem serial_matching_payment (N q nu : Nat) (qle : q≤N) (nule : nu≤q) :
    N-(N-q+nu)=q-nu := by omega

theorem serial_matching_link_count (N q tau : Nat) (qle : q≤N) :
    N+(N-q)+tau=2*N-q+tau := by omega

#print axioms roots_unique
#print axioms different_root_descendants_disjoint
#print axioms no_path_into_closed_region
#print axioms cycle_region_incoming_closed
#print axioms horizontal_bp_other_neighbour
#print axioms path_depth_monotone
#print axioms serial_matching_payment
#print axioms serial_matching_link_count
end SubQuorum.HorizontalBPForests
