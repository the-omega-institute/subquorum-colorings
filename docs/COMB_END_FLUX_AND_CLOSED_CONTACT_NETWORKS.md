# Two-tiling end flux and compensation through closed contact networks

19 October 2026. A general extension of the exact comb-end debt ledger.
The proof below recovers the compensation carried by saturated end contacts.
It covers arbitrarily many contacts between source mouths, without spending
a partial comb receiver or a shifted tile as a new original-ledger resource.
Unrestricted exterior compensation and the universal grid bound remain open.

## 1. Hypotheses and the second tiling

Work on an even-by-even rectangular grid with mn vertices. Use the complete
initial-source, complete perpendicular contact-comb, matching,
support, freezing and thin/one-square coverage hypotheses of
`COMB_END_DEBT_AND_EXACT_MOUTH_LEDGER.md`, Sections 1 and 5. In particular,
there are B distinct prescribed positive long sources, each with whole charge
one; their physical mouths F_H are pairwise disjoint. Each actual whole comb
receiver is counted once and has charge zero. Normalize as in that note.

Fix one mouth F={r,r+1} x {1,...,w-2}, where r and w are even. Its N=(w-2)/2
physical tiles use column pairs (1,2),(3,4),...,(w-3,w-2). The two columns
1,w-2 are forced blank. The shifted squares use (2,3),(4,5),...,(w-4,w-3),
and partition every remaining vertex of F into N-1 squares.

Let S,U be the physical sparse/saturated one-endpoint tile counts, C the
number of full two-endpoint columns, and D the total deficit 2-t on actual
physical no-P tiles. Define D' as the sum of 2-t over shifted squares with
no P. Every summand of D' is nonnegative by the selected-square capacity.
D' is an auxiliary count, not a separately allocated physical-tile payment.

## 2. The end types swap under the transverse shift

**Type-swap lemma.** Every full endpoint column has two P and one T in its
shifted square. Each physical sparse end becomes a saturated shifted end,
and each physical saturated end becomes a sparse shifted end. Thus the
shifted end counts are exactly U sparse and S saturated.

Proof. Every endpoint column lies in both partitions because the deleted
boundary columns are blank. For each fixed endpoint column the adjacent
column paired to it changes to the opposite side under a shift by one.
The mouth row pair stays fixed, so full and partial columns stay full and
partial. Terminal tile ownership excludes a second complete comb from the
same shifted square, including an opposite-corner pair.

In a full column the alternating side supports put exactly one T in either
choice of paired neighboring column. That T forbids the other corner.
In a partial column the axial end support lies in the same row pair and
same column as P. On the side containing the endpoint's perpendicular
support there is one further T and a forced blank. On the other side both
corners are blank: one is forbidden by the axial T, the other by the
alternating side support of the next endpoint along the comb. This argument
includes length-two combs. Changing the paired side therefore exchanges
the (P,T)=(1,1) and (1,2) types. No feasible completion changes those forced
labels. Translation and grid symmetries give every source orientation. QED.

Write mu=|T in F|+|P in F|/2 and E=S+U. The shifted type table gives exactly

    mu = 2K' + (S-U)/2 + sum_(shifted no-P squares Q) t_Q,

where K' is the number of shifted endpoint squares. Consequently

    D' = 2(N-1)-mu+(S-U)/2.

The previous physical table gives D=2N-mu+(U-S)/2. Subtracting yields

    D = 2-S+U+D',             D'>=0.                 (1)

In the previous notation A=2(N-1)+(S+U)/2-mu, we now have the stronger exact
formula A=U+D'. In particular every saturated physical end supplies one unit
of the formerly undifferentiated slack, and

    D>=2-S+U.                                      (2)

This is a counting identity for the actual physical no-P donor total D.
We do not sum the original charges of shifted squares, do not identify them
with complete receivers, and do not spend D and D' as two donor sets.

## 3. Exact conservation along complete combs

