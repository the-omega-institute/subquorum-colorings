import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.BoundaryFluxCuts

inductive TileRole where
  | nonnegative
  | newNegativeU
  | oldNegativeU
  | negativeRotor
  | rotorMate
  deriving DecidableEq

def oldDebit (role : TileRole) : Int := if role = .oldNegativeU then 1 else 0

def negativeRotor (role : TileRole) : Int := if role = .negativeRotor then 1 else 0

def rotorMate (role : TileRole) : Int := if role = .rotorMate then 1 else 0

def tileResidual (role : TileRole) (weight terminals : Int) : Int :=
  weight+terminals+oldDebit role+negativeRotor role-rotorMate role

def tileCertificate (role : TileRole) (weight terminals : Int) : Prop :=
  0 ≤ terminals ∧ match role with
    | .nonnegative => 0 ≤ weight
    | .newNegativeU => weight = -1 ∧ terminals = 1
    | .oldNegativeU => weight = -1 ∧ terminals = 0
    | .negativeRotor => weight = -1 ∧ terminals = 0
    | .rotorMate => weight = 1

theorem tile_residual_nonnegative (role : TileRole) (weight terminals : Int)
    (hcertificate : tileCertificate role weight terminals) :
    0 ≤ tileResidual role weight terminals := by
  cases role <;>
    simp_all [tileCertificate, tileResidual, oldDebit, negativeRotor, rotorMate] <;> omega

def sumInt (values : List Int) : Int :=
  match values with
  | [] => 0
  | first :: remaining => first+sumInt remaining

theorem sum_nonnegative (values : List Int)
    (hvalues : ∀ value ∈ values, 0 ≤ value) : 0 ≤ sumInt values := by
  induction values with
  | nil => simp [sumInt]
  | cons first remaining inductionHypothesis =>
    have hfirst := hvalues first (by simp)
    have hremaining : ∀ value ∈ remaining, 0 ≤ value := by
      intro value hmember
      exact hvalues value (by simp [hmember])
    have hinduction := inductionHypothesis hremaining
    simp only [sumInt]
    omega

structure Arc where
  source : Nat
  target : Nat

def incoming (region : Nat → Bool) (arc : Arc) : Int :=
  if !region arc.source && region arc.target then 1 else 0

def outgoing (region : Nat → Bool) (arc : Arc) : Int :=
  if region arc.source && !region arc.target then 1 else 0

def membership (region : Nat → Bool) (tile : Nat) : Int :=
  if region tile then 1 else 0

theorem arc_boundary_identity (region : Nat → Bool) (arc : Arc) :
    incoming region arc-outgoing region arc =
      membership region arc.target-membership region arc.source := by
  cases hsource : region arc.source <;> cases htarget : region arc.target <;>
    simp [incoming, outgoing, membership, hsource, htarget]

theorem arc_complement_conservation (region : Nat → Bool) (arc : Arc) :
    incoming region arc-outgoing region arc+
      incoming (fun tile => !region tile) arc-outgoing (fun tile => !region tile) arc = 0 := by
  cases hsource : region arc.source <;> cases htarget : region arc.target <;>
    simp [incoming, outgoing, hsource, htarget]

def flux (region : Nat → Bool) (arcs : List Arc) : Int :=
  sumInt (arcs.map fun arc => incoming region arc-outgoing region arc)

theorem flux_complement_conservation (region : Nat → Bool) (arcs : List Arc) :
    flux region arcs+flux (fun tile => !region tile) arcs = 0 := by
  induction arcs with
  | nil => simp [flux, sumInt]
  | cons first remaining inductionHypothesis =>
    have hfirst := arc_complement_conservation region first
    simp only [flux, List.map_cons, sumInt] at *
    omega

structure Region where
  addedPositive : Int
  oldDoubledBeta : Int
  actualOldNegative : Int
  eligibleOldNegative : Int
  incoming : Int
  outgoing : Int
  residual : Int
  doubledIncrement : Int

def certified (region : Region) : Prop :=
  region.actualOldNegative ≤ region.eligibleOldNegative ∧
  0 ≤ region.residual ∧
  region.doubledIncrement = 2*region.addedPositive-region.oldDoubledBeta-
    region.actualOldNegative+region.incoming-region.outgoing+region.residual

