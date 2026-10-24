import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 10000
set_option maxHeartbeats 2000000

namespace SubQuorum.ExchangeTerminalNonunique

abbrev EndpointVertex := Fin 14

def endpointCoordinates : Array (Nat × Nat) :=
  #[(1,1), (1,2), (1,3), (1,4), (2,2), (2,3), (2,4),
    (3,2), (3,3), (3,4), (3,5), (4,1), (4,2), (4,3)]

def gridAdjacent (first second : Nat × Nat) : Prop :=
  (first.1 = second.1 ∧ (first.2+1 = second.2 ∨ second.2+1 = first.2)) ∨
  (first.2 = second.2 ∧ (first.1+1 = second.1 ∨ second.1+1 = first.1))

instance (first second : Nat × Nat) : Decidable (gridAdjacent first second) := by
  unfold gridAdjacent
  infer_instance

def endpointAdjacent (first second : EndpointVertex) : Prop :=
  gridAdjacent endpointCoordinates[first.val]! endpointCoordinates[second.val]!

instance (first second : EndpointVertex) : Decidable (endpointAdjacent first second) := by
  unfold endpointAdjacent
  infer_instance

def horizontalIndices : Array Nat := #[1,0,3,2,7,6,5,4,13,10,9,12,11,8]
def verticalIndices : Array Nat := #[1,0,5,6,7,2,3,4,13,10,9,12,11,8]

def horizontal (vertex : EndpointVertex) : EndpointVertex :=
  Fin.ofNat 14 horizontalIndices[vertex.val]!

def vertical (vertex : EndpointVertex) : EndpointVertex :=
  Fin.ofNat 14 verticalIndices[vertex.val]!

theorem both_matchings_valid :
    (∀ vertex, horizontal (horizontal vertex) = vertex ∧
      endpointAdjacent vertex (horizontal vertex)) ∧
    (∀ vertex, vertical (vertical vertex) = vertex ∧
      endpointAdjacent vertex (vertical vertex)) := by decide

theorem matchings_distinct : horizontal ≠ vertical := by
  intro hequal
  have hvalue := congrFun hequal (2 : EndpointVertex)
  have hfalse : horizontal 2 ≠ vertical 2 := by decide
  exact hfalse hvalue

theorem paired_exclusion (mate : EndpointVertex → EndpointVertex)
    (hinvolution : ∀ vertex, mate (mate vertex) = vertex)
    (vertex partner other : EndpointVertex) (hpaired : mate partner = other)
    (hdifferent : vertex ≠ other) : mate vertex ≠ partner := by
  intro hpair
  have hback := hinvolution vertex
  rw [hpair, hpaired] at hback
  exact hdifferent hback.symm

