import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 1600000

namespace SubQuorum.BTColumnCorridorObstruction

def extreme (lo hi : Nat) (side : Bool) : Nat := if side then hi else lo

/-- A gap has at most one paying terminal at either side. Replacing its
old interval choices by the two available extremes preserves injectivity. -/
theorem compressed_payment_injective (paid : Bool → Prop) (old : Bool → Nat)
    (lo hi : Nat)
    (bounded : ∀ s, paid s → lo ≤ old s ∧ old s ≤ hi)
    (injective : ∀ s t, paid s → paid t → old s = old t → s = t) :
    ∀ s t, paid s → paid t → extreme lo hi s = extreme lo hi t → s = t := by
  intro s t hs ht same
  cases s <;> cases t
  · rfl
  · have bounds0 := bounded false hs
    have bounds1 := bounded true ht
    have eq : old false = old true := by simp [extreme] at same; omega
    exact injective false true hs ht eq
  · have bounds1 := bounded true hs
    have bounds0 := bounded false ht
    have eq : old true = old false := by simp [extreme] at same; omega
    exact injective true false hs ht eq
  · rfl

theorem compressed_payment_available (available : Nat → Prop) (lo hi : Nat)
    (left : available lo) (right : available hi) (side : Bool) :
    available (extreme lo hi side) := by
  cases side
  · exact left
  · exact right

inductive Frozen {V : Type} (P T : V → Prop) (mate : V → V) (adj : V → V → Prop) :
    V → Prop where
  | ss {v a b : V} : P v → a ≠ b → adj v a → adj v b →
      T a → T b → Frozen P T mate adj v
  | sp {v a b : V} : P v → a ≠ b → adj v a → adj v b →
      T a → P b → Frozen P T mate adj (mate b) → Frozen P T mate adj v
  | ps {v a b : V} : P v → a ≠ b → adj v a → adj v b →
      P a → Frozen P T mate adj (mate a) → T b → Frozen P T mate adj v
  | pp {v a b : V} : P v → a ≠ b → adj v a → adj v b →
      P a → Frozen P T mate adj (mate a) →
      P b → Frozen P T mate adj (mate b) → Frozen P T mate adj v

theorem Frozen.step {V : Type} {P T : V → Prop} {mate : V → V}
    {adj : V → V → Prop} {v a b : V} (pv : P v) (distinct : a ≠ b)
    (va : adj v a) (vb : adj v b)
    (ha : T a ∨ (P a ∧ Frozen P T mate adj (mate a)))
    (hb : T b ∨ (P b ∧ Frozen P T mate adj (mate b))) : Frozen P T mate adj v := by
  rcases ha with ta | ⟨pa, fa⟩
  · rcases hb with tb | ⟨pb, fb⟩
    · exact Frozen.ss pv distinct va vb ta tb
    · exact Frozen.sp pv distinct va vb ta pb fb
  · rcases hb with tb | ⟨pb, fb⟩
    · exact Frozen.ps pv distinct va vb pa fa tb
    · exact Frozen.pp pv distinct va vb pa fa pb fb

theorem strict_rank_complete {V : Type} (P T : V → Prop) (mate : V → V)
    (adj : V → V → Prop) (rank : V → Nat)
    (closed : ∀ v, P v → P (mate v))
    (certificate : ∀ v, P v → ∃ a b, a ≠ b ∧ adj v a ∧ adj v b ∧
      (T a ∨ (P a ∧ rank (mate a) < rank v)) ∧
      (T b ∨ (P b ∧ rank (mate b) < rank v))) :
    ∀ v, P v → Frozen P T mate adj v := by
  have complete : ∀ n, ∀ v, rank v = n → P v → Frozen P T mate adj v := by
    intro n
    induction n using Nat.strongRecOn with
    | ind n ih =>
      intro v hv pv
      obtain ⟨a, b, distinct, va, vb, ha, hb⟩ := certificate v pv
      apply Frozen.step pv distinct va vb
      · rcases ha with selected | ⟨endpoint, lower⟩
        · exact Or.inl selected
        · exact Or.inr ⟨endpoint, ih (rank (mate a)) (by omega) (mate a) rfl (closed a endpoint)⟩
      · rcases hb with selected | ⟨endpoint, lower⟩
        · exact Or.inl selected
        · exact Or.inr ⟨endpoint, ih (rank (mate b)) (by omega) (mate b) rfl (closed b endpoint)⟩
  intro v pv
  exact complete (rank v) v rfl pv

abbrev Point := Nat × Nat

def adjacent (a b : Point) : Prop :=
  (a.1 = b.1 ∧ (a.2+1 = b.2 ∨ b.2+1 = a.2)) ∨
  (a.2 = b.2 ∧ (a.1+1 = b.1 ∨ b.1+1 = a.1))
instance (a b : Point) : Decidable (adjacent a b) :=
  inferInstanceAs (Decidable ((_ ∧ (_ ∨ _)) ∨ (_ ∧ (_ ∨ _))))

