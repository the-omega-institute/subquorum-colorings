import Lean.Elab.Tactic.Omega

/-! Scoped formal checks for the general-port/tile note. The actual-grid
adapter, max-flow/min-cut, normalization and family embedding are written.
The four-corner result checks the entire local label hypothesis, not a
finite collection of board sizes. -/
set_option autoImplicit false
namespace SubQuorum.GeneralSquarePorts

inductive Label where
  | hole | selected | occupied
  deriving DecidableEq

def occ (x : Label) : Nat := if x = .hole then 0 else 1
def sel (x : Label) : Nat := if x = .selected then 1 else 0
def endpoint (x : Label) : Nat := if x = .occupied then 1 else 0

def feasible (a b c d : Label) : Prop :=
  (a = .selected → occ b + occ d ≤ 1) ∧
  (b = .selected → occ a + occ c ≤ 1) ∧
  (c = .selected → occ b + occ d ≤ 1) ∧
  (d = .selected → occ a + occ c ≤ 1)

instance (a b c d : Label) : Decidable (feasible a b c d) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _))

def tCount (a b c d : Label) := sel a + sel b + sel c + sel d
def pCount (a b c d : Label) := endpoint a + endpoint b + endpoint c + endpoint d

theorem local_C4_profile (a b c d : Label) :
    feasible a b c d →
    tCount a b c d ≤ 2 ∧
    pCount a b c d ≤ (if tCount a b c d = 0 then 4
      else if tCount a b c d = 1 then 2 else 1) := by
  cases a <;> cases b <;> cases c <;> cases d <;> decide

theorem local_C4_charge (a b c d : Label) :
    feasible a b c d →
    2*tCount a b c d+pCount a b c d ≤
      4+(if tCount a b c d = 2 ∧ pCount a b c d = 1 then 1 else 0) := by
  cases a <;> cases b <;> cases c <;> cases d <;> decide

theorem debt_diagonal (a b c d : Label) :
    feasible a b c d → tCount a b c d = 2 → pCount a b c d = 1 →
    ((a = .selected ∧ c = .selected) ∨
     (b = .selected ∧ d = .selected)) := by
  cases a <;> cases b <;> cases c <;> cases d <;> decide

theorem local_slack (a b c d : Label) (i : Nat)
    (h : feasible a b c d) (hm : 2*i ≤ pCount a b c d) :
    tCount a b c d+i ≤ 2 := by
  obtain ⟨ht,hp⟩ := local_C4_profile a b c d h
  split at hp
  · omega
  · split at hp <;> omega

theorem signed_cycle_ledger (m u0 b0 c0 u1 b1 c1 : Nat)
    (h0 : u0+b0+c0=m) (h1 : u1+b1+c1=m) :
    (u1 : Int)-u0=(b0 : Int)-b1+(c0 : Int)-c1 := by omega

theorem regional_white_cancellation
    (tiles pw tw hw internal outgoing tb : Int)
    (white_partition : 2*tiles=pw+tw+hw)
    (matching_partition : pw=internal+outgoing) :
    tb-hw-outgoing=tb+tw+internal-2*tiles := by omega

theorem local_reserve_cancellation (t p i : Int) :
    2*(2-t-i)-(p-2*i)=4-2*t-p := by omega

theorem regional_cross_excess (t internal crossing tiles slack : Int)
    (hs : slack=2*tiles-t-internal) :
    t+(internal+crossing)-2*tiles=crossing-slack := by omega

theorem debt_boundary_identity (e s d boundary debt reserve : Int)
    (incidence : d=2*e+boundary)
    (local_reserve : 2*s-d=reserve-debt) :
    2*(e-s)=debt-reserve-boundary := by omega

theorem debt_flow_deficit (delta debt capacity : Nat)
    (h : 2*delta+capacity=debt) :
    debt-capacity=2*delta ∧ ∃ n : Nat, debt-capacity=2*n := by
  constructor
  · omega
  · exact ⟨delta, by omega⟩

theorem debt_free_regional_bound (e s boundary reserve : Nat)
    (h : 2*e+boundary+reserve=2*s) : e ≤ s := by omega

theorem positive_component (xs : List Int) (h : 0 < xs.sum) :
    ∃ x, x ∈ xs ∧ 0 < x := by
  induction xs with
  | nil => simp at h
  | cons a xs ih =>
    by_cases ha : 0 < a
    · exact ⟨a, by simp, ha⟩
    · have hs : 0 < xs.sum := by
        simp only [List.sum_cons] at h
        omega
      obtain ⟨x,hx,hpos⟩ := ih hs
      exact ⟨x, List.mem_cons_of_mem a hx, hpos⟩

theorem cycle_relay_cost (k : Nat) :
    (2*k+2 : Nat)+2=2*(k+2) := by omega

theorem cycle_relay_margin (H : Nat) :
    3*H+6-(H+4)=2*H+2 := by omega

theorem old_cycle_unbounded_expense (K : Nat) :
    ∃ H : Nat, 2 ≤ H ∧ (∃ n : Nat, H=2*n) ∧ K*2 < H+2 := by
  refine ⟨2*(K+1), by omega, ⟨K+1,rfl⟩, by omega⟩

end SubQuorum.GeneralSquarePorts
#print axioms SubQuorum.GeneralSquarePorts.local_C4_profile
#print axioms SubQuorum.GeneralSquarePorts.local_C4_charge
#print axioms SubQuorum.GeneralSquarePorts.debt_diagonal
#print axioms SubQuorum.GeneralSquarePorts.local_slack
#print axioms SubQuorum.GeneralSquarePorts.signed_cycle_ledger
#print axioms SubQuorum.GeneralSquarePorts.regional_white_cancellation
#print axioms SubQuorum.GeneralSquarePorts.local_reserve_cancellation
#print axioms SubQuorum.GeneralSquarePorts.regional_cross_excess
#print axioms SubQuorum.GeneralSquarePorts.debt_boundary_identity
#print axioms SubQuorum.GeneralSquarePorts.debt_flow_deficit
#print axioms SubQuorum.GeneralSquarePorts.debt_free_regional_bound
#print axioms SubQuorum.GeneralSquarePorts.positive_component
#print axioms SubQuorum.GeneralSquarePorts.cycle_relay_cost
#print axioms SubQuorum.GeneralSquarePorts.cycle_relay_margin
#print axioms SubQuorum.GeneralSquarePorts.old_cycle_unbounded_expense
