# Escaping prescribed sources have nonnegative phase, but no automatic source credit

19 October 2026. The cavity ledger extends to arbitrary partial contacts
with prescribed positive long sources, in either direction. Such contacts
introduce no negative phase term. However, counting every source that
touches a cavity as supplying two units is false by an arbitrarily large
amount: a uniform feasible frozen family has a partial sources in one
root cavity and physical deficit exactly two, for every a>=1.

This extension reuses the established row-band source tables. The new
statements are their complete cavity aggregation, exact source-credit
criterion and an all-parameter sharp obstruction. It is not a new proof
of the row-band lemmas or the unrestricted grid inequality.

## 1. Hypotheses and exact phase

Use the fixed terminal representative, physical tiling, actual matching
and whole-receiver ledger

    Delta=mn/2-|T|-|M|=-B+D_all+E,       E>=0.

There are B prescribed complete positive long sources, each of whole
corrected charge +1, with even width at least eight, positive physical
phase, the prescribed matching and frozen supports. A source may point
in any tile-preserving direction. Other final receivers are nonpositive.
Every endpoint meeting a chosen root cavity C belongs to one of these
prescribed sources or a prescribed complete straight comb. Complete
components may escape C. No other endpoint shape is allowed there.

Put a horizontal downward root in the relative frame of the closed-cavity
note: chamber {0,1} x {0,...,w-1}, arms through r=2h+2, physical squares
beginning at even rows and odd columns, and

    C={2,...,r+1} x {1,...,w-2}.

Every other root direction is obtained by tile-preserving symmetries.
The root's extreme columns have no endpoints and exactly 2h retained
selections in total. That boundary proof depends only on the root's
supports and feasibility, not on containment of foreign components.
The trimmed horizontally shifted partition therefore still gives

    D_C-Dprime_C=2+sum_K (E_C(K)-Eprime_C(K)).       (1)

Here E_C(K),Eprime_C(K) are raw excess sums t+p/2-2 over endpoint squares
owned by K, not corrected partial matching charges. Every endpoint square
is complete in each partition, even though its component may leave C.
Neither partial raw excess nor a shifted square is a new donor resource.

For each nonroot source K define Gamma_C(K)=E_C(K)-Eprime_C(K).

**Partial-source phase lemma.** Gamma_C(K)>=0 for every prescribed K.
More precisely, if its chamber is parallel to the root's chamber, then

    Gamma_C(K)=number of K's physical terminal tip tiles in C.     (2)

If its chamber is perpendicular, Gamma_C(K) is a sum of nonnegative
integer row-band gains. If K is fully enclosed in C, Gamma_C(K)>=2,
sharply, by the whole-flank lemma. Full containment is a sufficient way
to earn two units; merely touching C is not.

Proof of (2). In a physical row band the parallel source's chamber and
full arm squares have zero raw excess in both column phases. A terminal
tip has +1/2 physically and -1/2 in the shifted partition, giving one.
Complete endpoint-free extreme columns prevent a chamber crossing a side
boundary in that band. A source may have just one arm inside C while its
chamber lies beyond the transverse boundary, so counts zero, one and two
are all possible. This is the complete parallel-source table, with all
selections outside endpoint squares still included in the deficit ledger.

For a perpendicular source, normalize it to open rightward in actual
even/even physical coordinates. Its chamber occupies rows u,...,v with
u odd and v even, and columns c,c+1 with c even. Every physical row band
meeting it is one of the following.

| Band | Physical/shifted raw contribution | Phase gain |
| --- | --- | --- |
| Two interior chamber rows | 0 and -2+ell_band+q_band | 2-ell_band-q_band |
| One chamber end row and its exterior neighbor | +1/2 and -1/2+optional_outer_selection | 1-optional_outer_selection |

The two sites on either flank in an interior band cannot both be selected:
each already sees its adjacent chamber endpoint, so another selected
neighbor would violate feasibility. Thus ell_band,q_band<=1. The optional
end selection is zero or one. If an end-row horizontal path enters the
cavity, it lies wholly between the endpoint-free extreme columns: otherwise
that connected path would contain a prohibited boundary endpoint. Thus
the established complete arm-band table applies, including its actual tip.
The two cases are exhaustive and every gain is nonnegative. Summing only
the actual row bands in C proves the claim, with no artificial ends at
the cut. For a fully enclosed source, pairing the entire outer flank and
excluding the two arm-adjacent inner sites strengthens the sum to two,
as proved in MIXED_DIRECTION_CAVITY_COMPENSATION.md. QED.

