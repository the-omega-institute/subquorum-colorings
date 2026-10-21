# Aligned root-pair batches and an unbounded old-band obstruction

Date: 22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Setting and statement

Use the immutable original endpoint/support/matching records, physical tiles
with coordinate floor division by two, and Phi=N+S+2F-E from
`SECONDARY_TEN_ROOT_BAR_PAIR_COMPENSATION.md`. All originals are full even U
or standard rotors as stipulated there. Source-labelled directed events exclude
the source's original supports even after those supports become occupied.

Consider a finite collection of that note's maximal-short-return instances,
translated by even row and column offsets, without rotations or reflections.
Their root sites p_i are distinct. For each instance retain its local old union
H_i and choose its EAST root O_i and EAST next owner V_i. Write P_i={O_i,V_i}.
All chosen new originals lie outside a common old inventory B containing every
H_i, and all distinct original records in B and the P_i are endpoint-disjoint.
Containment is containment of originals with their immutable records. When
these are actual owners in a complete extension, the earlier classification
provides their form; the counting theorem itself needs just the displayed
records and endpoint disjointness, not an extension-existence assertion.

In each translated local chart:

* C=h+13 is odd; O has bar rows t,t+1, near column C, near tip30,
  even far column X=C+B0-1, and even far tip v0=t+f0.
* V has bar rows s,s+1, even near column C-1, near tip22,
  odd far column C+B-2, and even far tip v=s+f.
* t<=22, s<=18, s<=t-2; breadths are even >=6 and depths even >=4.
* eta=1 exactly when B=B0+2 and v>=t. With delta0,kappa as in the
  pair note, the local pair gain is
  ell_i=2-delta0-eta-kappa+2*kappa*delta0.

Put r=#{i:eta_i=0}, g_i=Phi(B+P_i)-Phi(B), and a_i=g_i-ell_i.
Then there is a nonreusing cross-pair debit estimate

    C_new/new := 2|F_cooperative|-|E_cross| >= -r,                 (1)

and the exact common-baseline ledger gives

    Phi(B+union_i P_i)-Phi(B)
      = sum_i(ell_i+a_i)+C_new/new
      >= sum_i a_i+sum_i(ell_i-1_{eta_i=0}) >= sum_i a_i.          (2)

Thus every new/new cross-pair loss is paid once by its contacted root pair's
own local credit. The old-baseline adjustments a_i remain explicit. No
nonnegativity of their sum is asserted for arbitrary B.

## Owner injection

O has charge+1, whereas V has charge-1, so the two roles cannot be the same
original. The near column of O is its unique minimum endpoint column, and the
last endpoint in that column is p_i+(5,0). Thus its immutable endpoint set
determines p_i: distinct root sites give distinct O originals.

The two degree-one endpoints of an EAST V are its leg tips. One tip is x_i=
p_i+(-3,-1), even/even; the other has even row and odd column. Consequently
x_i is the unique even/even terminal. Even translations preserve these
parities, and distinct p_i give distinct x_i and hence distinct V originals.
Every new source contribution to N+S is therefore counted once. Receipt
disjointness still requires the geometric arguments below.

## Aligned-bar packing

Lemma. A full U whose bar top is even, left column even and right column odd
has its whole endpoint-tile footprint inside the aligned interval of its bar
columns. Two endpoint-disjoint U originals in this phase have disjoint entire
endpoint-tile footprints, regardless of their widths, depths or translations.

Proof. Sharing a tile with a column in an interval starting even and ending
odd forces one's column into that same interval. Order the two even bar tops
s1<=s2. If an endpoint of the first U shares a tile with an endpoint of the
second, its row is at least s2, since s2 is even. If the tops coincide, the
first bar contains the first endpoint's column at row s2. If they differ,
s2>=s1+2, so the first endpoint must lie on a continuous leg, which again
contains that column at row s2. The column lies within the second bar's
aligned interval, giving a common endpoint at row s2, a contradiction.
This is an interval proof with no upper bound on any parameter.

It applies to all V_i. The column phase is essential: U(8,10,10) in chart
(r,c) and its translation by (4,8) are endpoint-disjoint positive originals
but have four physical endpoint tiles in common.

## Protected root tiles and the unique foreign port

Every tile in the near boundary column of O_i is full in H_i+O_i+V_i.
From t through row20, V and O supply its left and right columns. At top
row22 the left cells are V at22 and P0 at23. At top rows24,26,28 P0 supplies
the left column. At top row30 the left cells are P0, and the right cells are
O at30 and Q at31. O's bar-interior tiles are full within O itself. Since
all originals are endpoint-disjoint, no foreign new original can touch any
of these tiles. Only O's far boundary tile column, with columns X,X+1,
can meet a foreign new original.

Two O originals cannot share a tile: it would have to be both far boundary
columns. Both occupy the even column X, and their far row intervals start
and end even. Overlapping tile-row intervals therefore contain a common
even endpoint row, contradicting endpoint disjointness. Combined with the
V packing lemma, every possible new/new shared tile is O_i/V_j with i!=j.

A V bar fills both rows of every tile it meets, so it cannot share a tile
with O_i. V's near column is even, as is X; a shared near-leg tile would
again force an endpoint collision in its even top row. Thus a foreign
contact must use V_j's odd far leg at X+1.

If that V bar top s_j lay in O_i's far interval [t_i,v0_i], its bar would
also contain (s_j,X), an endpoint of O_i. A shared tile of the two continuous
even-start/even-tip intervals implies a shared actual even row. Hence
endpoint disjointness forces s_j<t_i and its far leg contains

    (t_i,X+1).                                                   (3)

