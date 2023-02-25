import matplotlib.pyplot as plt
import numpy as np

# Dummy data
weapons = ['Gun', 'Rifle', 'Knife', 'Grenade']
values = [20, 30, 15, 35]

# Create the figure and axis
fig, ax = plt.subplots(figsize=(8, 4))

# Plot the horizontal bars
ax.barh(weapons, values)

# Add the x-axis label
ax.set_xlabel('Amount activated')

# Add the y-axis label
ax.set_ylabel('Weapon')

# Add the title
ax.set_title('Weaponstats Total')

# Iterate through the bars to add the percentage and absolute values
for i, bar in enumerate(ax.containers):
    width = bar.width
    height = bar.height[0]

    # Calculate the percentage value
    percent = (width / sum(values)) * 100

    # Add the percentage value to the left of the bar
    ax.text(width, height, f'{percent:.1f}%', ha='left', va='center')

    # Add the absolute value to the right of the bar
    ax.text(width, height, f'{width:,}', ha='right', va='center')

plt.show()