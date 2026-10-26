import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 16384
set_option maxHeartbeats 0

/- Colour factorization and conditional exact interfaces, for arbitrary types.
   The concrete grid matching, coordinates and trap adapter are written and
   independently executable; this file does not claim that full adapter. -/
namespace SubQuorum.TwoPortUnboundedRematching
universe u v

def Supported {V : Type u} (Adj : V → V → Prop) (K P F : V → Prop)
    (mate : V → V) (x : V) : Prop :=
  ∃ a b, a≠b ∧ Adj x a ∧ Adj x b ∧
    (K a ∨ P a ∧ F (mate a)) ∧ (K b ∨ P b ∧ F (mate b))

def Closed {V : Type u} (Adj : V → V → Prop) (K P : V → Prop)
    (mate : V → V) (F : V → Prop) : Prop :=
  ∀ x, P x → Supported Adj K P F mate x → F x

def Frozen {V : Type u} (Adj : V → V → Prop) (K P : V → Prop)
    (mate : V → V) (x : V) : Prop :=
  ∀ F : V → Prop, Closed Adj K P mate F → F x

/-- Adjacency and actual matching each reverse the bipartition, so an endpoint
    depends only on earlier endpoints of its OWN colour. -/
theorem actual_mate_preserves_dependency_colour {V : Type u}
    (Adj : V → V → Prop) (P : V → Prop) (mate : V → V) (colour : V → Bool)
    (hadj : ∀ x y, Adj x y → colour y = !(colour x))
    (hmate : ∀ y, P y → colour (mate y) = !(colour y)) :
    ∀ x y, Adj x y → P y → colour (mate y)=colour x := by
  intro x y hxy hp
  rw [hmate y hp,hadj x y hxy,Bool.not_not]

/-- Change the initial kept sites arbitrarily away from one colour's
    neighbourhood. Its least freezing closure is unchanged. No assumption on
    freezing of the OTHER colour is needed. -/
theorem colour_freezing_invariant {V : Type u} {C : Type v}
    (Adj : V → V → Prop) (K₁ K₂ P : V → Prop) (mate : V → V)
    (colour : V → C) (c : C)
    (hdep : ∀ x y, Adj x y → P y → colour (mate y)=colour x)
    (hK : ∀ x y, P x → colour x=c → Adj x y → (K₁ y ↔ K₂ y)) :
    ∀ x, P x → colour x=c →
      (Frozen Adj K₁ P mate x ↔ Frozen Adj K₂ P mate x) := by
  classical
  have one_way : ∀ K L : V → Prop,
      (∀ x y, P x → colour x=c → Adj x y → (K y → L y)) →
      ∀ x, P x → colour x=c → Frozen Adj K P mate x → Frozen Adj L P mate x := by
    intro K L hchange x _hx hcx hf F hc
    let G : V → Prop := fun y => colour y≠c ∨ F y
    have hG : Closed Adj K P mate G := by
      intro y hpy hsup
      by_cases hcy : colour y=c
      · apply Or.inr
        apply hc y hpy
        obtain ⟨a,b,hab,hya,hyb,ha,hb⟩ := hsup
        refine ⟨a,b,hab,hya,hyb,?_,?_⟩
        · rcases ha with hk | ⟨hp,hg⟩
          · exact Or.inl (hchange y a hpy hcy hya hk)
          · apply Or.inr
            refine ⟨hp,?_⟩
            rcases hg with hnot | hyes
            · exact False.elim (hnot ((hdep y a hya hp).trans hcy))
            · exact hyes
        · rcases hb with hk | ⟨hp,hg⟩
          · exact Or.inl (hchange y b hpy hcy hyb hk)
          · apply Or.inr
            refine ⟨hp,?_⟩
            rcases hg with hnot | hyes
            · exact False.elim (hnot ((hdep y b hyb hp).trans hcy))
            · exact hyes
      · exact Or.inl hcy
    rcases hf G hG with hnot | hyes
    · exact False.elim (hnot hcx)
    · exact hyes
  intro x hx hcx
  constructor
  · exact one_way K₁ K₂ (fun y z hy hcy hyz => (hK y z hy hcy hyz).mp) x hx hcx
  · exact one_way K₂ K₁ (fun y z hy hcy hyz => (hK y z hy hcy hyz).mpr) x hx hcx

/-- Positive certificates and two input-blocked traps determine the entire
    interface map, with all hypotheses explicit. This does not assert that
    every actual matching on the same footprint has this response. -/
theorem exact_two_input_response {V : Type u}
    (P E B W F : V → Prop) (a b : Prop)
    (hcover : ∀ x, P x → E x ∨ B x ∨ W x)
    (hE : ∀ x, E x → F x)
    (hB : a → ∀ x, B x → F x)
    (hW : b → ∀ x, W x → F x)
    (hnotB : ¬a → ∀ x, B x → ¬F x)
    (hnotW : ¬b → ∀ x, W x → ¬F x) :
    ∀ x, P x → (F x ↔ E x ∨ a ∧ B x ∨ b ∧ W x) := by
  classical
  intro x hp
  constructor
  · intro hf
    rcases hcover x hp with he | hb | hw
    · exact Or.inl he
    · by_cases ha : a
      · exact Or.inr (Or.inl ⟨ha,hb⟩)
      · exact False.elim (hnotB ha x hb hf)
    · by_cases hh : b
      · exact Or.inr (Or.inr ⟨hh,hw⟩)
      · exact False.elim (hnotW hh x hw hf)
  · intro h
    rcases h with he | ⟨ha,hb⟩ | ⟨hh,hw⟩
    · exact hE x he
    · exact hB ha x hb
    · exact hW hh x hw

