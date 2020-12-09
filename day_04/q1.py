from itertools import cycle
from dataclasses import dataclass
from pprint import pprint
from typing import List
from functools import reduce
import operator
import re

TEST_INPUT = [
    'ecl:gry pid:860033327 eyr:2020 hcl:#fffffd',
    'byr:1937 iyr:2017 cid:147 hgt:183cm',
    '',
    'iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884',
    'hcl:#cfa07d byr:1929',
    '',
    'hcl:#ae17e1 iyr:2013',
    'eyr:2024',
    'ecl:brn pid:760753108 byr:1931',
    'hgt:179cm',
    '',
    'hcl:#cfa07d eyr:2025 pid:166559648',
    'iyr:2011 ecl:brn hgt:59in',
    ''
]

TEST_INVALID = [
    'eyr:1972 cid:100',
    'hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926',
    '',
    'iyr:2019',
    'hcl:#602927 eyr:1967 hgt:170cm',
    'ecl:grn pid:012533040 byr:1946',
    '',
    'hcl:dab227 iyr:2012',
    'ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277',
    '',
    'hgt:59cm ecl:zzz',
    'eyr:2038 hcl:74454a iyr:2023',
    'pid:3556412378 byr:2007',
]

TEST_VALID = [
    'pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980',
    'hcl:#623a2f',
    '',
    'eyr:2029 ecl:blu cid:129 byr:1989',
    'iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm',
    '',
    'hcl:#888785',
    'hgt:164cm byr:2001 iyr:2015 cid:88',
    'pid:545766238 ecl:hzl',
    'eyr:2022',
    '',
    'iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719',
]


FOUR_DIGITS = r'^(\d{4})$'

def regex(regex):
    def validator(x):
        return bool(re.match(regex, x))
    return validator

def between(min_v, max_v, regex=FOUR_DIGITS):
    def validator(x):
        result = re.match(regex, x)
        if not result:
            return False
        return min_v <= int(result.group(1)) <= max_v
    return validator

class Passport:

    FIELDS = {
        'byr',
        'iyr',
        'eyr',
        'hgt',
        'hcl',
        'ecl',
        'pid',
        'cid',
    }

    VALIDATORS = {
        # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        'byr': between(1920, 2002, FOUR_DIGITS),
        # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        'iyr': between(2010, 2020, FOUR_DIGITS),
        # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        'eyr': between(2020, 2030, FOUR_DIGITS),
        # hgt (Height) - a number followed by either cm or in:
        #     If cm, the number must be at least 150 and at most 193.
        #     If in, the number must be at least 59 and at most 76.
        'hgt': lambda x: between(150, 193, r'(^\d{3})cm$')(x) or between(59, 76, r'(^\d{2})in$')(x),
        # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        'hcl': regex(r'^#[0-9a-f]{6}$'),
        # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        'ecl': regex(r'^(amb|blu|brn|gry|grn|hzl|oth)$'),
        # pid (Passport ID) - a nine-digit number, including leading zeroes.
        'pid': regex(r'^\d{9}$'),
        # cid (Country ID) - ignored, missing or not.
        # 'cid': lambda x: True
    }

    def __init__(self):
        self.dict = dict()

    def add_line(self, line):
        for field in line.strip().split(' '):
            self.add_field(field)

    def add_field(self, field_string):
        key, value = field_string.strip().split(':')
        assert key in Passport.FIELDS
        if key in self.dict:
            raise Exception('Bang')
        self.dict[key] = value

    def valid(self):
        for key, validator in Passport.VALIDATORS.items():
            if key not in self.dict:
                return False
            if not validator(self.dict[key]):
                print(self.dict)
                print(key)
                return False
        return True


    def __repr__(self):
        return f'<valid: {self.valid()} {repr(self.dict)}>'


def build_passports(lines):
    passports = []

    p = None
    for line in lines:
        if line.strip():
            if p is None:
                p = Passport()
            p.add_line(line)
        else:
            passports.append(p)
            p = Passport()
    if p:
        passports.append(p)
    return passports


def tests():
    print('Tests\n-----\n')
    
    passports = build_passports(TEST_INPUT)
    s1 = sum(p.valid() for p in passports)
    print('Total valid: ', s1)

    passports = build_passports(TEST_INVALID)
    s2 = sum(p.valid() for p in passports)
    print('Total valid: ',s2)

    passports = build_passports(TEST_VALID)
    s3 = sum(p.valid() for p in passports)
    print('Total valid: ', s3)

    assert s2 == 0
    assert s3 == 4

    assert Passport.VALIDATORS['byr']('2002')
    assert not Passport.VALIDATORS['byr']('2003')

    assert Passport.VALIDATORS['hgt']('60in')
    assert Passport.VALIDATORS['hgt']('190cm')
    assert not Passport.VALIDATORS['hgt']('190in')
    assert not Passport.VALIDATORS['hgt']('190')

    assert Passport.VALIDATORS['hcl']('#123abc')
    assert not Passport.VALIDATORS['hcl']('#123abz')
    assert not Passport.VALIDATORS['hcl']('123abc')

    assert Passport.VALIDATORS['ecl']('brn')
    assert not Passport.VALIDATORS['ecl']('wat')

    assert Passport.VALIDATORS['pid']('000000001')
    assert not Passport.VALIDATORS['pid']('0123456789')

def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        passports = build_passports(input_file.readlines())

    print('Total valid: ', sum(p.valid() for p in passports))
    # 124 too high


if __name__ == '__main__':
    tests()
    print('')
    main()
