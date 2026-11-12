# Exact bipartite padding, connectivity and selected-star gap stability

All graphs are finite and simple. Write beta_2 for the maximum size of a
set inducing maximum degree at most one. A two-star-forming set forms every
outside vertex with two selected vertices and a not necessarily induced
K_(1,2). Minimality means inclusion-minimality.

**Result.** For every r>=2 and t>=1 there is an explicit connected bipartite
graph P_(r,t) with

    n=12r+2t, |S|=8r,
    beta_2(P_(r,t))=max(7r,6r+t),
    delta(P_(r,t))=kappa(P_(r,t))=t+1,
    Delta(P_(r,t))=6r+t,                                (1)

where S is minimal forming and induces exactly2r copies of P3 and2r
isolates. In particular it has no selected edge component. Hence

    |S|-beta_2(P_(r,t))=min(r,2r-t).                      (2)

Here kappa is vertex connectivity. No exact SF_2 value is asserted.

Fix any integer h>=2 and put t=h-1. For all r>=max(2,t), the graph is
h-connected, has minimum degree h, and has selected gap r at order
12r+2(h-1). The ratio tends to1/12 as r tends to infinity. Together with
the established selected-star upper bound floor(n/12), this proves:

**The coefficient1/12 remains asymptotically sharp even after imposing
any fixed lower bound on both minimum degree and vertex connectivity.**

The maximum degree in this construction grows with r; this is not a
bounded-maximum-degree or regular sharpness statement. It does not
contradict the strict unrounded-equality obstruction at minimum degree two.

The choice t=r gives a second useful conclusion:

    n=14r, beta_2=7r=n/2, |S|=8r,
    delta=kappa=r+1, Delta=7r.                           (3)

Thus a positive selected-star gap can coexist with beta_2=n/2 and
arbitrarily high minimum degree and vertex connectivity. In particular
it refutes the candidate strengthening

    4 beta_2(G)>=2|S|+|V(G)|                             (4)

for general bipartite selected-star minimal sets. At (3), its two sides
are28r and30r. This does not refute a version restricted to regular graphs
or full rectangles. The general constructions and parameter calculations
are proved next; finite checks are controls, not their proof.

## Exact dissociation number under a bipartite universal extension

Let H be a bipartite graph with nonempty fixed parts A,B and no isolated
vertices. Add t>=1 new vertices X in the A part and t new vertices Y in
the B part. Add all edges from X to B union Y and from Y to A. Keep all
old edges, and call the result J_t(H). Then

    beta_2(J_t(H))=max(beta_2(H), |A|+t, |B|+t).          (5)

The three lower bounds are attained by an old maximum dissociation set
and the two full bipartition classes.

For the upper bound let D be dissociation. If D avoids X union Y, it has
size at most beta_2(H). Suppose D meets X. A selected vertex of X is
adjacent to every vertex of B union Y, so D meets that opposite part in
at most one vertex. If there is no opposite vertex, |D|<=|A|+t. If the
opposite vertex lies in Y, it is adjacent to every A union X vertex, so
|D|<=2<=|A|+t. Otherwise the opposite vertex is some old b in B.
Its adjacency to all X forces D to contain exactly one X vertex. That
already uses its degree-one capacity, so all old A vertices chosen by D
avoid N_H(b). Therefore

    |D|<=|A|-deg_H(b)+2<=|A|+1<=|A|+t.

The middle inequality uses the no-isolate hypothesis. If D instead meets
Y, the symmetric argument gives |D|<=|B|+t. This exhausts all cases and
proves (5), without optimization or enumeration.

The no-isolate hypothesis should not be silently dropped at t=1. For
example, if H has one vertex in each part and no edge, the extension has
a dissociation three-set consisting of one new vertex and both old
vertices, while all three displayed bounds in (5) equal2.

There is also an exact formula without the no-isolate hypothesis. Put
delta_A=min_(a in A) deg_H(a) and delta_B=min_(b in B) deg_H(b), retaining
nonempty fixed parts and t>=1. Then

    beta_2(J_t(H))=max(beta_2(H), |A|+t, |B|+t,
                      |A|-delta_B+2, |B|-delta_A+2).    (5a)

The preceding case proof gives the upper bound before using deg_H(b)>=1,
and its symmetric case gives the other extra term. To attain
|A|-delta_B+2, choose an old b of minimum degree in B, one new x in X,
and every old A vertex outside N_H(b). The only induced edge is xb.
The other extra term is attained symmetrically. Together with the three
old lower constructions, this proves (5a). In particular (5) holds for
every bipartite H with nonempty parts whenever t>=2, even if H has
isolated vertices. At t=1, (5a) accounts exactly for the possible extra
unit due to an isolated old vertex. No formation assumption is needed
for either dissociation formula.

