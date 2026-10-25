import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.CyclicBetaEscapeCuts

/-- A path has n source edges and n+1 gates. Omit the chosen root gate. -/
def pathGate {n : Nat} (root : Fin (n+1)) (source : Fin n) : Fin (n+1) :=
  ⟨if source.val < root.val then source.val else source.val+1, by
    split <;> omega⟩

theorem path_gate_incident {n : Nat} (root : Fin (n+1)) (source : Fin n) :
    (pathGate root source).val = source.val ∨
    (pathGate root source).val = source.val+1 := by
  by_cases below : source.val < root.val
  · exact Or.inl (by simp [pathGate, below])
  · exact Or.inr (by simp [pathGate, below])

theorem path_gate_avoids_root {n : Nat} (root : Fin (n+1)) (source : Fin n) :
    pathGate root source ≠ root := by
  intro same
  have values := congrArg Fin.val same
  simp only [pathGate] at values
  split at values <;> omega

theorem path_gate_injective {n : Nat} (root : Fin (n+1)) :
    Function.Injective (pathGate root) := by
  intro x y same
  have values := congrArg Fin.val same
  simp only [pathGate] at values
  apply Fin.ext
  split at values <;> split at values <;> omega

theorem path_gate_covers_nonroot {n : Nat} (root gate : Fin (n+1))
    (different : gate ≠ root) : ∃ source : Fin n, pathGate root source = gate := by
  have unequal : gate.val ≠ root.val := fun same => different (Fin.ext same)
  by_cases below : gate.val < root.val
  · refine ⟨⟨gate.val, by omega⟩, Fin.ext ?_⟩
    simp [pathGate, below]
  · have above : root.val < gate.val := by omega
    refine ⟨⟨gate.val-1, by omega⟩, Fin.ext ?_⟩
    simp only [pathGate]
    split <;> omega

/-- The empty one-gate gap has no source edges and is covered vacuously. -/
theorem isolated_gap_no_interval_source (source : Fin 0) : False :=
  Nat.not_lt_zero source.val source.isLt

/-- Every resource tree chooses an unused gate in that same tree.
A gap has at most one unused gate, giving the necessary tree/gap injection.
This does not assume a fixed association between the two partitions. -/
theorem unused_roots_give_tree_gap_injection {Tree Gate Gap : Type}
    (inside : Gate → Tree → Prop) (unused : Gate → Prop)
    (gap : Gate → Gap) (root : Tree → Gate)
    (rootInside : ∀ t, inside (root t) t)
    (disjointTrees : ∀ g t u, inside g t → inside g u → t=u)
    (rootUnused : ∀ t, unused (root t))
    (oneUnusedPerGap : ∀ g h, unused g → unused h → gap g=gap h → g=h) :
    Function.Injective (fun t => gap (root t)) := by
  intro t u same
  have roots := oneUnusedPerGap (root t) (root u) (rootUnused t) (rootUnused u) same
  exact disjointTrees (root t) t u (rootInside t) (roots.symm ▸ rootInside u)

/-- Distinct source-to-gate assignments followed by distinct original units
cannot reuse a unit. Only injection on actually used gates is required. -/
theorem interval_payment_injective {Source Gate Interval : Type}
    (gate : Source → Gate) (unit : Gate → Interval)
    (gateDistinct : Function.Injective gate)
    (usedUnitDistinct : ∀ s t, unit (gate s)=unit (gate t) → gate s=gate t) :
    Function.Injective (fun s => unit (gate s)) := by
  intro s t same
  exact gateDistinct (usedUnitDistinct s t same)

/-- Interval and whole-beta identities remain separate, each used once. -/
theorem joint_payment_injective {SourceI SourceB Interval Beta : Type}
    (interval : SourceI → Interval) (beta : SourceB → Beta)
    (intervalDistinct : Function.Injective interval)
    (betaDistinct : Function.Injective beta) :
    Function.Injective (fun s : Sum SourceI SourceB =>
      match s with
      | .inl x => (Sum.inl (interval x) : Sum Interval Beta)
      | .inr y => Sum.inr (beta y)) := by
  intro x y same
  cases x with
  | inl a =>
    cases y with
    | inl b => exact congrArg Sum.inl (intervalDistinct (Sum.inl.inj same))
    | inr b => cases same
  | inr a =>
    cases y with
    | inl b => cases same
    | inr b => exact congrArg Sum.inr (betaDistinct (Sum.inr.inj same))

