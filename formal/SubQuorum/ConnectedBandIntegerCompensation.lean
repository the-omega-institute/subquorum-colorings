import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 0

/- Algebraic core of CONNECTED_BAND_INTEGER_COMPENSATION.md.
   This file does not formalize the board-to-local-coordinate reduction.
   No native_decide, custom axioms, or admitted proofs are used. -/
namespace SubQuorum.ConnectedBandIntegerCompensation

def bw (N : Nat) (b : Bool) : Nat := if b then N else 0

theorem local_thirteen
    (N A B C D E F G : Nat) (x y z u v w : Bool)
    (hA : A ≤ N) (hB : B ≤ N) (hC : C ≤ N) (_hD : D ≤ N)
    (_hE : E ≤ N) (hF : F ≤ N) (hG : G ≤ N)
    (hx : x = true → A = N ∧ D = N)
    (hy : y = true → A = N ∧ B = N ∧ E = N)
    (hz : z = true → 3*N ≤ B+C+F+G)
    (hu : u = true → 2*N ≤ A+D+E)
    (hv : v = true → 2*N ≤ B+E+F)
    (hw : w = true → N ≤ C+F) :
    bw N x + bw N y + bw N z + bw N u + bw N v + bw N w
      ≤ A+B+C+D+E+F+G := by
  cases x <;> cases y <;> cases z <;> cases u <;> cases v <;> cases w <;>
    simp_all [bw] <;> omega

theorem left_boundary
    (N A B C D E F G : Nat) (y z u v w : Bool)
    (hA : A = N) (hD : D = N) (hB : B ≤ N) (hC : C ≤ N)
    (_hE : E ≤ N) (hF : F ≤ N) (hG : G ≤ N)
    (hy : y = true → A = N ∧ B = N ∧ E = N)
    (hz : z = true → 3*N ≤ B+C+F+G)
    (hu : u = true → 2*N ≤ A+D+E)
    (hv : v = true → 2*N ≤ B+E+F)
    (hw : w = true → N ≤ C+F) :
    N + bw N y + bw N z + bw N u + bw N v + bw N w
      ≤ A+B+C+D+E+F+G := by
  cases y <;> cases z <;> cases u <;> cases v <;> cases w <;>
    simp_all [bw] <;> omega

-- Indices refer to the exact POCKET and EDGES order in the companion checker.
-- e17 is the upper-port crossing indicator (either outside mate);
-- e18 is the lower-port crossing indicator.
def occ (t e : Nat → Nat) (v : Nat) : Nat := t v + match v with
  | 0 => e 0
  | 1 => e 1 + e 17
  | 2 => e 0 + e 2 + e 3
  | 3 => e 2 + e 4 + e 5
  | 4 => e 1 + e 4 + e 18
  | 5 => e 6
  | 6 => e 7 + e 8
  | 7 => e 3 + e 7 + e 9 + e 10
  | 8 => e 5 + e 9 + e 11
  | 9 => e 6 + e 12
  | 10 => e 12 + e 13
  | 11 => e 8 + e 13 + e 14
  | 12 => e 10 + e 14 + e 15
  | 13 => e 11 + e 15 + e 16
  | 14 => e 16
  | _ => 0

def pocketLhs (t e : Nat → Nat) : Nat :=
  1*(occ t e 0) +
  2*(t 2 + occ t e 0 + occ t e 3) +
  1*(2*(t 2) + occ t e 0 + occ t e 3 + occ t e 7) +
  4*(t 4 + occ t e 1) +
  1*(t 6 + occ t e 7 + occ t e 11) +
  1*(t 8 + occ t e 3 + occ t e 7) +
  4*(t 9 + occ t e 5 + occ t e 10) +
  3*(t 11 + occ t e 6 + occ t e 12) +
  1*(t 12 + occ t e 7 + occ t e 13) +
  3*(t 13 + occ t e 8 + occ t e 14) +
  1*(occ t e 14)

def pocketW (t e : Nat → Nat) : Nat :=
  t 0 + t 1 + t 2 + t 3 + t 4 + t 5 + t 6 + t 7 + t 8 + t 9 + t 10 + t 11 + t 12 + t 13 + t 14 + e 0 + e 1 + e 2 + e 3 + e 4 + e 5 + e 6 + e 7 + e 8 + e 9 + e 10 + e 11 + e 12 + e 13 + e 14 + e 15 + e 16 + e 17

def costly (e : Nat → Nat) : Nat := e 5 + e 7 + e 9 + e 10
def extra (e : Nat → Nat) : Nat := e 13 + e 16

theorem pocket_coefficients (t e : Nat → Nat) :
    pocketLhs t e = 4*pocketW t e + 3*costly e + extra e := by
  simp only [pocketLhs, pocketW, costly, extra, occ]
  omega

theorem pocket_bound (t e : Nat → Nat)
    (h0 : occ t e 0 ≤ 1)
    (h1 : t 2 + occ t e 0 + occ t e 3 ≤ 2)
    (h2 : 2*(t 2) + occ t e 0 + occ t e 3 + occ t e 7 ≤ 3)
    (h3 : t 4 + occ t e 1 ≤ 1)
    (h4 : t 6 + occ t e 7 + occ t e 11 ≤ 2)
    (h5 : t 8 + occ t e 3 + occ t e 7 ≤ 2)
    (h6 : t 9 + occ t e 5 + occ t e 10 ≤ 2)
    (h7 : t 11 + occ t e 6 + occ t e 12 ≤ 2)
    (h8 : t 12 + occ t e 7 + occ t e 13 ≤ 2)
    (h9 : t 13 + occ t e 8 + occ t e 14 ≤ 2)
    (h10 : occ t e 14 ≤ 1)
    : pocketW t e ≤ 9 := by
  have hsum : pocketLhs t e ≤ 39 := by
    unfold pocketLhs
    omega
  have hid := pocket_coefficients t e
  omega

theorem connected_band_count (m W : Nat) (hm : 2 ≤ m)
    (hcover : W ≤ 2*m+6+7*(m-1)) : W+1 ≤ 9*m := by
  omega

theorem whole_board_bound (m J wc wp wi : Nat) (_hm : 2 ≤ m)
    (hc : wc+1 ≤ 9*m) (hp : wp ≤ 9) (hi : wi ≤ 2)
    (hcolour : J = 9*m+19+wc+wp+wi) : J ≤ 18*m+29 := by
  omega

theorem exact_attainer_arithmetic (m : Nat) :
    17*(m+1)+12+m = 18*m+29 := by omega

theorem exterior_token_budget (m J plus minus : Nat)
    (hbound : J ≤ 18*m+29)
    (hcharge : plus + 2*J = minus + 37*m+60) :
    minus+m+2 ≤ plus := by omega

-- First pay exterior negative half units, then the net strip debt.
-- These inequalities certify that list indices are distinct and precede reserve.
theorem token_indices (m plus minus j : Nat)
    (hbudget : minus+m+2 ≤ plus) (hj : j < minus+m) :
    j < plus ∧ j < plus-2 := by omega

theorem unused_tokens (m plus minus : Nat)
    (hbudget : minus+m+2 ≤ plus) : 2 ≤ plus-(minus+m) := by omega

#print axioms local_thirteen
#print axioms left_boundary
#print axioms pocket_coefficients
#print axioms pocket_bound
#print axioms connected_band_count
#print axioms whole_board_bound
#print axioms exact_attainer_arithmetic
#print axioms exterior_token_budget
#print axioms token_indices
#print axioms unused_tokens
end SubQuorum.ConnectedBandIntegerCompensation
