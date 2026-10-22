import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 10000
set_option maxHeartbeats 4000000

namespace SubQuorum.ConnectedSharpEntryChains

def site (index : Nat) : Nat × Nat :=
  ([(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(2,2),(2,3),
    (2,4),(2,5),(3,2),(3,3),(3,5),(4,1),(4,2),(4,3),
    (0,1),(0,3),(0,6),(1,0),(1,7),(3,6),(4,0),(4,5),(5,1),(5,3)]
    : List (Nat × Nat)).getD index (0,0)

def adjacent (first second : Nat) : Prop :=
  let firstSite := site first
  let secondSite := site second
  (firstSite.1+1 = secondSite.1 ∧ firstSite.2 = secondSite.2) ∨
  (secondSite.1+1 = firstSite.1 ∧ firstSite.2 = secondSite.2) ∨
  (firstSite.2+1 = secondSite.2 ∧ firstSite.1 = secondSite.1) ∨
  (secondSite.2+1 = firstSite.2 ∧ firstSite.1 = secondSite.1)

instance (first second : Nat) : Decidable (adjacent first second) := by
  unfold adjacent
  infer_instance

def partners (vertical : Bool) : List Nat :=
  if vertical then [1,0,7,8,5,4,10,2,3,12,6,15,9,14,13,11]
  else [1,0,3,2,5,4,10,8,7,12,6,15,9,14,13,11]

def partner (vertical : Bool) (endpoint : Nat) : Nat :=
  (partners vertical).getD endpoint 0

def certificate (vertical : Bool) : List (Nat × Nat × Nat) :=
  if vertical then
    [(0,16,19),(12,21,23),(2,17,1),(6,1,7),(8,7,9),(4,3,9),(11,7,10),(14,10,15),
     (5,18,20),(13,22,24),(15,14,25),(10,11,14),(7,6,11),(1,2,6),(3,2,4),(9,4,8)]
  else
    [(0,16,19),(12,21,23),(2,17,1),(4,3,9),(8,3,9),(6,1,7),(11,7,10),(14,10,15),
     (5,18,20),(13,22,24),(15,14,25),(10,11,14),(7,6,11),(3,4,8),(1,2,6),(9,4,8)]

def rank (vertical : Bool) (endpoint : Nat) : Nat :=
  (certificate vertical).findIdx fun row => row.1 == endpoint

def witnessValid (vertical : Bool) (step witness : Nat) : Prop :=
  witness < 26 ∧
  (witness < 16 → rank vertical (partner vertical witness) < step) ∧
  (witness = 20 ∨ witness = 22 → 8 ≤ step)

instance (vertical : Bool) (step witness : Nat) :
    Decidable (witnessValid vertical step witness) := by
  unfold witnessValid
  infer_instance

def rowValid (vertical : Bool) (step : Nat) : Prop :=
  let row := (certificate vertical).getD step (0,0,0)
  row.1 < 16 ∧ row.2.1 ≠ row.2.2 ∧
  adjacent row.1 row.2.1 ∧ adjacent row.1 row.2.2 ∧
  row.2.1 ≠ partner vertical row.1 ∧ row.2.2 ≠ partner vertical row.1 ∧
  witnessValid vertical step row.2.1 ∧ witnessValid vertical step row.2.2

instance (vertical : Bool) (step : Nat) : Decidable (rowValid vertical step) := by
  unfold rowValid
  infer_instance

theorem all_template_rows : ∀ vertical : Bool, ∀ step : Fin 16,
    rowValid vertical step.val := by decide

theorem template_coverage : ∀ vertical : Bool, ∀ endpoint : Fin 16,
    rank vertical endpoint.val < 16 ∧
    ((certificate vertical).getD (rank vertical endpoint.val) (0,0,0)).1 = endpoint.val := by
  decide

theorem partner_involution : ∀ vertical : Bool, ∀ endpoint : Fin 16,
    partner vertical endpoint.val < 16 ∧
    partner vertical (partner vertical endpoint.val) = endpoint.val ∧
    partner vertical endpoint.val ≠ endpoint.val ∧
    adjacent endpoint.val (partner vertical endpoint.val) := by decide

theorem port_mates_in_prefix : ∀ vertical : Bool,
    rank vertical (partner vertical 5) < 8 ∧
    rank vertical (partner vertical 13) < 8 := by decide

def occupiedDegree (endpoint : Nat) : Nat :=
  ((List.range 26).filter fun other => decide (adjacent endpoint other)).length

theorem core_endpoint_degrees : ∀ endpoint : Fin 16,
    occupiedDegree endpoint.val = if endpoint.val = 2 ∨ endpoint.val = 7 then 4 else 3 := by
  decide

theorem core_support_degrees : ∀ support : Fin 10,
    occupiedDegree (support.val+16) = 1 := by decide

theorem ranked_certificate_excludes_bundle
    {Endpoint Vertex : Type}
    (adjacentTo : Endpoint → Vertex → Prop)
    (selected : Vertex → Prop)
    (mate : Endpoint → Vertex)
    (promotion : Endpoint → Prop)
    (endpointRank : Endpoint → Nat)
    (certificateExists : ∀ endpoint, ∃ first second,
      first ≠ second ∧ adjacentTo endpoint first ∧ adjacentTo endpoint second ∧
      (selected first ∨ ∃ previous, endpointRank previous < endpointRank endpoint ∧ mate previous = first) ∧
      (selected second ∨ ∃ previous, endpointRank previous < endpointRank endpoint ∧ mate previous = second))
    (feasible : ∀ endpoint first second,
      promotion endpoint → first ≠ second → adjacentTo endpoint first → adjacentTo endpoint second →
      (selected first ∨ ∃ previous, mate previous = first ∧ ¬ promotion previous) →
      (selected second ∨ ∃ previous, mate previous = second ∧ ¬ promotion previous) → False) :
    ∀ endpoint, ¬ promotion endpoint := by
  have byRank : ∀ bound, ∀ endpoint, endpointRank endpoint = bound → ¬ promotion endpoint := by
    intro bound
    induction bound using Nat.strongRecOn with
    | ind bound previous =>
      intro endpoint rankEquation promoted
      obtain ⟨first, second, distinct, firstAdjacent, secondAdjacent, firstWitness, secondWitness⟩ :=
        certificateExists endpoint
      have persistent : ∀ witness,
          (selected witness ∨ ∃ earlier, endpointRank earlier < endpointRank endpoint ∧ mate earlier = witness) →
          (selected witness ∨ ∃ earlier, mate earlier = witness ∧ ¬ promotion earlier) := by
        intro witness witnessCertificate
        rcases witnessCertificate with selectedWitness | ⟨earlier, lower, mateEquation⟩
        · exact Or.inl selectedWitness
        · have lowerBound : endpointRank earlier < bound := by omega
          exact Or.inr ⟨earlier, mateEquation, previous (endpointRank earlier) lowerBound earlier rfl⟩
      exact feasible endpoint first second promoted distinct firstAdjacent secondAdjacent
        (persistent first firstWitness) (persistent second secondWitness)
  intro endpoint
  exact byRank (endpointRank endpoint) endpoint rfl

theorem exact_connected_counts (copies selections endpoints matchingEdges : Nat)
    (hselections : selections + 2*(copies-1) = 10*copies)
    (hendpoints : endpoints = 16*copies)
    (hmatching : 2*matchingEdges = endpoints)
    (hpositive : 1 ≤ copies) :
    selections = 8*copies+2 ∧ matchingEdges = 8*copies := by omega

theorem board_margin (copies rowShift : Nat) :
    (rowShift+6)*(3*copies+1) = (16*copies+2) + rowShift*(3*copies+1) + 2*copies+4 := by
  rw [Nat.add_mul]
  omega

#print axioms all_template_rows
#print axioms template_coverage
#print axioms partner_involution
#print axioms port_mates_in_prefix
#print axioms core_endpoint_degrees
#print axioms core_support_degrees
#print axioms ranked_certificate_excludes_bundle
#print axioms exact_connected_counts
#print axioms board_margin

end SubQuorum.ConnectedSharpEntryChains
