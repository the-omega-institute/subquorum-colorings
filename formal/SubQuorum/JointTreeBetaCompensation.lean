import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.JointTreeBetaCompensation

/-- Edges are original interval identities along a simple path of n edges.
Before rerooting edge i pays vertex i+1; afterwards it pays vertex i.
The final vertex receives the distinct whole-beta resource. -/
def oldOwner {n : Nat} (e : Fin n) : Fin (n+1) := ⟨e.val+1, by omega⟩
def newOwner {n : Nat} (e : Fin n) : Fin (n+1) := ⟨e.val, by omega⟩

theorem old_owners_injective {n : Nat} :
    Function.Injective (@oldOwner n) := by
  intro e f same
  have values := congrArg Fin.val same
  apply Fin.ext
  simp only [oldOwner] at values
  omega

theorem new_owners_injective {n : Nat} :
    Function.Injective (@newOwner n) := by
  intro e f same
  have values := congrArg (fun v : Fin (n+1) => v.val) same
  exact Fin.ext values

theorem old_paid_domain {n : Nat} (v : Fin (n+1)) :
    (∃ e : Fin n, oldOwner e = v) ↔ 0 < v.val := by
  constructor
  · rintro ⟨e, equal⟩
    have values := congrArg Fin.val equal
    simp only [oldOwner] at values
    omega
  · intro positive
    exact ⟨⟨v.val-1, by omega⟩, Fin.ext (by simp only [oldOwner]; omega)⟩

theorem new_paid_domain {n : Nat} (v : Fin (n+1)) :
    (∃ e : Fin n, newOwner e = v) ↔ v.val < n := by
  constructor
  · rintro ⟨e, equal⟩
    have values := congrArg Fin.val equal
    simp only [newOwner] at values
    omega
  · intro below
    exact ⟨⟨v.val, below⟩, Fin.ext rfl⟩

/-- Every path vertex is paid after rerooting: by an old edge or the beta. -/
theorem every_vertex_paid_after {n : Nat} (v : Fin (n+1)) :
    (∃ e : Fin n, newOwner e = v) ∨ v.val = n := by
  by_cases below : v.val < n
  · exact Or.inl ((new_paid_domain v).mpr below)
  · exact Or.inr (by omega)

/-- Given physical incidence at both ends, either orientation is valid. -/
theorem both_orientations_incident {n : Nat} {Demand Resource : Type}
    (vertex : Fin (n+1) → Demand) (resource : Fin n → Resource)
    (incident : Resource → Demand → Prop)
    (ends : ∀ e, incident (resource e) (vertex (newOwner e)) ∧
                       incident (resource e) (vertex (oldOwner e))) :
    (∀ e, incident (resource e) (vertex (oldOwner e))) ∧
    (∀ e, incident (resource e) (vertex (newOwner e))) := by
  exact ⟨fun e => (ends e).2, fun e => (ends e).1⟩

/-- Both resource-indexed assignments use precisely the same original units. -/
theorem original_resource_set_preserved {n : Nat} {Demand Resource : Type}
    (vertex : Fin (n+1) → Demand) (resource : Fin n → Resource) (j : Resource) :
    (∃ e, resource e = j ∧ ∃ v, vertex (oldOwner e) = v) ↔
    (∃ e, resource e = j ∧ ∃ v, vertex (newOwner e) = v) := by
  constructor
  · rintro ⟨e, identity, _⟩
    exact ⟨e, identity, vertex (newOwner e), rfl⟩
  · rintro ⟨e, identity, _⟩
    exact ⟨e, identity, vertex (oldOwner e), rfl⟩

/-- A simple physical path has no demand reuse in either orientation. -/
theorem physical_owners_injective {n : Nat} {Demand : Type}
    (vertex : Fin (n+1) → Demand) (simple : Function.Injective vertex) :
    Function.Injective (fun e : Fin n => vertex (oldOwner e)) ∧
    Function.Injective (fun e : Fin n => vertex (newOwner e)) := by
  exact ⟨fun _ _ h => old_owners_injective (simple h),
         fun _ _ h => new_owners_injective (simple h)⟩

