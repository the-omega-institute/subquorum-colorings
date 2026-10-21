# A two-direction cavity excludes the root depth-eight branch

21 October 2026. This strengthens the
[first deep root triple](SECONDARY_TEN_ROOT_DEEP_TRIPLE.md). It uses the
same explicit EVERY-original full even U/standard-rotor model, immutable
supports/matching, and complete-feasibility convention. The argument reuses
the forced-support exclusion method of the earlier
[distinct-owner depth-eight lemma](SECONDARY_TEN_DEPTH_EIGHT_COMPLETE_EXCLUSION.md)
at a different root geometry. It is not an arbitrary-grid exhaustion result.

## A geometric lemma with no component-size cutoff

Use coordinates relative to a site x=(0,0). For an integer q>=3 let the
following sites be retained endpoints of originals other than a proposed
consumer J of x:

    north: (-1,c), 0<=c<=q;
    east:  (0,q);
    south: (4,c), 0<=c<=q-1;
    west:  (r,-1), r=0,1,2.                         (G)

Then NO full permitted U or standard rotor endpoint set can contain x
while avoiding all of(G). In particular if x is an absent original
support in a complete feasible family with these retained guards, that
family cannot exist.

Proof. The north and west neighbors of x are foreign retained endpoints.
An original consuming x must have an own matching neighbor; its possible
own endpoint neighbors at x are therefore a nonempty subset of east and
south. Inspecting the full canonical U endpoint definition gives exactly
these possibilities:

1. A terminal with matching direction south. Its incident leg has depth
   d>=4 and occupies every site(0,0),(1,0),...,(d,0). In particular it
   hits the south guard(4,0).
2. A degree-two outer bar corner, with own neighbors east and south.
   Either its south ray is a stem of depth>=4, or it is a bar ray of
   length L-1>=5. It also contains(4,0), a south guard.
3. A terminal with matching direction east. After possible interchange
   of its legs it has incident depth d>=4, an incident ray(0,c) for
   0<=c<=d, and bar columns d-1,d. The breadth direction of its bar is
   either north or south. If d>=q the incident ray hits the east guard
   (0,q). If d<q and the bar points north, its endpoint(-1,d) hits a
   north guard. If d<q and the bar points south, its breadth L>=6 makes
   (4,d) a bar endpoint, hitting a south guard because d<=q-1.

These roles exhaust a full U: its two stem terminals have degree one;
its outer row0 bar corners have degree two with perpendicular neighbors;
other degree-two stem sites have opposite neighbors; and every remaining
bar site has at least three endpoint neighbors. The last two categories
cannot have all own neighbors in {east,south}. Rigid motions and exchanging
near/far legs give precisely the roles above and preserve the full set.
The actual matching can only impose further restrictions.

For the fixed standard rotor there are precisely four allowed translated
and reflected endpoint shapes at x. Listing their full endpoint sets
relative to x makes the finite catalogue transparent:

| Matching direction | Endpoint set | Collision in(G) |
|---|---|---|
| south | {(0,0),(1,0),(1,1),(1,2),(2,-1),(2,0),(2,1),(3,1)} | (2,-1) |
| east | {(-2,1),(-1,1),(-1,2),(-1,3),(0,0),(0,1),(0,2),(1,2)} | (-1,1) |
| south | {(0,0),(1,-2),(1,-1),(1,0),(2,-1),(2,0),(2,1),(3,-1)} | (1,-1) |
| east | {(-1,2),(0,0),(0,1),(0,2),(1,1),(1,2),(1,3),(2,1)} | (-1,2) |

Each non-tip rotor endpoint has too many own neighbors, or neighbors in
an excluded direction. Rotating its four tips into east/south and choosing
the two handed shapes yields exactly this table. Its collisions need
only q>=2. Thus neither kind of permitted original can consume x.

Finally an absent original support with both north and west foreign
endpoint neighbors cannot remain unconsumed in a complete feasible family:
such a support must otherwise have exactly one occupied neighbor. Its
actual consuming original would have to be disjoint from all retained
guards, a contradiction. This proves the lemma. No search cutoff or
independent-positive-receipt assumption occurs in this argument.

## Application to every depth-eight A of the root triple

Retain the full H3 chain and specified first deep B, arbitrary actual
E-owner R of the accepted pair theorem, and any geometrically admissible
depth-eight t0 owner

    A=U(L,8,f), chart(a-12+r,s+1-c),
    6<=L<=v+12, 4<=f<=z-4, all even.

The point x=(a-12,s+1) is A's ORIGINAL bar-exterior support (0,0).
It is absent from every retained endpoint set: it is outside A's bar,
B at this row has only its stems at s1 and C, R has columns>=C, and
all old H3 endpoints start at row a-8 or below. Both foreign neighbors
are retained: north(a-13,s+1) is B's row1 bar; west(a-12,s) is A's
row0 near corner. The east and south neighbors are free in this inventory.

Take q=u+12>=24 and translate(G) by x. Every guard is a retained endpoint:

- The north strip is B's row1 bar at row a-13, from column s+1 to
  C=s+u+13. Its bar includes this whole interval.
