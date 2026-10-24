import SubQuorum.BTColumnCorridorObstruction

set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

namespace SubQuorum.FrozenSupportTreeReroot

abbrev Point := BTColumnCorridorObstruction.Point
abbrev adjacent := BTColumnCorridorObstruction.adjacent
abbrev Witness := BTColumnCorridorObstruction.Witness
abbrev verticalPartner := BTColumnCorridorObstruction.verticalPartner

def selected : List Point := [(1,8), (2,2), (2,4), (2,14), (3,2), (3,5), (3,9), (3,11), (3,15), (4,3), (4,6), (4,8), (4,10), (5,5), (5,7), (6,2), (6,6), (6,15), (7,16), (8,1), (8,15), (9,2), (9,4), (9,6), (9,8), (9,10), (9,12), (9,14), (9,16)]
def matching : List (Point × Point) := [((3,4), (4,4)), ((3,12), (4,12)), ((3,13), (3,14)), ((4,13), (5,13)), ((5,4), (6,4)), ((5,8), (6,8)), ((5,10), (6,10)), ((5,11), (5,12)), ((6,3), (7,3)), ((6,9), (7,9)), ((6,11), (6,12)), ((6,13), (6,14)), ((7,4), (7,5)), ((7,6), (7,7)), ((7,8), (8,8)), ((7,10), (7,11)), ((7,12), (7,13)), ((7,14), (8,14)), ((8,2), (8,3)), ((8,4), (8,5)), ((8,6), (8,7)), ((8,9), (8,10)), ((8,12), (8,13))]
def endpoints : List Point := matching.flatMap fun e => [e.1,e.2]
def mate (v : Point) : Point := BTColumnCorridorObstruction.lookupMate v matching
def nonmateAdjacent (v w : Point) : Prop := adjacent v w ∧ w ≠ mate v
instance (v w : Point) : Decidable (nonmateAdjacent v w) := inferInstanceAs (Decidable (_ ∧ _))
def witnesses : List Witness := [
  ⟨(3,4), 0, (2,4), (3,5)⟩,
  ⟨(3,14), 0, (2,14), (3,15)⟩,
  ⟨(5,8), 0, (4,8), (5,7)⟩,
  ⟨(8,2), 0, (8,1), (9,2)⟩,
  ⟨(8,14), 0, (8,15), (9,14)⟩,
  ⟨(3,12), 1, (3,11), (3,13)⟩,
  ⟨(5,4), 1, (4,4), (5,5)⟩,
  ⟨(6,14), 1, (6,15), (7,14)⟩,
  ⟨(8,4), 1, (8,3), (9,4)⟩,
  ⟨(4,13), 2, (3,13), (4,12)⟩,
  ⟨(6,3), 2, (6,2), (6,4)⟩,
  ⟨(7,13), 2, (6,13), (7,14)⟩,
  ⟨(8,6), 2, (8,5), (9,6)⟩,
  ⟨(5,12), 3, (4,12), (5,13)⟩,
  ⟨(6,12), 3, (6,13), (7,12)⟩,
  ⟨(7,4), 3, (6,4), (7,3)⟩,
  ⟨(8,8), 3, (8,7), (9,8)⟩,
  ⟨(8,12), 3, (7,12), (9,12)⟩,
  ⟨(5,10), 4, (4,10), (5,11)⟩,
  ⟨(7,6), 4, (6,6), (7,5)⟩,
  ⟨(7,7), 4, (7,8), (8,7)⟩,
  ⟨(7,11), 4, (6,11), (7,12)⟩,
  ⟨(6,9), 5, (6,8), (6,10)⟩,
  ⟨(6,10), 5, (6,11), (7,10)⟩,
  ⟨(6,11), 5, (5,11), (6,10)⟩,
  ⟨(7,5), 5, (7,6), (8,5)⟩,
  ⟨(7,8), 5, (6,8), (7,7)⟩,
  ⟨(7,9), 5, (7,8), (7,10)⟩,
  ⟨(8,10), 5, (7,10), (9,10)⟩,
  ⟨(5,11), 6, (5,10), (6,11)⟩,
  ⟨(6,8), 6, (6,9), (7,8)⟩,
  ⟨(6,13), 6, (5,13), (6,12)⟩,
  ⟨(7,3), 6, (7,4), (8,3)⟩,
  ⟨(7,10), 6, (6,10), (7,9)⟩,
  ⟨(8,7), 6, (7,7), (8,8)⟩,
  ⟨(8,9), 6, (7,9), (8,8)⟩,
  ⟨(5,13), 7, (5,12), (6,13)⟩,
  ⟨(6,4), 7, (6,3), (7,4)⟩,
  ⟨(7,12), 7, (6,12), (7,11)⟩,
  ⟨(8,5), 7, (7,5), (8,6)⟩,
  ⟨(4,4), 8, (4,3), (5,4)⟩,
  ⟨(4,12), 8, (4,13), (5,12)⟩,
  ⟨(7,14), 8, (6,14), (7,13)⟩,
  ⟨(8,3), 8, (7,3), (8,4)⟩,
  ⟨(3,13), 9, (3,12), (4,13)⟩,
  ⟨(8,13), 9, (7,13), (8,14)⟩]
