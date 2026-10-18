import StarForming.CubicStability
import StarForming.DissociationCover

namespace StarForming.CubicPathAccounting

open StarForming.Regular StarForming.CubicStability
open StarForming.DissociationCover

theorem augment_isolated_pairs {Vertex : Type}
    (adjacency : Vertex → Vertex → Prop) (selection added : Vertex → Prop)
    (partner : Vertex → Vertex)
    (hsymmetric : ∀ first second, adjacency first second → adjacency second first)
    (hdissociates : Dissociates adjacency selection)
    (hisolated : ∀ vertex, added vertex → ∀ neighbor,
      selection neighbor → ¬ adjacency (partner vertex) neighbor)
    (hneighbor : ∀ vertex, added vertex → ∀ neighbor,
      selection neighbor → adjacency vertex neighbor → neighbor = partner vertex)
    (hindependent : ∀ first second, added first → added second → ¬ adjacency first second)
    (hinjective : ∀ first second, added first → added second →
      partner first = partner second → first = second) :
    Dissociates adjacency (fun vertex => selection vertex ∨ added vertex) := by
  intro center first second hcenter hfirst hsecond hfirstEdge hsecondEdge
  rcases hcenter with hcenter | hcenter
  · rcases hfirst with hfirst | hfirst
    · rcases hsecond with hsecond | hsecond
      · exact hdissociates center first second hcenter hfirst hsecond hfirstEdge hsecondEdge
      · have hequal := hneighbor second hsecond center hcenter (hsymmetric _ _ hsecondEdge)
        exact False.elim (hisolated second hsecond first hfirst (hequal ▸ hfirstEdge))
    · rcases hsecond with hsecond | hsecond
      · have hequal := hneighbor first hfirst center hcenter (hsymmetric _ _ hfirstEdge)
        exact False.elim (hisolated first hfirst second hsecond (hequal ▸ hsecondEdge))
      · apply hinjective first second hfirst hsecond
        exact (hneighbor first hfirst center hcenter (hsymmetric _ _ hfirstEdge)).symm.trans
          (hneighbor second hsecond center hcenter (hsymmetric _ _ hsecondEdge))
  · rcases hfirst with hfirst | hfirst
    · rcases hsecond with hsecond | hsecond
      · exact (hneighbor center hcenter first hfirst hfirstEdge).trans
          (hneighbor center hcenter second hsecond hsecondEdge).symm
      · exact False.elim (hindependent center second hcenter hsecond hsecondEdge)
    · exact False.elim (hindependent center first hcenter hfirst hfirstEdge)

theorem extra_leaf_failure_is_unused {Vertex : Type}
    (adjacency : Vertex → Vertex → Prop) (selection : Vertex → Prop)
    (htrianglefree : ∀ outside first second, adjacency outside first →
      adjacency outside second → adjacency first second → False)
    (witness reserved : Vertex → Vertex)
    (hfailure : ∀ owner, High adjacency selection owner →
      Failure adjacency selection owner (witness owner))
    (hreserved : ∀ owner, High adjacency selection owner →
      ¬ adjacency (witness owner) owner →
      ∀ neighbor, selection neighbor → adjacency (witness owner) neighbor →
        neighbor = reserved owner)
    (leaf support outside : Vertex) (hleaf : selection leaf) (hsupport : selection support)
    (hleafedge : adjacency leaf support) (houtsideedge : adjacency outside leaf)
    (hunique : ∀ neighbor, selection neighbor → adjacency leaf neighbor → neighbor = support)
    (hextra : leaf ≠ reserved support) :
    ∀ owner, High adjacency selection owner → outside ≠ witness owner := by
  intro owner hhigh hequal
  have hshared := shared_leaf_high_witness_has_good_support_owner adjacency selection
    htrianglefree leaf support owner outside hleaf hsupport hleafedge houtsideedge
    hunique hhigh (hequal.symm ▸ hfailure owner hhigh)
  have hnonadjacent : ¬ adjacency (witness owner) owner := hequal ▸ hshared.2
  have hsame := hreserved owner hhigh hnonadjacent leaf hleaf (hequal ▸ houtsideedge)
  exact hextra (hshared.1 ▸ hsame)

