# An active short-tail merger and a sealed retained escape

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

The short-chain reduction leaves a real geometric obstruction: two different
alpha-entered short mixed tails can meet the SAME BP of a longer mixed strand
on a completely frozen original board. The example below survives alpha
reachability pruning and short-chain contraction. The receiving mixed owner
supports two different original intervals, but the two sources together can
pay only one in the indicated restricted pool. Every source separately can
pay one. Thus neither independent reachability nor internal chain compression
eliminates the shared entrance capacity.

We also prove a necessary geometric escape lemma for every such short-tail
fork. The escape P sites are injective, but the example puts a retained escape
in a sealed pure two-point PP/M cycle. Consequently this witness does not
automatically provide an additional open owner or adjacent interval. This
extends the earlier alpha/beta escape analysis to the horizontal-short-tail
case. The general warning against counting escape sites as resources was
already established; we claim the new local geometry and active realization,
not that warning as a new principle.

The example refutes these stronger local rules, not universal compensation.
Its complete original pool pays both alphas at zero links. No improvement
of the unrestricted 5/6 bound follows.

## 1. Original frozen board and the short-tail fork

Use the original feasible (T,M), endpoint set P and horizontal two-row bands
of [the short-chain note](SHORT_MIXED_CHAINS_AND_CORRIDOR_HOLE_BUDGET.md).
All original endpoints have finite strict freezing ranks rho. A nonmate
neighbor w is retained at v if w is T, or w is P and
rho(mate(w)) < rho(v). Complete freezing requires two distinct retained
neighbors at every P. Work on the original board throughout; no deletion
is used to justify a freezing assertion.

Normalize the source row r to be odd (the lower row of its band), let c be
an internal column, and require

    n_-=(r,c-2), t_-=(r,c-1), b=(r,c), t_+=(r,c+1), n_+=(r,c+2)

all P, with n_- and n_+ BP, t_- and t_+ TP, and actual matches
n_- -- t_- and t_+ -- n_+. The central b is BP. These are two distinct
one-edge short mixed owners ending at t_-/t_+, not virtual tips. The permitted
links t_- -> b and t_+ -> b share the actual same BP. Reflections handle the
other physical directions.

## 2. A general retained-escape lemma

**Lemma 1.** Put b*=(r+1,c). The actual mate of b is b*. For each sign s,
put d_s=(r+1,c+2s) and z_s=(r+1,c+s). Then:

1. rho(n_s) < rho(b). Both (r,c+3s) and d_s are retained at n_s.
2. At least one z_s is retained at b*. Every such z_s is P, its adjacent
   d_s is P, and

       rho(mate(z_s)) < rho(b*),
       rho(mate(d_s)) < rho(n_s) < rho(b).

3. The actual mate of that z_s is either d_s or (r+2,c+s).
4. Choosing ANY retained z_s at each fork gives different P vertices for
   different central BP forks in this fixed band frame.

**Proof.** The in-band partner of b is blank, and both horizontal neighbors
t_- and t_+ are already matched to their outer BPs. Thus b must match its
out-of-band neighbor b*. At b its only nonmate occupied candidates are the
two tails, so both are retained, giving rho(n_s)<rho(b).

At n_s the mate is t_s and the in-band partner is blank. Only the outward
horizontal neighbor (r,c+3s) and d_s remain as possible retained neighbors.
Both are therefore present and retained. In particular d_s is occupied.
At b*, at most one nonmate neighbor is vertical, so at least one of its two
horizontal neighbors z_s must be retained. It cannot be T: it would see
both b* and the already occupied d_s, violating feasibility. Thus z_s is P.
The occupied d_s cannot now be T either, since it sees n_s and z_s. This gives
the displayed strict ranks. Of z_s's four potential mates, t_s is already
matched to n_s and b* to b. Only d_s and the further vertical neighbor remain.
This proves (1)--(3), including the necessary existence of coordinates that
would otherwise be outside the finite rectangle.

For (4), in the fixed frame the map taking a source row to its out-of-band
row is an involution: r+1 for odd r, r-1 for even r. Equal escape points
therefore imply equal source rows. If the chosen sides are equal, equal
escape columns imply equal centers and the same fork. If sides are opposite,
the central columns differ by two. The shared intermediate TP of one fork
would then be actually matched horizontally to the central BP of the other
fork. But that BP has its forced vertical actual mate. Matching uniqueness
excludes this case. Hence the selected escape points are distinct. □

