from dataclasses import dataclass, field
import logging

TEST_INPUT = [
    'FBFBBFFRLR',
    'BFFFBBFRRR',
    'FFFBBBFRRR',
    'BBFFBBFRLL',
]

NUM_ROWS = 128
NUM_COLS = 8

def divide_seats(string, inc_char, seats):
    offset = 0
    logging.debug(string)
    for char in string:
        seats /= 2
        logging.debug(char)
        if char == inc_char:
            offset += seats
            logging.debug(f'  upper half: {offset}, +{seats}')
        else:
            logging.debug(f'  lower half: {offset}, +0')
    return int(offset)

def parse_front_back(string, seats=128):
    return divide_seats(string, 'B', seats)

def parse_left_right(string, seats=8):
    return divide_seats(string, 'R', seats)

def decode_seat_code(string: str) -> 'Seat':
    row_code = string[:7]
    column_code = string[7:]
    return Seat(parse_front_back(row_code), parse_left_right(column_code))

@dataclass(frozen=True)
class Seat:

    row: int
    column: int
    seat_id: int = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'seat_id', (self.row * 8) + self.column)


def tests():
    print('Tests\n-----\n')
    results = [decode_seat_code(code) for code in TEST_INPUT]
    print(results)

def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        results = [decode_seat_code(code.strip()) for code in input_file.readlines()]

    print('Max seat ID: ', max(s.seat_id for s in results))
    
    all_seats = {Seat(row, column) for row in range(NUM_ROWS) for column in range(NUM_COLS)}
    missing_seats = all_seats.difference(results)
    results = sorted(missing_seats, key=lambda e: e.row)
    for r in results:
        print(r)


if __name__ == '__main__':
    tests()
    print('')
    main()
