import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.JointGateResourceCuts

/-- Encode each payment by its cut-side gate, otherwise its original interval. -/
def cutCode {S G I : Type} (gate : S → G) (interval : S → I)
    (H : G → Prop) [DecidablePred H] (s : S) : Sum G I :=
  if H (gate s) then Sum.inl (gate s) else Sum.inr (interval s)

/-- An arbitrary cut's chosen capacities cannot be charged twice. -/
theorem cutCode_injective {S G I : Type} (gate : S → G) (interval : S → I)
    (H : G → Prop) [DecidablePred H]
    (hg : Function.Injective gate) (hi : Function.Injective interval) :
    Function.Injective (cutCode gate interval H) := by
  intro a b same
  unfold cutCode at same
  split at same <;> split at same
  · exact hg (Sum.inl.inj same)
  · cases same
  · cases same
  · exact hi (Sum.inr.inj same)

/-- Repeated original resource identities are forbidden. -/
theorem capacity_once {S R : Type} (f : S → R) (hf : Function.Injective f)
    (a b : S) (different : a ≠ b) : f a ≠ f b := by
  intro same
  exact different (hf same)

/-- Three payments cannot all cross just one gate or one interval. -/
theorem three_sources_two_capacities {G I : Type} (gate : Fin 3 → G)
    (interval : Fin 3 → I) (g : G) (j : I)
    (hg : Function.Injective gate) (hi : Function.Injective interval)
    (cover : ∀ s, gate s=g ∨ interval s=j) : False := by
  have n01 : (0 : Fin 3) ≠ 1 := by decide
  have n02 : (0 : Fin 3) ≠ 2 := by decide
  have n12 : (1 : Fin 3) ≠ 2 := by decide
  rcases cover 0 with h0 | h0
  · rcases cover 1 with h1 | h1
    · exact n01 (hg (h0.trans h1.symm))
    · rcases cover 2 with h2 | h2
      · exact n02 (hg (h0.trans h2.symm))
      · exact n12 (hi (h1.trans h2.symm))
  · rcases cover 1 with h1 | h1
    · rcases cover 2 with h2 | h2
      · exact n12 (hg (h1.trans h2.symm))
      · exact n02 (hi (h0.trans h2.symm))
    · exact n01 (hi (h0.trans h1.symm))

def Incidence (s : Fin 4) (g : Fin 5) : Prop :=
  (g.val=0 ∧ (s.val=0 ∨ s.val=1)) ∨
  (g.val=1 ∧ (s.val=1 ∨ s.val=2)) ∨
  (g.val=2 ∧ (s.val=2 ∨ s.val=0)) ∨
  ((g.val=3 ∨ g.val=4) ∧ s.val=3)

def Support (g : Fin 5) (j : Fin 4) : Prop :=
  (g.val=0 ∧ (j.val=0 ∨ j.val=1)) ∨
  ((g.val=1 ∨ g.val=2) ∧ j.val=2) ∨
  (g.val=3 ∧ (j.val=0 ∨ j.val=3)) ∨
  (g.val=4 ∧ (j.val=1 ∨ j.val=3))

instance (s : Fin 4) (g : Fin 5) : Decidable (Incidence s g) :=
  inferInstanceAs (Decidable ((_ ∧ (_ ∨ _)) ∨ (_ ∧ (_ ∨ _)) ∨
    (_ ∧ (_ ∨ _)) ∨ ((_ ∨ _) ∧ _)))
instance (g : Fin 5) (j : Fin 4) : Decidable (Support g j) :=
  inferInstanceAs (Decidable ((_ ∧ (_ ∨ _)) ∨ ((_ ∨ _) ∧ _) ∨
    (_ ∧ (_ ∨ _)) ∨ (_ ∧ (_ ∨ _))))

def sourceGate (s : Fin 4) : Fin 5 := ⟨s.val, by omega⟩

/-- All source--gate demands can independently be matched. -/
theorem source_gate_matching :
    (∀ s, Incidence s (sourceGate s)) ∧ Function.Injective sourceGate := by
  unfold Function.Injective
  decide

def intervalGate (j : Fin 4) : Fin 5 :=
  if j.val=0 then 0 else if j.val=1 then 4 else if j.val=2 then 1 else 3

/-- Four gates can independently be matched to four different intervals. -/
theorem gate_interval_matching :
    (∀ j, Support (intervalGate j) j) ∧ Function.Injective intervalGate := by
  unfold Function.Injective
  decide

def reachGate (s : Fin 4) : Fin 5 :=
  if s.val=0 ∨ s.val=1 then 0 else if s.val=2 then 1 else 3

