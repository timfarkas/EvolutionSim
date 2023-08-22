import numpy
import matplotlib.pyplot as plt

def reproduce(i, n, s):
    p = i/n
    expectedP = (p*(1+s))/(p*(1+s)+(1-p))
    j = numpy.random.binomial(n, expectedP)
    return j

#### takes population and proportion of mutants and outputs new proportion of mutants new population [j,n] based on growth factor r
def reproduceGrowing(i, n, s, r=0.1):
    c = 1000    # Capacity of the system
    n = int((1+r)*n*(1-(r*n)/((1+r)*c)))                       # before bottleneck
    
    p = i/n
    expectedP = (p*(1+s))/(p*(1+s)+(1-p))
    j = numpy.random.binomial(n, expectedP)
    return [j,n]

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
            array = reproduceGrowing(j, n, modS)     #growing population
            j = array[0] 
            n = array[1]  
        elif currentGen == bottleneckTimestamp-1:
            #print (decimationFactor)
            nDecimated = int(n* decimationFactor)                            # decimates population size
            j = numpy.random.binomial(nDecimated, p)                                 # calculates new j
            p = j/nDecimated
            #newJ = reproduce(j, nDecimated, modS)           # constant population  
            array = reproduceGrowing(j, nDecimated, modS)     #growing population
            j = array[0] 
            n = array[1]
        else:                                                       # regrowing population size
            #newJ = reproduce(j, n, modS)           # constant population  
            array = reproduceGrowing(j, n, modS)     #growing population
            #print("Generation: "+str(currentGen)+" "+ str(j))
            j = array[0] 
            n = array[1]

        p = j/n
        simulation[0].append(currentGen)
        simulation[1].append(p*n)
        if p == 0:
            simulation[2] = 0
            break
        if p == 1:
            #print("BREAK, n ="+str(n))
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
        modS = numpy.abs(sinusModifier(gen, s, 25, 2))
        return modS
    else:
        return 1 
#else if mode == "random":



### takes current generation, unmodified selection coefficient and environment mode and returns modified selection coefficient modulated by periodic fluctuations of specified amplitude with a given period 
def sinusModifier(gen, s, period, amplitude):
	modS = s * numpy.sin((1/period)*gen) * amplitude
	return modS


# SIMULATIONS
initialMutants = 10
population = 1000
fitnessBenefit = 0.02
maxGenerations = 1000
runs = 200

### vanilla
simulations = runSimulations(initialMutants,population,fitnessBenefit, maxGenerations, runs,1100,1)
vanillaFixation = str(simulations[1])
plt.plot(simulations[0][0][0],simulations[0][0][1],color="green", label = "standard, P(fix)="+vanillaFixation)
for simulation in simulations[0][::1]:
    plt.plot(simulation[0],simulation[1],color="green")

### seasonalVariation
simulations = runSimulations(initialMutants,population,fitnessBenefit, maxGenerations,runs,1100,1,"Seasons")
seasonalVariationFixation = str(simulations[1])
plt.plot(simulations[0][0][0],simulations[0][0][1],color="blue", label = "seasonalVariation, P(fix)="+ seasonalVariationFixation)
for simulation in simulations[0][::1]:
    plt.plot(simulation[0],simulation[1],color="blue")


### bottleneck
bottleneckTimestamp = 100
simulations = runSimulations(initialMutants,population,fitnessBenefit, maxGenerations, runs,bottleneckTimestamp,0.1)
bottleneckFixation = str(simulations[1])
plt.plot(simulations[0][0][0],simulations[0][0][1],color="red", label = "bottleneck, P(fix)="+bottleneckFixation)
for simulation in simulations[0][::1]:
    plt.plot(simulation[0],simulation[1],color="red")

plt.xlabel("Generations")
plt.axvline(x = bottleneckTimestamp,color = 'r',linestyle='--')
plt.ylabel("p")


plt.suptitle("WRIGHT FISHER")
subtext = "initialMutants = "+str(initialMutants)+"; population = "+str(population)+"; fitnessBenefit ="+str(fitnessBenefit*100)+"%; maxGenerations = "+str(maxGenerations)+"; runs ="+str(runs)
plt.legend(title='Legend')
plt.title(subtext, fontsize=10, color='gray')
plt.show()

