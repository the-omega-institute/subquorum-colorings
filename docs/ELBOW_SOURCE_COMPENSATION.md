# Thick elbows: freezing, partial phase and the cost of adding a source class

19 October 2026. This note proves an all-width, all-height positive bent
receiver family beyond the prescribed straight-chamber sources. Its partial
phase is nonnegative in both strip directions. A transverse band through the
turn earns at least one unit even when neither physical tip belongs to the
region. Full phase is at least two, sharply. Adding these receivers to a
mouth/channel theorem also costs their actual whole charge: their phase must
not be treated as free extra supply.

These statements concern the explicit elbow matching and retained supports
below. They do not classify arbitrary positive bends or prove the universal
grid inequality. Finite controls and scoped Lean results have separate scopes.

## 1. Coordinates, matching and hypotheses

Use relative coordinates with physical squares starting at even rows and odd
columns. Thus row bands are {2i,2i+1}, column bands {2j-1,2j}. A translation
to actual even/even tiling has even row offset and odd column offset. Let
w>=6 and h>=4 both be even. The complete endpoint component is

    H=({0,1} x {0,...,w-1})
      union ({2,...,h-1} x {w-2,w-1})
      union {(2,0),(h,w-1)}.                         (1)

The actual matching consists of

- (0,j)--(0,j+1), j=0,2,...,w-2;
- (1,j)--(1,j+1), j=1,3,...,w-3;
- (1,0)--(2,0);
- (r,w-1)--(r+1,w-1), r=1,3,...,h-1;
- (r,w-2)--(r+1,w-2), r=2,4,...,h-2.

Retain the following selected sites:

    (0,-1),(0,w),(2,-1),(3,0),(h+1,w-1),
    (r,w),   r=2,4,...,h,
    (r,w-3), r=3,5,...,h-1.                         (2)

All these vertices lie in the ambient grid. For the canonical construction
all unlisted sites are blank. More generally allow any feasible exterior:
old selections see at most one occupied neighbor; H is the complete endpoint
component with the matching above; all supports (2) remain selected. Other
components must satisfy the surrounding theorem's hypotheses. In particular
their endpoints cannot be added to H without leaving this family.

The matching partitions H. The canonical supports each see exactly their
prescribed endpoint and are pairwise nonadjacent. The restriction w>=6 keeps
the short-tip supports separate from the inner-leg supports, including h=4.
Thus the blank-exterior construction is feasible for every parameter pair.
Additional selections can only be made subject to feasibility.

## 2. Freezing and whole receiver charge

Use the retained-mate rule: an endpoint is frozen if it sees two old
selections, one selection and the mate of a frozen endpoint, or the mates
of two frozen endpoints. The two retained neighbors must be distinct.
The general frozen-exclusion theorem then rules out every simultaneous
promotion bundle, including bundles using other components.

**Freezing theorem.** Every endpoint of (1) is frozen under (2).

Proof. Denote the short tip by L=(2,0), the chamber endpoints by
T_j=(0,j), B_j=(1,j), and the two leg columns by A_r=(r,w-2),
R_r=(r,w-1). Both L and R_h have two selected neighbors, so are frozen.
Descend r=h-2,h-4,...,2. Endpoint R_r sees its selected outer support
(r,w) and R_(r+1), whose mate R_(r+2) is already frozen. Hence every even
R_r is frozen.

T_0 sees (0,-1) and B_0=mate(L), so is frozen. The left chamber wave is

    T_(2i) -> B_(2i+1) -> T_(2i+2).

The first step uses the retained B_(2i)=mate(B_(2i-1)) and
T_(2i+1)=mate(T_(2i)); at i=0 replace the first frozen predecessor by L.
The second uses T_(2i+1)=mate(T_(2i)) and
B_(2i+2)=mate(B_(2i+1)). Stop at T_(w-2); no nonexistent final step is used.
This freezes all even top and odd interior bottom endpoints.

At the right side T_(w-1) sees (0,w) and B_(w-1)=mate(R_2), so is frozen.
The reflected wave first freezes B_(w-2), using B_(w-1)=mate(R_2) and
T_(w-2)=mate(T_(w-1)), and then alternates leftward. It freezes all odd
top and even interior bottom endpoints. The two remaining chamber corners
B_0 and B_(w-1) now each have two retained chamber neighbors: respectively
T_0=mate(T_1), B_1=mate(B_2), and
T_(w-1)=mate(T_(w-2)), B_(w-2)=mate(B_(w-3)). They too are frozen.