Each complete comb has either no singleton physical end tiles, or exactly
one sparse and one saturated end tile. This follows from even endpoint
count and alternating supports in a fixed tiling. Let the contact collection
consist of all combs meeting at least one prescribed mouth. For each comb
record whether its sparse end tile is in the union of mouths and whether
its saturated end tile is in that union. Missing singleton tiles have neither
flag. Mouth disjointness makes each flag have at most one source owner.

Partition the combs with a flagged end into three classes:

- I: both end tiles lie in mouths;
- O: only the sparse end tile lies in a mouth;
- J: only the saturated end tile lies in a mouth.

The remaining combs contribute neither end flag. With S_total=sum_H S_H and
U_total=sum_H U_H, this disjoint partition proves

    S_total=I+O,       U_total=I+J,
    U_total-S_total=J-O.                            (3)

Equivalently orient each such comb from its sparse end toward its saturated
end, with an exterior vertex for an end outside the mouths. Internal edges
cancel in the sum of vertex imbalances. Parallel contacts are allowed; no
acyclicity, tree, degree bound or bound on I is needed. A physical end tile
cannot be in two mouths, and a whole comb receiver still occurs just once.

## 4. A stronger initial-pair bound and a closed-network theorem

Let R be the sum of deficits -rho(R_K) over nonprescribed final receivers
and 2-t over physical no-P tiles outside all mouth donor sets. As before,
R>=0. Summing (1) in the original physical ledger gives the exact identity

    mn/2-|T_0|-|M_0|
      = B+U_total-S_total+sum_H D'_H+R
      = B+J-O+sum_H D'_H+R.                         (4)

All counts in (4) are final-representative counts. The prescribed end labels,
their source ownership and their flags already persist from the initial pair,
because all source/comb endpoints and supports are frozen. Objective-preserving
normalization therefore proves

    |T_0|+|M_0| <= mn/2-B+O-J.                     (5)

In particular coefficient one holds whenever O<=B+J; it is enough to have
O<=B. This is strictly more permissive than the previous sufficient criterion
S_total<=B, since an arbitrary number I of internal end contacts has canceled.

**Closed end-contact theorem.** Suppose every sparse end tile in a source
mouth has the opposite saturated end tile of its complete comb in some
source mouth. Then O=0 and

    |T_0|+|M_0| <= mn/2-B-J <= mn/2-B.             (6)

The conclusion holds for any number of internal comb connections, including
several connections between the same two sources. It requires no new local
resource outside the mouths. The saturated endpoint's shifted-square slack
pays the sparse endpoint's lost unit through the exact counts; all actual
payments remain the distinct physical no-P tiles in those mouths.

Whenever O<=B+J, (5) removes the entire |M_0|/6 loss in the universal bound
|T_0|+(5/6)|M_0|<=mn/2. The closed-network case gives the further strict
margin B+J in (6). We do not extend this improvement to arbitrary endpoint
components or arbitrary nonperpendicular mouth contacts.

## 5. Unbounded closed networks and the remaining boundary obstruction

The extension beyond S_total<=B occurs in an explicit all-size family,
not only among the finite controls. Fix k>=1, put w=4k+10, and use a
32-by-(w+8) rectangle with physical tile origins at even coordinates.
Place the prescribed depth-two downward source with chamber rows 2,3,
columns 3,...,w+2, and arm endpoints in rows 4,...,8 at columns 3,w+2.
Use its prescribed matching and supports. Obtain a second source by the
tile-preserving reflection (row,column) -> (23-row,w+5-column). Its chamber
is in rows 20,21 and its tips are in row 15. The mouths are rows 8,9 and
14,15, both on columns 4,...,w+1.

