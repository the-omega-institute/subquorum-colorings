# Unbounded star-forming gaps in cubic bipartite graphs of girth six

19 October 2026. Regularity does not restore equality between the
dissociation number and the upper 2-star-forming number. The Heawood graph
already separates them, and an edge replacement construction gives a
two-connected cubic bipartite family with an unbounded linear gap. All
claims needed for that family have proofs below; finite searches only
discovered and checked the construction. No smallest-order or historical
priority claim is made.

## Statement and definitions

For each positive integer r there is a two-connected cubic bipartite
graph F_r, of order 14r and girth six, such that

    Gamma(F_r)=alpha(F_r)=7r,
    beta_2(F_r)=7r+floor(r/2),
    SF_2(F_r)>=8r.

Consequently

    SF_2(F_r)-beta_2(F_r)>=ceil(r/2)>=|V(F_r)|/28.

The exact SF value for the whole family is not needed or claimed here.
The coefficient 1/28 is not claimed optimal among cubic bipartite graphs.
This result complements the earlier nonregular subcubic family; it does
not improve that family's coefficient 1/22.

A set S is 2-star-forming if every x outside S has two distinct neighbors
in S, or a neighbor in S which itself has a neighbor in S. These are the
two possible positions of x in a non-induced K_{1,2} on S union {x}.
Minimality is inclusion-minimality, and SF_2 maximizes the size of a
minimal set. The dissociation number beta_2 maximizes the size of a set
inducing maximum degree at most one.

## The Fano plane and its Heawood incidence graph

Represent the seven Fano points by the nonzero vectors of F_2^3. Its
lines are the triples {x,y,x+y} for distinct nonzero x,y. Two distinct
points lie on exactly one line. Each point lies on three lines, and
dually each pair of lines meets in exactly one point. The incidence
graph H has the seven points and seven lines as its bipartition and an
edge for each incidence. This is the Heawood graph: it is cubic, has no
four-cycle, and has six-cycles from noncollinear point triples.

For an explicit labeling, use points i in Z/7Z and lines L_j with

    L_j={j,j-1,j-3},
    N(i)={L_i,L_(i+1),L_(i+3)}.

The differences of {0,1,3} contain each nonzero residue once, so this
cyclic presentation has exactly the Fano incidence property. Numeric
labels for verification are i for a point and 7+j for L_j.
An explicit identification with nonzero binary vectors, encoded as
integers, sends cyclic points 0,...,6 to 1,2,4,5,7,3,6. The three entries
on each displayed line have bitwise sum zero.

### The dissociation number is seven

**Lemma 1.** beta_2(H)=7.

Either bipartition part attains seven. Suppose that a dissociation set
has at least eight vertices; by taking a subset, assume it has exactly
eight. Let p and q be its numbers of points and lines. By point-line
duality assume p<=q, so p<=4.

For p=0 there are not eight lines. If p=1 and q=7, the selected point
has three selected incident lines. If p=2 and q=6, either selected point
has at least two selected incident lines, since only one line is omitted.

If p=3 and q=5, each selected point must lie on both of the two omitted
lines: otherwise at least two of its three lines would be selected.
Two distinct selected points would then lie on two common lines, which
is impossible in the Fano plane.

Finally let p=q=4. Each selected line contains at least two of the three
omitted points, since it can contain at most one selected point. At most
three lines can contain a pair from those three omitted points, because
each pair determines exactly one line. Four selected lines are therefore
impossible. This proves the upper bound.

### An eight-point minimal star-forming set

Choose noncollinear Fano points a,b,c and put n=a+b+c. Select the four
points a,b,c,n and the four lines

    ab={a,b,a+b}, ac={a,c,a+c}, bc={b,c,b+c},
    E={a+b,a+c,b+c}.

Call this eight-set S. The first three points and first three lines
induce a six-cycle. The point n and line E are isolated in H[S].

Every omitted point is one of a+b,a+c,b+c. It lies on its corresponding
selected side line and on E, hence has two selected neighbors. Every
omitted line is one of

    {a,b+c,n}, {b,a+c,n}, {c,a+b,n},

and contains a selected triangle point and n. Thus S is star-forming.

Deleting n or E fails at the deleted vertex itself, since it has no
selected neighbor. Deleting a triangle point, for example a, leaves the
outside line {a,b+c,n} with n as its sole selected neighbor; n is isolated.
Deleting a side line, for example ab, leaves the outside point a+b with
E as its sole selected neighbor; E is isolated. These eight deletion
witnesses prove minimality, since star formation is upward closed.
Therefore SF_2(H)>=8>7=beta_2(H), by a direct argument.

In the numeric labeling take

    S={1,2,3,5,7,9,10,11}.