- The east guard is B's far endpoint-column point(a-12,C).
- The south strip is P0's row0 bar at row a-8, columns s+1 through
  s+u+12=C-1.
- The three west sites are A's near column s at rows a-12,a-11,a-10.

All guards belong to old H3,B,A. They are independent of L,f,R's breadth
and far depth, the other block parameters and the number of later blocks.
An additional actual owner of x is distinct from all these originals,
because x is absent from their full endpoint sets. The geometric lemma
therefore rules it out. Completeness forces such an owner, so NO complete
feasible full-U/rotor extension can contain this depth-eight A prefix.

## Stronger actual-owner classification and compensation

The full geometric root-triple classification and all its receipt formulas
remain correct. The d8 family, however, has no complete-family instances.
It remains a valid control for a negative marginal in a partial inventory,
and cannot witness failure of a complete-family monotonicity statement.

In every complete feasible extension containing the specified root B,
the actual t0 owner consequently has only d4 or d6. With the notation of
the root-triple note, its exact marginal after B,R is

    L-1-epsilon, epsilon=[L=v+12].

If epsilon0 this is at least5. If epsilon1, L=v+12>=24 and the marginal
is v+10>=22. Hence EVERY actual choice gives

    DeltaPhi({B,R,A}|H3)=u+v+L+24-epsilon
                      >=u+v+30>=54.

This improves the geometric triple lower bound46 to the complete-model
conditional bound54, while using exactly the same single union of physical
tiles and events. The cavity proof creates no additional source credit;
it excludes impossible parameter values. The bound54 is not asserted
sharp among complete extensions, whose existence is not proved here.

## The reflected R-support cavity removes two more branches

The same geometric lemma also applies at a different missing support,
without changing the root-triple ledger. This additional deduction was
made AFTER the cavity audit request; that request does not cover it.

Let p=(a-9,C-1), R's original row0 bar-exterior support. It is absent:
R begins at column C, A ends at column s<C-1, old H3 begins at row a-8,
and B has only its two stem columns at row a-9. Its east neighbor is an
R endpoint and its south neighbor is P0's row0 endpoint. A consuming
original can only have own neighbors north/west. Reflect both relative
coordinate axes in the geometric lemma, so these become east/south.

If A has d6, choose q=u+12. The reflected north strip is row a-8,
columns s through C-1: P0 supplies s+1,...,C-1 and A's near stem
supplies column s. The reflected east wall is(a-9,s), in A's lower
bar row. The reflected south strip is row a-13, columns s+1 through
C-1, in B's lower bar. The reflected west guards are column C at rows
a-9,a-10,a-11: R supplies the first and B its other two far-stem points.
All guards are retained endpoints, independent of A's L and f and R's
parameters. The missing support p is forced to be consumed, but the
reflected cavity forbids every permitted consumer. Thus ALL d6 actual
t0-owner branches also have no complete extension.

If A has d4 and tight breadth L=v+12, choose q=u+v+24=C-1-s1. Its
reflected north strip is row a-8, columns s1 through C-1. B's near
stem supplies s1, A's row0 bar supplies s1+1 through s, and P0's
row0 bar supplies s+1 through C-1. The reflected east wall(a-9,s1)
is in B's near stem. The reflected south strip is B's lower bar at
row a-13, columns s1+1 through C-1. The same three C-column R/B
points supply the reflected west guards. This again forces the cavity
contradiction, excluding EVERY tight d4 branch at all far lengths.

Consequently, conditional on a complete extension containing the specified
first deep B, the actual t0 owner necessarily has

    d=4, 6<=L<=v+10, 4<=f<=z-8, all even.

Only geometric necessity is asserted; complete extendibility of these
remaining prefixes is OPEN. Since epsilon0, its exact marginal is L-1
and the joint gain is u+v+L+24>=u+v+30>=54. The strengthened bound is
unchanged, while the residual actual-owner classification is narrower.
The two reflected exclusions add no source credit or physical receipt.

## Evidence and remaining scope

- [Full-original controls](../develop/check_secondary_ten_root_cavity_exclusion.py).
- [Scoped local Lean](../formal/SubQuorum/SecondaryTenRootCavityExclusion.lean).
- [Validation and review state](../output/secondary-ten-root-cavity-exclusion-validation.json).

The general U proof covers every legal breadth and both leg lengths. Finite
U samples check its explicit witnesses. The four-row rotor table is a
fixed finite catalogue, independent of grid or chain size. The full H3
controls check original support absence and every retained guard site.
Scoped Lean establishes the explicit cavity collisions, guard transfer and
conditional stronger arithmetic; the catalogue/completeness adapter is
an ordinary written proof. The independent triple audit submitted before
this deduction does NOT cover the cavity exclusion or the bound54.
The initial cavity audit itself covers the general cavity and first d8
application, not the subsequent two reflected applications. Those have
their own written coordinate proof, full-original controls and scoped
Lean guard-transfer checks; independent follow-up is still needed.

Further actual owners may still have negative signed interactions. No
global monotonicity, packing of overlapping root triples, arbitrary-grid
catalogue exhaustion, global5/6 improvement or grid equality is claimed.
Next study the remaining nontight d4 owners and their newly forced supports
or a single full-family nonreused allocation. The submitted manuscript
is preserved.