This lemma uses horizontal actual mating of BOTH tails. The earlier
vertical-TP row injection theorem does not apply to them. The lemma is an
injection into original P sites with strict predecessors. It is not an
injection into distinct strands, available intervals or unused payment units.

## 3. Explicit alpha-entered realization

The permanent [fixture](../develop/fixtures/frozen_active_short_tail_merger.json)
gives all 25 selected points, 31 matching edges/62 endpoints, strict rank
witnesses and the full three relevant strand traces on a 14x18 board.
Coordinates in this note are ZERO-BASED. Bands are (0,1),(2,3),... .

The two alphas have distinct endpoint pairs

    A_L: (5,6), (3,1),      A_R: (5,12), (3,15).

Both bend through other occupied bands. The two original short mixed
strands are the actual matching edges

    L: (5,7)--(5,8),        R: (5,10)--(5,11),

where (5,7)/(5,11) are BP and (5,8)/(5,10) are TP. The central longer
mixed strand is

    G: (5,9),(6,9),(7,9),(8,9),(9,9),(10,9),

with BP (5,9) and TP (10,9). The four actual permitted links are

    A_L TP (5,6) -> L BP (5,7),
    L TP (5,8)   -> G BP (5,9),
    A_R TP (5,12)-> R BP (5,11),
    R TP (5,10)  -> G BP (5,9).

Thus both short heads are reached from different original alpha sources.
All five owners are alpha reachable.

Keep exactly these five original owners and the two available original
intervals

    J_0=(band5, first10, last10),
    J_1=(band5, first12, last12).

This restricts only the allocation model, not T or M. Keep ALL original
links among these owners and intersect each original whole support W with
{J_0,J_1}; do not invent or remove individual support incidences. The two
alphas and L,R have empty support in this pool, while W(G)={J_0,J_1}.
The two intervals are distinct BB singleton components, separated by a BT
column at column11; both are unmarked. The checker reconstructs all these
facts from the original board.

**Proposition 2 (exact active obstruction).** This restricted system has
V_full=V_ord=1 and minimum actual links c=2. Each source alone has value1
and cost2. The bipartite projection which connects each source to each
reachable original interval has matching number2.

**Proof.** Either source has its displayed two-link route through its short
mixed owner and G to either interval, giving payment1 at cost2. Every route
in the restricted system to either interval must pass through G: only G
supports them, and there is no beta sink. Both entrances into G use the
same physical BP (5,9), so at most one can be selected. This proves payment
at most1 without enumerating terminal matchings. To reach G from either
alpha requires first entering L or R and then using its outgoing link;
there is no direct alpha-to-G edge. Thus every paying route has at least
two actual links. The witness proves exact cost2. Separately each source
reaches BOTH J_0,J_1, so their reachability projection has a matching of2.
The projection forgets the shared capacity-one entrance and cannot be used
as a joint packing. □

Pruning non-alpha-reachable mixed owners removes none of these five owners.
Both maximal short chains have length1, so exact weighted chain contraction
retains their two capacity-one conduits and G's shared entrance. Thus the
obstruction is a genuine residual interface of the previous reduction.
This does not refute compensation from the COMPLETE original resource pool.

## 4. The retained escape can be a sealed pure cycle

