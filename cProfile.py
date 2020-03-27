import timeit, random


def slow_function():
    total = []

    for i, _ in enumerate(range(100_000_000)):
        total.append(random.random())

    return total


print(f'{timeit.timeit(slow_function, number=1)}')