import SubQuorum.WidthSixBottomOwner

set_option autoImplicit false

namespace SubQuorum.NeutralPhaseTenDescent

open WidthSixBottomOwner

def phaseTenAtForcedPoint (flipRow flipColumn : Bool) (anchor : Point) : Prop :=
  anchor.1%2 = (if flipRow then 1 else 0) ∧
  anchor.2%2 = (if flipColumn then 0 else 1)

def pulledReceiverOrigin (flipRow flipColumn : Bool) (anchor : Point) : Point :=
  (anchor.1 - (if flipRow then 0 else 1),
   anchor.2 - (if flipColumn then 0 else 1))

theorem pulled_receiver_tile_bounds (transpose flipRow flipColumn : Bool)
    (anchor point : Point) :
    (-1 ≤ point.1 ∧ point.1 ≤ 0 ∧ -1 ≤ point.2 ∧ point.2 ≤ 0) ↔
    (let origin := pulledReceiverOrigin flipRow flipColumn anchor
     let canonical := pull transpose flipRow flipColumn anchor point
     origin.1 ≤ canonical.1 ∧ canonical.1 ≤ origin.1+1 ∧
     origin.2 ≤ canonical.2 ∧ canonical.2 ≤ origin.2+1) := by
  cases transpose <;> cases flipRow <;> cases flipColumn <;>
    simp [pulledReceiverOrigin, pull] <;> omega

theorem phase_ten_parity_of_receiver_origin (flipRow flipColumn : Bool)
    (anchor : Point)
    (hrow : (pulledReceiverOrigin flipRow flipColumn anchor).1%2 = 1)
    (hcolumn : (pulledReceiverOrigin flipRow flipColumn anchor).2%2 = 0) :
    phaseTenAtForcedPoint flipRow flipColumn anchor := by
  cases flipRow <;> cases flipColumn <;>
    simp [pulledReceiverOrigin, phaseTenAtForcedPoint] at hrow hcolumn ⊢ <;> omega

theorem original_owner_excludes_foreign_endpoints
    {Owner : Type} (owns : Owner → Point → Prop) (active passive forced : Owner)
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hunique : ∀ first second point,
      owns first point → owns second point → first = second)
    (hforced : owns forced (0,0))
    (hnotActive : ¬ owns active (0,0)) (hnotPassive : ¬ owns passive (0,0))
    (hmodel : ∀ point, owns forced point ↔
      endpoint width left right (pull transpose flipRow flipColumn anchor point))
    (hwest : owns active (0,-1)) (hsouth : owns passive (1,0))
    (hnorthwest : owns active (-1,-1)) (hsoutheast : owns passive (1,1)) :
    (¬ endpoint width left right (pull transpose flipRow flipColumn anchor (0,-1))) ∧
    (¬ endpoint width left right (pull transpose flipRow flipColumn anchor (1,0))) ∧
    (¬ endpoint width left right (pull transpose flipRow flipColumn anchor (-1,-1))) ∧
    (¬ endpoint width left right (pull transpose flipRow flipColumn anchor (1,1))) := by
  have hforeign : ∀ owner point, (¬ owns owner (0,0)) → owns owner point →
      ¬ endpoint width left right (pull transpose flipRow flipColumn anchor point) := by
    intro owner point hnot hpoint hendpoint
    have hequal := hunique owner forced point hpoint ((hmodel point).mpr hendpoint)
    exact hnot (hequal.symm ▸ hforced)
  exact ⟨hforeign active (0,-1) hnotActive hwest,
    hforeign passive (1,0) hnotPassive hsouth,
    hforeign active (-1,-1) hnotActive hnorthwest,
    hforeign passive (1,1) hnotPassive hsoutheast⟩

set_option maxHeartbeats 2000000 in
theorem phase_ten_forced_owner_is_north_terminal
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hevenWidth : width%2 = 0) (hevenLeft : left%2 = 0) (hevenRight : right%2 = 0)
    (hroot : endpoint width left right anchor)
    (hwest : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,-1)))
    (hsouth : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (1,0)))
    (hnorthwest : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (-1,-1)))
    (hsoutheast : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (1,1)))
    (hphase : phaseTenAtForcedPoint flipRow flipColumn anchor) :
    transpose = false ∧ flipRow = false ∧
      ((flipColumn = false ∧ anchor = (left,1)) ∨
       (flipColumn = true ∧ anchor = (right,width))) := by
  rcases anchor with ⟨row,column⟩
  rcases hroot with hbar | hnear | hfar
  all_goals
    cases transpose <;> cases flipRow <;> cases flipColumn <;>
      simp [endpoint, pull, phaseTenAtForcedPoint, Prod.mk.injEq] at hwest hsouth hnorthwest hsoutheast hphase ⊢ <;> omega

theorem phase_ten_terminal_owns_next_corner (width incident far : Int)
    (hwidth : 6 ≤ width) (hincident : 4 ≤ incident) :
    endpoint width incident far (incident-1,1) := by
  simp [endpoint]
  omega

