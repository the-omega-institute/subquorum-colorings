# Exact deletion certificates can require a neutral exchange to escape

Optimizing [cover-saturated exchanges](COVER_SATURATED_COORDINATED_EXCHANGES.md)
over all minimum covers and all proposed operations still need not recover the
true minimum matching cost. The shared odd-path family gives an exact barrier:
for every even $r\ge4$, the best such one-batch certificate has cost one,
whereas the actual all-helper optimum has cost zero. Reaching zero requires
$r$ replacements, although only $r-1$ matching edges are available to save.
There is an explicit permitted route, and in any order of its $r$ operations,
exactly one operation is neutral and all the others save one matching edge.

## Setup

Take indices $V=\{0,\ldots,4r-1\}$, $b=2r$, with $r\ge4$ even.
Let $A=P\cup Q=C_{4r}$ in its natural cyclic order:

$$
 P=\{(2j,2j+1):0\le j<2r\},\qquad
 Q=\{(2j+1,2j+2\bmod4r):0\le j<2r\}.
$$

Give index $v$ physical colour $\lfloor v/2\rfloor\bmod2$. With
$\pi(i)=i\mathbin{\mathrm{xor}}1$, the owner squares are

$$
 K_i=(2i,2r+2\pi(i),2i+1,2r+2\pi(i)+1),\quad 0\le i<r.
$$

These define the same $10r$-vertex two-connected bipartite physical family
of minimum degree two and maximum degree three as in the
[shared-path construction](PAIR_CONFLICTS_AND_ACTIVATION_BUDGET_OPTIMUM.md).
The physical graph has helpers subdividing $P$, witness edges $Q$, each
witness attached to its own owner, and the owner squares. Its witness/helper
core is a subdivided cycle. After deleting one core point each owner square
retains at least three attachments to the remaining connected path; after
deleting an owner the residual owner path still has three attachments to the
intact core. This proves two-connectivity.

Use the permitted initial omission

$$
 U_1=\{1,\ldots,2r-1\}\cup\{2r+2\},\qquad |U_1|=2r.
$$

It has two points in every owner square. Its auxiliary graph is an odd path
on $1,\ldots,2r-1$ plus one isolate, so

$$
 \nu_1=r-1,\qquad C_1=\{2,4,\ldots,2r-2\}
$$

is a minimum cover.

## Sharp obstruction to every one-batch exact-deletion certificate

Allow arbitrary replacement sets $X\subseteq U_1$, $Y\subseteq V\setminus U_1$
with $|X|=|Y|$, subject to $X$ lying in some minimum cover of $A[U_1]$
and every point of $Y$ being isolated in the final induced graph. Allowing
arbitrary $X,Y$ here is more generous than one operation per owner; owner
permittedness is required for a physical certificate.

**Theorem.** The best cost attainable by such a certificate is exactly one.
The actual minimum over all permitted omissions is zero, so $\beta_I=6r$.

**Proof of the obstruction.** A zero-cost final omission $U'$ is independent
in $C_{4r}$. Cardinality is preserved, so $|U'|=2r$, the maximum independent
size of that cycle. The only independent sets of this size are the even and
odd classes $E,O$: between consecutive selected points there must be at least
one unselected point, and equality of the two counts makes every cyclic gap
exactly two. Both intersections have size $r$:

$$
 |U_1\cap E|=|U_1\cap O|=r.
$$

For $E$, there are $r-1$ even indices in the odd path and the extra even
isolate; for $O$ there are the $r$ odd indices of the path. Thus reaching
either zero-cost omission requires exactly $r$ replacements. But a deletion
set contained in a minimum cover has size at most $\nu_1=r-1$. Therefore
no such batch can reach cost zero, regardless of the cover or additions
chosen. Its nonnegative integer cost is at least one.

**Attainment of cost one.** For $j=2,\ldots,r-1$, replace

$$
 2j\longmapsto2r+2\pi(j).
$$

These are $r-2$ different owner operations with removals in $C_1$.
Their additions are independent and have no neighbour in $U_1$.
Each changed owner complement is an edge, and all unchanged owner components
remain permitted. The cover-saturation theorem gives exact cost
$(r-1)-(r-2)=1$. Hence the certificate optimum is exactly one.

Finally, $E$ is itself permitted: every owner square has its two odd
indices retained, an owner edge. Thus it gives cost zero and the all-helper
objective $\beta_I=3b-0=6r$. ∎

This is a barrier to completeness of the **one-batch exact-deletion rule**,
not a counterexample to the rule's validity. Nor does it obstruct the
$8b/3$ target on this family: cost one already meets its threshold
$\lfloor2r/3\rfloor$. It is not an exact claim about the unrestricted
physical dissociation number.

## Every displayed shortest route has exactly one neutral step

There is a direct owner-by-owner route from $U_1$ to $E$:

$$
 \begin{array}{ll}
 K_0:&1\mapsto0,\\
 K_1:&3\mapsto2r,\\
 K_i\ (2\le i<r):&2i+1\mapsto2r+2\pi(i).
 \end{array}                                             \tag{1}
$$

On $K_0$, the unchanged omitted point is $2r+2$; on every other square
it is $2i$. Thus (1) leaves exactly its two even indices omitted in every
owner square. Every operation is permitted, and any ordering remains
permitted throughout because the owner components are different.

**Proposition.** Every permutation of (1) has exactly $r-1$ steps reducing
the matching cost by one, exactly one step leaving it unchanged, and no
step increasing it.

**Proof.** One replacement removes one old vertex and adds one new vertex.
Deletion changes matching number by zero or minus one; addition changes it
by zero or plus one. A complete replacement therefore changes it by
$-1,0$, or $1$. The $r$ replacements start at cost $r-1$ and end at zero.
Let $d,z,i$ be the numbers of decreasing, neutral and increasing steps.
Then $d-i=r-1$ and $d+z+i=r$, so $2i+z=1$. Hence $i=0,z=1,d=r-1$. ∎

Any cardinality-preserving route from $U_1$ to a zero-cost omission needs
at least $r$ replacements, because each replacement can remove only one
point from $U_1\setminus E$ or $U_1\setminus O$. In particular a
strict-descent-only route cannot reach zero: it can have at most $r-1$
strict decreases from the initial nonnegative cost $r-1$. This explains
precisely why an algorithm insisting on an immediate saving at every step
can stop too early. The displayed route proves that one neutral exchange
suffices for every scale and every ordering of those operations.

A longer owner-permitted route can avoid neutral steps by first increasing
cost. At $r=4$, the replacements $1\mapsto11$, $10\mapsto1$,
$2\mapsto9$, $4\mapsto15$, $6\mapsto13$ reach $O$ with costs
$3,4,3,2,1,0$. Thus the necessity statement concerns nonincreasing
single-replacement routes and the displayed shortest route, not all longer
routes permitting increases. This control was supplied in the independent
review and separately checked locally.

## Evidence and scope

The standalone checker uses only the Python standard library. It constructs
coordinates directly, checks every one-operation-per-owner outcome for $r=4,6$,
checks all orders of (1) on those scales, verifies the only maximum independent
sets by literal enumeration on $C_{16}$, and checks explicit certificates and
random schedules at larger even scales. It does not import the project
matching or exchange algorithms. General-size statements have the proofs above.
Independent review returned **ACCEPT**. The reviewer ran the original
checker unchanged with assertions and reproduced its complete report
byte-for-byte. The full response, frozen hashes and actual execution scope
are preserved in [`output/exact-deletion-barrier-review.json`](../output/exact-deletion-barrier-review.json). The universal physical bound and all general
grid objectives remain open; no Lean is used.
