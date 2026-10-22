# Simultaneous compensation for mixed aligned U sources in six rows

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Model and theorem

Use the immutable canonical full-even-U endpoint/support/matching records,
physical tiles tau(r,c)=(floor(r/2),floor(c/2)), source charges q, mixed full
tile count J and directed source-labelled event count K from
`SIX_ROW_TRANSVERSE_U_BUDGET.md` and its prerequisites. An event from source
i is (i,p,z), with p its endpoint, z a foreign endpoint in the same tile,
p,z adjacent, and z NOT an original support of i. Consumed supports remain
original supports for this definition. Let

    Phi(Y)=sum_i max(0,-q_i)+2J(Y)-K(Y).

Consider any finite family of pairwise endpoint-disjoint full sources in
rows0..5 of the following two types:

* V sources: arbitrary transverse U(6,d,f), even independent d,f>=4,
  either direction and any integer bar start. Write a,b for the numbers
  with even and odd bar start, respectively.
* H sources: full U(B,4,4), even B>=6, under either chart

      Down: (r,c) -> (1+r,L-1+c),
      Up:   (r,c) -> (4-r,L-1+c),

  where L is even. Its projection is I=[L,L+B-1]. Its two complete bar
  rows are1,2 (Down) or3,4 (Up), and its stems terminate at row5 or0.
  This is an interior bar phase. Boundary-phase horizontal U sources,
  odd-L H sources, rotors and all other types are excluded.

Then, without a completeness assumption,

    Phi(V union H) >= Phi(V)+sum_H(B/2-3)
                  >= a+2b+sum_H(B/2-3) >=0.                (1)

Each H marginal bound is sharp as an endpoint-only statement, even with
two V sources. In particular B=6 can have marginal0.

For the complete-pocket strengthening, require the entire family to lie
inside an aligned six-row pocket [0,5]x[0,N-1] of the established spanning
upward-U chamber. Retain the old occupied boundary and all original
supports not consumed by actual endpoints. Require every retained
support in the pocket to have exactly one occupied neighbour. All new
sources in this pocket must be exactly the V and H above; no additional
endpoint owner or clipped support is permitted. Then

    Phi(V union H) >= Phi(V)+sum_H(B/2-2)
                  >= a+2b+sum_H(B/2-2)
                  >= number(V)+number(H).                 (2)

A nonempty complete pocket in this class has Phi>=2, so its whole
chamber increment is at least7. This extends the transverse-only chamber
theorem to a mixed-orientation class. It does not establish the unrestricted
complete-pocket theorem or control any exterior contribution.

## Geometric separation of horizontal projections

Every H has endpoints in every column of I on its outer bar row1 or4.
Each of its two side stems has endpoints at every row1..4. For distinct
H sources, order their left ends L1<=L2. If L2<=R1, the second source's
left stem meets the first source's outer bar at (1,L2) or(4,L2).
Endpoint-disjointness forbids this. Thus their closed projections are
disjoint, including H sources of opposite orientations.

A V bar fills all six rows in its two columns. Therefore neither bar
column can meet any H projection, by collision with that H's outer bar.

For a Down H, no V endpoint in row5 can lie over I. Its bar is outside
I; any bottom stem entering I from either side must pass the H endpoint
(5,L) or(5,R). For an Up H the reflected exclusion holds in row0.
The V endpoints over I are consequently confined to row0 for Down, or
row5 for Up. Call this the overflying row.

At most one V owner from either side can reach the overflying row over
I. If two bars on the same side both reach I, the farther stem must
cross the nearer bar, an endpoint collision. Hence there are at most
two visiting owners. Each contributes an interval entering I from its
left or right end; two such intervals are disjoint.

Because both L and B are even, each H footprint occupies whole physical
tile columns. Distinct H footprints are therefore disjoint as tile sets,
even when their projections are immediately adjacent. There are no
H/H intratile events or full mixed tiles. All new V/H events and tiles
belong to the unique H footprint involved. No old V/V event disappears:
source endpoints and original supports are immutable.

## Exact physical-column accounting

Fix a Down H; Up is its reflection r->5-r, which preserves tiles. Put
t=B/2. Its charge is1-B, so its source mass is B-1. In each of the t
physical tile columns of I, the only possible V/H contact is between
V endpoints on row0 and H endpoints on row1. Its other rows cannot
meet V endpoints. Let k be the number of these V endpoints in the
two columns, and debit be new event count minus twice new mixed-full
tile count in that physical column.

| Coverage of the two columns | New events | New full mixed tiles | Debit |
|---|---:|---:|---:|
| No V endpoint | 0 | 0 | 0 |
| One V endpoint | at most2 | 0 | at most2 |
| Two endpoints, same V owner | exactly3 | 1 | 1 |
| Two endpoints, different owners | at most4 | 1 | at most2 |