theorem arbitrary_cut_bound (region : Region) (hcertificate : certified region) :
    2*region.addedPositive-region.oldDoubledBeta-region.eligibleOldNegative+
      region.incoming-region.outgoing ≤ region.doubledIncrement := by
  unfold certified at hcertificate
  omega

def sumField (regions : List Region) (field : Region → Int) : Int :=
  match regions with
  | [] => 0
  | first :: remaining => field first+sumField remaining field

theorem exact_partition_sum (regions : List Region)
    (hcertificates : ∀ region ∈ regions, certified region) :
    sumField regions Region.doubledIncrement =
      2*sumField regions Region.addedPositive-sumField regions Region.oldDoubledBeta-
      sumField regions Region.actualOldNegative+sumField regions Region.incoming-
      sumField regions Region.outgoing+sumField regions Region.residual := by
  induction regions with
  | nil => simp [sumField]
  | cons first remaining inductionHypothesis =>
    have hfirst := hcertificates first (by simp)
    have hremaining : ∀ region ∈ remaining, certified region := by
      intro region hmember
      exact hcertificates region (by simp [hmember])
    have hinduction := inductionHypothesis hremaining
    unfold certified at hfirst
    simp only [sumField]
    omega

theorem partition_bound_with_flux (regions : List Region)
    (hcertificates : ∀ region ∈ regions, certified region) :
    2*sumField regions Region.addedPositive-sumField regions Region.oldDoubledBeta-
      sumField regions Region.eligibleOldNegative+sumField regions Region.incoming-
      sumField regions Region.outgoing ≤ sumField regions Region.doubledIncrement := by
  induction regions with
  | nil => simp [sumField]
  | cons first remaining inductionHypothesis =>
    have hfirst := arbitrary_cut_bound first (hcertificates first (by simp))
    have hremaining : ∀ region ∈ remaining, certified region := by
      intro region hmember
      exact hcertificates region (by simp [hmember])
    have hinduction := inductionHypothesis hremaining
    simp only [sumField]
    omega

theorem partition_bound_with_conserved_flux (regions : List Region)
    (hcertificates : ∀ region ∈ regions, certified region)
    (hconservation : sumField regions Region.incoming = sumField regions Region.outgoing) :
    2*sumField regions Region.addedPositive-sumField regions Region.oldDoubledBeta-
      sumField regions Region.eligibleOldNegative ≤ sumField regions Region.doubledIncrement := by
  have hsum := partition_bound_with_flux regions hcertificates
  omega

theorem old_rotor_boundary_repair :
    (0 : Int) = 0-(-1)-0+0-1+0 := by decide

theorem split_positive_terminal_repair : (-1 : Int)+1 = 0 := by decide

def ceilHalf (value : Int) : Int := (value+1)/2

theorem zero_rotor_exact_partition : sumInt [-1, -1, 1, 1] = 0 := by decide

theorem zero_rotor_separate_rounding :
    sumInt (([-1, -1, 1, 1] : List Int).map ceilHalf) = 2 := by decide

#print axioms TileRole
#print axioms oldDebit
#print axioms negativeRotor
#print axioms rotorMate
#print axioms tileResidual
#print axioms tileCertificate
#print axioms tile_residual_nonnegative
#print axioms sumInt
#print axioms sum_nonnegative
#print axioms Arc
#print axioms incoming
#print axioms outgoing
#print axioms membership
#print axioms arc_boundary_identity
#print axioms arc_complement_conservation
#print axioms flux
#print axioms flux_complement_conservation
#print axioms Region
#print axioms certified
#print axioms arbitrary_cut_bound
#print axioms sumField
#print axioms exact_partition_sum
#print axioms partition_bound_with_flux
#print axioms partition_bound_with_conserved_flux
#print axioms old_rotor_boundary_repair
#print axioms split_positive_terminal_repair
#print axioms ceilHalf
#print axioms zero_rotor_exact_partition
#print axioms zero_rotor_separate_rounding

end SubQuorum.BoundaryFluxCuts
