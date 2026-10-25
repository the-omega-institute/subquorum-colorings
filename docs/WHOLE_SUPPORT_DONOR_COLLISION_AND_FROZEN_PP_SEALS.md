# Whole-support donor collision with frozen PP seals

Subsequent [whole-support normal form](WHOLE_SUPPORT_FORK_NORMAL_FORM.md):
because this family has no beta owners, its full-support maximum compensation
and minimum additional link cost are exactly an ordinary owner-support flow.
The larger theorem separately accounts for beta-body interval witnesses using
explicit two-arm forks; none are present in this family.

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

The subsequent [full-pool singleton obstruction](FULL_POOL_SINGLETON_OBSTRUCTION.md)
adds isolated selections to seal the alternative resources. That new family
has maximum compensation one for two alphas over all terminal matchings,
even with the complete raw resource pool. The present family remains
repairable as proved below; the two results concern different configurations.

Two deficient components can each have a legal, separately successful mixed
continuation, using distinct gates and terminals, while those continuations
together expose only one original interval. We realize this in the **whole
path-support** interface, including internal PP witnesses. The construction
works at every even height parameter W>=8, survives arbitrary blank right
padding, and gives arbitrarily many simultaneous collisions by separated
stacking. A different lower exit repairs every copy with distinct original
units. Thus the individual-reachability rule fails; the target grid inequality
and the existence of some full mixed compensation are not refuted.

This fills the physical gap explicitly recorded in
[exact component reserves](MIXED_SUPPORT_COMPONENT_MERGE_ACCOUNTING.md).
The older [terminal collision](SHARED_DONOR_COLLISION_AFTER_MIXED_RELAYS.md)
had internal PP support that already paid both demands. The new pure PP seals
remove exactly that bypass. No maximum-selection or unique-matching hypothesis
is imposed or asserted for the new family.

## 1. Actual all-height construction

Coordinates below are (row,column). Fix even W>=8. Start with two copies of
relay_family(W,4,1,1), the second translated ten columns right, as in the old
collision family. For an explicit definition, the left copy has selections

    (4,c), c in {3,5,7,9}; (5,c), c in {2,10}; (6,8);
    (7,c), c in {3,7}; (W+2,c), c in {3,8};
    (W+4,c), c in {2,10}; (W+5,c), c in {3,5,7,9}.

Its original matching edges are

    (5+2i,5)--(6+2i,5),             0<=i<W/2;
    (6+2i,6)--(7+2i,6),             0<=i<W/2-1;
    (r,6)--(r,7), (r,8)--(r,9),     r in {5,W+4};
    (W+3,7)--(W+3,8);
    (r,3)--(r,4),                  r in {5,W+4};
    (6,4)--(7,4); (W+2,4)--(W+3,4).

Translate this entire list by ten columns for the right copy. Now add

    (r,c)--(r+1,c),   r=8,10,...,W,   c in {4,14}.          (1)

Keep the selections unchanged. Use the aligned physical packet rows4..W+5,
columns0..21, with two-row bands starting at4,6,...,W+4. This packet contains
all selections, matching endpoints, and every original 2-by-2 tile meeting an
endpoint; therefore all physical receivers are included. The constructor's
enclosing board may contain extra blank exterior cells; packet and whole-board
counts are kept distinct.

There are W-6 added edges in(1). They coincide with within-band vertical PP
connectors and each forms its own pure two-edge cycle in the matching/connector
multigraph. They supply **no beta credit**. The original two alpha strands
remain the columns5 and15 through all packet bands.

## 2. Feasibility and arbitrary-length freezing proof

The old two-copy construction is feasible and completely frozen by its explicit
relay certificate. A new endpoint has row8..W+1 and column4 or14. Inspection of
the displayed selections shows that none is adjacent to a selection. Thus no
selection gains an occupied neighbour. New endpoints are distinct and avoid
all old endpoints. The two columns of additions are disjoint and do not affect
each other. The actual matching remains feasible.

Old matching mates do not change; every old retained-neighbour freezing witness
remains either an original selection or an original endpoint with the same
mate. Replay the entire old freezing certificate first. The addition of other
endpoints does not invalidate any such witness.

Fix c=4 or14. Every new endpoint (r,c) has the side witness (r,c+1) on its old
alpha strand. That witness's old actual mate is now frozen. At the upper end,
(7,c) is an old endpoint with frozen mate. Freeze

    (8,c), (10,c), ..., (W,c)                              (2)

