import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.FrozenSelectionFrontier

/-- At a leaf with only two permissible selected witnesses, a strict freezing
witness forces both. The coordinate adapter excludes the third nonmate site
because it has two fixed P neighbours. -/
theorem leaf_forces_seals (Site : Type) (T : Site → Prop) (u v : Site)
    (witnesses : ∃ a b, a ≠ b ∧ T a ∧ T b ∧ (a = u ∨ a = v) ∧ (b = u ∨ b = v)) :
    T u ∧ T v := by
  obtain ⟨a,b,hab,ha,hb,haUV,hbUV⟩ := witnesses
  rcases haUV with rfl | rfl <;> rcases hbUV with rfl | rfl
  · exact False.elim (hab rfl)
  · exact ⟨ha,hb⟩
  · exact ⟨hb,ha⟩
  · exact False.elim (hab rfl)

def missing (x y : Bool) : Nat := (if x then 0 else 1) + (if y then 0 else 1)
def alpha (x y : Bool) : Nat := if x && y then 1 else 0
def beta (x y : Bool) : Nat := if !x && !y then 1 else 0

theorem central_identity (x y : Bool) : missing x y + alpha x y = 1 + beta x y := by
  cases x <;> cases y <;> decide

def sumMissing (xs : List (Bool × Bool)) : Nat :=
  (xs.map (fun p => missing p.1 p.2)).sum
def sumAlpha (xs : List (Bool × Bool)) : Nat :=
  (xs.map (fun p => alpha p.1 p.2)).sum
def sumBeta (xs : List (Bool × Bool)) : Nat :=
  (xs.map (fun p => beta p.1 p.2)).sum

/-- The exact central-source identity for arbitrarily many modules. -/
theorem central_list_identity (xs : List (Bool × Bool)) :
    sumMissing xs + sumAlpha xs = xs.length + sumBeta xs := by
  induction xs with
  | nil => rfl
  | cons p xs ih =>
      have h := central_identity p.1 p.2
      simp only [sumMissing, sumAlpha, sumBeta, List.map_cons, List.sum_cons,
        List.length_cons] at *
      omega

/-- Physical cover members are disjoint; unused member losses are nonnegative.
The geometric adapter supplies the three charged sums, never one twice. -/
theorem disjoint_loss_budget (ell missingTips terminalBeta terminalUnits rest : Nat)
    (partition : ell = missingTips + terminalBeta + terminalUnits + rest) :
    missingTips + terminalBeta + terminalUnits ≤ ell := by omega

/-- The two independently established injections, into disjoint cap losses
and into capacity-one whole-beta/interval sinks, imply the strengthened bound. -/
theorem coupled_frontier (ell a v k b missingTips terminalBeta terminalUnits : Int)
    (central : missingTips + a = k + b)
    (coverBudget : missingTips + terminalBeta + terminalUnits ≤ ell)
    (paymentBudget : v ≤ terminalBeta + terminalUnits) :
    k + b ≤ ell + (a-v) := by omega

theorem slack_frontier (S ell D k b : Int) (slack : S = 2*k+ell)
    (coupled : k+b ≤ ell+D) : 3*k+b ≤ S+D := by omega

/-- Arbitrary deletions, additions and replacements are all included: this
uses only the final T, not a retained subset of the original maximizer. -/
theorem repair_net_loss (tau size D k b : Int) (bNonnegative : 0 ≤ b)
    (coupled : k+b ≤ (tau-size)+D) (repaired : D=0) : size ≤ tau-k := by omega

theorem pareto_upper (tau size D d k b : Int) (bNonnegative : 0 ≤ b)
    (coupled : k+b ≤ (tau-size)+D) (threshold : D ≤ d) :
    size ≤ tau-k+d := by omega

