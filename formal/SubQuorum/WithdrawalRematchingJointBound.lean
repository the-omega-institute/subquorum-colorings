import Lean.Elab.Tactic.Omega

set_option autoImplicit false
namespace SubQuorum.WithdrawalRematchingJointBound

/-- A selected site with an old endpoint neighbour excludes any other
    occupied neighbour, without referring to that old endpoint's mate. -/
theorem anchored_pair (t o : Nat) (ht : t ≤ 1) (ho : o ≤ 1)
    (selected : t = 1 → o = 0) : t + o ≤ 1 := by
  by_cases h : t = 1
  · have := selected h
    omega
  · omega

theorem wedge (t oa ob : Nat) (ht : t ≤ 1) (ha : oa ≤ 1) (hb : ob ≤ 1)
    (selected : t = 1 → oa + ob ≤ 1) : t + oa + ob ≤ 2 := by
  by_cases h : t = 1
  · have := selected h
    omega
  · omega

def sum9 (f : Nat → Nat) : Nat :=
  f 0+f 1+f 2+f 3+f 4+f 5+f 6+f 7+f 8

/-- d,g,b,u,v,a,s,l,r: the certificate is expressed entirely in occupation
    indicators and therefore permits matching edges crossing the tree cut. -/
def weightedLHS (t o : Nat → Nat) : Nat :=
  (t 1+o 0)+(t 4+o 3)+(t 2+o 1+o 4)+
  (t 5+o 2+o 6)+(t 6+o 7+o 8)+t 0+t 7+t 8+o 5+t 3

theorem occupation_identity (t o : Nat → Nat) :
    weightedLHS t o = sum9 t + sum9 o := by
  simp only [weightedLHS,sum9]
  omega

theorem tree_occupation_bound (t o : Nat → Nat)
    (ag : t 1+o 0 ≤ 1) (av : t 4+o 3 ≤ 1)
    (wb : t 2+o 1+o 4 ≤ 2) (wa : t 5+o 2+o 6 ≤ 2)
    (ws : t 6+o 7+o 8 ≤ 2)
    (td : t 0 ≤ 1) (tl : t 7 ≤ 1) (tr : t 8 ≤ 1)
    (oa : o 5 ≤ 1) (tu : t 3=0) : sum9 t+sum9 o ≤ 12 := by
  have hi := occupation_identity t o
  have hb : weightedLHS t o ≤ 12 := by
    unfold weightedLHS
    omega
  omega

theorem tree_charge_bound (t o : Nat → Nat) (p : Nat)
    (occupationCount : sum9 o = sum9 t+p)
    (bound : sum9 t+sum9 o ≤ 12) : 2*sum9 t+p ≤ 12 := by omega

/-- Boundary crossings at U have coefficient zero in the pocket certificate;
    crossings at V have coefficient three. The expensive-edge sum is nonnegative. -/
theorem pocket_integer_bound (selected internal crossV costly lhs : Nat)
    (identity : lhs=3*(selected+internal+crossV)+2*costly)
    (bound : lhs ≤ 29) : selected+internal+crossV ≤ 9 := by omega

theorem pocket_signed_boundary_bound (selected internal crossU crossV newP : Nat)
    (endpointCount : newP=2*internal+crossU+crossV)
    (localBound : selected+internal+crossV ≤ 9) :
    2*selected+newP+crossV ≤ 18+crossU := by omega

theorem pocket_half_slack (selected internal crossU crossV newP : Nat)
    (portCapacity : crossU ≤ 1)
    (endpointCount : newP=2*internal+crossU+crossV)
    (localBound : selected+internal+crossV ≤ 9) :
    2*selected+newP ≤ 19 := by omega

theorem gate_occupation_bound (tu tv ou ov : Nat)
    (upperNotSelected : tu=0) (anchor : tv+ou ≤ 1)
    (lowerOccupied : ov ≤ 1) : tu+tv+ou+ov ≤ 2 := by omega

/-- Closure under the ACTUAL matching is used only for an untouched star. -/
theorem closed_star_bound (selected actualEdges : Nat)
    (matchingSize : actualEdges ≤ 1)
    (noEdge : actualEdges=0 → selected ≤ 3)
    (oneEdge : actualEdges=1 → selected ≤ 2) :
    2*selected+2*actualEdges ≤ 6 := by
  by_cases h : actualEdges=0
  · have := noEdge h
    omega
  · have h1 : actualEdges=1 := by omega
    have := oneEdge h1
    omega

theorem disjoint_component_sum (k q extraTwice : Nat) (valid : q+1 ≤ k)
    (partitionBound : extraTwice ≤ 19+12*q+8*(k-1-q)+2*(k+1)) :
    extraTwice ≤ 10*k+13+4*q := by omega

/-- The half-unit certificate loss occurs ONCE, in the fixed pocket. -/
theorem one_global_integer_rounding (k q extraTwice total : Nat)
    (extraBound : extraTwice ≤ 10*k+13+4*q)
    (oldCount : 2*total+2*q=24*k+12+extraTwice) :
    total ≤ 17*k+12+q := by omega

theorem joint_margin (k q total : Nat) (valid : q ≤ k)
    (bound : total ≤ 17*k+12+q) : total+(k-q) ≤ 18*k+12 := by omega

/-- At a sharp configuration the total doubled certificate slack is one.
    This is a consequence of counts, not a claim of local realizability. -/
theorem sharp_slack_identity (k q extraTwice : Nat)
    (oldCount : 2*(17*k+12+q)+2*q=24*k+12+extraTwice) :
    extraTwice+1=10*k+13+4*q := by omega

theorem exterior_signed_cut (k q strip outside : Int)
    (stripCount : strip=1-k) (wholeBound : strip+outside ≥ 2*(k-q)) :
    outside ≥ 3*k-1-2*q := by omega

/-- Positive exterior tokens must first cover all exterior negative charges;
    only then may the net strip deficit and remaining margin be counted. -/
theorem actual_token_capacity (k q positive negative : Nat)
    (nonempty : 1 ≤ k) (valid : q ≤ k)
    (signedCut : negative+3*k ≤ positive+1+2*q) :
    negative+(k-1)+2*(k-q) ≤ positive := by omega

def includeToken {demand available : Nat} (capacity : demand ≤ available)
    (i : Fin demand) : Fin available := ⟨i.val, Nat.lt_of_lt_of_le i.isLt capacity⟩

theorem physical_token_injective {demand available : Nat} (capacity : demand ≤ available) :
    Function.Injective (includeToken capacity) := by
  intro a b same
  apply Fin.ext
  exact congrArg (fun x : Fin available => x.val) same

theorem unspent_token_margin (k q positive negative : Nat)
    (capacity : negative+(k-1)+2*(k-q) ≤ positive) :
    positive-(negative+(k-1)) ≥ 2*(k-q) := by omega

#print axioms anchored_pair
#print axioms wedge
#print axioms occupation_identity
#print axioms tree_occupation_bound
#print axioms tree_charge_bound
#print axioms pocket_integer_bound
#print axioms pocket_signed_boundary_bound
#print axioms pocket_half_slack
#print axioms gate_occupation_bound
#print axioms closed_star_bound
#print axioms disjoint_component_sum
#print axioms one_global_integer_rounding
#print axioms joint_margin
#print axioms sharp_slack_identity
#print axioms exterior_signed_cut
#print axioms actual_token_capacity
#print axioms physical_token_injective
#print axioms unspent_token_margin

end SubQuorum.WithdrawalRematchingJointBound
