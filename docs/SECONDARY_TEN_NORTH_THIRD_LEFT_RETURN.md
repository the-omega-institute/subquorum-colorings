# Third left consumer: interior repair and a returning-bar obstruction

21 October 2026. Owners: Haobo Ma and Wenlin Zhang. Status: general
written geometric proofs, independently reconstructed finite controls;
not independently reviewed or newly Lean-formalized.

Retain the exact six original owners Q,D,L,C,E,W of the
[outward cavity family](SECONDARY_TEN_NORTH_OUTWARD_CAVITY.md), with b even,
a=b-9, w>=12 even, t=4, v=6, C=U(8,6,4), E=U(6,4,4).
The next missing D support is p=(a+2,w+10). Consider a north-terminal
left-pointing candidate consumer

    T=U(k,ell,z), T(r,c)=(a+2-ell+r,w+11-c),

where k>=6 and ell,z>=4 are even. All counts use aligned 2-by-2 tiles,
ORIGINAL supports and ORIGINAL owners. Write Rraw=S+2F-Ev and
Phi=N+Rraw, where Ev counts actual directed foreign endpoint events.
N counts positive original owners only. These are partial source families;
their Rraw is not asserted to equal a feasible complete model's reserve.

## Interior far leg: exact repair

If k<=w+4, endpoint disjointness from the six fixed owners is equivalent
to z<=ell-6. For every such candidate,

    Delta S=k-1, Delta F=Delta Ev=Delta N=0,
    Delta Rraw=Delta Phi=k-1>=5.                 (1)

Proof. Put d=a+2-ell and f=w+11-k. Then 7<=f<=w+5, so the
far column lies strictly inside D's upper bar, whose row is a-2 and
whose columns are 6 through w+9. If ell=4, T's lower bar at a-1
already intersects D. If ell>=6, its far leg starts at or above a-2
and intersects that D bar whenever d+z>=a-2, or z>=ell-4.
Even parity therefore forces z<=ell-6, and consequently ell>=10.

Conversely this inequality places the entire T bar at or above a-7,
and its far leg ends at or above a-4. D's highest occupied tile row
has lower coordinate a-3. L,C,E,Q,W have no endpoints above D's bar,
so neither the bar nor far leg shares an endpoint tile with any fixed
owner. T's near column is w+10, in a tile column beyond D and L.
W ends at column w+5. Q ends at column11, below w+10. C's stems
are in columns w+7 and w+14, and its bar starts at row a+5.
E's stems are in columns w+8 and w+13, and its bar starts at a+3.
Thus the near leg, which ends at a+2, also shares no endpoint tile
with any fixed owner. This proves disjointness and no shared tiles.

The original charge in this phase is 1-k, and a single source's own
full tiles are excluded from F. No new mixed tile or directed event
exists; old classifications are unchanged. Hence (1). This repairs the
previous displayed loss3 with at least2 remaining in this restricted
inventory. Those2 are not yet a globally available compensation credit.

## Returning bar: an all-width obstruction to uniform repair

For EVERY even w>=12 choose instead k=w+6, ell=6, z=4. Thus

    T=U(w+6,6,4), T(r,c)=(a-4+r,w+11-c).       (2)

This consumes p, is endpoint-disjoint from all six fixed owners, and has
charge -(w+5). Its exact insertion counts are

    Delta S=w+5, Delta F=(w+4)/2,
    Delta Ev=2(w+4), Delta N=0,
    Delta Rraw=Delta Phi=1.                    (3)

In particular the rule "either next orientation restores at least3"
is FALSE under endpoint disjointness and these prescribed consumers.
Relative to Q/D/W the seven-owner Phi is still lower by2, because the
preceding six-owner package had exact loss3. This is a counterexample
to that LOCAL repair rule, not to the target inequality mu>=0.

Proof. T's bar occupies rows a-4,a-3 and columns5 through w+10.
Its near leg lies in column w+10 down to row a+2, and its far leg in
column5 down to row a. Both stems lie outside D's endpoint tile columns;
the other five owners have no endpoint in these bar tiles or stem tiles.
The only shared endpoint tiles have lower coordinates

    (a-3,2j), j=3,...,(w+8)/2.

Each contains T's lower bar row a-3 and D's upper bar row a-2,
with two endpoints from each original owner. There are (w+4)/2 tiles.
Every such tile becomes mixed full, and each of its two vertical edges
gives BOTH directed events. Neither direction is excluded: along these
bar columns, the opposite row is not an original support of its owner.
Thus each tile supplies one full tile and four events, contributing -2
to 2F-Ev. Their total debit is w+4. Together with Delta S=w+5 this
proves (3). No event is charged twice: the two directions are distinct
original-owner events, each included once in the same inventory.

This family is explicitly INCOMPLETE. T's axial original support
q=(a+1,5) remains absent, with T's endpoint (a,5) to its north and
D's endpoint (a+1,6) to its east. Its consumption must be followed in
any complete extension. Another absent T support (a+2,w+11) has E's
endpoint (a+3,w+11) to its south and T's p to its west. The local
identity alone neither proves nor disproves extendibility. At b40,w12,
Phi(Q/D/W)=21, Phi(Q/D/L/C/E/W)=18, and insertion (2) gives Phi=19;
even this partial functional is positive, so a target counterexample
is not claimed.

## Consequence and verification

Together with the [third-right repair](SECONDARY_TEN_NORTH_THIRD_RIGHT_REPAIR.md),
this separates a genuine interior compensation mechanism from a return
which spends width-sized mass on an already occupied D bar. A global
proof must follow the new support closure or reserve the shared band
jointly. It cannot allocate k-1 as fresh credit before deducting its
original directed contacts, nor use D's occupied band a second time.

The [checker](../develop/check_secondary_ten_north_third_left_return.py)
reconstructs endpoints, original supports, mixed tiles and directed
events independently for translated, small and large widths. It checks
the exact contact tile/event SETS, the interior disjointness criterion,
both missing supports and the comparison with Q/D/W. Its
[receipt](../output/secondary-ten-north-third-left-controls.json) is finite
corroboration; the unbounded statements follow from the proofs above.
No earlier Oracle ACCEPT or Lean result is claimed to cover this note.
Unrestricted allocation, arbitrary additional owners, complete
realizability, and the rectangular-grid triple equality remain OPEN.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
