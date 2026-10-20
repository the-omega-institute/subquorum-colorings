# An explicit residual-coverage criterion for coefficient one

21 October 2026. This is a deduction from the new
[persistent corridor theorem](PERSISTENT_CORRIDOR_AND_STRIP_CAPACITY.md)
and the established joint S/P/R activation injection. The full unrestricted
allocation and rectangular-grid equality remain OPEN.

Consider any complete original U/rotor family. Let q count marked sides
whose actual canonical gate consumer is positive or rotor. The established
joint injection gives q<=A, where A counts actual activated positive
terminal occurrences. Every remaining gate consumer is a negative U.

Select c of those negative-consumer marked sides whose horizontal full-bar
route has the protected cap certificate. Assign each its actual cap. The
cap reconstruction in the corridor theorem makes this assignment injective.
Let t be the number of remaining negative-U marked sides. Thus

    G=q+c+t,  G<=2N.

Count distinct strip owners and physical lower pairs as in the corridor
theorem; call their counts u and p. They may include additional certified
capacities not assigned to the c selected sides. Retain the established
number m8 of disjoint persistent receipts. The corridor reserve floor gives

    2R>=A+m8+c+2u+2p.

The fact that only c selected cap units appear is deliberate: any additional
cap capacity is discarded, never counted twice. Consequently

    2mu=2N+2R-2G
        >=2N-q-c-2t+m8+2u+2p
        >=m8-t+2u+2p,

where the first inequality uses q<=A and the second uses
q+c+t=G<=2N. Integer rounding yields the explicit result

    mu>=p+u+ceil((m8-t)/2).                           (1)

In particular

    t<=2(p+u)+m8+1                                   (2)

is sufficient for mu>=0: the displayed lower bound on 2mu is then at
least minus one, and 2mu is an even integer. No second copy of A, an
original negative charge, or reserve from a separate component enters
this argument. The u strips are counted once per original owner, including
when both corners certify different marked sides.

If each counted strip owner has at least one selected cap, then u>=c
because each owner has at most two selected cap claims and at least two
upper pairs. Taking p=m8=0 gives the convenient weaker sufficient condition
t<=2c+1. For c=0 this recovers the established at-most-one-negative-consumer
condition; certified strips enlarge the permitted uncovered residual.
The sharper condition (2) also uses extra width, lower pairs, and m8.

For the complete I/J/K family of the corridor note, I has two uncovered
negative gates and no corridor strip, so (2) does not establish allocation
for I. In J and K both marked gates have certified caps, t=0, and their
shared upper strip has u=d/2-1. If g=4, J also has p=d/2-1; (1) is exact:
mu(J)>=d-2, equal to the calculated margin. At g>=6, J and K have p=0
from this certificate library and the weaker floor mu>=d/2-1. This is a
coverage distinction, not a failure of the target in I or a claim of
sharpness for the taller chambers.

Whenever (2) holds, the established sigma>=mu bound proves
|T|+|M|<=mn/2 on the stated complete-source configurations. This improves
the previous 5/6 matching coefficient by |M|/6 on those configurations.
Universal coverage of (2) and a decomposition of arbitrary grid extremizers
into the required complete sources remain unproved.

The final two declarations in
formal/SubQuorum/PersistentCorridorCapacity.lean prove the integer implication
(1)-(2) with explicit mark-partition, activation-injection and reserve-floor
hypotheses. The physical adapters remain the written theorems cited above.
The original corridor review request preceded this corollary and terminated
with a broker browser failure, not a mathematical response. A fresh independent
request includes BOTH notes; its separate receipt tracks the actual outcome.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
