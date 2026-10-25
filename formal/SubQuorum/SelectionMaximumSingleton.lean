import SubQuorum.BTColumnCorridorObstruction

set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

namespace SubQuorum.SelectionMaximumSingleton
open SubQuorum.BTColumnCorridorObstruction (Frozen Point adjacent)

/-- Feasibility by uniqueness of an occupied neighbour. This formulation
also covers isolated selected vertices without finite cardinality machinery. -/
def Feasible {V : Type} (adj : V → V → Prop) (P T : V → Prop) : Prop :=
  (∀ v, T v → ¬ P v) ∧
  ∀ v, T v → ∀ a b, adj v a → adj v b → (P a ∨ T a) → (P b ∨ T b) → a=b

theorem isolated_selection_addable {V : Type} (adj : V → V → Prop)
    (P T : V → Prop) (x : V) (symmetric : ∀ a b, adj a b → adj b a)
    (irreflexive : ∀ a, ¬ adj a a) (free : ¬ P x)
    (feasible : Feasible adj P T)
    (isolated : ∀ y, adj x y → ¬ (P y ∨ T y)) :
    Feasible adj P (fun v => T v ∨ v=x) := by
  constructor
  · intro v selected
    rcases selected with old | same
    · exact feasible.1 v old
    · simpa only [same] using free
  · intro v selected a b va vb ha hb
    rcases selected with old | same
    · have ax : a ≠ x := by
        intro eq
        subst a
        exact isolated v (symmetric _ _ va) (Or.inr old)
      have bx : b ≠ x := by
        intro eq
        subst b
        exact isolated v (symmetric _ _ vb) (Or.inr old)
      have oa : P a ∨ T a := by
        rcases ha with hp | ht | hx
        · exact Or.inl hp
        · exact Or.inr ht
        · exact False.elim (ax hx)
      have ob : P b ∨ T b := by
        rcases hb with hp | ht | hx
        · exact Or.inl hp
        · exact Or.inr ht
        · exact False.elim (bx hx)
      exact feasible.2 v old a b va vb oa ob
    · subst v
      have impossible : False := by
        rcases ha with hp | ht | hx
        · exact isolated a va (Or.inl hp)
        · exact isolated a va (Or.inr ht)
        · subst a; exact irreflexive x va
      exact False.elim impossible

/-- All feasible monotone extensions lie in the single-addition candidate
hull. If it avoids x's neighbourhood, x stays isolated in every extension. -/
theorem candidate_hull_isolated {V : Type} (adj : V → V → Prop)
    (P T U candidate : V → Prop) (x : V)
    (base : ∀ y, adj x y → ¬ (P y ∨ T y))
    (hull : ∀ y, U y → T y ∨ candidate y)
    (noCandidateNeighbour : ∀ y, candidate y → ¬ adj x y) :
    ∀ y, adj x y → ¬ (P y ∨ U y) := by
  intro y xy occupied
  rcases occupied with hp | hu
  · exact base y xy (Or.inl hp)
  · rcases hull y hu with ht | hc
    · exact base y xy (Or.inr ht)
    · exact noCandidateNeighbour y hc xy

theorem maximal_contains_compatible {V : Type} (F : (V → Prop) → Prop)
    (T : V → Prop) (x : V)
    (maximal : ∀ U, F U → (∀ v, T v → U v) → (∀ v, U v → T v))
    (compatible : F (fun v => T v ∨ v=x)) : T x := by
  exact maximal _ compatible (fun _ h => Or.inl h) x (Or.inr rfl)

theorem frozen_extend_selection {V : Type} (P T U : V → Prop)
    (mate : V → V) (adj : V → V → Prop) (extend : ∀ v, T v → U v)
    {v : V} (frozen : Frozen P T mate adj v) : Frozen P U mate adj v := by
  induction frozen with
  | ss pv distinct va vb ta tb => exact Frozen.ss pv distinct va vb (extend _ ta) (extend _ tb)
  | sp pv distinct va vb ta pb _ ih => exact Frozen.sp pv distinct va vb (extend _ ta) pb ih
  | ps pv distinct va vb pa _ tb ih => exact Frozen.ps pv distinct va vb pa ih (extend _ tb)
  | pp pv distinct va vb pa _ pb _ ihA ihB => exact Frozen.pp pv distinct va vb pa ihA pb ihB