## 2. The open-source cavity and capacity theorem

Let G_C=sum_(nonroot prescribed sources K) Gamma_C(K). Let Phi_C be the
saturated-minus-sparse membership of complete-comb physical singleton
ends in C. The exact component sum in (1) is G_C+Phi_C, hence

    D_C=2+G_C+Phi_C+Dprime_C,       G_C,Dprime_C>=0.   (3)

In particular, an escaping prescribed source creates no new signed debt.
Only the complete-comb end memberships can be negative in this ledger.
For n fully enclosed sources write G_C=2n+A_C+G_partial, with all last
terms nonnegative, recovering and strengthening the earlier mixed theorem.
Parallel partial sources can also earn two when both tips are in C even
if their chamber is outside C. Thus enclosure is no longer the required
notion of source credit.

For N root cavities, put G=sum_j G_Cj and Phi=sum_j Phi_Cj. If each original
positive no-endpoint donor belongs to at most c cavities, c>=1, then

    2N+G+Phi <= sum_j D_Cj <= c D_all,
    c Delta >= 2N+G+Phi-cB+cE.                     (4)

Actual pointwise physical incidence proves the upper inequality; the same
source may occur in different phase counts without supplying any physical
donor a second time. No phase gain is added to D_all after (4).
Nonnegative weights lambda_j satisfying sum_(j:Q in C_j)lambda_j<=1 on
every positive physical donor instead give

    Delta >= -B+sum_j lambda_j(2+G_Cj+Phi_Cj)+E.    (5)

These are sufficient certificates under geometric hypotheses, not automatic
existence theorems. For example, c=2, N=B and Phi>=-1 imply Delta>=0 by
integrality, even with arbitrary escaping source contacts. No general
twofold cover by all root cavities or lower bound on Phi is asserted.
The inequality in (5) improves the universal 5/6 coefficient to one on
every covered class for which its weighted certificate is at least B.

For an initial-pair formulation require the above component coverage
initially by the complete frozen prescribed data. All endpoints occurring
in a cavity are frozen, and every normalization step retains old selections
and only removes/promotes its own old endpoints. Thus it cannot change
the cavity labels. Complete containment of these components is unnecessary.
The outside nonpositive-receiver coverage for E>=0 remains a separate
hypothesis.

## 3. Arbitrarily many partial sources with physical deficit exactly two

**Sharp obstruction family.** For any a>=1, H>=3, even W>=32a and even
V>=2H+2, there is a feasible fully frozen configuration with a+1 positive
sources, no combs, and one root cavity satisfying

    a partial foreign sources meet C,
    G_C=Phi_C=Dprime_C=0,     D_C=2.               (6)

Thus the proposed rule D_C>=2(1+number of touching foreign sources) is
false, with overclaim 2a. This refutes that local allocation rule. It
does not refute coefficient one or the grid triple equality.
Indeed the whole family is in the previously proved source-only class,
so its global coefficient-one inequality already follows from the
directional averaging theorem.

Place the root at chamber origin (2,3), width W and depth H. Set y=2H+4;
then C={4,...,y+1} x {4,...,W+1} in actual even/even physical coordinates.
For i=0,...,a-1 put c_i=14+32i. A rightward positive source of width V
and depth one has chamber rows 7,...,V+6 and columns c_i,c_i+1. Its
horizontal arms run through c_i+4 in rows 7,V+6; use the prescribed
matching, lateral and axial supports. Add the sharp flank selections

    (row,c_i-1) for odd row 7,...,V+5,
    (row,c_i+2) for odd row 9,...,V+3.

All endpoints in its lower arm are outside C because V+6>=y+4. Its upper
arm and some chamber rows are inside C, so it is partial. The source's
actual whole phase gain is two, but all of that gain is outside C.

The following explicit filling is independent of an optimizer. Start with
these selected columns on each cavity row, interpreting intervals of
even/odd columns literally.

