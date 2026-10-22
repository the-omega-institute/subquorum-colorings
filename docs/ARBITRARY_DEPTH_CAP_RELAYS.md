# Frozen relays of arbitrary depth and their exact access distance

22 October 2026. Written all-parameter proof with finite checks and a scoped
Lean walk formalization. This extends the selected-cap mechanism in
[terminal cancellation](TERMINAL_CANCELLATION_AND_STRANDED_DEMAND.md).
The written construction received an independent ACCEPT review on23 October;
the archived review distinguishes proof checking from reported code execution.

## Statement

For every even W>=8, even H>=4 and positive integers p,q, there is a feasible,
completely frozen actual matching with a unique perfect matching on its endpoint
graph, and a physically receiver-closed aligned packet of dimensions

    (W+2) by (H+6+2d),       d=max(p,q), s=p+q.

It has exactly one original TP--TP demand, no BP--BP credit, and H+1+s mixed
paths. Initially its demand has neither direct BB access nor selected-cap
TP--BT--BB access. Among ALL matchings of unit horizontal adjacencies between
opposite-kind original terminals, the minimum number of links exposing direct-or-cap access at both free
ends of its remaining TP--TP path is exactly

    min(p,2)+min(q,H/2).                                      (1)

Access coverage alone does not exclude a twice-marked connector. A particular
all-left choice, using s links, always reaches two distinct unmarked intervals
and pays the demand with exactly ONE interval reserve. Mixed relays supply no
beta credit. The exact compact-packet inventory is

    |T|=H+9+2s, |M|=W+H+s+2,
    S=WH/2+2W-H-5+d(W+2)-3s, B=W+2,
    S-B=(W/2-1)H+W-7+d(W+2)-3s >=17.                         (2)

In particular, W=8,H=2L,p=q=L, for L>=3, gives height TEN and width 4L+6,
with |T|=6L+9, |M|=4L+10, S=10L+11 and B=10. Access requires at least L+2
horizontal links, and this minimum is attained. No fixed number of horizontal
cancellation links suffices uniformly, even at this fixed height. The target
inequality is satisfied with positive margin 10L+1; the obstruction concerns
bounded cancellation before access, not that inequality or other global rules.

## Coordinates and feasibility

Use raw integer coordinates and set R=W+4. Begin with direct_family(W,H) in
the preceding note and permanent checker. For each triple

    (r,e,t)=(5,-1,p) or (R,+1,q),

remove the old selected cap (r,2). Add the following selections and matching
edges, retaining every other old selection and edge:

    T: (r+e,3-2j),                         1<=j<=t;
       (r,2-2t);
       (r-e,4-2j),                        2<=j<=t;
       (r-2e,1).
    M: (r,3-2j)--(r,4-2j),                1<=j<=t;
       (r-e,2)--(r-2e,2).

Translate columns by 2d, leaving rows unchanged. An enclosing board has
dimensions (W+12) by (2H+12+2d). The compact packet, before translation, is
rows 4 through W+5 and columns -2d through H+5. Its boundaries align with the
original 2-by-2 tiles. It contains all selected sites, endpoints and every
complete physical tile meeting an endpoint, so it contains every receiver.

All newly added endpoints are distinct, and the only removed occupied sites
are immediately replaced by endpoints of new horizontal gates. New selections
are separated in each guard row by two columns. Each guard has only its gate
endpoint as an occupied neighbour; the final cap has only its final TP endpoint;
the side selection at (r-2e,1) has only (r-2e,2). The retained old selections
gain no occupied neighbour. The upper and lower modifications do not interact
when W>=8. Thus every selected vertex has occupied degree at most one, and
the matching and selection are feasible for all parameters.

There are 2t+1 added selections and one removed selection per side, a net 2t,
and t+1 added matching edges. This proves the first two counts in (2).

## A complete strictly ordered freezing certificate

Write TP_j=(r,3-2j), BP_j=(r,4-2j). Freeze TP_t first, using its guard
(r+e,3-2t) and the final cap. Then freeze TP_(t-1),...,TP_1: its two
retained neighbours are its original guard and BP_(j+1), whose mate has
already frozen. This makes BP_1=(r,2) retained. Do this on both sides.

Now replay the complete old-family freezing certificate. The only old
selections removed were the two caps; their replacement endpoints BP_1 are
already retained, so every old witness remains valid. Next, on each side,
freeze, in order,

    (r-e,2)   using (r,2),(r-e,3);
    (r-2e,2)  using (r-2e,1),(r-2e,3);
    BP_1      using (r,3),(r-e,2).

The old endpoints in these witness pairs have frozen, and the new vertical
pair is retained in the required order. Finally freeze BP_2,...,BP_t. BP_j
uses its selected guard (r-e,4-2j) and TP_(j-1). The mate BP_(j-1) of that
second witness has already frozen. Every new endpoint is now frozen, with
strictly earlier witnesses throughout. This is a general certificate, not an
inference from the finite parameter controls.

