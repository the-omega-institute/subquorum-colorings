# One square ear with an unbounded error and a connected residual graph

For every integer s>=1 there is a connected bipartite base B_s with a
specified single edge de, such that the residual R_s=B_s-{d,e} is
connected and bipartite, and attaching the square d-alpha-beta-e-d gives
a graph J_s satisfying

    |V(R_s)|=21s, |V(J_s)|=21s+4,
    SF_2(J_s)=12s+2,
    SF_2(R_s)<=12s-ceil(s/3).

Consequently

    SF_2(J_s)-(2+SF_2(R_s)) >= ceil(s/3).                 (1)

Thus connectedness of the base, final graph, and residual does not permit
an additive error bound depending only on the number of square ears.
The subsequent [exact interface theorem](EXACT_DECORATED_INTERFACE_FORMULA.md)
strengthens this to SF_2(R_s)=12s-mu(s), with exact single-ear error mu(s),
where mu(s)=2floor(s/4)+min(s mod4,2). The proof below retains the original
domination estimate and its original review scope.

The residual has maximum degree at most six. The two root degrees grow
with s, so (1) makes no fixed-degree claim for B_s or J_s.

## 1. The supplying local theorem

We use the fully proved local cap in
[the bipartite partial-ear note](BIPARTITE_PARTIAL_EAR_OBSTRUCTION.md),
Section 2. Recall its ten-vertex block: two-sets A,V,W,Z and vertices
p,u, with all A--V and W--Z edges and, for i=1,2, the edges

    a_i z_i, v_i w_i, p z_i, u w_i.

Only Z has neighbours outside the block; both Z vertices meet a common
vertex y. The whole exterior may be arbitrary, provided it attaches to
this block only through y. In any inclusion-minimal forming set S, the
block contributes at most six; it contributes at most five if it has
any selected Z vertex, or if y is selected. The proof uses safe deletions
which never delete Z and preserve the formation or activity needed at y.
It therefore applies when y also has neighbours in other modules.

Take two such blocks at each vertex y. This is the 21-vertex F_2 from
the supplying note. Its contribution to a minimal forming set in an
arbitrary exterior attached through y is at most twelve when y is
omitted, and at most eleven (including y) when y is selected. Moreover,
if y is omitted and a Z vertex is selected, the contribution is at most
eleven. All these are bounds on restrictions of a globally minimal
forming set, not assertions that the restriction is itself minimal.

Formation means formation by a not-necessarily-induced K_(1,2): every
outside vertex has at least two selected neighbours, or one selected
neighbour with a selected neighbour of its own. Minimality tests the
newly deleted vertex as well. This convention is the one used in the
supplying theorem and the checker here.

## 2. Construction and bipartition

Take s disjoint copies of F_2, with vertices y_1,...,y_s. Add exactly
the path edges y_j y_(j+1), j=1,...,s-1. The resulting graph is R_s.
Every copy of F_2 is connected, so R_s is connected. Its y vertices
have four block neighbours and at most two path neighbours. All other
degrees are at most five; hence Delta(R_s)<=6.

Each F_2 has bipartition

    L_j={y_j} union (A_j,1 union W_j,1 union {p_j,1})
                union (A_j,2 union W_j,2 union {p_j,2}),
    K_j=(V_j,1 union Z_j,1 union {u_j,1})
                union (V_j,2 union Z_j,2 union {u_j,2}).

Use L_j as the global left side for odd j and as the global right side
for even j, reversing K_j accordingly. Consecutive y vertices then
lie in opposite sides, so R_s is bipartite.

Add roots d,e and the edge de. Connect d to all odd-indexed y_j and e
to all even-indexed y_j. Put d on the right and e on the left. This
gives the connected bipartite base B_s. Attach new alpha on the left
and beta on the right, with d-alpha, alpha-beta, beta-e. Then J_s is
connected and bipartite, the specified root matching has one edge de,
and deleting d,e from the base leaves exactly R_s. Its order and the
final order are 21s and 21s+4 as claimed. In J_s, d and e have degrees
ceil(s/2)+2 and floor(s/2)+2, respectively.

## 3. A loss forced by the path of exterior vertices

Let S be any inclusion-minimal forming set of R_s. Let S_j be its
restriction to the j-th F_2 copy, and set

    c_j=12-|S_j|.

