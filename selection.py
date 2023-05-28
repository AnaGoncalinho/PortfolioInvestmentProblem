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
