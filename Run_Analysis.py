from charles import Individual, Population
from pip import get_fitness
from selection import *
from crossover import *
from mutation import *
from pip_data import *
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import product

# Create a variable to store the different methods and operator applied
methods = {
    'selection': [tournament_sel, fps, ranking_sel],
    'crossover': [single_point_co, cycle_xo, arithmetic_xo],
    'mutation': [swap_mutation, inversion_mutation, scramble_mutation],
    'elitism': [True, False]
}

# Create a dataframe to contain the following columns: iteration, generation, fitness, representation and configuration
metrics_df = pd.DataFrame(columns=[
  'iteration',
  'generation',
  'fitness',
  'representation',
  'config',
])

# For all of the possible configurations, run the population evolve function 100 times
for s in methods['selection']:
    for c in methods['crossover']:
        for m in methods['mutation']:
            for e in methods['elitism']:
                # Store configuration name as the concatenation of selection method, crossover and mutation operators,
                # with elitism names
                configuration = f"{s.__name__}, {c.__name__}, {m.__name__}, elitism {e}"
                for iteration_number in range(100):
                    pop = Population(
                        size=50,
                        sol_size=10,
                        valid_set=[i for i in range(len(returns))],
                        replacement=False,
                        optim="max")

                    # Store the values in evolution variables
                    evolution = pop.evolve(gens=50, select=ranking_sel, mutate=swap_mutation, crossover=single_point_co,
                                           mut_prob=0.05, xo_prob=0.9, elitism=True)

                    # Convert evolution to a dataframe
                    evolution = pd.DataFrame(evolution,columns=['generation', 'fitness', 'representation']).assign(
                        iteration=iteration_number, config=configuration).loc[:, ['iteration', 'generation', 'fitness',
                                                                                  'representation', 'config']]

                    # Append evolution_log_df to metrics dataframe
                    metrics_df = pd.concat([metrics_df, evolution], axis=0, ignore_index=True)


# We decided to safe the dataframe with final solutions to each configuration is a csv for future access. Every time
# we need to rerun the plots, we don't need to run this code also, what can take some time.
metrics_df.to_csv('metrics.csv', index=False)