/-- Every source reaches its distinct same-index interval. -/
theorem source_interval_reachability_matching :
    ∀ s, Incidence s (reachGate s) ∧ Support (reachGate s) s := by decide

/-- Each of the first three payments must cross gate0 or original interval z. -/
theorem first_three_cover (s : Fin 4) (g : Fin 5) (j : Fin 4)
    (hs : s.val<3) (inc : Incidence s g) (sup : Support g j) :
    g.val=0 ∨ j.val=2 := by
  unfold Incidence at inc
  unfold Support at sup
  omega

/-- Marginal matchings cannot be combined into a four-source joint packing. -/
theorem no_joint_full_payment (gate : Fin 4 → Fin 5) (interval : Fin 4 → Fin 4)
    (inc : ∀ s, Incidence s (gate s)) (sup : ∀ s, Support (gate s) (interval s))
    (hg : Function.Injective gate) (hi : Function.Injective interval) : False := by
  let embed : Fin 3 → Fin 4 := fun s => ⟨s.val, by omega⟩
  have he : Function.Injective embed := by
    intro a b h
    apply Fin.ext
    exact congrArg (fun x : Fin 4 => x.val) h
  apply three_sources_two_capacities (fun s => gate (embed s))
    (fun s => interval (embed s)) (0 : Fin 5) (2 : Fin 4)
    (fun _ _ h => he (hg h)) (fun _ _ h => he (hi h))
  intro s
  have cover := first_three_cover (embed s) (gate (embed s)) (interval (embed s))
    (by change s.val<3; exact s.isLt) (inc _) (sup _)
  rcases cover with h | h
  · exact Or.inl (Fin.ext h)
  · exact Or.inr (Fin.ext h)

def paidSource (s : Fin 3) : Fin 4 := if s.val=0 then 0 else if s.val=1 then 1 else 3
def paidGate (s : Fin 3) : Fin 5 := if s.val=0 then 0 else if s.val=1 then 1 else 4
def paidInterval (s : Fin 3) : Fin 4 := if s.val=0 then 0 else if s.val=1 then 2 else 1

/-- Explicit joint packing a->0->x, b->1->z, d->4->y attains three. -/
theorem joint_three_witness :
    (∀ s, Incidence (paidSource s) (paidGate s) ∧ Support (paidGate s) (paidInterval s)) ∧
    Function.Injective paidSource ∧ Function.Injective paidGate ∧ Function.Injective paidInterval := by
  unfold Function.Injective
  decide

/-- Actual matching and PP-band steps both reverse chessboard color. -/
inductive Strand {V : Type} (M PP : V → V → Prop) : V → V → Prop where
  | single {u v : V} : M u v → Strand M PP u v
  | extend {u v x y : V} : M u v → PP v x → Strand M PP x y → Strand M PP u y

/-- Every open alternating original strand has opposite-colored endpoints. -/
theorem strand_opposite_colors {V : Type} (M PP : V → V → Prop) (color : V → Bool)
    (mc : ∀ u v, M u v → color u ≠ color v)
    (pc : ∀ u v, PP u v → color u ≠ color v) :
    ∀ u v, Strand M PP u v → color u ≠ color v := by
  intro u v path
  induction path with
  | single edge => exact mc _ _ edge
  | @extend u v x y edge partner rest ih =>
    have a := mc u v edge
    have b := pc v x partner
    cases hu : color u <;> cases hv : color v <;> cases hx : color x <;>
      cases hy : color y <;> simp_all

/-- Gates reached from different ends of a strand have opposite BP colors. -/
theorem separate_ports_opposite_gates (u v g h : Bool)
    (ends : u ≠ v) (leftLink : u ≠ g) (rightLink : v ≠ h) : g ≠ h := by
  revert u v g h
  decide

/-- A triangle of sources using different ends at its two gates is impossible. -/
theorem no_separate_port_triangle (g h k : Bool)
    (gh : g ≠ h) (hk : h ≠ k) (kg : k ≠ g) : False := by
  cases g <;> cases h <;> cases k <;> simp_all

#print axioms strand_opposite_colors
#print axioms separate_ports_opposite_gates
#print axioms no_separate_port_triangle

#print axioms cutCode_injective
#print axioms capacity_once
#print axioms three_sources_two_capacities
#print axioms source_gate_matching
#print axioms gate_interval_matching
#print axioms source_interval_reachability_matching
#print axioms first_three_cover
#print axioms no_joint_full_payment
#print axioms joint_three_witness

end SubQuorum.JointGateResourceCuts
