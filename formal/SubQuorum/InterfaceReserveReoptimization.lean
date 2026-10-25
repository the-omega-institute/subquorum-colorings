import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.InterfaceReserveReoptimization

/-- A simple path starting at s cannot have any later vertex equal to s.
This excludes reverse source arcs, even when other residual arcs reverse. -/
theorem simple_path_no_source_reentry {V : Type} {n : Nat}
    (vertex : Fin (n+1) → V) (s : V)
    (injective : ∀ i j, vertex i=vertex j → i=j)
    (start : vertex ⟨0,by omega⟩=s) (i : Fin n) :
    vertex ⟨i.val+1,by omega⟩ ≠ s := by
  intro same
  have index := injective ⟨i.val+1,by omega⟩ ⟨0,by omega⟩ (same.trans start.symm)
  have values := congrArg Fin.val index
  change i.val+1=0 at values
  omega

/-- A purported reverse traversal of any source arc would enter s. -/
theorem simple_path_no_reverse_source {V A : Type} {n : Nat}
    (vertex : Fin (n+1) → V) (s : V)
    (injective : ∀ i j, vertex i=vertex j → i=j)
    (start : vertex ⟨0,by omega⟩=s)
    (reverseSource : Fin n → A → Prop)
    (entersSource : ∀ i a, reverseSource i a → vertex ⟨i.val+1,by omega⟩=s) :
    ∀ i a, ¬ reverseSource i a := by
  intro i a reverse
  exact simple_path_no_source_reentry vertex s injective start i (entersSource i a reverse)

/-- With no reverse source traversal, a saturated unit source cannot lose
flow. The post-update capacity bound also prevents a second payment. -/
theorem saturated_source_survives (old next forward backward : Int)
    (paid : old=1) (update : next=old+forward-backward)
    (forwardNonnegative : 0≤forward) (noReverse : backward=0)
    (capacity : next≤1) : next=1 := by omega

/-- Iterate the local augmentation invariant, retaining the original source
identities rather than just the total payment count. -/
theorem protected_sources_survive_iterations {A : Type}
    (flow : Nat → A → Int) (kept : A → Prop)
    (initial : ∀ a, kept a → flow 0 a=1)
    (step : ∀ k a, kept a → flow k a=1 → flow (k+1) a=1) :
    ∀ k a, kept a → flow k a=1 := by
  intro k
  induction k with
  | zero => exact initial
  | succ k ih =>
    intro a ha
    exact step k a ha (ih a ha)

/-- If p distinct old unit sources survive and the old-only bound is p,
there are no additional old payments hidden in the interface gain. -/
theorem exact_interface_gain (p old new joint : Int)
    (retained : p≤old) (localMaxima : old≤p)
    (decomposition : joint=old+new) : old=p ∧ new=joint-p := by omega

/-- The cut expression and unpaid-interface expression refer to the SAME
withdrawn original set. Their complement identity needs no enumeration. -/
theorem joint_cut_deficit_identity (p a removed localRank interfaceRank : Int) :
    p+a-(removed+localRank+interfaceRank)=
      (p-localRank)+(a-interfaceRank)-removed := by omega

/-- Exact min-cut characterization becomes an exact maximum-deficit
characterization; the attaining witness is retained, not separately chosen. -/
theorem exact_deficit_from_attained_cut {F : Type}
    (cut : F → Int) (witness : F) (p a joint : Int)
    (lower : ∀ f, joint≤cut f) (attained : joint=cut witness) :
    (∀ f, p+a-cut f≤p+a-joint) ∧
      p+a-cut witness=p+a-joint := by
  constructor
  · intro f
    have := lower f
    omega
  · omega

/-- Full compensation iff every cut can pay the old p plus all a new
sources, assuming the actual attained minimum-cut and source bounds. -/
theorem full_payment_cut_criterion {F : Type}
    (cut : F → Int) (witness : F) (p a joint : Int)
    (lower : ∀ f, joint≤cut f) (attained : joint=cut witness)
    (sourceBound : joint≤p+a) :
    joint=p+a ↔ ∀ f, p+a≤cut f := by
  constructor
  · intro full f
    have := lower f
    omega
  · intro allCuts
    have := allCuts witness
    omega

/-- The fixed pack plus unused matching is a candidate in the rerouted
network, so optimizing routes can only improve the old reserve bound. -/
theorem rerouting_dominates_fixed_pack (p joint theta nu : Int)
    (gain : theta=joint-p) (fixedPack : p+nu≤joint) : nu≤theta := by omega

theorem reoptimized_global_deficit (al a p joint global dlocal dglobal theta : Int)
    (gain : theta=joint-p) (embedding : joint≤global)
    (localDeficit : dlocal=al-p) (globalDeficit : dglobal=al+a-global) :
    dglobal≤dlocal+a-theta := by omega

