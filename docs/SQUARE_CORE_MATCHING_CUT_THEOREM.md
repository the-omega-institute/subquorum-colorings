# A sharp matching-cut bound for physical square-owner templates

13 November 2026. The construction below gives a sharp all-helper template
bound and a conditional improvement of the subcubic star-forming gap. Graphs
are finite and simple. A dissociation set induces maximum degree at most one;
its maximum cardinality is denoted by beta_2. For a template H with specified
helper set I, beta_I(H) is the maximum cardinality among dissociation sets
containing every vertex of I. Thus beta_2(H)>=beta_I(H).

## 1. Template and result

The physical bipartite graph H has disjoint layers I,X,C of orders b,2b,2b.
Each helper i has two distinct witness neighbours in X, and these pairs
partition X. Each witness has exactly one distinct owner in C; owner:X->C
is a bijection. The remaining edges are a partial matching Q on X and the
owner core H[C]. There are no other edges. Suppose every owner-core component
is an isolated vertex, an isolated edge or a four-cycle. Let t count its
four-cycles. Then 4t<=2b, and

**Theorem 1.** A dissociation set containing all helpers can be constructed
with cardinality at least

    3b-floor(t/2) >= ceil(11b/4).                         (1)

The refined bound is sharp for every pair of integers b,t with b>=2t>=0,
allowing disconnected templates. In particular 11/4 is a sharp uniform
coefficient for beta_I in this class. No equality claim for a connected
class or for the unrestricted star-forming gap is needed here.

The algorithm uses graph bipartition and matching-neighbour selection. Those
operations take linear work; the provided deterministic implementation sorts
labels and has polynomial runtime. It does not invoke an exponential
independent-set search or an external independence theorem.

## 2. An independent set across a matching cut

Pair the two witnesses of every helper by an auxiliary edge P. P is a
perfect matching preserving physical bipartition colour. Q reverses that
colour. These are distinct types of adjacency: P is virtual, whereas Q is
a physical witness edge.

Let V be the witnesses whose owners belong to core four-cycles. Each square
has two owners of either physical colour. Pair the opposite owners in each
square and transport those pairs to witnesses, obtaining a perfect matching
R on V. It preserves physical colour. Write V=V0 disjoint-union V1, where
|V0|=|V1|=2t. Restrict P and Q to V; both restrictions may be partial.
Let J be the simple union of these restricted matchings and R. Coincident
P and R edges are a single adjacency.

**Lemma 2.** This graph J has an independent set Y of size at least
ceil(3t/2).

**Proof.** Inside either physical side, P union R is bipartite with equally
sized proper classes in every component. To see this, first remove a
coincident P,R edge and its two vertices as a two-vertex component: neither
endpoint can have any other P or R edge. In the remaining union, matching
types alternate. A path must begin and end with R, because R covers every
vertex; it therefore has even order. A cycle is alternating and also even.
Each such component has two proper classes of equal size.

Choose one proper class in every component on V0 and call their union Y0.
Its cardinality is exactly t. The Q-neighbours of Y0 occupy at most t vertices
of V1, because Q is a matching. At least t vertices of V1 remain. Their induced
P union R graph is bipartite; in every component choose a larger proper
class, obtaining Y1 of cardinality at least ceil(t/2). Both Yi are independent
inside their physical sides, and no Q edge joins them. Therefore

    Y=Y0 union Y1,   |Y|>=t+ceil(t/2)=ceil(3t/2).

All P,Q,R adjacencies have been respected simultaneously. QED.

For t=0 the construction returns the empty set. Reversing the roles of V0,V1
also works; the implementation constructs both alternatives and returns a
larger one. Their sizes are not added.

## 3. Physical extension and exact rounding

Since Y is independent in R, its owners contain at most one endpoint of each
opposite-owner pair. Extend those owners to a set Z containing exactly one
endpoint of every such pair, so |Z|=2t. Each square in C-Z retains one owner
of each physical colour, which form an edge. All nonsquare core components
remain isolated vertices or edges.