| Row | Selected columns before the foreign-source patches |
| --- | --- |
| even 4,...,y-2 | {5} and even 8,...,W |
| odd 5,...,y-1 | {4,6,7} and odd 9,...,W+1 |
| y | {5} and even 8,...,W-2 |
| y+1 | {5,W} and odd 7,...,W-1 |

For each c=c_i make these local changes to those rows:

- row 7: remove c+1,c+3;
- every even row 8,...,y: remove c,c+2,c+4 and add c+3;
- every odd row 9,...,y+1: remove c+1,c+3 and add c+2,c+4.

Take the union with the prescribed supports and complete sharp flanks;
no prescribed selection is deleted. The entire construction fits in
(V+12) by (W+8), with vertices indexed from zero.

### Uniform feasibility and count proof

Different foreign chambers are 32 columns apart. Their entire endpoint
and support envelopes lie in [c_i-1,c_i+5], leaving 25 intermediate columns;
no two such envelopes interact. Their endpoints are at least four rows
below the root chamber and at least eleven columns from its arms. The
complete frozen source/matching lemmas apply simultaneously.

Outside the patches the filling alternates opposite column parities on
consecutive rows; these sites have no selected neighbor, except the
explicit horizontal pair {6,7} on ordinary odd rows, the final vertical
pair at column 5, and final horizontal pair {W-1,W}. Every selection in
the first row sees exactly its root chamber endpoint above. The root's
inside/axial supports exclude the boundary corners
as before. None of the repeated selections adds a neighbor to them.

At an upper foreign arm, row 6 has selections at c,c+2,c+4, each adjacent
only to its own row-7 endpoint. In row 7, selections c-1 and c+5 see only
the chamber endpoint and tip respectively. In later chamber bands, odd-row
selections c-1,c+2 each see just their own chamber endpoint; {c+4,c+5}
is a selected horizontal pair with no other occupied neighbor. The even-row
selection c+3 sees the upper-arm endpoint when its row is 8, and is isolated
thereafter. All other nearby columns retain the alternating pattern.
These statements check every local interface, including rows 5/6,7/8
and the last two rows. Below C, the next even row has no selected chamber
flank; the lower arm and its additional supports start no earlier than
row y+3, so no last-row selection acquires a second occupied neighbor.
This proves feasibility for every a,H,W,V, not only checked values.

The upper foreign arm band has optional outer selection one, so its
phase gain is zero. Every subsequent intersecting chamber band has one
outer and one inner flank selection, giving gain 2-1-1=0. Thus G_C=0.
Every shifted no-endpoint square has two selections: away from patches
this follows from the two alternating rows, with the explicit vertical
pair at the left end and horizontal pair at the right end in the final
band. At a chamber patch the two adjacent no-endpoint shifted pairs have
selections (upper,c+3),(lower,c+4) and (lower,c+5),(upper,c+6).
At the upper arm the right adjacent pair is (lower,c+5),(upper,c+6);
the other affected shifted squares contain endpoints. Hence Dprime_C=0.
Equation (3) gives D_C=2. Directly, the only positive physical donors are
the two last-band tiles with column pairs {6,7} and {W,W+1}, each of
deficit one. This also proves (6) without relying on optimization.

## 4. Verification and remaining work

`develop/check_open_source_cavities.py` checks 90 physical configurations
and eight symmetry images. These include 48 sharp all-count family cases,
partial parallel-source gains zero/one/two, complete mixed-source controls
and escaping-comb signed flux. The checker recomputes feasibility,
freezing, component ownership, both raw partitions, every perpendicular
row-band formula, exact tip counts and the original whole-receiver ledger.
The smallest sharp witness includes all selections and matching edges.

Existing local Lean lemmas already prove chamber-flank capacity and arm-cap
counts; the whole-flank arithmetic is also audited. The additional formal
statements in `formal/SubQuorum/OpenSourceCavities.lean` aggregate arbitrary
row-band gains and the conditional open-source/capacity ledger. The full
geometric adapters and coordinate family remain written proofs. Finite
controls do not replace their proof.

The partial-contact restriction has been removed for the prescribed long
sources. Arbitrary positive bent components, uncontrolled negative comb
flux and existence of enough low-multiplicity cavity capacity remain open.
Future routing must earn actual Gamma or physical capacity; simply charging
two to every component that enters a region fails by the unbounded family.
