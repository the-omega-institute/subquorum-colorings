import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 16384
set_option maxHeartbeats 0

/- Algebra and arbitrary-length state induction for the boundary-withdrawal
   theorem. The graph-coordinate reduction and frozen construction are written
   proofs, not encoded here. No custom axioms, sorry or native_decide. -/
namespace SubQuorum.BoundaryWithdrawalCompensation

def bw (N : Nat) (b : Bool) : Nat := if b then N else 0

theorem saturated_input_state
    (N A B C D E F G : Nat) (y z u v w : Bool) (hN : 0 < N)
    (_hA : A ≤ N) (_hB : B ≤ N) (_hC : C ≤ N) (hD : D = N)
    (hE : E ≤ N) (hF : F ≤ N) (hG : G ≤ N)
    (hy : y = true → A=N ∧ B=N ∧ E=N)
    (hz : z = true → 3*N ≤ B+C+F+G)
    (hu : u = true → 2*N ≤ A+D+E)
    (hv : v = true → 2*N ≤ B+E+F)
    (hw : w = true → N ≤ C+F)
    (heq : A+B+C+D+E+F+G = bw N y+bw N z+bw N u+bw N v+bw N w) :
    y=false ∧ z=false ∧ u=true ∧ v=true ∧ w=true ∧
      A=0 ∧ B=0 ∧ C=0 ∧ E=N ∧ F=N ∧ G=0 := by
  cases y <;> cases z <;> cases u <;> cases v <;> cases w <;>
    simp_all [bw] <;> omega

theorem right_end_bound (N A B C : Nat) (x y u w : Bool)
    (_hA : A ≤ N) (_hB : B ≤ N) (_hC : C ≤ N)
    (hx : x=true → A=N ∧ B=N) (hy : y=true → A=N ∧ C=N)
    (hu : u=true → 2*N ≤ A+B+C) :
    bw N x+bw N y+bw N u+bw N w ≤ N+A+B+C := by
  cases x <;> cases y <;> cases u <;> cases w <;> simp_all [bw] <;> omega

theorem right_end_input_bound (N A B C : Nat) (y u w : Bool)
    (_hA : A ≤ N) (_hB : B=N) (_hC : C ≤ N)
    (hy : y=true → A=N ∧ C=N) (hu : u=true → 2*N ≤ A+B+C) :
    bw N y+bw N u+bw N w ≤ A+B+C := by
  cases y <;> cases u <;> cases w <;> simp_all [bw] <;> omega

-- Indices: sorted AP, then sorted internal edges followed by PORTS in checker.
def occ (t e : Nat → Nat) (v : Nat) : Nat := t v + match v with
  | 0 => e 0
  | 1 => e 1 + e 20 + e 21
  | 2 => e 0 + e 2 + e 3
  | 3 => e 2 + e 4 + e 5
  | 4 => e 1 + e 4 + e 6 + e 22
  | 5 => e 7
  | 6 => e 8 + e 9
  | 7 => e 3 + e 8 + e 10 + e 11
  | 8 => e 5 + e 10 + e 12 + e 13
  | 9 => e 6 + e 12 + e 14 + e 23
  | 10 => e 7 + e 15
  | 11 => e 15 + e 16
  | 12 => e 9 + e 16 + e 17
  | 13 => e 11 + e 17 + e 18
  | 14 => e 13 + e 18 + e 19
  | 15 => e 14 + e 19 + e 24
  | _ => 0

def pocketLhs (t e : Nat → Nat) : Nat :=
  1*(occ t e 0) +
  4*(t 2 + occ t e 0 + occ t e 3) +
  1*(2*(t 2) + occ t e 0 + occ t e 3 + occ t e 7) +
  4*(t 4 + occ t e 1) +
  2*(t 4 + occ t e 1 + occ t e 9) +
  2*(occ t e 6) +
  2*(t 6 + occ t e 7 + occ t e 12) +
  3*(t 8 + occ t e 9 + occ t e 14) +
  1*(3*(t 8) + occ t e 3 + occ t e 7 + occ t e 9 + occ t e 14) +
  6*(t 10 + occ t e 5 + occ t e 11) +
  2*(t 12 + occ t e 6 + occ t e 13) +
  2*(2*(t 13) + occ t e 7 + occ t e 12 + occ t e 14)

def pocketW (t e : Nat → Nat) : Nat :=
  t 0 + t 1 + t 2 + t 3 + t 4 + t 5 + t 6 + t 7 + t 8 + t 9 + t 10 + t 11 + t 12 + t 13 + t 14 + t 15 + e 0 + e 1 + e 2 + e 3 + e 4 + e 5 + e 6 + e 7 + e 8 + e 9 + e 10 + e 11 + e 12 + e 13 + e 14 + e 15 + e 16 + e 17 + e 18 + e 19 + e 20 + e 21 + e 23

def extra (e : Nat → Nat) : Nat := 4*(e 8) + 2*(e 9) + 2*(e 11) + 4*(e 16) + 2*(e 18)

theorem pocket_coefficients (t e : Nat → Nat) :
    pocketLhs t e + 6*(t 15) = 6*pocketW t e + extra e := by
  simp only [pocketLhs, pocketW, extra, occ]
  omega

