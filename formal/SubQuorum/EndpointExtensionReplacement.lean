import Lean.Elab.Tactic.Omega
set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 16000000
namespace SubQuorum.EndpointExtensionReplacement

theorem selected_guard_blank {V : Type} (T O : V → Prop) (adj : V → V → Prop)
    (unique : ∀ t, T t → ∀ x, O x → adj t x → ∀ y, O y → adj t y → x=y)
    (t p q : V) (ht : T t) (hp : O p) (htp : adj t p) (htq : adj t q)
    (different : p≠q) : ¬ O q := by
  intro hq
  exact different (unique t ht p hp htp q hq htq)

/-- Every selected site already has an OLD occupied neighbour. With the
selected set fixed, no newly added endpoint can be adjacent to it. -/
theorem saturation_no_new_tip {V : Type} (T P₀ P₁ : V → Prop)
    (adj : V → V → Prop)
    (retain : ∀ x, P₀ x → P₁ x)
    (disjoint : ∀ x, P₁ x → ¬ T x)
    (saturated : ∀ t, T t → ∃ w, (T w ∨ P₀ w) ∧ adj t w)
    (unique : ∀ t, T t → ∀ x, (T x ∨ P₁ x) → adj t x →
      ∀ y, (T y ∨ P₁ y) → adj t y → x=y)
    (t v : V) (ht : T t) (hv : P₁ v) (htv : adj t v) : P₀ v := by
  obtain ⟨w,hw,htw⟩ := saturated t ht
  have occupied : T w ∨ P₁ w := hw.elim Or.inl (fun h => Or.inr (retain w h))
  have eq := unique t ht w occupied htw v (Or.inr hv) htv
  cases hw with
  | inl tw => exact False.elim (disjoint v hv (eq ▸ tw))
  | inr pw => exact eq ▸ pw

/-- A guarded old BB column either remains blank or supplies a physical BP.
This is a two-state local replacement, not an extra beta resource. -/
theorem local_two_state_replacement {V : Type} (T P : V → Prop)
    (u q : V) [Decidable (P u)] (notSelected : ¬ T u)
    (guard : ¬ (T q ∨ P q)) :
    (P u ∧ ¬ (T q ∨ P q)) ∨
    (¬ (T u ∨ P u) ∧ ¬ (T q ∨ P q)) := by
  by_cases hp : P u
  · exact Or.inl ⟨hp,guard⟩
  · exact Or.inr ⟨fun h => h.elim notSelected hp,guard⟩

def adapt {BP I : Type} (filled : I → Bool) (site : I → BP) :
    Sum BP I → Sum BP I
  | Sum.inl b => Sum.inl b
  | Sum.inr j => if filled j then Sum.inl (site j) else Sum.inr j

def Allowed {BP I : Type} (old : BP → Prop) : Sum BP I → Prop
  | Sum.inl b => old b
  | Sum.inr _ => True

/-- Simultaneous substitutions cannot collide: candidate sites are distinct
and were not among the old physical BP targets. Interval identities are kept. -/
theorem adaptive_target_injection {BP I : Type} (old : BP → Prop)
    (site : I → BP) (filled : I → Bool)
    (fresh : ∀ j, ¬ old (site j))
    (siteInjective : ∀ i j, site i=site j → i=j)
    (x y : Sum BP I) (hx : Allowed old x) (hy : Allowed old y)
    (heq : adapt filled site x=adapt filled site y) : x=y := by
  cases x with
  | inl b =>
    cases y with
    | inl c => exact congrArg Sum.inl (Sum.inl.inj heq)
    | inr j =>
      cases hj : filled j with
      | false => simp [adapt,hj] at heq
      | true =>
        have eq : b=site j := by simpa [adapt,hj] using heq
        exact False.elim (fresh j (eq ▸ hx))
  | inr i =>
    cases y with
    | inl b =>
      cases hi : filled i with
      | false => simp [adapt,hi] at heq
      | true =>
        have eq : site i=b := by simpa [adapt,hi] using heq
        exact False.elim (fresh i (eq.symm ▸ hy))
    | inr j =>
      cases hi : filled i <;> cases hj : filled j <;> simp [adapt,hi,hj] at heq
      · exact congrArg Sum.inr heq
      · exact congrArg Sum.inr (siteInjective i j heq)

