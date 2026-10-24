import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenBothFarChargeSeparation

theorem receiver_charge (halfBreadth halfFar : Int) :
    (2*halfBreadth+4+halfFar)+(5+halfFar)-2*(halfBreadth+5+halfFar) = -1 := by
  omega

theorem consumer_charge (breadth halfFar : Int) :
    (breadth+1+halfFar)+(4+halfFar)-2*(breadth+2+halfFar) = 1-breadth := by
  omega

theorem pair_negative_mass (breadth : Int) (hwidth : 6 ≤ breadth) :
    max 0 (-(-1 : Int))+max 0 (-(1-breadth)) = breadth := by omega

theorem earlier_base_column_bound (offset previous width column : Int)
    (hrecurrence : offset = previous-width-12)
    (hcolumn : previous+2 ≤ column) : offset+width+14 ≤ column := by omega

theorem odd_column_boundary (barRight column : Int)
    (hparity : barRight % 2 = 1) (hcolumn : barRight+1 ≤ column) :
    barRight/2 < column/2 := by omega

theorem earlier_small_owner_bound (first second row : Int)
    (hgap : first+18 ≤ second) (hrow : row ≤ first+2) :
    row ≤ second-16 := by omega

theorem earlier_small_owner_tiles (second row : Int)
    (hrow : row ≤ second-16) : row/2 < (second-11)/2 := by omega

theorem concrete_receiver : (71 : Int)+18-2*45 = -1 := by omega

theorem concrete_consumer : (41 : Int)+16-2*42 = -27 := by omega

end SubQuorum.SecondaryTenBothFarChargeSeparation
