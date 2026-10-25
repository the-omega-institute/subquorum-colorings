import SubQuorum.SelectionMaximumSingleton

set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

namespace SubQuorum.PerpendicularGuardedReserves
open SubQuorum.BTColumnCorridorObstruction (Frozen Point adjacent)
open SubQuorum.SelectionMaximumSingleton (Feasible)

/-- A selected guard that already faces an occupied point forbids every
other neighbour from being either selected or a matching endpoint. -/
theorem saturated_guard_excludes {V : Type} (adj : V → V → Prop)
    (P T : V → Prop) (feasible : Feasible adj P T)
    (s p x : V) (ts : T s) (sp : adj s p) (sx : adj s x)
    (occupied : P p ∨ T p) (distinct : p ≠ x) : ¬ (P x ∨ T x) := by
  intro ox
  exact distinct (feasible.2 s ts p x sp sx occupied ox)

theorem two_endpoints_exclude_selection {V : Type} (adj : V → V → Prop)
    (P T : V → Prop) (feasible : Feasible adj P T)
    (x p z : V) (xp : adj x p) (xz : adj x z)
    (pp : P p) (pz : P z) (different : p ≠ z) : ¬ T x := by
  intro tx
  exact different (feasible.2 x tx p z xp xz (Or.inl pp) (Or.inl pz))

def chooseReserve {I R : Type} (upper lower : I → R) (available : R → Prop)
    [DecidablePred available] (i : I) : R :=
  if available (upper i) then upper i else lower i

theorem chosen_reserve_available {I R : Type} (upper lower : I → R)
    (available : R → Prop) [DecidablePred available]
    (survives : ∀ i, available (upper i) ∨ available (lower i)) :
    ∀ i, available (chooseReserve upper lower available i) := by
  intro i
  unfold chooseReserve
  split
  · assumption
  · exact (survives i).resolve_left (by assumption)

theorem chosen_reserves_injective {I R : Type} (upper lower : I → R)
    (owner : R → I) (available : R → Prop) [DecidablePred available]
    (ownsUpper : ∀ i, owner (upper i)=i) (ownsLower : ∀ i, owner (lower i)=i) :
    ∀ i j, chooseReserve upper lower available i=chooseReserve upper lower available j → i=j := by
  have owned : ∀ i, owner (chooseReserve upper lower available i)=i := by
    intro i
    unfold chooseReserve
    split
    · exact ownsUpper i
    · exact ownsLower i
  intro i j equal
  exact (owned i).symm.trans ((congrArg owner equal).trans (owned j))

theorem one_removal_survives {I R : Type} (upper lower : I → R)
    (removed : R → Prop) (atMostOne : ∀ i, ¬ (removed (upper i) ∧ removed (lower i))) :
    ∀ i, ¬ removed (upper i) ∨ ¬ removed (lower i) := by
  intro i
  classical
  by_cases hu : removed (upper i)
  · exact Or.inr (fun hl => atMostOne i ⟨hu,hl⟩)
  · exact Or.inl hu

def colourWeight {V : Type} (black : V → Bool) (v : V) : Int := if black v then 1 else -1

def balance {V : Type} (black : V → Bool) : List V → Int
  | [] => 0
  | v::vs => colourWeight black v + balance black vs

theorem balance_append {V : Type} (black : V → Bool) (xs ys : List V) :
    balance black (xs++ys)=balance black xs+balance black ys := by
  induction xs with
  | nil => simp [balance]
  | cons v vs ih => simp only [List.cons_append, balance, ih]; omega

theorem opposite_weight {V : Type} (black : V → Bool) (u v : V)
    (opposite : black u ≠ black v) : colourWeight black u+colourWeight black v=0 := by
  cases hu : black u <;> cases hv : black v <;> simp_all [colourWeight]

