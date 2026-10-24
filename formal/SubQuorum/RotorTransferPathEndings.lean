import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.RotorTransferPathEndings

abbrev Point := Int × Int

def uEndpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def firstTransverse (width height far : Int) (point : Point) : Prop :=
  uEndpoint width height far (height+2-point.2,point.1-1)

def secondPair (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (point.1-4,point.2-4)

theorem consecutive_pairs_force_a_width_drop
    (width near far crossWidth height crossFar : Int)
    (hheight : 6 ≤ height) (hcross : 6 ≤ crossWidth)
    (hdisjoint : ∀ point, secondPair width near far point →
      ¬firstTransverse crossWidth height crossFar point) : width ≤ height-4 := by
  by_cases hbound : width ≤ height-4
  · exact hbound
  have hpair : secondPair width near far (4,height+1) := by
    unfold secondPair uEndpoint
    dsimp
    omega
  have hcrossPoint : firstTransverse crossWidth height crossFar (4,height+1) := by
    unfold firstTransverse uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (4,height+1) hpair hcrossPoint)

theorem consecutive_pair_widths_decrease_by_eight
    (producerWidth height nextWidth : Int)
    (hheight : height ≤ producerWidth-4)
    (hnext : nextWidth ≤ height-4) : nextWidth ≤ producerWidth-8 := by
  omega

theorem two_pair_edges_require_initial_width_at_least_fourteen
    (producerWidth nextWidth : Int)
    (hnext : 6 ≤ nextWidth) (hdescent : nextWidth ≤ producerWidth-8) :
    14 ≤ producerWidth := by
  omega

def recipientTransverse (width height far : Int) (point : Point) : Prop :=
  uEndpoint width height far (height-point.1,point.2+1)

def singletonConsumer (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (near+3-point.1,3-point.2)

theorem pair_then_singleton_requires_vertical_clearance
    (width near far crossWidth height crossFar : Int)
    (hwidth : 6 ≤ width)
    (hheight : 6 ≤ height) (hcross : 6 ≤ crossWidth)
    (hdisjoint : ∀ point, singletonConsumer width near far point →
      ¬recipientTransverse crossWidth height crossFar point) : near ≤ height-5 := by
  by_cases hbound : near ≤ height-5
  · exact hbound
  have hsingle : singletonConsumer width near far (height-1,2) := by
    unfold singletonConsumer uEndpoint
    dsimp
    omega
  have hcrossPoint : recipientTransverse crossWidth height crossFar (height-1,2) := by
    unfold recipientTransverse uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (height-1,2) hsingle hcrossPoint)

theorem even_singleton_clearance_is_six
    (near height halfNear halfHeight : Int)
    (hnear : near = 2*halfNear) (hheight : height = 2*halfHeight)
    (hbound : near ≤ height-5) : near ≤ height-6 := by
  omega

theorem no_singleton_consumer_can_follow_a_pair_transfer
    (width near far crossWidth height crossFar : Int)
    (hwidth : 6 ≤ width) (hnear : 4 ≤ near)
    (hheight : 6 ≤ height) (hcross : 6 ≤ crossWidth)
    (hdisjoint : ∀ point, singletonConsumer width near far point →
      ¬recipientTransverse crossWidth height crossFar point) : False := by
  by_cases hbar : near+2 ≤ height
  · have hsingle : singletonConsumer width near far (near+2,0) := by
      unfold singletonConsumer uEndpoint
      dsimp
      omega
    have hcrossPoint : recipientTransverse crossWidth height crossFar (near+2,0) := by
      unfold recipientTransverse uEndpoint
      dsimp
      omega
    exact hdisjoint (near+2,0) hsingle hcrossPoint
  · have hsingle : singletonConsumer width near far (height-1,2) := by
      unfold singletonConsumer uEndpoint
      dsimp
      omega
    have hcrossPoint : recipientTransverse crossWidth height crossFar (height-1,2) := by
      unfold recipientTransverse uEndpoint
      dsimp
      omega
    exact hdisjoint (height-1,2) hsingle hcrossPoint

theorem a_tight_pair_cannot_have_a_singleton_exit
    (recipientNear height singletonNear : Int)
    (htight : height = recipientNear+2)
    (hproducer : recipientNear ≤ singletonNear)
    (hgap : singletonNear ≤ height-6) : False := by
  omega

