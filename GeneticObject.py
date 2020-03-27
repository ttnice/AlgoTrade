import random, json
'''
4T Programmer tranthuongtienthinh@gmail.com

This program allow you to do genetic algorithmon list.
Just create :
    - a function that generate parameter for your list.
    - 
'''


import random, json, string
'''
4T Programmer tranthuongtienthinh@gmail.com

This program allow you to do genetic algorithmon list.
Just create :
    - a function that generate parameter for your list.
    - 
'''


class Genetic:
    def __init__(self, f_create, individu_size, population_size, saving=True, target_score=None):
        self.f_create = f_create

        self.population = []
        self.new_population = []
        self.population_size = population_size
        self.individu_size = individu_size
        self.saving = saving
        self.generation = 1
        self.target_score = target_score if target_score != None else individu_size
        self.done = False

        self.elite_size = 0
        self.random_size = 0

    def create(self):
        # Create a bunch of population in the list population
        # Using the f_create function given in __init__

        for i in range(self.population_size):
            self.population.append({
                'individu': [self.f_create() for i in range(self.individu_size)],
                'score': None
            })

    def selection(self, elite_size, random_size, shift=0.2):
        # You have to give Score to each population before doing a selection and to rank them :
        ' sorted("self".population, key=lambda k: k["score"], reverse=True) '
        # The selection paste the bests individu into self.next_generation

        children = []
        self.elite_size = elite_size
        self.random_size = random_size

        for i in range(elite_size):
            children.append(self.population[i]['individu'].copy())
        for i in range(random_size):
            pick = int((1-(random.random()**shift))*self.population_size)
            children.append(self.population[pick]['individu'].copy())
        self.new_population += children

    def breed(self, parent1, parent2):
        # To take random gene from the parents and give them to the child

        gene = int(random.random() * self.population_size)
        child = parent1[:gene] + parent2[gene:]
        return child

    def breed_population(self, shift=0.2):
        # Create bunch of child into self.next_generation

        children = []
        length = self.population_size - (self.elite_size + self.random_size)
        for i in range(length):
            pick1 = int((1 - (random.random() ** shift)) * self.population_size)
            pick2 = int((1 - (random.random() ** shift)) * self.population_size)
            parent1 = self.population[pick1]['individu'].copy()
            parent2 = self.population[pick2]['individu'].copy()
            child = self.breed(parent1, parent2)
            children.append(child)
        self.new_population += children

    def mutate(self, mutation_rate):
        # Change random gene from the individu in self.next_generation

        for individu_index in range(self.population_size):
            if random.random() < mutation_rate:
                for i in range(int((random.random()**(2 - mutation_rate)) * len(self.new_population[0]))):
                    self.new_population[individu_index][random.randrange(len(self.new_population[0]))] = self.f_create()

    def next_generation(self):
        # Save self.population ranked with score
        # Create a Log file
        # Discard replace self.population by self.next_generation and Discard

        if self.saving:
            self.save(self.generation)
        with open('Genetic/LogNumber.txt', 'a') as outfile:
            outfile.write(f'For Generation {self.generation} :\n')
            outfile.write(f'Best Score : {self.population[0]["score"]}\n')
            outfile.write(f'Average Score : {sum([self.population[i]["score"] for i in range(self.population_size)])/self.population_size} \n')
            outfile.write(f'Worst Score : {self.population[-1]["score"]} \n\n')
        print(f'{self.generation} - {self.population[0]}')

        if self.population[0]["score"] >= self.target_score:
            if not self.saving:
                self.save(self.generation)
            print(self.population[0])
            print('Done !')
            self.done = True

        self.population = []
        for i in range(self.population_size):
            self.population.append({
                'individu': self.new_population[i],
                'score': None
            })
        self.generation += 1
        self.new_population = []

    def save(self, name):
        with open(f'Genetic/Generation_{name}.txt', 'w') as outfile:
            json.dump(self.population, outfile)
            outfile.close()

    def load(self, name):
        self.generation = name
        with open(f'Genetic/Generation_{name}.txt', 'r') as outfile:
            self.population = json.load(outfile)
            outfile.close()


if __name__ == '__main__':
    # Example with a list of number
    target = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


    def f_create():
        return random.randrange(10)


    def ranking(population):
        length = len(target)
        for individu_index in range(len(population)):
            individu = population[individu_index]
            score = 0
            for i in range(length):
                if target[i] == individu['individu'][i]:
                    score += 1
            population[individu_index]['score'] = score
        return sorted(population, key=lambda k: k["score"], reverse=True)


    my_genetic = Genetic(f_create, len(target), 100, False)
    my_genetic.create()
    while not my_genetic.done:
        my_genetic.population = ranking(my_genetic.population)
        my_genetic.selection(10, 5)
        my_genetic.breed_population()
        my_genetic.mutate(0.5)
        my_genetic.next_generation()

