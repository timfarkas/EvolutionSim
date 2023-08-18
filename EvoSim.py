import numpy
import matplotlib.pyplot as plt

n=1000
runs = 100
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
    ## array simulation [currentGen, p, Bool fixation ]
    simulation = [[],[],None]
    j = initialJ
    for currentGen in range(0, generations):
        newJ = reproduce(j, n, mutationBenefit)
        #print("Generation: "+str(currentGen)+" "+ str(j))
        j = newJ
        p = j/n
        simulation[0].append(currentGen)
        simulation[1].append(p)
        if p == 0:
            simulation[2] = 0
            break
        if p == 1:
            simulation[2] = 1
            break
    return simulation
        
## runs several simulations and returns [[array of all simulation histories], float fixationProbability]
## initialJ is the number of initial mutants, n is population size
def runSimulations(initialJ, n, mutationBenefit, generations = 1000, runs = 100):
    simulations = [[],0]
    for run in range(0, runs):
        simulation = simulate(initialJ, n, mutationBenefit, generations)
        simulations[0].append(simulation)
        simulations[1] = simulations[1] + simulation[2] 
    fixationProb = simulations[1]/simulations[0].__len__()
    simulations[1] = fixationProb
    return simulations


simulations = runSimulations(50,1000,0.02, 1000, 100)
for simulation in simulations[0]:
    plt.plot(simulation[0],simulation[1])
plt.xlabel("Generations")
plt.ylabel("p")
plt.title("Fixation probability: "+ str(simulations[1]))
plt.show()

