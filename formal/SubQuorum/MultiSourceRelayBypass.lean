import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.MultiSourceRelayBypass

/-- The direct/private route must cost no more than the same source's gate route. -/
def Covered {R : Type} (DA DB : R → Prop) (ca cb outCost : R → Nat)
    (entryA entryB : Nat) (r : R) : Prop :=
  (DA r ∧ ca r ≤ entryA + outCost r) ∨
  (DB r ∧ cb r ≤ entryB + outCost r)

/-- One original covered unit in a two-route collision allows a direct bypass,
possibly swapping the original source-to-resource assignments. Unit identities
and both payments remain; at most one route still needs the shared gate. -/
theorem repair_two_routes {R : Type} (DA DB output : R → Prop)
    (ca cb oc : R → Nat) (ea eb : Nat) (j k : R)
    (different : j ≠ k) (hj : output j) (hk : output k)
    (covered : Covered DA DB ca cb oc ea eb j ∨ Covered DA DB ca cb oc ea eb k) :
    ∃ ra rb,
      ((ra = j ∧ rb = k) ∨ (ra = k ∧ rb = j)) ∧ ra ≠ rb ∧
      ((DA ra ∧ output rb ∧ ca ra + eb + oc rb ≤ ea + oc j + eb + oc k) ∨
       (output ra ∧ DB rb ∧ ea + oc ra + cb rb ≤ ea + oc j + eb + oc k)) := by
  rcases covered with h | h
  · rcases h with ⟨direct, cheap⟩ | ⟨direct, cheap⟩
    · refine ⟨j,k,Or.inl ⟨rfl,rfl⟩,different,Or.inl ⟨direct,hk,?_⟩⟩
      omega
    · refine ⟨k,j,Or.inr ⟨rfl,rfl⟩,Ne.symm different,Or.inr ⟨hk,direct,?_⟩⟩
      omega
  · rcases h with ⟨direct, cheap⟩ | ⟨direct, cheap⟩
    · refine ⟨k,j,Or.inr ⟨rfl,rfl⟩,Ne.symm different,Or.inl ⟨direct,hj,?_⟩⟩
      omega
    · refine ⟨j,k,Or.inl ⟨rfl,rfl⟩,different,Or.inr ⟨hj,direct,?_⟩⟩
      omega

/-- An uncovered set with at most one identity cannot contain a collision pair. -/
theorem one_uncovered_implies_pair_covered {R : Type} (cover : R → Prop)
    (unique : ∀ r s, ¬ cover r → ¬ cover s → r = s)
    (j k : R) (different : j ≠ k) : cover j ∨ cover k := by
  classical
  by_cases hj : cover j
  · exact Or.inl hj
  · by_cases hk : cover k
    · exact Or.inr hk
    · exact False.elim (different (unique j k hj hk))

/-- Two different overloaded module labels cannot share a selected source. -/
theorem overloaded_source_sets_disjoint {S G : Type} (label : S → G)
    (Pg Ph : S → Prop) (g h : G) (different : g ≠ h)
    (hg : ∀ s, Pg s → label s = g) (hh : ∀ s, Ph s → label s = h) :
    ∀ s, ¬ (Pg s ∧ Ph s) := by
  intro s both
  exact different ((hg s both.1).symm.trans (hh s both.2))

theorem one_gate_forbids_two_loads (a b : Nat)
    (capacity : a+b ≤ 1) (ha : 1 ≤ a) (hb : 1 ≤ b) : False := by omega

/-- Generic finite normalization: the geometric/route adapter must supply each
legal step, resource preservation, payment preservation, and cost monotonicity. -/
theorem finite_normalization {X : Type} (bad payment cost : X → Nat)
    (step : X → X → Prop)
    (progress : ∀ x, bad x ≠ 0 → ∃ y, step x y)
    (decrease : ∀ x y, step x y → bad y < bad x)
    (same_payment : ∀ x y, step x y → payment y = payment x)
    (no_cost_increase : ∀ x y, step x y → cost y ≤ cost x) :
    ∀ x, ∃ y, bad y = 0 ∧ payment y = payment x ∧ cost y ≤ cost x := by
  have inductionClaim : ∀ n, ∀ x, bad x = n →
      ∃ y, bad y = 0 ∧ payment y = payment x ∧ cost y ≤ cost x := by
    intro n
    induction n using Nat.strongRecOn with
    | ind n ih =>
      intro x hx
      by_cases hz : bad x = 0
      · exact ⟨x,hz,rfl,Nat.le_refl _⟩
      · obtain ⟨z,hs⟩ := progress x hz
        have lower : bad z < n := by
          have h := decrease x z hs
          omega
        obtain ⟨y,hy,hp,hc⟩ := ih (bad z) lower z rfl
        exact ⟨y,hy,hp.trans (same_payment x z hs),
          Nat.le_trans hc (no_cost_increase x z hs)⟩
  intro x
  exact inductionClaim (bad x) x rfl

/-- Explicit deficiency correction; no original resource can be credited twice. -/
theorem deficiency_bound (sources projection paid defect : Nat)
    (projection_le : projection ≤ sources) (certificate : projection ≤ paid+defect) :
    sources-paid ≤ (sources-projection)+defect := by omega

theorem half_projection_bound (projection defect : Nat)
    (disjoint_pairs : 2*defect ≤ projection) :
    (projection+1)/2 ≤ projection-defect := by omega

theorem capacity_two_projection_bound (projection defect : Nat)
    (disjoint_triples : 3*defect ≤ projection) :
    (2*projection+2)/3 ≤ projection-defect := by omega

theorem joint_rank_not_sum (badGates sourceRank unitRank jointRank : Nat)
    (h1 : jointRank ≤ badGates) (h2 : jointRank ≤ sourceRank)
    (h3 : jointRank ≤ unitRank) :
    jointRank ≤ min badGates (min sourceRank unitRank) := by omega

#print axioms repair_two_routes
#print axioms one_uncovered_implies_pair_covered
#print axioms overloaded_source_sets_disjoint
#print axioms one_gate_forbids_two_loads
#print axioms finite_normalization
#print axioms deficiency_bound
#print axioms half_projection_bound
#print axioms capacity_two_projection_bound
#print axioms joint_rank_not_sum

end SubQuorum.MultiSourceRelayBypass