def secondRotorCompanion (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (near+5-point.1,5-point.2)

theorem a_second_rotor_companion_cannot_fit_next_to_the_pair_wall
    (width near far crossWidth height crossFar : Int)
    (hwidth : 6 ≤ width) (hnear : 4 ≤ near)
    (hheight : 6 ≤ height) (hcross : 6 ≤ crossWidth)
    (hdisjoint : ∀ point, secondRotorCompanion width near far point →
      ¬recipientTransverse crossWidth height crossFar point) : False := by
  by_cases hbar : near+4 ≤ height
  · have hcompanion : secondRotorCompanion width near far (near+4,0) := by
      unfold secondRotorCompanion uEndpoint
      dsimp
      omega
    have hcrossPoint : recipientTransverse crossWidth height crossFar (near+4,0) := by
      unfold recipientTransverse uEndpoint
      dsimp
      omega
    exact hdisjoint (near+4,0) hcompanion hcrossPoint
  · have hcompanion : secondRotorCompanion width near far (height-1,4) := by
      unfold secondRotorCompanion uEndpoint
      dsimp
      omega
    have hcrossPoint : recipientTransverse crossWidth height crossFar (height-1,4) := by
      unfold recipientTransverse uEndpoint
      dsimp
      omega
    exact hdisjoint (height-1,4) hcompanion hcrossPoint

theorem a_tight_pair_with_rotor_exit_has_height_six
    (recipientNear height : Int)
    (htight : height = recipientNear+2) (hrotor : recipientNear = 4) : height = 6 := by
  omega

def companion (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (near+3-point.2,point.1-2)

theorem a_hypothetical_pair_producer_hits_the_initial_bar
    (width near far incident height : Int)
    (hincident : 4 ≤ incident) (hheight : incident+4 ≤ height)
    (hproducer : height ≤ width-4) : uEndpoint width near far (0,incident+4) := by
  unfold uEndpoint
  dsimp
  omega

theorem the_companion_north_support_is_consumed
    (crossWidth height crossFar : Int)
    (hcross : 6 ≤ crossWidth) (hheight : 8 ≤ height) :
    firstTransverse crossWidth height crossFar (2,3) := by
  unfold firstTransverse uEndpoint
  dsimp
  omega

theorem rotor_companion_clearance_requires_producer_width_twelve
    (width height incident : Int)
    (hincident : 4 ≤ incident) (hclearance : incident ≤ height-4)
    (hbound : height ≤ width-4) : 12 ≤ width := by
  omega

def pairFrame (point : Point) : Point := (point.2+2,point.1+2)

def pairIterate : Nat → Point → Point
  | 0, point => point
  | length+1, point => pairFrame (pairIterate length point)

theorem pair_iteration_increases_the_diagonal
    (length : Nat) (point : Point) :
    (pairIterate length point).1+(pairIterate length point).2 =
      point.1+point.2+4*(length : Int) := by
  induction length with
  | zero => simp [pairIterate]
  | succ length inductionHypothesis =>
    simp only [pairIterate, pairFrame]
    dsimp
    omega

theorem a_nonempty_pair_run_cannot_close
    (length : Nat) (point : Point) (hpositive : 0 < length) :
    pairIterate length point ≠ point := by
  intro hclosed
  have hdiagonal := pair_iteration_increases_the_diagonal length point
  rw [hclosed] at hdiagonal
  omega

theorem exact_transfer_root_ledger
    (positive marked reserve capacity edges activatedRoots negativeSinks activation : Int)
    (hreserve : 2*reserve = activation+capacity)
    (hactivation : activation = edges+activatedRoots)
    (hmarked : marked = edges+negativeSinks) :
    2*(positive+reserve-marked) =
      capacity+(2*positive-edges)+activatedRoots-2*negativeSinks := by
  omega

theorem exact_path_deficit_ledger
    (positive marked reserve capacity unmarkedPaths activatedUnmarkedRoots
      markedPaths activatedMarkedRoots edges : Int)
    (hvertices : 2*positive = edges+unmarkedPaths+markedPaths)
    (hactivation : 2*reserve = edges+activatedUnmarkedRoots+activatedMarkedRoots+capacity)
    (hmarks : marked = edges+markedPaths) :
    2*(positive+reserve-marked) = capacity+
      (unmarkedPaths+activatedUnmarkedRoots)-(markedPaths-activatedMarkedRoots) := by
  omega

end SubQuorum.RotorTransferPathEndings