theorem matching_balanced {V : Type} (black : V → Bool) (edges : List (V × V))
    (opposite : ∀ e ∈ edges, black e.1 ≠ black e.2) :
    balance black (edges.flatMap fun e => [e.1,e.2])=0 := by
  induction edges with
  | nil => rfl
  | cons e es ih =>
    have tail := ih (fun f hf => opposite f (by simp [hf]))
    have head := opposite_weight black e.1 e.2 (opposite e (by simp))
    simp only [List.flatMap_cons, List.cons_append, List.nil_append, balance]
    rw [tail]
    omega

theorem single_colour_balance {V : Type} (black : V → Bool) (vs : List V)
    (allBlack : ∀ v ∈ vs, black v=true) : balance black vs=(vs.length : Int) := by
  induction vs with
  | nil => rfl
  | cons v vs ih =>
    have head := allBlack v (by simp)
    have tail := ih (fun u hu => allBlack u (by simp [hu]))
    simp [balance, colourWeight, head, tail]
    omega

theorem no_single_colour_matching_extension {V : Type} (black : V → Bool)
    (old extra : List V) (edges : List (V × V))
    (balancedOld : balance black old=0)
    (allBlack : ∀ v ∈ extra, black v=true)
    (covers : old++extra=edges.flatMap fun e => [e.1,e.2])
    (opposite : ∀ e ∈ edges, black e.1 ≠ black e.2) : extra=[] := by
  have extended : balance black (old++extra)=0 := by
    rw [covers]
    exact matching_balanced black edges opposite
  rw [balance_append, balancedOld, Int.zero_add, single_colour_balance black extra allBlack] at extended
  have len : extra.length=0 := by omega
  cases extra with
  | nil => rfl
  | cons v vs => simp only [List.length_cons] at len; omega

def selected : List Point := [(0,1), (0,2), (0,4), (0,5), (0,7), (0,8), (1,0), (1,3), (1,6), (1,9), (2,1), (2,4), (2,5), (2,8), (3,0), (3,3), (3,6), (3,9), (5,0), (5,9), (7,0), (7,3), (7,5), (7,9), (8,2), (8,4), (8,6), (9,0), (9,3), (9,5), (9,9), (10,1), (10,4), (10,6), (10,8), (11,0), (11,2), (11,3), (11,5), (11,7), (11,9)]
def matching : List (Point × Point) := [((5,1),(5,2)), ((5,3),(5,4)), ((5,5),(5,6)), ((5,7),(5,8)), ((6,2),(6,3)), ((6,4),(6,5)), ((6,6),(6,7)), ((6,1),(7,1)), ((8,1),(9,1)), ((6,8),(7,8)), ((8,8),(9,8)), ((7,7),(8,7)), ((3,1),(4,1)), ((4,2),(4,3)), ((3,8),(4,8)), ((4,7),(4,6)), ((4,4),(4,5))]
def endpoints : List Point := matching.flatMap fun e => [e.1,e.2]
def mate (v : Point) : Point := BTColumnCorridorObstruction.lookupMate v matching
def nonmateAdjacent (v w : Point) : Prop := adjacent v w ∧ w ≠ mate v
instance (v w : Point) : Decidable (nonmateAdjacent v w) := inferInstanceAs (Decidable (_ ∧ _))
def witnesses : List BTColumnCorridorObstruction.Witness := [
  ⟨(3,1), 0, (2,1), (3,0)⟩,
  ⟨(3,8), 1, (2,8), (3,9)⟩,
  ⟨(4,1), 28, (4,2), (5,1)⟩,
  ⟨(4,2), 26, (4,1), (5,2)⟩,
  ⟨(4,3), 27, (3,3), (5,3)⟩,
  ⟨(4,4), 30, (4,3), (5,4)⟩,
  ⟨(4,5), 31, (4,6), (5,5)⟩,
  ⟨(4,6), 32, (3,6), (4,5)⟩,
  ⟨(4,7), 29, (4,8), (5,7)⟩,
  ⟨(4,8), 33, (4,7), (5,8)⟩,
  ⟨(5,1), 2, (4,1), (5,0)⟩,
  ⟨(5,2), 20, (5,3), (6,2)⟩,
  ⟨(5,3), 11, (5,2), (6,3)⟩,
  ⟨(5,4), 18, (5,5), (6,4)⟩,
  ⟨(5,5), 13, (5,4), (6,5)⟩,
  ⟨(5,6), 16, (5,7), (6,6)⟩,
  ⟨(5,7), 15, (5,6), (6,7)⟩,
  ⟨(5,8), 4, (4,8), (5,9)⟩,
  ⟨(6,1), 21, (5,1), (6,2)⟩,
  ⟨(6,2), 10, (5,2), (6,1)⟩,
  ⟨(6,3), 19, (5,3), (6,4)⟩,
  ⟨(6,4), 12, (5,4), (6,3)⟩,
  ⟨(6,5), 17, (5,5), (6,6)⟩,
  ⟨(6,6), 14, (5,6), (6,5)⟩,
  ⟨(6,7), 9, (5,7), (6,8)⟩,
  ⟨(6,8), 23, (5,8), (6,7)⟩,
  ⟨(7,1), 6, (7,0), (8,1)⟩,
  ⟨(7,7), 24, (6,7), (7,8)⟩,
  ⟨(7,8), 7, (7,9), (8,8)⟩,
  ⟨(8,1), 22, (7,1), (8,2)⟩,
  ⟨(8,7), 8, (8,6), (8,8)⟩,
  ⟨(8,8), 25, (7,8), (8,7)⟩,
  ⟨(9,1), 3, (9,0), (10,1)⟩,
  ⟨(9,8), 5, (9,9), (10,8)⟩]
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
    (∀ v ∈ selected ++ endpoints, v.1<12 ∧ v.2<10) ∧
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

