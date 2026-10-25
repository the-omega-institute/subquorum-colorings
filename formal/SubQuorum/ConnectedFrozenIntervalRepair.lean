import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 2000000

namespace SubQuorum.ConnectedFrozenIntervalRepair

/-- Reuse an old complete rank after a finite mate change. Any changed mate
must already be frozen in the new system. This is an arbitrary-rank theorem,
not a bounded simulation of the concrete copies. -/
theorem rank_replay {V : Type} (P T F : V → Prop)
    (adj : V → V → Prop) (oldMate newMate : V → V) (rank : V → Nat)
    (oldWitness : ∀ v, P v → ∃ x y, x≠y ∧ adj v x ∧ adj v y ∧
      (T x ∨ (P (oldMate x) ∧ rank (oldMate x)<rank v)) ∧
      (T y ∨ (P (oldMate y) ∧ rank (oldMate y)<rank v)))
    (changedSafe : ∀ w, newMate w=oldMate w ∨ F (newMate w))
    (closed : ∀ v, P v → ∀ x y, x≠y → adj v x → adj v y →
      (T x ∨ F (newMate x)) → (T y ∨ F (newMate y)) → F v) :
    ∀ v, P v → F v := by
  have bounded : ∀ n, ∀ v, P v → rank v<n → F v := by
    intro n
    induction n with
    | zero => intro v hp hlt; omega
    | succ n ih =>
      intro v hp hlt
      obtain ⟨x,y,hxy,hvx,hvy,hx,hy⟩ := oldWitness v hp
      have adapt : ∀ w, (T w ∨ (P (oldMate w) ∧ rank (oldMate w)<rank v)) →
          (T w ∨ F (newMate w)) := by
        intro w hw
        rcases hw with ht | ⟨hpm,hmrank⟩
        · exact Or.inl ht
        · rcases changedSafe w with heq | hf
          · apply Or.inr
            rw [heq]
            exact ih (oldMate w) hpm (by omega)
          · exact Or.inr hf
      exact closed v hp x y hxy hvx hvy (adapt x hx) (adapt y hy)
  intro v hv
  exact bounded (rank v+1) v hv (Nat.lt_succ_self _)

abbrev Point := Nat × Nat

def adjacent (v w : Point) : Prop :=
  (v.1=w.1 ∧ (v.2+1=w.2 ∨ w.2+1=v.2)) ∨
  (v.2=w.2 ∧ (v.1+1=w.1 ∨ w.1+1=v.1))
instance (v w : Point) : Decidable (adjacent v w) :=
  inferInstanceAs (Decidable ((_ ∧ (_ ∨ _)) ∨ (_ ∧ (_ ∨ _))))

def patch : List Point := [(0,0),(1,0),(0,1),(1,1),(0,2),(1,2),(0,3),(1,3)]
def boundary : List Point := [(0,0),(1,0),(0,3),(1,3)]
def interior : List Point := [(0,1),(1,1),(0,2),(1,2)]
def bandMate (v : Point) : Point := (1-v.1,v.2)
def oldMate (v : Point) : Point :=
  if v.2=0 ∨ v.2=3 then bandMate v else if v.2=1 then (v.1,2) else (v.1,1)
def newMate (v : Point) : Point :=
  if v.2=0 then (v.1,1) else if v.2=1 then (v.1,0)
  else if v.2=2 then (v.1,3) else (v.1,2)

/-- Every actual/band edge is internal to the eight PP endpoints before and
after the splice; no terminal strand can enter or exit this closed patch. -/
theorem pure_pp_patch_closed : ∀ v∈patch,
    bandMate v∈patch ∧ oldMate v∈patch ∧ newMate v∈patch ∧
    oldMate (oldMate v)=v ∧ newMate (newMate v)=v ∧
    adjacent v (oldMate v) ∧ adjacent v (newMate v) := by decide

