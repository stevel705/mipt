#! /usr/bin/env python3 python get_mr_variant.py hob2021158

import string
import sys

tasks = list(range(120, 126))

if __name__ == '__main__':
    result = 0
    for symbol in sys.argv[1]:
        for num, elem in enumerate(string.ascii_lowercase):
            if symbol == elem:
                result += num
                break
    print(tasks[result % len(tasks)])
