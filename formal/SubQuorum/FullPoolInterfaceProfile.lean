import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.FullPoolInterfaceProfile

inductive Kind where
  | old | iface | upperOut | upperIn | upperEnd | lowerOut | lowerIn | lowerEnd
  deriving DecidableEq, Repr

abbrev Node := Nat × Kind
abbrev UnitID := Nat × Bool

def transition : Kind → Kind → Prop
  | .old, .upperOut | .old, .upperIn | .old, .lowerOut | .old, .lowerIn => True
  | .upperIn, .upperEnd | .lowerIn, .lowerEnd => True
  | _, _ => False

def Edge (u v : Node) : Prop := u.1=v.1 ∧ transition u.2 v.2

inductive Route (start : Node) : Node → Nat → Prop where
  | root : Route start start 0
  | step {u v : Node} {n : Nat} : Route start u n → Edge u v → Route start v (n+1)

/-- This is an arbitrary-length route invariant, for every copy index. -/
theorem route_copy_index {a b : Node} {n : Nat} (route : Route a b n) : a.1=b.1 := by
  induction route with
  | root => rfl
  | step _ edge ih => exact ih.trans edge.1

/-- No physical link in the compiled closure has the interface as target. -/
theorem no_incoming_interface (u v : Kind) (edge : transition u v) : v≠.iface := by
  cases u <;> cases v <;> simp_all [transition]

theorem old_route_not_interface (i : Nat) {v : Node} {n : Nat}
    (route : Route (i,.old) v n) : v.2≠.iface := by
  cases route with
  | root => change Kind.old≠Kind.iface; decide
  | step previous edge => exact no_incoming_interface _ _ edge.2

def Supports (repair : Nat → Prop) (v : Node) (j : UnitID) : Prop :=
  v.1=j.1 ∧ ((j.2=false ∧ (v.2=.iface ∨ v.2=.lowerEnd)) ∨
             (j.2=true ∧ v.2=.upperOut ∧ repair v.1))

/-- Every actual payment belongs to the route's original copy, even when
many source-free originals outside the closure exist on the board. -/
theorem payment_copy_index (repair : Nat → Prop) {a b : Node} {j : UnitID} {n : Nat}
    (route : Route a b n) (support : Supports repair b j) : a.1=j.1 :=
  (route_copy_index route).trans support.1

/-- Without a repair, every payable old route ends at that copy's one
original shared unit. Beta sinks are absent from this compiled closure. -/
theorem unrepaired_payment_unique (repair : Nat → Prop) (i : Nat)
    (unrepaired : ¬repair i) {v : Node} {j : UnitID} {n : Nat}
    (route : Route (i,.old) v n) (support : Supports repair v j) : j=(i,false) := by
  have copyIndex := route_copy_index route
  have paidIndex := payment_copy_index repair route support
  have bit : j.2=false := by
    cases support.2 with
    | inl shared => exact shared.1
    | inr priv =>
      have repaired : repair i := by simpa [←copyIndex] using priv.2.2
      exact False.elim (unrepaired repaired)
  exact Prod.ext paidIndex.symm bit

/-- Interface sources have no non-self exits, so any legal route has
length zero and their sole payment is the same shared original unit. -/
theorem interface_route_stationary (i : Nat) {v : Node} {n : Nat}
    (route : Route (i,.iface) v n) : v=(i,.iface) ∧ n=0 := by
  induction route with
  | root => exact ⟨rfl,rfl⟩
  | step previous edge ih =>
    have impossible := edge.2
    rw [ih.1] at impossible
    simp [transition] at impossible

theorem interface_payment_unique (repair : Nat → Prop) (i : Nat)
    {v : Node} {j : UnitID} {n : Nat}
    (route : Route (i,.iface) v n) (support : Supports repair v j) : j=(i,false) := by
  have stationary := interface_route_stationary i route
  have same := stationary.1
  subst v
  have bit : j.2=false := by
    cases support.2 with
    | inl shared => exact shared.1
    | inr priv => cases priv.2.1
  exact Prod.ext support.1.symm bit

/-- Paying both roots in an unrepaired copy reuses j, contradicting the
required injectivity. This is uniform in the number of stacked copies. -/
theorem unrepaired_two_root_collision (repair : Nat → Prop) (i : Nat)
    (unrepaired : ¬repair i) {oldExit interfaceExit : Node}
    {oldUnit interfaceUnit : UnitID} {oldLength interfaceLength : Nat}
    (oldRoute : Route (i,.old) oldExit oldLength)
    (newRoute : Route (i,.iface) interfaceExit interfaceLength)
    (oldSupported : Supports repair oldExit oldUnit)
    (newSupported : Supports repair interfaceExit interfaceUnit) : oldUnit=interfaceUnit :=
  (unrepaired_payment_unique repair i unrepaired oldRoute oldSupported).trans
    (interface_payment_unique repair i newRoute newSupported).symm

def level : Kind → Nat
  | .old | .iface => 0
  | .upperOut | .upperIn | .lowerOut | .lowerIn => 1
  | .upperEnd | .lowerEnd => 2

