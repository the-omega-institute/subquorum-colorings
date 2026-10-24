import Mathlib.Data.Fintype.EquivFin
import Mathlib.Data.Finset.Card
import Mathlib.Tactic

set_option autoImplicit false
set_option backward.isDefEq.respectTransparency false

namespace SubQuorum.EndpointCompensation

structure Network (Vertex Component : Type*) where
  color : Vertex → Bool
  component : Vertex → Component
  physical : Vertex → Vertex
  physical_involutive : Function.Involutive physical
  physical_color : ∀ vertex, color (physical vertex) = !(color vertex)
  physical_component : ∀ vertex, component (physical vertex) = component vertex
  auxiliary : Vertex → Vertex
  auxiliary_involutive : Function.Involutive auxiliary
  auxiliary_color : ∀ vertex, auxiliary vertex ≠ vertex →
    color (auxiliary vertex) = !(color vertex)
  auxiliary_component : ∀ vertex, component (auxiliary vertex) = component vertex
  isDemand : Vertex → Prop

variable {Vertex Component : Type*} [Fintype Vertex]
  (network : Network Vertex Component)

noncomputable def colored (color : Bool) (component : Component) : Finset Vertex := by
  classical
  exact Finset.univ.filter (fun vertex => network.color vertex = color ∧
    network.component vertex = component)

noncomputable def paired (color : Bool) (component : Component) : Finset Vertex := by
  classical
  exact (colored network color component).filter (fun vertex => network.auxiliary vertex ≠ vertex)

noncomputable def terminals (color : Bool) (component : Component) : Finset Vertex := by
  classical
  exact (colored network color component).filter (fun vertex => network.auxiliary vertex = vertex)

noncomputable def demands (color : Bool) (component : Component) : Finset Vertex := by
  classical
  exact (terminals network color component).filter network.isDemand

noncomputable def supplies (color : Bool) (component : Component) : Finset Vertex := by
  classical
  exact (terminals network color component).filter (fun vertex => ¬network.isDemand vertex)

theorem mem_colored (color : Bool) (component : Component) (vertex : Vertex) :
    vertex ∈ colored network color component ↔
      network.color vertex = color ∧ network.component vertex = component := by
  classical
  simp [colored]

theorem mem_paired (color : Bool) (component : Component) (vertex : Vertex) :
    vertex ∈ paired network color component ↔
      network.color vertex = color ∧ network.component vertex = component ∧
        network.auxiliary vertex ≠ vertex := by
  classical
  simp [paired, mem_colored, and_assoc]

theorem mem_demands (color : Bool) (component : Component) (vertex : Vertex) :
    vertex ∈ demands network color component ↔
      network.color vertex = color ∧ network.component vertex = component ∧
        network.auxiliary vertex = vertex ∧ network.isDemand vertex := by
  classical
  simp [demands, terminals, mem_colored, and_assoc]

theorem mem_supplies (color : Bool) (component : Component) (vertex : Vertex) :
    vertex ∈ supplies network color component ↔
      network.color vertex = color ∧ network.component vertex = component ∧
        network.auxiliary vertex = vertex ∧ ¬network.isDemand vertex := by
  classical
  simp [supplies, terminals, mem_colored, and_assoc]

theorem physical_color_balance (component : Component) :
    (colored network false component).card = (colored network true component).card := by
  classical
  apply Finset.card_equiv (network.physical_involutive.toPerm network.physical)
  intro vertex
  simp only [Function.Involutive.coe_toPerm, mem_colored,
    network.physical_color, network.physical_component]
  cases network.color vertex <;> simp

theorem auxiliary_maps (color : Bool) (component : Component) (vertex : Vertex)
    (hvertex : vertex ∈ paired network color component) :
    network.auxiliary vertex ∈ paired network (!color) component := by
  rw [mem_paired] at hvertex ⊢
  refine ⟨?_, ?_, ?_⟩
  · rw [network.auxiliary_color vertex hvertex.2.2, hvertex.1]
  · rw [network.auxiliary_component, hvertex.2.1]
  · rw [network.auxiliary_involutive vertex]
    exact Ne.symm hvertex.2.2

