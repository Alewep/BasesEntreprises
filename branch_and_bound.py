import math
from typing import List, Union, Callable, Any

import heuristique
from glouton import glouton
from parsing import Base


class Node:
    def __init__(self, solution: List[Base] = []):
        self.solution = solution

    def bound(self):
        cost = 0
        for base in self.solution:
            cost += base.cost
        return cost

    def get_sons(self, bases: List[Base], entreprises: List[str]) -> Union[List[Any], None]:
        node_list = []
        rest_bases = list(set(bases).difference(set(self.solution)))

        entreprises_selected = []
        for base in self.solution:
            entreprises_selected += base.liste

        rest_entreprises = list(set(entreprises).difference(set(entreprises_selected)))

        if not rest_entreprises:
            return None

        for base in rest_bases:
            for entreprise in rest_entreprises:
                if entreprise in base.liste:
                    new_son = Node(self.solution + [base])
                    node_list.append(new_son)
                    break
        return node_list


def branch_and_bound(bases: List[Base], entreprises: List[str], heuristique: Callable[[Base, List[str]], Any],
                     best=0,sort_heuristique=True):
    best_node = None
    if best is not None:
        best = glouton(bases, entreprises, heuristique)[1]
    else :
        best = math.inf

    root = Node()
    solutions = [root]
    iteration = 0
    while solutions:
        iteration += 1
        current_node = solutions.pop(0)
        bound = current_node.bound()
        if bound <= best:
            sons = current_node.get_sons(bases, entreprises)

            if sons:
                if sort_heuristique :
                    sons.sort(key=lambda n: heuristique(n.solution[-1], entreprises))
                solutions = solutions + sons
            else:
                best_node = current_node
                best = bound

    return best_node.solution, best, iteration