Uniqueness follows by a separate leaf-removal argument. On each side, TP_t
is an endpoint-graph leaf. Force its gate and continue inward through gate1.
Replay the old direct-family forced matching order. After the old edge
(5,3)--(6,3), force the new edge (6,2)--(7,2), whose first endpoint is now
a leaf. After the old edge (R-3,3)--(R-2,3), force the lower new edge
(R-2,2)--(R-1,2), whose first endpoint is now a leaf. These insertions leave
the rest of the old leaf order valid and exhaust the endpoint graph.

## Exact terminal geometry and the lower bound

The new gates are mixed paths with TP_j and BP_j as their actual terminals.
The new vertical edge on each side is an internal PP loop in its aligned band.
The original sole alpha path still joins (5,3) to (R,3); all remaining original
paths are unchanged. Hence alpha=1,beta=0,gamma=H+1+s. Terminal conservation
then implies alpha'=1,beta'=0 under every admissible horizontal link matching.

The terminal sets in rows5 and R are closed under all such links and all strand
edges except the original alpha, which is their sole connection. In each row
there is a line of adjacent mixed gates on either side of its original alpha
tip. Upper depths are p on the left and2 on the right; lower depths are q on
the left and H/2 on the right. Interior TP tips have a BP column on both sides,
so have neither direct nor selected-cap access. Only the two far tips in each
row have cap access. There are no direct BB ports in either terminal row.

The alternating component containing the original alpha cannot be a cycle:
its free charge is negative and it contains no beta owner. Removing the alpha
edge splits that component into two simple paths, one in each row. Starting
at the original tip, a nontrivial row path must first take a horizontal link,
then an entire mixed gate, and continue. Linking a gate to its own paired tip
only closes a detached cycle; it cannot advance the alpha component. A simple
path in a linear gate chain cannot reverse without reusing a terminal. Each
crossed gate therefore costs one link, and access requires reaching one of
the two far tips. This proves the two lower bounds min(p,2) and min(q,H/2).
Their resources are disjoint rows, so their costs add.

Choose the nearer end independently in each row and take all successive
cross-gate links along that monotone route. These links form a matching: each
gate uses its two distinct terminals, and the two rows are disjoint. They
attain (1). Arbitrary links elsewhere can only add to the total, so (1) is
the minimum among all horizontal link matchings, including nonmaximal ones.

The scoped Lean file formalizes arbitrary unit gate walks, their displacement
bound, exact nearest-exit attainment and the two-row lower bound, including
L+2 at fixed height. The grid-to-gate-chain adapter above remains a written
geometric proof; Lean does not check the whole grid construction.

## Payment and absence of repeated resources

For a uniformly safe choice, take on each side the t links

    (r,5-2j)--(r,4-2j), 1<=j<=t.

The two new free tips are (5,3-2p),(R,3-2q). Each accesses its selected cap
at column2-2t and then BB at column1-2t. After translation the BB column is
1+2(d-t)>=1. These targets are blank singleton intervals, because the adjacent
columns contain no TT column. They lie in distinct bands and meet neither
boundary mark (at columns0 and H+5+2d). No other alpha connector exists.

The single connector thus merges TWO previously unmarked interval components
into ONE, using exactly one unit of h0. It has no marked endpoint and produces
no twice-marked path. Explicitly,

    initially: beta'=0, u_cap=1, h2_cap=0, h0_cap=S-B+1;
    finally:   beta'=0, u_cap=0, h2_cap=0, h0_cap=S-B.

Each original mixed owner contributes zero credit, independent of relay depth.
No beta owner, cap mediator or interval reserve is paid twice. The shortest
access route need not have this unmarked property: at H=4, both right exits
lead to boundary-marked intervals, so taking both can leave h2_cap=1. This
does not contradict (1), which concerns access, not automatic compensation.

The area and inventories give (2) directly. Its positivity also has the exact
decomposition, with w=W/2,

    S-B=17+(w-4)(H+2+2d)+3(H-4)+4(d-1)+3(2d-s).

All terms after17 are nonnegative. Substituting W=8,H=2L,p=q=L gives the
fixed-height formulas in the statement, and (1) becomes L+2 for L>=3.

## Reproduction and scope

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_arbitrary_depth_cap_relays.py --output output/arbitrary-depth-cap-relays-validation.json

The permanent checker verifies90 parameter tuples, including asymmetric
depths and L through64. It checks feasibility, complete serial freezing,
independent unique matching, receiver closure, inventories, original and
virtual ledgers, shortest access distance and an attaining horizontal matching.
Three small tuples additionally exhaust118928 horizontal link matchings.
These computations check the formulas and adapters; the arguments above
establish the unrestricted parameter statements.

This is a precise obstruction to uniformly bounded horizontal access rules
and a nonempty all-parameter compensation lemma. It does not prove that every
frozen residual demand reaches a suitable interval, nor that multiple demands
can allocate those intervals without collision. The general target
h2_cap+u_cap<=h0_cap+beta' and the outside overlap correction2N_out remain open.
No universal improvement of5/6 or triple grid equality is claimed.

Independent mathematical review3be86c00-4cd7-4f9c-8a8d-91a2432ebee9 gives
ACCEPT for the full written construction and exact access minimum. Its sole
wording recommendation, explicitly stating unit horizontal original-terminal
adjacencies, is incorporated above. The review does not certify Python or Lean
execution. See output/arbitrary-depth-cap-relays-oracle.json.