Every V contacting O_i would contain this same point. There is at most one
such V. If eta_i=1, its own V_i already contains (3), so no foreign V can
contact O_i at all. Each root with eta_i=0 therefore has at most one debit.
There is no analogous bound on how many roots one V may contact.

## Exact debit and common-baseline ledger

An odd-row endpoint of any of these new U originals has its preceding
even-row endpoint in the same column. Consequently no vertical intratile
event can run between two different new owners: its odd-row endpoint would
force an endpoint collision at the even row.

In an O/V foreign contact, O directions toward the foreign column survive
exactly at odd rows; V directions toward O survive exactly at even rows.
Every shared tile below the terminal overlap tile has both endpoint columns
full. It contributes two cross events and one cooperative full tile, net
zero. At the sole final tile of the overlap, at least one column stops at
its even top row. There is exactly one cross event. The tile is either
incomplete, giving -1, or completed by old endpoints, giving +1. Thus the
entire contact contributes at least -1. A tile cannot belong to two foreign
contacts: O/O and V/V tile overlap have already been excluded. Charging this
single possible loss to the contacted root proves (1) without reusing credit.

For completeness, define F_i as the full tiles newly created by B+P_i.
The sets F_i are disjoint: any missing baseline cell in a tile in F_i must
be supplied by P_i, so another endpoint-disjoint P_j cannot also complete it.
They also cannot contain an endpoint of a different P_j. Let F_cooperative
be all remaining newly full tiles after the simultaneous addition. The
new event sets from the individual additions are disjoint when owners are
given their fixed global labels. The only additional events are E_cross,
whose source and target belong to different P_i. Old events remain old.
These partitions prove the equality in (2). Finally kappa=1 implies eta=1,
so eta=0 gives ell=2-delta0>=1; eta=1 gives ell>=0. This proves both
inequalities in (2).

## An explicit family: one receiver can contact arbitrarily many roots

For every integer n>=1, take n copies of the local old parameters
h=12,g=4,L=6,D=16,F=4, translated by (0,100i), 0<=i<n. Define

    C_i=25+100i, X=25+100(n-1)+7,
    t_i=-10(n-1-i), B0_i=X-C_i+1, f0_i=4.

Choose O_i=U(B0_i,30-t_i,4) with chart (t_i+r,C_i-1+c).
Put s_i=t_i-6 and choose V_i with chart (s_i+r,C_i-2+c):

    V_0=U(B0_0+2,28-t_0,8-t_0),
    V_i=U(6,28-t_i,4) for i>=1.

All dimensions are admissible even numbers. The local old endpoint blocks
have column range [-34,31]+100i and lie below all new bars. Their column
ranges are disjoint. New near stems meet only their own old blocks, and
their local frontiers are legal. X is beyond every old endpoint. Root far
intervals [t_i,t_i+4] are separated by ten rows. The long far stem of V_0
is at X+1 and ends at2, so it passes outside the root bars, meeting the
physical far tiles of every O_i but none of their endpoint columns.
For i>=1, V_i's far stem ends at t_i-2; its bar begins four rows after
the preceding root bar top, at that root's far-tip row but strictly left
of X. These facts also exclude every new/new endpoint
collision. They give a general endpoint-disjointness proof for every n.

The only foreign contacts are O_i/V_0, i>=1. Write j for half the length
of the overlap interval: j=2 except at the final root, where j=1.
Each contact has j full tiles, 2j+1 cross events and net -1.
There are no cooperative receipts
with another old block: new bars are above all old endpoints, far stems
are beyond their rightmost aligned boundary, and near stems lie inside
their separated column ranges. Thus a_i=0 for B=union H_i. Locally,
eta_0=1 and all other eta_i=0; delta0_i=kappa_i=0. Therefore

    sum ell_i=2n-1, C_new/new=-(n-1), simultaneous gain=n.         (4)

If instead all P_i with i>=1 are retained in the OLD inventory and only
P_0 is added, its exact marginal is 1-(n-1)=2-n, unbounded below.
This refutes arbitrary-old-extension monotonicity and any proposed rule
allowing just one contact per receiving V. It does not refute (2), a
complete-extendible-family inequality, or the global target: complete
extension of this partial family has not been established.

## Validation and remaining task

`develop/check_aligned_bar_batch_compensation.py` checks 2161 disjoint
aligned U pairs, 614 collision controls, the opposite-phase counterexample,
and ten full-source batches at n=1,2,3,6,12 with two even translations.
It checks global event labels, exact cooperative tiles, each foreign debit,
zero old adjustment, (4), and the old-extension marginal 2-n.

`formal/SubQuorum/AlignedBarPacking.lean` passes Lean4.33.0: 14 explicit
declarations, including 11 theorems, with individual ordinary-axiom audits,
no warnings, sorry or native evaluation. It proves aligned U tile packing,
root-anchor uniqueness, the bar-precedence implication, near-column full
coverage, the eligible-root credit bound and the final ledger arithmetic.
The source-role adapter, event partition, one-contact geometry, and the
unbounded family's source construction remain general written proofs.
The finite controls supplement those proofs. This new batch theorem has
not yet received independent Oracle review; the two prerequisite root/pair
proofs have completed ACCEPT reviews, with the pair checker domain corrected.

The next mathematical task is to bound the external old adjustments a_i
under actual complete-family constraints. Other root directions, rotations,
nonmaximal returns, arbitrary catalogue coverage, full-family allocation,
the global 5/6 improvement and rectangular-grid triple equality remain open.