def originalSelected : List Point := selected.map Prod.swap
def originalEndpoints : List Point := endpoints.map Prod.swap
def board : List Point := (List.range 10).flatMap fun r => (List.range 12).map fun c => (r,c)
def endpointHull : List Point := [(4,9), (5,10), (6,11), (7,9)]

theorem endpoint_hull_valid : ∀ v ∈ board,
    (v ∈ endpointHull ↔ v ∉ originalSelected ∧ v ∉ originalEndpoints ∧
      ∀ t ∈ originalSelected, adjacent t v →
        ∀ u ∈ originalSelected ++ originalEndpoints, ¬ adjacent t u) := by decide

theorem endpoint_hull_isolation : ∀ v ∈ endpointHull,
    (v.1+v.2)%2=0 ∨ ∀ u ∈ originalEndpoints ++ endpointHull, ¬ adjacent v u := by decide

theorem two_actual_reserves :
    (2,2) ∉ selected ++ endpoints ∧ (3,2) ∉ selected ++ endpoints ∧
    (2,7) ∉ selected ++ endpoints ∧ (3,7) ∉ selected ++ endpoints ∧
    (2,1) ∈ selected ∧ (3,1) ∈ endpoints ∧
    (2,8) ∈ selected ∧ (3,8) ∈ endpoints ∧
    (∀ r ∈ [1,3,6,8], ¬ ((2,r) ∈ selected ∧ (3,r) ∈ selected)) := by decide

#print axioms saturated_guard_excludes
#print axioms two_endpoints_exclude_selection
#print axioms chosen_reserve_available
#print axioms chosen_reserves_injective
#print axioms one_removal_survives
#print axioms balance_append
#print axioms opposite_weight
#print axioms matching_balanced
#print axioms single_colour_balance
#print axioms no_single_colour_matching_extension
#print axioms geometry_valid
#print axioms mate_closed
#print axioms certificate_valid
#print axioms all_endpoints_frozen
#print axioms endpoint_hull_valid
#print axioms endpoint_hull_isolation
#print axioms two_actual_reserves

end SubQuorum.PerpendicularGuardedReserves
