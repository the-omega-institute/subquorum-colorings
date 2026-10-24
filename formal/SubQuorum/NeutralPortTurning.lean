import Std

set_option autoImplicit false

namespace SubQuorum.NeutralPortTurning

def localMoment (sign : Int) (phase01 : Bool) (active : Nat) : Int :=
  sign * (if phase01 then (active : Int) else (active : Int)-2)

def localCapacity (phase01 : Bool) (active : Nat) : Nat :=
  if phase01 then active else 2-active

theorem local_moment_bounds (sign : Int) (phase01 : Bool) (active : Nat)
    (hsign : sign = 1 ∨ sign = -1) (hactive : active ≤ 2) :
    -(localCapacity phase01 active : Int) ≤ localMoment sign phase01 active ∧
    localMoment sign phase01 active ≤ localCapacity phase01 active := by
  rcases hsign with rfl | rfl <;> cases phase01 <;>
    simp [localMoment, localCapacity] <;> omega

def signedMoment : List (Int × Bool × Nat) → Int
  | [] => 0
  | entry :: rest => localMoment entry.1 entry.2.1 entry.2.2+signedMoment rest

def capacityTotal : List (Int × Bool × Nat) → Nat
  | [] => 0
  | entry :: rest => localCapacity entry.2.1 entry.2.2+capacityTotal rest

theorem signed_moment_bounds (entries : List (Int × Bool × Nat))
    (hentries : ∀ entry ∈ entries, (entry.1 = 1 ∨ entry.1 = -1) ∧ entry.2.2 ≤ 2) :
    -(capacityTotal entries : Int) ≤ signedMoment entries ∧
    signedMoment entries ≤ capacityTotal entries := by
  induction entries with
  | nil => simp [signedMoment, capacityTotal]
  | cons entry rest inductionHypothesis =>
    have hentry := hentries entry (by simp)
    have hrest : ∀ item ∈ rest, (item.1 = 1 ∨ item.1 = -1) ∧ item.2.2 ≤ 2 := by
      intro item hitem
      exact hentries item (by simp [hitem])
    have htail := inductionHypothesis hrest
    have hlocal := local_moment_bounds entry.1 entry.2.1 entry.2.2 hentry.1 hentry.2
    simp only [signedMoment, capacityTotal, Int.natCast_add]
    omega

theorem total_turn_forces_capacity (entries : List (Int × Bool × Nat))
    (hentries : ∀ entry ∈ entries, (entry.1 = 1 ∨ entry.1 = -1) ∧ entry.2.2 ≤ 2)
    (hturn : signedMoment entries = 4 ∨ signedMoment entries = -4) :
    4 ≤ capacityTotal entries := by
  have hbounds := signed_moment_bounds entries hentries
  omega

theorem closed_curve_count (components phase01 phase10 active01 active10 passive10 : Nat)
    (hactive : active01+active10 = phase01+phase10)
    (hphase10 : active10+passive10 = 2*phase10)
    (hturning : 4*components ≤ active01+passive10) :
    4*components+phase10 ≤ phase01+2*passive10 := by omega

theorem double_passive_count
    (components positive01 negative01 positive10 negative10 single10 passive10 : Nat)
    (hbalance : positive01+positive10 = negative01+negative10)
    (hpassive : passive10 = 2*negative10+single10)
    (hturning : 4*components ≤ positive01+negative01+positive10+3*negative10+2*single10) :
    2*components ≤ negative01+passive10 := by omega

theorem closed_passive_occurrences_do_not_repeat {Port : Type}
    (closedPorts originalPassiveCorners : List Port)
    (hdistinct : closedPorts.Nodup)
    (hsubset : closedPorts ⊆ originalPassiveCorners) :
    closedPorts.length ≤ originalPassiveCorners.length :=
  hdistinct.length_le_of_subset hsubset

theorem shared_activation_boundary_budget
    (components phase01 phase10 passive10 allPassive activation boundary : Nat)
    (hcurves : 4*components+phase10 ≤ phase01+2*passive10)
    (hsubset : passive10 ≤ allPassive)
    (hcorner : allPassive ≤ 2*activation+boundary) :
    4*components+phase10 ≤ phase01+4*activation+2*boundary := by omega

theorem double_passive_shared_budget
    (components sinks passive10 allPassive activation boundary : Nat)
    (hcurves : 2*components ≤ sinks+passive10)
    (hsubset : passive10 ≤ allPassive)
    (hcorner : allPassive ≤ 2*activation+boundary) :
    2*components ≤ sinks+2*activation+boundary := by omega

theorem retained_reserve_budget
    (components phase01 phase10 activation unfilled rotor boundary reserve : Nat)
    (hcurves : 4*components+phase10 ≤ phase01+4*activation+2*boundary)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary) :
    4*components+phase10+2*boundary+4*unfilled+4*rotor ≤ phase01+8*reserve := by omega

theorem AA_phase_count (components phase01 phase10 passive10 : Nat)
    (hcurves : 4*components+phase10 ≤ phase01+2*passive10)
    (hnoPassive : passive10 = 0) :
    phase10+4*components ≤ phase01 := by omega

theorem AA_sink_count (components sinks passive10 : Nat)
    (hcurves : 2*components ≤ sinks+passive10) (hnoPassive : passive10 = 0) :
    2*components ≤ sinks := by omega

end SubQuorum.NeutralPortTurning
