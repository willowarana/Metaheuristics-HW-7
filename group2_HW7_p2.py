#!/usr/bin/env python
# coding: utf-8

# #### Genetic Algorithm

# In[1]:


#need some python libraries
import copy
import math
import random
from random import Random
import numpy as np

#to setup a random number generator, we will specify a "seed" value
#need this for the random number generation -- do not change
seed = 51132023
myPRNG = Random(seed)

#to get a random number between 0 and 1, use this:             myPRNG.random()
#to get a random number between lwrBnd and upprBnd, use this:  myPRNG.uniform(lwrBnd,upprBnd)
#to get a random integer between lwrBnd and upprBnd, use this: myPRNG.randint(lwrBnd,upprBnd)

#number of elements in a solution
n = 150

#create an "instance" for the knapsack problem
value = []
for i in range(0,n):
    #value.append(round(myPRNG.expovariate(1/500)+1,1))
    value.append(round(myPRNG.triangular(150,2000,500),1))

weights = []
for i in range(0,n):
    weights.append(round(myPRNG.triangular(8,300,95),1))

#define max weight for the knapsack
maxWeight = 2500

all_items={}
for i in range(n):
    all_items[i+1]=(value[i],weights[i])


#change anything you like below this line, but keep the gist of the program ------------------------------------

#monitor the number of solutions evaluated
solutionsChecked = 0


populationSize = 150 #size of GA population
Generations = 100    #number of GA generations

crossOverRate = 0.8  #currently not used in the implementation; neeeds to be used.
mutationRate = 0.05  #currently not used in the implementation; neeeds to be used.
eliteSolutions = 10  #currently not used in the implementation; neeed to use some type of elitism


#create an continuous valued chromosome
def createChromosome(n):
    x = [0] * n #this list has a value for each item: 1 indicates the item is packed, 0 otherwise
    currentWeight = 0 #weight starts at zero before we add items
    full = False
    while not full: #while we still have available capacity
        selectedItem = myPRNG.randint(0,n - 1) #select a random item to add
        if currentWeight + weights[selectedItem] <= maxWeight: #if adding the item does not exceed the capacity
            x[selectedItem] = 1 #add the item to the knapsack
            currentWeight += weights[selectedItem] #update the current weight
        else:
                full = True #the weight limit has been reached
    return x

#create initial population by calling the "createChromosome" function many times and adding each to a list of chromosomes (a.k.a., the "population")
def initializePopulation(): #n is size of population; d is dimensions of chromosome

    population = [] #list of chromosomes in the population
    populationFitness = [] #list of fitness values in the population

    for i in range(populationSize): #for each chromosome in the population
        population.append(createChromosome(n)) #add a chromosome
        populationFitness.append(evaluate(population[i])) #add that chromosome's fitness value to the fitness list

    tempZip = zip(population, populationFitness) #store the population and its fitness values
    popVals = sorted(tempZip, key=lambda tempZip: tempZip[1], reverse = True) #sort the population by best value

    return popVals #return the population and fitness values

#implement a crossover
def crossover(x1,x2):
    #with some probability (i.e., crossoverRate) perform breeding via crossover,
    rand_num = myPRNG.random()
    if rand_num <= crossOverRate:  # Perform a cross over
        cross_over_point=myPRNG.randint(1,150)
        offspring1=x1[:cross_over_point]+x2[cross_over_point:]
        offspring2=x1[cross_over_point:]+x2[:cross_over_point]
    else:
        # if no breeding occurs, then offspring1 and offspring2 can simply be copies of x1 and x2, respectively
        offspring1=x1[:]
        offspring2=x2[:]
    return offspring1, offspring2  #two offspring are returned


#function to compute the weight of chromosome x
def calcWeight(x):

    a=np.array(x)
    c=np.array(weights)

    totalWeight = np.dot(a,c)    #compute the weight value of the knapsack selection

    return totalWeight   #returns total weight

#function to determine how many items have been selected in a particular chromosome x
def itemsSelected(x):

    a=np.array(x)
    return np.sum(a)   #returns total number of items selected

#function to evaluate a solution x
def evaluate(x):

    a=np.array(x) #create arrays from the previous lists
    b=np.array(value)
    c=np.array(weights)

    totalValue = np.dot(a,b)     #compute the value of the knapsack selection
    totalWeight = calcWeight(x)   #compute the weight value of the knapsack selection

    if totalWeight > maxWeight: #if the weight exceeds the limit
        penalty = 500*(totalWeight - maxWeight) # set a large penalty for exceeding the max weight
        totalValue = totalValue-penalty #add the penalty to the totalValue

    fitness  = totalValue #set the fitness value to the total value
    return fitness   #returns the chromosome fitness



