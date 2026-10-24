import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 10000
set_option maxHeartbeats 4000000

namespace SubQuorum.MatchingBlockTileLedger

def endpointConnected (northwest northeast southwest southeast : Fin 5) : Prop :=
  (northwest ≠ 0 ∨ northeast ≠ 0 ∨ southwest ≠ 0 ∨ southeast ≠ 0) ∧
  (northwest = 0 ∨ southeast = 0 ∨ northeast ≠ 0 ∨ southwest ≠ 0) ∧
  (northeast = 0 ∨ southwest = 0 ∨ northwest ≠ 0 ∨ southeast ≠ 0)

def fibresConnected (northwest northeast southwest southeast : Fin 5) : Prop :=
  (northwest ≠ 0 ∧ northwest = southeast → northeast = northwest ∨ southwest = northwest) ∧
  (northeast ≠ 0 ∧ northeast = southwest → northwest = northeast ∨ southeast = northeast)

instance (northwest northeast southwest southeast : Fin 5) :
    Decidable (endpointConnected northwest northeast southwest southeast) := by
  unfold endpointConnected
  infer_instance

instance (northwest northeast southwest southeast : Fin 5) :
    Decidable (fibresConnected northwest northeast southwest southeast) := by
  unfold fibresConnected
  infer_instance

def blockCount (northwest northeast southwest southeast : Fin 5) : Nat :=
  (([northwest, northeast, southwest, southeast].filter fun corner => corner != 0).eraseDups).length

def crossEdge (first second : Fin 5) : Nat :=
  if first ≠ 0 ∧ second ≠ 0 ∧ first ≠ second then 1 else 0

def crossEdges (northwest northeast southwest southeast : Fin 5) : Nat :=
  crossEdge northwest northeast + crossEdge northeast southeast +
  crossEdge southeast southwest + crossEdge southwest northwest

def mixedFull (northwest northeast southwest southeast : Fin 5) : Nat :=
  if northwest ≠ 0 ∧ northeast ≠ 0 ∧ southwest ≠ 0 ∧ southeast ≠ 0 ∧
      2 ≤ blockCount northwest northeast southwest southeast then 1 else 0

theorem tile_contraction (northwest northeast southwest southeast : Fin 5)
    (hendpoints : endpointConnected northwest northeast southwest southeast)
    (hblocks : fibresConnected northwest northeast southwest southeast) :
    crossEdges northwest northeast southwest southeast + 1 =
      blockCount northwest northeast southwest southeast + mixedFull northwest northeast southwest southeast := by
  have checked : ∀ northwest northeast southwest southeast : Fin 5,
      endpointConnected northwest northeast southwest southeast →
      fibresConnected northwest northeast southwest southeast →
      crossEdges northwest northeast southwest southeast + 1 =
        blockCount northwest northeast southwest southeast + mixedFull northwest northeast southwest southeast := by decide
  exact checked northwest northeast southwest southeast hendpoints hblocks

def selected (corner : Fin 3) : Nat := if corner = 1 then 1 else 0
def endpoint (corner : Fin 3) : Nat := if corner = 2 then 1 else 0
def occupied (corner : Fin 3) : Nat := if corner ≠ 0 then 1 else 0

def tileFeasible (northwest northeast southwest southeast : Fin 3) : Prop :=
  (northwest = 1 → occupied northeast + occupied southwest ≤ 1) ∧
  (northeast = 1 → occupied northwest + occupied southeast ≤ 1) ∧
  (southwest = 1 → occupied northwest + occupied southeast ≤ 1) ∧
  (southeast = 1 → occupied northeast + occupied southwest ≤ 1)

def fewSelected (northwest northeast southwest southeast : Fin 3) : Prop :=
  (northwest = 2 → selected northeast + selected southwest ≤ 1) ∧
  (northeast = 2 → selected northwest + selected southeast ≤ 1) ∧
  (southwest = 2 → selected northwest + selected southeast ≤ 1) ∧
  (southeast = 2 → selected northeast + selected southwest ≤ 1)

instance (northwest northeast southwest southeast : Fin 3) :
    Decidable (tileFeasible northwest northeast southwest southeast) := by
  unfold tileFeasible
  infer_instance

instance (northwest northeast southwest southeast : Fin 3) :
    Decidable (fewSelected northwest northeast southwest southeast) := by
  unfold fewSelected
  infer_instance