The local theorem makes every c_j a nonnegative integer. If c_j=0,
then y_j is omitted, and no Z vertex in either block of that copy is
selected. Otherwise one of the sharper eleven-point caps applies.
All selected neighbours capable of forming y_j must therefore lie
among y_(j-1),y_(j+1), with nonexistent endpoints omitted. Formation
in particular requires at least one such neighbour to be selected.
If y_i is selected, the eleven-point cap gives c_i>=1.

Thus the set D={j:c_j>=1} dominates the path on indices 1,...,s:
each index is either in D or adjacent to an index in D. A single path
vertex covers at most three indices in its closed neighbourhood. Taking
the union of these neighbourhoods gives

    s <= sum_(j in D) |N_path[j]| <= 3|D|.

It follows that

    sum_j c_j >= |D| >= ceil(s/3),
    |S|=12s-sum_j c_j <=12s-ceil(s/3).

This proves the residual upper bound. No sufficiency claim about this
dominating condition is needed: it is a necessary consequence of literal
formation and the local cap. The exact formula for SF_2(R_s) is
proved separately in the later interface theorem, using a stronger
activity-sensitive block cap. It is not a consequence of domination alone.

## 4. Exact value after attaching the one ear

The square-ear lemma needed here has a short direct proof. A forming
set selects at least two square vertices: with none, an interior vertex
has no selected neighbour; with only d (respectively e), beta
(respectively alpha) has none; with only alpha (respectively beta),
the other interior vertex has just that inactive selected neighbour.
If both roots are selected and at least one interior vertex is selected,
delete a selected interior vertex. The roots stay active through de and
form every omitted interior vertex. If exactly one root is selected
and there are at least three square selections, both interior vertices
are selected. For the selection {d,alpha,beta}, delete beta: the retained
active d-alpha edge forms beta and e. The other-root case is symmetric.
Every deletion preserves the selected roots' activity and hence all
exterior formation. Thus a globally minimal forming set has exactly
two square selections, even with arbitrary exterior root neighbours.

The arbitrary-exterior local
cap still bounds each F_2 copy by twelve, including y_j if selected.
Consequently SF_2(J_s)<=12s+2.

For attainment, in each of its 2s ten-vertex blocks select

    T=A union V union {p,u},

and select {d,e} from the square. Omit every y_j and all W,Z,alpha,beta.
Each W_i has selected neighbours v_i,u and each Z_i has selected
neighbours a_i,p. The roots d,e are mutually active, so they form all
y_j as well as alpha,beta. The whole set therefore forms and has size
12s+2.

Every selection is essential. Deleting a_i leaves z_i with the sole
inactive selected neighbour p. Deleting v_i leaves w_i with the sole
inactive selected neighbour u. Deleting p or u leaves that vertex with
no selected neighbour. The exterior y_j remains omitted in every such
test; none of the path edges or root edges affects these witnesses.
Deleting d leaves alpha with no selected neighbour, and deleting e
leaves beta with no selected neighbour. Thus every single deletion
fails. Formation is upward closed, so the set is inclusion-minimal.
This proves SF_2(J_s)=12s+2. Combining it with the residual bound gives
(1) for every s>=1. At s=1 the supplying theorem gives the exact
residual value eleven and the exact final value fourteen.

## 5. Verification scope

Run `python3 scripts/check_connected_residual_ear.py`. This standalone
checker constructs both graphs directly, checks the stated orders,
degrees, bipartitions and connectivity, and tests formation and every
single deletion of the attaining set, including each specified witness.
It also exhausts all index subsets for short paths to check the
dominating-set count independently. It does not enumerate all minimal
forming sets of R_s or J_s or establish their upper bounds by search.
The bounds for arbitrary s follow from Sections 3 and 4.

This deduction extends the arbitrary-exterior local cap accepted in
the separate bipartite partial-ear audit. Its own independent review
returned **ACCEPT** and ran the unchanged original checker with assertions
enabled. Both the generated349-byte report and stdout matched the supplied
report byte-for-byte: seven graph sizes s in {1,2,3,4,8,16,64},1,190
deletions,1,190 named witnesses, and32,766 path subsets for lengths1 to14.
These are the exact sampled sizes, not all integers through64.

The complete response, input hashes and execution scope are preserved
in `output/connected-residual-ear-review.json`, created after the verdict.
The reviewed input did not contain that subsequent review record or the
separate square-ear note. The reviewer reconstructed the square lemma
directly; that proof is now included in Section4 above. The only other
post-review changes clarify the witness wording and add this verification
record. No checker changed. The earlier partial-ear audits did not include
the present construction. No Lean verification is claimed here.
