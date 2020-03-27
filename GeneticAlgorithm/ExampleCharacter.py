import random, string
from GeneticObject import Genetic


if __name__ == '__main__':
    # Example with a list of character
    target = ['H', 'e', 'l', 'l', 'o', 'W', 'o', 'r', 'l', 'd']

    def f_create():
        return random.choice(string.ascii_letters)

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
    # my_genetic.load(69)
    while not my_genetic.done:
        my_genetic.population = ranking(my_genetic.population)
        my_genetic.selection(10, 5)
        my_genetic.breed_population()
        my_genetic.mutate(0.5)
        my_genetic.next_generation()