/-- Every final alpha has two free TP ends, all assigned distinct intervals. -/
theorem interval_payment_budget (h aFinal : Nat)
    (ends : 2*aFinal≤5-h) : aFinal≤(5-h)/2 := by omega

theorem four_fills_force_beta_only (h aFinal : Nat) (four : 4≤h)
    (ends : 2*aFinal≤5-h) : aFinal=0 := by omega

theorem payment_ledger (a b aFinal bFinal : Nat)
    (balance : a+bFinal=b+aFinal) (monotone : bFinal≤b) :
    b-bFinal+aFinal=a := by omega

abbrev Point := Nat × Nat
def selected : List Point := [(0,3),(0,6),(1,1),(1,7),(1,9),(1,12),(1,20),(1,22),(2,19),(3,5),(3,8),(3,15),(4,4),(4,6),(4,17),(4,19),(6,22),(7,1),(9,11),(10,13),(11,11),(12,13),(13,6),(13,14),(14,1),(14,8),(14,12),(14,16),(15,11),(15,14),(16,12),(17,6),(17,13),(18,7),(18,11),(19,12),(19,15),(20,16),(21,1),(24,1),(24,22),(25,2),(25,4),(25,6),(25,8),(25,11),(25,17),(25,19),(25,21)]
def endpoints : List Point := [(1,3),(1,4),(1,5),(1,6),(2,1),(2,2),(2,3),(2,4),(2,5),(2,9),(2,10),(2,11),(2,12),(2,20),(2,21),(2,22),(3,1),(3,2),(3,9),(3,10),(3,11),(3,12),(3,13),(3,14),(3,21),(3,22),(4,1),(4,2),(4,9),(4,10),(4,11),(4,12),(4,13),(4,14),(4,21),(4,22),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),(5,9),(5,10),(5,11),(5,12),(5,13),(5,14),(5,15),(5,16),(5,17),(5,18),(5,19),(5,20),(5,21),(5,22),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(6,9),(6,10),(6,11),(6,12),(6,13),(6,14),(6,15),(6,16),(6,17),(6,18),(6,19),(6,20),(7,3),(7,4),(7,5),(7,6),(7,7),(7,8),(7,9),(7,10),(7,11),(7,12),(7,13),(7,14),(7,15),(7,16),(7,17),(7,18),(7,19),(7,20),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8),(8,9),(8,10),(8,15),(8,16),(8,17),(8,18),(8,19),(8,20),(9,3),(9,4),(9,5),(9,6),(9,7),(9,8),(9,9),(9,10),(9,15),(9,16),(9,17),(9,18),(9,19),(9,20),(10,3),(10,4),(10,5),(10,8),(10,9),(10,14),(10,15),(10,16),(10,17),(10,18),(10,19),(10,20),(11,3),(11,4),(11,5),(11,8),(11,9),(11,14),(11,15),(11,16),(11,17),(11,18),(11,19),(11,20),(12,3),(12,4),(12,5),(12,8),(12,9),(12,10),(12,11),(12,14),(12,17),(12,18),(12,19),(12,20),(13,3),(13,4),(13,5),(13,8),(13,9),(13,10),(13,11),(13,17),(13,18),(13,19),(13,20),(14,3),(14,4),(14,11),(14,17),(14,18),(14,19),(14,20),(15,1),(15,2),(15,3),(15,4),(15,17),(15,18),(15,19),(15,20),(16,1),(16,2),(16,3),(16,4),(16,13),(16,14),(16,15),(16,16),(16,17),(16,18),(16,19),(16,20),(17,1),(17,2),(17,3),(17,4),(17,15),(17,16),(17,17),(17,18),(17,19),(17,20),(18,1),(18,2),(18,3),(18,4),(18,5),(18,6),(18,15),(18,16),(18,17),(18,18),(18,19),(18,20),(19,1),(19,2),(19,3),(19,4),(19,5),(19,6),(19,11),(19,17),(19,18),(19,19),(19,20),(20,1),(20,2),(20,3),(20,4),(20,5),(20,6),(20,7),(20,8),(20,9),(20,10),(20,11),(20,17),(20,18),(20,19),(20,20),(21,3),(21,4),(21,5),(21,6),(21,7),(21,8),(21,9),(21,10),(21,11),(21,18),(21,19),(21,20),(22,3),(22,4),(22,5),(22,6),(22,7),(22,8),(22,9),(22,10),(22,11),(22,12),(22,13),(22,14),(22,15),(22,16),(22,17),(22,18),(22,19),(22,20),(23,3),(23,4),(23,5),(23,6),(23,7),(23,8),(23,9),(23,10),(23,11),(23,12),(23,13),(23,14),(23,15),(23,16),(23,17),(23,18),(23,19),(23,20),(24,2),(24,3),(24,4),(24,5),(24,6),(24,8),(24,9),(24,10),(24,11),(24,17),(24,18),(24,19),(24,20),(24,21)]
def oldLinks : List (Point × Point) := [((1,3),(1,4)),((1,6),(1,5)),((15,1),(15,2)),((16,13),(16,14)),((18,15),(18,16)),((2,5),(2,4)),((20,1),(20,2)),((24,11),(24,10)),((24,19),(24,18)),((24,21),(24,20)),((24,2),(24,3)),((24,4),(24,5)),((24,8),(24,9)),((5,17),(5,16)),((5,19),(5,18)),((5,4),(5,3)),((5,6),(5,5)),((6,1),(6,2))]
def flexible : List (Point × Point) := [((12,14),(12,15)),((14,11),(14,10)),((19,11),(19,10)),((24,6),(24,7)),((24,17),(24,16))]
def partner (v : Point) : Point := (v.1 ^^^ 1,v.2)
def adjacent (v w : Point) : Prop :=
  (v.1=w.1 ∧ (v.2+1=w.2 ∨ w.2+1=v.2)) ∨
  (v.2=w.2 ∧ (v.1+1=w.1 ∨ w.1+1=v.1))
