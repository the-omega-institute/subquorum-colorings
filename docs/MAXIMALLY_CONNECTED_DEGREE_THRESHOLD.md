# Sharpness with vertex connectivity equal to the minimum degree

**Theorem.** For all integers p>=3 and k>=1 there is a finite simple
bipartite graph G with a specified inclusion-minimal two-star-forming set
S inducing P_3's and isolates, for which

    n=14pk, |S|=8pk, beta_2(G)=7pk,
    delta(G)=kappa(G)=p+1, Delta(G)=4p-3.

Thus for every delta>=4 the sharp selected-star degree coefficient at
Delta=4delta-7 is attained at every cyclic scale even with vertex
connectivity equal to its largest possible value, delta. The exact gap
is n/14. This strengthens the two-connected construction; beta_2 remains
the unrestricted dissociation number, and no exact SF_2 value is asserted.

## Simultaneously safe witness ports

Start with the full dense base F of DENSE_WITNESS_DEGREE_THRESHOLD.md,
with p blocks in each wing and all cross-witness edges. Delete ALL p
diagonal edges b_j^L b_j^R to obtain C_p. Every a still has all opposite
witness neighbours; each b has all except its own-index opposite b.
Selected vertices still have degree p+1, connectors 4p-3, a-witnesses
2p+1, and b-witnesses now 2p+1. In particular the minimum remains p+1.

The arbitrary-dissociation-set proof in that note applies to C_p as well.
This does not follow by monotonicity under deletion; it follows by tracing
the actual edge relations used in the proof. Its fixed witness kernel has:

- complete K_(2,2) between L_j and R_(j+1);
- all edges from a_j^L to R_j;
- all edges from a_(j+2)^R to L_j.

Every such edge survives deletion of ALL diagonal b--b edges. The
no-connector and single-connector arguments use only this kernel and
local block/connector edges. Pair/triple connector counts use the same
slot witness cap and the unchanged connector incidences. The p=3,
two-same-colour equality contradiction uses that every right a is
universal to left witnesses (and conversely), which also survives.
Consequently the whole cap proof, with cross-saturation computed in the
actual graph C_p, still gives beta_2(C_p)<=7p. The same attaining set
(left c,x,i; right x,y,a,b) has size 7p. Hence

    beta_2(C_p)=7p.                                  (1)

These are simultaneous safe deletions, not separate one-edge assumptions.

## Every deleted piece has connectivity p+1

Let Z be any set of at most p vertices. We prove C_p-Z connected.
The surviving witness core has at least p>=3 vertices in each part.
Each witness misses at most one opposite witness. Any two witnesses
in the same part have a common surviving opposite neighbour, since at
most two of at least three are excluded. Every witness also has a
surviving opposite neighbour. Thus the whole surviving witness core
is connected. Call a surviving vertex attached if it has a path to it.

For p>=4, every connector has at least 2p-3>=p+1 own-wing leaf neighbours.
Each such leaf has a distinct witness owner (x-a or y-b), and all these
leaf-owner pairs are vertex-disjoint. At most p deletions cannot hit
all pairs. One surviving pair attaches the connector to the witness core.
Thus every surviving connector is attached.

For p=3, the omission indices are constants 0 for x, 1 for y, 2 for c.
Index-2 connectors have all six own leaves as neighbours and are attached
by the same argument. An index-0 or index-1 connector has three own leaf
neighbours and all three opposite centres. If one of its three disjoint
leaf-owner pairs survives it is attached. Otherwise Z must have exactly
three vertices, all in those pairs in the connector's own wing. The
opposite wing is entirely untouched; each opposite centre has a path
through an own leaf and witness to the core. The connector therefore
attaches through any of its opposite centres. This also proves attachment
for every connector at p=3.

A surviving i has p own connectors and its witness b as neighbours. Since
there are p+1 distinct neighbours, at least one survives, attaching i.
For a surviving x or y, its witness owner and p-1 own connectors give
p direct routes to attached vertices. If one survives it is attached.
If all p are deleted, Z is exactly that owner plus those p-1 connectors.
The leaf's own centre and every opposite connector are untouched, so the
leaf attaches through its centre to an opposite connector. This avoids
any circular assumption that all centres were already attached.

Finally every surviving centre has its two leaves and p-1 opposite
connectors as p+1 neighbours, all attached when present. At least one
survives. Hence every vertex of C_p-Z is attached and the graph is
connected. Thus kappa(C_p)>=p+1. Its minimum degree is p+1, so

    kappa(C_p)=delta(C_p)=p+1.                        (2)

## Parallel links retain maximum possible connectivity

Take k disjoint copies of C_p. For every j=0,...,p-1, add

    b_j^L(h) b_j^R(h+1), h modulo k.

At k=1 this restores all deleted edges and gives F. At k>=2, each
consecutive pair of pieces has a bundle of p independent linking edges.
Every port belongs to just one linking edge. Distinct left and right
ports ensure that at k=2 the two bundles consist of 2p distinct edges.

After deleting at most p vertices, (2) keeps every surviving piece
connected. At most p links are lost, since a deleted vertex is on at
most one linking edge. For k>=3, disconnecting the cycle of connected
pieces would require losing every edge of at least two bundles, at
least 2p links. For k=2 it would require losing all 2p links. Both are
impossible. At k=1 the graph is a supergraph of C_p and is connected
after such deletions by (2). Thus kappa(G)>=p+1 at every k. Minimum
degree p+1 supplies equality.

All b-degrees are restored to 2p+2, so max degree is 4p-3 and min degree
p+1. The selected subgraph, formation and literal single-deletion failures
are unchanged; every new edge has two outside endpoints. Every dissociation
set restricts in each piece to at most 7p by (1), and repeating the
attaining set avoids every left port, so it attains 7pk. This proves all
the theorem's parameters and the exact coefficient equality.

## Verification

Run `python3 -B scripts/check_maximally_connected_threshold.py`.
The checker tests physical multiple-port pieces and completed graphs,
including degrees, formation, each literal minimality failure and the
attaining set. Exact recursion additionally controls p=3,4 simultaneous
multi-edge deletions. Vertex-split integer flows certify connectivity
p+1 on six finite models: for p+1 distinct roots, every nonadjacent
root-target pair has at least p+1 internally vertex-disjoint paths.
A cut of fewer than p+1 vertices leaves a surviving root; a separated
vertex would contradict one such flow. Minimum degree gives the matching
upper bound. This is a finite implementation control, while (1),(2) and
the bundle argument prove the result for all p,k.

The independent final exact-source audit returned **ACCEPT**. It reconstructed
all 10 manifest files and ran the original checker unchanged, with
assertions enabled, terminal exit status 0. The reviewer captured 1,064 bytes of nonempty startup-through-exit stderr from an unrelated spreadsheet-runtime warmup exception; checker assertions passed and the process exited 0. The full warning and this qualification are retained in the review record. The complete 10,978-byte report was reproduced byte-for-byte
(SHA-256 81e98abc5c4ea6c3280321221113a0807e9d6d1386deb4a06feb8affe5c77fa3). The exact source manifest, full response and
execution scope are in `../output/maximally-connected-threshold-review.json`. Only this evidence paragraph
was added after the reviewed source freeze; the proof and checker are unchanged.
