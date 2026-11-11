# A degree bound for selected-star gaps when the minimum degree is at least two

Let G be nonempty, finite, simple and bipartite, with minimum degree at least
2 and maximum degree Delta. Let S be an inclusion-minimal two-star-forming
set whose selected components are stars, edges or isolates. Write n=|V(G)|,
d=|S|-beta_2(G) and M=max(7,Delta). Then the degree bound is

    d <= floor(M*n/(12*M+2)).

No sharpness of this new coefficient is claimed. It concerns the specified
selection, and not every minimal forming set in an arbitrary graph.

Use the one permitted witness assignment in SHARP_SELECTED_STAR_GAP.md.
There are c selected centres, e=2c+s selected leaves, q direct-only centres,
e+q distinct chosen outside witnesses W, and t=a+b2+b3 touched selected
isolates, classified by h=1,h=2,h>=3 chosen-witness neighbours. Let mu be
the matching number of the labelled centre-to-h2-helper graph. Put

    r=n-(c+2e+q+t)>=0.

This r counts exactly all selected edge vertices, untouched selected
isolates, and outside vertices not in W. In particular it is at least
the number of outside vertices not in W. The proved ledgers are

    t>=2d+s,
    q+s+2mu-2b2>=0,
    4n>=48d+9s+b3+7mu,
    6n>=72d+q+13s+10mu.

Repeating their proof with the exact r remainder in the vertex count gives

    4(n-12d)>=9s+b3+7mu+4r,                 (A)
    6(n-12d)>=q+13s+10mu+6r.                (B)

The added terms follow because the only use of n in each proof was the
lower bound n>=5c+3s+q+2d; its strengthened version has an additional +r.
No new witness assignment or reallocation is made.

Every h=1 selected isolate has at least two graph neighbours, no selected
neighbour, and exactly one neighbour in W. It therefore has a neighbour
outside S union W. Each such unused outside vertex has at most Delta
neighbours, so counting these actual edges gives

    a <= Delta*r.                            (C)

Write eta=n-12d>=0. The t and b2 ledgers imply

    2d <= a+b2+b3-s
        <= a+q/2+mu+b3-s/2.

Adding (A) to one half of (B) gives

    q/2+b3 <= 7eta-(31/2)s-12mu-7r.

Using (C),

    2d <= 7eta+(Delta-7)r-16s-11mu.          (D)

If Delta<=7, nonnegativity gives 2d<=7eta. If Delta>=7, (A) gives
r<=eta, hence 2d<=Delta*eta. In either case 2d<=M(n-12d), proving
the claimed integer bound. When d<=0 the conclusion is immediate.

More generally, if minimum degree is at least delta>=2, each h=1 isolate
needs at least delta-1 neighbours outside S union W. Thus
(delta-1)a<=Delta*r. With L=max(7(delta-1),Delta), the same proof gives

    d <= floor(L*n/(12*L+2(delta-1))).

The minimum and maximum degree assumptions refer to the entire graph.
These bounds improve n/12 within the selected-star class for fixed Delta,
but their optimality and implications for all minimal grid selections are
separate questions. No universal 5/6 improvement is inferred.

Reproduce the finite controls with `python3 scripts/check_selected_star_degree_budget.py`.
The controls and general argument have separate verification scopes; see
`output/selected-star-degree-budget-review.json` for the final review status.

Both the initial degree-refinement review and the final source audit returned
**ACCEPT**. The final review reconstructed all five manifest files, ran the
original public-path checker unchanged with assertions to terminal completion,
and reproduced its entire finite report byte-for-byte. The 727,240 ledger
controls and the 38-vertex exact optimization support the general proof above.