/-- At a sealed true maximum, alpha count and unpaid demand both equal k. -/
theorem every_maximum (ell D a v k b missingTips terminalBeta terminalUnits : Int)
    (maximal : ell=0) (vNonnegative : 0≤v) (bNonnegative : 0≤b)
    (missingNonnegative : 0≤missingTips) (central : missingTips+a=k+b)
    (aAtMost : a≤k) (definition : D=a-v)
    (coverBudget : missingTips+terminalBeta+terminalUnits≤ell)
    (paymentBudget : v≤terminalBeta+terminalUnits) :
    D=k ∧ a=k ∧ b=0 ∧ v=0 := by omega

/-- k-d distinct private lower beta sinks give equality, with all sources
retained; the common strict freezing schedule is checked geometrically. -/
theorem sharp_attainer (tau k d : Int) :
    let size := tau-(k-d)
    let a := k
    let v := k-d
    size=tau-k+d ∧ a-v=d ∧ (tau-size)+(a-v)=k := by omega

/-- Combine a proved upper bound with a supplied geometric attainer. -/
theorem exact_frontier (Feasible : Int → Int → Prop) (tau k d : Int)
    (upper : ∀ size deficit, Feasible size deficit → deficit≤d → size≤tau-k+d)
    (attaining : Feasible (tau-k+d) d) :
    Feasible (tau-k+d) d ∧ ∀ size deficit,
      Feasible size deficit → deficit≤d → size≤tau-k+d := ⟨attaining,upper⟩

/-- Fixing both central alpha and beta counts gives the complete inventory
frontier, including thresholds above the number of available sources. -/
theorem inventory_upper (tau size D d a v k b missingTips terminalBeta terminalUnits : Int)
    (central : missingTips+a=k+b) (definition : D=a-v)
    (vNonnegative : 0≤v) (threshold : D≤d)
    (coverBudget : missingTips+terminalBeta+terminalUnits≤tau-size)
    (paymentBudget : v≤terminalBeta+terminalUnits) :
    size≤tau-k-b+min a d := by omega

/-- Remove missing central partners, then open one distinct private beta for
exactly max(0,a-d) retained sources. This attains the inventory bound. -/
theorem inventory_attainer (tau k a b d : Int)
    (aNonnegative : 0≤a) (dNonnegative : 0≤d) :
    let paid := max 0 (a-d)
    let size := tau-(k-a+b)-paid
    let D := a-paid
    0≤paid ∧ paid≤a ∧ D=min a d ∧ D≤d ∧ size=tau-k-b+min a d := by omega

/-- Without any seals, source-tile and gap losses have explicit corrections.
The missing outer3 partners equal occupied outer4 sites plus left beta count. -/
theorem unsealed_coupling (ell D a v k b missingTips outer4 leftBeta rightBeta units empty2 missingOuter3 : Int)
    (central : missingTips+a=k+b) (definition : D=a-v)
    (boundaryIdentity : outer4+leftBeta=missingOuter3)
    (coverBudget : missingTips-outer4+rightBeta+units-empty2≤ell)
    (paymentBudget : v≤leftBeta+rightBeta+units) :
    k+b≤ell+D+(missingOuter3+empty2) := by omega

/-- Per specified leaf, the exact boundary defect is0 iff frozen and otherwise
is1 or2. The coordinate/first-freezing-time adapter supplies this inequality. -/
theorem unfrozen_leaf_budget (ell D E U k b : Int)
    (corrected : k+b≤ell+D+E) (defectBound : E≤2*U) :
    k+b≤ell+D+2*U := by omega

theorem same_size_repair_unfreezes_leaves (ell D E U k b : Int)
    (sameSize : ell=0) (complete : D=0)
    (corrected : k+b≤ell+D+E) (defectBound : E≤2*U) :
    k+b≤2*U := by omega

/-- Arbitrarily long owner walks; the coordinate adapter supplies the actual
standard TP-to-BP links and their module labels. -/
inductive Walk {Node : Type} (Edge : Node → Node → Prop) : Node → Node → Prop
  | refl (v : Node) : Walk Edge v v
  | step {a b c : Node} : Walk Edge a b → Edge b c → Walk Edge a c

