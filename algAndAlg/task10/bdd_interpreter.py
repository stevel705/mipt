import sys
import re

sep = ' '
lines_raw = sys.stdin.read().strip().split('\n')
lines_full = []
unparsed = []
for line in lines_raw:
    if re.match(r'^(\w+ \d+ \d+|TRUE|FALSE)$', line):
        lines_full.append(line)
    else:
        unparsed.append(line)
assert len(lines_full) > 0

lines = [x.split() for x in lines_full]
visits = [0] * len(lines)
vars = list(set([line[0] for line in lines if len(line) == 3]))
print()
print(end=' ')
print(*(vars + ['RESULT']), sep=sep)

for val in range(2 ** len(vars)):
    var_values = [(x, (val >> i) & 1) for i, x in enumerate(vars)]
    var_lookup = dict(var_values)
    pos = 0
    while len(lines[pos]) == 3:
        curr_var_value = var_lookup[lines[pos][0]]
        last_pos = pos
        pos = int(lines[pos][curr_var_value + 1])
        if pos >= len(lines):
            print('Destination out of range!')
            print('"{}" at line {} ("{}")'.format(pos, last_pos, lines_full[last_pos]))
            exit()
        visits[pos] += 1
    result = +(lines[pos][0] == 'TRUE')
    print(end=' ')
    print(*([str(v) for x, v in var_values] + [str(result)]), sep=sep)

print()
print('Lines visits:')
for i, line, v in zip(range(len(lines)), lines, visits):
    print('{:2d}'.format(i), end='|')
    if len(line) == 3:
        print('{} {:2d} {:2d}'.format(line[0], int(line[1]), int(line[2])), end=' ')
    else:
        print(line[0], end=' ')
    if v:
        print('<-- {:2d} visits'.format(v), end=' ')
    print()

if len(unparsed) > 0:
    print()
    print('Unparsed lines in output:')
    print(*unparsed, sep='\n')
