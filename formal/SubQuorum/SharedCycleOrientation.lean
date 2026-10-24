import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SharedCycleOrientation

inductive Kind where
  | minus
  | plus
  deriving DecidableEq

structure Edge where
  left : Kind
  right : Kind

def charge : Edge → Int
  | ⟨.minus, .minus⟩ => -1
  | ⟨.plus, .plus⟩ => 1
  | _ => 0

def positive : List Edge → Nat
  | [] => 0
  | edge :: rest => (if edge.left = .plus ∧ edge.right = .plus then 1 else 0) + positive rest

def negative : List Edge → Nat
  | [] => 0
  | edge :: rest => (if edge.left = .minus ∧ edge.right = .minus then 1 else 0) + negative rest

def total : List Edge → Int
  | [] => 0
  | edge :: rest => charge edge + total rest

inductive Walk : Kind → Kind → List Edge → Prop where
  | single (left right : Kind) : Walk left right [⟨left, right⟩]
  | cons (left first second right : Kind) (rest : List Edge)
      (opposite : first ≠ second) (tail : Walk second right rest) :
      Walk left right (⟨left, first⟩ :: rest)

theorem opposite_splice (left first second right : Kind) (opposite : first ≠ second) :
    charge ⟨left, first⟩ + charge ⟨second, right⟩ = charge ⟨left, right⟩ := by
  cases left <;> cases first <;> cases second <;> cases right <;>
    simp_all [charge]

theorem walk_charge {left right : Kind} {edges : List Edge}
    (walk : Walk left right edges) : total edges = charge ⟨left, right⟩ := by
  induction walk with
  | single left right => simp [total]
  | cons left first second right rest opposite tail inductionHypothesis =>
    simp only [total, inductionHypothesis]
    exact opposite_splice left first second right opposite

theorem signed_edge_count (edges : List Edge) :
    total edges = (positive edges : Int) - (negative edges : Int) := by
  induction edges with
  | nil => simp [total, positive, negative]
  | cons edge rest inductionHypothesis =>
    obtain ⟨left, right⟩ := edge
    cases left <;> cases right <;> simp_all [total, positive, negative, charge] <;> omega

theorem route_orientation_identity {left right : Kind} {edges : List Edge}
    (walk : Walk left right edges) :
    (positive edges : Int) - (negative edges : Int) = charge ⟨left, right⟩ := by
  rw [← signed_edge_count, walk_charge walk]

theorem alpha_requires_negative_edge {edges : List Edge}
    (walk : Walk .minus .minus edges) : 1 ≤ negative edges := by
  have identity := route_orientation_identity walk
  simp only [charge] at identity
  omega

theorem beta_requires_positive_edge {edges : List Edge}
    (walk : Walk .plus .plus edges) : 1 ≤ positive edges := by
  have identity := route_orientation_identity walk
  simp only [charge] at identity
  omega

structure Route where
  left : Kind
  right : Kind
  edges : List Edge
  valid : Walk left right edges

def alphas : List Route → Nat
  | [] => 0
  | route :: rest => (if route.left = .minus ∧ route.right = .minus then 1 else 0) + alphas rest

def betas : List Route → Nat
  | [] => 0
  | route :: rest => (if route.left = .plus ∧ route.right = .plus then 1 else 0) + betas rest

def negativeBudget : List Route → Nat
  | [] => 0
  | route :: rest => negative route.edges + negativeBudget rest

def positiveBudget : List Route → Nat
  | [] => 0
  | route :: rest => positive route.edges + positiveBudget rest

theorem finite_alpha_nonreuse_bound (routes : List Route) :
    alphas routes ≤ negativeBudget routes := by
  induction routes with
  | nil => simp [alphas, negativeBudget]
  | cons route rest inductionHypothesis =>
    obtain ⟨left, right, edges, valid⟩ := route
    cases left <;> cases right <;> simp only [alphas, negativeBudget] <;>
      simp only [and_self, reduceCtorEq, and_false, false_and, ↓reduceIte] <;>
      try omega
    have witness := alpha_requires_negative_edge valid
    omega

theorem finite_beta_nonreuse_bound (routes : List Route) :
    betas routes ≤ positiveBudget routes := by
  induction routes with
  | nil => simp [betas, positiveBudget]
  | cons route rest inductionHypothesis =>
    obtain ⟨left, right, edges, valid⟩ := route
    cases left <;> cases right <;> simp only [betas, positiveBudget] <;>
      simp only [and_self, reduceCtorEq, and_false, false_and, ↓reduceIte] <;>
      try omega
    have witness := beta_requires_positive_edge valid
    omega

theorem coherent_routes_have_no_alpha (routes : List Route)
    (coherent : negativeBudget routes = 0) : alphas routes = 0 := by
  have bound := finite_alpha_nonreuse_bound routes
  omega

theorem coherent_routes_have_no_beta (routes : List Route)
    (coherent : positiveBudget routes = 0) : betas routes = 0 := by
  have bound := finite_beta_nonreuse_bound routes
  omega

theorem forest_rank_controls_residual_alpha (routes : List Route) (rank : Nat)
    (balancedErrors : positiveBudget routes = negativeBudget routes)
    (forestErrors : positiveBudget routes + negativeBudget routes ≤ rank) :
    alphas routes ≤ rank / 2 := by
  have bound := finite_alpha_nonreuse_bound routes
  omega

end SubQuorum.SharedCycleOrientation

#print axioms SubQuorum.SharedCycleOrientation.walk_charge
#print axioms SubQuorum.SharedCycleOrientation.signed_edge_count
#print axioms SubQuorum.SharedCycleOrientation.route_orientation_identity
#print axioms SubQuorum.SharedCycleOrientation.alpha_requires_negative_edge
#print axioms SubQuorum.SharedCycleOrientation.beta_requires_positive_edge
#print axioms SubQuorum.SharedCycleOrientation.finite_alpha_nonreuse_bound
#print axioms SubQuorum.SharedCycleOrientation.finite_beta_nonreuse_bound
#print axioms SubQuorum.SharedCycleOrientation.coherent_routes_have_no_alpha
#print axioms SubQuorum.SharedCycleOrientation.coherent_routes_have_no_beta
#print axioms SubQuorum.SharedCycleOrientation.forest_rank_controls_residual_alpha