in that order. For the first vertex use (7,c) and its side witness. For the
vertex (r,c) with r>8 use (r-1,c) and its side witness: the mate of (r-1,c)
is (r-2,c), already frozen in(2). The witnesses are distinct adjacent nonmates.
At the lower end (W+2,c) is an old endpoint with frozen mate. Freeze

    (W+1,c), (W-1,c), ..., (9,c)                           (3)

in that order, using the side witness and the next endpoint below. Its mate
is the previously frozen odd endpoint, or the old lower-boundary mate in the
first step. This proves complete freezing by two finite inductions for every
W; it is not extrapolation from enumerated heights.

The Lean lemma oriented_seal_frozen proves this arbitrary-length dependency
induction. frozen_extend_endpoints proves inheritance of old freezing under
unchanged old mates and retained witnesses. Coordinate contact lemmas verify
the upper and reversed lower orientations; the full all-W coordinate adapter
remains the written argument just given.

## 3. Complete original support and interval inventory

Use B for blank, T for selected and P for a matching endpoint. PT and TP have
the same unordered column type; below the labels keep the upper/lower order.
The packet's band-label lists, indexed by columns0..21, are

    top/bottom:
    BB BB BT PT BP PT BP PT BP PT BT BB BT PT BP PT BP PT BP PT BT BB
    second band (rows6,7):
    BB BB BB BT PP PP PP BT BT BB BB BB BB BT PP PP PP BT BT BB BB BB
    penultimate band (rowsW+2,W+3):
    BB BB BB BT PP PP PP BP PT BB BB BB BB BT PP PP PP BP PT BB BB BB
    every other interior band (rows8,9 through W,W+1):
    BB BB BB BB PP PP PP BB BB BB BB BB BB BB PP PP PP BB BB BB BB BB.

There are W/2-3 bands of the last type. There are no TT columns in these lists, so each BB column starts its own
BB--TT interval unit; consecutive BB columns are distinct units. The four band classes
have respectively4,10,10,16 interval units. Hence

    raw intervals = 2*4+2*10+16*(W/2-3) = 8W-20;
    original boundary marks B = 2*(W/2+1) = W+2;
    available original units I = 7W-22.                   (4)

Both extreme columns are BB and belong to different intervals in every band.
All other inventory follows directly from the coordinate lists:

    |T|=34, |M|=3W+10, |P|=6W+20;
    alpha=2, beta=0, mixed=14, pure cycles=2W-4.           (5)

For whole-support access, an alpha can own units in an endpoint-free gap only
if a boundary P column of that gap belongs to its path. In the top and bottom
bands, columns5 and15 have BP columns on both sides. In the second and
penultimate bands they have PP columns on both sides. In every remaining
interior band they now have PP neighbours4,6 and14,16. Consequently neither
alpha has **any** incident whole-support interval. Before the added caps,
columns4 and14 of the last band class were blank; those were precisely the
hidden private gaps. Newly added cycles do not belong to either alpha.
This proves the absence of every internal-support bypass, not just tip access.

Fix C0={ (5,5)--(5,6) }. This absorbs the left mixed strand at columns6,7
of the top band, making (5,7) the left upper free tip. Its new support still
has no interval: the adjacent endpoint columns4 and8 block both possible
gaps. Lower free tips are (W+4,5),(W+4,15); the right upper tip is (5,15).
The two isolated whole-support deficient components therefore persist.

## 4. Distinct mixed routes to one resource

Relative to C0 choose either or both of the legal links

    L: (5,7)--(5,8),     mixed exit (5,9);
    R: (5,15)--(5,14),   mixed exit (5,13).                (6)

Each uses a different mixed owner and different terminals. All links in C0,
L,R are unit horizontal original TP--BP adjacencies. Neither beta units nor
shared gates are involved. L sees the original singleton interval J in band0,
column11, namely the physical pair {(4,11),(5,11)}, through cap column10.
R sees the **same J**, through cap column12. The lists in Section3 show that
these added supports see no other available interval; all other alpha support
remains unchanged. J is unmarked and is separated from other BB intervals by
its neighbouring BT columns10 and12.

| Extra links after C0 | Whole-support owners of J | Maximum paid | Defect |
| --- | --- | --- | --- |
| none | none | 0 | 2 |
| L | left alpha only | 1 | 1 |
| R | right alpha only | 1 | 1 |
| L and R | both alphas | 1 | 1 |

The complete two-demand set has exactly one neighbouring resource. This is an
explicit Hall witness and proves the simultaneous payment maximum is one.
It realizes the preceding exact merge formula g=min(d,S) with d=2,S=1.
Starting instead after C0+L, adding R has d=1,S=0 and gain0: reaching a used
interval only transfers the unpaid root into a tight paid component. Thus
both forms of resource reuse occur in actual whole-support geometry.

