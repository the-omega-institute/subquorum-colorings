import Lean.Elab.Tactic.Omega
set_option autoImplicit false
namespace SubQuorum.LowerGuardMergerFrontier

def sum13 (f : Nat → Nat) : Nat :=
  f 0+f 1+f 2+f 3+f 4+f 5+f 6+f 7+f 8+f 9+f 10+f 11+f 12

/-- d,u,g,b,v,h,e,a,L,z,l,s,r; all terms are occupation constraints. -/
def jointLHS (t o : Nat → Nat) : Nat :=
  3*(t 2+o 0)+3*(t 4+o 1)+2*(t 5+o 6)+(t 5+o 9)+
  3*(t 3+o 2+o 4)+2*(t 6+o 5+o 10)+2*(t 7+o 3+o 6)+
  (t 7+o 3+o 11)+(t 9+o 5+o 8)+2*(t 9+o 8+o 10)+
  2*(t 10+o 9+o 11)+3*(t 11+o 7+o 12)+
  3*(t 0+t 8+t 12)+3*t 1

theorem joint_identity (t o : Nat → Nat) :
    jointLHS t o+t 6+t 10 = 3*(sum13 t+sum13 o)+o 6+o 10 := by
  simp only [jointLHS,sum13]
  omega

theorem joint_weighted_bound (t o : Nat → Nat)
    (a0 : t 2+o 0 ≤ 1) (a1 : t 4+o 1 ≤ 1)
    (a2 : t 5+o 6 ≤ 1) (a3 : t 5+o 9 ≤ 1)
    (w0 : t 3+o 2+o 4 ≤ 2) (w1 : t 6+o 5+o 10 ≤ 2)
    (w2 : t 7+o 3+o 6 ≤ 2) (w3 : t 7+o 3+o 11 ≤ 2)
    (w4 : t 9+o 5+o 8 ≤ 2) (w5 : t 9+o 8+o 10 ≤ 2)
    (w6 : t 10+o 9+o 11 ≤ 2) (w7 : t 11+o 7+o 12 ≤ 2)
    (td : t 0 ≤ 1) (tL : t 8 ≤ 1) (tr : t 12 ≤ 1) (tu : t 1=0)
    (se : t 6 ≤ o 6) (sl : t 10 ≤ o 10) :
    sum13 t+sum13 o ≤ 16 := by
  have hi := joint_identity t o
  have upper : jointLHS t o ≤ 50 := by
    unfold jointLHS
    omega
  omega

def sum7 (f : Nat → Nat) : Nat := f 0+f 1+f 2+f 3+f 4+f 5+f 6

/-- h,a,L,z,l,s,r. Charge eleven has a forced unmatched centre. -/
def lowerLHS (t o : Nat → Nat) : Nat :=
  (t 0+o 3)+(t 3+o 0+o 2)+(t 5+o 1+o 6)+
  t 1+t 6+t 2+t 4+o 4+o 5

theorem lower_identity (t o : Nat → Nat) :
    lowerLHS t o=sum7 t+sum7 o := by
  simp only [lowerLHS,sum7]
  omega

theorem lower_occupation_bound (t o : Nat → Nat)
    (anchor : t 0+o 3 ≤ 1) (wz : t 3+o 0+o 2 ≤ 2)
    (ws : t 5+o 1+o 6 ≤ 2)
    (ta : t 1 ≤ 1) (tr : t 6 ≤ 1) (tL : t 2 ≤ 1) (tl : t 4 ≤ 1)
    (ol : o 4 ≤ 1) (os : o 5 ≤ 1) : sum7 t+sum7 o ≤ 11 := by
  have hi := lower_identity t o
  have upper : lowerLHS t o ≤ 11 := by unfold lowerLHS; omega
  omega

theorem lower_equality_data (t o : Nat → Nat)
    (anchor : t 0+o 3 ≤ 1) (wz : t 3+o 0+o 2 ≤ 2)
    (ws : t 5+o 1+o 6 ≤ 2)
    (ta : t 1 ≤ 1) (tr : t 6 ≤ 1) (tL : t 2 ≤ 1) (tl : t 4 ≤ 1)
    (ol : o 4 ≤ 1) (os : o 5 ≤ 1)
    (eq : sum7 t+sum7 o=11) : t 1=1 ∧ t 4=1 ∧ t 6=1 ∧ o 5=1 := by
  have hi := lower_identity t o
  unfold lowerLHS at hi
  omega

theorem lower_matching_bound (t o p : Nat → Nat)
    (anchor : t 0+o 3 ≤ 1) (wz : t 3+o 0+o 2 ≤ 2)
    (ws : t 5+o 1+o 6 ≤ 2)
    (ta : t 1 ≤ 1) (tr : t 6 ≤ 1) (tL : t 2 ≤ 1) (tl : t 4 ≤ 1)
    (ol : o 4 ≤ 1) (os : o 5 ≤ 1)
    (occupation : ∀ i, o i=t i+p i) (bounded : ∀ i, o i ≤ 1)
    (centreHasMate : p 5 ≤ p 1+p 4+p 6) : sum7 t+sum7 o ≤ 10 := by
  have bound := lower_occupation_bound t o anchor wz ws ta tr tL tl ol os
  by_cases notBound : sum7 t+sum7 o ≤ 10
  · exact notBound
  · have equality : sum7 t+sum7 o=11 := by omega
    obtain ⟨ea,el,er,es⟩ := lower_equality_data t o anchor wz ws ta tr tL tl ol os equality
    have oa := occupation 1
    have ol' := occupation 4
    have or' := occupation 6
    have os' := occupation 5
    have ba := bounded 1
    have bl := bounded 4
    have br := bounded 6
    omega

