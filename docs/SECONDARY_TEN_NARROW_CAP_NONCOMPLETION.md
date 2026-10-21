# Complete-family exclusion of the narrow positive zero-increment cap

21 October 2026. This general geometric lemma excludes an entire branch in
the existing U/rotor source model. It supplies no new global allocation bound.

## Statement and assumptions

Use exactly the original-source model and the residual family A of
[the persistent-pair note](SECONDARY_TEN_PERSISTENT_PAIR_COMPENSATION.md):
all original endpoints and original supports are retained, endpoint sets of
different originals are disjoint, and each unconsumed original support has
only one occupied neighbor in a complete feasible fusion. Allowed originals
are all legal U sources and the explicitly specified D4 rotor orbit. Legal
U breadths are even and at least6; both legs are even and at least4.
No change to this source catalogue or completeness condition is made here.

Let a be odd, w>=12 even, and let A be Q,D,L,C,E,W,T0,V, where

    V=U(k,8,z),  (r,c) -> (a-6+r,w+12-c),

with either k=w+8 and 4<=z<=14 even, or k=w+10 and z>=16 even. These are
the two residual branches already established. For even ell>=12 and
s in {6,8}, define the original source

    K_s=U(s,ell,ell-8),  (r,c) -> (a+1-ell+r,w+15-c).

**Theorem. No complete feasible U/rotor family can retain all originals of
A+K_s.** This holds with arbitrarily many further originals, arbitrary legal
dimensions, and arbitrary translations preserving the stated phase.

K_s itself is endpoint-disjoint from A and has original charge+1 and exact
DeltaPhi(K_s|A)=0. Thus a nonnegative partial inventory and endpoint
disjointness do not establish complete extendibility. The width6 instance
is the entire positive zero-increment family of the preceding note.

## A different forced support closes the cavity

Put p=(a+2,w+12). This is V's original near lateral support: in V's canonical
coordinates it is (8,0). It is not an endpoint of A+K_s. Its neighbors

    west  (a+2,w+11) belongs to V,
    east  (a+2,w+13) belongs to E,
    south (a+3,w+12) belongs to E.

are fixed foreign original endpoints. If p were unconsumed in a complete
fusion, its three occupied neighbors would violate the support condition.
Therefore p must belong to a further original consumer J. Its matching
partner must be north of p: all other neighboring sites already have foreign
owners. Additional originals can only impose more endpoint exclusions.

The only U endpoint with no own neighbor other than north is a north terminal.
After relabeling the two legs, every U candidate therefore has one of the
following frames, with breadth h>=6 and even depth d>=4, other leg f>=4:

    J_right=U(h,d,f), (r,c) -> (a+2-d+r,w+11+c),
    J_left =U(h,d,f), (r,c) -> (a+2-d+r,w+13-c).

The U bar corners and internal endpoints have at least two own neighbors
and cannot occur at p. Rotor inner endpoints have three own neighbors, so
only the two north-terminal rotor forms remain. This is a role argument
for the full source catalogue, not a dimension-bounded search.

## Every U candidate has an explicit foreign-endpoint collision

The table gives a point simultaneously in J and the indicated fixed blocker.
All bounds are inclusive except d<ell, as displayed.

| Candidate | Depth range | Collision point | Blocker |
|---|---|---|---|
| Either direction | d>=ell | (a+2-ell,w+12) | K_s bar |
| Right | 4<=d<ell | (a+3-d,w+14) | K_s near stem |
| Left | 4<=d<=8 | (a+3-d,w+11) | V near stem or bar |
| Left | 10<=d<ell | (a+3-d,w+15-s) | K_s far stem |

Here is the coordinate check, with no unstated upper bound on h,d,f,ell.

- If d>=ell, the point is in J's near column. Its intrinsic row is d-ell,
  which is either a bar row or a valid near-stem row. In K_s it is intrinsic
  (1,3), a bar endpoint since s>=6.
