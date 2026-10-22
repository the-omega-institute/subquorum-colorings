# Endpoint-free gap capacities and an unrouteable frozen family

23 October 2026. Authors: Haobo Ma and Wenlin Zhang.

The direct/single-cap compensation network need not route even one demand
in a completely frozen, uniquely matched configuration. We give an arbitrary
length family with one source, no beta resource and no path from that source
to any permitted interval, although the exact scalar margin is positive.
It also defeats every fixed radius for endpoint-free interval access.

A maximal endpoint-free column gap supplies a larger local accounting region.
Its available capacity is exactly its number of unmarked BB--TT interval
units. These units can be allocated to the gap's adjacent TP terminals,
with at most two candidate terminals per unit. The resulting conditional
compensation theorem handles the new family without any additional links.
The allocation theorem is the earlier degree-two theorem; the new content
is this physical gap adapter and the frozen obstruction to bounded access.

## 1. Exact capacity of an endpoint-free gap

Use a feasible pair (T,M), actual endpoints P, and a matching-closed aligned
two-row packet J as in COMPENSATION_FLOW_NORMAL_FORM.md. Each band begins
with BB, ends with a blank corner, and has the established boundary marks.
Use B for the number of distinct marked BB--TT intervals, not the number
of blank sites. Let L be the number of all such interval units.

In one band, a gap G is a maximal consecutive set of columns containing
no endpoint. It may contain BB, TT and BT columns, with either order of BT.
Every TT column has BB neighbors: each of its two selections already sees
the other selection, so all horizontal neighbors must be blank. A TT column
cannot meet a P column or the packet ends. Thus every BB--TT forest interval
is wholly inside one gap. Write a_G,b_G for its TT and BB column counts.

The interval graph inside G is a forest with a_G+b_G vertices and 2a_G
edges. It therefore has exactly b_G-a_G components, each of weighted
surplus one. BT columns contribute zero. Hence

    |G|/2 - |T intersect G| = b_G-a_G = L_G.

Here |G| counts vertices. If m_G distinct interval units in G are marked,
the exact capacity remaining after that reservation is

    c_G = L_G-m_G >= 0.                                  (1)

Keep each of these c_G original units separately identifiable. Aggregating
their capacity does not create an extra credit for a BT column, a cap,
a boundary mark, or the whole gap. Gaps in different bands are physically
disjoint; their interval units partition the packet's original interval pool.

## 2. Gap access and resource ownership

Declare that a free TP terminal in a column immediately beside G can use
any one unmarked interval unit in G. The witness is the endpoint-free
column segment from that terminal to the chosen interval. This is a
counting allocation, not a claim to change the actual matching or to
promote an endpoint through selected vertices.

Use the abstract cancellation theorem with this enlarged fixed access
relation on original physical terminals and interval identities. This
extends its earlier physical adapter. Disjointness concerns strand owners,
terminal use and resource units, not physical transport through disjoint
grid paths.

There are at most two such terminal candidates: one at either boundary
column of G. A TP column has exactly one endpoint. Consequently each
original interval unit has at most two candidate terminals, and hence
at most two distinct current alpha owners. If both terminals belong
to the same virtual alpha, it remains a singly owned resource.

The previous direct TP--BB and same-row TP--BT--BB accesses are included:
their intervening columns and target interval lie in the adjacent gap.
The new relation also permits longer endpoint-free segments. A terminal
cannot skip another P column to claim a more distant gap.

Any permitted opposite-label terminal matching C can first be fixed and
contracted. Access is retained only at its surviving free TP terminals;
the same gap geometry and unit resource identities remain valid.

**Gap compensation theorem.** Form the two-owner resource multigraph on
all current alpha demands, using every unmarked interval unit and the
gap access relation. Let t_G be the number of tree components with no
singly owned resource, including isolated demands. Let q_G be the number
of units unused by a maximum allocation and beta' the current whole-beta
count. Then

    maximum interval payment = alpha'-t_G,
    S_J-B = q_G+beta'-t_G.                               (2)

