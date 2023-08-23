import numpy
import matplotlib.pyplot as plt


class EvoSim:
    def __init__(self,parameters):
        self.parameters = parameters
        #self.combinedSimulation()
    
    #### takes population and proportion of mutants and outputs new proportion of mutants new population [j,n] based on growth factor r
    def reproduceGrowing(self, i, n, s, c ,r):
        n = int((1+r)*n*(1-(r*n)/((1+r)*c)))                       # before bottleneck
        p = i/n
        expectedP = (p*(1+s))/(p*(1+s)+(1-p))
        j = numpy.random.binomial(n, expectedP)
        return [j,n]

    ### takes initial mutants j, population size n, mutationbenefit s and no of generations
    def simulate(self, initialJ, n, mutationBenefit, generations = 1000, bottleneckTimestamp = 500, decimationFactor = 1, mode = None,c = 1000,r = 0.1): #bottleneck variables added
        ## array simulation [currentGen, p, Bool fixation ]
        simulation = [[],[],0]
        j = initialJ
        p = j/n
        for currentGen in range(0, generations):            
            ### modify mutationBenefit based on environmentalBenefitModifier to simulate environmental effects on mutationBenefit
            modS = mutationBenefit * self.environmentalBenefitModifier(currentGen,mutationBenefit,mode)
            p = j/n
            
            if currentGen == bottleneckTimestamp-1:
                nDecimated = int(n* decimationFactor)                   # decimates population size
                j = numpy.random.binomial(nDecimated, p)                # calculates new j
                p = j/nDecimated  
                array = self.reproduceGrowing(j, nDecimated, modS,c,r)       #growing population  
            else:                                                       # regrowing population size
                array = self.reproduceGrowing(j, n, modS,c,r)                #growing population

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
    def runSimulations(self,initialJ, n, mutationBenefit, generations = 1000, runs = 100, bottleneckTimestamp = 500, decimation = 1, envMode = None,c=1000,r=1):
        simulations = [[],0]
        #print(runs)
        for run in range(0, runs):
            simulation = self.simulate(initialJ, n, mutationBenefit, generations, bottleneckTimestamp, decimation, envMode,c,r)     # bottleneck variables added
            simulations[0].append(simulation)
            simulations[1] = simulations[1] + simulation[2] 
        if len(simulations[0]) > 0:  # Überprüfe, ob die Liste nicht leer ist
            fixationProb = simulations[1] / len(simulations[0])
            simulations[1] = fixationProb
        else:
            fixationProb = 0
        simulations[1] = fixationProb
        return simulations

    ### takes current generation, unmodified selection coefficient and environment mode and returns modified selection coefficient
    def environmentalBenefitModifier(self,gen, s, mode):
        if mode is None:
            return 1
        if mode.lower() == "seasons":
            return numpy.abs(self.sinusModifier(gen, s, 25, 2))
        else:
            return 1 
    
    ### takes current generation, unmodified selection coefficient and environment mode and returns modified selection coefficient modulated by periodic fluctuations of specified amplitude with a given period 
    def sinusModifier(self, gen, s, period, amplitude):
	    return s * numpy.sin((1/period)*gen) * amplitude
    
    def combinedSimulation(self):
        population          = int(self.parameters[0])
        maxGenerations      = int(self.parameters[1])
        runs                = int(self.parameters[2])
        c                   = int(self.parameters[3])
        initialMutants      = int(self.parameters[4])
        r                   = int(self.parameters[5])
        fitnessBenefit      = self.parameters[6]
        bottleneckTimestamp = int(self.parameters[7])
        decimationFactor    = int(self.parameters[8])
        plt.clf()
        ### vanilla
        #(initialJ, n, mutationBenefit, generations = 1000, runs = 100, bottleneckTimestamp = 1100, decimation = 1, envMode = None,c=1000,r=1):
        noBottleneck = maxGenerations +1
        simulations = self.runSimulations(initialMutants,population,fitnessBenefit, maxGenerations, runs,noBottleneck,1,None,c,r) #,1,None,c,r
        vanillaFixation = str(simulations[1])
        plt.plot(simulations[0][0][0],simulations[0][0][1],color="green", label = "standard, P(fix)="+vanillaFixation)
        for simulation in simulations[0][::1]:
            plt.plot(simulation[0],simulation[1],color="green")

        ### seasonalVariation
        simulations = self.runSimulations(initialMutants,population,fitnessBenefit, maxGenerations,runs,bottleneckTimestamp,decimationFactor,"Seasons",c,r)
        seasonalVariationFixation = str(simulations[1])
        plt.plot(simulations[0][0][0],simulations[0][0][1],color="blue", label = "seasonalVariation, P(fix)="+ seasonalVariationFixation)
        for simulation in simulations[0][::1]:
            plt.plot(simulation[0],simulation[1],color="blue")


        ### bottleneck
        simulations = self.runSimulations(initialMutants,population,fitnessBenefit, maxGenerations, runs,bottleneckTimestamp,decimationFactor,None,c,r)
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
        
        return simulations