def record (v : Point) : Witness := (witnesses.find? fun w => w.point == v).getD default
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
    (∀ v ∈ selected ++ endpoints, v.1 < 12 ∧ v.2 < 18) ∧
    (∀ v ∈ selected,
      ((selected ++ endpoints).filter fun w => decide (adjacent v w)).length ≤ 1) := by decide

theorem mate_closed : ∀ v ∈ endpoints, mate v ∈ endpoints := by decide
theorem certificate_valid : ∀ v ∈ endpoints, validAt v := by decide

theorem all_endpoints_frozen : ∀ v ∈ endpoints,
    BTColumnCorridorObstruction.Frozen (fun x => x ∈ endpoints)
      (fun x => x ∈ selected) mate nonmateAdjacent v := by
  apply BTColumnCorridorObstruction.strict_rank_complete
    (fun x => x ∈ endpoints) (fun x => x ∈ selected)
    mate nonmateAdjacent rank mate_closed
  intro v pv
  exact ⟨(record v).left, (record v).right, certificate_valid v pv⟩

def tp (v : Point) : Prop := v ∈ endpoints ∧ verticalPartner v ∈ selected
def bp (v : Point) : Prop := v ∈ endpoints ∧ verticalPartner v ∉ selected ∧ verticalPartner v ∉ endpoints
def blank (v : Point) : Prop := v ∉ selected ∧ v ∉ endpoints
instance (v : Point) : Decidable (tp v) := inferInstanceAs (Decidable (_ ∧ _))
instance (v : Point) : Decidable (bp v) := inferInstanceAs (Decidable (_ ∧ _ ∧ _))
instance (v : Point) : Decidable (blank v) := inferInstanceAs (Decidable (_ ∧ _))
def bb (v : Point) : Prop := blank v ∧ blank (verticalPartner v)
instance (v : Point) : Decidable (bb v) := inferInstanceAs (Decidable (_ ∧ _))

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

def allPaths : List (List Point) := [[(3,12), (4,12), (5,12), (5,11)],
  [(3,13), (3,14)],
  [(3,4), (4,4), (5,4), (6,4), (7,4), (7,5)],
  [(5,10), (6,10), (7,10), (7,11), (6,11), (6,12), (7,12), (7,13), (6,13), (6,14), (7,14), (8,14)],
  [(5,8), (6,8), (7,8), (8,8)],
  [(7,6), (7,7)],
  [(8,9), (8,10)],
  [(8,12), (8,13)],
  [(8,2), (8,3)],
  [(8,4), (8,5)],
  [(8,6), (8,7)]]
def ppCycles : List (List Point) := [[(4,13), (5,13)], [(6,3), (7,3)], [(6,9), (7,9)]]
def alphaA : List Point := [(5,8), (6,8), (7,8), (8,8)]
def alphaB : List Point := [(5,10), (6,10), (7,10), (7,11), (6,11), (6,12), (7,12), (7,13), (6,13), (6,14), (7,14), (8,14)]
def betaPath : List Point := [(3,12), (4,12), (5,12), (5,11)]
def allComponents : List (List Point) := allPaths ++ ppCycles
def terminalPairs : List (Point × Point) := allPaths.map fun path => (path.head!,path.getLast!)
def terminalMate (v : Point) : Point := BTColumnCorridorObstruction.lookupMate v terminalPairs

theorem decomposition_valid :
    (∀ path ∈ allPaths, alternating true path) ∧
    (∀ path ∈ ppCycles, alternating true path ∧ verticalPartner path.getLast! = path.head!) ∧
    allComponents.flatten.Nodup ∧
    (∀ v ∈ endpoints, v ∈ allComponents.flatten) ∧
    (∀ v ∈ allComponents.flatten, v ∈ endpoints) ∧
    alphaA ∈ allPaths ∧ alphaB ∈ allPaths ∧ betaPath ∈ allPaths := by decide

