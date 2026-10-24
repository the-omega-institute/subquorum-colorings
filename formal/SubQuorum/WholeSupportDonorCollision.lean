import SubQuorum.BTColumnCorridorObstruction

set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

namespace SubQuorum.WholeSupportDonorCollision
open SubQuorum.BTColumnCorridorObstruction (Frozen Point adjacent)

/-- Adding endpoints with unchanged old mates preserves every old derivation,
provided the old nonmate witnesses remain valid. -/
theorem frozen_extend_endpoints {V : Type} (P Q T : V → Prop)
    (oldMate newMate : V → V) (oldAdj newAdj : V → V → Prop)
    (endpoints : ∀ v, P v → Q v)
    (mates : ∀ v, P v → newMate v=oldMate v)
    (adjacency : ∀ v, P v → ∀ w, oldAdj v w → newAdj v w)
    {v : V} (frozen : Frozen P T oldMate oldAdj v) : Frozen Q T newMate newAdj v := by
  induction frozen with
  | ss pv distinct va vb ta tb =>
    exact Frozen.ss (endpoints _ pv) distinct (adjacency _ pv _ va) (adjacency _ pv _ vb) ta tb
  | sp pv distinct va vb ta pb _ ih =>
    apply Frozen.sp (endpoints _ pv) distinct (adjacency _ pv _ va) (adjacency _ pv _ vb) ta (endpoints _ pb)
    simpa only [mates _ pb] using ih
  | ps pv distinct va vb pa _ tb ih =>
    apply Frozen.ps (endpoints _ pv) distinct (adjacency _ pv _ va) (adjacency _ pv _ vb) (endpoints _ pa)
    · simpa only [mates _ pa] using ih
    · exact tb
  | pp pv distinct va vb pa _ pb _ ihA ihB =>
    apply Frozen.pp (endpoints _ pv) distinct (adjacency _ pv _ va) (adjacency _ pv _ vb) (endpoints _ pa)
    · simpa only [mates _ pa] using ihA
    · exact endpoints _ pb
    · simpa only [mates _ pb] using ihB

def predecessor {V : Type} (boundary : V) (paired : Nat → V) (i : Nat) : V :=
  if i=0 then boundary else paired (i-1)

/-- One orientation of an arbitrary-length PP seal. Each new vertex has one
already retained side witness; its other witness's mate is the prior vertex.
Apply this to upper endpoints from top to bottom, and to lower endpoints
in reverse order with the lower boundary. -/
theorem oriented_seal_frozen {V : Type} (P T : V → Prop) (mate : V → V)
    (adj : V → V → Prop) (vertex paired side : Nat → V) (boundary : V) (n : Nat)
    (vertexP : ∀ i, i<n → P (vertex i))
    (pairedP : ∀ i, i<n → P (paired i))
    (pairedMate : ∀ i, i<n → mate (paired i)=vertex i)
    (sideRetained : ∀ i, i<n → P (side i) ∧ Frozen P T mate adj (mate (side i)))
    (boundaryRetained : P boundary ∧ Frozen P T mate adj (mate boundary))
    (witnesses : ∀ i, i<n → side i ≠ predecessor boundary paired i ∧
      adj (vertex i) (side i) ∧ adj (vertex i) (predecessor boundary paired i)) :
    ∀ i, i<n → Frozen P T mate adj (vertex i) := by
  intro i
  induction i with
  | zero =>
    intro hi
    obtain ⟨different,va,vb⟩ := witnesses 0 hi
    apply Frozen.pp (vertexP 0 hi) different va vb
      (sideRetained 0 hi).1 (sideRetained 0 hi).2
    · simpa only [predecessor,ite_true] using boundaryRetained.1
    · simpa only [predecessor,ite_true] using boundaryRetained.2
  | succ i ih =>
    intro hi
    obtain ⟨different,va,vb⟩ := witnesses (i+1) hi
    apply Frozen.pp (vertexP (i+1) hi) different va vb
      (sideRetained (i+1) hi).1 (sideRetained (i+1) hi).2
    · simpa only [predecessor,Nat.add_eq_zero_iff,Nat.one_ne_zero,and_false,ite_false,
                  Nat.add_sub_cancel] using pairedP i (by omega)
    · simp only [predecessor,Nat.add_eq_zero_iff,Nat.one_ne_zero,and_false,ite_false,
                 Nat.add_sub_cancel]
      rw [pairedMate i (by omega)]
      exact ih (by omega)

