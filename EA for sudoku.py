from enum import unique
from operator import index
from random import choice, random 
import random
import numpy as np

### PARAMERS VALUES ###

def countEmpty(strGrid):
    """
    Return amount of empty space in a given grid
    """
    emptySpace = 0 # counter for the empty space in a grid

    for i in strGrid:
        if i == ".":
            emptySpace += 1
    
    return emptySpace

def string2Array2d(strGrid):
    """
    Return a np 9x9 array from the string given in Grid.ss file.
    """
    array1dGrid = []

    for i in strGrid:
        if i == ".":
            array1dGrid.append("0")
        elif i == "1" or i == "2" or i == "3" or i == "4" or i == "5" or i == "6" or i == "7" or i == "8" or i == "9" :
            array1dGrid.append(i)

    array1d = np.array(array1dGrid)
    array2d = np.reshape(array1d, (-1, 9))

    return array2d

# All input grids provided
grid1 = """
3..!..5!.47
..6!.42!..1
...!..7!89.
---!---!---
.5.!.16!..2
..3!...!..4
81.!...!7..
---!---!---
..2!...!4..
56.!87.!1..
...!3..!6..
"""
grid2 = """
..2!...!634
1.6!...!58.
..7!3..!29.
---!---!---
.85!..1!..6
...!75.!.23
..3!...!.5.
---!---!---
314!..2!...
..9!.8.!4..
72.!.4.!..9
"""
grid3 = """
..4!.1.!.6.
9..!...!.3.
.5.!796!...
---!---!---
..2!5.4!9..
.83!.6.!...
...!...!6.7
---!---!---
...!9.3!.7.
...!...!...
..6!...!.1.
"""

# grid settings
grid = grid3 # change the input grid here for the EA

#original board for cross checking
original = string2Array2d(grid)

#input board
input_board = string2Array2d(grid)

"""
# example
# original =np.array( [
# ['3','0','0','0','0','5','0','4','7'],
# ['0','0','6','0','4','2','0','0','1'],
# ['0','0','0','0','0','7','8','9','0'],
# ['0','5','0','0','1','6','0','0','2'],
# ['0','0','3','0','0','0','0','0','4'],
# ['8','1','0','0','0','0','7','0','0'],
# ['0','0','2','0','0','0','4','0','0'],
# ['5','6','0','8','7','0','1','0','0'],
# ['0','0','0','3','0','0','6','0','0']])
# example
# input_board = np.array( [
# ['3','0','0','0','0','5','0','4','7'],
# ['0','0','6','0','4','2','0','0','1'],
# ['0','0','0','0','0','7','8','9','0'],
# ['0','5','0','0','1','6','0','0','2'],
# ['0','0','3','0','0','0','0','0','4'],
# ['8','1','0','0','0','0','7','0','0'],
# ['0','0','2','0','0','0','4','0','0'],
# ['5','6','0','8','7','0','1','0','0'],
# ['0','0','0','3','0','0','6','0','0']])
"""
INDIVIDUAL_SIZE = 81 # a sudoku length

NUMBER_GENERATION = 100 

# Population size settings, uncomment the select one of the many settings.
POPULATION_SIZE = 10
# POPULATION_SIZE = 100
# POPULATION_SIZE = 1000
# POPULATION_SIZE = 10000

TRUNCATION_RATE = 0.5
MUTATION_RATE = 1.0 / countEmpty(grid)

### EVOLUTIONARY ALGORITHM ###

def evolve():
    """
    The main function for the evolutionary algorithm.
    """
    
    population = create_pop() # initial population of filled sudoku grids
    # find the fitness score for each sudoku solution in the population
    fitness_population = evaluate_pop(population) 

    # repeat producing generations of solutions according to NUMBER_GENERATION
    for gen in range(NUMBER_GENERATION):
        # sort the individual solution by the lowest fitness score in a list
        mating_pool = select_pop(population, fitness_population)
        # perform cross overing between two randomly chosen solution
        offspring_population = crossover_pop(mating_pool)
         # cross check template, before filling random number the solution
        population = mutate_pop(offspring_population)

        fitness_population = evaluate_pop(population) # provide a fitness score
        # return the best solution with its fitness score
        best_ind, best_fit = best_pop(population, fitness_population)
        print( "#", gen, " fit:",best_fit, "\n",best_ind)

### POPULATION-LEVEL OPERATORS ###

def create_pop():
    """
    Create & return a set amount of population according to POPULATION_SIZE
    """
    return [ create_ind() for _ in range(POPULATION_SIZE) ]

def evaluate_pop(population):
    """
    Calculate & return a list of the fitness score for each sudoku in the population
    """
    return [ evaluate_ind(individual) for individual in population ]