theorem extension_constant_slack (w added : Nat) (wge : 8≤w)
    (bound : added ≤ 8*w-33) : 41+added+(3*w+10)+4 ≤ (w+2)*11 := by omega

theorem w8_cover_bound (added : Nat) (bound : added ≤ 31-6+5) :
    41+added ≤ 71 := by omega

theorem fixed_P_constant_slack (w selected : Nat) (bound : selected ≤ 8*w+8) :
    selected+(3*w+10)+4 ≤ (w+2)*11 := by omega

theorem fixed_P_attaining_count (n : Nat) (nlarge : 4≤n) :
    56+16*(n-3)=16*n+8 := by omega

theorem w8_exact_ledger : 72+34+4=10*22/2 := by decide

def selected : List Point := [(0,1), (0,3), (0,5), (0,7), (0,9), (0,11), (0,13), (0,15), (0,17), (0,19), (0,21), (1,0), (1,2), (1,10), (1,12), (1,20), (2,0), (2,8), (2,11), (2,18), (2,21), (3,1), (3,3), (3,7), (3,9), (3,11), (3,13), (3,17), (3,19), (3,21), (4,0), (4,2), (4,8), (4,10), (4,12), (4,18), (4,20), (5,0), (5,2), (5,7), (5,9), (5,11), (5,13), (5,17), (5,19), (5,21), (6,1), (6,3), (6,8), (6,10), (6,12), (6,18), (6,20), (7,0), (7,11), (7,21), (8,0), (8,2), (8,10), (8,12), (8,20), (9,1), (9,3), (9,5), (9,7), (9,9), (9,11), (9,13), (9,15), (9,17), (9,19), (9,21)]
def matching : List (Point × Point) := [((1,5),(2,5)), ((3,5),(4,5)), ((5,5),(6,5)), ((7,5),(8,5)), ((2,6),(3,6)), ((4,6),(5,6)), ((6,6),(7,6)), ((1,6),(1,7)), ((1,8),(1,9)), ((8,6),(8,7)), ((8,8),(8,9)), ((7,7),(7,8)), ((1,3),(1,4)), ((2,4),(3,4)), ((8,3),(8,4)), ((7,4),(6,4)), ((1,15),(2,15)), ((3,15),(4,15)), ((5,15),(6,15)), ((7,15),(8,15)), ((2,16),(3,16)), ((4,16),(5,16)), ((6,16),(7,16)), ((1,16),(1,17)), ((1,18),(1,19)), ((8,16),(8,17)), ((8,18),(8,19)), ((7,17),(7,18)), ((1,13),(1,14)), ((2,14),(3,14)), ((8,13),(8,14)), ((7,14),(6,14)), ((4,4),(5,4)), ((4,14),(5,14))]
def endpoints : List Point := matching.flatMap fun e => [e.1,e.2]
def mate (v : Point) : Point := BTColumnCorridorObstruction.lookupMate v matching
def nonmateAdjacent (v w : Point) : Prop := adjacent v w ∧ w ≠ mate v
instance (v w : Point) : Decidable (nonmateAdjacent v w) := inferInstanceAs (Decidable (_ ∧ _))
def witnesses : List BTColumnCorridorObstruction.Witness := [
  ⟨(1,3), 0, (0,3), (1,2)⟩,
  ⟨(1,4), 6, (1,5), (2,4)⟩,
  ⟨(1,5), 1, (0,5), (1,4)⟩,
  ⟨(1,6), 6, (1,5), (2,6)⟩,
  ⟨(1,7), 1, (0,7), (1,8)⟩,
  ⟨(1,8), 7, (1,7), (2,8)⟩,
  ⟨(1,9), 0, (0,9), (1,10)⟩,
  ⟨(1,13), 0, (0,13), (1,12)⟩,
  ⟨(1,14), 6, (1,15), (2,14)⟩,
  ⟨(1,15), 1, (0,15), (1,14)⟩,
  ⟨(1,16), 6, (1,15), (2,16)⟩,
  ⟨(1,17), 1, (0,17), (1,18)⟩,
  ⟨(1,18), 7, (1,17), (2,18)⟩,
  ⟨(1,19), 0, (0,19), (1,20)⟩,
  ⟨(2,4), 2, (1,4), (2,5)⟩,
  ⟨(2,5), 5, (2,6), (3,5)⟩,
  ⟨(2,6), 2, (1,6), (2,5)⟩,
  ⟨(2,14), 2, (1,14), (2,15)⟩,
  ⟨(2,15), 5, (2,14), (2,16)⟩,
  ⟨(2,16), 2, (1,16), (2,15)⟩,
  ⟨(3,4), 5, (3,3), (3,5)⟩,
  ⟨(3,5), 3, (2,5), (3,4)⟩,
  ⟨(3,6), 4, (3,7), (4,6)⟩,
  ⟨(3,14), 4, (3,13), (4,14)⟩,
  ⟨(3,15), 3, (2,15), (3,14)⟩,
  ⟨(3,16), 4, (3,17), (4,16)⟩,
  ⟨(4,4), 4, (3,4), (4,5)⟩,
  ⟨(4,5), 4, (4,6), (5,5)⟩,
  ⟨(4,6), 4, (3,6), (4,5)⟩,
  ⟨(4,14), 4, (3,14), (4,15)⟩,
  ⟨(4,15), 4, (4,14), (4,16)⟩,
  ⟨(4,16), 4, (3,16), (4,15)⟩,
  ⟨(5,4), 4, (5,5), (6,4)⟩,
  ⟨(5,5), 5, (4,5), (5,4)⟩,
  ⟨(5,6), 3, (5,7), (6,6)⟩,
  ⟨(5,14), 3, (5,13), (6,14)⟩,
  ⟨(5,15), 5, (4,15), (5,14)⟩,
  ⟨(5,16), 3, (5,17), (6,16)⟩,
  ⟨(6,4), 5, (5,4), (6,3)⟩,
  ⟨(6,5), 3, (6,4), (6,6)⟩,
  ⟨(6,6), 6, (5,6), (6,5)⟩,
  ⟨(6,14), 6, (5,14), (6,15)⟩,
  ⟨(6,15), 3, (6,14), (6,16)⟩,
  ⟨(6,16), 6, (5,16), (6,15)⟩,
  ⟨(7,4), 2, (7,5), (8,4)⟩,
  ⟨(7,5), 6, (6,5), (7,4)⟩,
  ⟨(7,6), 2, (7,5), (7,7)⟩,
  ⟨(7,7), 8, (7,6), (8,7)⟩,
  ⟨(7,8), 1, (6,8), (8,8)⟩,
  ⟨(7,14), 2, (7,15), (8,14)⟩,
  ⟨(7,15), 7, (6,15), (7,14)⟩,
  ⟨(7,16), 2, (7,15), (7,17)⟩,
  ⟨(7,17), 9, (7,16), (8,17)⟩,
  ⟨(7,18), 1, (6,18), (8,18)⟩,
  ⟨(8,3), 0, (8,2), (9,3)⟩,
  ⟨(8,4), 7, (7,4), (8,5)⟩,
  ⟨(8,5), 1, (8,4), (9,5)⟩,
  ⟨(8,6), 7, (7,6), (8,5)⟩,
  ⟨(8,7), 1, (8,8), (9,7)⟩,
  ⟨(8,8), 9, (7,8), (8,7)⟩,
  ⟨(8,9), 0, (8,10), (9,9)⟩,
  ⟨(8,13), 0, (8,12), (9,13)⟩,
  ⟨(8,14), 8, (7,14), (8,15)⟩,
  ⟨(8,15), 1, (8,14), (9,15)⟩,
  ⟨(8,16), 8, (7,16), (8,15)⟩,
  ⟨(8,17), 1, (8,18), (9,17)⟩,
  ⟨(8,18), 10, (7,18), (8,17)⟩,
  ⟨(8,19), 0, (8,20), (9,19)⟩]
