import Lean.Elab.Tactic.Omega

/-! All-finite-resource accounting. Each list entry represents one physical
resource with an original paid/unpaid label and exactly one final owner class.
The geometry-to-unique-resource-list adapter, permutation routing, cycle rank,
and actual grid construction remain written proofs. -/
set_option autoImplicit false
namespace SubQuorum.ContactCycleLedger

inductive FinalUse where
  | paid | bad | cycle
  deriving DecidableEq

structure Resource where
  oldPaid : Bool
  finalUse : FinalUse

def tally (test : Resource → Bool) : List Resource → Nat
  | [] => 0
  | r :: rs => (if test r then 1 else 0) + tally test rs

def oldPaid := tally (fun r => r.oldPaid)
def oldBad := tally (fun r => !r.oldPaid)
def paid := tally (fun r => decide (r.finalUse = .paid))
def bad := tally (fun r => decide (r.finalUse = .bad))
def cycles := tally (fun r => decide (r.finalUse = .cycle))

theorem old_partition (rs : List Resource) :
    oldPaid rs + oldBad rs = rs.length := by
  induction rs with
  | nil => rfl
  | cons r rs ih =>
      cases r with
      | mk b use =>
          cases b <;> simp [oldPaid, oldBad, tally] at * <;> omega

theorem new_partition (rs : List Resource) :
    paid rs + bad rs + cycles rs = rs.length := by
  induction rs with
  | nil => rfl
  | cons r rs ih =>
      cases r with
      | mk b use =>
          cases use <;> simp [paid, bad, cycles, tally] at * <;> omega

theorem resource_ledger (rs : List Resource) :
    oldPaid rs + oldBad rs = paid rs + bad rs + cycles rs := by
  have h := old_partition rs
  have h' := new_partition rs
  omega

/-- Use integer differences: the new payment cost may decrease. -/
theorem signed_cost (rs : List Resource) :
    (paid rs : Int) - oldPaid rs =
      (oldBad rs : Int) - bad rs - cycles rs := by
  have h := resource_ledger rs
  omega

/-- The adapter must establish no final bad-path resources before using
this specialization. In the written theorem every final path is TH. -/
theorem full_repair_cost (rs : List Resource) (full : bad rs = 0) :
    (paid rs : Int) - oldPaid rs = (oldBad rs : Int) - cycles rs := by
  have h := signed_cost rs
  omega

theorem forest_full_repair_cost (rs : List Resource)
    (full : bad rs = 0) (noCycles : cycles rs = 0) :
    paid rs = oldPaid rs + oldBad rs := by
  have h := resource_ledger rs
  omega

theorem no_increment_iff (rs : List Resource) (full : bad rs = 0) :
    paid rs ≤ oldPaid rs ↔ oldBad rs ≤ cycles rs := by
  have h := resource_ledger rs
  omega

end SubQuorum.ContactCycleLedger
#print axioms SubQuorum.ContactCycleLedger.old_partition
#print axioms SubQuorum.ContactCycleLedger.new_partition
#print axioms SubQuorum.ContactCycleLedger.resource_ledger
#print axioms SubQuorum.ContactCycleLedger.signed_cost
#print axioms SubQuorum.ContactCycleLedger.full_repair_cost
#print axioms SubQuorum.ContactCycleLedger.forest_full_repair_cost
#print axioms SubQuorum.ContactCycleLedger.no_increment_iff
