import SubQuorum.FrozenSharedMixedGate

set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 5000000

namespace SubQuorum.TwoSidedDeadEscape

open SubQuorum.FrozenSharedMixedGate (Point adjacent Frozen strict_rank_complete)
abbrev Witness := SubQuorum.FrozenSharedMixedGate.Witness

def selected : List Point := [(3,8),(3,20),(4,6),(4,9),(4,11),(4,13),(4,15),(4,17),(4,19),(4,22),(5,7),(5,10),(5,18),(5,21),(6,20),(6,22),(7,23),(8,10),(10,10),(10,23),(11,11),(11,14),(11,16),(11,18),(11,20),(11,22)]

def matching : List (Point × Point) := [((4,7),(4,8)),((4,20),(4,21)),((5,11),(5,12)),((5,13),(6,13)),((5,14),(6,14)),((5,15),(6,15)),((5,16),(5,17)),((6,12),(7,12)),((6,16),(7,16)),((7,13),(8,13)),((7,14),(8,14)),((7,15),(8,15)),((7,20),(8,20)),((7,21),(7,22)),((8,11),(8,12)),((8,16),(8,17)),((8,18),(8,19)),((8,21),(9,21)),((9,11),(10,11)),((9,12),(9,13)),((9,14),(10,14)),((9,15),(9,16)),((9,17),(9,18)),((9,19),(9,20)),((10,15),(10,16)),((10,17),(10,18)),((10,19),(10,20)),((10,21),(10,22))]

def witnesses : List Witness := [
  ⟨(4,7),0,(4,6),(5,7)⟩,
  ⟨(4,8),0,(3,8),(4,9)⟩,
  ⟨(4,20),0,(3,20),(4,19)⟩,
  ⟨(4,21),0,(4,22),(5,21)⟩,
  ⟨(5,11),0,(4,11),(5,10)⟩,
  ⟨(5,12),6,(5,13),(6,12)⟩,
  ⟨(5,13),1,(4,13),(5,12)⟩,
  ⟨(5,14),11,(5,13),(5,15)⟩,
  ⟨(5,15),1,(4,15),(5,16)⟩,
  ⟨(5,16),11,(5,15),(6,16)⟩,
  ⟨(5,17),0,(4,17),(5,18)⟩,
  ⟨(6,12),2,(5,12),(6,13)⟩,
  ⟨(6,13),5,(6,12),(7,13)⟩,
  ⟨(6,14),2,(6,13),(6,15)⟩,
  ⟨(6,15),10,(6,16),(7,15)⟩,
  ⟨(6,16),2,(5,16),(6,15)⟩,
  ⟨(7,12),4,(7,13),(8,12)⟩,
  ⟨(7,13),3,(6,13),(7,12)⟩,
  ⟨(7,14),9,(7,13),(7,15)⟩,
  ⟨(7,15),3,(6,15),(7,16)⟩,
  ⟨(7,16),9,(7,15),(8,16)⟩,
  ⟨(7,20),1,(6,20),(7,21)⟩,
  ⟨(7,21),8,(7,20),(8,21)⟩,
  ⟨(7,22),0,(6,22),(7,23)⟩,
  ⟨(8,11),1,(8,10),(9,11)⟩,
  ⟨(8,12),4,(7,12),(8,13)⟩,
  ⟨(8,13),3,(8,12),(9,13)⟩,
  ⟨(8,14),4,(8,13),(8,15)⟩,
  ⟨(8,15),8,(8,16),(9,15)⟩,
  ⟨(8,16),4,(7,16),(8,15)⟩,
  ⟨(8,17),6,(8,18),(9,17)⟩,
  ⟨(8,18),6,(8,17),(9,18)⟩,
  ⟨(8,19),4,(8,20),(9,19)⟩,
  ⟨(8,20),7,(8,19),(9,20)⟩,
  ⟨(8,21),2,(7,21),(8,20)⟩,
  ⟨(9,11),6,(8,11),(9,12)⟩,
  ⟨(9,12),2,(8,12),(9,11)⟩,
  ⟨(9,13),5,(8,13),(9,14)⟩,
  ⟨(9,14),8,(9,13),(9,15)⟩,
  ⟨(9,15),4,(8,15),(10,15)⟩,
  ⟨(9,16),7,(8,16),(9,17)⟩,
  ⟨(9,17),5,(8,17),(9,16)⟩,
  ⟨(9,18),5,(8,18),(9,19)⟩,
  ⟨(9,19),6,(9,18),(10,19)⟩,
  ⟨(9,20),3,(8,20),(9,21)⟩,
  ⟨(9,21),7,(9,20),(10,21)⟩,
  ⟨(10,11),0,(10,10),(11,11)⟩,
  ⟨(10,14),4,(10,15),(11,14)⟩,
  ⟨(10,15),9,(9,15),(10,14)⟩,
  ⟨(10,16),3,(10,17),(11,16)⟩,
  ⟨(10,17),10,(9,17),(10,16)⟩,
  ⟨(10,18),2,(10,19),(11,18)⟩,
  ⟨(10,19),11,(9,19),(10,18)⟩,
  ⟨(10,20),1,(10,21),(11,20)⟩,
  ⟨(10,21),12,(9,21),(10,20)⟩,
  ⟨(10,22),0,(10,23),(11,22)⟩]

