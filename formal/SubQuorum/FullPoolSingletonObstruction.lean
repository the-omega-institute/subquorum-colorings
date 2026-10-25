import SubQuorum.BTColumnCorridorObstruction

set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

namespace SubQuorum.FullPoolSingletonObstruction
open SubQuorum.BTColumnCorridorObstruction (Frozen Point adjacent)

inductive Reach {O : Type} (edge : O → O → Prop) (a : O) : O → Prop where
  | root : Reach edge a a
  | step {u v : O} : Reach edge a u → edge u v → Reach edge a v

theorem reach_stays_closed {O : Type} (edge : O → O → Prop) (closed : O → Prop)
    (stable : ∀ u v, closed u → edge u v → closed v)
    {a b : O} (start : closed a) (route : Reach edge a b) : closed b := by
  induction route with
  | root => exact start
  | step _ edge ih => exact stable _ _ ih edge

/-- A cut invariant applies to arbitrary routes, not a fixed prior matching.
The written no-beta cancellation decomposition supplies these routes. -/
theorem singleton_payments_unique {O R D : Type} (edge : O → O → Prop)
    (closed : O → Prop) (support : O → R → Prop) (unit : R)
    (stable : ∀ u v, closed u → edge u v → closed v)
    (onlyUnit : ∀ o r, closed o → support o r → r=unit)
    (root exit : D → O) (payment : D → R)
    (starts : ∀ d, closed (root d))
    (routes : ∀ d, Reach edge (root d) (exit d))
    (supported : ∀ d, support (exit d) (payment d))
    (distinct : ∀ a b, payment a=payment b → a=b) : ∀ a b : D, a=b := by
  intro a b
  have ha := onlyUnit _ _ (reach_stays_closed edge closed stable (starts a) (routes a)) (supported a)
  have hb := onlyUnit _ _ (reach_stays_closed edge closed stable (starts b) (routes b)) (supported b)
  exact distinct a b (ha.trans hb.symm)

theorem no_two_distinct_singleton_payments {D R : Type} (payment : D → R) (unit : R)
    (a b : D) (different : a ≠ b) (paidA : payment a=unit) (paidB : payment b=unit) :
    ¬ (∀ x y, payment x=payment y → x=y) := by
  intro injective
  exact different (injective a b (paidA.trans paidB.symm))

theorem raw_ledger (w : Nat) :
    (w+12)*22=2*(41+(3*w+10)+(8*w+81)) ∧
    (8*w+83)-2=8*w+81 := by omega

theorem original_marked_ledger (w : Nat) :
    (w+12)*22=2*(37+(3*w+10)+(w+12)+(7*w+73)) := by omega

theorem stack_ledger (w q : Nat) :
    q*((w+12)*22)=2*(q*41+q*(3*w+10)+q*(8*w+81)) := by
  have h := congrArg (fun n : Nat => q*n) (raw_ledger w).1
  simpa only [Nat.mul_add, Nat.mul_assoc, Nat.mul_left_comm q 2] using h

