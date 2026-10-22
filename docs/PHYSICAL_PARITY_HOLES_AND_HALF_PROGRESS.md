# Real-grid coverage has parity holes and can give only half the requested progress

23 October 2026. Authors: Haobo Ma and Wenlin Zhang.

The exact selector reduction solves coverage. Even on feasible, completely
frozen rectangular-grid packets with a unique actual matching, its feasible
selection sizes need not form an initial interval. We construct an all-size
family with exactly the feasible sizes 0,2,...,2q. At each positive feasible
size r, every admissible replacement leaves at least 2q-r/2 alphas, and the
smallest possible sign-error count is exactly r/2. These bounds permit
arbitrary internal rematching, joint source/resource endpoint choices and
activation of any collection of complete original mixed pairs.

This is a counterexample to deriving r units of compensation from a size-r
coverage solution, or to growing coverage by single-unit augmentation in
the general selector model. It is not a counterexample to the grid scalar
inequality: its packet margin is explicitly positive, and interval resources
are deliberately not virtualized in this beta-only coverage question.

## 1. A block-balance obstruction before any orientation search

Let M,A,E and source/resource/mixed groups satisfy the balanced mixed-port
interface. Partition the original endpoint set into blocks X such that every
old A edge, every original open strand and every candidate E edge stays in
one block. Original cycles must also lie in individual blocks. In particular,
the blocks can be unions of components of E when E contains M and A.

Write a_X for the number of selected source ends in X, b_X for selected
resource ends, and t_X for activated whole mixed pairs. An admissible N
restricted to X covers

    2|A_X|+a_X+b_X+2t_X vertices.

Therefore a_X+b_X is even. In the prescribed signing the old A-covered
vertices have total sign zero, and each active mixed pair adds zero.
Selected source and resource ends add -a_X and +b_X. Since N has no edge
leaving X, signed incidence gives the stronger exact identity

    a_X-b_X = 2(h_minus,X-h_plus,X).                    (1)

Consequently a coherent replacement requires a_X=b_X in EVERY block,
not merely equality of the global source and resource totals. Also

    h >= (1/2) sum_X max(a_X-b_X,0)
       = (1/4) sum_X |a_X-b_X|,                        (2)

where h is the global number of negative same-sign N edges and the second
equality uses sum a_X=sum b_X. Negative internal edges in different blocks
are distinct, so this is not a repeated charge of the same sign error.
These errors bound progress; they are not interval or beta resource units.

### The corresponding cut identity

If X is a union of original M/A components but E may leave X, let c_minus,X
and c_plus,X count N edges crossing its boundary, according to the sign of
their endpoint inside X. The same incidence calculation gives

    a_X-b_X = 2(h_minus,X-h_plus,X)+c_minus,X-c_plus,X. (3)

For coherent N all internal errors vanish and every crossing edge has
opposite endpoint signs. Direct it from its negative endpoint to its
positive endpoint. Then a_X-b_X is exactly its outgoing-minus-incoming
unit flow. In particular

    |a_X-b_X| <= |N crossing X| <= nu(E crossing X),     (4)

where nu is the maximum matching size in the bipartite cut graph. The last
bound uses endpoint capacity, not the number of available candidate edges.
This is a necessary cut condition, not a sufficient existence theorem.
Equations (1)--(4) are direct general proofs independent of the family below.

## 2. Explicit physical building blocks

Use the accepted D(W,4) template, for even W>=6. To make the coordinates
reproducible, its selected set is

    {(4,3),(4,5),(4,7),(5,2),(5,8),(6,6),(7,5),
     (W+4,2),(W+4,8),(W+5,3),(W+5,5),(W+5,7),(W+2,6)}.

Its actual edges are

    (row,3)--(row+1,3)       row=5,7,...,W+3;
    (row,4)--(row+1,4)       row=6,8,...,W+2;
    (5,4)--(5,5), (5,6)--(5,7);
    (W+4,4)--(W+4,5), (W+4,6)--(W+4,7);
    (W+3,5)--(W+3,6).

It has 13 selected sites and W+4 actual edges. Its existing serial freezing
and forced-matching schedules are given in uniform_certificates of the
terminal-cancellation checker. Translation and reflection preserve them.

