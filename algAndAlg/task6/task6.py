# Задание 6: НВП-разложение

import sys
import math
import numpy as np
from numpy.linalg import inv
sys.setrecursionlimit(10000)

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

def Log2(x): 
    return (math.log10(x) / math.log10(2))
  
def is_power_of_two(n): 
    '''
    Is the matrix a power of two
    Input: n - shape of matrix
    Output: True or False
    '''
    return (math.ceil(Log2(n)) == math.floor(Log2(n)))

# def mat_to_z2(mat):
#     '''
#     Converting the matrix to Z9 format
#     Input: nxn matrix
#     Output: nxn matrix in Z9 format
#     '''  
#     return np.remainder(mat, 2)
def inv(a):
    n = a.shape[0]
    if n == 1:
        return a

    half_size = n // 2
    b = a[:half_size, -half_size:]
    c = inv(a[half_size:, -half_size:])
    a = inv(a[:half_size:, :half_size])
    b = strassen(strassen(a, b), c)

    res = np.zeros((n, n), dtype=np.int)
    res[:half_size, :half_size] = a 
    res[:half_size, half_size:] = b 
    res[half_size:, half_size:] = c 

    return res

def permutation(A, P):
    result = np.zeros((len(A), len(A[0])))
    indexes = []
    for i in range(len(A[0])):
        for j in range(len(A[0])):
            if P[i][j] == 1:
                indexes.append(j)

    for i in range(len(A[0])):
        for j in range(len(A)):
            ind = indexes[i]
            result[j,ind] = A[j, i]
    
    return result
    
def LUP(A, m, p):
    if m == 1:
        L = np.array([1])

        P = np.eye(p)
        for i in range(p):
            if A[0, i] == 1:
                ind = i
                break
            else:
                ind = 0
        P[0, 0], P[ind, ind], P[ind, 0], P[0, ind]=0, 0, 1, 1

        U = permutation(A, P) 

        return L, U, P
    else:
        split_m = m // 2
        B, C = A[:split_m , :p], A[split_m:, :p]
        L_1, U_1, P_1 = LUP(B, split_m, p)

        P_1_inv = P_1.T
        D = permutation(C, P_1_inv) 
        
        E, F = U_1[:, :split_m], D[:, :split_m]

        E_inv = inv(E) 
        FE_inv = strassen(F, E_inv) 
        FE_invU = strassen(FE_inv, U_1)
        
        # 9
        G = (D + FE_invU) % 2
        # 10
        G_s = G[:, -(p - split_m):]
       
        # 11
        L_2, U_2, P_2 = LUP(G_s, split_m, p - split_m)

        zero_down, zero_up = np.zeros((p - split_m, split_m)), np.zeros((split_m, p - split_m))
        I_split_m = np.eye(split_m)
        # 12
        P_3 = np.vstack((np.hstack((I_split_m, zero_up)), np.hstack((zero_down, P_2))))
        P_3_inv = P_3.T

        # 13
        H = permutation(U_1, P_3_inv) 

        # 14
        O_m = np.zeros((split_m, split_m))
        try:
            L_O = np.hstack((L_1, O_m))
            FE_L2 = np.hstack((FE_inv, L_2))
        except:
            L_1 = L_1[:, np.newaxis]
            L_2 = L_2[:, np.newaxis]
            L_O = np.hstack((L_1, O_m))
            FE_L2 = np.hstack((FE_inv, L_2))

        L = np.vstack((L_O, FE_L2)) % 2
        
        # 15
        U = np.vstack((H, np.hstack((O_m, U_2)))) % 2

        # 16 
        P = permutation(P_3, P_1) % 2

        return L, U, P
        

def main(matrix):

    if np.size(matrix) == 1:
        print(1)
        return

    power = matrix.shape[0]

    # check shape of matrix
    change = False
    if not is_power_of_two(matrix.shape[0]):
        matrix = add_eye(matrix)
        change = True
    
    L, U, P = LUP(matrix, matrix.shape[0], matrix.shape[0])
   
    def print_matrix(matrix, n=matrix.shape[0]):
        '''
        Print matrix
        Input: nxn matrix, optional - n=shape
        ''' 
        for line in matrix[:n, :n].astype(np.int32):
            print(" ".join(map(str, line)))
    
    if change:
        print_matrix(L, n=power)
        print_matrix(U, n=power)
        print_matrix(P, n=power)
    else:
        print_matrix(L)
        print_matrix(U)
        print_matrix(P)

matrix = np.loadtxt(sys.stdin, dtype='int')
# matrix = np.array([[1, 0, 1],
#                    [1, 1, 0],
#                    [1, 1, 1]])

main(matrix)