theorem matching_classification (mate : EndpointVertex → EndpointVertex)
    (hinvolution : ∀ vertex, mate (mate vertex) = vertex)
    (hadjacent : ∀ vertex, endpointAdjacent vertex (mate vertex)) :
    mate = horizontal ∨ mate = vertical := by
  have h01 : mate 0 = 1 :=
    (by decide : ∀ other : EndpointVertex, endpointAdjacent 0 other → other = 1)
      (mate 0) (hadjacent 0)
  have h10 : mate 1 = 0 := by simpa only [h01] using hinvolution 0
  have h109 : mate 10 = 9 :=
    (by decide : ∀ other : EndpointVertex, endpointAdjacent 10 other → other = 9)
      (mate 10) (hadjacent 10)
  have h910 : mate 9 = 10 := by simpa only [h109] using hinvolution 10
  have h1112 : mate 11 = 12 :=
    (by decide : ∀ other : EndpointVertex, endpointAdjacent 11 other → other = 12)
      (mate 11) (hadjacent 11)
  have h1211 : mate 12 = 11 := by simpa only [h1112] using hinvolution 11
  have h138 : mate 13 = 8 := by
    have hposs := (by decide : ∀ other : EndpointVertex,
      endpointAdjacent 13 other → other = 8 ∨ other = 12) (mate 13) (hadjacent 13)
    rcases hposs with hpair | hpair
    · exact hpair
    · exact False.elim (paired_exclusion mate hinvolution 13 12 11 h1211 (by decide) hpair)
  have h813 : mate 8 = 13 := by simpa only [h138] using hinvolution 13
  have h74 : mate 7 = 4 := by
    have hposs := (by decide : ∀ other : EndpointVertex,
      endpointAdjacent 7 other → other = 4 ∨ other = 8 ∨ other = 12)
      (mate 7) (hadjacent 7)
    rcases hposs with hpair | hpair | hpair
    · exact hpair
    · exact False.elim (paired_exclusion mate hinvolution 7 8 13 h813 (by decide) hpair)
    · exact False.elim (paired_exclusion mate hinvolution 7 12 11 h1211 (by decide) hpair)
  have h47 : mate 4 = 7 := by simpa only [h74] using hinvolution 7
  have hposs := (by decide : ∀ other : EndpointVertex,
    endpointAdjacent 2 other → other = 1 ∨ other = 3 ∨ other = 5)
    (mate 2) (hadjacent 2)
  have hcases : ∀ vertex : EndpointVertex,
      vertex = 0 ∨ vertex = 1 ∨ vertex = 2 ∨ vertex = 3 ∨ vertex = 4 ∨
      vertex = 5 ∨ vertex = 6 ∨ vertex = 7 ∨ vertex = 8 ∨ vertex = 9 ∨
      vertex = 10 ∨ vertex = 11 ∨ vertex = 12 ∨ vertex = 13 := by decide
  rcases hposs with hpair | hpair | hpair
  · exact False.elim (paired_exclusion mate hinvolution 2 1 0 h10 (by decide) hpair)
  · have h32 : mate 3 = 2 := by simpa only [hpair] using hinvolution 2
    have h56 : mate 5 = 6 := by
      have hother := (by decide : ∀ other : EndpointVertex,
        endpointAdjacent 5 other → other = 2 ∨ other = 4 ∨ other = 6 ∨ other = 8)
        (mate 5) (hadjacent 5)
      rcases hother with hother | hother | hother | hother
      · exact False.elim (paired_exclusion mate hinvolution 5 2 3 hpair (by decide) hother)
      · exact False.elim (paired_exclusion mate hinvolution 5 4 7 h47 (by decide) hother)
      · exact hother
      · exact False.elim (paired_exclusion mate hinvolution 5 8 13 h813 (by decide) hother)
    have h65 : mate 6 = 5 := by simpa only [h56] using hinvolution 5
    left
    funext vertex
    rcases hcases vertex with rfl | rfl | rfl | rfl | rfl | rfl | rfl |
      rfl | rfl | rfl | rfl | rfl | rfl | rfl
    all_goals simp only [h01, h10, hpair, h32, h47, h56, h65, h74,
      h813, h910, h109, h1112, h1211, h138]; rfl
  · have h52 : mate 5 = 2 := by simpa only [hpair] using hinvolution 2
    have h36 : mate 3 = 6 := by
      have hother := (by decide : ∀ other : EndpointVertex,
        endpointAdjacent 3 other → other = 2 ∨ other = 6) (mate 3) (hadjacent 3)
      rcases hother with hother | hother
      · exact False.elim (paired_exclusion mate hinvolution 3 2 5 hpair (by decide) hother)
      · exact hother
    have h63 : mate 6 = 3 := by simpa only [h36] using hinvolution 3
    right
    funext vertex
    rcases hcases vertex with rfl | rfl | rfl | rfl | rfl | rfl | rfl |
      rfl | rfl | rfl | rfl | rfl | rfl | rfl
    all_goals simp only [h01, h10, hpair, h36, h47, h52, h63, h74,
      h813, h910, h109, h1112, h1211, h138]; rfl

abbrev Vertex := Fin 23