Set D=I union (C-Z) union Y. Each selected witness has its owner in Z,
so that owner is absent; it has no selected Q-neighbour. P-independence gives
at most one selected witness per helper. Hence each witness pairs only with
its helper, each helper meets at most one witness, and the selected owners
induce only edges and isolates. These are all possible incidences, proving
that D is an actual dissociation set in H. In particular,

    |D|=b+(2b-2t)+|Y|
        >=3b-2t+ceil(3t/2)=3b-floor(t/2).

As t<=b/2, its right side is at least 11b/4, giving (1) after integer rounding.
The exact integer surplus needed below is

    4|D|-11b >= b-4floor(t/2)
                  =b-2t+2(t mod 2)>=0.                   (2)

Every helper and every opposite-owner pair has a unique allocation; no
independent-set alternatives or surpluses are spent twice.

## 4. A sharp twenty-vertex block and all refined parameters

Take b=4 and identify witnesses and their corresponding owners by indices
0,...,7. The helper pairs, witness edges, physical witness colours and core
squares are

    P: 01,23,45,67;
    Q: 12,34,56,70;
    physical colours: 0,0,1,1,0,0,1,1;
    owner-square cyclic orders: (0,2,4,6), (1,3,5,7).

Give each helper and each owner the colour opposite to its witness. These
instructions define a physical bipartite template on twenty vertices.
Here A=P union Q is C8. The opposite-owner matching is R=04,15,26,37;
J is the Wagner graph (the eight-vertex Mobius ladder). This identification
is descriptive, with no novelty claim for that known graph.

We prove beta_I<=11 directly. Let D contain all four helpers, let U be the
indices of its omitted owners, and let Y be its selected witness indices.
Every square loses at least two owners, so |U|>=4 and U meets each of the two
owner-index sets in at least two places. Every selected witness forces its
owner to be omitted, giving Y subset U. Also Y is independent in A: a helper
cannot meet two selected witnesses and a Q edge cannot join two selected
witnesses already meeting helpers. Consequently

    |D|=4+(8-|U|)+|Y|<=12.

Equality would require Y=U and hence A-independence of U. In C8 every
independent set has at most four vertices, and the only independent sets of
size four are the two alternating classes, namely all even or all odd
indices. Neither meets both owner squares in at least two places. Equality
is impossible, and beta_I<=11. Theorem 1 attains eleven, so beta_I=11.
(The independent finite optimizer also gives beta_2=11 for this block.)

Dissociation sets containing all helpers restrict independently to disjoint
template components. Thus beta_I is additive for disjoint unions. Take
floor(t/2) copies of this block. If t is odd add a single-square template
with b=2 and Q empty. Its beta_I is six: retain adjacent owners of the square
and one witness from each of the two helpers whose opposite-pair owners
were omitted. Finally add b-2t square-free one-helper templates with Q empty
and no core edges, each with beta_I=3. The general upper bound beta_I<=3b
in either added block follows from the injection of selected witnesses into
omitted owners. The resulting template has exactly b helpers and t squares,
and its exact beta_I is 3b-floor(t/2). This proves refined sharpness for all
feasible b,t, as well as the coefficient 11/4 at b=4s,t=2s.

## 5. Conditional lifting to an arbitrary minimal selected set

A two-star-forming set S covers every vertex outside S by a not necessarily
induced K_(1,2) containing exactly two vertices of S. Minimality means
inclusion-minimality. SF_2 is the maximum cardinality of such a minimal set.
Fix a minimal S in a bipartite graph G of maximum degree three. Use the
proved disjoint deletion-witness extraction in
`SHARP_BIPARTITE_STAR_FORMING_GAP.md`, restated and lifted in
`UNRESTRICTED_SUBCUBIC_GAP_IMPROVEMENT.md`. Here are the full counts and
compatibility facts used in this consequence.

Let R_S be the selected isolates and selected isolated-edge vertices, and I_S
the selected isolates. Select p disjoint triples (c,ell,x), where ell is a
selected leaf with only selected neighbour c and x has only selected
neighbour ell. Remove both c and ell from the remaining selected owner list.
Each remaining selected owner has a distinct outside witness, whose selected
neighbourhood is its owner, possibly with one isolate. Let u count these
pairs. The pairs and triples are vertex-disjoint, and

    |S|=|R_S|+2p+u.

