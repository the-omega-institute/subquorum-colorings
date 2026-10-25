import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.CanonicalBandCoarsening

def positiveCount : List Nat → Nat
  | [] => 0
  | h::hs => (if h=0 then 0 else 1)+positiveCount hs

theorem positive_count_le_sum (xs : List Nat) : positiveCount xs ≤ xs.sum := by
  induction xs with
  | nil => simp [positiveCount]
  | cons h hs ih =>
      by_cases zero : h=0
      · simp only [positiveCount,if_pos zero,List.sum_cons]
        omega
      · have positive : 1≤h := by omega
        simp only [positiveCount,if_neg zero,List.sum_cons]
        omega

theorem positive_sum_has_child (xs : List Nat) (positive : 0<xs.sum) :
    0<positiveCount xs := by
  induction xs with
  | nil => simp at positive
  | cons h hs ih =>
      by_cases zero : h=0
      · simp only [List.sum_cons,zero,Nat.zero_add] at positive
        have ht := ih positive
        simp [positiveCount,zero,ht]
      · simp only [positiveCount,if_neg zero]
        omega

/-- Arbitrarily many nonnegative forest children: a positive parent of
capacity one contains exactly one positive child, never two. -/
theorem unique_positive_child_count (xs : List Nat) (parent : xs.sum=1) :
    positiveCount xs=1 := by
  have upper := positive_count_le_sum xs
  have lower := positive_sum_has_child xs (by omega)
  omega

theorem balanced_parent_no_positive_child (xs : List Nat) (parent : xs.sum=0) :
    positiveCount xs=0 := by
  have upper := positive_count_le_sum xs
  omega

def weightSum {α : Type} (weight : α → Nat) : List α → Nat
  | [] => 0
  | h::hs => weight h+weightSum weight hs

theorem member_weight_le_sum {α : Type} (weight : α → Nat) (xs : List α)
    (a : α) (member : a∈xs) : weight a≤weightSum weight xs := by
  induction xs with
  | nil => simp at member
  | cons h hs ih =>
      simp only [List.mem_cons] at member
      rcases member with equal | tail
      · subst a
        simp only [weightSum]
        omega
      · have bound := ih tail
        simp only [weightSum]
        omega

/-- This is identity uniqueness, not just a count of capacity values.
Nodup expresses the disjoint forest-child partition used by the adapter. -/
theorem positive_child_identity_unique {α : Type} (weight : α → Nat)
    (xs : List α) (distinct : xs.Nodup) (capacity : weightSum weight xs≤1)
    (a b : α) (ha : a∈xs) (hb : b∈xs)
    (pa : 0<weight a) (pb : 0<weight b) : a=b := by
  induction xs with
  | nil => simp at ha
  | cons h hs ih =>
      have tailDistinct := (List.nodup_cons.mp distinct).2
      have tailCapacity : weightSum weight hs≤1 := by
        simp only [weightSum] at capacity
        omega
      simp only [List.mem_cons] at ha hb
      rcases ha with ea | ha
      · rcases hb with eb | hb
        · exact ea.trans eb.symm
        · have bound := member_weight_le_sum weight hs b hb
          subst a
          simp only [weightSum] at capacity
          omega
      · rcases hb with eb | hb
        · have bound := member_weight_le_sum weight hs a ha
          subst b
          simp only [weightSum] at capacity
          omega
        · exact ih tailDistinct tailCapacity ha hb

/-- The geometric adapter supplies each parent's actual child list and
capacity identity. They force injectivity of the positive resource map. -/
theorem positive_parent_map_injective {Fine Coarse : Type}
    (rho : Fine → Coarse) (children : Coarse → List Fine)
    (capacity : ∀ c, weightSum (fun _ : Fine => 1) (children c)≤1)
    (distinct : ∀ c, (children c).Nodup)
    (contains : ∀ f, f∈children (rho f)) :
    ∀ a b, rho a=rho b → a=b := by
  intro a b equal
  apply positive_child_identity_unique (fun _ : Fine => 1) (children (rho a))
      (distinct (rho a)) (capacity (rho a)) a b (contains a)
  · rw [equal]
    exact contains b
  · omega
  · omega

/-- Resource-using primitives retain disjoint resources after transport.
A primitive may be a one-arm path or a two-source beta fork. -/
theorem pack_resource_injection {Use Fine Coarse : Type}
    (active : Use → Prop) (spend : Use → Fine) (rho : Fine → Coarse)
    (oldUnique : ∀ a b, active a → active b → spend a=spend b → a=b)
    (mapUnique : ∀ a b, rho a=rho b → a=b) :
    ∀ a b, active a → active b → rho (spend a)=rho (spend b) → a=b := by
  intro a b ha hb equal
  exact oldUnique a b ha hb (mapUnique (spend a) (spend b) equal)