theorem upper_seal_contacts (c i : Nat) :
    (8+2*i,c+1) ≠ (7+2*i,c) ∧
    adjacent (8+2*i,c) (8+2*i,c+1) ∧
    adjacent (8+2*i,c) (7+2*i,c) ∧
    (8+2*i,c+1) ≠ (9+2*i,c) ∧ (7+2*i,c) ≠ (9+2*i,c) := by
  simp [adjacent] <;> omega

theorem lower_seal_contacts (c n k : Nat) (hk : k<n) :
    (7+2*n-2*k,c+1) ≠ (8+2*n-2*k,c) ∧
    adjacent (7+2*n-2*k,c) (7+2*n-2*k,c+1) ∧
    adjacent (7+2*n-2*k,c) (8+2*n-2*k,c) ∧
    (7+2*n-2*k,c+1) ≠ (6+2*n-2*k,c) ∧
    (8+2*n-2*k,c) ≠ (6+2*n-2*k,c) := by
  simp [adjacent] <;> omega

theorem seal_packet_ledger (w : Nat) (hw : 8≤w) :
    (w+2)*22 = 2*(34+(3*w+10)+(w+2)+(7*w-24)) := by omega

theorem collision_and_repair_ledgers (i : Nat) (hi : 2≤i) :
    (i : Int)-2 = (i-1 : Nat)-1 ∧ (i : Int)-2 = (i-2 : Nat) := by omega

-- Concrete data and strict-rank certificate are inserted below from the
-- permanent W=8 fixture; the all-height geometric adapter remains written.