def select_pop(population, fitness_population):
    """
    Select & Return a list of individual sudoku solution sorted by their fitness score, 
    with a certain portion of the population going through mutation. 
    Defined by TRUNCATION_RATE.
    """
    # sort individuals by its fitness score
    sorted_population = sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])
    # 
    return [ individual for individual, fitness in sorted_population[:int(POPULATION_SIZE * TRUNCATION_RATE)] ]

def crossover_pop(population):
    """
    Return a population of crossovered individual solutions
    """
    
    cross_pop = [] # stores all crossovered population
    # crossover all individuals in the population
    for _ in range(POPULATION_SIZE):
        # randomly choose a a pair individual
        choice1 = random.choice(population) 
        choice2 = random.choice(population)

        # produce an offspring with the chosen pair
        item = crossover_ind(choice1, choice2)
        # stores an offspring to a list, which represents a crossovered population
        cross_pop.append(item) 
    
    cross = np.array(cross_pop) # data type convertion
    return cross

def mutate_pop(population):
    """
    Returns a population of mutated individuals of sudoku solutions
    """
    return [ mutate_ind(individual) for individual in population ]

def best_pop(population, fitness_population):
    """
    Select & return the individual with the best or lowest fitness score
    """
    return sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])[0]

### INDIVIDUAL-LEVEL OPERATORS: REPRESENTATION & PROBLEM SPECIFIC ###

def checkDefault(arrayItem,posy,posx,origin):
    '''
    check if there is already a default number in the current sudoku puzzle.
    
    '''
    if arrayItem == '0':
        # print('0f') # testing check point
        return False # this position is not a default number on its sudoku puzzle
    elif arrayItem == origin[posy][posx]: # No changes to any default number.
        # print('t') # testing check point
        return True # this position is a default number on its sudoku puzzle
    elif arrayItem != origin[posy][posx]:
        # print('1f') # testing check point
        return False # this position is not a default number on its sudoku puzzle


def create_ind():
    """
    populates random number to variable space in a given sudoku puzzle
    """
    array = input_board
    origin = original

    for y in range(len(array)):
        for x in range(len(array)):

            if not(checkDefault(array[y][x],y,x,origin)):
                ranNum = str(random.randint(1,9))
                array[y][x] = ranNum

    return array


def crossover_ind(individual1, individual2): # swap rows between 2 random solution
    """
    Return a crossovered child from a pair of individual sudoku solution
    """
    offspring = [] # stores rows of numbers from either pair
    # create a child by randomly choosing a row from either parent
    for row_pair in zip(individual1, individual2):
        # randomly choose a row of numbers from either pair
        choice0 = choice(row_pair) 
        offspring.append(choice0) # add a row to offspring

    children = np.array(offspring) # casting
    return children


def mutate_ind(individual): # put random numbers in the id array inside a 2d array
    """
    return a mutated solution by randomizing variable numbers in a grid
    """
    origin = original # stores the original grid template
    # check every number on the grid on y & x axis
    for y in range(len(individual)):
        for x in range(len(individual)):
            # if the number is not a default number on the original grid
            if not(checkDefault(individual[y][x],y,x,origin)):
                ran = random.random()
                # change the variable number under a certain random rate
                if ran < MUTATION_RATE:
                    ranNum = str(random.randint(1,9))
                    individual[y][x] = ranNum

    return individual


def evaluate_ind(individual):
    """
    calculate the fitness score of a sudoku solution
    """
    
    solution = individual

    fitness = 0 # the amount of duplicated numbers of a sudoku solution
    unique = list()
    # check the number of duplicated numbers in each row
    for row in solution:
        unique = row
        fitness += 9 - len(set(unique)) 
        # calculate the amount of duplicated numbers in a given list
    
    # check the number of duplicated numbers in each colum
    for x in range(len(solution)):
        col = solution[:,x]
        unique = col
        fitness += 9 - len(set(unique)) 
        # calculate the amount of duplicated numbers in a given list

    # check the number of duplicated numbers in each local 3x3 grid
    for i in range(0, 9, 3):
        for j in range(0, 9, 3): # loop through the 2d array in a pattern
            # content for each subgrid
            subrow1 = solution[i][j:j+3]
            subrow2 = solution[i+1][j:j+3]
            subrow3 = solution[i+2][j:j+3]
            # stores content of a subgrid to a 1d array
            subgrid = [*subrow1,*subrow2,*subrow3]
            unique = subgrid
            fitness += 9 - len(set(unique)) 
            # calculate the amount of duplicated numbers in a given list

    return fitness



### EVOLVE! ###
print("EVOLVE!")
evolve()
print("Empty: ",countEmpty(grid)) # test code
