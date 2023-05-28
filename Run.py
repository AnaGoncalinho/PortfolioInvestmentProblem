import numpy as np
from copy import deepcopy
from pip_data import *
from crossover import *
from mutation import *
from selection import *
from charles import Population, Individual
from pip import *

# Create a population, with size 50, solutions should have size 10, with values between 0 and 49 (indexes of investments
# data), without replacement and as a maximization problem.
pop = Population(
    size=50,
    sol_size=10,
    valid_set=[i for i in range(len(returns))],
    replacement=False,
    optim="max")

# Then, use the function evolve to perform the Genetic Algorithm
pop.evolve(gens=50, select=ranking_sel, mutate=swap_mutation, crossover=single_point_co, mut_prob=0.05, xo_prob=0.9,
           elitism=True)
