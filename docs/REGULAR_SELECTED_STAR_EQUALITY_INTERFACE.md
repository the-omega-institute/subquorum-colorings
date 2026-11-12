# Necessary interface at regular selected-star equality

Let G be a nonempty finite simple k-regular bipartite graph, k>=4. Let S
be an inclusion-minimal two-star-forming set whose selected components
are stars, edges or isolates. Write d=|S|-beta_2(G). Use the fixed witness
assignment and notation from FULL_DEGREE_CAPACITY_FOR_SELECTED_STARS.md.

**Theorem.** If n=(12k-14)d>0, then each selected star is P3, and there
are exactly d star centres in each bipartition class. Each centre has
one private leaf witness and one leaf witness with a selected isolate
helper; all helpers are distinct. The chosen witness graph G[W] has two
parts of size 2d. In each part d vertices have degree k-1 and d have
degree k-2. In particular

    d>=ceil((k-1)/2)=floor(k/2).                         (1)

Thus no equality instance exists at order34 in regular degree4, or at
order46 in regular degree5. The complete graph-theoretic sharpness question
is not decided by this exclusion.

## Equality forces a fixed ledger template

The accepted whole-cut identity, with delta=Delta=k and after subtracting
(12k-14)d, is

    0=(2k-5)J+(2k-3)(T-2d)+(2k-3)(R-2d)+D
      +2F+(2k-1)(B-2d)
      +(2k-5)(s+mu)+(2k-7)b3+2z0.

Every summand is nonnegative and every displayed coefficient is positive.
Consequently

    J=D=F=s=mu=b3=z0=0, T=R=B=2d.

Now D=q-2b2=0, R=c-q+b2=2d, T=a+b2=2d, and
J=c+2q-a-2b2=0. Substitution into J gives 4b2=0. Hence

    q=b2=0, c=a=2d, e=4d, t=2d.                         (2)

The selected-size and total-vertex counts, together with B=2d, give

    m=(6k-14)d, u=(6k-12)d.                            (3)

Here m counts selected edge-component vertices, not edges.

There are e=2c distinct leaf witnesses. Every centre is clean since q=0,
and at least one chosen witness per centre is private. All touched
selected isolates have h=1, so H=sum h(i)=a=c. The witness-incidence cap
is also c, and exactly c of the 2c witnesses must be helped. Each centre
therefore has exactly one private witness and one helped witness. Each
helped witness has exactly one helper and the helpers are distinct.

## The witnesses must support their own degrees

There is a useful exact form of the cut slack. For any witness assignment
and any k, using the regular F_k expression and actual degree deficits,

    Fhat=F_k+epsilon_S-epsilon_U
        =(c+s+2q-H)+2|E(G[U])|+|E(U,W)|.                (4)

Indeed, expanding the exact degree sum over S gives

    |E(S,U)|=sum_(v in S)deg(v)-3e-m-q-H.

The difference sum_(v in U)deg(v)-|E(S,U)| is exactly
2|E(G[U])|+|E(U,W)|. Substitution yields (4).

For regular equality both deficits vanish, F=0 and H=c. Thus (4)
forces E(G[U]) and E(U,W) to be empty. Every private witness has exactly
one selected neighbour and no U neighbour. Regularity forces its other
k-1 neighbours to lie in W. Every helped witness has exactly two selected
neighbours, so its degree in G[W] is k-2.

Let c_A,c_B count the centres in the fixed bipartition classes. A leaf
witness has the same colour as its centre. Thus W_A contains c_A private
and c_A helped vertices; W_B contains c_B of each type. Counting the
edges of G[W] from each side gives

    (2k-3)c_A=(2k-3)c_B.

Therefore c_A=c_B=d. Each witness part has size2d. A private witness
has k-1 distinct neighbours in the other witness part, proving2d>=k-1
and (1). This uses simplicity at exactly the neighbour-count step.

## What the witness-interface condition does and does not prove

The necessary degree sequence for G[W] can be realized for every integer
d>=floor(k/2). Label each part by residues0,...,2d-1. Put an edge from
left i to right i+j modulo2d for j=1,...,k-2. Since k-2<=2d-1 these are
distinct nonzero shifts, giving degree k-2 at every vertex. Add the d
diagonal edges i--i for0<=i<d. Those designated private vertices now
have degree k-1 on both sides, and all other vertices have degree k-2.

This constructs only the witness interface. It neither completes S--U
nor proves the unrestricted dissociation optimum of a resulting graph.
In particular it supplies no extremal graph or improved asymptotic
coefficient. The general whole-cut bound and its six-ledger relaxation
remain distinct from graph-sharpness.

## A direct unit-grid resource consequence

For a full h-by-w rectangle and a selected-star minimal S with no selected
edge components, equation(15) in the whole-cut note with k=4,m=0 gives

    8d+c+q<=epsilon_S-epsilon_U<=2h+2w.

Consequently

    d<=floor((2h+2w-c-q)/8)<=floor((h+w)/4).             (5)

This is a perimeter-order cap for this specified class of selections.
The degree deficits are actual sums and the inequality holds for d<=0
as well. It does not show that all minimal forming selections of a grid
have this form, or prove arbitrary-width SF_2=beta_2=psi_sq.

All arguments here are general. No new enumeration or Lean verification
is claimed. Independent proof review returned **ACCEPT**. It reviewed this general
argument using the supplied whole-cut note as prior premises; no code
execution, Lean or historical-priority check was requested or claimed.
The full response is in `output/regular-selected-star-equality-review.json`.