theorem auxiliary_color_balance (component : Component) :
    (paired network false component).card = (paired network true component).card := by
  classical
  refine Finset.card_bij (fun vertex _ => network.auxiliary vertex) ?_ ?_ ?_
  · intro vertex hvertex
    exact auxiliary_maps network false component vertex hvertex
  · intro first _ second _ hequal
    exact network.auxiliary_involutive.injective hequal
  · intro vertex hvertex
    refine ⟨network.auxiliary vertex, ?_, network.auxiliary_involutive vertex⟩
    simpa using auxiliary_maps network true component vertex hvertex

theorem paired_terminal_partition (color : Bool) (component : Component) :
    (paired network color component).card + (terminals network color component).card =
      (colored network color component).card := by
  classical
  simpa only [paired, terminals, not_not] using
    Finset.card_filter_add_card_filter_not (s := colored network color component)
      (fun vertex => network.auxiliary vertex ≠ vertex)

theorem terminal_color_balance (component : Component) :
    (terminals network false component).card = (terminals network true component).card := by
  have hphysical := physical_color_balance network component
  have hauxiliary := auxiliary_color_balance network component
  have hblack := paired_terminal_partition network false component
  have hwhite := paired_terminal_partition network true component
  omega

theorem demand_supply_partition (color : Bool) (component : Component) :
    (demands network color component).card + (supplies network color component).card =
      (terminals network color component).card := by
  classical
  exact Finset.card_filter_add_card_filter_not network.isDemand

def MonochromaticDemands (component : Component) : Prop :=
  ∀ first second, network.component first = component → network.component second = component →
    network.auxiliary first = first → network.auxiliary second = second →
    network.isDemand first → network.isDemand second → network.color first = network.color second

theorem monochromatic_one_side_empty (component : Component)
    (hmono : MonochromaticDemands network component) :
    demands network false component = ∅ ∨ demands network true component = ∅ := by
  classical
  by_cases hblack : demands network false component = ∅
  · exact Or.inl hblack
  · right
    obtain ⟨first, hfirst⟩ := Finset.nonempty_iff_ne_empty.mpr hblack
    rw [mem_demands] at hfirst
    apply Finset.eq_empty_iff_forall_notMem.mpr
    intro second hsecond
    rw [mem_demands] at hsecond
    have hequal := hmono first second hfirst.2.1 hsecond.2.1 hfirst.2.2.1
      hsecond.2.2.1 hfirst.2.2.2 hsecond.2.2.2
    rw [hfirst.1, hsecond.1] at hequal
    cases hequal

theorem one_color_compensation (component : Component)
    (hmono : MonochromaticDemands network component) :
    (demands network false component).card ≤ (supplies network true component).card ∧
      (demands network true component).card ≤ (supplies network false component).card := by
  have hbalance := terminal_color_balance network component
  have hblack := demand_supply_partition network false component
  have hwhite := demand_supply_partition network true component
  have hcounts : (demands network false component).card + (supplies network false component).card =
      (demands network true component).card + (supplies network true component).card :=
    hblack.trans (hbalance.trans hwhite.symm)
  obtain hempty | hempty := monochromatic_one_side_empty network component hmono
  · have hzero := congrArg Finset.card hempty
    simp only [Finset.card_empty] at hzero
    constructor <;> omega
  · have hzero := congrArg Finset.card hempty
    simp only [Finset.card_empty] at hzero
    constructor <;> omega

theorem one_color_injective_compensation (component : Component)
    (hmono : MonochromaticDemands network component) :
    Nonempty ((demands network false component) ↪ (supplies network true component)) ∧
      Nonempty ((demands network true component) ↪ (supplies network false component)) := by
  classical
  obtain ⟨hblack, hwhite⟩ := one_color_compensation network component hmono
  constructor
  · apply Function.Embedding.nonempty_of_card_le
    simpa using hblack
  · apply Function.Embedding.nonempty_of_card_le
    simpa using hwhite

theorem one_color_embedding (color : Bool) (component : Component)
    (hmono : MonochromaticDemands network component) :
    Nonempty ((demands network color component) ↪ (supplies network (!color) component)) := by
  cases color
  · exact (one_color_injective_compensation network component hmono).1
  · exact (one_color_injective_compensation network component hmono).2

