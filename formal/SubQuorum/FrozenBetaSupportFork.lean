import SubQuorum.BTColumnCorridorObstruction

set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

namespace SubQuorum.FrozenBetaSupportFork
open SubQuorum.BTColumnCorridorObstruction (Frozen Point adjacent)

-- Permanent finite fixture. General support allocation and optimum proofs
-- are written in FROZEN_BETA_SUPPORT_FORK_AND_RESERVED_RESOURCE_GAIN.md.
def selected : List Point := [(1,7), (1,9), (2,2), (2,10), (3,1), (4,3), (4,5), (5,1), (5,10), (6,12), (7,1), (10,1), (10,8), (12,1), (12,9), (13,2), (13,5), (13,8), (13,10), (13,12), (14,7)]
def matching : List (Point × Point) := [((2,7), (3,7)), ((2,8), (2,9)), ((3,2), (4,2)), ((3,8), (4,8)), ((4,7), (5,7)), ((5,2), (6,2)), ((5,5), (6,5)), ((5,6), (6,6)), ((5,8), (6,8)), ((6,3), (6,4)), ((6,7), (7,7)), ((6,9), (6,10)), ((7,2), (7,3)), ((7,4), (7,5)), ((7,6), (8,6)), ((7,8), (7,9)), ((7,10), (7,11)), ((7,12), (8,12)), ((8,5), (9,5)), ((8,11), (9,11)), ((9,6), (10,6)), ((9,12), (10,12)), ((10,2), (10,3)), ((10,4), (10,5)), ((10,7), (11,7)), ((10,11), (11,11)), ((11,2), (12,2)), ((11,3), (11,4)), ((11,5), (12,5)), ((11,6), (12,6)), ((11,12), (12,12)), ((12,7), (13,7)), ((12,10), (12,11))]
def endpoints : List Point := matching.flatMap fun e => [e.1,e.2]
def mate (v : Point) : Point := BTColumnCorridorObstruction.lookupMate v matching
def nonmateAdjacent (v w : Point) : Prop := adjacent v w ∧ w ≠ mate v
instance (v w : Point) : Decidable (nonmateAdjacent v w) := inferInstanceAs (Decidable (_ ∧ _))
def witnesses : List BTColumnCorridorObstruction.Witness := [
  ⟨(2,7), 1, (1,7), (2,8)⟩,
  ⟨(2,8), 13, (2,7), (3,8)⟩,
  ⟨(2,9), 0, (1,9), (2,10)⟩,
  ⟨(3,2), 0, (2,2), (3,1)⟩,
  ⟨(3,7), 12, (3,8), (4,7)⟩,
  ⟨(3,8), 2, (2,8), (3,7)⟩,
  ⟨(4,2), 15, (4,3), (5,2)⟩,
  ⟨(4,7), 3, (3,7), (4,8)⟩,
  ⟨(4,8), 11, (4,7), (5,8)⟩,
  ⟨(5,2), 1, (4,2), (5,1)⟩,
  ⟨(5,5), 11, (4,5), (5,6)⟩,
  ⟨(5,6), 6, (5,5), (5,7)⟩,
  ⟨(5,7), 10, (5,8), (6,7)⟩,
  ⟨(5,8), 4, (4,8), (5,7)⟩,
  ⟨(6,2), 14, (6,3), (7,2)⟩,
  ⟨(6,3), 3, (6,2), (7,3)⟩,
  ⟨(6,4), 12, (6,5), (7,4)⟩,
  ⟨(6,5), 5, (6,4), (7,5)⟩,
  ⟨(6,6), 10, (6,7), (7,6)⟩,
  ⟨(6,7), 5, (5,7), (6,8)⟩,
  ⟨(6,8), 9, (6,9), (7,8)⟩,
  ⟨(6,9), 7, (6,8), (7,9)⟩,
  ⟨(6,10), 7, (5,10), (7,10)⟩,
  ⟨(7,2), 2, (6,2), (7,1)⟩,
  ⟨(7,3), 13, (6,3), (7,4)⟩,
  ⟨(7,4), 4, (6,4), (7,3)⟩,
  ⟨(7,5), 9, (7,6), (8,5)⟩,
  ⟨(7,6), 6, (7,5), (7,7)⟩,
  ⟨(7,7), 9, (7,6), (7,8)⟩,
  ⟨(7,8), 6, (6,8), (7,7)⟩,
  ⟨(7,9), 8, (6,9), (7,10)⟩,
  ⟨(7,10), 8, (6,10), (7,9)⟩,
  ⟨(7,11), 6, (7,12), (8,11)⟩,
  ⟨(7,12), 9, (6,12), (7,11)⟩,
  ⟨(8,5), 7, (7,5), (8,6)⟩,
  ⟨(8,6), 8, (8,5), (9,6)⟩,
  ⟨(8,11), 10, (7,11), (8,12)⟩,
  ⟨(8,12), 5, (8,11), (9,12)⟩,
  ⟨(9,5), 7, (9,6), (10,5)⟩,
  ⟨(9,6), 8, (8,6), (9,5)⟩,
  ⟨(9,11), 4, (9,12), (10,11)⟩,
  ⟨(9,12), 11, (8,12), (9,11)⟩,
  ⟨(10,2), 1, (10,1), (11,2)⟩,
  ⟨(10,3), 13, (10,4), (11,3)⟩,
  ⟨(10,4), 3, (10,3), (11,4)⟩,
  ⟨(10,5), 9, (9,5), (10,6)⟩,
  ⟨(10,6), 6, (10,5), (11,6)⟩,
  ⟨(10,7), 9, (10,6), (10,8)⟩,
  ⟨(10,11), 12, (9,11), (10,12)⟩,
  ⟨(10,12), 3, (10,11), (11,12)⟩,
  ⟨(11,2), 14, (10,2), (11,3)⟩,
  ⟨(11,3), 2, (10,3), (11,2)⟩,
  ⟨(11,4), 12, (10,4), (11,5)⟩,
  ⟨(11,5), 4, (10,5), (11,4)⟩,
  ⟨(11,6), 10, (10,6), (11,7)⟩,
  ⟨(11,7), 6, (11,6), (12,7)⟩,
  ⟨(11,11), 2, (11,12), (12,11)⟩,
  ⟨(11,12), 13, (10,12), (11,11)⟩,
  ⟨(12,2), 0, (12,1), (13,2)⟩,
  ⟨(12,5), 11, (12,6), (13,5)⟩,
  ⟨(12,6), 5, (12,5), (12,7)⟩,
  ⟨(12,7), 11, (11,7), (12,6)⟩,
  ⟨(12,10), 0, (12,9), (13,10)⟩,
  ⟨(12,11), 14, (11,11), (12,12)⟩,
  ⟨(12,12), 1, (12,11), (13,12)⟩,
  ⟨(13,7), 0, (13,8), (14,7)⟩]
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
    (∀ v ∈ selected ++ endpoints, 1≤v.1 ∧ v.1≤14 ∧ v.2<14) ∧
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