theorem four_new_bridge_sites_freeze (F : Point → Prop)
    (core : ∀ v∈boundary, F v)
    (closed : ∀ v∈interior, ∀ x y, x≠y → adjacent v x → adjacent v y →
      F (newMate x) → F (newMate y) → F v) : ∀ v∈interior, F v := by
  intro v hv
  simp only [interior,List.mem_cons,List.not_mem_nil,or_false] at hv
  rcases hv with rfl | rfl | rfl | rfl
  · apply closed (0,1) (by decide) (0,2) (1,1) (by decide) (by decide) (by decide)
    · simpa [newMate] using core (0,3) (by decide)
    · simpa [newMate] using core (1,0) (by decide)
  · apply closed (1,1) (by decide) (1,2) (0,1) (by decide) (by decide) (by decide)
    · simpa [newMate] using core (1,3) (by decide)
    · simpa [newMate] using core (0,0) (by decide)
  · apply closed (0,2) (by decide) (0,1) (1,2) (by decide) (by decide) (by decide)
    · simpa [newMate] using core (0,0) (by decide)
    · simpa [newMate] using core (1,3) (by decide)
  · apply closed (1,2) (by decide) (1,1) (0,2) (by decide) (by decide) (by decide)
    · simpa [newMate] using core (1,0) (by decide)
    · simpa [newMate] using core (0,3) (by decide)

theorem block_translation_injective (i j c d : Nat)
    (hc : 0<c ∧ c≤22) (hd : 0<d ∧ d≤22)
    (same : 24*i+c=24*j+d) : i=j ∧ c=d := by omega

theorem zero_support_forbids_matching {D R : Type} (support : D → R → Prop)
    (emptyDemand : D) (empty : ∀ r, ¬ support emptyDemand r)
    (assign : D → R) (valid : ∀ d, support d (assign d)) : False := by
  exact empty (assign emptyDemand) (valid emptyDemand)

theorem whole_interval_rank_gap (q r : Nat) (rank : r≤2*q) :
    2*q≤4*q-r := by omega

theorem strict_interval_hall_failure (q r : Nat) (positive : 0<q)
    (rank : r≤2*q) : r<4*q := by omega

theorem beta_only_ledger (a b bFinal : Nat) (ledger : a+bFinal=b) :
    b-bFinal=a := by omega

theorem beta_minimum_link_count (n sourceLinks mixedLinks total : Nat)
    (sources : 4*n≤sourceLinks) (mixed : n≤mixedLinks)
    (disjoint : sourceLinks+mixedLinks≤total) : 5*n≤total := by omega

-- The concrete occupied-side witness data is generated from the permanent
-- fixed fixture. It is followed by a kernel check; no existential search.

