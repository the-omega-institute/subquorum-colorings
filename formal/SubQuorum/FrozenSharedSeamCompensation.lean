import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 8192

namespace SubQuorum.FrozenSharedSeamCompensation

def bit (b : Bool) : Nat := if b then 1 else 0
def reserved (left right : Bool) : Nat := 2 - (bit left + bit right)
def units (first second : Bool) : Nat := bit first + bit second

/-- Targets 0,1 are the two PRIVATE beta units, 2,3 the actual shared
interval identities, and 4 the unpaid choice. -/
def allowed (left right first second : Bool) (side target : Nat) : Bool :=
  if target == 4 then true
  else if target == 0 then side == 0 && left
  else if target == 1 then side == 1 && right
  else if target == 2 then first
  else if target == 3 then second
  else false

def legal (left right first second : Bool) (a b : Nat) : Bool :=
  allowed left right first second 0 a &&
  allowed left right first second 1 b &&
  (a != b || a == 4)

def paid (a b : Nat) : Nat := (if a < 4 then 1 else 0) + (if b < 4 then 1 else 0)

def allocationRank (left right first second : Bool) : Nat :=
  ((List.range 5).flatMap fun a => (List.range 5).map fun b =>
    if legal left right first second a b then paid a b else 0).foldl Nat.max 0

/-- Exhaust all actual assignments to the four resource identities, allowing
unpaid sources. Shared targets must be different; they are never cloned. -/
theorem exact_two_side_rank : ∀ left right first second : Bool,
    allocationRank left right first second =
      2 - (reserved left right - units first second) := by decide

theorem one_shared_unit_not_two_payments :
    allocationRank false false true false = 1 ∧
    allocationRank false false true true = 2 := by decide

/-- Arithmetic used after the two private beta identities are counted. -/
theorem side_capacity (r z : Nat) (hr : r ≤ 2) :
    min 2 (2-r+z) = 2-(r-z) := by omega

def defect (seams : List (Nat × Nat)) : Nat :=
  match seams with
  | [] => 0
  | (r,z)::rest => (r-z) + defect rest

def clusterValue (seams : List (Nat × Nat)) : Nat :=
  match seams with
  | [] => 0
  | (r,z)::rest => (3-(r-z)) + clusterValue rest

def clusterCost (seams : List (Nat × Nat)) : Nat :=
  match seams with
  | [] => 0
  | (r,z)::rest => (4-(r-z)) + clusterCost rest

/-- An arbitrary list of independent seam clusters, not a bounded q test.
The route/identity hypotheses establishing independence are in the note. -/
theorem simultaneous_cluster_budget (seams : List (Nat × Nat))
    (bounded : ∀ p ∈ seams, p.1 ≤ 2) :
    clusterValue seams + defect seams = 3*seams.length ∧
    clusterCost seams + defect seams = 4*seams.length := by
  induction seams with
  | nil => simp [clusterValue, clusterCost, defect]
  | cons p rest ih =>
    have hp : p.1 ≤ 2 := bounded p (by simp)
    have hb : ∀ x ∈ rest, x.1 ≤ 2 := by
      intro x hx
      exact bounded x (by simp [hx])
    obtain ⟨hv,hc⟩ := ih hb
    simp only [clusterValue, clusterCost, defect, List.length_cons]
    constructor <;> omega

theorem total_value_cost (seams : List (Nat × Nat))
    (bounded : ∀ p ∈ seams, p.1 ≤ 2) :
    (seams.length+4+clusterValue seams) + defect seams = 4*(seams.length+1) ∧
    (seams.length+5+clusterCost seams) + defect seams = 5*(seams.length+1) := by
  obtain ⟨hv,hc⟩ := simultaneous_cluster_budget seams bounded
  constructor <;> omega

/-- No original singleton column in one seam equals a unit in another seam. -/
theorem seam_unit_identity_injective (i j a b : Nat)
    (ha : a ≤ 1) (hb : b ≤ 1)
    (same : 24*i+23+a = 24*j+23+b) : i=j ∧ a=b := by omega

theorem shared_target_forces_same_source {S R : Type}
    (allocation : S → R)
    (injective : ∀ x y, allocation x=allocation y → x=y)
    (x y : S) (same : allocation x=allocation y) : x=y :=
  injective x y same

#print axioms exact_two_side_rank
#print axioms one_shared_unit_not_two_payments
#print axioms side_capacity
#print axioms simultaneous_cluster_budget
#print axioms total_value_cost
#print axioms seam_unit_identity_injective
#print axioms shared_target_forces_same_source

end SubQuorum.FrozenSharedSeamCompensation