theorem transition_level (u v : Kind) (edge : transition u v) : level v≤level u+1 := by
  cases u <;> cases v <;> simp_all [transition,level]

theorem route_level_bound {a b : Node} {n : Nat} (route : Route a b n) :
    level b.2≤level a.2+n := by
  induction route with
  | root => omega
  | step _ edge ih =>
    have := transition_level _ _ edge.2
    omega

/-- Any old route paid on j uses at least two links; the interface's
zero-link route cannot silently substitute for that old source identity. -/
theorem old_shared_needs_two (repair : Nat → Prop) (i : Nat)
    {v : Node} {n : Nat} (route : Route (i,.old) v n)
    (support : Supports repair v (i,false)) : 2≤n := by
  have notInterface := old_route_not_interface i route
  have lower : v.2=.lowerEnd := by
    cases support.2 with
    | inl shared =>
      cases shared.2 with
      | inl no => exact False.elim (notInterface no)
      | inr yes => exact yes
    | inr priv => cases priv.1
  have bound := route_level_bound route
  simpa [level,lower] using bound

theorem old_private_needs_one (repair : Nat → Prop) (i : Nat)
    {v : Node} {n : Nat} (route : Route (i,.old) v n)
    (support : Supports repair v (i,true)) : 1≤n := by
  have upper : v.2=.upperOut := by
    cases support.2 with
    | inl shared => cases shared.1
    | inr priv => exact priv.2.1
  have bound := route_level_bound route
  simpa [level,upper] using bound

theorem explicit_old_lower_route (i : Nat) : Route (i,.old) (i,.lowerEnd) 2 := by
  have first : Route (i,.old) (i,.lowerIn) 1 := Route.step Route.root ⟨rfl,trivial⟩
  exact Route.step first ⟨rfl,trivial⟩

theorem explicit_old_upper_route (i : Nat) : Route (i,.old) (i,.upperOut) 1 := by
  exact Route.step Route.root ⟨rfl, trivial⟩

theorem repaired_distinct_payments (repair : Nat → Prop) (i : Nat) (fixed : repair i) :
    Supports repair (i,.upperOut) (i,true) ∧
    Supports repair (i,.iface) (i,false) ∧ (i,true)≠(i,false) := by
  refine ⟨⟨rfl,Or.inr ⟨rfl,rfl,fixed⟩⟩,⟨rfl,Or.inl ⟨rfl,Or.inl rfl⟩⟩,?_⟩
  intro same
  have := congrArg Prod.snd same
  cases this

theorem different_copies_distinct_units (i k : Nat) (a b : Bool) (different : i≠k) :
    (i,a)≠(k,b) := by
  intro same
  exact different (congrArg Prod.fst same)

/-- Sum the exact per-copy value and cost counts supplied by the written
finite-disjointness proof. These equalities do not assume full payment. -/
theorem aggregate_profile (q s : Nat) (subset : s≤q) :
    (q-s)+2*s=q+s ∧ 2*q-(q+s)=q-s ∧
    2*(q-s)+s=2*q-s ∧ (q+s)-q=s ∧
    (2*q-s)-s=2*(q-s) := by omega

theorem joint_withdrawal_defect (q lost removed : Int) :
    (q-(q-lost))+(q-(q-removed))-removed=lost := by omega

theorem numerical_slack (w q s : Int) (height : 8≤w) (copies : 1≤q) (repairs : 0≤s) :
    11*(q*(w+4)-2)-(41*q-s)-q*(3*w+10)=q*(8*w-7)+s-22 ∧
    0<q*(8*w-7)+s-22 := by
  constructor
  · simp only [Int.mul_add,Int.mul_sub]
    rw [Int.mul_left_comm q 8 w,Int.mul_left_comm q 3 w]
    omega
  · have h : 57≤8*w-7 := by omega
    have prod : 57≤q*(8*w-7) := by
      have : 1*(8*w-7)≤q*(8*w-7) := Int.mul_le_mul_of_nonneg_right copies (by omega)
      omega
    omega