Proof. The ownership bound just proved permits direct application of
ONE_SIDED_INTERVAL_AND_BETA_ALLOCATION.md, Section 1. The resource total
is exactly L-B, and the unchanged physical identity is
S_J=L+beta'-alpha'. Substituting the maximum allocation proves (2).
Each allocated unit belongs to exactly one original interval in exactly
one gap. Multiple payments from a gap consume different units, so no
physical resource is counted twice. QED.

For example, if every current alpha has at least two distinct unmarked
interval neighbors, t_G=0 and S_J>=B. The two neighbors may lie in one
gap of capacity at least two, or in different gaps. A deficient tree with
n demands has only n-1 edge resources and no singly owned resource, so
its sum of demand degrees is 2n-2 and cannot have all degrees at least two.
This gives a coefficient-one packet class, without restricting PP path
length, bends, matching orientation, or the presence of occupied bands
elsewhere. It does not assert that every frozen packet meets the condition.

For a global application use tile-disjoint packets and complete original
receiver closure. With the existing outside deficit D_out, positive demand
q_out, negative charge R_out and receiver-overlap count N_out, retain the
exact global ledger

    margin = sum S_J + D_out - q_out + R_out - 2N_out.

Thus packets satisfying (2) with t_G=0 give the coefficient-one bound when
q_out+2N_out <= sum B + D_out + R_out. In the original single-terminal
setting N_out=0. Gap units paid inside a packet cannot also be used as
outside donors. The general geometric budget remains open.

## 3. Arbitrary-length completely frozen obstruction

Let W>=6 be even and d>=1. Start with direct_family(W,4), in its original
coordinates. Its two extreme terminal rows are r=5 and r=W+4. Their
opposite rows in the same band are respectively r*=4 and r*=W+5.
Each terminal row has the local pattern

    cap T2, TP3, BP4, TP5, BP6, TP7, cap T8,

with mixed strand pairs BP4/TP5 and BP6/TP7. The two TP3 terminals belong
to the original alpha. The original system has alpha=1, beta=0, gamma=5.

For each extreme row and each j=1,...,d add two selections at columns
2-j and 8+j. Put them in row r* when j is odd and row r when j is even.
There are exactly 4d new selections. All are isolated in the final
occupied set: successive added selections alternate rows, their vertical
neighbors are blank, and their neighbors toward the old caps are blank
in their own row. Their other vertical neighbors outside the band are
blank, as is immediate from the direct-family support list. None is
adjacent to an old endpoint or old selection.

Consequently feasibility is preserved. The endpoint graph and actual
matching are unchanged, so the matching is still unique. Every old
freezing event remains valid with the same witnesses; all endpoints
still freeze. This uses the explicit all-W direct-family certificate,
not finite verification as a substitute for a freezing argument.

Take J to have rows 4..W+5 and columns -d..9+d. It is tile-aligned after
the common horizontal translation d+2. Its dimensions are
(W+2) by (2d+10), all selections and endpoints lie inside, and both end
columns in every band are BB. Therefore B=W+2. The exact inventory is

    |T|=13+4d, |M|=W+4,
    S_J-B = 3W-9+(W-2)d > 0,
    L-B = 3W-8+(W-2)d.                                  (3)

The added selections are not vertically beside any endpoint, so the
TP/BP/PP types, strand pairing, and horizontal terminal-link candidates
are unchanged.

### The old network has value zero, with C0 empty

All TP terminals reachable from the source are TP3,TP5,TP7 in the two
extreme rows. From TP3 one can enter BP4/TP5, and then BP6/TP7. TP7 cannot
advance through cap T8; TP3 cannot advance left through cap T2. There is
no link escaping these two row chains and no beta owner.

The source and each relay terminal have no direct BB neighbor. The only
old single-cap candidate exits were BB1 and BB9. The j=1 selections turn
both into BT columns, blocking them; all further added columns contain
no endpoints and cannot create a new terminal link. Thus every source-
reachable TP has no direct/single-cap access. The old network has

    nu=0, delta=1, Z empty, Q=L-B,

