# Pure U01 cycles have disjoint interior absorber families

20 October 2026. Under the unrestricted complete-source assumptions, each
pure U01 neutral port cycle C has a family V(C) of actual original U sources
absorbing its inward forced supports. Its members lie wholly inside C, and
V(C) and V(D) are DISJOINT for different such cycles, including nested ones.
If m(C) is C's number of original U01 owners, then

    |V(C)| >= ceil((m(C)+4)/8),
    sum_C ceil((m(C)+4)/8) <= |union_C V(C)|.          (1)

In particular each cycle requires its own complete interior U source. This
strengthens the Hall-only proposal in completed researcha3325b82: the geometric
regions prove actual absorber-family separation, so rounded quotas add. The
right side counts SOURCES, not reserve payments. Full coefficient-one allocation
and rectangular-grid equality remain OPEN.

## The specified curves and forced points

Use the exact port graph and simple lattice polygons of
[neutral port turning](NEUTRAL_U_PORT_TURNING_AND_SHARED_BUDGET.md).
Phase01 ports are original terminal1P1T occurrences; phase10 ports are original
outer-bar-corner1P1T occurrences. A neutral contact has actual profile2P1T,
one active and one passive port. Distinct closed components have vertex-disjoint
simple lattice curves, because all source arcs use unique original endpoints
and their contacts are unit lattice edges. The chosen family below contains
only cycles whose original owners all have phase01. Other source types,
other curves, all full contacts and source recurrence remain allowed.

At any actual neutral01-to-01 contact, transport the fixed physical partition
and normalize active p=(0,0), passive q=(0,1), with p's incident stem pointing
south. The inward forced support is z=(1,1); its actual physical tile is

    Qz={1,2}x{0,1}.

The active source owns the EXACT original pair {(1,0),(2,0)} in Qz and has
the original support z, anchored at (1,0). The passive original terminal also
has support z, anchored at q. Those two persistent endpoint neighbors force
z into P, with an owner different from both incident sources.

The inward frame is a transport, not a parity reset. Complete sources give
the foreign endpoint barriers

    {(r,0):0<=r<=4} union {(0,c):1<=c<=5}.           (2)

The strong conclusions below require these complete barriers and the original
exact pair, not only the existence of a two-source contact.

## Global nonreuse of forced supports and local owner capacity

If two contacts produced the same z, their original active pairs would lie in
the SAME physical Qz. The only two adjacent pairs avoiding z intersect at the
opposite corner. Endpoint uniqueness identifies their owner; that owner's
exact original pair in Qz is fixed. The original support z has a unique anchor
in that source. This identifies p+s, then p+2s, hence p,s,d and the contact.
Thus forced points are globally distinct, even between different cycles.

A rotor cannot own z. Its endpoint graph is connected and its coordinate
spans are both three. Starting from z, every endpoint has both coordinates
at most4. If any endpoint leaves the positive quadrant, the first boundary
vertex of an original endpoint path lies in (2). Otherwise z attains both
minimum coordinates, but no bounding-box corner of the rotor is an endpoint.
Both possibilities contradict the explicit complete rotor template. Rotations
and reflections preserve these properties. The exact16-role kernel check is
an additional finite-template verification of the same all-translation fact.

The two perpendicular foreign neighbors north and west of z exclude every U
endpoint role except its two terminals and two upper outer bar corners. A
straight stem/bar point has two opposite endpoint neighbors; other bar points
have at least three. Each original U therefore owns at most FOUR of the
globally distinct forced points, independently of dimensions or orientation.

## No forced point is on any closed neutral U-port curve

Suppose z lay on such a curve. At a straight source-arc point, two opposite
own neighbors include one of z's two perpendicular foreign neighbors, giving
an endpoint collision. At an arc bend of a phase01 source, the original outer
bar corner lies in an original full tile, incompatible with the foreign exact
pair already in Qz. At a curve port, the physical tile's actual2P1T profile
is incompatible with the three endpoints already in Qz (the pair plus z).
Unit contact edges have no interior lattice vertices. These cases exhaust
the prescribed source arcs and contact edges. Hence z is on no such curve.