Fix d>=2 and L=2d+4. A pair packet contains a reflected copy under
(row,column)->(row,10-column) and an ordinary copy translated L columns
to the right. Actual endpoints in either copy occupy only columns 3..7
and L+3..L+7 respectively, leaving a gap of 2d-1 columns, 8..L+2.

An **alpha pair packet** keeps these row coordinates. For each gap column
c, add a selected site at row5 if c is even and row4 if c is odd; do the
same at row W+4 if c is even and row W+5 if c is odd. The first and last
sites in each row chain are already old selected caps. There are two
original alphas, no beta and ten mixed paths. The alpha tips are

    (5,7), (W+4,7);     (5,L+3), (W+4,L+3).

The only all-BT portal edges between the copies join the upper two alpha
tips and the lower two alpha tips. In particular, the one-edge route

    (5,7), (5,L+3)                                      (5)

is a permitted source--source auxiliary addition.

A **beta pair packet** instead translates both base copies down one row.
In the upper gap use selected row6 at even c and row7 at odd c; in the
lower gap use selected row W+5 at even c and row W+4 at odd c. The original
inventory is no alpha, two betas and two mixed paths. The beta tips are

    (6,5), (W+5,3);     (6,L+5), (W+5,L+7).

The upper and lower corridor boundaries are now PP columns. Each corridor
supplies its four row combinations as candidate portal edges. The route

    (6,L+5), (6,L+4), (7,L+4), (7,L+3), (6,L+3),
    (6,7), (7,7), (7,6), (6,6), (6,5)                   (6)

alternates five new candidate edges and four old A edges. Its central edge
is an upper portal; the other new edges are occupied horizontal grid edges.
The removed A edges are the vertical pairs in columns L+4,L+3,7,6 of that
upper band. Thus it covers one tip from each beta, with no mixed activation.

### Physical validity for all parameters

The gap has odd length at least three. Selected sites alternate rows; the
two end sites in each gap are the original caps, each adjacent to exactly
one old endpoint. Every newly added selected site is strictly inside the
endpoint-free gap, is isolated from the other selected sites, and has no
old endpoint neighbor. No old selected site gains an occupied neighbor.
Thus feasibility follows from that of each D template.

Actual endpoints in different copies have no grid adjacency across the
gap. All original freezing witnesses survive; new selected sites cannot
invalidate them. The actual endpoint graph is the disjoint union of the
two template endpoint graphs, so its perfect matching remains unique.
The gap changes the auxiliary candidates, not the actual matching.

In the even placement a direct trace of the two template paths gives the
stated alpha inventory. In the odd placement, the column-3 actual edges
become doubled M/A cycles, and the column-4 chain joins the upper free
tip at column5 to the lower tip at column7. This is the sole beta of each
ordinary copy; its reflected image has columns5 and3. The remaining top
horizontal pair forms the sole mixed strand. This proves the beta inventory.

## 3. The full q-family and its exact feasible sizes

Take q alpha pair packets and q beta pair packets, alternately translated
down by multiples of W+16. Put them in the rectangle

    m=2q(W+16), n=2d+20, q>=1.

Use every row band (2j,2j+1). Include in E EVERY occupied-endpoint grid edge
and EVERY row combination across each maximal endpoint-free all-BT gap.
Thus M,A are subsets of E. No E edge joins different pair packets: the
packets are separated by blank rows and gap edges remain within row bands.
The whole packet inventory is

    k=b=2q, g=12q.                                     (7)

Source groups are all original alphas and resource groups all original
betas. Permit activation of any complete original mixed pairs. No interval
is virtualized, and no old alpha payment is reserved: f=0.

**Exact coverage theorem.** An admissible N selecting r different sources
and r different beta resources exists if and only if

    r in {0,2,4,...,2q}.                                (8)

Proof. Each alpha pair block contains no original beta, at most two source
groups, and only complete internal mixed groups. By the even-domain count
in Section1, its number of selected source ends is either zero or two.
Summing over alpha blocks makes r even. The same holds on beta blocks.
Optional mixed activation contributes an even number and cannot remove
the parity obstruction. Clearly r<=2q.

