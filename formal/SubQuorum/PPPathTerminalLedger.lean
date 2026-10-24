import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.PPPathTerminalLedger

inductive PathKind where
  | tp_tp
  | bp_bp
  | tp_bp
  | tp_external
  | bp_external
  | external_external
  deriving DecidableEq

open PathKind

def tpEnds : PathKind → Int
  | tp_tp => 2
  | tp_bp | tp_external => 1
  | _ => 0

def bpEnds : PathKind → Int
  | bp_bp => 2
  | tp_bp | bp_external => 1
  | _ => 0

def externalEnds : PathKind → Int
  | external_external => 2
  | tp_external | bp_external => 1
  | _ => 0

def tally (measure : PathKind → Int) : List PathKind → Int
  | [] => 0
  | kind :: rest => measure kind + tally measure rest

def countKind (target : PathKind) : List PathKind → Int :=
  tally (fun kind => if kind = target then 1 else 0)

theorem tp_terminal_inventory (paths : List PathKind) :
    tally tpEnds paths = 2 * countKind tp_tp paths + countKind tp_bp paths +
      countKind tp_external paths := by
  induction paths with
  | nil => rfl
  | cons kind rest inductionHypothesis =>
    cases kind <;> simp_all [tally, tpEnds, countKind] <;> omega

theorem bp_terminal_inventory (paths : List PathKind) :
    tally bpEnds paths = 2 * countKind bp_bp paths + countKind tp_bp paths +
      countKind bp_external paths := by
  induction paths with
  | nil => rfl
  | cons kind rest inductionHypothesis =>
    cases kind <;> simp_all [tally, bpEnds, countKind] <;> omega

theorem external_terminal_inventory (paths : List PathKind) :
    tally externalEnds paths = 2 * countKind external_external paths +
      countKind tp_external paths + countKind bp_external paths := by
  induction paths with
  | nil => rfl
  | cons kind rest inductionHypothesis =>
    cases kind <;> simp_all [tally, externalEnds, countKind] <;> omega

theorem exact_path_debit (paths : List PathKind) :
    tally bpEnds paths - tally tpEnds paths =
      2 * (countKind bp_bp paths - countKind tp_tp paths) +
      countKind bp_external paths - countKind tp_external paths := by
  have tpInventory := tp_terminal_inventory paths
  have bpInventory := bp_terminal_inventory paths
  omega

inductive AlternatingPathSize : Nat → Nat → Prop where
  | edge : AlternatingPathSize 1 0
  | extend {matchingEdges ppColumns : Nat}
      (prior : AlternatingPathSize matchingEdges ppColumns) :
      AlternatingPathSize (matchingEdges + 1) (ppColumns + 1)

theorem arbitrary_pp_chain_size {matchingEdges ppColumns : Nat}
    (trace : AlternatingPathSize matchingEdges ppColumns) :
    matchingEdges = ppColumns + 1 := by
  induction trace with
  | edge => rfl
  | extend prior inductionHypothesis => omega

theorem exact_column_identity (columns doubleBlank doubleSelected mixed singleEndpoint
    singleSelected doubleEndpoint selected endpoints surplusTwice : Int)
    (columnCount : columns = doubleBlank + doubleSelected + mixed + singleEndpoint +
      singleSelected + doubleEndpoint)
    (selectionCount : selected = 2 * doubleSelected + mixed + singleSelected)
    (endpointCount : endpoints = mixed + singleEndpoint + 2 * doubleEndpoint)
    (surplusDefinition : surplusTwice = 2 * columns - 2 * selected - endpoints) :
    surplusTwice = 2 * (doubleBlank - doubleSelected) + singleEndpoint - mixed := by omega

theorem exact_packet_ledger (paths : List PathKind) (surplusTwice balance : Int)
    (columnIdentity : surplusTwice = 2 * balance + tally bpEnds paths - tally tpEnds paths) :
    surplusTwice = 2 * (balance + countKind bp_bp paths - countKind tp_tp paths) +
      countKind bp_external paths - countKind tp_external paths := by
  have pathDebit := exact_path_debit paths
  omega

