import re
import logging

TEST_INPUT = [
    'class: 1-3 or 5-7',
    'row: 6-11 or 33-44',
    'seat: 13-40 or 45-50',
    '',
    'your ticket:',
    '7,1,14',
    '',
    'nearby tickets:',
    '7,3,47',
    '40,4,50',
    '55,2,20',
    '38,6,12',
]

class Validator:

    def __init__(self, line):
        t = line.split(': ')
        self.name = t[0]
        self.expression = t[1]
        self.valid_ranges = []
        for groups in re.findall(r'(\d+)-(\d+)', self.expression):
            lower = int(groups[0])
            upper = int(groups[1])
            self.valid_ranges.append((lower, upper))

    def validate(self, number):
        result = any(lower <= number <= upper for lower, upper in self.valid_ranges)
        logging.debug('%d in %s: %s', number, self.valid_ranges, result)
        return result

    def invalid_numbers(self, numbers):
        return [n for n in numbers if not self.validate(n)]

    def __repr__(self):
        return f'{self.name}: {self.expression}'


def parse_input(lines):
    # Making an explicit iterable allows us to save our progress when we break from for.
    iter_lines = iter(lines)
    validators = {}
    print('Parsing validators:')
    for line in iter_lines:
        if line == '':
            break
        v = Validator(line)
        validators[v.name] = v
    # skip next_line
    print('Parsing ', next(iter_lines))
    your_ticket = [int(n) for n in next(iter_lines).split(',')]
    # skip t0 nearby tickets
    next(iter_lines)
    print('Parsing ', next(iter_lines))
    nearby_tickets = [[int(n) for n in line.split(',')] for line in iter_lines]
    return validators, your_ticket, nearby_tickets

def part_1(validators, tickets):
    invalid_numbers = []
    for t in tickets:
        logging.debug(t)
        for n in t:
            if not any(v.validate(n) for v in validators.values()):
                invalid_numbers.append(n)
        logging.debug(invalid_numbers)
    print('ticket scanning error rate:', sum(invalid_numbers))

def tests():
    print('Tests\n-----\n')
    validators, your_ticket, nearby_tickets = parse_input(TEST_INPUT)
    part_1(validators, nearby_tickets)

def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        validators, your_ticket, nearby_tickets= parse_input((line.strip() for line in input_file.readlines()))
    part_1(validators, nearby_tickets)

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    tests()
    print('')
    main()
