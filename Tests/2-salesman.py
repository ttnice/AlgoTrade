import random, numpy, math, copy, matplotlib.pyplot as plt

# https://ericphanson.com/blog/2016/the-traveling-salesman-and-10-lines-of-python/
cities = [random.sample(range(100), 2) for x in range(15)];
tour = random.sample(range(15),15);
for gene, temperature in enumerate(numpy.logspace(0,5,num=100_000)[::-1]):
    [i,j] = sorted(random.sample(range(15),2));
    newTour =  tour[:i] + tour[j:j+1] +  tour[i+1:j] + tour[i:i+1] + tour[j+1:];
    if math.exp( ( sum([ math.sqrt(sum([(cities[tour[(k+1) % 15]][d] - cities[tour[k % 15]][d])**2 for d in [0,1] ])) for k in [j,j-1,i,i-1]]) - sum([math.sqrt(sum([(cities[newTour[(k+1) % 15]][d] - cities[newTour[k % 15]][d])**2 for d in [0,1] ])) for k in [j,j-1,i,i-1]])) / temperature) > random.random():
        tour = copy.copy(newTour);
    if gene % 10_000 == 0:
        plt.plot([cities[tour[i % 15]][0] for i in range(16)], [cities[tour[i % 15]][1] for i in range(16)], 'xb-');
        plt.title(f'Generation {gene}')
        plt.pause(0.0001)
        plt.close()
    print(f'Generation {gene}')

plt.plot([cities[tour[i % 15]][0] for i in range(16)], [cities[tour[i % 15]][1] for i in range(16)], 'xb-');
plt.title(f'Generation {gene}')
plt.show()