def endpointCount (northwest northeast southwest southeast : Fin 3) : Nat :=
  endpoint northwest + endpoint northeast + endpoint southwest + endpoint southeast

def selectedCount (northwest northeast southwest southeast : Fin 3) : Nat :=
  selected northwest + selected northeast + selected southwest + selected southeast

theorem flexible_tile_budget (northwest northeast southwest southeast : Fin 3)
    (hfeasible : tileFeasible northwest northeast southwest southeast)
    (hfew : fewSelected northwest northeast southwest southeast)
    (hnonempty : 0 < endpointCount northwest northeast southwest southeast) :
    endpointCount northwest northeast southwest southeast +
      2*selectedCount northwest northeast southwest southeast ≤ 4 := by
  have checked : ∀ northwest northeast southwest southeast : Fin 3,
      tileFeasible northwest northeast southwest southeast →
      fewSelected northwest northeast southwest southeast →
      0 < endpointCount northwest northeast southwest southeast →
      endpointCount northwest northeast southwest southeast +
        2*selectedCount northwest northeast southwest southeast ≤ 4 := by decide
  exact checked northwest northeast southwest southeast hfeasible hfew hnonempty

def chosen (site : Bool) : Nat := if site then 1 else 0

theorem forced_same_tile_budget (first second : Bool)
    (hpair : ¬(first = true ∧ second = true)) : chosen first + chosen second ≤ 1 := by
  have checked : ∀ first second : Bool,
      ¬(first = true ∧ second = true) → chosen first + chosen second ≤ 1 := by decide
  exact checked first second hpair

theorem forced_crossing_budget (northwest southwest innerWest innerEast southeast northeast : Bool)
    (hleft : ¬(northwest = true ∧ southwest = true))
    (hmiddle : ¬(innerWest = true ∧ innerEast = true))
    (hright : ¬(southeast = true ∧ northeast = true)) :
    chosen northwest + chosen southwest + chosen innerWest +
      chosen innerEast + chosen southeast + chosen northeast ≤ 3 := by
  have hfirst := forced_same_tile_budget northwest southwest hleft
  have hsecond := forced_same_tile_budget innerWest innerEast hmiddle
  have hthird := forced_same_tile_budget southeast northeast hright
  omega

theorem exact_block_ledger (charge rawCharge interfaceWeight fullMixed overlap : Int)
    (hraw : charge = rawCharge + overlap)
    (hoverlap : overlap = interfaceWeight - 2*fullMixed) :
    charge = rawCharge + interfaceWeight - 2*fullMixed := by omega

theorem exact_global_margin (halfArea objective deficit buffer interfaceWeight fullMixed charge : Int)
    (harea : halfArea-objective = deficit-charge)
    (hcharge : charge = interfaceWeight-2*fullMixed-buffer) :
    halfArea-objective = deficit+buffer+2*fullMixed-interfaceWeight := by omega

theorem sufficient_interface_bound
    (halfArea objective deficit buffer interfaceWeight fullMixed : Int)
    (hledger : halfArea-objective = deficit+buffer+2*fullMixed-interfaceWeight)
    (hinterface : interfaceWeight ≤ deficit+2*fullMixed) :
    objective+buffer ≤ halfArea := by omega

theorem occupied_band_charge (halfWidth : Int) :
    (8*halfWidth+7)-2*(halfWidth+1)-(8*halfWidth+3) = 2-2*halfWidth := by omega

theorem occupied_band_margin (width halfArea objective deficit buffer interfaceWeight fullMixed : Int)
    (hwidth : 2*fullMixed = width+2)
    (hdeficit : deficit = 5*width-10)
    (hbuffer : buffer = 4*width+3)
    (hinterface : interfaceWeight = 4*width+7)
    (hledger : halfArea-objective = deficit+buffer+2*fullMixed-interfaceWeight) :
    halfArea-objective = 6*width-12 := by omega

#print axioms tile_contraction
#print axioms flexible_tile_budget
#print axioms forced_same_tile_budget
#print axioms forced_crossing_budget
#print axioms exact_block_ledger
#print axioms exact_global_margin
#print axioms sufficient_interface_bound
#print axioms occupied_band_charge
#print axioms occupied_band_margin

end SubQuorum.MatchingBlockTileLedger
