import Lean.Elab.Tactic.Omega
set_option autoImplicit false
namespace SubQuorum.TwoGateRematchingRepair

/- General three-source interface: B,C share gate U and its beta fallback;
D,C share gate W. Every resource identity has capacity one. -/
inductive BRoute (I : Type) where
  | direct : I → BRoute I
  | viaU : I → BRoute I
  | beta : BRoute I
inductive DRoute (I : Type) where
  | direct : I → DRoute I
  | viaW : I → DRoute I
inductive CRoute (I : Type) where
  | direct : I → CRoute I
  | viaU : I → CRoute I
  | beta : CRoute I
  | viaW : I → CRoute I

def bUnit {I : Type} : BRoute I → Option I
  | .direct i | .viaU i => some i
  | .beta => none
def dUnit {I : Type} : DRoute I → Option I
  | .direct i | .viaW i => some i
def cUnit {I : Type} : CRoute I → Option I
  | .direct i | .viaU i | .viaW i => some i
  | .beta => none

def different {I : Type} : Option I → Option I → Prop
  | some i, some j => i ≠ j
  | _, _ => True

def bAllowed {I : Type} (P U : I → Prop) : BRoute I → Prop
  | .direct i => P i
  | .viaU i => U i
  | .beta => True
def dAllowed {I : Type} (L W : I → Prop) : DRoute I → Prop
  | .direct i => L i
  | .viaW i => W i
def cAllowed {I : Type} (R U W : I → Prop) : CRoute I → Prop
  | .direct i => R i
  | .viaU i => U i
  | .beta => True
  | .viaW i => W i

def gateU {I : Type} : BRoute I → CRoute I → Prop
  | .viaU _, .viaU _ | .viaU _, .beta | .beta, .viaU _ | .beta, .beta => False
  | _, _ => True
def gateW {I : Type} : DRoute I → CRoute I → Prop
  | .viaW _, .viaW _ => False
  | _, _ => True

def Valid {I : Type} (P L R U W : I → Prop)
    (b : BRoute I) (d : DRoute I) (c : CRoute I) : Prop :=
  bAllowed P U b ∧ dAllowed L W d ∧ cAllowed R U W c ∧
  different (bUnit b) (dUnit d) ∧ different (bUnit b) (cUnit c) ∧
  different (dUnit d) (cUnit c) ∧ gateU b c ∧ gateW d c

def Repair {I : Type} (P L R W : I → Prop) : Prop :=
  (∃ x y, L x ∧ (P y ∨ R y ∨ W y) ∧ x ≠ y) ∨
  (∃ x y, W x ∧ (P y ∨ R y) ∧ x ≠ y)

/-- Complete full-payment criterion, for arbitrary original identity types and
arbitrary available support predicates. U cannot fix a value deficit by itself:
its interval route shares the entrance of the unconditional beta fallback. -/
theorem full_payment_iff {I : Type} (P L R U W : I → Prop) :
    (∃ b d c, Valid P L R U W b d c) ↔ Repair P L R W := by
  constructor
  · rintro ⟨b,d,c,hb,hd,hc,hbd,hbc,hdc,hu,hw⟩
    cases b with
    | direct b =>
      cases d with
      | direct d => exact Or.inl ⟨d,b,hd,Or.inl hb,Ne.symm hbd⟩
      | viaW d => exact Or.inr ⟨d,b,hd,Or.inl hb,Ne.symm hbd⟩
    | viaU b =>
      cases c with
      | direct c =>
        cases d with
        | direct d => exact Or.inl ⟨d,c,hd,Or.inr (Or.inl hc),hdc⟩
        | viaW d => exact Or.inr ⟨d,c,hd,Or.inr hc,hdc⟩
      | viaU c => exact False.elim hu
      | beta => exact False.elim hu
      | viaW c =>
        cases d with
        | direct d => exact Or.inl ⟨d,c,hd,Or.inr (Or.inr hc),hdc⟩
        | viaW d => exact False.elim hw
    | beta =>
      cases c with
      | direct c =>
        cases d with
        | direct d => exact Or.inl ⟨d,c,hd,Or.inr (Or.inl hc),hdc⟩
        | viaW d => exact Or.inr ⟨d,c,hd,Or.inr hc,hdc⟩
      | viaU c => exact False.elim hu
      | beta => exact False.elim hu
      | viaW c =>
        cases d with
        | direct d => exact Or.inl ⟨d,c,hd,Or.inr (Or.inr hc),hdc⟩
        | viaW d => exact False.elim hw
  · intro h
    rcases h with ⟨x,y,hl,hp | hr | hw,hne⟩ | ⟨x,y,hw,hp | hr,hne⟩
    · exact ⟨.direct y,.direct x,.beta,hp,hl,True.intro,Ne.symm hne,
        True.intro,True.intro,True.intro,True.intro⟩
    · exact ⟨.beta,.direct x,.direct y,True.intro,hl,hr,True.intro,
        True.intro,hne,True.intro,True.intro⟩
    · exact ⟨.beta,.direct x,.viaW y,True.intro,hl,hw,True.intro,
        True.intro,hne,True.intro,True.intro⟩
    · exact ⟨.direct y,.viaW x,.beta,hp,hw,True.intro,Ne.symm hne,
        True.intro,True.intro,True.intro,True.intro⟩
    · exact ⟨.beta,.viaW x,.direct y,True.intro,hw,hr,True.intro,
        True.intro,hne,True.intro,True.intro⟩

/-- Availability confined to the two shared gates cannot pay all three,
even if there are many different available W units. -/
theorem no_direct_D_or_B_or_C {I : Type} (U W : I → Prop) :
    ¬ ∃ b d c, Valid (fun _ => False) (fun _ => False)
      (fun _ => False) U W b d c := by
  rw [full_payment_iff]
  simp [Repair]

/-- Two different identities shared by P and L do suffice: C takes the beta,
B and D take separate direct units. Identity inequality is indispensable. -/
theorem two_shared_direct_units {I : Type} (P L R U W : I → Prop)
    (x y : I) (hl : L x) (hp : P y) (hne : x ≠ y) :
    ∃ b d c, Valid P L R U W b d c := by
  apply (full_payment_iff P L R U W).mpr
  exact Or.inl ⟨x,y,hl,Or.inl hp,hne⟩

#print axioms full_payment_iff
#print axioms no_direct_D_or_B_or_C
#print axioms two_shared_direct_units
end SubQuorum.TwoGateRematchingRepair
