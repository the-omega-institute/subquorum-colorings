import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.OneSidedResourceAllocation

theorem resource_has_only_two_owners {Demand Resource : Type}
    (incident : Resource → Demand → Prop)
    (capacity : ∀ resource first second third,
      incident resource first → incident resource second → incident resource third →
      first = second ∨ first = third ∨ second = third)
    {resource : Resource} {child parent other : Demand}
    (childIncident : incident resource child) (parentIncident : incident resource parent)
    (distinct : child ≠ parent) (otherIncident : incident resource other) :
    other = child ∨ other = parent := by
  have alternatives := capacity resource child parent other childIncident parentIncident otherIncident
  rcases alternatives with equal | equal | equal
  · exact False.elim (distinct equal)
  · exact Or.inl equal.symm
  · exact Or.inr equal.symm

theorem decreasing_parent_resources_are_injective {Demand Resource : Type}
    (incident : Resource → Demand → Prop)
    (capacity : ∀ resource first second third,
      incident resource first → incident resource second → incident resource third →
      first = second ∨ first = third ∨ second = third)
    (rank : Demand → Nat) (parent : Demand → Demand) (pay : Demand → Resource)
    (childIncident : ∀ child, 0 < rank child → incident (pay child) child)
    (parentIncident : ∀ child, 0 < rank child → incident (pay child) (parent child))
    (decrease : ∀ child, 0 < rank child → rank (parent child) < rank child)
    {first second : Demand} (firstPositive : 0 < rank first)
    (secondPositive : 0 < rank second) (sameResource : pay first = pay second) :
    first = second := by
  by_cases equal : first = second
  · exact equal
  · have firstDecrease := decrease first firstPositive
    have secondDecrease := decrease second secondPositive
    have firstDistinct : first ≠ parent first := by
      intro equality
      rw [← equality] at firstDecrease
      omega
    have secondDistinct : second ≠ parent second := by
      intro equality
      rw [← equality] at secondDecrease
      omega
    have secondAtFirst : incident (pay first) second := by
      rw [sameResource]
      exact childIncident second secondPositive
    have firstAtSecond : incident (pay second) first := by
      rw [← sameResource]
      exact childIncident first firstPositive
    have firstOwners := resource_has_only_two_owners incident capacity
      (childIncident first firstPositive) (parentIncident first firstPositive)
      firstDistinct secondAtFirst
    have secondOwners := resource_has_only_two_owners incident capacity
      (childIncident second secondPositive) (parentIncident second secondPositive)
      secondDistinct firstAtSecond
    have secondIsParent : second = parent first := by
      rcases firstOwners with same | same
      · exact False.elim (equal same.symm)
      · exact same
    have firstIsParent : first = parent second := by
      rcases secondOwners with same | same
      · exact False.elim (equal same)
      · exact same
    rw [← secondIsParent] at firstDecrease
    rw [← firstIsParent] at secondDecrease
    omega

theorem combine_core_and_branches {Demand Resource : Type}
    (rank : Demand → Nat) (pay : Demand → Resource)
    (coreInjective : ∀ first second, rank first = 0 → rank second = 0 →
      pay first = pay second → first = second)
    (branchInjective : ∀ first second, 0 < rank first → 0 < rank second →
      pay first = pay second → first = second)
    (coreDisjoint : ∀ core branch, rank core = 0 → 0 < rank branch → pay core ≠ pay branch) :
    Function.Injective pay := by
  intro first second same
  by_cases firstCore : rank first = 0
  · by_cases secondCore : rank second = 0
    · exact coreInjective first second firstCore secondCore same
    · have positive : 0 < rank second := by omega
      exact False.elim (coreDisjoint first second firstCore positive same)
  · have firstPositive : 0 < rank first := by omega
    by_cases secondCore : rank second = 0
    · exact False.elim (coreDisjoint second first secondCore firstPositive same.symm)
    · have secondPositive : 0 < rank second := by omega
      exact branchInjective first second firstPositive secondPositive same

theorem allocation_ledger (surplus boundary resources demands assigned spare defect beta : Int)
    (packet : surplus - boundary = resources + beta - demands)
    (demandInventory : demands = assigned + defect)
    (resourceInventory : resources = assigned + spare) :
    surplus - boundary = spare + beta - defect := by omega

theorem complete_allocation_compensates (surplus boundary spare beta : Int)
    (ledger : surplus - boundary = spare + beta)
    (spareNonnegative : 0 ≤ spare) (betaNonnegative : 0 ≤ beta) :
    boundary ≤ surplus := by omega

theorem connected_tree_shortfall (demands resources assigned : Nat)
    (treeInventory : resources + 1 = demands) (injectiveBound : assigned ≤ resources) :
    assigned < demands := by omega

theorem chain_one_new_resource_suffices (demands oldResources newResources : Nat)
    (treeInventory : oldResources + 1 = demands)
    (newResource : newResources = oldResources + 1) : newResources = demands := by omega

end SubQuorum.OneSidedResourceAllocation

#print axioms SubQuorum.OneSidedResourceAllocation.resource_has_only_two_owners
#print axioms SubQuorum.OneSidedResourceAllocation.decreasing_parent_resources_are_injective
#print axioms SubQuorum.OneSidedResourceAllocation.combine_core_and_branches
#print axioms SubQuorum.OneSidedResourceAllocation.allocation_ledger
#print axioms SubQuorum.OneSidedResourceAllocation.complete_allocation_compensates
#print axioms SubQuorum.OneSidedResourceAllocation.connected_tree_shortfall
#print axioms SubQuorum.OneSidedResourceAllocation.chain_one_new_resource_suffices