abbrev Point := Nat × Nat
abbrev OriginalUnit := Nat × Nat × Nat
def selected : List Point := [(0, 1), (0, 3), (0, 5), (0, 7), (0, 9), (0, 11), (0, 13), (0, 15), (0, 17), (0, 19), (0, 21), (1, 0), (1, 2), (1, 10), (1, 12), (1, 20), (2, 8), (2, 18), (3, 3), (3, 7), (3, 13), (3, 17), (6, 3), (6, 8), (6, 13), (6, 18), (8, 0), (8, 2), (8, 10), (8, 12), (8, 20), (9, 1), (9, 3), (9, 5), (9, 7), (9, 9), (9, 13), (9, 15), (9, 17), (9, 19), (9, 21)]
def matching : List (Point × Point) := [((1, 5), (2, 5)), ((3, 5), (4, 5)), ((5, 5), (6, 5)), ((7, 5), (8, 5)), ((2, 6), (3, 6)), ((4, 6), (5, 6)), ((6, 6), (7, 6)), ((1, 6), (1, 7)), ((1, 8), (1, 9)), ((8, 6), (8, 7)), ((8, 8), (8, 9)), ((7, 7), (7, 8)), ((1, 3), (1, 4)), ((2, 4), (3, 4)), ((8, 3), (8, 4)), ((7, 4), (6, 4)), ((1, 15), (2, 15)), ((3, 15), (4, 15)), ((5, 15), (6, 15)), ((7, 15), (8, 15)), ((2, 16), (3, 16)), ((4, 16), (5, 16)), ((6, 16), (7, 16)), ((1, 16), (1, 17)), ((1, 18), (1, 19)), ((8, 16), (8, 17)), ((8, 18), (8, 19)), ((7, 17), (7, 18)), ((1, 13), (1, 14)), ((2, 14), (3, 14)), ((8, 13), (8, 14)), ((7, 14), (6, 14)), ((4, 4), (5, 4)), ((4, 14), (5, 14))]
def actualPairs : List (Point × Point) := [((1, 3), (1, 4)), ((1, 5), (8, 5)), ((1, 6), (1, 7)), ((1, 8), (1, 9)), ((1, 13), (8, 13)), ((2, 16), (3, 16)), ((4, 16), (5, 16)), ((6, 16), (7, 18)), ((7, 7), (7, 8)), ((8, 3), (8, 4)), ((8, 6), (8, 7)), ((8, 8), (8, 9))]
def ownerLinks : List (Nat × Nat) := [(1, 0), (1, 2), (1, 9), (1, 10), (2, 3), (5, 6), (10, 11)]
def closedOwners : List Nat := [0, 1, 2, 3, 4, 9, 10, 11]
def oldOwners : List Nat := [1]
def interfaceOwners : List Nat := [4]
def originalUnits : List OriginalUnit := [(1, 0, 0), (1, 1, 1), (1, 2, 2), (1, 9, 9), (1, 10, 10), (1, 11, 11), (1, 12, 12), (2, 0, 0), (2, 1, 1), (2, 2, 2), (2, 3, 3), (2, 7, 7), (2, 8, 8), (2, 9, 9), (2, 10, 10), (2, 11, 11), (2, 12, 12), (2, 13, 13), (3, 0, 0), (3, 1, 1), (3, 2, 2), (3, 9, 9), (3, 10, 10), (3, 11, 11), (3, 12, 12), (4, 11, 11), (7, 3, 3), (7, 4, 4), (7, 5, 5), (8, 2, 2), (8, 3, 3), (8, 4, 4), (8, 5, 5), (8, 6, 6), (8, 7, 7)]
def betaOwners : List Nat := [6,7]
def actualShared : OriginalUnit := (4,11,11)

def actualSupport (o : Nat) : List OriginalUnit :=
  match o with
  | 4 | 11 => [actualShared]
  | _ => []

def compiledKind (o : Nat) : Kind :=
  match o with
  | 0 => .upperOut
  | 1 => .old
  | 2 => .upperIn
  | 3 => .upperEnd
  | 4 => .iface
  | 9 => .lowerOut
  | 10 => .lowerIn
  | 11 => .lowerEnd
  | _ => .upperEnd

theorem actual_board_counts : selected.length=41 ∧ matching.length=34 ∧
    originalUnits.length=35 ∧ 10*22/2-41-34=35 ∧
    actualPairs[1]! = ((1,5),(8,5)) ∧ actualPairs[4]! = ((1,13),(8,13)) := by decide

theorem actual_closed_exit_support_table :
    (∀ o ∈ closedOwners, o ∉ betaOwners ∧
       (actualSupport o=[] ∨ actualSupport o=[actualShared])) ∧
    (∀ e ∈ ownerLinks, e.1 ∈ closedOwners →
       e.2 ∈ closedOwners ∧ transition (compiledKind e.1) (compiledKind e.2)) := by
  constructor
  · intro o mem
    simp only [closedOwners,List.mem_cons,List.not_mem_nil,or_false] at mem
    rcases mem with h|h|h|h|h|h|h|h <;> subst o <;> decide
  · intro e mem inside
    simp only [ownerLinks,List.mem_cons,List.not_mem_nil,or_false] at mem
    rcases mem with h|h|h|h|h|h|h <;> subst e <;>
      simp_all [closedOwners,compiledKind,transition]

#print axioms actual_board_counts
#print axioms actual_closed_exit_support_table

#print axioms route_copy_index
#print axioms no_incoming_interface
#print axioms old_route_not_interface
#print axioms payment_copy_index
#print axioms unrepaired_payment_unique
#print axioms interface_route_stationary
#print axioms interface_payment_unique
#print axioms unrepaired_two_root_collision
#print axioms transition_level
#print axioms route_level_bound
#print axioms old_shared_needs_two
#print axioms old_private_needs_one
#print axioms explicit_old_lower_route
#print axioms explicit_old_upper_route
#print axioms repaired_distinct_payments
#print axioms different_copies_distinct_units
#print axioms aggregate_profile
#print axioms joint_withdrawal_defect
#print axioms numerical_slack

end SubQuorum.FullPoolInterfaceProfile
