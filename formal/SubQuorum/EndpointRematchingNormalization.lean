import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.EndpointRematchingNormalization

def normalizedMate {Vertex : Type} (inside : Vertex → Prop) [DecidablePred inside]
    (actual auxiliary : Vertex → Vertex) (point : Vertex) : Vertex :=
  if inside point then auxiliary point else actual point

theorem unchanged_outside {Vertex : Type} (inside : Vertex → Prop) [DecidablePred inside]
    (actual auxiliary : Vertex → Vertex) (point : Vertex) (outside : ¬inside point) :
    normalizedMate inside actual auxiliary point = actual point := by
  simp [normalizedMate, outside]

theorem auxiliary_inside {Vertex : Type} (inside : Vertex → Prop) [DecidablePred inside]
    (actual auxiliary : Vertex → Vertex) (point : Vertex) (member : inside point) :
    normalizedMate inside actual auxiliary point = auxiliary point := by
  simp [normalizedMate, member]

theorem normalized_involution {Vertex : Type} (inside : Vertex → Prop) [DecidablePred inside]
    (actual auxiliary : Vertex → Vertex)
    (actualInvolution : ∀ point, actual (actual point) = point)
    (auxiliaryInvolution : ∀ point, inside point → auxiliary (auxiliary point) = point)
    (actualClosed : ∀ point, inside point → inside (actual point))
    (auxiliaryClosed : ∀ point, inside point → inside (auxiliary point)) :
    ∀ point, normalizedMate inside actual auxiliary
      (normalizedMate inside actual auxiliary point) = point := by
  intro point
  by_cases member : inside point
  · have following := auxiliaryClosed point member
    simp only [normalizedMate, if_pos member, if_pos following]
    exact auxiliaryInvolution point member
  · have following : ¬inside (actual point) := by
      intro contrary
      have returned := actualClosed (actual point) contrary
      rw [actualInvolution point] at returned
      exact member returned
    simp only [normalizedMate, if_neg member, if_neg following]
    exact actualInvolution point

theorem normalized_no_fixed_points {Vertex : Type} (inside : Vertex → Prop)
    [DecidablePred inside] (actual auxiliary : Vertex → Vertex)
    (actualDistinct : ∀ point, actual point ≠ point)
    (auxiliaryDistinct : ∀ point, inside point → auxiliary point ≠ point) :
    ∀ point, normalizedMate inside actual auxiliary point ≠ point := by
  intro point
  by_cases member : inside point
  · simpa only [normalizedMate, if_pos member] using auxiliaryDistinct point member
  · simpa only [normalizedMate, if_neg member] using actualDistinct point

theorem normalized_edges_permitted {Vertex : Type} (inside : Vertex → Prop)
    [DecidablePred inside] (actual auxiliary : Vertex → Vertex)
    (permitted : Vertex → Vertex → Prop)
    (actualPermitted : ∀ point, permitted point (actual point))
    (auxiliaryPermitted : ∀ point, inside point → permitted point (auxiliary point)) :
    ∀ point, permitted point (normalizedMate inside actual auxiliary point) := by
  intro point
  by_cases member : inside point
  · simpa only [normalizedMate, if_pos member] using auxiliaryPermitted point member
  · simpa only [normalizedMate, if_neg member] using actualPermitted point

/-- An even old island and a boundary of capacity two have zero or two
    crossing matching edges. The cut-count identity is a separate hypothesis. -/
theorem even_two_port_cut (oldPairs internal crossing : Nat)
    (count : 2*oldPairs=2*internal+crossing) (ports : crossing ≤ 2) :
    crossing=0 ∨ crossing=2 := by omega

/-- With two distinct ports, an even boundary cannot use exactly one. -/
theorem synchronized_ports (left right : Nat) (hl : left ≤ 1) (hr : right ≤ 1)
    (even : left+right=0 ∨ left+right=2) : left=right := by omega

/-- No member of a witness trap can have a finite strict-rank certificate,
    even if only a subset of all endpoints has been certified. -/
theorem no_certified_trap {V : Type} (P T trap certified : V → Prop)
    (mate : V → V) (adj : V → V → Prop) (rank : V → Nat)
    (certificate : ∀ v, certified v → ∃ a b, a ≠ b ∧ adj v a ∧ adj v b ∧
      (T a ∨ (P a ∧ certified (mate a) ∧ rank (mate a) < rank v)) ∧
      (T b ∨ (P b ∧ certified (mate b) ∧ rank (mate b) < rank v)))
    (noSelected : ∀ v a, trap v → adj v a → ¬ T a)
    (externalUnique : ∀ v a b, trap v → adj v a → adj v b →
      P a → P b → ¬trap (mate a) → ¬trap (mate b) → a=b) :
    ∀ v, trap v → ¬certified v := by
  have empty : ∀ n, ∀ v, rank v=n → trap v → ¬certified v := by
    intro n
    induction n using Nat.strongRecOn with
    | ind n ih =>
      intro v hv member present
      obtain ⟨a,b,distinct,ha,hb,wa,wb⟩ := certificate v present
      have pa : P a ∧ certified (mate a) ∧ rank (mate a) < rank v := by
        rcases wa with selected | endpoint
        · exact False.elim (noSelected v a member ha selected)
        · exact endpoint
      have pb : P b ∧ certified (mate b) ∧ rank (mate b) < rank v := by
        rcases wb with selected | endpoint
        · exact False.elim (noSelected v b member hb selected)
        · exact endpoint
      by_cases ta : trap (mate a)
      · exact ih (rank (mate a)) (by omega) (mate a) rfl ta pa.2.1
      · by_cases tb : trap (mate b)
        · exact ih (rank (mate b)) (by omega) (mate b) rfl tb pb.2.1
        · exact distinct (externalUnique v a b member ha hb pa.1 pb.1 ta tb)
  intro v member
  exact empty (rank v) v rfl member