instance (v w : Point) : Decidable (adjacent v w) :=
  inferInstanceAs (Decidable ((_ ∧ (_ ∨ _)) ∨ (_ ∧ (_ ∨ _))))
def TP (v : Point) : Prop := v∈endpoints ∧ partner v∈selected
instance (v : Point) : Decidable (TP v) := inferInstanceAs (Decidable (_ ∧ _))

theorem actual_all_selected_saturated : selected.length=49 ∧
    ∀ t∈selected, ((selected++endpoints).filter fun w => decide (adjacent t w)).length=1 := by decide

theorem actual_twenty_three_guards :
    ∀ e∈oldLinks++flexible, TP e.1 ∧ adjacent e.1 e.2 ∧
      adjacent (partner e.1) (partner e.2) ∧
      e.1≠partner e.2 ∧ partner e.2∉selected ∧ partner e.2∉endpoints := by decide

theorem actual_static_certificate_targets :
    oldLinks.length=18 ∧ flexible.length=5 ∧
    ((oldLinks++flexible).map Prod.fst).Nodup ∧
    (∀ v∈endpoints, TP v → v∈(oldLinks++flexible).map Prod.fst) ∧
    (oldLinks.map Prod.snd).Nodup ∧ (flexible.map Prod.snd).Nodup ∧
    (∀ u∈oldLinks.map Prod.snd, u∈endpoints) ∧
    (∀ u∈flexible.map Prod.snd, u∉endpoints ∧ u∉selected) := by decide

theorem actual_five_singleton_guards : ∀ e∈flexible,
    e.2.2>0 ∧ e.2.2<23 ∧
    ¬ ((2*(e.2.1/2),e.2.2-1)∈selected ∧ (2*(e.2.1/2)+1,e.2.2-1)∈selected) ∧
    ¬ ((2*(e.2.1/2),e.2.2+1)∈selected ∧ (2*(e.2.1/2)+1,e.2.2+1)∈selected) := by decide

#print axioms selected_guard_blank
#print axioms saturation_no_new_tip
#print axioms local_two_state_replacement
#print axioms adaptive_target_injection
#print axioms interval_payment_budget
#print axioms four_fills_force_beta_only
#print axioms payment_ledger
#print axioms actual_all_selected_saturated
#print axioms actual_twenty_three_guards
#print axioms actual_static_certificate_targets
#print axioms actual_five_singleton_guards
end SubQuorum.EndpointExtensionReplacement

