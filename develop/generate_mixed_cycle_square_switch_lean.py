"""Generate the new actual308P square-switch certificate, using existing
strict-rank proof infrastructure. Does not rewrite the previous Lean file.
"""
from pathlib import Path

source=Path('develop/generate_frozen_mixed_cycle_lean.py').read_text()
source=source.replace('frozen_all_mixed_gate_cycle.json','frozen_mixed_cycle_square_switch.json')
source=source.replace('SubQuorum.FrozenMixedGateCycle','SubQuorum.MixedCycleSquareSwitch')
source=source.replace("Path('formal/SubQuorum/FrozenMixedGateCycle.lean')",
                      "Path('formal/SubQuorum/MixedCycleSquareSwitch.lean')")
source=source.replace('roots=[(5,6),(5,19),(24,6),(5,4),',
                      'roots=[(5,6),(5,19),(24,6),(24,4),')
source=source.replace('eight_actual_cycle_contacts','eight_retained_tip_adjacencies')
assert "Path('formal/SubQuorum/FrozenMixedGateCycle.lean')" not in source
exec(compile(source,'<square-switch certificate generator>','exec'))