For odd r=3,5,...,h-1, A_r sees selected (r,w-3) and R_r=mate(R_(r+1)),
so these A_r are frozen. A_2 sees B_(w-2)=mate(B_(w-3)) and
R_2=mate(B_(w-1)), and is frozen. Now R_3 sees R_2 and A_3=mate(A_2),
so is frozen. For h>4 continue the zigzag
A_4,R_5,A_6,R_7,...,A_(h-2),R_(h-1); for h=4 the two seeds finish the leg.
At A_(2i+2), the retained neighbors are A_(2i+1)=mate(A_(2i)) and
R_(2i+2)=mate(R_(2i+1)); at R_(2i+3) they are
R_(2i+2)=mate(R_(2i+1)) and A_(2i+3)=mate(A_(2i+2)).
All named neighbors are distinct and grid-adjacent. This exhausts H. QED.

The physical receiver has

    |H|=2w+2h-2,  |M_H|=w+h-1,
    |R_H|=w/2+h+1 squares,  |T intersect R_H|=h+4.

Its whole corrected charge is therefore

    rho_H=|T intersect R_H|+|H|/2-2|R_H|=1.         (3)

These counts hold in every feasible exterior. A nonendpoint receiver corner
is either adjacent to two H endpoints, forbidding its selection, or adjacent
to a prescribed selected support already seeing its H endpoint, forbidding
any occupancy. Completeness of H excludes foreign endpoints at corners
adjacent to H. Thus extra exterior data cannot change the receiver labels.

## 3. Exact two-direction band tables

Throughout this section C is an admissible rectangular union of complete
physical squares. For a horizontal shift its extreme columns must be
endpoint-free, and for a vertical shift its extreme rows must be endpoint-free.
Trim those columns or rows, respectively, in the shifted partition. Only
complete physical bands are retained. The band paths encountered below must
be contained in full; the endpoint-free extremes imply this path-completeness
condition by the connected-path arguments given below. No statement here
is made for arbitrary nonrectangular square unions or a cut transition path.

For such a rectangle C let E_C(H) be the sum of
t+p/2-2 over its squares containing H endpoints. Define E'_C(H) using the
partition shifted one site in the strip direction, with the corresponding
endpoint-free extreme columns or rows trimmed. Only squares containing actual H endpoints are
included. Set Gamma_C(H)=E_C(H)-E'_C(H). These are raw excesses, not
corrected partial matching charges or additional donor supplies.

First take a horizontal shift. In any complete physical row band, the
chamber and full leg have zero raw excess in both phases. The actual short
tip band {2,3} and bottom-tip band {h,h+1} each contribute +1/2 physically
and -1/2 shifted. Thus, for any admissible rectangle with endpoint-free
extreme columns,

    Gamma_C(H)=number of its actual physical tip tiles in C.    (4)

The two disconnected paths in band {2,3} cause no extra term: the left tip
and right full-leg path have separate zero/nonzero contributions. Any path
that meets C must be complete laterally, or would contain an endpoint on
an extreme column. Top and bottom cuts only select genuine row bands.

For a vertical shift, consider the physical column bands below. Upper-flank
selections are at row -1 and lower-flank selections at row 2. Let a_j,b_j
be the numbers selected on the corresponding two-site flank pairs; each is
at most one, since both sites already neighbor chamber endpoints.

| Relative column band | Physical raw | Shifted raw | Gain |
| --- | --- | --- | --- |
| {-1,0} | 1/2 | -1/2+a_0 | 1-a_0 |
| {j,j+1}, j=1,3,...,w-5 | 0 | -2+a_j+b_j | 2-a_j-b_j |
| {w-3,w-2}, transition | 0 | -2+a_* | 2-a_* |
| {w-1,w} | 1/2 | -1/2+a_end | 1-a_end |

Here a_0,a_end are individual optional upper selections, hence zero or one.
For completeness the transition shifted squares, in longitudinal order, are:
top cap raw a_*-1; junction rows {1,2} with three endpoints and no selections,
raw -1/2; interior leg squares raw zero; bottom cap rows {h-1,h} with one
endpoint and its inner selected support, raw -1/2. This is valid also when
h=4, when no intermediate leg squares occur. Its physical squares all have
raw zero. Thus the transition gain is at least one.

