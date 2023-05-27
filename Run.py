import numpy as np
from copy import deepcopy
from pip_data import *
from crossover import *
from mutation import *
from selection import *
from charles import Population, Individual
from pip import *


pop = Population(
    size=50,
    sol_size=10,
    valid_set=[i for i in range(len(returns))],
    replacement=False,
    optim="max")

pop.evolve(gens=50, select=ranking_sel, mutate=swap_mutation, crossover=single_point_co,
           mut_prob=0.05, xo_prob=0.9, elitism=True)
