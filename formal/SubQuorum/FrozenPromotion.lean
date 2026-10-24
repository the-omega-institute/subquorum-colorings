import Std

set_option autoImplicit false

namespace SubQuorum.FrozenPromotion

inductive Frozen {Vertex : Type} (adjacent : Vertex → Vertex → Prop)
    (selected : Vertex → Prop) (mate : Vertex → Vertex) : Vertex → Prop where
  | two_selected (vertex first second : Vertex)
      (hfirstAdjacent : adjacent vertex first) (hsecondAdjacent : adjacent vertex second)
      (hdistinct : first ≠ second) (hfirst : selected first) (hsecond : selected second) :
      Frozen adjacent selected mate vertex
  | selected_frozen (vertex first second : Vertex)
      (hfirstAdjacent : adjacent vertex first) (hsecondAdjacent : adjacent vertex second)
      (hdistinct : first ≠ second) (hfirst : selected first)
      (hsecond : Frozen adjacent selected mate (mate second)) :
      Frozen adjacent selected mate vertex
  | two_frozen (vertex first second : Vertex)
      (hfirstAdjacent : adjacent vertex first) (hsecondAdjacent : adjacent vertex second)
      (hdistinct : first ≠ second)
      (hfirst : Frozen adjacent selected mate (mate first))
      (hsecond : Frozen adjacent selected mate (mate second)) :
      Frozen adjacent selected mate vertex

theorem frozen_exclusion {Vertex : Type}
    (adjacent : Vertex → Vertex → Prop) (selected promoted retained : Vertex → Prop)
    (mate : Vertex → Vertex)
    (hselected : ∀ vertex, selected vertex → retained vertex)
    (hretained : ∀ vertex, ¬ promoted (mate vertex) → retained vertex)
    (hfeasible : ∀ vertex first second, promoted vertex →
      adjacent vertex first → adjacent vertex second →
      retained first → retained second → first = second)
    (vertex : Vertex) (hfrozen : Frozen adjacent selected mate vertex) :
    ¬ promoted vertex := by
  induction hfrozen with
  | two_selected vertex first second hfirstAdjacent hsecondAdjacent hdistinct hfirst hsecond =>
      intro hpromoted
      exact hdistinct (hfeasible vertex first second hpromoted hfirstAdjacent hsecondAdjacent
        (hselected first hfirst) (hselected second hsecond))
  | selected_frozen vertex first second hfirstAdjacent hsecondAdjacent hdistinct hfirst
      hsecond inductionHypothesis =>
      intro hpromoted
      exact hdistinct (hfeasible vertex first second hpromoted hfirstAdjacent hsecondAdjacent
        (hselected first hfirst) (hretained second inductionHypothesis))
  | two_frozen vertex first second hfirstAdjacent hsecondAdjacent hdistinct hfirst hsecond
      firstInductionHypothesis secondInductionHypothesis =>
      intro hpromoted
      exact hdistinct (hfeasible vertex first second hpromoted hfirstAdjacent hsecondAdjacent
        (hretained first firstInductionHypothesis) (hretained second secondInductionHypothesis))

end SubQuorum.FrozenPromotion
