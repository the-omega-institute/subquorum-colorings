import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenInternalShortPair

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def northAt (row column breadth incident far : Int) (left : Bool) (point : Point) : Prop :=
  endpoint breadth incident far
    (point.1-row+incident, if left then column+1-point.2 else point.2-column+1)

def oldP (origin offset width : Int) (point : Point) : Prop :=
  endpoint (width+12) 10 4 (point.1-origin+8,offset+width+13-point.2)

theorem narrow_receiver_hits_P (origin offset width breadth far : Int)
    (hbreadth : 6 ≤ breadth)
    (hnarrow : breadth ≤ width+13) (hfar : 4 ≤ far) :
    northAt (origin-1) (offset+width+13) breadth 10 far true
      (origin-8,offset+width+14-breadth) ∧
    oldP origin offset width (origin-8,offset+width+14-breadth) := by
  unfold northAt oldP endpoint
  dsimp
  omega

theorem receiver_bar_contains_t_column (origin offset width breadth far : Int)
    (hwidth : 12 ≤ width) (hbreadth : width+14 ≤ breadth) :
    northAt (origin-1) (offset+width+13) breadth 10 far true (origin-10,offset) := by
  unfold northAt endpoint
  dsimp
  omega

theorem deep_t_hits_receiver_bar (origin offset breadth incident far : Int)
    (hbreadth : 6 ≤ breadth) (hincident : 6 ≤ incident) (left : Bool) :
    northAt (origin-4) offset breadth incident far left (origin-10,offset) := by
  cases left <;> unfold northAt endpoint <;> dsimp <;> omega

theorem t_incident_locked (incident : Int) (hlower : 4 ≤ incident)
    (heven : incident % 2 = 0) (hnotdeep : ¬6 ≤ incident) : incident = 4 := by omega

theorem right_four_hits_P (origin offset width breadth far : Int)
    (hwidth : 12 ≤ width) (hbreadth : 6 ≤ breadth) :
    northAt (origin-4) offset breadth 4 far false (origin-8,offset+1) ∧
    oldP origin offset width (origin-8,offset+1) := by
  unfold northAt oldP endpoint
  dsimp
  omega

theorem insufficient_width_hits_t_bar (origin offset width receiverBreadth breadth far other : Int)
    (hlower : width+14 ≤ receiverBreadth)
    (hupper : receiverBreadth ≤ width+breadth+13) (hfar : 4 ≤ far) :
    northAt (origin-1) (offset+width+13) receiverBreadth 10 far true
      (origin-8,offset+width+14-receiverBreadth) ∧
    northAt (origin-4) offset breadth 4 other true
      (origin-8,offset+width+14-receiverBreadth) := by
  unfold northAt endpoint
  dsimp
  omega

theorem coupled_width_lower (width receiverBreadth breadth : Int)
    (hfailure : ¬receiverBreadth ≤ width+breadth+13) :
    width+breadth+14 ≤ receiverBreadth := by omega

theorem shortest_width_lower (width receiverBreadth breadth : Int)
    (hbreadth : 6 ≤ breadth) (hcoupled : width+breadth+14 ≤ receiverBreadth) :
    width+20 ≤ receiverBreadth := by omega

theorem tight_general_depth_hits_t_footprint (origin offset width incident far : Int)
    (hincident : 10 ≤ incident)
    (hfar : incident-6 ≤ far) :
    northAt (origin-1) (offset+width+13) (width+14) incident far true
      (origin-8,offset) := by
  unfold northAt endpoint
  dsimp
  omega

theorem tight_general_far_bound (incident far : Int)
    (hincident : incident % 2 = 0) (hfar : far % 2 = 0)
    (havoids : ¬incident-6 ≤ far) : far ≤ incident-8 := by omega

theorem next_B_far_collision (origin offset width nextWidth depth breadth incident far : Int)
    (hbreadth : 6 ≤ breadth)
    (hincident : 12 ≤ incident) :
    northAt (origin+depth-10) (offset-nextWidth-12) (width+nextWidth+26)
      (depth+6) 4 false (origin-12,offset+width+13) ∧
    northAt (origin-1) (offset+width+13) breadth incident far true
      (origin-12,offset+width+13) := by
  unfold northAt endpoint
  dsimp
  omega

theorem next_B_forces_ten (incident : Int)
    (hlower : 10 ≤ incident) (heven : incident % 2 = 0)
    (havoids : ¬12 ≤ incident) : incident = 10 := by omega

