# Exact signed gluing across a shared original source

21 October sharpening: the [canonical gate-consumption theorem](MARKED_SIDE_GATE_CONSUMPTION.md)
proves that the duplicate count d_s below is identically zero in actual
complete-source configurations. A marked positive side has a single fixed
gate consumer; marking it in both branches would place that consumer in
their one-source intersection, which cannot consume its own original
support. Thus the physical margin identity is
mu(F)=mu(L)+mu(Right)-N_s-S_s. The earlier OR-count proof remains below;
the independent review of its reserve dependency/deletion criterion does
not cover this subsequent sharpening.

20 October 2026. A complete feasible U/rotor family can be split legally at
a single original source whenever its exclusive sides have no endpoint edge
between them. Unlike endpoint-component additivity, the two restrictions now
SHARE that entire source. The exact reserve formula is

    R(F)=R(L)+R(Right)-S_s,                         (1)

where S_s=max(0,-charge(s)) is the shared original negative mass. Actual
mark multiplicity gives the exact allocation-margin formula

    mu(F)=mu(L)+mu(Right)-N_s-S_s+d_s.              (2)

Here N_s is1 for a positive separator and0 otherwise; d_s counts its actual
canonical sides marked in BOTH restrictions. Thus shared source mass cannot
be spent separately on both branches. The theorem applies to arbitrary
permitted phases, dimensions, recurring owners and numbers of branches.
It is a structural reduction for the full unrestricted allocation problem,
not a proof of that inequality or rectangular-grid equality.

## 1. Hypotheses and the source contact graph

Keep the complete fixed-source hypotheses of
[the retention theorem](SOURCE_RETENTION_HORN_CLOSURE.md): pairwise disjoint
original endpoint sets P_i, all unchanged matching edges, original supports
T_i with unique original occupied anchor a_i(x), and a complete feasible
full fusion. Each original endpoint tile profile is connected, as in the
established U/rotor catalogue. The partition into physical2x2 tiles stays fixed.

Let F=A disjoint-union {s} disjoint-union B, with A,B nonempty owner sets.
Assume NO lattice edge joins an endpoint of an A-source to an endpoint of
a B-source. There may be arbitrarily many contacts from either side to s.
Put L=A union{s}, Right=B union{s}, retaining each whole original source.

Equivalently, form the source contact graph whose vertices are original
sources and whose edges are actual adjacencies between endpoints of different
owners. Remove s, partition the remaining graph components into two nonempty
groups, and restore s to each. A source may contain many endpoints and contact
several other sources repeatedly; one graph edge does not represent one unit
of reserve. If the full source graph is connected, s is an articulation and
both restrictions also have connected endpoint graphs.

## 2. Each restriction is actually complete feasible

We prove the claim for L; the other side is symmetric. Its occupied set is
exactly the union of the original O_i=P_i union T_i of retained sources.
Take a mandatory selected x in L and a retained producer i. Its original
anchor a_i(x) persists. If x remains selected in the full family, full
feasibility immediately excludes any second occupied neighbor in L.

Otherwise x is an endpoint of a removed B-owner j. The edge from x to its
retained producer anchor excludes i in A by the no-cross-edge hypothesis.
Therefore i=s and x is an original support of s.

Suppose y!=a_s(x) is another occupied neighbor of x in L. It cannot belong
to O_s, by intrinsic single-source feasibility. Thus choose an A-owner k
with y in O_k. If y is an endpoint of k, its edge to x directly violates
the no-cross-edge condition. If y is an original support of k, let b be
its anchor in P_k. The distinct endpoint owners j,k imply b!=x. In the
full fusion y has occupied neighbors b and x, so it MUST be consumed into
an endpoint of a unique owner l.

If l is in A, its edge to x in B is forbidden. If l is in B, its edge to
b in A is forbidden. Thus l=s. But now y is an original endpoint of s,
while x is its original support with a second original occupied neighbor
y!=a_s(x), again impossible. This proves feasibility, including restored
support/support conflicts. No restored support is omitted.

Original endpoint degrees stay at least three because each retained O_i
persists; original endpoint disjointness preserves the matching. Hence these
are genuine complete-source restrictions, not merely feasible profile lists.
This geometric argument is what makes the following gluing identities legal.

## 3. Exact event and full-tile partitions

Use the SAME reserve ledger as
[the signed-extension note](CLOSED_EXTENSION_SIGNED_RESERVE_AND_LATTICE_OBSTRUCTION.md):

    R(I)=S(I)+2|Fmix(I)|-|E(I)|.