/- New-selection extension. These lemmas check the geometric exclusions and
the exact end-count/payment budget; they do NOT formalize the whole grid flow. -/
namespace SubQuorum.EndpointExtensionReplacement.SelectionBudget

theorem two_retained_neighbors_forbid_selection {V : Type}
    (T O : V → Prop) (adj : V → V → Prop)
    (unique : ∀ t, T t → ∀ x, O x → adj t x → ∀ y, O y → adj t y → x=y)
    (u x y : V) (hx : O x) (hy : O y) (hux : adj u x) (huy : adj u y)
    (different : x≠y) : ¬ T u := by
  intro ht
  exact different (unique u ht x hx hux y hy huy)

theorem retained_neighbor_forbids_selected_pair {V : Type}
    (T O : V → Prop) (adj : V → V → Prop)
    (selectedOccupied : ∀ v, T v → O v)
    (unique : ∀ t, T t → ∀ x, O x → adj t x → ∀ y, O y → adj t y → x=y)
    (s q w : V) (hw : O w) (hsq : adj s q) (hsw : adj s w)
    (different : q≠w) : ¬ (T s ∧ T q) := by
  intro h
  exact different (unique s h.1 q (selectedOccupied q h.2) hsq w hw hsw)

/-- True marks an old free TP that has its own distinct interval assignment.
False marks a genuinely new TP, which this retained certificate leaves open. -/
abbrev Ends := List (Bool × Bool)

def oldEnds : Ends → Nat
  | [] => 0
  | (x,y)::xs => (if x then 1 else 0)+(if y then 1 else 0)+oldEnds xs

def newEnds : Ends → Nat
  | [] => 0
  | (x,y)::xs => (if x then 0 else 1)+(if y then 0 else 1)+newEnds xs

def unpaid : Ends → Nat
  | [] => 0
  | (x,y)::xs => (if x || y then 0 else 1)+unpaid xs

def paid : Ends → Nat
  | [] => 0
  | (x,y)::xs => (if x || y then 1 else 0)+paid xs

theorem exact_end_counts (xs : Ends) :
    paid xs+unpaid xs=xs.length ∧
    2*unpaid xs≤newEnds xs ∧ paid xs≤oldEnds xs ∧
    oldEnds xs+newEnds xs=2*xs.length := by
  induction xs with
  | nil => simp [paid,unpaid,oldEnds,newEnds]
  | cons e xs ih =>
    rcases e with ⟨x,y⟩
    cases x <;> cases y <;>
      simp [paid,unpaid,oldEnds,newEnds] at * <;> omega

theorem new_tip_defect_budget (xs : Ends) (delta : Nat)
    (availableNewEnds : newEnds xs≤delta) : unpaid xs≤delta/2 := by
  have h := (exact_end_counts xs).2.1
  omega

theorem interval_payment_budget (xs : Ends) (r delta : Nat)
    (availableOldEnds : oldEnds xs≤r) (availableNewEnds : newEnds xs≤delta) :
    paid xs≤r ∧ paid xs≤(r+delta)/2 := by
  obtain ⟨hcounts,hunpaid,hpaid,htotal⟩ := exact_end_counts xs
  omega

theorem exact_payment_loss (xs : Ends) (a b bFinal : Nat)
    (ledger : a+bFinal=b+xs.length) (betaMonotone : bFinal≤b) :
    b-bFinal+paid xs+unpaid xs=a := by
  have h := (exact_end_counts xs).1
  omega

theorem at_most_one_new_tip_has_no_loss (xs : Ends) (delta : Nat)
    (availableNewEnds : newEnds xs≤delta) (one : delta≤1) : unpaid xs=0 := by
  have h := new_tip_defect_budget xs delta availableNewEnds
  omega