Conversely, for r=2a choose a alpha blocks and a beta blocks. Add (5) in
each chosen alpha block, and flip the A-alternating route (6) in each
chosen beta block. Retain A elsewhere. Every selected group contributes
exactly one end; all old PP vertices remain covered. These disjoint
replacements select exactly r different source and resource groups. QED.

There is also an explicit Tutte certificate in the selector graph G_r for
every odd r. Partition its vertices into all alpha-block physical and
local gadget vertices plus the r source slots, and all beta-block vertices
plus the r resource slots. There are no edges across this partition.
Each part has even local vertex count plus r, hence is odd. Therefore G_r
has at least two odd components already at Z=empty. For q=1 this gives
G_2 perfectly matchable while G_1 has this explicit obstruction.

## 4. Exact half-progress and unavoidable orientation error

**Sharp progress theorem.** For any admissible N at a feasible size r,
allowing all the freedoms in Section3,

    alpha_N >= 2q-r/2, beta_N >= 2q-r/2,
    h >= r/2                                            (9)

for every allowed original-cycle signing. All three optima are attained
simultaneously by the construction above. In particular no positive-r
admissible replacement is coherent, and coverage size r does not establish
the desired alpha_N<=2q-r.

Proof. In an alpha pair block with a selected source ends and t active
mixed pairs, the surviving free endpoint inventories satisfy

    2 alpha_X+mixed_X = 4+10-a-t,
    2 beta_X +mixed_X = 10-t.

Hence alpha_X-beta_X=2-a/2, so alpha_X>=2-a/2. Sum over all alpha blocks;
any alphas in beta blocks are additional. This gives the first inequality.
The symmetric beta-block calculation gives the second. Equation (2)
gives h>=r/2 directly: all source selections are in source-only blocks,
and all resource selections in resource-only blocks.

For attainment, the source--source link merges two old alphas into one
alpha. The beta route merges the two lower beta tails into one beta;
its first and last new edges double actual edges, and it opens the old
two-edge cycles at columns7 and L+3. No original mixed path is changed.
After a paired source/beta operation the inventories are alpha1, beta1,
mixed12 in place of alpha2, beta2, mixed12. Thus the construction has

    alpha_N=beta_N=2q-r/2, mixed_N=12q.

The selected upper alpha ends both have negative sign, so (5) contributes
one negative N edge. The chosen upper beta tips have positive sign. Their
actual mates in columns6 and L+4 are negative, and their old A mates in
row7 are positive. Give each opened cycle positive sign in row6 and
negative sign in row7. Then every new beta-route edge crosses signs except
the central portal, whose endpoints are both positive. All retained A
edges cross. This is exactly one negative and one positive N edge per
paired operation, so h=r/2. The construction adds 3r auxiliary edges and
deletes 2r; no claim of cost optimality is made. QED.

At r=2q, coverage has selected every original alpha and beta group, yet
at least q alphas and q betas remain. The failure is exactly the proposed
coverage-to-compensation implication, with arbitrary-size sharp error q.

## 5. Positive physical ledger and next proof obligation

The full rectangle has

    |T|=q(8d+40), |M|=4q(W+4), B=2q(W+16).

The two corridor bands in each pair packet add 4d-6 selected sites beyond
their two base copies; the end caps were already counted. It follows that

    S_J-B=q[(2d+14)W+24d+232] > 0.                       (10)

Here S_J=mn/2-|T|-|M|. Since k=b, the original interval-unit ledger has
exactly this positive surplus after its boundary units are removed.
The family therefore does not disprove the scalar target or any claimed
universal grid bound. Allowing certified interval resources changes the
selection problem and can break the source/resource separation. Such an
access must name its original interval identity and remove its former
credit if virtualized; the parity obstruction does not license duplicate use.

The useful refinement is to test block and cut balance before treating a
coverage solution as progress. A successful general proof must supply
coherent boundary flux or distinct accessible interval resources to each
source-heavy region. Merely maximizing the global number of selected
source and beta groups, even with complete mixed-pair activation, is
insufficient. Equations (3)--(4) expose the geometric capacity obligation;
they do not settle its sufficiency or the general grid problem.

### A complete interval repair of this same family

