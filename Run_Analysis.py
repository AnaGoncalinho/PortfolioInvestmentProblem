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

target_graph = []
for i in range(len(investments)):
    target = (investments[i], returns[i], risks[i])
    target_graph.append(target)

methods = {
    'selection': [tournament_sel, fps, ranking_sel],
    'crossover': [single_point_co, cycle_xo, arithmetic_xo],
    'mutation': [swap_mutation, inversion_mutation, scramble_mutation],
    'elitism': [True, False]
}

# Create a dataframe to contain the following columns: iteration, generation, fitness and representation
metrics_df = pd.DataFrame(columns=[
  'iteration',
  'generation',
  'fitness',
  'representation',
  'config',
])


for s in methods['selection']:
    for c in methods['crossover']:
        for m in methods['mutation']:
            for e in methods['elitism']:
                configuration = f"{s.__name__}, {c.__name__}, {m.__name__}, elitism {e}"
                for iteration_number in range(100):
                    pop = Population(
                        size=50,
                        sol_size=10,
                        valid_set=[i for i in range(len(returns))],
                        replacement=False,
                        optim="max")

                    evolution = pop.evolve(gens=50, select=ranking_sel, mutate=swap_mutation, crossover=single_point_co,
                                           mut_prob=0.05, xo_prob=0.9, elitism=True)

                    # Convert evolution to a dataframe
                    evolution = pd.DataFrame(evolution,columns=['generation', 'fitness', 'representation']).assign(
                        iteration=iteration_number, config=configuration).loc[:, ['iteration', 'generation', 'fitness',
                                                                                  'representation', 'config']]

                    # Append evolution_log_df to iterated_evolution_log_df
                    metrics_df = pd.concat([metrics_df, evolution], axis=0, ignore_index=True)


# Save iterated_evolution_log_df to a csv file, so we don't have
# to re-run the GA every time
metrics_df.to_csv('metrics.csv', index=False)


