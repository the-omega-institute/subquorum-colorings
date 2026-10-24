import Std

set_option autoImplicit false

namespace SubQuorum.BranchedRotorNetworks

def positiveCount : List Int → Int
  | [] => 0
  | charge :: rest => (if charge > 0 then 1 else 0)+positiveCount rest

theorem charge_bounded_by_positive_modules : (charges : List Int) →
    (∀ charge ∈ charges, charge ≤ 1) → charges.sum ≤ positiveCount charges
  | [], _ => by simp [positiveCount]
  | charge :: rest, hcharges => by
      have hhead : charge ≤ 1 := hcharges charge (by simp)
      have htail : ∀ other ∈ rest, other ≤ 1 := by
        intro other hother
        exact hcharges other (by simp [hother])
      have hinduction := charge_bounded_by_positive_modules rest htail
      simp only [List.sum_cons, positiveCount]
      split <;> omega

theorem exact_splice_cancellation (selected edges tiles intratile : Int) :
    (selected-2*intratile)+edges-2*(tiles-intratile) = selected+edges-2*tiles := by
  omega

theorem branched_compensation
    (halfArea selected matching charge positiveModules donorUnits deficit : Int)
    (hledger : halfArea-selected-matching = deficit-charge)
    (hcharge : charge ≤ positiveModules) (hdistinct : positiveModules ≤ donorUnits)
    (hcapacity : donorUnits ≤ deficit) : selected+matching ≤ halfArea := by
  omega

theorem donor_tile_injection {Module Tile Selection : Type}
    (chosen : Module → Selection) (donor : Module → Tile) (soleSelected : Tile → Selection)
    (hchosen : ∀ first second, chosen first = chosen second → first = second)
    (hsole : ∀ module, chosen module = soleSelected (donor module)) :
    ∀ first second, donor first = donor second → first = second := by
  intro first second hequal
  apply hchosen
  rw [hsole first, hsole second, hequal]

theorem star_charge (width : Int) :
    28+(4*width+16)-2*(2*width+21) = 2 := by
  omega

theorem chain_charge (amount : Int) :
    28*amount+(89*amount-17)-2*(58*amount-9) = amount+1 := by
  omega

theorem chain_module_charge (amount : Int) : 2*amount-(amount-1) = amount+1 := by
  omega

theorem chain_charge_unbounded (bound : Nat) :
    ∃ amount : Nat, 1 ≤ amount ∧ (bound : Int) < (amount : Int)+1 := by
  refine ⟨bound+1, ?_, ?_⟩ <;> omega

theorem chain_compensation (amount : Int) (hpositive : 1 ≤ amount) :
    amount+1 ≤ 4*amount := by
  omega

theorem chain_half_area (amount : Int) (hpositive : 1 ≤ amount) :
    (46*amount-6)+(89*amount-17) ≤ 600*amount-150 := by
  omega

theorem chain_corrected_identity (amount : Int) :
    (600*amount-150)-(46*amount-6)-(89*amount-17) =
      (466*amount-126)-(amount+1) := by
  omega

theorem reserved_donors_remain (positiveModules charge reserved lost remaining : Int)
    (hcharge : charge ≤ positiveModules) (hlost : lost ≤ reserved)
    (hremaining : remaining = positiveModules-lost) : charge-reserved ≤ remaining := by
  omega

theorem first_five_shape_impossible (remaining : Int)
    (hdonors : 5 ≤ remaining) (hshape : remaining ≤ 4) : False := by
  omega

end SubQuorum.BranchedRotorNetworks