## 5. Distinct lower repair and exact additional costs

A further legal link is

    D: (W+4,15)--(W+4,14), mixed exit (W+4,13).            (7)

Its cap column12 reaches the original singleton J_bottom in packet band W/2,
column11, physical pair {(W+4,11),(W+5,11)}. It differs from J by band identity.
The links C0+L+D therefore pay both alphas using distinct original units.
They use different mixed owners and terminals; beta consumption is zero.
The same D repairs C0+L+R with one further link, retaining the use of J.

The exact minimum number of **additional** links after fixed C0 is two.
Indeed both current alphas initially have empty whole support. There are no
beta strands, and one link can enlarge at most one alpha by a mixed strand;
an alpha--alpha link is not TP--BP. With one link at least one original alpha
still has empty support. L+D attains two. After C0+L+R, zero further links
cannot repair its Hall defect, while D repairs it in one. These are costs
relative to the declared fixed C0, not total costs including C0.

Write U for the unused available interval count at maximum allocation and t
for the deficient-component count. Initially U=I,t=2; after L+R, U=I-1,t=1;
after repair U=I-2,t=0. Throughout

    U+beta-t = I-2 = 7W-24 > 0.                           (8)

For example W=8 has a10-by22 packet,34 selected vertices,34 matching edges,
44 raw intervals,10 marks and I=34 available units; margin32. Independently,
packet area/2-|T|-|M|-B = 11(W+2)-34-(3W+10)-(W+2)=7W-24.
The construction refutes the individual compensation rule, not the target
inequality. Arbitrary right padding by2p blank columns creates p new units
per two-row band and moves each right mark to the new last interval. Thus I
and the margin increase by(W+2)p. The alphas remain behind the same endpoint
barriers, so their initial/collision defects remain2/1 for every p>=0.

## 6. Arbitrarily many simultaneous whole-support collisions

Translate each packet up by4 rows and place q copies at vertical stride W+4,
with two blank rows between successive packets. The enclosing whole board is

    height q*(W+2)+2*(q-1), width22.

There is no intercopy occupied adjacency, so the feasibility and freezing
proofs replay independently. Use all whole-board bands. Each empty separating
two-row band has22 singleton BB intervals and two marks, contributing20
available units. Thus

    alpha=2q, beta=0;
    I_q=q*(7W-22)+20*(q-1);
    margin=I_q-2q=q*(7W-24)+20*(q-1)>0.                  (9)

The q copies of C0 leave2q isolated deficient whole-support components. The
2q pairwise disjoint prescribed L/R continuations each succeed separately,
but simultaneously pay only q: each copy merges two old deficient components
with its one old unused unit. The remaining defect is q. The empty separator
bands have no alpha support and cannot silently act as extra donor credit.
The q different lower links D pay the remainder using q different original
lower intervals. The full mixed network therefore repairs this entire family.

## 7. Reproduction and exact verification scope

Run from the research root:

    python3 develop/check_whole_support_donor_collision.py --output output/whole-support-donor-collision-validation.json
    python3 develop/check_whole_support_collision_formal.py --lean /path/to/lean-4.33.0 --output output/whole-support-collision-lean-validation.json

The solver-free checker validates84 physical boards: every even W=8..40
with four padding choices, plus16 carried isometries. It checks420 physical
before/after transitions,24 whole-board stacks containing156 collision
clusters,444 monotone-extension models and744 component identities. It
recomputes feasible occupancy, full freezing, original interval identities,
whole-support incidence, exact merge gains, distinct lower repairs and residual
minimum link costs. Every declared link is checked against the original legal
TP--BP link set. The permanent W8 fixture records68 endpoints and ten freezing
layers. No SAT solver is needed to verify it.

Ten new Lean declarations and16 dependency audits pass locally on Lean4.33.0,
without sorry, native_decide or additional axioms beyond propext,
Classical.choice and Quot.sound. The new declarations cover general freezing
inheritance, arbitrary-length oriented seal induction, both coordinate contact
lemmas, scalar ledgers, and concrete W8 feasible geometry plus all68 frozen
endpoints. The all-height support inventory, full coordinate application,
stacking, matching allocation specialization and route optimality are written
proofs with finite independent checks; they are not claimed as fully formalized.
No external review of this new note has been requested or completed.

The next constructive problem is to choose legal mixed continuations with
enough different old unused units in every resulting component, respecting
mixed-owner capacity. This family supplies an actual, arbitrarily repeatable
test against resource reuse; it does not settle universal mixed compensation
or improve the general5/6 bound. The11 October submitted manuscript is preserved.