def record (v : Point) : BTColumnCorridorObstruction.Witness :=
  (witnesses.find? fun w => w.point == v).getD default
def rank (v : Point) : Nat := (record v).rank
def validAt (v : Point) : Prop :=
  let a := (record v).left
  let b := (record v).right
  a ≠ b ∧ nonmateAdjacent v a ∧ nonmateAdjacent v b ∧
    (a ∈ selected ∨ (a ∈ endpoints ∧ rank (mate a) < rank v)) ∧
    (b ∈ selected ∨ (b ∈ endpoints ∧ rank (mate b) < rank v))
instance (v : Point) : Decidable (validAt v) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ (_ ∨ (_ ∧ _)) ∧ (_ ∨ (_ ∧ _))))

theorem geometry_valid :
    selected.Nodup ∧ endpoints.Nodup ∧
    (∀ e ∈ matching, adjacent e.1 e.2) ∧
    (∀ v ∈ endpoints, v ∉ selected) ∧
    (∀ v ∈ selected ++ endpoints, v.1<10 ∧ v.2<22) ∧
    (∀ v ∈ selected,
      ((selected ++ endpoints).filter fun w => decide (adjacent v w)).length ≤ 1) := by decide

theorem mate_closed : ∀ v ∈ endpoints, mate v ∈ endpoints := by decide
theorem certificate_valid : ∀ v ∈ endpoints, validAt v := by decide