/-- An all-length route invariant, independent of the number of owners. -/
theorem walk_preserves_module (Node : Type) (Edge : Node → Node → Prop)
    (moduleId : Node → Nat) (sameModule : ∀ u v, Edge u v → moduleId u=moduleId v)
    (a b : Node) (walk : Walk Edge a b) : moduleId a=moduleId b := by
  induction walk with
  | refl => rfl
  | step _ edge ih => exact ih.trans (sameModule _ _ edge)

/-- A module has only one central body, so a route from its central source
cannot arrive at a different central body. -/
theorem reached_central_is_source (Node : Type) (Edge : Node → Node → Prop)
    (moduleId : Node → Nat) (Central : Node → Prop)
    (sameModule : ∀ u v, Edge u v → moduleId u=moduleId v)
    (uniqueCentral : ∀ u v, Central u → Central v → moduleId u=moduleId v → u=v)
    (a b : Node) (sourceCentral : Central a) (targetCentral : Central b)
    (walk : Walk Edge a b) : a=b := by
  exact uniqueCentral a b sourceCentral targetCentral
    (walk_preserves_module Node Edge moduleId sameModule a b walk)

/-- The central beta credit is not a sink for any central alpha source;
whole-beta/interval sink counting therefore needs only terminal bodies. -/
theorem central_beta_unreachable (Node : Type) (Edge : Node → Node → Prop)
    (moduleId : Node → Nat) (Central Alpha Beta : Node → Prop)
    (sameModule : ∀ u v, Edge u v → moduleId u=moduleId v)
    (uniqueCentral : ∀ u v, Central u → Central v → moduleId u=moduleId v → u=v)
    (disjoint : ∀ v, Alpha v → Beta v → False)
    (a b : Node) (sourceCentral : Central a) (targetCentral : Central b)
    (sourceAlpha : Alpha a) (targetBeta : Beta b) : ¬ Walk Edge a b := by
  intro walk
  have equal := reached_central_is_source Node Edge moduleId Central sameModule
    uniqueCentral a b sourceCentral targetCentral walk
  exact disjoint b (equal ▸ sourceAlpha) targetBeta

end SubQuorum.FrozenSelectionFrontier

#print axioms SubQuorum.FrozenSelectionFrontier.leaf_forces_seals
#print axioms SubQuorum.FrozenSelectionFrontier.central_identity
#print axioms SubQuorum.FrozenSelectionFrontier.central_list_identity
#print axioms SubQuorum.FrozenSelectionFrontier.disjoint_loss_budget
#print axioms SubQuorum.FrozenSelectionFrontier.coupled_frontier
#print axioms SubQuorum.FrozenSelectionFrontier.slack_frontier
#print axioms SubQuorum.FrozenSelectionFrontier.repair_net_loss
#print axioms SubQuorum.FrozenSelectionFrontier.pareto_upper
#print axioms SubQuorum.FrozenSelectionFrontier.every_maximum
#print axioms SubQuorum.FrozenSelectionFrontier.sharp_attainer
#print axioms SubQuorum.FrozenSelectionFrontier.exact_frontier

#print axioms SubQuorum.FrozenSelectionFrontier.inventory_upper
#print axioms SubQuorum.FrozenSelectionFrontier.inventory_attainer

#print axioms SubQuorum.FrozenSelectionFrontier.unsealed_coupling
#print axioms SubQuorum.FrozenSelectionFrontier.unfrozen_leaf_budget
#print axioms SubQuorum.FrozenSelectionFrontier.same_size_repair_unfreezes_leaves

#print axioms SubQuorum.FrozenSelectionFrontier.walk_preserves_module
#print axioms SubQuorum.FrozenSelectionFrontier.reached_central_is_source
#print axioms SubQuorum.FrozenSelectionFrontier.central_beta_unreachable