- In the short-right case, the point is J's bar endpoint (1,3). In K_s it is
  in the near column at row ell+2-d, between2 and ell since d>=4 and d<ell.
- In the short-left case, the point is J's bar endpoint (1,2). In V it is in
  the near column at intrinsic row9-d, between1 and5. Row1 is a bar row;
  the remaining rows are in V's length8 near stem.
- In the remaining left case, the point is J's bar endpoint (1,s-2).
  The bound 6<=s<=8 gives 4<=s-2<=6<=h. In K_s it is in the far column
  at row ell+2-d, between2 and ell-8 because d>=10 and d<ell.

Evenness of d ensures that there is no depth between8 and10. Thus the table
exhausts all legal north-terminal U candidates. The last inequality shows
exactly why narrow breadth matters: a minimal legal J bar necessarily spans
K_s's far column when s<=8. No exclusion for wider caps is claimed.

## Both north rotors are blocked already by E

In coordinates relative to p, the two terminal endpoint footprints are

    {(-3,-1),(-2,-1),(-2,0),(-2,1),
     (-1,-2),(-1,-1),(-1,0),(0,0)},

    {(-3,1),(-2,-1),(-2,0),(-2,1),
     (-1,0),(-1,1),(-1,2),(0,0)}.

Both contain p+(-2,1)=(a,w+13), E's original far terminal. The stated D4
catalogue gives precisely these two forms at a north terminal; rotations
and reflections of inner endpoints have already been excluded by their
three own neighbors. Hence no rotor consumer exists either.

Every allowed original consumer at p has now been excluded. This contradicts
the completeness requirement and proves the theorem. Keeping additional
originals cannot remove a collision with a retained original endpoint.

## Exact charge and contact inventory of the excluded cap

K_s's original matching has s+ell-5 edges. Its endpoint tiles number
s/2+ell-3; exactly ell counted original supports lie in those tiles.
Therefore its charge is (s+ell-5)+ell-2(s/2+ell-3)=1.
There are exactly two shared endpoint tiles with A:

| Lower corner | Newly full | New directed events |
|---|---:|---:|
| (a-7,w+14-s) | 0 | 1 |
| (a+1,w+14) | 0 | 0 |

The sole event goes from V's upper bar at (a-6,w+15-s) to K_s's far
terminal (a-7,w+15-s). The opposite direction targets K_s's original axial
support. The C/K_s terminal tile is shared but both directions are excluded
by original axial supports. Thus DeltaN=1, DeltaS=DeltaF=0, DeltaEv=1,
and DeltaPhi=0. These are partial-inventory identities; the exclusion proof
uses forced occupancy and endpoint collisions, not the sign of Phi.

## Consequence for the previous negative marginal

The all-width family H of
[the negative-marginal note](SECONDARY_TEN_NEGATIVE_MARGINAL_BAND.md)
was inserted after K_6 and had exact DeltaPhi=-w/2. That algebraic identity
remains correct. The present theorem proves that its prescribed A+K_6
prefix already has no complete feasible extension. Consequently A+K_6+H
cannot occur as retained originals in a complete feasible U/rotor family.

This eliminates that entire negative-marginal branch from the complete-model
proof search. It does not validate the failed rule on arbitrary partial
inventories, classify all consumers of the earlier persistent pair, or
establish reserve monotonicity under actual complete source retention.
The complete global allocation/grid-equality problem remains open.

## Verification scope

`develop/check_secondary_ten_narrow_cap_exclusion.py` reconstructs all original
sources, exact charge/contact sets, three forced neighbors, every collision
witness, both rotor footprints, and a finite complete north-role catalogue.
The unbounded proof is the role classification and collision table above.

`formal/SubQuorum/SecondaryTenNarrowCapExclusion.lean` independently states
the endpoint predicates and verifies the unbounded absence, three anchors,
four collision cases, exhaustive left/right depth splits and both explicit
north-rotor footprints. Formalization of the entire source-catalogue
classification and abstract complete-family implication is not claimed.
Lean execution and axiom inspection are recorded separately.
