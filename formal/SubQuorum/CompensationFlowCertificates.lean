import Lean.Elab.Tactic.Omega
import Init.Data.List.Perm

set_option autoImplicit false

namespace SubQuorum.CompensationFlowCertificates

theorem shared_terminal_forces_same_route {Route Terminal Owner : Type}
    (owner : Terminal → Owner) (usesTerminal : Route → Terminal → Prop)
    (usesOwner : Route → Owner → Prop)
    (ownership : ∀ route terminal, usesTerminal route terminal → usesOwner route (owner terminal))
    (exclusive : ∀ first second strand, usesOwner first strand → usesOwner second strand →
      first = second)
    {first second : Route} {terminal : Terminal}
    (firstUse : usesTerminal first terminal) (secondUse : usesTerminal second terminal) :
    first = second :=
  exclusive first second (owner terminal) (ownership first terminal firstUse)
    (ownership second terminal secondUse)

theorem terminal_lists_form_matching {Terminal : Type} (routes : List (List Terminal))
    (within : ∀ terminals ∈ routes, terminals.Nodup)
    (between : routes.Pairwise (fun first second =>
      ∀ terminal ∈ first, ∀ other ∈ second, terminal ≠ other)) :
    routes.flatten.Nodup :=
  List.pairwise_flatten.mpr ⟨within, between⟩

theorem separator_certificate_injective {Route Source Obstacle : Type}
    (source : Route → Source) (obstacle : Route → Obstacle) (blocked : Route → Bool)
    (uniqueSource : Function.Injective source)
    (uniqueObstacle : ∀ first second, blocked first = true → blocked second = true →
      obstacle first = obstacle second → first = second) :
    Function.Injective (fun route =>
      if blocked route then Sum.inr (obstacle route) else Sum.inl (source route)) := by
  intro first second same
  cases firstFlag : blocked first <;> cases secondFlag : blocked second <;>
    simp [firstFlag, secondFlag] at same
  · exact uniqueSource same
  · exact uniqueObstacle first second firstFlag secondFlag same

theorem separator_count_bound {Route Source Obstacle : Type}
    (routes : List Route) (unblocked : List Source) (separator : List Obstacle)
    (certificate : Route → Sum Source Obstacle)
    (uniqueRoutes : routes.Nodup) (uniqueCertificate : Function.Injective certificate)
    (certified : ∀ route ∈ routes,
      certificate route ∈ unblocked.map Sum.inl ++ separator.map Sum.inr) :
    routes.length ≤ unblocked.length + separator.length := by
  have mappedUnique : (routes.map certificate).Nodup := by
    apply List.pairwise_map.mpr
    exact uniqueRoutes.imp (fun distinct same => distinct (uniqueCertificate same))
  have contained : routes.map certificate ⊆
      unblocked.map Sum.inl ++ separator.map Sum.inr := by
    intro value member
    obtain ⟨route, routeMember, same⟩ := List.mem_map.mp member
    rw [← same]
    exact certified route routeMember
  have bound := mappedUnique.length_le_of_subset contained
  simpa using bound

theorem protected_core_resources_stay_unique {Resource : Type}
    (core added : List Resource) (coreUnique : core.Nodup) (addedUnique : added.Nodup)
    (reserved : ∀ first ∈ core, ∀ second ∈ added, first ≠ second) :
    (core ++ added).Nodup :=
  List.nodup_append.mpr ⟨coreUnique, addedUnique, reserved⟩

theorem exact_resource_ledger (surplus boundary resources demands routed unused unpaid : Int)
    (physical : surplus - boundary = resources - demands)
    (resourceInventory : resources = routed + unused)
    (demandInventory : demands = routed + unpaid) :
    surplus - boundary = unused - unpaid := by omega

end SubQuorum.CompensationFlowCertificates

#print axioms SubQuorum.CompensationFlowCertificates.shared_terminal_forces_same_route
#print axioms SubQuorum.CompensationFlowCertificates.terminal_lists_form_matching
#print axioms SubQuorum.CompensationFlowCertificates.separator_certificate_injective
#print axioms SubQuorum.CompensationFlowCertificates.separator_count_bound
#print axioms SubQuorum.CompensationFlowCertificates.protected_core_resources_stay_unique
#print axioms SubQuorum.CompensationFlowCertificates.exact_resource_ledger
