# Exact sub-quorum values from C4-free pair packing

19 October 2026. This note returns directly to Sahbi's representative
reduction. Its general proof is independent of finite enumeration and of
the star-forming architecture bounds. No priority claim is made.

## Definitions and theorem

A feasible representative pair consists of a matching M and a set T
disjoint from V(M), such that each vertex of T has at most one neighbor
in A=T union V(M). Set Omega(G)=max(|T|+|M|). Sahbi's reduction gives

    beta_2(G) <= psi_sq(G) <= Omega(G).

Here beta_2 is the maximum size of a dissociation set, whose induced graph
has maximum degree at most one. See [the grid proof](GRID_PROFILE_PROOF.md)
for the representative reduction and its source attribution.

**Theorem.** Let G be a finite simple D-regular bipartite graph without a
four-cycle, with D>=3 and N vertices in each part. If

    N <= 2(D-1)(D-2)+4,

then beta_2(G)=psi_sq(G)=Omega(G)=N. Equal part sizes also follow from
regularity by edge counting. Connectedness is not required.

## General proof, including ownership of the pair count

Fix a feasible pair and put m=|M| and B=V(G) minus A. Let t_L,t_R,b_L,b_R
be the T and B counts on the two sides. Each matching edge meets both
sides once, giving

    t_L+m+b_L=N,                t_R+m+b_R=N.

Suppose |T|+m=N+delta with an integer delta>=1. Subtraction gives

    t_R=b_L+delta,              t_L=b_R+delta,
    m+b_L+b_R=N-delta.                                  (1)

Each T_R vertex has at least D-1 neighbors in B_L, since it has degree D
and at most one neighbor in A. Assign to it all unordered pairs of its
B_L neighbors. No pair has two distinct owners: two owners and their two
common neighbors would be four distinct vertices forming a four-cycle.
Thus the assigned pair sets are disjoint, and

    choose(D-1,2) t_R <= choose(b_L,2).

Exchange L and R for the other inequality. With a=(D-1)(D-2)>0, multiply
by two and use (1):

    a(b_L+delta) <= b_L(b_L-1),
    a(b_R+delta) <= b_R(b_R-1).                          (2)

For nonnegative integer b, (2) forces b>=a+2. Indeed, if b<=a+1, then
b(b-1)<=ab, whereas a(b+delta)>ab because a>0 and delta>=1.
This contradiction also handles b=0. Hence (1) gives

    N=m+b_L+b_R+delta >= 2a+5,

contrary to the size hypothesis. Every representative objective is at
most N. One whole bipartition class is independent and has size N, so
N<=beta_2<=psi_sq<=Omega<=N. This proves the theorem. Each side's pair
count uses its own pairs; no pair or matching endpoint is charged twice.

## Every finite projective plane

**Corollary.** For the incidence graph of any finite projective plane of
order q>=2,

    beta_2 = psi_sq = Omega = q^2+q+1.

Each side has N=q^2+q+1 vertices and each degree is D=q+1. Two points lie
on a unique line, so a four-cycle is impossible. The threshold holds since

    2q(q-1)+4 - (q^2+q+1) = q^2-3q+3 > 0.

Writing q=2+k gives k^2+k+1>0. This uses only projective-plane axioms,
including for non-Desarguesian planes when they exist; it assumes neither
finite fields nor a classification.

For D=3, the theorem covers every C4-free cubic bipartite graph on at most
sixteen vertices. The Heawood graph in particular has

    beta_2 = psi_sq = Omega = 7 < 8 = SF_2.

The SF value has the independent general Fano proof in
[the cubic note](CUBIC_STAR_FORMING_GAPS.md). This separates SF from the
original sub-quorum parameter even under cubic regularity and girth six.
It does not refute the rectangular-grid triple equality; grids have
different local geometry. No equality is asserted for larger C4-free
regular graphs outside the theorem's range.

## Optimal-support rigidity and the first possible excess

The same ownership proof gives more information than the size threshold.
For any representative pair with objective N+delta>N, (1),(2) imply

    m+delta <= N-2a-4,              a=(D-1)(D-2).        (3)

Indeed both unused counts are at least a+2, and (1) is an equality.
In particular Omega<=max(N,2N-2a-4). At the first possible order
N=2a+5, the upper bound is N+1; attaining N+1 forces m=0. Any first-order
excess is therefore already a dissociation set, without matching edges.

There is also rigidity at objective exactly N. Equations (1),(2) remain
valid with delta=0. For each unused-side count b, they give

    b=0 or b>=a+1.                                      (4)

