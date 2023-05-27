import numpy as np
from copy import deepcopy
from pip_data import *
from crossover import *
from mutation import *
from selection import *
from charles import Population, Individual


def get_fitness(self):
    """A simple objective function to calculate distances
    for the TSP problem.
    Returns:
        int: the total return minus the risk of the investment
    """
    # We only want to chosen one investment, we cannot choose the same investment several times, so we need to check the
    # cardinality of each individual, if there are any repeated investments, that individual has fitness risk - return.
    cardinality = cardinality_check(self)
    if cardinality < len(self.representation):
        fitness = (portfolio_risk(self) - portfolio_return(self))
    # We also need to check if the total investment required for this individual is higher than our budget
    total_investment = portfolio_investment(self)
    if budget < total_investment and budget is not None:
        fitness = (portfolio_risk(self) - portfolio_return(self))
    elif cardinality == len(self.representation):
        fitness = (portfolio_return(self) - portfolio_risk(self))
    return fitness


def portfolio_investment(self):
    sum_investment = 0
    for i in range(len(self.representation)):
        sum_investment += investments[self.representation[i]]
    return int(sum_investment)


def portfolio_return(self):
    sum_return = 0
    for i in range(len(self.representation)):
        sum_return += investments[self.representation[i]] + (investments[self.representation[i]] * returns[self.representation[i]])
    return int(sum_return)


def portfolio_risk(self):
    sum_risk = 0
    for i in range(len(self.representation)):
        sum_risk += risks[self.representation[i]]
    return int(sum_risk)


def portfolio_excess_return(self):
    variation = np.var(returns)
    return variation


def cardinality_check(self):
    '''Function to see if there are repeated investment in one individual'''
    cardinality = len(set(self.representation))
    return cardinality


# Monkey patching
Individual.get_fitness = get_fitness