theorem all_endpoints_frozen : ∀ v ∈ endpoints,
    Frozen (fun x => x ∈ endpoints) (fun x => x ∈ selected) mate nonmateAdjacent v := by
  apply BTColumnCorridorObstruction.strict_rank_complete (fun x => x ∈ endpoints)
    (fun x => x ∈ selected) mate nonmateAdjacent rank mate_closed
  intro v pv
  exact ⟨(record v).left,(record v).right,certificate_valid v pv⟩



def ownerLinks : List (Nat × Nat) := [(0,0), (1,0), (1,2), (1,10), (1,11), (2,2), (2,3), (3,3), (4,4), (5,4), (5,6), (5,13), (5,14), (6,6), (6,7), (7,7), (8,8), (9,9), (10,10), (11,11), (11,12), (12,12), (13,13), (14,14), (14,15), (15,15)]
def reachableOwners : List Nat := [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15]
def ownerSupport : List (Nat × List (Nat × Nat × Nat)) := [(0, []), (1, []), (2, []), (3, []), (4, []), (5, []), (6, []), (7, []), (8, [(3,9,9), (3,13,13)]), (9, [(3,19,19)]), (10, []), (11, []), (12, []), (13, []), (14, []), (15, [])]

theorem sources_inside : 1 ∈ reachableOwners ∧ 5 ∈ reachableOwners := by decide

theorem reachable_closed : ∀ e ∈ ownerLinks,
    e.1 ∈ reachableOwners → e.2 ∈ reachableOwners := by decide

theorem reachable_support_empty : ∀ e ∈ ownerSupport,
    e.1 ∈ reachableOwners → e.2=[] := by decide

theorem selected_count : selected.length=72 := by decide

#print axioms isolated_selection_addable
#print axioms candidate_hull_isolated
#print axioms maximal_contains_compatible
#print axioms frozen_extend_selection
#print axioms extension_constant_slack
#print axioms w8_cover_bound
#print axioms fixed_P_constant_slack
#print axioms fixed_P_attaining_count
#print axioms w8_exact_ledger
#print axioms geometry_valid
#print axioms mate_closed
#print axioms certificate_valid
#print axioms all_endpoints_frozen
#print axioms sources_inside
#print axioms reachable_closed
#print axioms reachable_support_empty
#print axioms selected_count

end SubQuorum.SelectionMaximumSingleton
