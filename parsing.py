import os
from typing import List


class Base:
    def __init__(self, name: str, cost: int, liste: List[str]):
        self.name = name
        self.cost = cost
        self.liste = liste

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name


# prend un nom d'un fichier sous forme de liste
# et retourne sous forme de liste python
def liste(liste_name: str) -> List[str]:
    resp = []
    with open(liste_name) as liste:
        nb_line = int(liste.readline())
        for i in range(nb_line):
            resp.append(liste.readline()[:-1])

    return resp


# Prend le nom d'un fichier en paramètre qui est une liste d'information avec cout d'acces
# retroune un objet Bases correspondant
def base(base_name: str) -> Base:
    cost = 0
    liste = []
    with open(base_name) as base:
        cost = int(base.readline())
        nb_line = int(base.readline())
        for i in range(nb_line):
            liste.append(base.readline()[:-1])

    return Base(os.path.basename(base_name), cost, liste)


# Prend le nom d'un fichier en paramètre qui est une liste de nom de bases
# et retourne l'ensemble des bases associé
def all_bases(liste_name: str, folder_base: str) -> List[Base]:
    ens = []
    liste_name_bases = liste(liste_name)
    for base_name in liste_name_bases:
        ens.append(base(folder_base + "/" + base_name))
    return ens