theorem two_guard_component_sum (k n0 ng nh nb g h extra : Nat)
    (partition : n0+ng+nh+nb+1=k) (upperCount : g=ng+nb) (lowerCount : h=nh+nb)
    (capacity : extra ≤ 19+10*n0+14*ng+12*nh+16*nb+4) :
    extra ≤ 10*k+13+4*g+2*h := by omega

theorem lower_permissions_cancel (k g h extra total : Nat)
    (extraBound : extra ≤ 10*k+13+4*g+2*h)
    (oldCount : 2*total+2*g+2*h=24*k+12+extra) : total ≤ 17*k+12+g := by omega

theorem sharp_margin (k g total : Nat) (valid : g ≤ k)
    (bound : total ≤ 17*k+12+g) : total+(k-g) ≤ 18*k+12 := by omega

/-- A matched endpoint cannot use its own mate as a strict freezing witness. -/
theorem strict_witness_not_mate {V : Type} (P T : V → Prop) (mate : V → V)
    (rank : V → Nat) (v w : V) (inv : mate (mate v)=v)
    (pm : P (mate v)) (disjoint : ∀ u, P u → ¬T u)
    (witness : T w ∨ (P w ∧ rank (mate w)<rank v)) : w ≠ mate v := by
  intro eq
  subst w
  rcases witness with selected | ⟨_,lower⟩
  · exact disjoint (mate v) pm selected
  · rw [inv] at lower
    omega

def Certified {V : Type} (P T : V → Prop) (adj : V → V → Prop)
    (mate : V → V) (rank : V → Nat) (v : V) : Prop :=
  ∃ a b, a ≠ b ∧ adj v a ∧ adj v b ∧
    (T a ∨ (P a ∧ rank (mate a)<rank v)) ∧
    (T b ∨ (P b ∧ rank (mate b)<rank v))

theorem mate_plus_one_exclusion {V : Type} (P T : V → Prop) (mate : V → V)
    (rank : V → Nat) (adj : V → V → Prop) (v z : V)
    (inv : mate (mate v)=v) (pm : P (mate v))
    (disjoint : ∀ u, P u → ¬T u)
    (only : ∀ u, adj v u → (P u ∨ T u) → u=mate v ∨ u=z) :
    ¬Certified P T adj mate rank v := by
  rintro ⟨a,b,distinct,ha,hb,wa,wb⟩
  have na := strict_witness_not_mate P T mate rank v a inv pm disjoint wa
  have nb := strict_witness_not_mate P T mate rank v b inv pm disjoint wb
  have oa : P a ∨ T a := by
    rcases wa with ht | ⟨hp,_⟩
    · exact Or.inr ht
    · exact Or.inl hp
  have ob : P b ∨ T b := by
    rcases wb with ht | ⟨hp,_⟩
    · exact Or.inr ht
    · exact Or.inl hp
  have az := (only a ha oa).resolve_left na
  have bz := (only b hb ob).resolve_left nb
  exact distinct (az.trans bz.symm)

/-- Two alternative degree-two traps force a guard to remain selected.
    The grid adapter supplies the displayed eligible-neighbour hypotheses. -/
theorem selection_forced_by_two_traps {V : Type} (P T : V → Prop) (mate : V → V)
    (rank : V → Nat) (adj : V → V → Prop) (old lower upper z : V)
    (oldP : P old) (inv : ∀ v, mate (mate v)=v)
    (closed : ∀ v, P v → P (mate v)) (disjoint : ∀ v, P v → ¬T v)
    (complete : ∀ v, P v → Certified P T adj mate rank v)
    (lowerTrap : P lower → ∀ u, adj lower u → (P u ∨ T u) → u=mate lower ∨ u=z)
    (oldTrap : ¬P lower → ¬T lower → ∀ u,
      adj old u → (P u ∨ T u) → u=mate old ∨ u=upper) : T lower := by
  by_cases absent : T lower
  · exact absent
  · by_cases endpoint : P lower
    · exact False.elim (mate_plus_one_exclusion P T mate rank adj lower z (inv lower)
        (closed lower endpoint) disjoint (lowerTrap endpoint) (complete lower endpoint))
    · exact False.elim (mate_plus_one_exclusion P T mate rank adj old upper (inv old)
        (closed old oldP) disjoint (oldTrap endpoint absent) (complete old oldP))

theorem explicit_lower_patch_counts (k h selected edges : Nat)
    (selectedCount : selected+h=13*k+11) (edgeCount : edges=4*k+1+h) :
    selected+edges=17*k+12 := by omega

theorem physical_exterior_cut (k g strip outside : Int)
    (stripCount : strip=1-k) (whole : strip+outside ≥ 2*(k-g)) :
    outside ≥ 3*k-1-2*g := by omega

#print axioms joint_identity
#print axioms joint_weighted_bound
#print axioms lower_identity
#print axioms lower_occupation_bound
#print axioms lower_equality_data
#print axioms lower_matching_bound
#print axioms two_guard_component_sum
#print axioms lower_permissions_cancel
#print axioms sharp_margin
#print axioms strict_witness_not_mate
#print axioms mate_plus_one_exclusion
#print axioms selection_forced_by_two_traps
#print axioms explicit_lower_patch_counts
#print axioms physical_exterior_cut

end SubQuorum.LowerGuardMergerFrontier