/-- Occupation-only sharp upper bounds transfer across normalization. -/
theorem sharp_bound_transfer (k selected originalEdges normalizedEdges : Nat)
    (sameCard : originalEdges=normalizedEdges)
    (normalizedBound : selected+normalizedEdges+k ≤ 18*k+12) :
    selected+originalEdges+k ≤ 18*k+12 := by omega

abbrev Point := Nat × Nat

def adjacent (a b : Point) : Prop :=
  (a.1=b.1 ∧ (a.2+1=b.2 ∨ b.2+1=a.2)) ∨
  (a.2=b.2 ∧ (a.1+1=b.1 ∨ b.1+1=a.1))
instance (a b : Point) : Decidable (adjacent a b) :=
  inferInstanceAs (Decidable ((_ ∧ (_ ∨ _)) ∨ (_ ∧ (_ ∨ _))))

def corePorts : List Point := [(1,5),(1,6),(1,7),(2,5),(2,6),(2,7),(3,5),(3,6),(3,7),(3,8)]
def trapNodes : List Point := [(1,6),(2,5),(2,7)]
def mate1 (v : Point) : Point :=
  if v=(1,5) then (1,6) else if v=(1,6) then (1,5) else
  if v=(1,7) then (2,7) else if v=(2,7) then (1,7) else
  if v=(2,5) then (2,6) else if v=(2,6) then (2,5) else
  if v=(3,5) then (3,6) else if v=(3,6) then (3,5) else
  if v=(3,7) then (3,8) else if v=(3,8) then (3,7) else
  v
theorem trap_geometry_1 :
    trapNodes.all (fun v => corePorts.all (fun a => corePorts.all (fun b =>
      decide ((adjacent v a ∧ adjacent v b ∧ mate1 a ∉ trapNodes ∧
        mate1 b ∉ trapNodes) → a=b)))) = true := by decide

def mate2 (v : Point) : Point :=
  if v=(1,5) then (2,5) else if v=(2,5) then (1,5) else
  if v=(1,6) then (1,7) else if v=(1,7) then (1,6) else
  if v=(2,6) then (2,7) else if v=(2,7) then (2,6) else
  if v=(3,5) then (3,6) else if v=(3,6) then (3,5) else
  if v=(3,7) then (3,8) else if v=(3,8) then (3,7) else
  v
theorem trap_geometry_2 :
    trapNodes.all (fun v => corePorts.all (fun a => corePorts.all (fun b =>
      decide ((adjacent v a ∧ adjacent v b ∧ mate2 a ∉ trapNodes ∧
        mate2 b ∉ trapNodes) → a=b)))) = true := by decide

def mate3 (v : Point) : Point :=
  if v=(1,5) then (2,5) else if v=(2,5) then (1,5) else
  if v=(1,6) then (2,6) else if v=(2,6) then (1,6) else
  if v=(1,7) then (2,7) else if v=(2,7) then (1,7) else
  if v=(3,5) then (3,6) else if v=(3,6) then (3,5) else
  if v=(3,7) then (3,8) else if v=(3,8) then (3,7) else
  v
theorem trap_geometry_3 :
    trapNodes.all (fun v => corePorts.all (fun a => corePorts.all (fun b =>
      decide ((adjacent v a ∧ adjacent v b ∧ mate3 a ∉ trapNodes ∧
        mate3 b ∉ trapNodes) → a=b)))) = true := by decide

/-- A rebate uses an ORIGINAL exterior tile identity; a new refund uses an
    ORIGINAL top-band BP-site identity. The two resource types are disjoint. -/
def actualPayment (i : Nat) (extra : Bool) : Sum Point Point :=
  if extra then Sum.inr (1,6+6*i) else Sum.inl (1,4+3*i)

theorem actual_payment_injective (i j : Nat) (a b : Bool)
    (same : actualPayment i a=actualPayment j b) : i=j ∧ a=b := by
  cases a <;> cases b <;> simp [actualPayment] at same ⊢ <;> omega

/-- Matching-created BP credits are cancelled against the matching-created
    demands, before recording any unspent physical full-unit reserves. -/
theorem actual_refund_ledger (k extra : Int) :
    (1+extra)-(k+extra)+(k-1)+2*k=2*k := by omega

#print axioms unchanged_outside
#print axioms auxiliary_inside
#print axioms normalized_involution
#print axioms normalized_no_fixed_points
#print axioms normalized_edges_permitted
#print axioms even_two_port_cut
#print axioms synchronized_ports
#print axioms no_certified_trap
#print axioms sharp_bound_transfer
#print axioms trap_geometry_1
#print axioms trap_geometry_2
#print axioms trap_geometry_3
#print axioms actual_payment_injective
#print axioms actual_refund_ledger

end SubQuorum.EndpointRematchingNormalization
