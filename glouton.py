from typing import List, Tuple, Callable, Any
from parsing import Base


def glouton(all_bases: List[Base], entreprises: List[str], heuristique: Callable[[Base, List[str]], Any]) :
    all_bases = all_bases[:]
    entreprises = entreprises[:]

    resultat = []
    total_cost = 0
    iteration = 0

    while entreprises:
        iteration += 1
        all_bases.sort(key=lambda x: heuristique(x, entreprises))
        first = min(all_bases, key=lambda x: heuristique(x, entreprises))
        all_bases.remove(first)
        for entreprise in first.liste:
            if entreprise in entreprises:
                entreprises.remove(entreprise)
        resultat.append(first)
        total_cost += first.cost

    return resultat, total_cost,iteration
