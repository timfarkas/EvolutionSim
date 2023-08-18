import numpy
import matplotlib

n=1000
runs = 100
generations = 10
j = 10
mutationBenefit = 0.05
currentGen = 0
p = j / n


def reproduce(i, n, s):
    p = i/n
    expectedP = (p*(1+s))/(p*(1+s)+(1-p))
    j = numpy.random.binomial(n, expectedP)
    return j
    
while True:
    currentGen = currentGen + 1
    newJ = reproduce(j, n, mutationBenefit)
    print("Generation: "+str(currentGen)+" "+ str(j))
    j = newJ