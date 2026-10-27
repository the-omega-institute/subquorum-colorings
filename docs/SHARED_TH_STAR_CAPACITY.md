# Exact shared-TH capacity from the order of physical contacts

One original TH component can support arbitrarily many simultaneous TT/HH
compensations. Its capacity is not one per component. It is also not given by
Hall matching on individually valid TT-to-HH relay pairs. The exact answer for
a star of contacts is the sequence of terminal types along the shared path.

This note gives a general fragment theorem, an exact resource partition, and
two arbitrary-size feasible grid families. They have identical P, M, auxiliary
N, witness squares, and |T|, but different placements of selections. One family
repairs all s bad pairs through a single original TH. In the other, every one
of the s-by-s individual ordered relay pairs is valid, yet the prescribed
simultaneous switches repair only ONE pair. The Hall overestimate is s-1.

A repair count here means the NET reduction in each TT/HH component count.
It does not identify original leaf pairs with both terminals paid: residual
paths can join arms from different leaves.

The obstruction concerns the specified original N and simultaneous contacts.
Both actual families have complete zero-M adjacent payments using other
certificates. No numerical sub-quorum inequality is refuted.

## 1. A central TH and monochromatic leaf paths

Let M be a fixed actual partial matching with endpoints P. Partition Q=V\P
into T,H. Let N be a full auxiliary perfect matching, allowed to touch H.
Use the terminal-path decomposition of M+N in the
[fixed-M note](MIXED_TERMINAL_SQUARE_COMPENSATION.md).

Choose one original TH path C, oriented from its T terminal to its H terminal.
Choose k DISTINCT other original terminal paths A1,...,Ak, each of type TT
or HH. For each Aj choose one actual unit square whose opposite N edges are
one on C and one on Aj. All k witness squares must have pairwise disjoint
vertex sets. Each leaf path has exactly ONE chosen contact. Other paths,
doubled M/N edges and P-only cycles are untouched.

Sort the contacts on C from T to H. Let w_j=T if that contact's leaf is TT,
and w_j=H if it is HH. Write

    u=(T, w_1, ..., w_k, H).                          (1)

Switch the k squares to their other sides, giving N'. Old cut edges are on
terminal paths and outside M. Each inserted edge connects two distinct
ORIGINAL components, C and a leaf, so it also lies outside M. Thus N' is a
full perfect matching, M is unchanged, and M intersect N'=M intersect N.
Square disjointness makes these specified switches commute.

## 2. Shared-star fragment theorem

Cut C at all its contact edges, producing k+1 consecutive fragments F0,...,Fk.
Cut each leaf at its single contact, producing two arms. Each leaf arm has
one terminal, and both arms have the same terminal type w_j. Zero-length
arms at terminals are allowed.

**Fragment theorem.** The affected vertices become exactly k+1 terminal paths
D0,...,Dk, with no P-only cycle. Di contains exactly Fi. Its terminal types
are u_i and u_{i+1}, for i=0,...,k. All physical vertices and original M edges
on the affected paths occur in exactly one Di.

Proof. Each new square edge attaches one cut endpoint of C to one arm of its
leaf. The two leaf arms attach to the two central fragments bordering that
contact. An internal Fi therefore receives one terminal arm at each end.
The initial F0 keeps C's T terminal and receives one leaf arm; Fk keeps C's
H terminal and receives one arm. These are paths with the stated endpoint
types. Every leaf arm ends at an original Q terminal, so none connects one
central fragment to another; a cycle cannot form. The fragments and arms
partition the old affected vertices and M edges, proving the last assertion.
The geometric orientation of either square only chooses WHICH equal-type
leaf terminal attaches to each side. It does not change (1) or the path types.

Define

    d_T = #{i : u_i=u_{i+1}=T},
    d_H = #{i : u_i=u_{i+1}=H},
    c   = #{i : u_i != u_{i+1}}.                     (2)

Then the exact affected output counts are (d_T,d_H,c). All affected paths
become TH if and only if (1) alternates strictly. Equivalently, k is even,
k=2s, and the contact word is

    w=(H,T,H,T,...,H,T)=(HT)^s.                      (3)

If there are s TT leaves and s HH leaves, let d=d_T=d_H. Equality follows by
counting T/H endpoint incidences: 2d_T+c=2s+1=2d_H+c. Thus

    (s,s,1) -> (d,d,2s+1-2d)                         (4)

within the star. Exactly s-d bad pairs are repaired. For global original
counts (a,b,t), the exact transformation is

    (a,b,t) -> (a-s+d, b-s+d, t+2s-2d).              (5)

