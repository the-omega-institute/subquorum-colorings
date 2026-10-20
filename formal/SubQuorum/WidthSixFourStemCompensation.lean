import Std

set_option autoImplicit false

namespace SubQuorum.WidthSixFourStemCompensation

abbrev Point := Int × Int
abbrev Owner := Bool × Int × Int

def rotorP : List Point :=
  [(1,2),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(4,3)]

def move (owner : Owner) (point : Point) : Point :=
  (point.1+owner.2.1,(if owner.1 then -point.2 else point.2)+owner.2.2)

def firstBlockers : List Point :=
  [(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),
   (2,2),(2,5),(3,2),(3,5),(4,2),(4,5),(5,2),(5,5),(6,2),(6,5)]

def secondBlockers : List Point :=
  firstBlockers ++ [(2,3),(3,3),(4,3),(5,3),(6,3)]

def rotorOwners (target : Point) (blocked : List Point) : List Owner :=
  (([false,true].flatMap fun mirror => rotorP.map fun endpoint =>
    (mirror,target.1-endpoint.1,
      target.2-(if mirror then -endpoint.2 else endpoint.2))).filter fun owner =>
        (rotorP.map (move owner)).all fun point => !blocked.contains point)

theorem first_tip_has_no_rotor_owner : rotorOwners (2,3) firstBlockers = [] := by decide

theorem second_tip_has_no_rotor_owner : rotorOwners (2,4) secondBlockers = [] := by decide

theorem right_bar_avoids_stem (stemHeight barHeight : Int)
    (hbar : 4 ≤ barHeight) (hevenStem : stemHeight%2 = 0)
    (hevenBar : barHeight%2 = 0)
    (hdisjoint : ¬(2 ≤ barHeight+1 ∧ barHeight+1 ≤ stemHeight+2)) :
    stemHeight+2 ≤ barHeight := by omega

theorem left_bar_is_impossible (incident outer : Int)
    (hstem : incident+2 ≤ outer) (hbar : outer+2 ≤ incident) : False := by omega

theorem four_stem_height_gap (outer first second right : Int)
    (hfirst : first+2 ≤ outer) (hsecond : second+2 ≤ first)
    (hright : right+2 ≤ second) : right+6 ≤ outer := by omega

theorem unpaid_full_chain_needs_gap_ten (long short outer first second right : Int)
    (hunpaid : outer+4 ≤ long) (hshort : short ≤ right)
    (hfirst : first+2 ≤ outer) (hsecond : second+2 ≤ first)
    (hright : right+2 ≤ second) : short+10 ≤ long := by omega

theorem gap_eight_full_chain_is_impossible (long short outer first second right : Int)
    (hgap : long ≤ short+8) (hunpaid : outer+4 ≤ long) (hshort : short ≤ right)
    (hfirst : first+2 ≤ outer) (hsecond : second+2 ≤ first)
    (hright : right+2 ≤ second) : False := by omega

theorem unpaid_nontight_clearance (long incident : Int)
    (hevenLong : long%2 = 0) (hevenIncident : incident%2 = 0)
    (hclearance : incident+2 ≤ long) (hnontight : incident+2 ≠ long) :
    incident+4 ≤ long := by omega

theorem close_tips_cannot_share_owner (width separation : Nat)
    (hwidth : 6 ≤ width) (hclose : separation ≤ 3)
    (hown : separation = width-1) : False := by omega

theorem unpaid_routes_cover_singles (single paid chain : Nat)
    (hpaid : paid ≤ single) (hroutes : single-paid ≤ chain) :
    single ≤ paid+chain := by omega

theorem joint_from_four_stem_payments (zeroCount single twice paid chain exterior
    activation unfilled rotor boundary reserve : Nat)
    (hactivation : single+2*twice ≤ activation)
    (hpool : 2*zeroCount+paid+chain+exterior ≤ unfilled+boundary)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary)
    (hcover : single ≤ paid+chain) : zeroCount+single+twice ≤ reserve := by omega

