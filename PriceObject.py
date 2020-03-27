import csv


class Price:
    BORN = 6_421_839
    def __init__(self, end):
        self.price = [[row[0], row[1], float(row[2])] for row in csv.reader(open('data/final.csv'))]
        self.born = len(self.price) - end

    def get_one_data(self, val):
        return [self.price[val]]

    def get_several_data(self, start, number):
        result = []
        for row in range(start, start+number):
            result.append(self.price[row][2])
        return result


if __name__ == '__main__':
    my_price = Price()
    print(my_price.price)
    print('Split')
    print(my_price.get_several_data(2, 6))

