import random
from GeneticObject import Genetic


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


    my_genetic = Genetic(f_create, len(target), 20, False)
    my_genetic.create()
    # my_genetic.load(73)
    while not my_genetic.done:
        my_genetic.population = ranking(my_genetic.population)
        my_genetic.pb = my_genetic.population.copy()
        my_genetic.selection(10, 5)
        my_genetic.breed_population()
        my_genetic.mutate(0.5)
        my_genetic.next_generation()