for every d, even when every matching of the permitted ordinary horizontal
TP--BP links is allowed. Pre-linking mixed owners cannot create an exit missing
from the full directed reachability graph. This is an unrestricted
access-model obstruction, not a protected-core obstruction.

It also refutes extending the earlier missing-alpha-terminal injection
to ALL TP terminals without usable cap access. In either extreme row,
TP3,TP5,TP7 have only BP4,BP6 as adjacent BP candidates: three terminals
cannot inject into two. The earlier theorem remains valid because it
concerns original alpha terminals; TP5 and TP7 here belong to mixed paths.

### Every fixed endpoint-free access radius fails

From TP3 toward the left, the old cap and d added columns all have
one selection and no endpoint. The first BB column is 1-d, at distance
d+2. It is unmarked, since the marked first column is -d. From TP7
toward the right the first BB is 9+d, also at distance d+2; this right
interval is marked in the chosen packet. TP5 is separated from both
gaps by P columns. These exhaust the source-reachable terminal exits.

Therefore even a strengthened access rule permitting every endpoint-free
segment of length at most R gives value zero whenever R<d+2. No uniform
finite radius suffices for this access mechanism on completely frozen
packets. This is a spatial access-distance statement: the original
direct/single-cap model stays blocked regardless of the number of
additional terminal links.

### Gap access pays the demand without a new link

The left endpoint-free gap beside the original upper TP3 contains the
unmarked singleton BB at column 1-d, with the BT corridor connecting
them. Its corresponding lower-band gap supplies a different unmarked
unit as well. Thus the original alpha has at least two distinct gap
resource neighbors. It is fully paid without any terminal cancellation:
the enlarged network has nu=1 and minimum additional link count zero.
No extra unit is attributed to the added selections or to the corridor.

The earlier model remains exact for its declared access relation. This
example refutes its proposed universal routing completeness, not the
normal-form theorem, the scalar target, or the grid conjecture. Indeed
(3) gives a positive margin even before the new allocation is chosen.

## 4. Verification

The permanent checker tests W in {6,8,12,20}, d=1..32. It checks feasibility,
isolation of every new selection, complete freezing, unique matching,
the compact receiver-closed packet and exact counts. The old full-flow
solver returns the empty-separator deficit-one certificate in all 128 cases;
the strengthened access radius below d+2 is also blocked. Gap access gives
one payment at zero new links in every case. Its adapter checks exact
physical gap capacity, disjoint interval ownership and at most two candidate
terminals per unit. These finite checks support Sections 1--3's general
proofs and do not replace them.

The adapter is additionally checked on 160 fully frozen geometric images:
both actual matchings of the bent fixture, the capacity-two rotor, occupied
bands, and a separate TT-forest control, including all eight symmetries and
four band phases. There are 449 exact allocation controls, including all
288 available single-link contractions in those images. Each is compared
with an independent bipartite matching algorithm and the unchanged scalar
ledger. A separate frozen two-copy example has two adjacent TP ports sharing
exactly two unmarked units in one gap; both ports see those same two units,
not four credits. Across the combined run, 578 adapter calls check 6,938
gaps and 54,792 available unit occurrences. These totals count repeated
controls, not distinct physical resources across different configurations.

This gap theorem has a written proof and these finite controls. It is not
part of the earlier Oracle acceptance of the augmentation theorem, and no
new Lean verification of the physical gap adapter is claimed.

Independent combined review b374e96c-be4a-42a3-90d7-453d93f6b389 accepts
this entire gap theorem and family, together with the unreflected
zero-capacity corridor extension. The full 20,762-character mathematical
answer is archived in output/zero-capacity-gap-beta-compensation-oracle.json.
The reviewer did not execute Python or Lean. The ordinary-link scope and
abstract-versus-physical adapter distinctions above implement its requested
clarifications. The later reflected PP and auxiliary-rematching results
are separately reviewed; this acceptance does not cover them.

Run:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_endpoint_free_gap_compensation.py --output output/endpoint-free-gap-compensation-validation.json

The general grid bound, arbitrary residual gap competition and the
three-parameter grid equality remain open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
