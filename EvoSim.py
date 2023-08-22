import numpy
import matplotlib.pyplot as plt

def reproduce(i, n, s):
    p = i/n
    expectedP = (p*(1+s))/(p*(1+s)+(1-p))
    j = numpy.random.binomial(n, expectedP)
    return j

def reproduceGrowing(i, n, s):
    c = 1000    # Capacity of the system
    r = 0.1         # growth factor
    nNew = int((1+r)*n*(1-(r*n)/((1+r)*c)))                       # before bottleneck
    
    p = i/n
    expectedP = (p*(1+s))/(p*(1+s)+(1-p))
    j = numpy.random.binomial(n, expectedP)
    return j

### takes initial mutants j, population size n, mutationbenefit s and no of generations
def simulate(initialJ, n, mutationBenefit, generations = 1000, bottleneckTimestamp = 500, decimationFactor = 1, mode = None): #bottleneck variables added
    # saves initial population size for bottleneck
    nOld = n
    ## array simulation [currentGen, p, Bool fixation ]
    simulation = [[],[],0]
    j = initialJ
    for currentGen in range(0, generations):            
        ### modify mutationBenefit based on environmentalBenefitModifier to simulate environmental effects on mutationBenefit
        modS = mutationBenefit * environmentalBenefitModifier(currentGen,mutationBenefit,mode)
        if currentGen < bottleneckTimestamp-1:      # situation before bottleneck
            
            #newJ = reproduce(j, n, modS)           # constant population  
            newJ = reproduceGrowing(j, n, modS)     #growing population
            
            j = newJ  
        elif currentGen == bottleneckTimestamp-1:
            #print (decimationFactor)
            n = int(n* decimationFactor)                            # decimates population size
            j = numpy.random.binomial(n, p)                                 # calculates new j
            p = j/n
            #newJ = reproduce(j, n, modS)           # constant population  
            newJ = reproduceGrowing(j, n, modS)     #growing population
            
            j = newJ
        else:                                                       # regrowing population size
            #newJ = reproduce(j, n, modS)           # constant population  
            newJ = reproduceGrowing(j, n, modS)     #growing population
            
            #print("Generation: "+str(currentGen)+" "+ str(j))
            j = newJ
            
        p = j/n
        simulation[0].append(currentGen)
        simulation[1].append(p*n)
        if p == 0:
            simulation[2] = 0
            break
        if p == 1:
            simulation[2] = 1
            break
    return simulation
        
## runs several simulations and returns [[array of all simulation histories], float fixationProbability]
## initialJ is the number of initial mutants, n is population size
## bottleneckTimestamp is the time where a population bottleneck is simulated, reducing the population to decimation
def runSimulations(initialJ, n, mutationBenefit, generations = 1000, runs = 100, bottleneckTimestamp = 1100, decimation = 1, envMode = None):
    simulations = [[],0]
    for run in range(0, runs):
        simulation = simulate(initialJ, n, mutationBenefit, generations, bottleneckTimestamp, decimation, envMode)     # bottleneck variables added
        simulations[0].append(simulation)
        simulations[1] = simulations[1] + simulation[2] 
    fixationProb = simulations[1]/simulations[0].__len__()
    simulations[1] = fixationProb
    return simulations

### takes current generation, unmodified selection coefficient and environment mode and returns modified selection coefficient
def environmentalBenefitModifier(gen, s, mode):
    if mode == None:
        return 1
    if mode.lower() == "seasons":
        return sinusModifier(gen, s, 25, 2)
    else:
        return 1 
#else if mode == "random":



### takes current generation, unmodified selection coefficient and environment mode and returns modified selection coefficient modulated by periodic fluctuations of specified amplitude with a given period 
def sinusModifier(gen, s, period, amplitude):
	modS = s * numpy.sin((1/period)*gen) * amplitude
	return modS

### vanilla
simulations = runSimulations(50,1000,0.02, 1000, 100,1100,1)
for simulation in simulations[0][::3]:
    plt.plot(simulation[0],simulation[1],color="green")
plt.xlabel("Generations")
plt.ylabel("p")
vanillaFixation = str(simulations[1])

### seasonalVariation
simulations = runSimulations(50,1000,0.02, 1000, 100,1100,1,"Seasons")
for simulation in simulations[0][::3]:
    plt.plot(simulation[0],simulation[1],color="blue")
plt.xlabel("Generations")
plt.ylabel("p")
seasonalVariationFixation = str(simulations[1])

### bottleneck
bottleneckTimestamp = 100
simulations = runSimulations(50, 1000, 0.02, 1000, 100,bottleneckTimestamp,0.1)
for simulation in simulations[0][::3]:
    plt.plot(simulation[0],simulation[1],color="red")
plt.xlabel("Generations")
plt.axvline(x = bottleneckTimestamp,color = 'r',linestyle='--')
plt.ylabel("p")
plt.title("Fixation probability: "+ str(simulations[1]))

bottleneckFixation = str(simulations[1])

plt.title("P(fixation): \n"+"Vanilla: "+ vanillaFixation + "\nSeasons: "+ seasonalVariationFixation + "\nBottleneck: "+bottleneckFixation)
plt.show()

