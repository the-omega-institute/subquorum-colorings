# A small-order obstruction for positive cubic selected-star gaps

Graphs are finite and simple. Suppose G is cubic and bipartite, and S is
an inclusion-minimal two-star-forming set inducing only stars, single edges
and isolates. Write d=|S|-beta_2(G), with unrestricted dissociation number.

**Proposition.** If d>0 then |V(G)|>=26.

This is an integer boundary consequence of the established two-colour
repair inequalities. It is not a new asymptotic coefficient, an exclusion
of every n=24d equality case, or a positive cubic example.

## Fixed witness counts and the established premises

Use one fixed permitted assignment from
[the two-colour repair theorem](SUBCUBIC_TWO_COLOUR_REPAIR_BOUND.md).
There are c selected star centres, e=2c+s selected leaves, m selected
vertices in edge components, and selected isolates. Thus m is even.
Among the centres q have no leaf with a private outside witness; each
such centre has one extra direct witness. The leaf and extra direct
witnesses form W. Let a,b2,b3 count selected isolates touching respectively
one, two and three chosen witnesses; z0 counts those touching none.
Put t=a+b2+b3 and u=|V(G) minus (S union W)|.
The matching number of the centre--h=2-helper repair graph is mu.
All these quantities, including s and mu, are nonnegative integers.

The established inequalities and cubic identity are

    J=c+s+2q-a-2b2-3b3 >=0,
    R=c-q+b2+b3-mu >=2d,
    T'=a+b2+b3-s-q >=2d,
    D=q+s+2mu-2b2 >=0,
    K=c+s+b2+b3 >=3d,
    B=c-q+t+m+z0-u >=2d,
    F0=3u-2c+s-3t+3q-2m-3z0 >=0,
    n=2J+4T'+2K+5B+2F0+2b3+2z0.

Their graph-theoretic proofs are supplied in that theorem. The last identity
implies n>=24d without a connectivity assumption.

## The integer boundary argument

If n<=24 and d>0, the last bound forces d=1 and n=24.
Every term in its nonnegative slack decomposition must be tight:

    J=F0=b3=z0=0, T'=2, K=3, B=2.

Put b=b2. The equations J=0,T'=2,K=3 give

    c=2+b-q, s=1-2b+q, a=2+s+q-b.

The inequalities R>=2 and D>=0 now imply, respectively,

    mu<=2b-2q,       mu>=2b-q-1/2.

Combining them gives q<=1/2, hence q=0 by integrality.
Since s=1-2b>=0 and b is an integer, b=0. Consequently

    c=2, s=1, a=3, mu=0, t=3.

The equation B=2 then gives u=m+3, while F0=0 gives
3u=12+2m. Substitution forces m=3, contrary to the even number of
selected vertices in edge components. Thus n<=24 is impossible.
A cubic bipartite graph has equally many vertices in each bipartition
class (count edges as three times either class size), so its order is
even. Therefore n>=26.

Only the published ledger, its equality consequences and the parity of
actual selected edge components were used. No finite search or negative
sample is a proof premise.