def endpoints : List Point := matching.flatMap fun e => [e.1,e.2]
def mate (v : Point) : Point := SubQuorum.FrozenSharedMixedGate.lookupMate v matching
def record (v : Point) : Witness := (witnesses.find? fun w => w.point == v).getD default
def rank (v : Point) : Nat := (record v).rank

def validAt (v : Point) : Prop :=
  let a := (record v).left
  let b := (record v).right
  a ≠ b ∧ adjacent v a ∧ adjacent v b ∧
    (a ∈ selected ∨ (a ∈ endpoints ∧ rank (mate a) < rank v)) ∧
    (b ∈ selected ∨ (b ∈ endpoints ∧ rank (mate b) < rank v))

instance (v : Point) : Decidable (validAt v) :=
  inferInstanceAs (Decidable (_ ≠ _ ∧ _ ∧ _ ∧ (_ ∨ (_ ∧ _)) ∧ (_ ∨ (_ ∧ _))))

theorem geometry_valid :
    endpoints.Nodup ∧
    (∀ e ∈ matching, adjacent e.1 e.2) ∧
    (∀ v ∈ endpoints, v ∉ selected) ∧
    (∀ v ∈ selected ++ endpoints, v.1 < 14 ∧ v.2 < 28) ∧
    (∀ v ∈ selected,
      ((selected ++ endpoints).filter fun w => decide (adjacent v w)).length ≤ 1) := by
  decide

theorem mate_closed : ∀ v ∈ endpoints, mate v ∈ endpoints := by decide
theorem certificate_valid : ∀ v ∈ endpoints, validAt v := by decide

theorem all_endpoints_frozen : ∀ v ∈ endpoints,
    Frozen (fun x => x ∈ endpoints) (fun x => x ∈ selected) mate adjacent v := by
  apply strict_rank_complete (fun x => x ∈ endpoints) (fun x => x ∈ selected)
    mate adjacent rank mate_closed
  intro v pv
  exact ⟨(record v).left,(record v).right,certificate_valid v pv⟩

def verticalPartner (v : Point) : Point :=
  if v.1 % 2 = 0 then (v.1+1,v.2) else (v.1-1,v.2)
def tp (v : Point) : Bool := decide (v ∈ endpoints ∧ verticalPartner v ∈ selected)
def bp (v : Point) : Bool :=
  decide (v ∈ endpoints ∧ verticalPartner v ∉ selected ∧ verticalPartner v ∉ endpoints)
def blank (v : Point) : Bool := decide (v ∉ selected ∧ v ∉ endpoints)

def alphaA : List Point := [(5,13),(6,13),(7,13),(8,13),(9,13),(9,12),(8,12),(8,11),(9,11),(10,11)]
def alphaB : List Point := [(5,15),(6,15),(7,15),(8,15),(9,15),(9,16),(8,16),(8,17),(9,17),(9,18),(8,18),(8,19),(9,19),(9,20),(8,20),(7,20)]
def mixedG : List Point := [(5,14),(6,14),(7,14),(8,14),(9,14),(10,14)]
def deadLeft : List Point := [(5,12),(5,11)]
def deadRight : List Point := [(5,16),(5,17)]

def alternating : Bool → List Point → Prop
  | _, [] => True
  | _, [_] => True
  | useMatching, a :: b :: rest =>
    (if useMatching then mate a = b else verticalPartner a = b) ∧
      alternating (!useMatching) (b :: rest)

