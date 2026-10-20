# A positive bottom owner forces at least two reserve units

20 October 2026. This gives an unbounded-clearance compensation obstruction
for the remaining complete-source AA closure problem. At the forced bottom
point of an unpaid full-chain double, an original positive owner would force
R>=2. Therefore the R=1 residual cannot close that point with ANY positive
source, including an arbitrary one-mark positive. Further negative-source
closure remains open, as does the unrestricted coefficient-one/grid target.

## 1. Hypotheses and theorem

Keep all complete-source assumptions and original ownership of
WIDTH_SIX_BOTTOM_OWNER_AND_WRAPPING_OBSTRUCTION.md, and the accepted
support-chain common-pool theorem. In particular every original support
outside final P remains selected, original endpoint sets are disjoint,
selected occupied degree is at most one, R is a nonnegative integer, and

    2R=A+U0+Z0+H, U0+H>=X.

A counts actual activated original positive terminal occurrences. X counts
actual original positive legs whose terminal is unactivated and which have
at least one consumed original exterior regular selection, INCLUDING the
bar-end selection with chain index zero. The accepted common-pool theorem
counts each such leg once and separates its payment from other resource
families. These definitions are essential below.

Normalize O=U(6,a,b), left terminal unactivated, right terminal activated,
and its longitudinal incoming phase11 owner L with tip(2,2), incident h
and h<=a-4. Let p=(h+3,2). As proved in the bottom-owner lemma, p is an
original O support forced into P and its original owner F differs from O,L.

**Theorem.** If F is an original positive U, then A+X>=3 and R>=2.
There is no upper bound on a-h, any source dimension or the number of
sources. No assumption is made that F is one-mark or double-marked.
Consequently a remaining R=1 AA residual has a negative U owner at p:
positive owners are excluded here, and all rotor roles are excluded by
the fixed original endpoint/retained-support stencil of the bottom lemma.

## 2. Translate the forced point and classify positive roles

Translate p to(0,0), keeping the original physical aligned tile partition.
Put g=a-h, even>=4. The following facts persist:

- O has original endpoints(r,-1) for 0<=r<=g-3.
- O's retained beyond-tip support is(g-2,-1).
- L's original bar occupies rows-2,-1, columns0..vL-1, with vL>=6.
- q=(g-2,0) belongs to NO original endpoint or support set.

The last statement follows because the retained beyond-tip support already
has persistent neighbor(g-3,-1). Any additional occupied neighbor q would
violate final selected feasibility. An original support at q would either
be retained or consumed into P; both are forbidden.

North and west of p are foreign original endpoints. An original U endpoint
there can only be a terminal with predecessor east/south, or an outer
upper-bar corner whose two own endpoint neighbors are east/south. At the
physical parity of p (odd row, even column before translation), only two
of these roles have original positive charge:

    terminal: predecessor south, bar west;
    upper corner: bar south, incident stem east.

This is a parity classification, not a dimension search. The Lean theorem
positive_bottom_role_catalogue checks it for arbitrary even dimensions and
all eight isometries directly from the original endpoint predicate and
positiveParity. To relate that predicate to the physical model, an original
positive image preserves aligned2x2 tiles. For a nontransposed image the
anchor-coordinate remainders must be(1-flipRow,flipColumn), and for a
transposed image they must be(flipRow,1-flipColumn), since p has physical
parity(1,0). These are exactly positiveParity; the signs have no effect on
an anchor remainder modulo two. Renaming the far terminal as the near
terminal interchanges the original legs without changing the physical map.

The positive terminal alternative is impossible. Write its incident height D.
Its exact near stem runs down from row0 through D, and its bar goes west in
rows D-1,D. Avoiding q gives D<g-2, hence D<=g-4 by evenness. The westward
bar then contains(D-1,-1), an original endpoint of O, because D>=4 and
D-1<=g-5. This contradicts original endpoint disjointness. The universal
coordinate contradiction is westward_terminal_cannot_fit in Lean.

Thus F has the positive corner form, after naming its incident stem:

    F(r,c)=(c-1,r), image of U(w,D,f).