## Minimal forming sets survive the extension

Suppose S is minimal forming in H and has at least two vertices in each
part. Every new vertex then has at least two selected neighbours, so S
forms the extension. The old selected graph H[S] is unchanged. Moreover,
for every Q subset S and every old vertex v outside Q, the selected
neighbours of v and their adjacency inside Q are unchanged. Thus every
old single-deletion failure for S persists, including failure at a newly
omitted selected vertex. This proves minimality in J_t(H). In particular,
the induced selected components and |S| are unchanged. No new vertex is
selected, and no new resource is used to repair an old deletion failure.

## The underlying selected-star family

Use the accepted balanced family G_(r,r), r>=2, from
SELECTED_STAR_COMPONENT_GAPS.md. For completeness its vertices are2r
six-vertex blocks with c,l,m,i,p,h, and edges

    c--l, c--m, l--p, m--h, i--h.

The first r centres have colour0, the other r colour1; witnesses have
their centre's colour, and leaves/isolates have the opposite colour.
Add every edge between the2r witnesses of the first group and the2r
witnesses of the second group. Select c,l,m,i in every block. The parts
have size6r, the graph is connected and has pendant selected isolates.
The established complete structural case proof gives

    |V(G_(r,r))|=12r, |S|=8r, beta_2(G_(r,r))=7r.         (6)

The r>=2 condition matters: G_(1,1) has beta_2=8, not7. The proof of
(6), including unrestricted rather than forced leaf-retaining optima,
is in the cited note. The current theorem uses it as an established
input, rather than inferring it from a finite control.

Define P_(r,t)=J_t(G_(r,r)). Formula(5) and (6) give the beta value in
(1). Each selected part has4r vertices, so the preservation theorem
applies. The selected components remain2r P3 stars and2r isolates.

## Exact minimum degree, maximum degree and connectivity

Let H be any connected bipartite graph with a pendant vertex, with
nonempty parts A,B, and consider J_t(H). Old degrees increase by t;
new degrees are respectively |B|+t and |A|+t. Since delta(H)=1 and
both parts are nonempty, the minimum degree of the extension is t+1.

Deleting at most t vertices leaves the graph connected. If both X and
Y still contain a vertex, their surviving complete bipartite graph is
connected, and every surviving old vertex attaches to its surviving
opposite new part. If X is entirely deleted, the deletion budget t
forces that these are all deleted vertices. The entire connected H
survives, and all Y vertices attach to A. The case with Y deleted is
symmetric. Thus kappa(J_t(H))>=t+1.

An old pendant vertex has exactly t+1 neighbours in the extension.
Deleting those neighbours isolates it and leaves other vertices, so
kappa<=t+1. This proves exact connectivity, not just a lower estimate.

For H=G_(r,r), each old degree is at most6r, and both parts have size6r.
The new vertices have degree6r+t, which is therefore the maximum. This
proves all degree and connectivity values in (1). Equations(2)-(4) and
the asymptotic sharpness assertion follow by the displayed arithmetic.

## Verification and boundaries

Run `python3 -B scripts/check_bipartite_universal_padding.py`; it uses
only the Python standard library, with assertions enabled. It checks all
682 fixed-part bipartite graphs with each part of size one through three,
including 327 without isolates, and 1,364 padded exact optima at t=1,2.
The one-part exact optimizer is compared with every full vertex subset
on these graphs and their extensions. Eligible minimal selections are
tested by literal non-induced stars before and after padding.

Six physical P_(r,t) instances receive independent unrestricted exact
optimization over a total of 2,744,320 one-part subsets and 2,498 integral
vertex-split flow tests, covering every nonadjacent pair in each graph.
Together with an explicit cut of size t+1, these certify the connectivity
of those finite instances. Six larger controls up to order448 check
actual degrees, selected components, lower sets, formation and deletion
failures; their exact beta and connectivity use the general proofs.
The all-parameter
statements above rely on the case proof, the established (6), and the
connectivity argument. No finite enumeration replaces those proofs.
Independent proof-only review returned **ACCEPT**, including an independently
derived version of (5a). The first final execution task ended in terminal
browser infrastructure failure without a mathematical response. A fresh
integrated exact-source execution audit is pending; no external checker
execution is claimed here. Full responses and scope are in
`output/bipartite-universal-padding-review.json`. No regular-family, grid equality, exact
SF_2, historical-priority or Lean claim is implied.
