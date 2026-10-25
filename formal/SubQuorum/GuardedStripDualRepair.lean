import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.GuardedStripDualRepair

abbrev Pred (α : Type) := α → Prop

def Union {α : Type} (F G : Pred α) : Pred α := fun a => F a ∨ G a
def Inter {α : Type} (F G : Pred α) : Pred α := fun a => F a ∧ G a
def Compl {α : Type} (F : Pred α) : Pred α := fun a => ¬F a

def Dual {α : Type} (card rank : Pred α → Int) (wholeRank : Int) (F : Pred α) : Int :=
  card F+rank (Compl F)-wholeRank

theorem complement_union {α : Type} (F G : Pred α) :
    Compl (Union F G)=Inter (Compl F) (Compl G) := by
  funext a
  apply propext
  simp [Compl,Union,Inter]

theorem complement_inter {α : Type} (F G : Pred α) :
    Compl (Inter F G)=Union (Compl F) (Compl G) := by
  classical
  funext a
  apply propext
  by_cases hf : F a <;> simp [Compl,Union,Inter,hf]

/-- The exact standard dual rank submodularity calculation. The physical
network-to-source-rank adapter and finite cardinality axioms are explicit
hypotheses, rather than inferred from numerical examples. -/
theorem dual_submodular {α : Type} (card rank : Pred α → Int) (wholeRank : Int)
    (cardModular : ∀ F G, card F+card G=card (Union F G)+card (Inter F G))
    (rankSubmodular : ∀ F G, rank F+rank G≥rank (Union F G)+rank (Inter F G))
    (F G : Pred α) :
    Dual card rank wholeRank F+Dual card rank wholeRank G ≥
      Dual card rank wholeRank (Union F G)+Dual card rank wholeRank (Inter F G) := by
  have cardinal := cardModular F G
  have submod := rankSubmodular (Compl F) (Compl G)
  rw [←complement_inter,←complement_union] at submod
  unfold Dual
  omega

theorem dual_single_increment (cardF cardG rankComplementF rankComplementG wholeRank : Int)
    (oneNew : cardG=cardF+1)
    (rankDrop : rankComplementG≤rankComplementF)
    (unitDrop : rankComplementF≤rankComplementG+1) :
    0≤(cardG+rankComplementG-wholeRank)-(cardF+rankComplementF-wholeRank) ∧
    (cardG+rankComplementG-wholeRank)-(cardF+rankComplementF-wholeRank)≤1 := by omega

/-- Diminishing returns makes any zero marginal persist in a larger pool. -/
theorem zero_marginal_persists (valueF valueG valueFe valueGe : Int)
    (zeroAtF : valueFe=valueF) (nonnegativeAtG : valueG≤valueGe)
    (diminishing : valueGe+valueF≤valueFe+valueG) : valueGe=valueG := by omega

def Insert {α : Type} (a : α) (F : Pred α) : Pred α := fun x => x=a ∨ F x

def Extend {α : Type} (F : Pred α) : List α → Pred α
  | [] => F
  | a::xs => Insert a (Extend F xs)

theorem included_extension {α : Type} (F : Pred α) (xs : List α) :
    ∀ a, F a → Extend F xs a := by
  induction xs with
  | nil => exact fun _ h => h
  | cons a xs ih => exact fun x h => Or.inr (ih x h)

/-- Arbitrarily many individually zero marginal switches have zero joint
benefit, under the explicit optimized-rank hypotheses. -/
theorem no_joint_gain {α : Type} (gain : Pred α → Int)
    (mono : ∀ F G, (∀ a, F a → G a) → gain F≤gain G)
    (diminishing : ∀ F G a, (∀ x, F x → G x) →
      gain (Insert a G)+gain F≤gain (Insert a F)+gain G)
    (F : Pred α) (xs : List α)
    (zero : ∀ a, a∈xs → gain (Insert a F)=gain F) : gain (Extend F xs)=gain F := by
  induction xs with
  | nil => rfl
  | cons a xs ih =>
    have tail := ih (fun x hx => zero x (List.mem_cons_of_mem a hx))
    have first := zero a (by simp)
    have low := mono (Extend F xs) (Insert a (Extend F xs)) (fun _ h => Or.inr h)
    have high := diminishing F (Extend F xs) a (included_extension F xs)
    change gain (Insert a (Extend F xs))=gain F
    omega

theorem full_payment_complement_iff (sources flipped rankComplement : Nat)
    (subsetCount : flipped≤sources) :
    flipped+rankComplement=sources ↔ rankComplement=sources-flipped := by omega

theorem minimum_full_switches (sources oldValue switches newValue : Nat)
    (full : newValue=sources) (unitBound : newValue≤oldValue+switches) :
    sources-oldValue≤switches := by omega

theorem component_representatives_injective {C A : Type} (representative : C → A)
    (belongs : A → C → Prop)
    (chosenMember : ∀ c, belongs (representative c) c)
    (uniqueComponent : ∀ a c d, belongs a c → belongs a d → c=d)
    (c d : C) (same : representative c=representative d) : c=d := by
  apply uniqueComponent (representative c) c d (chosenMember c)
  exact same ▸ chosenMember d

theorem component_gain_not_additive (oldValue newFirst newSecond newBoth : Int)
    (first : newFirst=oldValue+1) (second : newSecond=oldValue+1)
    (sharedDefect : newBoth=oldValue+1) :
    (newFirst-oldValue)+(newSecond-oldValue)=2 ∧ newBoth-oldValue=1 := by omega

theorem unchanged_slack_deficit_improvement (slack oldDeficit newDeficit gain : Int)
    (repair : newDeficit=oldDeficit-gain) :
    slack+newDeficit=slack+oldDeficit-gain := by omega

theorem stacked_slack_count (n q opened : Int) :
    6*(q*(2*n+4)-2) - (q*(9*n+5)+2*(q-1)-opened) - q*(3*n+5) =
      12*q-10+opened := by
  simp only [Int.mul_add,Int.mul_sub,Int.mul_left_comm q]
  omega

#print axioms complement_union
#print axioms complement_inter
#print axioms dual_submodular
#print axioms dual_single_increment
#print axioms zero_marginal_persists
#print axioms included_extension
#print axioms no_joint_gain
#print axioms full_payment_complement_iff
#print axioms minimum_full_switches
#print axioms component_representatives_injective
#print axioms component_gain_not_additive
#print axioms unchanged_slack_deficit_improvement
#print axioms stacked_slack_count

end SubQuorum.GuardedStripDualRepair