theorem two_inputs_necessary_sufficient {V : Type u}
    (P E B W F : V → Prop) (a b : Prop)
    (hcover : ∀ x, P x → E x ∨ B x ∨ W x)
    (hE : ∀ x, E x → F x)
    (hB : a → ∀ x, B x → F x)
    (hW : b → ∀ x, W x → F x)
    (hnotB : ¬a → ∀ x, B x → ¬F x)
    (hnotW : ¬b → ∀ x, W x → ¬F x)
    (hBnonempty : ∃ x, P x ∧ B x) (hWnonempty : ∃ x, P x ∧ W x) :
    (∀ x, P x → F x) ↔ a ∧ b := by
  classical
  constructor
  · intro hall
    obtain ⟨x,hpx,hbx⟩ := hBnonempty
    obtain ⟨y,hpy,hwy⟩ := hWnonempty
    have ha : a := by
      by_cases h : a
      · exact h
      · exact False.elim (hnotB h x hbx (hall x hpx))
    have hb : b := by
      by_cases h : b
      · exact h
      · exact False.elim (hnotW h y hwy (hall y hpy))
    exact ⟨ha,hb⟩
  · rintro ⟨ha,hb⟩ x hp
    rcases hcover x hp with he | hbb | hw
    · exact hE x he
    · exact hB ha x hbb
    · exact hW hb x hw

theorem zipper_matching_counts (m : Nat) :
    1+5*(m+1)+1+m+(3*m+2)=9*m+9 ∧
    (9*m+9)-(m+2)=8*m+7 := by omega

theorem exact_interface_counts (m : Nat) :
    2+(9*m+7)=9*m+9 ∧
    (9*m+9)+(9*m+9)=18*m+18 ∧
    (9*m+9)+2+(9*m+7)=18*m+18 := by omega

theorem early_black_checks (l : Nat) : 0<1 ∧ 1<2 ∧ 2<3 ∧ 3<4+l := by omega

theorem lower_black_step (l : Nat) (hl : 1≤l) : 4+(l-1)<4+l := by omega

theorem terminal_G_check (m : Nat) : (3*m+2)+2<(3*m+2)+3 := by omega

theorem lower_white_step (m l : Nat) (hl : l+1<3*m+2) :
    (3*m+2)+2-(l+1)<(3*m+2)+2-l := by omega

theorem white_core_steps (m j : Nat) (hj : 1≤j) :
    (3*m+2)+2+6*(j-1)+5<(3*m+2)+2+6*j ∧
    (3*m+2)+1-3*j<(3*m+2)+2+6*j := by omega

theorem white_core_successors (m j : Nat) :
    (3*m+2)+2+6*j<(3*m+2)+3+6*j ∧
    (3*m+2)+3+6*j<(3*m+2)+4+6*j ∧
    (3*m+2)+4+6*j<(3*m+2)+5+6*j ∧
    (3*m+2)+5+6*j<(3*m+2)+6+6*j ∧
    (3*m+2)+6+6*j<(3*m+2)+7+6*j := by omega

theorem changed_cap_seam_checks (m : Nat) :
    (3*m+2)+3<(3*m+2)+4 ∧
    (3*m+2)+2+6*m+4=9*m+8 ∧
    9*m+8<9*m+9 ∧ 9*m+9<9*m+10 ∧ 9*m+10<9*m+11 ∧
    9*m+11<9*m+12 ∧ 9*m+12<9*m+13 := by omega

theorem rank_max_checks (m j l : Nat) (hj : j≤m) (hl : l<3*m+2) :
    (3*m+2)+2+6*j+4≤9*m+13 ∧ 4+l≤9*m+13 ∧
    (3*m+2)+6≤9*m+13 := by omega

theorem no_uniform_defect_per_port (C : Nat) :
    ∃ m : Nat, 2≤m ∧ 8*m+7>C*2 := by
  exact ⟨C+2,by omega,by omega⟩

theorem no_uniform_rematching_radius (R : Nat) :
    ∃ m : Nat, 2≤m ∧ 6*m+4>R := by
  exact ⟨R+2,by omega,by omega⟩

theorem fixed_port_affine_defect_bound_fails (C : Nat) :
    ∃ m : Nat, 2≤m ∧
      (18*m+30)+(8*m+7)>(18*m+30)+C*2 := by
  exact ⟨C+2,by omega,by omega⟩

#print axioms actual_mate_preserves_dependency_colour
#print axioms colour_freezing_invariant
#print axioms exact_two_input_response
#print axioms two_inputs_necessary_sufficient
#print axioms zipper_matching_counts
#print axioms exact_interface_counts
#print axioms early_black_checks
#print axioms lower_black_step
#print axioms terminal_G_check
#print axioms lower_white_step
#print axioms white_core_steps
#print axioms white_core_successors
#print axioms changed_cap_seam_checks
#print axioms rank_max_checks
#print axioms no_uniform_defect_per_port
#print axioms no_uniform_rematching_radius
#print axioms fixed_port_affine_defect_bound_fails
end SubQuorum.TwoPortUnboundedRematching
