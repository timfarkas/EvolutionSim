import numpy
import matplotlib.pyplot as plt

n=1000
runs = 100
generations = 10
j = 10
mutationBenefit = 0.05
p = j / n

def reproduce(i, n, s):
    p = i/n
    expectedP = (p*(1+s))/(p*(1+s)+(1-p))
    j = numpy.random.binomial(n, expectedP)
    return j
    
### takes initial mutants j, population size n, mutationbenefit s and no of generations
def simulate(initialJ, n, mutationBenefit, generations = 1000):
    simulation = [[],[]]
    j = initialJ
    for currentGen in range(0, generations):
        newJ = reproduce(j, n, mutationBenefit)
        print("Generation: "+str(currentGen)+" "+ str(j))
        j = newJ
        p = j/n
        simulation[0].append(currentGen)
        simulation[1].append(p)
        if p == 0 or p == 1:
            break
    return simulation
        
## runs several simulations and returns an array of all simulation histories
def runSimulations(initialJ, n, mutationBenefit, generations = 1000, runs = 100):
    simulations = []
    for run in range(0, runs):
        simulations.append(simulate(initialJ, n, mutationBenefit, generations))
    return simulations


simulations = runSimulations(100,1000,0.1)
for simulation in simulations:
    plt.plot(simulation[0],simulation[1])
plt.xlabel("Generations")
plt.ylabel("p")
plt.show()