For each index 0<=i<k, set c_i=8+4i and put a complete vertical comb in
column c_i, rows 9,...,14, with matching pairs (9,10),(11,12),(13,14).
Select axial supports (8,c_i),(15,c_i), and side supports
(row,c_i-1) at odd rows and (row,c_i+1) at even rows. Leave every unlisted
site blank. Every selected support has exactly its intended endpoint as
occupied neighbor. Consecutive comb supports on alternating sides are at
distance three, and different comb centers are four apart, so their selected
supports are nonadjacent. All combs and their supports stay at least four
columns from the source arms; the two source chambers are far from the combs.
There is no new endpoint edge joining different prescribed components.
Thus the pair is feasible, complete, and fully frozen by the general source
and comb waves. The placement and its reflected source lie in the stated
even rectangle for every k.

Each first-mouth endpoint is a sparse singleton end, since its column is
even and its side support is on the left. Its opposite second-mouth end
is saturated. Hence B=2,I=k,O=J=0,S_total=U_total=k. The closed-network
theorem gives |T|+|M|<=mn/2-2 for every k, including all k>=3 where the old
sparse-count criterion fails. Extra feasible mouth selections are allowed
by the theorem; the all-k existence proof does not rely on optimizing them.

The two-ending-comb obstacle has one source, O=2,J=0, no internal contacts,
and D'=0 in its mouth. Hence (4) assigns mouth-plus-source balance -1, as
it must. The actual exterior remainder R is positive. Formula (5) alone
does not establish the target in this case.

The previous shared-comb fixture has two sources and one internal contact,
so I=1,O=J=0. Its mouth counts (S,U,D)=(1,0,1),(0,1,3) have D'=0 in both
mouths. The four actual donor units pay the two sources with margin two.
The stronger accounting explains the second mouth's forced extra unit.

The remaining research task is exterior payment for the unmatched sparse
owners O when O>B+J, as well as coverage of parallel/bent/other endpoint
contacts. A neutral whole receiver never supplies an additional unit merely
because its end has been visited. Neither finite controls nor this network
conservation prove the unrestricted grid bound or triple equality.

## 6. Verification and formal scope

`develop/check_comb_end_flux.py` checks 696 optimized single-mouth contact
configurations, including all six start/end/crossing types, and 138 optimized
two-source bridge configurations with up to eight distinct complete combs.
It checks physical and shifted end-type counts separately, the exact identity
(1), integer slack A=U+D', feasibility, terminality, complete frozen components
and whole receiver charges. Twenty-four symmetry images include transposition.

Of the bridge configurations, 120 have S_total>B, beyond the previous sparse
count sufficient criterion. Every one has S_total=U_total and actual donor
payment 4+sum D'. A concrete 32-by-30 witness has B=2, three internal combs,
mouth triples (S,U,D)=(3,0,1),(0,3,5), and total D'=2. It therefore pays six
units against two source charges. A separate mixed-orientation four-source,
six-comb configuration has total S=U=6 and actual payment twelve. The exact
source/matching data and receipts are in `output/comb-end-flux-controls.json`.
These finite controls are auxiliary to the general type-swap and conservation
proofs, not a replacement for them.

The sequential local Lean 4.33.0 audit passes 85 declarations. Four new ones
in `formal/SubQuorum/CombEndFlux.lean` check a physical integer-coordinate
opposite-side forced-blank/selected-count lemma; conditional two-tiling flux
under explicit weighted/cardinality identities; conservation on arbitrary
finite lists of end-membership flags; and the conditional boundary-flux
inequality. Only the standard logical axioms are used. Full all-orientation
type swapping, partition/cardinality adapters, complete-comb ownership and
the initial-pair theorem remain written proofs. The receipt is
`output/comb-end-flux-formal-check.json`; peak child RSS was about 1.14 GB.
The task-owned reproducible cache was removed after preserving the receipt
and confirming no actual lean/lake executable was active.

The previous transverse-comb ACCEPT and the pending exact-debt review concern
earlier input. This closed-network extension requires its own review; no
previous verdict is inherited. The explicit all-k construction in Section 5
was added after that new review request and is outside its submitted input.