Here 1,2,3 are the triangle points, 5 is n, and 7 is E. Deleting
1,2,3,5,7,9,10,11 respectively fails at 8,12,13,5,7,6,0,4.

## Removing one incidence: the saturated-port lemma

Fix an incident point P and line L, and let B=H-PL. Call P and L its
ports; only these two vertices have degree two in B.

**Lemma 2.** Every dissociation set D in B has size at most eight. If it
has size eight, both ports belong to D and each has exactly one neighbor
in B[D].

Deleting P from any D gives a dissociation set in H, because PL is the
only missing edge. Lemma 1 therefore gives |D|<=8. If an eight-set omits
either port, it is already dissociation in H, a contradiction. Both
ports must be selected.

Write p,q for the selected point and line counts, so p+q=8. We first
show p=q=4, without using a symmetry that fixes the chosen flag. If p=1,
the selected point P has its two remaining lines selected, impossible.
If p=2, the selected point other than P has at least two selected incident
lines because q=6. If p=3, the two selected points other than P must both
lie on both omitted lines, again impossible. The case p=0 is excluded by
the number of lines. The dual argument excludes q<=3. Thus p=q=4.

Let U be the three omitted points. Each selected line other than L
contains at least two members of U. There are three such selected lines,
so they are precisely the three pair-lines of U, and U is noncollinear;
otherwise all its pairs would determine the same line. Write U={a,b,c},
where a,b,c are linearly independent vectors.

The selected points are

    a+b, a+c, b+c, n=a+b+c.

The three selected pair-lines meet these four points at a+b,a+c,b+c,
respectively. Since L has at most two selected points in the original
plane, it meets U; since L is not one of the three pair-lines, it meets
U exactly once. Relabeling a,b,c, we have L={a,b+c,n}.

The port P is therefore b+c or n. If P=n, then b+c is adjacent in B[D]
to both L and the selected line bc, contrary to dissociation. Hence
P=b+c. Its remaining selected neighbor is bc, and L's remaining selected
neighbor is n. Both ports have selected degree exactly one, as claimed.

This proof covers every choice of incident P,L. No classification from
finite enumeration is used.

## The cubic composition

Choose in the numeric H the outside edge P--L with P=0 and L=8=L_1;
both endpoints are omitted by S. Take r disjoint copies B_i of H-PL,
and add the edges

    L_i--P_(i+1),       i modulo r.

For r=1 this restores H. For r>=2 the added edges connect different
copies. Denote the resulting graph by F_r. Each port receives exactly
one new edge, so every vertex has degree three. All new edges run from
a line to a point, preserving the bipartition. There are 14r vertices
and 21r edges.

### Star-forming minimality is preserved

**Lemma 3 (rewiring outside a fixed selection).** If two graphs on the
same vertex set differ only in edges with both endpoints outside a set
S, then S is minimal 2-star-forming in one graph exactly when it is so
in the other.

For every T subset S and x outside T, at most one vertex outside S can
belong to T union {x}. Thus the graphs induced on T union {x} are identical:
none of the changed edges can occur there. The star-forming property
therefore agrees for every T subset S, including S and all its proper
subsets, which proves the lemma. The same reasoning works for any fixed
star size, though only size two is needed here.

In the disjoint union of r copies of H, the union S_r of their eight-sets
is minimal star-forming: stars and deletion failures separate by component.
All removed and added interface edges have both endpoints outside S_r.
Lemma 3 preserves minimality, so

    SF_2(F_r)>=|S_r|=8r.

### Exact dissociation count without sharing a budget twice

For any dissociation set D in F_r, put d_i=|D intersect V(B_i)| and let
t be the number of copies with d_i=8. Lemma 2 gives

    |D|=sum_i d_i <= 7r+t.

If d_i=8, its two selected ports already have selected degree one inside
B_i. The adjacent port P_(i+1) must therefore be omitted, since it is
adjacent to L_i. In particular d_(i+1) cannot also equal eight. Thus the
eight-copies form an independent set in the cyclic order, and

    t<=floor(r/2),       |D|<=7r+floor(r/2).

More explicitly, the successor map sends every eight-copy to a distinct
non-eight-copy. Its image and domain are disjoint, so 2t<=r.

For r=1 the restored edge directly forbids d_1=8, giving the same bound.
Each copy is counted once, and each saturated port is used only to exclude
its following eight-copy; the bound does not reuse a shared surplus.

For the matching lower bound in B, the following sets are dissociation:

    D_8={0,1,2,3,7,8,12,13},
    D_7={1,2,4,5,7,10,13}.

The eight-set selects both ports; the seven-set omits both. Their induced
edges, respectively, are

    D_8: 0--7, 1--8, 2--12, 3--13;
    D_7: 2--10, 4--7, 5--13, with 1 isolated.

