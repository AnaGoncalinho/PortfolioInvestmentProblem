from random import uniform, choice
from operator import attrgetter


def fps(population):
    """Fitness proportionate selection implementation.
    Args:
        population (Population): The population we want to select from.
    Returns:
        Individual: selected individual.
    """
    if population.optim == "max":
        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual
    elif population.optim == "min":
        # Sum total 1/fitness for min
        total_fitness = sum([1/i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += 1/individual.fitness
            if position > spin:
                return individual
    else:
        raise Exception("No optimization specified (min or max).")


def tournament_sel(population, size=4):
    """Tournament selection implementation.
    Args:
        population (Population): The population we want to select from.
        size (int): Size of the tournament.
    Returns:
        Individual: The best individual in the tournament.
    """
    # Select individuals based on tournament size
    # with choice, there is a possibility of repetition in the choices,
    # so every individual has a chance of getting selected
    tournament = [choice(population.individuals) for _ in range(size)]
    # with sample, there is no repetition of choices
    # tournament = sample(population.individuals, size)
    if population.optim == "max":
        return max(tournament, key=attrgetter("fitness"))
    elif population.optim == "min":
        return min(tournament, key=attrgetter("fitness"))
    else:
        raise Exception('No optimization specified')


def ranking_sel(population):
    """Ranking selection implementation.
        Args:
            population (Population): The population we want to select from.
        Returns:
            Individual: Select an individual.
        """
    # Sort individuals based on optimization approach
    if population.optim == 'max':
        population.individuals.sort(key=attrgetter('fitness'))
    elif population.optim == 'min':
        population.individuals.sort(key=attrgetter('fitness'), reverse=True)
    else:
        raise Exception('No optimization specified')
    # Sum ranks
    total = sum(range(population.size+1))
    # Get a random position
    spin = uniform(0, total)
    position = 0
    # Iterate until the spin is found
    for count, individual in enumerate(population):
        position += count + 1
        if position > spin:
            return individual


def stochastic_sel(population):
    """Stochastic Universal Sampling implementation.
    Requires: population we want to select from.
    Ensures: selected individualS (both 2, chosen at once)
    """
    if population.optim == "max":
        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # define interval btw pointers according to pop size
        pointer_interval = total_fitness / 2  # coz we want to select 2 individuals
        # Get both 'positions' on the wheel
        spin1 = uniform(0, total_fitness)
        if spin1 > pointer_interval:
            spin2 = spin1 - pointer_interval
        else:
            spin2 = spin1 + pointer_interval
        # initiates list to store selected individuals
        individuals_stochastic = []
        position = 0
        i = 0
        for individual in population:
            # finds individuals
            position += individual.fitness
            if (position > spin1 or position > spin2) and len(individuals_stochastic) == 0:
                individuals_stochastic.append(i)
            if position > spin1 and position > spin2:
                individuals_stochastic.append(i)
            if len(individuals_stochastic) == 2:
                break
            i += 1
        return individuals_stochastic
    elif population.optim == "min_errors" or population.optim == "min_45sum" or population.optim == "min_factorial":
        # Sum total fitness
        total_fitness = sum([1 / i.fitness for i in population])
        # define interval btw pointers according to pop size
        pointer_interval = total_fitness / 2  # coz we want to select 2 individuals
        # Get both 'positions' on the wheel
        spin1 = uniform(0, total_fitness)
        if spin1 > pointer_interval:
            spin2 = spin1 - pointer_interval
        else:
            spin2 = spin1 + pointer_interval
        # initiates list to store selected individuals
        individuals_stochastic = []
        position = 0
        i = 0
        for individual in population:
            # finds individuals
            position += 1 / individual.fitness
            if (position > spin1 or position > spin2) and len(individuals_stochastic) == 0:
                individuals_stochastic.append(i)
            if position > spin1 and position > spin2:
                individuals_stochastic.append(i)
            if len(individuals_stochastic) == 2:
                break
            i += 1
        return individuals_stochastic
    else:
        raise Exception("No optimization specified (min or max).")
