# Short-leg double marks inject into unweighted defect occurrences

20 October 2026. We prove a single-use geometric witness bound for the
nonexceptional double-marked sources in the complete U/rotor model. It
excludes fourteen of the seventeen symbolic defect patterns in the first
connected two-demand, one-reserve candidate. It does not yet exclude the
three remaining patterns or prove unrestricted joint allocation.

## 1. Definitions and statement

Keep all complete-source assumptions, actual canonical marks and original
ownership from ENDPOINT_COMPONENT_RESERVE_AND_CONNECTED_OBSTRUCTIONS.md.
All original supports outside final P are retained; every final selected
vertex has at most one occupied neighbor. No source is truncated. Negative
dimensions and rotor phases are arbitrary. A positive is nonexceptional
when its normalized dimensions satisfy either w=6 with arbitrary even
a,b>=4, or w in {8,10} with a,b in {4,6}. Let d count ACTUAL doubly marked
nonexceptional positives. Let A,U0,Z0,L1,L2bar,L2mutual,L3 be the exact
geometric counts from EXACT_GEOMETRIC_EVENT_RESERVE.md, and put

    F=L2bar+L3, E=U0+Z0+L1+L2bar+2L2mutual.

Thus F counts the nonfull irregular-pair and mixed-triple defect TILES
without weight-two multiplicity; the exact identity is D=2R=A+F+E.

**Injection theorem.** There is an injection from these d positive sources
into the disjoint union of the A original activated positive-terminal
occurrences and the F actual irregular-pair or mixed-triple defect tiles. Consequently

    d <= A+F,
    d+E <= D.                                (1)

The occurrences and tiles are the ones already present in the exact
identity. No ambient half-areas are added, and no parity is rounded per
source. All claims below apply before imposing D=2 or connectedness.

## 2. The forced short-leg pair tile

Consider a doubly marked nonexceptional positive with both terminals
unactivated and both marked gates occupied. Normalize it to U(w,a,b),
with bar in rows0,1. Width6 is impossible: the occupied marked gate on a
shorter/equal leg would activate that terminal by the occupied-gate lemma.
Thus w is8 or10 and both heights are4 or6.

The unactivated gate roles and the transverse-footprint argument in
SATURATED_TWO_GATE_GEOMETRY.md do not require zero reserve. Phase10
activates a terminal, and every remaining gate is transverse or a phase11
longitudinal terminal. Two DISTINCT transverse owners overlap at(2,5).
For a COMMON owner the only forms are the upright and inverted nested U.
An upright common owner requires both heights>=8 using original supports
alone, hence is impossible here. An inverted common owner is longitudinal
on both sides. Therefore at least one of the two gates is longitudinal.

Reflect sides if necessary. At the left gate u=(2,2), let h be the incoming
terminal's incident height. The selected positive tip support(a+1,1)
forces q=(a+1,2) to be finally blank. Endpoint disjointness and the incoming
stem give h<=a-2 without any full-tile assumption. Since h>=4 and
a in {4,6}, necessarily a=6 and h=4.

The incoming source has near stem column2, rows2 through6, and bar rows5,6
running right from column2. Its outside corner tile is

    Q={6,7} x {2,3}.

Its original profile is exactly {(6,2),(6,3)} with no selected support:
an irregular2P0T pair. The corner q=(7,2) is blank, so Q is nonfull.
It has either just that pair, contributing one L2bar tile, or the third
endpoint(7,3), contributing one L3 tile. It is therefore in F. The chosen
positive has NO original endpoint or support anywhere in Q.

The fourth corner r=(7,3) cannot be finally selected. If it were a
retained support, its original anchor is occupied. An anchor different
from t=(6,3) would give r two occupied neighbors. An anchor equal to t
would identify its source with the incoming pair owner by endpoint
disjointness, but that owner has no original support in Q. Thus r is
blank or an endpoint, as required by the two final profiles above.

Translate this configuration so p=(6,2) becomes(0,0). Its fixed local data
are an original negative pair at p=(0,0),t=(0,1), original negative
endpoints(-1,0),(-1,1),(0,2), a positive endpoint z=(0,-1), and a finally
blank corner q=(1,0). These data will prevent either kind of witness reuse.

## 3. Distinct positives cannot use the same forced tile