Every covered column contributes one event emitted by H: H has no
original supports on row0. A V endpoint emits back unless its neighbour
on row1 is one of its original lateral supports. For two consecutive
endpoints from the same V stem, exactly one of the row1 neighbours is
such a support, by the alternating canonical support rule. This proves
the exact3 in the third row, including terminal positions. The two
row0 and two row1 endpoints form a full mixed tile exactly when k=2.
No tile here was already full in V, which has no endpoints on row1
over I. All possible events and new tiles have now been accounted for.

At most two physical columns are partially covered (k=1): one per
interval terminal. At most one fully covered physical column can have
two visiting owners: it must contain their terminal seam. A partial
column and a two-owner full seam cannot coexist. If the two intervals
leave a gap there is no seam; if they meet without a gap their union
covers all I, so there is no partial column. With only one visitor,
there is at most one partial column and no seam.

Assign a provisional debit1 to each of the t columns. An empty column
costs less, an ordinary full column costs exactly1, and an exceptional
partial or two-owner column costs at most one extra. Thus

    debit(H)<=t+2,
    Delta_H=B-1-debit(H)>=B/2-3.                          (3)

The disjoint physical footprints give an exact simultaneous partition,

    Phi(V union H)-Phi(V)=sum_H Delta_H.                  (4)

In particular, these are simultaneous marginals against the same V
inventory, not separate estimates that spend the V mass repeatedly.
Combining (3),(4) with the established Phi(V)>=a+2b proves (1).

## Completeness removes every partial column

For a Down H, suppose a visiting V top stem terminates strictly inside
I and the next point in its direction is uncovered. That point is its
original beyond-tip support, still strictly inside I. It already has
two distinct occupied neighbours: its own terminal on row0 and the
old top boundary endpoint on row-1. It therefore cannot remain a
retained support; completeness forces an actual endpoint there.

No H endpoint can consume it: this H has no endpoints on row0, and
other H projections are disjoint. No V bar can consume it, since all
bars are outside I. The only possible consumer is the other visiting
top stem. Consequently the visiting intervals either cover none of
I or cover all of I. A nonempty uncovered gap, including a terminal
gap with only one visitor, is impossible. The reflected proof applies
to an Up H using the occupied row6 boundary.

Since I is a union of complete physical columns, no partially covered
column remains. At most one two-owner seam is exceptional, hence

    debit(H)<=t+1,
    Delta_H>=B/2-2>=1.                                   (5)

Equations (4),(5) prove (2). For a nonempty complete pocket with at
least two sources, (2) gives Phi>=2. A sole V is excluded by the
inherited-support singleton proof of the transverse theorem. A sole
H has no foreign events or mixed tiles and Phi=B-1>=5. Thus every
nonempty complete pocket in the stated class has Phi>=2. Its physical
tiles are disjoint from the old core, so the established upward-U
chamber contribution5 gives total increment>=7. The bound is sharp
in this expanded class because it contains the previously proved
locally complete opposed V pairs for every even outer width W>=12.
This does not assert per-H sharpness under completeness or global
extendibility of a local pocket.

## A sharp obstruction to unconditional one-unit H compensation

For any even B>=6 and even L>=6, use a Down H with projection
[L,L+B-1] and two V sources, in the transverse notation
(bar,direction,bottomDepth,topDepth):

    (0,+1,4,L+B-4),
    (L+B+4,-1,4,6).

Their top stems end at L+B-4 and L+B-1. The two uncovered points
L+B-3,L+B-2 straddle a tile boundary. There are exactly two partial
columns and t-2 ordinary full columns. At each partial column both
directed events occur, so debit=t+2 and Delta_H=t-3. The records are
endpoint-disjoint for every stated B,L; their bottom stems stop
outside the H projection. Reflecting rows gives Up examples.

For B=L=6, Phi(V)=2 and Phi(V union H)=2. Therefore the proposed
rule 'every endpoint-disjoint added aligned H pays at least1' is
false. This is a counterexample to that rule only, not to (1), (2),
or any global grid inequality. The two uncovered top supports also
explain why this endpoint-only example cannot itself be a complete
pocket in the allowed class.

## Verification and remaining coverage

Run `PYTHONDONTWRITEBYTECODE=1 python3
develop/check_six_row_mixed_aligned_u_budget.py`. The verifier rebuilds
full canonical records, exact mixed tile sets and source-labelled
event sets; checks their simultaneous disjoint partition; and checks
the marginal bounds. It also constructs locally complete families
in the actual inherited old core and checks all retained pocket
support degrees. Oppositely oriented adjacent H blocks are not
assumed locally complete: they can leave conflicting side supports.

The arbitrary-parameter proofs above do not follow from enumeration.
This new mixed theorem has no new Lean verification and has not yet
received an independent review verdict. The earlier transverse
geometry/arithmetic Lean file retains its narrower documented scope.
Boundary-phase H, odd-L alignment, rotors, exterior signed budgets,
universal source decomposition and the unrestricted global5/6 and
rectangular-grid equality goals remain open. The submitted manuscript
is unchanged.
