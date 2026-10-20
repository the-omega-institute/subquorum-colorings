import Std

set_option autoImplicit false

namespace SubQuorum.MixedCycleExternalAbsorbers

def contactTurn (sign : Int) (activeExit : Bool) : Int :=
  if activeExit then -sign else sign

def incidentPhase10Sign (sign : Int) (first01 second01 : Bool) : Int :=
  (if first01 then 0 else sign)+(if second01 then 0 else -sign)

def phase01ContactTurn (sign : Int) (first01 second01 activeExit : Bool) : Int :=
  if first01 && second01 then contactTurn sign activeExit else 0

def passivePhase10Sign (sign : Int) (first01 second01 activeExit : Bool) : Int :=
  if activeExit then (if second01 then 0 else -sign)
  else (if first01 then 0 else sign)

def doublePhase10Turn (sign : Int) (first01 second01 activeExit : Bool) : Int :=
  if !first01 && !second01 then contactTurn sign activeExit else 0

theorem each_contact_cancels_its_incident_source_signs
    (sign : Int) (first01 second01 activeExit : Bool) :
    contactTurn sign activeExit+incidentPhase10Sign sign first01 second01 =
      phase01ContactTurn sign first01 second01 activeExit+
      2*passivePhase10Sign sign first01 second01 activeExit-
      doublePhase10Turn sign first01 second01 activeExit := by
  cases first01 <;> cases second01 <;> cases activeExit <;>
    simp [contactTurn, incidentPhase10Sign, phase01ContactTurn,
      passivePhase10Sign, doublePhase10Turn] <;> omega

theorem corrected_inward_count
    (phase01 phase10 components inward passive01Positive passive01Negative
      passive10Negative : Nat)
    (hidentity : 2*inward+phase10+2*passive01Positive =
      phase01+4*components+2*passive01Negative+2*passive10Negative) :
    phase01+4*components ≤ phase10+2*(passive01Positive+passive01Negative)+2*inward := by
  omega

theorem external_absorber_count_for_all_mixed_cycles
    (phase01 phase10 components passive01 inward internalAbsorptions externalOwners : Nat)
    (hturning : phase01+4*components ≤ phase10+2*passive01+2*inward)
    (habsorb : inward ≤ internalAbsorptions+4*externalOwners)
    (hinternal : internalAbsorptions ≤ 2*phase10) :
    phase01+4*components ≤ 5*phase10+2*passive01+8*externalOwners := by
  omega

theorem external_absorber_count_with_shared_passive_budget
    (phase01 phase10 components passive01 allPassive externalOwners activation boundary : Nat)
    (hcount : phase01+4*components ≤ 5*phase10+2*passive01+8*externalOwners)
    (hsubset : passive01 ≤ allPassive)
    (hpassive : allPassive ≤ 2*activation+boundary) :
    phase01+4*components ≤ 5*phase10+4*activation+2*boundary+8*externalOwners := by
  omega

theorem retained_reserve_identity_for_mixed_cycles
    (phase01 phase10 components externalOwners activation boundary unfilled rotor reserve : Nat)
    (hcount : phase01+4*components ≤ 5*phase10+4*activation+2*boundary+8*externalOwners)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary) :
    phase01+4*components+4*unfilled+4*rotor+2*boundary ≤
      5*phase10+8*externalOwners+8*reserve := by
  omega

def externalQuota (phase01 phase10 passive01 internalAbsorptions : Nat) : Nat :=
  ((phase01+4-(phase10+2*passive01+2*internalAbsorptions))+7)/8

theorem rounded_external_quota
    (phase01 phase10 passive01 internalAbsorptions externalOwners : Nat)
    (hcount : phase01+4 ≤ phase10+2*passive01+2*internalAbsorptions+8*externalOwners) :
    externalQuota phase01 phase10 passive01 internalAbsorptions ≤ externalOwners := by
  simp [externalQuota]
  omega

theorem a_region_label_prevents_external_owner_reuse
    {Curve Owner : Type} (region : Owner → Curve) (absorbs : Curve → Owner → Prop)
    (hregion : ∀ curve owner, absorbs curve owner → region owner = curve)
    (first second : Curve) (owner : Owner)
    (hfirst : absorbs first owner) (hsecond : absorbs second owner) : first = second := by
  exact (hregion first owner hfirst).symm.trans (hregion second owner hsecond)

theorem AA_mixed_cycle_external_budget
    (phase01 phase10 components externalOwners activation boundary : Nat)
    (hcount : phase01+4*components ≤ 5*phase10+4*activation+2*boundary+8*externalOwners)
    (hactivation : activation = 2) (hboundary : boundary = 0) :
    phase01+4*components ≤ 5*phase10+8*externalOwners+8 := by
  omega

end SubQuorum.MixedCycleExternalAbsorbers
