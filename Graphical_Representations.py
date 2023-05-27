import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

metrics = pd.read_csv('metrics.csv')

print(tabulate(metrics.query('generation == 50').groupby('config').agg({'fitness': 'mean'}).sort_values('fitness'), headers='keys'))

plot = metrics.groupby(['config','generation']).agg({'fitness': 'mean'}).reset_index()

fig, ax = plt.subplots(figsize=(12, 10))
sns.lineplot(
    x='generation',
    y='fitness',
    data=plot,
    hue='config'
)

# Titles and labels
plt.title('Evolution of mean fitness over generations', fontsize=15, y=1.03)
ax.set_ylabel('Mean fitness')
ax.set_xlabel('Generation')

# Place legend on the bottom of the plot
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 5), ncol=1).set_title('Configuration')

plt.show()
