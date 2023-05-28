import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
import numpy as np

metrics = pd.read_csv('metrics.csv')

# First we want to check the average best fitness value found for each of the configurations used
print(tabulate(metrics.query('generation == 50').groupby('config').agg({'fitness': 'mean'}).sort_values('fitness'), headers='keys'))

# Then we are going to compare, for each of the configurations, the maximum fitness for each generation. Since each
# configuration was run 100 times, we need to compute the mean for all the generations
plot = metrics.groupby(['config', 'generation']).agg({'fitness': 'mean'}).reset_index()

# Set figure size, just to ensure that the results are visible and understandable, that is not too small.
fig, ax = plt.subplots(figsize=(12, 10))

# Define the axis, in x we have the generation and in the y we have the fitness. The data used is the one created to
# show the mean per generation per configuration.
sns.lineplot(x='generation', y='fitness', data=plot, hue='config')

# Set title and labels
plt.title('Evolution of fitness over generations', fontsize=20)
ax.set_ylabel('Mean Fitness')
ax.set_xlabel('Generation')

# The legend show be outside the plot, so we can see everything that is being represented
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 5), ncol=1).set_title('Configuration')

# Finally, plot the graph
plt.show()

# Now we will look for the statistical significance of the results. We choose only the last generation, so we have the
# best individual of all. We will show a graph with representations similar to boxplot, but more one example given
# during theoretical classes
plot2 = metrics.query('generation == 50').groupby(['config', 'generation']).agg({'fitness': ['mean', 'std']}).\
    droplevel(0, axis=1).assign(ci_lower=lambda x: x['mean'] - 1.96 * x['std']/np.sqrt(x.shape[0]),
                                ci_upper=lambda x: x['mean'] + 1.96 * x['std']/np.sqrt(x.shape[0])).\
    reset_index().sort_values('mean')

# Set figure size, just to ensure that the results are visible and understandable, that is not too small.
fig, ax = plt.subplots(figsize=(12, 10))

# The plot2 will show the range, while this new plot will place dots is the place of the mean
sns.scatterplot(data=plot2, x='mean', y='config')

# Confidence intervals, for every configuration we need to compute the lower and upper quantile so they appear in the
# plot
for lower, upper, y in zip(plot2['ci_lower'], plot2['ci_upper'], range(plot2.shape[0])):
    plt.plot((lower, upper), (y, y), 'r-')
    plt.plot((lower, lower), (y-0.2, y+0.2))
    plt.plot((upper, upper), (y-0.2, y+0.2))

# Set title and labels
plt.title('Comparison of fitness of best individual in each configuration', fontsize=20)
plt.xlabel('Fitness')
plt.ylabel('Configuration')

fig = plt.figure()
fig.subplots_adjust(left=-20, right=30)

# Finally, plot the graph
plt.show()
