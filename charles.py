from random import choice, random
from operator import attrgetter
from copy import deepcopy
from pip_data import *


class Individual:
    def __init__(
            self,
            representation=None,
            size=None,
            replacement=True,
            valid_set=None,
    ):
        if representation is None:
            if replacement:
                self.representation = [choice(valid_set) for i in range(size)]
            elif not replacement:
                self.representation = sample(valid_set, size)
        else:
            self.representation = representation
        self.fitness = self.get_fitness()

    def get_fitness(self):
        raise Exception("You need to monkey patch the fitness path.")

    def get_neighbours(self, func, **kwargs):
        raise Exception("You need to monkey patch the neighbourhood function.")

    def index(self, value):
        return self.representation.index(value)

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f"Individual(size={len(self.representation)}); Fitness: {self.fitness}"


class Population:
    def __init__(self, size, optim, **kwargs):
        self.individuals = []
        self.size = size
        self.optim = optim
        for _ in range(size):
            self.individuals.append(
                Individual(
                    size=kwargs["sol_size"],
                    replacement=kwargs["replacement"],
                    valid_set=kwargs["valid_set"],
                )
            )

    def evolve(self, gens, xo_prob, mut_prob, select, mutate, crossover, elitism):
        # We decided to create a new variable that will store the best individual at each generation. This step was
        # implemented to help achieve the results faster in the graphical representations and final analysis.
        evolution = []
        # Repeat the evolution process for n generations
        for i in range(gens):
            new_pop = []

            # If True, perform elitism. Basically select the best individual from the population to go to next one
            # without going through any crossover or mutation. Here, we just select the best individual from the
            # current population, without transferring it to the new population automatically.
            if elitism:
                if self.optim == "max":
                    elite = deepcopy(max(self.individuals, key=attrgetter("fitness")))
                elif self.optim == "min":
                    elite = deepcopy(min(self.individuals, key=attrgetter("fitness")))

            # While the new population isn't complete, i.e., its size is still smaller than the size of the parent
            # population, we need to keep selecting individuals from current population to the nest one.
            while len(new_pop) < self.size:
                parent1, parent2 = select(self), select(self)

                # With a certain probability apply crossover to the selected parents
                if random() < xo_prob:
                    offspring1, offspring2 = crossover(parent1, parent2)
                else:
                    offspring1, offspring2 = parent1, parent2

                # With a certain probability apply mutation to the parents (originally selected or the ones obtained
                # after crossover)
                if random() < mut_prob:
                    offspring1 = mutate(offspring1)
                if random() < mut_prob:
                    offspring2 = mutate(offspring2)

                # Add to the new population the first parent
                new_pop.append(Individual(representation=offspring1))
                # If the size of the new population is still lower than the size of the initial population, we add the
                # second parent. The insertion of the parents is made in different steps because we can reach a phase
                # where only one individual is missing, and then we just need to add one parent.
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2))

            # If true, we will remove the worst individual from the new population if its fitness is worse than the
            # fitness of the best individual of the parents' population.
            if elitism:
                if self.optim == "max":
                    worst = min(new_pop, key=attrgetter("fitness"))
                    if elite.fitness > worst.fitness:
                        new_pop.pop(new_pop.index(worst))
                        new_pop.append(elite)

                elif self.optim == "min":
                    worst = max(new_pop, key=attrgetter("fitness"))
                    if elite.fitness < worst.fitness:
                        new_pop.pop(new_pop.index(worst))
                        new_pop.append(elite)

            # Finally, set the new population as the current population
            self.individuals = new_pop

            # This part is just for function outputs. There are a lot of commented rows because of the visualizations.
            # Since we used Population class to develop the visualization, we didn't want it to return outputs everytime
            # the class was run. If it is going to be used separately from the visualizations, please uncomment the rows
            if self.optim == "max":
                # final_individual = []
                # for i in self.individuals:
                # final_individual = i.representation
                # final_investment, final_return, final_risk = 0, 0, 0
                # for j in final_individual:
                # final_investment += investments[j]
                # final_return += investments[j] + (investments[j]*returns[j])
                # final_risk += risks[j]
                # print(f'Final investment: {final_investment},   Final return: {final_return},   Final risk: {final_risk}')
                # print(f'Best Individual: {max(self, key=attrgetter("fitness"))}')
                best_individual = max(self, key=attrgetter("fitness"))
            elif self.optim == "min":
                # final_individual = []
                # for i in self.individuals:
                # final_individual = i.representation
                # final_investment, final_return, final_risk = 0, 0, 0
                # for j in final_individual:
                # final_investment += investments[j]
                # final_return += investments[j] + (investments[j] * returns[j])
                # final_risk += risks[j]
                # print(f'Final investment: {final_investment},   Final return: {final_return},   Final risk: {final_risk}')
                # print(f'Best Individual: {min(self, key=attrgetter("fitness"))}')
                best_individual = min(self, key=attrgetter("fitness"))

            # Append to the variable created the best individual of each generation. Append generation number, fitness
            # value and the best individual
            evolution.append([i + 1, best_individual.fitness, best_individual.representation])

        return evolution

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]
