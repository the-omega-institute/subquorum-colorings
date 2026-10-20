import SubQuorum.WidthSixBottomOwner

set_option autoImplicit false

namespace SubQuorum.NeutralCycleInteriorTransfer

open WidthSixBottomOwner

def inwardBlockers : List Point :=
  [(-1,-1),(0,-1),(1,-1),(2,-1),(3,-1),
   (-1,0),(-1,1),(-1,2),(-1,3),(-1,4)]

theorem neutral_forced_point_has_no_rotor_owner :
    rotorOwners inwardBlockers = [] := by decide

set_option maxHeartbeats 1000000 in
theorem perpendicular_foreign_neighbors_allow_only_four_original_roles
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hroot : endpoint width left right anchor)
    (hnorth : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (-1,0)))
    (hwest : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,-1))) :
    anchor = (0,1) ∨ anchor = (0,width) ∨
      anchor = (left,1) ∨ anchor = (right,width) := by
  rcases anchor with ⟨row,column⟩
  rcases hroot with hbar | hnear | hfar
  all_goals
    cases transpose <;> cases flipRow <;> cases flipColumn <;>
      simp [pull, endpoint, Prod.mk.injEq] at hnorth hwest ⊢ <;> omega

theorem interior_contacts_from_oriented_turning
    (phase01 phase10 inward outward : Nat)
    (hcontacts : inward+outward+phase10 = phase01)
    (hturn : inward = outward+4) :
    2*inward+phase10 = phase01+4 := by
  omega

theorem four_point_capacity_gives_hall_condition
    (curves forcedPoints neighboringOwners : Nat)
    (hdemand : 4*curves ≤ forcedPoints)
    (hcapacity : forcedPoints ≤ 4*neighboringOwners) :
    curves ≤ neighboringOwners := by
  omega

theorem mixed_cycle_internal_source_budget
    (phase01 phase10 components inward newSources : Nat)
    (hturning : 2*inward+phase10 = phase01+4*components)
    (hcapacity : inward ≤ 2*phase10+4*newSources) :
    phase01+4*components ≤ 5*phase10+8*newSources := by
  omega

def sourceQuota (phase01 : Nat) : Nat := (phase01+11)/8

theorem pure_cycle_rounded_source_quota
    (phase01 inward sources : Nat)
    (hturning : 2*inward = phase01+4)
    (hcapacity : inward ≤ 4*sources) :
    sourceQuota phase01 ≤ sources := by
  simp [sourceQuota]
  omega

def quotaTotal : List (Nat × Nat) → Nat
  | [] => 0
  | entry::rest => sourceQuota entry.1+quotaTotal rest

def ownerTotal : List (Nat × Nat) → Nat
  | [] => 0
  | entry::rest => entry.2+ownerTotal rest

theorem rounded_cycle_quotas_aggregate_without_reusing_owner_counts
    (entries : List (Nat × Nat))
    (hentries : ∀ entry ∈ entries, entry.1+4 ≤ 8*entry.2) :
    quotaTotal entries ≤ ownerTotal entries := by
  induction entries with
  | nil => simp [quotaTotal, ownerTotal]
  | cons entry rest inductionHypothesis =>
    have hentry := hentries entry (by simp)
    have hrest : ∀ item ∈ rest, item.1+4 ≤ 8*item.2 := by
      intro item hitem
      exact hentries item (by simp [hitem])
    have htail := inductionHypothesis hrest
    have hquota : sourceQuota entry.1 ≤ entry.2 := by
      simp [sourceQuota]
      omega
    simp only [quotaTotal, ownerTotal]
    omega

end SubQuorum.NeutralCycleInteriorTransfer
