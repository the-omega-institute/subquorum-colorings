import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 16384
set_option maxHeartbeats 0

namespace SubQuorum.UnprotectedWhitePair

inductive Site where
  | r | s | d | e | g | h
  deriving DecidableEq

/-- A projection of a feasible actual matching near the two boundary white
    sites. Black sites may have mates outside this six-site projection; only
    the two white mate values are used. Selected white sites are allowed. -/
structure LocalModel where
  T : Site → Prop
  O : Site → Prop
  mate : Site → Site
  selected_occupied : ∀ v, T v → O v
  r_degree : T .r → ¬(O .d ∧ O .g)
  s_degree : T .s → ¬(O .e ∧ O .h)
  g_degree : T .g → ¬(O .r ∧ O .s)
  r_mate : O .r → ¬T .r →
    (mate .r=.d ∨ mate .r=.g) ∧ ¬T (mate .r)
  s_mate : O .s → ¬T .s →
    (mate .s=.e ∨ mate .s=.g ∨ mate .s=.h) ∧ ¬T (mate .s)
  mate_occupied : ∀ v, (v=.r ∨ v=.s) → O v → ¬T v → O (mate v)
  distinct_mates : O .r → ¬T .r → O .s → ¬T .s → mate .r ≠ mate .s

/-- When both white sites are occupied, selecting their common black neighbour
    violates its degree condition, regardless of the white site types. -/
theorem common_neighbour_not_selected (L : LocalModel)
    (hr : L.O .r) (hs : L.O .s) : ¬L.T .g := by
  intro ht
  exact L.g_degree ht ⟨hr,hs⟩

/-- This is the missing joint obstruction when white selections are allowed:
    d,e,h cannot all be selected while both white sites are occupied. -/
theorem three_private_neighbours_not_all_selected (L : LocalModel)
    (hr : L.O .r) (hs : L.O .s) :
    ¬(L.T .d ∧ L.T .e ∧ L.T .h) := by
  intro ⟨hd,he,hh⟩
  have ns : ¬L.T .s := by
    intro ht
    exact L.s_degree ht ⟨L.selected_occupied .e he,L.selected_occupied .h hh⟩
  obtain ⟨sm,snt⟩ := L.s_mate hs ns
  have smg : L.mate .s=.g := by
    rcases sm with sm | sm | sm
    · exact False.elim (snt (sm ▸ he))
    · exact sm
    · exact False.elim (snt (sm ▸ hh))
  have og : L.O .g := smg ▸ L.mate_occupied .s (Or.inr rfl) hs ns
  by_cases tr : L.T .r
  · exact L.r_degree tr ⟨L.selected_occupied .d hd,og⟩
  · obtain ⟨rm,rnt⟩ := L.r_mate hr tr
    have rmg : L.mate .r=.g := by
      rcases rm with rm | rm
      · exact False.elim (rnt (rm ▸ hd))
      · exact rm
    exact L.distinct_mates hr tr hs ns (rmg.trans smg.symm)

/-- With either white site occupied, selecting all four black sites is
    impossible: selected degree or the absence of an actual mate excludes it. -/
theorem occupied_white_excludes_four_selected (L : LocalModel)
    (ho : L.O .r ∨ L.O .s) :
    ¬(L.T .d ∧ L.T .e ∧ L.T .g ∧ L.T .h) := by
  intro ⟨hd,he,hg,hh⟩
  rcases ho with hr | hs
  · by_cases tr : L.T .r
    · exact L.r_degree tr ⟨L.selected_occupied .d hd,L.selected_occupied .g hg⟩
    · obtain ⟨rm,rnt⟩ := L.r_mate hr tr
      rcases rm with rm | rm
      · exact rnt (rm ▸ hd)
      · exact rnt (rm ▸ hg)
  · by_cases ts : L.T .s
    · exact L.s_degree ts ⟨L.selected_occupied .e he,L.selected_occupied .h hh⟩
    · obtain ⟨sm,snt⟩ := L.s_mate hs ts
      rcases sm with sm | sm | sm
      · exact snt (sm ▸ he)
      · exact snt (sm ▸ hg)
      · exact snt (sm ▸ hh)

noncomputable def bit (p : Prop) : Nat := by
  classical
  exact if p then 1 else 0

