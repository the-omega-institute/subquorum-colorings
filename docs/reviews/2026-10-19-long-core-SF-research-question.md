# Research question: exact upper star formation of the long-core family

Determine SF_2(L_k) for all k>=1. In particular prove SF_2(L_k)=36k,
or give a fully specified k and inclusion-minimal forming set larger than36k.
We need a general argument; finite optimization is discovery only.

Use the same Q_k and L_k as in your preceding sharp-omission proof:
H,X are length6kcycles, edges h_i-u_i-x_i, two hubs per six-index
block with u_(6t+j)-y_(2t+(j mod2)), and every x_(2j)-x_(2j+1)
deleted. At each deleted pair attach a fresh Heawood graph with edge
(0,8) removed, joining point0to oddX and line8to evenX. The Heawood
labeling has points0..6 and lines7..13; line7+j meets points j,j-1,j-3
mod7. Thus n(L_k)=62k, and the graph is connected cubic bipartite.

Your preceding argument, independently checked and written, gives exactly
beta_2(L_k)=33k+floor(k/2). A minimal forming witness of size36k
selects all core H,U and, in each Heawood block, {1,2,3,5,7,9,10,11}.
All port rewiring is outside that selection. Its selected isolates total6k.
The established cubic inequality gives
36k <= SF_2(L_k) <= 36k+floor(2floor(k/2)/7).
Thus exact36k is already proved for k<=7, but not for larger k.

Forming means: every outside vertex x has two selected neighbors, or
a selected neighbor with another selected neighbor. Stars are non-induced.
Minimality is inclusion-minimality, not minimum size.

One established input may help: in ANY surrounding graph attached to a
broken Heawood block only through its two ports, every minimal forming
set selects at most eight vertices of that block. This follows from a
general robust-deletion proof using Fano geometry. Therefore each of the
3kattached blocks contributes at most8. However an independent12kcap
on the core is not yet proved and should not be assumed.

A tempting route is false even for k1: a core selection of size13 need
not have a robust non-X deletion. With labels H0..5,U6..11,X12..17,Y18,19,
the selection {0,1,3,4,5,6,8,10,11,12,13,15,18} has no such robust
deletion. Robust means active selected v, every selected neighbor has
selected degree>=2, and every omitted neighbor x has selected degree>=3
or degree2with its selected neighbor other than v active. This counter
only refutes that deletion rule, not a global SF bound. A coupled core/
Heawood compensation proof may still work.

Please focus on the exactSF question, using private failure witnesses,
robust deletion, weighted accounting, or another general structural
argument. If36kfails, verify full global formation and every single-vertex
deletion, not just local nonredundancy. Distinguish exactSF from a larger
minimal witness, and do not infer a new asymptotic gap coefficient from
a single finite example.