instance (useMatching : Bool) (path : List Point) : Decidable (alternating useMatching path) :=
  match path with
  | [] => isTrue True.intro
  | [_] => isTrue True.intro
  | _ :: b :: rest =>
    have := instDecidableAlternating (!useMatching) (b :: rest)
    inferInstanceAs (Decidable ((_ : Prop) ∧ alternating (!useMatching) (b :: rest)))

theorem critical_strands :
    alternating true alphaA ∧ alternating true alphaB ∧ alternating true mixedG ∧
    alternating true deadLeft ∧ alternating true deadRight ∧
    (alphaA ++ alphaB ++ mixedG ++ deadLeft ++ deadRight).Nodup ∧
    (∀ v ∈ alphaA ++ alphaB ++ mixedG ++ deadLeft ++ deadRight, v ∈ endpoints) ∧
    tp (5,13) = true ∧ tp (10,11) = true ∧
    tp (5,15) = true ∧ tp (7,20) = true ∧
    bp (5,14) = true ∧ tp (10,14) = true ∧
    bp (5,12) = true ∧ tp (5,11) = true ∧
    bp (5,16) = true ∧ tp (5,17) = true := by decide

def bpNeighbours (v : Point) : List Point :=
  endpoints.filter fun w => bp w && decide (v.1 = w.1 ∧ adjacent v w)

/-- Exact physical fork and both outward actual matching edges. -/
theorem fork_and_two_forced_escapes :
    bpNeighbours (5,13) = [(5,12),(5,14)] ∧
    bpNeighbours (5,15) = [(5,14),(5,16)] ∧
    mate (5,13) = (6,13) ∧ mate (5,14) = (6,14) ∧ mate (5,15) = (6,15) ∧
    mate (5,12) = (5,11) ∧ mate (5,16) = (5,17) := by decide

/-- BB columns in endpoint-free gaps incident to this actual owner body.
    Includes boundary columns; no resource reservation is used for emptiness. -/
def wholeBBSupport (body : List Point) : List Point :=
  ((List.range 7).flatMap fun band => (List.range 28).map fun col => (band,col)).filter
    fun j => blank (2*j.1,j.2) && blank (2*j.1+1,j.2) &&
      body.any (fun v => decide (v.1/2 = j.1) && endpoints.all (fun p =>
        !decide (p.1/2 = j.1 ∧
          ((v.2 < p.2 ∧ p.2 ≤ j.2) ∨ (j.2 ≤ p.2 ∧ p.2 < v.2)))))

theorem both_escapes_have_no_original_BB_support :
    wholeBBSupport deadLeft = [] ∧ wholeBBSupport deadRight = [] := by decide

theorem both_escapes_have_only_self_output :
    bpNeighbours (5,11) = [(5,12)] ∧ bpNeighbours (5,17) = [(5,16)] := by decide

/-- The receiver is productive, and its two units are also direct alpha-A units. -/
theorem productive_gate_and_support_shadow :
    wholeBBSupport mixedG = [(5,12),(5,13)] ∧
    (5,12) ∈ wholeBBSupport alphaA ∧ (5,13) ∈ wholeBBSupport alphaA ∧
    (3,17) ∈ wholeBBSupport alphaB := by decide

/-- With an original second distinct unit in L, the shadow unit can pay B. -/
theorem distinct_shadow_payment {U : Type} {L S : U → Prop} {j k : U}
    (sj : S j) (lk : L k) (different : j ≠ k) :
    L k ∧ S j ∧ k ≠ j := by
  exact ⟨lk,sj,Ne.symm different⟩

/-- Gate loads add even when the two selected resource identities differ. -/
theorem one_gate_forbids_two_routes (loadA loadB : Nat)
    (capacity : loadA+loadB ≤ 1) (usedA : 1 ≤ loadA) (usedB : 1 ≤ loadB) : False := by
  omega

#print axioms geometry_valid
#print axioms mate_closed
#print axioms certificate_valid
#print axioms all_endpoints_frozen
#print axioms critical_strands
#print axioms fork_and_two_forced_escapes
#print axioms both_escapes_have_no_original_BB_support
#print axioms both_escapes_have_only_self_output
#print axioms productive_gate_and_support_shadow
#print axioms distinct_shadow_payment
#print axioms one_gate_forbids_two_routes

end SubQuorum.TwoSidedDeadEscape