theorem terminal_inventory :
    (terminalPairs.filter fun e => decide (tp e.1 ∧ tp e.2)) = [((5,10),(8,14)),((5,8),(8,8))] ∧
    (terminalPairs.filter fun e => decide (bp e.1 ∧ bp e.2)) = [((3,12),(5,11))] ∧
    (∀ path ∈ allPaths, (tp path.head! ∨ bp path.head!) ∧ (tp path.getLast! ∨ bp path.getLast!)) := by decide

def allowedLink (u v : Point) : Prop :=
  tp u ∧ bp v ∧ u.1 = v.1 ∧ adjacent u v ∧ terminalMate u ≠ v
instance (u v : Point) : Decidable (allowedLink u v) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _ ∧ _))

theorem direct_beta_asymmetry :
    (∀ a ∈ [(5,8),(8,8)], ∀ b ∈ [(3,12),(5,11)], ¬ allowedLink a b) ∧
    allowedLink (5,10) (5,11) ∧
    ¬ allowedLink (8,14) (3,12) ∧ ¬ allowedLink (8,14) (5,11) := by decide

def sameGap (v target : Point) : Prop :=
  v.1/2 = target.1/2 ∧
  ∀ c ∈ List.range 18,
    ((v.2 < c ∧ c ≤ target.2) ∨ (target.2 ≤ c ∧ c < v.2)) →
      (2*(v.1/2),c) ∉ endpoints ∧ (2*(v.1/2)+1,c) ∉ endpoints
instance (v target : Point) : Decidable (sameGap v target) :=
  inferInstanceAs (Decidable (_ ∧ _))
def supportAt (path : List Point) (target : Point) : Prop :=
  ∃ v ∈ path, sameGap v target
instance (path : List Point) (target : Point) : Decidable (supportAt path target) :=
  inferInstanceAs (Decidable (∃ v ∈ path, sameGap v target))
def unmarkedBB : List Point :=
  ((List.range 6).flatMap fun b => (List.range 18).map fun c => (2*b,c)).filter
    fun v => decide (0 < v.2 ∧ v.2 < 17 ∧ bb v)

theorem support_sees_only_shared_unmarked_unit :
    (4,9) ∈ unmarkedBB ∧
    (∀ j ∈ unmarkedBB, supportAt alphaA j ↔ j = (4,9)) ∧
    (∀ j ∈ unmarkedBB, supportAt alphaB j ↔ j = (4,9)) := by decide

theorem two_marked_boundary_exits :
    bb (6,17) ∧ bb (8,17) ∧ supportAt alphaB (6,17) ∧ supportAt alphaB (8,17) ∧
    (6,17) ∉ unmarkedBB ∧ (8,17) ∉ unmarkedBB := by decide

theorem shared_gap_is_singleton :
    bb (4,9) ∧ (5,8) ∈ endpoints ∧ (5,10) ∈ endpoints ∧
    tp (5,8) ∧ tp (5,10) := by decide

theorem wider_mixed_alternative :
    allowedLink (8,8) (8,9) ∧ ((8,9),(8,10)) ∈ terminalPairs ∧
    tp (8,10) ∧ bb (8,11) ∧ (8,11) ∈ unmarkedBB ∧ (4,9) ≠ (8,11) := by decide

theorem exact_geometry_counts :
    selected.length = 29 ∧ matching.length = 23 ∧ endpoints.length = 46 ∧
    12*18/2 - 29 - 23 - 12 = (44 : Nat) := by decide

theorem stacked_ledger (q : Int) :
    108*q - 29*q - 23*q - 12*q = 44*q := by omega

end SubQuorum.FrozenSupportTreeReroot

#print axioms SubQuorum.FrozenSupportTreeReroot.geometry_valid
#print axioms SubQuorum.FrozenSupportTreeReroot.mate_closed
#print axioms SubQuorum.FrozenSupportTreeReroot.certificate_valid
#print axioms SubQuorum.FrozenSupportTreeReroot.all_endpoints_frozen
#print axioms SubQuorum.FrozenSupportTreeReroot.decomposition_valid
#print axioms SubQuorum.FrozenSupportTreeReroot.terminal_inventory
#print axioms SubQuorum.FrozenSupportTreeReroot.direct_beta_asymmetry
#print axioms SubQuorum.FrozenSupportTreeReroot.support_sees_only_shared_unmarked_unit
#print axioms SubQuorum.FrozenSupportTreeReroot.two_marked_boundary_exits
#print axioms SubQuorum.FrozenSupportTreeReroot.shared_gap_is_singleton
#print axioms SubQuorum.FrozenSupportTreeReroot.wider_mixed_alternative
#print axioms SubQuorum.FrozenSupportTreeReroot.exact_geometry_counts
#print axioms SubQuorum.FrozenSupportTreeReroot.stacked_ledger
