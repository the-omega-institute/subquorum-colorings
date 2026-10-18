# Research question: the corrected long-core omission inequality

Find a general mathematical proof or a counterexample to
max_D (|D|+m(D)) = 12k+floor(k/2), for every k>=1, in the graph below.
Finite enumeration or solver optima may guide discovery but cannot replace
the general proof. A local inequality with a rigorously proved boundary
potential would be useful; do not assert a state table is proved merely
because it was enumerated.

Let H and X be cycles of length6k, let U={u_i:0<=i<6k}, and let
Y={y_(2b),y_(2b+1):0<=b<k}. Add h_i--u_i--x_i and
u_(6b+j)--y_(2b+(j mod2)) for0<=j<6. Delete every alternating X edge
x_(2j)--x_(2j+1),0<=j<3k. Call the resulting20k-vertex graph Q_k.
The remaining X edges are x_(2j+1)--x_(2j+2), cyclically. A dissociation
set means an induced subgraph of maximum degree at most one. m(D)
counts the deleted pairs with both endpoints omitted. For k=1 this is
the accepted fixed six-port core. Its bound |D|+m<=12 does NOT extend
additively to longer cores.

An exact all-k LOWER construction is already found. Open each six-index
block by removing the interblock H5--H0 and X5--X0 edges. Two local types:
A selects H indices{0,1,4,5}, U{2,3}, X{0,1,4,5}, both Y hubs.
B selects H{1,4}, all six U, X{2,3}, no Y.
Type A has12vertices and1omitted cut pair, local score13.
Type B has10vertices and2omitted cut pairs, local score12.
Inside each open block these sets dissociate. Both H and X boundary
vertices are selected in A; all four are omitted in B. Thus all cyclic
words in A,B with no adjacent A (including last/first) give global
dissociation sets: every added seam has an omitted endpoint. Taking
floor(k/2) copies of A and the other blocks B proves score
12k+floor(k/2). The natural word is(AB)^r for even k=2r, and
(AB)^r B for odd k=2r+1.

The deficient-degree identity for Q_k is
54k-5|D|+2p = i_D+2e_complement,
where p counts selected X ports. It alone is insufficient.
An alternative objective is |D|+m =3k+|D intersect(H union U union Y)|+b,
where b counts the deleted pairs with BOTH endpoints selected.
Finite binary MILP probes k=1..10 report exactly the proposed values;
this is evidence only and establishes no all-k upper bound.

Why the corrected bound matters: attach one broken Heawood block at
each of the3kdeleted pairs, using its original saturated ports. The
full graph has order62k and a literal minimal forming selection of
size36k (with6kselected isolates). For any full dissociation set, if
b of the broken blocks have size8, their distinct core pairs are
omitted. Hence an upper bound F(k) for |D|+m in Q_k implies
beta(full)<=21k+F(k). The A/B construction and7- or8-vertex Heawood
witnesses give beta(full)>=33k+floor(k/2). Thus proving the corrected
core bound would give exact beta of this new family. It does NOT yet
give exact SF=36k: the selected set is only a lower witness, and cubic
compensation may allow a slightly larger SF at large k. Keep that
distinction explicit.

The prior one-cut saturation, isolate compensation and cubic inequality
are established inputs. Please focus on the single sharp all-k upper
bound above. If it is false, give a fully specified dissociation set and
omitted pairs with score exceeding12k+floor(k/2).