/-- The geometric family has positive numerical slack: a restricted-pool
exchange is not a numerical counterexample. -/
theorem physical_slack (w : Nat) (height : 8≤w) :
    11*((w:Int)+2)-40-(3*(w:Int)+10)=8*(w:Int)-28 ∧
    0<8*(w:Int)-28 := by omega

abbrev Point := Nat × Nat
abbrev UnitID := Nat × Nat × Nat

/-- Explicit original units and links of the physical W=8 fixture. The
Python adapter separately compares these constants to the actual board. -/
def shared : UnitID := (4,11,11)
def privateUnit : UnitID := (0,1,1)
def lowerLinks : List (Point × Point) := [((8,5),(8,6)),((8,7),(8,8))]
def upperLinks : List (Point × Point) := [((1,5),(1,4))]
def restrictedSupport (owner : Nat) : List UnitID :=
  match owner with
  | 1 => []
  | 4 => [shared]
  | 0 => [privateUnit]
  | 11 => [shared]
  | _ => []

/-- The two final payments have distinct ORIGINAL identities; I has no
access to the resource left over by the old lower-route baseline. -/
theorem actual_two_unit_exchange :
    shared≠privateUnit ∧ restrictedSupport 1=[] ∧
    shared ∈ restrictedSupport 4 ∧ privateUnit ∉ restrictedSupport 4 ∧
    privateUnit ∈ restrictedSupport 0 ∧ shared ∈ restrictedSupport 11 ∧
    lowerLinks.length=2 ∧ upperLinks.length=1 := by decide


def actualPairs : List (Point × Point) := [((1, 3), (1, 4)), ((1, 5), (8, 5)), ((1, 6), (1, 7)), ((1, 8), (1, 9)), ((1, 13), (8, 13)), ((2, 16), (3, 16)), ((4, 16), (5, 16)), ((6, 16), (7, 18)), ((7, 7), (7, 8)), ((8, 3), (8, 4)), ((8, 6), (8, 7)), ((8, 8), (8, 9))]
def actualLinks : List (Point × Point) := [((1, 3), (1, 4)), ((1, 5), (1, 4)), ((1, 5), (1, 6)), ((1, 7), (1, 6)), ((1, 7), (1, 8)), ((1, 9), (1, 8)), ((7, 8), (7, 7)), ((8, 3), (8, 4)), ((8, 5), (8, 4)), ((8, 5), (8, 6)), ((8, 7), (8, 6)), ((8, 7), (8, 8)), ((8, 9), (8, 8)), ((3, 16), (2, 16)), ((3, 16), (4, 16))]
def actualAlphaOwners : List Nat := [1,4]

/-- Both alternative routes use declared physical links, connect through
actual owner pairs, and stay disjoint from the new interface source. -/
theorem actual_route_owner_incidence :
    (∀ e ∈ lowerLinks, e ∈ actualLinks) ∧
    (∀ e ∈ upperLinks, e ∈ actualLinks) ∧
    actualPairs[1]! = ((1,5),(8,5)) ∧
    actualPairs[4]! = ((1,13),(8,13)) ∧
    actualPairs[10]! = ((8,6),(8,7)) ∧
    actualPairs[11]! = ((8,8),(8,9)) ∧
    actualPairs[0]! = ((1,3),(1,4)) ∧
    ([1,10,11,4] : List Nat).Nodup ∧ ([1,0,4] : List Nat).Nodup ∧
    ([(1,privateUnit),(4,shared)].map Prod.snd).Nodup := by
  constructor
  · intro e he
    have h : e=((8,5),(8,6)) ∨ e=((8,7),(8,8)) := by simpa [lowerLinks] using he
    cases h with
    | inl same => subst e; decide
    | inr same => subst e; decide
  constructor
  · intro e he
    have same : e=((1,5),(1,4)) := by simpa [upperLinks] using he
    subst e
    decide
  decide

/-- Count/cost tables, not a formalization of the geometric adapter. -/
theorem actual_strict_gain_and_cost :
    (2:Int)-1=1 ∧ (0:Int)<1 ∧ (1:Int)<2 ∧ 11*(8+2)-40-(3*8+10)=36 := by decide

#print axioms simple_path_no_source_reentry
#print axioms simple_path_no_reverse_source
#print axioms saturated_source_survives
#print axioms protected_sources_survive_iterations
#print axioms exact_interface_gain
#print axioms joint_cut_deficit_identity
#print axioms exact_deficit_from_attained_cut
#print axioms full_payment_cut_criterion
#print axioms rerouting_dominates_fixed_pack
#print axioms reoptimized_global_deficit
#print axioms physical_slack
#print axioms actual_two_unit_exchange
#print axioms actual_route_owner_incidence
#print axioms actual_strict_gain_and_cost

end SubQuorum.InterfaceReserveReoptimization