E is the actual source-labelled directed intratile event set. An event tail
and target are adjacent endpoints. They cannot have respective owners in A
and B, so each full-family event lies in L or Right. An event belonging to
BOTH would have its tail owner s and, by endpoint ownership uniqueness,
target owner s. This contradicts the event requirement that the target lie
outside the tail owner's ORIGINAL occupied set. Consequently

    E(F)=E(L) disjoint-union E(Right).               (3)

Fmix counts actual full endpoint tiles not originally full in any one
retained source. We now prove the analogous, less automatic fact

    Fmix(F)=Fmix(L) disjoint-union Fmix(Right).       (4)

Take a full tile Q of F. If it had exclusive endpoints from BOTH A and B,
look at P_s intersect Q. An original source's nonempty tile profile is a
connected subset of the four-cycle; the empty profile is also allowed.
The complement of a proper connected profile is connected: with zero,
one, two adjacent or three separator endpoints it is respectively the
cycle, a three-vertex path, an edge or a singleton. All complement vertices
are endpoints, since Q is full. A connected complement containing owners
from both exclusive sides must contain an A--B endpoint edge, forbidden.
The case of four separator endpoints has no exclusive endpoint. Therefore
every full tile is already full in at least one restriction.

Fullness in both restrictions would make all four endpoints belong to s,
so Q would be originally full and excluded from Fmix. Finally an old mixed
full tile cannot become a new owner's original full tile: endpoint ownership
is disjoint. This proves the exact disjoint mixed-full-tile partition (4).
Connected ORIGINAL tile profiles are essential here; disconnected diagonal
profiles would not give the complement argument.

Original negative mass has its ordinary inclusion-exclusion identity

    S(F)=S(L)+S(Right)-S_s.

Combine this with (3)--(4) to prove (1). A singleton original source has
no foreign event and no mixed full tile, so R({s})=S_s exactly. In
particular (1) is a valuation at these geometrically legal separators,
despite reserve being neither submodular nor supermodular on the general
feasible-source lattice. No lattice inequality is being assumed.

## 4. Actual marked sides and the exact demand correction

For a positive owner i in A, every endpoint witness marking one of its
canonical sides belongs to A or s: otherwise its endpoint contact is an
A--B edge. Such a witness cannot instead be an unconsumed foreign support,
because that support would have both its distinct original anchor and the
positive protector as occupied neighbors. Thus all actual marks of i are
unchanged in L. The same holds for positive owners in B and Right.

If s is positive, each of its two sides is marked in F exactly when it is
marked in at least one restriction. A single original source has no foreign
marks of its own. Define d_s as the number of its sides marked in both
restrictions; d_s is0 for a nonpositive separator. Then

    N(F)=N(L)+N(Right)-N_s,
    G(F)=G(L)+G(Right)-d_s.

Together with (1), these identities prove (2). Multiple witnesses for one
side are not multiple demands; d_s corrects precisely that overlap, not
the number of witness vertices or graph edges.

For r branches with pairwise no cross endpoint contact and common source s,
the same proof, or repeated binary gluing, yields

    R(F)=sum_t R(I_t)-(r-1)S_s,
    mu(F)=sum_t mu(I_t)-(r-1)(N_s+S_s)+D_s,

where D_s=sum over the two positive separator sides of(max(0,m_side-1)),
and m_side is the number of restrictions in which that actual side is marked.
For nonpositive s put D_s=0. The shared source is subtracted r-1 times,
leaving its original mass ONCE in the global ledger.

## 5. Consequences for a genuine allocation counterexample

All conclusions below are reductions of the FULL mu>=0 problem; no existence
of a counterexample is asserted. Choose a negative-margin complete source
family with the least possible number of original sources, if one exists.
The established endpoint-component restriction first lets it be connected.

We also use the independently established
[exact geometric reserve theorem](EXACT_GEOMETRIC_EVENT_RESERVE.md), Sections1--3:
every complete feasible restriction J in this same fixed-source U/rotor
catalogue satisfies

    2R(J)=A(J)+U0(J)+Z0(J)+L1(J)+2L2bar(J)+2L2mutual(J)+L3(J)>=0.

Section2 above proves that both separator restrictions meet that theorem's
complete-source and occupied-neighbor hypotheses; the original catalogue and
physical tile partition are unchanged. This supplies R(J)>=0 without assuming
allocation mu(J)>=0. Nonnegativity does not follow merely from the signed
definition S+2|Fmix|-|E|, or from minimum-counterexample reasoning.

