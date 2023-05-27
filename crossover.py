from random import randint, sample, uniform


def single_point_co(parent1, parent2):
    """Implementation of single point crossover.
    Args:
        parent1 (Individual): First parent for crossover.
        parent2 (Individual): Second parent for crossover.
    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    co_point = randint(1, len(parent1) - 2)
    offspring1 = parent1[:co_point] + parent2[co_point:]
    offspring2 = parent2[:co_point] + parent1[co_point:]
    return offspring1, offspring2


def arithmetic_xo(parent1, parent2):
    """Implementation of arithmetic crossover/geometric crossover with constant alpha.

    Args:
        parent1 (Individual): First parent for crossover.
        parent2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    alpha = uniform(0, 1)
    offspring1 = [None] * len(parent1)
    offspring2 = [None] * len(parent1)
    for i in range(len(parent1)):
        offspring1[i] = int(parent1[i] * alpha + (1 - alpha) * parent2[i])
        offspring2[i] = int(parent2[i] * alpha + (1 - alpha) * parent1[i])
    return offspring1, offspring2


def cycle_xo(parent1, parent2):
    """Implementation of cycle crossover.
        Args:
            parent1 (Individual): First parent for crossover.
            parent2 (Individual): Second parent for crossover.
        Returns:
            Individuals: Two offspring, resulting from the crossover.
        """
    # offspring placeholders
    offspring1 = [[] for _ in range(len(parent1))]
    offspring2 = [[] for _ in range(len(parent1))]
    # Set index randomly with the length of one parent. We want to create a new array with random indexes
    offspring1_index = sample(range(len(parent1)), len(parent1))
    offspring2_index = sample(range(len(parent1)), len(parent1))
    index_off = 0
    val_inside1 = offspring1_index[index_off]
    val_inside2 = offspring2_index[index_off]
    val1_initial = 60
    count = 0
    # copy the cycle elements
    while val_inside1 != val1_initial and count < len(offspring1_index):
        # assign of the parents to the offsprings
        offspring1[index_off] = parent2[index_off]
        offspring2[index_off] = parent1[index_off]
        # index of the val2 in the offspring1
        index_off = offspring1_index.index(val_inside2)
        count = count + 1
        # new values for the inside
        val_inside1 = offspring1_index[index_off]
        val_inside2 = offspring2_index[index_off]
    # assign the corresponding parent return
    for index, element in enumerate(offspring1):
        if not element:
            offspring1[index] = parent1[index]
            offspring2[index] = parent2[index]
    return offspring1, offspring2