Every endpoint path within a listed column band is connected. Endpoint-free
extreme rows of C force an encountered path to lie wholly inside C, so the
full band table applies even if H escapes C through its other boundaries.
Each encountered gain is nonnegative. In particular,

    Gamma_C(H)>=0;
    Gamma_C(H)>=1 if C meets the full transition-band endpoint path. (5)

The transition rectangle with relative rows -2,...,h+1 and columns
w-3,w-2 contains neither actual physical tip tile, yet satisfies the latter
inequality. This is a credit from the turn, not an invented cut endpoint.
Tile-preserving rotations/reflections give the other directions.

## 4. Sharp whole phase

Let A be the total selected count at (-1,j), j=0,...,w-1, and B the count
at (2,j), j=1,...,w-4. Summing the perpendicular table gives

    Gamma_full(H)=w-A-B>=2.                         (6)

Indeed A<=w/2. Site (2,1) sees H endpoints (2,0),(1,1), so is not selected.
Pair (2,2),(2,3), then (2,4),(2,5), etc., leaving the last site w-4 if
necessary; each pair has at most one selection. Thus B<=(w-4)/2.
The existing whole-flank arithmetic lemma also proves the final bound from
these two inequalities. Parallel full phase is exactly two by (4).

The bound is attained by adding upper selections (-1,j) for even j through
w-2 and lower selections (2,j) for even j from 2 through w-4. Each sees
exactly its adjacent chamber endpoint; none neighbors another new selection
or any old support. The extreme new lower sites are separated from the
short-tip and inner-leg supports by a blank column. Hence this is feasible
for every w,h, gives A=w/2,B=(w-4)/2 and perpendicular phase exactly two.

## 5. The extra-source charge must be paid

The accepted channel raw identity extends to these elbow components by
adding their nonnegative Gamma_C to G_C. Endpoint-square ownership stays
unique: adjacent endpoints share their component; a singleton physical or
shifted occurrence has a retained support in its square excluding a foreign
opposite corner. The table checks explicitly cover the two elbow tips and
perpendicular caps. Other endpoint-square patterns have adjacent H endpoints.

However, the original doubled mouth ledger cannot be reused unchanged if
elbows are added as new positive receivers without their own root mouths.
Let B_L be the old prescribed long sources, B_E the new elbows. Assume all
remaining receivers are nonpositive and retain the normalization hypotheses.
The whole receiver ledger is

    Delta=-B_L-B_E+D_all+E,       E>=0.

Use only the original long-source mouths for m_Q, and let A be the sum of
their nonnegative additional source phases, now including elbow contacts.
The existing strip calculation gives the corrected exact ledger

    2Delta=F+A+Dprime+Dsingle+2R-2B_E.              (7)

To verify the new term directly, original strip deficits sum to
2B_L+F+A+Dprime. Physical mouth incidence gives
2D_all=(sum of strip deficits)+Dsingle+2R_noP. Substitute into the whole
receiver ledger, with R=R_noP+E. Each elbow contributes its actual charge
one before doubling, regardless of where its phase is encountered.

For channels with nonnegative weights satisfying the original pointwise
capacity sum_(j:Q in C_j) w_j<=2-m_Q on every positive physical donor,

    2Delta>=F-2B_E+
      sum_j w_j(2-delta_j+G_L,j+G_E,j+Phi_j).       (8)

The proof uses the same single physical donor account as the accepted
channel theorem and (7). In particular, phase in an old mouth and phase in
a channel certify physical deficits; neither can be added again as supply.
If sum_j w_j G_E,j>=2B_E, the old weighted certificate is recovered with
the new elbows present. A fully enclosed elbow in a weight-one channel
supplies its two-unit tax sharply. A tip-free transition contact supplies
only one; covering every elbow merely once in such a band is insufficient.
Several contacts can pay it only if the actual donor capacities also hold.

Thus (8) is a new coefficient-one certificate for the stated extended class,
whenever its right side is at least -1 and Delta is integral. It improves
5/6 to one on that class; it is not a universal 5/6 improvement. Omitting
-2B_E would be a ledger error, not evidence against the global target.

