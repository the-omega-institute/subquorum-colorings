import SubQuorum.FrozenHalfAreaAttainers

set_option autoImplicit false
set_option maxRecDepth 16384
set_option maxHeartbeats 0

/- The coordinate rank adapter remains a written all-length proof. Reuse
   FrozenHalfAreaAttainers.certificate_implies_frozen for rank induction.
   These new kernels check distinct physical shield identities, the exact
   shared-guard count, and the conditional restricted freezing obstruction. -/
namespace SubQuorum.NeutralOccupiedEnvelopes
open SubQuorum.FrozenHalfAreaAttainers

inductive Shield where
  | left | right | common
  deriving DecidableEq

def point (j : Nat) (s : Shield) : Int × Int :=
  match s with
  | .left => (1,8+6*(j:Int))
  | .right => (1,10+6*(j:Int))
  | .common => (2,9+6*(j:Int))

/-- Even neighbouring envelopes cannot name the same physical shield. -/
theorem shield_coordinate_injective (i j : Nat) (s t : Shield)
    (h : point i s = point j t) : i=j ∧ s=t := by
  cases s <;> cases t <;> simp only [point, Prod.mk.injEq] at h
  all_goals first | exact ⟨by omega,rfl⟩ | omega

inductive Entry where
  | none | left | right | both
  deriving DecidableEq

def entries : Entry → Nat
  | .none => 0 | .left => 1 | .right => 1 | .both => 2
def active : Entry → Nat
  | .none => 0 | _ => 1
def double : Entry → Nat
  | .both => 1 | _ => 0
def guards : Entry → List Shield
  | .none => []
  | .left => [.left,.common]
  | .right => [.right,.common]
  | .both => [.left,.right,.common]

def total {α : Type} (f : α → Nat) : List α → Nat
  | [] => 0
  | e::rest => f e + total f rest

/-- Common shields are counted once per active index. Together with physical
    coordinate injectivity this gives the exact union cardinality. -/
theorem exact_shared_guard_count (word : List Entry) :
    total (fun e => (guards e).length) word =
      total entries word + total active word := by
  induction word with
  | nil => rfl
  | cons e rest ih =>
    cases e <;> simp only [total,guards,entries,active,List.length_cons,List.length_nil] at * <;> omega

/-- Every nonempty direct entry pattern has strictly more new black endpoints
    than common shields that could escape the singleton obstruction. -/
theorem restricted_conversion_shortage (word : List Entry)
    (hne : 0 < total entries word) :
    total double word < total entries word := by
  have bound : ∀ w : List Entry, 2 * total double w ≤ total entries w := by
    intro w
    induction w with
    | nil => simp [total]
    | cons e rest ih =>
      cases e <;> simp only [total,entries,double] at * <;> omega
  have hb := bound word
  omega

/-- A converted shield with no selected neighbour and at most its own mate
    plus one other occupied neighbour is a singleton trap, for ANY matching.
    The concrete geometric premise is checked in the coordinate verifier. -/
theorem singleton_shield_excludes_freezing {V : Type}
    (Adj : V → V → Prop) (T P : V → Prop) (mate : V → V)
    (v other : V) (hp : P v) (hinv : mate (mate v)=v)
    (hnoT : ∀ a, Adj v a → ¬T a)
    (hdegree : ∀ a, Adj v a → P a → a=mate v ∨ a=other) :
    ¬ Frozen Adj T P mate v := by
  refine trap_excludes_frozen Adj T P (fun x => x=v) mate ?_ v hp rfl
  intro x _hx hsame hsup
  subst x
  obtain ⟨a,b,hab,hva,hvb,ha,hb⟩ := hsup
  have only : ∀ z, Adj v z → (T z ∨ P z ∧ ¬mate z=v) → z=other := by
    intro z hvz hz
    rcases hz with ht | ⟨hpz,hn⟩
    · exact False.elim (hnoT z hvz ht)
    · rcases hdegree z hvz hpz with he | he
      · exact False.elim (hn (he ▸ hinv))
      · exact he
  exact hab ((only a hva ha).trans (only b hvb hb).symm)

/-- Colour balance requires one white conversion per new direct black entry;
    the geometric singleton lemma bounds all potentially freezing conversions
    by the double-entry common shields. Those two conditions cannot coexist. -/
