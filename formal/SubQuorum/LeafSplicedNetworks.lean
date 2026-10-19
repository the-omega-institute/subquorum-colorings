import Std

set_option autoImplicit false

namespace SubQuorum.LeafSplicedNetworks

def pathValid : List Int → Prop
  | [] => True
  | [charge] => charge ≤ 1
  | first :: second :: rest => first ≤ 1 ∧ first+second ≤ 0 ∧ pathValid (second :: rest)

theorem tail_valid (first : Int) (rest : List Int)
    (hvalid : pathValid (first :: rest)) : pathValid rest := by
  cases rest with
  | nil => trivial
  | cons second remaining => exact hvalid.2.2

theorem path_charge_bound : (charges : List Int) → pathValid charges →
    charges.sum ≤ if charges.length % 2 = 0 then 0 else 1
  | [], _ => by simp
  | [first], hvalid => by simpa [pathValid] using hvalid
  | first :: second :: rest, hvalid => by
      have hrest := tail_valid second rest hvalid.2.2
      have hbound := path_charge_bound rest hrest
      have hpair : first+second ≤ 0 := hvalid.2.1
      simp only [List.sum_cons, List.length_cons]
      split <;> split at hbound <;> omega

theorem even_path_nonpositive (charges : List Int) (hvalid : pathValid charges)
    (heven : charges.length % 2 = 0) : charges.sum ≤ 0 := by
  simpa [heven] using path_charge_bound charges hvalid

theorem odd_path_at_most_one (charges : List Int) (hvalid : pathValid charges) :
    charges.sum ≤ 1 := by
  have hbound := path_charge_bound charges hvalid
  split at hbound <;> omega

theorem adjacent_module_budget (first second : Int)
    (hfirst : first = 1 ∨ first ≤ -1) (hsecond : second = 1 ∨ second ≤ -1)
    (hseparate : ¬ (first = 1 ∧ second = 1)) : first+second ≤ 0 := by
  rcases hfirst with hfirst | hfirst <;>
    rcases hsecond with hsecond | hsecond <;> omega

theorem splice_charge_identity (selected edges tiles overlaps : Int) :
    (selected-2*overlaps)+edges-2*(tiles-overlaps) = selected+edges-2*tiles := by
  omega

theorem receiver_ledger_adapter
    (oldSelected oldEdges oldTiles overlaps selected edges tiles : Int)
    (hselected : selected = oldSelected-2*overlaps)
    (hedges : edges = oldEdges) (htiles : tiles = oldTiles-overlaps) :
    selected+edges-2*tiles = oldSelected+oldEdges-2*oldTiles := by
  omega

theorem positive_path_compensated (charge donor : Int)
    (hbound : charge ≤ 1) (hdonor : donor = 1) : charge ≤ donor := by
  omega

theorem phase_zero_charge (width halfSum : Int) (heven : width = 2*(width/2)) :
    (halfSum+4)+(width+halfSum-1)-2*(width/2+halfSum+1) = 1 := by
  omega

theorem phase_column_charge (width halfSum : Int) (heven : width = 2*(width/2)) :
    halfSum+(width+halfSum-1)-2*(width/2+halfSum) = -1 := by
  omega

theorem phase_row_charge (width halfSum : Int) :
    (halfSum+2)+(width+halfSum-1)-2*(width+halfSum) = 1-width := by
  omega

theorem phase_both_charge (width halfSum : Int) :
    (halfSum-2)+(width+halfSum-1)-2*(width+halfSum-2) = 1-width := by
  omega

theorem nonpositive_phase (width : Int) (hwidth : 6 ≤ width) : 1-width ≤ -1 := by
  omega

theorem half_area_from_distinct_donors
    (halfArea selected matching totalCharge deficit positiveNetworks : Int)
    (hledger : halfArea-selected-matching = deficit-totalCharge)
    (hnetworks : totalCharge ≤ positiveNetworks)
    (hdonors : positiveNetworks ≤ deficit) : selected+matching ≤ halfArea := by
  omega

theorem coefficient_improvement (halfArea selected matching : Int)
    (hbound : selected+matching ≤ halfArea) :
    6*selected+5*matching ≤ 6*halfArea-matching := by
  omega

theorem surviving_distinct_donors
    (positiveNetworks charge reserved lost remaining residualCharge : Int)
    (hcharge : charge ≤ positiveNetworks) (hlost : lost ≤ reserved)
    (hremaining : remaining = positiveNetworks-lost)
    (hresidual : residualCharge = charge-reserved) : residualCharge ≤ remaining := by
  omega

theorem first_five_support_excluded (positiveTiles : Int)
    (hdonors : 5 ≤ positiveTiles) (hshape : positiveTiles ≤ 4) : False := by
  omega

end SubQuorum.LeafSplicedNetworks
