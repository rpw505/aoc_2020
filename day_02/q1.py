from itertools import takewhile, combinations  # It's almost too easy.
from functools import reduce
import operator
import re
from collections import Counter
from dataclasses import dataclass
from pprint import pprint

@dataclass
class PasswordRecord:
    text: str
    min: int
    max: int
    char: str
    password: str


    def __init__(self, line):
        # 1-3 a: abcde
        # 1-3 b: cdefg
        # 2-9 c: ccccccccc
        self.text = line.strip()
        regex = r'(\d*)-(\d*) (.): (.*)'
        m = re.match(regex, line)

        self.min = int(m.group(1))
        self.max = int(m.group(2))
        self.char = m.group(3)
        self.password = m.group(4)

    def __repr__(self):
        return f'<{self.text}, {self.valid}, {self.valid_2}>'

    @property
    def valid(self) -> bool:
        counts = Counter(self.password)
        return self.min <= counts.get(self.char, 0) <= self.max
    
    @property
    def valid_2(self) -> bool:
        return (self.password[self.min-1] == self.char) ^ (self.password[self.max-1] == self.char)


def tests():
    print('Tests\n-----\n')
    
    test_input = [
        PasswordRecord('1-3 a: abcde'),
        PasswordRecord('1-3 b: cdefg'),
        PasswordRecord('2-9 c: ccccccccc')
    ]
    print(test_input)
    

def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        input_list = [PasswordRecord(line) for line in input_file.readlines()]
    
    pprint(input_list)
    print('Number of valid passwords: ', sum(e.valid for e in input_list))
    print('Number of valid_2 passwords: ', sum(e.valid_2 for e in input_list))

if __name__ == '__main__':
    tests()
    main()
