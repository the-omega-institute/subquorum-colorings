import Std

set_option autoImplicit false

namespace SubQuorum.SupportChainCompensation

theorem propagate_to_end (length : Nat) (consumed full : Nat → Prop)
    (hstart : consumed 0)
    (hstep : ∀ index, index < length → consumed index → full index → consumed (index+1))
    (hnoStop : ∀ index, index < length → consumed index → full index) :
    ∀ index, index ≤ length → consumed index := by
  intro index
  induction index with
  | zero => intro _; exact hstart
  | succ index previous =>
    intro hbound
    have hindex : index < length := by omega
    exact hstep index hindex (previous (by omega))
      (hnoStop index hindex (previous (by omega)))

theorem unactivated_chain_has_stop (length : Nat) (consumed full : Nat → Prop)
    (hstart : consumed 0)
    (hstep : ∀ index, index < length → consumed index → full index → consumed (index+1))
    (hterminal : ¬consumed length) :
    ∃ index, index < length ∧ consumed index ∧ ¬full index := by
  apply Classical.byContradiction
  intro hnone
  have hnoStop : ∀ index, index < length → consumed index → full index := by
    intro index hindex hconsumed
    apply Classical.byContradiction
    intro hnot
    exact hnone ⟨index, hindex, hconsumed, hnot⟩
  exact hterminal (propagate_to_end length consumed full hstart hstep hnoStop length (by omega))

theorem no_stopping_defect_fills_chain (length : Nat) (consumed full : Nat → Prop)
    (hstart : consumed 0)
    (hstep : ∀ index, index < length → consumed index → full index → consumed (index+1))
    (hnoStop : ∀ index, index < length → consumed index → full index) :
    ∀ index, index < length → full index := by
  intro index hindex
  exact hnoStop index hindex
    (propagate_to_end length consumed full hstart hstep hnoStop index (by omega))

theorem two_pairs_cannot_share_nonfull_square {Point : Type}
    (first second third fourth : Point) (occupied : List Point)
    (hdistinct : [first, second, third, fourth].Nodup)
    (hsubset : [first, second, third, fourth] ⊆ occupied)
    (hnonfull : occupied.length ≤ 3) : False := by
  have hcount := hdistinct.length_le_of_subset hsubset
  simp only [List.length_cons, List.length_nil] at hcount
  omega

theorem separate_slot_lists {Slot : Type} (old fresh pool : List Slot)
    (hold : old.Nodup) (hfresh : fresh.Nodup)
    (hseparate : ∀ first ∈ old, ∀ second ∈ fresh, first ≠ second)
    (hsubset : old ++ fresh ⊆ pool) : old.length+fresh.length ≤ pool.length := by
  have hdistinct : (old ++ fresh).Nodup := List.nodup_append.mpr ⟨hold, hfresh, hseparate⟩
  have hcount := hdistinct.length_le_of_subset hsubset
  simpa only [List.length_append] using hcount

theorem shared_chain_reserve (zeroCount single twice paid broken exterior activation unfilled
    rotor boundary reserve : Nat)
    (hactivation : single+2*twice ≤ activation)
    (hpool : 2*zeroCount+paid+broken+exterior ≤ unfilled+boundary)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary) :
    2*(zeroCount+single+twice) ≤ 2*reserve+single-paid-broken-exterior := by omega

theorem joint_from_chain_budget (zeroCount single twice paid broken exterior exceptional
    unmarked activation unfilled rotor boundary reserve : Nat)
    (hactivation : single+2*twice ≤ activation)
    (hpool : 2*zeroCount+paid+broken+exterior ≤ unfilled+boundary)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary)
    (hbudget : single+2*exceptional ≤ 2*unmarked+paid+broken+exterior+1) :
    zeroCount+single+twice+exceptional ≤ unmarked+reserve := by omega

theorem signed_chain_margin (zeroCount single twice paid broken exterior exceptional unmarked
    activation unfilled rotor boundary reserve : Nat) (margin : Int)
    (hactivation : single+2*twice ≤ activation)
    (hpool : 2*zeroCount+paid+broken+exterior ≤ unfilled+boundary)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary)
    (hledger : (unmarked : Int)+reserve-(zeroCount+single+twice+exceptional) ≤ margin) :
    (unmarked : Int)-exceptional-((single : Int)-paid-broken-exterior)/2 ≤ margin := by omega

theorem two_extra_units_improve_bound (single paid broken exterior : Int)
    (hextra : 2 ≤ broken+exterior) :
    (single-paid-broken-exterior)/2+1 ≤ (single-paid)/2 := by omega

theorem signed_remainder_sum (values : List Int) :
    values.sum = 2*(values.map (fun value => value/2)).sum+
      (values.map (fun value => value%2)).sum := by
  induction values with
  | nil => simp
  | cons value rest previous =>
    simp only [List.sum_cons, List.map_cons]
    omega

theorem component_parity_gain (values : List Int) :
    values.sum/2-(values.map (fun value => value/2)).sum =
      (values.map (fun value => value%2)).sum/2 := by
  have hsum := signed_remainder_sum values
  omega

theorem first_reserve_failure_has_no_chain_payments (zeroCount single twice paid broken exterior
    unmarked activation unfilled rotor boundary reserve : Nat)
    (hactivation : single+2*twice ≤ activation)
    (hpool : 2*zeroCount+paid+broken+exterior ≤ unfilled+boundary)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary)
    (hreserve : reserve = 1) (hfailure : unmarked+reserve < zeroCount+single+twice) :
    unmarked = 0 ∧ zeroCount = 0 ∧ single = 2 ∧ twice = 0 ∧ paid = 0 ∧
      broken = 0 ∧ exterior = 0 ∧ activation = 2 ∧ unfilled = 0 ∧ rotor = 0 ∧ boundary = 0 := by
  omega

end SubQuorum.SupportChainCompensation
