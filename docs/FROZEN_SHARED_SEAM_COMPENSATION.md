# Actual shared seam resources: exact simultaneous beta replacement

25 October 2026. Haobo Ma and Wenlin Zhang. Independent research branch.

The connected completely frozen family in
[the preceding note](CONNECTED_FROZEN_INTERVAL_REPAIR_OBSTRUCTION.md)
has genuine productive cross-copy interval sharing. Its beta-only owner
graph separates by copy, but its whole-support compensation network does
not. We identify the shared resources and give an exact all-size joint
reservation theorem. This settles simultaneous side-beta replacement using
seam resources in this family; it does not prove universal frozen-grid
compensation or improve 5/6.

## 1. Board and original resource identities

For q>=1, use exactly the preceding board B_q: q+1 copies of the actual
28-by-24, 49T/308P board, translated by (0,24i), with its closed PP splice
at every seam. The preceding arbitrary-rank replay proves complete freezing
for every q. The occupied graph is connected. No geometric modification,
new selection or further matching change is made in this note.

For seam i=0,...,q-1, the original band-12 intervals

    J_i^0=(band 12, first=last=23+24i),
    J_i^1=(band 12, first=last=24+24i)                  (1)

are two DIFFERENT singleton resources in the final large rectangle. Both
are supported by the mixed owners with terminal pairs

    G_i^R=((24,20),(24,21))+(0,24i),
    G_(i+1)^L=((24,2),(24,3))+(0,24(i+1)).             (2)

The two sources reaching these gates are respectively the right alpha
R_i and the left alpha L_(i+1). Each route uses one actual terminal link.
These are productive supports, even when all beta owners remain available.

Here and below support means the established WHOLE original-owner support
model, not a claim that the shared interval touches a free alpha tip. The
interval witnesses lie on the indicated mixed owners. Every resource is
recomputed from the final board before assigning its identity.

To check (1)--(2) geometrically, at band12 the row pair is (24,25). In
copy i the last strand node of G_i^R is column21; in copy i+1 the first
strand node of G_(i+1)^L is column2+24(i+1)=26+24i. The intervening blank
columns 22+24i,...,25+24i form one P-free gap. Its outer columns contain
T, whereas the two middle columns in (1) are BB, each an available original
unit. Both boundary owners support these two units. The PP splice
is in band1 and does not change this band12 calculation.

For completeness, these 2q units are the ONLY cross-copy shared resources
whose two incident owners survive alpha-reachability/productivity pruning.
Other cross-copy supports are in band0, between mixed strands unreachable
from any alpha. This follows by inspecting the fixed base strands: after
the closed PP splice, terminal links never cross a seam, so alpha
reachability is copywise unchanged. Inspect the last P-containing band node
in the left copy and the first in the right copy. A gap crossing the seam
can be shared only by these two boundary strands. Their fixed types are:

| Band | Last P column in a base copy | First P column in a base copy | Left boundary strand / right boundary strand |
| --- | --- | --- | --- |
| 0 | 6 | 3 | unreachable mixed / unreachable mixed |
| 1 | 22 | 1 | PP cycle / PP cycle, including the new splice |
| 2 | 22 | 1 | PP cycle / PP cycle |
| 3,7,10 | 20 | 1 | PP cycle / unreachable mixed |
| 4,5,6,11 | 20 | 3 | PP cycle / PP cycle |
| 8,9 | 20 | 1 | PP cycle / PP cycle |
| 12 | 21 | 2 | productive mixed / productive mixed |
| 13 | none | none | no P strand |

Pure PP cycles have no owner in the terminal compensation model. Band12
has exactly the two available BB units (1); band0 has no alpha-reachable
boundary owner. All rows are fixed base-coordinate facts, unchanged in
each translated copy except the explicitly closed band1 PP splice.
The verifier checks this exhaustive classification against every final
original interval, including resources not used in the theorem.

## 2. Precise reservation policy

Write n=q+1. Each copy has four original alpha sources: top T_i, left L_i,
right R_i and bottom D_i. There are six original beta owners per copy.
Denote by B_i^L, B_i^R and B_i^D the owners with terminal pairs

    B_i^L=((2,3),(5,3))+(0,24i),
    B_i^R=((2,20),(5,20))+(0,24i),
    B_i^D=((20,17),(18,16))+(0,24i).

At each seam, arbitrarily reserve either, neither, or both of
B_i^R and B_(i+1)^L. Let r_i in {0,1,2} count the reserved owners. A
reserved beta is withheld ENTIRELY: neither BP entrance, its body, nor
its private whole-beta payment may be used. This is the correct policy if
that entire owner must remain available for another disjoint certificate.
It is a restriction on available compensation, not deletion of physical
vertices or a claim that new external demands have been embedded.

All other original beta owners and mixed owners remain available. Retain
every original alpha source. The available interval pool is an arbitrary
subset Q of the 2q units (1), and NO other original interval. Put

    z_i=|Q intersect {J_i^0,J_i^1}|,
    delta_i=max(0,r_i-z_i),    Delta=sum_i delta_i.          (3)

No seam beta in this policy belongs to two different seams. No resource
identity in (1) belongs to two different seams, although each has two
different copy owners. Units in one seam are never made private copies.

## 3. Exact joint compensation theorem

**Theorem.** Under precisely the policy above, ordinary compensation and
full compensation allowing beta-body forks have the same maximum payment
and the same minimum link cost at that maximum:

    V_ord=V_full=4n-Delta,
    c_ord=c_full=5n-Delta.                                 (4)

