import SubQuorum.BTColumnCorridorObstruction

set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

namespace SubQuorum.ForcedMatesAdjacentMaxima
open SubQuorum.BTColumnCorridorObstruction (Frozen Point adjacent)

/-- A strict leaf-pair rank certificate forces every adjacent involutive
mate map to equal the canonical one. No finiteness or enumeration is used. -/
theorem strict_leaf_rank_unique {V : Type} (adj : V → V → Prop)
    (g h : V → V) (rank : V → Nat) (leaf : V → V)
    (gg : ∀ v, g (g v)=v) (hh : ∀ v, h (h v)=v)
    (choice : ∀ v, leaf v=v ∨ leaf v=g v)
    (hAdjacent : ∀ v, adj v (h v))
    (earlier : ∀ v u, adj (leaf v) u → u ≠ g (leaf v) → rank u < rank v) :
    ∀ v, h v=g v := by
  have byRank : ∀ n v, rank v=n → h v=g v := by
    intro n
    induction n using Nat.strongRecOn with
    | ind n ih =>
      intro v rv
      have forced : h (leaf v)=g (leaf v) := by
        apply Classical.byContradiction
        intro bad
        have smaller : rank (h (leaf v)) < n := by
          rw [← rv]
          exact earlier v _ (hAdjacent _) bad
        have known := ih _ smaller _ rfl
        have inverse : leaf v=g (h (leaf v)) := (hh _).symm.trans known
        have equal : g (leaf v)=h (leaf v) :=
          (congrArg g inverse).trans (gg _)
        exact bad equal.symm
      rcases choice v with same | partner
      · simpa only [same] using forced
      · rw [partner, gg] at forced
        have inv := hh (g v)
        rw [forced] at inv
        exact inv
  intro v
  exact byRank (rank v) v rfl

def selected : List Point := [(0,1), (0,3), (0,5), (0,7), (0,9), (0,11), (1,0), (1,2), (1,10), (2,0), (2,8), (2,11), (3,1), (3,3), (3,7), (3,9), (3,11), (4,0), (4,2), (4,8), (4,10), (5,0), (5,2), (5,7), (5,9), (5,11), (6,1), (6,3), (6,8), (6,10), (7,0), (7,11), (8,0), (8,2), (8,10), (9,1), (9,3), (9,5), (9,7), (9,9), (9,11)]
def matching : List (Point × Point) := [((1,5),(2,5)), ((3,5),(4,5)), ((5,5),(6,5)), ((7,5),(8,5)), ((2,6),(3,6)), ((4,6),(5,6)), ((6,6),(7,6)), ((1,6),(1,7)), ((1,8),(1,9)), ((8,6),(8,7)), ((8,8),(8,9)), ((7,7),(7,8)), ((1,3),(1,4)), ((2,4),(3,4)), ((8,3),(8,4)), ((7,4),(6,4)), ((4,4),(5,4))]
def endpoints : List Point := matching.flatMap fun e => [e.1,e.2]
def mate (v : Point) : Point := BTColumnCorridorObstruction.lookupMate v matching
def nonmateAdjacent (v w : Point) : Prop := adjacent v w ∧ w ≠ mate v
instance (v w : Point) : Decidable (nonmateAdjacent v w) := inferInstanceAs (Decidable (_ ∧ _))
def witnesses : List BTColumnCorridorObstruction.Witness := [
  ⟨(1,3), 0, (0,3), (1,2)⟩,
  ⟨(1,4), 28, (1,5), (2,4)⟩,
  ⟨(1,5), 2, (0,5), (1,4)⟩,
  ⟨(1,6), 21, (1,5), (2,6)⟩,
  ⟨(1,7), 6, (0,7), (1,8)⟩,
  ⟨(1,8), 22, (1,7), (2,8)⟩,
  ⟨(1,9), 3, (0,9), (1,10)⟩,
  ⟨(2,4), 26, (1,4), (2,5)⟩,
  ⟨(2,5), 20, (2,6), (3,5)⟩,
  ⟨(2,6), 10, (1,6), (2,5)⟩,
  ⟨(3,4), 27, (3,3), (3,5)⟩,
  ⟨(3,5), 11, (2,5), (3,6)⟩,
  ⟨(3,6), 19, (3,5), (3,7)⟩,
  ⟨(4,4), 30, (3,4), (4,5)⟩,
  ⟨(4,5), 18, (4,6), (5,5)⟩,
  ⟨(4,6), 12, (3,6), (4,5)⟩,
  ⟨(5,4), 31, (5,5), (6,4)⟩,
  ⟨(5,5), 13, (4,5), (5,6)⟩,
  ⟨(5,6), 17, (5,5), (5,7)⟩,
  ⟨(6,4), 32, (5,4), (6,3)⟩,
  ⟨(6,5), 16, (6,6), (7,5)⟩,
  ⟨(6,6), 14, (5,6), (6,5)⟩,
  ⟨(7,4), 29, (7,5), (8,4)⟩,
  ⟨(7,5), 15, (6,5), (7,6)⟩,
  ⟨(7,6), 9, (7,5), (7,7)⟩,
  ⟨(7,7), 24, (7,6), (8,7)⟩,
  ⟨(7,8), 8, (6,8), (8,8)⟩,
  ⟨(8,3), 1, (8,2), (9,3)⟩,
  ⟨(8,4), 33, (7,4), (8,5)⟩,
  ⟨(8,5), 4, (8,4), (9,5)⟩,
  ⟨(8,6), 23, (7,6), (8,5)⟩,
  ⟨(8,7), 7, (8,8), (9,7)⟩,
  ⟨(8,8), 25, (7,8), (8,7)⟩,
  ⟨(8,9), 5, (8,10), (9,9)⟩]
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
    (∀ v ∈ selected ++ endpoints, v.1<10 ∧ v.2<12) ∧
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


