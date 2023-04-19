#basic hill climbing search provided as base code for the DSA/ISE 5113 course
#author: Charles Nicholson
#date: 4/5/2019

#NOTE: You will need to change various parts of this code.  However, please keep the majority of the code intact (e.g., you may revise existing logic/functions and add new logic/functions, but don't completely rewrite the entire base code!)  
#However, I would like all students to have the same problem instance, therefore please do not change anything relating to:
#   random number generation
#   number of items (should be 150)
#   random problem instance
#   weight limit of the knapsack

#------------------------------------------------------------------------------

#Willow Arana, Cobey Weemes, Mansura Roly
#Date: 4/18/23


#need some python libraries
import copy
from random import Random   #need this for the random number generation -- do not change
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
    value.append(round(myPRNG.triangular(5,1000,200),1))
    
weights = []
for i in range(0,n):
    weights.append(round(myPRNG.triangular(10,200,60),1))
    
#define max weight for the knapsack
maxWeight = 2500

#change anything you like below this line ------------------------------------

#monitor the number of solutions evaluated
solutionsChecked = 0

#function to evaluate a solution x
def evaluate(x):
          
    a=np.array(x)
    b=np.array(value)
    c=np.array(weights)
    totalValue = np.dot(a,b) #compute the value of the knapsack selection
    totalWeight = np.dot(a,c) #compute the weight value of the knapsack selection
    sortedWeights = sorted(weights, reverse = True) #sort the weights in descending order
    heaviestItem = 0 #start with the heaviest item
    while totalWeight > maxWeight: #if the knapsack is too heavy
        for i in range(0,n): #for each item
            if weights[i] == sortedWeights[heaviestItem] and x[i] == 1: #if the item is the heaviest item and is in the knapsack
                x[i] = 0 #remove the item from the knapsack
                totalWeight -= weights[i] #update the total weight
                totalValue -= value[i] #update the total value
                break #we already removed the largest weight, so no need to stay in for loop
        heaviestItem += 1 #go to the next heaviest item
    return [totalValue, totalWeight] #returns a list of both total value and total weight
#here is a simple function to create a neighborhood
#1-flip neighborhood of solution x         
def neighborhood(x):
        
    nbrhood = []     
    
    for i in range(0,n):
        nbrhood.append(x[:])
        if nbrhood[i][i] == 1:
            nbrhood[i][i] = 0
        else:
            nbrhood[i][i] = 1
      
    return nbrhood
          


#create the initial solution
def initial_solution():
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



#varaible to record the number of solutions evaluated
solutionsChecked = 0

x_curr = initial_solution()  #x_curr will hold the current solution 
x_best = x_curr[:]           #x_best will hold the best solution 
f_curr = evaluate(x_curr)    #f_curr will hold the evaluation of the current soluton 
f_best = f_curr[:]



#begin local search overall logic ----------------
done = 0
    
while done == 0:
            
    Neighborhood = neighborhood(x_curr)   #create a list of all neighbors in the neighborhood of x_curr
    
    for s in Neighborhood:                #evaluate every member in the neighborhood of x_curr
        solutionsChecked = solutionsChecked + 1
        if evaluate(s)[0] > f_best[0]:   
            x_best = s[:]                 #find the best member and keep track of that solution
            f_best = evaluate(s)[:]       #and store its evaluation  
    
    if f_best == f_curr:                  #if there were no improving solutions in the neighborhood
        done = 1
    else:
        
        x_curr = x_best[:]         #else: move to the neighbor solution and continue
        f_curr = f_best[:]         #evalute the current solution
        
        print ("\nTotal number of solutions checked: ", solutionsChecked)
        print ("Best value found so far: ", f_best)        
    
print ("\nFinal number of solutions checked: ", solutionsChecked)
print ("Best value found: ", f_best[0])
print ("Weight is: ", f_best[1])
print ("Total number of items selected: ", np.sum(x_best))
print ("Best solution: ", x_best)