def oldEndpoints : List Point := [(1,3),(1,4),(1,5),(1,6),(2,1),(2,2),(2,3),(2,4),(2,5),(2,9),(2,10),(2,11),(2,12),(2,20),(2,21),(2,22),(3,1),(3,2),(3,9),(3,10),(3,11),(3,12),(3,13),(3,14),(3,21),(3,22),(4,1),(4,2),(4,9),(4,10),(4,11),(4,12),(4,13),(4,14),(4,21),(4,22),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),(5,9),(5,10),(5,11),(5,12),(5,13),(5,14),(5,15),(5,16),(5,17),(5,18),(5,19),(5,20),(5,21),(5,22),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(6,9),(6,10),(6,11),(6,12),(6,13),(6,14),(6,15),(6,16),(6,17),(6,18),(6,19),(6,20),(7,3),(7,4),(7,5),(7,6),(7,7),(7,8),(7,9),(7,10),(7,11),(7,12),(7,13),(7,14),(7,15),(7,16),(7,17),(7,18),(7,19),(7,20),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8),(8,9),(8,10),(8,15),(8,16),(8,17),(8,18),(8,19),(8,20),(9,3),(9,4),(9,5),(9,6),(9,7),(9,8),(9,9),(9,10),(9,15),(9,16),(9,17),(9,18),(9,19),(9,20),(10,3),(10,4),(10,5),(10,8),(10,9),(10,14),(10,15),(10,16),(10,17),(10,18),(10,19),(10,20),(11,3),(11,4),(11,5),(11,8),(11,9),(11,14),(11,15),(11,16),(11,17),(11,18),(11,19),(11,20),(12,3),(12,4),(12,5),(12,8),(12,9),(12,10),(12,11),(12,14),(12,17),(12,18),(12,19),(12,20),(13,3),(13,4),(13,5),(13,8),(13,9),(13,10),(13,11),(13,17),(13,18),(13,19),(13,20),(14,3),(14,4),(14,11),(14,17),(14,18),(14,19),(14,20),(15,1),(15,2),(15,3),(15,4),(15,17),(15,18),(15,19),(15,20),(16,1),(16,2),(16,3),(16,4),(16,13),(16,14),(16,15),(16,16),(16,17),(16,18),(16,19),(16,20),(17,1),(17,2),(17,3),(17,4),(17,15),(17,16),(17,17),(17,18),(17,19),(17,20),(18,1),(18,2),(18,3),(18,4),(18,5),(18,6),(18,15),(18,16),(18,17),(18,18),(18,19),(18,20),(19,1),(19,2),(19,3),(19,4),(19,5),(19,6),(19,11),(19,17),(19,18),(19,19),(19,20),(20,1),(20,2),(20,3),(20,4),(20,5),(20,6),(20,7),(20,8),(20,9),(20,10),(20,11),(20,17),(20,18),(20,19),(20,20),(21,3),(21,4),(21,5),(21,6),(21,7),(21,8),(21,9),(21,10),(21,11),(21,18),(21,19),(21,20),(22,3),(22,4),(22,5),(22,6),(22,7),(22,8),(22,9),(22,10),(22,11),(22,12),(22,13),(22,14),(22,15),(22,16),(22,17),(22,18),(22,19),(22,20),(23,3),(23,4),(23,5),(23,6),(23,7),(23,8),(23,9),(23,10),(23,11),(23,12),(23,13),(23,14),(23,15),(23,16),(23,17),(23,18),(23,19),(23,20),(24,2),(24,3),(24,4),(24,5),(24,6),(24,8),(24,9),(24,10),(24,11),(24,17),(24,18),(24,19),(24,20),(24,21)]

def shadowGuards : List (Point × Point × Point) := [
  ((2,17),(5,16),(5,18)),
  ((3,17),(6,16),(6,18)),
  ((3,16),(6,15),(6,17)),
  ((3,15),(6,14),(6,16)),
  ((3,14),(6,13),(6,15)),
  ((3,13),(6,12),(6,14)),
  ((3,12),(6,11),(6,13)),
  ((3,11),(6,10),(6,12)),
  ((3,10),(6,9),(6,11)),
  ((3,9),(6,8),(6,10)),
  ((3,8),(6,7),(6,9)),
  ((3,7),(6,6),(6,8)),
  ((3,6),(6,5),(6,7)),
  ((2,6),(5,5),(5,7)),
  ((12,19),(24,18),(24,20)),
  ((11,19),(22,18),(22,20)),
  ((10,19),(20,18),(20,20)),
  ((9,19),(18,18),(18,20)),
  ((8,19),(16,18),(16,20)),
  ((7,19),(14,18),(14,20)),
  ((6,19),(12,18),(12,20)),
  ((5,19),(10,18),(10,20)),
  ((4,19),(8,18),(8,20)),
  ((3,19),(6,18),(6,20)),
  ((2,19),(5,18),(5,20))]

theorem actual_occupied_side_witnesses : shadowGuards.length=25 ∧
    (shadowGuards.map Prod.fst).Nodup ∧ ∀ e∈shadowGuards,
      e.2.1∈oldEndpoints ∧ e.2.2∈oldEndpoints ∧
      e.2.1.1/2=e.1.1 ∧ e.2.1.2+1=e.1.2 ∧
      e.2.2.1/2=e.1.1 ∧ e.2.2.2=e.1.2+1 := by decide

#print axioms actual_occupied_side_witnesses


#print axioms rank_replay
#print axioms pure_pp_patch_closed
#print axioms four_new_bridge_sites_freeze
#print axioms block_translation_injective
#print axioms zero_support_forbids_matching
#print axioms whole_interval_rank_gap
#print axioms strict_interval_hall_failure
#print axioms beta_only_ledger
#print axioms beta_minimum_link_count
end SubQuorum.ConnectedFrozenIntervalRepair
