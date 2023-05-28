from random import sample, randint, uniform

investments = sample(range(0, 1500), 50)

returns = []
for i in range(50):
    number = uniform(0, 1)
    returns.append(round(number))


risks = []
for i in range(50):
    risks.append(randint(0, 10))

budget = 10000