The unmatched T and unused H counts of the final TH-payment collection are
2(a-s+d) and 2(b-s+d). These are exact endpoint counts, not merely bounds.

## 3. Physical resource capacity, including partial repair

Let R(Fi) denote the actual M edges on central fragment Fi. At contact j,
let L_j and R_j be the leaf-arm M-edge sets attached to the fragments before
and after the contact, respectively. These names refer to attachment order,
not an assumed coordinate direction. Set

    S_i = R(Fi)
          disjoint-union (R_i if i>=1)
          disjoint-union (L_{i+1} if i<k).             (6)

The sets S_0,...,S_k partition the entire original affected M-edge set. The
TH payments use exactly

    disjoint-union { S_i : u_i != u_{i+1} }.           (7)

Every central segment and leaf arm has one final owner. Sharing an original
TH is therefore permitted, while sharing a physical fragment between two
payments is not. Equation (7) also handles a failed contact word: resources
on the resulting TT or HH paths are not TH payments.

When (3) holds, all S_i are used, so with U denoting the global union of TH
payment resources,

    U_after = U_before disjoint-union
              (disjoint-union_j R(Aj)).               (8)

The incremental physical cost is the sum of all original bad leaf-path
M-edge counts. The central TH's resources occur once, however many contacts
it has. In a failed word, some formerly used central resources may instead
lie on an unpaid TT or unused HH path. They cannot be claimed as a numerical
rebate while those selected endpoints remain unpaid.

Several such stars with disjoint ORIGINAL component sets combine independently.
For alternating stars repairing a total of S TT leaves, the global change is
(a-S,b-S,t+2S), with disjoint cost increments from their leaf paths. If they
cover all original TT, there is a full payment and

    J=|T|+|M|=area/2-(b-a),
    |T|+(5/6)|M|=area/2-(b-a)-|M|/6.                 (9)

This expands the sufficient certificate class beyond component-disjoint
single relays. It does not prove that arbitrary grid configurations admit
covering stars, nor a universal 5/6 improvement.

## 4. Individual ordered Hall matching can overestimate repair without bound

Take a balanced contact word

    w=H^s T^s,     s>=1.                             (10)

Every HH contact precedes every TT contact on C. Any TT leaf and any HH leaf
therefore form a correct individual ordered relay through C: when oriented
from the TT source toward the HH sink, the central path's outgoing HH contact
comes before its incoming TT contact in T-to-H order. Both selected squares
are disjoint. The graph on the designated leaves, using their prescribed contacts, is
K_{s,s}, and has a
matching of size s satisfying every Hall inequality.

Choose that matching's s pairs. Collectively their squares are STILL pairwise
vertex-disjoint: each leaf and each contact occurs once. Their shared central
component is the missing constraint. Switching all 2s squares has extended
word T,H^s,T^s,H, hence

    d_T=d_H=s-1, c=3.                               (11)

The TT and HH component counts each decrease by exactly one. Reordering
these same disjoint switches cannot
improve the result, because they commute. Thus matching individually valid
ordered relays, even with disjoint actual square supports and distinct bad
endpoint paths, does not imply simultaneous repair of the matching's size.

This does not justify assigning capacity one to a shared TH. The alternating
word (HT)^s has the same number of contacts and leaves, and repairs all s.
Capacity must retain the ordered physical fragments or an equivalent exact
state; neither raw contact reachability nor a universal one-per-component
restriction expresses this star's correct behavior.

## 5. Arbitrary-word feasible full-grid construction

For any k>=1 and contact word w of length k, take a 6-by-W grid, W=6k+2.
The central TH path is

    C=(5,0),(4,0),(3,0),(3,1),...,(3,W-1),(4,W-1),(5,W-1).

For leaf j=0,...,k-1, set c_j=2+6j and take the U-shaped path

    (0,c_j),(1,c_j),(2,c_j),(2,c_j+1),
    (2,c_j+2),(2,c_j+3),(1,c_j+3),(0,c_j+3).          (12)

On every displayed path, N consists of its edges at positions 0,2,4,...;
M consists of its edges at positions 1,3,5,... . Select (5,0), and both top
terminals of exactly those leaves whose label is T; all other Q sites are H.
The centre and leaves are vertex-disjoint. M covers precisely their internal
vertices. A selected top leaf terminal has its one vertical P neighbour and
holes on either horizontal side; different leaves have two gap columns and
nonadjacent terminals. The central selection (5,0) sees only P=(4,0).
Consequently EVERY word gives a feasible actual configuration.