theorem next_B_near_collision (origin offset width nextWidth depth breadth far : Int)
    (hwidth : 12 ≤ width) (hnext : 12 ≤ nextWidth) (hdepth : 24 ≤ depth)
    (hbreadth : width+nextWidth+26 ≤ breadth) :
    northAt (origin+depth-10) (offset-nextWidth-12) (width+nextWidth+26)
      (depth+6) 4 false (origin-10,offset-nextWidth-12) ∧
    northAt (origin-1) (offset+width+13) breadth 10 far true
      (origin-10,offset-nextWidth-12) := by
  unfold northAt endpoint
  dsimp
  omega

theorem next_B_receiver_upper (width nextWidth breadth : Int)
    (hwidth : width % 2 = 0) (hnext : nextWidth % 2 = 0)
    (hbreadth : breadth % 2 = 0) (havoids : ¬width+nextWidth+26 ≤ breadth) :
    breadth ≤ width+nextWidth+24 := by omega

theorem next_B_consumer_width (width nextWidth receiverBreadth breadth : Int)
    (hlower : width+breadth+14 ≤ receiverBreadth)
    (hupper : receiverBreadth ≤ width+nextWidth+24) : breadth ≤ nextWidth+10 := by omega

theorem pair_original_mass (breadth : Int) (hbreadth : 6 ≤ breadth) :
    max 0 (-(1-breadth))+max 0 (-(-1 : Int)) = breadth := by omega

def pairGain (breadth tight : Int) : Int := breadth-2*tight

theorem pair_receipt_identity (breadth tight : Int) :
    breadth+2*6-(12+2*tight) = pairGain breadth tight := by
  unfold pairGain
  omega

theorem pair_gain_lower (breadth tight : Int)
    (hbreadth : 6 ≤ breadth) (htight : tight = 0 ∨ tight = 1) :
    4 ≤ pairGain breadth tight := by unfold pairGain; omega

theorem R_endpoint_row_footprint (origin column breadth : Int) (point : Point)
    (hendpoint : northAt (origin-1) column breadth 10 4 true point) :
    origin-11 ≤ point.1 ∧ point.1 ≤ origin-1 := by
  unfold northAt endpoint at hendpoint
  dsimp at hendpoint
  omega

theorem T_endpoint_row_footprint (origin column breadth : Int) (point : Point)
    (hendpoint : northAt (origin-4) column breadth 4 4 true point) :
    origin-8 ≤ point.1 ∧ point.1 ≤ origin-4 := by
  unfold northAt endpoint at hendpoint
  dsimp at hendpoint
  omega

theorem endpoint_tile_row_footprint (origin row : Int)
    (hlower : origin-11 ≤ row) (hupper : row ≤ origin-1) :
    (origin-11)/2 ≤ row/2 ∧ row/2 ≤ (origin-1)/2 := by omega

theorem row_footprints_separated (first second : Int) (hgap : first+18 ≤ second) :
    (first-1)/2+4 ≤ (second-11)/2 := by omega

theorem row_footprints_disjoint (first second tileRow : Int)
    (hgap : first+18 ≤ second)
    (hfirst : tileRow ≤ (first-1)/2) (hsecond : (second-11)/2 ≤ tileRow) : False := by
  have hseparated := row_footprints_separated first second hgap
  omega

theorem tight_new_support (origin farColumn : Int) :
    (origin-6,farColumn) ≠ (origin-7,farColumn) ∧
    (origin-6,farColumn) ≠ (origin-6,farColumn+1) := by
  constructor <;> intro hequal <;> have h := congrArg Prod.fst hequal <;>
    have hcolumn := congrArg Prod.snd hequal <;> dsimp at * <;> omega

def totalGain : List (Int × Int) → Int
  | [] => 0
  | pair :: remaining => pairGain pair.1 pair.2+totalGain remaining

def validPairs : List (Int × Int) → Prop
  | [] => True
  | pair :: remaining => 6 ≤ pair.1 ∧ (pair.2 = 0 ∨ pair.2 = 1) ∧ validPairs remaining

theorem simultaneous_lower (pairs : List (Int × Int)) (hvalid : validPairs pairs) :
    4*(pairs.length : Int) ≤ totalGain pairs := by
  induction pairs with
  | nil => simp [totalGain]
  | cons pair remaining inductionHypothesis =>
    simp only [validPairs] at hvalid
    have hpair := pair_gain_lower pair.1 pair.2 hvalid.1 hvalid.2.1
    have hremaining := inductionHypothesis hvalid.2.2
    simp only [totalGain, List.length_cons]
    omega

end SubQuorum.SecondaryTenInternalShortPair
