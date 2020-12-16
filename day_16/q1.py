import re
import logging
from typing import List, Tuple, Set
from functools import reduce
import operator

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

TEST_INPUT_2 = [
    'class: 0-1 or 4-19',
    'row: 0-5 or 8-19',
    'seat: 0-13 or 16-19',
    '',
    'your ticket:',
    '11,12,13',
    '',
    'nearby tickets:',
    '3,9,18',
    '15,1,5',
    '5,14,9',
]

class Validator:
    """Validate a ticket field."""

    def __init__(self, line):
        t = line.split(': ')
        self.name = t[0]
        self.expression = t[1]
        self.valid_ranges = []
        self.invalid_field_indexes = set()
        for groups in re.findall(r'(\d+)-(\d+)', self.expression):
            lower = int(groups[0])
            upper = int(groups[1])
            self.valid_ranges.append((lower, upper))

    def validate(self, number):
        result = any(lower <= number <= upper for lower, upper in self.valid_ranges)
        logging.debug('%d in %s: %s', number, self.valid_ranges, result)
        return result

    def scan_ticket(self, ticket):
        for i, number in enumerate(ticket):
            result = self.validate(number)
            if not result:
                # Collect indexes of ticket fields that this cannot be.
                self.invalid_field_indexes.add(i)

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
    nearby_tickets = [tuple(int(n) for n in line.split(',')) for line in iter_lines]
    return validators, your_ticket, nearby_tickets

def part_1(validators, tickets: List[Tuple[int]]):
    """Returns set of possibly valid tickets (all values valid for at least one field)"""
    invalid_numbers = []
    invalid_tickets = set()
    for t in tickets:
        logging.debug(t)
        for n in t:
            if not any(v.validate(n) for v in validators.values()):
                invalid_numbers.append(n)
                invalid_tickets.add(t)
        logging.debug(invalid_numbers)
    print('ticket scanning error rate:', sum(invalid_numbers))
    return set(tickets) - invalid_tickets

def part_2(validators, your_ticket, tickets: Set[Tuple[int]]):
    for ticket in tickets:
        for v in validators.values():
            v.scan_ticket(ticket)
    
    ticket_indexes = set(range(len(your_ticket)))
    results = []
    for v in sorted(validators.values(), key=lambda e: len(e.invalid_field_indexes), reverse=True):
        index = ticket_indexes - v.invalid_field_indexes
        assert len(index) == 1
        index = next(iter(index))
        ticket_indexes.remove(index)
        results.append((index, v))
    results = sorted(results, key=lambda t: t[0])

    value = 1
    for n, v in zip(your_ticket, results):
        if v[1].name.startswith('departure'):
            value *= n
    print('your ticket: ', value)
    


def tests():
    print('Tests\n-----\n')
    validators, your_ticket, nearby_tickets = parse_input(TEST_INPUT)
    part_1(validators, nearby_tickets)

    validators, your_ticket, nearby_tickets = parse_input(TEST_INPUT_2)
    valid_tickets = part_1(validators, nearby_tickets)
    part_2(validators, your_ticket, valid_tickets)

def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        validators, your_ticket, nearby_tickets= parse_input((line.strip() for line in input_file.readlines()))

    valid_tickets = part_1(validators, nearby_tickets)
    part_2(validators, your_ticket, valid_tickets)

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    tests()
    print('')
    main()