theorem nonnegative_margin (zeroCount single twice unmarked reserve : Nat) (margin : Int)
    (hreserve : zeroCount+single+twice ≤ reserve)
    (hledger : (unmarked : Int)+reserve-(zeroCount+single+twice) ≤ margin) :
    (unmarked : Int) ≤ margin := by omega

theorem adjacent_far_leg_tradeoff (firstHeight secondHeight firstWidth secondWidth farHeight : Int)
    (hseparation : secondHeight+2 ≤ firstHeight)
    (hevenFirstHeight : firstHeight%2 = 0) (hevenSecondHeight : secondHeight%2 = 0)
    (hevenFirstWidth : firstWidth%2 = 0) (hevenSecondWidth : secondWidth%2 = 0)
    (hevenFar : farHeight%2 = 0)
    (hdisjoint : ¬(firstHeight+2-farHeight ≤ secondHeight+2 ∧
      secondHeight+2 ≤ firstHeight+2 ∧ firstWidth+1 ≤ secondWidth+2)) :
    secondWidth+2 ≤ firstWidth ∨ secondHeight+farHeight+2 ≤ firstHeight := by omega

theorem weighted_height_gap (outer first second right extraFirst extraSecond extraThird : Int)
    (hfirst : first+2+extraFirst ≤ outer) (hsecond : second+2+extraSecond ≤ first)
    (hright : right+2+extraThird ≤ second) :
    right+6+extraFirst+extraSecond+extraThird ≤ outer := by omega

theorem widths_descend_at_gap_twelve (long short outer first second right
    widthFirst widthSecond widthThird widthFourth : Int)
    (hgap : long ≤ short+12) (hunpaid : outer+4 ≤ long) (hshort : short ≤ right)
    (hfirst : first+2 ≤ outer) (hsecond : second+2 ≤ first) (hright : right+2 ≤ second)
    (htradeFirst : widthSecond+2 ≤ widthFirst ∨ first+6 ≤ outer)
    (htradeSecond : widthThird+2 ≤ widthSecond ∨ second+6 ≤ first)
    (htradeThird : widthFourth+2 ≤ widthThird ∨ right+6 ≤ second) :
    widthSecond+2 ≤ widthFirst ∧ widthThird+2 ≤ widthSecond ∧ widthFourth+2 ≤ widthThird := by omega

theorem descending_width_minima (first second third fourth : Int)
    (hminimum : 6 ≤ fourth) (hfirst : second+2 ≤ first)
    (hsecond : third+2 ≤ second) (hthird : fourth+2 ≤ third) :
    12 ≤ first ∧ 10 ≤ second ∧ 8 ≤ third := by omega

theorem gap_ten_fixes_heights (long short outer first second right : Int)
    (hgap : long = short+10) (hunpaid : outer+4 ≤ long) (hshort : short ≤ right)
    (hfirst : first+2 ≤ outer) (hsecond : second+2 ≤ first) (hright : right+2 ≤ second) :
    outer = short+6 ∧ first = short+4 ∧ second = short+2 ∧ right = short := by omega

theorem small_left_width_needs_gap_fourteen (long short outer first second right
    widthFirst widthSecond widthThird widthFourth : Int)
    (hunpaid : outer+4 ≤ long) (hshort : short ≤ right)
    (hfirst : first+2 ≤ outer) (hsecond : second+2 ≤ first) (hright : right+2 ≤ second)
    (hwidth : widthFirst ≤ 10) (hminimum : 6 ≤ widthFourth)
    (htradeFirst : widthSecond+2 ≤ widthFirst ∨ first+6 ≤ outer)
    (htradeSecond : widthThird+2 ≤ widthSecond ∨ second+6 ≤ first)
    (htradeThird : widthFourth+2 ≤ widthThird ∨ right+6 ≤ second) :
    short+14 ≤ long := by omega

end SubQuorum.WidthSixFourStemCompensation
