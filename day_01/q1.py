from itertools import takewhile, combinations  # It's almost too easy.
from functools import reduce
import operator

def sum_to_2020(input_tuple):
    return input_tuple[0] + input_tuple[1] == 2020

def find_numbers_that_sums_to_value(input_list, value, numbers):
    numbers_that_sum_to_value = filter(lambda n: sum(n) == value, combinations(input_list, numbers))
    match = next(numbers_that_sum_to_value)
    return match

def tests():
    print('Tests\n-----\n')
    test_input = [1721, 979, 366, 299, 675, 1456]

    result = find_numbers_that_sums_to_value(test_input, 2020, 2)
    print(result)

    print(result[0] * result[1])
    print('')
    result = find_numbers_that_sums_to_value(test_input, 2020, 3)
    print(result)
    print(reduce(operator.mul, result))
    

def main():
    print('Main\n----\n')
    with open("input_1.txt", 'r') as input_file:
        input_list = list(map(int, input_file.readlines()))

    print('2 numbers that sum to 2020:')
    result = find_numbers_that_sums_to_value(input_list, 2020, 2)
    print(result)
    print(reduce(operator.mul, result))
    print('\n3 numbers that sum to 2020:')
    result = find_numbers_that_sums_to_value(input_list, 2020, 3)
    print(result)
    print(reduce(operator.mul, result))

if __name__ == '__main__':
    tests()
    main()