def coordinates : Array (Nat × Nat) :=
  #[(1,1), (1,2), (1,3), (1,4), (2,2), (2,3), (2,4), (3,2), (3,3), (3,4), (3,5), (4,1), (4,2), (4,3), (0,1), (0,3), (1,0), (1,5), (3,6), (4,0), (4,5), (5,1), (5,3)]

def coordinate (vertex : Vertex) : Nat × Nat := coordinates[vertex.val]!

def adjacent (first second : Vertex) : Prop :=
  gridAdjacent (coordinate first) (coordinate second)

instance (first second : Vertex) : Decidable (adjacent first second) := by
  unfold adjacent
  infer_instance

def Endpoint (vertex : Vertex) : Prop := vertex.val < 14
def Selected (vertex : Vertex) : Prop := 14 ≤ vertex.val

instance (vertex : Vertex) : Decidable (Endpoint vertex) := by
  unfold Endpoint
  infer_instance

instance (vertex : Vertex) : Decidable (Selected vertex) := by
  unfold Selected
  infer_instance

def extend (mate : EndpointVertex → EndpointVertex) (vertex : Vertex) : Vertex :=
  if hendpoint : vertex.val < 14 then
    ⟨(mate ⟨vertex.val, hendpoint⟩).val, Nat.lt_trans (mate ⟨vertex.val, hendpoint⟩).isLt (by decide)⟩
  else vertex

def actualMate (choice : Bool) : Vertex → Vertex :=
  extend (if choice then vertical else horizontal)

def ranks0 : Array Nat := #[1,6,2,5,4,4,3,3,4,5,1,1,5,2,0,0,0,0,0,0,0,0,0]
def firstWitness0 : Array Nat := #[14,2,15,17,1,4,3,8,5,6,18,19,7,12,14,15,16,17,18,19,20,21,22]
def secondWitness0 : Array Nat := #[16,4,1,6,5,8,9,12,9,8,20,21,13,22,14,15,16,17,18,19,20,21,22]
def ranks1 : Array Nat := #[1,5,2,5,3,4,3,3,3,6,1,1,4,2,0,0,0,0,0,0,0,0,0]
def firstWitness1 : Array Nat := #[14,2,15,2,1,4,5,8,5,6,18,19,7,12,14,15,16,17,18,19,20,21,22]
def secondWitness1 : Array Nat := #[16,4,1,17,5,8,9,12,9,8,20,21,13,22,14,15,16,17,18,19,20,21,22]

def rank (choice : Bool) (vertex : Vertex) : Nat :=
  (if choice then ranks1 else ranks0)[vertex.val]!

def firstWitness (choice : Bool) (vertex : Vertex) : Vertex :=
  Fin.ofNat 23 (if choice then firstWitness1 else firstWitness0)[vertex.val]!

def secondWitness (choice : Bool) (vertex : Vertex) : Vertex :=
  Fin.ofNat 23 (if choice then secondWitness1 else secondWitness0)[vertex.val]!

def Prior (choice : Bool) (vertex witness : Vertex) : Prop :=
  Selected witness ∨ (Endpoint (actualMate choice witness) ∧
    rank choice (actualMate choice witness) < rank choice vertex)

instance (choice : Bool) (vertex witness : Vertex) : Decidable (Prior choice vertex witness) := by
  unfold Prior
  infer_instance

theorem coordinate_facts :
    (∀ vertex : Vertex, (coordinate vertex).1 < 6 ∧ (coordinate vertex).2 < 8) ∧
    (∀ first second : Vertex, coordinate first = coordinate second → first = second) ∧
    (∀ chosen : Vertex, Selected chosen → ∀ first second : Vertex,
      adjacent chosen first → adjacent chosen second → first = second) ∧
    (∀ vertex : Vertex, Endpoint vertex →
      3 ≤ ((List.finRange 23).filter fun other => decide (adjacent vertex other)).length) := by decide

theorem actual_mate_involution : ∀ choice vertex,
    actualMate choice (actualMate choice vertex) = vertex := by decide

