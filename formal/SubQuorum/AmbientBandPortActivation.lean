import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 16384
set_option maxHeartbeats 0

/- Generic seeded freezing and phase composition, with the scalar audit for
   the all-length ambient example. The coordinate adapter remains written and
   independently executable; this is not an end-to-end coordinate theorem. -/
namespace SubQuorum.AmbientBandPortActivation
universe u v w

def Supported {V : Type u} (Adj : V → V → Prop) (T P F : V → Prop)
    (mate : V → V) (x : V) : Prop :=
  ∃ a b, a≠b ∧ Adj x a ∧ Adj x b ∧
    (T a ∨ P a ∧ F (mate a)) ∧ (T b ∨ P b ∧ F (mate b))

def Closed {V : Type u} (Adj : V → V → Prop) (T P : V → Prop)
    (mate : V → V) (F : V → Prop) : Prop :=
  ∀ x, P x → Supported Adj T P F mate x → F x

/-- Least freezing closure with an explicit set of supplied frozen endpoints. -/
def FreezeFrom {V : Type u} (Adj : V → V → Prop) (T P : V → Prop)
    (mate : V → V) (seed : V → Prop) (x : V) : Prop :=
  ∀ F : V → Prop, (∀ y, seed y → F y) → Closed Adj T P mate F → F x

/-- A stage can use only supplied endpoints or earlier endpoints in that stage.
    Induction is on the rank of the ACTUAL mate of each witness site. -/
theorem stage_rank_forces_closed {V : Type u}
    (Adj : V → V → Prop) (T P Done S : V → Prop) (mate : V → V)
    (rank : V → Nat) (hSP : ∀ x, S x → P x)
    (hcert : ∀ x, S x → Supported Adj T P
      (fun y => Done y ∨ S y ∧ rank y < rank x) mate x)
    (F : V → Prop) (hDone : ∀ x, Done x → F x)
    (hclosed : Closed Adj T P mate F) : ∀ x, S x → F x := by
  have aux : ∀ n x, rank x=n → S x → F x := by
    intro n
    induction n using Nat.strongRecOn with
    | ind n ih =>
      intro x heq hs
      obtain ⟨a,b,hab,hxa,hxb,ha,hb⟩ := hcert x hs
      apply hclosed x (hSP x hs)
      refine ⟨a,b,hab,hxa,hxb,?_,?_⟩
      · rcases ha with ht | ⟨hp,hd | ⟨hsa,hr⟩⟩
        · exact Or.inl ht
        · exact Or.inr ⟨hp,hDone (mate a) hd⟩
        · exact Or.inr ⟨hp,ih (rank (mate a)) (by omega) (mate a) rfl hsa⟩
      · rcases hb with ht | ⟨hp,hd | ⟨hsb,hr⟩⟩
        · exact Or.inl ht
        · exact Or.inr ⟨hp,hDone (mate b) hd⟩
        · exact Or.inr ⟨hp,ih (rank (mate b)) (by omega) (mate b) rfl hsb⟩
  intro x hs
  exact aux (rank x) x rfl hs

theorem stage_certificate_implies_seeded_freezing {V : Type u}
    (Adj : V → V → Prop) (T P Done S : V → Prop) (mate : V → V)
    (rank : V → Nat) (hSP : ∀ x, S x → P x)
    (hcert : ∀ x, S x → Supported Adj T P
      (fun y => Done y ∨ S y ∧ rank y < rank x) mate x) :
    ∀ x, S x → FreezeFrom Adj T P mate Done x := by
  intro x hs F hd hc
  exact stage_rank_forces_closed Adj T P Done S mate rank hSP hcert F hd hc x hs

/-- Early cap endpoints, then the band, then the remaining cap: a completely
    explicit conditional composition, without assuming either entire region
    frozen at the outset. Matching-closed regions make the local adapters valid;
    the abstract statement only needs the supplied closures and endpoint cover. -/
theorem three_stage_composition {V : Type u}
    (Adj : V → V → Prop) (T P E R C : V → Prop) (mate : V → V)
    (hcover : ∀ x, P x → E x ∨ R x ∨ C x)
    (hearly : ∀ x, E x → FreezeFrom Adj T P mate (fun _ => False) x)
    (hregion : ∀ x, R x → FreezeFrom Adj T P mate E x)
    (hreturn : ∀ x, C x → FreezeFrom Adj T P mate (fun y => E y ∨ R y) x) :
    ∀ x, P x → FreezeFrom Adj T P mate (fun _ => False) x := by
  intro x hp F hfalse hc
  have hE : ∀ y, E y → F y := by
    intro y hy
    exact hearly y hy F hfalse hc
  have hR : ∀ y, R y → F y := by
    intro y hy
    exact hregion y hy F hE hc
  have hC : ∀ y, C y → F y := by
    intro y hy
    apply hreturn y hy F ?_ hc
    intro z hz
    rcases hz with he | hr
    · exact hE z he
    · exact hR z hr
  rcases hcover x hp with he | hr | hh
  · exact hE x he
  · exact hR x hr
  · exact hC x hh

/-- A trap is excluded even with supplied input, provided that input avoids it. -/
theorem seeded_trap_exclusion {V : Type u}
    (Adj : V → V → Prop) (T P seed S : V → Prop) (mate : V → V)
    (hseed : ∀ x, seed x → ¬S x)
    (htrap : ∀ x, P x → S x →
      ¬Supported Adj T P (fun y => ¬S y) mate x) :
    ∀ x, S x → ¬FreezeFrom Adj T P mate seed x := by
  intro x hs hf
  have hc : Closed Adj T P mate (fun y => ¬S y) := by
    intro y hp hsup hsy
    exact htrap y hp hsy hsup
  exact (hf (fun y => ¬S y) hseed hc) hs