Complete auxiliary N explicitly:

* pair row 3 horizontally, from each even column to the next;
* pair rows 4 and 5 vertically in every column;
* on each leaf block in the top three rows, use the four displayed path N
  edges, plus the horizontal middle-column pair in each of rows 0 and 1;
* the left, intermediate and right two-column gaps start at columns 6j,
  j=0,...,k; pair each gap horizontally in rows 0,1,2.

These groups partition the board and include all displayed path N edges.
The added top pairs and interior bottom pairs are HH components. There are
no actual M edges outside C and the leaves.

The k squares have top-left corners (2,c_j). They are vertex-disjoint. Each
cuts the leaf edge (2,c_j)--(2,c_j+1) and the opposite central edge in row 3.
Their positions on C are 2+c_j, strictly increasing with j. Thus this realizes
the exact prescribed word on an actual full rectangular grid, at every k.

If p leaves are TT and q are HH, k=p+q, the counts are

    |M|=6k+2, |T|=2p+1, |H|=24k+7-2p,
    (a,b,t)=(p,11k+q+3,1).                           (13)

The central path uses 3k+2 actual M edges; each leaf uses three. The final
paths corresponding to F0,...,Fk have exact physical costs

    |S_0|=3, |S_i|=6 (1<=i<k), |S_k|=5.             (14)

To check (14), the first central fragment has two M edges, an internal one
has three, and the final one has three. Cutting a U-leaf's first horizontal
N edge leaves one M edge on the arm attached before the contact and two on
the arm attached after it. Substituting into (6) gives 3,6,...,6,5. Their sum
is 6k+2=|M|, so this is also an explicit complete resource partition.

For k=2s the words (HT)^s and H^sT^s have identical P,M,N, contacts and counts
|T|=2s+1, |H|=46s+7, |M|=12s+2, J=14s+3. For s>=2 the T placements differ; at s=1 both words are HT.

| Word | Global initial counts | Global final counts | Final TH M-cost |
| --- | --- | --- | --- |
| (HT)^s | (s,23s+3,1) | (0,22s+3,2s+1) | 12s+2 |
| H^sT^s | (s,23s+3,1) | (s-1,23s+2,3) | 14 |

The first increments cost from 6s+2 to 12s+2, exactly the 6s distinct leaf
M edges, while using the central resources once. The second's three changes
in extended word select only S0, S_s, S_{2s}, costing 3+6+5=14; the remaining
s-1 TT and s-1 HH paths each cost six. The count of repaired pairs, not just
the aggregate physical cost, must be checked before calling a certificate full.

Every configuration has a complete zero-M adjacent payment: each TT leaf's
two selected top terminals go to its two top middle-column holes, and (5,0)
goes to (5,1). These are distinct targets and disjoint edges. Hence neither
family is a counterexample to unrestricted payment or the numerical target.
Their J lies below half-area by 22s+3. No freezing assumption is made.

## 6. Validation and next geometric question

The [standalone checker](../develop/check_shared_th_star.py) checks full M/N,
actual feasibility, original component/contact identities, all fragment owners,
the exact word counts and physical resource partition. It checks every word
of lengths 1,...,8 (510 actual feasible boards), both families at s=1,...,40,
and all s^2 individual ordered pairings for s=1,...,8 (204 pair controls).
Finite checks validate the construction; the general theorem and all-length
coordinate proof above do not depend on enumeration.

The remaining step is to combine such exact fragment constraints across more
than one shared TH component, where the fragment network may also contain
closed P-only cycles. A coarse Hall graph omits essential state. An appropriate
global condition must guarantee actual TH connections and unique ownership of
each physical fragment, rather than separately feasible routes alone.

[Computational output](../output/shared-th-star.json) records each scope. The
[seven Lean declarations](../formal/SubQuorum/SharedTHStar.lean), with
[local execution and axiom audit](../output/shared-th-star-formal.json), prove
all-finite-word edge-count partition, absence of monochromatic outputs iff
alternation, alternating/blocked word counts for all s, and conditional balanced
endpoint arithmetic. The geometry-to-word and physical-resource adapters,
coordinate feasibility, and individual-pair Hall projection remain written.
This is not end-to-end grid Lean. A separate [independent review ACCEPT](../output/shared-th-star-review.json)
covers this star theorem and reports rerunning the submitted checker, reproducing
510 words, 40 positive/40 blocked lengths and 204 pair controls with byte-identical
and parsed-equal JSON. It did not execute Lean or the helpers’ standalone suites.
The general contact-network/cycle-credit theorem is outside that review.
