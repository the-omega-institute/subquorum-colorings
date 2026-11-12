# Short auxiliary components: square completion and owner-path surplus

13 November 2026. This note closes the mixed P2/P4/C4 auxiliary class for
arbitrary owner paths and even cycles. It also records a quantitative
owner-path refinement of the preceding rainbow-forest theorem. No assertion
is made for longer auxiliary paths or cycles.

## 1. Domain and exact target

Use N=2b witness indices, a perfect helper matching P, a partial witness
matching Q, and A=P union Q. The owner graph B has paths or even cycles as
components. In the physical bipartite domain, colours agree on P and differ
on Q and B. The actual template has b helpers, N witnesses and N owners,
and has maximum degree at most3. All helpers must be retained.

An omission U is permitted when B[V minus U] has maximum degree at most1.
The established exact formula is

    beta_I = 3b - min_permitted_U nu(A[U]).                       (1)

Let

    R(B) = sum (|K| mod3), over the PATH components K of B,      (2)

including isolated vertices as paths of order1. Cycles do not enter R.

**Theorem1.** If every auxiliary component of A is P2, P4 or C4, there is
a permitted U satisfying

    nu(A[U]) <= floor((N-R(B))/6).                              (3)

Consequently the original physical template has an actual all-helper
dissociation certificate of size

    beta_I >= 3b-floor((2b-R(B))/6)
            = ceil(8b/3+R(B)/6) >= ceil(8b/3).                  (4)

The abstract statement3 needs no physical colouring. The physical statement
uses only the original template's edges. In particular, artificial completion
edges need not respect its bipartition and are never added to that graph.

## 2. The owner-path surplus already present in the forest proof

**Lemma2.** If A is a union of C4s on M vertices and B has paths/even cycles,
there is an A-independent B-dissociation set S with

    |S| >= ceil(M/3+R(B)/6).                                  (5)

**Proof.** Use the preceding [all-owner square theorem](ALL_OWNER_AUXILIARY_SQUARES.md)
and its [complete rainbow-rank proof](../manuscript/auxiliary-square-forest-proof.tex),
keeping the path surplus instead of discarding it. The details needed for
the refinement are as follows.

Remove closed components of A union B consisting of one owner C4 on one
auxiliary square, or two owner C4s on two auxiliary squares. They supply
respectively2 compatible vertices on4 indices and3 on8. They contain no
owner paths, and exceed their order divided by3 by2/3 and1/3, respectively.

On the residual instance let exceptional owner cycles have deficits d_i=2/3
for order4mod6 and d_i=1/3 for order2mod6. Put d=sum d_i. An owner path of
order l has maximum dissociation size ceil(2l/3), and

    ceil(2l/3) - 2l/3 = (l mod3)/3.

Thus the residual owner dissociation number is exactly

    beta_2(B_res) = 2M_res/3 + R(B)/3 - d.                     (6)

The earlier graphic-rank argument gives one rainbow forest of r>=d
prescribed-edge exchanges, at most one per exceptional owner cycle. For
clarity, for every subset of such cycles, a connected projected component
with x cycles of order4mod6 and y of order2mod6 uses at least x+2y auxiliary
squares. Its graphic rank is at least(2x+y)/3. The only small exceptions
would fill one or two squares with closed owner C4s, already removed.
Rado's independent-representative formula therefore gives r>=sum d_i.
These inequalities hold for every subset of cycles, on the same rank
ground set; no separate credit is allocated to overlapping subsets.

The leaf-to-root parity switches of that one forest make at least r square
intersections of a maximum owner set odd. Independent subsets in those
squares have total size at least

    ceil((beta_2(B_res)+r)/2)
      >= ceil(M_res/3+R(B)/6).                               (7)

Unite with the compatible sets on the removed closed components. Their
nonnegative surplus and integrality give5 for the full M. Each square is
used once, every owner exchange belongs to its own cycle, and the same
global R(B) occurs once in6. QED.

This is a refinement of the existing proof, not a new independent use of
Rado's theorem. Its classical attribution and general representative proof
remain in the cited manuscript source.

## 3. Completing the auxiliary graph, including odd P2 parity

**Proof of Theorem1.** Close each P4 by joining its two endpoints. Pair the
P2 components; for pairs (a,b),(c,d), add bc and da to form a C4. Existing
C4 components remain as they are. All original auxiliary edges are retained.

