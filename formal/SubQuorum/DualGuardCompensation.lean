import SubQuorum.BranchedRotorNetworks

set_option autoImplicit false

namespace SubQuorum.DualGuardCompensation

def tile (point : Int × Int) : Int × Int := (point.1/2, point.2/2)

def leftProtectors : List (Int × Int) := [(2,1),(4,1),(1,3)]

def rightProtectors (width : Int) : List (Int × Int) :=
  [(2,width),(4,width),(1,width-2)]

theorem left_right_protectors_disjoint (width : Int) (hwidth : 6 ≤ width)
    (point : Int × Int) (hleft : point ∈ leftProtectors) : point ∉ rightProtectors width := by
  intro hright
  rcases point with ⟨row, column⟩
  simp [leftProtectors, rightProtectors, Prod.mk.injEq] at hleft hright
  omega

theorem donor_tiles_distinct (width : Int) (hwidth : 6 ≤ width) :
    tile (3,2) ≠ tile (3,width-1) := by
  intro hequal
  have hcolumn := congrArg Prod.snd hequal
  simp [tile] at hcolumn
  omega

theorem left_events_intertile :
    tile (2,1) ≠ tile (2,2) ∧ tile (4,1) ≠ tile (4,2) ∧
      tile (1,3) ≠ tile (2,3) := by decide

theorem right_events_intertile (halfWidth : Int) :
    tile (2,2*halfWidth) ≠ tile (2,2*halfWidth-1) ∧
      tile (4,2*halfWidth) ≠ tile (4,2*halfWidth-1) ∧
      tile (1,2*halfWidth-2) ≠ tile (2,2*halfWidth-2) := by
  constructor
  · intro hequal
    have hcolumn := congrArg Prod.snd hequal
    simp [tile] at hcolumn
    omega
  constructor
  · intro hequal
    have hcolumn := congrArg Prod.snd hequal
    simp [tile] at hcolumn
    omega
  · intro hequal
    have hrow := congrArg Prod.fst hequal
    simp [tile] at hrow

theorem side_witness_injective {Module Endpoint : Type}
    (owner : Endpoint → Module) (side : Endpoint → Bool)
    (witness : Module × Bool → Endpoint)
    (howner : ∀ unit, owner (witness unit) = unit.1)
    (hside : ∀ unit, side (witness unit) = unit.2) :
    ∀ first second, witness first = witness second → first = second := by
  intro first second hequal
  apply Prod.ext
  · rw [← howner first, ← howner second, hequal]
  · rw [← hside first, ← hside second, hequal]

theorem loss_witness_not_internal {Unit Endpoint : Type}
    (witness : Unit → Endpoint) (internal : Endpoint → Prop)
    (houtside : ∀ unit, ¬internal (witness unit)) :
    ∀ unit endpoint, internal endpoint → witness unit ≠ endpoint := by
  intro unit endpoint hinternal hequal
  apply houtside unit
  rw [hequal]
  exact hinternal

theorem two_side_donor_injection {Unit Tile Selection : Type}
    (chosen : Unit → Selection) (donor : Unit → Tile) (sole : Tile → Selection)
    (hchosen : ∀ first second, chosen first = chosen second → first = second)
    (hsole : ∀ unit, chosen unit = sole (donor unit)) :
    ∀ first second, donor first = donor second → first = second :=
  BranchedRotorNetworks.donor_tile_injection chosen donor sole hchosen hsole

theorem marked_sides_bound (positive left right marked : Int)
    (hright : right ≤ positive) (hmarked : marked = left+right) :
    marked ≤ positive+left := by omega

theorem surviving_two_side_units (positive marked survivors : Int)
    (hsurvivors : survivors = 2*positive-marked) :
    survivors-positive = positive-marked := by omega

theorem dual_guard_budget (halfArea selected matching deficit charge positive
    negativeMass squares inside marked : Int)
    (hledger : halfArea-selected-matching = deficit-charge)
    (hcharge : charge = positive-negativeMass-2*squares+inside)
    (hdonors : 2*positive-marked ≤ deficit) :
    positive+negativeMass+2*squares-inside-marked ≤ halfArea-selected-matching := by omega

theorem dual_guard_compensation (halfArea selected matching deficit charge positive
    negativeMass squares inside marked : Int)
    (hledger : halfArea-selected-matching = deficit-charge)
    (hcharge : charge = positive-negativeMass-2*squares+inside)
    (hdonors : 2*positive-marked ≤ deficit)
    (hbudget : inside+marked ≤ positive+negativeMass+2*squares) :
    selected+matching ≤ halfArea := by omega

theorem credit_never_decreases (positive negativeMass squares inside marked left : Int)
    (hmarked : marked ≤ positive+left) :
    negativeMass+2*squares-inside-left ≤
      positive+negativeMass+2*squares-inside-marked := by omega

theorem exact_credit_gain (positive negativeMass squares inside left right : Int) :
    (positive+negativeMass+2*squares-inside-(left+right))-
      (negativeMass+2*squares-inside-left) = positive-right := by omega

theorem nonduplicated_coarse_budget (positive negativeMass squares inside marked degreeFour : Int)
    (hdisjoint : inside+marked ≤ degreeFour) :
    positive+negativeMass+2*squares-degreeFour ≤
      positive+negativeMass+2*squares-inside-marked := by omega

theorem degree_three_strict_budget (positive negativeMass squares : Int) :
    positive+negativeMass+2*squares-0-0 = positive+negativeMass+2*squares := by omega

theorem external_charge_budget (halfArea selected matching deficit charge positive
    negativeMass squares inside marked externalCharge : Int)
    (hledger : halfArea-selected-matching = deficit-charge)
    (hcharge : charge = positive-negativeMass-2*squares+inside+externalCharge)
    (hdonors : 2*positive-marked ≤ deficit)
    (hexternal : externalCharge ≤ positive+negativeMass+2*squares-inside-marked) :
    selected+matching ≤ halfArea := by omega

theorem four_way_credit : (4 : Int)+0+2*1-0-0 = 6 := by decide

theorem star_credit : (4 : Int)+2-0-0 = 6 := by decide

theorem chain_credit (amount : Int) : 4*amount+(3*amount-1) = 7*amount-1 := by omega

end SubQuorum.DualGuardCompensation