def selected : List Point := [(4, 1), (4, 3), (4, 5), (4, 7), (4, 9), (5, 2), (5, 8), (6, 6), (7, 5), (8, 6), (10, 2), (10, 8), (11, 1), (11, 3), (11, 5), (11, 7), (11, 9)]

def matching : List (Point × Point) := [((5, 3), (6, 3)), ((7, 3), (8, 3)), ((9, 3), (10, 3)), ((6, 4), (7, 4)), ((8, 4), (9, 4)), ((5, 4), (5, 5)), ((5, 6), (5, 7)), ((10, 4), (10, 5)), ((10, 6), (10, 7)), ((9, 5), (9, 6))]

def endpoints : List Point := matching.flatMap fun e => [e.1, e.2]
def lookupMate (v : Point) : List (Point × Point) → Point
  | [] => v
  | (a, b) :: rest => if v = a then b else if v = b then a else lookupMate v rest
def mate (v : Point) : Point := lookupMate v matching

def nonmateAdjacent (v w : Point) : Prop := adjacent v w ∧ w ≠ mate v
instance (v w : Point) : Decidable (nonmateAdjacent v w) :=
  inferInstanceAs (Decidable (_ ∧ _))

structure Witness where
  point : Point
  rank : Nat
  left : Point
  right : Point
  deriving Inhabited

def witnesses : List Witness := [
  ⟨(5, 3), 0, (4, 3), (5, 2)⟩,
  ⟨(5, 7), 0, (4, 7), (5, 8)⟩,
  ⟨(10, 3), 0, (10, 2), (11, 3)⟩,
  ⟨(10, 7), 0, (10, 8), (11, 7)⟩,
  ⟨(5, 5), 1, (4, 5), (5, 6)⟩,
  ⟨(9, 6), 1, (8, 6), (10, 6)⟩,
  ⟨(10, 5), 1, (10, 6), (11, 5)⟩,
  ⟨(6, 4), 2, (5, 4), (6, 3)⟩,
  ⟨(9, 4), 2, (9, 3), (9, 5)⟩,
  ⟨(7, 3), 3, (6, 3), (7, 4)⟩,
  ⟨(7, 4), 3, (7, 5), (8, 4)⟩,
  ⟨(8, 3), 3, (8, 4), (9, 3)⟩,
  ⟨(6, 3), 4, (6, 4), (7, 3)⟩,
  ⟨(8, 4), 4, (7, 4), (8, 3)⟩,
  ⟨(5, 4), 5, (5, 3), (6, 4)⟩,
  ⟨(9, 3), 5, (8, 3), (9, 4)⟩,
  ⟨(5, 6), 6, (5, 5), (6, 6)⟩,
  ⟨(10, 4), 6, (9, 4), (10, 3)⟩,
  ⟨(9, 5), 7, (9, 4), (10, 5)⟩,
  ⟨(10, 6), 8, (9, 6), (10, 5)⟩]

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
    (∀ v ∈ selected ++ endpoints, v.1 < 18 ∧ v.2 < 20) ∧
    (∀ v ∈ selected,
      ((selected ++ endpoints).filter fun w => decide (adjacent v w)).length ≤ 1) := by decide

theorem mate_closed : ∀ v ∈ endpoints, mate v ∈ endpoints := by decide
theorem certificate_valid : ∀ v ∈ endpoints, validAt v := by decide

theorem all_endpoints_frozen : ∀ v ∈ endpoints,
    Frozen (fun x => x ∈ endpoints) (fun x => x ∈ selected) mate nonmateAdjacent v := by
  apply strict_rank_complete (fun x => x ∈ endpoints) (fun x => x ∈ selected)
    mate nonmateAdjacent rank mate_closed
  intro v pv
  exact ⟨(record v).left, (record v).right, certificate_valid v pv⟩

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

def alphaPath : List Point := [(5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3)]
def mixedPairs : List (Point × Point) := [((5, 4), (5, 5)), ((5, 6), (5, 7)), ((9, 5), (9, 6)), ((10, 4), (10, 5)), ((10, 6), (10, 7))]
def terminalPairs : List (Point × Point) := [((5, 3), (10, 3)), ((5, 4), (5, 5)), ((5, 6), (5, 7)), ((9, 5), (9, 6)), ((10, 4), (10, 5)), ((10, 6), (10, 7))]
def tpTips : List Point := [(5, 3), (5, 5), (5, 7), (9, 6), (10, 3), (10, 5), (10, 7)]
def bpTips : List Point := [(5, 4), (5, 6), (9, 5), (10, 4), (10, 6)]

def allPaths : List (List Point) := alphaPath :: (mixedPairs.map fun e => [e.1, e.2])
-- Coincident actual and vertical edges are retained as two-edge PP cycles.
def ppCycles : List (List Point) := [[(6,4),(7,4)], [(8,4),(9,4)]]
def allComponents : List (List Point) := allPaths ++ ppCycles
def terminalMate (v : Point) : Point := lookupMate v terminalPairs