theorem physical_phase_ten_owner_is_north_terminal
    {Owner : Type} (owns : Owner → Point → Prop) (active passive forced : Owner)
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hevenWidth : width%2 = 0) (hevenLeft : left%2 = 0) (hevenRight : right%2 = 0)
    (hunique : ∀ first second point,
      owns first point → owns second point → first = second)
    (hforced : owns forced (0,0))
    (hnotActive : ¬ owns active (0,0)) (hnotPassive : ¬ owns passive (0,0))
    (hmodel : ∀ point, owns forced point ↔
      endpoint width left right (pull transpose flipRow flipColumn anchor point))
    (hwest : owns active (0,-1)) (hsouth : owns passive (1,0))
    (hnorthwest : owns active (-1,-1)) (hsoutheast : owns passive (1,1))
    (hrow : (pulledReceiverOrigin flipRow flipColumn anchor).1%2 = 1)
    (hcolumn : (pulledReceiverOrigin flipRow flipColumn anchor).2%2 = 0) :
    transpose = false ∧ flipRow = false ∧
      ((flipColumn = false ∧ anchor = (left,1)) ∨
       (flipColumn = true ∧ anchor = (right,width))) := by
  have hroot := (hmodel (0,0)).mp hforced
  simp [pull] at hroot
  obtain ⟨hwest',hsouth',hnorthwest',hsoutheast'⟩ :=
    original_owner_excludes_foreign_endpoints owns active passive forced
      width left right anchor transpose flipRow flipColumn hunique hforced
      hnotActive hnotPassive hmodel hwest hsouth hnorthwest hsoutheast
  exact phase_ten_forced_owner_is_north_terminal width left right anchor
    transpose flipRow flipColumn hwidth hleft hright hevenWidth hevenLeft hevenRight
    hroot hwest' hsouth' hnorthwest' hsoutheast'
    (phase_ten_parity_of_receiver_origin flipRow flipColumn anchor hrow hcolumn)

theorem north_terminal_full_run_and_east_bar
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hevenLeft : left%2 = 0) (hevenRight : right%2 = 0)
    (hrole : transpose = false ∧ flipRow = false ∧
      ((flipColumn = false ∧ anchor = (left,1)) ∨
       (flipColumn = true ∧ anchor = (right,width)))) :
    ∃ incident : Int, 4 ≤ incident ∧ incident%2 = 0 ∧
      (∀ row : Int, -incident ≤ row → row ≤ 0 →
        endpoint width left right (pull transpose flipRow flipColumn anchor (row,0))) ∧
      (∀ column : Int, 0 ≤ column → column ≤ width-1 →
        endpoint width left right
          (pull transpose flipRow flipColumn anchor (1-incident,column))) ∧
      (¬ endpoint width left right (pull transpose flipRow flipColumn anchor (1,0))) := by
  rcases hrole with ⟨rfl,rfl,⟨rfl,rfl⟩ | ⟨rfl,rfl⟩⟩
  · refine ⟨left,hleft,hevenLeft,?_,?_,?_⟩
    · intro row hlower hupper
      simp [pull, endpoint]
      omega
    · intro column hlower hupper
      simp [pull, endpoint]
      omega
    · simp [pull, endpoint]
      omega
  · refine ⟨right,hright,hevenRight,?_,?_,?_⟩
    · intro row hlower hupper
      simp [pull, endpoint]
      omega
    · intro column hlower hupper
      simp [pull, endpoint]
      omega
    · simp [pull, endpoint]
      omega

theorem incident_height_strictly_decreases (active incoming : Int)
    (hactive : 4 ≤ active) (_hincoming : 4 ≤ incoming)
    (hevenActive : active%2 = 0) (hevenIncoming : incoming%2 = 0)
    (hdisjoint : ¬ (-incoming ≤ 2-active ∧ 2-active ≤ 0)) :
    incoming+4 ≤ active := by omega

theorem original_disjointness_implies_height_descent
    {Owner : Type} (owns : Owner → Point → Prop) (activeOwner forcedOwner : Owner)
    (active incoming : Int)
    (hactive : 4 ≤ active) (hincoming : 4 ≤ incoming)
    (hevenActive : active%2 = 0) (hevenIncoming : incoming%2 = 0)
    (hunique : ∀ first second point,
      owns first point → owns second point → first = second)
    (hforced : owns forcedOwner (0,0)) (hnotActive : ¬ owns activeOwner (0,0))
    (hbar : owns activeOwner (2-active,0))
    (hrun : ∀ row : Int, -incoming ≤ row → row ≤ 0 → owns forcedOwner (row,0)) :
    incoming+4 ≤ active := by
  apply incident_height_strictly_decreases active incoming hactive hincoming
    hevenActive hevenIncoming
  intro ⟨hlower,hupper⟩
  have hequal := hunique activeOwner forcedOwner (2-active,0) hbar
    (hrun (2-active) hlower hupper)
  exact hnotActive (hequal.symm ▸ hforced)

theorem shortest_legs_exclude_phase_ten (active incoming : Int)
    (hactive : active = 4 ∨ active = 6) (hincoming : 4 ≤ incoming)
    (hdescent : incoming+4 ≤ active) : False := by omega

theorem minimal_height_descent_is_sharp (incoming : Int) :
    incoming+4-incoming = 4 := by omega

theorem iterated_descent_bound (height : Nat → Int) (length : Nat)
    (hstep : ∀ index, index+1 < length →
      height (index+1)+4 ≤ height index) :
    ∀ index, index < length →
      height index+4*(index : Int) ≤ height 0 := by
  intro index hindex
  induction index with
  | zero => simp
  | succ index ih =>
    have hprior : index < length := by omega
    have hbefore := ih hprior
    have hnext := hstep index (by omega)
    omega

end SubQuorum.NeutralPhaseTenDescent