## 6. A uniform mixed family, including occupied terminal bands

Take even W>=32, root depth d>=1, even elbow height h>=4 and wall half-lengths
ell_L,ell_R>=h/2+2. Start with the root source, walls and zero-payment mouth
filling of Section 4 of `COMB_CHANNEL_COMPENSATION.md`, with y=2d+4.
Omit its horizontal comb blocker. Put the width-six elbow (1)-(2) at origin
(y+4,13), with no optional flank selections. This is the prescribed positive
phase, since y+4 is even and 13 odd. No elbow root mouth is introduced.

The elbow's complete support footprint has columns 12,...,19 and rows
y+4,...,y+h+5. The wall inward supports are in columns 10,21; the root's
vertical arms are in columns 3,W+2. Thus each interface has a blank separating
column. The elbow begins at least three rows below the last mouth filling
row y+1. Its bottom endpoint row y+h+4 is at most
s=y+2min(ell_L,ell_R), and its final support is at most s+1. These bounds
also cover h=4 and the minimal wall lengths. The feasibility and freezing
proofs for each complete component therefore apply without cross-component
collisions. At the minimum wall half-length the elbow's bottom tip occupies
the channel's terminal band.

Write ell=min(ell_L,ell_R), delta=0 for equal ends and one otherwise. The
root mouth is unchanged and has zero physical/shifted deficit and F=-2.
There is exactly one extra positive receiver, B_E=1. The elbow is contained
and parallel, so its channel gain is exactly two. The wall flux inside C
is zero. Direct partition counts give

    D_C=10ell-2h-6-delta,
    Dprime_C=10ell-2h-10.                           (9)

Indeed C has 6(ell+1) physical squares, of which h+4 belong to the elbow
receiver. Its no-endpoint squares contain 12 first-band mouth selections,
2(ell-1) intermediate wall supports and delta continuing-wall corners.
The elbow's h+4 supports are all in its physical receiver and contribute
no further no-endpoint selections. Hence the no-endpoint square count is
6ell-h+2 and its selected count is 2ell+10+delta, proving the first formula.

The trimmed shifted partition has 5(ell+1) squares, including h/2+4 elbow
endpoint squares: three chamber squares, a tip and leg square in band
{2,3}, (h-4)/2 intermediate leg squares, and the bottom-tip square. The
remaining squares have ten first-band mouth selections and h+2 elbow
supports. These are the three upper/left exterior supports, h/2 outer
even-row supports and h/2-1 inner odd-row supports. Thus its no-endpoint
count is 5ell+1-h/2 and selected count h+12, proving the second formula.

Every positive channel donor is outside the zero-payment original mouth,
so it has residual multiplicity capacity two. With channel weight two,
the extended inequality, including the extra-source tax, gives

    2Delta>=-2-2+2(2-delta+2)=4-2delta,
    Delta>=2 for aligned ends, Delta>=1 otherwise.             (10)

The unadjusted old ledger would instead exceed the actual 2Delta by exactly
two units: all receivers here have charge zero except the root and elbow,
so Delta=D_all-2, while -2+2D_all=2Delta+2. This is a checkable failure of
blindly retaining the old ledger. It is repaired by (7) and is not a failure
of the coefficient-one target. Repeating the weight-two channel would also
overdraw actual positive donors; the pointwise capacity rejects that reuse.

## 7. Verification scope

`develop/check_elbow_sources.py` independently constructs the actual matching,
checks feasibility and complete frozen certificates, recomputes whole charge
and both raw partitions, tests all band tables in 60 parameter cases, all
317 feasible small flank subsets and 32 greedy exteriors, and checks 11,928
admissible partial rectangles, 48 mixed channel cases and eight symmetry
images. Sharp full phase
and a tip-free transition contact are checked separately. The smallest sharp
witness is preserved. These are controls, not the all-parameter proof above.

The separate Lean module formalizes a retained-mate two-chain wave, the blank
corner forced by a three-endpoint junction, the conditional transition-band
raw arithmetic and the extended residual ledger with its explicit elbow tax.
Coordinate matching coverage, the full freezing construction, geometric band
tables and source/channel interfaces remain written proofs. Arbitrary positive
bent receivers, sufficient channel coverage and grid triple equality remain
open. Existing manuscripts are unaffected.
