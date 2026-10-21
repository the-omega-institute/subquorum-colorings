# Four retained originals exclude the entire second-return family

22 October 2026. This proves a complete-extension obstruction for the
[unbounded second-return family](SECONDARY_TEN_UNBOUNDED_SECOND_RETURN.md).
The obstruction already occurs in FOUR retained original U records; it
does not depend on the old second-block far parameter g, R, T or W.
The negative partial-union receipt remains correct. It cannot occur as
this retained subfamily in a complete extension of the stated model.

## Model and local obstruction lemma

Work in the square grid, retaining every original endpoint, matching
and support. Original endpoint sets are pairwise disjoint. Every new
original is a full U(B,d,f), with even B>=6,d,f>=4, in any lattice
orientation, or a standard rotor in any lattice orientation. Each
unconsumed original support must have exactly one occupied neighbour.
Consequently an absent original support with at least two retained
endpoint neighbours must be occupied by a fresh original in a complete
extension. Additional originals cannot delete a retained endpoint or
change an original's supports. This is the explicit full-U/rotor model,
not a claim that it exhausts arbitrary rectangular-grid configurations.

Fix any integer C. Suppose the retained endpoint union contains

    (r,C-1), 23<=r<=33;
    (r,C+1), 25<=r<=31;
    (22,C), (31,C).                              (1)

Suppose p=(25,C) is an ORIGINAL support and the three points
(25,C),(28,C),(30,C) are absent from this fixed baseline endpoint
union. Then NO complete extension exists in this model. The assertion
is invariant under translations and all square-lattice isometries.
Extra originals cannot repair the obstruction: any owner they place at
one of these three holes is distinct from every fixed baseline owner.

### The first fresh owner is forced into a corner form

The west and east neighbours of p are retained endpoints by (1), so
p must be an endpoint of a fresh original O, whose internal endpoint
neighbours at p can only point north or south.

For a rotor, an endpoint has degree one or three in its endpoint-induced
grid graph. Degree three is impossible here. In either north-terminal
pattern, O contains p+(-2,-1)=(23,C-1); in either south-terminal
pattern it contains p+(2,-1)=(27,C-1). All are retained endpoints.
These are the complete four terminal patterns under the eight lattice
symmetries, so no rotor can own p.

For a full U, a point with no horizontal internal neighbour must lie
on a vertical leg, away from its bar. Every point on either bar row
has a horizontal internal neighbour, and a horizontal leg also has a
horizontal internal neighbour. Thus let t be the bar row of the leg
through p, let d>=4 be its even depth, and write sigma=+1 or-1 for
its direction from the bar. The U contains every point in column C
between t and t+sigma*d, including row25. The retained cap at row22
and the retained endpoint at row31 confine this ENTIRE interval to
rows23,...,30. In particular23<=t<=30.

The leg's bar endpoint has a same-row horizontal companion on the
side into which the bar extends. At every row25,...,30 BOTH possible
companions are retained by (1), so t cannot be in that interval.
At rows23,24 the west companion is retained, so the bar must extend
east. Its leg must point south because it contains row25. If t=24,
the U's inner bar row contains (25,C+1), a retained endpoint. Hence
t=23. The depth bound23+d<=30 and even d>=4 give d in{4,6}.

Thus EVERY possible U owner has the exact normal form, after exchanging
its two legs if necessary,

    O=U(B,d,f), chart(23+r,C-1+c),
    B>=6, d in{4,6}, f>=4, all even.             (2)

This conclusion is necessary; extra retained endpoints may exclude
some of these forms already. It preserves the original support and
matching phase: reversal of the even bar length exchanges the equal
parity bar matching and the two leg records.

### Both remaining depths force a forbidden next owner

The original near axial support of (2) is

    p'=(24+d,C).

It is neither an endpoint of O nor a baseline endpoint, by the three
explicit hole assumptions. It must therefore belong to a distinct
additional original in any complete extension: either that original
already occupies it, or the occupied neighbours below force occupation.
That owner's endpoints are disjoint from EVERY baseline original and O.
This also handles all other additional originals without treating a
point as blocked against its own owner.

For d=6, p'=(30,C) has north endpoint (29,C) in O and the retained
west/east/south endpoints (30,C-1),(30,C+1),(31,C). A distinct owner
containing p' has no available adjacent endpoint for its matching
edge. This contradicts the original matching requirement, regardless
of the new owner's shape.

For d=4, p'=(28,C) has north endpoint (27,C) in O and west/east
retained endpoints (28,C-1),(28,C+1). Any distinct owner containing
p' must have its own matching neighbour south and cannot have any
other internal neighbour there. In a full U this is a south terminal;
its even leg length at least4 gives a continuous endpoint stem through
(31,C), already retained. In a rotor it is one of two south-terminal
patterns, both containing (30,C-1), already retained. Every allowed
owner is excluded. If its south neighbour were already occupied by
yet another retained owner, the contradiction would be still immediate.

Both depths in (2) are impossible. This proves the local obstruction
with no bound on breadth, far-leg length or the number of extra owners.
No source reserve, full-tile count or compensation credit is used.

## Four explicit originals realizing the obstruction

For every even h>=12 set C=h+13. Retain the following complete U records:

    K=U(6,6,4),       chart(25+r,C+c);
    P=U(h+12,10,4),   chart(23+r,C-c);
    D=U(6,4,4),       chart(35-r,h+7+c);
    V=U(6,4,h+8),     chart(16+c,h+15-r).         (3)