theorem no_fully_frozen_restricted_conversion (word : List Entry)
    (converted : Nat) (hne : 0 < total entries word)
    (hbalance : converted=total entries word)
    (hfullyFrozen : converted≤total double word) : False := by
  have hs := restricted_conversion_shortage word hne
  omega

/- The enlarged permission domain allows any of the three black cells at
   each envelope, and white conversions may be pooled across envelopes. -/
inductive Mask where
  | empty | d | e | de | w | dw | ew | full
  deriving DecidableEq

def blacks : Mask → Nat
  | .empty => 0 | .d | .e | .w => 1
  | .de | .dw | .ew => 2 | .full => 3
def forced : Mask → Nat
  | .empty => 0 | .d | .e => 2 | _ => 3
def deficit : Mask → Nat
  | .empty | .full => 0 | .w => 2 | _ => 1
def Complete : List Mask → Prop
  | [] => True
  | mask::rest => (mask=.empty ∨ mask=.full) ∧ Complete rest

/-- All eight local masks, counting the shared physical guards once. -/
theorem local_full_envelope_budget (mask : Mask) :
    forced mask = blacks mask + deficit mask ∧
    (deficit mask=0 ↔ mask=.empty ∨ mask=.full) := by
  cases mask <;> decide

/-- Pooling the white conversions globally cannot cancel any local deficit. -/
theorem all_length_full_envelope_budget (word : List Mask) :
    total forced word = total blacks word + total deficit word := by
  induction word with
  | nil => rfl
  | cons mask rest ih =>
    have he := (local_full_envelope_budget mask).1
    simp only [total]
    omega

/-- Equality classifies the allowed footprint: every envelope is empty or
    contains all six sites. It does not classify actual matchings. -/
theorem zero_deficit_iff_complete_cells (word : List Mask) :
    total deficit word=0 ↔ Complete word := by
  induction word with
  | nil => simp [total,Complete]
  | cons mask rest ih =>
    have he := (local_full_envelope_budget mask).2
    simp only [total,Complete]
    constructor
    · intro hz
      have hez : deficit mask=0 := by omega
      have hrz : total deficit rest=0 := by omega
      exact ⟨he.mp hez,ih.mp hrz⟩
    · intro ⟨hc,hr⟩
      have hez := he.mpr hc
      have hrz := ih.mpr hr
      omega

/-- Actual bipartite colour balance supplies hobjective. Geometry supplies
    hwithdrawn. Both are explicit; no matching or coordinate adapter is
    silently assumed formalized. Neutrality forces all-or-nothing cells and
    withdrawal of exactly their forced guards. -/
theorem neutral_objective_forces_complete_cells (word : List Mask)
    (withdrawn : Nat) (J J0 : Int)
    (hobjective : J=J0+(total blacks word:Int)-(withdrawn:Int))
    (hwithdrawn : total forced word≤withdrawn) :
    J+(total deficit word:Int)≤J0 ∧
    (J=J0 → Complete word ∧ withdrawn=total forced word) := by
  have hb := all_length_full_envelope_budget word
  constructor
  · omega
  · intro hj
    have hz : total deficit word=0 := by omega
    exact ⟨(zero_deficit_iff_complete_cells word).mp hz,by omega⟩

end SubQuorum.NeutralOccupiedEnvelopes
#print axioms SubQuorum.NeutralOccupiedEnvelopes.shield_coordinate_injective
#print axioms SubQuorum.NeutralOccupiedEnvelopes.exact_shared_guard_count
#print axioms SubQuorum.NeutralOccupiedEnvelopes.restricted_conversion_shortage
#print axioms SubQuorum.NeutralOccupiedEnvelopes.singleton_shield_excludes_freezing
#print axioms SubQuorum.NeutralOccupiedEnvelopes.no_fully_frozen_restricted_conversion
#print axioms SubQuorum.NeutralOccupiedEnvelopes.local_full_envelope_budget
#print axioms SubQuorum.NeutralOccupiedEnvelopes.all_length_full_envelope_budget
#print axioms SubQuorum.NeutralOccupiedEnvelopes.zero_deficit_iff_complete_cells
#print axioms SubQuorum.NeutralOccupiedEnvelopes.neutral_objective_forces_complete_cells