Furthermore no phase01 owner on ANY closed port curve can own z anywhere in
its full source: its terminals are neutral ports, its two upper outer bar
corners lie in original full tiles, and all remaining roles were excluded.
In particular z's actual owner is different from every owner of any chosen
pure U01 cycle. This last statement is needed before using the other curves
as endpoint barriers; distinct curve labels alone would not establish it.

## Exact inward count and complete-source containment

Orient a pure U01 curve C with total quarter-turn4. The source signs chi
alternate, so its source-arc turns sum to zero. Each neutral contact contributes
one convex or concave turn. If I(C),O(C) count these, then

    I(C)-O(C)=4, I(C)+O(C)=m(C),
    I(C)=(m(C)+4)/2 >=4.                            (3)

The corresponding forced point lies strictly inside C at a convex contact,
and strictly outside at a concave contact. Its unit contact square has no
curve edge in its open face, and the previous section excludes its opposite
vertex from every curve. Thus local inside/outside classification is valid
even when distant parts of the polygon run nearby.

Define V(C) using the actual owners of its I(C) inside forced points. Every
member is a U, not a rotor, and is not a source of any chosen cycle. Its
endpoint graph is connected and disjoint from every chosen curve. A unit
lattice endpoint path cannot cross a curve without sharing an integer vertex.
It follows that all its endpoints lie strictly inside C. Each original support
is one unit from its own endpoint anchor, so it lies inside C or on C; an
on-curve support is already consumed by an original curve endpoint. This is
complete-source containment, not a claim that deletion of the other sources
would leave a feasible standalone subfusion.

## Why nested cycles cannot reuse an absorber

For any inward forced point z of C, one unit edge joins z to its active
original anchor x=p+s on C. Let D be a distinct chosen pure U01 cycle.
Neither endpoint z,x belongs to D. A unit lattice edge cannot cross D in
its interior: any intersection of unit lattice edges has an integer endpoint.
Therefore z and x lie on the SAME side of D.

Two vertex-disjoint simple closed curves are either nested or have disjoint
interiors. If D lies inside C, then x, and hence z, lie outside D. Connected
endpoint ownership then puts the entire P_V outside D for V in V(C).
But every V in V(D) lies strictly inside D. The two families are disjoint.
If C lies inside D use the symmetric argument. With disjoint interiors,
containment alone gives disjointness. Thus V(C) intersects V(D) in the empty
set for every distinct pair, including arbitrary nesting depth.

This is the extra geometric step beyond the research response's Hall count.
It prevents a single source's four-point capacity from being spread over
different chosen pure cycles, and preserves individual rounding.

## Simultaneous count and remaining payment gap

The local capacity and (3) give

    (m(C)+4)/2 <=4|V(C)|,
    ceil((m(C)+4)/8) <= |V(C)|.

Sum using the PROVED pairwise disjoint absorber families to obtain (1).
For instance a six-source pure cycle requires at least two interior sources,
and two such cycles require at least four different sources. This is a
conditional necessity, not a claim that a six-source cycle is realizable.
One may also select distinct source representatives for all cycles, as in
the original Hall proposal, but the disjoint-family conclusion is stronger.

No member of V(C) has yet been assigned an unused A/U0/Z0/H payment. It may
have full or critical receivers, U11 caps or open port continuations. The
spatial region argument proves source nonreuse, not a source-to-reserve map.
In particular (1) cannot be added to a reserve lower bound as extra R.
Mixed cycles can have their own phase10 terminal absorbers; the above proof
deliberately does not assert the same separation for those cycles. Closing
those actual continuations and the marked-positive-side allocation remains
the full task.

## Verification scope

[NeutralCycleInteriorTransfer.lean](../formal/SubQuorum/NeutralCycleInteriorTransfer.lean)
checks the exact rotor template, arbitrary-dimension four-role U catalogue,
conditional turning/capacity counts and rounded quota aggregation. The simple
polygon, same-side unit-edge, connected-source containment and pairwise region
separation are written geometric proofs, not a Lean formalization of the plane.
Finite controls remain discovery/checking evidence and do not prove (1).