theorem phase_rank_strict (K phase₁ phase₂ rank₁ rank₂ : Nat)
    (hr : rank₁≤K)
    (horder : phase₁<phase₂ ∨ phase₁=phase₂ ∧ rank₁<rank₂) :
    phase₁*(K+1)+rank₁ < phase₂*(K+1)+rank₂ := by
  rcases horder with hp | ⟨hp,hrank⟩
  · have hh : (phase₁+1)*(K+1)≤phase₂*(K+1) :=
      Nat.mul_le_mul_right (K+1) hp
    simp only [Nat.add_mul, Nat.one_mul] at hh
    omega
  · subst phase₂
    omega

theorem early_cap_rank_checks :
    0<1 ∧ 0<2 ∧ 1<2 ∧ 1<3 ∧ 2<3 ∧ 2<4 ∧ 3<4 ∧ 1<5 ∧
    4<5 ∧ 1<6 ∧ 5<6 := by omega

theorem return_cap_rank_checks (m : Nat) (_hm : 2≤m) :
    1<3*m+3 ∧ 3*m+2<3*m+3 ∧ 3*m+3<3*m+4 ∧ 0<3*m+4 ∧
    3*m+3<3*m+5 ∧ 3*m+4<3*m+5 ∧
    3*m+5<3*m+6 ∧ 3*m+4<3*m+6 ∧
    3*m+6<3*m+7 ∧ 3*m+4<3*m+7 := by omega

theorem flipped_band_rank_checks (m : Nat) (_hm : 2≤m) :
    1<3*m+2 ∧ 2<3 ∧ 2<4 ∧ 3<4 ∧ 3*m+1<3*m+3 ∧
    3*m+2<3*m+3 ∧ 3*m+1<3*m+3 ∧ 2<4 := by omega

theorem cap_rank_max (m : Nat) : 3*m+7≤9*m+7 := by omega

theorem cap_counts : 11+7=18 ∧ 2*18=6*6 ∧ 14=2*7 := by omega

theorem ambient_counts (m : Nat) :
    (9*m+21)+11=9*m+32 ∧ (9*m+9)+7=9*m+16 ∧
    (9*m+32)+(9*m+16)=18*m+48 ∧
    2*(18*m+48)=6*(6*m+16) := by omega

/-- The cap has an internal debt: its positive token is already spent. -/
theorem zero_charge_is_not_unused_credit (plus minus : Nat)
    (hp : plus=1) (hm : minus=1) : plus=minus ∧ ¬(minus+1≤plus) := by omega

theorem union_token_budget (m : Nat) :
    (m+3)+1=m+4 ∧ ¬(m+4+1≤m+4) := by omega

/-- Encode copy identity in the payment, preserving both injectivity and
    exhaustion for any index set. This formalizes nonreuse across copies. -/
theorem indexed_payment_bijective {I : Type u} {A : Type v} {B : Type w}
    (pay : I → A → B)
    (hinj : ∀ i a b, pay i a=pay i b → a=b)
    (honto : ∀ i b, ∃ a, pay i a=b) :
    (∀ x y : I×A, (x.1,pay x.1 x.2)=(y.1,pay y.1 y.2) → x=y) ∧
    (∀ z : I×B, ∃ x : I×A, (x.1,pay x.1 x.2)=z) := by
  constructor
  · intro x y h
    rcases x with ⟨i,a⟩
    rcases y with ⟨j,b⟩
    have hij : i=j := congrArg Prod.fst h
    cases hij
    have hab : a=b := hinj i a b (congrArg Prod.snd h)
    cases hab
    rfl
  · intro z
    rcases z with ⟨i,b⟩
    obtain ⟨a,ha⟩ := honto i b
    exact ⟨(i,a),by simp only [ha]⟩

theorem stack_objective (q W T M : Nat) (hq : 1≤q)
    (hcopy : T+M=3*W) :
    q*T+(q-1)*W+q*M+W=4*(q*W) := by
  have hmain : q*T+q*M=3*(q*W) := by
    rw [←Nat.mul_add,hcopy]
    simp only [Nat.mul_assoc,Nat.mul_comm]
  have hsep : (q-1)*W+W=q*W := by
    have hh : q-1+1=q := by omega
    calc
      (q-1)*W+W=(q-1+1)*W := by rw [Nat.add_mul,Nat.one_mul]
      _=q*W := by rw [hh]
  omega

theorem stack_half_area (q W J : Nat) (hq : 1≤q)
    (hJ : J+W=4*(q*W)) : 2*J=(8*q-2)*W := by
  have hh : (8*q-2)+2=8*q := by omega
  have hid : (8*q-2)*W+2*W=8*(q*W) := by
    rw [←Nat.add_mul,hh,Nat.mul_assoc]
  omega

theorem no_reserve_per_flipped_region (q f plus minus : Nat)
    (hf : 0<f) (hp : plus=q) (hm : minus=q) :
    ¬(minus+2*f≤plus) := by omega

#print axioms stage_rank_forces_closed
#print axioms stage_certificate_implies_seeded_freezing
#print axioms three_stage_composition
#print axioms seeded_trap_exclusion
#print axioms phase_rank_strict
#print axioms early_cap_rank_checks
#print axioms return_cap_rank_checks
#print axioms flipped_band_rank_checks
#print axioms cap_rank_max
#print axioms cap_counts
#print axioms ambient_counts
#print axioms zero_charge_is_not_unused_credit
#print axioms union_token_budget
#print axioms indexed_payment_bijective
#print axioms stack_objective
#print axioms stack_half_area
#print axioms no_reserve_per_flipped_region
end SubQuorum.AmbientBandPortActivation
