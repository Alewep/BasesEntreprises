import math

import brute_force
import glouton
import heuristique
from branch_and_bound import branch_and_bound
from parsing import all_bases, liste

import time

start = time.time()

entreprises = liste("Data/Scénarios/Liste Entreprises/Liste Ent1.txt")
bases = all_bases("Data/Scénarios/Liste Bases/Liste Bases1.txt", "Data/Bases")

# print(entreprises)
print(glouton.glouton(bases, entreprises, heuristique.heuristique_ratio))

#print(branch_and_bound(bases, entreprises, heuristique.heuristique_big_cover, best=None, sort_heuristique=False))
# print(brute_force.brute_force(bases, entreprises, 4)[0])

end = time.time()

print(end - start)
