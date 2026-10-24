import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.FrozenBetaForkEscape

def outRow (r : Int) : Int := if r%2=0 then r-1 else r+1

theorem outRow_involutive (r : Int) : outRow (outRow r)=r := by
  unfold outRow
  split <;> split <;> omega

theorem outRow_ne (r : Int) : outRow r≠r := by
  unfold outRow
  split <;> omega

theorem outRow_injective (r s : Int) (h : outRow r=outRow s) : r=s := by
  have twice := congrArg outRow h
  simpa only [outRow_involutive] using twice

def twoOfThree (x y z : Prop) : Prop := (x ∧ y) ∨ (x ∧ z) ∨ (y ∧ z)

/-- The geometric adapter identifies the three nonmate candidates of the
alpha mate. The beta's opposite-end dependency prevents its mate being kept,
so BOTH the escape and inward-band neighbor must be kept. -/
theorem strict_escape_dependency (alphaMate beta escapeMate inwardMate : Nat)
    (betaRequires : alphaMate<beta)
    (twoWitnesses : twoOfThree (beta<alphaMate) (escapeMate<alphaMate)
      (inwardMate<alphaMate)) :
    escapeMate<alphaMate ∧ inwardMate<alphaMate ∧ alphaMate<beta := by
  rcases twoWitnesses with h | h | h <;> rcases h with ⟨h₁,h₂⟩ <;> omega

/-- If the outward BP were vertically matched to the escape, the escape's
retention and the BP's own two-witness rule would give opposite strict ranks.
Geometry supplies the list of available matching directions. -/
theorem vertical_outer_mate_impossible (alphaMate outerBP : Nat)
    (escapeRequires : outerBP<alphaMate) (outerRequires : alphaMate<outerBP) :
    False := by omega

abbrev Point := Int × Int

def dx (right : Bool) : Int := if right then 1 else -1

structure Motif where
  row : Int
  col : Int
  right : Bool
deriving DecidableEq

def alpha (f : Motif) : Point := (f.row,f.col)
def across (f : Motif) : Point := (outRow f.row,f.col)
def outer (f : Motif) : Point := (f.row,f.col+dx f.right)
def outward (f : Motif) : Point := (f.row,f.col+2*dx f.right)
def escape (f : Motif) : Point := (outRow f.row,f.col+dx f.right)

/-- This is an actual matching-coordinate injection, rather than a numerical
capacity assumption. Extend the grid's mate map by identity off its endpoint
set to obtain an involution on Point. The written freezing lemma supplies
vertical alpha mates and the forced outward BP mates. -/
theorem escape_injective (mate : Point → Point)
    (involution : ∀ p, mate (mate p)=p) (f g : Motif)
    (gAlphaVertical : mate (alpha g)=across g)
    (fOuterOutward : mate (outer f)=outward f)
    (same : escape f=escape g) : f=g := by
  rcases f with ⟨r,c,s⟩
  rcases g with ⟨u,d,t⟩
  have rows := congrArg Prod.fst same
  simp only [escape] at rows
  have rowEq := outRow_injective r u rows
  subst u
  have cols := congrArg Prod.snd same
  simp only [escape] at cols
  by_cases sameDir : s=t
  · subst t
    have colEq : c=d := by omega
    subst d
    rfl
  · have offset : d=c+2*dx s := by
      cases s <;> cases t <;> simp_all [dx] <;> omega
    have target : outward ⟨r,c,s⟩=alpha ⟨r,d,t⟩ := by
      simp only [outward,alpha]
      rw [offset]
    have back := involution (outer ⟨r,c,s⟩)
    rw [fOuterOutward,target,gAlphaVertical] at back
    have impossible := congrArg Prod.fst back
    simp only [across,outer] at impossible
    exact False.elim (outRow_ne r impossible)

#print axioms outRow_involutive
#print axioms outRow_ne
#print axioms outRow_injective
#print axioms strict_escape_dependency
#print axioms vertical_outer_mate_impossible
#print axioms escape_injective

end SubQuorum.FrozenBetaForkEscape