def leafPairs : List (Point × Point) := [((1,3),(1,4)), ((1,9),(1,8)), ((8,3),(8,4)), ((8,9),(8,8)), ((1,7),(1,6)), ((1,5),(2,5)), ((2,4),(3,4)), ((2,6),(3,6)), ((3,5),(4,5)), ((4,4),(5,4)), ((4,6),(5,6)), ((5,5),(6,5)), ((6,4),(7,4)), ((6,6),(7,6)), ((7,5),(8,5)), ((8,6),(8,7)), ((7,7),(7,8))]
def pairRank (v : Point) : Nat :=
  ((leafPairs.zipIdx).find? fun e => e.1.1 == v || e.1.2 == v).map Prod.snd |>.getD 0

theorem leaf_certificate_valid :
    (leafPairs.flatMap (fun e => [e.1,e.2])).Nodup ∧
    (∀ v ∈ endpoints, ∃ e ∈ leafPairs, v=e.1 ∨ v=e.2) ∧
    (∀ e ∈ leafPairs, mate e.1=e.2 ∧ mate e.2=e.1 ∧
      pairRank e.1=pairRank e.2 ∧
      ∀ u ∈ endpoints, adjacent e.1 u → u ≠ e.2 → pairRank u < pairRank e.1) := by decide

theorem attained_counts : selected.length=41 ∧ matching.length=17 ∧ endpoints.length=34 := by decide

theorem module_count_identity (n q : Nat) :
    (7*q+2)*n+3*q+2 + q*(3*n+5) + 2*q = (n+1)*(10*q+2) := by
  simp only [Nat.add_mul, Nat.mul_add, Nat.mul_assoc]
  rw [Nat.mul_left_comm n 10 q, Nat.mul_comm n q, Nat.mul_left_comm q 3 n]
  omega

theorem replaced_patch_budget (n q cap : Nat)
    (tileBound : cap+2*q ≤ (7*q+2)*n+5*q+2) :
    cap ≤ (7*q+2)*n+3*q+2 := by omega

#print axioms strict_leaf_rank_unique
#print axioms geometry_valid
#print axioms mate_closed
#print axioms certificate_valid
#print axioms all_endpoints_frozen
#print axioms leaf_certificate_valid
#print axioms attained_counts
#print axioms module_count_identity
#print axioms replaced_patch_budget

end SubQuorum.ForcedMatesAdjacentMaxima
