import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.MixedRelayEndpointAccounting

inductive Kind where
  | minus
  | plus
  deriving DecidableEq

def flip : Kind → Kind
  | .minus => .plus
  | .plus => .minus

def sign : Kind → Int
  | .minus => -1
  | .plus => 1

def signed : List Kind → Int
  | [] => 0
  | first :: rest => sign first + signed rest

structure Edge where
  left : Kind
  right : Kind

def ends : List Edge → List Kind
  | [] => []
  | edge :: rest => edge.left :: edge.right :: ends rest

def positive : List Edge → Nat
  | [] => 0
  | edge :: rest => (if edge.left = .plus ∧ edge.right = .plus then 1 else 0) + positive rest

def negative : List Edge → Nat
  | [] => 0
  | edge :: rest => (if edge.left = .minus ∧ edge.right = .minus then 1 else 0) + negative rest

inductive Neutral : List Edge → Prop where
  | nil : Neutral []
  | cons (left right : Kind) (rest : List Edge) (opposite : left ≠ right)
      (tail : Neutral rest) : Neutral (⟨left, right⟩ :: rest)

theorem signed_append (first second : List Kind) :
    signed (first ++ second) = signed first + signed second := by
  induction first with
  | nil => simp [signed]
  | cons first rest inductionHypothesis =>
    simp only [List.cons_append, signed, inductionHypothesis]
    omega

theorem signed_flip (kinds : List Kind) : signed (kinds.map flip) = -signed kinds := by
  induction kinds with
  | nil => simp [signed]
  | cons first rest inductionHypothesis =>
    cases first <;> simp only [List.map_cons, flip, signed, sign, inductionHypothesis] <;> omega

theorem permutation_signed {first second : List Kind} (permutation : List.Perm first second) :
    signed first = signed second := by
  induction permutation with
  | nil => rfl
  | cons first permutation inductionHypothesis => simp only [signed, inductionHypothesis]
  | swap first second rest => simp only [signed]; omega
  | trans first second firstHypothesis secondHypothesis => omega

theorem neutral_actual_endpoint_sum {actual : List Edge} (neutral : Neutral actual) :
    signed (ends actual) = 0 := by
  induction neutral with
  | nil => rfl
  | cons left right rest opposite tail inductionHypothesis =>
    cases left <;> cases right <;> simp_all [ends, signed, sign]

theorem signed_auxiliary_edge_count (auxiliary : List Edge) :
    signed (ends auxiliary) = 2*((positive auxiliary : Int)-(negative auxiliary : Int)) := by
  induction auxiliary with
  | nil => simp [ends, signed, positive, negative]
  | cons edge rest inductionHypothesis =>
    obtain ⟨left, right⟩ := edge
    cases left <;> cases right <;>
      simp_all [ends, signed, positive, negative, sign] <;> omega

theorem mixed_relay_component_identity (actual auxiliary : List Edge)
    (chosen relay : List Kind) (neutral : Neutral actual)
    (incidence : List.Perm (ends auxiliary ++ relay) (ends actual ++ chosen)) :
    2*((positive auxiliary : Int)-(negative auxiliary : Int)) =
      signed (chosen ++ relay.map flip) := by
  have partition := permutation_signed incidence
  have actualSum := neutral_actual_endpoint_sum neutral
  have auxiliarySum := signed_auxiliary_edge_count auxiliary
  rw [signed_append, signed_append] at partition
  rw [signed_append, signed_flip]
  omega

theorem alpha_requires_negative_edge (actual auxiliary : List Edge)
    (chosen relay : List Kind) (neutral : Neutral actual)
    (incidence : List.Perm (ends auxiliary ++ relay) (ends actual ++ chosen))
    (physicalEnds : chosen ++ relay.map flip = [.minus, .minus]) :
    1 ≤ negative auxiliary := by
  have identity := mixed_relay_component_identity actual auxiliary chosen relay neutral incidence
  rw [physicalEnds] at identity
  simp only [signed, sign] at identity
  omega

theorem beta_requires_positive_edge (actual auxiliary : List Edge)
    (chosen relay : List Kind) (neutral : Neutral actual)
    (incidence : List.Perm (ends auxiliary ++ relay) (ends actual ++ chosen))
    (physicalEnds : chosen ++ relay.map flip = [.plus, .plus]) :
    1 ≤ positive auxiliary := by
  have identity := mixed_relay_component_identity actual auxiliary chosen relay neutral incidence
  rw [physicalEnds] at identity
  simp only [signed, sign] at identity
  omega

theorem coherent_component_has_zero_boundary (actual auxiliary : List Edge)
    (chosen relay : List Kind) (neutral : Neutral actual)
    (incidence : List.Perm (ends auxiliary ++ relay) (ends actual ++ chosen))
    (noPositive : positive auxiliary = 0) (noNegative : negative auxiliary = 0) :
    signed (chosen ++ relay.map flip) = 0 := by
  have identity := mixed_relay_component_identity actual auxiliary chosen relay neutral incidence
  omega