def selected : List Point := [(4,3), (4,5), (4,7), (4,9), (4,13), (4,15), (4,17), (4,19), (5,2), (5,10), (5,12), (5,20), (6,8), (6,18), (7,3), (7,7), (7,13), (7,17), (10,3), (10,8), (10,13), (10,18), (12,2), (12,10), (12,12), (12,20), (13,3), (13,5), (13,7), (13,9), (13,13), (13,15), (13,17), (13,19)]
def matching : List (Point × Point) := [((5,5), (6,5)), ((7,5), (8,5)), ((9,5), (10,5)), ((11,5), (12,5)), ((6,6), (7,6)), ((8,6), (9,6)), ((10,6), (11,6)), ((5,6), (5,7)), ((5,8), (5,9)), ((12,6), (12,7)), ((12,8), (12,9)), ((11,7), (11,8)), ((5,3), (5,4)), ((6,4), (7,4)), ((12,3), (12,4)), ((11,4), (10,4)), ((5,15), (6,15)), ((7,15), (8,15)), ((9,15), (10,15)), ((11,15), (12,15)), ((6,16), (7,16)), ((8,16), (9,16)), ((10,16), (11,16)), ((5,16), (5,17)), ((5,18), (5,19)), ((12,16), (12,17)), ((12,18), (12,19)), ((11,17), (11,18)), ((5,13), (5,14)), ((6,14), (7,14)), ((12,13), (12,14)), ((11,14), (10,14)), ((8,4), (9,4)), ((8,14), (9,14))]
def endpoints : List Point := matching.flatMap fun e => [e.1,e.2]
def mate (v : Point) : Point := BTColumnCorridorObstruction.lookupMate v matching
def nonmateAdjacent (v w : Point) : Prop := adjacent v w ∧ w ≠ mate v
instance (v w : Point) : Decidable (nonmateAdjacent v w) := inferInstanceAs (Decidable (_ ∧ _))
def witnesses : List BTColumnCorridorObstruction.Witness := [
  ⟨(5,3), 0, (4,3), (5,2)⟩,
  ⟨(5,9), 0, (4,9), (5,10)⟩,
  ⟨(5,13), 0, (4,13), (5,12)⟩,
  ⟨(5,19), 0, (4,19), (5,20)⟩,
  ⟨(12,3), 0, (12,2), (13,3)⟩,
  ⟨(12,9), 0, (12,10), (13,9)⟩,
  ⟨(12,13), 0, (12,12), (13,13)⟩,
  ⟨(12,19), 0, (12,20), (13,19)⟩,
  ⟨(5,5), 1, (4,5), (5,4)⟩,
  ⟨(5,7), 1, (4,7), (5,8)⟩,
  ⟨(5,15), 1, (4,15), (5,14)⟩,
  ⟨(5,17), 1, (4,17), (5,18)⟩,
  ⟨(11,8), 1, (10,8), (12,8)⟩,
  ⟨(11,18), 1, (10,18), (12,18)⟩,
  ⟨(12,5), 1, (12,4), (13,5)⟩,
  ⟨(12,7), 1, (12,8), (13,7)⟩,
  ⟨(12,15), 1, (12,14), (13,15)⟩,
  ⟨(12,17), 1, (12,18), (13,17)⟩,
  ⟨(6,4), 2, (5,4), (6,5)⟩,
  ⟨(6,6), 2, (5,6), (6,5)⟩,
  ⟨(6,14), 2, (5,14), (6,15)⟩,
  ⟨(6,16), 2, (5,16), (6,15)⟩,
  ⟨(11,4), 2, (11,5), (12,4)⟩,
  ⟨(11,6), 2, (11,5), (11,7)⟩,
  ⟨(11,14), 2, (11,15), (12,14)⟩,
  ⟨(11,16), 2, (11,15), (11,17)⟩,
  ⟨(7,5), 3, (6,5), (7,4)⟩,
  ⟨(7,15), 3, (6,15), (7,14)⟩,
  ⟨(10,5), 3, (10,4), (10,6)⟩,
  ⟨(10,15), 3, (10,14), (10,16)⟩,
  ⟨(8,4), 4, (7,4), (8,5)⟩,
  ⟨(8,6), 4, (7,6), (8,5)⟩,
  ⟨(8,14), 4, (7,14), (8,15)⟩,
  ⟨(8,16), 4, (7,16), (8,15)⟩,
  ⟨(9,4), 4, (9,5), (10,4)⟩,
  ⟨(9,6), 4, (9,5), (10,6)⟩,
  ⟨(9,14), 4, (9,15), (10,14)⟩,
  ⟨(9,16), 4, (9,15), (10,16)⟩,
  ⟨(7,4), 5, (7,3), (8,4)⟩,
  ⟨(7,6), 5, (7,7), (8,6)⟩,
  ⟨(7,14), 5, (7,13), (8,14)⟩,
  ⟨(7,16), 5, (7,17), (8,16)⟩,
  ⟨(8,5), 5, (8,4), (8,6)⟩,
  ⟨(8,15), 5, (8,14), (8,16)⟩,
  ⟨(9,5), 5, (8,5), (9,4)⟩,
  ⟨(9,15), 5, (8,15), (9,14)⟩,
  ⟨(10,4), 5, (9,4), (10,3)⟩,
  ⟨(10,14), 5, (9,14), (10,13)⟩,
  ⟨(6,5), 6, (6,4), (6,6)⟩,
  ⟨(6,15), 6, (6,14), (6,16)⟩,
  ⟨(10,6), 6, (9,6), (10,5)⟩,
  ⟨(10,16), 6, (9,16), (10,15)⟩,
  ⟨(11,5), 6, (10,5), (11,4)⟩,
  ⟨(11,15), 6, (10,15), (11,14)⟩,
  ⟨(5,4), 7, (5,5), (6,4)⟩,
  ⟨(5,6), 7, (5,5), (6,6)⟩,
  ⟨(5,14), 7, (5,15), (6,14)⟩,
  ⟨(5,16), 7, (5,15), (6,16)⟩,
  ⟨(12,4), 7, (11,4), (12,5)⟩,
  ⟨(12,6), 7, (11,6), (12,5)⟩,
  ⟨(12,14), 7, (11,14), (12,15)⟩,
  ⟨(12,16), 7, (11,16), (12,15)⟩,
  ⟨(5,8), 8, (5,7), (6,8)⟩,
  ⟨(5,18), 8, (5,17), (6,18)⟩,
  ⟨(11,7), 8, (11,6), (12,7)⟩,
  ⟨(11,17), 8, (11,16), (12,17)⟩,
  ⟨(12,8), 9, (11,8), (12,7)⟩,
  ⟨(12,18), 9, (11,18), (12,17)⟩]
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
    (∀ v ∈ selected ++ endpoints, v.1<20 ∧ v.2<26) ∧
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

#print axioms frozen_extend_endpoints
#print axioms oriented_seal_frozen
#print axioms upper_seal_contacts
#print axioms lower_seal_contacts
#print axioms seal_packet_ledger
#print axioms collision_and_repair_ledgers
#print axioms geometry_valid
#print axioms mate_closed
#print axioms certificate_valid
#print axioms all_endpoints_frozen

end SubQuorum.WholeSupportDonorCollision
