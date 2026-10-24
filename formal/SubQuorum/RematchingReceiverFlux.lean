import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.RematchingReceiverFlux

def adjacent (row column otherRow otherColumn : Int) : Prop :=
  (otherRow = row-1 ∧ otherColumn = column) ∨
  (otherRow = row+1 ∧ otherColumn = column) ∨
  (otherRow = row ∧ otherColumn = column-1) ∨
  (otherRow = row ∧ otherColumn = column+1)

def promoted (row column : Int) : Prop :=
  (row = 5 ∧ column = 5) ∨ (row = 6 ∧ column = 2) ∨
  (row = 6 ∧ column = 4) ∨ (row = 7 ∧ column = 3) ∨
  (row = 7 ∧ column = 5)

def deleted (row column : Int) : Prop :=
  (row = 5 ∧ column = 6) ∨ (row = 7 ∧ column = 2) ∨
  (row = 6 ∧ column = 3) ∨ (row = 7 ∧ column = 4) ∨
  (row = 6 ∧ column = 5)

def prescribedBlank (row column : Int) : Prop :=
  (row = 4 ∧ column = 5) ∨ (row = 6 ∧ column = 1) ∨
  (row = 7 ∧ column = 6)

set_option maxHeartbeats 2000000 in
theorem retained_neighbors_unique
    (row column firstRow firstColumn secondRow secondColumn : Int)
    (hpromoted : promoted row column)
    (hfirst : adjacent row column firstRow firstColumn)
    (hsecond : adjacent row column secondRow secondColumn)
    (hfirstNotDeleted : ¬deleted firstRow firstColumn)
    (hsecondNotDeleted : ¬deleted secondRow secondColumn)
    (hfirstNotBlank : ¬prescribedBlank firstRow firstColumn)
    (hsecondNotBlank : ¬prescribedBlank secondRow secondColumn) :
    firstRow = secondRow ∧ firstColumn = secondColumn := by
  simp only [promoted] at hpromoted
  rcases hpromoted with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
  all_goals
    simp only [adjacent] at hfirst hsecond
    simp only [deleted] at hfirstNotDeleted hsecondNotDeleted
    simp only [prescribedBlank] at hfirstNotBlank hsecondNotBlank
    omega

theorem occupied_retained_neighbors_unique
    (occupied : Int → Int → Prop)
    (hblank : ∀ row column, prescribedBlank row column → ¬occupied row column)
    (row column firstRow firstColumn secondRow secondColumn : Int)
    (hpromoted : promoted row column)
    (hfirst : adjacent row column firstRow firstColumn)
    (hsecond : adjacent row column secondRow secondColumn)
    (hfirstRetained : occupied firstRow firstColumn ∧ ¬deleted firstRow firstColumn)
    (hsecondRetained : occupied secondRow secondColumn ∧ ¬deleted secondRow secondColumn) :
    firstRow = secondRow ∧ firstColumn = secondColumn := by
  exact retained_neighbors_unique row column firstRow firstColumn secondRow secondColumn
    hpromoted hfirst hsecond hfirstRetained.2 hsecondRetained.2
    (fun hcorner => hblank firstRow firstColumn hcorner hfirstRetained.1)
    (fun hcorner => hblank secondRow secondColumn hcorner hsecondRetained.1)

theorem regional_flux
    (oldSelected newSelected oldMatching newMatching oldTiles newTiles
      promotions freedTiles freedSelected oldCharge newCharge : Int)
    (hselected : newSelected+freedSelected = oldSelected+promotions)
    (hmatching : newMatching = oldMatching-promotions)
    (htiles : newTiles+freedTiles = oldTiles)
    (holdCharge : oldCharge = oldSelected+oldMatching-2*oldTiles)
    (hnewCharge : newCharge = newSelected+newMatching-2*newTiles) :
    newCharge = oldCharge+2*freedTiles-freedSelected := by omega

theorem regional_charge_nondecreasing
    (oldCharge newCharge freedTiles freedSelected : Int)
    (hflux : newCharge = oldCharge+2*freedTiles-freedSelected)
    (hcapacity : freedSelected ≤ 2*freedTiles) : oldCharge ≤ newCharge := by omega

theorem global_deficit_conservation
    (oldDeficit newDeficit oldCharge newCharge freedDeficit : Int)
    (hdeficit : newDeficit = oldDeficit+freedDeficit)
    (hcharge : newCharge = oldCharge+freedDeficit) :
    newDeficit-newCharge = oldDeficit-oldCharge := by omega

theorem five_edge_objective (selected matching : Int) :
    selected+5+(matching-5) = selected+matching := by omega

#print axioms adjacent
#print axioms promoted
#print axioms deleted
#print axioms prescribedBlank
#print axioms retained_neighbors_unique
#print axioms occupied_retained_neighbors_unique
#print axioms regional_flux
#print axioms regional_charge_nondecreasing
#print axioms global_deficit_conservation
#print axioms five_edge_objective

end SubQuorum.RematchingReceiverFlux
