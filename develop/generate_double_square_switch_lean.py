"""Generate the actual double-switch strict-rank certificate without changing old files."""
from pathlib import Path
source=Path('develop/generate_frozen_mixed_cycle_lean.py').read_text()
source=source.replace('frozen_all_mixed_gate_cycle.json','frozen_double_square_switch.json')
source=source.replace('SubQuorum.FrozenMixedGateCycle','SubQuorum.DoubleSquareSwitch')
source=source.replace("Path('formal/SubQuorum/FrozenMixedGateCycle.lean')", "Path('formal/SubQuorum/DoubleSquareSwitch.lean')")
source=source.replace('roots=[(5,6),(5,19),(24,6),(5,4),', 'roots=[(5,6),(24,19),(24,6),(24,4),')
source=source.replace('eight_actual_cycle_contacts','eight_retained_tip_adjacencies')
assert "Path('formal/SubQuorum/FrozenMixedGateCycle.lean')" not in source
exec(compile(source,'<double-switch generator>','exec'))
