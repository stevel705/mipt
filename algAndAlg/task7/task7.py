# Задание 7: Конструкция Пэли и коды Боуза—Шриханде

# Реализуйте алгоритм построения кодов Боуза—Шриханде второго типа, которые построены по матрице Адамара, 
# построенной в свою очередь на основе конструкции Пэли. На вход программы подаётся единственное целое число n. 
# Гарантируется, что n делится на 4 без остатка, и что (n−1) — простое число. 
# Программа должна выдать 2n строчек длины n, содержащих нули и единицы. Строчки должны быть все различны, 
# причём количество различных позиций в любой паре различных строчек должно быть не менее n/2.

# Вычислительной оптимальности не требуется, но полезно, например, предвычислить таблицу значений символа Лежандра.

import numpy as np


def inv_matrix(matrix):
    matrix_ = matrix.copy()
    return np.array([1 * (i + 1) % 2 for i in matrix_])

def build_Hadamard_matrix(n):
    result = np.zeros((n, n))
    p = n - 1 

    residues = np.zeros(2 * p)

    residues[:p] = -1
    
    for i in range(1, ((p - 1) // 2) + 1):
        residues[i * i % p] = 1

    residues[p:2 * p] = residues[: - p]

    result[0, :] = 1

    result[:, 0] = 1
    
    for i in range(1, n):
        for j in range(1, n):
            result[i, j] = residues[j - i + p]    

    return result

    
def print_matrix(matrix):
    '''
    Print matrix
    Input: nxn matrix, optional - n=shape
    ''' 
    n = matrix.shape[0]
    for line in matrix[:n, :n].astype(np.int32):
        print("".join(map(str, line)))

def main():
    n = int(input())
    
    hadamard_matrix = build_Hadamard_matrix(n)

    hadamard_matrix[hadamard_matrix < 0] = 0

    hadamard_matrix2 = inv_matrix(hadamard_matrix)

    hadamard_matrix = hadamard_matrix[::-1]

    result_code = np.vstack((hadamard_matrix2, hadamard_matrix))

    print_matrix(result_code)

main()