def selected : List Point := [(4,1), (4,3), (4,5), (4,7), (4,9), (4,11), (4,13), (4,15), (4,17), (4,19), (4,21), (5,0), (5,2), (5,10), (5,12), (5,20), (6,8), (6,18), (7,3), (7,7), (7,13), (7,17), (10,3), (10,8), (10,13), (10,18), (12,0), (12,2), (12,10), (12,12), (12,20), (13,1), (13,3), (13,5), (13,7), (13,9), (13,13), (13,15), (13,17), (13,19), (13,21)]
def matching : List (Point × Point) := [((5,5), (6,5)), ((7,5), (8,5)), ((9,5), (10,5)), ((11,5), (12,5)), ((6,6), (7,6)), ((8,6), (9,6)), ((10,6), (11,6)), ((5,6), (5,7)), ((5,8), (5,9)), ((12,6), (12,7)), ((12,8), (12,9)), ((11,7), (11,8)), ((5,3), (5,4)), ((6,4), (7,4)), ((12,3), (12,4)), ((11,4), (10,4)), ((5,15), (6,15)), ((7,15), (8,15)), ((9,15), (10,15)), ((11,15), (12,15)), ((6,16), (7,16)), ((8,16), (9,16)), ((10,16), (11,16)), ((5,16), (5,17)), ((5,18), (5,19)), ((12,16), (12,17)), ((12,18), (12,19)), ((11,17), (11,18)), ((5,13), (5,14)), ((6,14), (7,14)), ((12,13), (12,14)), ((11,14), (10,14)), ((8,4), (9,4)), ((8,14), (9,14))]
def endpoints : List Point := matching.flatMap fun e => [e.1,e.2]
def mate (v : Point) : Point := BTColumnCorridorObstruction.lookupMate v matching
def nonmateAdjacent (v w : Point) : Prop := adjacent v w ∧ w ≠ mate v
instance (v w : Point) : Decidable (nonmateAdjacent v w) := inferInstanceAs (Decidable (_ ∧ _))
def witnesses : List BTColumnCorridorObstruction.Witness := [
  ⟨(5,3), 0, (4,3), (5,2)⟩,
  ⟨(5,4), 7, (5,5), (6,4)⟩,
  ⟨(5,5), 1, (4,5), (5,4)⟩,
  ⟨(5,6), 7, (5,5), (6,6)⟩,
  ⟨(5,7), 1, (4,7), (5,8)⟩,
  ⟨(5,8), 8, (5,7), (6,8)⟩,
  ⟨(5,9), 0, (4,9), (5,10)⟩,
  ⟨(5,13), 0, (4,13), (5,12)⟩,
  ⟨(5,14), 7, (5,15), (6,14)⟩,
  ⟨(5,15), 1, (4,15), (5,14)⟩,
  ⟨(5,16), 7, (5,15), (6,16)⟩,
  ⟨(5,17), 1, (4,17), (5,18)⟩,
  ⟨(5,18), 8, (5,17), (6,18)⟩,
  ⟨(5,19), 0, (4,19), (5,20)⟩,
  ⟨(6,4), 2, (5,4), (6,5)⟩,
  ⟨(6,5), 6, (6,4), (6,6)⟩,
  ⟨(6,6), 2, (5,6), (6,5)⟩,
  ⟨(6,14), 2, (5,14), (6,15)⟩,
  ⟨(6,15), 6, (6,14), (6,16)⟩,
  ⟨(6,16), 2, (5,16), (6,15)⟩,
  ⟨(7,4), 5, (7,3), (8,4)⟩,
  ⟨(7,5), 3, (6,5), (7,4)⟩,
  ⟨(7,6), 5, (7,7), (8,6)⟩,
  ⟨(7,14), 5, (7,13), (8,14)⟩,
  ⟨(7,15), 3, (6,15), (7,14)⟩,
  ⟨(7,16), 5, (7,17), (8,16)⟩,
  ⟨(8,4), 4, (7,4), (8,5)⟩,
  ⟨(8,5), 5, (8,4), (8,6)⟩,
  ⟨(8,6), 4, (7,6), (8,5)⟩,
  ⟨(8,14), 4, (7,14), (8,15)⟩,
  ⟨(8,15), 5, (8,14), (8,16)⟩,
  ⟨(8,16), 4, (7,16), (8,15)⟩,
  ⟨(9,4), 4, (9,5), (10,4)⟩,
  ⟨(9,5), 5, (8,5), (9,4)⟩,
  ⟨(9,6), 4, (9,5), (10,6)⟩,
  ⟨(9,14), 4, (9,15), (10,14)⟩,
  ⟨(9,15), 5, (8,15), (9,14)⟩,
  ⟨(9,16), 4, (9,15), (10,16)⟩,
  ⟨(10,4), 5, (9,4), (10,3)⟩,
  ⟨(10,5), 3, (10,4), (10,6)⟩,
  ⟨(10,6), 6, (9,6), (10,5)⟩,
  ⟨(10,14), 5, (9,14), (10,13)⟩,
  ⟨(10,15), 3, (10,14), (10,16)⟩,
  ⟨(10,16), 6, (9,16), (10,15)⟩,
  ⟨(11,4), 2, (11,5), (12,4)⟩,
  ⟨(11,5), 6, (10,5), (11,4)⟩,
  ⟨(11,6), 2, (11,5), (11,7)⟩,
  ⟨(11,7), 8, (11,6), (12,7)⟩,
  ⟨(11,8), 1, (10,8), (12,8)⟩,
  ⟨(11,14), 2, (11,15), (12,14)⟩,
  ⟨(11,15), 6, (10,15), (11,14)⟩,
  ⟨(11,16), 2, (11,15), (11,17)⟩,
  ⟨(11,17), 8, (11,16), (12,17)⟩,
  ⟨(11,18), 1, (10,18), (12,18)⟩,
  ⟨(12,3), 0, (12,2), (13,3)⟩,
  ⟨(12,4), 7, (11,4), (12,5)⟩,
  ⟨(12,5), 1, (12,4), (13,5)⟩,
  ⟨(12,6), 7, (11,6), (12,5)⟩,
  ⟨(12,7), 1, (12,8), (13,7)⟩,
  ⟨(12,8), 9, (11,8), (12,7)⟩,
  ⟨(12,9), 0, (12,10), (13,9)⟩,
  ⟨(12,13), 0, (12,12), (13,13)⟩,
  ⟨(12,14), 7, (11,14), (12,15)⟩,
  ⟨(12,15), 1, (12,14), (13,15)⟩,
  ⟨(12,16), 7, (11,16), (12,15)⟩,
  ⟨(12,17), 1, (12,18), (13,17)⟩,
  ⟨(12,18), 9, (11,18), (12,17)⟩,
  ⟨(12,19), 0, (12,20), (13,19)⟩]
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
    (∀ v ∈ selected ++ endpoints, v.1<20 ∧ v.2<22) ∧
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
def ownerSupport : List (Nat × List Point) := [(0, []), (1, []), (2, []), (3, []), (4, []), (5, []), (6, []), (7, []), (8, [(5,9), (5,10), (5,11), (5,12)]), (9, [(5,19), (5,20), (5,21)]), (10, []), (11, []), (12, [(6,11)]), (13, [(6,11)]), (14, []), (15, [])]