abbrev DemandVertex := {vertex : Vertex // network.auxiliary vertex = vertex ∧ network.isDemand vertex}

abbrev SupplyVertex := {vertex : Vertex // network.auxiliary vertex = vertex ∧ ¬network.isDemand vertex}

noncomputable def componentAllocation
    (hmono : ∀ component, MonochromaticDemands network component)
    (color : Bool) (component : Component) :
    (demands network color component) ↪ (supplies network (!color) component) :=
  Classical.choice (one_color_embedding network color component (hmono component))

noncomputable def allocation
    (hmono : ∀ component, MonochromaticDemands network component)
    (vertex : DemandVertex network) : SupplyVertex network := by
  classical
  let source : demands network (network.color vertex.val) (network.component vertex.val) :=
    ⟨vertex.val, (mem_demands network _ _ _).mpr ⟨rfl, rfl, vertex.property⟩⟩
  let target := componentAllocation network hmono _ _ source
  have htarget := (mem_supplies network _ _ _).mp target.property
  exact ⟨target.val, htarget.2.2⟩

theorem allocation_component
    (hmono : ∀ component, MonochromaticDemands network component)
    (vertex : DemandVertex network) :
    network.component (allocation network hmono vertex).val = network.component vertex.val := by
  classical
  exact ((mem_supplies network _ _ _).mp
    (componentAllocation network hmono _ _
      ⟨vertex.val, (mem_demands network _ _ _).mpr ⟨rfl, rfl, vertex.property⟩⟩).property).2.1

theorem allocation_color
    (hmono : ∀ component, MonochromaticDemands network component)
    (vertex : DemandVertex network) :
    network.color (allocation network hmono vertex).val = !(network.color vertex.val) := by
  classical
  exact ((mem_supplies network _ _ _).mp
    (componentAllocation network hmono _ _
      ⟨vertex.val, (mem_demands network _ _ _).mpr ⟨rfl, rfl, vertex.property⟩⟩).property).1

theorem componentAllocation_injective_values
    (hmono : ∀ component, MonochromaticDemands network component)
    (firstColor secondColor : Bool) (firstComponent secondComponent : Component)
    (hcolor : firstColor = secondColor) (hcomponent : firstComponent = secondComponent)
    (first : demands network firstColor firstComponent)
    (second : demands network secondColor secondComponent)
    (hequal : (componentAllocation network hmono firstColor firstComponent first).val =
      (componentAllocation network hmono secondColor secondComponent second).val) :
    first.val = second.val := by
  subst secondColor
  subst secondComponent
  have htargets := Subtype.ext hequal
  have hsources := (componentAllocation network hmono firstColor firstComponent).injective htargets
  exact congrArg (fun vertex : demands network firstColor firstComponent => vertex.val) hsources

theorem allocation_injective
    (hmono : ∀ component, MonochromaticDemands network component) :
    Function.Injective (allocation network hmono) := by
  classical
  intro first second hequal
  have hvertices := congrArg Subtype.val hequal
  have hcomponent : network.component first.val = network.component second.val := by
    rw [← allocation_component network hmono first, ← allocation_component network hmono second]
    exact congrArg network.component hvertices
  have hcolor : network.color first.val = network.color second.val := by
    have hflipped : (!(network.color first.val)) = (!(network.color second.val)) := by
      rw [← allocation_color network hmono first, ← allocation_color network hmono second]
      exact congrArg network.color hvertices
    simpa using congrArg Bool.not hflipped
  apply Subtype.ext
  exact componentAllocation_injective_values network hmono _ _ _ _ hcolor hcomponent
    ⟨first.val, (mem_demands network _ _ _).mpr ⟨rfl, rfl, first.property⟩⟩
    ⟨second.val, (mem_demands network _ _ _).mpr ⟨rfl, rfl, second.property⟩⟩ hvertices

#print axioms terminal_color_balance
#print axioms one_color_injective_compensation
#print axioms allocation_injective

end SubQuorum.EndpointCompensation
