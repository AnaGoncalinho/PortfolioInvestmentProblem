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
    elif cardinality == len(self.representation) and budget >= total_investment:
        fitness = (portfolio_return(self) - portfolio_risk(self))
    return fitness


# This function was created to compute the investment amount of an individual
def portfolio_investment(self):
    sum_investment = 0
    for i in range(len(self.representation)):
        sum_investment += investments[self.representation[i]]
    return int(sum_investment)


# This function was created to compute the return of the investment amount of an individual
def portfolio_return(self):
    sum_return = 0
    for i in range(len(self.representation)):
        sum_return += investments[self.representation[i]] + (
                    investments[self.representation[i]] * returns[self.representation[i]])
    return int(sum_return)


# This function was created to compute the risk of investment of an individual
def portfolio_risk(self):
    sum_risk = 0
    for i in range(len(self.representation)):
        sum_risk += risks[self.representation[i]]
    return int(sum_risk)


# This function was created to check the cardinality of an individual, basically to check if there were any repeated
# investments within an individual
def cardinality_check(self):
    cardinality = len(set(self.representation))
    return cardinality


# Monkey patching
Individual.get_fitness = get_fitness