theorem exact_target_equivalence (surplusTwice balance alpha beta tau delta target : Int)
    (ledger : surplusTwice = 2 * (balance + beta - alpha) + delta - tau) :
    2 * target ≤ surplusTwice ↔ 2 * alpha + tau ≤ 2 * (balance - target + beta) + delta := by
  omega

theorem closed_packet_no_tp_pairs (surplusTwice balance beta target : Int)
    (ledger : surplusTwice = 2 * (balance + beta))
    (bpPairsNonnegative : 0 ≤ beta) (boundary : target ≤ balance) :
    2 * target ≤ surplusTwice := by omega

theorem closed_packet_owned_reserve (surplusTwice balance alpha beta target : Int)
    (ledger : surplusTwice = 2 * (balance + beta - alpha))
    (reserve : alpha ≤ balance - target + beta) :
    2 * target ≤ surplusTwice := by omega

theorem external_external_has_zero_debit :
    bpEnds external_external - tpEnds external_external = 0 := by rfl

theorem neutral_path_and_loop_partition (width halfHeight : Nat) (tall : 1 ≤ halfHeight) :
    (width + halfHeight + 1) + (halfHeight - 1) = width + 2 * halfHeight := by
  omega

theorem neutral_backward_connector (width : Nat) (wide : 6 ≤ width) :
    6 < width + 3 := by omega

theorem neutral_connector_changes_column_parity (halfWidth : Nat) :
    (2 * halfWidth + 3) % 2 ≠ 6 % 2 := by omega

theorem exact_margin_after_one_tp_path (balance surplusTwice : Int)
    (ledger : surplusTwice = 2 * (balance - 1)) :
    surplusTwice + 2 = 2 * balance := by omega

theorem alternate_phase_balance_shift (surplusTwice originalBalance alternateBalance width : Int)
    (original : surplusTwice = 2 * (originalBalance - 1))
    (alternate : surplusTwice - 2 * (width + 12) = 2 * (alternateBalance + width - 2)) :
    originalBalance - alternateBalance = 2 * width + 11 := by omega

theorem alternate_phase_closed_bound (surplusTwice balance width target : Int)
    (wide : 6 ≤ width) (boundary : target ≤ balance)
    (ledger : surplusTwice = 2 * (balance + width - 2)) :
    2 * target ≤ surplusTwice := by omega

end SubQuorum.PPPathTerminalLedger

#print axioms SubQuorum.PPPathTerminalLedger.tp_terminal_inventory
#print axioms SubQuorum.PPPathTerminalLedger.bp_terminal_inventory
#print axioms SubQuorum.PPPathTerminalLedger.external_terminal_inventory
#print axioms SubQuorum.PPPathTerminalLedger.exact_path_debit
#print axioms SubQuorum.PPPathTerminalLedger.arbitrary_pp_chain_size
#print axioms SubQuorum.PPPathTerminalLedger.exact_column_identity
#print axioms SubQuorum.PPPathTerminalLedger.exact_packet_ledger
#print axioms SubQuorum.PPPathTerminalLedger.exact_target_equivalence
#print axioms SubQuorum.PPPathTerminalLedger.closed_packet_no_tp_pairs
#print axioms SubQuorum.PPPathTerminalLedger.closed_packet_owned_reserve
#print axioms SubQuorum.PPPathTerminalLedger.external_external_has_zero_debit
#print axioms SubQuorum.PPPathTerminalLedger.neutral_path_and_loop_partition
#print axioms SubQuorum.PPPathTerminalLedger.neutral_backward_connector
#print axioms SubQuorum.PPPathTerminalLedger.neutral_connector_changes_column_parity
#print axioms SubQuorum.PPPathTerminalLedger.exact_margin_after_one_tp_path
#print axioms SubQuorum.PPPathTerminalLedger.alternate_phase_balance_shift
#print axioms SubQuorum.PPPathTerminalLedger.alternate_phase_closed_bound
