import SubQuorum.BranchedRotorNetworks

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 16000000

namespace SubQuorum.DegreeThreeFusion

def neighborPresent (mask : Fin 16) (neighbor : Fin 4) : Bool :=
  mask.val.testBit neighbor.val

def occupiedCount (mask : Fin 16) : Nat :=
  ((List.finRange 4).filter fun neighbor => neighborPresent mask neighbor).length

def includesNeighbors (old final : Fin 16) : Prop :=
  ∀ neighbor : Fin 4, neighborPresent old neighbor = true → neighborPresent final neighbor = true

instance (old final : Fin 16) : Decidable (includesNeighbors old final) := by
  unfold includesNeighbors
  infer_instance

theorem degree_three_preserves_neighbors : ∀ old final : Fin 16,
    includesNeighbors old final → occupiedCount old = 3 → occupiedCount final = 3 →
      ∀ neighbor : Fin 4, neighborPresent old neighbor = neighborPresent final neighbor := by
  decide

theorem two_blank_neighbors_exclude_endpoint : ∀ final : Fin 16,
    neighborPresent final 0 = false → neighborPresent final 1 = false →
      occupiedCount final = 3 → False := by
  decide

def tileLabel (pattern : Fin 625) (corner : Fin 4) : Nat :=
  pattern.val / 5^corner.val % 5

def connectedCorners (member : Fin 4 → Bool) : Bool :=
  !((member 0 && member 3 && !member 1 && !member 2) ||
    (member 1 && member 2 && !member 0 && !member 3))

def endpointCount (pattern : Fin 625) : Nat :=
  ((List.finRange 4).filter fun corner => decide (0 < tileLabel pattern corner)).length

def labelCount (pattern : Fin 625) (label : Nat) : Nat :=
  ((List.finRange 4).filter fun corner => decide (tileLabel pattern corner = label)).length

def representedModules (pattern : Fin 625) : Nat :=
  ((List.range 4).filter fun label => decide (0 < labelCount pattern (label+1))).length

def foreignEdges (pattern : Fin 625) : Nat :=
  ([(0,1),(0,2),(1,3),(2,3)] : List (Fin 4 × Fin 4)).countP fun edge =>
    decide (0 < tileLabel pattern edge.1 ∧ 0 < tileLabel pattern edge.2 ∧
      tileLabel pattern edge.1 ≠ tileLabel pattern edge.2)

def newMixedSquare (pattern : Fin 625) : Nat :=
  if endpointCount pattern = 4 ∧ 1 < representedModules pattern then 1 else 0

def admissible (pattern : Fin 625) : Prop :=
  0 < endpointCount pattern ∧
    connectedCorners (fun corner => decide (0 < tileLabel pattern corner)) = true ∧
    (∀ label : Fin 4, connectedCorners
      (fun corner => decide (tileLabel pattern corner = label.val+1)) = true)

def degreeThreeAdmissible (pattern : Fin 625) : Prop :=
  admissible pattern ∧
    (endpointCount pattern = 4 →
      ∀ label : Fin 4, labelCount pattern (label.val+1) = 0 ∨
        labelCount pattern (label.val+1) = 1 ∨ labelCount pattern (label.val+1) = 4)

instance (pattern : Fin 625) : Decidable (admissible pattern) := by
  unfold admissible
  infer_instance

instance (pattern : Fin 625) : Decidable (degreeThreeAdmissible pattern) := by
  unfold degreeThreeAdmissible
  infer_instance

theorem local_tile_correction : ∀ pattern : Fin 625, admissible pattern →
    foreignEdges pattern+1 = representedModules pattern+newMixedSquare pattern := by
  decide

theorem mixed_square_has_four_modules : ∀ pattern : Fin 625,
    degreeThreeAdmissible pattern → endpointCount pattern = 4 →
      representedModules pattern = 1 ∨ representedModules pattern = 4 := by
  decide