* It has no zero-charge articulation source. For such s, N_s=S_s=d_s=0,
  so mu(F)=mu(L)+mu(Right). A negative full margin would give a smaller
  negative-margin complete fusion. All zero-charge sources here are rotor
  types; this reduction uses their ZERO original charge, not an added rotor
  capacity assumption.
* At a positive articulation, the two branches cannot mark a common actual
  canonical side of the separator. If d_s>=1, equation(2) gives
  mu(F)>=mu(L)+mu(Right), again forcing a smaller counterexample. Applied
  to all branch partitions, this means each separator side may be marked
  from at most one branch in a minimal counterexample.
* A positive-articulation branch with no other positive source and no mark
  of s can be removed. Its margin is1+R(branch)>=1. In(2) d_s=0, so the
  complementary restriction has margin at most the full negative margin.
* At a negative articulation, individual nonnegative branch margins do NOT
  automatically suffice. The exact criterion is
  mu(L)+mu(Right)>=S_s. In particular, a branch without positive sources
  can be removed without increasing the margin whenever R(branch)>=S_s.
  More exactly, if J is that branch and K its complement sharing s, then
  mu(K)=mu(F)+S_s-R(J). For a particular known negative full margin, K
  remains a counterexample exactly when R(J)>S_s+mu(F). The stronger
  R(J)>=S_s gives a uniform guarantee from negativity alone. Proving such
  a shared-mass bound is a geometric obligation, not a consequence of legality.

The later [connected marked-hull construction](DEMAND_HULL_RESERVE_COMPARISON_OBSTRUCTION.md)
shows that this stronger shared-mass bound is false for arbitrary positive-free
branches: its separator V3 has S_s=k+7, while the complete connected branch
with no positives has R=k/2+18. For even k>=24 that branch cannot be deleted
without increasing the margin. The exact gluing and margin-dependent criterion
remain valid; a general pruning proof cannot assume universal branch coverage.

Thus a proposed proof by splitting along source articulations has an exact
shared-resource requirement. It cannot sum existing per-branch allocation
inequalities and count the separator's negative mass twice. The general
unrestricted allocation and grid equality remain OPEN, including negative
articulation transfers and source cores that have no such separator.

## 6. Complete connected example and verification scope

In the eight-source connected family of
[the preceding obstruction](CONNECTED_POSITIVE_SOURCE_CUT_OBSTRUCTION.md),
take s=V2, L={V1,V2,V3,V4}, Right={V2,V5,V6,V7,V8}. These are legal connected
restrictions. The original separator charge is-1. Direct complete-source
reconstruction gives

    R(L)=3, R(Right)=16, R(F)=18=3+16-1;
    mu(L)=3, mu(Right)=15, mu(F)=17=3+15-1.

The discrepancy is the ONE shared source mass. The identity holds for all
even k>=4 by the same fixed seam and separator theorem, not just the control
member k10. No positive source or actual mark has been relabelled.

Run `python3 develop/check_source_separator_transfer.py`. It verifies2080
actual legal separator splits across640 phase/isometry images of20 complete
fixtures, covering negative, zero and positive separator charges, and checks
the displayed connected example. Branch partitions are exhaustive through
eight branches; larger branch counts use singleton-branch samples. These
controls have d_s=0; positive duplicate-mark corrections remain covered by
the written union-of-witness proof, not positive finite examples. General
feasibility and valuation proofs are Sections2--4, not finite extrapolation.

`formal/SubQuorum/SourceSeparatorTransfer.lean` has three source-level
declarations: legal restriction under no cross endpoint contact, event cover
by the two restrictions, and event disjointness. These use actual abstract
endpoint/support/anchor/event predicates. The physical profile-complement
argument for full tiles, finite count valuation and canonical-mark adapter
remain written. No end-to-end Lean proof of(1),(2) or full allocation is
claimed. See the scoped execution receipt for the final build and axiom audit.
The previous Horn ACCEPT does not cover this new separator theorem.

Independent review e39795ea returned REVISE on21October: it accepted the
restriction and exact identities under the catalogue/mark hypotheses, but
requested the explicit R(J)>=0 dependency and corrected negative-deletion
wording. Both changes are supplied in Section5 above; they have not yet
received a subsequent independent verdict. The first review4633dbbd ended
in infrastructure_retry_exhausted and supplied no mathematical verdict.
