import itertools
from typing import List

import parsing
from parsing import Base


def brute_force(bases: List[Base], entreprises: List[str], n):
    bases = bases[:]
    entreprises = entreprises[:]
    valids = []
    for possibles in itertools.product(bases, repeat=n):
        cost = 0
        entreprise_temp = entreprises.copy()

        for possible in possibles:
            cost += possible.cost
            for entreprise in possible.liste:
                if entreprise in entreprise_temp:
                    entreprise_temp.remove(entreprise)

        if not entreprise_temp:
            valids.append((list(set([x.name for x in possibles])), cost))
    valids.sort(key=lambda x: x[1])

    return valids