theorem fusion_charge_identity (oldSelected matching oldTiles internalContacts squares : Int) :
    (oldSelected-2*internalContacts)+matching-2*(oldTiles-internalContacts+squares) =
      oldSelected+matching-2*oldTiles-2*squares := by
  omega

theorem receiver_ledger_adapter
    (oldSelected matching oldTiles contacts squares selected tiles : Int)
    (hselected : selected = oldSelected-2*contacts)
    (htiles : tiles = oldTiles-contacts+squares) :
    selected+matching-2*tiles = oldSelected+matching-2*oldTiles-2*squares := by
  omega

theorem degree_four_fusion_identity
    (oldSelected matching oldTiles internalContacts squares insideDefect : Int) :
    (oldSelected-2*internalContacts+insideDefect)+matching-
      2*(oldTiles-internalContacts+squares) =
        oldSelected+matching-2*oldTiles-2*squares+insideDefect := by
  omega

theorem degree_four_loss_not_doubled (inside outside marked total : Int)
    (hpartition : total = inside+outside) (hmarked : marked ≤ outside) :
    inside+marked ≤ total := by
  omega

theorem controlled_degree_four_fusion
    (halfArea selected matching deficit isolatedCharge positiveModules
      negativeMass squares insideDefect marked degreeFour : Int)
    (hledger : halfArea-selected-matching = deficit-isolatedCharge+2*squares-insideDefect)
    (hnegative : negativeMass = positiveModules-isolatedCharge)
    (hdonors : positiveModules-marked ≤ deficit)
    (hnonreuse : insideDefect+marked ≤ degreeFour) :
    negativeMass+2*squares-degreeFour ≤ halfArea-selected-matching := by
  omega

theorem degree_four_compensation_criterion
    (slack negativeMass squares degreeFour : Int)
    (hbound : negativeMass+2*squares-degreeFour ≤ slack)
    (hpaid : degreeFour ≤ negativeMass+2*squares) : 0 ≤ slack := by
  omega

theorem strict_fusion_compensation
    (halfArea selected matching deficit isolatedCharge positiveModules squares : Int)
    (hledger : halfArea-selected-matching = deficit-isolatedCharge+2*squares)
    (hcharge : isolatedCharge ≤ positiveModules) (hdonors : positiveModules ≤ deficit) :
    selected+matching+2*squares ≤ halfArea := by
  omega

theorem protected_budget_fusion
    (halfArea selected matching deficit isolatedCharge donors squares : Int)
    (hledger : halfArea-selected-matching = deficit-isolatedCharge+2*squares)
    (hcharge : isolatedCharge ≤ donors+2*squares) (hdonors : donors ≤ deficit) :
    selected+matching ≤ halfArea := by
  omega

theorem arbitrary_module_list_budget (charges : List Int)
    (hcharges : ∀ charge ∈ charges, charge ≤ 1) :
    charges.sum ≤ BranchedRotorNetworks.positiveCount charges :=
  BranchedRotorNetworks.charge_bounded_by_positive_modules charges hcharges

theorem one_boundary_vertex_forbids_foreign_matching
    (modulePairs internalEdges foreignEdgesUsed : Nat)
    (hboundary : foreignEdgesUsed ≤ 1)
    (hcover : 2*internalEdges+foreignEdgesUsed = 2*modulePairs) : foreignEdgesUsed = 0 := by
  omega

theorem four_way_original_charge (width : Int) :
    24+(4*width+12)-2*(2*width+17) = 2 := by
  omega

theorem four_way_correction_is_necessary : (4 : Int)-2 = 2 ∧ (2 : Int) ≠ 4 := by
  decide

theorem occupied_band_ledger (width : Int) :
    (2-width)-2*2+4 = 2-width := by
  omega

theorem occupied_band_strict_slack (width : Int) (hwidth : 6 ≤ width) :
    width-1 ≤ (8*width+8)-(2*width+20) := by
  omega

end SubQuorum.DegreeThreeFusion