Consequently full compensation under the policy holds if and only if
z_i>=r_i at EVERY seam. Total interval counts alone are insufficient.

**Proof.** We first record every possible terminal route to an available
resource. This is a fixed local strand calculation, repeated by translation;
the PP splice changes no noncycle strand and no terminal link. Ignoring
routes to withheld intervals and reserved betas gives the complete table:

| Alpha source | Beta destinations, with link cost | Available seam intervals |
| --- | --- | --- |
| T_i | either of two private top betas, cost1 each | none |
| L_i | B_i^L, cost1 | the two units of seam i-1 via G_i^L, cost1, when i>0 |
| R_i | B_i^R, cost1; B_i^D, cost2 | the two units of seam i via G_i^R, cost1, when i<q |
| D_i | B_i^D, cost2 | none |

The first links of the seam interval routes are explicitly
(24,19+24i)->(24,20+24i) and
(24,4+24(i+1))->(24,3+24(i+1)).
The two-link bottom route is
(24,17+24i)->(24,18+24i), then
(18,15+24i)->(18,16+24i).
The R_i fallback first enters that same bottom mixed owner from its other
adjacent TP. It cannot create a second unit of B_i^D.

Completeness of the table is checked by following each of the eight alpha
TP endpoints and every subsequent mixed TP in the fixed base board until
it hits beta or revisits an owner. Cycles cannot improve a positive-link
cost route. No terminal link reaches another copy. The only available
cross-copy resources are (1), incident exactly to the gates (2). Thus the
table covers arbitrary q, not just a finite list of boards.

No beta body supports any unit of Q. A beta fork needs an available
interval at that beta body to pay a second incoming alpha. There are
therefore no productive forks under this policy, and the full model has
the ordinary optimum. This is not asserted for other interval pools.

Group D_i,R_i,L_(i+1) into one cluster for each seam i<q. In that cluster,
B_i^D is an always-available unit reached only by D_i or R_i, at cost2.
The side sources have 2-r_i distinct available private beta units and
z_i shared interval units. Let

    t_i=min(2,2-r_i+z_i)=2-delta_i.

At most t_i side payments can avoid B_i^D: every such payment uses one
of these distinct side resources, and there are at most two side sources.
At most one additional payment uses B_i^D. This proves the cluster upper
bound 1+t_i=3-delta_i. Conversely pay D_i using B_i^D, pay each side with
its own available beta when possible, and match up to min(r_i,z_i)
remaining sides to DIFFERENT units of Q at this seam. Both side gates
support both units, so this achieves 3-delta_i simultaneously.

All these side routes are owner disjoint from the chosen bottom route
and from each other. Private beta identities, side gates and intervals
are disjoint between clusters. Thus adding the cluster bounds and
constructions is legitimate; no interval or beta is spent twice.

At a maximum-payment packing in a cluster, B_i^D must be used: without it
there are at most t_i payments, whereas 1+t_i are attainable. Every route
to B_i^D costs two links. Every other payment costs at least one. Hence
minimum cluster cost is at least (1+t_i)+1=4-delta_i. The preceding
construction attains it. This argument also allows dropping D_i and
paying R_i via the fallback; it does not assume preservation of a chosen
bottom assignment when proving the lower bound.

The n top sources, L_0, and R_q,D_q remain outside these clusters. Their
distinct beta routes pay n+3 sources at cost n+4. Combining q cluster
values gives n+3+3q-Delta=4n-Delta; combining their costs gives
n+4+4q-Delta=5n-Delta. This proves (4). QED.

## 4. Sharp failure of independently reusing shared slack

Reserve BOTH side betas at every seam, and open just J_i^0 per seam.
Each side separately has a one-link repair through that SAME original
interval. A copywise account that credits the interval once on each side
predicts that all 4n sources are compensated. In fact (4) gives

    Delta=q,   V=3q+4,   c=4q+5.                            (5)

This is an arbitrary-size completely frozen connected geometric example
of an incorrect independent-credit rule. It is a reservation/pool obstacle,
NOT a counterexample to the unrestricted compensation inequality. If both
units at every seam are opened, Delta=0, all reserved side betas remain
unused, and V=4n,c=5n. If reservations are removed, even the empty interval
pool already has full payment, as proved in the preceding note.

There is also a location obstruction invisible to total resource counts:
for q=2, reserve both betas at seam0, neither at seam1, and place both
available units at seam1. Total z equals total r, but Delta=2. Resources
at a different seam cannot pay the missing side demands.

## 5. Verification and scope

Run from the research checkout:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_frozen_shared_seam_compensation.py
    cd formal
    lean SubQuorum/FrozenSharedSeamCompensation.lean

The verifier independently rebuilds final resources and physical support,
checks the complete route table, and verifies the previously constructed
general rank certificate for q=1,...,12. It exhausts all reservation and
interval-identity states for q=1,2, tests further reproducible larger
states, and compares ordinary flow, full BP-aware fork flow and selected
independent primitive packings. Results are in
[the validation receipt](../output/frozen-shared-seam-validation.json).

Lean checks the local two-source allocation problem, the exact arithmetic
budget for arbitrary lists of seams, and injection facts that prevent
charging a seam unit twice. Physical strand extraction and the all-size
route classification remain written proofs with Python corroboration;
this is not an end-to-end Lean proof of the geometric family.

The next unresolved task is to prove a geometric cut budget for arbitrary
frozen owner networks, or realize a failure with the FULL original interval
and beta pool. The restricted deficits (3)--(5) cannot establish such a
failure. No submitted manuscript, public main branch or shared CI changes
are needed for this result.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
