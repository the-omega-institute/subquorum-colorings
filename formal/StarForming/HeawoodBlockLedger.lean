import Std

namespace StarForming.HeawoodBlockLedger

structure Credit where
  isolates : Nat
  unused : Nat
  coreIsolates : Nat

def credits : List Credit → Nat
  | [] => 0
  | entry :: rest => entry.isolates + entry.unused + entry.coreIsolates + credits rest

theorem local_block_credit
    (size deficit isolates unused exports imports selectedPorts selectedCore coreIsolates : Int)
    (hsize : size + deficit = 8)
    (hidentity : unused + exports - imports =
      42 - 5 * size - isolates + selectedPorts - selectedCore)
    (hflux : exports - imports + selectedCore - selectedPorts ≤
      5 * deficit + coreIsolates) :
    2 ≤ isolates + unused + coreIsolates := by
  omega

theorem sum_block_credit (ledger : List Credit)
    (hcredit : ∀ entry, entry ∈ ledger → 2 ≤ entry.isolates + entry.unused + entry.coreIsolates) :
    2 * ledger.length ≤ credits ledger := by
  induction ledger with
  | nil => simp [credits]
  | cons entry rest inductionHypothesis =>
    have hhead := hcredit entry (by simp)
    have htail : ∀ other, other ∈ rest →
        2 ≤ other.isolates + other.unused + other.coreIsolates := by
      intro other hmember
      exact hcredit other (by simp [hmember])
    have hbound := inductionHypothesis htail
    change 2 * (rest.length + 1) ≤
      entry.isolates + entry.unused + entry.coreIsolates + credits rest
    omega

theorem global_block_cap (order size isolates unused blockCredits blocks : Nat)
    (hidentity : 5 * size + isolates + unused = 3 * order)
    (hlocal : 2 * blocks ≤ blockCredits)
    (hnoreuse : blockCredits ≤ isolates + unused) :
    5 * size + 2 * blocks ≤ 3 * order := by
  omega

theorem long_core_upper (copies size : Nat)
    (hcapacity : 5 * size + 6 * copies ≤ 186 * copies) :
    size ≤ 36 * copies := by
  omega

end StarForming.HeawoodBlockLedger
