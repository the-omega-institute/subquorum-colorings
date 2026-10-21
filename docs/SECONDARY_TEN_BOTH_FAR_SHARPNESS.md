# A sharp simultaneous family with both far lengths unbounded

22 October 2026. This is a corollary of the exact ledger in
[the both-far compensation theorem](SECONDARY_TEN_BOTH_FAR_COMPENSATION.md).
It proves that its coefficient four cannot be increased under the stated
endpoint-disjoint selected-union hypotheses, even if both far legs must
be arbitrarily long. No complete extension of this family is asserted;
sharpness among COMPLETE extensions is a different question.

## Construction and statement

For any m>=1 and even g>=4, take m+1 old H3 blocks with

    w_j=12, z_j=g+24, root breadth6,
    a_j=a_0+j(g+18), s_j=s_0-24j,

where a_0 is odd and s_0 even. At every internal index j=1,...,m,
select the complete original records

    R_j=U(32,10,g+2), chart(a_j-11+r,s_j+26-c),
    T_j=U(6,4,g), chart(a_j-8+r,s_j+1-c).

All chosen originals are endpoint-disjoint from the whole H3 chain and
each other. They satisfy the paired width relation with M=6,q=0.
Their exact NEW simultaneous counts are

    negative mass =6m,
    mixed full tiles =m(g/2+5),
    directed foreign events =m(g+12),
    DeltaPhi=4m.                                    (1)

Thus the lower bound holds with equality for every number of pairs and
without a far-length ceiling. This is a family of partial original
configurations, not a counterexample to global allocation or evidence
that every member has a complete feasible extension.

## General geometric proof

The columns and terminals in the both-far theorem are

    F_j=s_j-6, G_j=s_j-5,
    b_j=a_j+g-9, y_j=a_j+g-8=b_j+1.

Both lengths are even in their required domains. For every nonlast
selected block j the first old frontier is k=j+1, since

    F_j=s_(j+1)+18, G_j=s_(j+1)+19.

These are the P-bar frontier cases. The exact old bounds read
b_j<=a_(j+1)-9 and y_j<=a_(j+1)-10. Their right sides are
a_j+g+9 and a_j+g+8 respectively, so both inequalities hold with
strict slack. For the last block there is no later frontier. Hence
every R_j and T_j is endpoint-disjoint from all H3, and all old
deductions d_j,delta_j vanish.

Within a pair R's far column is one cell left of T's bar/far edge.
The bars begin at different rows and the short near columns are
separated. The two originals therefore have no common endpoint.
For ordered selected blocks i<j, pair i has maximum endpoint row

    max(a_i-1,a_i+g-8).

Pair j starts at row a_j-11>=a_i+g+7. Both terms in the earlier
maximum are strictly smaller: a_i-1<a_i+g+7 and
a_i+g-8<a_i+g+7. Thus their endpoint ROW intervals are disjoint;
the first later bar row is even, so their physical tile rows are
disjoint as well. This verifies every endpoint-disjointness hypothesis
of the simultaneous theorem directly, for all m,g.

For each pair q=0,b<y,d=delta=chi=0. There are g/2-1 mutual full
tiles and g mutual events, in addition to the six near full tiles
and twelve near events. Each pair contributes negative mass six and
no positive original. Distinct pairs have disjoint new receipt sets,
so the counts add exactly and give (1). Each source mass, physical
tile and labelled event is used once.

## Verification scope

The companion verifier invokes the full-original exact-set checker of
the both-far theorem, then independently checks the predicted linear
counts in (1). It covers varying m and g, including both far lengths
around2000. These controls supplement the all-parameter proof above.
The main theorem's scoped Lean result is unchanged; no separate full
formalization of this sharpness construction is claimed.

This corollary was written AFTER the independent review input780b9242
was submitted. That input covers the main both-far theorem and its
E-frontier dependency, not this additional sharpness construction.