They are endpoint-disjoint. Indeed V ends at row22 while all other
records start at row23. K has columns C+1,...,C+6, whereas P has
columns at most C-1 and D at most C. P's bar occupies rows23,24;
its two later stems are columns1,C-1. D has rows31,...,35 and
columns h+8,...,C, avoiding both P stems because h>=12. These
inequalities compare complete endpoint sets, not only their bars.

P supplies the entire left wall in (1), K the entire right wall,
V the cap (22,C), and D the cap (31,C). The point p=(25,C) is
K's original left bar-end support. All three holes (25,C),(28,C),(30,C)
belong to none of the four endpoint sets. The two neighbours of p in
P and K therefore force its
occupation. The local lemma proves:

    {K,P,D,V} has no complete full-U/rotor extension.             (4)

All four records occur unchanged in the earlier H3+R+T+W+V family:
K is its root, P=P_0, D=B_0[4], and V is its second-return owner.
Therefore that ENTIRE two-parameter family has no complete extension,
for every even h>=12,g>=4. Adding R,T,W or further originals cannot
remove the obstruction. This is stronger than excluding any particular
choice at the later q=(23,C).

## Consequences for compensation and the next research step

The exact partial increment-h/2-1 and the positive V marginal-h/2-2
remain valid mathematical identities. They refute the endpoint-disjoint
partial-union rule. They are not losses that an actual complete family
in this model must repay: such a family cannot contain these originals.

Likewise the upward/downward q-owner receipt identities in the
[next-owner note](SECONDARY_TEN_NEXT_SUPPORT_EAST_TERMINAL.md) remain
valid for the specified endpoint-disjoint partial unions. Their
application to actual complete extensions of this H is now vacuous.
Do not treat them as a nonempty new case of global compensation.

This result removes one entire unbounded-return obstruction from the
actual-family allocation problem; it does not prove that other returns
are absent. The prior simultaneous selected-pair>=4m theorem remains
unchanged. The following corollary gives a necessary restriction on
an entire class of genuinely possible return candidates.

### Corollary: an upward return has a strict root-column reach limit

Retain H3+R+T+W before V, with even h>=12,g>=4, and let an actual
owner of z=(22,7) have the upward east-terminal form

    A=U(L,D,F), chart(23-c,7+D-r),
    L>=6,D,F>=4, all even.                       (5)

Then every complete extension containing A must satisfy

    D<=h+4.                                     (6)

Indeed, all A endpoints have row at most22. If D>=h+6, its continuous
near leg contains (22,h+13), supplying the cap of (1). The same
three old originals K,P,D from (3), together with A, have all three
holes empty and satisfy the local obstruction. They cannot extend.
The remaining even values have D<=h+4. Here the symbol D in (5)
denotes the leg depth; the old record labelled D in (3) is unchanged.

For the allowed range4<=D<=h+4, the exact partial-union receipt is

    charge(A)=1;
    newFull=D/2+1;
    newEvents=3D/2+1;
    DeltaPhi(A|H3+R+T+W)=2-D/2.                  (7)

To see this directly, put b=7+D<=h+11. The only foreign endpoints
in A's tiles are P's row23 and W's terminal(22,6). The new full
tiles have top-left (22,6),(22,8),...,(22,b-1). The first is the
three-owner W/A/P tile, counted once. The complete new event set is

    P:(23,c)->A:(22,c), c=7,...,b;
    A:(22,c)->P:(23,c), c=8,10,...,b-1.

Both old directions between W:(22,6) and P:(23,6) remain old.
The W/A horizontal directions target their original axial supports.
The odd-column A-downward directions target original lateral supports.
Every other A endpoint tile lies above the old union. The source
counts are matching L-1+(D+F)/2, tiles L/2+1+(D+F)/2, and inside
supports4+(D+F)/2, giving charge1. Its new positive-owner count and
the two disjoint receipt sets prove (7), without reused old events.

The whole selected increment after this return is consequently3-D/2.
It can still decrease with h within (6); neither full extendibility
nor global compensation follows from the reach restriction alone.
The next actual root-support owner at (25,h+13) must be included
in a successful joint budget for these shorter return candidates.

Next classify returns that avoid at least one of the two
caps or two wall segments, and prove a joint nonreusing budget for
the genuinely extendible residual families. Global5/6 improvement,
catalogue exhaustion and rectangular-grid triple equality remain open.

The companion verifier checks complete source records, all small-shape
roles and both support phases, large corner dimensions, the forced
second-support patterns and translated/isometric applications. These
are finite controls of the written general proof. The associated Lean
scope and independent-review status are recorded separately.

Run `PYTHONDONTWRITEBYTECODE=1 python3 develop/check_secondary_ten_four_original_return_obstruction.py`.
The current controls pass6912eligible U roles,64complete corner-record
normalizations,16first-rotor placements,72corner gate receipts,
72south-rotor exclusions,16exact inclusions in the earlier family,
and96translated/isometric four-original applications. These controls
include breadth and far length2000; those values are not proof cutoffs.

`formal/SubQuorum/SecondaryTenFourOriginalReturnObstruction.lean`
proves12local theorems in16explicit declarations. Its all-parameter
vertical-leg normalization derives bar row23, south/east directions
and depth4or6 from the actual continuous leg and bar-neighbour data.
It also checks the cap, rotor-fork, forced matching and sealed-next-
owner contradictions. The source-role adapter and complete-extension
ownership argument remain written. Lean4.33.0 and every individual
axiom audit pass cleanly; no complete source-model formalization is claimed.
The first independent-review packet covers the local lemma and
four-original application; the later reach-limit/receipt corollary is
outside that packet and has its own exact controls.