For b>0 divide ab<=b(b-1) by b. If N<=2a+1, the partition identity
m+b_L+b_R=N prevents both b counts from being positive. Thus one is
zero. The identities t_R=b_L,t_L=b_R show that T lies entirely in one
bipartition class. Every vertex of that class is occupied, and all
occupied vertices in the other class are matching endpoints. This
describes every representative pair of objective N, not just one choice
of an optimum. It does not require the matching itself to be empty.

For a projective plane, N<=2a+1 is equivalent to q(q-3)>=0. Consequently
**every optimum in every projective plane of order q>=3 has this one-side
singleton support.** The q=2 exception is necessary. In the normalized
F_2 triple labeling used by the controls, T={1,2,3,11,12,13} and
M={{0,8}} form a feasible Heawood optimum of objective7, with three
singletons on each side. This labeling is separate from the cyclic
Heawood labels used in the star-forming notes.

## Sharpness in the cubic case: the eighteen-vertex Pappus graph

The bound N<=8 for D=3 cannot be enlarged even to N<=9. Use vertices
0,...,17, with even vertices on one side. The odd neighborhoods are

| Odd vertex | Even neighbors |
|---|---|
|1|0,2,8|
|3|2,4,10|
|5|0,4,6|
|7|6,8,14|
|9|8,10,16|
|11|6,10,12|
|13|2,12,14|
|15|4,14,16|
|17|0,12,16|

This is the Pappus graph, also specified by the Hamilton cycle
0--1--...--17--0 and LCF sequence [5,7,-7,7,-7,-5] repeated three times.
Each point occurs in three triples and no unordered pair occurs twice;
the table therefore proves simple cubic bipartiteness and absence of C4.
The displayed spanning cycle proves two-connectivity. The ten-set

    S={0,1,4,6,7,9,10,12,13,15}

induces exactly the five edges0--1,4--15,6--7,9--10,12--13.
Thus beta_2>=10. With a=2,N=9, (3) gives m+delta<=1 for every positive
excess, hence Omega<=10. Therefore

    beta_2(Pappus)=psi_sq(Pappus)=Omega(Pappus)=10>9.

Every maximum representative pair has M empty. Furthermore every
ten-color sub-quorum coloring has a ten-vertex dissociation support and
uses a different color at every support vertex: an edge-containing class
would contribute a matching representative, which was just ruled out;
all classes are therefore edge-free, so each colored vertex has at most
one colored neighbor. Its support is a dissociation set of size at most
ten and has at least ten vertices to represent its ten colors.

The upper bound is the general counting proof, not the exact optimizer.
The finite table and ten-set are independently kernel-checked in Lean.
No novel claim about the Pappus dissociation value is made.

## Verification and limits

[Independent controls](../scripts/check_c4_free_representatives.py) construct
prime-order projective planes and check full incidence and pair-ownership
conditions. For q=2,3 they exhaust all subsets of one side and check the
pair bound for all opposite-side vertices with at least D-1 neighbors in
that subset. Exact occupied-set optimization separately checks Omega on
the Heawood and Mobius-Kantor graphs. These are checks, not proof premises.

[C4FreeRepresentatives.lean](../formal/StarForming/C4FreeRepresentatives.lean)
formalizes graph-level pair-owner uniqueness, six conditional integer
packing/rigidity statements and three finite Pappus graph certificates.
The graph-to-cardinality summation,
representative reduction, projective-plane axioms and full parameter
equalities retain the written proofs above; full formalization is not
claimed. All ten declarations pass Lean4.33.0 with only propext,
Classical.choice and Quot.sound, as recorded in the
[formal receipt](../output/c4-free-representative-formal-check.json).

The [finite receipt](../output/c4-free-representative-controls.json) records
four planes q=2,3,5,7, a total of16640unused-side subsets, exact optimization
over344064occupied sets on the three small graphs, all16384Heawood
star-forming subsets and40000arithmetic checks. Reproduce with:

```sh
python3 scripts/check_c4_free_representatives.py --output output/c4-free-representative-controls.json
python3 scripts/check_cover_pullback_formal.py --lean /path/to/lean4.33.0/bin/lean --audit c4-representatives --output output/c4-free-representative-formal-check.json
```

Literature status: the representative reduction is due to Sahbi,
arXiv:2609.25128v1. This is a deduction from that reduction and pair packing.
External priority for the projective-plane specialization remains to be
established before making a manuscript novelty claim. The
[source-specific context check](C4_FREE_LITERATURE_20261019.md) identifies
the relevant degree and subcubic results in Sahbi v4 and the concrete
limits of the external search. A separate
[independent proof audit](../output/c4-free-representative-oracle-review.json)
has been requested; its verdict is not presumed by the written proof.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
