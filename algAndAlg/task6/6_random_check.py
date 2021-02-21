import sys
import subprocess

import numpy as np
from tqdm import tqdm

argline = sys.argv[1:]
if not argline:
    print('Usage:')
    print('  $ python 6_random_check.py <command_to_run_your_solution>')
    print('Example:')
    print('  $ python 6_random_check.py python 6_my_solution.py')
    exit()
    

def check(failure, msg, inp, out):
    if failure:
        print()
        print('Input:', inp, sep='\n')
        print('Output:', out, sep='\n')
        print(msg)
        exit()

def is_singular(mat):
    return not np.allclose(np.linalg.det(mat) % 2, 1)

def mat2str(mat):
    return '\n'.join(' '.join(str(x) for x in row) for row in mat)

print('Checking the program on random matrices...')
for i in tqdm(range(150)):
    size = 2 if i < 5 else (3 if i < 15 else (4 if i < 60 else (5 if i < 100 else (6 if i < 140 else 7))))

    while True:
        mat_in = np.round(np.random.random((size, size))).astype('b')
        if not is_singular(mat_in):
            break
    
    inp = mat2str(mat_in)
    proc = subprocess.run(argline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=inp, encoding='ascii')
    (out, err) = proc.stdout.strip(), proc.stderr
    
    if err != '':
        print()
        print('Input:', inp, sep='\n')
        print('Error:', err, sep='\n')
        exit()
    
    if out == '':
        print()
        print('Input:', inp, sep='\n')
        print('Output is empty!')
        exit()

    check(len(out.split('\n')) != 3 * size, 'Incorrect size of output, must be ' + str(3 * size) + ' lines', inp, out)
    check(sum(sum(x == '' for x in row.split(' ')) for row in out.split('\n')) != 0, 'Incorrect spacing in output', inp, out)
    check(sum(sum(x != '0' and x != '1' for x in row.split(' ')) for row in out.split('\n')) != 0, 'Unexpected tokens in output, only 0 and 1 are allowed', inp, out)
    data = [[int(x) for x in row.split(' ')] for row in out.split('\n')]
    
    l, u, p = np.array(data[:size]), np.array(data[size:2*size]), np.array(data[2*size:])
    
    check(is_singular(l), 'L is singular', inp, out)
    check(is_singular(u), 'U is singular', inp, out)
    check(is_singular(p), 'P is singular', inp, out)
    
    check(not np.allclose(l, np.tril(l)), 'L is not a lower triangle matrix', inp, out)
    check(not np.allclose(u, np.triu(u)), 'U is not an upper triangle matrix', inp, out)
    check(np.any(p.sum(axis=0) - 1) or np.any(p.sum(axis=1) - 1), 'P is not a permutation matrix', inp, out)
    
    got = (l @ u @ p) & 1
    if not np.allclose(got, mat_in):
        print()
        print('Product of LUP is not A, decomposition is not correct')
        print('Input:', inp, sep='\n')
        print('Product of LUP:')
        np.savetxt(sys.stdout, got, fmt='%d')
        print('Output:', out, sep='\n')
        exit()

print()
print('Seems to be correct!')