def verticalPartner (v : Point) : Point :=
  if v.1 % 2 = 0 then (v.1+1, v.2) else (v.1-1, v.2)
def tp (v : Point) : Prop := v ∈ endpoints ∧ verticalPartner v ∈ selected
def bp (v : Point) : Prop := v ∈ endpoints ∧ verticalPartner v ∉ selected ∧ verticalPartner v ∉ endpoints
def blank (v : Point) : Prop := v ∉ selected ∧ v ∉ endpoints
instance (v : Point) : Decidable (tp v) := inferInstanceAs (Decidable (_ ∧ _))
instance (v : Point) : Decidable (bp v) := inferInstanceAs (Decidable (_ ∧ _ ∧ _))
instance (v : Point) : Decidable (blank v) := inferInstanceAs (Decidable (_ ∧ _))
def bb (v : Point) : Prop := blank v ∧ blank (verticalPartner v)
def bt (v : Point) : Prop :=
  (v ∈ selected ∧ blank (verticalPartner v)) ∨ (blank v ∧ verticalPartner v ∈ selected)
instance (v : Point) : Decidable (bb v) := inferInstanceAs (Decidable (_ ∧ _))
instance (v : Point) : Decidable (bt v) := inferInstanceAs (Decidable ((_ ∧ _) ∨ (_ ∧ _)))

def alternating : Bool → List Point → Prop
  | _, [] => True
  | _, [_] => True
  | useMatching, a :: b :: rest =>
    (if useMatching then mate a = b else verticalPartner a = b) ∧ alternating (!useMatching) (b :: rest)
instance (useMatching : Bool) (path : List Point) : Decidable (alternating useMatching path) :=
  match path with
  | [] => isTrue True.intro
  | [_] => isTrue True.intro
  | _ :: b :: rest =>
    have := instDecidableAlternating (!useMatching) (b :: rest)
    inferInstanceAs (Decidable ((_ : Prop) ∧ alternating (!useMatching) (b :: rest)))

def allPaths : List (List Point) := [
  [(3,2), (4,2), (5,2), (6,2), (7,2), (7,3), (6,3), (6,4), (7,4), (7,5), (6,5), (5,5)],
  [(2,9), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (7,9), (6,9), (6,10), (7,10), (7,11)],
  [(5,6), (6,6), (7,6), (8,6), (9,6), (10,6), (11,6), (12,6)],
  [(7,12), (8,12), (9,12), (10,12), (11,12), (12,12)],
  [(12,2), (11,2), (10,2), (10,3), (11,3), (11,4), (10,4), (10,5), (11,5), (12,5)],
  [(12,10), (12,11)]]
