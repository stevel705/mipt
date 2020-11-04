# # Задание 4: алгоритм Штрассена + быстрое возведение в степень

# def matrix_multiply(A, B):
#     if the matrix has a shape of 2^7 x 2^7 use built-in Python methods to multiply:
#         return multiplication of A and B by numpy
#     else:
#         Create the four pieces of the first input matrix
#         Create the four pieces of the second input matrix
#         Carry out the 7 multiplications by calling matrix_multiply and store them
#         Add up the multiplications into the four quarters of the result
#         Reassemble the result matrix and return it

# # INPUT
# # 2 0 1
# # 4 2 7
# # 3 5 5

# # OUTPUT 
# # 1 0 5
# # 2 1 8
# # 6 7 7


import sys
import math
import numpy as np

def add_eye(mat):
    '''
    If matrix not even, add eye matrix
    Input: nxn matrix 
    Output: n+1xn+1 matrix 
    '''
    # find nearest power of two
    two_in_power = 2
    power = 1
    while two_in_power <= mat.shape[0]:
        two_in_power *= 2
        power += 1

    # add the angle of the unit matrix
    b = np.eye(two_in_power)
    z = two_in_power - mat.shape[0]
    b[:-z,:-z] = mat
    return b

def split(mat): 
    """ 
    Splits a given matrix into quarters. 
    Input: nxn matrix 
    Output: tuple containing 4 n/2 x n/2 matrices corresponding to a11, a12, a21, a22
    """
    row, col = mat.shape 
    row2, col2 = row // 2, col // 2
    return mat[:row2,:col2], mat[:row2,col2:], mat[row2:,:col2], mat[row2:,col2:] 
  
def strassen(A, B): 
    """ 
    Computes matrix product by divide and conquer approach, recursively. 
    Input: nxn matrices A and B 
    Output: nxn matrix, product of A and B 
    """
    # Base case when size of matrices is 1x1 
    if len(A) == 1: 
        return A * B 
  
    # Splitting the matrices into quadrants. This will be done recursively 
    # untill the base case is reached. 

    a11, a12, a21, a22 = split(A) 
    b11, b12, b21, b22 = split(B) 
    
    # Computing the 7 products, recursively (p1, p2...p7) 
    p1 = strassen(a11, b12 - b22)   
    p2 = strassen(a11 + a12, b22)         
    p3 = strassen(a21 + a22, b11)         
    p4 = strassen(a22, b21 - b11)         
    p5 = strassen(a11 + a22, b11 + b22)         
    p6 = strassen(a12 - a22, b21 + b22)   
    p7 = strassen(a11 - a21, b11 + b12)   
  
    # Computing the values of the 4 quadrants of the final matrix c 
    c11 = p5 + p4 - p2 + p6   
    c12 = p1 + p2            
    c21 = p3 + p4             
    c22 = p1 + p5 - p3 - p7   
  
    # Combining the 4 quadrants into a single matrix by stacking horizontally and vertically. 
    c = np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))  
    
    return c 

def log_mult(mat, n):
    '''
    Fast exponentiation of a matrix
    Input: nxn matrix, n - power
    Output: Matrix**n
    '''
    res = np.eye(mat.shape[0])
    while n:
        if n & 1:
            res = strassen(res, mat)
            res = arr_to_z9(res)
            n -= 1
        else:
            mat = strassen(mat, mat)
            mat = arr_to_z9(mat)
            n = n >> 1
    return res

def Log2(x): 
    return (math.log10(x) / math.log10(2))
  
def is_power_of_two(n): 
    '''
    Is the matrix a power of two
    Input: n - shape of matrix
    Output: True or False
    '''
    return (math.ceil(Log2(n)) == math.floor(Log2(n)))

def arr_to_z9(mat):
    '''
    Converting the matrix to Z9 format
    Input: nxn matrix
    Output: nxn matrix in Z9 format
    '''  
    return np.remainder(mat, 9)

def main(matrix):
    '''
    Main program
    Input: matrix
    '''
    if np.size(matrix) == 1:
        print(1)
        return

    power = matrix.shape[0]

    # check shape of matrix
    change = False
    if not is_power_of_two(matrix.shape[0]):
        matrix = add_eye(matrix)
        change = True


    final_mat = log_mult(matrix, power)

    def print_matrix(matrix, n=matrix.shape[0]):
        '''
        Print matrix
        Input: nxn matrix, optional - n=shape
        ''' 
        for line in matrix[:n, :n].astype(np.int32):
            print(" ".join(map(str, line)))

    if change:
        print_matrix(final_mat, n=power)
    else:
        print_matrix(final_mat)
    

# mat = np.loadtxt(sys.stdin, dtype='int')
mat = np.array([[2, 0, 1],
                [4, 2, 7],
                [3, 5, 5]])

# n = 3
# mat = np.random.randint(0, 8, size=[n, n])
main(mat)