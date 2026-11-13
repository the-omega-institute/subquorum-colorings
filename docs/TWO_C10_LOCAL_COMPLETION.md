# A closed two-
\(C_{10}\) owner class

This note isolates one local ingredient of the unverified \(C_{20}\) candidate.
It is a theorem about the owner class
\[
B=2C_{10}\sqcup kC_4,
\]
for every \(k\geq0\). It does not prove the global theorem with one auxiliary
\(C_{20}\); that theorem additionally needs an absorption argument coupling a
root region to all exterior owner families.

Let \(V\) be the common index set. Let \(P\) be a perfect matching on \(V\),
let \(Q\) be a partial matching, and put \(A=P\cup Q\). Assume that \(A\) is
bipartite and that a physical two-colouring is constant on \(P\)-edges and
opposite on \(Q\)-edges and on the owner cycles in \(B\). An omission set \(U\)
is permitted when \(B[V\setminus U]\) has maximum degree at most one. Then
\[
\boxed{
\min_{U\ \mathrm{permitted}}\nu(A[U])
\leq \left\lfloor {k+7\over2}\right\rfloor
\leq \left\lfloor {4k+20\over6}\right\rfloor .
}
\tag{1}
\]

The second inequality is elementary. The first is the useful local statement.

## Proof

Put a virtual matching on every owner \(C_4\), pairing opposite vertices. The
virtual edges are used only to prescribe an omission pattern; they are not
added to \(A\). Follow the components of \(P\) together with these virtual
edges. A component meeting the two \(C_{10}\)'s has two endpoints on the
long owner cycles, and endpoints of the same physical colour are paired. For
each physical colour this produces a perfect contact matching on the ten
vertices consisting of five positions on each \(C_{10}\). The number of
contacts between the two five-sets is odd, hence is \(1\), \(3\), or \(5\).
Components without a long-cycle endpoint play no role.

The following five-cycle fact is the only finite combinatorial ingredient.
For every such contact matching, there are bit labels on its two five-sets
which are opposite across each contact and for which each five-cycle has at
most one equal-labelled cyclic edge, except in ten complementary-contact
patterns. In those exceptional patterns one can choose either long cycle to
have three equal-labelled cyclic edges while the other has at most one.

Here is a direct proof by the three possible numbers of cross contacts. With
one cross contact, the two sides have two internal contact pairs. Up to
complementation, the three words
\[
01011,\qquad 01101,\qquad 01010
\]
realize the three possible pair placements; complementing one side enforces
the cross contact. With three cross contacts, each side has one internal pair.
Choose the unique-labelled position among the three cross-contact positions.
The internal pair rules out at most one of these three choices on each side,
so the two allowed sets intersect under the contact bijection. Choose a common
position and opposite unique labels. With five cross contacts, identify the
two five-sets. If they have a common nonedge, choose that pair as the minority
pair on both cycles. If they do not, the two five-edge sets partition
\(E(K_5)\); choosing an adjacent minority pair on one side makes that side
have three equal edges and the corresponding pair nonadjacent on the other
side. This gives the exceptional alternative. The ten exceptional patterns
are exactly the complementary five-cycle pairs.

Use one such labelling for each physical colour. Complementing all labels of
one physical colour gives an independent phase bit. If both long cycles are
good in both colours, the standard two-triple repair adds at most one
omission in expectation over the four phase choices. If a contact pattern is
exceptional, choose the same long cycle as the exceptional one for both
physical colours; the same four-state repair table gives the same bound. The
repair only adds omissions on the two \(C_{10}\)'s, and the table keeps at
most four omissions of either physical colour on each long cycle. Each \(C_4\)
already has two omissions from the virtual opposite pair.

For completeness, the finite statement used here can be checked without any
graph library: enumerate the \(945\) perfect matchings on ten labelled
vertices, classify their \(1/3/5\) cross-contact cases, and enumerate the four
independent phase choices. The Python checker records \(225,600,120\) matchings
in the three cases, ten exceptional patterns, and checks deterministic physical
samples. The accompanying C++ audit exhaustively checks all \(945^2=893025\)
pairs of contact matchings for the four-state repair bound:

    c++ -O3 -std=c++17 develop/check_two_c10_contact_pairs.cpp \
      -o /tmp/two-c10-contact-pairs
    /tmp/two-c10-contact-pairs

It reports all \(893025\) pairs, including the at-most-four-per-colour repair
cap used in the pruning step. The Python checker also checks random physical
\(P\cup Q\) samples by exhaustive minimum-omission enumeration.
The captured result is in `output/two-c10-contact-pairs.txt`.

Before repair, the selected set is independent for \(P\), because labels are
opposite on every \(P\)-plus-virtual path. Therefore every selected \(Q\)-edge
is the only possible selected edge in the initial owner set, and
\[
\mathbb E\,\nu(A[\widehat U])={|Q|\over4}
\leq {4k+20\over8}={k\over2}+{5\over2}.
\tag{2}
\]

The repair adds at most one in expectation. Some phase therefore has matching
number at most \((k+7)/2\). Since the matching number is integral, it is at
most its floor. Finally prune each long-cycle omission set to an
inclusion-minimal triple-hitting set. A \(C_{10}\) then has four or five
omissions. Five omissions would force all five positions of one physical
colour to be omitted, contrary to the construction's at-most-four-per-
colour bound; hence pruning leaves four. Pruning cannot increase
\(\nu(A[U])\), and the \(C_4\) omissions remain at two each. This proves
(1).

The finite controls support the contact classification and the repair table;
they are not used as a substitute for the argument above. The unverified
global \(C_{20}\) candidate still requires a proof that every root support is
reduced to these local classes while preserving one common compensation
forest.