If the number of P2 components is even, this gives a square union A+ on
the original N indices. Lemma2 provides S independent in A+, dissociation
in B, and |S|>=ceil(N/3+R/6). Put U=V minus S. On an auxiliary square K,
independence of S implies

    nu(A+[K minus S]) = 2-|S intersect K|.

Summing disjoint squares yields

    nu(A+[U]) = N/2-|S| <= floor((N-R)/6).

Removing completion edges cannot increase matching number, so the same
permitted U proves3 in the original A.

If the P2 count is odd, add ONE artificial P2 on two new indices, and pair
it with the remaining original P2. Declare both new owner vertices isolated
in B+. Now M=N+2 and

    R(B+) = R(B)+2.                                          (8)

Apply Lemma2 on the completed square graph A+ to obtain S+. For U+=V+ minus
S+, the SAME single global matching calculation gives

    nu(A+[U+]) = M/2-|S+|
       <= floor((M-R(B+))/6)
        = floor((N-R(B))/6).                                 (9)

The two added indices increase the order by2 and the path remainder by2;
these cancel inside the one floor in9. There is no separate rounding of
the artificial component and no duplicate path credit.

Restrict S+ to original indices and take U=V minus(S+ intersect V). It is
permitted, because the original B is unchanged and dissociation is hereditary.
A[U] is a subgraph of A+[U+], so its matching number is no greater. This
proves3. Finally compute an actual maximum independent set T in the ORIGINAL
A[U]. The original helpers, original owners V minus U, and witnesses T form
the physical dissociation set counted in1, proving4. QED.

The completion is an auxiliary proof device. Pairing two P2s of the same
physical colour can give completion edges incompatible with that colour.
This is allowed because Lemma2 is colour-free; no bipartite physical
completion, extension of the actual Q matching, or preservation of degrees
in an augmented physical graph is asserted. The delivered physical certificate
is checked using the original P,Q,B and colours only.

The coefficient8/3 remains sharp in this class: the previously proved
thirty-vertex block with all auxiliary components C4 has b=6 and beta_I=16.
No sharpness assertion is made for connected strictly mixed subclasses.

## 4. A connected mixed instance outside preceding global tests

The [fixed coordinate fixture](../develop/fixtures/short-auxiliary-completion.json)
has b=40 and200 actual vertices. Its auxiliary graph has18 C4s and2 P4s;
its owner graph is8 C8s and one C16. It is bipartite and connected with
minimum degree2 and maximum degree3. The checker verifies these statements
directly on all actual vertices and edges.

Its minimum omission cardinality is30. The old one-saving cardinality rule
would give14, above the target floor(80/6)=13. It has9 exceptional owner
cycles, and none is C4 or6k. All512 alternating owner-matching phase choices
have at least2 K4s; hence neither K4-free nor at-most-one-K4 repair applies
to those specified matchings. The auxiliary-square-only API also rejects it.

The new construction returns a valid all-helper set of size111, with original
matching cost9. Its target is107; no exact all-helper or unrestricted optimum
is claimed for this200-vertex graph. This example witnesses applicability
beyond the listed global tests, not a new universal graph-gap coefficient.

## 5. Implementation, verification and remaining scope

[short_auxiliary_completion.py](../develop/short_auxiliary_completion.py) returns
the added auxiliary edges, any artificial indices, full forest certificate,
and permitted original U, original matching and physical owner/witness set.
The existing square constructor gains a colour-free entry point with explicit
input validation; its original physical API and report remain unchanged.

Run the assertion-enabled checkers:

```sh
python3 -B scripts/check_short_auxiliary_completion.py
python3 -B scripts/check_auxiliary_square_forest.py
```

The first uses independent matching recurrences, literal owner/omission
choices, original physical induced-degree checks, artificial-edge colour
controls, odd P2 parity and path-remainder cases. The second checks regression
of the inherited complete constructor against its original full report.
General statements rely on the proofs, not finite extrapolation.

This proves the actual all-helper target for arbitrary short auxiliary
mixtures. It does not solve unrestricted omission optimization, general SF/beta
complexity, longer auxiliary P6/P8/C8 components, the universal subcubic sharp
gap constant, geometric multiple-Hall routing, unit5/6 or arbitrary-width grid
triple equality. No submitted manuscript or email is changed.