inductive Payment where
  | gate (entrance interval : Nat)
  | beta (originalIdentity : Nat)
  deriving DecidableEq

def Payment.resource : Payment → Sum Nat Nat
  | .gate _ interval => .inl interval
  | .beta identity => .inr identity

/-- p=0 is supported only at g1; z=1 at g2,g3. Three original beta
options are at A=0,B=1,D=3. The D option is toggled, not inferred. -/
def Legal (allowD : Bool) (source : Nat) : Payment → Prop
  | .gate g u => (g=source ∨ g=(source+1)%4) ∧
      ((u=0 ∧ g=1) ∨ (u=1 ∧ (g=2 ∨ g=3)))
  | .beta b => (source=0 ∧ b=0) ∨ (source=1 ∧ b=1) ∨
      (allowD=true ∧ source=3 ∧ b=2)

instance (allowD : Bool) (s : Nat) (p : Payment) : Decidable (Legal allowD s p) :=
  by cases p <;> unfold Legal <;> infer_instance

/-- With only A/B beta exits, C and D both require the same original z. -/
theorem late_sources_require_z (source : Nat) (late : source=2 ∨ source=3)
    (payment : Payment) (legal : Legal false source payment) :
    payment.resource = Sum.inl 1 := by
  rcases late with rfl | rfl
  · cases payment with
    | gate g u =>
      simp only [Legal] at legal
      have : u=1 := by omega
      simp [Payment.resource, this]
    | beta b => simp [Legal] at legal
  · cases payment with
    | gate g u =>
      simp only [Legal] at legal
      have : u=1 := by omega
      simp [Payment.resource, this]
    | beta b => simp [Legal] at legal

theorem restricted_pair_cannot_pay_all
    (payment : Fin 4 → Payment) (legal : ∀ s, Legal false s.val (payment s))
    (distinct : Function.Injective (fun s => (payment s).resource)) : False := by
  have c := late_sources_require_z 2 (Or.inl rfl) (payment ⟨2, by omega⟩)
    (legal ⟨2, by omega⟩)
  have d := late_sources_require_z 3 (Or.inr rfl) (payment ⟨3, by omega⟩)
    (legal ⟨3, by omega⟩)
  have same := distinct (c.trans d.symm)
  have values := congrArg Fin.val same
  change (2 : Nat) = 3 at values
  omega

def repairedPayment (s : Fin 4) : Payment :=
  match s.val with
  | 0 => .beta 0
  | 1 => .gate 1 0
  | 2 => .gate 2 1
  | _ => .beta 2

theorem repaired_payment_legal : ∀ s : Fin 4, Legal true s.val (repairedPayment s) := by
  decide

theorem repaired_payment_distinct :
    Function.Injective (fun s : Fin 4 => (repairedPayment s).resource) := by
  change ∀ x y : Fin 4,
    (repairedPayment x).resource = (repairedPayment y).resource → x=y
  decide

end SubQuorum.CyclicBetaEscapeCuts

#print axioms SubQuorum.CyclicBetaEscapeCuts.path_gate_incident
#print axioms SubQuorum.CyclicBetaEscapeCuts.path_gate_avoids_root
#print axioms SubQuorum.CyclicBetaEscapeCuts.path_gate_injective
#print axioms SubQuorum.CyclicBetaEscapeCuts.path_gate_covers_nonroot
#print axioms SubQuorum.CyclicBetaEscapeCuts.isolated_gap_no_interval_source
#print axioms SubQuorum.CyclicBetaEscapeCuts.unused_roots_give_tree_gap_injection
#print axioms SubQuorum.CyclicBetaEscapeCuts.interval_payment_injective
#print axioms SubQuorum.CyclicBetaEscapeCuts.joint_payment_injective
#print axioms SubQuorum.CyclicBetaEscapeCuts.late_sources_require_z
#print axioms SubQuorum.CyclicBetaEscapeCuts.restricted_pair_cannot_pay_all
#print axioms SubQuorum.CyclicBetaEscapeCuts.repaired_payment_legal
#print axioms SubQuorum.CyclicBetaEscapeCuts.repaired_payment_distinct