theorem general_component_endpoint_identity (actual auxiliary : List Edge)
    (chosen relay : List Kind)
    (incidence : List.Perm (ends auxiliary ++ relay) (ends actual ++ chosen)) :
    2*(((positive auxiliary : Int)-(negative auxiliary : Int))-
      ((positive actual : Int)-(negative actual : Int))) =
      signed (chosen ++ relay.map flip) := by
  have partition := permutation_signed incidence
  have actualSum := signed_auxiliary_edge_count actual
  have auxiliarySum := signed_auxiliary_edge_count auxiliary
  rw [signed_append, signed_append] at partition
  rw [signed_append, signed_flip]
  omega

theorem alpha_has_marker_or_negative_auxiliary_edge (actual auxiliary : List Edge)
    (chosen relay : List Kind)
    (incidence : List.Perm (ends auxiliary ++ relay) (ends actual ++ chosen))
    (physicalEnds : chosen ++ relay.map flip = [.minus, .minus]) :
    1 ≤ positive actual + negative auxiliary := by
  have identity := general_component_endpoint_identity actual auxiliary chosen relay incidence
  rw [physicalEnds] at identity
  simp only [signed, sign] at identity
  omega

theorem coherent_alpha_has_actual_marker (actual auxiliary : List Edge)
    (chosen relay : List Kind)
    (incidence : List.Perm (ends auxiliary ++ relay) (ends actual ++ chosen))
    (physicalEnds : chosen ++ relay.map flip = [.minus, .minus])
    (noNegative : negative auxiliary = 0) :
    1 ≤ positive actual := by
  have witness := alpha_has_marker_or_negative_auxiliary_edge actual auxiliary chosen relay
    incidence physicalEnds
  omega

theorem full_domain_component_identity (actual auxiliary : List Edge)
    (free : List Kind)
    (incidence : List.Perm (ends auxiliary ++ free) (ends actual)) :
    2*(((positive auxiliary : Int)-(negative auxiliary : Int))-
      ((positive actual : Int)-(negative actual : Int))) = -signed free := by
  have partition := permutation_signed incidence
  have actualSum := signed_auxiliary_edge_count actual
  have auxiliarySum := signed_auxiliary_edge_count auxiliary
  rw [signed_append] at partition
  omega

theorem full_domain_alpha_has_marker_or_error (actual auxiliary : List Edge)
    (free : List Kind)
    (incidence : List.Perm (ends auxiliary ++ free) (ends actual))
    (physicalEnds : free.map flip = [.minus, .minus]) :
    1 ≤ positive actual + negative auxiliary := by
  have identity := full_domain_component_identity actual auxiliary free incidence
  have reversal := signed_flip free
  rw [physicalEnds] at reversal
  simp only [signed, sign] at reversal
  omega

theorem full_domain_coherent_alpha_marker (actual auxiliary : List Edge)
    (free : List Kind)
    (incidence : List.Perm (ends auxiliary ++ free) (ends actual))
    (physicalEnds : free.map flip = [.minus, .minus])
    (noNegative : negative auxiliary = 0) :
    1 ≤ positive actual := by
  have witness := full_domain_alpha_has_marker_or_error actual auxiliary free incidence physicalEnds
  omega

end SubQuorum.MixedRelayEndpointAccounting

#print axioms SubQuorum.MixedRelayEndpointAccounting.neutral_actual_endpoint_sum
#print axioms SubQuorum.MixedRelayEndpointAccounting.signed_auxiliary_edge_count
#print axioms SubQuorum.MixedRelayEndpointAccounting.mixed_relay_component_identity
#print axioms SubQuorum.MixedRelayEndpointAccounting.alpha_requires_negative_edge
#print axioms SubQuorum.MixedRelayEndpointAccounting.beta_requires_positive_edge
#print axioms SubQuorum.MixedRelayEndpointAccounting.coherent_component_has_zero_boundary
#print axioms SubQuorum.MixedRelayEndpointAccounting.general_component_endpoint_identity
#print axioms SubQuorum.MixedRelayEndpointAccounting.alpha_has_marker_or_negative_auxiliary_edge
#print axioms SubQuorum.MixedRelayEndpointAccounting.coherent_alpha_has_actual_marker
#print axioms SubQuorum.MixedRelayEndpointAccounting.full_domain_component_identity
#print axioms SubQuorum.MixedRelayEndpointAccounting.full_domain_alpha_has_marker_or_error
#print axioms SubQuorum.MixedRelayEndpointAccounting.full_domain_coherent_alpha_marker