theorem bit_le_one (p : Prop) : bit p≤1 := by
  classical
  by_cases hp : p <;> simp [bit,hp]

/-- Full two-white-site capacity with no prohibition on selecting r or s. -/
theorem actual_capacity (L : LocalModel) :
    bit (L.T .d)+bit (L.T .e)+bit (L.T .g)+bit (L.T .h) ≤
      2+bit (¬L.O .r)+bit (¬L.O .s) := by
  classical
  have hd := bit_le_one (L.T .d)
  have he := bit_le_one (L.T .e)
  have hg := bit_le_one (L.T .g)
  have hh := bit_le_one (L.T .h)
  by_cases hr : L.O .r
  · by_cases hs : L.O .s
    · have ng := common_neighbour_not_selected L hr hs
      have hn := three_private_neighbours_not_all_selected L hr hs
      have sum3 : bit (L.T .d)+bit (L.T .e)+bit (L.T .h)≤2 := by
        by_cases td : L.T .d <;> by_cases te : L.T .e <;> by_cases th : L.T .h
        all_goals simp_all [bit]
      simp only [bit,ng,hr,hs,not_true_eq_false,ite_false]
      simpa [bit] using sum3
    · have hn := occupied_white_excludes_four_selected L (Or.inl hr)
      have sum4 : bit (L.T .d)+bit (L.T .e)+bit (L.T .g)+bit (L.T .h)≤3 := by
        by_cases td : L.T .d <;> by_cases te : L.T .e <;> by_cases tg : L.T .g <;> by_cases th : L.T .h
        all_goals simp_all [bit]
      simpa [bit,hr,hs] using sum4
  · by_cases hs : L.O .s
    · have hn := occupied_white_excludes_four_selected L (Or.inr hs)
      have sum4 : bit (L.T .d)+bit (L.T .e)+bit (L.T .g)+bit (L.T .h)≤3 := by
        by_cases td : L.T .d <;> by_cases te : L.T .e <;> by_cases tg : L.T .g <;> by_cases th : L.T .h
        all_goals simp_all [bit]
      simpa [bit,hr,hs] using sum4
    · simp only [bit,hr,hs,not_false_eq_true,ite_true]
      simpa [bit] using (show bit (L.T .d)+bit (L.T .e)+bit (L.T .g)+bit (L.T .h)≤4 by omega)

/-- Four new top black selections fit into six disjoint physical white holes. -/
theorem top_block_budget (A B C D u v w x y z : Nat)
    (_hA : A≤1) (_hB : B≤1) (_hC : C≤1) (_hD : D≤1)
    (_hu : u≤1) (_hv : v≤1) (hw : w≤1) (_hx : x≤1) (_hy : y≤1) (_hz : z≤1)
    (ha : A≤u+v) (hb : B≤u ∧ B≤w)
    (hc : 2*C≤w+x+y) (hd : 2*D≤x+y+z) :
    A+B+C+D≤u+v+w+x+y+z := by
  have hab : A+B≤u+v+w := by omega
  have hcd : C+D≤x+y+z := by omega
  omega

/-- The terminal's two distinct empty neighbours lie outside the pocket/tail
    hole set. The coordinate adapter supplies this disjoint cardinality split. -/
theorem terminal_one_unit_budget (oldSelected totalBlack baseH terminalH otherH Hw Ow J half : Nat)
    (hT : totalBlack=oldSelected+1) (hH : Hw=baseH+terminalH+otherH)
    (hbase : oldSelected≤baseH) (hterminal : 2≤terminalH)
    (hJ : J=totalBlack+Ow) (hhalf : half=Hw+Ow) : J+1≤half := by
  omega

end SubQuorum.UnprotectedWhitePair
#print axioms SubQuorum.UnprotectedWhitePair.common_neighbour_not_selected
#print axioms SubQuorum.UnprotectedWhitePair.three_private_neighbours_not_all_selected
#print axioms SubQuorum.UnprotectedWhitePair.occupied_white_excludes_four_selected
#print axioms SubQuorum.UnprotectedWhitePair.bit_le_one
#print axioms SubQuorum.UnprotectedWhitePair.actual_capacity
#print axioms SubQuorum.UnprotectedWhitePair.top_block_budget

#print axioms SubQuorum.UnprotectedWhitePair.terminal_one_unit_budget