theorem decomposition_valid :
    (∀ path ∈ allPaths, alternating true path) ∧
    (∀ path ∈ ppCycles, alternating true path ∧
      verticalPartner (path.getLast!) = path.head!) ∧
    allComponents.flatten.Nodup ∧
    (∀ v ∈ endpoints, v ∈ allComponents.flatten) ∧
    (∀ v ∈ allComponents.flatten, v ∈ endpoints) ∧
    tp (5,3) ∧ tp (10,3) ∧
    (∀ e ∈ mixedPairs, (tp e.1 ∧ bp e.2) ∨ (bp e.1 ∧ tp e.2)) := by decide

theorem tip_lists_valid :
    (∀ v ∈ endpoints, tp v ↔ v ∈ tpTips) ∧
    (∀ v ∈ endpoints, bp v ↔ v ∈ bpTips) ∧
    (∀ e ∈ terminalPairs, ¬ (bp e.1 ∧ bp e.2)) := by decide

def reachableTips : List Point := [(5,3),(5,5),(5,7),(10,3),(10,5),(10,7)]
def allowedLink (u v : Point) : Prop :=
  tp u ∧ bp v ∧ u.1 = v.1 ∧ adjacent u v ∧ terminalMate u ≠ v
instance (u v : Point) : Decidable (allowedLink u v) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _ ∧ _))

def oldAccess (v : Point) : Prop :=
  (0 < v.2 ∧ bb (v.1,v.2-1)) ∨ bb (v.1,v.2+1) ∨
  (2 ≤ v.2 ∧ (v.1,v.2-1) ∈ selected ∧ blank (verticalPartner (v.1,v.2-1)) ∧ bb (v.1,v.2-2)) ∨
  ((v.1,v.2+1) ∈ selected ∧ blank (verticalPartner (v.1,v.2+1)) ∧ bb (v.1,v.2+2))
instance (v : Point) : Decidable (oldAccess v) :=
  inferInstanceAs (Decidable ((_ ∧ _) ∨ _ ∨ (_ ∧ _ ∧ _ ∧ _) ∨ (_ ∧ _ ∧ _)))

theorem closure_valid : ∀ u ∈ reachableTips, ∀ v ∈ bpTips,
    allowedLink u v → terminalMate v ∈ reachableTips := by decide
theorem no_old_access : ∀ u ∈ reachableTips, ¬ oldAccess u := by decide

inductive RelayReach : Point → Prop where
  | upper : RelayReach (5,3)
  | lower : RelayReach (10,3)
  | step {u v : Point} : RelayReach u → v ∈ bpTips → allowedLink u v → RelayReach (terminalMate v)

theorem all_routes_stay_inside {u : Point} (reachable : RelayReach u) : u ∈ reachableTips := by
  induction reachable with
  | upper => decide
  | lower => decide
  | @step u v _ member link ih => exact closure_valid u ih v member link

theorem no_reachable_old_exit {u : Point} (reachable : RelayReach u) : ¬ oldAccess u := by
  exact no_old_access u (all_routes_stay_inside reachable)

theorem two_link_exit : RelayReach (5,7) := by
  have first : RelayReach (5,5) := by
    change RelayReach (terminalMate (5,4))
    exact RelayReach.step RelayReach.upper (by decide) (by decide)
  change RelayReach (terminalMate (5,6))
  exact RelayReach.step first (by decide) (by decide)

theorem longer_corridor_witness :
    bt (5,8) ∧ bt (5,9) ∧ bb (5,10) ∧ 0 < (10 : Nat) ∧ 10 < 11 := by decide

theorem sizes_and_positive_packet_margin :
    selected.length = 17 ∧ matching.length = 10 ∧ endpoints.length = 20 ∧
    8*12/2-17-20/2-8 = (13 : Nat) := by decide

end SubQuorum.BTColumnCorridorObstruction

#print axioms SubQuorum.BTColumnCorridorObstruction.strict_rank_complete
#print axioms SubQuorum.BTColumnCorridorObstruction.compressed_payment_injective
#print axioms SubQuorum.BTColumnCorridorObstruction.compressed_payment_available
#print axioms SubQuorum.BTColumnCorridorObstruction.geometry_valid
#print axioms SubQuorum.BTColumnCorridorObstruction.mate_closed
#print axioms SubQuorum.BTColumnCorridorObstruction.certificate_valid
#print axioms SubQuorum.BTColumnCorridorObstruction.all_endpoints_frozen
#print axioms SubQuorum.BTColumnCorridorObstruction.decomposition_valid
#print axioms SubQuorum.BTColumnCorridorObstruction.tip_lists_valid
#print axioms SubQuorum.BTColumnCorridorObstruction.closure_valid
#print axioms SubQuorum.BTColumnCorridorObstruction.no_old_access
#print axioms SubQuorum.BTColumnCorridorObstruction.all_routes_stay_inside
#print axioms SubQuorum.BTColumnCorridorObstruction.no_reachable_old_exit
#print axioms SubQuorum.BTColumnCorridorObstruction.two_link_exit
#print axioms SubQuorum.BTColumnCorridorObstruction.longer_corridor_witness
#print axioms SubQuorum.BTColumnCorridorObstruction.sizes_and_positive_packet_margin
