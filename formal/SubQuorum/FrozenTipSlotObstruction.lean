import SubQuorum.FrozenSharedMixedGate

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 1600000

namespace SubQuorum.FrozenTipSlotObstruction

open SubQuorum.FrozenSharedMixedGate (Point adjacent Frozen strict_rank_complete)

def selected : List Point := [
  (1,4),(2,3),(2,6),(2,8),(3,9),(4,2),(5,3),(6,2),(6,5),
  (6,9),(7,1),(7,4),(7,6),(7,8),(7,10),(8,3),(8,10),
  (6,11),(5,12),(7,13),(8,12)]

def matching : List (Point × Point) := [
  ((2,4),(3,4)),((3,5),(4,5)),((3,6),(4,6)),((3,7),(3,8)),
  ((4,3),(4,4)),((4,7),(5,7)),((5,6),(6,6)),((6,7),(6,8)),
  ((7,2),(7,3)),((6,12),(7,12))]

abbrev Witness := SubQuorum.FrozenSharedMixedGate.Witness

def witnesses : List Witness := [
  ⟨(2,4),0,(1,4),(2,3)⟩, ⟨(3,4),3,(3,5),(4,4)⟩,
  ⟨(3,5),3,(3,4),(3,6)⟩, ⟨(3,6),1,(2,6),(3,7)⟩,
  ⟨(3,7),3,(3,6),(4,7)⟩, ⟨(3,8),0,(2,8),(3,9)⟩,
  ⟨(4,3),0,(4,2),(5,3)⟩, ⟨(4,4),4,(3,4),(4,5)⟩,
  ⟨(4,5),2,(4,4),(4,6)⟩, ⟨(4,6),2,(4,7),(5,6)⟩,
  ⟨(4,7),2,(3,7),(4,6)⟩, ⟨(5,6),3,(4,6),(5,7)⟩,
  ⟨(5,7),1,(5,6),(6,7)⟩, ⟨(6,6),0,(6,5),(7,6)⟩,
  ⟨(6,7),4,(5,7),(6,6)⟩, ⟨(6,8),0,(6,9),(7,8)⟩,
  ⟨(6,12),0,(5,12),(6,11)⟩, ⟨(7,2),0,(6,2),(7,1)⟩,
  ⟨(7,3),0,(7,4),(8,3)⟩, ⟨(7,12),0,(7,13),(8,12)⟩]

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
    (∀ v ∈ selected ++ endpoints, v.1 < 10 ∧ v.2 < 16) ∧
    (∀ v ∈ selected,
      ((selected ++ endpoints).filter fun w => decide (adjacent v w)).length ≤ 1) := by
  decide

theorem mate_closed : ∀ v ∈ endpoints, mate v ∈ endpoints := by decide
theorem certificate_valid : ∀ v ∈ endpoints, validAt v := by decide

theorem all_endpoints_frozen :
    ∀ v ∈ endpoints,
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

def alphaA : List Point := [(3,6),(4,6),(5,6),(6,6)]
def mixedD : List Point := [(6,7),(6,8)]
def betaB : List Point := [(3,5),(4,5)]

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
    alternating true alphaA ∧ alternating true mixedD ∧ alternating true betaB ∧
    (alphaA ++ mixedD ++ betaB).Nodup ∧
    (∀ v ∈ alphaA ++ mixedD ++ betaB, v ∈ endpoints) ∧
    tp (3,6) = true ∧ tp (6,6) = true ∧ tp (6,8) = true ∧
    bp (6,7) = true ∧ bp (3,5) = true ∧ bp (4,5) = true := by
  decide

/-- BB-unit witnesses in endpoint-free gaps bounding a specified owner's body.
    The concrete board has no TT columns, so every BB column is one unit.
    We deliberately include marked boundary BB units too: emptiness is stronger. -/
def wholeSupport (body : List Point) : List Point :=
  ((List.range 5).flatMap fun band => (List.range 16).map fun col => (band,col)).filter
    fun j => blank (2*j.1,j.2) && blank (2*j.1+1,j.2) &&
      body.any (fun v => decide (v.1/2 = j.1) && endpoints.all (fun p =>
        !decide (p.1/2 = j.1 ∧
          ((v.2 < p.2 ∧ p.2 ≤ j.2) ∨ (j.2 ≤ p.2 ∧ p.2 < v.2)))))

theorem no_interval_witness_even_including_boundary :
    wholeSupport alphaA = [] ∧ wholeSupport mixedD = [] := by decide

def bpNeighbours (v : Point) : List Point :=
  endpoints.filter fun w => bp w && decide (v.1 = w.1 ∧ adjacent v w)

abbrev Target := Sum Point (Point × Bool)
def choices (v : Point) (body : List Point) : List Target :=
  (bpNeighbours v).map Sum.inl ++ (wholeSupport body).flatMap
    fun j => [Sum.inr (j,false),Sum.inr (j,true)]

theorem both_tips_have_one_identical_choice :
    choices (6,6) alphaA = [Sum.inl (6,7)] ∧
    choices (6,8) mixedD = [Sum.inl (6,7)] := by decide

/-- Alpha reachability does not make the all-TP two-slot matching necessary. -/
theorem no_injective_tip_assignment (f : Point → Target)
    (ha : f (6,6) ∈ choices (6,6) alphaA)
    (hd : f (6,8) ∈ choices (6,8) mixedD)
    (injective : ∀ a b, f a = f b → a = b) : False := by
  rw [both_tips_have_one_identical_choice.1] at ha
  rw [both_tips_have_one_identical_choice.2] at hd
  have hx : f (6,6) = Sum.inl (6,7) := List.mem_singleton.mp ha
  have hy : f (6,8) = Sum.inl (6,7) := List.mem_singleton.mp hd
  have bad := injective (6,6) (6,8) (hx.trans hy.symm)
  exact (by decide : ((6,6) : Point) ≠ (6,8)) bad

theorem alpha_reaches_mixed_and_has_beta_payment :
    adjacent (6,6) (6,7) ∧ adjacent (3,6) (3,5) ∧
    tp (6,6) = true ∧ bp (6,7) = true ∧
    tp (3,6) = true ∧ bp (3,5) = true := by decide

/-- The PP seal blocks any later BB unit to the right of column 12. -/
theorem right_pp_seal (j : Nat) (hj : 12 ≤ j) :
    ∃ p ∈ endpoints, p.1/2 = 3 ∧
      ((6 < p.2 ∧ p.2 ≤ j) ∧ (8 < p.2 ∧ p.2 ≤ j)) := by
  refine ⟨(6,12),by decide,by decide,?_,?_⟩ <;> omega

/-- The exact deficit of q independent copies, and their full payment count. -/
theorem copy_accounting (q : Nat) : 2*q-q = q ∧ q-q = 0 := by omega

theorem closed_owner_charge_bound (a b m intervals : Nat)
    (h : 2*a+m ≤ 2*b+m+2*intervals) : a ≤ b+intervals := by omega

#print axioms geometry_valid
#print axioms all_endpoints_frozen
#print axioms critical_strands
#print axioms no_interval_witness_even_including_boundary
#print axioms no_injective_tip_assignment
#print axioms right_pp_seal
#print axioms closed_owner_charge_bound

end SubQuorum.FrozenTipSlotObstruction