Assign D_8 to floor(r/2) nonadjacent copies and D_7 to the rest. Every
interface has an omitted endpoint, so the union is dissociation. This
attains the upper bound and proves

    beta_2(F_r)=7r+floor(r/2).

### Connectivity, girth and upper domination

Within each B, the edges of shifts zero and three form a spanning cycle:

    point i -- L_(i+3) -- point (i+3),

iterated modulo seven. Since adding three generates Z/7Z, this visits
all fourteen vertices. The deleted edge P--L_1 has shift one, so none of
these spanning-cycle edges was removed.

Removing any vertex leaves each affected copy connected by the remaining
spanning path, and destroys at most one interface edge because the ports
are distinct. For r>=2 the cyclic arrangement of copies remains connected,
including r=2 with its two distinct interfaces. Thus F_r is two-connected.
For r=1 the spanning cycle proves the same assertion.

The base has girth six. Any path inside B between its ports has length
at least five: a shorter odd path, together with PL, would give a
four-cycle in H. A cycle using interfaces must use all r interfaces;
within each traversed copy it joins the two ports. For r>=2 it therefore
has length at least 6r. The selected six-cycle in every copy survives,
so F_r has girth exactly six.

The shift-zero edges i--L_i give a perfect matching in each copy, which
was not changed by the interface operation. Either bipartition part has
7r vertices, so alpha(F_r)=7r. The classical bipartite identity Gamma=alpha
of Cockayne--Favaron--Payan--Thomason, already cited in the earlier note,
then gives Gamma(F_r)=7r. This uses that existing theorem, not a new
upper-domination identity.

The dissociation formula and minimal8r-set prove the stated gap. These
finite cubic graphs are nonplanar: a planar bipartite graph of girth at
least six has at most 3(|V|-2)/2 edges, whereas F_r has 3|V|/2.

## Scope and next questions

This settles the existence of connected, indeed two-connected, cubic
bipartite graphs with unbounded star-forming gaps, even with girth six.
It supplies full general proofs of the saturation rule and interface
accounting. Exact SF for this family, a sharp universal cubic gap bound,
unbounded gaps under three-connectivity and rectangular-grid equality
remain separate questions. General bipartite and planar-bipartite threshold
complexity is addressed by Bhattacharjee's external October 14 work;
complexity restricted to cubic or two-connected graphs is not settled here.
The [literature note](STAR_FORMING_LITERATURE_20261019.md) records the source,
scope and independent controls. No manuscript or email is changed.

## Verification and reproduction

The [independent checker](../scripts/check_cubic_starforming.py) constructs
the Fano incidence graph from binary-vector triples. Its
[control receipt](../output/cubic-starforming-controls.json) records all
16,384 base subsets, 114,688 literal-star/local-predicate comparisons,
all-proper-subset minimality, the exact finite base values beta_2=7 and
SF_2=8, and all 16,384 subsets of the broken-incidence block. Exactly four
eight-sets survive in that block, each satisfying Lemma 2. A port-state
transfer calculation and explicit attaining sets independently agree for
r=1,...,32; structural and minimality controls pass for those 32 graphs.
The optional independent C++ enumerator agrees on the base graph and values.
These finite checks support, and do not replace, the general proofs above.

The [Lean source](../formal/StarForming/CubicCertificate.lean) proves
rewiring invariance of star formation and inclusion-minimality on arbitrary
vertex types. It also checks the explicit Heawood graph's cubic simplicity,
the eight-set, its deletion failures and minimality, its cardinality, and
conditional arithmetic from the local capacity and dense-block inequalities.
The [Lean receipt](../output/cubic-starforming-formal-check.json) records
nine successful Lean 4.33.0 audits; the rewiring lemmas use no axioms and
the remaining declarations use only standard logical axioms. No sorry or
compiler-trust certificate is used. The Fano dissociation geometry, Lemma 2,
global cyclic embedding, exact beta attainment, connectivity and girth have
written proofs here; they are not claimed fully Lean formalized.

An independent Oracle review of this written proof is pending. Its
[receipt](../output/cubic-starforming-oracle-review.json) preserves the
original request and live handle; no approval is claimed before a response.

Reproduce the controls with Python 3 and the optional C++20 enumerator:

    python3 scripts/check_cubic_starforming.py --output output/cubic-starforming-controls.json
    g++ -std=c++20 -O3 scripts/explore_subcubic_starforming.cpp -o /tmp/cubic-starforming-check
    python3 scripts/check_cubic_starforming.py --cpp /tmp/cubic-starforming-check --output output/cubic-starforming-controls.json
    python3 scripts/check_subcubic_formal.py --cubic --lean /path/to/lean-4.33.0 --output output/cubic-starforming-formal-check.json