Let a count isolates incident to exactly one assigned pair witness, b those
incident to at least two, and b3 those incident to exactly three. Maximum
degree three allows no larger count. The two established dissociation
exchanges give 2d<=min(a+b,p+b), where d=|S|-beta_2(G). Also
u>=a+2b+b3, |R_S|>=a+b and n>=|S|+p+u.

The b'=b-b3 isolates with exactly two assigned pair witnesses form the helper
layer of an actual induced template, with their 2b' witnesses and distinct
owners. Its owner degree is at most two, and its witness interface is a
partial matching. The condition for the following theorem is on THIS actual
extracted owner core: it must have only P1,P2,C4 components.

All R_S outside those helpers and the p chosen leaves can be retained with
ANY dissociation set of the template. They induce edges and isolates, have
no selected-core cross edges, and no edge to a template witness, whose only
selected neighbours are its specified owner and helper. The retained set
has size L=|R_S|-b'+p. Thus (1) and (2) give

    beta_2(G)-L >= 3b'-floor(t/2),
    W:=4(beta_2(G)-L)-11b' >= b'-4floor(t/2)>=0.       (3)

Put

    m=min(a,p), alpha=a-m, pi=p-m,
    e=u-a-2b, r=|R_S|-a-b, q=n-|S|-p-u,
    tau=m+b-2d.

The preceding witness facts give
r,alpha,pi,e-b3,b3,q,tau>=0. Substitution using the exact vertex counts gives

    n=10d+m+r+3(alpha+pi)+2e+q+5tau,
    beta_2(G)-L=2m+alpha+pi+3b+e-b3-d,
    2d+W=7m+4(alpha+pi)+4e+7b3+tau.

Eliminate m from seven times the first identity using the third. This yields
the exact nonnegative identity

    7n-72d = W+7r+17(alpha+pi)+10(e-b3)
                +3b3+7q+34tau >=0.                       (4)

**Theorem 3.** If the actual extracted core described above has only
P1,P2,C4 components, then

    |S|-beta_2(G) <= floor(7n/72).

More precisely its margin is bounded by the right side of (4), with W
at least the structural surplus in (3). This bounds SF_2(G)-beta_2(G) when
a maximum-cardinality minimal S admits such an extraction. Passing from a
larger core to an induced subcore can leave P3 components, so a larger
square-core presentation alone does not establish the hypothesis.

The conditional coefficient 7/72 improves the preceding square-core 5/51
certificate. The unrestricted 7/71 coefficient remains the applicable bound
without this extraction condition; no unrestricted 7/72 or sharp 7/72 claim
is made. The independent square-core matching-cut lemma does not establish
physical multiple-Hall grid routing or the general grid triple equality.

## 6. Verification and dependencies

Run with assertions enabled and without PYTHONOPTIMIZE:

    python3 -B scripts/check_square_core_matching_cut.py

The checker independently rebuilds auxiliary adjacencies, literally optimizes
small independent sets, scores all returned physical dissociation sets and
checks their minimal selected sets. It compares small physical models with
an independent dissociation recurrence and the two fixtures additionally
with the exact all-helper matching optimizer. It also checks every minimal
selection in the stated complete small labelled bipartite graph controls,
nonempty retained exterior resources, physical relabellings and colour
reversals. The sharp block's permitted omission sets are checked directly.
Larger random controls and disjoint block instances test implementation;
the written arguments above prove all sizes and sharpness. Formal zero-slack
ledger rays verify arithmetic only, without claiming graph realizability.
The generated report records exact finite scope and deterministic digest.

The matching-cut proof is self-contained. It supersedes a local proposal to
apply Staton's general 5n/14 independence theorem to J; that intermediate
implementation was archived privately rather than published as the final
result. The inherited witness extraction and older suppliers are unchanged.
No new Lean execution, priority claim for general independence theorems,
email transmission or modification of the October submitted paper is part
of this result. Independent review status is recorded separately in
`output/square-core-matching-cut-review.json`.