def ppCycles : List (List Point) := [
  [(2,7), (3,7)],
  [(4,7), (5,7)],
  [(6,7), (7,7)],
  [(8,11), (9,11)],
  [(8,5), (9,5)],
  [(10,11), (11,11)],
  [(10,7), (11,7)],
  [(12,7), (13,7)]]
def terminalPairs : List (Point × Point) := [((3,2), (5,5)), ((2,9), (7,11)), ((5,6), (12,6)), ((7,12), (12,12)), ((12,2), (12,5)), ((12,10), (12,11))]
def allComponents : List (List Point) := allPaths ++ ppCycles

theorem decomposition_valid :
    (∀ path ∈ allPaths, alternating true path ∧ path.length % 2 = 0 ∧
      ¬ verticalPartner path.head! ∈ endpoints ∧
      ¬ verticalPartner path.getLast! ∈ endpoints) ∧
    (∀ path ∈ ppCycles, alternating true path ∧
      verticalPartner path.getLast! = path.head!) ∧
    allComponents.flatten.Nodup ∧
    (∀ v ∈ endpoints, v ∈ allComponents.flatten) ∧
    (∀ v ∈ allComponents.flatten, v ∈ endpoints) ∧
    allPaths.length = 6 ∧ ppCycles.length = 8 := by decide

theorem owner_types_valid :
    tp (3,2) ∧ tp (5,5) ∧ tp (12,2) ∧ tp (12,5) ∧
    bp (5,6) ∧ bp (12,6) ∧ tp (7,12) ∧ tp (12,12) ∧
    bp (2,9) ∧ bp (7,11) ∧ tp (12,10) ∧ bp (12,11) := by decide

def terminalMate (v : Point) : Point :=
  BTColumnCorridorObstruction.lookupMate v terminalPairs

def allowedLink (u v : Point) : Prop :=
  tp u ∧ bp v ∧ u.1 = v.1 ∧ adjacent u v ∧ terminalMate u ≠ v
instance (u v : Point) : Decidable (allowedLink u v) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _ ∧ _))

theorem fork_links_valid :
    allowedLink (5,5) (5,6) ∧ allowedLink (12,5) (12,6) ∧
    [(5,5),(5,6),(12,5),(12,6)].Nodup ∧
    terminalMate (5,5) = (3,2) ∧ terminalMate (12,5) = (12,2) ∧
    terminalMate (5,6) = (12,6) := by decide

-- The beta passes through PP column6 of band4. Its gap is bounded on
-- the other side by a pure two-edge PP cycle, not another open owner.
theorem interior_gap_geometry :
    (8,6) ∈ allPaths[2]! ∧ (9,6) ∈ allPaths[2]! ∧
    (∀ c ∈ [7,8,9,10], bb (8,c)) ∧
    [(8,11),(9,11)] ∈ ppCycles ∧
    (∀ path ∈ allPaths, (8,11) ∉ path ∧ (9,11) ∉ path) := by decide

theorem sizes_and_margin :
    selected.length = 21 ∧ matching.length = 33 ∧ endpoints.length = 66 ∧
    (43 : Int)+2-3 = 42 ∧ (16*14/2-21-33-16 : Int) = 42 := by decide

def copyPoint (i : Nat) (v : Point) : Point := (16*i+v.1,v.2)

/-- All occupied points in different copies are separated by blank rows. -/
theorem copies_no_occupied_adjacency (i j : Nat) (v w : Point)
    (different : i ≠ j) (vlow : 1≤v.1) (vhigh : v.1≤14)
    (wlow : 1≤w.1) (whigh : w.1≤14) :
    ¬ adjacent (copyPoint i v) (copyPoint j w) := by
  simp only [copyPoint,adjacent]
  omega

theorem copied_units_distinct (i j : Nat)
    (same : copyPoint i (8,7) = copyPoint j (8,7)) : i=j := by
  simp only [copyPoint,Prod.mk.injEq] at same
  omega

/-- Linear whole-board inventory and the reserved-interface gap.
The physical all-q adapter and optimality arguments remain written. -/
theorem stack_ledgers (q : Nat) :
    ((16*q)*14/2 : Int)-(21*q)-(33*q)-(16*q) = 42*q ∧
    (43*q : Int)+2*q-3*q = 42*q ∧
    (2*q : Int)-q = q := by omega

#print axioms geometry_valid
#print axioms mate_closed
#print axioms certificate_valid
#print axioms all_endpoints_frozen
#print axioms decomposition_valid
#print axioms owner_types_valid
#print axioms fork_links_valid
#print axioms interior_gap_geometry
#print axioms sizes_and_margin
#print axioms copies_no_occupied_adjacency
#print axioms copied_units_distinct
#print axioms stack_ledgers

end SubQuorum.FrozenBetaSupportFork