theorem endpoint_count (isolatedHigh degreeOneHigh nontrivialPaths paths extraLeaves : Nat)
    (hpaths : paths = isolatedHigh + nontrivialPaths)
    (hendpoints : degreeOneHigh = 2 * nontrivialPaths)
    (hleaves : extraLeaves = 2 * isolatedHigh + degreeOneHigh) :
    extraLeaves = 2 * paths := by
  omega

theorem high_outside_color_balance (badLeft badRight fullLeft fullRight extraLeft extraRight : Int)
    (hhigh : 2 * (badLeft + fullLeft) - extraLeft =
      2 * (badRight + fullRight) - extraRight)
    (houtside : 2 * fullLeft + badRight + extraLeft =
      2 * fullRight + badLeft + extraRight) :
    badLeft - badRight = -4 * (fullLeft - fullRight) ∧
      extraLeft - extraRight = -6 * (fullLeft - fullRight) := by
  omega

theorem at_most_two_paths_balanced
    (badLeft badRight fullLeft fullRight extraLeft extraRight : Nat)
    (hbad : (badLeft : Int) - badRight = -4 * ((fullLeft : Int) - fullRight))
    (hextra : (extraLeft : Int) - extraRight = -6 * ((fullLeft : Int) - fullRight))
    (hsmall : extraLeft + extraRight ≤ 4) :
    badLeft = badRight ∧ fullLeft = fullRight ∧ extraLeft = extraRight := by
  omega

theorem exchange_signed_debt
    (size first second isolateLeft isolateRight badLeft badRight fullLeft fullRight
      extraLeft extraRight : Int)
    (hfirst : first = size - isolateLeft - extraLeft + badLeft - badRight)
    (hsecond : second = size - isolateRight - extraRight - badLeft + badRight)
    (hhigh : 2 * (badLeft + fullLeft) - extraLeft =
      2 * (badRight + fullRight) - extraRight) :
    first - second = -(isolateLeft - isolateRight + 2 * (fullLeft - fullRight)) := by
  omega

theorem signed_debt_lower_bound (first second beta debt slack : Int)
    (hfirst : first ≤ beta) (hsecond : second ≤ beta)
    (hdifference : first - second = -debt)
    (hslack : slack = 2 * beta - first - second) :
    debt ≤ slack ∧ -debt ≤ slack := by
  omega

theorem zero_slack_forces_debt_balance (first second beta debt : Int)
    (hfirst : first ≤ beta) (hsecond : second ≤ beta)
    (hdifference : first - second = -debt)
    (hslack : 2 * beta - first - second = 0) :
    debt = 0 ∧ first = beta ∧ second = beta := by
  omega

theorem equality_gap (order size beta isolates paths : Int)
    (hcapacity : 3 * order - 5 * size = isolates + 2 * paths)
    (hequality : 7 * size = 3 * order + 2 * beta) :
    2 * (size - beta) = isolates + 2 * paths := by
  omega

theorem augmented_isolate_compensation (size first second beta isolates : Nat)
    (hsum : 2 * size = first + second + isolates)
    (hfirst : first ≤ beta) (hsecond : second ≤ beta) :
    2 * size ≤ 2 * beta + isolates := by
  omega

theorem augmented_capacity_lower_bound (capacity size beta isolates first second : Int)
    (hsum : first + second = 2 * size - isolates)
    (hfirst : first ≤ beta) (hsecond : second ≤ beta) :
    capacity - isolates ≤ capacity + 2 * beta - 2 * size := by
  omega

theorem augmented_path_slack (order size beta isolates paths first second : Int)
    (hcapacity : 3 * order - 5 * size = isolates + 2 * paths)
    (hsum : first + second = 2 * size - isolates)
    (hfirst : first ≤ beta) (hsecond : second ≤ beta) :
    2 * paths ≤ 3 * order + 2 * beta - 7 * size := by
  omega

end StarForming.CubicPathAccounting
