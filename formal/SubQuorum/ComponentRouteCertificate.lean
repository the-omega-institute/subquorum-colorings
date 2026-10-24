import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.ComponentRouteCertificate

/-- Skip one prescribed vertex in an alternating path. -/
def skip (root i : Nat) : Nat := if i < root then i else i + 1

theorem skip_bounds {n root i : Nat} (hi : i < n) :
    skip root i ≤ n ∧ skip root i ≠ root ∧
      (skip root i = i ∨ skip root i = i + 1) := by
  unfold skip
  split <;> omega

theorem skip_injective {root i j : Nat} (h : skip root i = skip root j) : i = j := by
  unfold skip at h
  split at h <;> split at h <;> omega

theorem skip_covers {n root a : Nat} (hr : root ≤ n) (ha : a ≤ n)
    (hne : a ≠ root) : ∃ i, i < n ∧ skip root i = a := by
  by_cases h : a < root
  · exact ⟨a, by omega, by simp [skip, h]⟩
  · refine ⟨a - 1, by omega, ?_⟩
    have hlt : ¬ a - 1 < root := by omega
    simp only [skip, if_neg hlt]
    omega

/-- Any vertex on the larger side can be left free; all other vertices
    are bijectively paired to an adjacent vertex on the smaller side. -/
theorem arbitrary_root_matching (n root : Nat) (hr : root ≤ n) :
    (∀ i, i < n → skip root i ≤ n ∧ skip root i ≠ root ∧
      (skip root i = i ∨ skip root i = i + 1)) ∧
    (∀ i j, skip root i = skip root j → i = j) ∧
    (∀ a, a ≤ n → a ≠ root → ∃ i, i < n ∧ skip root i = a) := by
  exact ⟨fun _ hi => skip_bounds hi, fun _ _ h => skip_injective h,
    fun _ ha hne => skip_covers hr ha hne⟩

/- These constructors encode the counts AFTER the written graph
classification. They do not formalize that classification itself. -/
inductive Component where
  | demand (n : Nat)
  | reserve (n : Nat)
  | balanced (n : Nat)
  deriving Repr

def alpha : Component → Nat
  | .demand n => n + 1
  | .reserve n => n
  | .balanced n => n

def beta : Component → Nat
  | .demand n => n
  | .reserve n => n + 1
  | .balanced n => n

def demand : Component → Nat
  | .demand _ => 1
  | _ => 0

def reserve : Component → Nat
  | .reserve _ => 1
  | _ => 0

def total (f : Component → Nat) : List Component → Nat
  | [] => 0
  | c :: cs => f c + total f cs

theorem component_balance (c : Component) : beta c + demand c = alpha c + reserve c := by
  cases c <;> simp [alpha, beta, demand, reserve]

theorem whole_balance (cs : List Component) :
    total beta cs + total demand cs = total alpha cs + total reserve cs := by
  induction cs with
  | nil => rfl
  | cons c cs ih =>
    have h := component_balance c
    simp only [total]
    omega

/-- Exact signed resource ledger; subtraction is in integers. -/
theorem resource_ledger (cs : List Component) (intervals : Int) :
    intervals + (total beta cs : Int) - (total alpha cs : Int) =
      intervals + (total reserve cs : Int) - (total demand cs : Int) := by
  have h := whole_balance cs
  omega

/-- On m,a0,b0,...,a(n-1),b(n-1), remove ai and bj with i <= j. -/
def exchange (i j a : Nat) : Nat := if i < a ∧ a ≤ j then a - 1 else a

theorem exchange_bounds {n i j a : Nat} (hij : i ≤ j) (ha : a < n) (hne : a ≠ i) :
    exchange i j a < n ∧ exchange i j a ≠ j ∧
      (exchange i j a = a ∨ exchange i j a + 1 = a) := by
  unfold exchange
  split <;> omega

theorem exchange_injective {i j a b : Nat}
    (hai : a ≠ i) (hbi : b ≠ i) (h : exchange i j a = exchange i j b) : a = b := by
  unfold exchange at h
  split at h <;> split at h <;> omega

theorem exchange_covers {n i j b : Nat} (hij : i ≤ j) (hj : j < n)
    (hb : b < n) (hne : b ≠ j) :
    ∃ a, a < n ∧ a ≠ i ∧ exchange i j a = b := by
  by_cases h : i ≤ b ∧ b < j
  · refine ⟨b + 1, by omega, by omega, ?_⟩
    have hc : i < b + 1 ∧ b + 1 ≤ j := by omega
    simp [exchange, hc]
  · refine ⟨b, hb, by omega, ?_⟩
    have hc : ¬ (i < b ∧ b ≤ j) := by omega
    simp [exchange, hc]

#print axioms skip_bounds
#print axioms skip_injective
#print axioms skip_covers
#print axioms arbitrary_root_matching
#print axioms component_balance
#print axioms whole_balance
#print axioms resource_ledger
#print axioms exchange_bounds
#print axioms exchange_injective
#print axioms exchange_covers

end SubQuorum.ComponentRouteCertificate
