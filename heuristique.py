import math
from typing import Union

from parsing import Base


def heuristique_ratio(base: Base, ens_entreprise: list) -> float:
    nb_base = 0
    for entreprise in ens_entreprise:
        if entreprise in base.liste:
            nb_base += 1

    return (base.cost / nb_base) if nb_base != 0 else math.inf


def heuristique_ratio_log(base: Base, ens_entreprise: list) -> float:
    nb_base = 0
    for entreprise in ens_entreprise:
        if entreprise in base.liste:
            nb_base += 1
    return (math.log(base.cost) / nb_base) if nb_base != 0 else math.inf


def heuristique_low_cost(base: Base, ens_entreprise: list) -> float:
    return base.cost


def heuristique_big_cover(base: Base, ens_entreprise: list) -> float:
    nb_base = 0
    for entreprise in ens_entreprise:
        if entreprise in base.liste:
            nb_base += 1
    return nb_base * -1