Its two-column bar occupies rows0..w-1, columns0,1. Its near incident
stem points east. The same description works for independent D,f>=4.

## 3. Two different original exterior selections are consumed

First w<=g-4. If w>=g, q is an original F bar endpoint. If w=g-2,
q is the original exterior far bar-end support F(0,w+1). Both contradict
the forbiddenness of q; evenness leaves w<=g-4. This endpoint/support
bound is positive_vertical_bar_fits_clearance in Lean.

The two original F exterior bar-end supports are

    sNear=F(0,0)=(-1,0),
    sFar =F(0,w+1)=(w,0).

sNear is an original endpoint of L and hence consumed. sFar has persistent
original F anchor(w-1,0), and also neighbors the original O endpoint(w,-1),
since0<=w<=g-4. The anchors are distinct. Therefore sFar cannot remain
selected and must be consumed into P as well. Both supports belong to
different original positive legs of F, even if the endpoints consuming them
belong to the same additional source.

## 4. Count occurrences through the existing common pool

For EACH of those two original F legs, either its terminal is activated,
giving an A occurrence, or it is unactivated and its consumed exterior
bar-end support gives an X occurrence. The chain index-zero case belongs
to X by its definition. The legs are distinct, so these are two distinct
original A/X occurrences. The accepted X theorem routes them without
reusing an existing witness; nothing here adds a second independent credit
for the same original leg or support.

O's activated right terminal gives another A occurrence. Since F!=O, this
occurrence differs from both F-leg occurrences. Thus

    A+X>=3,
    2R=A+U0+Z0+H>=A+X>=3,
    R>=2.

The final step uses integer R, not rounding a separately owned half-unit.
The two new Lean budget statements check all four activation choices and
the common-pool implication. No claim is made that F creates two fresh
H units: activated legs are charged through A, unactivated ones through X.
This is the precise mechanism preventing duplicate use of a resource.

## 5. Scope, verification and next question

This excludes an entire unbounded closure mechanism in the R=1 residual.
It does not exclude the negative phase01/10/11 U owners allowed by the
bottom-owner role catalogue at larger clearance. Nor does a new negative
owner by itself provide a fresh compensation unit. A source may still
participate in both double staircases through different original tips.
The full finite closure and arbitrary-grid targets remain OPEN.

Five new declarations in formal/SubQuorum/WidthSixBottomOwner.lean check
the universal positive role catalogue, westward-terminal collision,
positive-bar endpoint/support clearance, four activation/exterior choices,
and R>=2. The full file now has eleven declarations. Physical positive-phase
normalization, source support retention and the accepted A/X routing theorem
are written dependencies. Finite controls in
develop/check_positive_bottom_owner_reserve.py reconstruct original positive
source images and both distinct exterior supports; they supplement the proof.

The bottom-point route was explored locally, including its upward wrapper
and clearance-four exclusion. The unbounded positive-owner A/X obstruction
was proposed in research follow-up54d0581e, completed at
2026-10-20T05:50:36.725UTC, observed gpt_6/pro,20781characters, and is
reconstructed above from complete sources. Its original streaming observation
ended with unexpected EOF; the SAME task's terminal response was retrieved.
No complete stream or exact stream/terminal match is claimed. The response
also proposes boundary-stop and cross-core obstructions; those are research
leads, not established results in this note. An independent audit is separate.

All eleven declarations in the final Lean file compile/build and pass
individual axiom audits, including the five new declarations above.
The new five use only propext, Classical.choice and Quot.sound as applicable,
without sorry/native_decide. The executable controls pass131584 source roles
with342 surviving positive-corner profiles, all carrying the two distinct
forced exterior selections; all248 parity-compatible activation/pool budgets
give R>=2. No complete feasible new physical fixture is claimed.
See output/positive-bottom-owner-reserve-formal-check.json and
output/positive-bottom-owner-reserve-controls.json. Independent audit
a7e79d96/conv_0c83fc4e281c2a91/original83141 is live; no ACCEPT verdict
for this additional theorem is claimed yet.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