theorem sources_inside : 1 ∈ reachableOwners ∧ 5 ∈ reachableOwners := by decide

theorem reachable_closed : ∀ e ∈ ownerLinks,
    e.1 ∈ reachableOwners → e.2 ∈ reachableOwners := by decide

theorem reachable_support_singleton : ∀ e ∈ ownerSupport,
    e.1 ∈ reachableOwners → ∀ j ∈ e.2, j=(6,11) := by decide

theorem both_have_singleton_witness :
    (12,[(6,11)]) ∈ ownerSupport ∧ (13,[(6,11)]) ∈ ownerSupport ∧
    (1,11) ∈ ownerLinks ∧ (11,12) ∈ ownerLinks ∧ (5,13) ∈ ownerLinks := by decide

#print axioms reach_stays_closed
#print axioms singleton_payments_unique
#print axioms no_two_distinct_singleton_payments
#print axioms raw_ledger
#print axioms original_marked_ledger
#print axioms stack_ledger
#print axioms geometry_valid
#print axioms mate_closed
#print axioms certificate_valid
#print axioms all_endpoints_frozen
#print axioms sources_inside
#print axioms reachable_closed
#print axioms reachable_support_singleton
#print axioms both_have_singleton_witness

end SubQuorum.FullPoolSingletonObstruction