theorem pack_witness_transport {Use Owner Fine Coarse : Type}
    (active : Use → Prop) (witness : Use → Owner) (spend : Use → Fine)
    (rho : Fine → Coarse) (oldSupport : Owner → Fine → Prop)
    (newSupport : Owner → Coarse → Prop)
    (oldWitness : ∀ u, active u → oldSupport (witness u) (spend u))
    (inclusion : ∀ a j, oldSupport a j → newSupport a (rho j)) :
    ∀ u, active u → newSupport (witness u) (rho (spend u)) := by
  intro u hu
  exact inclusion (witness u) (spend u) (oldWitness u hu)

theorem transported_pool_avoids_withdrawals {Fine Coarse : Type}
    (rho : Fine → Coarse) (mapUnique : ∀ a b, rho a=rho b → a=b)
    (withdrawn : Fine → Prop) (j : Fine) (kept : ¬withdrawn j) :
    ¬∃ r, withdrawn r ∧ rho r=rho j := by
  rintro ⟨r,hr,equal⟩
  exact kept ((mapUnique r j equal) ▸ hr)

def capLoss : List (Nat × Bool) → Nat
  | [] => 0
  | h::hs => h.1+capLoss hs
def hits : List (Nat × Bool) → Nat
  | [] => 0
  | h::hs => (if h.2 then 1 else 0)+hits hs
def unpaid : List (Nat × Bool) → Nat
  | [] => 0
  | h::hs => (if h.1=0 ∧ h.2=false then 1 else 0)+unpaid hs

/-- An arbitrary number of private sources: each paid source either uses
a hit guard or consumes a distinct positive cap loss. -/
theorem arbitrary_list_joint_budget (xs : List (Nat × Bool)) :
    xs.length≤capLoss xs+unpaid xs+hits xs := by
  induction xs with
  | nil => simp [capLoss,hits,unpaid]
  | cons h hs ih =>
      rcases h with ⟨loss,hit⟩
      cases hit <;> by_cases zero : loss=0 <;>
        simp [capLoss,hits,unpaid,zero] <;> omega

theorem physical_joint_budget (xs : List (Nat × Bool)) (ell joins : Nat)
    (cover : capLoss xs≤ell) (distinctCuts : hits xs≤joins) :
    xs.length≤ell+unpaid xs+joins := by
  have h := arbitrary_list_joint_budget xs
  omega

theorem sharp_quota_upper (tau size k d j : Int)
    (allT : size≤tau) (budget : k≤tau-size+d+j) :
    size≤tau-max 0 (k-d-j) := by omega

theorem sharp_quota_attainer (k d j : Nat) (threshold : d≤k) :
    let q := min j (k-d)
    let ell := k-d-q
    q≤j ∧ q+ell+d=k ∧ (ell : Int)=max 0 ((k : Int)-d-j) := by
  simp only
  omega

theorem no_point_loss_at_canonical (k : Nat) :
    k-k=0 ∧ max (0 : Int) ((k : Int)-0-k)=0 := by omega

theorem terminal_tax_monotone (d4 s oldB newB oldTax newTax : Int)
    (oldIdentity : oldTax=d4+oldB+s) (newIdentity : newTax=d4+newB+s)
    (portsRetained : newB≤oldB) : newTax≤oldTax := by omega

end SubQuorum.CanonicalBandCoarsening

#print axioms SubQuorum.CanonicalBandCoarsening.positive_count_le_sum
#print axioms SubQuorum.CanonicalBandCoarsening.positive_sum_has_child
#print axioms SubQuorum.CanonicalBandCoarsening.unique_positive_child_count
#print axioms SubQuorum.CanonicalBandCoarsening.balanced_parent_no_positive_child
#print axioms SubQuorum.CanonicalBandCoarsening.member_weight_le_sum
#print axioms SubQuorum.CanonicalBandCoarsening.positive_child_identity_unique
#print axioms SubQuorum.CanonicalBandCoarsening.positive_parent_map_injective
#print axioms SubQuorum.CanonicalBandCoarsening.pack_resource_injection
#print axioms SubQuorum.CanonicalBandCoarsening.pack_witness_transport
#print axioms SubQuorum.CanonicalBandCoarsening.transported_pool_avoids_withdrawals
#print axioms SubQuorum.CanonicalBandCoarsening.arbitrary_list_joint_budget
#print axioms SubQuorum.CanonicalBandCoarsening.physical_joint_budget
#print axioms SubQuorum.CanonicalBandCoarsening.sharp_quota_upper
#print axioms SubQuorum.CanonicalBandCoarsening.sharp_quota_attainer
#print axioms SubQuorum.CanonicalBandCoarsening.no_point_loss_at_canonical
#print axioms SubQuorum.CanonicalBandCoarsening.terminal_tax_monotone
