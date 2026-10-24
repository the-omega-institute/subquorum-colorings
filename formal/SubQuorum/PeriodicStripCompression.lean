import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.PeriodicStripCompression

abbrev Point := Int × Int

def liftRow (cut row : Int) : Int :=
  if row < cut then row else row + 2

def liftPoint (cut : Int) (point : Point) : Point :=
  (liftRow cut point.1, point.2)

def occupiedDegree (occupied : Point → Bool) (point : Point) : Nat :=
  (if occupied (point.1-1, point.2) then 1 else 0) +
  (if occupied (point.1+1, point.2) then 1 else 0) +
  (if occupied (point.1, point.2-1) then 1 else 0) +
  (if occupied (point.1, point.2+1) then 1 else 0)

theorem periodic_splice_preserves_occupied_degree
    (occupied : Point → Bool) (cut : Int)
    (hfirst : ∀ column, occupied (cut-1, column) = occupied (cut+1, column))
    (hsecond : ∀ column, occupied (cut, column) = occupied (cut+2, column))
    (point : Point) :
    occupiedDegree (fun vertex => occupied (liftPoint cut vertex)) point =
      occupiedDegree occupied (liftPoint cut point) := by
  rcases point with ⟨row, column⟩
  have hprevious : occupied (liftRow cut (row-1), column) =
      occupied (liftRow cut row-1, column) := by
    by_cases hbelow : row < cut
    · have hprior : row-1 < cut := by omega
      simp [liftRow, hbelow, hprior]
    · by_cases hseam : row = cut
      · subst row
        have hprior : cut-1 < cut := by omega
        have hequal : cut+2-1 = cut+1 := by omega
        simpa [liftRow, hprior, hequal] using hfirst column
      · have hprior : ¬row-1 < cut := by omega
        have hequal : row-1+2 = row+2-1 := by omega
        simp [liftRow, hbelow, hprior, hequal]
  have hnext : occupied (liftRow cut (row+1), column) =
      occupied (liftRow cut row+1, column) := by
    by_cases hbelow : row < cut
    · by_cases hseam : row = cut-1
      · subst row
        have hprior : cut-1 < cut := by omega
        have hequal : cut-1+1 = cut := by omega
        simpa [liftRow, hprior, hequal] using (hsecond column).symm
      · have hprior : row+1 < cut := by omega
        simp [liftRow, hbelow, hprior]
    · have hprior : ¬row+1 < cut := by omega
      have hequal : row+1+2 = row+2+1 := by omega
      simp [liftRow, hbelow, hprior, hequal]
  dsimp only [occupiedDegree, liftPoint]
  simp only [hprevious, hnext]

theorem periodic_splice_preserves_selected_feasibility
    (occupied selected : Point → Bool) (cut : Int)
    (hfirst : ∀ column, occupied (cut-1, column) = occupied (cut+1, column))
    (hsecond : ∀ column, occupied (cut, column) = occupied (cut+2, column))
    (hfeasible : ∀ point, selected point = true → occupiedDegree occupied point ≤ 1) :
    ∀ point, selected (liftPoint cut point) = true →
      occupiedDegree (fun vertex => occupied (liftPoint cut vertex)) point ≤ 1 := by
  intro point hselected
  rw [periodic_splice_preserves_occupied_degree occupied cut hfirst hsecond point]
  exact hfeasible (liftPoint cut point) hselected

theorem periodic_splice_preserves_endpoint_degree
    (occupied endpoint : Point → Bool) (cut : Int)
    (hfirst : ∀ column, occupied (cut-1, column) = occupied (cut+1, column))
    (hsecond : ∀ column, occupied (cut, column) = occupied (cut+2, column))
    (hdegree : ∀ point, endpoint point = true → 3 ≤ occupiedDegree occupied point) :
    ∀ point, endpoint (liftPoint cut point) = true →
      3 ≤ occupiedDegree (fun vertex => occupied (liftPoint cut vertex)) point := by
  intro point hendpoint
  rw [periodic_splice_preserves_occupied_degree occupied cut hfirst hsecond point]
  exact hdegree (liftPoint cut point) hendpoint

end SubQuorum.PeriodicStripCompression