At the normalized fork, b=(5,9), b*=(6,9), and the left escape z=(6,8) is
retained at b*. Its actual mate is z'=(7,8), and this is also its PP band
partner. They form a pure two-point PP/M cycle with no open terminal.
The saved strict ranks include

    rho(z')=4 < rho(b*)=5,
    rho(n_-)=10 < rho(b)=11,
    rho(n_+)=7 < rho(b)=11.

The two flanking columns of this cycle are both PP:

    (6,7),(7,7) are P,       (6,9),(7,9) are P.

Consequently the cycle has no adjacent endpoint-free gap on either side
and supplies no open beta/mixed owner. It is a retained escape satisfying
Lemma 1, not merely an unrelated occupied point. The strict rank witnesses
show all endpoints still freeze. Therefore converting each forced escape
into a new open owner or adjacent interval is invalid even for an active
short-tail merger. Site injectivity alone cannot remove the capacity cut.
No assertion about a farther global compensation route is excluded.

## 5. Complete pools and the all-q family

On the complete board, A_L has the direct unmarked singleton interval at
(band2,column5) beside (5,6), and A_R has the different singleton at
(band2,column13) beside (5,12). Pay each by its own interval with no links.
There are exactly two original alphas, so full and ordinary values are2
and minimum link cost is0. These are old original resource identities,
not credits assigned to the escape cycle.

For any q>=1 take copies translated by 14i rows, 0<=i<q, and optionally add
any even number of blank columns at the right. Occupied rows in each copy
lie between1 and11, leaving separating blank rows; no occupied adjacency,
terminal link or whole-support incidence connects different copies. Replay
the same strict witnesses in every copy. The relevant interval identities
are distinct across bands and the marked boundary status is unchanged.

In the restricted pool of q copies, each copy has its own capacity-one G
entrance. Proposition 2 gives an upper bound q and q disjoint two-link
witnesses achieve it. Every payment costs at least2 links, so exactly

    V_restricted=q,  k-V_restricted=q,  c_restricted=2q.

Each of the 2q sources individually pays1; the reachability projection pays
2q, overcounting by q. All owners remain source reachable, and all q chosen
retained escape sites lie in their respective sealed two-point cycles.
Complete pools have V_full=V_ord=2q,c=0 through the distinct original bypass
intervals. This is a general separation proof for all q and all even blank
right paddings; finite q<=8 tests only verify coordinates and bookkeeping.

## 6. Verification and limits

The solver-free command is

    python3 develop/check_active_short_tail_merger.py --output output/active-short-tail-merger-validation.json

The [receipt](../output/active-short-tail-merger-validation.json) records nine
base/carried-isometry physical checks with exact restricted/full values,
24 separated-copy/padding models, 24 independent primitive-pack comparisons,
and 228 geometric scans with109 short-tail forks and109 distinct retained
escape sites. The fork scans check the forced actual mates, two sets of
strict rank inequalities and the allowed escape-mate directions. The
geometric proof of Lemma1 and the capacity proof of Proposition2 do not
rely on their sample size.

[ActiveShortTailMerger.lean](../formal/SubQuorum/ActiveShortTailMerger.lean)
checks original feasibility, matching geometry and ALL62 endpoints' inductive
freezing, the two distinct alternating alpha traces, the actual long mixed
trace, short-tail/entrance links, two different gap units and the sealed
retained cycle. It also proves a generic same-target exclusion and a
conditional separated-capacity ledger. Nine declarations are axiom-audited;
see the [formal receipt](../output/active-short-tail-merger-formal-check.json).
The grid-to-strand/support adapter, general escape-site injection and the
full flow interpretation are written proofs, not claimed end-to-end Lean.

The optional Z3 discovery script is separate from the verifier. Its SAT
model provided a candidate only; all claimed properties are checked anew
without importing Z3, and the actual freezing is derived in Lean. No UNSAT
or timeout observation is used as a general nonexistence argument.

An oracle-broker request was attempted through the streaming NyxID service.
The selected public Pro pool reported26 online workers at dispatch, but task
03b95177-eec4-40c3-af54-bbe4f2d5f91b failed with
model_unavailable@selecting_model. It returned NO mathematical review. The
[failure receipt](../output/active-short-tail-merger-oracle-status.json)
records this; no external acceptance is claimed.

The next general obligation is to combine original bypass intervals and
retained escape structure in a JOINT residual cut argument. The current
example proves that reachable pruning, chain contraction and counting
escape sites cannot by themselves eliminate shared entrances. It leaves
open whether the full original frozen geometry always has enough different
bypasses, and whether that can yield a better bound than5/6. The 11 October
submitted manuscript, public main, PR3 and shared CI remain outside this
research change. No Mail operation is part of this round.

## Continuation: retaining the old matching forces persistent payments

The [completion note](ACTIVE_MERGER_COMPLETION_AND_PERSISTENT_PAYMENTS.md)
classifies the actual bypass gap under arbitrary admissible fixed-packet
monotone completely frozen extensions. Sealing its last interval forces a
cycle and an exclusive beta; the other alpha keeps a private corridor unit.
Both old sources therefore eliminate exactly even with exterior coupling.
The restricted obstruction here and the open arbitrary-matching problem
remain as stated.