A nonfull tile cannot contain two disjoint original pair profiles. Hence
if two forced constructions produced Q, their pair has the same original
owner. In a complete U of width>=6, the two endpoints of this outside bar
pair distinguish its corner: p has original endpoint degree two (stem and
bar), and t has degree three. The source fixes the stem direction and the
direction along the bar. Each forced construction must therefore have the
same p, bar direction and external positive endpoint z=p-(bar direction).
Both chosen positives would contain z. Original endpoint disjointness
then makes them the SAME original source. Selecting one forced tile per
source is injective, including when an incoming source owns both gates.

This uses original endpoint degrees within the one pair owner, not final
occupied degrees. An extra endpoint elsewhere in Q cannot change them.

## 4. Forced tiles cannot also pay blank-gate marks

Suppose Q were the canonical donor tile of any blank-gate marked positive
source V. A canonical donor has an original selected corner x, an adjacent
anchor outside Q, a diagonal opposite corner, and its endpoint protector
outside Q beyond that opposite corner. There are exactly eight orientations,
two for each choice of x. Check them in the translated coordinates above:

- If x=(1,0), it is the finally blank q, impossible for an original support.
- If x=(0,1), its outside anchor is either(-1,1) or(0,2), both endpoints
  of the original negative owner. Endpoint disjointness excludes V.
- If x=(0,0), its anchor is either(-1,0), again negative, or z=(0,-1).
  In the latter case V must be the chosen positive because it contains z.
  That positive has no original support in Q, contradicting x in its T.
- If x=(1,1), an anchor at(1,2) gives gate(0,1), already an endpoint and
  therefore not blank. The other orientation has anchor(2,1), gate(1,0)
  and endpoint protector z=(0,-1). Again V is the chosen positive, which
  has no original support in Q. This is impossible.

These eight orientations exhaust a signed permutation of the canonical
square pattern; no bound on V's dimensions is used. Thus a forced pair
tile cannot coincide with ANY marked canonical tile having a blank gate.
Excluding only repeated forced tiles would not establish the theorem:
this cross-type exclusion is essential.

## 5. Constructing the injection and its consequences

Partition the d sources in this order. If one of its own positive terminals
is activated, choose one such source-labelled occurrence in A. Different
positive sources give different occurrences, even in the same physical tile.
Otherwise, if it has a blank-gate marked side, choose one such canonical
tile. The established canonical donor-tile injection makes these tiles
distinct. More precisely, the blank-gate lemma gives an original phase11
U pair2P0T or2P1T in the tile. With2P0T the final tile is either that
pair alone (L2bar), or a mixed triple (L3). With2P1T its original support
must be consumed, making a mixed triple (L3). The gate stays blank, so
fullness is impossible. Thus the tile lies in F; it is never L1 or
L2mutual. This sharper profile fact is needed for the three-pattern result.
For all remaining sources Section2 supplies a forced pair tile in F.
Section3 makes those choices distinct, and Section4 separates them from
all chosen blank-gate tiles. Finally A occurrences and F tiles are disjoint
classes in the exact reserve identity, even if coordinates coincide.
This proves the injection and both inequalities in(1).

For arbitrary positive dimensions let L count exceptional positives as in
the preceding notes. Since n2<=d+L, (1) also gives

    n2+E <= D+L.                             (2)

The result holds independently on each actual endpoint component, because
the complete-source restriction preserves these marks and geometric counts.
The reserve R=S+C-Kirregular is integral by its original source ledger;
the identity D=2R alone would give only half-integrality. With that
ledger integrality, a failing component with L=0 satisfies

    n0+R+1 <= n2 <= 2R-E.                   (3)

In particular a failing component with R=1 has EXACTLY n0=0,n2=2,
U0=Z0=L1=L2bar=L2mutual=0. The previous seventeen D=2 patterns reduce to
exactly three symbolic possibilities:

    A+A, A+L3, L3+L3.