theorem transcript_valid : ∀ choice vertex, Endpoint vertex →
    firstWitness choice vertex ≠ secondWitness choice vertex ∧
    adjacent vertex (firstWitness choice vertex) ∧
    adjacent vertex (secondWitness choice vertex) ∧
    Prior choice vertex (firstWitness choice vertex) ∧
    Prior choice vertex (secondWitness choice vertex) := by decide

theorem both_matchings_exclude_bundles (choice : Bool)
    (promoted retained : Vertex → Prop)
    (hsubset : ∀ vertex, promoted vertex → Endpoint vertex)
    (hselected : ∀ vertex, Selected vertex → retained vertex)
    (hmate : ∀ vertex, Endpoint vertex → ¬promoted vertex →
      retained (actualMate choice vertex))
    (hfeasible : ∀ vertex, promoted vertex → ∀ first second,
      adjacent vertex first → adjacent vertex second →
      retained first → retained second → first = second) :
    ∀ vertex, ¬promoted vertex := by
  have bounded : ∀ bound : Nat, ∀ vertex, Endpoint vertex →
      rank choice vertex < bound → ¬promoted vertex := by
    intro bound
    induction bound with
    | zero =>
      intro vertex hendpoint hrank
      omega
    | succ bound inductionHypothesis =>
      intro vertex hendpoint hrank hpromoted
      obtain ⟨hdifferent, hfirst, hsecond, hfirstPrior, hsecondPrior⟩ :=
        transcript_valid choice vertex hendpoint
      have prior_retained : ∀ witness, Prior choice vertex witness → retained witness := by
        intro witness hprior
        rcases hprior with hselection | ⟨hearlierEndpoint, hearlierRank⟩
        · exact hselected witness hselection
        · have hearlierBound : rank choice (actualMate choice witness) < bound := by omega
          have hunpromoted := inductionHypothesis (actualMate choice witness)
            hearlierEndpoint hearlierBound
          have hkept := hmate (actualMate choice witness) hearlierEndpoint hunpromoted
          simpa only [actual_mate_involution] using hkept
      exact hdifferent (hfeasible vertex hpromoted _ _ hfirst hsecond
        (prior_retained _ hfirstPrior) (prior_retained _ hsecondPrior))
  intro vertex hpromoted
  exact bounded (rank choice vertex+1) vertex (hsubset vertex hpromoted)
    (by omega) hpromoted

theorem all_matchings_exclude_bundles (mate : EndpointVertex → EndpointVertex)
    (hinvolution : ∀ vertex, mate (mate vertex) = vertex)
    (hadjacent : ∀ vertex, endpointAdjacent vertex (mate vertex))
    (promoted retained : Vertex → Prop)
    (hsubset : ∀ vertex, promoted vertex → Endpoint vertex)
    (hselected : ∀ vertex, Selected vertex → retained vertex)
    (hmate : ∀ vertex, Endpoint vertex → ¬promoted vertex → retained (extend mate vertex))
    (hfeasible : ∀ vertex, promoted vertex → ∀ first second,
      adjacent vertex first → adjacent vertex second →
      retained first → retained second → first = second) :
    ∀ vertex, ¬promoted vertex := by
  rcases matching_classification mate hinvolution hadjacent with rfl | rfl
  · exact both_matchings_exclude_bundles false promoted retained hsubset hselected hmate hfeasible
  · exact both_matchings_exclude_bundles true promoted retained hsubset hselected hmate hfeasible

theorem positive_graft_charge (width height : Int) :
    (height+9)+(width+height+6)-(width+2*height+14) = 1 := by omega

#print axioms both_matchings_valid
#print axioms matchings_distinct
#print axioms paired_exclusion
#print axioms matching_classification
#print axioms coordinate_facts
#print axioms actual_mate_involution
#print axioms transcript_valid
#print axioms both_matchings_exclude_bundles
#print axioms all_matchings_exclude_bundles
#print axioms positive_graft_charge

end SubQuorum.ExchangeTerminalNonunique
