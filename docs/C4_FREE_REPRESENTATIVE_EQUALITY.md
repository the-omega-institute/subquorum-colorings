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

## Verification and limits

[Independent controls](../scripts/check_c4_free_representatives.py) construct
prime-order projective planes and check full incidence and pair-ownership
conditions. For q=2,3 they exhaust all subsets of one side and check the
pair bound for all opposite-side vertices with at least D-1 neighbors in
that subset. Exact occupied-set optimization separately checks Omega on
the Heawood and Mobius-Kantor graphs. These are checks, not proof premises.

[C4FreeRepresentatives.lean](../formal/StarForming/C4FreeRepresentatives.lean)
formalizes graph-level pair-owner uniqueness, the integer packing threshold
and its two-sided consequence. The graph-to-cardinality summation,
representative reduction, projective-plane axioms and full parameter
equalities retain the written proofs above; full formalization is not
claimed. All four declarations pass Lean4.33.0 with only propext,
Classical.choice and Quot.sound, as recorded in the
[formal receipt](../output/c4-free-representative-formal-check.json).

The [finite receipt](../output/c4-free-representative-controls.json) records
four planes q=2,3,5,7, a total of16640unused-side subsets, exact optimization
over81920occupied sets on the two small graphs, all16384Heawood
star-forming subsets and40000arithmetic checks. Reproduce with:

```sh
python3 scripts/check_c4_free_representatives.py --output output/c4-free-representative-controls.json
python3 scripts/check_cover_pullback_formal.py --lean /path/to/lean4.33.0/bin/lean --audit c4-representatives --output output/c4-free-representative-formal-check.json
```

Literature status: the representative reduction is due to Sahbi,
arXiv:2609.25128v1. This is a deduction from that reduction and pair packing.
External priority for the projective-plane specialization remains to be
established before making a manuscript novelty claim.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
