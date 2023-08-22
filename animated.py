import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation  

# function to simulate genetic drift using the Wright-Fisher model
def simulate_wright_fisher(population_size, initial_allele_count, generations):
    allele_counts = [] # number of alleles in each gen 
    current_count = initial_allele_count
    
    for i in range(generations):
        current_count = int(np.random.binomial(population_size, current_count / population_size, 1))
        allele_counts.append(current_count)
    
    return allele_counts

# can be changed: 
population_size = 1000
prob = 0.01
generations = 100
simul_number = 10


initial_allele_count = population_size * prob 

simulations = [] # stores allele count arrays 
for j in range(simul_number): 
    allele_counts = simulate_wright_fisher(population_size, initial_allele_count, generations)
    simulations.append(allele_counts)


# plot simulation results
x = []
y = [] # is going to become a list of arrays 
for j in range(simul_number): 
    new_array = []
    y.append(new_array)

fig, ax = plt.subplots()
ax.set_title('Wright-Fisher Model for Genetic Drift')
ax.set_xlabel('generation')
ax.set_ylabel('allele frequencies')
green_colors = plt.cm.get_cmap('Greens', simul_number)


# function that draws each frame of the animation 
def animate(i): 
    x.append(i)
    for j in range(simul_number): 
        y[j].append(simulations[j][i])

    ax.clear()
    for j in range(simul_number): 
        ax.plot(x, y[j], color=green_colors(j))
    ax.set_title('Wright-Fisher Model for Genetic Drift')
    ax.set_xlabel('generation')
    ax.set_ylabel('allele frequencies') 
    ax.set_xlim([0,generations])
    ax.set_ylim([0,population_size])

ani = FuncAnimation(fig, animate, frames=generations, interval=10, repeat=False)
plt.show()