/-- Retained endpoints already give two distinct occupied neighbours at
each flexible candidate. Thus no extension can select that candidate. -/
theorem actual_candidates_have_two_retained_neighbors : ∀ e∈flexible,
    ∃ x∈endpoints, ∃ y∈endpoints, x≠y ∧ adjacent e.2 x ∧ adjacent e.2 y := by
  intro e he
  simp only [flexible,List.mem_cons,List.not_mem_nil,or_false] at he
  rcases he with rfl | rfl | rfl | rfl | rfl
  · exact ⟨(11,15),by decide,(12,14),by decide,by decide,by decide,by decide⟩
  · exact ⟨(13,10),by decide,(14,11),by decide,by decide,by decide,by decide⟩
  · exact ⟨(19,11),by decide,(20,10),by decide,by decide,by decide,by decide⟩
  · exact ⟨(23,7),by decide,(24,6),by decide,by decide,by decide,by decide⟩
  · exact ⟨(23,16),by decide,(24,17),by decide,by decide,by decide,by decide⟩

def columnBlocked (b c : Nat) : Prop :=
    (2*b,c)∈endpoints ∨ (2*b+1,c)∈endpoints ∨
    (∃ w∈endpoints, adjacent (2*b,c) w ∧ w≠(2*b+1,c)) ∨
    (∃ w∈endpoints, adjacent (2*b+1,c) w ∧ w≠(2*b,c))
instance (b c : Nat) : Decidable (columnBlocked b c) :=
  inferInstanceAs (Decidable (_ ∨ _ ∨ _ ∨ _))

/-- Each adjacent column either contains a retained endpoint, or selecting
both its sites would give one of them two occupied neighbours. Hence every
surviving flexible BB is STILL a singleton even with new selections. -/
theorem actual_adjacent_columns_cannot_become_TT : ∀ e∈flexible,
    columnBlocked (e.2.1/2) (e.2.2-1) ∧ columnBlocked (e.2.1/2) (e.2.2+1) := by
  intro e he
  simp only [flexible,List.mem_cons,List.not_mem_nil,or_false] at he
  rcases he with rfl | rfl | rfl | rfl | rfl
  · change columnBlocked 6 14 ∧ columnBlocked 6 16
    exact ⟨Or.inl (by decide),Or.inr (Or.inr (Or.inl
      ⟨(11,16),by decide,by decide,by decide⟩))⟩
  · change columnBlocked 7 9 ∧ columnBlocked 7 11
    exact ⟨Or.inr (Or.inr (Or.inl
      ⟨(13,9),by decide,by decide,by decide⟩)),Or.inl (by decide)⟩
  · change columnBlocked 9 9 ∧ columnBlocked 9 11
    exact ⟨Or.inr (Or.inr (Or.inr
      ⟨(20,9),by decide,by decide,by decide⟩)),Or.inr (Or.inl (by decide))⟩
  · change columnBlocked 12 6 ∧ columnBlocked 12 8
    exact ⟨Or.inl (by decide),Or.inl (by decide)⟩
  · change columnBlocked 12 15 ∧ columnBlocked 12 17
    exact ⟨Or.inr (Or.inr (Or.inl
      ⟨(23,15),by decide,by decide,by decide⟩)),Or.inl (by decide)⟩

def individuallyAllowed (v : Point) : Prop :=
    ((selected++endpoints).filter fun w => decide (adjacent v w)).length≤1 ∧
    ∀ t∈selected, ¬ adjacent v t
instance (v : Point) : Decidable (individuallyAllowed v) :=
  inferInstanceAs (Decidable (_ ∧ _))

/-- Necessary conditions on a new selection at an old blank band partner.
This is a finite complete audit of the ACTUAL old endpoint set, not a claim
about arbitrary starting geometries or all possible new endpoints. -/
theorem actual_unique_promotable_old_endpoint : ∀ v∈endpoints,
    partner v∉selected → partner v∉endpoints →
    individuallyAllowed (partner v) → v=(3,14) := by decide

#print axioms two_retained_neighbors_forbid_selection
#print axioms retained_neighbor_forbids_selected_pair
#print axioms exact_end_counts
#print axioms new_tip_defect_budget
#print axioms interval_payment_budget
#print axioms exact_payment_loss
#print axioms at_most_one_new_tip_has_no_loss
#print axioms actual_candidates_have_two_retained_neighbors
#print axioms actual_adjacent_columns_cannot_become_TT
#print axioms actual_unique_promotable_old_endpoint
end SubQuorum.EndpointExtensionReplacement.SelectionBudget