/-- Each of the n old path owners loses its previous interval assignment.
If it remains interval-paid, its new original interval is different. -/
theorem every_old_path_assignment_changes {n : Nat} {Demand Resource : Type}
    (vertex : Fin (n+1) → Demand) (resource : Fin n → Resource)
    (simple : Function.Injective vertex) (distinct : Function.Injective resource)
    (e f : Fin n) (sameDemand : vertex (oldOwner e) = vertex (newOwner f)) :
    resource e ≠ resource f := by
  intro sameResource
  have ef := distinct sameResource
  have owners := simple sameDemand
  have values := congrArg Fin.val owners
  simp only [oldOwner, newOwner] at values
  subst f
  omega

/-- The beta-paid new root cannot also be paid by a path interval. -/
theorem beta_root_disjoint {n : Nat} {Demand : Type}
    (vertex : Fin (n+1) → Demand) (simple : Function.Injective vertex)
    (e : Fin n) : vertex ⟨n, by omega⟩ ≠ vertex (newOwner e) := by
  intro equal
  have values := congrArg Fin.val (simple equal)
  simp only [newOwner] at values
  omega

/-- Off-path allocations remain fixed and cannot collide with the new path.
The disjointness hypothesis is supplied by the simple-tree path decomposition. -/
theorem merge_unchanged_off_path {n : Nat} {Demand OtherResource : Type}
    (vertex : Fin (n+1) → Demand) (simple : Function.Injective vertex)
    (outside : OtherResource → Demand) (outsideInjective : Function.Injective outside)
    (offPath : ∀ e v, outside e ≠ vertex v) :
    Function.Injective (Sum.elim (fun e : Fin n => vertex (newOwner e)) outside) := by
  intro first second same
  cases first with
  | inl e =>
    cases second with
    | inl f =>
      exact congrArg Sum.inl (new_owners_injective (simple same))
    | inr f => exact False.elim (offPath f (newOwner e) same.symm)
  | inr e =>
    cases second with
    | inl f => exact False.elim (offPath e (newOwner f) same)
    | inr f => exact congrArg Sum.inr (outsideInjective same)

/-- A whole beta is a separate typed resource, never an extra interval credit. -/
theorem beta_and_path_resources_disjoint {Interval Beta : Type}
    (interval : Interval) (beta : Beta) :
    (Sum.inl interval : Sum Interval Beta) ≠ Sum.inr beta := by
  intro impossible
  cases impossible

theorem joint_ledger (surplus boundary unused beta defect matched : Int)
    (original : surplus - boundary = unused + beta - defect) :
    surplus - boundary = unused + (beta-matched) - (defect-matched) := by
  omega

theorem saturated_tree_compensation (surplus boundary unused beta matched : Int)
    (ledger : surplus - boundary = unused + beta - matched)
    (spare : 0 ≤ unused) (distinctBetaBound : matched ≤ beta) :
    boundary ≤ surplus := by omega

end SubQuorum.JointTreeBetaCompensation

#print axioms SubQuorum.JointTreeBetaCompensation.old_owners_injective
#print axioms SubQuorum.JointTreeBetaCompensation.new_owners_injective
#print axioms SubQuorum.JointTreeBetaCompensation.old_paid_domain
#print axioms SubQuorum.JointTreeBetaCompensation.new_paid_domain
#print axioms SubQuorum.JointTreeBetaCompensation.every_vertex_paid_after
#print axioms SubQuorum.JointTreeBetaCompensation.both_orientations_incident
#print axioms SubQuorum.JointTreeBetaCompensation.original_resource_set_preserved
#print axioms SubQuorum.JointTreeBetaCompensation.physical_owners_injective
#print axioms SubQuorum.JointTreeBetaCompensation.every_old_path_assignment_changes
#print axioms SubQuorum.JointTreeBetaCompensation.beta_root_disjoint
#print axioms SubQuorum.JointTreeBetaCompensation.merge_unchanged_off_path
#print axioms SubQuorum.JointTreeBetaCompensation.beta_and_path_resources_disjoint
#print axioms SubQuorum.JointTreeBetaCompensation.joint_ledger
#print axioms SubQuorum.JointTreeBetaCompensation.saturated_tree_compensation