Each notation means two distinct resources. In L3+L3 they are necessarily
different physical tiles. Separately labelled A occurrences, or an A
occurrence and a tile, may have coincident coordinates. The two weight-two alternatives and every pair
involving U0, Z0 or L1 are excluded by the universal injection, not enumeration.
The three remaining patterns are necessary alternatives, not realized fusions.
Every L3 tile used by this injection has a pair-plus-singleton original
partition; a three-singleton L3 tile cannot be a witness. Under this
extremal equality every activation and nonfull defect tile is
used once by the injection; there can be no unused occurrence in those
classes. There may still be arbitrarily many one-mark sources and zero-
defect full tiles; no source-count or negative-dimension cutoff is inferred.

Joint allocation would require the stronger 2(n2-n0)<=D. Inequality(1)
does not prove it, nor does a negative allocation margin imply a negative
ambient grid slack. The next task is the simultaneous connected geometry
of those three patterns, together with exceptional dimensions and higher R.

## 6. Equality forces further simultaneous restrictions

In the nonexceptional failing R=1 component, d=D=A+F=2. The constructed
injection therefore uses EVERY resource in A and F. This concerns the
labelled finite resource pool, not a rounding of its weighted sum.

Every activation belongs to a double-marked source; otherwise its original
source label cannot be the chosen activation of either demand. Each such
activated double has exactly one activated terminal. It cannot have any
blank-gate mark: that tile cannot be another source's canonical blank tile,
and Section4 prevents its use as another source's forced tile. Since its
source already chose A, the tile would be an unused resource in F.

The same argument shows that every blank-gate mark belongs to a double
with no activated terminal, and each such source has at most one blank-gate
mark. A one-mark positive with a blank gate would likewise leave an unused
tile. These exclusions use the established injection of ALL canonical
tiles, rather than just those selected for the proof.

If a nonactivated double has both gates occupied, it is a width8/10,
height4/6 positive. Each longitudinal gate gives the forced tile of Section2.
If both gates were longitudinal, their tiles would be distinct: otherwise
the same original corner p and incoming stem direction s reconstructed
in Section3 give the same gate u=p+4s, because the incident height is4.
In the normalization p=(6,2), s=(-1,0), so u=(2,2). The two gates differ.
Each tile can serve only
this positive among forced witnesses, and neither can be a blank witness.
One would therefore remain unused. Thus exactly one gate is longitudinal
and the other transverse, and their original owners are distinct. In
particular the common inverted owner cannot occur in this extremal case.

Finally, every L3 tile in the three remaining alternatives has exactly two
original owners, a pair and a singleton. Three-singleton L3 tiles are not
in the image of either F-witness branch and would remain unused. These
are additional necessary simultaneous-geometry conditions. They do not
assert that any of the three alternatives has a complete realization.

## 7. Validation scope

The companion verifier reconstructs actual positive terminal activations,
canonical marks, and forced tiles in complete physical fusions, checking
cross-type disjointness before counting. Separate role controls check all
eight donor orientations and the original corner reconstruction. Finite
controls discover mistakes and exercise the written argument; they cannot
replace Sections2--5 or realize/exclude the remaining connected patterns.

The Lean companion checks the local eight-orientation certificate,
finite-list injection cardinality, weighted-count consequences and exact
three-pattern reduction under the stated geometric adapters. Source-role
normalization, forced-pair ownership and complete-fusion adapters remain
the written proof above. Execution and independent review status are
recorded separately; no inherited review verdict is claimed.

Controls PASS on664 complete physical images, including128 assigned
forced-pair witnesses and24 images with several such witnesses. This
fixture set does not exercise a selected nonexceptional A/blank witness;
those branches use the established source-label/canonical-tile injections.
All eight cross-type donor orientations and48 original corner controls
pass. The seventeen symbolic D2 patterns leave three under the proved bound.
All eleven scoped Lean declarations compile locally with Lean4.33.0 and their
individual axiom audits pass without sorryAx/native_decide. See the controls
and formal-check JSON receipts. Independent review0b750ade completed
ACCEPT for the earlier weaker six-pattern version; review0cd69c94
completed ACCEPT for the current three-pattern bound and the saturation
consequences, conditional on the stated complete-source dependencies.
Their original streams ended with DONE and match the task API responses
exactly. Both reviews concern written arguments; neither executed Lean
or the checker or freshly retrieved every dependency. The present note
includes the requested reserve-integrality, retained-support and gate-
reconstruction clarifications. The stronger two-slot theorem has a
separate review and does not inherit these verdicts.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