#performs tournament selection; k chromosomes are selected (with repeats allowed) and the best advances to the mating pool
#function returns the mating pool with size equal to the initial population
def tournamentSelection(pop,k):

    #randomly select k chromosomes; the best joins the mating pool
    matingPool = []

    while len(matingPool)<populationSize:

        ids = [myPRNG.randint(0,populationSize-1) for i in range(k)]
        competingIndividuals = [pop[i][1] for i in ids]
        bestID=ids[competingIndividuals.index(max(competingIndividuals))]
        matingPool.append(pop[bestID][0])

    return matingPool


def rouletteWheel(population):
    #randomly select k chromosomes; the best joins the mating pool
    matingPool = []

    fitness_sum=sum(i[1] for i in population) # Calculate the sum of fitness values
    probabilities=[i[1]/fitness_sum for i in population] # Calculate the probability of selection for each individual
    cumulative_probability=[]
    temp=0
    for j in range(len(population)):
        temp=temp+probabilities[j]
        cumulative_probability.append(temp)

    #create sometype of rouletteWheel selection -- can be based on fitness function or fitness rank
    #(remember the population is always ordered from most fit to least fit, so pop[0] is the fittest chromosome in the population, and pop[populationSize-1] is the least fit!
    for i in range(len(population)):
        spin = random.random()
        for i in cumulative_probability:
            if i>spin:
                try:
                    pop=population[cumulative_probability.index(i)+1][0]
                except:
                    pop=population[cumulative_probability.index(i)][0]
                break
        matingPool.append(pop)

    return matingPool


#function to mutate solutions
def mutate(x):
    rand_num = myPRNG.random() #generate a random number
    mutated_x=x[:] #make a copy of the given solution
    if rand_num <= mutationRate:  #if mutation occurs
        mutation_point=myPRNG.randint(1,n-1) # #choose a random item
        mutated_x[mutation_point]= 1-mutated_x[mutation_point] #swap from 0 to 1 or 1 to 0
        return mutated_x #return mutated solution
    return mutated_x #return original solution


#breeding -- uses the "mating pool" and calls "crossover" function
def breeding(matingPool):
    #the parents will be the first two individuals, then next two, then next two and so on

    children = [] #list of children
    childrenFitness = [] #list of associated fitness values of children
    for i in range(0,populationSize-1,2): #for every even chromosome in the population
        child1,child2=crossover(matingPool[i],matingPool[i+1]) #two parents are chosen to mate

        child1=mutate(child1) #mutate the first child
        child2=mutate(child2) #mutate the second child

        children.append(child1) #add the children to the list of children
        children.append(child2)

        childrenFitness.append(evaluate(child1)) #add the children's fitness scores to the fitness list
        childrenFitness.append(evaluate(child2))

    tempZip = zip(children, childrenFitness) #store the children and their associated fitness values in one list
    popVals = sorted(tempZip, key=lambda tempZip: tempZip[1], reverse = True) #sort the children by value

    #the return object is a sorted list of tuples:
    #the first element of the tuple is the chromosome; the second element is the fitness value
    #for example:  popVals[0] is represents the best individual in the population
    #popVals[0] for a 2D problem might be  ([-70.2, 426.1], 483.3)  -- chromosome is the list [-70.2, 426.1] and the fitness is 483.3

    return popVals


#insertion step
def insert(pop,kids):
    new_list = pop[:eliteSolutions] + kids #keep the elite solutions and insert the children
    return new_list



#perform a simple summary on the population: returns the best chromosome fitness, the average population fitness, and the variance of the population fitness
def summaryFitness(pop):
    a=np.array(list(zip(*pop))[1])
    return np.max(a), np.mean(a), np.min(a), np.std(a)


#the best solution should always be the first element...
def bestSolutionInPopulation(pop):
    print ("Best solution: ", pop[0][0])
    print ("Items selected: ", itemsSelected(pop[0][0]))
    print ("Value: ", pop[0][1])
    print ("Weight: ", calcWeight(pop[0][0]))


def main():
    #GA main code
    Population = initializePopulation() #initialize the first population

    for j in range(Generations): #for each generation

        mates=rouletteWheel(Population) #determine the set of mates

        Offspring = breeding(mates) #generate offspring and do mutations
        Population = insert(Population, Offspring) #create the distribution of the new population

        #end of GA main code

        maxVal, meanVal, minVal, stdVal=summaryFitness(Population)          #check out the population at each generation
        # print("Iteration: ", j, summaryFitness(Population))                 #print to screen; turn this off for faster results

    print (summaryFitness(Population))
    bestSolutionInPopulation(Population)


if __name__ == "__main__":
    main()


# ### Test Cells

# In[ ]:




