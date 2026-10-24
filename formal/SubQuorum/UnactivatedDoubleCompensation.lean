import Std

set_option autoImplicit false

namespace SubQuorum.UnactivatedDoubleCompensation

abbrev Point := Int × Int

theorem blank_gate_no_triple {Owner : Type} (first second elbow : Owner)
    (firstPresent secondPresent : Prop)
    (hfirst : firstPresent → first = elbow ∧ (secondPresent → second ≠ first))
    (hsecond : secondPresent → second = elbow) : ¬(firstPresent ∧ secondPresent) := by
  intro hboth
  have hfirstRole := hfirst hboth.1
  have hsecondRole := hsecond hboth.2
  exact (hfirstRole.2 hboth.2) (hsecondRole.trans hfirstRole.1.symm)

theorem blank_gate_regular_pair_excluded (firstPresent secondPresent : Prop)
    (hnoboth : ¬(firstPresent ∧ secondPresent))
    (hfirst : firstPresent) (hretainedSupport : firstPresent → secondPresent) : False := by
  exact hnoboth ⟨hfirst, hretainedSupport hfirst⟩

theorem short_corner_forbidden (height incoming : Int)
    (hheight : height = 4 ∨ height = 6) (hincoming : 4 ≤ incoming) :
    (2 ≤ height+1 ∧ height+1 ≤ incoming+2) ∨ height+1 = incoming+3 := by omega

theorem short_vertical_bar_forbidden (height width : Int)
    (hheight : height = 4 ∨ height = 6) (hwidth : 6 ≤ width) :
    2 ≤ height+1 ∧ height+1 ≤ width+1 := by omega

theorem longitudinal_height_four (height incoming : Int)
    (hheight : height = 4 ∨ height = 6) (hincoming : 4 ≤ incoming)
    (hclearance : incoming ≤ height-2) : height = 6 ∧ incoming = 4 := by omega

def leftLongitudinalBar (width : Int) (point : Point) : Prop :=
  (point.1 = 5 ∨ point.1 = 6) ∧ 2 ≤ point.2 ∧ point.2 ≤ width+1

def rightTransverseBar (positiveWidth incident width : Int) (point : Point) : Prop :=
  2 ≤ point.1 ∧ point.1 ≤ width+1 ∧
    (point.2 = positiveWidth-incident-1 ∨ point.2 = positiveWidth-incident)

def rightLongitudinalBar (positiveWidth width : Int) (point : Point) : Prop :=
  (point.1 = 5 ∨ point.1 = 6) ∧ positiveWidth-width ≤ point.2 ∧
    point.2 ≤ positiveWidth-1

theorem longitudinal_transverse_overlap (positiveWidth incident leftWidth rightWidth : Int)
    (hpositive : positiveWidth = 8 ∨ positiveWidth = 10)
    (hincident : 4 ≤ incident) (hclearance : incident ≤ positiveWidth-4)
    (hleft : 6 ≤ leftWidth) (hright : 6 ≤ rightWidth) :
    leftLongitudinalBar leftWidth (5, positiveWidth-incident) ∧
      rightTransverseBar positiveWidth incident rightWidth (5, positiveWidth-incident) := by
  dsimp [leftLongitudinalBar, rightTransverseBar]
  omega

theorem two_longitudinal_overlap (positiveWidth leftWidth rightWidth : Int)
    (hpositive : positiveWidth = 8 ∨ positiveWidth = 10)
    (hleft : 6 ≤ leftWidth) (hright : 6 ≤ rightWidth) :
    leftLongitudinalBar leftWidth (5,5) ∧
      rightLongitudinalBar positiveWidth rightWidth (5,5) := by
  dsimp [leftLongitudinalBar, rightLongitudinalBar]
  omega

theorem forced_tiles_distinct (width : Int) (hwidth : 8 ≤ width) :
    (1 : Int) ≠ (width-2)/2 := by omega

theorem physical_slot_count {Slot : Type} (slots pool : List Slot)
    (blank occupied : Nat) (hnodup : slots.Nodup) (hsubset : slots ⊆ pool)
    (hlength : slots.length = 2*blank+2*occupied) :
    2*blank+2*occupied ≤ pool.length := by
  have hcount := hnodup.length_le_of_subset hsubset
  omega

theorem zero_activation_double_paid (zeroCount blank occupied boundary : Nat)
    (hclassification : zeroCount ≤ blank+occupied)
    (hslots : 2*blank+2*occupied ≤ boundary) : 2*zeroCount ≤ boundary := by omega

theorem full_defect_bound (zeroCount single twice activation unused rotor boundary reserve : Nat)
    (hactivation : single+2*twice ≤ activation)
    (hboundary : 2*zeroCount ≤ boundary)
    (hidentity : 2*reserve = activation+unused+rotor+boundary) :
    2*(zeroCount+single+twice) ≤ 2*reserve+single := by omega

theorem reserve_after_single_activations (zeroCount single twice activation unused rotor boundary
    reserve : Nat)
    (hactivation : single+2*twice ≤ activation)
    (hboundary : 2*zeroCount ≤ boundary)
    (hidentity : 2*reserve = activation+unused+rotor+boundary) :
    zeroCount+single+twice ≤ reserve+single/2 := by
  have hdefect := full_defect_bound zeroCount single twice activation unused rotor boundary reserve
    hactivation hboundary hidentity
  omega

theorem joint_when_single_activation_budget (zeroCount single twice exceptional unmarked activation
    unused rotor boundary reserve : Nat)
    (hactivation : single+2*twice ≤ activation)
    (hboundary : 2*zeroCount ≤ boundary)
    (hidentity : 2*reserve = activation+unused+rotor+boundary)
    (hbudget : exceptional+single/2 ≤ unmarked) :
    zeroCount+single+twice+exceptional ≤ unmarked+reserve := by
  have hreserve := reserve_after_single_activations zeroCount single twice activation unused rotor
    boundary reserve hactivation hboundary hidentity
  omega

theorem one_single_activation_pays (zeroCount single twice activation unused rotor boundary reserve : Nat)
    (hactivation : single+2*twice ≤ activation)
    (hboundary : 2*zeroCount ≤ boundary)
    (hidentity : 2*reserve = activation+unused+rotor+boundary)
    (hsingle : single ≤ 1) : zeroCount+single+twice ≤ reserve := by
  have hreserve := reserve_after_single_activations zeroCount single twice activation unused rotor
    boundary reserve hactivation hboundary hidentity
  omega

theorem first_reserve_failure_only_two_activations (zeroCount single twice unmarked activation unused
    rotor boundary reserve : Nat)
    (hactivation : single+2*twice ≤ activation)
    (hboundary : 2*zeroCount ≤ boundary)
    (hidentity : 2*reserve = activation+unused+rotor+boundary)
    (hreserve : reserve = 1) (hfailure : unmarked+reserve < zeroCount+single+twice) :
    unmarked = 0 ∧ zeroCount = 0 ∧ single = 2 ∧ twice = 0 ∧
      activation = 2 ∧ boundary = 0 ∧ unused = 0 ∧ rotor = 0 := by omega

theorem boundary_zero_excludes_all_tiles (lone bar mutualPairs mixed : Nat)
    (hzero : lone+2*bar+2*mutualPairs+mixed = 0) :
    lone = 0 ∧ bar = 0 ∧ mutualPairs = 0 ∧ mixed = 0 := by omega

end SubQuorum.UnactivatedDoubleCompensation
