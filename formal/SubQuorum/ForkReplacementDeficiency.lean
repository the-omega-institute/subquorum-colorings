import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.ForkReplacementDeficiency

/-- Ordinary local payments have values zero, one or two. A component that
pays both original sources needs a representative interval. -/
def sumPayments : List Nat → Nat
  | [] => 0
  | a :: rest => a + sumPayments rest

def doubled : List Nat → Nat
  | [] => 0
  | a :: rest => (if a=2 then 1 else 0) + doubled rest

theorem ordinary_count_bound (counts : List Nat) :
    (∀ a ∈ counts, a≤2) → sumPayments counts ≤ counts.length + doubled counts := by
  induction counts with
  | nil => simp [sumPayments,doubled]
  | cons a rest ih =>
    intro bounded
    have ha : a≤2 := bounded a (by simp)
    have tailBound : ∀ b ∈ rest, b≤2 := by
      intro b hb
      exact bounded b (by simp [hb])
    have tail := ih tailBound
    by_cases same : a=2
    · simp only [sumPayments,doubled,same,ite_true,List.length_cons]
      omega
    · simp only [sumPayments,doubled,same,ite_false,List.length_cons]
      omega

/-- One original interval payment per certificate forbids two different
old interval identities being charged to that certificate. -/
theorem one_certificate_one_interval {Resource Certificate : Type}
    (paid : Certificate → Resource) (c : Certificate) (j k : Resource)
    (first : paid c=j) (second : paid c=k) : j=k := by
  exact first.symm.trans second

/-- If all eligible arm units are blocked, and each has a unique other owner,
that other-owner map is injective. The written two-owner adapter supplies
these witnesses and the block identity. -/
theorem external_owners_injective {Resource Owner Certificate : Type}
    (eligible : Resource → Prop) (other : Resource → Owner)
    (ownerCertificate : Owner → Certificate) (paid : Certificate → Resource)
    (blocked : ∀ j, eligible j → paid (ownerCertificate (other j))=j) :
    ∀ j k, eligible j → eligible k → other j=other k → j=k := by
  intro j k hj hk same
  calc
    j = paid (ownerCertificate (other j)) := (blocked j hj).symm
    _ = paid (ownerCertificate (other k)) := by rw [same]
    _ = k := blocked k hk

theorem private_arm_unit_not_used_outside {Resource Owner : Type}
    (support : Resource → Owner → Prop) (inside : Owner → Prop)
    (usedOutside : Resource → Prop) (j : Resource)
    (noOutsideWitness : ∀ o, support j o → inside o)
    (useNeedsWitness : usedOutside j → ∃ o, support j o ∧ ¬inside o) :
    ¬usedOutside j := by
  intro used
  obtain ⟨o,supported,outside⟩ := useNeedsWitness used
  exact outside (noOutsideWitness o supported)

/-- Owner-disjoint certificates cannot each spend a different unit whose
only outside witness is this same owner. -/
theorem same_external_owner_forces_same_unit {Resource Owner Certificate : Type}
    (contains : Certificate → Owner → Prop) (paid : Certificate → Resource)
    (x : Owner) (j k : Resource)
    (ownerDisjoint : ∀ c d, contains c x → contains d x → c=d)
    (first : ∃ c, contains c x ∧ paid c=j)
    (second : ∃ c, contains c x ∧ paid c=k) : j=k := by
  obtain ⟨c,hc,pj⟩ := first
  obtain ⟨d,hd,pk⟩ := second
  have same := ownerDisjoint c d hc hd
  subst d
  exact pj.symm.trans pk

/-- A prefix ending before beta removes at least its last entry link. -/
theorem prefix_saves_one_link (arm other cutLength : Nat) (before : cutLength<arm) :
    cutLength+other+1≤arm+other := by omega

/-- Swapping different old fork intervals along an injective successor map
cannot duplicate any original interval identity. -/
theorem swapped_intervals_injective {Fork Resource : Type}
    (interval : Fork → Resource) (next : Fork → Fork)
    (differentIntervals : Function.Injective interval)
    (differentSuccessors : Function.Injective next) :
    Function.Injective (fun f => interval (next f)) := by
  intro f g same
  exact differentSuccessors (differentIntervals same)

theorem swapped_intervals_avoid_fixed {Fork Resource : Type}
    (interval : Fork → Resource) (next : Fork → Fork) (fixed : Resource → Prop)
    (oldDisjoint : ∀ f, ¬fixed (interval f)) :
    ∀ f, ¬fixed (interval (next f)) := by
  intro f
  exact oldDisjoint (next f)

theorem matching_defect_ledger (h mu delta ordinary : Int)
    (matched : delta=h-mu) (value : ordinary=h+mu) :
    ordinary=2*h-delta ∧ 2*h-ordinary=delta := by omega

theorem tree_defect_ledger (h mu trees ordinary : Int)
    (treeMatching : mu=h-trees) (value : ordinary=h+mu) :
    ordinary=2*h-trees := by omega

theorem whole_network_gap_bound (full ordinary k h mu : Int)
    (packing : full=k+2*h) (replacement : k+h+mu≤ordinary) :
    full-ordinary≤h-mu := by omega

/-- This is the arithmetic specialization of the original-alpha token
injection. Geometry, direct arms and the destination classification remain
explicit hypotheses of the written theorem. -/
theorem direct_fork_external_token_bound (forks neighbors outsideBeta blocked mixed marks : Int)
    (capacity : 4*forks≤2*neighbors+2*forks+2*outsideBeta+2*blocked+mixed+marks) :
    2*(forks-neighbors)≤2*outsideBeta+2*blocked+mixed+marks := by omega

#print axioms ordinary_count_bound
#print axioms one_certificate_one_interval
#print axioms external_owners_injective
#print axioms private_arm_unit_not_used_outside
#print axioms same_external_owner_forces_same_unit
#print axioms prefix_saves_one_link
#print axioms swapped_intervals_injective
#print axioms swapped_intervals_avoid_fixed
#print axioms matching_defect_ledger
#print axioms tree_defect_ledger
#print axioms whole_network_gap_bound
#print axioms direct_fork_external_token_bound

end SubQuorum.ForkReplacementDeficiency