The original interval interface gives an explicit positive repair, not just
the scalar positivity check. In every alpha pair block use these four
terminal TP--BP links, with that block's row translation understood:

    (5,7)--(5,6),       (5,5)--(5,4),
    (5,L+3)--(5,L+4),   (5,L+5)--(5,L+6).                (11)

The reflected copy's original upper mixed strands are
(5,6)--(5,5) and (5,4)--(5,3); the ordinary copy's are
(5,L+4)--(5,L+5) and (5,L+6)--(5,L+7). Thus each selected upper source
end continues through exactly two different old mixed strands. Its final
alpha retains the old lower source end and ends at (5,3) on the left or
(5,L+7) on the right. The four links are occupied horizontal grid edges,
and different branches have disjoint terminals and old mixed owners.

The left final tip has the selected cap (5,2) in a BT column and a BB
column at column1 beyond it; the right tip similarly has selected cap
(5,L+8) and BB column L+9. These are exactly the existing selected-cap
access certificates: the cap is in the tip's row and the target column
is BB. The accessed original units are the singleton BB intervals

    (upper band,column1), (upper band,column L+9).

They are different, contain neither boundary column, and are different
again in different translated alpha blocks. Both witnessing tips remain
free of cancellation. Pay each of the 2q final alphas by its specified
unit. No old beta is consumed; no opened cycle or mixed path supplies a
credit. After the 4q links, the terminal inventory is

    alpha'=2q, beta'=2q, mixed'=8q,

and every final alpha has a different original interval payment. Hence
the exact terminal-cancellation/allocation compensation value is 2q,
the maximum possible. The number of unpaid alphas is zero.

This uses the already proved cancellation and selected-cap access
interfaces, and gives an all-parameter geometric assignment. It does not
claim physical auxiliary coverage of the payment tips: those tips remain
free and witness interval payments. If the intervals are instead represented
by formal beta groups, their original units must be removed from the old
ledger before applying the accounting selector construction. Either view
changes the beta-only coverage problem of Sections3--4, so there is no
contradiction with its parity holes or unavoidable same-sign error.

This positive repair was added after the parity-hole review was dispatched.
That first task, ef2bd5ff-d074-43cb-b1d2-81d185cc755e, subsequently ended in
`infrastructure_retry_exhausted / cdp_disconnected@typing` without a
mathematical answer. Its failure is archived separately. The full version,
including this repair, is now under independent review in fresh task
ad20d68a-f6be-4046-abd2-fec554a524b3. No acceptance is claimed in advance.

## 6. Reproducibility and scope

The checker passes 36 complete feasible/frozen/unique-matching families,
108 explicit even-size replacement witnesses with selector lifts and exact
forest error certificates, 144 independent even-vertex blocks and 720 full
candidate portal edges. It separately checks 4706 abstract block selections.
Additional controls construct 72 actual odd-r selector graphs and verify
their empty-set Tutte witnesses, 480 exact signed block identities, and
36 complete interval repairs using 144 different original payments over
288 terminal links. No old beta is consumed in those interval repairs.
Odd-size impossibility, arbitrary-mixed-activation robustness and the
all-size lower bounds follow from the written proofs, not exhaustive
enumeration of physical replacements.

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_physical_joint_selection_parity_holes.py --output output/physical-joint-selection-parity-holes-validation.json

This theorem is later than the accepted balanced-mixed/selector review and
is not covered by that acceptance. General grid compensation, universal
5/6 improvement and rectangular-grid triple equality remain open.

Eleven local declarations in `formal/SubQuorum/JointSelectionBlockBalance.lean`
compile in Lean4.33.0 on the session-selected local Mac. They prove endpoint
cardinality from supplied incidence permutations, closed-block parity,
signed balance and disjoint error summation, conditional cut capacity,
half-progress and the odd-slot obstruction. All eleven axiom audits pass;
ten use propext/Quot.sound and the cut-capacity declaration additionally
uses Classical.choice. There is no sorry, native decision or new axiom.
The actual geometric incidence and matching constructions remain written
proofs; this is not a formalization of the complete graph theorem.
The execution record is `output/physical-joint-selection-parity-holes-lean.json`.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