theorem pocket_bound (t e : Nat → Nat)
    (h0 : occ t e 0 ≤ 1)
    (h1 : t 2 + occ t e 0 + occ t e 3 ≤ 2)
    (h2 : 2*(t 2) + occ t e 0 + occ t e 3 + occ t e 7 ≤ 3)
    (h3 : t 4 + occ t e 1 ≤ 1)
    (h4 : t 4 + occ t e 1 + occ t e 9 ≤ 2)
    (h5 : occ t e 6 ≤ 1)
    (h6 : t 6 + occ t e 7 + occ t e 12 ≤ 2)
    (h7 : t 8 + occ t e 9 + occ t e 14 ≤ 2)
    (h8 : 3*(t 8) + occ t e 3 + occ t e 7 + occ t e 9 + occ t e 14 ≤ 4)
    (h9 : t 10 + occ t e 5 + occ t e 11 ≤ 2)
    (h10 : t 12 + occ t e 6 + occ t e 13 ≤ 2)
    (h11 : 2*(t 13) + occ t e 7 + occ t e 12 + occ t e 14 ≤ 3)
    : pocketW t e ≤ 9+t 15 := by
  have hsum : pocketLhs t e ≤ 58 := by
    unfold pocketLhs
    omega
  have hid := pocket_coefficients t e
  omega

theorem pocket_gain_state (W tr oq : Nat)
    (hr : tr ≤ 1) (hq : oq ≤ 1)
    (h1 : W ≤ 9+tr) (h2 : W ≤ 9+oq) (hW : W=10) : tr=1 ∧ oq=1 := by
  omega

def blockSum (b : Nat → Nat) : Nat → Nat
  | 0 => 0
  | n+1 => blockSum b n + b n

theorem block_sum_bound (n : Nat) (b : Nat → Nat)
    (hb : ∀ i, i<n → b i ≤ 7) : blockSum b n ≤ 7*n := by
  induction n with
  | zero => simp [blockSum]
  | succ n ih =>
    have hn : b n ≤ 7 := hb n (by omega)
    have hpre : blockSum b n ≤ 7*n := ih (fun i hi => hb i (by omega))
    simp only [blockSum]
    omega

theorem saturated_prefix_state (n : Nat) (p : Nat → Bool) (b : Nat → Nat)
    (hb : ∀ i, i<n → b i ≤ 7) (h0 : p 0=true)
    (hprop : ∀ i, i<n → p i=true → b i=7 → p (i+1)=true) :
    blockSum b n ≤ 7*n ∧ (blockSum b n=7*n → p n=true) := by
  induction n with
  | zero => constructor; simp [blockSum]; intro _; exact h0
  | succ n ih =>
    have hprev := ih (fun i hi => hb i (by omega))
      (fun i hi hs he => hprop i (by omega) hs he)
    have hn : b n ≤ 7 := hb n (by omega)
    constructor
    · simp only [blockSum]; omega
    · intro heq
      have heq' : blockSum b n+b n=7*(n+1) := heq
      have heqp : blockSum b n=7*n := by omega
      have hbn : b n=7 := by omega
      exact hprop n (by omega) (hprev.2 heqp) hbn

theorem chain_compensation (n r : Nat) (p : Nat → Bool) (b : Nat → Nat)
    (hb : ∀ i, i<n → b i ≤ 7) (h0 : p 0=true)
    (hprop : ∀ i, i<n → p i=true → b i=7 → p (i+1)=true)
    (hr : r ≤ 4) (hend : p n=true → r ≤ 3) : blockSum b n+r ≤ 7*n+3 := by
  have hp := saturated_prefix_state n p b hb h0 hprop
  by_cases heq : blockSum b n=7*n
  · have hsmall := hend (hp.2 heq)
    omega
  · omega

theorem whole_board_bound (m J L S r : Nat)
    (hL : L ≤ 10) (hS : S ≤ 7*m) (hr : r ≤ 4)
    (hcomp : L=10 → S+r ≤ 7*m+3)
    (hcolour : J=9*m+16+L+2*m+S+r) : J ≤ 18*m+29 := by
  by_cases heq : L=10
  · have hc := hcomp heq
    omega
  · omega

theorem potential_prefix (n : Nat) (p b : Nat → Nat)
    (hstep : ∀ i, i<n → b i+p i ≤ 7+p (i+1)) :
    blockSum b n+p 0 ≤ 7*n+p n := by
  induction n with
  | zero => simp [blockSum]
  | succ n ih =>
    have hp := ih (fun i hi => hstep i (by omega))
    have hn := hstep n (by omega)
    simp only [blockSum]
    omega

theorem potential_whole_board_bound (m J L S r p0 pm : Nat)
    (hL : L ≤ 9+p0) (hS : S+p0 ≤ 7*m+pm) (hr : r+pm ≤ 4)
    (hcolour : J=9*m+16+L+2*m+S+r) : J ≤ 18*m+29 := by omega

theorem physical_token_budget (m J plus minus : Nat)
    (hJ : J ≤ 18*m+29) (hcharge : plus+2*J=minus+37*m+60) :
    minus+m+2 ≤ plus := by omega

#print axioms saturated_input_state
#print axioms right_end_bound
#print axioms right_end_input_bound
#print axioms pocket_coefficients
#print axioms pocket_bound
#print axioms pocket_gain_state
#print axioms block_sum_bound
#print axioms saturated_prefix_state
#print axioms chain_compensation
#print axioms whole_board_bound
#print axioms potential_prefix
#print axioms potential_whole_board_bound
#print axioms physical_token_budget
end SubQuorum.BoundaryWithdrawalCompensation
