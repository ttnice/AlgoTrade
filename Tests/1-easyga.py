from pyeasyga import pyeasyga

# setup data
data = [{'name': 'box1', 'value': 4, 'weight': 12},
        {'name': 'box2', 'value': 2, 'weight': 1},
        {'name': 'box3', 'value': 10, 'weight': 4},
        {'name': 'box4', 'value': 1, 'weight': 1},
        {'name': 'box5', 'value': 2, 'weight': 2}]

ga = pyeasyga.GeneticAlgorithm(data)        # initialise the GA with data

times = 0
# define a fitness function
def fitness(individual, data):
    global times
    times += 1
    values, weights = 0, 0
    for selected, box in zip(individual, data):
        if selected:
            values += box.get('value')
            weights += box.get('weight')
    if weights > 15:
        values = 0
    return values

ga.fitness_function = fitness               # set the GA's fitness function
ga.run()                                    # run the GA
print(ga.best_individual())                 # print the GA's best solution
print(times)
print(ga.current_generation)